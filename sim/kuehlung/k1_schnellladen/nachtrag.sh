#!/bin/bash
# KI-generiert (Claude Sonnet, 2026-11-17). K1 Nachtrag: alle NMC-Faelle auf aktuellem CAD-Netz (Kern r 6,25), K3 mit Tab-Scheibe. 4 parallel, CPU, nice 10.
cd /home/cae/hermes/batterie/sim/kuehlung/k1_schnellladen && source ../../../umgebung.sh
python k1_rechnen.py --liste | grep NMC | xargs -P 4 -I{} nice -n 10 python k1_rechnen.py {}
echo FERTIG $(date)
