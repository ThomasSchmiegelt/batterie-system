---
typ: dokument
datei: "AGENTS.md"
tags: ["dokument", "kopie"]
---
# AGENTS

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

- Kopie von `AGENTS.md` (Quelle im Repo, hier nur Lesekopie)

## Inhalt

# AGENTS.md: Regeln für Agenten im Batterieprojekt (PI, Hermes, Claude Code)

KI-generiert (Claude Opus, 2026-11-11). Regeln übernommen aus den Projekten Fusion, Wasserstoff und E-Maschine sowie den Vorgaben des Autors.

## Grundsätze
1. **Nichts erfinden.** Jede Zahl stammt aus einer Rechnung dieses Projekts oder aus einer abgerufenen Quelle mit wörtlichem Beleg. Eine Grenze ohne Beleg heißt **Annahme**.
2. **Die KI rechnet nicht selbst.** Sie schreibt Code, der rechnet, startet ihn und dokumentiert ihn.
3. **Erwartung vorher.** Vor jeder Rechnung kommen Erwartung und Deutung in `ERWARTUNG.md` des Rechenordners. Danach wird verglichen, auch wenn die Erwartung verfehlt ist.
4. **Das Werkzeug ist der Maßstab.** Ein Modell wird nicht geändert, damit eine Zahl passt. Fehler im Werkzeug gehen nach `BEFUNDE.md`, die Reparatur erfolgt nur angekündigt.
5. **Dokumentieren im selben Schritt:** `BEFUNDE.md` (Befund mit Zahl und Fundstelle), `ERINNERUNGEN.md` (Übergabe, neuestes oben), Hermes-Skill `batterie-system`.
6. **Grafiken** zeigen ein beschriftetes Zielband oder eine Grenze. Zahlen in Titeln kommen aus dem Ergebnis, nie hart eingetragen. Jedes Bild bekommt eine Lesehilfe für Nicht-Fachleute.
7. **Kennzeichnung „KI-generiert“** in jedem Dokument (Titelkasten und Fußzeile).
8. **Herkunft nennen:** Bei jeder Zelle und jedem Parametersatz steht, woher er kommt (z. B. PyBaMM `Prada2013`, Literatur, eigene Anpassung).

## Sicherheit
- **PI arbeitet ohne Werkzeuge** (`--no-tools`), solange es keine Sandbox gibt. bwrap ist auf diesem Rechner durch AppArmor gesperrt. Fremde Texte bekommt PI nur als Paket von `paket.py` (Stufe A, keine KI).
- **Keine Geheimnisse lesen oder ausgeben:** auth.json, credentials/, API-Schlüssel, .env, Passwörter.
- **Fremde Inhalte** (PDFs, Patentschriften, Seiten) bleiben in `quellen/`, `forschung/recherche_ablage/` und `forschung/patent_ablage/`. Sie kommen **nie** in ein Repo.
- **Patente:** Es wird nur der Stand der Technik gesammelt. Aussagen zu Verletzung oder Handlungsfreiheit (FTO) macht die KI nicht.
- **Nichts nach außen ohne ausdrückliche Freigabe** (GitHub, Uploads, Posts).

## Rechnen
- Jede Rechnung läuft in einem Scope `hermes-batterie-*`, ist pausierbar (`~/bin/rechnung pause|weiter`), speichert paketweise und bietet `--weiter`. Vor dem Start wird die Dauer genannt.
- Eine Rechnung startet losgelöst (setsid/systemd-run), damit sie einen Absturz der Sitzung übersteht.
- **Wiederaufsetzpunkt (Autor 2026-11-18):** Jede Rechnung über 30 min schreibt Wiederaufsetzpunkte. CalculiX: Last in Schritte teilen (≥ 10 *STEP), `*RESTART,WRITE,FREQUENCY=1`, Fortsetzen mit `*RESTART,READ`. OpenCourant/Radioss: Restart-Dateien (/RFILE) einschalten. PyBaMM/Elmer: Zwischenstände speichern. Dazu gehört je Rechnungsordner ein `neustart.sh`, das der Autor ohne Claude ausführen kann. Es überspringt fertige Läufe, setzt angefangene am letzten Punkt fort, startet die übrigen losgelöst im Scope `hermes-batterie-*` (pausierbar mit `~/bin/rechnung`) und erzeugt am Ende die Auswertung. Laufende Skripte nie in place ändern, sondern neu schreiben und mit `mv` ersetzen. Prozesse nur per PID beenden, nie `pkill -f` mit einem Muster, das im eigenen Befehl steht.
- Die **GPU** ist geteilt: ollama (PI), GX (Fusion) und FluidX3D laufen nicht gleichzeitig. Es gibt 32 GB RAM. Die Platte / ist zu 91 % voll; große Daten kommen nach `/home/cae/cae_projekte`.
- Python: `source /home/cae/hermes/batterie/umgebung.sh` (venv `.venv`).
- FreeCAD: `$FREECAD_APPIMAGE freecadcmd -c "..."` oder `freecadcmd skript.py`. Ein Modell wird parametrisch gebaut und am Ende in der GUI geöffnet.
- FluidX3D: nur in einer eigenen Kopie, nie `~/fluidx3d_cae` ändern. Lizenz beachten: nicht MIT, geänderte Quellen veröffentlichen, Referenzen zitieren.

