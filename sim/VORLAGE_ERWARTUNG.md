# ERWARTUNG <Rechnung>: <Titel>

KI-generiert (<Modell>, JJJJ-MM-TT), Entwurf. Vorlage: `sim/VORLAGE_ERWARTUNG.md` (docs/17 §2, Tor T2). Pflicht vor jeder Rechnung (AGENTS.md Grundsatz 3). Jeder Abschnitt unten muss ausgefüllt sein, sonst startet `rechnen/warteschlange.sh` den Schritt nicht (`python3 pm/tor.py <Ordner>`). Zusätzlich muss im Ordner eine `eingaben.json` liegen (Maße mit Quelle, Format siehe `pm/masse_abgleich.py`). Nicht anwendbar heißt: Begründung hinschreiben, nicht leer lassen.

## Anforderung
REQ-xxx (Messgröße, Ort, Lastfall und Kriterium wie in `pm/anforderungen.json`). Die ID muss dort stehen.

## Steckbrief
Verweis auf `pm/steckbriefe/BT-xxx_<LFP|NMC>.md` (erzeugt mit `pm/steckbrief.py`), Stand vom Tag der Rechnung.

## Vorrechnung
Analytische oder 1D-Abschätzung (Rechenweg, Ergebnis, Ort der Datei). Tor T3 (L2).

## Erwartung
Zahlenband je Ergebnisgröße vor der Rechnung, mit Begründung. Wird das Band verfehlt, wird zuerst die Erwartung geprüft, nicht das Modell angepasst.

## Plausibilitätskriterien
Woran erkennt man vor der Deutung, dass das Ergebnis physikalisch unsinnig ist (Energiebilanz, Vorzeichen, Größenordnung, Symmetrie)?

## Abbruchkriterien (Wächter)
Schwellen für Zeitschritt, Energiefehler, Laufzeit, Wiederaufsetzpunkt; vorher offline an einem alten Lauf getestet (`rechnen/waechter.py`).

## Informationsgewinn der Varianten
Je Variante: Welche Frage beantwortet sie, die die anderen nicht beantworten? Varianten ohne eigenen Informationsgewinn entfallen (L9).

## Zielband Bild
Welche Bilder entstehen, welches Zielband oder welche Grenze ist eingezeichnet, welche Lesehilfe gehört dazu.

## Prüfung
(Nach der Rechnung auszufüllen von Opus: Vergleich Erwartung gegen Ergebnis mit Dateipfad, Deutung, Befund.)
Pflichtzeilen (maschinenlesbar, für die Prozesskennzahlen BAT-DOC-22 QN4):
`Erwartung: getroffen | teilweise | verfehlt`
`Gefunden von: Opus | Sonnet | Haiku | PI | Autor | Wächter | Tor`
