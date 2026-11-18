#!/bin/bash
# nachlauf.sh -- W16/W17 kamen nach Start von alles.sh dazu (laufender Block liest die Liste nicht neu).
# Wartet auf „ALLES FERTIG“, dann lauf.sh wissen (fertige Themen werden übersprungen). KI-generiert (Claude Opus, 2026-11-12).
cd "$(dirname "$0")"; until grep -q "ALLES FERTIG" verlauf.log; do sleep 60; done; [ -e STOP ] || bash lauf.sh wissen
