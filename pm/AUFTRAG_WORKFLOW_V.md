# Auftrag Sonnet: Werkzeuge für den Workflow der Schleife 2 (V-Modell)

KI-generiert (Claude Opus, 2026-11-23). Konzept: `docs/17_workflow_schleife.md` (zuerst lesen), Normen: `docs/07_normen_und_vorschriften.md`.
Es kommen keine neuen Zahlen und keine Grenzwerte dazu. Fehlt ein Wert, schreibst du „nicht definiert“. Laufende Skripte änderst du nie an Ort und Stelle: neue Datei schreiben, dann `mv`. Kein Commit.

## Ausgaben
1. **`pm/anforderungen.json`**: alle REQ-P und REQ-D aus `docs/01_lastenheft.md`, Text unverändert. Neue Felder je REQ: `messgroesse`, `ort`, `lastfall`, `methode` (A/S/I/T/R), `ebene` (System/Subsystem/Bauteil), `kriterium` (maschinenlesbar, z. B. `{"groesse":"T_max","op":"<=","wert":45,"einheit":"°C"}`), `nachweis` (Liste mit Pfad zur Ergebnisdatei und JSON-Schlüssel), `bestaetigt_autor` (true/false), `herkunft` (Zitat oder Quelle).
   - Felder fülltst du nur, wenn sie wörtlich im Lastenheft oder im REQ-Überblick von `bericht/bericht.tex` stehen. Alles andere bleibt `"nicht definiert"`.
   - Dazu ein leerer Abschnitt `REQ-G` (gesetzlich) mit einem Eintrag für die Maschinenrichtlinie, Status „nicht anwendbar (zu belegen, W37)“.
2. **`pm/plan/verifikation.py`**: liest `anforderungen.json` und die Nachweisdateien und schreibt `docs/06_verifikationsplan.md` als V-Modell-Matrix.
   - Spalten: REQ, Ebene, Methode, Kriterium, Ist-Wert mit Quelle, Bewertung.
   - Die Bewertung folgt den Stufen aus docs/17 §1. Bei S ist die höchste Stufe „rechnerisch erfüllt (nicht validiert)“.
   - Am Ende steht eine Zählung je Bewertung. Zusätzlich gibt das Skript `bericht/verifikation_tabelle.tex` für den Bericht aus.
3. **`sim/VORLAGE_ERWARTUNG.md`** mit diesen Pflichtabschnitten:
   - `## Anforderung` (REQ-ID)
   - `## Steckbrief` (Verweis)
   - `## Vorrechnung`
   - `## Erwartung`
   - `## Plausibilitätskriterien`
   - `## Abbruchkriterien (Wächter)`
   - `## Informationsgewinn der Varianten`
   - `## Zielband Bild`
   - `## Prüfung` (nach der Rechnung)

   Dazu **`pm/tor.py <ordner>`**: prüft, dass die Abschnitte vorhanden und nicht leer sind, dass die REQ-ID in anforderungen.json steht und dass es `eingaben.json` gibt. Rückgabe rc 0 oder 1 mit Liste der Fehler. Prüfe das Werkzeug an `sim/kuehlung/k5_parallel`. Dort werden Lücken erwartet, und es sind echte Lücken.
4. **`pm/steckbrief.py BT-xxx [LFP|NMC]`**: schreibt `pm/steckbriefe/BT-xxx_<var>.md`.
   - Inhalt: Merkmale aus parameter.json, Anzahlen, Querschnitte und Massen aus `cad/baukasten/ausgabe/ergebnis_<var>.json` und der Stückliste, außerdem Eltern- und Kindbauteile aus struktur.json.
   - Prüfe es mit BT-610.
5. **`pm/masse_abgleich.py`**: Jeder Rechenordner mit `eingaben.json` (Format `{"name": {"wert":…, "quelle":"parameter:<merkmal>" | "cad:<schluessel>" | "stueckliste:<pos>"}}`) wird mit dem aktuellen Stand verglichen. Gemeldet werden Abweichungen und eine CAD-Masse, die mehr als 2 % von der Stückliste abweicht.
   - Für `sim/kuehlung/k5_parallel` legst du ein `eingaben.json` aus dessen Skripten an. Werte nur übernehmen, nicht ändern.
6. **`pm.py freigabe`** (neuer Unterbefehl): schreibt `docs/19_freigaberunde.md` mit allen Akten außer „entschieden…“, allen REQ mit „nicht definiert“ oder `bestaetigt_autor:false` und allen `A_*`-Annahmen aus `cad/baukasten/annahmen*.json` ohne Akte. Je Zeile: ID, Frage, Vorschlag, Spalte „Autor: ja/nein/ändern“.
7. **`rechnen/warteschlange.sh`**: bei Schritten mit Rechenordner zuerst `pm/tor.py`. Fällt das Tor durch, wird der Schritt übersprungen. Das steht dann in `verlauf.log` und in `rechnen/TOR_FEHLT`.
   - Mit `TOR=aus` als 4. Spalte in schritte.txt wird das Tor übersprungen. Bestehende Zeilen bekommen `TOR=aus`, damit sich nichts ändert.
   - Wie bei jedem laufenden Skript: neue Datei schreiben, dann `mv`. Prüfen mit `bash -n`.
8. **Recherche W35–W39** in `forschung/themen_wissen.tsv`, Themen nach docs/07:
   - W35 UN R100 Rev. 3, GTR 20 und UN 38.3
   - W36 R94, R95, R135
   - W37 EU 2023/1542, 2023/1230 Art. 1 Ausnahmen, 2024/1689
   - W38 GB 38031-2025 und GB/T 31467
   - W39 Automotive SPICE PAM

   Die Suchbegriffe sind englisch. Suche offizielle URLs (unece.org, eur-lex.europa.eu, openstd.samr.gov.cn, vda-qmc.de) mit WebSearch und prüfe jede mit `curl -sI` auf HTTP 200. Nicht erreichbare Quellen trägst du nicht ein, sie gehen in die Rückmeldung. Danach `bash rechnen/gpu_warten.sh && bash forschung/lauf.sh wissen W35` und so weiter, nacheinander, losgelöst mit setsid.
9. Zeile in `docs/08_ki_einsatz_protokoll.md` (Sonnet, Auftrag, Dateien).

## Abbruch
Zurück an Opus geht, was im Lastenheft widersprüchlich ist, was eine neue Annahme verlangt und was am bestehenden Ablauf nicht passt. Du deutest nichts.
Rückmeldung höchstens 8 Zeilen: Dateien, Ausgabe von tor.py für k5, Zählung aus verifikation.py, URLs W35–W39 ok/fehlt.
