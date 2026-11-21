| Dok.-Nr. | BAT-DOC-18 | Version | 0.3 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Kostenbewertung je Variante (REQ-P16, Vorgänge KO1, KO2) | Ersteller | Claude Sonnet (KI), Auftrag Opus | Prüfer | Opus (offen) |

> **KI-generiert** (Claude Sonnet, 2026-11-19), Entwurf. Alle Preise sind **Annahmen** (ERW-KO1/KO2, Opus) oder aus Distributorpreisen abgeleitet. Belegt ist nur der Marktpreis W29.

## Ergebnis in einem Satz
Nach KO2 (Stückliste SL3.1, Blech-Kühlplatte mit echter Masse, Kühlkreis BT-661…665, Normteile, Serienfaktor f_serie 0,35) ergibt die **Teilsumme** (offene Positionen fehlen, also **untere Schranke**) für LFP 6.557 € je Pack (88,7 €/kWh, im Band) und für NMC 8.737 € (117,6 €/kWh, im Band).

## Zahlen (Quelle: `pm/kosten/ergebnis_LFP.json`, `pm/kosten/ergebnis_NMC.json`)
| | LFP | NMC |
|---|---|---|
| Energie (kWh) | 73,92 | 74,27 |
| Teilsumme Pack (€) | 6.557 | 8.737 |
| €/kWh | 88,7 | 117,6 |
| Zellkosten (€) / Zellanteil | 3.696 / 56,4 % | 5.570 / 63,8 % |
| BT-200 Zellverbund (€ / Anteil) | 297 / 4,5 % | 384 / 4,4 % |
| BT-300 BMS/Sensorik (€ / Anteil) | 528 / 8,1 % | 661 / 7,6 % |
| BT-400 Verbinder/Leitung (€ / Anteil) | 48 / 0,7 % | 125 / 1,4 % |
| BT-500 Gehäuse/Struktur (€ / Anteil) | 545 / 8,3 % | 516 / 5,9 % |
| BT-600 Kühlung (€ / Anteil) | 792 / 12,1 % | 778 / 8,9 % |
| BT-700 Schaltbox/Stecker (€ / Anteil) | 345 / 5,3 % | 369 / 4,2 % |
| Fertigung (€ / Anteil) | 306 / 4,7 % | 333 / 3,8 % |
| Offene Positionen | 3 | 2 |
| Zellpreis -20 % / +20 % → Pack | -11,3 % / +11,3 % | -12,8 % / +12,8 % |
| Abstand zum Beleg 89,2 €/kWh | -0,5 €/kWh | 28,4 €/kWh |

Beleg: 97 USD/kWh BEV-Packpreis 2024 (BNEF, `forschung/ergebnis/W29.md`), Kurs 0,92 (Annahme). Der Beleg ist ein **Preis**, hier gerechnet sind **Herstellkosten** ohne Gemeinkosten und Marge; Vergleich nur als Größenordnung.

## Abgleich mit der Erwartung KO2 (`pm/kosten/ERWARTUNG.md`, Nachtrag 2)
| Erwartung (ERW-KO2) | LFP | NMC |
|---|---|---|
| Pack (Erwartung; Band ±8 %) | 6.250 € (Band 5.750–6.750): 6.557 € (4,9 %), im Band | 8.600 € (Band 7.912–9.288): 8.737 € (1,6 %), im Band |
| €/kWh (Erwartung; Band ±8 %) | 85 (Band 78,2–91,8): 88,7 (4,4 %) | 116 (Band 106,7–125,3): 117,6 (1,4 %) |
| Anteil verifiziert/abgeleitet < 1 % | 0,25 %: erfüllt | 0,18 %: erfüllt |
| Position ohne Menge/Masse als „offen“ ausgewiesen | erfüllt (alle offenen mit Grund) | erfüllt (alle offenen mit Grund) |

Frühere Prüfungen (ERW-KO1/Nachtrag 1, Zielband KO1 LFP 5 500–7 000 € / NMC 7 000–9 000 €): LFP Pack im Band, Zellanteil 56,4 % (VERFEHLT (< 60 % oder > 85 %)), größte Nicht-Zell-Position BT-610 8,7 %; NMC Pack im Band, Zellanteil 63,8 % (unter 65 %, Schwelle 60 % nicht unterschritten), größte Nicht-Zell-Position BT-610 6,4 %.

Deutung bleibt bei Opus. Die Teilsumme ist eine untere Schranke (offene Positionen fehlen).

