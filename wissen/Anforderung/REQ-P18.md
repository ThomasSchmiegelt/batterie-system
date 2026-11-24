---
typ: anforderung
gruppe: "REQ-P"
methode: "R"
ebene: "System"
bewertung: "offen"
tags: ["anforderung", "bewertung/offen"]
verifiziert_durch: ["docs/24_gefahrenanalyse_hara.md"]
---
# REQ-P18

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

Funktionale Sicherheit nach ISO 26262

- Wert (Lastenheft): ASIL je Sicherheitsziel nach HARA BAT-DOC-24 (Vorschlag: SG-01 ASIL D, SG-02/03/04/08 C, SG-05/06/07 B); SG-01 ASIL D und Umfang HARA+SG+FSR+FMEDA (Autor, Freigaberunde 2026-11-24); alle Einstufungen HE-01…12 und FTTI (Annahme) übernommen (Autor, Freigaberunde 2026-11-24 R2)
- Priorität: Muss
- Vom Autor bestätigt: nein

## Verifikation (V-Modell-Matrix)

- Methode: R (A Analyse, S Simulation, I Inspektion, T Test, R Review)
- Ebene: System
- Kriterium: HARA vorhanden [Opus (Vorschlag 2026-11-24, Freigabe Autor offen)]<br>FSR_umgesetzt vorhanden [Opus (Vorschlag 2026-11-24, Freigabe Autor offen)]
- Ist-Wert: [HARA] kein Nachweis verknüpft; [FSR_umgesetzt] kein Nachweis verknüpft
- Bewertung: **offen**
- Matrix: [[Dokument/06_verifikationsplan]] · Lastenheft: [[Dokument/01_lastenheft]] · Verfolgung: [[Dokument/03_anforderungsverfolgung]]

## Nachweisdateien
- [[Nachweis/docs_24_gefahrenanalyse_hara.md|docs/24_gefahrenanalyse_hara.md]]

## Vorgänge
- [[Vorgang/S1|S1]] – Gefahrenanalyse HARA ISO 26262-3, Sicherheitsziele, FSR (BAT-DOC-24)

## Bauteile
- [[Bauteil/BT-311|BT-311]]
- [[Bauteil/BT-322|BT-322]]
- [[Bauteil/BT-325|BT-325]]
- [[Bauteil/BT-715|BT-715]]
