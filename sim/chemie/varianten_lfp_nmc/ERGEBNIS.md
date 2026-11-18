| Dok.-Nr. | ERG-C0b | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Ergebnis Variantenvergleich LFP-Blade / NMC-4680 mit Messwerten (800 V, 400 km, 1500 kg) | Ersteller | Claude Sonnet (KI) | Prüfer | Opus (Rohdaten) |

> **KI-generiert.** Entwurf, nicht freigegeben. Quelle aller Zahlen: `sim/chemie/varianten_lfp_nmc/ergebnis.json` (erzeugt von `varianten.py`, Eingaben `eingaben.json` und `../vergleich_lfp_nmc/eingaben.json`). Keine Deutung, die schreibt Opus.

## Rechenweg und Festlegungen
Wie C0 (Schritte 1–9). LFP: s = 250, p = 1, Ah aus Energie. NMC 4680: s = 217, Ah fest 23,125, p = ceil(E_brutto·1000/(s·U·Ah)), Packmasse = Zellen · 355 g / k, Fall B mit E_ist iteriert. Mitte des LFP-Zellbands = 185 Wh/kg (Bandmitte laut Auftrag); Hauptwert 160 (gemessen) zusätzlich. Packfaktor k 0,75 (Band 0,65–0,85). Bauraum: nötige Pack-Wh/L gegen Zelle-Wh/L × Volumennutzung; „knapp“ = innerhalb ±2 %.

## Tabelle je Variante und Fall (Mitte = LFP 185 Wh/kg bzw. NMC fest, k 0,75)

| Größe | LFP A | LFP B | NMC A | NMC B |
|---|---|---|---|---|
| Reihe s | 250 | 250 | 217 | 217 |
| parallel p | 1 | 1 | 4 | 5 |
| Zellen | 250 | 250 | 868 | 1085 |
| E_brutto Bedarf [kWh] | 73,9 | 89,9 | 73,9 | 86,6 |
| E_ist [kWh] | 73,9 | 89,9 | 74,3 | 92,8 |
| Ah je Zelle | 92,4 | 112,3 | 23,1 | 23,1 |
| Packmasse Mitte [kg] | 532,7 | 647,7 | 410,9 | 513,6 |
| Spanne über w und k [kg] | 414–711 | 480–931 | 363–474 | 453–593 |
| Gesamtmasse [kg] | 1500 | 2148 | 1500 | 2014 |
| Batterieanteil Mitte | 35,5 % | 30,2 % | 27,4 % | 25,5 % |
| Grenze 30 % [kg] | 450 | 644 | 450 | 604 |
| Anteil unter Grenze (Mitte) | nein | nein | ja | ja |
| Pack-Wh/L nötig | 203,9 | 247,9 | 203,9 | 238,8 |
| Bauraum | erfüllt | nicht erfüllt | erfüllt | erfüllt |
| Schritte Fall B | 0 | 6 | 0 | 3 |

Zyklenbedarf 1000: LFP erfüllt (Band [2500, 9000]), NMC unsicher (Band [400, 1200], keine 4680-Quelle).

## LFP nach Zellwert (k 0,75)

| w [Wh/kg] | Packmasse A [kg] | Anteil A | Ah A | E_brutto B [kWh] | Packmasse B [kg] | Anteil B | Ah B |
|---|---|---|---|---|---|---|---|
| 160 (gemessen, Hauptwert) | 615,9 | 41,1 % | 92,4 | 93,0 | 775,1 | 34,1 % | 116,3 |
| 185 (Mitte) | 532,7 | 35,5 % | 92,4 | 89,9 | 647,7 | 30,2 % | 112,3 |
| 210 (Hersteller) | 469,3 | 31,3 % | 92,4 | 87,6 | 556,3 | 27,1 % | 109,5 |

## NMC 4680 nach Packfaktor k (Zellwert fest)

| k | Packmasse A [kg] | p A | Anteil A | Packmasse B [kg] | p B | Anteil B |
|---|---|---|---|---|---|---|
| 0.65 | 474,1 | 4 | 31,6 % | 592,6 | 5 | 28,3 % |
| 0.75 | 410,9 | 4 | 27,4 % | 513,6 | 5 | 25,5 % |
| 0.85 | 362,5 | 4 | 24,2 % | 453,1 | 5 | 23,2 % |

## Bauraum je Volumennutzung

| Variante/Fall | nötig [Wh/L] | Volumennutzung | verfügbar [Wh/L] | Abweichung | Urteil |
|---|---|---|---|---|---|
| LFP A | 203,9 | 0,6 | 213,2 | 4,5 % | erfüllt |
| LFP B | 247,9 | 0,6 | 213,2 | -14,0 % | nicht erfüllt |
| NMC A | 203,9 | 0,4 | 257,3 | 26,2 % | erfüllt |
| NMC A | 203,9 | 0,6 | 386,0 | 89,3 % | erfüllt |
| NMC B | 238,8 | 0,4 | 257,3 | 7,8 % | erfüllt |
| NMC B | 238,8 | 0,6 | 386,0 | 61,6 % | erfüllt |

## Empfindlichkeit (Hub der Packmasse in kg, Mitte, je Größe einzeln)

