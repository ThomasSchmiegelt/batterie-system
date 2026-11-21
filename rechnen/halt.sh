#!/bin/bash
# KI-generiert (Claude Opus, 2026-11-20). Hält die Warteschlange sauber an. Siehe LIESMICH.md.
cd /home/cae/hermes/batterie; touch rechnen/STOP; touch forschung/STOP 2>/dev/null
for c in $(find sim -name "*.ctl" -newer rechnen/schritte.txt 2>/dev/null); do grep -q "/STOP" "$c" || echo "/STOP" >> "$c"; done   # OpenCourant
echo "STOP gesetzt. Warte auf das Ende des laufenden Schritts …"
P=$(cat rechnen/lauf.pid 2>/dev/null)
for i in $(seq 1 180); do { [ -z "$P" ] || ! kill -0 "$P" 2>/dev/null; } && { echo "ANGEHALTEN – Rechner kann aus. Weiter mit: bash rechnen/start.sh"; exit 0; }; sleep 10; done
K=$(cat rechnen/kind.pid 2>/dev/null); echo "Schritt reagiert nach 30 min nicht; beende Prozessgruppe $K"; [ -n "$K" ] && kill -TERM -- -"$K" 2>/dev/null; sleep 20
echo "ANGEHALTEN (hart) – Rechner kann aus. Der abgebrochene Schritt wird beim Start neu gerechnet."
