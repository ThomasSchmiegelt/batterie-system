# Software (geprüft 2026-11-11)

KI-generiert (Claude Opus). Jeder Eintrag wurde auf diesem Rechner aufgerufen.

| Aufgabe | Programm | Version | Aufruf | Probe |
|---|---|---|---|---|
| Elektrochemie der Zelle | PyBaMM | 26.10.1.1 | `.venv/bin/python` | LFP `Prada2013`, SPMe, 1C bis 2,0 V: 3,514 → 2,000 V, 1,939 Ah ✓ |
| Parametrisches CAD | FreeCAD | 1.1.4 (AppImage) | `$FREECAD_APPIMAGE freecadcmd -c "..."` | Quader erzeugt, Volumen berechnet ✓ |
| Darstellung, Rendering | Blender | 4.0.2 (`/usr/bin`), 4.2.9 in `~/Applications` | `blender -b -P skript.py` | Version ✓ |
| Video zusammensetzen | ffmpeg | 6.1.1 (`/usr/bin`) | `video/erzeuge_video.sh` (libx264, drawtext) | Version ✓ |
| Vernetzung | gmsh | 4.12.1 (System), 4.15.2 (Python) | `import gmsh` | Import ✓ |
| Wärme, Festigkeit (FEM) | ElmerFEM | 26.2 | `ElmerGrid`, `ElmerSolver` | Version ✓ |
| Strömung Kühlplatte | FluidX3D (OpenCL, RTX 3090) | eigene Kopie anlegen | vorhandene Kopien `~/fluidx3d_*` | in Wasserstoff/Fusion genutzt |
| Auswertung | numpy, scipy, pandas, scikit-learn, matplotlib, plotly, pyvista, meshio, trimesh | siehe `requirements.txt` | `.venv` | Import ✓ |
| Nachbearbeitung | ParaView | System | `paraview` | vorhanden |
| Bericht | pdflatex, latexmk, pandoc | System | – | vorhanden |
| Recherche Patente | Skill `patent-recherche` (Google Patents ohne Schlüssel, 1 Anfrage/s) | 0.1.0 | `~/.hermes/skills/cae/patent-recherche/` | Suche und Abruf mit BYD-Beispiel ✓ |
| Recherche Wissen | Skill `web-recherche` (Wikipedia, OSTI, OpenAlex, arXiv) | 0.1.0 | `~/.hermes/skills/cae/web-recherche/` | aus Fusion, 29 Belege 0 Fehler |
| Lokaler Agent | PI + ollama `qwen-gross` (27B, 64k) | – | `~/.npm-global/bin/pi` | aus Fusion und Moltbot |
| Festigkeit, Seitencrash quasistatisch | CalculiX | 2.21 | `ccx` (`~/.local/bin/ccx`) | Version ✓ (2026-11-12) |
| Skizze am 3D-Modell → Prompt (Pre/Post) | Sketch-to-Prompt (eigenes Projekt, MIT) | – | `python3 -m sketch_to_prompt.server <ordner>` in `~/sketch-to-prompt` | aus Fusion |
| Wissensgraph (Notizen aus dem Wissensnetz) | Obsidian (kostenlos auch gewerblich laut obsidian.md/license, Stand 20.02.2025; nicht quelloffen) | – | **nicht installiert**; Vault = Projektordner, Notizen unter `wissen/` | – |
| Unternehmenspräsentation (.pptx, PDF) | python-pptx (MIT) + LibreOffice (System, Umwandlung in PDF) | – | python-pptx 1.0.2 installiert in .venv (2026-11-23, Vorgang B5); `soffice --headless --convert-to pdf` | LibreOffice vorhanden |
| Dynamische Crash-Rechnung X2 (explizit) | OpenCourant latest-20261011 (AGPLv3, intern genutzt, nicht weitergegeben) | latest-20261011 | `source /home/cae/cae_projekte/werkzeuge/opencourant/umgebung.sh`, dann `starter_linux64_gf -i <_0000.rad> -np 1` und `engine_linux64_gf -i <_0001.rad>` (nur CPU, `OMP_NUM_THREADS`); Rauchtest TWISBEAM bestanden (Referenz ref.extract identisch) | nur Nutzerverzeichnis, ohne sudo |
| Schaltungssimulation E3 | ngspice (BSD-3) | 42 (Ubuntu-noble-Paket, `dpkg -x` nach `~/.local/opt/ngspice`, ohne sudo) | `source umgebung.sh`, `ngspice -b` | Vorladung 912 V gerechnet ✓ (2026-11-24) |
| Schaltplan als Code E3 | SKiDL (MIT) 3.0.0, spicelib 1.6.4 | in `.venv` | `import skidl` | installiert (2026-11-24), Nutzung offen |
| Leiterplatte E3 | KiCad (Flatpak, GPL-3) | 10.0.8 (nicht 9) | `werkzeuge/kicad-cli.sh`, `werkzeuge/kicad-python.sh` (pcbnew) | Platine gebaut, DRC, Gerber, STEP, Render ✓ (2026-11-24) ; Freerouting siehe nächste Zeile |
| Autorouter E3 | Freerouting CLI (GPL-3) | 2.5.0 (Native Image, von Opus installiert, `$FREEROUTING`) | `$FREEROUTING -de x.dsn -do x.ses -mp N` | **stürzt ab** (UnsupportedFeatureError ComponentOutline, GraalVM-Serialisierung), keine SES erzeugt (2026-11-24) |

Nicht vorhanden und nicht nötig: OpenFOAM (FluidX3D und Elmer decken die Strömung ab), ngspice (die Elektrik wird in Python gerechnet, die Netzwerke sind klein).
Mögliche spätere Ergänzung: Cantera (Gaszusammensetzung beim thermischen Durchgehen), nur wenn Schritt 1 das verlangt.

Umgebung: `source umgebung.sh`. Neu aufbauen: `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`.
