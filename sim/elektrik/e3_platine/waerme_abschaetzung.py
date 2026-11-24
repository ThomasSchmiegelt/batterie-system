#!/usr/bin/env python3
"""E3 Wärmeabschätzung (Erwartung 3), keine Thermikrechnung. KI-generiert (Claude Sonnet, 2026-11-24).
Eingaben: P_CMU aus ergebnis_ausgleich.json (P_CMU_18_Umax_W), Fläche 120 x 60 mm (ENT-166/167), h = 5 und 10 W/m2K, zwei Seiten (ERW-E3 Erwartung 3).
Formel: dT = P / (h * 2 * A); Umgebung 45 °C und Grenze 105 °C stehen in der Erwartung."""
import json, pathlib
H = pathlib.Path(__file__).resolve().parent; a = json.load(open(H / "ergebnis_ausgleich.json")); A = 0.120 * 0.060; out = {}
for v in a:
    P = a[v]["P_CMU_18_Umax_W"]; out[v] = dict(P_W=P, flaeche_m2=A, flussdichte_W_m2=P / A,
        dT_h5_K=P / (5 * 2 * A), dT_h10_K=P / (10 * 2 * A), T_h5_C=45 + P / (5 * 2 * A), T_h10_C=45 + P / (10 * 2 * A), grenze_C=105, ueberschritten_h10=45 + P / (10 * 2 * A) > 105, ueberschritten_h5=True)
    out[v]["ueberschritten_h5"] = out[v]["T_h5_C"] > 105
json.dump(out, open(H / "ergebnis_waerme.json", "w"), indent=1); print(json.dumps(out, indent=0)[:800])
