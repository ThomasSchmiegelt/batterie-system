---
typ: dokument
datei: "README.md"
tags: ["dokument", "kopie"]
---
# README

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

- Kopie von `README.md` (Quelle im Repo, hier nur Lesekopie)

## Inhalt

# Batteriesystem mit KI-Agenten: ein Agentic Workflow für nachweispflichtige Entwicklung

> **KI-generiert.** Aufbau, Skripte und Texte von Claude Opus, Sonnet und Haiku (Anthropic) sowie einem lokalen LLM, gesteuert und geprüft von Thomas Schmiegelt. Angelegt 2026-11-11. Testprojekt zum Thema „KI im Engineering“, nicht begutachtet. Den Status „freigegeben“ setzt nur der Mensch.

**Um die Batterie geht es hier nur am Rande. Im Mittelpunkt steht die Frage, wie KI-Agenten Entwicklungsarbeit so übernehmen können, dass man ihren Ergebnissen trauen kann.** Als Anwendungsfall dient ein vollständiges Batteriepack für einen Kompaktwagen (400 km Reichweite, 10–80 % in 20 min). Von wenigen Vorgaben bis zum Bericht reicht die Kette über Lastenheft, Zellmodell, Verschaltung, parametrisches CAD, Kühlung, Hochvolt, Crash, Stückliste und Kosten.

## Agentenarchitektur (Orchestrator-Worker)

| Rolle | Modell / Werkzeug | Aufgabe |
|---|---|---|
| Orchestrator | Claude Opus (Claude Code) | Anforderungen, Methodenwahl, **Erwartung vor jeder Rechnung**, Deutung, Fehlersuche, Prüfung an Rohdaten |
| Worker | Claude Sonnet (Subagent `sonnet-umsetzer`) | Skripte, Rechnungen, Auswertungen und Berichtsentwürfe, jeweils nach schriftlichem Auftrag |
| Worker | Claude Haiku (Subagent `haiku-helfer`) | Mechanisches: Logs, Listen, Formatprüfung |
| Lokales LLM | PI-Agent über Ollama, offline | Recherche, Zweitmeinung, automatischer Prüfschritt nach Rechnungen |
| Maschine | FreeCAD (headless), Elmer FEM, FluidX3D (LBM, GPU), OpenCourant (explizit), PyBaMM | Rechnen, losgelöst und unterbrechbar |
| Mensch | Autor | Vorgaben, Freigaben, alles nach außen |

Regeln: `CLAUDE.md` (`CLAUDE.md`, im Repo), `AGENTS.md` (`AGENTS.md`, im Repo). Jede Delegation steht im KI-Einsatzprotokoll (`docs/08_ki_einsatz_protokoll.md`, im Repo) mit wer, was, Prüfung und Ergebnis.

## Was den Workflow nachprüfbar macht

- **Anforderungen zuerst:** 30 Anforderungen (Lastenheft (`docs/01_lastenheft.md`, im Repo)) und eine automatisch erzeugte Anforderungsverfolgung (`docs/03_anforderungsverfolgung.md`, im Repo).
- **Entscheidungsakten:** 157 Akten `pm/entscheidungen/ENT-*.md` mit Begründung, Alternativen, Belegen und Status. Das CAD liest Maße **nur** aus Akten mit Status „entschieden“ (`pm.py parameter`).
- **Erwartung vor dem Ergebnis:** Ohne `ERWARTUNG.md` mit Zielband rechnet kein Agent. Jede Grafik zeigt dieses Zielband.
- **Prüfung an Rohdaten, nicht am Agentenbericht:** Opus prüft jedes Ergebnis selbst, bei Haiku reicht eine Stichprobe.
- **Recherche mit Grounding-Prüfung** (`forschung/`): Stufe A holt die Quellen ohne KI, Stufe B lässt das lokale LLM offline nur auf diesen Texten arbeiten, Stufe C prüft jedes Zitat wörtlich gegen die Quelle (`pruefe.py`). Nur geprüfte Werte dürfen als Beleg in eine Akte.
- **Vektorsuche und RAG über die Projektakten** (`pm/vektorsuche/`): Embeddings lokal über Ollama, ChromaDB, Antworten mit Belegpflicht, und eine Prüfung im Code, ob jede zitierte Akte wirklich abgerufen wurde.
- **Unterbrechbare Rechenwarteschlange** (`rechnen/`): Fertig-Marken, Stop-Datei, Wiederaufsetzen nach einem Neustart des Rechners. Sie läuft auch weiter, wenn das Token-Kontingent des Cloud-Modells aufgebraucht ist.
- **Ehrliches Fehlerprotokoll:** `BEFUNDE.md` (`BEFUNDE.md`, im Repo) und ein eigenes Berichtskapitel über Grenzen, Fehler und Unsicherheiten der KI.

