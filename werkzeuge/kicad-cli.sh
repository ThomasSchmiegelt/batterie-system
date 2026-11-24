#!/bin/bash
# KI-generiert (Sonnet, 2026-11-24). KiCad 9 per Flatpak (Nutzer-Installation), Zugriff auf Projekt und e3-Ausgabe.
exec flatpak run --user --filesystem=/home/cae/hermes/batterie --filesystem=/home/cae/cae_projekte/batterie --command=kicad-cli org.kicad.KiCad "$@"
