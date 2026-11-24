#!/bin/bash
# KI-generiert (Claude Sonnet, 2026-11-24), Entwurf. E3b: alle Laeufe nacheinander (fertige werden uebersprungen), danach Auswertung.
cd "$(dirname "$0")"; source /home/cae/hermes/batterie/umgebung.sh
for v in LFP NMC; do for n in grob fein; do for f in a b c; do
  [ -e STOP ] && exit 75
  python3 lauf_einzel.py $f $v $n >> lauf_alle.log 2>&1
done; done; for f in a b c; do python3 lauf_einzel.py $f $v fein cu0 >> lauf_alle.log 2>&1; done; done
python3 e3b_auswerten.py >> lauf_alle.log 2>&1; touch lauf_alle.fertig
