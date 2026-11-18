| Dok.-Nr. | ERG-G1 | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Ergebnis G1-Vorprüfung Zellanordnung | Ersteller | Claude Sonnet (KI) | Prüfer | Opus (Rohdaten) |

> **KI-generiert.** Claude Sonnet, 2026-11-17, Auftrag G1-V. Entwurf, nicht vom Menschen freigegeben. Quelle aller Zahlen: `sim/geometrie/g1_anordnung/ergebnis.json` (aus `eingaben.json` durch `anordnung.py`).

## Ergebnis (Basiswerte)
Bauraum 1950 x 1430 x 130 mm, Rand 30 mm je Seite, Innen 1890 x 1370 mm; Höhe unten/oben 20/10 mm. Alle Randwerte sind Annahmen (`eingaben.json`).

| Variante | Fall | Zelle | Anordnung | Reserve in mm | Urteil |
|---|---|---|---|---|---|
| LFP | A | 92.4 Ah, 681 mm | Länge quer (B), 2 Reihen x 125 | L 16 / B 8 / H 10 | passt |
| LFP | B | 116.2 Ah, 840 mm | gedreht, Länge in L, 2 Reihen x 125 | L 210 / B -504 / H 10 | passt nicht |
| NMC | A | 868 Zellen | 1260 Plätze (Reihen entlang B), 69 % belegt | Plätze 392 / H 20 | passt |
| NMC | B | 1085 Zellen | 1260 Plätze (Reihen entlang B), 86 % belegt | Plätze 175 / H 20 | passt |

Reserve negativ = fehlt. LFP: Stapellänge n Zellen = n*Dicke + (n-1)*Abstand. Beide Lagen (quer und gedreht) wurden geprüft, die bessere ist angegeben. Bild: `anordnung.png`, Lesehilfe: `anordnung_lesehilfe.md`.

## Empfindlichkeit (je Annahme einzeln auf Bandende)
| Annahme | Basis | Bandwert | kippt Urteil |
|---|---|---|---|
| rand | 30 | 20 | - |
| rand | 30 | 50 | LFP_A |
| gap_lfp | 1.0 | 0.5 | - |
| gap_lfp | 1.0 | 2.0 | LFP_A |
| gap_nmc | 2.0 | 1.0 | - |
| gap_nmc | 2.0 | 3.0 | - |
| h_unten | 20 | 15 | - |
| h_unten | 20 | 30 | - |
| h_oben | 10 | 5 | - |
| h_oben | 10 | 15 | - |

Kippende Annahmen: gap_lfp kippt LFP_A; rand kippt LFP_A.

## Abgleich ERWARTUNG.md Punkt für Punkt
- ERFÜLLT: 1a LFP A Länge 680-682 mm (Erwartung Nachtrag Lauf 3: 681). Ist: 681.0 mm (92.4 Ah)
- ERFÜLLT: 1b zwei Reihen quer, 2 x Länge <= B innen (Nachtrag Lauf 3: 1362 <= 1370). Ist: 2 Reihen, Reserve B 8 mm
- ABWEICHUNG: 1c bei 1 mm Abstand passt knapp NICHT in L (125 Zellen). Ist: 125 Zellen je Reihe, Stapel 1874 mm, Reserve L 16 mm (Erwartung rechnete 125 x 15 = 1875; hier n*14+(n-1)*1 = 1874)
- ERFÜLLT: 1d bei 0,5 mm Abstand passt es. Ist: Stapel 1812 mm, Reserve L 78 mm, passt=True
- ERFÜLLT: 1e Höhe 120 <= 130 passt. Ist: 120 mm, Reserve 10 mm
- ERFÜLLT: 2 LFP B passt nicht (nicht verfehlt, wenn passt=False). Ist: Zelle 840 mm (116.2 Ah bei 93.0 kWh; Erwartung nannte 111 Ah/790 mm), beste Lage gedreht, Länge in L, passt=False
- ERFÜLLT: 3a NMC A Plätze 1100-1300 (Erwartung etwa 1200). Ist: 1260 Plätze (28/28 je Reihe, 45 Reihen)
- ERFÜLLT: 3b NMC A passt mit Reserve, rund 70 % belegt. Ist: 69 % belegt, passt=True
- ERFÜLLT: 3c NMC A Höhe 110 mm, 20 mm frei. Ist: 110 mm, Reserve 20 mm
- ERFÜLLT: 4 NMC B passt knapp (1085 <= etwa 1200). Ist: 1085 auf 1260 Plätzen = 86 %
- ERFÜLLT: 5 stärkste Annahme: LFP Zellabstand/Rand, NMC Zellabstand. Ist: Kipper: gap_lfp kippt LFP_A; rand kippt LFP_A
- Verfehlte-Erwartung-Kriterien (ERWARTUNG.md): keines eingetreten

## Offene Punkte
- Die Erwartung nennt für LFP Fall B 111 Ah / etwa 790 mm; `eingaben.json` gibt E = 93.0 kWh (B_LFP), das ergibt 116.2 Ah / 840 mm. Das Urteil „passt nicht“ ändert sich dadurch nicht. Opus prüft, welcher Wert gelten soll.
- Gemischte Anordnungen (Zellen in zwei Lagen, Restreihen) und Zellverbinder-/Kühlplatzbedarf sind nicht modelliert.

*KI-generiert, Entwurf. Dokument ERG-G1, Version 1.0.*

## Lauf 3 (Längenregel mit fester Endzone, Bauraum 1950 x 1430 mm)
KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. Längenregel `laenge_regel` aus `eingaben.json`: Elektrodenlänge ∝ Ah plus feste Endzone (65.5 mm). Lauf-2-Stand: `ergebnis_lauf2.json` (Bauraum 1950 x 1400 mm).

| Größe | Lauf 2 | Lauf 3 |
|---|---|---|
| LFP A | 92.4 Ah, 660 mm, passt (Reserve L 16 / B 19) | 92.4 Ah, 681 mm, passt (Reserve L 16 / B 8) |
| LFP B | 116.2 Ah, 831 mm, passt nicht (Reserve L 228 / B -534) | 116.2 Ah, 840 mm, passt nicht (Reserve L 210 / B -504) |
| NMC A | 868 / 1232 Plätze = 70 %, passt | 868 / 1260 Plätze = 69 %, passt |
| NMC B | 1085 / 1232 Plätze = 88 %, passt | 1085 / 1260 Plätze = 86 %, passt |

Abgleich mit dem Nachtrag in `ERWARTUNG.md` (Lauf 3):
1. LFP A Zelle 681 mm, zwei Reihen quer 1362 ≤ 1370 mm, Reserve B etwa 8 mm, L 16 mm: Ist 681.0 mm, 2 Reihen, belegt 1362.0 mm, Reserve B 8.0 mm, L 16 mm: **erfüllt**
2. LFP B Zelle etwa 840 mm, passt weiter nicht: Ist 840 mm, passt nicht: **erfüllt**
3. NMC etwa eine Reihe mehr (etwa 1270 Plätze), Belegung A etwa 68 %: Ist 1260 Plätze (Lauf 2: 1232), 69 % belegt: **erfüllt** (Erwartung nannte etwa 1270, gerechnet 1260)
Verfehlt-Kriterium des Nachtrags (LFP A passt nicht): nicht eingetreten.

