---
typ: befund
tags: ["befund"]
---
# B-BAT-003

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

B-BAT-003 (2026-11-12) Patente P02–P10: Spalten verrutscht (Opus-Fehler in lauf.sh), PI blieb ehrlich

Quelle: [[Dokument/BEFUNDE]]

## Vorgänge
- [[Vorgang/R2|R2]] – Werkzeuge T01-T07 (Open Source Zellchemie, Elektroauslegung, Ersatzmodelle)
- [[Vorgang/R3|R3]] – Patente P01-P10
- [[Vorgang/R5|R5]] – Werkzeugwahl festlegen (ENT): Zellmodell, Packmodell, Schaltung
- [[Vorgang/G4|G4]] – Pack: Zellanordnung, Querträger, Kühlplatte, Deckel
- [[Vorgang/E1|E1]] – Zellverbinder/Kabel: Querschnitt, Verluste, Erwärmung (Zielband als Annahme)

## Text aus BEFUNDE.md

- `IFS=$'\t' read` fasst leere Felder zusammen (Tab gilt als Leerraum). Bei Themen ohne Inhaber rückte der deutsche Zweck („Kühlung“) in die Suchspalte → 0 Treffer; P06–P10 brachen ab (paket.py IndexError bei leerer Trefferliste).
- PI auf leeren Paketen: meldete „Trefferliste leer, keine Auswertung möglich“, erfand keine Patente (Links nicht aus dem Paket: 0).
- Behoben: Tabs vor dem Einlesen in ein Nicht-Leerraumzeichen getauscht; paket.py verträgt leere Trefferlisten. P02–P10 und T02 neu gerechnet (nachlauf2.sh): T02 jetzt 4/0. Patente danach weiter leer: Google Patents antwortet mit HTTP 503 (Bot-Schutz nach dem ersten Durchlauf). Nicht umgangen; einmaliger Versuch nach 2 h (nachlauf3.sh). Alternativen mit Anmeldung (EPO OPS, Lens.org) bräuchten die Zustimmung des Autors. Vorgang: [R3]
