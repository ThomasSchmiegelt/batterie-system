---
typ: anforderung
gruppe: "REQ-P"
methode: "T"
ebene: "System"
bewertung: "offen"
tags: ["anforderung", "bewertung/offen"]
---
# REQ-P13

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

Schutzart, Isolation, Berührschutz

- Wert (Lastenheft): IP67, R_iso ≥ 100 Ω/V (UN R100, DC-Bus, W35) (Autor, Freigaberunde 2026-11-23)
- Priorität: Muss
- Vom Autor bestätigt: ja

## Verifikation (V-Modell-Matrix)

- Methode: T (A Analyse, S Simulation, I Inspektion, T Test, R Review)
- Ebene: System
- Kriterium: R_iso >= 100 Ω/V [Autor (Freigaberunde 2026-11-23)]<br>Schutzart == IP67 [Autor (Freigaberunde 2026-11-23)]
- Ist-Wert: [R_iso] kein Nachweis verknüpft; [Schutzart] kein Nachweis verknüpft
- Bewertung: **offen**
- Matrix: [[Dokument/06_verifikationsplan]] · Lastenheft: [[Dokument/01_lastenheft]] · Verfolgung: [[Dokument/03_anforderungsverfolgung]]

## Nachweisdateien
- kein Nachweis verknüpft

## Vorgänge
- [[Vorgang/G5|G5]] – Bauregeln + Prüfskript (Abstände, Isolation, Montagefolge)
- [[Vorgang/E2|E2]] – Schutzkonzept: Sicherung, Schütze, Vorladung, Isolationswächter
- [[Vorgang/L1|L1]] – Kabelverlegung: Weg skizzieren (Sketch-to-Prompt), Prüfskript Biegeradius/Abstand HV-NV/Kühlleitung, FreeCAD-Sweep
- [[Vorgang/E4|E4]] – Schaltungsmodell ngspice/Modelica: Vorladung, Kurzschluss

## Bauteile
- [[Bauteil/BT-350|BT-350]]
- [[Bauteil/BT-400|BT-400]]
- [[Bauteil/BT-430|BT-430]]
- [[Bauteil/BT-440|BT-440]]
- [[Bauteil/BT-450|BT-450]]
- [[Bauteil/BT-500|BT-500]]
- [[Bauteil/BT-510|BT-510]]
- [[Bauteil/BT-520|BT-520]]
- [[Bauteil/BT-570|BT-570]]
- [[Bauteil/BT-580|BT-580]]
- [[Bauteil/BT-590|BT-590]]
- [[Bauteil/BT-700|BT-700]]
- [[Bauteil/BT-710|BT-710]]
- [[Bauteil/BT-711|BT-711]]
- [[Bauteil/BT-712|BT-712]]
- [[Bauteil/BT-713|BT-713]]
- [[Bauteil/BT-715|BT-715]]
- [[Bauteil/BT-720|BT-720]]
- [[Bauteil/BT-721|BT-721]]
- [[Bauteil/BT-722|BT-722]]
- [[Bauteil/BT-730|BT-730]]
- [[Bauteil/BT-780|BT-780]]
