#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. Auftrag K0-R. Treiber fuer render_cycles.py (Blender Cycles, CPU).
Wiederverwendbar (K1): Fall-Ordner mit case_tNNNN.vtu + ergebnis.json (T_max_t_C, ziel_T_max_C, farbskala_max_C).
Aufruf: python3 bilder_cycles.py [--ordner sim/kuehlung/k0_zelle] [--faelle LFP_K1_L2 ...] [--samples 128] [--nur-standbilder]"""
import json, os, subprocess, shutil, argparse
import numpy as np, meshio
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, matplotlib.image as mpimg
HIER = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser(); ap.add_argument("--ordner", default=HIER); ap.add_argument("--faelle", nargs="*", default=["LFP_K1_L2", "NMC_K1_L2", "NMC_K2_L2"])
ap.add_argument("--samples", type=int, default=128); ap.add_argument("--samples-film", type=int, default=48); ap.add_argument("--nur-standbilder", action="store_true"); ap.add_argument("--nur-tafel", action="store_true")
A = ap.parse_args(); H = os.path.abspath(A.ordner); OUT = f"{H}/bilder"; os.makedirs(OUT, exist_ok=True)
SCR = os.environ.get("K0_ROH", "/tmp/claude-1003/-home-cae-hermes-batterie/7f4107cf-6c34-48d7-a591-998f97e12db1/scratchpad/k0c")
ERG = json.load(open(f"{H}/ergebnis.json")); ZT = ERG["ziel_T_max_C"]; VMAX = ERG["farbskala_max_C"]; VMIN = ERG["faelle"][A.faelle[0]]["meta"].get("T_kuehl", 25.0)
HINT = {"LFP_K1_L2": "LFP, Boden gekühlt (K1, Hauptfall), halbe Dicke weggeschnitten, echte Proportion", "NMC_K1_L2": "NMC 4680, Boden gekühlt (K1, Hauptfall), Viertel weggeschnitten",
        "NMC_K2_L2": "NMC 4680, Kühlband am Mantel (K2, Vergleich), Viertel weggeschnitten"}
SCHRITTE = list(range(0, 121, 3)); BILD_T = [0, 300, 600, 900, 1200]; HEX_FACES = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
def exportiere(fall):
    d = f"{H}/elmer/fall_{fall}"; m = meshio.read(f"{d}/case_t0001.vtu"); P = np.asarray(m.points) * 1e3
    hexc = [c.data for c in m.cells if c.type == "hexahedron"][0]; cen = P[hexc].mean(1); nmc = fall.startswith("NMC")
    keep = ~((cen[:, 0] > 0) & (cen[:, 1] < 0)) if nmc else cen[:, 2] <= P[:, 2].max() / 2
    fl = {}
    for h in hexc[keep]:
        for f in HEX_FACES: q = tuple(int(i) for i in h[list(f)]); fl.setdefault(tuple(sorted(q)), []).append(q)
    F0 = np.array([v[0] for v in fl.values() if len(v) == 1]); used = np.unique(F0); mp = -np.ones(len(P), int); mp[used] = np.arange(len(used)); Pu = P[used].copy()
    if not nmc: Pu = np.stack([Pu[:, 0], -Pu[:, 2], Pu[:, 1]], 1)   # LFP: Solver (x Laenge, y Hoehe, z Dicke) -> Blender (x, -z, y=Hoehe nach oben), echte Proportion, Drehung ohne Spiegelung
    Ts = []
    for s in SCHRITTE:
        f = f"{d}/case_t{s:04d}.vtu"
        if not os.path.exists(f): m0 = meshio.read(f"{d}/case_t0001.vtu"); T = np.full(len(P), VMIN)
        else: T = np.asarray(meshio.read(f).point_data["temperature"]).ravel()
        Ts.append(T[used])
    lut = plt.get_cmap("inferno")(np.linspace(0, 1, 256))[:, :3]; out = f"{SCR}/{fall}_export.npz"; os.makedirs(SCR, exist_ok=True)
    np.savez(out, P=Pu, F=mp[F0], T=np.array(Ts), steps=np.array(SCHRITTE), lut=lut); return out
def komponiere(fall, st, roh, lupe, ziel, anker):
    r = ERG["faelle"][fall]; T = r["T_max_t_C"][st]; img = mpimg.imread(roh); lfp = fall.startswith("LFP")
    fig = plt.figure(figsize=(11.5, 7.6)); ax = fig.add_axes([0.0, 0.34 if lfp else 0.10, 0.84, 0.56 if lfp else 0.80]); ax.imshow(img); ax.axis("off")
    if lfp and lupe:
        ax2 = fig.add_axes([0.02, 0.10, 0.34, 0.24]); ax2.imshow(mpimg.imread(lupe)); ax2.axis("off"); ax2.set_title("Lupe: Schnittfläche am Boden (Kühlplatte grau)", fontsize=8, loc="left")
        ra = anker["lupe_rect"]; h_, w_ = img.shape[:2]
        ax.add_patch(plt.Rectangle((ra[0] * w_, (1 - ra[3]) * h_), (ra[2] - ra[0]) * w_, (ra[3] - ra[1]) * h_, fill=False, ec="cyan", lw=1.2))
    cax = fig.add_axes([0.88, 0.16, 0.025, 0.68]); g = np.linspace(VMAX, VMIN, 256)[:, None]
    cax.imshow(g, aspect="auto", cmap="inferno", extent=[0, 1, VMIN, VMAX]); cax.set_xticks([]); cax.yaxis.tick_right(); cax.yaxis.set_label_position("right"); cax.set_ylabel("Temperatur (°C)")
    cax.axhline(ZT, color="cyan", lw=3); fig.text(0.86, 0.87, f"cyan = Vorgabe\n{ZT:g} °C (REQ-P09)", color="teal", ha="left", fontsize=8, fontweight="bold")
    fig.suptitle(f"{fall.replace('_', ' ')}: {HINT[fall]}", fontsize=11, y=0.975)
    fig.text(0.02, 0.93, f"t = {st * 10:d} s ({st * 10 / 60:.1f} min)   T_max = {T:.1f} °C   Schnellladen 10→80 % in 20 min (≈ 2,1 C)", fontsize=11, fontweight="bold")
    fig.text(0.40 if lfp else 0.02, 0.05 if lfp else 0.045, "Annahmen: Kühlmittel 25 °C, h = 500 W/(m²·K) (Kühlplatte bzw. Kühlband nur angedeutet).\nSchnittflächen zeigen das Innere; Farbskala in allen Bildern 25–54 °C. Cyan an der Skala = Vorgabe 45 °C.", fontsize=8, color="0.25")
    fig.text(0.5, 0.012, f"KI-generiert, Entwurf, nicht freigegeben. Quelle: Elmer-Rechnung sim/kuehlung/k0_zelle/elmer/fall_{fall}, Zahlen aus ergebnis.json; Blender Cycles (CPU) + matplotlib.", ha="center", fontsize=7, color="0.3")
    fig.savefig(ziel, dpi=100); plt.close(fig)
if __name__ == "__main__":
    BL = os.environ.get("BLENDER", "/usr/bin/blender")
    for fall in A.faelle:
        roh = f"{SCR}/{fall}"; fr = f"{SCR}/{fall}_frames"; os.makedirs(roh, exist_ok=True); os.makedirs(fr, exist_ok=True)
        if not A.nur_tafel:
            npz = exportiere(fall); var = "lfp" if fall.startswith("LFP") else "nmc"; ku = "band" if "K2" in fall else "platte"
            def lauf(schritte, samples):
                subprocess.run(["nice", "-n", "10", BL, "-b", "-P", f"{H}/render_cycles.py", "--", "--npz", npz, "--aus", roh, "--vmin", str(VMIN), "--vmax", str(VMAX), "--variante", var, "--kuehl", ku,
                                "--samples", str(samples), "--lupe", "1", "--schritte"] + [str(s) for s in schritte], check=True, capture_output=True)
            lauf([t // 10 for t in BILD_T], A.samples)
            if not A.nur_standbilder: lauf([s for s in SCHRITTE if s * 10 not in BILD_T], A.samples_film)
        anker = json.load(open(f"{roh}/anker.json"))
        for n, st in enumerate(SCHRITTE):
            if A.nur_standbilder and st * 10 not in BILD_T: continue
            lu = f"{roh}/roh_lupe_{st:04d}.png"; komponiere(fall, st, f"{roh}/roh_haupt_{st:04d}.png", lu if os.path.exists(lu) else None, f"{fr}/f_{n:04d}.png", anker)
        for t in BILD_T: shutil.copy(f"{fr}/f_{SCHRITTE.index(t // 10):04d}.png", f"{OUT}/cycles_{fall}_t{t:04d}.png")
        if not A.nur_standbilder:
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "8", "-i", f"{fr}/f_%04d.png", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2", f"{OUT}/cycles_{fall}.mp4"], check=True)
        print(fall, "ok")
    # Bildtafel: 3 Faelle x 5 Zeitpunkte, gemeinsame Skala
    fig, axs = plt.subplots(len(A.faelle), 5, figsize=(20, 4.6 * len(A.faelle)), squeeze=False)
    for i, fall in enumerate(A.faelle):
        for j, t in enumerate(BILD_T):
            axs[i][j].imshow(mpimg.imread(f"{OUT}/cycles_{fall}_t{t:04d}.png")); axs[i][j].axis("off")
    fig.text(0.5, 0.995, f"K0 Temperaturverlauf L2 (2,1 C), Zeilen: Fall, Spalten: t = 0, 300, 600, 900, 1200 s; gemeinsame Skala {VMIN:g}–{VMAX:g} °C, Vorgabe {ZT:g} °C (cyan an der Skala)", ha="center", va="top", fontsize=13)
    fig.text(0.5, 0.004, "KI-generiert, Entwurf, nicht freigegeben. Annahmen: Kühlmittel 25 °C, h = 500 W/(m²·K). Quelle: sim/kuehlung/k0_zelle/ergebnis.json, Blender Cycles (CPU).", ha="center", fontsize=9)
    plt.tight_layout(rect=[0, 0.015, 1, 0.97]); fig.savefig(f"{OUT}/tafel_L2.png", dpi=80); plt.close(fig)
