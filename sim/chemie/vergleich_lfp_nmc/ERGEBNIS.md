| Dok.-Nr. | ERGEBNIS-C0 | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Ergebnis Chemievergleich LFP/NMC (1500 kg, 400 km) | Ersteller | Claude Sonnet (KI) | Prüfer | Opus (Rohdaten) |

> **KI-generiert.** Entwurf, nicht vom Menschen freigegeben. Alle Zahlen aus `sim/chemie/vergleich_lfp_nmc/ergebnis.json` (erzeugt von `vergleich.py` aus `eingaben.json`). Mitte eines Bandes = arithmetisches Mittel. Keine Empfehlung, keine Deutung (schreibt Opus).

Zyklenbedarf = 1000 Vollzyklen; Bauraumvolumen 345.8 L (ergebnis.json). Grenze Batterieanteil 30 % (Annahme).

## Ergebnis je Chemie und Fall (Mitte)

| Chemie | Fall | w [Wh/kg] | E_netto [kWh] | E_brutto [kWh] | Verbrauch [kWh/100 km] | Packmasse [kg] | Spanne w,k [kg] | Gesamtmasse [kg] | Anteil | Grenze [kg] | unter Grenze | Schritte | Zellen in Reihe | Pack-Wh/L nötig | Bauraum |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| LFP | A | 197.5 | 68.00 | 73.91 | 17.00 | 499.0 | 414–615 | 1500.0 | 33.3 % | 450.0 | nein | 0 | 250 | 213.7 | offen (keine Quelle) |
| LFP | B | 197.5 | 81.57 | 88.66 | 20.39 | 598.5 | 480–773 | 2098.5 | 28.5 % | 629.6 | ja | 6 | 250 | 256.4 | offen (keine Quelle) |
| NMC | A | 212.5 | 68.00 | 73.91 | 17.00 | 463.8 | 316–758 | 1500.0 | 30.9 % | 450.0 | nein | 0 | 220 | 213.7 | Zellband 250–842 Wh/L (Zelle, nicht Pack; allgemein Li-Ion): Bedarf unter Bandanfang |
| NMC | B | 212.5 | 80.43 | 87.43 | 20.11 | 548.6 | 353–1014 | 2048.6 | 26.8 % | 614.6 | ja | 6 | 220 | 252.8 | Zellband 250–842 Wh/L (Zelle, nicht Pack; allgemein Li-Ion): Bedarf im Band |

NMC Reihe bei Spannungsband 3,6/3,7 V: 223, 217 Zellen.

## Zyklen

| Chemie | Band | Bedarf | Urteil |
|---|---|---|---|
| LFP | 2500–9000 | 1000 | erfüllt |
| NMC | 400–1200 | 1000 | unsicher (Li-Ion allgemein, nicht NMC-spezifisch) |

## Empfindlichkeit der Packmasse (je Größe einzeln, andere in der Mitte)

| Chemie | Fall | k 0,65 / 0,85 [kg] | Hub k | w unten / oben [kg] | Hub w | a 0,3 / 0,7 [kg] | Hub a | stärkste Annahme |
|---|---|---|---|---|---|---|---|---|
| LFP | A | 576 / 440 | 135 | 533 / 469 | 63 | – | – | k |
| LFP | B | 712 / 516 | 196 | 648 / 556 | 91 | 554 / 650 | 96 | k |
| NMC | A | 535 / 409 | 126 | 657 / 358 | 299 | – | – | w |
| NMC | B | 651 / 474 | 177 | 841 / 407 | 434 | 511 / 592 | 81 | w |

## Abgleich mit ERWARTUNG.md

1. Energie: netto 68.0 kWh, brutto 73.9 kWh in A (erwartet 68/74): **erfüllt**. Fall B brutto +20.0 % (LFP), +18.3 % (NMC) (erwartet 15–25 %): **erfüllt**. Iteration: 6 Schritte, konvergiert: **erfüllt**.
2. Masse: Bänder überlappen (LFP 185–210, NMC 150–275 Wh/kg): **erfüllt**. Packmasse Mitte 464–499 kg (A), 549–599 kg (B), erwartet 400–600: **erfüllt**. NMC am oberen Bandende (275 Wh/kg) 358 kg (A), 407 kg (B), deutlich leichter: **erfüllt**.
3. Grenze 30 %: Fall A LFP 33.3 %, NMC 30.9 % (beide über 30 %, erwartet nahe/darüber): **erfüllt**. Fall B LFP 28.5 %, NMC 26.8 % (beide unter 30 %, aber nur knapp; erwartet eher darunter): **erfüllt**.
4. Zellzahl: LFP 250 (erwartet ca. 250), NMC 220 (erwartet ca. 220), Abweichung 0 %: **erfüllt**.
5. Zyklen: Bedarf 1000; LFP erfüllt, NMC unsicher: **erfüllt**.
6. Bauraum: nötig 213.7 Wh/L (A), 256.4 (B LFP), 252.8 (B NMC) (erwartet ca. 214): **erfüllt** für Fall A; LFP „offen (keine Quelle)“: **erfüllt**. Hinweis: NMC-Zellband 250–842 Wh/L, Bedarf A unter Bandanfang, Bedarf B knapp im Band (Zelle, nicht Pack; allgemein Li-Ion).
7. Deutung vorab: keine Rechengröße, wird von Opus beurteilt.

Verfehlte Erwartungen nach den Kriterien der ERWARTUNG.md: keine.

---
*KI-generiert (Claude Sonnet, 2026-11-16), Entwurf, nicht vom Menschen freigegeben. BAT-ERGEBNIS-C0 v1.0.*
