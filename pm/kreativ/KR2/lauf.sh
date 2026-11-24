#!/bin/bash
# KR2: Kopfstand, Paarurteile, Rang. Fortsetzen: dasselbe Skript (fertige Urteile werden übersprungen). KI-generiert (Claude Sonnet, 2026-11-24).
cd /home/cae/hermes/batterie && source umgebung.sh && cd pm/kreativ
[ -f KR2/kopfstand.json ] || python3 kreativ.py kopfstand KR2
python3 kreativ.py paare KR2 && python3 kreativ.py rang KR2
