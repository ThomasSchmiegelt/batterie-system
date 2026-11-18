| Dok.-Nr. | BAT-DOC-12 | Version | 0.1 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Projektmanagement | Ersteller | Claude Opus (KI) | Prüfer | – (Mensch offen) |

> **KI-generiert.** Entwurf, nicht vom Menschen freigegeben.

## Auftrag (wörtlich, Rechtschreibung korrigiert)
> „Ich will im Batterieprojekt eine weitere Stufe einführen, und zwar das Projektmanagement. Es sollen Entscheidungen dokumentiert werden. Das Ziel soll sein, am Ende mit dem Bauteil zu sprechen, um zu erfahren, wie und warum es so aussieht, wie es aussieht. Ein weiteres Ziel ist die Projektdokumentation. Das soll ein Abschlussvideo sein. Am Anfang entsteht die Zelle, die Zellenstacks, die Regelung, die Verkabelung, die gesamte geometrische Struktur und Kühlung sowie zusätzliche Komponenten. Das steht aber ganz am Abschluss. Ich rufe dann mehr oder weniger PI auf und kann so in Interaktion mit dem Bauteil treten.“ (Autor, 2026-11-11)

## Grundsatz: Jede Form hat eine Akte
1. **Bauteilbaum** `pm/bauteile/struktur.json`: BT-000 System, BT-100 Zelle, BT-200 Zellstack, BT-300 Regelung, BT-400 Verkabelung, BT-500 Struktur, BT-600 Kühlung, BT-700 Zusatzkomponenten. Darunter seit 2026-11-16 je Stücklistenposition ein Bauteil (z. B. BT-530 Querträger, BT-610 Kühlplatte, BT-711 Hauptschütze; 46 Bauteile, ENT-004 Vorschlag). Jedes Bauteil hat Merkmale wie `dicke_mm`; das Feld `stueckliste` verbindet es mit der Stückliste.
2. **Entscheidungsakte** `pm/entscheidungen/ENT-NNN.md`, je Entscheidung eine Datei: Frage, Alternativen, Begründung, Folgen. Dazu Bauteil, Merkmal, Wert, Anforderungen und Belege. Neu anlegen mit `python3 pm/pm.py neu "Titel" BT-100 dicke_mm`.
3. **Einzige Maßquelle:** `pm.py parameter` erzeugt `pm/bauteile/parameter.json` aus den Akten mit Status „entschieden“. Das CAD liest nur diese Datei. Ein Maß ohne Akte gibt es nicht.
4. **Prüfung:** `pm.py pruefe` meldet fehlende Bauteile, Merkmale, Anforderungen und Befunde sowie doppelte gültige Entscheidungen. `pm.py register` erzeugt `docs/04_entscheidungen.md`.
5. **Änderung:** Eine neue Akte mit `ersetzt: ENT-alt` ersetzt die alte. Die alte bleibt erhalten, sodass die Geschichte nachvollziehbar ist.
6. **Status:** „vorgeschlagen“ setzt Opus, „entschieden“ setzt nur der Autor.

## Bauteilgespräch (Ziel 1)
`bash pm/gespraech.sh BT-100` öffnet eine interaktive Sitzung. Mit einer Frage dahinter gibt es eine einzelne Antwort, die protokolliert wird:
`bash pm/gespraech.sh BT-100 "Warum bist du so dick?"`.
- Der Kontext entsteht ohne KI aus den eigenen Akten (`pm.py kontext`). PI läuft ohne Werkzeuge, die Rolle steht in `pm/ROLLE_BAUTEIL.md`.
- Jeder Aktenverweis in der Antwort wird gegen den Kontext geprüft (✓ oder ✗). Das Protokoll liegt in `pm/gespraeche/`.
- Test 2026-11-11 mit der Zelle: Antwort in 33 s, 4 von 4 Verweisen gültig. Noch nicht Entschiedenes hat die Zelle als „noch nicht entschieden“ gemeldet.

## Abschlussvideo (Ziel 2)
Storyboard: `video/STORYBOARD.md` (BAT-DOC-13). Es entsteht am Schluss in der Reihenfolge Zelle → Stack → Regelung → Verkabelung → Struktur → Kühlung → Zusatzkomponenten → System.

## Meilensteine
| Nr | Meilenstein | Kriterium | Status |
|---|---|---|---|
| M0 | Vorbereitung | Struktur, Software, Agenten, Doku, PM | erreicht 2026-11-11 |
| M1 | Vorgaben | REQ-P01…P08 vom Autor | offen |
| M2 | Wissen und Patente | P01–P10, W01–W07 mit 0 Fehlern in pruefe.py, von Opus gelesen | offen |
| M3 | Zelle | Chemie und Maße entschieden, PyBaMM validiert | offen |
| M4 | Stack, Elektrik | Verschaltung, Verbinder, BMS-Umfang entschieden | offen |
| M5 | Struktur, Kühlung | CAD aus parameter.json, Kühlung nachgewiesen | offen |
| M6 | Abschluss | Bericht, Abschlussvideo, Unternehmenspräsentation, Bauteilgespräch für alle BT | offen |

## Projektsteuerung
- **Stand je Arbeitstag:** `ERINNERUNGEN.md` (Übergabe) und `docs/08_ki_einsatz_protokoll.md` (wer hat was gemacht, wie lange).
- **Kennzahlen für den gewerblichen Test:** Laufzeit je Arbeitspaket, Zahl der Agentenaufrufe je Modell, gefundene Fehler je Prüfstufe.
