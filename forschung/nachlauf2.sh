#!/bin/bash
# nachlauf2.sh -- Patente P02-P10 (Spaltenfehler B-BAT-003) und T02 (schwach, B-BAT-002) neu, nach nachlauf.sh. KI-generiert (Claude Opus, 2026-11-12).
cd "$(dirname "$0")"; while pgrep -f "bash nachlauf.sh" >/dev/null; do sleep 30; done
[ -e STOP ] || bash lauf.sh patente; [ -e STOP ] || bash lauf.sh werkzeuge T02
echo "$(date '+%F %T') NACHLAUF2 FERTIG" >> verlauf.log
