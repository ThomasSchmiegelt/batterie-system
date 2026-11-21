#!/bin/bash
# KI-generiert (Claude Sonnet, 2026-11-20), Entwurf. Aufruf: auswerten.sh <Fall z.B. LFP_a> : nur wenn lauf/<Fall>/fertig.txt existiert; Zahlen, Bilder, Film
cd "$(dirname "$0")"; source ../../../umgebung.sh
[ -f lauf/$1/fertig.txt ] || { echo "Lauf $1 nicht fertig"; exit 1; }
python3 auswerten.py $1 film
