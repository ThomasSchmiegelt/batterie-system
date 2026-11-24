# Läuft im KiCad-Flatpak: bms_route_dsn.py dsn|ses (Muster: sim/elektrik/e3_platine/route_dsn.py, unverändert übernommen bis auf Namen). KI-generiert (Claude Sonnet, 2026-11-24).
import sys, pcbnew
m = sys.argv[1]; D = "/home/cae/cae_projekte/batterie/e3c/route"
b = pcbnew.LoadBoard(f"{D}/bms.kicad_pcb")
if m == "dsn": print("DSN", pcbnew.ExportSpecctraDSN(b, f"{D}/bms.dsn"))
else: print("SES", pcbnew.ImportSpecctraSES(b, f"{D}/bms.ses")); pcbnew.SaveBoard(f"{D}/bms_geroutet.kicad_pcb", b)
