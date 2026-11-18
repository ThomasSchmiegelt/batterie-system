#!/bin/bash
# KI-generiert (Claude Sonnet, 2026-11-18), Entwurf. OpenCourant-Lauf eines Falls mit Wiederaufsetzpunkten. Aufruf: lauf_oc.sh <Fall z.B. LFP_w20>   (NT Threads, Standard 4; nur CPU)
# Ablauf: Starter (falls X2_0000_0001.rst fehlt), dann Abschnitte k = 1..N (Decks X2_000k.rad, /RUN/X2/k, siehe x2.py). Jeder Abschnitt endet normal und schreibt X2_000k_0001.rst;
# fertige Abschnitte werden uebersprungen, ein unterbrochener beginnt von vorn (Verlust hoechstens ein Abschnitt). Logs: starter.log, engine_<k>.log.
F=$1; D="$(cd "$(dirname "$0")" && pwd)"; cd "$D/lauf_oc/$F" || exit 1
source /home/cae/cae_projekte/werkzeuge/opencourant/umgebung.sh; export OMP_NUM_THREADS=${NT:-4}; EX=$OPENCOURANT_PATH/exec
NS=$(ls X2_[0-9][0-9][0-9][0-9].rad | grep -v X2_0000 | wc -l)
if [ ! -f X2_0000_0001.rst ]; then
  nice -n 10 $EX/starter_linux64_gf -i X2_0000.rad -np 1 > starter.log 2>&1
  grep -q "NORMAL TERMINATION\\|TERMINATION WITH WARNING" starter.log || { echo "Starter fehlgeschlagen"; exit 1; }
fi
for k in $(seq 1 $NS); do
  K=$(printf %04d $k)
  [ -f X2_${K}_0001.rst ] && continue
  nice -n 10 $EX/engine_linux64_gf -i X2_$K.rad > engine_$k.log 2>&1
  grep -q "NORMAL TERMINATION" engine_$k.log || { echo "Abschnitt $k nicht normal beendet" >&2; exit 1; }
done
echo "fertig $(date +%T)" > fertig.txt
