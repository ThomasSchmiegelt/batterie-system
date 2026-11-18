#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-18), Entwurf. Auftrag X1b. Energieverlust je w aus den Pack-Formeln von cad/pack/pack.py (nur nachgebildet, CAD nicht neu gerechnet).
Annahmen laut ERWARTUNG.md (ERW-X1b): Breite fest 1430, Knautschzone w je Seite geht von der Zellbreite ab. LFP: Reserve 8 mm, Rest kuerzt die Zelle (Energie proportional zur Zelllaenge: Annahme). NMC: Reihen/Zellen je Feld wie pack.py."""
import json, math
from pathlib import Path
R = Path(__file__).resolve().parents[3]; D = Path(__file__).parent
out = {}
for v in ("LFP", "NMC"):
    J = json.load(open(R / f"cad/pack/entwurf/parameter_{v}.json")); A = {k: x["wert"] for k, x in J["A"].items()}; P = J["parameter"]
    B = float(P["BT-000"]["bauraum_breite_mm"]["wert"]); L = float(P["BT-000"]["bauraum_laenge_mm"]["wert"]); rand = A["A_rand_mm"]; res = {}
    for w in (0, 15, 20, 30):
        Bi = B - 2 * (rand + w)
        if v == "LFP":
            Lc = float(P["BT-100"]["laenge_mm"]["wert"]); frei = B - 2 * rand - 2 * Lc   # Reserve bei w=0
            Lneu = min(Lc, (Bi) / 2)
            res[w] = {"Innenbreite_mm": Bi, "Reserve_w0_mm": frei, "Zelllaenge_neu_mm": Lneu, "Energieverlust_proz": round((1 - Lneu / Lc) * 100, 2)}
        else:
            d = float(P["BT-100"]["durchmesser_mm"]["wert"]); ab = A["A_zellabstand_NMC_mm"]; t = d + ab; rp = t * math.sqrt(3) / 2; nq = int(A["A_quertraeger_anzahl"]); qb = A["A_quertraeger_breite_mm"]; sp = A["A_quertraeger_spiel_mm"]
            feld = (L - 2 * rand - nq * qb - nq * 2 * sp) / (nq + 1); ng = int((Bi - d) // t) + 1; nu = int((Bi - d - t / 2) // t) + 1; rows = int((feld - d) // rp) + 1
            je = int(A["A_zellzahl_NMC"]) // (nq + 1); cap = sum(ng if r % 2 == 0 else nu for r in range(rows)); need = 0; c = 0
            while c < je and need < rows: c += ng if need % 2 == 0 else nu; need += 1
            res[w] = {"Innenbreite_mm": Bi, "Zellen_gerade_Reihe": ng, "Zellen_ungerade_Reihe": nu, "Reihen_verfuegbar": rows, "Reihen_noetig": need, "Zellen_je_Feld_soll": je, "Kapazitaet_Feld": cap, "Zellen_je_Feld_ist": min(je, cap), "Energieverlust_proz": round((1 - min(je, cap) / je) * 100, 2)}
    out[v] = res
json.dump({"hinweis": "KI-generiert, Entwurf. Nachbildung der Formeln aus cad/pack/pack.py, kein CAD-Lauf.", "ergebnis": out}, open(D / "energieverlust.json", "w"), indent=1)
for v in out:
    for w, r in out[v].items(): print(v, w, r)
