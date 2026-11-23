---
typ: befund
tags: ["befund"]
---
# B-BAT-047

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

Wissensgraph: erste Lückenliste und Abweichungen CAD gegen Stückliste (2026-11-23, Opus)

Quelle: [[Dokument/BEFUNDE]]

## Vorgänge
- –

## Text aus BEFUNDE.md

- Die Probe `folgen BT-000.bauraum_laenge_mm` findet K5, k3_gesamt, x1 und x1b. Dafür war Schema-Nachtrag 1 nötig (CAD-Lauf-Knoten). Ohne diesen Knoten hätte der Graph die veraltete K5-Rechnung nicht gefunden.
- Eingaben sind jetzt bei 15 von 16 Rechnungen als `eingaben_graph.json` erfasst, aus wörtlichen Verweisen in den Skripten. Ein Name im Skript ist noch kein Beleg für eine Eingabe, die Prüfung durch Opus steht aus. Die REQ-Zuordnung steht bei allen 16 Rechnungen, 4 davon hat Opus zugeordnet.
- Massenabgleich: Die Gesamtmasse CAD gegen Stückliste liegt unter 2 %, aber 29 Positionen weichen um mehr als 2 % ab. Beispiele: Stromschiene 440.2 +282/+305 %, Schrauben 590.1 +318/+323 %, Pol-Lasche 440.1 −72 %, Verguss und Zellträger NMC rund −60 %, Schaltbox 700.1 +41/+38 %. Die Summe stimmt nur, weil sich Fehler ausgleichen. Das wird ein Punkt für Schleife 2: die Stückliste aus der CAD-Geometrie ableiten.
- Merkmale, die eine Rechnung verwendet, ohne dass eine Akte sie festlegt: BT-210.zellen_je_reihe, BT-250.zellabstand_mm. Beide gehen in die Freigaberunde.
