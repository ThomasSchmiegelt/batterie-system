#!/bin/bash
# KI-generiert (Claude Sonnet, 2026-11-24), Entwurf. Neustart E3b ohne Claude: setzt die Laeufe fort (fertige = lauf/*/res.json werden uebersprungen), losgeloest und pausierbar (~/bin/rechnung).
cd "$(dirname "$0")"; rm -f STOP lauf_alle.fertig
systemd-run --user --scope --unit=hermes-batterie-e3b-$(date +%H%M%S) nice -n 15 setsid bash lauf_alle.sh </dev/null >/dev/null 2>&1 &
echo "gestartet; Log lauf_alle.log; fertig, wenn lauf_alle.fertig existiert"
