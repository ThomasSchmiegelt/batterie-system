# KI-generiert (Claude Sonnet, 2026-11-24), Entwurf. FreeCAD: Pack-STEP (pack_<V>_e2d_e3.step) -> Dreiecksnetze nach Gruppen für die Blender-Einbauansicht der CMU (einbau_blender.py).
import os, json, FreeCAD, Import
V = os.environ["E3V"]; doc = FreeCAD.newDocument("p"); Import.insert(f"/home/cae/cae_projekte/batterie/e2/pack_{V}_e2d_e3.step", "p")
out = {"CMU": {}, "Rest": {"punkte": [], "dreiecke": []}, "Rahmen": {"punkte": [], "dreiecke": []}}
RAH = ("Seitenrahmen", "Quertraeger", "Boden")
def tess(sh, dev):
    p, t = sh.tessellate(dev); return [[v.x, v.y, v.z] for v in p], [list(x) for x in t]
n = 0
for o in doc.Objects:
    if not hasattr(o, "Shape") or o.Shape.isNull() or not o.Shape.Solids: continue
    nm = o.Label; n += 1
    if nm.startswith("CMU_"):
        p, t = tess(o.Shape, 0.05); out["CMU"][nm] = dict(punkte=p, dreiecke=t, bbox=[o.Shape.BoundBox.XMin, o.Shape.BoundBox.YMin, o.Shape.BoundBox.ZMin, o.Shape.BoundBox.XMax, o.Shape.BoundBox.YMax, o.Shape.BoundBox.ZMax]); continue
    grp = "Rahmen" if any(nm.startswith(r) for r in RAH) else "Rest"
    if nm.startswith(("Zelle", "Cell")) : continue    # Zellen weglassen (nur Umgebung der Endzone wird gezeigt)
    p, t = tess(o.Shape, 1.0); d = out[grp]; off = len(d["punkte"]); d["punkte"] += p; d["dreiecke"] += [[off + i for i in x] for x in t]
json.dump(out, open(f"/home/cae/cae_projekte/batterie/e3/einbau_{V}.json", "w"))
print("fertig", V, n, list(out["CMU"].keys())[:3], len(out["Rest"]["punkte"]), len(out["Rahmen"]["punkte"]))
