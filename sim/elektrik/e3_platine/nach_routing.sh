#!/bin/bash
# KI-generiert (Sonnet, 2026-11-24). SES importieren, DRC, Gerber, STEP, Render. Aufruf: bash nach_routing.sh LFP NMC
cd /home/cae/hermes/batterie/sim/elektrik/e3_platine; source ../../../umgebung.sh
O=/home/cae/cae_projekte/batterie/e3; K=/home/cae/hermes/batterie/werkzeuge/kicad-cli.sh
for v in "$@"; do
  true
  [ -f $O/cmu_${v}_ungeroutet.kicad_pcb ] || cp $O/cmu_$v.kicad_pcb $O/cmu_${v}_ungeroutet.kicad_pcb
  cp $O/route/cmu_${v}_geroutet.kicad_pcb $O/cmu_$v.kicad_pcb
  rm -rf $O/gerber_$v; mkdir $O/gerber_$v
  nice $K pcb export gerbers -o $O/gerber_$v/ $O/cmu_$v.kicad_pcb >/dev/null 2>&1; nice $K pcb export drill -o $O/gerber_$v/ $O/cmu_$v.kicad_pcb >/dev/null 2>&1
  nice $K pcb export step --subst-models --force -o $O/cmu_$v.step $O/cmu_$v.kicad_pcb 2>&1 | tail -1
  for s in top bottom; do nice $K pcb render --side $s --quality basic -w 2400 -h 1200 -o $O/cmu_${v}_$s.png $O/cmu_$v.kicad_pcb >/dev/null 2>&1; done
done
python3 drc_auswerten.py "$@"