## Status der Preise (3 Stufen)
Stufen: „verifiziert (Wxx/Datenblatt)“, „abgeleitet aus Distributorpreis“, „Schätzung (Annahme Opus)“. Quelle `pm/kosten/eingaben.json` und `ergebnis_<V>.json` (`eur_je_stufe`).

| Stufe | LFP € | LFP Anteil | NMC € | NMC Anteil |
|---|---|---|---|---|
| verifiziert | 0,00 | 0,00 % | 0,00 | 0,00 % |
| abgeleitet | 16,32 | 0,25 % | 15,54 | 0,18 % |
| Schätzung | 6.540,51 | 99,75 % | 8.721,62 | 99,82 % |

Abgeleitet sind: Schmelzsicherung Eaton EKC14-40 (25,84 € Menge 1 × f_serie 0,35 = 9,04 €, Teil des BT-713-Satzes) und NTC Vishay NTCS0603E3 (0,37 € × f_serie = 0,13 €). f_serie ist selbst eine Schätzung (Annahme Opus). Arcol HS50 wird nicht verwendet (gehört nicht zum gewählten Vishay RH050). Der Marktpreis W29 ist ein Beleg zum Vergleich, keine Position; **verifiziert** ist keine Position.

**Zielwert für REQ-P16:** keiner, bleibt offen (Autor). Das Zielband in den Bildern ist eine Erwartung (Schätzung), kein Zielwert.

