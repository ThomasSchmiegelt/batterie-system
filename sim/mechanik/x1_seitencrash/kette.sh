#!/bin/bash
# KI-generiert (Claude Sonnet, 2026-11-18). Aufruf: kette.sh <Lauf1> <Lauf2>: nacheinander, 4 Threads
cd "$(dirname "$0")"; for r in "$@"; do NT=4 ./lauf.sh $r; done
