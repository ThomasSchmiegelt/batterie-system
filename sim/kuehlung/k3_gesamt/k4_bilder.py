#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-21), Entwurf. Bild K4: Temperatur der Zellblock-Mittellage (Draufsicht) aus elmer/k4_0_t0001.vtu, Zielband 33-37 C (ERWARTUNG) und Grenze 45 C."""
import json, os, numpy as np, meshio
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
import sys
arg = lambda n, d: sys.argv[sys.argv.index(n)+1] if n in sys.argv else d
FALL, VAR = arg("--fall", "LFP_P0"), arg("--var", "V0"); H = os.path.dirname(os.path.abspath(__file__)); ED = f"{H}/elmer_{FALL}_{VAR}"; r = json.load(open(f"{ED}/ergebnis.json")); m = meshio.read(r["datei"]); T = m.point_data["temperature"].ravel(); X = m.points*1000
zi = json.load(open(f"{ED}/netzinfo.json"))["lagen_z_mm"]; zm = sum(zi[:2])+(90.0 if FALL.startswith("LFP") else 80.0)/2; s = np.abs(X[:, 2]-zm) < 8
fig, ax = plt.subplots(figsize=(10, 6)); sc = ax.tricontourf(X[s, 0], X[s, 1], T[s], levels=np.linspace(24, max(46, T.max()), 30), cmap="inferno"); cb = plt.colorbar(sc, label="T [C]")
ax.tricontour(X[s, 0], X[s, 1], T[s], levels=[33, 37, 45], colors=["c", "c", "w"], linewidths=[1, 1, 2])
ax.set_xlabel("x Laenge [mm]"); ax.set_ylabel("y Breite [mm]"); ax.set_title(f"K4 {FALL} {VAR}, Mittellage Zellblock. T_max {r['T_max_Zellblock_C']:.1f} C bei x {r['x_Tmax_mm']:.0f}, y {r['y_Tmax_mm']:.0f} mm; Zielband 33-37 C (cyan), Grenze 45 C (weiss)", fontsize=8)
fig.text(0.01, 0.01, "KI-generiert (Claude Sonnet), Entwurf, nicht freigegeben. Homogenisierter Zellblock, Aussenflaechen adiabat.", fontsize=7); fig.savefig(f"{H}/k4_temperatur_{FALL}_{VAR}.png", dpi=110, bbox_inches="tight")
