#!/bin/bash
# KI-generiert (Claude Sonnet, 2026-11-24), Entwurf. SV1: Pack-CAD mit PACK_SV1=1 (setzt PACK_E3C voraus). Aufruf: bash pack_sv1.sh LFP NMC. Dauer LFP ca. 3 min, NMC ca. 8 min (CPU).
cd /home/cae/hermes/batterie; source umgebung.sh
for v in "$@"; do PACK_SV1=1 PACK_E3C=1 PACK_VARIANTE=$v nice -n 10 $FREECAD_APPIMAGE freecadcmd cad/pack/pack_e2d.py > sim/mechanik/sv1_stecker_verschraubung/pack_${v}_sv1.log 2>&1; done
touch sim/mechanik/sv1_stecker_verschraubung/pack_sv1_$(echo $@ | tr ' ' _).fertig
