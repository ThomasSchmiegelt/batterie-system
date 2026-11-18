| Dok.-Nr. | LH-K1 | Version | 0.1 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Lesehilfe zu den K1-Bildern (Schnellladen) | Ersteller | Claude Sonnet (KI), Auftrag Opus | Prüfer | – (Opus offen) |

> **KI-generiert.** Entwurf, nicht vom Menschen freigegeben. Quelle aller Zahlen: `sim/kuehlung/k1_schnellladen/ergebnis.json` (erzeugt von `k1_auswertung.py` aus `elmer/fall_*/`). Vorgaben T_max ≤ 45 °C und Spreizung ≤ 5 K sind Annahmen (REQ-P09 offen).

**Lesehilfe zu `profile.png`** Oben: wie stark die Zelle mit welchem Strom geladen wird (in C: 1C lädt die Zelle in einer Stunde voll, 2C in 30 Minuten). Unten: wie der Ladezustand dabei von 10 auf 80 % steigt. Alle fünf Ladeprofile (P0 bis P4) laden denselben Hub; sie unterscheiden sich in Höhe und Verlauf des Stroms und damit in der Ladedauer (20, 25 oder 30 Minuten). Die gezackte Linie P2 ist das Wechselladen: halbe Zeit doppelter Strom, dazwischen Pause. Je höher der Strom, desto mehr Wärme entsteht in der Zelle (Wärme wächst mit dem Quadrat des Stroms).

**Lesehilfe zu `verlauf_profile_LFP.png`** Oben die höchste Temperatur in der Zelle über die Ladezeit, unten der Temperaturunterschied zwischen heißester und kühlster Stelle im Zellkern (Spreizung). Der grüne Bereich ist das Zielband: darunter ist die Vorgabe erfüllt (45 °C bzw. 5 K, Linie beschriftet). Fünf Ladeprofile, LFP-Zelle, Kühlung am Boden. Die Spitzenwerte stehen in der Legende. Kurven, die in den grünen Bereich passen, halten die Vorgabe ein.

**Lesehilfe zu `verlauf_profile_NMC.png`** Wie das LFP-Bild, aber für die runde 4680-Zelle (NMC). Grüner Bereich = Zielband, Linie = Vorgabe 45 °C bzw. 5 K.

**Lesehilfe zu `verlauf_kuehlung_LFP.png`** Wie die Profilbilder, aber für Kühlvarianten bei gleichem Ladeprofil P0 (konstant 2,1C): mehr Wärmeübergang am Boden (h 1000, h 2000), Kühlung auf zwei gegenüberliegenden Seiten (K3), Vorkühlung auf 15 °C (V15), dazu gestrichelt zwei Kombinationen mit Stufenprofil bzw. K3 und h 1000. Grüner Bereich = Zielband. Man sieht, welche Maßnahme die Temperatur und welche die Spreizung senkt.

**Lesehilfe zu `verlauf_kuehlung_NMC.png`** Wie das LFP-Bild, für die 4680-Zelle; zusätzlich die Kombination Profil P3 mit h 2000.

**Lesehilfe zu `landkarte.png`** Übersicht aller gerechneten Fälle (Zeilen) für beide Zellarten (Spalten). Jedes Feld zeigt den Spitzenwert über die Ladezeit; grün = Vorgabe eingehalten (T_max ≤ 45 °C bzw. ΔT ≤ 5 K), rot = verfehlt. Die Spalte „Ampel“ fasst je Zelle beide Vorgaben zusammen: grün = beide erfüllt, gelb = nur eine, rot = keine. Graue Felder: nicht gerechnet.
