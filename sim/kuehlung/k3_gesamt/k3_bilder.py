#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-21), Entwurf. Bilder und Film K3 aus lauf_umlenk_re{RE}/feld.npz und ergebnis.json (Zahlen nur aus Ergebnisdateien)."""
import json, os, subprocess, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
import sys
RE = sys.argv[1] if len(sys.argv) > 1 else "200"; H = os.path.dirname(os.path.abspath(__file__)); E = json.load(open(f"{H}/eingaben.json"))
d = np.load(f"{H}/lauf_umlenk_re{RE}/feld.npz"); ux, uz, T, fl = d["ux"], d["uz"], d["T"], d["fl"]; U = json.load(open(f"{H}/lauf_umlenk_re{RE}/ergebnis.json"))
Ny = ux.shape[1]; ym = Ny//2; zpm = U["zellen_je_mm"]
def schnitt(y):
    v = np.sqrt(ux[:, y, :]**2+uz[:, y, :]**2); v = np.where(fl[:, y, :], v, np.nan); return v
v = schnitt(ym); ext = [0, v.shape[1]/zpm, 0, v.shape[0]/zpm]
fig, ax = plt.subplots(figsize=(11, 4)); im = ax.imshow(v, origin="lower", extent=ext, cmap="viridis"); plt.colorbar(im, label="|u| Gitter-Einheiten")
vm = np.nanmean(v[int(v.shape[0]*0.45):]); ax.contour(np.linspace(0, ext[1], v.shape[1]), np.linspace(0, ext[3], v.shape[0]), np.nan_to_num(v, nan=9) < 0.1*vm, levels=[0.5], colors="r", linewidths=0.6)
ax.set_xlabel("x quer zur Bahn [mm]"); ax.set_ylabel("z entlang der Bahn [mm]")
ax.set_title(f"K3 Umlenkung, Geschwindigkeit in Kanalmitte. Rot: Totzone (< 10 % des Mittels), Anteil Kammer {100*U['totzone_anteil_kammer']:.1f} %, Ziel < 5 % der Kanalflaeche (ERWARTUNG)", fontsize=8)
fig.text(0.01, 0.01, "KI-generiert (Claude Sonnet), Entwurf, nicht freigegeben", fontsize=7); fig.savefig(f"{H}/k3_umlenk_u_re{RE}.png", dpi=110, bbox_inches="tight"); plt.close(fig)
Tm = np.where(fl[:, ym, :], T[:, ym, :], np.nan); fig, ax = plt.subplots(figsize=(11, 4)); im = ax.imshow(Tm, origin="lower", extent=ext, cmap="inferno"); plt.colorbar(im, label="T Gitter-Einheiten")
ax.set_xlabel("x [mm]"); ax.set_ylabel("z [mm]"); ax.set_title(f"K3 Fluidtemperatur (Gitter-Einheit), Bilanz Soll am Austritt {U['T_aus_bilanz_lb']:.3g}, Abweichung Ziel +-5 %", fontsize=8)
fig.text(0.01, 0.01, "KI-generiert (Claude Sonnet), Entwurf, nicht freigegeben", fontsize=7); fig.savefig(f"{H}/k3_umlenk_T_re{RE}.png", dpi=110, bbox_inches="tight"); plt.close(fig)
if os.path.exists(f"{H}/ergebnis.json"):
    r = json.load(open(f"{H}/ergebnis.json")); fig, ax = plt.subplots(1, 2, figsize=(8, 3.5))
    for a, (k, t) in zip(ax, (("dp_abw_prozent", "Druckverlust Platte"), ("h_abw_prozent", "h Teilkanal"))):
        a.axhspan(-30, 30, color="g", alpha=0.25, label="Zielband +-30 % (ERWARTUNG)"); a.bar([0], [r[k]], color="C0"); a.set_title(t+" FluidX3D gegen K2b [%]", fontsize=9); a.set_xticks([]); a.legend(fontsize=7)
    fig.text(0.01, 0.01, "KI-generiert (Claude Sonnet), Entwurf", fontsize=7); fig.savefig(f"{H}/k3_vergleich.png", dpi=110, bbox_inches="tight"); plt.close(fig)
os.makedirs(f"{H}/film", exist_ok=True)
for k, y in enumerate(range(2, Ny-2)):     # Film: Schnitte ueber die Kanalhoehe (Endfeld; kein Zeitverlauf gespeichert)
    fig, ax = plt.subplots(figsize=(10, 3.6)); ax.imshow(schnitt(y), origin="lower", extent=ext, cmap="viridis"); ax.set_title(f"K3 |u|, Schnitt Hoehe {y/zpm:.1f} mm (KI-generiert, Entwurf)", fontsize=8); fig.savefig(f"{H}/film/f{k:03d}.png", dpi=80); plt.close(fig)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", f"{H}/film/f%03d.png", "-pix_fmt", "yuv420p", f"{H}/k3_film.mp4"], check=True)
