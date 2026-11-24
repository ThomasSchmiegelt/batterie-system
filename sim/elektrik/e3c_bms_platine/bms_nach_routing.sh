#!/bin/bash
# E3c: nach dem Routing (bms_route.sh) übernehmen und Ergebnisse neu erzeugen. KI-generiert (Claude Sonnet, 2026-11-24). Aufruf: bash bms_nach_routing.sh
cd /home/cae/hermes/batterie; source umgebung.sh; S=sim/elektrik/e3c_bms_platine; O=/home/cae/cae_projekte/batterie/e3c
cp $O/route/bms_geroutet.kicad_pcb $O/bms.kicad_pcb; cp $O/route/bms_geroutet.kicad_pro $O/bms.kicad_pro 2>/dev/null; cp $O/route/bms_geroutet.kicad_dru $O/bms.kicad_dru 2>/dev/null
werkzeuge/kicad-cli.sh pcb drc --severity-all --format json -o $O/bms_drc.json $O/bms.kicad_pcb >/dev/null
werkzeuge/kicad-cli.sh pcb export step --subst-models --force -o $O/bms.step $O/bms.kicad_pcb > $O/step.log 2>&1
werkzeuge/kicad-cli.sh pcb export gerbers -o $O/gerber/ $O/bms.kicad_pcb >/dev/null 2>&1
werkzeuge/kicad-python.sh $S/bms_pruefung.py | tail -1
$FREECAD_APPIMAGE freecadcmd $S/bms_masse_modelle.py > $O/masse_modelle.log 2>&1
$FREECAD_APPIMAGE freecadcmd $S/bms_bauteile_netz.py > $O/bauteile_netz.log 2>&1
python3 $S/bms_ergebnis.py | tail -3
touch $O/nach_routing.fertig
python3 $S/bms_routing_ergebnis.py > /dev/null
touch $O/nach_routing_bilder.fertig
