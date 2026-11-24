---
typ: befund
tags: ["befund"]
---
# B-BAT-045

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

B-BAT-045 Erste Prüfung mit den neuen Workflow-Werkzeugen (2026-11-23, Opus)

Quelle: [[Dokument/BEFUNDE]]

## Vorgänge
- [[Vorgang/R3|R3]] – Patente P01-P10
- [[Vorgang/E3|E3]] – Steuerung/BMS: Messkonzept, Ladezustand, Ausgleich (Konzept, offene Software aus T06)

## Text aus BEFUNDE.md

Werkzeuge nach BAT-DOC-23 (Sonnet), Vorschläge für Methode, Ebene und Lastfall von Opus (pm/anforderungen.json, Autor offen).
- `verifikation.py`: von 31 REQ sind 2 verfehlt (P07 Länge 2373 gegen 1950 mm, P09 Spreizung LFP 9,6 K), 1 offen und 28 nicht definiert. 28 Anforderungen haben also kein prüfbares Kriterium. Das bestätigt Lehre L7.
- Das Lastenheft nennt noch L = 1950 mm (ENT-013). Im Bericht steht 2030 mm (ENT-102), die Vorgabe des Autors erlaubt Längenwachstum. Der Widerspruch muss in der Freigaberunde geklärt werden.
- Laut Lastenheft gilt „Spreizung **in der Zelle** ≤ 5 K“ (docs/01, Zeile 28). Die Rechnungen werten ΔT über den Zellblock aus. Das ist ein Hinweis zur offenen ΔT-Frage.
- `masse_abgleich.py`: K5 (verteiler.py) rechnet mit packlaenge 2030 mm, aktuell sind es 2373 mm (+16,9 %). Die Rohrlänge und damit Δp im Verteiler sind damit veraltet. Neu rechnen, bevor die Pumpe ausgelegt wird.
- `tor.py` auf k5_parallel: 8 Lücken, die ERWARTUNG der ersten Schleife hatte die neuen Pflichtabschnitte noch nicht. Für alte Ordner ist das erwartet. Das Tor gilt für neue Rechnungen.
- Recherche W35–W37: unece.org antwortet mit 403, eur-lex mit einer WAF-Abfrage. Diese Texte sind automatisch nicht abrufbar. W38/W39 sind eingetragen. forschung/STOP vom 22.11. steht noch.