## Preise je Eintrag
| Schlüssel | Preis | Einheit | Status | wert_ko1 | LFP € / Pack | NMC € / Pack |
|---|---|---|---|---|---|---|
| BT-100 | LFP 50 / NMC 75 | €/kWh | Schätzung (Annahme Opus, ERW-KO1) | – | 3.696,00 | 5.570,25 |
| BT-210 | 6,00 | €/kg | Schätzung (Annahme Opus, ERW-KO1) | – | offen | offen |
| BT-220 | 6,00 | €/kg | Schätzung (Annahme Opus, ERW-KO1) | – | 26,70 | – |
| BT-230 | 20,00 | €/kg | Schätzung (Annahme Opus, ERW-KO1) | – | 270,58 | 252,17 |
| BT-240 | entfällt | €/kg | entfällt | 6 | 0,00 | – |
| BT-250 | 6,00 | €/kg | Schätzung (Annahme Opus, ERW-KO1) | – | – | 18,41 |
| BT-260 | 10,00 | €/kg | Schätzung (Annahme Opus, ERW-KO1) | – | – | 113,61 |
| BT-310 | 120,00 | €/Stück | Schätzung (Annahme Opus, ERW-KO1) | – | 120,00 | 120,00 |
| BT-320 | 15,00 | €/Stück | Schätzung (Annahme Opus, ERW-KO1) | – | 210,00 | 195,00 |
| BT-330 | 0,13 | €/Stück | abgeleitet aus Distributorpreis | 0.5 | 7,28 | 6,50 |
| BT-340 | 40,00 | €/Stück | Schätzung (Annahme Opus, ERW-KO1) | – | 40,00 | 40,00 |
| BT-350 | 20,00 | €/Stück | Schätzung (Annahme Opus, ERW-KO1) | – | 20,00 | 20,00 |
| BT-360 | 8,00 | €/m | Schätzung (Annahme Opus, ERW-KO1) | – | 94,33 | 246,38 |
| BT-361 | 0,30 | €/Stück | Schätzung (Annahme Opus, ERW-KO1) | – | 0,60 | – |
| BT-410 | 8,00 | €/kg | Schätzung (Annahme Opus, ERW-KO1) | – | offen | 4,24 |
| BT-420 | 8,00 | €/kg | Schätzung (Annahme Opus, ERW-KO1) | – | 15,37 | 87,65 |
| BT-430 | 25,00 | €/m | Schätzung (Annahme Opus, ERW-KO1) | – | 26,99 | 27,21 |
| BT-440 | 8,00 | €/kg | Schätzung (Annahme Opus, ERW-KO1) | – | 5,35 | 3,75 |
| BT-510 | 6,00 | €/kg | Schätzung (Annahme Opus, ERW-KO1) | – | 142,29 | 135,34 |
| BT-520 | 6,00 | €/kg | Schätzung (Annahme Opus, ERW-KO1) | – | 94,66 | 90,21 |
| BT-530 | 6,00 | €/kg | Schätzung (Annahme Opus, ERW-KO1) | – | 24,83 | 24,83 |
| BT-540 | 6,00 | €/kg | Schätzung (Annahme Opus, ERW-KO1) | – | 84,39 | 78,67 |
| BT-550 | 6,00 | €/kg | Schätzung (Annahme Opus, ERW-KO1) | – | 142,29 | 135,34 |
| BT-560 | 1,50 | €/Stück | Schätzung (Annahme Opus, ERW-KO2) | 0.5 | 18,00 | 18,00 |
| BT-570 | 5,00 | €/Stück | Schätzung (Annahme Opus, ERW-KO1) | 5 | 5,00 | 5,00 |
| BT-610 | 12,00 | €/kg | Schätzung (Annahme Opus, ERW-KO2) | 12 | 571,94 | 558,62 |
| BT-620 | 12,00 | €/kg | Schätzung (Annahme Opus, ERW-KO1) | – | 5,92 | 5,53 |
| BT-630 | 10,00 | €/Stück | Schätzung (Annahme Opus, ERW-KO1) | – | 20,00 | 20,00 |
| BT-640 | 3,00 | €/Stück | Schätzung (Annahme Opus, ERW-KO1) | – | 6,00 | 6,00 |
| BT-650 | 3,00 | €/L | Schätzung (Annahme Opus, ERW-KO1) | – | offen | offen |
| BT-660 | entfällt | €/Stück | entfällt | 0 | 0,00 | 0,00 |
| BT-710 | 8,00 | €/kg | Schätzung (Annahme Opus, ERW-KO1) | – | 15,73 | 15,42 |
| BT-711 | 45,00 | €/Stück | Schätzung (Annahme Opus, ERW-KO1) | – | 90,00 | 90,00 |
| BT-712 | 25,00 | €/Stück | Schätzung (Annahme Opus, ERW-KO1) | – | 50,00 | 50,00 |
| BT-713 | 44,04 | €/Satz | Schätzung (Annahme Opus, ERW-KO2) | 55 | 44,04 | 44,04 |
| BT-720 | 40,00 | €/Stück | Schätzung (Annahme Opus, ERW-KO1) | – | – | 40,00 |
| BT-721 | 15,00 | €/Satz | Schätzung (Annahme Opus, ERW-KO1) | – | 15,00 | – |
| BT-722 | 0,00 | €/Stück | Schätzung (Annahme Opus, ERW-KO1) | – | 0,00 | – |
| BT-730 | 80,00 | €/Satz | Schätzung (Annahme Opus, ERW-KO1) | – | 80,00 | 80,00 |
| BT-740 | 15,00 | €/Stück | Schätzung (Annahme Opus, ERW-KO1) | – | 15,00 | 15,00 |
| BT-750 | 8,00 | €/Stück | Schätzung (Annahme Opus, ERW-KO1) | – | 8,00 | 8,00 |
| BT-760 | 0,00 | €/Stück | Schätzung (Annahme Opus, ERW-KO1) | – | 0,00 | 0,00 |
| BT-770 | 25,00 | €/Stück | Schätzung (Annahme Opus, ERW-KO1) | – | 25,00 | 25,00 |
| BT-780 | 2,00 | €/Stück | Schätzung (Annahme Opus, ERW-KO1) | – | 2,00 | 2,00 |
| BT-580 | 4,00 | €/Stück | Schätzung (Annahme Opus, ERW-KO2) | – | 12,00 | 8,00 |
| BT-661 | 60,00 | €/Stück | Schätzung (Annahme Opus, ERW-KO2) | – | 60,00 | 60,00 |
| BT-662 | 70,00 | €/Stück | Schätzung (Annahme Opus, ERW-KO2) | – | 70,00 | 70,00 |
| BT-663 | 35,00 | €/Stück | Schätzung (Annahme Opus, ERW-KO2) | – | 35,00 | 35,00 |
| BT-664 | 15,00 | €/Satz | Schätzung (Annahme Opus, ERW-KO2) | – | 15,00 | 15,00 |
| BT-665 | 8,00 | €/Stück | Schätzung (Annahme Opus, ERW-KO2) | – | 8,00 | 8,00 |
| BT-450 | 6,00 | €/kg | Schätzung (Annahme Opus, ERW-KO2) | – | – | 1,83 |
| BT-590:Schraube | 0,10 | €/Stück | Schätzung (Annahme Opus, ERW-KO2) | – | 8,40 | 7,20 |
| BT-590:Kabelschuh | 1,50 | €/Stück | Schätzung (Annahme Opus, ERW-KO2) | – | 12,00 | 12,00 |
| BT-590:Clip | 0,10 | €/Stück | Schätzung (Annahme Opus, ERW-KO2) | – | 0,40 | 0,40 |
| BT-590:Schrumpfschlauch | 0,20 | €/Stück | Schätzung (Annahme Opus, ERW-KO2) | – | 1,20 | 1,20 |
| BT-360:Detail | 0,00 | €/Stück | Schätzung (Annahme Opus, ERW-KO2) | – | 0,00 | 0,00 |
| BT-360:Daisy | 3,00 | €/Stück | Schätzung (Annahme Opus, ERW-KO2) | – | 36,00 | 33,00 |
| Beleg Packpreis | 97 USD/kWh = 89,2 €/kWh | €/kWh | verifiziert (W29, Zitat geprüft) | – | – | – |
| Fertigung | 10 % Nicht-Zell + 50 €/Pack | – | Schätzung (Annahme Opus, ERW-KO1) | – | 306 | 333 |

