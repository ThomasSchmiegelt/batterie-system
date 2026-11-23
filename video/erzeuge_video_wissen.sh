#!/bin/bash
# KI-generiert (Claude Sonnet, 2026-11-23), Entwurf. Auftrag video/AUFTRAG_VIDEO_WISSEN.md (REQ-D13, BAT-DOC-13b). Setzt fort: vorhandene Einzelbilder werden übersprungen.
# Aufruf: bash video/erzeuge_video_wissen.sh [text|graph|render|zusammen|alles]   (alles = Standard; render wartet vorher auf freie GPU, Scope hermes-batterie-video-wissen, pausierbar mit ~/bin/rechnung)
cd /home/cae/hermes/batterie; source umgebung.sh; D=/home/cae/cae_projekte/batterie_video/wissen; mkdir -p $D/graph $D/teile
NF=3150
graph()   { systemd-run --user --scope --unit=hermes-batterie-video-wissen-graph python3 video/graph_zeitraffer.py bilder >> $D/graph.log 2>&1; }   # CPU, darf parallel zum Rendern laufen
render()  {
  bash rechnen/gpu_warten.sh || { echo "GPU-Wartepause abgebrochen (rechnen/STOP)"; return 1; }
  VIDEO_VARIANTE=wissen systemd-run --user --scope --unit=hermes-batterie-video-wissen blender -b -P video/szenen.py -- 0 $((NF-1)) >> $D/render.log 2>&1
}
text()    { python3 video/begleittext_wissen.py; }
zusammen() {
  for k in graph teile; do n=$(ls $D/$k/*.png 2>/dev/null | wc -l); [ "$n" -lt $NF ] && { echo "$k: nur $n von $NF Bildern"; return 1; }; done
  ffmpeg -y -hide_banner -loglevel error -framerate 25 -i $D/graph/%04d.png -framerate 25 -i $D/teile/%04d.png -filter_complex \
   "[0:v][1:v]overlay,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:text='Thomas Schmiegelt':fontcolor=white:fontsize=30:borderw=2:bordercolor=black@0.7:x=(w-text_w)/2:y=h-52[v]" \
   -map "[v]" -frames:v $NF -c:v libx264 -pix_fmt yuv420p -crf 18 -r 25 video/abschluss_wissen.mp4 && echo "video/abschluss_wissen.mp4 fertig"
}
case "${1:-alles}" in text) text;; graph) graph;; render) render;; zusammen) zusammen;; alles) graph && render && text && zusammen;; esac
