#!/bin/bash
# KI-generiert (Claude Sonnet, 2026-11-21), Entwurf. Aufruf: bash sim/kuehlung/k3_gesamt/lauf.sh bahn|umlenk <Re> | auswerten | film | k4 <Fall> <Variante>
# Fall: LFP_P0 | NMC_P4 | LFP_DAUER | NMC_DAUER; Variante: V0 (wie bisher) | V1 gegensinnig | V2 Durchfluss x2 | V3 = V1+V2.
# Jeder Schritt dauert < 30 min und startet bei STOP/Neustart von vorn (kein Wiederaufsetzpunkt noetig). Pruefung: $RECHNEN_STOP (FluidX3D je Abschnitt, Elmer vor dem Start).
cd /home/cae/hermes/batterie/sim/kuehlung/k3_gesamt && source /home/cae/hermes/batterie/umgebung.sh >/dev/null 2>&1
[ -n "$RECHNEN_STOP" ] && [ -e "$RECHNEN_STOP" ] && { echo STOP; exit 75; }
case "$1" in
 bahn|umlenk) curl -s localhost:11434/api/ps | grep -q '"name"' && { echo "ollama hat ein Modell geladen, GPU belegt"; exit 76; }; python3 k3_fluidx3d.py $1 --re $2 ;;
 auswerten) python3 k3_fluidx3d.py auswerten && python3 k3_bilder.py 200 ;;
 film) python3 k3_film.py rechnen && python3 k3_film.py bild ;;
 k4) A="--fall $2 --var $3"; python3 k4_elmer.py netz $A && python3 k4_elmer.py rechnen $A && python3 k4_elmer.py auswerten $A && python3 k4_bilder.py $A ;;
esac
