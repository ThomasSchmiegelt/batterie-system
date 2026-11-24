#!/bin/bash
# KI-generiert (Claude Sonnet, 2026-11-24). Schaltplan erzeugen, prüfen (ERC, Netzliste), PDF und PNG je Blatt, Quelle ins Repo kopieren.
cd /home/cae/hermes/batterie/sim/elektrik/e3c_bms_platine; source ../../../umgebung.sh
python3 bms_schaltplan.py || exit 1
python3 bms_schaltplan_pruefung.py | cut -c1-420
K=/home/cae/hermes/batterie/werkzeuge/kicad-cli.sh
$K sch export pdf -o $PWD/schaltplan_bms.pdf /home/cae/cae_projekte/batterie/e3c/schaltplan/bms_schaltplan.kicad_sch >/dev/null 2>&1
rm -f schaltplan_bms_blatt*.png; pdftoppm -r 130 -png schaltplan_bms.pdf schaltplan_bms_blatt
rm -rf schaltplan_quelle; mkdir schaltplan_quelle; cp /home/cae/cae_projekte/batterie/e3c/schaltplan/*.kicad_sch /home/cae/cae_projekte/batterie/e3c/schaltplan/*.kicad_pro schaltplan_quelle/
ls schaltplan_bms_blatt*
