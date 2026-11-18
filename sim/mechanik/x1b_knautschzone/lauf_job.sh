#!/bin/bash
# KI-generiert (Claude Sonnet, 2026-11-18), Entwurf. Aufruf: lauf_job.sh <Ordner unter lauf/> <Job x1|x1r1..>; Log: ccx.log (x1) bzw. <Job>.log. NT Threads (Standard 4), nice.
# Die Restart-Datei (<Job>.rout, einige GB) liegt wegen der vollen Systemplatte unter /home/cae/cae_projekte/batterie/x1b_restart/<Ordner>/ (Symlink im Laufordner).
cd "$(dirname "$0")/lauf/$1" || exit 1
export OMP_NUM_THREADS=${NT:-4} CCX_NPROC_EQUATION_SOLVER=${NT:-4}
RD=/home/cae/cae_projekte/batterie/x1b_restart/$1; mkdir -p "$RD"
[ -e "$2.rout" ] || [ -L "$2.rout" ] || ln -s "$RD/$2.rout" "$2.rout"
LOG=$2.log; [ "$2" = x1 ] && LOG=ccx.log
nice -n 10 ~/.local/bin/ccx $2 > $LOG 2>&1
echo "fertig $(date +%T)" >> $LOG
