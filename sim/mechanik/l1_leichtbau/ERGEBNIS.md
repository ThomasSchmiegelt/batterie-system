| Dok.-Nr. | ERG-L1 | Version | 0.1 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Ergebnis L1: Leichtbau-Potenzial des Packs (OPT-012), Studie ohne CAD-Änderung | Ersteller | Claude Sonnet (KI) | Prüfer | Opus (offen) |

> **KI-generiert** (Claude Sonnet, 2026-11-24). Entwurf, nicht freigegeben. Grundlage `ERWARTUNG.md` (ERW-L1, Opus, nicht geändert). Zahlen aus `ergebnis.json` in diesem Ordner (erzeugt von `leichtbau.py`, Eingang `cad/pack/entwurf/ergebnis_<V>_e2d_e3c.json` und `parameter_<V>.json`, nur gelesen). Die **Einsparspannen der Hebel sind Schätzungen von Opus** (ERWARTUNG.md), nicht gerechnet. Was aus der Geometrie folgt, ist als solches benannt. Es wurde kein CAD geändert.

## Was getan wurde
Massen der Gruppen ab 3 kg aus dem CAD-Ergebnis übernommen und aus Maßen und Dichten nachgerechnet (Plausibilität). Hebelspannen H1 bis H7 aus ERWARTUNG.md als Eingabe addiert (`ergebnis.json`, summe_spanne_kg, masse_neu_kg). Je Hebel zurückgerechnet, welcher Parameter die Spanne erfordern würde (rueckrechnung). Wasserfallbilder mit Zielband REQ-P07. **Band aus W51: offen** (`forschung/ergebnis/W51.md` fehlt, nur `W51.err` und `W51.jsonl` vorhanden, keine bestandene Zitatprüfung).

## Abgleich der Erwartungen
| Nr | Erwartung (ERWARTUNG.md) | Ergebnis (Quelle `ergebnis.json`) | Urteil |
|---|---|---|---|
| 1 | LFP −45…−75 kg → 545–575 kg (80–85 %); NMC −50…−85 kg → 400–430 kg (72–77 %) | Summe der Opus-Spannen LFP −44…−80 kg → **540…576 kg** (Zellanteil 80.3…85.7 %); NMC −49…−88 kg → **394…433 kg** (Zellanteil 71.1…78.1 %) | im Wesentlichen bestätigt; die Summen der Einzelspannen sind etwas breiter als die Erwartung (Rundung); die Spannen selbst sind ungeprüft (siehe Befunde 1, 2, 4) |
| 2 | LFP-Ziel 528 kg nur mit Cell-to-Pack; NMC 370 kg unerreichbar | LFP: auch mit der oberen Spanne 540 kg, Lücke zum Ziel 12…48 kg. NMC: Zellen allein 308 kg, für 370 kg blieben 62 kg Rest, der Rest wiegt heute 174 kg und müsste um 112 kg sinken (obere Spanne: Lücke 24…63 kg). LFP-Rest muss um 92 kg sinken | bestätigt (kein Ziel erreicht, auch nicht mit der oberen Spanne) |
| 3 | H1/H2 größte Hebel; H2 berührt Crash X3 und Dichtheit | H1 (15…25 kg) und H2 (10…20 kg) haben die größten Spannen (Summe 45 von höchstens 80 kg), aber nur nach Annahme Opus; **die Rückrechnung stellt H1 infrage** (Befund 1) | teilweise bestätigt (Rangfolge ja, Machbarkeit H1 unsicher) |

## Masse der Gruppen ab 3 kg und Nachrechnung (b)
Nachrechnung aus Maßen und Dichten (`parameter_<V>.json`, Block A), Abweichung gegen CAD-Masse; Grenze der Erwartung 5 %. Alle Gruppen liegen innerhalb. Bei Gruppenverbinder und Gruppenbrücke nur Volumen × Dichte Al (Konsistenzprüfung), keine Geometrienachrechnung.

**LFP** (Ist 619.8 kg, Zellen 462.5 kg, Rest 157.3 kg)

| Gruppe | CAD [kg] | nachgerechnet [kg] | Abw. [%] | Werkstoff (CAD) |
|---|---|---|---|---|
| Unterfahrschutz | 23.75 | 23.75 | 0.0 | Al |
| Boden | 23.75 | 23.75 | 0.0 | Al |
| Seitenrahmen | 21.79 | 21.79 | -0.0 | Al (Vollprofil, Obergrenze) |
| Kuehlplatte | 46.94 | 47.11 | 0.4 | Al (Vollmaterial, Obergrenze) |
| Pad | 13.53 | 13.63 | 0.8 | Pad |
| Deckel | 15.80 | 15.83 | 0.2 | Al |
| Quertraeger | 4.16 | 4.16 | 0.0 | Al |

**NMC** (Ist 482.4 kg, Zellen 308.1 kg, Rest 174.3 kg)

