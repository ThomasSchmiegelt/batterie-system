#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-18), Entwurf. Auftrag X1 (AUFTRAG.md, ERWARTUNG.md).
Aufruf: x1.py <LFP|NMC> <LF1|LF2> <netzname> <h_nah_mm> [umax_mm]
Schritte: gmsh-Netz (Schalen S8R/S6) -> CalculiX-Deck (Kontakt, NLGEOM, Plastizität) -> ccx -> auswerten.py."""
import sys, json, math, subprocess, os
from pathlib import Path
import numpy as np, gmsh
D = Path(__file__).resolve().parent
EI = json.load(open(D / "eingaben.json"))
var, lf, netz, hn = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]); UMAX = float(sys.argv[5]) if len(sys.argv) > 5 else 60.0
HF = float(os.environ.get('X1_HF', 40))
V = EI["varianten"][var]; L = V["L_mm"]; h = V["rahmen_hoehe_mm"]; W = V["rahmen_breite_mm"]; tw = V["rahmen_wand_mm"]; nk = V["rahmen_kammern"]
qx = V["quertraeger_x0_mm"]; qb = V["quertraeger_breite_mm"]; qh = V["quertraeger_hoehe_mm"]; qt = V["quertraeger_wand_mm"]; zc = V["quertraeger_zmitte_ueber_rahmenunterkante_mm"]
bt = V["boden_dicke_mm"]; YL = EI["modell_ausschnitt"]["quertraeger_laenge_mm"]["wert"]
xp = (qx[0] + qb / 2 + qx[1] + qb / 2) / 2 if lf == "LF1" else qx[1] + qb / 2
Rp = EI["pfahl"]["durchmesser_mm"]["wert"] / 2
T = D / "lauf" / f"{var}_{lf}_{netz}"; T.mkdir(parents=True, exist_ok=True)
ym = tw / 2; ywebs = [ym + i * (W - tw) / nk for i in range(nk + 1)]   # Stege (Wände) bei y
zb, zt = tw / 2, h - tw / 2
# ---------------- Geometrie
gmsh.initialize(); gmsh.option.setNumber("General.Terminal", 0); gmsh.model.add("x1"); oc = gmsh.model.occ
def quad(p0, p1, p2, p3):
    ps = [oc.addPoint(*p) for p in (p0, p1, p2, p3)]; ls = [oc.addLine(ps[i], ps[(i + 1) % 4]) for i in range(4)]
    return oc.addPlaneSurface([oc.addCurveLoop(ls)])
fr = [];  cm = []; pl = []; op = []
for y in ywebs: fr.append(quad((0, y, zb), (L, y, zb), (L, y, zt), (0, y, zt)))          # Stege / Aussen- und Innenwand
for z in (zb, zt): fr.append(quad((0, ym, z), (L, ym, z), (L, W - ym, z), (0, W - ym, z)))   # Gurte
yi = W - ym
for x0 in qx:
    xa, xb = x0 + qt / 2, x0 + qb - qt / 2; za, zz = zc - qh / 2 + qt / 2, zc + qh / 2 - qt / 2
    cm += [quad((xa, yi, za), (xa, YL, za), (xa, YL, zz), (xa, yi, zz)), quad((xb, yi, za), (xb, YL, za), (xb, YL, zz), (xb, yi, zz)),
           quad((xa, yi, za), (xb, yi, za), (xb, YL, za), (xa, YL, za)), quad((xa, yi, zz), (xb, yi, zz), (xb, YL, zz), (xa, YL, zz))]
    op.append(quad((xa, yi, za), (xb, yi, za), (xb, yi, zz), (xa, yi, zz)))
pl.append(quad((0, yi, zb), (L, yi, zb), (L, YL, zb), (0, YL, zb)))
oc.synchronize()
allf = [(2, s) for s in fr + cm + pl + op]
res, _ = oc.fragment(allf, []); oc.synchronize()
def cog(t): return gmsh.model.occ.getCenterOfMass(2, t)
# Öffnungsflächen entfernen: Fläche in Ebene y=yi, innerhalb der Öffnungsrechtecke
rem = []
for (_, s) in gmsh.model.getEntities(2):
    c = cog(s); bb = gmsh.model.getBoundingBox(2, s)
    if abs(bb[1] - yi) < 1e-6 and abs(bb[4] - yi) < 1e-6:
        for x0 in qx:
            xa, xb = x0 + qt / 2, x0 + qb - qt / 2
            if xa - 1e-6 <= bb[0] and bb[3] <= xb + 1e-6 and (zc - qh / 2 + qt / 2 - 1e-6) <= bb[2] and bb[5] <= zc + qh / 2 - qt / 2 + 1e-6: rem.append((2, s))
oc.remove(rem); oc.synchronize()
# Gruppen nach Lage
grp = {"RAHMEN": [], "QUER": [], "BODEN": [], "AUSSEN": [], "INNEN": []}
for (_, s) in gmsh.model.getEntities(2):
    bb = gmsh.model.getBoundingBox(2, s)
    if abs(bb[2] - zb) < 1e-6 and abs(bb[5] - zb) < 1e-6 and bb[4] > yi + 1: grp["BODEN"].append(s)       # Bodenstreifen
    elif bb[1] > yi - 1e-6 and bb[4] > yi + 1e-6 and not (abs(bb[1] - bb[4]) < 1e-6): grp["QUER"].append(s) if bb[0] > 0 and bb[3] < L else grp["BODEN"].append(s)
    elif abs(bb[1] - bb[4]) < 1e-6 and abs(bb[1] - yi) < 1e-6 and (bb[0] >= 0): grp["RAHMEN"].append(s); grp["INNEN"].append(s)
    else: grp["RAHMEN"].append(s)
    if abs(bb[1] - ym) < 1e-6 and abs(bb[4] - ym) < 1e-6: grp["AUSSEN"].append(s)
# Bodenstreifenstücke zwischen Querträgern fehlen nicht (Streifen y>yi) – Querträger liegen über dem Boden (z>zb)
gmsh.model.occ.synchronize()
xmid = xp
f = gmsh.model.mesh.field
f.add("MathEval", 1); f.setString(1, "F", f"{hn}+({HF}-{hn})*Min(1,Max(0,(Sqrt((x-{xmid})^2+0.25*y^2)-110)/250))")
f.setAsBackgroundMesh(1)
gmsh.option.setNumber("Mesh.MeshSizeExtendFromBoundary", 0); gmsh.option.setNumber("Mesh.MeshSizeFromPoints", 0); gmsh.option.setNumber("Mesh.MeshSizeFromCurvature", 0)
gmsh.option.setNumber("Mesh.Algorithm", 8); gmsh.option.setNumber("Mesh.RecombineAll", 1); gmsh.option.setNumber("Mesh.RecombinationAlgorithm", 1)
gmsh.option.setNumber("Mesh.ElementOrder", 2); gmsh.option.setNumber("Mesh.SecondOrderIncomplete", 1)
gmsh.model.mesh.generate(2); gmsh.model.mesh.setOrder(2)
ntags, ncoord, _ = gmsh.model.mesh.getNodes(); ncoord = ncoord.reshape(-1, 3); node = {int(t): c for t, c in zip(ntags, ncoord)}
# ---- Elemente je Fläche
elems = {"S8R": [], "S6": []}; eg = {}   # eid -> (typ, nodes, gruppe)
eid = 0; byg = {k: [] for k in grp}; sect = {}
def gname(s):
    if s in grp["BODEN"]: return "BODEN"
    if s in grp["QUER"]: return "QUER"
    return "RAHMEN"
for (_, s) in gmsh.model.getEntities(2):
    types, etags, enodes = gmsh.model.mesh.getElements(2, s)
    for ty, et, en in zip(types, etags, enodes):
        npn = {16: 8, 9: 6, 3: 4, 2: 3, 10: 9}.get(ty)
        if ty not in (16, 9): raise SystemExit(f"Elementtyp {ty} nicht erwartet")
        en = np.array(en, dtype=int).reshape(-1, npn)
        for row in en:
            eid += 1; tname = "S8R" if ty == 16 else "S6"; elems[tname].append((eid, [int(x) for x in row])); eg[eid] = gname(s)
            if s in grp["AUSSEN"]: byg["AUSSEN"].append((eid, [int(x) for x in row], tname))
            if s in grp["INNEN"]: byg["INNEN"].append((eid, [int(x) for x in row], tname))
gmsh.finalize()
used = sorted({n for t in elems for _, nn in elems[t] for n in nn}); 
# ---------------- Pfahl: Hex-Platte
RE = Rp                            # ccx expandiert Schalen: Kontaktfläche = echte Aussenfläche (y = 0), kein Versatz
cl = 0.5                           # Anfangsabstand Pfahlspitze zur Mittelfläche der Aussenwand in mm (Pfahlweg beginnt bei 0)
cy = 0.0 - cl - RE
ang = np.radians(np.linspace(-80, 80, int(160 * math.pi / 180 * RE / 8) + 1)); zs = np.linspace(-30, h + 30, int((h + 60) / 8) + 1)
dp = 10.0; nid0 = 1000000; pn = {}; pe = []
def pnid(i, j, k): return nid0 + (k * len(ang) + i) * len(zs) + j
for k, r in enumerate((RE, RE - dp)):
    for i, a in enumerate(ang):
        for j, z in enumerate(zs): pn[pnid(i, j, k)] = (xp + r * math.sin(a), cy + r * math.cos(a), z)
pid = 2000000
for i in range(len(ang) - 1):
    for j in range(len(zs) - 1):
        pid += 1; pe.append((pid, [pnid(i, j, 0), pnid(i + 1, j, 0), pnid(i + 1, j + 1, 0), pnid(i, j + 1, 0), pnid(i, j, 1), pnid(i + 1, j, 1), pnid(i + 1, j + 1, 1), pnid(i, j + 1, 1)]))
# Orientierung prüfen (Volumen > 0)
def hexvol(nn):
    p = np.array([pn[n] for n in nn]); return np.dot(np.cross(p[1] - p[0], p[3] - p[0]), p[4] - p[0])
if hexvol(pe[0][1]) < 0: pe = [(i, [n[0], n[3], n[2], n[1], n[4], n[7], n[6], n[5]]) for i, n in pe]
# Basisfläche (k=0, Kontaktseite) = Fläche F1 (Knoten 1-2-3-4), Aussennormale F1 zeigt weg von Knoten 5-8 -> zum Rahmen
backn = [pnid(i, j, 1) for i in range(len(ang)) for j in range(len(zs))]
# Normale der Rahmen-Aussenwand: Knotenreihenfolge -> Richtung
def normal(nn):
    p = [node[n] for n in nn[:4]]; return np.cross(p[1] - p[0], p[3] - p[0])
# ---------------- Deck schreiben
mat = EI["werkstoff"]; Em = mat["E_MPa"]["wert"]; nu = mat["nu"]["wert"]; Rp02 = mat["Rp02_MPa"]["wert"]; Rm = mat["Rm_MPa"]["wert"]; Au = mat["Bruchdehnung"]["wert"]
cx0 = [x0 for x0 in qx]
nodes_inn = []   # Innenwand-Knoten (Messung Zellberührung) nur im Bereich |x - xp| < 500
ninn = {n for _, nn, _ in byg["INNEN"] for n in nn}
ninn = sorted(n for n in ninn if abs(node[n][0] - xp) < 500)
nfix_end = sorted(n for n in used if node[n][0] < 1e-6 or node[n][0] > L - 1e-6)
nfix_far = sorted(n for n in used if node[n][1] > YL - 1e-6)
with open(T / "x1.inp", "w") as fo:
    w = fo.write
    w("*NODE, NSET=NALL\n")
    for n in used: w(f"{n}, {node[n][0]:.6f}, {node[n][1]:.6f}, {node[n][2]:.6f}\n")
    for n, c in pn.items(): w(f"{n}, {c[0]:.6f}, {c[1]:.6f}, {c[2]:.6f}\n")
    for tname, lst in elems.items():
        if not lst: continue
        for g in ("RAHMEN", "QUER", "BODEN"):
            sel = [e for e in lst if eg[e[0]] == g]
            if not sel: continue
            w(f"*ELEMENT, TYPE={tname}, ELSET=E_{g}_{tname}\n")
            for i, nn in sel: w(f"{i}, " + ", ".join(map(str, nn)) + "\n")
    w("*ELEMENT, TYPE=C3D8, ELSET=EPFAHL\n")
    for i, nn in pe: w(f"{i}, " + ", ".join(map(str, nn)) + "\n")
    for g, ts in (("RAHMEN", tw), ("QUER", qt), ("BODEN", bt)):
        names = [f"E_{g}_{t}" for t in ("S8R", "S6") if any(eg[e[0]] == g for e in elems[t])]
        w(f"*ELSET, ELSET=E_{g}\n" + ",\n".join(names) + "\n")
        for nm in names: w(f"*SHELL SECTION, ELSET={nm}, MATERIAL=AL\n{ts}\n")
    w(f"*SOLID SECTION, ELSET=EPFAHL, MATERIAL=PFAHL\n")
    w(f"*MATERIAL, NAME=AL\n*ELASTIC\n{Em}, {nu}\n*PLASTIC\n{Rp02}, 0.0\n{Rm}, {Au}\n")
    w(f"*MATERIAL, NAME=PFAHL\n*ELASTIC\n{2.1e7}, 0.3\n")
    # Aussenfläche (Slave) als Elementfläche der Schale; Pfahl (Master) Fläche F1 der Hex-Elemente
    # Normalenrichtung: SPOS wenn Normale in -y zeigt (zum Pfahl)
    spos = []; sneg = []
    for i, nn, tn in byg["AUSSEN"]:
        (spos if normal(nn)[1] < 0 else sneg).append(i)
    w("*SURFACE, NAME=SAUSSEN, TYPE=ELEMENT\n")
    for i in spos: w(f"{i}, SPOS\n")
    for i in sneg: w(f"{i}, SNEG\n")
    w("*SURFACE, NAME=SPFAHL, TYPE=ELEMENT\n")
    for i, _ in pe: w(f"{i}, S1\n")
    w("*SURFACE INTERACTION, NAME=SI\n*SURFACE BEHAVIOR, PRESSURE-OVERCLOSURE=LINEAR\n1.e5\n")
    w("*CONTACT PAIR, INTERACTION=SI, TYPE=SURFACE TO SURFACE\nSAUSSEN, SPFAHL\n")
    w("*NSET, NSET=NEND\n" + ",\n".join(map(str, nfix_end)) + "\n")
    w("*NSET, NSET=NFAR\n" + ",\n".join(map(str, nfix_far)) + "\n")
    w("*NSET, NSET=NBACK\n" + ",\n".join(map(str, backn)) + "\n")
    w("*NSET, NSET=NINN\n" + ",\n".join(map(str, ninn)) + "\n")
    w("*BOUNDARY\nNEND, 1, 3\nNFAR, 1, 3\n*BOUNDARY\nNBACK, 1, 1\nNBACK, 3, 3\n")
    w("*STEP, NLGEOM, INC=400\n*STATIC\n0.01, 1.0, 1.e-5, 0.02\n")
    w(f"*BOUNDARY\nNBACK, 2, 2, {UMAX}\n")
    w("*NODE PRINT, NSET=NBACK, TOTALS=ONLY, FREQUENCY=1\nRF\n*NODE PRINT, NSET=NINN, FREQUENCY=1\nU\n")
    w("*NODE FILE, FREQUENCY=10\nU\n*EL FILE, FREQUENCY=10\nPEEQ\n*END STEP\n")
json.dump({"var": var, "lf": lf, "netz": netz, "xp": xp, "h_nah": hn, "umax": UMAX, "cl": cl, "n_knoten": len(used), "n_elem": eid, "pole_back_nodes": len(backn),
           "inn_x": {str(n): node[n][0] for n in ninn}, "L": L, "h": h, "quer_x0": qx, "qb": qb, "spos": len(spos), "sneg": len(sneg)}, open(T / "modell.json", "w"))
print("Deck", T / "x1.inp", "Knoten", len(used), "Elemente", eid, "spos/sneg", len(spos), len(sneg), "xp", xp)
