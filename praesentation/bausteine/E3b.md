> **KI-generiert** (Claude Sonnet, 2026-11-24), Entwurf. Folienbaustein Vorgang E3b.

# Das Wärmeleitpad hält die CMU-Platine kühl
**Kernaussage: Mit Wärmeleitpad zur gekühlten Wand bleibt die Platine bei rund 49 °C, ohne Pad wären es etwa 120 °C (Grenze 105 °C).**

**Bild:** sim/elektrik/e3b_platine_waerme/e3b_temperatur.png (Zielband: unter 105 °C, Grenze beschriftet)

**Zahlen** (Quelle sim/elektrik/e3b_platine_waerme/ergebnis.json, Block `vergleich`, feines Netz):
- T_max mit Pad und Vias: LFP 49,07 °C, NMC 48,93 °C
- T_max mit Pad ohne Vias: LFP 57,11 °C, NMC 56,69 °C
- T_max ohne Pad (Prüffall): LFP 120,30 °C, NMC 118,00 °C (über 105 °C)
- 94 bis 98 % der Wärme gehen über das Pad in die Wand
- Annahmen (Kupferlagen, Vias, Wand 45 °C) offen; Abgleich in sim/elektrik/e3b_platine_waerme/ERGEBNIS.md

*KI-generiert, Entwurf.*
