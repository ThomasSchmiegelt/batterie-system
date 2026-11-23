#!/bin/bash
# KI-generiert (Claude Sonnet, 2026-11-20), Entwurf. X3 OpenCourant-Lauf, wiederaufsetzbar. Aufruf: lauf.sh <Fall z.B. LFP_a> (NT Threads, Standard 6; nur CPU)
# Deck erzeugen: x3.py (siehe dort). Abschnitte k=1..N (X3_000k.rad); fertige werden uebersprungen. $RECHNEN_STOP: vor jedem Abschnitt geprueft, waehrend des Abschnitts alle 10 s
# (dann /STOP in X3_000k.ctl, Engine schreibt Restart und endet; Neustart setzt von dort fort).
# Nachtrag 6 (Opus 2026-11-23, Sonnet): Live-Pruefung alle 60 s (waechter_pruef.py live): dt < dt0/10 oder |ERROR| > 10 % (Fall a; Fall b nur dt) -> Engine per PID beenden, Grund in FEHLER_waechter.txt und rechnen/verlauf.log.
# Nachtrag 4 (Opus 2026-11-23, Sonnet): Waechter. Abschnitt > $MAXMIN min (Standard 45; normal 19-22 min) -> Engine per PID beenden (TERM, nach 20 s KILL), FEHLER. Abschnitt ohne X3_000k_0001.rst nach Ende -> FEHLER sofort. Nie pkill -f.
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
  P=$!; T0=$SECONDS; LC=$SECONDS; MAXS=$(( ${MAXMIN:-45} * 60 ))
  while kill -0 $P 2>/dev/null; do
    if [ -f "$STOPF" ] && [ ! -f X3_$K.ctl ]; then echo "/STOP" > X3_$K.ctl; fi
    if [ $((SECONDS - T0)) -gt $MAXS ]; then
      echo "FEHLER: Abschnitt $k laeuft laenger als ${MAXMIN:-45} min (vermutlich Zeitschrittkollaps); beende PID $P" >&2
      kill -TERM $P 2>/dev/null; sleep 20; kill -0 $P 2>/dev/null && kill -KILL $P 2>/dev/null
      wait $P 2>/dev/null; echo "FEHLER Waechter Abschnitt $k $(date +%T)" > FEHLER_waechter.txt; exit 1
    fi
    if [ $((SECONDS - LC)) -ge 60 ]; then
      LC=$SECONDS
      G=$(python3 "$D/waechter_pruef.py" live X3_$K.out . 2>/dev/null); RC=$?
      if [ $RC -eq 1 ]; then
        echo "FEHLER: Waechter Abschnitt $k: $G; beende PID $P" >&2
        kill -TERM $P 2>/dev/null; sleep 20; kill -0 $P 2>/dev/null && kill -KILL $P 2>/dev/null
        wait $P 2>/dev/null; echo "FEHLER Waechter live Abschnitt $k $(date +%T): $G" > FEHLER_waechter.txt
        echo "$(date +%T) X3_$F Waechter live Abschnitt $k: $G" >> /home/cae/hermes/batterie/rechnen/verlauf.log; exit 1
      fi
    fi
    sleep 5
  done
  wait $P
  grep -q "NORMAL TERMINATION" engine_$k.log || { echo "Abschnitt $k nicht normal beendet" >&2; exit 1; }
  [ -f X3_${K}_0001.rst ] || { echo "FEHLER: Abschnitt $k ohne X3_${K}_0001.rst beendet" >&2; echo "FEHLER keine rst Abschnitt $k $(date +%T)" > FEHLER_waechter.txt; exit 1; }
  rm -f X3_$K.unfertig
  [ -f "$STOPF" ] && grep -qi "STOP" engine_$k.log && { echo "angehalten in Abschnitt $k"; exit 0; }
done
echo "fertig $(date +%T)" > fertig.txt
