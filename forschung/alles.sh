#!/bin/bash
# alles.sh -- Reihenfolge: Wissen (W01-W15), Werkzeuge (T01-T07), Patente (P01-P10). KI-generiert (Claude Opus, 2026-11-12).
cd "$(dirname "$0")"; for a in wissen werkzeuge patente; do bash lauf.sh $a; [ -e STOP ] && break; done
echo "$(date '+%F %T') ALLES FERTIG" >> verlauf.log
