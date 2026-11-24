# Im KiCad-Flatpak: entfernt hängende Vias (DRC via_dangling) und verbreitert Bahnen unter 0,15 mm (Mindestbreite) aus der Router-Ausgabe auf 0,15 mm. KI-generiert (Claude Sonnet, 2026-11-24)
import sys, json, pcbnew
V = sys.argv[1]; D = "/home/cae/cae_projekte/batterie/e3/route"
b = pcbnew.LoadBoard(f"{D}/cmu_{V}_geroutet.kicad_pcb"); d = json.load(open(f"{D}/chk_{V}_drc.json"))
pos = [(x["items"][0]["pos"]["x"], x["items"][0]["pos"]["y"]) for x in d["violations"] if x["type"] == "via_dangling"]
vias = []; m = 0
for t in b.Tracks():
    if t.Type() == pcbnew.PCB_VIA_T:
        p = t.GetPosition()
        if any(abs(p.x / 1e6 - px) < 0.01 and abs(p.y / 1e6 - py) < 0.01 for px, py in pos): vias.append(t)
    elif t.Type() == pcbnew.PCB_TRACE_T and t.GetWidth() < pcbnew.FromMM(0.15): t.SetWidth(pcbnew.FromMM(0.15)); m += 1
for t in vias: b.Remove(t)
pcbnew.SaveBoard(f"{D}/cmu_{V}_geroutet.kicad_pcb", b); print("vias entfernt", len(vias), "Bahnen verbreitert", m)
