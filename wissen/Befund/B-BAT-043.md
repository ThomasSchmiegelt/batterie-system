---
typ: befund
tags: ["befund"]
---
# B-BAT-043

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

Parallelführung mit Z-Verteiler in der Platte funktioniert nicht (2026-11-23, Opus)

Quelle: [[Dokument/BEFUNDE]]

## Vorgänge
- –

## Text aus BEFUNDE.md

- Die Verteilerrechnung (Sonnet, sim/kuehlung/k5_parallel) zeigt: Die Platte hat 120 Kanäle mit zusammen 3 840 mm² Querschnitt. Ein Sammler in Kanalhöhe (25 × 4 mm = 100 mm²) verteilt das Kühlmittel extrem ungleich, einzelne Kanäle bekommen bis zum 11-Fachen des Mittels, mittlere fast nichts. Bei Durchfluss ×3 steigt Δp auf 0,44 bar.
- Fehler von Opus: Beim Schreiben der Erwartung hatte Opus wenige breite Bahnen vor Augen statt 120 einzelner Kanäle. Die Erwartung war klar verfehlt, Sonnet brach deshalb ab, wie im Auftrag vorgesehen, ohne die Erwartung anzupassen.
- Neue Variante: k parallele kurze Mäander aus einem außen liegenden Verteilerrohr (ERWARTUNG Nachtrag 1). ENT-158 muss danach überarbeitet werden.
- K5 gerechnet (23.11.): Mit k = 2 parallelen Mäandern aus einem Rohr Ø 25 weicht die Verteilung um höchstens 2 % ab, Δp liegt bei ×3 bei 0,171 bar. K4 LFP: ΔT 7,6 K, T_max 34,1 °C. NMC: ΔT 1,3 K. Opus hat Re (etwa 1100) und Δp (Schätzung 0,16 bar) im Kopf nachgerechnet, beides passt. ENT-158 ist überarbeitet (wert gruppiert_k2). Offen für den Autor: ob ΔT ≤ 5 K die Spreizung zwischen den Zellen meint oder auch das Gefälle innerhalb einer Zelle.
- G5.9 im CAD (Sonnet, 23.11.): 0 Kollisionen, Breite 1430 mm, Länge +38 mm (LFP 2373, NMC 2273 mm), Platte −0,22 kg, je 2 Verteiler- und Sammelrohre Ø 25 zusammen 0,49 kg, Kosten +0,16 % (LFP) bzw. +0,11 % (NMC). Alles im Erwartungsband G5.9. Abweichung von der Rechnung: Die Platten sind im CAD nicht gegenläufig geschaltet, sondern parallel. Deshalb wird V4p ohne Gegenlauf nachgerechnet (K5 Nachtrag 2). Opus hat angenommen: Rohre übereinander, Deckelschrauben weichen seitlich aus (benannte Annahme).
- V4p wie gebaut (ohne Gegenlauf): LFP ΔT 9,6 K, T_max 35,6 °C, im Band. NMC ΔT 2,6 K, Erwartung < 2 K verfehlt; Ziel NMC ≤ 5 K aber erfüllt. Der Gegenlauf bringt bei LFP 2,0 K, bei NMC 1,3 K. Bei NMC wirkt er stärker als erwartet, vermutlich weil das Gefälle in der Zelle dort klein ist und die Kühlmittelaufwärmung den größeren Anteil hat (Deutung Opus). Der Gegenlauf im CAD wird zum Verbesserungsvorschlag (Grenze von Nachtrag 2: 2 K). Sonnet fand dabei einen Skriptfehler: V_GEGEN wurde im Parallelzweig nie abgefragt. Der erste V4p-Lauf wurde verworfen.
- Masse (23.11., Opus beim Prüfen der Stücklisten-Tabellen): Auf Stand G5.9 wiegt LFP 626,8 kg und überschreitet das Zielband 560–620 kg knapp. Die Zusammenfassung des Berichts nannte noch 619,8 kg (Stand E2D). NMC 486,4 kg (Band 390–430 kg). Korrigiert im Bericht, Masse kommt in die Verbesserungen.
