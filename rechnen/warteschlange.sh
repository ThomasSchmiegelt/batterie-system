#!/bin/bash
# KI-generiert (Claude Opus, 2026-11-20). Arbeitet rechnen/schritte.txt der Reihe nach ab, überspringt fertige, hört bei rechnen/STOP auf.
cd /home/cae/hermes/batterie; source umgebung.sh >/dev/null 2>&1; export RECHNEN_STOP=$PWD/rechnen/STOP
L=rechnen/verlauf.log; echo "=== START $(date '+%F %T')" >>$L
while true; do   # schritte.txt bei jedem Durchgang neu lesen (angehängte Schritte werden mitgenommen), ersten offenen Schritt nehmen
  ZEILE=""; while IFS= read -r z; do I=$(echo "${z%%|*}"); [ -f rechnen/fertig/$I ] || { ZEILE="$z"; break; }; done < <(grep -v '^\s*#' rechnen/schritte.txt | grep '|')
  [ -z "$ZEILE" ] && break
  IFS="|" read -r ID GPU CMD <<< "$ZEILE"
  ID=$(echo $ID); [ -f rechnen/fertig/$ID ] && continue
  [ -f rechnen/STOP ] && { echo "--- angehalten vor $ID $(date +%T)" >>$L; break; }
  if [ "$(echo $GPU)" = ja ]; then while pgrep -x ollama >/dev/null && curl -s localhost:11434/api/ps | grep -q '"name"'; do sleep 30; done; fi
  echo "--- $ID start $(date '+%F %T'): $CMD" >>$L
  setsid bash -c "$CMD" >>rechnen/log_$ID.txt 2>&1 < /dev/null & K=$!; echo $K > rechnen/kind.pid; wait $K; RC=$?
  if [ -f rechnen/STOP ]; then echo "--- $ID angehalten (rc=$RC) $(date +%T)" >>$L; break; fi
  if [ $RC -eq 0 ]; then date '+%F %T' > rechnen/fertig/$ID; echo "--- $ID fertig $(date +%T)" >>$L
  else echo "--- $ID FEHLER rc=$RC $(date +%T) – Warteschlange hält (Log rechnen/log_$ID.txt)" >>$L; break; fi
done
echo "=== ENDE $(date '+%F %T')" >>$L; rm -f rechnen/lauf.pid rechnen/kind.pid
