#!/bin/bash
cd "$(dirname "$0")"
while pgrep -x ccx > /dev/null; do sleep 20; done
NT=4 ./kette.sh "LFP 20" "LFP 30" "NMC 30" &
NT=4 ./kette.sh "NMC 15" "NMC 20" &
wait
source ../../../umgebung.sh; python3 auswerten.py > auswerten.log 2>&1
