# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Batteriesystem (Testprojekt für den gewerblichen Einsatz von KI-Agenten)

KI-generiert (Claude Opus, 2026-11-11, ergänzt 2026-11-16). Regeln für alle Agenten: `AGENTS.md`. Dokumentation: `docs/` (Register `docs/00_dokumentenlenkung.md`).

## Ziel: eine komplette Batterie
Gebaut wird das ganze Pack BT-000 als parametrisches CAD mit nachgerechneter Chemie, Elektrik, Kühlung und Mechanik, nicht nur die Zelle. Jedes Teil begründet seine Form aus Akten. Drei Informationsquellen werden dafür zusammengeführt:
1. **Struktur** (`pm/bauteile/struktur.json`): Bauteilbaum mit Merkmalen. Nur was dort als Bauteil mit Merkmal steht, kann eine Akte bekommen (`pm.py pruefe`) und damit gebaut werden. Jede Position der Stückliste (`pm/bauteile/stueckliste.json`, Feld `bt`) braucht deshalb ein eigenes Bauteil mit Merkmalen, bevor ihr CAD entsteht.
2. **Information** (`forschung/ergebnis/<Nr>.md`, nur Werte mit bestandener Zitatprüfung; `pm/startwerte.json`, nur Annahmen): Ein Wert kommt in eine Akte ENT-NNN, mit der Fundstelle (z. B. `W03`) in `belege`. Ein Wert ohne Beleg ist eine **Annahme** und wird so benannt.
3. **Rechnung** (`sim/*`): Ergebnisse wie Zellwärme, Querschnitte oder Kühlplattenmaß gehen als neue Akte zurück und ändern über `parameter.json` das CAD.

Reihenfolge nach Netzplan (`pm/plan/kritischer_pfad.txt`): R4 Recherche prüfen → V1/V2 Startsatz und Lastenheft freigeben → G1 Zellmaße → C1–C4 Zellmodell → G3 Verschaltung → G4 Pack → K/E/M/X Kühlung, Elektrik, Mechanik, Crash → SL2 → B Bericht, Video, Präsentation.
Widersprüche zwischen Startwerten, Stückliste und Recherche werden vor dem CAD geklärt. Den aktuellen Stand der Lücken hält `BEFUNDE.md` fest (B-BAT-004).

## Arbeitsteilung: Opus verteilt selbstständig
Vorgabe des Autors vom 2026-11-11: „auch soll opus die arbeiten an sonnet, haiku und pi deligieren, ohne dass ich das laufend sagen muss.“
Das gilt dauerhaft. Opus fragt nicht nach, ob verteilt werden soll. Es verteilt nach dieser Tabelle.

| Wer | Aufgaben | Wie |
|---|---|---|
| **Opus** (leitet) | Anforderungen und Entscheidungen, Erwartung vor jeder Rechnung, neue Annahmen und Grenzwerte, Methodenwahl, Deutung der Ergebnisse, Fehlersuche im Modell, Gegenprüfung an Rohdaten, Freigabevorschlag an den Menschen | selbst |
| **Sonnet** | Skripte nach Vorgabe, Rechnungen starten und fortsetzen, Tabellen, Bilder und Berichtsentwürfe aus Ergebnisdateien, Übersetzung DE/EN, Dokumente nach Vorlage | Agent `sonnet-umsetzer` (`.claude/agents/`) |
| **Haiku** | Mechanisches: Log-Auszüge, Listen, Umformatieren, Links und Nummern prüfen, Rechtschreibung | Agent `haiku-helfer` |
| **PI** (lokal, ohne Werkzeuge) | Patentrecherche, Wissensaufbau, Zweitmeinung zu Texten | `bash forschung/lauf.sh …` (drei Stufen, Zitate automatisch geprüft) |
| **Maschine** | Rechnen (PyBaMM, Elmer, FluidX3D, FreeCAD) | Skripte, losgelöst und pausierbar |
| **Mensch** (Autor) | Vorgaben, Freigaben, alles nach außen | – |

