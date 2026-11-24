---
typ: dokument
nr: "BAT-DOC-23"
version: "0.1"
status: "Entwurf"
tags: ["dokument"]
---
# BAT-DOC-23 – Workflow für die nächste Konstruktionsschleife (V-Modell)

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

- Datei: `docs/17_workflow_schleife`
- Version: 0.1
- Status: Entwurf
- Typ: Projektdokument (Dokumentenlenkung [[Dokument/00_dokumentenlenkung]])

## Genannte Anforderungen (Textvorkommen)
- –

## Genannte Entscheidungen, Befunde, Bauteile (Textvorkommen)
- –

## Vorgänge, die dieses Dokument nennen
- –

## Inhalt (Kopie aus `docs/17_workflow_schleife.md`)

| Dok.-Nr. | BAT-DOC-23 | Version | 0.1 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Workflow für die nächste Konstruktionsschleife (V-Modell) | Ersteller | Claude Opus (KI) | Prüfer | – (Mensch offen) |

> **KI-generiert.** Entwurf, nicht vom Menschen freigegeben. Testprojekt „KI im Engineering“, kein Produkt.

Auftrag des Autors (2026-11-23): „kannst du bitte deine verbesserungsvorschläge in den worflow umsetzten. Die Requirements sollten am Ende entsprechend des V Modells geprüft werden.“ und „bevor wir eine intteration durchführen sollten wir unseren workflow optimieren“.
Grundlage: Kapitel „Lehren für die nächste Konstruktionsschleife“ im Abschlussbericht 1.2 (Regeln L1–L11). Die Regeln sind Vorschläge von Opus aus den Befunden der ersten Schleife; der Auftrag zur Umsetzung kommt vom Autor.

## 1 V-Modell im Projekt

```
 Anforderung (Lastenheft, REQ)  ─────────────────────────────  Validierung (Autor: erfüllt das Pack den Auftrag?)
   Systemauslegung (Pack, ENT)  ─────────────────────  Systemverifikation (REQ-Matrix, docs/06)
     Subsysteme (Kühlung, Elektrik, Mechanik)  ───  Subsystemnachweis (K/E/X-Rechnungen)
       Bauteil (BT, Merkmal, CAD)  ───────────  Bauteilprüfung (Kollision, Maßabgleich, Stückliste)
```

Jede Anforderung bekommt beim Anlegen (linker Ast) schon ihren Nachweis (rechter Ast): Messgröße, Ort, Lastfall, Methode, Ebene, Abnahmekriterium. Die Prüfung am Ende liest die Ergebnisdateien automatisch und vergleicht sie mit dem Kriterium (`pm/plan/verifikation.py` → `docs/06_verifikationsplan.md`).

**Nachweismethoden:** A Analyse (Handrechnung, 1D), S Simulation (FEM/CFD/PyBaMM), I Inspektion (CAD-Maß, Stückliste), T Versuch, R Durchsicht (Dokument, Norm).
**Bewertung je Anforderung:**
| Bewertung | Bedeutung |
|---|---|
| nachgewiesen | Kriterium erfüllt mit validierter Methode (A, I, T, R) |
| rechnerisch erfüllt (nicht validiert) | Kriterium erfüllt, aber nur mit unvalidierter Simulation. Kein Freigabenachweis. |
| verfehlt | Kriterium nicht erfüllt |
| offen | Nachweis noch nicht geführt |
| blockiert | Nachweis mit vorhandenen Daten nicht möglich (z. B. Zellmessung fehlt) |
| nicht definiert | Messgröße, Ort oder Lastfall fehlen. Der Autor muss die Anforderung schärfen. |

Eine Simulation ersetzt in diesem Projekt keinen Versuch. Bis ein Versuch vorliegt, ist „rechnerisch erfüllt“ die höchste Stufe für S.

## 2 Ablauf einer Rechnung (Tore)

| Tor | Inhalt | Werkzeug | Regel |
|---|---|---|---|
| T0 Anforderung scharf | REQ hat Messgröße, Ort, Lastfall, Kriterium, vom Autor bestätigt | `pm/anforderungen.json` | L7 |
| T1 Steckbrief | Anzahlen, Querschnitte, Lastpfad und Werkstoffe des Bauteils automatisch aus CAD-Ausgabe und parameter.json | `pm/steckbrief.py BT-xxx` | L1 |
| T2 ERWARTUNG | Pflichtabschnitte aus `sim/VORLAGE_ERWARTUNG.md`, einschließlich Plausibilitäts- und Abbruchkriterien und erwartetem Informationsgewinn je Variante | `pm/tor.py <Ordner>` | L3, L9 |
| T3 Vorrechnung | analytisch oder 1D, Ergebnis in der ERWARTUNG eingetragen | Rechenordner | L2 |
| T4 Lauf mit Wächter | Zeitschritt, Energie, Laufzeit, Wiederaufsetzpunkt; Schwellen vorher offline an einem alten Lauf getestet | `rechnen/waechter.py` (allgemein) | L4 |
| T5 Auswertung | Bild mit Zielband, Drucktauglichkeit geprüft | `pm/plan/bilder.py` | L8 |
| T6 Verifikationseintrag | Ergebnis in die REQ-Matrix | `pm/plan/verifikation.py` | V-Modell |

