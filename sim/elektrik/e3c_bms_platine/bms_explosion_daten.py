# KI-generiert (Claude Sonnet, 2026-11-24), Entwurf. Muster: e3_platine/explosion_daten.py. Im KiCad-Flatpak: Leiterbild je Lage als JSON für die Blender-Explosionsansicht (bms_explosion_blender.py).
import sys, json, pcbnew
b = pcbnew.LoadBoard(f"/home/cae/cae_projekte/batterie/e3c/bms.kicad_pcb")
bb = b.GetBoardEdgesBoundingBox(); out = dict(x0=bb.GetX() / 1e6, y0=bb.GetY() / 1e6, w=bb.GetWidth() / 1e6, h=bb.GetHeight() / 1e6, bahn=[], pads=[], vias=[], zonen=[])
for t in b.Tracks():
    if t.Type() == pcbnew.PCB_VIA_T: out["vias"].append([t.GetPosition().x / 1e6, t.GetPosition().y / 1e6, t.GetWidth(pcbnew.F_Cu) / 1e6, t.GetDrillValue() / 1e6, t.GetNetname()])
    else: out["bahn"].append([t.GetLayerName(), t.GetStart().x / 1e6, t.GetStart().y / 1e6, t.GetEnd().x / 1e6, t.GetEnd().y / 1e6, t.GetWidth() / 1e6])
for f in b.GetFootprints():
    for p in f.Pads():
        r = p.GetBoundingBox(); out["pads"].append(["F.Cu" if p.IsOnLayer(pcbnew.F_Cu) else "B.Cu", r.GetCenter().x / 1e6, r.GetCenter().y / 1e6, r.GetWidth() / 1e6, r.GetHeight() / 1e6, f.GetReference()])
for z in b.Zones():
    z.GetFilledPolysList(z.GetFirstLayer()) if False else None
    for L in z.GetLayerSet().Seq():
        ps = z.GetFilledPolysList(L)
        for i in range(ps.OutlineCount()):
            o = ps.Outline(i); out["zonen"].append([pcbnew.LayerName(L), z.GetNetname(), [[o.CPoint(k).x / 1e6, o.CPoint(k).y / 1e6] for k in range(o.PointCount())]])
json.dump(out, open(f"/home/cae/cae_projekte/batterie/e3c/explosion.json", "w"))
print(len(out["bahn"]), len(out["vias"]), len(out["pads"]), len(out["zonen"]))
