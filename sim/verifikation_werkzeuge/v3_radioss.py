#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-23), Entwurf. QN1 V3: OpenRadioss (OpenCourant-Build), Kragbalken quasistatisch linear-elastisch, Endkraft F.
Analytisch: delta = F L^3/(3 E I), I = b^4/12 (Euler-Bernoulli). Einheiten mm, kg, ms (Kraft kN, Spannung GPa). Brick (Isolid 24, MAT/ELAST), eingespannte Stirnflaeche,
Last: glatte cos-Rampe der Endkraft ueber V3_rampe_ms (viele Eigenperioden), dann Halten; Durchbiegung = Mittel der letzten 10 ms am Balkenende (Mittel der Endknoten).
Energiebilanz: Aeussere Arbeit - (innere + kinetische + Rotations- + Feder- + Kontakt- + Hourglass-Energie) aus der TH-Datei, max. Betrag / Endarbeit, gegen 1 %. Aufruf: python3 v3_radioss.py"""
import json, os, subprocess, shutil, csv, re, math, sys
import numpy as np
from vcommon import *
L, b, E, nu, rho, F, Tr = w("V3_laenge_mm"), w("V3_querschnitt_mm"), w("V3_E_GPa"), w("V3_nu"), w("V3_rho_kg_mm3"), w("V3_kraft_kN"), w("V3_rampe_ms")
nl, nq = w("V3_elemente")["laengs"], w("V3_elemente")["quer"]
I = b**4/12; delta_ana = F*L**3/(3*E*I)
TEND = Tr+40.0
D = f"{H}/lauf_V3"; shutil.rmtree(D, ignore_errors=True); os.makedirs(D)
nid = lambda i, j, k: 1+i+(nl+1)*(j+(nq+1)*k)
r = ["#RADIOSS STARTER", "/BEGIN", "V3E", "      2019         0", "                  kg                  mm                  ms", "                  kg                  mm                  ms", "/TITLE", "KI-generiert (Claude Sonnet) Entwurf QN1 V3 Kragbalken", "/NODE"]
for k in range(nq+1):
    for j in range(nq+1):
        for i in range(nl+1): r.append(f"{nid(i,j,k):10d}{i*L/nl:20.8g}{j*b/nq:20.8g}{k*b/nq:20.8g}")
r += ["/MAT/ELAST/1", "Testwerkstoff", f"{rho:20.8g}{0:20d}", f"{E:20.8g}{nu:20.8g}",
      "/PROP/TYPE14/1", "Balken", "#   Isolid    Ismstr               Icpre     Inpts Itetra4 Itetra10      Imas    Iframe", "        24         0                   0         0         0         0         0         1",
      "#                 qa                  qb                   h", f"{0:20d}{0:20d}{0.1:20.8g}", "#           LAMBDA_V                MU_V                  dn", f"{0:20d}{0:20d}{0:20d}", "#             dt_min", f"{0:20d}",
      "/PART/1", "Balken", f"{1:10d}{1:10d}{0:10d}", "/BRICK/1"]
eid = 0
for k in range(nq):
    for j in range(nq):
        for i in range(nl):
            eid += 1; n = [nid(i, j, k), nid(i+1, j, k), nid(i+1, j+1, k), nid(i, j+1, k), nid(i, j, k+1), nid(i+1, j, k+1), nid(i+1, j+1, k+1), nid(i, j+1, k+1)]
            r.append(f"{eid:10d}" + "".join(f"{x:10d}" for x in n))
lst = lambda ns: "\n".join("".join(f"{x:10d}" for x in ns[i:i+10]) for i in range(0, len(ns), 10))
fix = [nid(0, j, k) for k in range(nq+1) for j in range(nq+1)]; tip = [nid(nl, j, k) for k in range(nq+1) for j in range(nq+1)]
r += ["/GRNOD/NODE/1", "eingespannt", lst(fix), "/BCS/1", "fest", "#  Tra rot   skew_ID  grnod_ID", "   111 111         0         1", "/GRNOD/NODE/2", "balkenende", lst(tip),
      "/CLOAD/1", "endkraft", "#funct_IDT       Dir   skew_ID sensor_ID  grnod_ID                       Ascalex             Fscaley", f"{1:10d}{'Y':>10s}{0:10d}{0:10d}{2:10d}{1:30.8g}{F/len(tip):20.8g}", "/FUNCT/1", "rampe", "#                  X                   Y"]
npt = 61
for m in range(npt): t = Tr*m/(npt-1); r.append(f"{t:20.8g}{0.5*(1-math.cos(math.pi*t/Tr)):20.8g}")
r += [f"{TEND*2:20.8g}{1.0:20.8g}", "/TH/NODE/1", "ende", "DEF", "#    NODid     Iskew"] + [f"{n:10d}{0:10d}" for n in tip] + ["/END"]
open(f"{D}/V3E_0000.rad", "w").write("\n".join(r)+"\n")
open(f"{D}/V3E_0001.rad", "w").write(f"/RUN/V3E/1\n{TEND:20.8g}\n/TFILE/4\n0.1\n/PRINT/-1/50000\n/DT\n0.9 0.0\n/PARITH/ON\n/ANIM/DT\n0.0 {TEND:.6g}\n")
env = dict(os.environ); OC = "/home/cae/cae_projekte/werkzeuge/opencourant/OpenCourant"
env.update(OPENCOURANT_PATH=OC, RAD_CFG_PATH=f"{OC}/hm_cfg_files", RAD_H3D_PATH=f"{OC}/extlib/h3d/lib/linux64", OMP_STACKSIZE="400m", OMP_NUM_THREADS="4", LD_LIBRARY_PATH=f"{OC}/extlib/hm_reader/linux64/:"+env.get("LD_LIBRARY_PATH", ""))
for exe, inp, lg in (("starter_linux64_gf", ["-i", "V3E_0000.rad", "-np", "1"], "starter.log"), ("engine_linux64_gf", ["-i", "V3E_0001.rad"], "engine.log")):
    p = subprocess.run([f"{OC}/exec/{exe}"]+inp, cwd=D, env=env, capture_output=True, text=True); open(f"{D}/{lg}", "w").write(p.stdout)
    if "NORMAL TERMINATION" not in p.stdout and "TERMINATION WITH WARNING" not in p.stdout: sys.exit(f"{exe} fehlgeschlagen, siehe {D}/{lg}")
th = [f for f in os.listdir(D) if re.match(r"V3ET\d+", f)][0]
subprocess.run([f"{OC}/exec/th_to_csv_linux64_gf", th], cwd=D, env=env, capture_output=True)
rows = list(csv.reader(open(f"{D}/{th}.csv"))); hd = rows[0]; A = np.array([[float(x) for x in rw] for rw in rows[1:]])
# TH-Spalten (geprueft an V3ET01.csv): 0 Zeit, 1 INTERNAL ENERGY, 2 KINETIC ENERGY, 8 ROTATION ENERGY, 9 EXTERNAL WORK, 10 SPRING, 11 CONTACT, 12 HOURGLASS;
# je Endknoten 6 Werte ab Spalte 24 (DX, DY, DZ, VX, VY, VZ), DY = 25+6n
assert hd[1] == "INTERNAL ENERGY" and hd[9] == "EXTERNAL WORK" and hd[2] == "KINETIC ENERGY"
nn = len(tip); cy = [25+6*n for n in range(nn)]; assert len(hd) == 24+6*nn
t = A[:, 0]; dy = A[:, cy].mean(axis=1)
m = t > TEND-10.0; delta = float(dy[m].mean()); osz = float(dy[m].max()-dy[m].min())
bil = A[:, 9]-(A[:, 1]+A[:, 2]+A[:, 8]+A[:, 10]+A[:, 11]+A[:, 12])       # Arbeit - (innere + kinetische + Rotation + Feder + Kontakt + Hourglass)
fe_max = float(100*np.abs(bil).max()/abs(A[-1, 9])); fe_end = float(100*bil[-1]/A[-1, 9])
IE = float(A[-1, 1]); W_ext = float(A[-1, 9]); W_clap = 0.5*F*delta       # kN*mm = J
abw = 100*(delta/delta_ana-1)
res = dict(hinweis="KI-generiert (Claude Sonnet, 2026-11-23), Entwurf. Erzeugt von v3_radioss.py.", werkzeug="OpenRadioss (OpenCourant-Build), Brick Isolid 24, MAT/ELAST", L_mm=L, b_mm=b, I_mm4=I, E_GPa=E, F_kN=F,
           delta_analytisch_mm=delta_ana, delta_werkzeug_mm=delta, restschwingung_mm=osz, abweichung_fein_pct=abw, ordnung_beobachtet=None,
           energiefehler_max_pct=fe_max, energiefehler_ende_pct=fe_end, aeussere_arbeit_J=W_ext, innere_energie_J=IE, clapeyron_FdeltaHalbe_J=W_clap, aeussere_arbeit_gegen_clapeyron_pct=100*(W_ext/W_clap-1),
           toleranz_delta_pct=TOL["V3_delta_pct"], toleranz_energie_pct=TOL["V3_energie_pct"], laufzeit_ms=TEND, zyklen=int(re.search(r"TOTAL NUMBER OF CYCLES\s*:\s*(\d+)", open(f"{D}/V3E_0001.out").read()).group(1)))
res["bestanden"] = bool(abs(abw) < TOL["V3_delta_pct"] and fe_max < TOL["V3_energie_pct"])
speichere("V3", res)
