---
typ: anforderung
gruppe: "REQ-D"
methode: "R"
ebene: "Prozess"
bewertung: "nachgewiesen"
tags: ["anforderung", "bewertung/nachgewiesen"]
kriterium_aus: ["Autor"]
verifiziert_durch: ["python3 pm/pm.py pruefe"]
---
# REQ-D11

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

Jede Entscheidung als Akte an Bauteil und Merkmal gebunden; CAD-Maße nur aus diesen Akten

- Wert (Lastenheft): –
- Priorität: –
- Vom Autor bestätigt: nein

## Verifikation (V-Modell-Matrix)

- Methode: R (A Analyse, S Simulation, I Inspektion, T Test, R Review)
- Ebene: Prozess
- Kriterium: Pruefskript rc0 [Autor]
- Ist-Wert: Pruefskript = rc 0 [python3 pm/pm.py pruefe]
- Bewertung: **nachgewiesen**
- Matrix: [[Dokument/06_verifikationsplan]] · Lastenheft: [[Dokument/01_lastenheft]] · Verfolgung: [[Dokument/03_anforderungsverfolgung]]

## Nachweisdateien
- kein Nachweis verknüpft
- Prüfskript: `python3 pm/pm.py pruefe`

## Vorgänge
- [[Vorgang/R5|R5]] – Werkzeugwahl festlegen (ENT): Zellmodell, Packmodell, Schaltung
- [[Vorgang/G1|G1]] – Zellmaße als ENT-Akten (aus W03/W08/P01, sonst Annahme)
- [[Vorgang/G2|G2]] – Parametrische Zelle FreeCAD (liest parameter.json)
- [[Vorgang/G4|G4]] – Pack: Zellanordnung, Querträger, Kühlplatte, Deckel
- [[Vorgang/SL2|SL2]] – Stückliste fortschreiben nach Auslegung (Mengen, Kauf/Eigen, Werkstoffe, Bezugsquellen)
