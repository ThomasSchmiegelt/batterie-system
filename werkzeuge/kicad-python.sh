#!/bin/bash
# KI-generiert (Sonnet, 2026-11-24). Python mit pcbnew im KiCad-Flatpak.
exec flatpak run --user --filesystem=/home/cae/hermes/batterie --filesystem=/home/cae/cae_projekte/batterie --command=python3 org.kicad.KiCad "$@"
