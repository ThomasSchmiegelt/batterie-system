| Dok.-Nr. | BAT-DOC-18 | Version | 0.2 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Kostenbewertung je Variante (REQ-P16, Vorgang KO1) | Ersteller | Claude Sonnet (KI), Auftrag Opus | Prüfer | Opus (offen) |

> **KI-generiert** (Claude Sonnet, 2026-11-18), Entwurf. Alle Preise sind **Annahmen** (ERW-KO1 inkl. Nachtrag 1, Opus). Belegt ist nur der Marktpreis W29.

## Ergebnis in einem Satz
Nach Nachtrag 1 (Fertigung nur auf Nicht-Zell-Summe, Kühlplatte × 0,6, Längen BT-360/430 aus dem CAD) ergibt die **Teilsumme** (offene Positionen fehlen, also **untere Schranke**) für LFP 5.935 € je Pack (80,3 €/kWh) und für NMC 8.149 € (109,7 €/kWh).

## Zahlen (Quelle: `pm/kosten/ergebnis_LFP.json`, `pm/kosten/ergebnis_NMC.json`)
| | LFP | NMC |
|---|---|---|
| Energie (kWh) | 73,92 | 74,27 |
| Teilsumme Pack (€) | 5.935 | 8.149 |
| €/kWh | 80,3 | 109,7 |
| Zellkosten (€) / Zellanteil | 3.696 / 62,3 % | 5.570 / 68,4 % |
| BT-200 Zellverbund (€ / Anteil) | 271 / 4,6 % | 384 / 4,7 % |
| BT-300 BMS/Sensorik (€ / Anteil) | 465 / 7,8 % | 601 / 7,4 % |
| BT-400 Verbinder/Leitung (€ / Anteil) | 35 / 0,6 % | 117 / 1,4 % |
| BT-500 Gehäuse/Struktur (€ / Anteil) | 535 / 9,0 % | 507 / 6,2 % |
| BT-600 Kühlung (€ / Anteil) | 338 / 5,7 % | 319 / 3,9 % |
| BT-700 Schaltbox/Stecker (€ / Anteil) | 346 / 5,8 % | 370 / 4,5 % |
| Fertigung (€ / Anteil) | 249 / 4,2 % | 280 / 3,4 % |
| Offene Positionen | 16 | 13 |
| Zellpreis -20 % / +20 % → Pack | -12,5 % / +12,5 % | -13,7 % / +13,7 % |
| Abstand zum Beleg 89,2 €/kWh | -8,9 €/kWh | 20,5 €/kWh |

Beleg: 97 USD/kWh BEV-Packpreis 2024 (BNEF, `forschung/ergebnis/W29.md`), Kurs 0,92 (Annahme). Der Beleg ist ein **Preis**, hier gerechnet sind **Herstellkosten** ohne Gemeinkosten und Marge; Vergleich nur als Größenordnung.

## Abgleich mit der Erwartung (`pm/kosten/ERWARTUNG.md`, Nachtrag 1)
| Erwartung | LFP | NMC |
|---|---|---|
| Pack LFP 5 500–7 000 € / NMC 7 000–9 000 € | 5.935 €: im Band | 8.149 €: im Band |
| €/kWh LFP 75–95 / NMC 95–120 | 80,3 €/kWh: im Band | 109,7 €/kWh: im Band |
| Nachtrag 1: LFP ≈ 5 800 € / 79 €/kWh / 63 %, NMC ≈ 7 900 € / 106 €/kWh / 70 % | 5.935 € / 80,3 / 62,3 % | 8.149 € / 109,7 / 68,4 % |
| Zellanteil 65–80 % (Verfehlt < 60 % oder > 85 %) | 62,3 %: unter dem Band 65 %, Verfehlt-Schwelle nicht erreicht | 68,4 %: im Band |
| keine Nicht-Zell-Position > 10 % | größte BT-610 5,7 %: erfüllt | größte BT-610 3,9 %: erfüllt |
| Zellpreis ±20 % → Pack ±13–16 % | ±12,5 % | ±13,7 % |

Gründe für Abweichungen nach unten bei Zellanteil/Pack: Teilsumme ohne offene Positionen (untere Schranke); deshalb liegt der Zellanteil real eher darunter, der Packpreis darüber. Deutung bleibt bei Opus.

## Preise je Position mit Status
Status: nur der BNEF-Packpreis (W29) ist „verifiziert (W29, Zitat geprüft)“; alle Positionspreise sind „Schätzung (Annahme Opus, ERW-KO1)“. Quelle `pm/kosten/eingaben.json` (Spalte status) und `ergebnis_<V>.json`.

