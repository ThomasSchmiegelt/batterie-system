| Dok.-Nr. | ERG-X1 | Version | 0.1 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Ergebnis X1: Seitenpfahl quasistatisch (CalculiX) | Ersteller | Claude Sonnet (KI) | Prüfer | Opus (offen) |

> **KI-generiert.** Claude Sonnet, 2026-11-18, Auftrag X1. Entwurf, nicht freigegeben. Alle Zahlen aus `sim/mechanik/x1_seitencrash/ergebnis.json` (Hauptnetz `m12`, Läufe in `lauf/<V>_<LF>_m12/`). Erwartung: `ERWARTUNG.md`. Pfahl Ø254 mm und Restkraft 100 kN sind **Annahmen** (W30 lieferte keine Normwerte).

## Was gerechnet wurde
Schalenmodell (S8R/S6, gmsh) des Seitenrahmens (Mehrkammerprofil 30 x 108 bzw. 102 mm, 3 Kammern, Wand 2,5 mm), 3 Querträger 26 x 54 x 2,5 (300 mm angeschlossen), Bodenstreifen 3 mm. Pfahl starr (Hex-Platte E x100), weggesteuert, reibungsfreier Kontakt, NLGEOM, Plastizität bilinear (260 MPa bei 0, 310 MPa bei 10 % PEEQ). Pfahlweg 6 mm (ab 0,5 mm Anfangsabstand), 4 Läufe (LFP/NMC x LF1/LF2) mit h = 12 mm nahe dem Pfahl, Netzstudie LFP LF1 mit h = 8 mm (nur bis 5 mm Weg).
LF1 = Pfahlmitte zwischen Querträger 1 und 2 (LFP x = 784, NMC x = 735 mm), LF2 = auf Querträger 2 (LFP x = 1031, NMC x = 975 mm).

## Zahlen bei Zellberührung (ergebnis.json, `läufe.<V>_<LF>.zellberuehrung_bei_spalt_mm`)
Zellberührung = größte y-Verschiebung der Rahmeninnenseite (außerhalb der Querträgerzonen, |x - x_Pfahl| < 500) erreicht den Spalt zur Zelle. Spalt aus dem CAD (eingaben.json `frei_weg`): LFP Zellverbinder 1 mm, Zellkörper 4 mm; NMC gerade Reihen **0 mm** (Zellen berühren die Rahmeninnenseite), ungerade 24 mm. Ausgewertet bei 1, 4 und 24 mm.

| Variante/LF | Spalt 1 mm: Weg, Kraft, Energie, PEEQ | Spalt 4 mm: Weg, Kraft, Energie, PEEQ |
|---|---|---|
| LFP LF1 | 1,04 mm, 28,9 kN, 18 J, 7,4 % | 4,14 mm, 61,2 kN, 164 J, 18,5 % |
| LFP LF2 | 1,07 mm, 30,5 kN, 19 J, 7,5 % | 4,22 mm, 62,9 kN, 174 J, 18,2 % |
| NMC LF1 | 1,04 mm, 29,0 kN, 18 J, 7,4 % | 4,15 mm, 62,2 kN, 166 J, 18,7 % |
| NMC LF2 | 1,08 mm, 31,1 kN, 20 J, 7,8 % | 4,23 mm, 64,4 kN, 178 J, 18,5 % |

Spalt 24 mm (NMC ungerade Reihen) wurde nicht erreicht (Rechnung bis 5,5 mm Pfahlweg). Ende (5,5 mm): Kraft 69,3 / 70,6 / 70,5 / 72,1 kN (LFP LF1, LFP LF2, NMC LF1, NMC LF2), Energie 253 / 260 / 256 / 265 J, PEEQ max 20,9 / 20,5 / 21,0 / 21,1 %, jeweils an der Unterseite des Rahmens (z ≈ 2,5 mm, y ≈ 5,8 mm) unter dem Pfahl.

