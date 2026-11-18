#!/bin/bash
# KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. Auftrag K0-R. Start: setsid systemd-run --user --scope --unit=hermes-batterie-k0r bash alle_cycles.sh
cd /home/cae/hermes/batterie/sim/kuehlung/k0_zelle; source /home/cae/hermes/batterie/umgebung.sh
python3 -I bilder_cycles.py --samples 80 --samples-film 16 > alle_cycles.log 2>&1; echo FERTIG >> alle_cycles.log
