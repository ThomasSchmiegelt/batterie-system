#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-24), Entwurf. Ein Lauf E3b: Netz, Elmer, Kennzahlen -> lauf/<name>/res.json. Aufruf: lauf_einzel.py FALL VAR NETZ [SENS]. Ueberspringt fertige Laeufe."""
import json, os, sys, subprocess, math, re
import numpy as np
H = os.path.dirname(os.path.abspath(__file__)); a = sys.argv[1:]; name = "_".join([a[0], a[1], a[2]]+a[3:4])
D = f"{H}/lauf/{name}"
if os.path.exists(f"{D}/res.json"): print("fertig", name); sys.exit(0)
subprocess.run([sys.executable, f"{H}/e3b_rechnen.py"]+a, check=True, stdout=subprocess.DEVNULL)
for f in ("scalars.dat", "e3b.vtu", "e3b0001.vtu"):
    try: os.remove(f"{D}/{f}")
    except OSError: pass
lg = open(f"{D}/elmer.log", "w"); subprocess.run(["nice", "-n", "15", "ElmerSolver", "e3b.sif"], cwd=D, check=True, stdout=lg, stderr=subprocess.STDOUT); lg.close()
import meshio
vt = [f for f in os.listdir(D) if f.endswith(".vtu")][0]; m = meshio.read(f"{D}/{vt}")
T = m.point_data["temperature"]-273.15; X = m.points
info = json.load(open(f"{D}/netzinfo.json")); sc = np.loadtxt(f"{D}/scalars.dat")
nm = {mm.group(1): int(mm.group(2))+99 for mm in re.finditer(r"\$ (\w+) = (\d+)", open(f"{D}/mesh.names").read().split("boundaries")[1])}
tri = None; ids = None
for ci, c in enumerate(m.cells):
    if c.type == "triangle": tri = c.data; ids = m.cell_data["GeometryIds"][ci] if "GeometryIds" in m.cell_data else None
EIN_h, EIN_eps, Tu = 5.0, 0.9, 45.0
def flux_in(sel):
    v = 0.0
    for t_, i_ in zip(tri[sel], ids[sel]):
        p = X[t_]; ar = 0.5*np.linalg.norm(np.cross(p[1]-p[0], p[2]-p[0])); Tt = T[t_].mean()
        v += ar*(EIN_h*(Tt-Tu)+EIN_eps*5.670374e-8*((Tt+273.15)**4-(Tu+273.15)**4))
    return v
ztop = X[:, 2].max(); zc = X[tri][:, :, 2]; sel_top = np.all(np.abs(zc-ztop) < 1e-9, axis=1); sel_unt = np.all(np.abs(zc) < 1e-9, axis=1)   # Flaechen nach Lage (Elmer-Rand-IDs sind umnummeriert)
Q_top = flux_in(sel_top); Q_unten = flux_in(sel_unt) if "unten" in nm else 0.0
i = int(np.argmax(T)); P = info.get("P_W")
res = dict(lauf=name, T_max_C=float(T.max()), T_min_C=float(T.min()), T_max_ort_mm=[float(x)*1000 for x in X[i]], Q_wand_elmer_W=(-float(sc[2]) if len(sc) > 2 else None),
           Q_oben_W=Q_top, Q_unten_luft_W=Q_unten, tets=info["tets"], knoten=info["knoten"], lam_xy=info["lam_xy"], lam_via_z=info["lam_via_z"], f_via=info["f_via"], vtu=vt)
json.dump(res, open(f"{D}/res.json", "w"), indent=1); print(res)
