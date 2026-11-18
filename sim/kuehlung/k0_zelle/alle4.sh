#!/bin/bash
# KI-generiert (Claude Sonnet, 2026-11-17). Wiederholt die L2-Faelle mit VTU-Ausgabe in jedem Schritt (Endzustand t = 1200 s). Log alle4.log
cd /home/cae/hermes/batterie/sim/kuehlung/k0_zelle && source ../../../umgebung.sh
for n in LFP_K1_L2 LFP_K1_L2_mischung NMC_K1_L2 NMC_K2_L2 NMC_K1_L2_spalt; do python rechnen.py $n; done
echo FERTIG $(date)
