---
typ: anforderung
gruppe: "REQ-P"
methode: "A"
ebene: "Bauteil"
bewertung: "offen"
tags: ["anforderung", "bewertung/offen"]
verifiziert_durch: ["sim/elektrik/e3_platine/ERGEBNIS.md"]
---
# REQ-P19

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

Isolationskoordination (Luft- und Kriechstrecken) auf Leiterplatten und in der Schaltbox

- Wert (Lastenheft): IEC 60664-1, Arbeitsspannung = U_max (REQ-P03), Verschmutzungsgrad 2, Überspannungskategorie II; verstärkte Isolierung HV ↔ NV; Werte je Bauteil ausweisen (Autor, Freigaberunde 2026-11-24); Auslegungshöhe 3000 m ü. NN (Luftstrecken mit Höhenkorrektur, Faktor 1,14–1,25 Annahme bis Normtext) (Autor 2026-11-24)
- Priorität: Muss
- Vom Autor bestätigt: nein

## Verifikation (V-Modell-Matrix)

- Methode: A (A Analyse, S Simulation, I Inspektion, T Test, R Review)
- Ebene: Bauteil
- Kriterium: Kriechstrecke_HV_NV_mm ≥ nach IEC 60664-1 (Vorschlag ≈ 10 mm verstärkt, Annahme) [Opus (Vorschlag 2026-11-24, Freigabe Autor offen)]<br>Auslegungshoehe_m = 3000 [Autor (2026-11-24)]<br>Kriechstrecke_ge_Luftstrecke wahr je Netzpaar [Opus (ERW-E3 N4)]
- Ist-Wert: [Kriechstrecke_HV_NV_mm] kein Nachweis verknüpft; [Auslegungshoehe_m] kein Nachweis verknüpft; [Kriechstrecke_ge_Luftstrecke] kein Nachweis verknüpft
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
