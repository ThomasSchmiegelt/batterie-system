---
typ: befund
tags: ["befund"]
---
# B-BAT-013

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

B-BAT-013 (2026-11-17) Entscheidungen des Autors: ENT-012 freigegeben, Bauraum verlängert (ENT-013)

Quelle: [[Dokument/BEFUNDE]]

## Vorgänge
- [[Vorgang/R3|R3]] – Patente P01-P10
- [[Vorgang/V1|V1]] – Lastenheft-Werte REQ-P01..P08 vorschlagen (Fahrzeug, kWh, Spannung, Leistung, Laden, Chemie, Bauraum, Temperatur)
- [[Vorgang/G1|G1]] – Zellmaße als ENT-Akten (aus W03/W08/P01, sonst Annahme)
- [[Vorgang/E1|E1]] – Zellverbinder/Kabel: Querschnitt, Verluste, Erwärmung (Zielband als Annahme)
- [[Vorgang/E3|E3]] – Steuerung/BMS: Messkonzept, Ladezustand, Ausgleich (Konzept, offene Software aus T06)
- [[Vorgang/K2|K2]] – Kanalverteilung 1D (Verteiler, Druckverlust)

## Text aus BEFUNDE.md

- Autor 2026-11-17: „ENT 012 ist freigegeben, verlängere den Bauraum, dokumentiere die entscheidungen“.
- ENT-012 (Baum mit Varianten, BT-250 Zellhalter) entschieden (Mensch). ENT-013: BT-000 bauraum_laenge_mm = 1950 mm für beide Varianten; Zahl von Opus aus G1 (1874 mm Stapel + 2 × 30 mm Rand = 1934 mm, + 16 mm Reserve). Breite 1400 und Höhe 130 mm bleiben Annahmen.
- Nachgeführt: Lastenheft REQ-P03 (800 V), REQ-P06 (zwei Varianten), REQ-P07 (L 1950 mm); docs/09 AEN-006…011; docs/04 (13 Akten, 0 Fehler).
- Neulauf (Sonnet, Opus nachgerechnet): nötig Fall A 208 Wh/L (vorher 214), LFP B 262; LFP A jetzt **erfüllt** (+2,3 %) und passt geometrisch mit 16 mm Reserve bei 1 mm Zellabstand. LFP B passt weiter nicht (Breite). NMC 1232 Plätze, Belegung 70/88 %. Massen unverändert. Erwartung (Nachtrag) erfüllt.
- Werkzeughinweis: erzeuge_bericht.py setzt die Kernaussage im Folienbaustein auf „(Opus)“ zurück → Skript muss vorhandene Kernaussage erhalten (offen für Sonnet). Vorgang: [G1] [V1] [C0]
