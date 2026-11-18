#!/bin/bash
# KI-generiert (Claude Sonnet, 2026-11-17). K1: P0-Abgleich mit K0 L2 (CPU, nice 10)
cd /home/cae/hermes/batterie/sim/kuehlung/k1_schnellladen && source ../../../umgebung.sh
nice -n 10 python k1_rechnen.py LFP_P0 & nice -n 10 python k1_rechnen.py NMC_P0 & wait
echo FERTIG $(date)
