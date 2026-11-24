# Läuft im KiCad-Flatpak: route_dsn.py <V> dsn|ses. KI-generiert (Claude Sonnet, 2026-11-24).
# dsn: exportiert Specctra DSN aus /home/cae/cae_projekte/batterie/e3/route/cmu_<V>.kicad_pcb; ses: importiert SES, speichert cmu_<V>_geroutet.kicad_pcb
import sys, pcbnew
V, m = sys.argv[1], sys.argv[2]; D = "/home/cae/cae_projekte/batterie/e3/route"
b = pcbnew.LoadBoard(f"{D}/cmu_{V}.kicad_pcb")
if m == "dsn":
    print("DSN", pcbnew.ExportSpecctraDSN(b, f"{D}/cmu_{V}.dsn"))
else:
    print("SES", pcbnew.ImportSpecctraSES(b, f"{D}/cmu_{V}.ses")); pcbnew.SaveBoard(f"{D}/cmu_{V}_geroutet.kicad_pcb", b)
