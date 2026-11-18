#!/bin/bash
# nachlauf3.sh -- Google Patents sperrte mit HTTP 503 (Bot-Schutz, B-BAT-003). Einmal nach 2 h eine Probeanfrage;
# nur wenn sie Treffer liefert, P02-P10 rechnen. Kein Umgehen der Sperre. KI-generiert (Claude Opus, 2026-11-12).
cd "$(dirname "$0")"; sleep 7200; [ -e STOP ] && exit 0
if python3 ~/.hermes/skills/cae/patent-recherche/patente.py suche "battery pack liquid cooling plate" --n 1 --ab 2015 2>&1 | grep -q "patents.google.com/patent"; then
  echo "$(date '+%F %T') Patente wieder erreichbar, P02-P10 starten" >> verlauf.log; bash lauf.sh patente
else
  echo "$(date '+%F %T') Patente weiter gesperrt (503); nicht erneut versucht" >> verlauf.log
fi
