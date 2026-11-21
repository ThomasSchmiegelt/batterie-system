#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-19), Entwurf. Bild K2b aus ergebnis_k2b.json."""
import json
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import kuehlplatte as K
O = json.load(open(f"{K.H}/ergebnis_k2b.json")); Q = K.E["k2b"]
col = {2: "#1b6ca8", 4: "#e08a00", 6: "#2a9d4b", 8: "#8e44ad"}
fig, ax = plt.subplots(1, 2, figsize=(15, 6.5))
for a, fn in zip(ax, Q["V_pack_L_min"]):
    X = [x for x in O["faelle"] if x["fall"] == fn]
    for n in Q["n_bahnen"]:
        S = [x for x in X if x["n_bahnen"] == n]
        a.plot([x["dp_bar"] for x in S], [x["U_gesamt"] for x in S], "o", color=col[n], ms=5, label=f"n = {n} Bahnen")
    a.axhspan(Q["U_ziel"], 700, xmin=0, xmax=1, color="#2a9d4b", alpha=.12); a.axhline(Q["U_ziel"], color="#2a9d4b")
    a.axvspan(1e-4, Q["dp_ziel_bar"], color="#2a9d4b", alpha=.12); a.axvline(Q["dp_ziel_bar"], color="#2a9d4b")
    a.text(2e-4, Q["U_ziel"]+8, f"Zielband U >= {Q['U_ziel']} W/(m2K) und dp <= {Q['dp_ziel_bar']} bar", color="#1d6b34", fontsize=9)
    ok = [x for x in X if x["ok_U"] and x["ok_dp"]]
    if ok:
        b = min(ok, key=lambda x: x["dp_bar"])
        a.plot(b["dp_bar"], b["U_gesamt"], "o", mfc="none", mec="k", ms=15, mew=2)
        a.annotate(f"Vorschlag: n={b['n_bahnen']}, w={b['breite_mm']} mm {b['fuehrung']}", (b["dp_bar"], b["U_gesamt"]), xytext=(15, -45), textcoords="offset points", arrowprops=dict(arrowstyle="->"), fontsize=9)
    a.set_xscale("log"); a.set_xlim(1e-4, 30); a.set_xlabel("Druckverlust je Platte [bar], log"); a.set_ylabel("Gesamtwaermedurchgang U [W/(m2K)]"); a.set_title(f"{fn}: {Q['V_pack_L_min'][fn]} L/min je Pack"); a.legend(loc="lower left", fontsize=8)
fig.suptitle("K2b Blechplatte 1/4/1 mm mit Maeander: U ueber dp (jeder Punkt eine Variante)", fontsize=11)
fig.text(0.5, 0.005, "KI-generiert (Claude Sonnet, 2026-11-19), Entwurf. Quelle: sim/kuehlung/k2_kuehlplatte/ergebnis_k2b.json", ha="center", fontsize=8)
fig.tight_layout(rect=(0, .02, 1, .96)); fig.savefig(f"{K.H}/k2b_U_dp.png", dpi=130)
