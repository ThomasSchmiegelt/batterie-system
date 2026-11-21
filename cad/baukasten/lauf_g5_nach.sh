#!/bin/bash
# KI-generiert (Claude Opus, 2026-11-20). Nachlauf: fehlende Ansichten draufsicht, kabelplan, bruecke rendern, beschriften, Bericht bauen.
cd /home/cae/hermes/batterie; source umgebung.sh >/dev/null 2>&1; LOG=cad/baukasten/ausgabe/lauf_g5_nach.log; echo "START $(date +%T)" >$LOG
for V in LFP NMC; do PACK_VARIANTE=$V RENDER_NUR=draufsicht,kabelplan,bruecke RENDER_SAMPLES=32 $BLENDER -b -P cad/baukasten/render_g5.py 2>&1 | grep -E "ANSICHT FERTIG|Error|Traceback" >>$LOG; done
python3 cad/baukasten/label_g5.py LFP,NMC >>$LOG 2>&1 || echo "FEHLER label" >>$LOG
cp cad/baukasten/bilder/g5_*.png bericht/bilder/
cd bericht; pdflatex -interaction=nonstopmode bericht.tex >/dev/null; pdflatex -interaction=nonstopmode bericht.tex >/dev/null; grep -E "Output written|^! " bericht.log >>../$LOG; cd ..
echo "NACH ENDE $(date +%T)" >>$LOG
