#!/bin/bash
# KR1 Stufen 5 und 7 losgelöst; pausierbar (~/bin/rechnung pause|weiter). Fortsetzen: dasselbe Skript (fertige Urteile werden übersprungen). KI-generiert (Claude Sonnet, 2026-11-24).
cd /home/cae/hermes/batterie && source umgebung.sh && cd pm/kreativ
python3 kreativ.py kopfstand KR1 && python3 kreativ.py paare KR1 && python3 kreativ.py rang KR1
