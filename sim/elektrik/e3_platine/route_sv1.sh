#!/bin/bash
# KI-generiert (Claude Sonnet, 2026-11-24), Entwurf. SV1: LFP neu routen nach dem Verfahren von route_lauf2.sh (DSN -> Freerouting -> SES), 3 Varianten parallel, NMC danach per route_uebertragen.py.
cd /home/cae/hermes/batterie/sim/elektrik/e3_platine; source ../../../umgebung.sh
python3 - <<'P'
import json,shutil,pathlib
O=pathlib.Path('/home/cae/cae_projekte/batterie/e3'); R=O/'route'; a=R/'alt_vor_sv1b'; a.mkdir(exist_ok=True)
for f in list(R.glob('*')):
    if f.is_file(): shutil.move(str(f),str(a/f.name))
for v in ('LFP',):
    shutil.copy(O/f'cmu_{v}.kicad_pcb',R/f'cmu_{v}.kicad_pcb'); p=json.load(open(O/f'cmu_{v}.kicad_pro'))
    for c in p['net_settings']['classes']:
        if c['name']=='Daisy': c['clearance']=2.5
    json.dump(p,open(R/f'cmu_{v}.kicad_pro','w'),indent=1)
P
../../../werkzeuge/kicad-python.sh route_dsn.py LFP dsn 2>&1|tail -1
cd /home/cae/cae_projekte/batterie/e3/route
for x in "a 14 5" "b 30 2" "c 20 3"; do set -- $x; (nice -n 10 timeout 1800 $FREEROUTING -de cmu_LFP.dsn -do cmu_LFP_$1.ses -mp $2 -mt $3 -l en > fr_LFP_$1.log 2>&1; echo done >> fr_LFP_$1.log) & done
wait
touch /home/cae/hermes/batterie/sim/elektrik/e3_platine/route_sv1.fertig
