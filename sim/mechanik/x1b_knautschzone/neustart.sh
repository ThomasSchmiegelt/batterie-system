#!/bin/bash
# KI-generiert (Claude Sonnet, 2026-11-18), Entwurf. Neustart X1b/X2 (Knautschzone explizit, OpenCourant), Regel AGENTS.md Rechnen/Wiederaufsetzpunkt. Die alte CalculiX-Fassung steht in neustart_ccx.sh.
# Aufruf:   bash neustart.sh [--zeigen] [Fall ...]      Faelle: LFP_w20 LFP_w15 LFP_w30 NMC_w20 (Standard: alle vier)
#   --zeigen  nur auflisten, was getan wuerde (Trockenlauf)
# Verhalten: Ein Lauf besteht aus Abschnitten (Standard 10). Jeder Abschnitt endet normal und schreibt eine Restart-Datei X2_<k>_0001.rst.
#   fertige Faelle (fertig.txt) werden uebersprungen, angefangene setzen beim ersten fehlenden Abschnitt fort (verloren geht hoechstens ein Abschnitt, ca. 1 bis 2 min),
#   fehlende werden neu erzeugt (x2.py), alles nur CPU, losgeloest (setsid nohup), 2 Ketten mit je 4 Threads, jeder Lauf im Scope hermes-batterie-x2-<fall> (pausieren: ~/bin/rechnung pause|weiter).
#   Am Ende auswerten_oc.py (Bilder, ergebnis_oc.json). Restart und Ergebnisse liegen unter /home/cae/cae_projekte/batterie/x2_lauf/<fall> (Symlink lauf_oc/<fall>).
# Abbruch:  pkill -f neustart_haupt; pkill -f lauf_oc.sh; pkill -INT -f engine_linux64_gf   (danach bash neustart.sh)
# Log:      neustart.log. Bricht ab, wenn schon ein Lauf (Starter/Engine) fuer X2 laeuft.
cd "$(dirname "$0")"; D=$PWD; ZEIGEN=0; FAELLE=""
for a in "$@"; do case "$a" in --zeigen) ZEIGEN=1;; *) FAELLE="$FAELLE $a";; esac; done
[ -z "$FAELLE" ] && FAELLE="LFP_w20 LFP_w15 LFP_w30 NMC_w20"
for p in $(pgrep -f "engine_linux64_gf|starter_linux64_gf"); do
  case "$(readlink /proc/$p/cwd 2>/dev/null)" in */x2_lauf/*|"$D"/lauf_oc/*) if [ $ZEIGEN = 1 ]; then echo "Hinweis: X2-Lauf aktiv (PID $p); ein echter Start wuerde abbrechen."; else echo "Abbruch: es laeuft schon ein X2-Lauf (PID $p). Erst beenden oder abwarten."; exit 1; fi;; esac
done
source "$D/../../../umgebung.sh"
log() { echo "$(date '+%F %T') $*" | tee -a "$D/neustart.log"; }
zustand() {
  local dir="$D/lauf_oc/$1"
  [ -f "$dir/X2_0001.rad" ] || { echo neu; return; }
  [ -f "$dir/fertig.txt" ] && { echo fertig; return; }
  ls "$dir"/X2_0*_0001.rst > /dev/null 2>&1 && { echo fortsetzen; return; }
  echo neu
}
PLAN=""; for f in $FAELLE; do z=$(zustand $f); n=$(ls "$D/lauf_oc/$f"/X2_0[0-9][0-9][0-9]_0001.rst 2>/dev/null | grep -vc "X2_0000_"); log "Fall $f: $z (fertige Abschnitte: $n)"; case $z in neu|fortsetzen) PLAN="$PLAN $f:$z";; esac; done
[ $ZEIGEN = 1 ] && { log "Trockenlauf: wuerde rechnen:${PLAN:- nichts}; danach auswerten_oc.py"; exit 0; }
[ -z "$PLAN" ] && { log "nichts zu tun, nur Auswertung"; python3 "$D/auswerten_oc.py" > "$D/auswerten_oc.log" 2>&1; exit 0; }
cat > "$D/neustart_kette.sh" <<'K'
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
K
chmod +x "$D/neustart_kette.sh"
A=""; B=""; i=0; for pz in $PLAN; do if [ $((i%2)) = 0 ]; then A="$A $pz"; else B="$B $pz"; fi; i=$((i+1)); done
cat > "$D/neustart_haupt.sh" <<H
#!/bin/bash
cd "$D"
[ -n "$A" ] && ./neustart_kette.sh $A &
[ -n "$B" ] && ./neustart_kette.sh $B &
wait
source "$D/../../../umgebung.sh"; python3 "$D/auswerten_oc.py" > "$D/auswerten_oc.log" 2>&1
echo "\$(date '+%F %T') alles fertig, Auswertung: auswerten_oc.log" >> "$D/neustart.log"
H
chmod +x "$D/neustart_haupt.sh"
setsid nohup "$D/neustart_haupt.sh" < /dev/null > /dev/null 2>&1 &
log "gestartet (Kette A:${A:- -} B:${B:- -}). Fortschritt: ls lauf_oc/<fall>/X2_*_0001.rst, tail lauf_oc/<fall>/engine_*.log; Log neustart.log"
