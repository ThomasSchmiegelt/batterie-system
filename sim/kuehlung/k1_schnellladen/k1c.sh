#!/bin/bash
# KI-generiert (Claude Sonnet, 2026-11-17). K1c: 3 Faelle (LFP K3 R 1,28; NMC K3b Q(t) gesamt / I*dU), CPU, nice 10. Dauer ca. 2-4 min.
cd /home/cae/hermes/batterie/sim/kuehlung/k1_schnellladen && source ../../../umgebung.sh
printf "%s\n" LFP_P0_K3_R128 NMC_C2gesamt_K3b NMC_C2idu_K3b | xargs -P 3 -I{} nice -n 10 python3 k1_rechnen.py {}
echo FERTIG $(date)
