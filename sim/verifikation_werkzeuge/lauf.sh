#!/bin/bash
# KI-generiert (Claude Sonnet, 2026-11-23), Entwurf. QN1: rechnet alle Werkzeug-Testfaelle V1-V5 neu (spaeter Regressionstest). Aufruf: bash lauf.sh [V1 V2 V3 V4 V5 ...] (Standard: alle)
# Losgeloest und pausierbar starten: setsid systemd-run --user --scope --unit=hermes-batterie-qn1 bash lauf.sh > lauf.log 2>&1 &   (Pause: ~/bin/rechnung pause)
# Dauer ca. 5-10 min (V1 20 s, V2 mehrere min nach GPU-Freigabe, V3 1 min, V4 5 s, V5 1 s). V2: nur nach rechnen/gpu_warten.sh. Stopp: rechnen/STOP (V2 prueft es).
# Jeder Fall dauert laut ERWARTUNG < 10 min, V2 meldet sonst Abbruch (kein stilles Verkleinern). Exitcode: 0 alle bestanden, 1 mindestens ein Fall verfehlt, 2 Fehler beim Rechnen.
cd /home/cae/hermes/batterie/sim/verifikation_werkzeuge && source /home/cae/hermes/batterie/umgebung.sh >/dev/null 2>&1
F=${@:-V1 V2 V3 V4 V5}; RC=0
for f in $F; do
  case $f in
    V1) S=v1_elmer.py ;; V2) S=v2_fluidx3d.py ;; V3) S=v3_radioss.py ;; V4) S=v4_pybamm.py ;; V5) S=v5_verteiler.py ;; *) echo "unbekannter Fall $f"; exit 2 ;;
  esac
  [ -e /home/cae/hermes/batterie/rechnen/STOP ] && { echo "STOP vor $f"; exit 75; }
  if [ "$f" = V2 ]; then bash /home/cae/hermes/batterie/rechnen/gpu_warten.sh || { echo "gpu_warten abgebrochen"; exit 75; }; fi
  echo "$(date +%T) $f Start"; python3 $S || { echo "$f Fehler beim Rechnen"; RC=2; }
done
python3 auswerten.py && python3 -c "
import json,sys; d=json.load(open('ergebnis.json')); sys.exit(0 if d['alle_bestanden'] else 1)" || [ $RC -ne 0 ] || RC=1
echo "$(date +%T) fertig, Exitcode $RC"; exit $RC
