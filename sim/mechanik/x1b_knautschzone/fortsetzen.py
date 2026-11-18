#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-18), Entwurf. Auftrag X1b-R. Aufruf: fortsetzen.py <Lauf-Ordner> [--info]
Erzeugt aus dem zuletzt fertigen Schritt (x1.sta bzw. x1r<j>.sta, Gesamtzeit) das Fortsetzungsdeck x1r<j+1>.inp (*RESTART,READ) mit den restlichen Schritten
und verlinkt <letzter Job>.rout als x1r<j+1>.rin. --info: nur ausgeben (Job, fertige Schritte, naechster Job). Rueckgabe 0 = Fortsetzung moeglich, 1 = nein."""
import sys, re, json, os
from pathlib import Path
d = Path(sys.argv[1]); info = "--info" in sys.argv; NS = int(os.environ.get("X1_NSTEP", 10)); DT = 1.0 / NS
jobs = ["x1"] + sorted((p.stem for p in d.glob("x1r*.inp")), key=lambda x: int(x[3:]))
last = jobs[-1]
def fertig_zeit(job):
    f = d / f"{job}.sta"; t = 0.0
    if not f.exists(): return 0.0
    for ln in f.read_text().splitlines():
        p = ln.split()
        if len(p) >= 7 and p[0].isdigit() and 'U' not in p[2]: t = max(t, float(p[4]))
    return t
t = max(fertig_zeit(j) for j in jobs); n = int(t / DT + 1e-6)
if not (d / f"{last}.rout").exists() or n < 1 or n >= NS: print(f"{d.name}: keine Fortsetzung moeglich (letzter Job {last}, fertige Schritte {n} von {NS}, rout {(d / f'{last}.rout').exists()})"); sys.exit(1)
new = f"x1r{len(jobs)}"
print(f"{d.name}: {n} von {NS} Schritten fertig (t={t:.4f}), Fortsetzung {new} aus {last}.rout")
if info: sys.exit(0)
txt = (d / "x1.inp").read_text(); head, *steps = re.split(r"(?m)^(?=\*STEP)", txt)
blocks = steps[n:]; blocks[0] = re.sub(r"(?m)^(\*STEP[^\n]*\n)", r"\1*RESTART, WRITE, FREQUENCY=1, OVERLAY\n", blocks[0], count=1) if "*RESTART" not in blocks[0] else blocks[0]
(d / f"{new}.inp").write_text(f"*RESTART, READ, STEP={n}\n" + "".join(blocks))
rin = d / f"{new}.rin"
if rin.exists() or rin.is_symlink(): rin.unlink()
rin.symlink_to(f"{last}.rout")
json.dump({"job": new, "vorgaenger": last, "t_start": n * DT, "schritte_fertig": n}, open(d / f"{new}.meta", "w"))
