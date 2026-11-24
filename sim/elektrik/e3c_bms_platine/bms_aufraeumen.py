# Im KiCad-Flatpak: Muster via_aufraeumen.py (E3, unverändert in der Logik), dazu Füllen der Flächen. Entfernt hängende Vias (aus chk_drc.json), verbreitert Bahnen < 0,15 mm, füllt Zonen.
# KI-generiert (Claude Sonnet, 2026-11-24).
import sys, json, pcbnew, os
D = "/home/cae/cae_projekte/batterie/e3c/route"
b = pcbnew.LoadBoard(f"{D}/bms_geroutet.kicad_pcb")
pos = []
if os.path.exists(f"{D}/chk_drc.json"):
    d = json.load(open(f"{D}/chk_drc.json")); pos = [(x["items"][0]["pos"]["x"], x["items"][0]["pos"]["y"]) for x in d["violations"] if x["type"] == "via_dangling"]
vias = []; m = 0
for t in b.Tracks():
    if t.Type() == pcbnew.PCB_VIA_T:
        p = t.GetPosition()
        if any(abs(p.x / 1e6 - px) < 0.01 and abs(p.y / 1e6 - py) < 0.01 for px, py in pos): vias.append(t)
    elif t.Type() == pcbnew.PCB_TRACE_T and t.GetWidth() < pcbnew.FromMM(0.15): t.SetWidth(pcbnew.FromMM(0.15)); m += 1
for t in vias: b.Remove(t)
# Zusätzliche Masse-Fläche auf B.Cu (NV: GND, HV: HV_GND), damit durch Innenlagenbahnen abgeriegelte Massevias der In1-Fläche trotzdem verbunden sind (Lauf 5: 2 Lücken)
mm = pcbnew.FromMM; B_ = 100.0; L_ = 160.0; ZX0, ZX1 = 100.0, 110.0
for netname, x0, x1 in (("GND", 0.5, ZX0 - 0.5), ("HV_GND", ZX1 + 0.5, L_ - 0.5)):
    zz = pcbnew.ZONE(b); ls = pcbnew.LSET(); ls.AddLayer(pcbnew.B_Cu); zz.SetLayerSet(ls); zz.SetNet(b.FindNet(netname)); zz.SetLocalClearance(mm(0.2)); zz.SetMinThickness(mm(0.15))
    zz.SetPadConnection(pcbnew.ZONE_CONNECTION_THERMAL); zz.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_ALWAYS); oo = zz.Outline(); oo.NewOutline()
    for (a_, c_) in ((x0, 0.5), (x1, 0.5), (x1, B_ - 0.5), (x0, B_ - 0.5)): oo.Append(mm(a_), mm(c_))
    b.Add(zz)
pcbnew.ZONE_FILLER(b).Fill(b.Zones())
pcbnew.SaveBoard(f"{D}/bms_geroutet.kicad_pcb", b); print("vias entfernt", len(vias), "Bahnen verbreitert", m)
