#!/bin/bash
# E3c Ablauf: Layout -> DSN -> Freerouting -> SES -> Aufräumen -> DRC. KI-generiert (Claude Sonnet, 2026-11-24). Aufruf (losgelöst): bash bms_route.sh [Lauf-Nr]
cd /home/cae/hermes/batterie; source umgebung.sh; S=sim/elektrik/e3c_bms_platine; O=/home/cae/cae_projekte/batterie/e3c; N=${1:-5}
python3 $S/bms_regeln.py > /dev/null
werkzeuge/kicad-python.sh $S/bms_pcb_bauen.py | tail -1
cp $O/bms.kicad_pcb $O/bms.kicad_pro $O/bms.kicad_dru $O/route/; cp $O/bms.kicad_pro $O/route/bms_geroutet.kicad_pro; cp $O/bms.kicad_dru $O/route/bms_geroutet.kicad_dru
werkzeuge/kicad-python.sh $S/bms_route_dsn.py dsn; rm -f $O/route/bms.ses
cd $O/route; nice -n 10 timeout 1500 $FREEROUTING -de bms.dsn -do bms.ses -mp 10 > fr$N.log 2>&1; cp bms.ses ses_lauf$N.ses
cd /home/cae/hermes/batterie; werkzeuge/kicad-python.sh $S/bms_route_dsn.py ses; rm -f $O/route/chk_drc.json
werkzeuge/kicad-cli.sh pcb drc --severity-all --format json -o $O/route/chk_drc.json $O/route/bms_geroutet.kicad_pcb >/dev/null
werkzeuge/kicad-python.sh $S/bms_aufraeumen.py
werkzeuge/kicad-cli.sh pcb drc --severity-all --format json -o $O/route/chk_drc2.json $O/route/bms_geroutet.kicad_pcb >/dev/null
python3 $S/drc_zeigen.py $O/route/chk_drc2.json | cut -c1-260 | head -12
touch $O/route/lauf$N.fertig
