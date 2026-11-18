#!/bin/bash
# KI-generiert (Claude Sonnet, 2026-11-17). Setzt K0 ab NMC_K1_L2 fort (iterativer Loeser fuer transient). Log: alle2.log
cd /home/cae/hermes/batterie/sim/kuehlung/k0_zelle && source ../../../umgebung.sh
for n in $(python rechnen.py --liste | sed -n '/^NMC_K1_L2$/,$p'); do python rechnen.py $n; done
echo FERTIG $(date)
