#!/bin/bash
# KI-generiert (Claude Sonnet 5.5, 2026-11-25), Entwurf. Rendert die drei 3D-Szenen (pack, cmu, bms) als RGBA-Einzelbilder, fertige werden übersprungen. Aufruf: bash video/render_elektronik3d.sh  (losgelöst: siehe unten)
cd /home/cae/hermes/batterie; source umgebung.sh; O=/home/cae/cae_projekte/batterie_video/elektronik3d; mkdir -p $O
bash rechnen/gpu_warten.sh || exit 1
for S in pack cmu bms; do
  case $S in pack) SM=32;; *) SM=48;; esac
  SZENE=$S VIDEO_SAMPLES=$SM blender -b -P video/szenen_elektronik3d.py >> $O/render_$S.log 2>&1
done
date '+%F %T' > $O/FERTIG
