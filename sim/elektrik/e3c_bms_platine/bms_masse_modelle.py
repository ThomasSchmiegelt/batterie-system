# KI-generiert (Claude Sonnet, 2026-11-24), Entwurf. Aufruf: $FREECAD_APPIMAGE freecadcmd bms_masse_modelle.py
# Volumen der KiCad-3D-Modelle (STEP) je Footprint der BMS-Platine -> _modellvolumen.json (mm3). Eigene Brücken-Footprints: /home/cae/cae_projekte/batterie/e3c/modelle.
import json, os, glob, Part
H = "/home/cae/hermes/batterie/sim/elektrik/e3c_bms_platine"
R3 = glob.glob("/home/cae/.local/share/flatpak/runtime/org.kicad.KiCad.Library.Packages3D/x86_64/stable/*/files/3dmodels")[0]
out = {}; fehl = []
for t in json.load(open(f"{H}/bms_teile.json"))["teile"]:
    lib, name = t["footprint"].split(":")
    if name in out: continue
    p = f"/home/cae/cae_projekte/batterie/e3c/modelle/{name}.step" if lib == "E3c" else f"{R3}/{lib}.3dshapes/{name}.step"
    if not os.path.exists(p): fehl.append(name); continue
    s = Part.read(p); out[name] = round(sum(x.Volume for x in s.Solids), 3)
json.dump(dict(volumen_mm3=out, ohne_modell=fehl), open(f"{H}/_modellvolumen.json", "w"), indent=1); print(len(out), "ohne Modell:", fehl)
