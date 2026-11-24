# KI-generiert (Claude Sonnet, 2026-11-24). Läuft mit kicad-python.sh: schreibt Pads je Netz des Layouts nach e3c/pcb_netze.json
import pcbnew, json
b = pcbnew.LoadBoard("/home/cae/cae_projekte/batterie/e3c/bms.kicad_pcb"); d = {}
for fp in b.GetFootprints():
    for p in fp.Pads():
        if p.GetNetname(): d.setdefault(p.GetNetname(), []).append([fp.GetReference(), p.GetNumber()])
json.dump(d, open("/home/cae/cae_projekte/batterie/e3c/pcb_netze.json", "w"))
