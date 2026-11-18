#!/bin/bash
# KI-generiert (Claude Opus, 2026-11-18). Arbeitet Recherchethemen nacheinander ab, auch wenn Claude beendet ist.
# Start: setsid nohup bash forschung/warteschlange.sh W31 W32 W33 > forschung/warteschlange.log 2>&1 &
# Abbruch: touch forschung/STOP. GPU nie doppelt: wartet auf laufende lauf.sh.
cd "$(dirname "$0")/.."
for nr in "$@"; do
  while pgrep -f "^bash forschung/lauf.sh" >/dev/null; do sleep 60; done
  [ -f forschung/STOP ] && { echo "$(date) STOP"; exit 0; }
  echo "$(date) start $nr"; bash forschung/lauf.sh wissen "$nr"; echo "$(date) ende $nr: $(tail -1 forschung/ergebnis/$nr.pruefung.txt 2>/dev/null)"
done
echo "$(date) Warteschlange fertig"
