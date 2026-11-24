# KI-generiert (Claude Sonnet, 2026-11-24), Entwurf. Muster: e3_platine/bauteile_netz.py. Im FreeCAD (freecadcmd): Bauteile aus bms.step (KiCad-Export) als Dreiecksnetz; Platinenkörper (160 x 100 x 1,6) wird weggelassen.
import os, json, FreeCAD, Part
s = Part.read("/home/cae/cae_projekte/batterie/e3c/bms.step"); bb = s.BoundBox
pts, tri = [], []; board = None; hmax = 0.0
for so in s.Solids:
    b = so.BoundBox
    if b.XLength > 100 and b.YLength > 50 and b.ZLength < 2.0: board = b; continue
    p, t = so.tessellate(0.05)
    o = len(pts); pts += [[v.x, v.y, v.z] for v in p]; tri += [[o + i for i in x] for x in t]
json.dump(dict(punkte=pts, dreiecke=tri, step_bbox=[bb.XMin, bb.YMin, bb.ZMin, bb.XMax, bb.YMax, bb.ZMax], platine_bbox=[board.XMin, board.YMin, board.ZMin, board.XMax, board.YMax, board.ZMax], solids=len(s.Solids)), open("/home/cae/cae_projekte/batterie/e3c/bauteile.json", "w"))
print("fertig", len(s.Solids), len(pts), "board", board.ZMin, board.ZMax, "bbox", bb.XLength, bb.YLength, bb.ZLength)
