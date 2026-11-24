#!/usr/bin/env python3
"""E3 Bilder SPICE: Ausgleichskennlinie und Vorladung mit Zielband. KI-generiert (Claude Sonnet, 2026-11-24). Zahlen nur aus ergebnis_*.json; Zielbänder = Erwartung ERW-E3 (+Nachtrag 1)."""
import json, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
H = "/home/cae/hermes/batterie/sim/elektrik/e3_platine"; a = json.load(open(f"{H}/ergebnis_ausgleich.json")); v = json.load(open(f"{H}/ergebnis_vorladung.json"))
fig, ax = plt.subplots(1, 2, figsize=(12, 4.6))
for k, c, band in (("LFP", "tab:blue", (0.136, 0.155)), ("NMC", "tab:orange", (0.109, 0.128))):
    U = a[k]["kennlinie"]["U_V"]; I = [x * 1000 for x in a[k]["kennlinie"]["I_A"]]; ax[0].plot(U, I, color=c, label=f"{k} (R = {a[k]['R_parallel_Ohm']:g} Ohm)")
    ax[0].fill_between([a[k]["U_Unenn_V"], a[k]["U_Umax_V"]], band[0] * 1000, band[1] * 1000, color=c, alpha=0.15, label=f"Zielband {k} Erwartung (Strom bei U_nenn bis U_max)")
ax[0].set_xlabel("Zellspannung in V"); ax[0].set_ylabel("Ausgleichsstrom in mA"); ax[0].set_title("Ausgleichskennlinie"); ax[0].legend(fontsize=7); ax[0].grid(alpha=.3)
ax[1].plot([t * 1000 for t in v["t"]], v["i_A"], label="Strom in A"); ax[1].set_xlabel("Zeit in ms"); ax[1].set_ylabel("Strom in A"); ax[1].set_xlim(0, 600)
ax[1].axhline(9.1, color="gray", ls="--", label="Erwartung Spitze 9,1 A"); ax[1].axvline(300, color="green", ls=":", label="Erwartung t_95 = 300 ms")
ax2 = ax[1].twinx(); ax2.plot([t * 1000 for t in v["t"]], v["uC_V"], color="tab:red", label="u_C in V"); ax2.set_ylabel("Kondensatorspannung in V")
ax[1].set_title(f"Vorladung 912 V: Energie im Widerstand {v['E_Widerstand_J']:.1f} J (Grenze 450 J)"); ax[1].legend(fontsize=7, loc="center right"); ax[1].grid(alpha=.3)
fig.suptitle("E3 SPICE (ngspice). KI-generiert (Claude Sonnet, 2026-11-24), Entwurf", fontsize=10); fig.tight_layout(); fig.savefig(f"{H}/spice_ausgleich_vorladung.png", dpi=110)
