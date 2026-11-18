# Software (geprüft 2026-11-11)

KI-generiert (Claude Opus). Jeder Eintrag wurde auf diesem Rechner aufgerufen.

| Aufgabe | Programm | Version | Aufruf | Probe |
|---|---|---|---|---|
| Elektrochemie der Zelle | PyBaMM | 26.10.1.1 | `.venv/bin/python` | LFP `Prada2013`, SPMe, 1C bis 2,0 V: 3,514 → 2,000 V, 1,939 Ah ✓ |
| Parametrisches CAD | FreeCAD | 1.1.4 (AppImage) | `$FREECAD_APPIMAGE freecadcmd -c "..."` | Quader erzeugt, Volumen berechnet ✓ |
| Darstellung, Rendering | Blender | 4.0.2 (`/usr/bin`), 4.2.9 in `~/Applications` | `blender -b -P skript.py` | Version ✓ |
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
| Unternehmenspräsentation (.pptx, PDF) | python-pptx (MIT) + LibreOffice (System, Umwandlung in PDF) | – | **python-pptx nicht installiert**, erst mit Vorgang B5; `soffice --headless --convert-to pdf` | LibreOffice vorhanden |

Nicht vorhanden und nicht nötig: OpenFOAM (FluidX3D und Elmer decken die Strömung ab), ngspice (die Elektrik wird in Python gerechnet, die Netzwerke sind klein).
Mögliche spätere Ergänzung: Cantera (Gaszusammensetzung beim thermischen Durchgehen), nur wenn Schritt 1 das verlangt.

Umgebung: `source umgebung.sh`. Neu aufbauen: `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`.
