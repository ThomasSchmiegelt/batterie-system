#!/bin/bash
# KI-generiert (Claude Sonnet, 2026-11-17). K1 Render (Blender Cycles CPU, nice 10). Log render.log
cd /home/cae/hermes/batterie/sim/kuehlung/k1_schnellladen && source ../../../umgebung.sh
python k1_render.py --samples 128
echo FERTIG $(date)
