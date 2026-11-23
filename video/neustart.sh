#!/bin/bash
# KI-generiert (Claude Sonnet, 2026-11-23), Entwurf. Setzt das Video fort: fertige Einzelbilder bleiben, fehlende werden gerendert, am Ende ffmpeg. Losgelöst starten: setsid bash video/neustart.sh >> /home/cae/cae_projekte/batterie_video/neustart.log 2>&1 &
cd /home/cae/hermes/batterie && exec bash video/erzeuge_video.sh alles
