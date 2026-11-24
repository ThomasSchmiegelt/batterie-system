# KI-generiert (Claude Sonnet, 2026-11-24), Entwurf. Aufruf: $FREECAD_APPIMAGE freecadcmd modelle_bauen.py
# Hüllkörper (STEP) für die zwei selbst definierten Brücken-Footprints der BMS-Platine (E3c): Körper 13,2 mm quer zur Sperrzone. Maße = Platzhalter (Footprint-Maße, Sonnet).
import FreeCAD, Part
O = "/home/cae/cae_projekte/batterie/e3c/modelle"
for name, (b, l, h) in {"ISO_Bruecke_8": (13.2, 6.5, 3.0), "Uebertrager_Bruecke_4": (13.2, 6.5, 4.0)}.items():
    s = Part.makeBox(b, l, h, FreeCAD.Vector(-b / 2, -l / 2, 0)); s.exportStep(f"{O}/{name}.step"); print(name, s.Volume)
