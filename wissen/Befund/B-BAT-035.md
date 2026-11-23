---
typ: befund
tags: ["befund"]
---
# B-BAT-035

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

(2026-11-19) KO2 Kosten mit Datenblättern und Kühlkreis; Opus-Fehler Zwischenlage

Quelle: [[Dokument/BEFUNDE]]

## Vorgänge
- –

## Text aus BEFUNDE.md

- KO2 (pm/kosten/ergebnis_<V>.json): LFP 6 793 € / 91,9 €/kWh, NMC 8 717 € / 117,4 €/kWh. ERW-KO2: LFP +8,7 % **verfehlt**, NMC +1,4 % erfüllt. Verifiziert + abgeleitet nur 0,2 % der Summe.
- Ursache LFP: Opus hatte die Zwischenlage BT-220 als 1 mm Mica-Vollmaterial festgelegt (242 Stück, 41,5 kg, 249 €). Korrektur: Schaumpad 300 kg/m³ (≈ 4,5 kg). Erwartet werden danach ≈ 89 €/kWh, der Neulauf läuft.
- Datenblattmassen: Hauptschütz GLFX250 0,8 kg statt 0,45 kg, Vorladeschütz + Widerstand 0,41 kg statt 0,15 kg (annahmen_g5.json).
