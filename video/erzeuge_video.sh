#!/bin/bash
# KI-generiert (Claude Sonnet, 2026-11-23), Entwurf. Auftrag video/AUFTRAG_VIDEO.md (REQ-D13). Arbeitet nach neustart-Logik: vorhandene Einzelbilder werden übersprungen.
# Aufruf: bash video/erzeuge_video.sh [text|render|zusammen|alles]   (alles = Standard; render wartet vorher auf freie GPU und läuft losgelöst im Scope hermes-batterie-video)
cd /home/cae/hermes/batterie; source umgebung.sh; D=/home/cae/cae_projekte/batterie_video; F=$D/frames; mkdir -p $F
NF=2750
text()    { python3 video/begleittext.py; }
render()  {
  bash rechnen/gpu_warten.sh || { echo "GPU-Wartepause abgebrochen (rechnen/STOP)"; return 1; }
  # Fehlende Bilder: Blender überspringt vorhandene (use_overwrite=False). EEVEE braucht die GPU.
  systemd-run --user --scope --unit=hermes-batterie-video-$$ blender -b -P video/szenen.py -- 0 $((NF-1)) >> $D/render.log 2>&1
}
zusammen() {
  n=$(ls $F/*.png 2>/dev/null | wc -l); [ "$n" -lt $NF ] && { echo "nur $n von $NF Bildern"; return 1; }
  ffmpeg -y -hide_banner -loglevel error -framerate 25 -i $F/%04d.png -filter_complex \
   "drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:text='Thomas Schmiegelt':fontcolor=white:fontsize=30:borderw=2:bordercolor=black@0.7:x=(w-text_w)/2:y=h-52[v]" \
   -map "[v]" -frames:v $NF -c:v libx264 -pix_fmt yuv420p -crf 18 -r 25 video/abschluss.mp4 && echo "video/abschluss.mp4 fertig"
}
case "${1:-alles}" in text) text;; render) render;; zusammen) zusammen;; alles) text && render && zusammen;; esac
