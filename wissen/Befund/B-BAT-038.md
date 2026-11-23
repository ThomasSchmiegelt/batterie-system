---
typ: befund
tags: ["befund"]
---
# B-BAT-038

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

(2026-11-21) Thermik K3/K4 Probe: Pack ΔT 16 K, Erwartung von Opus falsch, LBM an der Stabilitätsgrenze

Quelle: [[Dokument/BEFUNDE]]

## Vorgänge
- –

## Text aus BEFUNDE.md

- K4 LFP Schnellladen (sim/kuehlung/k3_gesamt/elmer/ergebnis.json): T_max 42,6 °C, ΔT 16,4 K. Die Erwartung 33–37 °C hatte die Kühlmittelaufwärmung von 10,2 K aus K2b vergessen (Opus-Fehler). Das Ergebnis ist plausibel, **verfehlt aber ΔT ≤ 5 K** und wird zum Verbesserungsvorschlag. Varianten gegensinnig und Durchfluss ×2 sind beauftragt.
- K3 FluidX3D: τ ≈ 0,502 bei Re 760 mit 2 Zellen/mm, also Δp +228 %, h +129 %, Temperatur NaN. Methode geändert: Re 100/200, 4 Zellen/mm, Nu und f·Re der ausgebildeten Strömung übertragen.
