# Batteriesystem: Zelle, Pack, Elektrik, Kühlung – entwickelt mit KI-Agenten

> **KI-generiert.** Aufbau, Skripte und Texte von Claude Opus (Anthropic) für Thomas Schmiegelt, angelegt 2026-11-11.
> Hobbyprojekt zum Thema „KI im Engineering“, nicht begutachtet.

**Testprojekt für den gewerblichen Einsatz von KI-Agenten.** Anforderungen, Nachverfolgung, Entscheidungen, Risiken und KI-Einsatzprotokoll liegen in [`docs/`](docs/00_dokumentenlenkung.md). Opus leitet und verteilt die Arbeit selbstständig an Sonnet, Haiku und PI ([`CLAUDE.md`](CLAUDE.md)).

**Stand: nur vorbereitet.** Es ist noch nichts gerechnet und nichts recherchiert. Offene Vorgaben stehen in [`PLAN.md`](PLAN.md).

## Ziel

Ein vollständiges Batteriesystem für ein Elektrofahrzeug, von der Zellchemie bis zum fertigen Pack:

1. **Chemie der Zelle:** Kathode, Anode, Elektrolyt. Spannung, Kapazität und Alterung werden mit einem elektrochemischen Modell (PyBaMM) gerechnet.
2. **Zellgeometrie:** Form und Abmessungen, parametrisches CAD.
3. **Zusammenbau:** Zellen, Träger, Gehäuse und Deckel zum Pack, Explosionsdarstellung.
4. **Elektrik:** Verschaltung der Zellen in Reihe und parallel, Zellverbinder, Sicherung, Schütze, Vorladung und Messung (BMS).
5. **Kühlung:** Kühlplatte, Strömung, Temperaturverteilung, schnelles Laden als Auslegungsfall.
6. **Wissensaufbau und Patentrecherche:** Stand der Technik mit wörtlichen Belegen.

Beispiel als Bezug: BYD Blade Battery (https://www.byd.com/de/technologie/blade-battery). Das sind lange, flache LFP-Zellen, die ohne Module direkt im Pack sitzen. Die Herstellerseite lädt ihren Inhalt per JavaScript nach und liefert beim automatischen Abruf keinen Text. Die Kennwerte holt deshalb die Recherche (`forschung/`, Thema W03 und P01) mit Belegen.

## Arbeitsweise (übernommen aus Fusion, Wasserstoff und E-Maschine)

- **Rollen:** Claude Code schreibt den Code, der rechnet, startet ihn und dokumentiert. PI (lokales Sprachmodell) recherchiert und prüft gegen. Hermes führt die Skills.
- **Erwartung vorher:** Vor jeder Rechnung werden Erwartung und Deutung festgelegt (`ERWARTUNG.md` im Rechenordner). Danach wird verglichen.
- **Zielband in jeder Grafik:** Jede Grafik zeigt einen beschrifteten Zielbereich. Ein unbelegter Grenzwert ist als **Annahme** gekennzeichnet.
- **Befunde:** Jeder Befund kommt in den Hermes-Skill und mit Zahl und Fundstelle nach `BEFUNDE.md`, im selben Schritt.
- **Pausierbar:** Jede Rechnung läuft in einem eigenen Scope (`~/bin/rechnung pause|weiter`), speichert paketweise und nennt ihre Dauer.
- **Kennzeichnung:** Jedes Dokument ist als KI-generiert gekennzeichnet (Titelkasten und Fußzeile).

## Aufbau

| Ordner | Inhalt | Werkzeug |
|---|---|---|
| `forschung/` | PI-Rechercheagent: Patente (P01–P10) und Wissensaufbau (W01–W07), in drei Stufen und sicher | Skill `patent-recherche`, `web-recherche` |
| `quellen/` | Fremde PDFs und Datenblätter. **Nicht im Repo** | – |
| `sim/chemie/` | Zellmodell: Entladekurve, Innenwiderstand, Wärmeentwicklung, Alterung | PyBaMM 26.10 |
| `cad/zelle/` | Parametrische Zelle (Länge, Breite, Dicke, Pole, Entgasungsventil) | FreeCAD 1.1.4 (Textmodus), Blender |
| `cad/pack/` | Pack: Zellanordnung, Träger, Kühlplatte, Gehäuse, Deckel | FreeCAD, Blender, gmsh |
| `sim/elektrik/` | Verschaltung, Spannungslage, Ströme, Verluste in Verbindern, Schutzkonzept | Python (scipy) |
| `sim/kuehlung/` | Kühlplatte: Verteilung im Kanal, Temperatur der Zellen beim Schnellladen | ElmerFEM 26.2, FluidX3D (eigene Kopie) |
| `sim/mechanik/` | Lasten auf den Pack (Stoß, Schwingung, Verspannung der Zellen) | ElmerFEM |
| `pm/` | Projektmanagement: Bauteilbaum, Entscheidungsakten ENT-*, Parameter fürs CAD, Bauteilgespräch mit PI | pm.py, gespraech.sh |
| `video/` | Abschlussvideo (Storyboard; entsteht am Schluss) | FreeCAD → Blender → ffmpeg |
| `bericht/` | Bericht DE und EN, kapitelweise | LaTeX |
| `docs/` | Dokumentationssatz BAT-DOC-00 bis 11: Lastenheft, Pflichtenheft, Nachverfolgung, Entscheidungen, FMEA, Verifikationsplan, Normenliste, KI-Einsatzprotokoll, Änderungen, Lizenzen, Prozess | Markdown |
| `.claude/agents/` | Agenten `sonnet-umsetzer`, `haiku-helfer` | Claude Code |

Software und Umgebung: [`SOFTWARE.md`](SOFTWARE.md). Regeln für Agenten: [`AGENTS.md`](AGENTS.md).
