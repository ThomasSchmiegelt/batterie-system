#!/bin/bash
# KI-generiert (Claude Sonnet, 2026-11-24), Entwurf. Routing-Lauf E3 (Ablauf wie Lauf 3): DSN -> Freerouting -mp 10 -> SES -> DRC. Aufruf: bash route_lauf.sh [Ordner-Suffix fürs alte]
cd /home/cae/hermes/batterie/sim/elektrik/e3_platine; source ../../../umgebung.sh
python3 - <<'P'
import json,shutil,pathlib,time
O=pathlib.Path('/home/cae/cae_projekte/batterie/e3'); R=O/'route'; a=R/'alt_lauf9'; a.mkdir(exist_ok=True)
for f in list(R.glob('*')):
    if f.is_file(): shutil.move(str(f),str(a/f.name))
for v in ('LFP','NMC'):
    shutil.copy(O/f'cmu_{v}.kicad_pcb',R/f'cmu_{v}.kicad_pcb'); p=json.load(open(O/f'cmu_{v}.kicad_pro'))
    for c in p['net_settings']['classes']:
        if c['name']=='Daisy': c['clearance']=2.5
    json.dump(p,open(R/f'cmu_{v}.kicad_pro','w'),indent=1)
P
for v in LFP NMC; do ../../../werkzeuge/kicad-python.sh route_dsn.py $v dsn 2>&1|tail -1; done
cd /home/cae/cae_projekte/batterie/e3/route
for v in LFP NMC; do (nice -n 10 timeout 2100 $FREEROUTING -de cmu_$v.dsn -do cmu_$v.ses -mp 14 -mt 5 -l en > fr_$v.log 2>&1; echo done >> fr_$v.log) & done
for i in $(seq 1 450); do grep -q "^done" fr_LFP.log && grep -q "^done" fr_NMC.log && break; sleep 5; done
ls *.ses > /dev/null 2>&1 && bash /tmp/claude-1003/chk.sh > /home/cae/hermes/batterie/sim/elektrik/e3_platine/route_chk.txt 2>&1
touch /home/cae/hermes/batterie/sim/elektrik/e3_platine/route.fertig
