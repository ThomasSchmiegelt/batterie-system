#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-24), Entwurf. E3b Auswertung: lauf/*/res.json -> ergebnis.json, Bild e3b_temperatur.png (Temperaturfeld je Fall und Variante, Grenze 105 C)."""
import json, os, glob
import numpy as np
H = os.path.dirname(os.path.abspath(__file__)); R = {}
for f in sorted(glob.glob(f"{H}/lauf/*/res.json")):
    r = json.load(open(f)); R[r["lauf"]] = r
def g(k): return R[k]["T_max_C"] if k in R else None
out = dict(hinweis="KI-generiert (Claude Sonnet, 2026-11-24), Entwurf. T_max aus lauf/<Fall>_<Var>_<Netz>[_cu0]/res.json (Elmer, stationaer). Fall a Pad+Vias, b Pad ohne Vias, c ohne Pad. cu0 = Sensitivitaet Kupfer ohne Beitrag zur Querleitung (lambda_xy 0,8).",
           grenze_C=105, laeufe=R, vergleich={})
for v in ("LFP", "NMC"):
    for f in "abc":
        gr, fe = g(f"{f}_{v}_grob"), g(f"{f}_{v}_fein")
        out["vergleich"][f"{f}_{v}"] = dict(T_max_grob_C=gr, T_max_fein_C=fe, netzunterschied_K=(abs(gr-fe) if gr is not None and fe is not None else None), T_max_cu0_fein_C=g(f"{f}_{v}_fein_cu0"),
            Q_wand_W=R.get(f"{f}_{v}_fein", {}).get("Q_wand_elmer_W"), Q_oben_W=R.get(f"{f}_{v}_fein", {}).get("Q_oben_W"), Q_unten_luft_W=R.get(f"{f}_{v}_fein", {}).get("Q_unten_luft_W"))
P = json.load(open(f"{H}/../e3_platine/ergebnis_ausgleich.json")); out["P_CMU_W"] = {v: P[v]["P_CMU_18_Umax_W"] for v in ("LFP", "NMC")}
for v in ("LFP", "NMC"):
    for f in "ab":
        q = out["vergleich"][f"{f}_{v}"]["Q_wand_W"]
        if q is not None: out["vergleich"][f"{f}_{v}"]["Wandanteil_prozent"] = 100*q/out["P_CMU_W"][v]
json.dump(out, open(f"{H}/ergebnis.json", "w"), indent=1, default=float)
# ---- Bild
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt, meshio, matplotlib.tri as mt
from matplotlib.colors import TwoSlopeNorm
fig, ax = plt.subplots(2, 3, figsize=(15, 6.6), constrained_layout=True); titel = {"a": "(a) Pad + Vias", "b": "(b) Pad, ohne Vias", "c": "(c) ohne Pad (Prüffall)"}
vmin = 45; vmax = float(np.ceil(max(r["T_max_C"] for k_, r in R.items() if k_.endswith("fein"))/5)*5+5); lev = np.linspace(vmin, vmax, int((vmax-vmin)/2.5)+1)
for i, v in enumerate(("LFP", "NMC")):
    for j, f in enumerate("abc"):
        k = f"{f}_{v}_fein"; a = ax[i, j]
        if k not in R: a.set_axis_off(); continue
        vt = f"{H}/lauf/{k}/{R[k]['vtu']}"; m = meshio.read(vt); X = m.points*1000; T = m.point_data["temperature"].ravel()-273.15
        tri = [c.data for c in m.cells if c.type == "triangle"][0]; zt = X[:, 2].max(); sel = np.all(np.abs(X[tri][:, :, 2]-zt) < 1e-6, axis=1)
        tr = mt.Triangulation(X[:, 0], X[:, 1], tri[sel]); cf = a.tricontourf(tr, T, levels=lev, cmap="turbo", extend="neither")
        if T.max() >= 105: a.tricontour(tr, T, levels=[105], colors="k", linewidths=2, linestyles="--")
        ii = int(np.argmax(np.where(np.isclose(X[:, 2], zt), T, -1))); a.plot(X[ii, 0], X[ii, 1], "wo", mec="k", ms=6)
        a.set_aspect("equal"); a.set_title(f"{v} {titel[f]}\nT_max {R[k]['T_max_C']:.1f} °C, Grenze 105 °C", fontsize=10); a.set_xlabel("x in mm"); a.set_ylabel("y in mm")
cb = fig.colorbar(cf, ax=ax, orientation="vertical", fraction=0.025, pad=0.02); cb.set_label("Temperatur Oberseite in °C (Zielband: unter 105 °C; schwarze Linie = Grenze 105 °C)", fontsize=9); cb.ax.axhline(105, color="k", lw=2)
fig.suptitle("E3b: stationäre Temperatur der CMU-Platine (Elmer, feines Netz). Zulässig: unter 105 °C. Wand 45 °C, Vorderseite h = 5 W/m²K + Strahlung. KI-generiert, Entwurf", fontsize=10.5); fig.text(0.5, -0.01, "KI-generiert (Claude Sonnet, 2026-11-24), Entwurf, nicht freigegeben. Quelle: sim/elektrik/e3b_platine_waerme/ergebnis.json. Weißer Punkt = heißeste Stelle der Oberseite.", ha="center", fontsize=8)
fig.savefig(f"{H}/e3b_temperatur.png", dpi=130, bbox_inches="tight"); print("Bild fertig")
