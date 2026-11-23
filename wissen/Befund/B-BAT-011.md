---
typ: befund
tags: ["befund"]
---
# B-BAT-011

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

B-BAT-011 (2026-11-16) Variantenvergleich mit Messwerten: NMC-4680 ein Drittel leichter, LFP-Blade im Bauraum knapp

Quelle: [[Dokument/BEFUNDE]]

## Vorgänge
- [[Vorgang/V1|V1]] – Lastenheft-Werte REQ-P01..P08 vorschlagen (Fahrzeug, kWh, Spannung, Leistung, Laden, Chemie, Bauraum, Temperatur)
- [[Vorgang/G3|G3]] – Verschaltung sS/pP aus Spannung und Energie festlegen (ENT)

## Text aus BEFUNDE.md

- Rechnung sim/chemie/varianten_lfp_nmc/ (Sonnet; Opus-Gegenrechnung gleich). Fall A: LFP 616 kg (160 Wh/kg gemessen; 469 kg bei 210 Gen 2), NMC 411 kg (217s×4p = 868 Zellen, 74,3 kWh). Anteil 41 % gegen 27 %.
- Fall B: LFP 93,0 kWh / 775 kg, NMC 86,6 kWh Bedarf, 5p → 92,8 kWh / 514 kg.
- Bauraum: LFP A −0,3 % (knapp), B nicht erfüllt; NMC erfüllt. Zyklen: LFP erfüllt, NMC unsicher.
- Stückliste je Variante: LFP 38 Pos., NMC 37 Pos. (200.2/200.4 entfallen, 200.5 Zellhalter neu; struktur.json BT-250 → 200.5 von Opus eingetragen). Offen: Zellen je Reihe und Fühler bei NMC aus LFP-Annahme (G4); Bild zeigt LFP-Balken bei Bandmitte statt Messwert.
- Deutung DEUTUNG.md. Vorgang: [C0] [V1] [G3]
