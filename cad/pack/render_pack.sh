#!/usr/bin/env bash
# KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. Auftrag G4. Komplette Kette neu, ohne Codeänderung (nach Freigabe der Akten: status entschieden).
# Aufruf: bash cad/pack/render_pack.sh [LFP NMC]   Dauer: LFP ca. 5 min, NMC ca. 25 min (CPU). Ein Lauf nur einmal gleichzeitig.
set -e; cd "$(dirname "$0")/../.."; source umgebung.sh
V="${@:-LFP NMC}"
python3 cad/pack/entwurf_parameter.py                      # Maße aus Akten (entschieden + vorgeschlagen)
for v in $V; do
  PACK_VARIANTE=$v $FREECAD_APPIMAGE freecadcmd cad/pack/pack.py   # Modell, Kollision, Massen, Netze
  PACK_VARIANTE=$v RENDER_SAMPLES=${RENDER_SAMPLES:-24} $BLENDER -b -P cad/pack/render_pack.py
  python3 cad/pack/label_pack.py $v
done
python3 cad/pack/pack_massen.py
rm -f cad/pack/entwurf/roh_*.png cad/pack/entwurf/roh_*.json   # Zwischenbilder (sonst als Ergebnisbild ohne Lesehilfe gelistet)
