#!/bin/bash
# KI-generiert (Claude Opus, 2026-11-21). Sammelt die Ergebnisbilder der Rechnungen für den Bericht (bericht/bilder/, Präfix je Rechnung) und erneuert das Bildverzeichnis docs/16.
cd /home/cae/hermes/batterie
for d in sim/kuehlung/k3_gesamt sim/kuehlung/k3_gesamt/elmer sim/mechanik/x3_crash_g5; do
  p=$(basename $d); [ "$p" = elmer ] && p=k4
  find $d -maxdepth 1 -name "*.png" ! -name "*probe*" | while read f; do cp -u "$f" "bericht/bilder/${p}_$(basename $f)"; done
done
python3 pm/plan/bilder.py >/dev/null 2>&1 || echo "Hinweis: pm/plan/bilder.py fehlgeschlagen"
ls bericht/bilder | grep -c -E "^(k3_gesamt|k4|x3_crash_g5)_"
