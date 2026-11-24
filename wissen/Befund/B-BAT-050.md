---
typ: befund
tags: ["befund"]
---
# B-BAT-050

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

Elektronik nur als Block, EMV und funktionale Sicherheit fehlten im Lastenheft (2026-11-24, gefunden von Opus auf Frage des Autors)

Quelle: [[Dokument/BEFUNDE]]

## Vorgänge
- –

## Text aus BEFUNDE.md

- Stand: BT-300/700 als Kaufteile ohne Innenleben. Kein REQ zu EMV, ISO 26262 und Kriechstrecken (nur docs/07 Zeile „sobald BMS ausgelegt wird“).
- Maßnahme: REQ-P17…P21 und REQ-D15 als Vorschlag. HARA-Entwurf BAT-DOC-24 (SG-01 Überladung ASIL D vorgeschlagen). BT-311, BT-321…325, BT-715 neu. Aufträge E3 (CMU-Platine KiCad, SPICE) und KR1 (Kreativmethode + Paarvergleich).
- Erwartung, die verfehlt werden kann: Die Wärme der Ausgleichswiderstände auf der CMU-Platine liegt ohne Wärmepfad vermutlich über 105 °C (ERW-E3 Punkt 3). Vorladung bei 912 V statt 800 V: 416 J statt 320 J.
- Offen beim Autor: Fragen F-S1…F-S6 (BAT-DOC-24), Pegel REQ-P17, Gewichte KR1.
