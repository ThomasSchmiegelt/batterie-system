# Auftrag Sonnet: Obsidian-Wissensnetz vervollständigen

KI-generiert (Claude Opus, 2026-11-23). Frage des Autors: „Ist die Doku für osidian vollständig“. Antwort von Opus: nein. Es fehlen die folgenden Punkte.

## Lücken (Opus, geprüft)
1. Anforderungen: 29 Notizen statt 31 (REQ-P16 und REQ-G01 fehlen). Künftig ist `pm/anforderungen.json` die Quelle der Anforderungen, mit Methode, Ebene, Kriterium und Bewertung aus `docs/06_verifikationsplan.md`.
2. Es fehlen Notizen für die Dokumente `docs/*.md` (Lenkung, Lastenheft, FMEA, Verifikation, Normen 07, Workflow 17, Freigaberunde 19, Kosten 18 und so weiter), für den Abschlussbericht `bericht/bericht.pdf` (Version 1.2, Kapitelliste aus bericht.toc), für die Folienbausteine `praesentation/bausteine/*`, für die Steckbriefe `pm/steckbriefe/*` und für die Regelwerke-Recherche W35–W42 (die läuft noch, siehe unten).
3. In `Start.md` fehlen Einstiege zu Bericht, V-Modell-Matrix, Workflow, Normen und Präsentation.

## Aufgaben
- Passe `pm/plan/wissensnetz.py` und `wissensnetz_obsidian.py` an: neuen Typ „Dokument“ und Verknüpfungen REQ ↔ VER-Bewertung ↔ Nachweisdatei.
- Neue Notizen verlinken auf vorhandene Notizen (ENT, B-BAT, BT, W). Es darf keine toten Links geben (Prüfung wie bisher).
- Jetzt laufen lassen und dann noch einmal, wenn in `rechnen/log_regelwerke.txt` „ALLE FERTIG“ steht. Darauf wartest du mit einem Hintergrundbefehl, der sich meldet. Kein Abfragen in einer Schleife im Vordergrund.
- `wissen/` ist erzeugt, Handarbeit dort wird überschrieben.
- Zeile in docs/08.

## Abbruch
Zurück an Opus geht alles, was eine inhaltliche Zuordnung verlangt und nicht in den Dateien steht. Rückmeldung höchstens 5 Zeilen: Zahl der Notizen je Typ, tote Links, Warnungen.
