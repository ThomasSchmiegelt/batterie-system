#!/bin/bash
# KI-generiert (Claude Sonnet, 2026-11-17). Wiederholt die beiden NMC-Netzstudienfaelle (Feinheit 2) mit iterativem Loeser (Umfpack: Speicherfehler). Log alle3.log
cd /home/cae/hermes/batterie/sim/kuehlung/k0_zelle && source ../../../umgebung.sh
for n in NMC_K1_L1_f2 NMC_K2_L1_f2; do python rechnen.py $n; done
echo FERTIG $(date)
