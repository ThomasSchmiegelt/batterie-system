# Auftrag Sonnet: Abschlussvideo (REQ-D13)

KI-generiert (Claude Opus, 2026-11-23). Anlass ist der Autor: „bei dem ersten projekt haben wir noch die präsentation und das video vergessen“.
Plan und Regeln stehen in `video/STORYBOARD.md` und gelten. Vor allem: Im Bild steht **nur „Thomas Schmiegelt“** unten, Erklärungen gehören in den Begleittext.

## Umfang (erste Fassung, Länge etwa 90–120 s)
- Variante LFP, Endstand G5.9. Die Szenen 1–8 nach Storyboard, je Bauteilgruppe einblenden, am Ende ein Rundflug und die Explosionsdarstellung.
- Geometrie: Aus dem FreeCAD-Baukasten (`cad/baukasten`, Maße aus parameter.json) je Bauteilgruppe exportieren, als glTF oder STL nach `/home/cae/cae_projekte/batterie_video/` (große Daten nicht ins Repo, die Platte / ist knapp). Vorhandene Exporte nutzt du, wenn es welche gibt.
- In Szene 6 kommt ein Ergebnisbild der Kühlung (Elmer V4p) als eingeblendete Ebene, in Szene 8 kurz ein Crashbild X3. Vorhandene PNG/MP4 verwenden.
- Blender im Hintergrund (`blender -b -P skript.py`), Renderer EEVEE oder Cycles, 1280×720, 25 fps. **Vor dem Rendern** `bash rechnen/gpu_warten.sh`, die GPU nicht doppelt belegen. Rendern losgelöst (setsid) im Scope `hermes-batterie-video`, pausierbar. Einzelbilder speichern, damit ein Abbruch weiterlaufen kann.
- Zusammenbau mit ffmpeg → `video/abschluss.mp4` (H.264). Den Begleittext `video/begleittext.md` (DE) erzeugt ein Skript aus `pm.py kontext <BT>`, nicht frei geschrieben.
- Skripte: `video/erzeuge_video.sh` und `video/szenen.py`, mit `neustart.sh`-Logik (fertige Bilder überspringen).
- Vor dem Rendern die Dauer nennen. Prüfung: 6 Standbilder aus dem fertigen Video als PNG ins Scratchpad und ansehen, ob die Teile sichtbar sind, nichts abgeschnitten ist und nur der Name im Bild steht.
- Zeile in docs/08, Software in SOFTWARE.md, wenn neu.

Abbruch: Zurück an Opus geht es, wenn der Export aus FreeCAD scheitert, die Renderzeit über 2 h liegt oder eine Szene ein Bauteil braucht, das es nicht gibt. Rückmeldung höchstens 6 Zeilen.
