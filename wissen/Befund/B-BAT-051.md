---
typ: befund
tags: ["befund"]
---
# B-BAT-051

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

E3 CMU-Platine: Wärme der Ausgleichswiderstände zu hoch, Layout ungeroutet (2026-11-24, Sonnet, Deutung Opus)

Quelle: [[Dokument/BEFUNDE]]

## Vorgänge
- –

## Text aus BEFUNDE.md

- SPICE an den Rohdaten geprüft (`sim/elektrik/e3_platine/ergebnis_*.json`): Ausgleich LFP 152 mA / NMC 127,4 mA bei U_max. Bei U_nenn dauert der Ausgleich +14 % länger als in E2 gerechnet. Vorladung 912 V: 9,12 A, 416 J, 300 ms. ENT-172 von 34 auf 32,45 Ω korrigiert; der Fehler lag in der Opus-Tabelle ERW-E3.
- **Wärme verfehlt (erwartet):** 9,6–10 W auf 120 × 60 mm ergeben ΔT 67 K (h = 10 W/m²K) bis 139 K (h = 5), also 112–184 °C bei 45 °C Umgebung. Deutung Opus: Die Strahlung ist nicht berücksichtigt (h_Strahlung ≈ 6 W/m²K), realistisch ≈ 90–110 °C, damit Grenze 105 °C erreicht. Folge: Wärmepfad zur Kühlplatte oder Taktung nötig → E3b (Elmer) und KR1-Ergebnis.
- Layout: 106 Teile (Erwartung 130–170; es fehlen Entkopplung, ESD und Abschlüsse, sie sind als Platzhalter offen). DRC 0 Verstöße, 212 Verbindungen nicht geroutet (Freerouting-Download vom Rechtesystem blockiert, Autor gefragt). Kollisionsfrei im Pack (NMC 0; LFP 3 Kollisionen schon vor E3).
- Opus-Entscheidungen: Ausnahme Pad-Abstand innerhalb eines Bauteils (0,15 mm) ist zulässig, die Kriechstrecke im Gehäuse verantwortet der Bauteilhersteller. Platinenmasse als Annahme aus FR4 1,85 g/cm³ und Cu-Anteil, offen bis E3b.