Regeln zur Verteilung:
1. **Auftrag schriftlich:** Ziel, Eingangsdateien, Ausgabedatei, Abbruchbedingung. Eine Rechnung braucht vorher eine `ERWARTUNG.md` von Opus.
2. **Opus prüft jedes Ergebnis** an den Rohdaten, nicht am Bericht des Agenten. Bei Haiku reicht eine Stichprobe. Bei PI ist `pruefe.py` mit 0 Fehlern die Voraussetzung, danach liest Opus die Aussagen.
3. **Protokoll:** Jede Verteilung bekommt eine Zeile in `docs/08_ki_einsatz_protokoll.md`: wer, was, Ergebnisdatei, Prüfung, Ergebnis der Prüfung.
4. **Parallel** laufen nur unabhängige Aufträge. Die GPU wird nicht doppelt belegt (PI/ollama, GX, FluidX3D).
5. **Warten auf eine Rechnung** übernimmt ein Hintergrundbefehl, der sich selbst meldet. Kein Abfragen in Schleife.
6. **Zurück an Opus geht**, was eine neue Annahme, eine verfehlte Erwartung, einen Widerspruch oder eine Grenzwertfrage enthält.

## Projektmanagement (BAT-DOC-12)
- Jede Auslegungsentscheidung: `python3 pm/pm.py neu "Titel" BT-xxx merkmal`, Akte ausfüllen, Status „vorgeschlagen“, dem Autor vorlegen. Danach `pm.py pruefe`, `register`, `parameter`.
- CAD-Skripte lesen Maße **nur** aus `pm/bauteile/parameter.json`. Kein Maß im Code ohne Akte.
- Ziel: Am Ende kann jedes Bauteil seine Form begründen (`pm/gespraech.sh`), und das Abschlussvideo zeigt die Entstehung (`video/STORYBOARD.md`).
- Ziel: Am Ende steht eine Unternehmenspräsentation (REQ-D14, `praesentation/STORYBOARD.md`). Wer einen Vorgang abschließt, der dort eine Folie speist, legt im selben Schritt den Folienbaustein `praesentation/bausteine/<Vorgang>.md` ab (Kernaussage 1 Satz, Bild mit Zielband, Zahlen mit Quellpfad). Gilt auch für Aufträge an Sonnet.

## Gewerblicher Maßstab (Testprojekt)
- **Anforderungen zuerst:** Jede Arbeit gehört zu einer Anforderung (`docs/01_lastenheft.md`, REQ-…) und erscheint in der Nachverfolgung (`docs/03_anforderungsverfolgung.md`, erzeugt von `pm/plan/wissensnetz.py`).
- **Entscheidungen** mit Begründung und Alternativen in den Akten `pm/entscheidungen/ENT-*.md`. `docs/04_entscheidungen.md` erzeugt `pm.py register` daraus. **Risiken** in `docs/05_risiken_fmea.md`. **Änderungen** in `docs/09_aenderungen.md`.
- **Dokumentkopf** in jedem Dokument: Nummer, Version, Status (Entwurf / geprüft (KI) / freigegeben (Mensch)), Ersteller (Modell), Prüfer.
- **„Freigegeben“** setzt nur der Mensch.
- **Fremde Inhalte und Lizenzen** in `docs/10_lizenzen_und_quellen.md`. Keine fremden Texte ins Repo.
- **Im selben Schritt mitschreiben:** `BEFUNDE.md`, `ERINNERUNGEN.md`, Hermes-Skill `~/.hermes/skills/cae/batterie-system/SKILL.md` und das Buch-Ereignisprotokoll `~/hermes/buch/ereignissprotokoll_batterie/ereignisprotokoll.md` (BA-NN, nur im Buch, nicht im Repo). Weitere Nutzerregeln stehen im Gedächtnis der Fusion-Instanz, die das Projekt angelegt hat (`~/.claude/projects/-home-cae-hermes-fusion/memory/`).

