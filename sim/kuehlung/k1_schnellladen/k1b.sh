#!/bin/bash
# KI-generiert (Claude Sonnet, 2026-11-17). K1b: 7 NMC-Faelle K3b, 4 parallel, CPU, nice 10. Dauer ca. 10-15 min.
cd /home/cae/hermes/batterie/sim/kuehlung/k1_schnellladen && source ../../../umgebung.sh
python3 k1_rechnen.py --liste | grep K3b | xargs -P 4 -I{} nice -n 10 python3 k1_rechnen.py {}
echo FERTIG $(date)
