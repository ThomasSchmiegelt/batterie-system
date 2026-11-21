#!/bin/bash
# KI-generiert (Claude Sonnet, 2026-11-20), Entwurf. Aufruf: lauf_x3.sh <V> <Lastfall> : Deck (Produktionsfeinheit) nur erzeugen, wenn noch keins da ist (Wiederaufsetzen!), dann lauf.sh.
cd "$(dirname "$0")"; source ../../../umgebung.sh
F=${1}_${2}
[ -f lauf/$F/X3_0000.rad ] || X3_HN=${X3_HN:-12} X3_HF=${X3_HF:-40} X3_HY=${X3_HY:-20} X3_NZ=${X3_NZ:-6} X3_NSEG=${X3_NSEG:-10} X3_TSTOP=${X3_TSTOP:-50} python3 x3.py $1 $2 || exit 1
bash lauf.sh $F
