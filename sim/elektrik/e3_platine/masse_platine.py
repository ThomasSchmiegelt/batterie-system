# KI-generiert (Claude Sonnet, 2026-11-24), Entwurf. Im KiCad-Flatpak: Kupferfläche je Lage aus dem Layout, Masse nach ERWARTUNG.md Nachtrag 6.
# Werte: FR4 1,85 g/cm3, Cu 8,96 g/cm3, 70 um Cu (außen laut Erwartung; Innenlagen ebenfalls 70 um = OFFEN, nicht in der Erwartung), Pad 1,0 mm x 3 g/cm3 (ENT-185),
# Bauteilmassen aus Nachtrag 6, Stecker = STEP-Volumen (KiCad-Bibliothek) x 1,4 g/cm3. Überlappungen von Bahn/Pad/Via werden nicht abgezogen (obere Schranke).
import sys, json, math, pcbnew
V = sys.argv[1]; b = pcbnew.LoadBoard(f"/home/cae/cae_projekte/batterie/e3/cmu_{V}.kicad_pcb")
lay = {pcbnew.F_Cu: "F.Cu", pcbnew.In1_Cu: "In1.Cu", pcbnew.In2_Cu: "In2.Cu", pcbnew.B_Cu: "B.Cu"}
A = {n: dict(bahn=0.0, pad=0.0, via=0.0, zone=0.0) for n in lay.values()}
for t in b.Tracks():
    if t.Type() == pcbnew.PCB_VIA_T:
        r = t.GetWidth(pcbnew.F_Cu) / 2e6; dr = t.GetDrillValue() / 2e6; a = math.pi * (r * r - dr * dr)
        for n in A: A[n]["via"] += a
    else:
        x1, y1, x2, y2 = t.GetStart().x / 1e6, t.GetStart().y / 1e6, t.GetEnd().x / 1e6, t.GetEnd().y / 1e6; w = t.GetWidth() / 1e6
        A[t.GetLayerName()]["bahn"] += math.hypot(x2 - x1, y2 - y1) * w + math.pi * w * w / 4
for f in b.GetFootprints():
    for p in f.Pads():
        for L, n in lay.items():
            if p.IsOnLayer(L): A[n]["pad"] += p.GetSize(L).x / 1e6 * p.GetSize(L).y / 1e6
for z in b.Zones():
    A[z.GetLayerName()]["zone"] += z.GetFilledArea() / 1e12
from collections import Counter
cnt = Counter(str(f.GetFPID().GetLibItemName()) for f in b.GetFootprints())
bb = b.GetBoardEdgesBoundingBox(); area = bb.GetWidth() / 1e6 * bb.GetHeight() / 1e6
json.dump(dict(flaeche_cu_mm2=A, platine_flaeche_mm2=area, footprints=dict(cnt)), open(f"/home/cae/hermes/batterie/sim/elektrik/e3_platine/_masse_roh_{V}.json", "w"))
