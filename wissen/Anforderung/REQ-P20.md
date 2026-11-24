---
typ: anforderung
gruppe: "REQ-P"
methode: "I"
ebene: "Bauteil"
bewertung: "offen"
tags: ["anforderung", "bewertung/offen"]
verifiziert_durch: ["sim/elektrik/e3_platine/ERGEBNIS.md"]
---
# REQ-P20

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

Umweltfestigkeit und Bauteilqualifikation der Elektronik

- Wert (Lastenheft): ISO 16750-1…5 (Klima, Schwingung, elektrisch); Bauteile AEC-Q100/Q101/Q200; Fertigung IPC-A-610 Klasse 3; Leiterbahnen IPC-2152 (Autor, Freigaberunde 2026-11-24)
- Priorität: Muss
- Vom Autor bestätigt: nein

## Verifikation (V-Modell-Matrix)

- Methode: I (A Analyse, S Simulation, I Inspektion, T Test, R Review)
- Ebene: Bauteil
- Kriterium: AEC_Q_Bauteile vorhanden [Opus (Vorschlag 2026-11-24, Freigabe Autor offen)]<br>IPC_Klasse = 3 [Opus (Vorschlag 2026-11-24, Freigabe Autor offen)]
- Ist-Wert: [AEC_Q_Bauteile] kein Nachweis verknüpft; [IPC_Klasse] kein Nachweis verknüpft
- Bewertung: **offen**
- Matrix: [[Dokument/06_verifikationsplan]] · Lastenheft: [[Dokument/01_lastenheft]] · Verfolgung: [[Dokument/03_anforderungsverfolgung]]

## Nachweisdateien
- [[Nachweis/sim_elektrik_e3_platine_ERGEBNIS.md|sim/elektrik/e3_platine/ERGEBNIS.md]]

## Vorgänge
- [[Vorgang/E3|E3]] – Steuerung/BMS: Messkonzept, Ladezustand, Ausgleich (Konzept, offene Software aus T06)
- [[Vorgang/E3b|E3b]] – Wärme CMU-Platine mit Pad (Elmer)

## Bauteile
- [[Bauteil/BT-321|BT-321]]
