---
typ: befund
tags: ["befund"]
---
# B-BAT-012

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

B-BAT-012 (2026-11-17) G1-Vorprüfung Zellanordnung: LFP-Blade passt nur ohne Zwischenraum, NMC-4680 mit Reserve

Quelle: [[Dokument/BEFUNDE]]

## Vorgänge
- [[Vorgang/G1|G1]] – Zellmaße als ENT-Akten (aus W03/W08/P01, sonst Annahme)
- [[Vorgang/G4|G4]] – Pack: Zellanordnung, Querträger, Kühlplatte, Deckel

## Text aus BEFUNDE.md

- Rechnung sim/geometrie/g1_anordnung/ (Sonnet; Opus Bild angesehen, Zählung NMC nachvollzogen: 32 Reihen × ~38 = 1200 Plätze).
- LFP A: 92,4 Ah → Zelle 660 × 90 × 14 mm, zwei Reihen quer (1320 ≤ 1340 mm). 125 Zellen je Reihe = 1874 mm gegen 1840 mm innen: passt nicht bei 1 mm Abstand; Grenze 0,73 mm. Blade-Zwischenlage (BT-220) und Wärmeschutz haben so keinen Platz. Höhe 120/130 mm passt.
- LFP B: 116,2 Ah → 831 mm, passt in keiner Lage. (Erwartung nannte 111 Ah/790 mm: Opus hatte die C0-Energie statt der C0b-Energie 93,0 kWh eingesetzt; Urteil unverändert.)
- NMC A: 868 von 1200 Plätzen (72 %), Höhenreserve 20 mm; NMC B: 1085 (90 %).
- Folge: Bestätigt C0b geometrisch. LFP braucht mehr Länge (≥ 1,93 m bei 1 mm), dünnere Rand-Annahme oder Fall A mit kleinerer Reichweite. Annahmen Rand 30 mm / Höhen bestätigt unkritisch; kritisch nur der LFP-Zellabstand. Vorgang: [G1] [G4]
