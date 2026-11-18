#!/bin/bash
# KI-generiert (Claude Sonnet, 2026-11-17). K1: alle Faelle ausser P0 (Gate lief vorher), 4 parallel, CPU, nice 10. Log alle.log
cd /home/cae/hermes/batterie/sim/kuehlung/k1_schnellladen && source ../../../umgebung.sh
python k1_rechnen.py --liste | grep -vx -e LFP_P0 -e NMC_P0 | xargs -P 4 -I{} nice -n 10 python k1_rechnen.py {}
echo FERTIG $(date)
