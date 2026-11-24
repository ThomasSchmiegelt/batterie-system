#!/usr/bin/env python3
"""E3 Bild der Platine (Ober- und Unterseite) mit Zielband = Umriss 120 x 60 mm. KI-generiert (Claude Sonnet, 2026-11-24), Entwurf.
Zahlen aus cmu_<V>_drc.json (/home/cae/cae_projekte/batterie/e3) und ergebnis_platine.json."""
import json, numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from PIL import Image
O = "/home/cae/cae_projekte/batterie/e3"; H = "/home/cae/hermes/batterie/sim/elektrik/e3_platine"
res = json.load(open(f"{H}/ergebnis_platine.json"))
def crop(p):
    im = Image.open(p).convert("RGBA"); a = np.array(im); m = a[:, :, 3] > 0; ys, xs = np.where(m); c = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1].copy(); c[c[:, :, 3] == 0] = 255; return c[:, :, :3]
for V in ("LFP", "NMC"):
    r = res[V]; fig, ax = plt.subplots(2, 1, figsize=(10, 10.2))
    for k, s in enumerate(("top", "bottom")):
        ax[k].imshow(crop(f"{O}/cmu_{V}_{s}.png")); ax[k].set_title(("Oberseite" if s == "top" else "Unterseite (nur Leiterbahnen und Vias)") + f", Umriss {r['laenge_mm']:g} x {r['breite_mm']:g} mm = Zielband (Passprüfung: {'passt' if r['passt'] else 'passt nicht'})", fontsize=11)
        ax[k].set_xticks([]); ax[k].set_yticks([])
        for sp in ax[k].spines.values(): sp.set_edgecolor("tab:red"); sp.set_linewidth(2.5)
    fig.suptitle(f"E3 CMU-Platine {V}: {r['teile']} Teile, 4 Lagen, DRC-Verstöße {r['drc_verstoesse']}, offene Verbindungen {r["drc_unverbunden"]} (geroutet)\nKI-generiert (Claude Sonnet, 2026-11-24), Entwurf", fontsize=11)
    fig.tight_layout(); fig.savefig(f"{H}/platine_{V}.png", dpi=110); plt.close(fig)
