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
# REQ-D01

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

Jede Zahl ist rückverfolgbar (Rechnung mit Datei oder Quelle mit wörtlichem Beleg)

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
- [[Vorgang/R1|R1]] – Wissensaufbau W01-W15 (Chemie, Zelltypen, Spannung, Kabel, Steuerung, Struktur)
- [[Vorgang/R2|R2]] – Werkzeuge T01-T07 (Open Source Zellchemie, Elektroauslegung, Ersatzmodelle)
- [[Vorgang/R4|R4]] – Recherche prüfen: Zitate, Aussagen, Widersprüche -> BEFUNDE
- [[Vorgang/SL1|SL1]] – Grobe Stückliste aus Startsatz (Baugruppen, Mengen mit Herleitung)
- [[Vorgang/C4|C4]] – Validierung gegen veröffentlichte Messkurven, Abgleich Erwartung
- [[Vorgang/U3|U3]] – Ersatzmodell anpassen (Gauß-Prozess), Kreuzvalidierung gegen zurückgehaltene Läufe
- [[Vorgang/SL2|SL2]] – Stückliste fortschreiben nach Auslegung (Mengen, Kauf/Eigen, Werkstoffe, Bezugsquellen)
- [[Vorgang/B5|B5]] – Unternehmenspräsentation aus Folienbausteinen erzeugen (pptx + PDF, DE/EN), Zahlen gegen Quellen prüfen
