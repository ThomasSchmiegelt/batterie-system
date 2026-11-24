#!/usr/bin/env python3
"""E3c Bild der BMS-Platine (Ober-/Unterseite) mit Zielband = Umriss 160 x 100 mm und der Sperrzone HV/NV (>= 10 mm). KI-generiert (Claude Sonnet, 2026-11-24), Entwurf.
Zahlen aus ergebnis_platine.json (bms_ergebnis.py)."""
import json, numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image
O = "/home/cae/cae_projekte/batterie/e3c"; H = "/home/cae/hermes/batterie/sim/elektrik/e3c_bms_platine"; r = json.load(open(f"{H}/ergebnis_platine.json")); sz = r["sperrzone"]
def crop(p):
    im = Image.open(p).convert("RGBA"); a = np.array(im); m = a[:, :, 3] > 0; ys, xs = np.where(m); c = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1].copy(); c[c[:, :, 3] == 0] = 255; return c[:, :, :3]
fig, ax = plt.subplots(2, 1, figsize=(11, 13))
for k, s in enumerate(("top", "bottom")):
    im = crop(f"{O}/bms_{s}.png"); im = im[:, ::-1] if s == "bottom" else im; h, w = im.shape[:2]; ax[k].imshow(im, extent=(0, r["laenge_mm"], r["breite_mm"], 0))
    ax[k].set_title(("Oberseite" if s == "top" else "Unterseite, gespiegelt (Blick durch die Platine; Bahnen, Vias, Massefläche)") + f", Umriss {r['laenge_mm']:g} x {r['breite_mm']:g} mm = Zielband", fontsize=11)
    ax[k].add_patch(Rectangle((sz["x_mm"][0], 0), sz["breite_mm"], r["breite_mm"], fill=True, fc=(1, 0.1, 0.1, 0.18), ec="red", lw=1.6, hatch="//"))
    ax[k].annotate("", xy=(sz["x_mm"][0], 4), xytext=(sz["x_mm"][1], 4), arrowprops=dict(arrowstyle="<->", color="darkred", lw=1.5))
    ax[k].annotate(f"Sperrzone {sz['breite_mm']:g} mm\n(Kriechstrecke, gemessen {sz['abstand_nv_hv_kupfer_mm']:g} mm)", xy=(sz["x_mm"][1], 25), xytext=(129, 25), ha="center", va="center", fontsize=8.5, color="darkred", arrowprops=dict(arrowstyle="->", color="darkred"), bbox=dict(fc="white", ec="darkred", alpha=0.9)); (lambda *a, **kw: None)(sum(sz["x_mm"]) / 2, 24, f"Sperrzone {sz['breite_mm']:g} mm\n(Kriechstrecke, gemessen {sz['abstand_nv_hv_kupfer_mm']:g} mm)", ha="center", va="center", fontsize=8.5, color="darkred", bbox=dict(fc="white", ec="darkred", alpha=0.9))
    ax[k].text(sz["x_mm"][0] - 2, r["breite_mm"] - 3, "Niedervolt (NV)", ha="right", fontsize=10, color="navy", bbox=dict(fc="white", ec="navy", alpha=0.85))
    ax[k].text(sz["x_mm"][1] + 2, r["breite_mm"] - 3, "Hochvolt-Seite (HV)", ha="left", fontsize=10, color="darkred", bbox=dict(fc="white", ec="darkred", alpha=0.85))
    ax[k].set_xlim(0, r["laenge_mm"]); ax[k].set_ylim(r["breite_mm"], 0); ax[k].set_xlabel("mm"); ax[k].set_ylabel("mm")
    for sp in ax[k].spines.values(): sp.set_edgecolor("tab:red"); sp.set_linewidth(2.5)
fig.suptitle(f"E3c BMS-Platine BT-311: {r['teile']} Teile, {r['lagen']} Lagen, DRC-Verstöße {r['drc_verstoesse']}, offene Verbindungen {r['drc_unverbunden']} (geroutet)\n"
             f"Nur {len(sz['bruecken'])} Teile überbrücken die Sperrzone (2 Übertrager, 2 digitale Isolatoren). KI-generiert (Claude Sonnet, 2026-11-24), Entwurf", fontsize=10.5)
fig.text(0.5, 0.012, "Lesehilfe: Die rot gestrichelte Fläche ist die Sperrzone: kein Kupfer, keine Bahn, kein Via. Links liegt die Niedervoltseite (Rechner, CAN, Schützansteuerung),\n"
         "rechts die Hochvoltseite (Shunt, Daisy-Chain, Sekundärpfad). Die vier grauen Blöcke in der Zone sind die einzigen Bauteile, die darüber hinwegreichen (verstärkte Isolation).\n"
         "Rote Umrandung = Zielband (Umriss 160 x 100 mm aus ENT-188/189). Die Unterseite ist so gespiegelt, dass links und rechts wie oben liegen.", ha="center", fontsize=8.3)
fig.tight_layout(rect=(0, 0.04, 1, 0.96)); fig.savefig(f"{H}/platine_bms.png", dpi=110); plt.close(fig)
