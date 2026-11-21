# PI Prüfbericht G5 (NACH)
KI-generiert (Claude Opus, G5_NACH, 2026-11-20). Nur Zahlen mit Quelldatei, keine Deutung.

## 1. Log: cad/baukasten/ausgabe/lauf_g5.log
- Zeilen mit "FEHLER": 0. Zeilen mit "Traceback": 0 (grep, ganzes Log, 210 443 Byte).
- Zeilen mit "Fehler" (kleingeschrieben), Zeilen 52, 871, 1690:
  - 52: `fertig LFP: 1343 Teile, 628.83 kg, 16 Fehler, 49 s`
  - 871: `fertig NMC: 3601 Teile, 479.98 kg, 16 Fehler, 532 s`
  - 1690: `170 Bilder, 110 Fehler`
- Letzte Zeile: `== 10:27:36 PI Prüfbericht`.

## 2. Prüfung (pruefung_LFP.txt / pruefung_NMC.txt, Zeile 1–2)
| | LFP | NMC |
|---|---|---|
| Teile | 1343 | 3601 |
| Masse | 628.83 kg | 479.98 kg |
| L×B×H | 2335×1430×245 mm | 2235×1430×228 mm |
| Fehler | 16 | 16 |
| Zeilen mit "Kollision" | 0 | 0 |

- 10 größte Kollisionen (mm³): nicht vorhanden, da Zeilen mit "Kollision": 0 (beide Dateien).
- Die 16 Fehler-Listenzeilen sind alle Massentoleranzen (kg, %); LFP größter Wert 700.1b schaltbox.deckel +56.7 %, 590.1 normteile.schraube +318.2 %; NMC größter 590.1 normteile.schraube +322.9 % (pruefung_LFP.txt, pruefung_NMC.txt, Zeilen 3–18).

## 3. Bilder in bericht/bilder/ (vs. bericht.tex, Stand 2026-11-20 10:09:50)
- 18/18 vorhanden: g5_{LFP,NMC}_{gesamt,explosion,schnitt,ecke,schaltbox,kuehlkreis,draufsicht,kabelplan,bruecke}.png (ls).
- Alle 18: Zeitstempel 2026-11-20 10:27:35 → neuer als bericht.tex (10:09:50) (stat).

## 4. LaTeX: bericht/bericht.log
- "Output written on bericht.pdf (78 pages, 51 612 788 bytes)", Zeile 3241.
- Zeilen mit "! ": 1 → Zeile 2670: `! LaTeX Error: Unicode character ↔ (U+2194)`.
- Zeilen mit "not found": 0.

## 5. Kosten (pm/kosten/ergebnis_LFP.json, ergebnis_NMC.json)
| | LFP | NMC |
|---|---|---|
| summe_eur_pack | 6556.83 € (6556.82540985816) | 8737.16 € (8737.162236589775) |
| summe_eur_je_kWh | 88.70 €/kWh (88.70164244937988) | 117.64 €/kWh (117.64053098949475) |
| energie_kWh | 73.92 | 74.27 |
| summe_vollstaendig | false | false |
| beleg_packpreis eur_je_kWh_berechnet | 89.24 (W29 BNEF 2024 BEV) | 89.24 (W29 BNEF 2024 BEV) |
