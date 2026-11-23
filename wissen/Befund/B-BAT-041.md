---
typ: befund
tags: ["befund"]
---
# B-BAT-041

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

E1 mit den G5-Längen und Freigabe der Kühlplatte (2026-11-22, Opus)

Quelle: [[Dokument/BEFUNDE]]

## Vorgänge
- –

## Text aus BEFUNDE.md

- Die HV-Leitung je Pol ist in G5 nur 779 mm lang (LFP) bzw. 679 mm (NMC). Die alte Annahme war die Gehäuselänge mit 2024 bzw. 1950 mm. Opus hat die Länge an der CAD-Masse nachgerechnet: 0,698 kg Cu bei 50 mm² ergeben 2 × 779 mm. Verlust LFP 105,2 → 73,0 W, damit ist die Grenze < 100 W jetzt **erfüllt**. NMC 385,4 → 364,5 W, die Grenze 300 W bleibt verfehlt. Die Erwartung (±30 %) war zu vorsichtig, weil die Schaltbox in G5 direkt am Stackende sitzt. Offen: Gruppenverbinder NMC im CAD 75 mm², in E1 45 mm² (sim/elektrik/e1_querschnitte/ERGEBNIS.md).
- Der Autor hat die Kühlplatte freigegeben (ENT-152 bis 156 entschieden): „muss aber optimiert werden“. Vorschlag ENT-158 ist Parallelführung mit Z-Verteiler plus gegenläufige Platten und Durchfluss ×3, Erwartung ΔT 6–8 K. Korrektur Opus: Parallelführung allein senkt die Kühlmittelaufwärmung nicht; sie wirkt über den kleineren Druckverlust, der mehr Durchfluss erlaubt.
