#!/bin/bash
# Kette (von neustart.sh erzeugt): Argumente <Fall>:<Zustand> ...
D="$(cd "$(dirname "$0")" && pwd)"; source "$D/../../../umgebung.sh"
for pz in "$@"; do
  f=${pz%:*}; z=${pz#*:}; v=${f%_*}; w=${f#*_w}; big=/home/cae/cae_projekte/batterie/x2_lauf/$f
  if [ ! -f "$D/lauf_oc/$f/X2_0001.rad" ]; then
    mkdir -p "$big"; [ -e "$D/lauf_oc/$f" ] || ln -s "$big" "$D/lauf_oc/$f"
    (cd "$D" && python3 x2.py $v $w > /dev/null) || { echo "$(date '+%F %T') Deck $f fehlgeschlagen" >> "$D/neustart.log"; continue; }
  fi
  echo "$(date '+%F %T') Start $f ($z)" >> "$D/neustart.log"
  NT=4 systemd-run --user --scope --unit="hermes-batterie-x2-$f" "$D/lauf_oc.sh" "$f"
  echo "$(date '+%F %T') Ende $f (fertig.txt: $([ -f "$D/lauf_oc/$f/fertig.txt" ] && echo ja || echo nein))" >> "$D/neustart.log"
done
