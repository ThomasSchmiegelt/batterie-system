---
typ: anforderung
gruppe: "REQ-P"
methode: "S"
ebene: "System"
bewertung: "offen"
tags: ["anforderung", "bewertung/offen"]
---
# REQ-P04

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

Dauer- und Spitzenleistung Entladen

- Wert (Lastenheft): P_spitze nach Startwert (10 s), P_dauer ≥ 60 kW (Autor, Freigaberunde 2026-11-23)
- Priorität: Muss
- Vom Autor bestätigt: ja

## Verifikation (V-Modell-Matrix)

- Methode: S (A Analyse, S Simulation, I Inspektion, T Test, R Review)
- Ebene: System
- Kriterium: P_spitze >= 150 kW [Autor (Freigaberunde 2026-11-23)]<br>P_dauer >= 60 kW [Autor (Freigaberunde 2026-11-23)]
- Ist-Wert: [P_spitze] kein Nachweis verknüpft; [P_dauer] kein Nachweis verknüpft
- Bewertung: **offen**
- Matrix: [[Dokument/06_verifikationsplan]] · Lastenheft: [[Dokument/01_lastenheft]] · Verfolgung: [[Dokument/03_anforderungsverfolgung]]

## Nachweisdateien
- kein Nachweis verknüpft

## Vorgänge
- [[Vorgang/V1|V1]] – Lastenheft-Werte REQ-P01..P08 vorschlagen (Fahrzeug, kWh, Spannung, Leistung, Laden, Chemie, Bauraum, Temperatur)
- [[Vorgang/V2|V2]] – Freigabe Lastenheft durch Autor
- [[Vorgang/C3|C3]] – Ratentest 0,5C/1C/2C, Wärmeleistung, R_i über SOC und T
- [[Vorgang/E1|E1]] – Zellverbinder/Kabel: Querschnitt, Verluste, Erwärmung (Zielband als Annahme)

## Bauteile
- [[Bauteil/BT-130|BT-130]]
- [[Bauteil/BT-400|BT-400]]
- [[Bauteil/BT-410|BT-410]]
- [[Bauteil/BT-420|BT-420]]
- [[Bauteil/BT-430|BT-430]]
- [[Bauteil/BT-711|BT-711]]
- [[Bauteil/BT-730|BT-730]]