## Befehle
Es gibt kein git, keinen Build, keine Tests und keinen Linter. Geprüft wird mit eigenen Skripten (`pm.py pruefe`, `pruefe.py`).
```bash
source umgebung.sh                          # venv .venv, $FREECAD_APPIMAGE, $BLENDER (neu: python3 -m venv .venv && .venv/bin/pip install -r requirements.txt)
python3 pm/pm.py pruefe                     # Verweise BT/REQ/B-BAT/Merkmal prüfen, doppelte gültige Entscheidungen
python3 pm/pm.py register                   # docs/04_entscheidungen.md aus den ENT-Akten
python3 pm/pm.py parameter                  # pm/bauteile/parameter.json (nur Akten mit Status „entschieden…“)
python3 pm/pm.py kontext BT-100             # Kontext fürs Bauteilgespräch
bash pm/gespraech.sh BT-100 "Frage"         # PI antwortet als Bauteil, Aktenverweise werden geprüft
python3 pm/startwerte.py "Kompaktwagen, 400 km Reichweite, in 20 min auf 80 %, Mitteleuropa"   # → pm/startwerte.json, docs/startparameter.md
python3 pm/bauteile/stueckliste.py          # → docs/13_stueckliste.md (liest startwerte.json)
python3 pm/plan/plan_batterie.py            # Netzplan, kritischer Pfad
python3 pm/plan/wissensnetz.py && python3 pm/plan/wissensnetz_ansicht.py   # wissensnetz.json/.html, docs/03, wissen/ (Obsidian)
bash forschung/lauf.sh wissen W05           # ein Recherchethema (patente|wissen|werkzeuge [Nr]); fertige werden übersprungen
bash forschung/alles.sh                     # alle Themen, ca. 3 h GPU. Abbruch: touch forschung/STOP; Log forschung/verlauf.log
```
Ein Thema neu rechnen: `rm forschung/ergebnis/<Nr>.*` (bei neuen Quellen auch `forschung/pakete/<Nr>.md`), dann `lauf.sh`.

## Aufbau und Datenfluss
- **Maßkette CAD:** `pm/bauteile/struktur.json` (Bauteilbaum BT-000…700 mit erlaubten Merkmalen) → Akten `pm/entscheidungen/ENT-NNN.md` (YAML-Kopf: bauteile, merkmal, wert, anforderungen, status) → `pm.py parameter` → `parameter.json` → CAD-Skripte in `cad/`. `ENT-*.md` werden mit `pm.py neu` aus `VORLAGE.md` angelegt.
- **Startwerte:** Ein Satz mit 4 Angaben → `startwerte.py` (alle Faktoren in `TAB_*` sind Annahmen) → `startwerte.json` → Stückliste und Lastenheft-Vorschlag REQ-P01…P10.
- **Recherche (`forschung/`):** Themen in `themen_{wissen,werkzeuge,patente}.tsv`, Aufträge `AUFTRAG_*.md`. Stufe A `paket.py` holt Texte ohne KI → `pakete/`. Stufe B: PI mit `--no-tools --offline` → `ergebnis/<Nr>.md`. Stufe C: `pruefe.py` prüft jedes Zitat wörtlich → `<Nr>.pruefung.txt`. Sammeldateien `WISSEN.md`, `WERKZEUGE.md`, `PATENTE.md` und das Wissensnetz entstehen nach jedem Thema neu. Die Helfer liegen außerhalb des Repos: `~/.hermes/skills/cae/patent-recherche/` und `.../web-recherche/`.
- **Erzeugte Dateien, nicht von Hand bearbeiten:** `docs/03_anforderungsverfolgung.md`, `docs/04_entscheidungen.md`, `docs/13_stueckliste.md`, `docs/startparameter.md`, `pm/bauteile/parameter.json`, `pm/plan/*.json|.csv|.html`, `wissen/` (wird geleert), `forschung/{WISSEN,WERKZEUGE,PATENTE}.md`. Stattdessen die Quelle ändern und das Skript laufen lassen.
- **Sim-Ordner** `sim/{chemie,elektrik,kuehlung,mechanik}` und `cad/{zelle,pack}` sind noch leer. Jede Rechnung dort braucht vorher eine `ERWARTUNG.md` (AGENTS.md).
- **Übergabestand:** `ERINNERUNGEN.md` (neueste Einträge oben, zuletzt Notizen am Ende) und `PLAN.md`. Befunde: `BEFUNDE.md` (B-BAT-NNN).
