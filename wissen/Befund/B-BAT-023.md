---
typ: befund
tags: ["befund"]
---
# B-BAT-023

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

B-BAT-023 (2026-11-17) C2 Kalibrierung: Blade-Widerstand gemessen 0,877 mΩ; 4680 schafft 30 min bei 1,5C, Plating-Risiko im Modell

Quelle: [[Dokument/BEFUNDE]]

## Vorgänge
- [[Vorgang/R3|R3]] – Patente P01-P10
- [[Vorgang/C2|C2]] – Zellmodell LFP (PyBaMM Prada2013) auf langes Format skalieren

## Text aus BEFUNDE.md

- Blade 25 °C, 15–90 % SOC: RMS 15,3 mV, R10 Modell 0,827 / Messung 0,877 mΩ (Test#5). Temperaturfit verfehlt (158 mV), OCV des Literatursatzes 143 mV daneben → **DFN für LFP nicht belastbar; Opus: für Wärme den gemessenen Widerstand nutzen** (unsere Zelle 1,28 mΩ → 48 W statt 55 W bei 2,1C; K1 war konservativ).
- 4680 (Chen2020-Material, W20-Geometrie, DCIR 6,4 mΩ im Band): 10→80 % in 29,7 min bei 1,5C CC-CV → REQ-P05 erfüllbar. Wärme 7,4 W (Modell) bzw. 11,5 W (I·ΔU) gegen K1b-Annahme 6,7 W → K1c: LFP 32,7 °C / 4,0 K ✓; 4680 mit Modellwärme 34,0 / 4,15 ✓, mit I·ΔU 39,1 / 6,5 ✗ (5 K). Opus: Differenz der Maße = Mischungswärme der Konzentrationsgradienten (I·ΔU gegen Gleichgewichts-OCV, obere Schranke); Autor: „einverstanden“ → Auslegung mit Modellwärme, I·ΔU als ungünstigster Fall; 4680-30 min „knapp, nicht abgesichert“; Plating als Risiko R-… **Anodenpotential < 0 V in allen Läufen (auch 1C)** → Plating-Risiko laut generischem Satz; ohne 4680-Messdaten nicht entscheidbar.
- openpyxl ins venv installiert (requirements.txt nachtragen). Vorgang: [C2]
