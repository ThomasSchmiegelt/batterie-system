# E3c Prüfungen am fertigen Layout, im KiCad-Flatpak: werkzeuge/kicad-python.sh bms_pruefung.py. KI-generiert (Claude Sonnet, 2026-11-24), Entwurf.
# Ausgabe: _pruefung_roh.json (Sperrzone, überbrückende Teile, Kupferflächen je Lage, Footprint-Zähler). Dichten/Masse: bms_masse.py.
import json, math, pcbnew
H = "/home/cae/hermes/batterie/sim/elektrik/e3c_bms_platine"; b = pcbnew.LoadBoard("/home/cae/cae_projekte/batterie/e3c/bms.kicad_pcb")
info = json.load(open(f"{H}/layout_info.json")); HV = set(info["hv_netze"]); ZX0, ZX1 = info["sperrzone_x_mm"]; T = {t["ref"]: t["tag"] for t in json.load(open(f"{H}/bms_teile.json"))["teile"]}
mm = lambda v: v / 1e6
nv_x, hv_x = [], []   # x-Ausdehnung von Kupfer: NV (max x) und HV (min x)
innen = 0; kreuz_bahn = 0
def reg(netz, xmin, xmax):
    (hv_x if netz in HV else nv_x).append((xmin, xmax))
for t in b.Tracks():
    if t.Type() == pcbnew.PCB_VIA_T:
        r = mm(t.GetWidth(pcbnew.F_Cu)) / 2; x = mm(t.GetPosition().x); reg(t.GetNetname(), x - r, x + r)
        if x + r > ZX0 and x - r < ZX1: innen += 1
    else:
        w = mm(t.GetWidth()) / 2; xa, xb = sorted((mm(t.GetStart().x), mm(t.GetEnd().x))); reg(t.GetNetname(), xa - w, xb + w)
        if xb + w > ZX0 and xa - w < ZX1: innen += 1
bruecken = []
for f in b.GetFootprints():
    for p in f.Pads():
        bb = p.GetBoundingBox(); xa, xb = mm(bb.GetX()), mm(bb.GetX() + bb.GetWidth()); reg(p.GetNetname(), xa, xb)
        if xb > ZX0 and xa < ZX1: innen += 1
    xs = [(mm(p.GetBoundingBox().GetX()), mm(p.GetBoundingBox().GetX() + p.GetBoundingBox().GetWidth()), p.GetNetname()) for p in f.Pads()]
    nvp = [x for x in xs if x[1] <= ZX0 + 1e-6]; hvp = [x for x in xs if x[0] >= ZX1 - 1e-6]
    if nvp and hvp: bruecken.append(dict(ref=f.GetReference(), tag=T[f.GetReference()], pad_abstand_mm=round(min(x[0] for x in hvp) - max(x[1] for x in nvp), 3), nv_netze=sorted({x[2] for x in nvp}), hv_netze=sorted({x[2] for x in hvp})))
zonen = []
for z in b.Zones():
    if z.GetIsRuleArea(): continue
    for L in z.GetLayerSet().Seq():
        ps = z.GetFilledPolysList(L); xs = [mm(ps.CVertex(i).x) for i in range(ps.TotalVertices())] if ps.OutlineCount() else []
        if xs: reg(z.GetNetname(), min(xs), max(xs)); zonen.append(dict(netz=z.GetNetname(), lage=pcbnew.LayerName(L), x_min=round(min(xs), 2), x_max=round(max(xs), 2)))
        if xs and max(xs) > ZX0 and min(xs) < ZX1: innen += 1
nv_max = max(x[1] for x in nv_x if x[1] <= ZX0 + 1e-6 or True and x[0] < ZX0); hv_min = min(x[0] for x in hv_x)
# Bauteile NV mit Kupfer auf der HV-Seite? (NV-Kupfer rechts der Zone / HV-Kupfer links davon)
nv_rechts = sum(1 for a, c in nv_x if a > ZX1 - 1e-6); hv_links = sum(1 for a, c in hv_x if c < ZX0 + 1e-6)
lay = {pcbnew.F_Cu: "F.Cu", pcbnew.In1_Cu: "In1.Cu", pcbnew.In2_Cu: "In2.Cu", pcbnew.B_Cu: "B.Cu"}
A = {n: dict(bahn=0.0, pad=0.0, via=0.0, zone=0.0) for n in lay.values()}
nseg = nvia = 0
for t in b.Tracks():
    if t.Type() == pcbnew.PCB_VIA_T:
        nvia += 1; r = mm(t.GetWidth(pcbnew.F_Cu)) / 2; dr = mm(t.GetDrillValue()) / 2
        for n in A: A[n]["via"] += math.pi * (r * r - dr * dr)
    else:
        nseg += 1; w = mm(t.GetWidth()); A[t.GetLayerName()]["bahn"] += math.hypot(mm(t.GetEnd().x) - mm(t.GetStart().x), mm(t.GetEnd().y) - mm(t.GetStart().y)) * w + math.pi * w * w / 4
for f in b.GetFootprints():
    for p in f.Pads():
        for L, n in lay.items():
            if p.IsOnLayer(L): A[n]["pad"] += mm(p.GetSize(L).x) * mm(p.GetSize(L).y)
for z in b.Zones():
    if z.GetIsRuleArea(): continue
    for L in z.GetLayerSet().Seq(): A[pcbnew.LayerName(L)]["zone"] += z.GetFilledArea() / 1e12
from collections import Counter
cnt = Counter(str(f.GetFPID().GetLibItemName()) for f in b.GetFootprints()); bb = b.GetBoardEdgesBoundingBox()
json.dump(dict(sperrzone_x_mm=[ZX0, ZX1], sperrzone_breite_mm=ZX1 - ZX0, objekte_in_sperrzone=innen, nv_kupfer_max_x_mm=round(nv_max, 3), hv_kupfer_min_x_mm=round(hv_min, 3), abstand_nv_hv_kupfer_mm=round(hv_min - nv_max, 3),
  nv_kupfer_rechts_der_zone=nv_rechts, hv_kupfer_links_der_zone=hv_links, bruecken=bruecken, zonen=zonen, flaeche_cu_mm2=A, platine_flaeche_mm2=mm(bb.GetWidth()) * mm(bb.GetHeight()), laenge_mm=mm(bb.GetWidth()), breite_mm=mm(bb.GetHeight()),
  footprints=dict(cnt), teile=len(b.GetFootprints()), bahnsegmente=nseg, vias=nvia, lagen=b.GetCopperLayerCount()), open(f"{H}/_pruefung_roh.json", "w"), indent=1)
print("fertig", innen, round(nv_max, 3), round(hv_min, 3), len(bruecken))
