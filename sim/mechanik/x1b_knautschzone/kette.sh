#!/bin/bash
# KI-generiert (Claude Sonnet, 2026-11-18), Entwurf. Aufruf: kette.sh "<V> <w>" ...  : Deck erzeugen und nacheinander rechnen (NT Threads, Standard 4). SELF=0 (kein Selbstkontakt).
cd "$(dirname "$0")"; source ../../../umgebung.sh
for p in "$@"; do set -- $p; SELF=0 python3 x1b.py $1 LF1 $2 12 4 > /dev/null && NT=${NT:-4} ./lauf.sh ${1}_LF1_w$2; done