| BT | Preis | Einheit | Status | LFP € / Pack | NMC € / Pack |
|---|---|---|---|---|---|
| BT-100 | LFP 50 / NMC 75 | €/kWh | Schätzung (Annahme Opus, ERW-KO1) | 3.696 | 5.570 |
| BT-210 | 6,00 | €/kg | Schätzung (Annahme Opus, ERW-KO1) | offen | offen |
| BT-220 | 6,00 | €/kg | Schätzung (Annahme Opus, ERW-KO1) | offen | – |
| BT-230 | 20,00 | €/kg | Schätzung (Annahme Opus, ERW-KO1) | 271 | 252 |
| BT-240 | 6,00 | €/kg | Schätzung (Annahme Opus, ERW-KO1) | offen | – |
| BT-250 | 6,00 | €/kg | Schätzung (Annahme Opus, ERW-KO1) | – | 18 |
| BT-260 | 10,00 | €/kg | Schätzung (Annahme Opus, ERW-KO1) | – | 114 |
| BT-310 | 120,00 | €/Stück | Schätzung (Annahme Opus, ERW-KO1) | 120 | 120 |
| BT-320 | 15,00 | €/Stück | Schätzung (Annahme Opus, ERW-KO1) | 210 | 195 |
| BT-330 | 0,50 | €/Stück | Schätzung (Annahme Opus, ERW-KO1) | offen | offen |
| BT-340 | 40,00 | €/Stück | Schätzung (Annahme Opus, ERW-KO1) | 40 | 40 |
| BT-350 | 20,00 | €/Stück | Schätzung (Annahme Opus, ERW-KO1) | offen | offen |
| BT-360 | 8,00 | €/m | Schätzung (Annahme Opus, ERW-KO1) | 94 | 246 |
| BT-361 | 0,30 | €/Stück | Schätzung (Annahme Opus, ERW-KO1) | 1 | – |
| BT-410 | 8,00 | €/kg | Schätzung (Annahme Opus, ERW-KO1) | offen | 2 |
| BT-420 | 8,00 | €/kg | Schätzung (Annahme Opus, ERW-KO1) | 8 | 88 |
| BT-430 | 25,00 | €/m | Schätzung (Annahme Opus, ERW-KO1) | 27 | 27 |
| BT-440 | 8,00 | €/kg | Schätzung (Annahme Opus, ERW-KO1) | 0 | 0 |
| BT-510 | 6,00 | €/kg | Schätzung (Annahme Opus, ERW-KO1) | 142 | 136 |
| BT-520 | 6,00 | €/kg | Schätzung (Annahme Opus, ERW-KO1) | 95 | 90 |
| BT-530 | 6,00 | €/kg | Schätzung (Annahme Opus, ERW-KO1) | 25 | 25 |
| BT-540 | 6,00 | €/kg | Schätzung (Annahme Opus, ERW-KO1) | 131 | 120 |
| BT-550 | 6,00 | €/kg | Schätzung (Annahme Opus, ERW-KO1) | 142 | 136 |
| BT-560 | 0,50 | €/Stück | Schätzung (Annahme Opus, ERW-KO1) | offen | offen |
| BT-570 | 5,00 | €/Stück | Schätzung (Annahme Opus, ERW-KO1) | offen | offen |
| BT-610 | 12,00 | €/kg | Schätzung (Annahme Opus, ERW-KO1) | 338 | 319 |
| BT-620 | 12,00 | €/kg | Schätzung (Annahme Opus, ERW-KO1) | offen | offen |
| BT-630 | 10,00 | €/Stück | Schätzung (Annahme Opus, ERW-KO1) | offen | offen |
| BT-640 | 3,00 | €/Stück | Schätzung (Annahme Opus, ERW-KO1) | offen | offen |
| BT-650 | 3,00 | €/L | Schätzung (Annahme Opus, ERW-KO1) | offen | offen |
| BT-660 | 0,00 | €/Stück | Schätzung (Annahme Opus, ERW-KO1) | 0 | 0 |
| BT-710 | 8,00 | €/kg | Schätzung (Annahme Opus, ERW-KO1) | 16 | 15 |
| BT-711 | 45,00 | €/Stück | Schätzung (Annahme Opus, ERW-KO1) | 90 | 90 |
| BT-712 | 25,00 | €/Stück | Schätzung (Annahme Opus, ERW-KO1) | 50 | 50 |
| BT-713 | 55,00 | €/Satz | Schätzung (Annahme Opus, ERW-KO1) | 55 | 55 |
| BT-720 | 40,00 | €/Stück | Schätzung (Annahme Opus, ERW-KO1) | 0 | 40 |
| BT-721 | 15,00 | €/Satz | Schätzung (Annahme Opus, ERW-KO1) | 15 | – |
| BT-722 | 0,00 | €/Stück | Schätzung (Annahme Opus, ERW-KO1) | 0 | – |
| BT-730 | 80,00 | €/Satz | Schätzung (Annahme Opus, ERW-KO1) | 80 | 80 |
| BT-740 | 15,00 | €/Stück | Schätzung (Annahme Opus, ERW-KO1) | 15 | 15 |
| BT-750 | 8,00 | €/Stück | Schätzung (Annahme Opus, ERW-KO1) | offen | offen |
| BT-760 | 0,00 | €/Stück | Schätzung (Annahme Opus, ERW-KO1) | 0 | 0 |
| BT-770 | 25,00 | €/Stück | Schätzung (Annahme Opus, ERW-KO1) | 25 | 25 |
| BT-780 | 2,00 | €/Stück | Schätzung (Annahme Opus, ERW-KO1) | offen | offen |
| Beleg Packpreis | 97 USD/kWh = 89,2 €/kWh | €/kWh | verifiziert (W29, Zitat geprüft) | – | – |
| Fertigung | 10 % Nicht-Zell + 50 €/Pack | – | Schätzung (Annahme Opus, ERW-KO1) | 249 | 280 |

