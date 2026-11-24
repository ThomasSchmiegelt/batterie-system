#!/bin/bash
# KI-generiert (Claude Sonnet, 2026-11-24), Entwurf. Platine neu bauen (E3_L, E3_PLATZ), Regeln, Platzierungs-DRC. Aufruf: E3_L=120 bash platz_lauf.sh
cd /home/cae/hermes/batterie/sim/elektrik/e3_platine; source ../../../umgebung.sh; O=/home/cae/cae_projekte/batterie/e3; K=/home/cae/hermes/batterie/werkzeuge/kicad-cli.sh
for v in LFP NMC; do E3_L=${E3_L:-120} E3_PLATZ=${E3_PLATZ:-B} ../../../werkzeuge/kicad-python.sh pcb_bauen.py $v 2>&1 | tail -1; done
python3 drc_regeln.py | tail -1
for v in LFP NMC; do $K pcb drc --severity-all --format json -o $O/platz_drc_$v.json $O/cmu_$v.kicad_pcb >/dev/null 2>&1; python3 -c "
import json,collections;d=json.load(open('$O/platz_drc_$v.json'));print('$v',collections.Counter(x['type'] for x in d['violations']))"; done
