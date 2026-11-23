# Auftrag Sonnet: Wissensgraph bauen

KI-generiert (Claude Opus, 2026-11-23). Das Schema steht in `pm/graph/SCHEMA.md` und ist verbindlich. Neue Kantentypen gehen zuerst an Opus.

## Ausgaben
1. `pm/graph/graph.py` (networkx, venv; Lizenz BSD in docs/10 eintragen, falls neu) baut den Graphen aus den Quellen im Schema → `pm/graph/graph.json` (node-link) und `pm/graph/graph.graphml`. Die Datei ist erzeugt und wird nicht von Hand bearbeitet.
   - Am Ende eine Zählung je Knoten- und Kantentyp.
   - Eine Liste unaufgelöster IDs: Kante zeigt auf nicht vorhandenen Knoten.
2. `pm/graph/frage.py` mit den Unterbefehlen `folgen`, `luecken`, `herkunft`, `norm` nach Schema. Ausgabe als Markdown, Option `--json`.
   - **Probe:** `folgen` auf das Merkmal der Packlänge findet sim/kuehlung/k5_parallel. Wenn nicht, liegt das an fehlenden Kanten. Das meldest du, ohne die Abfrage zurechtzubiegen.
3. `pm/graph/reqif.py`: Export der Anforderungen mit Attributen (Text, Wert, Methode, Ebene, Kriterium, Bewertung, Herkunft) und der Verknüpfungen verifiziert_durch und erfuellt_beitrag als ReqIF 1.2 (XML) → `pm/graph/anforderungen.reqif`.
   - Prüfe gegen das öffentliche XSD, wenn es abrufbar ist (OMG). Sonst gilt Wohlgeformtheit plus eigene Strukturprüfung, das schreibst du in die Rückmeldung.
4. Obsidian: `wissensnetz_obsidian.py` schreibt die typisierten Kanten als Eigenschaften (YAML-Frontmatter, z. B. `verifiziert_durch: [...]`) in die Notizen. Die Text-Links bleiben. Tote Links 0.
5. `pm.py folgen <ID>` ruft `frage.py folgen` auf (docs/17 §6 Punkt 2).
6. Ergänze in docs/17 einen Abschnitt „Wissensgraph“ (5 Zeilen, Befehle) und in CLAUDE.md unter Befehle zwei Zeilen. Den Hermes-Skill ergänzt du mit einem Satz.
7. Lauf: `luecken` ausführen, Ausgabe nach `docs/21_graph_luecken.md` (Kopf BAT-DOC-21, Entwurf). Zeile in docs/08.

## Abbruch
Zurück an Opus geht jede Kante, die eine Deutung verlangt (z. B. ob ein Befund eine Entscheidung widerlegt), und jeder Widerspruch zwischen den Quellen. Rückmeldung höchstens 6 Zeilen: Zählung der Knoten und Kanten, unaufgelöste IDs, Probe folgen ok/nicht ok, die fünf größten Lücken, ReqIF-Prüfung.