## Offene Positionen (untere Schranke, nicht als 0 gezählt)

**LFP (3):** 200.1 BT-210 Zellreihe zwischen Querträgern (Ano (Masse offen); 400.1 BT-410 Zellverbinder (Zellabgriff, Plus un (Masse offen); 600.5 BT-650 Kühlmittel Wasser-Glykol (Volumen offen)

**NMC (2):** 200.1 BT-210 Zellreihe zwischen Querträgern (Ano (Masse offen); 600.5 BT-650 Kühlmittel Wasser-Glykol (Volumen offen)

Entfallen (0 €, nicht offen): BT-240 Verspannung, BT-660 (ersetzt durch BT-661…665); BT-720 LFP ersetzt durch BT-721/722 (Positionszuordnung `pos_zu_preis`).

## Annahmen und Auslegungen
1. Fertigung: 10 % auf die Nicht-Zell-Summe + 50 € je Pack (Nachtrag 1).
2. BT-610 Kühlplatte: 12 €/kg × Blechmasse aus K2b (Blech 1/4/1, ENT-152…156); der Faktor 0,6 entfällt (ERW-KO2 Punkt 4). Bis G5.7 steht die K2b-Masse in der Stückliste.
3. Längen aus `cad/pack/entwurf/ergebnis_<V>_e2d.json`: BT-360 FPC = Masse / `A_e2_fpc_masse_kg_m`; BT-430 HV-Leitung = `e2.hv_laenge_gesamt_m`. Die Länge gilt nur für die Position 300.6 bzw. 400.3; die Positionen 360.3 und 360.4 (FPC-Detail, Daisy-Chain) erhalten keinen Längenpreis und sind offen (in KO1 wurde die FPC-Länge dreifach gezählt, siehe Hinweis in `eingaben.json laengen_aus_cad`).
4. BT-721/722 zusammen 15 €, BT-713 als Satz (44,04 €), BT-730 als Satz (80 €). BT-712 25 €/Stück bei Menge 2 (Auslegung). BT-210 ist eine Anordnung ohne Masse und bleibt offen.
5. Kühlmittelvolumen BT-650 offen; Masse BT-620 offen bis G5-CAD.
6. Massen BT-510…550, 620, 630 und Schläuche 660.4 sind bis zur Gesamtmontage (G5.7) die Obergrenzen aus e2d bzw. offen; nach `stueckliste_v3.py --aus-cad` ersetzt die CAD-Masse sie.

## Bilder (Zielband beschriftet, Lesehilfe im Bild)
- `pm/kosten/kosten_LFP.png`, `kosten_NMC.png`, `kosten_vergleich.png`: gestapelter Balken €/kWh je Baugruppe, Zielband ERW-KO2 ±8 % (schwarzer Rahmen), Beleg 89,2 €/kWh (rot).

## Dateien und Neulauf
`pm/kosten/eingaben.json`, `preisregeln.py`, `kosten.py`, `bilder.py`, `doku.py`, `ergebnis_LFP.json`, `ergebnis_NMC.json`, `praesentation/bausteine/KO1.md`, `KO2.md`.
Neulauf nach der Gesamtmontage: `python3 pm/bauteile/stueckliste_v3.py --aus-cad && python3 pm/kosten/kosten.py && python3 pm/kosten/bilder.py && python3 pm/kosten/doku.py`.

*KI-generiert, Entwurf. Nicht freigegeben. BAT-DOC-18.*
