#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-23), Entwurf. QN1 V1: Elmer Waerme stationaer, Platte Dicke L, Quelle q, beide Seiten T_w.
Analytisch: T_max - T_w = q L^2/(8 k); Waermestrom je Wand = q L/2 (je m^2). Netz: strukturiertes Q4-Netz (gmsh transfinite, ElmerGrid 14 2),
Streifen 1 Zelle breit (seitlich adiabat). Aufruf: python3 v1_elmer.py"""
import json, os, subprocess, sys, shutil
import numpy as np
from vcommon import *
L, q, k, Tw = w("V1_dicke_L_m"), w("V1_quelle_q_W_m3"), w("V1_leitfaehigkeit_k_W_mK"), w("V1_wandtemperatur_C")
dT_ana = q*L*L/(8*k)
def rechne(N):
    import gmsh
    D = f"{H}/lauf_V1/N{N}"; shutil.rmtree(D, ignore_errors=True); os.makedirs(D)
    gmsh.initialize(["-v", "0"]); gmsh.option.setNumber("General.Terminal", 0); gmsh.model.add("v1"); B = L/10        # Streifenbreite (Annahme Sonnet, ohne Einfluss: adiabat, eindimensional)
    p = [gmsh.model.geo.addPoint(x, y, 0) for x, y in ((0, 0), (B, 0), (B, L), (0, L))]
    l = [gmsh.model.geo.addLine(p[i], p[(i+1) % 4]) for i in range(4)]
    cl = gmsh.model.geo.addCurveLoop(l); s = gmsh.model.geo.addPlaneSurface([cl])
    gmsh.model.geo.mesh.setTransfiniteCurve(l[0], 2); gmsh.model.geo.mesh.setTransfiniteCurve(l[2], 2)
    gmsh.model.geo.mesh.setTransfiniteCurve(l[1], N+1); gmsh.model.geo.mesh.setTransfiniteCurve(l[3], N+1)
    gmsh.model.geo.mesh.setTransfiniteSurface(s); gmsh.model.geo.mesh.setRecombine(2, s); gmsh.model.geo.synchronize()
    gmsh.model.addPhysicalGroup(1, [l[0]], 1); gmsh.model.addPhysicalGroup(1, [l[2]], 2); gmsh.model.addPhysicalGroup(1, [l[1], l[3]], 3); gmsh.model.addPhysicalGroup(2, [s], 1)
    gmsh.option.setNumber("Mesh.MshFileVersion", 2.2); gmsh.model.mesh.generate(2); gmsh.write(f"{D}/netz.msh"); gmsh.finalize()
    subprocess.run(["ElmerGrid", "14", "2", "netz.msh", "-autoclean"], cwd=D, check=True, capture_output=True)
    open(f"{D}/v1.sif", "w").write(f"""Header
  Mesh DB "." "netz"
End
Simulation
  Coordinate System = Cartesian 2D
  Simulation Type = Steady State
  Steady State Max Iterations = 1
  Output Intervals = 0
End
Constants
End
Equation 1
  Active Solvers(2) = 1 2
End
Solver 1
  Equation = Heat Equation
  Procedure = "HeatSolve" "HeatSolver"
  Variable = Temperature
  Calculate Loads = Logical True
  Linear System Solver = Direct
  Linear System Direct Method = UMFPACK
  Steady State Convergence Tolerance = 1e-10
End
Solver 2
  Equation = SaveScalars
  Procedure = "SaveData" "SaveScalars"
  Filename = skalare.dat
  Variable 1 = Temperature
  Operator 1 = max
  Variable 2 = Temperature
  Operator 2 = min
  Variable 3 = Temperature Loads
  Operator 3 = boundary sum
End
Material 1
  Name = "Testwerkstoff"
  Density = 1.0
  Heat Conductivity = {k}
End
Body 1
  Target Bodies(1) = 1
  Equation = 1
  Material = 1
  Body Force = 1
End
Body Force 1
  Heat Source = {q}
End
Boundary Condition 1
  Target Boundaries(1) = 1
  Temperature = {Tw}
  Save Scalars = Logical True
End
Boundary Condition 2
  Target Boundaries(1) = 2
  Temperature = {Tw}
  Save Scalars = Logical True
End
""")
    r = subprocess.run(["ElmerSolver", "v1.sif"], cwd=D, capture_output=True, text=True); open(f"{D}/solver.log", "w").write(r.stdout[-5000:]+r.stderr[-2000:])
    if r.returncode: sys.exit(f"ElmerSolver Fehler N={N}, siehe {D}/solver.log")
    sk = [float(x) for x in open(f"{D}/skalare.dat").read().split()] if False else None
    names = open(f"{D}/skalare.dat.names").read(); vals = [float(x) for x in open(f"{D}/skalare.dat").read().split()]
    # Spalten: max T, min T, boundary sum loads (Elmer-Namen siehe .names)
    return dict(N=N, h_m=L/N, T_max=vals[0], T_min=vals[1], loads_sum=vals[2], namen=names.strip().splitlines()[-4:])
def serie(Ns):
    res = []
    for N in Ns:
        r = rechne(N); r["abw_pct"] = 100*(r["T_max"]-Tw-dT_ana)/dT_ana; res.append(r)
        # Waermestrom: Elmer 'temperature loads' (Boundary Sum) ueber alle Randknoten = Waermestrom beider Waende je Streifenbreite B und Tiefe 1 m
        B = L/10; r["waermestrom_ist_W_je_m"] = abs(r["loads_sum"]); r["waermestrom_soll_W_je_m"] = q*L*B
        r["waermestrom_abw_pct"] = 100*(r["waermestrom_ist_W_je_m"]/r["waermestrom_soll_W_je_m"]-1)
    return res
ung = serie(w("V1_netzstufen_elemente_ungerade")); ger = serie(w("V1_netzstufen_elemente_gerade_zusatz"))
h = [r["h_m"] for r in ung]; err = [abs(r["abw_pct"]) for r in ung]
out = dict(hinweis="KI-generiert (Claude Sonnet, 2026-11-23), Entwurf. Erzeugt von v1_elmer.py.", loesung_dT_K=dT_ana, werkzeug="Elmer HeatSolve (v26.2), Q4 linear",
           reihe_ungerade=ung, reihe_gerade_zusatz=ger, ordnung_beobachtet=ordnung(h, err), abweichung_fein_pct=ung[-1]["abw_pct"],
           waermestrom_abw_fein_pct=ung[-1]["waermestrom_abw_pct"], toleranz_pct=TOL["V1_T_pct"], toleranz_waermestrom_pct=TOL["V1_waermestrom_pct"],
           bestanden=bool(abs(ung[-1]["abw_pct"]) < TOL["V1_T_pct"] and abs(ung[-1]["waermestrom_abw_pct"]) < TOL["V1_waermestrom_pct"]),
           anmerkung_gerade="Gerade Elementzahl: Knoten in der Mitte, Knotenwert bei konstanter Quelle und Q4 exakt (Abweichung nahe Rundung), Ordnung dort nicht bestimmbar.")
speichere("V1", out)
