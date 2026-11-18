#!/bin/bash
# KI-generiert (Claude Sonnet, 2026-11-18), Entwurf. Aufruf: lauf.sh <Ordner unter lauf/>  (ccx, nice, 8 Threads, nur CPU)
cd "$(dirname "$0")/lauf/$1" || exit 1
export OMP_NUM_THREADS=${NT:-4} CCX_NPROC_EQUATION_SOLVER=${NT:-4}
nice -n 10 ~/.local/bin/ccx x1 > ccx.log 2>&1
echo "fertig $(date +%T)" >> ccx.log
