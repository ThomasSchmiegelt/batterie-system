# Wissensgraph: Schema (Opus)

KI-generiert (Claude Opus, 2026-11-23). Freigabe Autor: „ja, es geht in die optimierung“. Gehört zu BAT-DOC-17, Workflow Schleife 2.
Grundsatz: Kanten kommen nur aus **strukturierten Feldern**. Kanten aus bloßen Textvorkommen bekommen den Typ `erwaehnt` und gelten nie als Beleg.

## Knoten
| Typ | ID | Quelle |
|---|---|---|
| Anforderung | REQ-P/D/G-NN | pm/anforderungen.json |
| Bauteil | BT-NNN | pm/bauteile/struktur.json |
| Merkmal | BT-NNN.merkmal | struktur.json (erlaubte Merkmale), Wert aus parameter.json |
| Entscheidung | ENT-NNN | pm/entscheidungen/ENT-*.md (YAML-Kopf) |
| Annahme | A_… / startwert:… | cad/baukasten/annahmen*.json, pm/startwerte*.json |
| Rechnung | Pfad des Rechenordners | sim/**/ERWARTUNG.md |
| Ergebnis | Datei::Schlüssel | Nachweise in anforderungen.json, ergebnis*.json |
| Befund | B-BAT-NNN | BEFUNDE.md |
| Quelle | Wxx, Pxx, Txx | forschung/ergebnis/*.md (nur mit .pruefung.txt) |
| Norm | Regelwerk | docs/07, docs/20 |
| Stuecklistenposition | Pos-Nr. je Variante | pm/bauteile/stueckliste_*.json (Feld bt) |
| Dokument | docs/…, bericht, praesentation, video | Dateien |

## Kanten (gerichtet, Typ, Quelle)
| Kante | von → nach | Quelle (Feld) |
|---|---|---|
| teil_von | Bauteil → Bauteil | struktur.json |
| hat_merkmal | Bauteil → Merkmal | struktur.json |
| legt_fest | Entscheidung → Merkmal | ENT `bauteile` + `merkmal` + `wert` |
| erfuellt_beitrag | Entscheidung → Anforderung | ENT `anforderungen` |
| belegt_durch | Entscheidung → Befund/Quelle/Ergebnis | ENT `belege` |
| ersetzt | Entscheidung → Entscheidung | ENT `ersetzt` |
| gilt_fuer | Entscheidung → Variante | ENT `variante` |
| verifiziert_durch | Anforderung → Ergebnis | anforderungen.json `nachweis` |
| kriterium_aus | Anforderung → Quelle/Norm/Annahme | `herkunft_kriterium` |
| gehoert_zu | Rechnung → Anforderung | ERWARTUNG `## Anforderung` (bei alten Ordnern: `erwaehnt`) |
| verwendet | Rechnung → Merkmal/Annahme/Ergebnis | `eingaben.json` (Präfix parameter:/cad:/stueckliste:/annahme:/ergebnis:) |
| erzeugt | Rechnung → Ergebnis | Ergebnisdateien im Ordner |
| realisiert | Stuecklistenposition → Bauteil | Stückliste `bt` |
| widerlegt / bestaetigt | Befund → Rechnung/Entscheidung | nur wenn der Befund das im Kopf als Feld führt, sonst `erwaehnt` |
| erwaehnt | beliebig → beliebig | Textvorkommen der ID (schwach, nur Ansicht) |

Eigenschaften je Knoten: Status (entschieden/vorgeschlagen, Bewertung aus verifikation.bewerte), Datum, Variante, Pfad.

## Abfragen (Pflicht)
1. `folgen <ID>`: alles stromabwärts über legt_fest → verwendet → erzeugt → verifiziert_durch (umgekehrt) und teil_von. Ergebnis ist die Liste der neu zu rechnenden Rechnungen, betroffenen Anforderungen, Bilder und Bausteine. **Probe:** `folgen BT-000.laenge` (oder das passende Merkmal der Packlänge) muss K5 (sim/kuehlung/k5_parallel) finden. Diesen veralteten Stand hat masse_abgleich.py schon gefunden.
2. `luecken`: Anforderung ohne verifiziert_durch, Rechnung ohne gehoert_zu, Entscheidung ohne belegt_durch, Merkmal ohne legt_fest (das CAD nutzt dann eine Annahme), Kriterium mit Herkunft Annahme, an dem eine „verfehlt“-Bewertung hängt.
3. `herkunft <ID>`: stromaufwärts bis zu Quelle, Norm, Annahme oder Autor-Vorgabe. Zeigt, worauf ein Wert am Ende beruht.
4. `norm <Regelwerk>`: betroffene Anforderungen, Bauteile und Rechnungen.

## Nachtrag 1 (Opus, 2026-11-23, nach dem ersten Lauf)
- Bestätigt: Knoten `Vorgabe` (ID „Autor“) und `Variante` (LFP, NMC). Startwerte und „Annahme Opus“ werden je Kriterium eigene Annahme-Knoten.
- Neu: Knoten `CAD-Lauf` (je Variante). Kanten `eingang_cad`: jedes Merkmal aus parameter.json → CAD-Lauf. Kante `erzeugt`: CAD-Lauf → jedes Ergebnis `cad:<schluessel>` aus cad/baukasten/ausgabe/ergebnis_<var>.json. Begründung: Das CAD liest alle Merkmale, also macht jede Merkmaländerung einen neuen CAD-Lauf nötig. Damit findet `folgen` über die CAD-Ausgabe alle Rechnungen mit `cad:`-Eingaben. Die Verknüpfung ist bewusst grob, eine feinere Zuordnung wäre geraten.
- Die Probe `folgen BT-000.bauraum_laenge_mm` muss danach K5 finden.
