#!/bin/bash
# KI-generiert (Claude Sonnet, 2026-11-17). Startet alle K0-Faelle (CPU, ein Kern). Log: alle.log
cd /home/cae/hermes/batterie/sim/kuehlung/k0_zelle && source ../../../umgebung.sh
for n in $(python rechnen.py --liste); do python rechnen.py $n; done
echo FERTIG $(date)
