#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-18), Entwurf. Auftrag X1b/X2-OC (AUFTRAG_X2.md, ERWARTUNG.md Nachtrag 1). Netz und Geometrie wie x1b.py (linear), Deck fuer OpenCourant (Radioss), Einheiten mm, ms, kg (kN, GPa, J).
Aufruf: x2.py <LFP|NMC> <w_mm> [h_nah_mm=12] [h_knaut_mm=4]; Ausgabe lauf_oc/<V>_w<w>/{X2_0000.rad,X2_0001.rad,modell.json}"""
import sys, json, math, subprocess, os
from pathlib import Path
import numpy as np, gmsh
D = Path(__file__).resolve().parent
EI = json.load(open(D.parent / "x1_seitencrash" / "eingaben.json")); TK = 2.0
var, lf, wk = sys.argv[1], "LF1", float(sys.argv[2]); hn = float(sys.argv[3]) if len(sys.argv) > 3 else 12.0; hk = float(sys.argv[4]) if len(sys.argv) > 4 else 4.0; netz = f"w{wk:g}" + os.environ.get("X1_TAG", "")
HF = float(os.environ.get('X1_HF', 40))
V = EI["varianten"][var]; L = V["L_mm"]; h = V["rahmen_hoehe_mm"]; W = V["rahmen_breite_mm"]; tw = V["rahmen_wand_mm"]; nk = V["rahmen_kammern"]
qx = V["quertraeger_x0_mm"]; qb = V["quertraeger_breite_mm"]; qh = V["quertraeger_hoehe_mm"]; qt = V["quertraeger_wand_mm"]; zc = V["quertraeger_zmitte_ueber_rahmenunterkante_mm"]
bt = V["boden_dicke_mm"]; YL = EI["modell_ausschnitt"]["quertraeger_laenge_mm"]["wert"]
xp = (qx[0] + qb / 2 + qx[1] + qb / 2) / 2 if lf == "LF1" else qx[1] + qb / 2
Rp = EI["pfahl"]["durchmesser_mm"]["wert"] / 2
T = D / os.environ.get("X2_DIR", "lauf_oc") / f"{var}_{netz}"; T.mkdir(parents=True, exist_ok=True)
ym = tw / 2; yo = -wk + TK / 2; ymid = (yo + ym) / 2; ywebs = [ym + i * (W - tw) / nk for i in range(nk + 1)]   # Stege (Wände) bei y
zb, zt = tw / 2, h - tw / 2
# ---------------- Geometrie
gmsh.initialize(); gmsh.option.setNumber("General.Terminal", 0); gmsh.model.add("x1"); oc = gmsh.model.occ
def quad(p0, p1, p2, p3):
    ps = [oc.addPoint(*p) for p in (p0, p1, p2, p3)]; ls = [oc.addLine(ps[i], ps[(i + 1) % 4]) for i in range(4)]
    return oc.addPlaneSurface([oc.addCurveLoop(ls)])
fr = [];  cm = []; pl = []; op = []
for y in ywebs: fr.append(quad((0, y, zb), (L, y, zb), (L, y, zt), (0, y, zt)))          # Stege / Aussen- und Innenwand
for z in (zb, zt): fr.append(quad((0, yo, z), (L, yo, z), (L, W - ym, z), (0, W - ym, z)))
for y in (yo, ymid): fr.append(quad((0, y, zb), (L, y, zb), (L, y, zt), (0, y, zt)))   # Knautschprofil: Aussenwand, Mittelsteg   # Gurte
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
grp = {"KNAUT": [], "RAHMEN": [], "QUER": [], "BODEN": [], "AUSSEN": [], "INNEN": []}
for (_, s) in gmsh.model.getEntities(2):
    bb = gmsh.model.getBoundingBox(2, s)
    if bb[4] <= ym + 1e-6 and bb[1] < ym - 1e-6: grp["KNAUT"].append(s)
    elif abs(bb[2] - zb) < 1e-6 and abs(bb[5] - zb) < 1e-6 and bb[4] > yi + 1: grp["BODEN"].append(s)       # Bodenstreifen
    elif bb[1] > yi - 1e-6 and bb[4] > yi + 1e-6 and not (abs(bb[1] - bb[4]) < 1e-6): grp["QUER"].append(s) if bb[0] > 0 and bb[3] < L else grp["BODEN"].append(s)
    elif abs(bb[1] - bb[4]) < 1e-6 and abs(bb[1] - yi) < 1e-6 and (bb[0] >= 0): grp["RAHMEN"].append(s); grp["INNEN"].append(s)
    else: grp["RAHMEN"].append(s)
    if abs(bb[1] - yo) < 1e-6 and abs(bb[4] - yo) < 1e-6: grp["AUSSEN"].append(s)
# Bodenstreifenstücke zwischen Querträgern fehlen nicht (Streifen y>yi) – Querträger liegen über dem Boden (z>zb)
gmsh.model.occ.synchronize()
xmid = xp
f = gmsh.model.mesh.field
f.add("MathEval", 1); f.setString(1, "F", f"{hn}+({HF}-{hn})*Min(1,Max(0,(Sqrt((x-{xmid})^2+0.25*y^2)-110)/250))")
f.add("Box", 2); f.setNumber(2, "VIn", hk); f.setNumber(2, "VOut", 1000); f.setNumber(2, "XMin", xmid - 110); f.setNumber(2, "XMax", xmid + 110)
f.setNumber(2, "YMin", yo - 1); f.setNumber(2, "YMax", ym + 2); f.setNumber(2, "ZMin", -1); f.setNumber(2, "ZMax", h + 1); f.setNumber(2, "Thickness", 40)
f.add("Min", 3); f.setNumbers(3, "FieldsList", [1, 2]); f.setAsBackgroundMesh(3)
gmsh.option.setNumber("Mesh.MeshSizeExtendFromBoundary", 0); gmsh.option.setNumber("Mesh.MeshSizeFromPoints", 0); gmsh.option.setNumber("Mesh.MeshSizeFromCurvature", 0)
gmsh.option.setNumber("Mesh.Algorithm", 8); gmsh.option.setNumber("Mesh.RecombineAll", 1); gmsh.option.setNumber("Mesh.RecombinationAlgorithm", 1)
gmsh.option.setNumber("Mesh.ElementOrder", 1)
gmsh.model.mesh.generate(2)
ntags, ncoord, _ = gmsh.model.mesh.getNodes(); ncoord = ncoord.reshape(-1, 3); node = {int(t): c for t, c in zip(ntags, ncoord)}
# ---- Elemente je Fläche
elems = {"S8R": [], "S6": []}; eg = {}   # eid -> (typ, nodes, gruppe)
eid = 0; byg = {k: [] for k in grp}; sect = {}
def gname(s):
    if s in grp["BODEN"]: return "BODEN"
    if s in grp["QUER"]: return "QUER"
    if s in grp["KNAUT"]: return "KNAUT"
    return "RAHMEN"
for (_, s) in gmsh.model.getEntities(2):
    types, etags, enodes = gmsh.model.mesh.getElements(2, s)
    for ty, et, en in zip(types, etags, enodes):
        npn = {3: 4, 2: 3}.get(ty)
        if ty not in (3, 2): raise SystemExit(f"Elementtyp {ty} nicht erwartet")
        en = np.array(en, dtype=int).reshape(-1, npn)
        for row in en:
            eid += 1; tname = "S8R" if ty == 3 else "S6"; elems[tname].append((eid, [int(x) for x in row])); eg[eid] = gname(s)
            if s in grp["AUSSEN"]: byg["AUSSEN"].append((eid, [int(x) for x in row], tname))
            if s in grp["INNEN"]: byg["INNEN"].append((eid, [int(x) for x in row], tname))
gmsh.finalize()
used = sorted({n for t in elems for _, nn in elems[t] for n in nn}); 

# ---------------- Deck (Radioss). Annahmen Herkunft ERW-X1 / ERW-X1b Nachtrag 1: 6082 T6 E 70 GPa, nu 0,33, Rp0,2 260 MPa, Rm 310 MPa bei 10 % PEEQ (bilinear, dann flach), Pfahl D254 starr 1500 kg, 5 kJ
mat = EI["werkstoff"]; E_GPa = mat["E_MPa"]["wert"] / 1e3; nu = mat["nu"]["wert"]; Rp02 = mat["Rp02_MPa"]["wert"] / 1e3; Rm = mat["Rm_MPa"]["wert"] / 1e3; Au = mat["Bruchdehnung"]["wert"]
RHO = float(os.environ.get("X2_RHO", 2.7e-6)); MP = 1500.0; EJ = float(os.environ.get("X2_E_J", 5000.0)); V0 = math.sqrt(2 * EJ / MP); TSTOP = float(os.environ.get("X2_TSTOP", 50.0))   # kg mm ms: v in mm/ms = m/s
b_h = (Rm - Rp02) / Au
yc = yo - TK / 2 - 0.5 - Rp          # Pfahlmitte y, Abstand 0,5 mm zur Aussenflaeche (wie ccx cl)
PARTS = {"KNAUT": (1, TK), "RAHMEN": (2, tw), "QUER": (3, qt), "BODEN": (4, bt)}
def fi(x): return f"{x:10d}"
shells = {g: [] for g in PARTS}
for t in ("S8R", "S6"):
    for i, nn in elems[t]: shells[eg[i]].append((i, nn))
nodes_g = {g: sorted({n for _, nn in shells[g] for n in nn}) for g in PARTS}
nfix_end = sorted(n for n in used if node[n][0] < 1e-6 or node[n][0] > L - 1e-6)
nfix_far = sorted(n for n in used if node[n][1] > YL - 1e-6)
NPOLE = 900000; nodes_inn = sorted(n for n in ninn_ for n in [n]) if False else None
innset = sorted(n for n in used if abs(node[n][1] - yi) < 1e-3 and abs(node[n][0] - xp) < 500 and not any(x0 - V["quertraeger_spiel_mm"] - 0.01 <= node[n][0] <= x0 + qb + V["quertraeger_spiel_mm"] + 0.01 for x0 in qx))   # Innenwand-Knoten (Zellberuehrung)
slave = sorted(set(nodes_g["KNAUT"]) | set(nodes_g["RAHMEN"]))
def lst(ids, per=10):
    return "\n".join("".join(f"{x:10d}" for x in ids[i:i + per]) for i in range(0, len(ids), per))
rad = []; w = rad.append
w("#RADIOSS STARTER\n/BEGIN\nX2                                                                              \n      2019         0\n                  kg                  mm                  ms\n                  kg                  mm                  ms")
w("/TITLE\nKI-generiert (Claude Sonnet) Entwurf X1b/X2 Knautschzone " + f"{var} w={wk:g}")
w("/NODE")
for n in used: w(f"{n:10d}{node[n][0]:20.8g}{node[n][1]:20.8g}{node[n][2]:20.8g}")
w(f"{NPOLE:10d}{xp:20.8g}{yc:20.8g}{-50.0:20.8g}")
w(f"/MAT/PLAS_JOHNS/1\nAl6082T6_bilinear\n#              RHO_I\n{RHO:20.8g}{0:20d}\n#                  E                  Nu     Iflag\n{E_GPa:20.8g}{nu:20.8g}{0:10d}\n#                  a                   b                   n           EPS_p_max            SIG_max0\n{Rp02:20.8g}{b_h:20.8g}{1.0:20.8g}{0:20d}{Rm:20.8g}\n#                  c           EPS_DOT_0       ICC   Fsmooth               F_cut               Chard\n{0:20d}{0:20d}{0:10d}{0:10d}{0:20d}{0:20d}\n#                  m              T_melt              rhoC_p                 T_r\n{0:20d}{0:20d}{0:20d}{0:20d}")
for g, (pid, th) in PARTS.items():
    w(f"/PROP/TYPE1/{pid}\n{g}\n#   Ishell    Ismstr     Ish3n    Idrill                            P_thick_fail\n        24         4         2         0                                       0\n#                 hm                  hf                  hr                  dm                  dn\n{0:20d}{0:20d}{0:20d}{0:20d}{0:20d}\n#        N   Istrain               Thick              Ashear              Ithick     Iplas\n         5         1{th:20.8g}{0:20d}{1:20d}{1:10d}")
    w(f"/PART/{pid}\n{g}\n{pid:10d}{1:10d}{0:10d}")
for g, (pid, th) in PARTS.items():
    w(f"/SHELL/{pid}")
    for i, nn in shells[g]:
        nn4 = nn if len(nn) == 4 else nn + [nn[-1]]
        w(f"{i:10d}{pid:10d}" + "".join(f"{x:10d}" for x in nn4[:4]) if False else f"{i:10d}" + "".join(f"{x:10d}" for x in nn4))
w("/GRNOD/NODE/1\nrandbedingung_enden\n" + lst(sorted(set(nfix_end) | set(nfix_far)))); w("/BCS/1\nfest\n#  Tra rot   skew_ID  grnod_ID\n   111 111         0         1")
w("/GRNOD/NODE/2\nkontaktknoten_knaut_rahmen\n" + lst(slave))
w(f"/RWALL/CYL/{NPOLE}\nPfahl_D254_1500kg\n#  node_ID     Slide grnod_ID1 grnod_ID2\n{NPOLE:10d}{0:10d}{2:10d}{0:10d}\n#           D_search                fric            Diameter                ffac       ifq\n{0:20d}{0:20d}{2 * Rp:20.8g}{0:20d}{0:10d}\n#               Mass                VX_0                VY_0                VZ_0\n{MP:20.8g}{0:20d}{V0:20.8g}{0:20d}\n#               X_M1                Y_M1                Z_M1\n{xp:20.8g}{yc:20.8g}{h + 50.0:20.8g}")
w("/GRNOD/NODE/3\nselbstkontakt_knaut\n" + lst(nodes_g["KNAUT"])); w("/SURF/PART/4\nknaut\n         1")
GM = float(os.environ.get("X2_GAP", 1.0))
w(f"/INTER/TYPE7/1\nselbstkontakt_knaut\n#  Slav_id   Mast_id      Istf      Ithe      Igap                Ibag      Idel     Icurv      Iadm\n{3:10d}{4:10d}{0:10d}{0:10d}{0:10d}{0:20d}{0:10d}{0:10d}{0:10d}\n#          Fscalegap             Gap_max             Fpenmax\n{0:20d}{0:20d}{0:20d}\n#              Stmin               Stmax          %mesh_size               dtmin  Irem_gap   Irem_i2\n{0:20d}{0:20d}{0:20d}{0:20d}{0:10d}{0:10d}\n#              Stfac                Fric              Gapmin              Tstart               Tstop\n{0:20d}{0:20d}{GM:20.8g}{0:20d}{0:20d}\n#      IBC                        Inacti                VisS                VisF              Bumult\n       000{0:30d}{0:20d}{0:20d}{0:20d}\n#    Ifric    Ifiltr               Xfreq     Iform   sens_ID   fct_IDf             AscaleF   fric_ID\n{0:10d}{0:10d}{0:20d}{0:10d}{0:10d}{0:10d}{0:20d}{0:10d}")
w("/GRNOD/NODE/9\ninnenwand\n" + lst(innset))
w(f"/TH/RWALL/1\nrwall\nDEF\n{NPOLE:10d}")
inn_mid = min(innset, key=lambda n: (node[n][0] - xp) ** 2 + (node[n][2] - h / 2) ** 2)   # Innenwandknoten naechst Pfahlmitte, halbe Hoehe
w(f"/TH/NODE/2\ninnenwand_mitte\nDEF\n{inn_mid:10d}")
w(f"/TH/NODE/3\npfahlknoten\nDEF\n{NPOLE:10d}")
w("/END")
(T / "X2_0000.rad").write_text("\n".join(rad) + "\n")
NSEG = int(os.environ.get("X2_NSEG", 10))   # Wiederaufsetzpunkte: Lauf in NSEG Abschnitte; jeder Abschnitt endet normal und schreibt X2_<k>_0001.rst (die /RFILE-Zwischendateien I/J sind in dieser Version nicht lesbar: Segfault)
for k in range(1, NSEG + 1):
    eng = f"""/RUN/X2/{k}
{TSTOP * k / NSEG:20.8g}
/ANIM/DT
0.0 {TSTOP / 100:.6g}
/ANIM/GZIP
/ANIM/VECT/DISP
/ANIM/ELEM/EPSP
/TFILE/4
0.05
/PRINT/-1/50
/DT
0.9 0.0
/PARITH/ON
"""
    (T / f"X2_{k:04d}.rad").write_text(eng)
json.dump({"var": var, "w": wk, "xp": xp, "yc": yc, "Rp": Rp, "v0_mm_ms": V0, "M_kg": MP, "E_J": EJ, "tstop_ms": TSTOP, "nseg": NSEG, "h": h, "L": L, "n_knoten": len(used), "n_schalen": eid, "innen_knoten": len(innset), "yo": yo, "ym": ym, "NPOLE": NPOLE, "quer_x0": qx, "qb": qb, "herkunft": "x2.py, Annahmen ERW-X1b Nachtrag 1"}, open(T / "modell.json", "w"))
print("Deck", T, "Knoten", len(used), "Schalen", eid, "v0", V0)
