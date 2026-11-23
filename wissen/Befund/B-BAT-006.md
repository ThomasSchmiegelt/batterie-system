---
typ: befund
tags: ["befund"]
---
# B-BAT-006

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

B-BAT-006 (2026-11-16) Chemievergleich LFP/NMC bei 1500 kg und 400 km: kein belegter Massenunterschied

Quelle: [[Dokument/BEFUNDE]]

## Vorgänge
- [[Vorgang/V1|V1]] – Lastenheft-Werte REQ-P01..P08 vorschlagen (Fahrzeug, kWh, Spannung, Leistung, Laden, Chemie, Bauraum, Temperatur)

## Text aus BEFUNDE.md

- Rechnung `sim/chemie/vergleich_lfp_nmc/` (Sonnet nach Auftrag, 2 min; Opus-Gegenrechnung mit eigenem Skript gleich). Erwartung (ERWARTUNG.md, vorher) Punkte 1–6 erfüllt.
- Fall A (1500 kg mit Batterie): 73,9 kWh brutto. Packmasse LFP 499 kg (414–615), NMC 464 kg (316–758). Batterieanteil 33,3 % bzw. 30,9 %, beide über der Annahme 30 %.
- Fall B (1500 kg ohne Batterie): 88,7 bzw. 87,4 kWh brutto (+20 %/+18 %, 6 Iterationsschritte). Packmasse 599 bzw. 549 kg, Anteil 28,5 % bzw. 26,8 %.
- Zyklenbedarf 1000: LFP erfüllt, NMC unsicher. Zellen in Reihe bei 800 V: 250 / 220. Bauraum (214 Wh/L nötig): für LFP offen.
- Stärkste Annahme: LFP Zellanteil am Pack (Hub 196 kg), NMC Zellband (Hub 434 kg).
- Folge: Vorschlag ENT-005 LFP-Blade als Hauptvariante. Die NMC-Wahl in startwerte.py beruhte auf einer unbelegten Annahme. Rückfrage an den Autor: 1500 kg mit oder ohne Batterie? Vorgang: [C0] [V1]
