#!/bin/bash
cd /home/cae/hermes/batterie
P=$(cat rechnen/lauf.pid 2>/dev/null); { [ -n "$P" ] && kill -0 "$P" 2>/dev/null && echo "LÄUFT (PID $P)"; } || echo "steht"
[ -f rechnen/STOP ] && echo "STOP gesetzt"
grep -v '^\s*#' rechnen/schritte.txt | grep '|' | while IFS='|' read -r ID G C; do ID=$(echo $ID); [ -f rechnen/fertig/$ID ] && echo "  fertig  $ID" || echo "  offen   $ID"; done
tail -3 rechnen/verlauf.log 2>/dev/null
