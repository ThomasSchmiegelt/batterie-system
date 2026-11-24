# KI-generiert (Claude Sonnet, 2026-11-24), Entwurf. Im FreeCAD (freecadcmd): Bauteile aus cmu_<V>.step (KiCad-Export) als Dreiecksnetz; Platinenkörper (120 x 60 x 1,6) wird weggelassen.
import os, json, FreeCAD, Part
V = os.environ["E3V"]; s = Part.read(f"/home/cae/cae_projekte/batterie/e3/cmu_{V}.step"); bb = s.BoundBox
pts, tri = [], []
for so in s.Solids:
    b = so.BoundBox
    if b.XLength > 100 and b.YLength > 50 and b.ZLength < 2.0: board = b; continue
    p, t = so.tessellate(0.05)
    o = len(pts); pts += [[v.x, v.y, v.z] for v in p]; tri += [[o + i for i in x] for x in t]
json.dump(dict(punkte=pts, dreiecke=tri, step_bbox=[bb.XMin, bb.YMin, bb.ZMin, bb.XMax, bb.YMax, bb.ZMax], platine_bbox=[board.XMin, board.YMin, board.ZMin, board.XMax, board.YMax, board.ZMax]), open(f"/home/cae/cae_projekte/batterie/e3/bauteile_{V}.json", "w"))
print("fertig", V, len(s.Solids), len(pts), "board", board.ZMin, board.ZMax)
