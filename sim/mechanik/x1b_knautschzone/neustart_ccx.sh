#!/bin/bash
# KI-generiert (Claude Sonnet, 2026-11-18), Entwurf. Neustart X1b (Knautschzone, CalculiX), Auftrag X1b-R, Regel AGENTS.md Rechnen/Wiederaufsetzpunkt.
# Aufruf:   bash neustart.sh [--zeigen] [--wiederholen]
#   --zeigen       nur auflisten, was getan wuerde (Trockenlauf)
#   --wiederholen  auch durch Divergenz abgebrochene Laeufe nochmal rechnen (sonst uebersprungen und gemeldet)
# Verhalten: fertige Laeufe ("Job finished") werden uebersprungen; angefangene mit Restart-Datei (.rout) am letzten fertigen Schritt fortgesetzt (x1rN);
#   angefangene ohne .rout (alte Einschritt-Decks) und fehlende neu erzeugt und gerechnet (alter Ordner -> lauf/<fall>.alt_<Zeit>).
#   2 Ketten mit je 4 Threads, jeder Lauf im Scope hermes-batterie-x1b-<fall> (pausieren: ~/bin/rechnung pause|weiter), losgeloest (setsid nohup). Am Ende auswerten.py.
# Abbruch:  laufende Rechnung stoppen: pkill -f neustart_kette; pkill -x ccx   (danach bash neustart.sh setzt fort)
# Log:      neustart.log in diesem Ordner. Bricht ab, wenn schon ein ccx fuer X1b laeuft.
cd "$(dirname "$0")"; D=$PWD; ZEIGEN=0; WIEDER=0
for a in "$@"; do [ "$a" = --zeigen ] && ZEIGEN=1; [ "$a" = --wiederholen ] && WIEDER=1; done
FAELLE="LFP_15 LFP_20 LFP_30 NMC_15 NMC_20 NMC_30"
for p in $(pgrep -x ccx); do
  case "$(readlink /proc/$p/cwd 2>/dev/null)" in "$D"/lauf/*) if [ $ZEIGEN = 1 ]; then echo "Hinweis: ccx fuer X1b laeuft (PID $p); ein echter Start wuerde abbrechen."; else echo "Abbruch: es laeuft schon ein ccx fuer X1b (PID $p). Erst beenden oder abwarten."; exit 1; fi;; esac
done
source "$D/../../../umgebung.sh"
log() { echo "$(date '+%F %T') $*" | tee -a "$D/neustart.log"; }
zustand() {   # $1 = Fall -> fertig | abgebrochen | fortsetzen | neu
  local v=${1%_*} w=${1#*_} dir="$D/lauf/${1%_*}_LF1_w${1#*_}"
  [ -f "$dir/x1.inp" ] || { echo neu; return; }
  local last=x1 lg=ccx.log; for f in $(ls "$dir"/x1r*.inp 2>/dev/null | sort -V); do last=$(basename $f .inp); lg=$last.log; done
  if grep -q "Job finished" "$dir/$lg" 2>/dev/null; then
    [ "$last" = x1 ] && { echo fertig; return; }
    python3 "$D/fortsetzen.py" "$dir" --info > /dev/null 2>&1 && { echo fortsetzen; return; }; echo fertig; return
  fi
  if { grep -q "\*ERROR" "$dir/$lg" 2>/dev/null || grep -q "^fertig" "$dir/$lg" 2>/dev/null; } && [ $WIEDER = 0 ]; then echo abgebrochen; return; fi
  if python3 "$D/fortsetzen.py" "$dir" --info > /dev/null 2>&1; then echo fortsetzen; else echo neu; fi
}
PLAN=""; for f in $FAELLE; do z=$(zustand $f); log "Fall $f: $z"; case $z in neu|fortsetzen) PLAN="$PLAN $f:$z";; esac; done
[ $ZEIGEN = 1 ] && { log "Trockenlauf: wuerde rechnen:${PLAN:- nichts}; danach auswerten.py"; exit 0; }
[ -z "$PLAN" ] && { log "nichts zu tun, nur Auswertung"; python3 "$D/auswerten.py" > "$D/auswerten.log" 2>&1; exit 0; }
cat > "$D/neustart_kette.sh" <<'K'
#!/bin/bash
# Kette (von neustart.sh erzeugt): Argumente <Fall>:<Zustand> ...
D="$(cd "$(dirname "$0")" && pwd)"; source "$D/../../../umgebung.sh"
for pz in "$@"; do
  f=${pz%:*}; z=${pz#*:}; v=${f%_*}; w=${f#*_}; dir="$D/lauf/${v}_LF1_w${w}"; unit="hermes-batterie-x1b-${v}_w${w}"
  if [ "$z" = neu ]; then
    [ -d "$dir" ] && mv "$dir" "$dir.alt_$(date +%H%M%S)"
    (cd "$D" && SELF=0 python3 x1b.py $v LF1 $w 12 4 > /dev/null) || { echo "$(date '+%F %T') Deck $f fehlgeschlagen" >> "$D/neustart.log"; continue; }
    job=x1
  else
    python3 "$D/fortsetzen.py" "$dir" >> "$D/neustart.log" 2>&1 || continue
    job=$(ls "$dir"/x1r*.inp | sort -V | tail -1 | xargs basename | sed 's/.inp//')
  fi
  echo "$(date '+%F %T') Start $f ($job)" >> "$D/neustart.log"
  NT=4 systemd-run --user --scope --unit="$unit" "$D/lauf_job.sh" "${v}_LF1_w${w}" "$job"
  echo "$(date '+%F %T') Ende $f ($job)" >> "$D/neustart.log"
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
source "$D/../../../umgebung.sh"; python3 "$D/auswerten.py" > "$D/auswerten.log" 2>&1
echo "\$(date '+%F %T') alles fertig, Auswertung: auswerten.log" >> "$D/neustart.log"
H
chmod +x "$D/neustart_haupt.sh"
setsid nohup "$D/neustart_haupt.sh" < /dev/null > /dev/null 2>&1 &
log "gestartet (Ketten: A:${A:- -} B:${B:- -}). Fortschritt: tail lauf/*/x1.sta; Log neustart.log"