`rechnen/warteschlange.sh` startet einen Rechenschritt nur, wenn `pm/tor.py` für den Ordner 0 Fehler meldet. Ausnahme: Schritte mit `TOR=aus` in `schritte.txt`, zum Beispiel Bilder und Auswertungen.

## 3 CAD und Maße
- **Kollisionen** nach jedem CAD-Lauf (L5). Bei mehr als 0 Kollisionen ist der Lauf rot. Weiter geht es nur nach einer Entscheidung von Opus mit Befund.
- **Eine Quelle für Maße** (L6): Jeder Rechenordner listet in `eingaben.json` die verwendeten Maße mit ihrer Quelle (Merkmal in parameter.json oder Feld der CAD-Ausgabe). `pm/masse_abgleich.py` vergleicht diese Liste mit dem aktuellen Stand und meldet veraltete Rechnungen.
- **Massen:** maßgeblich ist die Stückliste. Weicht die CAD-Masse um mehr als 2 % ab, wird das gemeldet.

## 4 Freigaberunden (L10)
`python3 pm/pm.py freigabe` schreibt `docs/19_freigaberunde.md`. Darin stehen alle offenen Akten, alle Anforderungen mit „nicht definiert“ und alle Annahmen ohne Akte, je eine Zeile mit Vorschlag. Diese Liste geht gesammelt an den Autor, zum Beispiel am Ende jedes Arbeitstags. Der Autor gibt einzelne Zeilen frei, statt jede Akte einzeln anzusehen.

## 5 Gesetze und Normen als Anforderungen
Rechtliche Anforderungen kommen als eigene Gruppe REQ-G ins Lastenheft. Ihre Werte stammen nur aus einer Recherche mit bestandener Zitatprüfung (Themen W35 ff.). Die erste Bewertung, welche Regelwerke anwendbar sind, steht in BAT-DOC-07. Sie ist eine Einschätzung von Opus aus dem Gedächtnis und muss belegt werden.

## 6 Weitere Verbesserungen (Opus)
1. **Annahmenregister:** Jede Annahme (A_…, startwerte, ERWARTUNG) steht mit Einfluss auf das Ergebnis in einer Liste. Die drei einflussreichsten Annahmen bekommen eine Empfindlichkeitsrechnung.
2. **Änderungsfolgen automatisch:** Ändert sich eine Akte, listet `pm.py folgen ENT-NNN` die betroffenen Rechnungen (über `eingaben.json`) und Bilder.
3. **Versuchsplan früh:** Für jede S-Anforderung wird schon in der Schleife ein Validierungsversuch benannt (Zelle thermisch, Δp und Verteilung der Platte, quasistatische Quetschung).
4. **Schleifenziel vorher festlegen:** Welche REQ soll die Schleife von „verfehlt“ oder „offen“ auf „rechnerisch erfüllt“ bringen? Danach wird die Reihenfolge der Rechnungen geplant.
5. **Messgrößen für den Prozess:** Anteil der getroffenen Erwartungen, Fehlalarme des Wächters, Rechenstunden je Erkenntnis und offene Akten je Tag. Daraus entsteht in BAT-DOC-08 eine Tabelle je Schleife.

## 7 Wissensgraph
Obsidian-Tresor ist `wissen/` (eigenständig, enthält Kopien der verlinkten Dokumente und verkleinerte Bilder `_bilder/`; typisierte Kanten stehen als Eigenschaften in den Notizen).
Schema `pm/graph/SCHEMA.md`, Bau aus strukturierten Feldern, Textvorkommen nur als schwache Kante `erwaehnt`. Der Graph ist eine erzeugte Datei.
- `python3 pm/graph/graph.py` baut `pm/graph/graph.json` und `graph.graphml` (Zählung, unaufgelöste IDs).
- `python3 pm/graph/frage.py folgen|luecken|herkunft|norm <ID|Regelwerk> [--json]`; `python3 pm/pm.py folgen <ID>` ruft `folgen` auf.
- `python3 pm/graph/reqif.py` schreibt `pm/graph/anforderungen.reqif` (ReqIF 1.2). Lücken: `docs/21_graph_luecken.md`.
- Grenze: Rechnungen ohne `eingaben.json` im Präfixformat (`parameter:`, `cad:` …) haben keine `verwendet`-Kanten, `folgen` findet sie dann nicht.

---
*KI-generiert (Claude Opus, 2026-11-23). Status Entwurf. Freigabe nur durch den Autor.*

