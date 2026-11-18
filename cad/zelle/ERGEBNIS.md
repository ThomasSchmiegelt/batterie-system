| Dok.-Nr. | ERG-G2 | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Ergebnis G2: parametrische Zelle LFP und NMC (Entwurfslauf) | Ersteller | Claude Sonnet (KI) | Prüfer | Opus (Modell und Bild) |

> **KI-generiert.** Entwurf, nicht freigegeben. Akten ENT-014…029 nur "vorgeschlagen". Quelle aller Zahlen: `cad/zelle/entwurf/ergebnis.json`.

## Was getan
`cad/zelle/entwurf_parameter.py` erzeugt `entwurf/parameter_<V>_entwurf.json` (Status entschieden + vorgeschlagen). `cad/zelle/zelle.py` baut daraus je Variante FCStd und STEP (FreeCAD 1.1.4 headless, `freecadcmd`). `zelle_bild.py` zeichnet die PNG aus der Tessellierung (matplotlib, da FreeCAD headless nicht rendert). `zelle_bericht.py` erzeugt dieses Dokument.

## Abgleich ERWARTUNG (cad/zelle/ERWARTUNG.md), Punkt für Punkt
| Nr | Erwartung | Ergebnis (Quelle) | Urteil |
|---|---|---|---|
| 1 | LFP 660 × 90 × 14 mm, 0,832 L, Wand 0,3 mm, zwei Pole an Stirnseiten, Polmaße Annahme, ≈ 355 Wh/L | 660 × 90 × 14 mm, Wand 0.3 mm, Außenvolumen 0.8316 L (-0.05 % gegen 0,832), 295.68 Wh → 355.6 Wh/L; Pole ANNAHME Ø 10.0 mm, 3.0 mm Überstand (`ergebnis_LFP.json`) | erfüllt (Abweichung < 1 %) |
| 2 | NMC Ø 46 × 80 mm, 0,133 L, Wand 0,4 mm, Plus oben, Minus Becherrand | Ø 46 × 80 mm, Wand 0.4 mm, Außenvolumen 0.13295 L (-0.04 % gegen 0,133), 85.56 Wh → 643.6 Wh/L; Pluspol ANNAHME Ø 12.0 mm, 1.0 mm (`ergebnis_NMC.json`) | erfüllt (Abweichung < 1 %) |
| 3 | Masse nicht aus CAD | Gehäusematerialvolumen LFP 41.67 cm³, NMC 5.87 cm³ nur als Kontrollgröße; keine Masse aus CAD | erfüllt |
| 4 | Modell liest nur parameter_<V>.json | Maße nur aus Parameterdatei; Test: Länge 700 mm in Kopie der Parameterdatei ergab ohne Codeänderung 0,882 L (Lauf im Scratchpad, nicht im Repo abgelegt). Fehlt ein Merkmal, bricht zelle.py ab (FEHLT). Im Code stehen nur ANNAHME_*-Konstanten (Pole) | erfüllt |
| 5 | STEP, PNG, Volumen in ergebnis.json | `zelle_LFP.step`, `zelle_NMC.step`, `zelle_LFP.png`, `zelle_NMC.png`, `ergebnis.json` | erfüllt |

Bounding Box mit Polen: LFP 666 × 90 × 14 mm (Pole stehen 3 mm je Seite über das Gehäuse; Annahme), NMC 46 × 46 × 81 mm. Wh/L bezieht sich auf das Gehäuseaußenvolumen ohne Pole (wie in der Erwartung).

## Offene Punkte (zurück an Opus)
- Polmaße sind Annahmen (keine Akte, keine Quelle). Vorschlag: eigene Akte oder Beleg suchen.
- Das Gehäuse ist ein leerer Hohlkörper (Innenaufbau BT-110 nicht modelliert). Material und Isolierfolie (ENT-023, ENT-028) sind nicht abgebildet.
- Die Pole im NMC-Bild zeigen kleine Darstellungsartefakte der Tiefensortierung (nur Bild, nicht Geometrie).
- `parameter_<V>.json` in pm/ enthält die Zellmaße noch nicht (nur Entwurfsdatei); Standardlauf von zelle.py bricht darum mit FEHLT ab, bis die Akten freigegeben sind.
- Nebenarbeit: `erzeuge_bericht.py` (C0b) erhält jetzt eine vorhandene Kernaussage. Die von Hand ergänzte Bauraum-Zeile in C0b.md wird vom Skript weiterhin überschrieben; ich habe C0b.md nach dem Testlauf aus der Sicherung wiederhergestellt (unverändert).


---
*KI-generiert (Claude Sonnet), Entwurf, nicht vom Menschen freigegeben.*
