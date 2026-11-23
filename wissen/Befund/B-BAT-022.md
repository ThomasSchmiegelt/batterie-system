---
typ: befund
tags: ["befund"]
---
# B-BAT-022

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

B-BAT-022 (2026-11-17) C1 Zellmodell: NMC bestätigt K1, aber 10→80 % erst in 36 min; LFP-Parametersatz passt nicht

Quelle: [[Dokument/BEFUNDE]]

## Vorgänge
- [[Vorgang/R3|R3]] – Patente P01-P10
- [[Vorgang/C1|C1]] – ERWARTUNG Zellmodell (Entladekurve, Wärme, Innenwiderstand)

## Text aus BEFUNDE.md

- PyBaMM (Sonnet): NMC Chen2020 23,19 Ah, DCIR 6,4 mΩ, Wärme 6,9 W (K1 6,7 W ✓). CC-CV: 4,2 V nach 21,8 min, 80 % nach 36,2 min → REQ-P05 (30 min) mit diesem Satz verfehlt (Satz ist 21700, nicht 4680).
- LFP Prada2013: halbe Beladung, Skalierung ×1,9 → DCIR 0,76 mΩ, Wärme 32,8 W gegen Messung 1,46 mΩ / 55 W. K1 bleibt bei Messung. → C2 Kalibrierung (Blade-Pulsdatensatz quellen/blade_datensatz). DEUTUNG.md. Vorgang: [C1]
