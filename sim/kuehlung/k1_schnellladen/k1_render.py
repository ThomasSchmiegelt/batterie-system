#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. Auftrag K1. Rendert den Endzustand je Variante mit ../k0_zelle/render_cycles.py (Blender Cycles, CPU, nice 10).
Auswahl (Regel): Fall, der beide Vorgaben (Spitzenwerte) erfuellt, sonst der Fall mit T_max-Spitze <= Grenze und kleinster dT-Spitze.
Aufruf: python3 k1_render.py [--samples 128]"""
import json, os, subprocess, sys, argparse
import numpy as np, meshio
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, matplotlib.image as mpimg
HIER = os.path.dirname(os.path.abspath(__file__)); K0 = os.path.join(os.path.dirname(HIER), "k0_zelle")
ap = argparse.ArgumentParser(); ap.add_argument("--samples", type=int, default=128); A = ap.parse_args()
ERG = json.load(open(f"{HIER}/ergebnis.json")); F = ERG["faelle"]; ZT, ZD = ERG["ziel_T_max_C"], ERG["ziel_dT_K"]
VMIN, VMAX = 25.0, 55.0
SCR = os.environ.get("K1_ROH", "/tmp/claude-1003/-home-cae-hermes-batterie/7f4107cf-6c34-48d7-a591-998f97e12db1/scratchpad/k1roh"); OUT = f"{HIER}/bilder"; os.makedirs(OUT, exist_ok=True); os.makedirs(SCR, exist_ok=True)
HEX_FACES = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
def waehle(v):
    c = {n: r for n, r in F.items() if r["meta"]["v"] == v}
    ok = [n for n, r in c.items() if r["T_max_Spitze_C"] <= ZT and r["dT_Spitze_K"] <= ZD]
    if ok: return min(ok, key=lambda n: c[n]["T_max_Spitze_C"]), "beide Vorgaben erfüllt (niedrigste T_max-Spitze unter den erfüllenden)"
    ok = [n for n, r in c.items() if r["T_max_Spitze_C"] <= ZT]
    return min(ok, key=lambda n: c[n]["dT_Spitze_K"]), f"keine erfüllt beide; bester = T_max ≤ {ZT:g} °C mit kleinster ΔT-Spitze"
def exportiere(fall):
    import glob
    d = f"{HIER}/elmer/fall_{fall}"; f_last = sorted(glob.glob(f"{d}/case_t*.vtu"))[-1]; m = meshio.read(f_last); P = np.asarray(m.points) * 1e3
    hexc = [c.data for c in m.cells if c.type == "hexahedron"][0]; cen = P[hexc].mean(1); nmc = fall.startswith("NMC")
    keep = ~((cen[:, 0] > 0) & (cen[:, 1] < 0)) if nmc else cen[:, 2] <= P[:, 2].max() / 2
    fl = {}
    for h in hexc[keep]:
        for f in HEX_FACES: q = tuple(int(i) for i in h[list(f)]); fl.setdefault(tuple(sorted(q)), []).append(q)
    F0 = np.array([v[0] for v in fl.values() if len(v) == 1]); used = np.unique(F0); mp = -np.ones(len(P), int); mp[used] = np.arange(len(used)); Pu = P[used].copy()
    if not nmc: Pu = np.stack([Pu[:, 0], -Pu[:, 2], Pu[:, 1]], 1)
    n = F[fall]["meta"]["n_schritte"]; T = np.asarray(m.point_data["temperature"]).ravel()[used]; T0 = np.full(len(used), F[fall]["meta"]["T_start"])
    lut = plt.get_cmap("inferno")(np.linspace(0, 1, 256))[:, :3]; out = f"{SCR}/{fall}_export.npz"
    np.savez(out, P=Pu, F=mp[F0], T=np.array([T0, T]), steps=np.array([0, n]), lut=lut); return out, n
BL = os.environ.get("BLENDER", "/usr/bin/blender")
for v in ("LFP", "NMC"):
    fall, grund = waehle(v); r = F[fall]; npz, n = exportiere(fall); roh = f"{SCR}/{fall}"; os.makedirs(roh, exist_ok=True)
    subprocess.run(["nice", "-n", "10", BL, "-b", "-P", f"{K0}/render_cycles.py", "--", "--npz", npz, "--aus", roh, "--vmin", str(VMIN), "--vmax", str(VMAX), "--variante", v.lower(), "--kuehl", "platte",
                    "--samples", str(A.samples), "--schritte", str(n)], check=True, capture_output=True)
    img = mpimg.imread(f"{roh}/roh_haupt_{n:04d}.png"); lfp = v == "LFP"
    fig = plt.figure(figsize=(11.5, 6.4)); ax = fig.add_axes([0.0, 0.14 if lfp else 0.10, 0.84, 0.70 if lfp else 0.78]); ax.imshow(img); ax.axis("off")
    cax = fig.add_axes([0.88, 0.16, 0.025, 0.62]); g = np.linspace(VMAX, VMIN, 256)[:, None]
    cax.imshow(g, aspect="auto", cmap="inferno", extent=[0, 1, VMIN, VMAX]); cax.set_xticks([]); cax.yaxis.tick_right(); cax.yaxis.set_label_position("right"); cax.set_ylabel("Temperatur (°C)")
    cax.axhline(ZT, color="cyan", lw=3); fig.text(0.86, 0.80, f"cyan = Vorgabe\n{ZT:g} °C (REQ-P09)", color="teal", ha="left", fontsize=8, fontweight="bold")
    st = r["meta"]["stufen"]; fig.suptitle(f"{fall.replace('_', ' ')} am Ladeende (t = {r['ladezeit_s']/60:.0f} min): T_max {r['T_max_Ende_C']:.1f} °C, ΔT Kern {r['dT_Ende_K']:.1f} K", fontsize=11.5, y=0.975)
    fig.text(0.02, 0.905, f"Auswahl: {grund}. Spitzen: T_max {r['T_max_Spitze_C']:.1f} °C, ΔT {r['dT_Spitze_K']:.1f} K (Vorgaben {ZT:g} °C / {ZD:g} K).", fontsize=8.5, color="0.2")
    kt = "beidseitig (Boden und Oben) gekühlt, h = %g" % r["meta"]["h"] if len(r["meta"]["raender"]) > 1 else "Boden gekühlt, h = %g" % r["meta"]["h"]
    fig.text(0.02, 0.05, f"Kühlung: {kt} W/(m²·K), Kühlmittel {r['meta']['T_kuehl']:g} °C, Start {r['meta']['T_start']:g} °C. Dargestellt ist nur die Bodenplatte (Kühlplatte grau); eine obere Platte ist nicht gezeichnet.\nSchnittflächen zeigen das Innere; Farbskala {VMIN:g}–{VMAX:g} °C.", fontsize=8, color="0.25")
    fig.text(0.5, 0.012, f"KI-generiert, Entwurf, nicht freigegeben. Quelle: sim/kuehlung/k1_schnellladen/elmer/fall_{fall}, Zahlen aus ergebnis.json; Blender Cycles (CPU) + matplotlib.", ha="center", fontsize=7, color="0.3")
    fig.savefig(f"{OUT}/render_{fall}_ende.png", dpi=100); plt.close(fig); print(v, fall, grund, flush=True)
