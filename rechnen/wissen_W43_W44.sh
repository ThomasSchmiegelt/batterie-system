#!/bin/bash
# KI-generiert (Claude Sonnet, 2026-11-23). QN2/QN1: W43, W44 nacheinander, GPU zuerst prüfen.
cd /home/cae/hermes/batterie
for t in W43 W44; do
  bash rechnen/gpu_warten.sh && bash forschung/lauf.sh wissen $t
done
echo "$(date '+%F %T') W43_W44 fertig" >> rechnen/verlauf.log; touch rechnen/W43_W44_FERTIG