| Gruppe | CAD [kg] | nachgerechnet [kg] | Abw. [%] | Werkstoff (CAD) |
|---|---|---|---|---|
| Unterfahrschutz | 22.59 | 22.59 | 0.0 | Al |
| Boden | 22.59 | 22.59 | 0.0 | Al |
| Seitenrahmen | 20.08 | 20.08 | -0.0 | Al (Vollprofil, Obergrenze) |
| Kuehlplatte | 44.34 | 44.74 | 0.9 | Al (Vollmaterial, Obergrenze) |
| Pad | 12.61 | 12.95 | 2.7 | Pad |
| Deckel | 15.06 | 15.06 | 0.0 | Al |
| Zelltraeger | 3.07 | 3.07 | 0.0 | offen (Werkstoff/Dichte fehlt) |
| Verguss | 11.36 | 11.36 | -0.0 | offen (Dichte fehlt) |
| Quertraeger | 4.16 | 4.16 | 0.0 | Al |
| Gruppenverbinder | 7.94 | 7.94 | 0.0 | Al (Annahme, Cu offen) |
| Gruppenbruecke | 3.02 | 3.02 | 0.0 | Al (Annahme, Cu offen) |

Gruppen ohne Hebel in der Liste: Querträger (4,2 kg), NMC Zellträger (3,1 kg), Gruppenverbinder (7,9 kg), Gruppenbrücke (3,0 kg). Die Verbinder sind als Al angenommen, „Cu offen“ (`ergebnis_NMC_e2d_e3c.json`).

## Befunde (Abweichungen zur Erwartung, an Opus)
1. **Kühlplatte (H1):** Die 46,9 kg (LFP) sind **nicht 6 mm vollflächig**, sondern Hüllmaß 8 mm (ENT-090) × Füllgrad 0,4 (Annahme Opus 2026-11-17: 2 Bleche je 1,5 mm + Kanalstege) = äquivalent 3.2 mm Al je Platte. 6 mm vollflächig wären 88.3 kg. Für −15…−25 kg müsste der Füllgrad auf 0.27…0.19 fallen, das heißt äquivalent 2.2…1.5 mm. Der Ist-Ansatz liegt bereits bei zwei Blechen mit zusammen 3,0 mm plus Stegen; die Spanne verlangt dünnere Bleche **und** Stege. Ob das tragfähig und dicht ist, ist ungeprüft. Die Spanne H1 ist damit wahrscheinlich zu hoch (Opus entscheiden).
2. **Seitenrahmen (H6):** Der Ist-Wert ist **bereits** ein Mehrkammerprofil (Faktor 0.36 gegen Vollprofil 59.8 kg; Wand 2,5 mm, 3 Kammern). Die Spanne −5…−10 kg verlangt Wand 1.91…1.33 mm (LFP), also unter dem W22-Bereich 2–3 mm. Mit 2,0 mm Wand: 17.6 kg (−4.2 kg).
3. **Unterfahrschutz (H3):** Im CAD ist er **Al, 3 mm** (`ergebnis_LFP_e2d_e3c.json`, werkstoff Al), nicht Stahl. Der Hebel „Stahl hochfest dünner“ ist daher ein Werkstoffwechsel; die Dichte von Stahl steht nicht in den Akten, deshalb keine Rechnung (neue Annahme, Opus). Die Spanne entspricht 21…42 % der Masse, bei Al äquivalent 2.37…1.74 mm.
4. **Pad (H5):** Aus der Geometrie: Fläche des Pads 27058 cm² gegen Zellfußfläche 23835 cm² (LFP) bzw. 25217 gegen 14425 cm² (NMC). „Nur unter den Zellen“ spart LFP **1.6 kg** (−12 %), NMC **5.4 kg** (−43 %), gegen Spanne 4…7 kg: LFP liegt darunter, NMC in der Spanne. „Dünner“ als 1 mm ist ohne Wärmeleitwert nicht zu bewerten (Annahme fehlt).
5. **Verguss (H7):** Ist bereits nur bis halbe Zellhöhe (Anteil 0.50, Annahme AUFTRAG G4). Die Spanne −5…−8 kg verlangt Anteil 0.28…0.15. Dichte 300 kg/m³ ist Annahme (PU-Schaum), die Masse wirkt klein gegen Zellmasse, die Sicherheitsfunktion (Propagation) ist nicht gerechnet.
6. **Boden (H2):** Boden ist Al, 3 mm, 23.7 kg; die Spanne −10…−20 kg entspricht 42…84 % des Bodens. Entfällt der Boden ganz, sind es höchstens 23.7 kg (ohne Verstärkung der Kühlplatte); dazu entfallen 3 mm Boden + 5 mm Luft = 8 mm Bauhöhe (Stapel 121 mm, Grenze 130 mm). **H1 und H2 sind nicht additiv:** trägt die Kühlplatte, muss sie dicker werden, das widerspricht H1.
7. **Anforderungsnummer:** Die Erwartung nennt Crash als REQ-P13; im Lastenheft ist REQ-P13 Schutzart/Isolation, **Crash ist REQ-P14** (`docs/01_lastenheft.md`). Hier wird REQ-P14 verwendet.
8. **H4 (Deckel):** Werkstoffdichte Verbund (SMC) steht nicht in den Akten; nur Rückrechnung: Spanne = 32…51 % der Deckelmasse.

