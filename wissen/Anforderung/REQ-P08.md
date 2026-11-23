---
typ: anforderung
gruppe: "REQ-P"
methode: "S"
ebene: "System"
bewertung: "offen"
tags: ["anforderung", "bewertung/offen"]
---
# REQ-P08

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

Umgebungstemperatur Betrieb und Laden

- Wert (Lastenheft): offen (°C)
- Priorität: Muss
- Vom Autor bestätigt: nein

## Verifikation (V-Modell-Matrix)

- Methode: S (A Analyse, S Simulation, I Inspektion, T Test, R Review)
- Ebene: System
- Kriterium: T_betrieb zwischen [-20, 45] °C [Annahme Opus]<br>T_laden zwischen [0, 45] °C [Annahme Opus]
- Ist-Wert: [T_betrieb] kein Nachweis verknüpft; [T_laden] kein Nachweis verknüpft
- Bewertung: **offen**
- Matrix: [[Dokument/06_verifikationsplan]] · Lastenheft: [[Dokument/01_lastenheft]] · Verfolgung: [[Dokument/03_anforderungsverfolgung]]

## Nachweisdateien
- kein Nachweis verknüpft

## Vorgänge
- [[Vorgang/V1|V1]] – Lastenheft-Werte REQ-P01..P08 vorschlagen (Fahrzeug, kWh, Spannung, Leistung, Laden, Chemie, Bauraum, Temperatur)
- [[Vorgang/V2|V2]] – Freigabe Lastenheft durch Autor

## Bauteile
- [[Bauteil/BT-600|BT-600]]
- [[Bauteil/BT-760|BT-760]]
