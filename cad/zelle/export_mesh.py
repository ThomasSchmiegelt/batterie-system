# KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. Auftrag G2-R (cad/zelle/AUFTRAG_RENDER.md).
"""Exportiert je Körper der Zelle ein OBJ (mm) nach entwurf/render/.
Aufruf: ZELLE_VARIANTE=LFP|NMC [ZELLE_AUSGABE=ordner] $FREECAD_APPIMAGE freecadcmd cad/zelle/export_mesh.py
Keine Maße im Code: Geometrie kommt aus entwurf/zelle_<V>.FCStd (erzeugt von zelle.py)."""
import os
import FreeCAD
R = os.environ.get("BATTERIE", "/home/cae/hermes/batterie")
var = os.environ.get("ZELLE_VARIANTE")
if var not in ("LFP", "NMC"): raise SystemExit("ZELLE_VARIANTE=LFP|NMC setzen")
ent = os.environ.get("ZELLE_AUSGABE") or f"{R}/cad/zelle/entwurf"
out = f"{ent}/render"; os.makedirs(out, exist_ok=True)
doc = FreeCAD.openDocument(f"{ent}/zelle_{var}.FCStd")
for o in doc.Objects:
    s = getattr(o, "Shape", None)
    if s is None or s.isNull(): continue
    pts, tri = s.tessellate(0.02)  # Abweichung 0.02 mm
    with open(f"{out}/{var}_{o.Name}.obj", "w") as f:
        f.write(f"# KI-generiert, Entwurf, mm, {var} {o.Name}\n")
        for p in pts: f.write(f"v {p.x:.5f} {p.y:.5f} {p.z:.5f}\n")
        for t in tri: f.write(f"f {t[0]+1} {t[1]+1} {t[2]+1}\n")
    print("OBJ", var, o.Name, len(pts), len(tri))
