---
typ: befund
tags: ["befund"]
---
# B-BAT-055

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

FMEDA E3d: Sekundärschutz misst die Summe statt jeder Zelle, SG-02 verfehlt ASIL C (2026-11-24, gefunden von Sonnet in E3d, Deutung Opus)

Quelle: [[Dokument/BEFUNDE]]

## Vorgänge
- –

## Text aus BEFUNDE.md

- SG-01: SPFM 99,92 %, LFM 98,14 % (ASIL D erreicht). **Gilt erst nach der Korrektur:** Der Sekundärschutz in `cmu_skidl.py` misst T18–T0, also die Summe. Eine Überladung einer einzelnen Zelle wird so nicht unabhängig erkannt (FSR-01 verletzt, Unschärfe in ERW-E3 von Opus). → 3 × 6-Zellen-Überspannungsschutz, neu FSR-12.
- SG-02: SPFM 95,71 % < 97 %. Beiträge: FET-Kurzschluss 0,72 FIT, AFE „Ausgleich hängt an“ 0,40 FIT. → Maßnahme M1, zwei Schalter in Reihe: 97,85 %. Wird umgesetzt (ERW-E3 N7).
- Einstufungen von Sonnet bestätigt: Stecker J1 als gemeinsame Ursache, Kurzschluss des Ausgleichswiderstands, Kommunikationsausfall „sicher“ nur mit Zeitüberwachung → neu FSR-11. PMHF nur der Restfehleranteil (grob).
- B-BAT-E3c: BT-722 hat kein Merkmal für lichte Höhe, BT-311 nur 4 Merkmale (Luftstrecke, Abstände, Schützkanäle ohne Akte); Passivwerte, HV-Hilfsversorgung und Schützstrom offen (E3c ERGEBNIS.md, Abschnitt Grenzen).
