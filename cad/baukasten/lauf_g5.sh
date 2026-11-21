#!/bin/bash
# KI-generiert (Claude Opus, 2026-11-20), Entwurf. G5-Rechenkette ohne KI: Montage → Netze → Renders → Beschriftung → Stückliste/Kosten → Bericht.
# Läuft losgelöst (nohup), schreibt cad/baukasten/ausgabe/lauf_g5.log, Ende: Zeile "LAUF_G5 ENDE <status>". Abbruch: touch cad/baukasten/STOP.
# Aufruf: nohup bash cad/baukasten/lauf_g5.sh [montage|render|rest|alle] > /dev/null 2>&1 &
cd /home/cae/hermes/batterie; source umgebung.sh >/dev/null 2>&1
LOG=cad/baukasten/ausgabe/lauf_g5.log; ART="${1:-alle}"; F=0
s() { [ -f cad/baukasten/STOP ] && { echo "STOP $(date +%T)" >>$LOG; echo "LAUF_G5 ENDE gestoppt" >>$LOG; exit 1; }; echo "== $(date +%T) $*" >>$LOG; "$@" >>$LOG 2>&1 || { echo "FEHLER: $*" >>$LOG; F=$((F+1)); }; }
echo "LAUF_G5 START $(date) $ART" >$LOG
for V in LFP NMC; do
  export PACK_VARIANTE=$V
  if [ "$ART" = alle -o "$ART" = montage ]; then G5_STEP=0 s $FREECAD_APPIMAGE freecadcmd cad/baukasten/montage.py; grep -m1 "G5 Montage" cad/baukasten/ausgabe/pruefung_$V.txt >>$LOG; fi
  if [ "$ART" != rest ]; then
    s $FREECAD_APPIMAGE freecadcmd cad/baukasten/render_g5_export.py
    G5_SCHNITT=1 s $FREECAD_APPIMAGE freecadcmd cad/baukasten/render_g5_export.py
    RENDER_SAMPLES=${RENDER_SAMPLES:-32} s $BLENDER -b -P cad/baukasten/render_g5.py
  fi
done
s python3 cad/baukasten/label_g5.py LFP,NMC
s cp cad/baukasten/bilder/g5_*.png bericht/bilder/
s python3 pm/bauteile/stueckliste_v3.py --aus-cad
s python3 pm/kosten/kosten.py; s python3 pm/kosten/bilder.py; s python3 pm/kosten/doku.py
s cp docs/13_stueckliste_LFP.md docs/13_stueckliste_NMC.md pm/bauteile/stueckliste_LFP.json pm/bauteile/stueckliste_NMC.json bericht/stueckliste/
cd bericht; s pdflatex -interaction=nonstopmode bericht.tex; s pdflatex -interaction=nonstopmode bericht.tex; cd ..
s python3 pm/plan/bilder.py
echo "LAUF_G5 ENDE fehler=$F $(date +%T)" >>$LOG
# PI (lokal, ollama, Werkzeuge read/bash/write) schreibt den Prüfbericht; Opus liest ihn und prüft Stichproben.
echo "== $(date +%T) PI Prüfbericht" >>$LOG
timeout 3600 "$HOME/.npm-global/bin/pi" --provider ollama --model "${MODELL:-qwen-gross:latest}" --no-extensions --no-skills --no-session \
  --tools read,bash,write -p "$(cat cad/baukasten/AUFTRAG_PI_G5.md)" >>$LOG 2>&1 || echo "FEHLER: PI" >>$LOG
echo "LAUF_G5 PI ENDE $(date +%T)" >>$LOG
EOF_MARK=1