## Beispiele aus dem Fehlerprotokoll

- **Crash:** Kennzahlen und Energiebilanz waren unauffällig (Fehler 0,19 %). Erst das Verformungsbild zeigte, dass Zellreihen ohne gegenseitigen Kontakt bis zu 319 mm wegrutschten. Seitdem gibt es eine automatische Plausibilitätsprüfung für jeden Crashfall (B-BAT-039/040).
- **Kosten:** Die vorab festgelegte Erwartung deckte eine falsche Vorgabe des Orchestrators selbst auf: 41,5 kg Glimmer im Pack (B-BAT-035).
- **Thermik:** Die Erwartung des Orchestrators hatte die Aufwärmung des Kühlmittels vergessen. Das Ergebnis von 16 K Temperaturunterschied war richtig, die Erwartung falsch (B-BAT-038).
- **Geometrie:** Die Kollisionsbereinigung der Gesamtmontage begann mit 67 Fehlern und endete bei 0, Schritt für Schritt nachvollziehbar (B-BAT-036/037).

## Stand (2026-11-21)

- Gesamtmontage G5 mit Blech-Kühlplatte (Mäander) für LFP und NMC kollisionsfrei, Stückliste und Kosten aktualisiert.
- Thermik: FluidX3D (Kanalströmung) und Elmer (ganzes Pack), mit Varianten. Ergebnis: Die Kühlung verfehlt das Ziel ΔT ≤ 5 K; der Verbesserungsvorschlag ist Parallelführung mit Z-Verteiler.
- Crash: Pfahlaufprall und Quetschung mit OpenCourant, mehrere Lastfälle laufen.
- Bericht: `bericht/bericht.pdf` (`bericht/bericht.pdf`, im Repo), 78 Seiten, Version 0.5 (Entwurf).

## Aufbau

| Ordner | Inhalt |
|---|---|
| `docs/` | Dokumentationssatz: Lastenheft, Pflichtenheft, Nachverfolgung, Entscheidungen, FMEA, Verifikationsplan, Normen, KI-Einsatzprotokoll, Änderungen, Lizenzen |
| `pm/` | Bauteilbaum, Entscheidungsakten, Parameter für das CAD, Stückliste, Kosten, Netzplan, Vektorsuche |
| `forschung/` | Recherche in drei Stufen mit Zitatprüfung (fremde Quelltexte sind nicht im Repo) |
| `cad/` | Parametrisches CAD (FreeCAD headless), Baukasten für die Gesamtmontage mit Kollisions- und Massenprüfung |
| `sim/` | Chemie (PyBaMM), Elektrik, Kühlung (Elmer, FluidX3D), Mechanik/Crash (CalculiX, OpenCourant); jeder Rechenordner mit `ERWARTUNG.md` |
| `rechnen/` | Unterbrechbare Warteschlange für die Rechnungen |
| `bericht/` | Bericht (LaTeX) |
| `.claude/agents/` | Definitionen der Worker-Agenten |

Software und Umgebung: `SOFTWARE.md` (`SOFTWARE.md`, im Repo). Fremde Inhalte und Lizenzen: `docs/10_lizenzen_und_quellen.md` (`docs/10_lizenzen_und_quellen.md`, im Repo).

