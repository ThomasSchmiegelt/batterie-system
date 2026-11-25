#!/bin/bash
# KI-generiert (Claude Sonnet 5.5, 2026-11-25), Entwurf. Auftrag video/AUFTRAG_VIDEO_ELEKTRONIK.md (REQ-D13, BAT-DOC-13c). Stufe 2: Szenen 4 und 5 sind 3D (Blender EEVEE, RGBA) aus video/szenen_elektronik3d.py, gerendert mit video/render_elektronik3d.sh nach /home/cae/cae_projekte/batterie_video/elektronik3d/; das Zusammensetzen ist CPU (Pillow).
# Aufruf: bash video/erzeuge_video_elektronik.sh [daten|storyboard|render3d|render|zusammen|alles]   (vorhandene Einzelbilder werden übersprungen)
cd /home/cae/hermes/batterie; source umgebung.sh; D=/home/cae/cae_projekte/batterie_video/elektronik; mkdir -p $D/bilder; NF=4125
render3d()   { systemd-run --user --scope --unit=hermes-batterie-video-elektronik bash video/render_elektronik3d.sh; }   # vorher: bash rechnen/gpu_warten.sh (steht im Skript)
daten()      { echo "daten.json liegt vor (Haiku, Opus): video/elektronik/daten.json"; }
storyboard() { echo "Storyboard: video/elektronik/STORYBOARD_kolibri.md (Kolibri 1, geprüft: pruefung_storyboard.txt)"; }
render()     { [ -f $D/layout.json ] || python3 - <<'P'
import sys, json; sys.path.insert(0, "video"); import graph_zeitraffer as g
ids = g.knoten(); E = g.kanten(ids); P, _ = g.layout(ids, E); json.dump({"ids": ids, "P": P.tolist()}, open("/home/cae/cae_projekte/batterie_video/elektronik/layout.json", "w"))
P
  systemd-run --user --scope --unit=hermes-batterie-video-elektronik python3 video/erzeuge_video_elektronik.py >> $D/render.log 2>&1; }
zusammen()   {
  n=$(ls $D/bilder/*.png 2>/dev/null | wc -l); [ "$n" -lt $NF ] && { echo "nur $n von $NF Bildern"; return 1; }
  ffmpeg -y -hide_banner -loglevel error -framerate 25 -i $D/bilder/%04d.png -c:v libx264 -pix_fmt yuv420p -crf 18 -r 25 video/elektronik_nachverfolgung.mp4 && echo "video/elektronik_nachverfolgung.mp4 fertig"; }
case "${1:-alles}" in daten) daten;; storyboard) storyboard;; render) render;; render3d) render3d;; zusammen) zusammen;; alles) daten; storyboard; render && zusammen;; esac