| Variante/Fall | Hub k | Hub w | Hub a | stärkste |
|---|---|---|---|---|
| LFP A | 145 | 147 | – | w |
| LFP B | 216 | 219 | 113 | w |
| NMC A | 112 | – | – | k |
| NMC B | 139 | – | 0 | k |

## Abgleich mit ERWARTUNG.md (Punkt für Punkt)

1. Energie: Fall A 73,9 kWh für beide (erwartet 73,9): erfüllt. Fall B LFP 93,0 kWh bei 160 Wh/kg (89,9 bei 185, 87,6 bei 210), erwartet 92–95: erfüllt. Fall B NMC 86,6 kWh Bedarf (E_ist 92,8), erwartet 84–86: verfehlt.
2. Zellen: LFP 250s × 1p, 92,4 Ah (erwartet 250s, etwa 92 Ah): erfüllt. NMC 217s × 4p = 868 Zellen (erwartet 868): erfüllt; E_ist 74,3 kWh (erwartet etwa 74): erfüllt. Fall B p = 5 (erwartet 5 möglich): erfüllt.
3. Masse Fall A: LFP 616 kg bei 160 (erwartet etwa 615, Prüfband 560–670): erfüllt; LFP 469 kg bei 210 (erwartet etwa 470): erfüllt; NMC 411 kg (erwartet etwa 410, Prüfband 370–450): erfüllt. NMC leichter als LFP auch bei 210 (469 gegen 411 kg): erfüllt.
4. Anteil Fall A: LFP 41,1 % bei 160 (erwartet etwa 40 %, über 30 %): erfüllt; NMC 27,4 % (erwartet etwa 27 %, unter 30 %): erfüllt.
5. Bauraum: LFP A nötig 203,9 gegen 213,2 Wh/L verfügbar, Urteil „erfüllt“ (erwartet knapp nicht erfüllt oder gerade erfüllt): verfehlt. LFP B 247,9 gegen 213,2, „nicht erfüllt“ (erwartet nicht erfüllt): erfüllt. NMC verfügbar 257,3–386,0 Wh/L (erwartet 257–386), A „erfüllt“, B „erfüllt“ (erwartet erfüllt): erfüllt.
6. Zyklen: LFP erfüllt (erwartet erfüllt): erfüllt; NMC unsicher (erwartet unsicher): erfüllt.
7. Deutung vorab: kein Rechenergebnis, nicht abgeglichen (Opus).

**Verfehlte-Erwartung-Kriterien:** LFP-Packmasse A 560–670 kg: erfüllt; NMC 370–450 kg: erfüllt; NMC-Parallelzahl A = 4: erfüllt; Fall B konvergiert (LFP 6, NMC 3 Schritte): erfüllt.

## Lauf 3 (Bauraum 1,95 × 1,43 × 0,13 m, ENT-030)
KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. Volumen 362,5 L (Lauf 2: 354,9 L, `ergebnis_lauf2.json`). Grundlage wie `bauraum.png`: Hauptwert (LFP 160 Wh/kg, k 0,75). Massen und Energien sind unverändert (Bauraum geht nicht ein): LFP A 615,9 kg (Lauf 2 615,9), NMC A 410,9 kg (Lauf 2 410,9).

| Größe | Lauf 2 | Lauf 3 |
|---|---|---|
| LFP A: nötig / verfügbar [Wh/L], Abweichung, Urteil | 208,3 / 213,2, +2.3 %, erfüllt | 203,9 / 213,2, +4.5 %, erfüllt |
| LFP B: nötig / verfügbar [Wh/L], Abweichung, Urteil | 262,1 / 213,2, -18.7 %, nicht erfüllt | 256,6 / 213,2, -16.9 %, nicht erfüllt |
| NMC A: nötig / verfügbar [Wh/L], Abweichung, Urteil | 208,3 / 257,3, +23.6 %, erfüllt | 203,9 / 257,3, +26.2 %, erfüllt |
| NMC B: nötig / verfügbar [Wh/L], Abweichung, Urteil | 243,9 / 257,3, +5.5 %, erfüllt | 238,8 / 257,3, +7.8 %, erfüllt |

Abgleich mit dem Nachtrag in `ERWARTUNG.md` (Lauf 3: nötig Fall A ≈ 204 und LFP B ≈ 257 Wh/L, LFP A erfüllt +4,6 %, LFP B nicht, NMC erfüllt, Massen unverändert):
- nötig Fall A 203,9 Wh/L (erwartet ≈ 204): erfüllt
- LFP A erfüllt, +4.5 % (erwartet erfüllt, +4,6 %; Rundung der Erwartung): erfüllt
- LFP B nicht erfüllt (erwartet nicht erfüllt): erfüllt; nötig 256,6 Wh/L (erwartet ≈ 257): erfüllt
- NMC A erfüllt, NMC B erfüllt (erwartet erfüllt): erfüllt
- Massen unverändert (Hauptwert LFP A, NMC A): erfüllt
Verfehlt-Kriterium des Nachtrags (Masse ändert sich oder LFP A nicht erfüllt): nicht eingetreten, wenn alle Punkte oben „erfüllt“ sind.

---
*KI-generiert (Claude Sonnet), Entwurf, nicht vom Menschen freigegeben.*
