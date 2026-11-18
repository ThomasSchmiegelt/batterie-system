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
| Pack-Wh/L nötig | 213,7 | 259,9 | 213,7 | 250,3 |
| Bauraum | knapp (±2 %) | nicht erfüllt | erfüllt | erfüllt |
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
| LFP A | 213,7 | 0,6 | 213,2 | -0,3 % | knapp (±2 %) |
| LFP B | 259,9 | 0,6 | 213,2 | -18,0 % | nicht erfüllt |
| NMC A | 213,7 | 0,4 | 257,3 | 20,4 % | erfüllt |
| NMC A | 213,7 | 0,6 | 386,0 | 80,6 % | erfüllt |
| NMC B | 250,3 | 0,4 | 257,3 | 2,8 % | erfüllt |
| NMC B | 250,3 | 0,6 | 386,0 | 54,2 % | erfüllt |

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
5. Bauraum: LFP A nötig 213,7 gegen 213,2 Wh/L verfügbar, Urteil „knapp (±2 %)“ (erwartet knapp nicht erfüllt oder gerade erfüllt): erfüllt. LFP B 259,9 gegen 213,2, „nicht erfüllt“ (erwartet nicht erfüllt): erfüllt. NMC verfügbar 257,3–386,0 Wh/L (erwartet 257–386), A „erfüllt“, B „erfüllt“ (erwartet erfüllt): erfüllt.
6. Zyklen: LFP erfüllt (erwartet erfüllt): erfüllt; NMC unsicher (erwartet unsicher): erfüllt.
7. Deutung vorab: kein Rechenergebnis, nicht abgeglichen (Opus).

**Verfehlte-Erwartung-Kriterien:** LFP-Packmasse A 560–670 kg: erfüllt; NMC 370–450 kg: erfüllt; NMC-Parallelzahl A = 4: erfüllt; Fall B konvergiert (LFP 6, NMC 3 Schritte): erfüllt.

---
*KI-generiert (Claude Sonnet), Entwurf, nicht vom Menschen freigegeben.*