## Tabelle je Hebel
Spalte kg: Spanne Opus (ERWARTUNG.md), LFP / NMC. Kosten, Sicherheit, Effizienz und Folgen sind **qualitative Einschätzungen von Sonnet ohne Rechnung**, Prüfung Opus (+ besser, 0 neutral, − schlechter, ? offen). Folge Thermik und Crash sind **nicht nachgewiesen**, sondern Prüfaufträge.

| Hebel | kg LFP / NMC | Rückrechnung (Quelle `ergebnis.json`) | Kosten | Sicherheit | Effizienz | Folge Crash (REQ-P14) / Thermik (REQ-P09) / Fertigung |
|---|---|---|---|---|---|---|
| H1 Kühlplatte dünner/Strangpressprofil | −15…25 / −15…25 | Füllgrad 0.40 → 0.27…0.19 | + (weniger Al; Strangpressprofil: Werkzeug) | − (Dichtheit, Beulen, Druck) | + (Masse) | Crash: Platte ist Teil der Last (Pfahl) → X3 prüfen; Thermik: Kanalquerschnitt und Druckverlust → K-Rechnung neu; Fertigung: Strangpress/Löten |
| H2 Boden + Kühlplatte zusammenlegen | −10…20 / −10…20 | 42…84 % des Bodens (LFP); höchstens 23.7 kg; Höhe −8 mm | + (weniger Teile) | − (IP67, Aufsetzen, Kühlmittel am Außenrand) | + (Masse, Höhe) | Crash: Boden ist heute die zweite Schale hinter dem Unterfahrschutz → X3 (Boden); Dichtheit: Schweiß-/Dichtnaht außen; nicht additiv mit H1 |
| H3 Unterfahrschutz dünner/Verbund | −5…10 / −5…10 | 21…42 %, äquiv. Al 2.37…1.74 mm; Ist Al, nicht Stahl | ? (Werkstoff) | − (Steinschlag, Aufsetzen REQ-P14) | + | Crash: Aufsetzen/Pfahl → X3; Thermik 0; Fertigung: neuer Werkstoff |
| H4 Deckel aus Verbund (SMC) | −5…8 / −5…8 | 32…51 % der Deckelmasse | ? | ? (Brandschutz, Druckentlastung, Schirmung EMV) | + | Crash gering; Thermik: Wärme/Flamme nach oben, Entgasungsweg → prüfen; EMV: Al schirmt, Verbund nicht |
| H5 Pad nur unter den Zellen/dünner | −4…7 / −4…7 (Geometrie: −1.6 / −5.4) | Fläche 12 % (LFP) / 43 % (NMC) | + | 0 (dünner: − Toleranzausgleich) | + (Masse); dünner: − Wärmepfad prüfen | Thermik: Kontaktfläche nur unter Zellen; Spalt zwischen Zellen ohne Pad → K0/K1 neu |
| H6 Seitenrahmen Kammerprofil | −5…10 / −5…10 | Ist bereits Kammerprofil; Wand 1.91…1.33 mm (LFP) | 0 | − (Seitencrash, Wand unter W22-Bereich 2–3 mm) | + | Crash: Seitenpfahl, Quetschung → X1; Thermik 0; Fertigung: Strangpress, dünnwandig |
| H7 NMC Verguss nur oben | – / −5…8 | Anteil 0.50 → 0.28…0.15 (Ist schon halbe Höhe) | + | − (Propagation, Fixierung bei Crash) | + | Thermik: Verguss bremst Propagation → Nachweis nötig; Crash: Zellfixierung; Fertigung: weniger Schaum |

## Offen
- Band aus W51 (Serien-Zellanteil): `forschung/ergebnis/W51.md` fehlt, nicht eingetragen.
- Neue Annahmen nötig (nicht getroffen): Dichte Stahl und SMC (H3, H4); Wärmeleitwert Pad und Mindestdicke (H5); Mindestwand Kühlplatte (H1); Mindestwand Seitenrahmen unter 2 mm (H6).
- Die Spannen H1, H3, H6 sind laut Rückrechnung ohne Annahmen außerhalb der Liste nicht belegbar; Opus entscheidet, ob sie gelten oder gesenkt werden.
- Crash- und Thermikfolgen sind Prüfaufträge, nicht nachgewiesen. Das CAD bleibt unverändert (REQ-P07 Ziel nicht neu festgelegt).

*KI-generiert (Claude Sonnet, 2026-11-24), Entwurf, nicht freigegeben.*