## Abgleich mit der Erwartung
- LF1 Kraft 30-80 kN: **ERFÜLLT**, aber nur als Kraft nach 1-4 mm Weg (29-62 kN), nicht als Spitze nach 30 mm Weg.
- LF2 Kraft 80-150 kN: **VERFEHLT** (31-64 kN bei Berührung, 71 kN bei 5,5 mm). Das Modell schwächer als erwartet, der Querträger wird bis 5,5 mm nicht belastet (LF1 und LF2 fast gleich).
- Energie bei Zellberührung 1-3 kJ (LF1): **VERFEHLT**, 0,02 kJ (Spalt 1 mm) bis 0,17 kJ (4 mm). Verfehlt-Kriterium "< 0,5 kJ" eingetreten. Ursache: Der freie Weg im CAD ist nur 1 mm (LFP) bzw. 0 mm (NMC); der Rahmen gibt kaum Weg her, weil die Stege axial belastet werden.
- "NMC mehr freier Weg (41,6 mm)": **nicht bestätigt**. 41,6 mm ist der Reihenabstand in x (t·√3/2), kein Weg in y; im CAD berühren NMC-Zellen gerader Reihen die Rahmeninnenseite.
- PEEQ im Rahmen > 10 % bei Zellberührung (LF1): bei 1 mm 7,4 %, bei 4 mm 18,5 %: **Rissgefahr markieren** (ab etwa 1,5 mm Weg).
- Verfehlt-Kriterien: LF1 > 150 kN nein; LF1 < 15 kN nein; keine Konvergenz nein; Energie < 0,5 kJ **ja**.
- Die Restkraft 100 kN (Annahme) wird bis 5,5 mm Weg nicht erreicht (max. 72 kN); sie würde erst bei größerem Weg erreicht, der CAD-seitig nicht frei ist.

## Netzstudie (ergebnis.json `netzstudie_LFP_LF1`)
LFP LF1, Hauptnetz h = 12 mm gegen fein h = 8 mm, Kraft bei gleichem Pfahlweg: 1,4 mm 33,9 gegen 33,7 kN (0,6 %), 4,4 mm 63,1 gegen 63,0 kN (0,1 %). Grenze < 10 %: **ERFÜLLT**. PEEQ max bei 4 mm: 18,5 % (grob) gegen 18,2 % (fein). Nicht untersucht: sehr feines Netz an der Spitze der Dehnung (Schalenvereinfachung).

## Modellgrenzen (Opus prüfen)
1. Nicht im Auftrag festgelegte Modelldetails, vom Modell gesetzt und in `eingaben.json` (`modell_ausschnitt`) vermerkt: Rahmenenden (x = 0 und L) voll eingespannt, Querträgerenden und Bodenstreifenrand bei y = 300 voll eingespannt, Bodenstreifen 300 mm breit auf der ganzen Länge, Rahmen mit Gurten oben und unten und gleichmäßig verteilten Stegen (Kammerbreite 9,17 mm), kein Deckel, keine Kühlplatten, keine Zellen.
2. Kein Selbstkontakt: Falten des Rahmens können sich durchdringen. Bei 5,5 mm Weg unkritisch, für größere Wege nicht gültig.
3. Frame-Verformung und Pfahlweg sind klein (≤ 5,5 mm); große Wege (bis 30 mm) wurden nicht gerechnet. Grund: Rechenzeit (22 min für 5 mm bei 13200 Knoten, 8 Threads) und die Vorgabe "höchstens 30 min je Lauf, 120 min gesamt". Gesamtdauer Gesamtauftrag 2 h 50 min (inkl. Fehlversuch mit falschem Kontaktabstand, 1. Sitzung unterbrochen).
4. Bei Spalt 0 mm (NMC gerade Reihen) ist die Zellberührung sofort; die Tabelle gibt dann den kleinsten ausgewerteten Spalt 1 mm als Näherung an.
5. Kontaktpenalty 1e5 N/mm³ numerisch, nicht kalibriert. Lage der Maximaldehnung (Unterseite) hängt am Gurt-Kanten-Modell.

## Offene Fragen an Opus
- Spalt zwischen Rahmeninnenseite und Zelle (LFP 1 mm Verbinder / 4 mm Zelle; NMC 0 mm): ist der Entwurf so gewollt? Ohne mehr freien Weg kann das Pack keine Energie vor der Zellberührung aufnehmen (Energie < 0,5 kJ).
- Randbedingungen (Punkt 1) bestätigen oder ändern; danach ggf. größeren Weg rechnen (Dauer geschätzt 2-3 h bei 30 mm).
- Interpretation "Seitenrahmen 3 Kammern, Wand 2,5" (Annahme A_seitenrahmen_*) gilt für die Steifigkeit; Variante mit Vollprofil (CAD heute) würde steifer.

Dateien: `eingaben.json`, `eingaben_erzeugen.py`, `x1.py` (Netz, Deck), `auswerten.py`, `frd.py`, `lauf.sh`, `kette.sh`, `ergebnis.json`, `kraft_weg.png`, `verformung_<V>_<LF>.png`, `lesehilfe.md`, `lauf/` (Decks, Logs, frd).

*KI-generiert, Entwurf. Dokument ERG-X1, Version 0.1.*
