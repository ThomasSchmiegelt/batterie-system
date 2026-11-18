#!/bin/bash
cd "/home/cae/hermes/batterie/sim/mechanik/x1b_knautschzone"
[ -n " LFP_w15:neu NMC_w20:neu" ] && ./neustart_kette.sh  LFP_w15:neu NMC_w20:neu &
[ -n " LFP_w30:neu" ] && ./neustart_kette.sh  LFP_w30:neu &
wait
source "/home/cae/hermes/batterie/sim/mechanik/x1b_knautschzone/../../../umgebung.sh"; python3 "/home/cae/hermes/batterie/sim/mechanik/x1b_knautschzone/auswerten_oc.py" > "/home/cae/hermes/batterie/sim/mechanik/x1b_knautschzone/auswerten_oc.log" 2>&1
echo "$(date '+%F %T') alles fertig, Auswertung: auswerten_oc.log" >> "/home/cae/hermes/batterie/sim/mechanik/x1b_knautschzone/neustart.log"
