#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-23), Entwurf. Vergleich K4 V0, V3, V4, V4p (V4p = V4 ohne Gegenlauf, gebautes CAD G5.9). Zahlen aus ../k3_gesamt/elmer_*/ergebnis.json."""
import json, os
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
H = os.path.dirname(os.path.abspath(__file__)); K = f"{H}/../k3_gesamt"; VS = ("V0", "V3", "V4", "V4p")
FS = (("LFP_P0", "LFP Schnellladen"), ("NMC_P4", "NMC 30 min"))
D = {(f, v): json.load(open(f"{K}/elmer_{f}_{v}/ergebnis.json")) for f, _ in FS for v in VS}
fig, ax = plt.subplots(1, 2, figsize=(11, 5.2))
for a, (key, tit, unit) in zip(ax, (("dT_Zellblock_K", "Temperaturunterschied im Zellblock ΔT", "K"), ("T_max_Zellblock_C", "Höchsttemperatur T_max", "°C"))):
    w = 0.38
    for i, (f, n) in enumerate(FS):
        v = [D[(f, x)][key] for x in VS]; b = a.bar([j + (i - 0.5) * w for j in range(4)], v, w, label=n, color=("tab:blue", "tab:orange")[i])
        for r, y in zip(b, v): a.text(r.get_x() + r.get_width() / 2, y, f"{y:.1f}", ha="center", va="bottom", fontsize=8)
    a.set_xticks(range(4)); a.set_xticklabels(["V0 Mäander", "V3 Mäander\n×2 Gegenlauf", "V4 k=2 ×3\nGegenlauf", "V4p k=2 ×3\nohne Gegenlauf (gebaut)"], fontsize=8)
    a.set_title(tit, fontsize=10); a.set_ylabel(unit); a.grid(alpha=0.3, axis="y")
    if key == "dT_Zellblock_K": a.axhline(5, color="green", ls="--"); a.text(3.45, 5.3, "Zielband ΔT ≤ 5 K (Annahme Opus)", color="green", fontsize=8, ha="right")
    a.legend(fontsize=8)
fig.suptitle(f"K4 Vergleich: V4p (gebaut) LFP ΔT {D[('LFP_P0','V4p')]['dT_Zellblock_K']:.1f} K, T_max {D[('LFP_P0','V4p')]['T_max_Zellblock_C']:.1f} °C; NMC ΔT {D[('NMC_P4','V4p')]['dT_Zellblock_K']:.1f} K", fontsize=10)
fig.text(0.01, 0.045, "Lesehilfe: Niedriger ist besser. Grün gestrichelt = Ziel für den Temperaturunterschied. V4p ist die Kühlplatte, wie sie im CAD G5.9 steht (Ober- und Unterplatte gleichsinnig).", fontsize=7)
fig.text(0.01, 0.01, "KI-generiert (Claude Sonnet), Entwurf, nicht freigegeben. Quelle: sim/kuehlung/k3_gesamt/elmer_*/ergebnis.json (Elmer K4).", fontsize=7)
fig.tight_layout(rect=(0, 0.07, 1, 0.95)); fig.savefig(f"{H}/k4_vergleich_V0_V3_V4_V4p.png", dpi=110)
