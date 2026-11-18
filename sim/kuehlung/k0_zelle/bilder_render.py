#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. Auftrag K0 Ergaenzung (Autor 2026-11-17).
Gerenderte Temperaturbilder (Blender Workbench, CPU; pvbatch ist ohne paraview-Python-Modul nicht nutzbar) fuer L2 je Fall, Bildfolge und MP4 (ffmpeg). Faelle: LFP_K1_L2, NMC_K1_L2 (Hauptfaelle), NMC_K2_L2 (Vergleich).
Farbskala und Vorgabe 45 C aus ergebnis.json (ziel_T_max_C, farbskala_max_C)."""
import json, os, subprocess, shutil, sys
import numpy as np, meshio
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, matplotlib.image as mpimg
HIER = os.path.dirname(os.path.abspath(__file__)); OUT = f"{HIER}/bilder"; os.makedirs(OUT, exist_ok=True)
ERG = json.load(open(f"{HIER}/ergebnis.json")); ZT = ERG["ziel_T_max_C"]; VMAX = ERG["farbskala_max_C"]; VMIN = ERG["faelle"]["LFP_K1_L2"]["meta"]["T_kuehl"] if "T_kuehl" in ERG["faelle"]["LFP_K1_L2"]["meta"] else 25.0
SCR = os.environ.get("K0_ROH", "/tmp/claude-1003/-home-cae-hermes-batterie/7f4107cf-6c34-48d7-a591-998f97e12db1/scratchpad/k0_roh")
FAELLE = {"LFP_K1_L2": "LFP, Boden gekühlt (K1, Hauptfall), aufgeschnitten bis zur halben Dicke",
          "NMC_K1_L2": "NMC 4680, Boden gekühlt (K1, Hauptfall), Viertel weggeschnitten",
          "NMC_K2_L2": "NMC 4680, Kühlband am Mantel (K2, nur Vergleich), Viertel weggeschnitten"}
SCHRITTE = list(range(0, 121, 3)); BILD_T = [0, 300, 600, 900, 1200]
def t0(fall):
    d = f"{HIER}/elmer/fall_{fall}"; m = meshio.read(f"{d}/case_t0001.vtu")
    m.point_data["temperature"] = np.full_like(m.point_data["temperature"], VMIN); meshio.write(f"{d}/case_t0000.vtu", m)   # Anfangszustand = Starttemperatur (Initial Condition)
HEX_FACES = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
ZSTRECK_LFP = 4.0   # Dicke der LFP-Zelle nur fuer die Darstellung 4-fach ueberhoeht (14 mm waere sonst kaum sichtbar)
def exportiere(fall):
    """Oberflaechennetz der aufgeschnittenen Zelle + Knotentemperaturen je Schritt -> npz (fuer Blender)."""
    d = f"{HIER}/elmer/fall_{fall}"; m = meshio.read(f"{d}/case_t0000.vtu"); P = np.asarray(m.points) * 1e3
    hexc = [c.data for c in m.cells if c.type == "hexahedron"][0]; cen = P[hexc].mean(1); nmc = fall.startswith("NMC")
    keep = ~((cen[:, 0] > 0) & (cen[:, 1] < 0)) if nmc else cen[:, 2] <= P[:, 2].max() / 2
    fl = {}
    for h in hexc[keep]:
        for f in HEX_FACES:
            q = tuple(int(i) for i in h[list(f)]); fl.setdefault(tuple(sorted(q)), []).append(q)
    F0 = np.array([v[0] for v in fl.values() if len(v) == 1]); used = np.unique(F0); mp = -np.ones(len(P), int); mp[used] = np.arange(len(used))
    Pu = P[used].copy()
    if not nmc: Pu[:, 2] *= ZSTRECK_LFP
    Ts = []
    for s in SCHRITTE:
        mm = meshio.read(f"{d}/case_t{s:04d}.vtu"); Ts.append(np.asarray(mm.point_data["temperature"]).ravel()[used])
    lut = plt.get_cmap("inferno")(np.linspace(0, 1, 256))[:, :3]
    out = f"{SCR}/{fall}_export.npz"; np.savez(out, P=Pu, F=mp[F0], T=np.array(Ts), steps=np.array(SCHRITTE), nmc=nmc, lut=lut); return out
def kuehl_hinweis(fall): return "Kühlplatte unten (Boden)" if "K1" in fall else "Kühlband rechts hinten am Mantel (25 % Umfang)"
def komponiere(fall, st, roh, ziel):
    r = ERG["faelle"][fall]; i = st  # Schritt = Index
    T = r["T_max_t_C"][i] if i < len(r["T_max_t_C"]) else None
    img = mpimg.imread(roh); fig = plt.figure(figsize=(11.5, 7.6)); ax = fig.add_axes([0.0, 0.10, 0.84, 0.80]); ax.imshow(img); ax.axis("off")
    cax = fig.add_axes([0.88, 0.16, 0.025, 0.68]); g = np.linspace(VMAX, VMIN, 256)[:, None]
    cax.imshow(g, aspect="auto", cmap="inferno", extent=[0, 1, VMIN, VMAX]); cax.set_xticks([]); cax.yaxis.tick_right(); cax.yaxis.set_label_position("right"); cax.set_ylabel("Temperatur (°C)")
    cax.axhline(ZT, color="cyan", lw=3); cax.text(-0.4, ZT, f"Vorgabe {ZT:g} °C", color="teal", va="center", ha="right", fontsize=9, fontweight="bold", transform=cax.get_yaxis_transform())
    fig.suptitle(f"{fall.replace('_', ' ')}: {FAELLE[fall]}", fontsize=11, y=0.975)
    fig.text(0.02, 0.93, f"t = {st * 10:d} s ({st * 10 / 60:.1f} min)   T_max = {T:.1f} °C   Schnellladen 10→80 % in 20 min (≈ 2,1 C)", fontsize=11, fontweight="bold")
    fig.text(0.02, 0.045, f"Kühlung: {kuehl_hinweis(fall)}, Kühlmittel 25 °C. Cyan an der Farbskala = Vorgabe 45 °C (REQ-P09).\nSchnittflächen zeigen das Innere. Farbskala in allen Bildern gleich." + (" LFP-Dicke nur zur Darstellung 4-fach überhöht." if fall.startswith("LFP") else "") + "", fontsize=8, color="0.25")
    fig.text(0.5, 0.012, "KI-generiert, Entwurf, nicht freigegeben. Quelle: Elmer-Rechnung sim/kuehlung/k0_zelle/elmer/fall_%s, Zahlen aus ergebnis.json; Blender Workbench (CPU, pvbatch ohne Python-Modul nicht nutzbar) + matplotlib." % fall, ha="center", fontsize=7, color="0.3")
    fig.savefig(ziel, dpi=100); plt.close(fig)
if __name__ == "__main__":
    for fall in FAELLE:
        t0(fall); roh = f"{SCR}/{fall}"; os.makedirs(roh, exist_ok=True)
        npz = exportiere(fall)
        subprocess.run([os.environ.get("BLENDER", "/usr/bin/blender"), "-b", "-P", f"{HIER}/render_blender.py", "--", npz, roh, str(VMIN), str(VMAX)] + [str(s) for s in SCHRITTE], check=True, capture_output=True)
        fr = f"{SCR}/{fall}_frames"; os.makedirs(fr, exist_ok=True)
        for n, st in enumerate(SCHRITTE): komponiere(fall, st, f"{roh}/roh_{st:04d}.png", f"{fr}/f_{n:04d}.png")
        for t in BILD_T: shutil.copy(f"{fr}/f_{SCHRITTE.index(t // 10):04d}.png", f"{OUT}/render_{fall}_t{t:04d}s.png")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "8", "-i", f"{fr}/f_%04d.png", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2", f"{OUT}/verlauf_{fall}.mp4"], check=True)
        print(fall, "ok", len(SCHRITTE), "Frames")
