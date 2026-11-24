#!/usr/bin/env python3
"""E3d Bild. KI-generiert (Claude Sonnet, 2026-11-24), Entwurf. Liest ergebnis.json, schreibt e3d_fmeda.png."""
import json, pathlib, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
H = pathlib.Path(__file__).resolve().parent; E = json.load(open(H / "ergebnis.json")); Z = E["ziel"]
fig = plt.figure(figsize=(14, 7.5)); gs = fig.add_gridspec(2, 2, width_ratios=[1, 1.1], hspace=.45, wspace=.95)
col = {"LFP": "#1b6ca8", "NMC": "#d9822b"}; OK, NOK = "#2e7d32", "#c62828"
for i, m in enumerate(("SPFM", "LFM")):
    ax = fig.add_subplot(gs[i, 0])
    for j, sg in enumerate(Z):
        for k, v in enumerate(("LFP", "NMC")):
            x = j + (k - .5) * .32; y = E["cmu"][v][sg][m] * 100
            ax.bar(x, y, .3, color=col[v], label=v if j == 0 else None); ax.text(x, y + .25, f"{y:.1f}", ha="center", fontsize=9)
        t = Z[sg][m] * 100; ax.hlines(t, j - .4, j + .4, color=OK, lw=3); ax.fill_between([j - .4, j + .4], t, 100.5, color=OK, alpha=.12, zorder=0)
        ax.text(j + .41, t, f"Ziel ASIL {Z[sg]['ASIL']}\n{t:.0f} %", va="center", fontsize=8, color=OK, bbox=dict(fc="white", ec="none", pad=1))
    ax.set_xticks(range(2)); ax.set_xticklabels([f"{sg} (ASIL {Z[sg]['ASIL']})" for sg in Z]); ax.set_xlim(-.5, 1.9)
    ax.set_ylim(80, 100.5); ax.set_ylabel(f"{m} in %  (Achse beginnt bei 80 %)"); ax.set_title(f"{m} je CMU"); ax.legend(loc="lower left", fontsize=8)
for i, sg in enumerate(Z):
    ax = fig.add_subplot(gs[i, 1]); t = E["top"]["LFP"][sg][::-1]
    ax.barh([d["posten"] + f" (x{d['anzahl_Teile']})" for d in t], [d["SPF_RF_FIT"] for d in t], color="#c62828", label="Restfehler (SPF/RF)")
    ax.barh([d["posten"] + f" (x{d['anzahl_Teile']})" for d in t], [d["MPF_latent_FIT"] for d in t], left=[d["SPF_RF_FIT"] for d in t], color="#6a4c93", label="latenter Zweitfehler (MPF)")
    ax.set_xlabel("Beitrag in FIT je CMU"); ax.set_title(f"Top-5 Beitraege {sg} (LFP = NMC)"); ax.legend(fontsize=8, loc="lower right"); ax.tick_params(axis="y", labelsize=8)
    c = E["cmu"]["LFP"][sg]; ax.set_xlim(0, max(d["SPF_RF_FIT"] + d["MPF_latent_FIT"] for d in t) * 1.25); ax.text(.98, .55, f"Summe Rest {c['lambda_SPF_RF_FIT']:.2f} FIT von {c['lambda_SR_FIT']:.1f} FIT", transform=ax.transAxes, ha="right", fontsize=8)
v = E["verfehlt"]
fig.suptitle("E3d grobe FMEDA CMU-Platine: " + ("Ziel verfehlt: " + ", ".join(v) if v else "alle Ziele erreicht") + "  (Annahmen Opus, ERW-E3d)", fontsize=12, color=NOK if v else OK)
fig.text(.01, .01, "KI-generiert (Claude Sonnet, 2026-11-24), Entwurf. Quelle: sim/elektrik/e3d_fmeda/ergebnis.json", fontsize=8)
fig.savefig(H / "e3d_fmeda.png", dpi=130, bbox_inches="tight")
