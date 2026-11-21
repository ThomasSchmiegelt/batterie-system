#!/bin/bash
# KI-generiert (Claude Opus, 2026-11-20). Startet die Warteschlange losgelöst (überlebt das Schließen des Terminals). Siehe LIESMICH.md.
cd /home/cae/hermes/batterie
if [ -f rechnen/lauf.pid ] && kill -0 "$(cat rechnen/lauf.pid)" 2>/dev/null; then echo "läuft schon (PID $(cat rechnen/lauf.pid))"; exit 0; fi
rm -f rechnen/STOP; setsid nohup bash rechnen/warteschlange.sh >/dev/null 2>&1 < /dev/null &
echo $! > rechnen/lauf.pid; echo "gestartet (PID $!). Log: rechnen/verlauf.log"