**Anteil an Schätzungen:** 100,0 % der Summe (LFP) und 100,0 % (NMC) beruhen auf Schätzungen (Annahme Opus, ERW-KO1); verifiziert ist keine Position, nur der Marktpreis-Beleg zum Vergleich.

**Zielwert für REQ-P16:** keiner, bleibt offen (Autor). Das Zielband in den Bildern ist eine Erwartung (Schätzung), kein Zielwert.

## Offene Positionen (untere Schranke, nicht als 0 gezählt; kein Abbruch nach Nachtrag 1)

**LFP (16):** BT-210 Zellreihe zwischen Querträgern (Cel (Masse offen); BT-220 Zwischenlage zwischen Zellen (Wärme (Masse offen); BT-240 Verspannung der Zellreihen (Endplat (Masse offen); BT-330 Temperaturfühler Zelle (Menge offen); BT-350 Isolationswächter (Menge offen); BT-410 Zellverbinder (Zellabgriff, Plus un (Masse offen); BT-560 Befestigungspunkte am Fahrzeug (Menge offen); BT-570 Druckausgleichselement (atmend, was (Menge offen); BT-620 Verteiler und Sammler (Masse offen); BT-630 Kühlmittelanschlüsse Ein/Aus (Menge offen); BT-640 Temperaturfühler Kühlmittel (Menge offen); BT-650 Kühlmittel Wasser-Glykol (Volumen offen bis K2); BT-750 Entgasungsventil mit Entgasungskana (Menge offen); BT-780 Kennzeichnung (Typschild, HV-Warnun (Menge offen); Dichtungen Stromschienen Cu der Schaltbox (e2d (kein BT, kein Preis (nicht im CAD)); Dichtungen Dichtungen (Deckel, Schaltbox, Serv (kein BT, kein Preis (nicht im CAD))

**NMC (13):** BT-210 Zellreihe zwischen Querträgern (Cel (Masse offen); BT-330 Temperaturfühler Zelle (Menge offen); BT-350 Isolationswächter (Menge offen); BT-560 Befestigungspunkte am Fahrzeug (Menge offen); BT-570 Druckausgleichselement (atmend, was (Menge offen); BT-620 Verteiler und Sammler (Masse offen); BT-630 Kühlmittelanschlüsse Ein/Aus (Menge offen); BT-640 Temperaturfühler Kühlmittel (Menge offen); BT-650 Kühlmittel Wasser-Glykol (Volumen offen bis K2); BT-750 Entgasungsventil mit Entgasungskana (Menge offen); BT-780 Kennzeichnung (Typschild, HV-Warnun (Menge offen); Dichtungen Stromschienen Cu der Schaltbox (e2d (kein BT, kein Preis (nicht im CAD)); Dichtungen Dichtungen (Deckel, Schaltbox, Serv (kein BT, kein Preis (nicht im CAD))

Hinweise: BT-760 Heizung und BT-660 Schnittstelle Preis 0 (Fahrzeug), nicht offen. BT-720 LFP ersetzt durch BT-721/722.

## Annahmen und Auslegungen
1. Fertigung: 10 % auf die Nicht-Zell-Summe + 50 € je Pack (Nachtrag 1).
2. BT-610 Kühlplatte: Masse × 0,6 bis K2 eine Hohlmasse liefert (Nachtrag 1).
3. Längen aus `cad/pack/entwurf/ergebnis_<V>_e2d.json`: BT-360 FPC = Masse / `A_e2_fpc_masse_kg_m` (0,05 kg/m); BT-430 HV-Leitung = `e2.hv_laenge_gesamt_m` direkt (Stand Bericht 0.3, vorher aus dem Volumen).
4. BT-721/722 zusammen 15 €, BT-713 (55 €) und BT-730 (80 €) als Satz (von Opus bestätigt). BT-712 25 €/Stück bei Menge 2 (Auslegung). BT-210/240 mit Al 6 €/kg, Masse offen, ohne Wirkung.
5. Kühlmittelvolumen BT-650 offen bis K2.

## Bilder (Zielband beschriftet, Lesehilfe im Bild)
- `pm/kosten/kosten_LFP.png`, `kosten_NMC.png`, `kosten_vergleich.png`: gestapelter Balken €/kWh je Baugruppe, Zielband (schwarzer Rahmen), Beleg 89,2 €/kWh (rot).

## Dateien
`pm/kosten/eingaben.json`, `kosten.py`, `bilder.py`, `doku.py`, `ergebnis_LFP.json`, `ergebnis_NMC.json`, `praesentation/bausteine/KO1.md`. Aufruf: `python3 pm/kosten/kosten.py && python3 pm/kosten/bilder.py && python3 pm/kosten/doku.py`.

*KI-generiert, Entwurf. Nicht freigegeben. BAT-DOC-18.*
