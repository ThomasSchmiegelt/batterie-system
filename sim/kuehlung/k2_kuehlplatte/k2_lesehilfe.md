| Dok.-Nr. | LH-K2 | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Lesehilfe zu den Bildern K2 | Ersteller | Claude Sonnet (KI) | Prüfer | Opus (offen) |

> **KI-generiert** (Claude Sonnet, 2026-11-17), Entwurf, nicht von Opus geprüft. Quelle aller Zahlen: sim/kuehlung/k2_kuehlplatte/ergebnis.json (Skript kuehlplatte.py, Eingaben eingaben.json).

**Lesehilfe zu durchfluss_druck.png.** Oben der Druckverlust, unten der Wärmeübergang (h) im Kanal, jeweils über der Menge Kühlmittel, die pro Minute durch das ganze Pack fließt. Links LFP, Mitte und rechts die 4680-Zelle (NMC) in zwei Ladefällen. Jede Linie ist eine Kanalbreite (Farbe) und Führung (durchgezogen quer, gestrichelt längs); Punkte markieren die Kühlmittelerwärmung 5, 8 und 10 K. Grün ist das Zielband (Annahme aus ERWARTUNG.md): oben höchstens 0,5 bar, unten h mindestens 500. Rot ist verfehlt (über 1 bar, unter h 300). Der Druckverlust liegt weit im grünen Bereich (Achse logarithmisch), h aber im roten bis weißen Bereich unter dem Ziel. Ein höherer Durchfluss verbessert h kaum, weil die Strömung laminar ist.

**Lesehilfe zu platte_LFP.png und platte_NMC.png.** Draufsicht auf eine der beiden Kühlplatten maßstäblich: viele parallele Kanäle (blau) zwischen Vorlauf (unten) und Rücklauf (oben), Stege weiß. Die Zahlen im Titel stammen aus ergebnis.json. Die gezeigte Variante (20 mm quer, ΔT 5 K) hat das höchste h der Rechnung und verfehlt das Ziel trotzdem.

---
*KI-generiert (Claude Sonnet, 2026-11-17), Entwurf.*

**Lesehilfe zu nachtrag_U_leistung.png.** Jeder Punkt ist eine Bauvariante (Farbe Kanalbreite, Kreis 5 mm Höhe, Dreieck 3 mm). Waagerecht steht die Pumpenleistung (logarithmisch, nur Varianten unter 0,5 bar), senkrecht der Gesamtwärmedurchgang von der Zelle über Pad und Blech ins Kühlmittel, bezogen auf die Plattenfläche. Oberhalb der grünen Linie (500, Annahme aus K0/K1) ist das Ziel erreicht. Je weiter links, desto weniger Pumpenleistung. Der schwarze Ring ist die Auswahl für ΔT ≤ 5 K.


**Lesehilfe zu k2b_U_dp.png.** Jeder Punkt ist eine Bauvariante der Blechplatte 1/4/1 mm mit Mäander (Farbe = Zahl der Bahnen n). Waagerecht steht der Druckverlust je Platte (logarithmisch), senkrecht der Gesamtwärmedurchgang U von der Zelle ins Kühlmittel. Das grün schattierte Feld oben links ist das Zielband (U mindestens 500, Druckverlust höchstens 0,5 bar, Annahmen aus ERWARTUNG.md). Je weiter links und höher ein Punkt, desto besser. Der schwarze Ring ist der Vorschlag mit dem kleinsten Druckverlust im Zielband. Links LFP (23 L/min je Pack), rechts NMC (20 L/min). Quelle: ergebnis_k2b.json.
