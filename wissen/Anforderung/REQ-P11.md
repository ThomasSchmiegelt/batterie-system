---
typ: anforderung
gruppe: "REQ-P"
methode: "T"
ebene: "System"
bewertung: "offen"
tags: ["anforderung", "bewertung/offen"]
---
# REQ-P11

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

Sicherheit: keine Ausbreitung des thermischen Durchgehens bzw. Warnzeit nach Norm

- Wert (Lastenheft): nach Norm (BAT-DOC-07)
- Priorität: Muss
- Vom Autor bestätigt: nein

## Verifikation (V-Modell-Matrix)

- Methode: T (A Analyse, S Simulation, I Inspektion, T Test, R Review)
- Ebene: System
- Kriterium: t_warnung >= 5 min [Norm (W35d belegt: UN R100 42024X1955, Warnung 5 min vor gefährlicher Situation im Fahrgastraum)]
- Ist-Wert: kein Nachweis verknüpft
- Bewertung: **offen**
- Matrix: [[Dokument/06_verifikationsplan]] · Lastenheft: [[Dokument/01_lastenheft]] · Verfolgung: [[Dokument/03_anforderungsverfolgung]]

## Nachweisdateien
- kein Nachweis verknüpft

## Vorgänge
- [[Vorgang/E2|E2]] – Schutzkonzept: Sicherung, Schütze, Vorladung, Isolationswächter
- [[Vorgang/X1|X1]] – Seitencrash Pfahl, quasistatisch: Eindringung in Gehäuse/Querträger (CalculiX, plastisch, Kontakt)
- [[Vorgang/F1|F1]] – FMEA und Verifikationsplan nachziehen

## Bauteile
- [[Bauteil/BT-100|BT-100]]
- [[Bauteil/BT-120|BT-120]]
- [[Bauteil/BT-140|BT-140]]
- [[Bauteil/BT-220|BT-220]]
- [[Bauteil/BT-250|BT-250]]
- [[Bauteil/BT-300|BT-300]]
- [[Bauteil/BT-700|BT-700]]
- [[Bauteil/BT-713|BT-713]]
- [[Bauteil/BT-750|BT-750]]
- [[Bauteil/BT-770|BT-770]]
