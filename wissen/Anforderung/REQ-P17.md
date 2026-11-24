---
typ: anforderung
gruppe: "REQ-P"
methode: "A"
ebene: "Subsystem"
bewertung: "offen"
tags: ["anforderung", "bewertung/offen"]
verifiziert_durch: ["sim/elektrik/e3_platine/ERGEBNIS.md"]
---
# REQ-P17

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

EMV der Elektronik (BMS, CMU, Schützansteuerung)

- Wert (Lastenheft): Störaussendung CISPR 25 Klasse 3 (Vorschlag); Störfestigkeit ISO 11452-2/-4; Transienten ISO 7637-2 am 12-V-Anschluss; ESD ISO 10605; Typgenehmigung UN R10 (Autor, Freigaberunde 2026-11-24)
- Priorität: Muss
- Vom Autor bestätigt: nein

## Verifikation (V-Modell-Matrix)

- Methode: A (A Analyse, S Simulation, I Inspektion, T Test, R Review)
- Ebene: Subsystem
- Kriterium: CISPR25_Klasse ≥ 3 [Autor (Freigaberunde 2026-11-24)]<br>ISO7637_2_Impulse bestanden 1, 2a, 3a, 3b [Opus (Vorschlag 2026-11-24, Freigabe Autor offen)]<br>ESD_Kontakt_kV ≥ 8 [Opus (Vorschlag 2026-11-24, Freigabe Autor offen)]
- Ist-Wert: [CISPR25_Klasse] kein Nachweis verknüpft; [ISO7637_2_Impulse] kein Nachweis verknüpft; [ESD_Kontakt_kV] kein Nachweis verknüpft
- Bewertung: **offen**
- Matrix: [[Dokument/06_verifikationsplan]] · Lastenheft: [[Dokument/01_lastenheft]] · Verfolgung: [[Dokument/03_anforderungsverfolgung]]

## Nachweisdateien
- [[Nachweis/sim_elektrik_e3_platine_ERGEBNIS.md|sim/elektrik/e3_platine/ERGEBNIS.md]]

## Vorgänge
- [[Vorgang/E3|E3]] – Steuerung/BMS: Messkonzept, Ladezustand, Ausgleich (Konzept, offene Software aus T06)

## Bauteile
- [[Bauteil/BT-311|BT-311]]
- [[Bauteil/BT-321|BT-321]]
- [[Bauteil/BT-324|BT-324]]
