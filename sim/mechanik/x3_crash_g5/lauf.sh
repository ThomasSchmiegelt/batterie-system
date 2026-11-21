#!/bin/bash
# KI-generiert (Claude Sonnet, 2026-11-20), Entwurf. X3 OpenCourant-Lauf, wiederaufsetzbar. Aufruf: lauf.sh <Fall z.B. LFP_a> (NT Threads, Standard 6; nur CPU)
# Deck erzeugen: x3.py (siehe dort). Abschnitte k=1..N (X3_000k.rad); fertige werden uebersprungen. $RECHNEN_STOP: vor jedem Abschnitt geprueft, waehrend des Abschnitts alle 10 s
# (dann /STOP in X3_000k.ctl, Engine schreibt Restart und endet; Neustart setzt von dort fort).
F=$1; D="$(cd "$(dirname "$0")" && pwd)"; cd "$D/lauf/$F" || exit 1
source /home/cae/cae_projekte/werkzeuge/opencourant/umgebung.sh; export OMP_NUM_THREADS=${NT:-6}; EX=$OPENCOURANT_PATH/exec
STOPF=${RECHNEN_STOP:-/home/cae/hermes/batterie/rechnen/STOP}
NS=$(ls X3_[0-9][0-9][0-9][0-9].rad | grep -v X3_0000 | wc -l)
if [ ! -f X3_0000_0001.rst ]; then
  nice -n 10 $EX/starter_linux64_gf -i X3_0000.rad -np 1 > starter.log 2>&1
  grep -q "NORMAL TERMINATION\|TERMINATION WITH WARNING" starter.log || { echo "Starter fehlgeschlagen"; exit 1; }
fi
for k in $(seq 1 $NS); do
  K=$(printf %04d $k)
  [ -f X3_${K}_0001.rst ] && [ ! -f X3_${K}.unfertig ] && continue
  [ -f "$STOPF" ] && { echo "STOP vor Abschnitt $k"; exit 0; }
  touch X3_$K.unfertig; rm -f X3_$K.ctl
  nice -n 10 $EX/engine_linux64_gf -i X3_$K.rad > engine_$k.log 2>&1 &
  P=$!
  while kill -0 $P 2>/dev/null; do
    if [ -f "$STOPF" ] && [ ! -f X3_$K.ctl ]; then echo "/STOP" > X3_$K.ctl; fi
    sleep 5
  done
  wait $P
  grep -q "NORMAL TERMINATION" engine_$k.log || { echo "Abschnitt $k nicht normal beendet" >&2; exit 1; }
  rm -f X3_$K.unfertig
  [ -f "$STOPF" ] && grep -qi "STOP" engine_$k.log && { echo "angehalten in Abschnitt $k"; exit 0; }
done
echo "fertig $(date +%T)" > fertig.txt
