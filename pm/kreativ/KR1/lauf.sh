#!/bin/bash
# KR1 Lauf 3: nur Reifegrad und Fehlermöglichkeiten über K2, K4, K5, K6 neu urteilen (Rest aus lauf2/paare.json), dann Rang. Fortsetzen: dasselbe Skript. KI-generiert (Claude Sonnet, 2026-11-24).
cd /home/cae/hermes/batterie && source umgebung.sh && cd pm/kreativ
python3 kreativ.py paare KR1 && python3 kreativ.py rang KR1
