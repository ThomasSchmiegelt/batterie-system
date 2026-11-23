#!/bin/bash
# KI-generiert (Claude Opus, 2026-11-20, ergänzt Claude Sonnet 2026-11-23: Tor pm/tor.py, Auftrag WORKFLOW_V Punkt 7, docs/17). Arbeitet rechnen/schritte.txt der Reihe nach ab, überspringt fertige, hört bei rechnen/STOP auf.
cd /home/cae/hermes/batterie; source umgebung.sh >/dev/null 2>&1; export RECHNEN_STOP=$PWD/rechnen/STOP
L=rechnen/verlauf.log; SKIP=" "; echo "=== START $(date '+%F %T')" >>$L
while true; do   # schritte.txt bei jedem Durchgang neu lesen (angehängte Schritte werden mitgenommen), ersten offenen Schritt nehmen
  ZEILE=""; while IFS= read -r z; do I=$(echo ${z%%|*}); [ -f rechnen/fertig/$I ] || [[ "$SKIP" == *" $I "* ]] || { ZEILE="$z"; break; }; done < <(grep -v '^\s*#' rechnen/schritte.txt | grep '|')
  [ -z "$ZEILE" ] && break
  IFS="|" read -r ID GPU CMD TORSP <<< "$ZEILE"
  ID=$(echo $ID); [ -f rechnen/fertig/$ID ] && continue
  # Tor T2 (docs/17): Schritt mit Rechenordner (erster sim/…-Pfad im Befehl) startet nur, wenn pm/tor.py 0 Fehler meldet; TOR=aus in Spalte 4 überspringt das Tor
  if [ "$(echo $TORSP)" != "TOR=aus" ]; then
    SD=$(echo "$CMD" | grep -o 'sim/[A-Za-z0-9_./-]*' | head -1); [ -n "$SD" ] && { [ -d "$SD" ] || SD=$(dirname "$SD"); }
    if [ -n "$SD" ] && [ -d "$SD" ]; then
      TORMELD=$(python3 pm/tor.py "$SD" 2>&1); if [ $? -ne 0 ]; then
        echo "--- $ID ÜBERSPRUNGEN: Tor zu für $SD $(date +%T)" >>$L; echo "$TORMELD" | sed 's/^/    /' >>$L
        { echo "$(date '+%F %T') $ID ($SD)"; echo "$TORMELD" | sed 's/^/    /'; } >>rechnen/TOR_FEHLT; SKIP="$SKIP$ID "; continue
      fi
    fi
  fi
  [ -f rechnen/STOP ] && { echo "--- angehalten vor $ID $(date +%T)" >>$L; break; }
  if [ "$(echo $GPU)" = ja ]; then bash rechnen/gpu_warten.sh || { echo "--- angehalten vor $ID (GPU-Warten, STOP) $(date +%T)" >>$L; break; }; fi   # GPU frei? sonst Pause (Vorgabe Autor 23.11.)
  echo "--- $ID start $(date '+%F %T'): $CMD" >>$L
  setsid bash -c "$CMD" >>rechnen/log_$ID.txt 2>&1 < /dev/null & K=$!; echo $K > rechnen/kind.pid; wait $K; RC=$?
  if [ -f rechnen/STOP ]; then echo "--- $ID angehalten (rc=$RC) $(date +%T)" >>$L; break; fi
  if [ $RC -eq 0 ]; then date '+%F %T' > rechnen/fertig/$ID; echo "--- $ID fertig $(date +%T)" >>$L
  else echo "--- $ID FEHLER rc=$RC $(date +%T) – Warteschlange hält (Log rechnen/log_$ID.txt)" >>$L; break; fi
done
echo "=== ENDE $(date '+%F %T')" >>$L; rm -f rechnen/lauf.pid rechnen/kind.pid
