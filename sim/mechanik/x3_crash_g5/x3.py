#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-20; Nachtrag 4 verworfen (Nachtrag 5, 2026-11-23): Istf=4/Inacti=6 und /DT/NODA/CST machten Fall b instabiler (Kollaps bei 0,535 ms), Deck wieder wie vor Nachtrag 4, siehe ERWARTUNG.md; Nachtrag 3 2026-11-21: LFP-Zellreihen als 4 homogene Blöcke zwischen den Querträgerlücken, siehe ERWARTUNG.md), Entwurf. Auftrag X3 (sim/AUFTRAG_K3_X3.md, ERWARTUNG.md). Pack G5 (Rahmen, Querträger, Boden, Deckel, Unterfahrschutz, Kühlplatten als Schalen; Zellreihen als Volumen) -> OpenCourant-Deck.
Einheiten mm, ms, kg (kN, GPa, J). Aufruf: x3.py <LFP> [lastfall=a] ; Umgebung: X3_HN (Schalenmass nah, 12), X3_HF (fern, 40), X3_HY (Zelle y-Teilung, 20), X3_NSEG (10), X3_TSTOP (50 ms), X3_E_J (5000), X3_TAG (Ordnername), X3_RZ_GAP.
Alle Maße aus eingaben.json (mit Herkunft je Wert). Ausgabe lauf/<V>_<lf>[_TAG]/{X3_0000.rad, X3_000k.rad, modell.json}"""
import sys, json, math, os
from pathlib import Path
import numpy as np, gmsh
D = Path(__file__).resolve().parent
var = sys.argv[1] if len(sys.argv) > 1 else "LFP"; lf = sys.argv[2] if len(sys.argv) > 2 else "a"   # Lastfaelle: a (5 kJ), a2 (20 kJ), a_s10 / a_s40 (Zellfliessgrenze 10/40 MPa), b (Quetschplatte)
EI = json.load(open(D / "eingaben.json")); EV = EI.get(var, {}) if var != "LFP" else {}; g = lambda k: (EV[k] if k in EV else EI[k])["wert"]
LFB = lf[0]
HN = float(os.environ.get("X3_HN", 12)); HF = float(os.environ.get("X3_HF", 40)); HY = float(os.environ.get("X3_HY", 20)); NZ = int(os.environ.get("X3_NZ", 3))
TAG = os.environ.get("X3_TAG", ""); T = D / "lauf" / f"{var}_{lf}{TAG}"; T.mkdir(parents=True, exist_ok=True)
L, B = g("L_mm"), g("B_mm"); t = g("rahmen_wand_mm"); nk = int(g("rahmen_kammern")); z0, z1 = g("rahmen_z_mm"); rand = g("rand_mm")
tb, td, tu, tp, tq = g("boden_mm"), g("deckel_mm"), g("ufs_mm"), g("kuehlplatte_ersatz_mm"), g("quertraeger_wand_mm")
qx = g("quertraeger_x0_mm"); qb = g("quertraeger_breite_mm"); qz = g("quertraeger_z_mm"); zp = g("kuehlplatte_z_mm")
cz0, cz1 = g("zelle_z_mm")
if var == "LFP":   # Nachtrag 3 (2026-11-21): Reihen zwischen den Querträgerlücken (Sprung > 20 mm) zu 4 homogenen Blöcken; fg = Summe Reihendicken / Blockbreite; nx = round(Breite/15)
    _d = g("zelle_dicke_mm"); _xs = sorted(g("zellreihen_x0_mm")); _grp = [[_xs[0]]]
    for _a, _b in zip(_xs, _xs[1:]): (_grp.append([_b]) if _b - _a > 20 else _grp[-1].append(_b))
    BLK = [(gr[0], gr[-1] + _d, g("zelle_y_mm")[0], g("zelle_y_mm")[1], len(gr) * _d / (gr[-1] + _d - gr[0])) for gr in _grp]; cdx = None; NXZ = 15.0
else: BLK = [tuple(b) for b in g("zellbloecke")]; cdx = None; NXZ = HY
cy0 = min(b[2] for b in BLK); cy1 = max(b[3] for b in BLK)
hk = (z1 - z0 - (nk + 1) * t) / nk
Rp = g("pfahl_d_mm") / 2; MP = g("pfahl_masse_kg"); EJ = float(os.environ.get("X3_E_J", g("pfahl_energie_a2_J") if lf == "a2" else g("pfahl_energie_J"))); V0 = math.sqrt(2 * EJ / MP)
TSTOP = float(os.environ.get("X3_TSTOP", 50.0)); NSEG = int(os.environ.get("X3_NSEG", 10))
xp = L / 2; ym = t / 2; yi = rand - t / 2   # Mittelflaeche Aussenwand / Innenwand
RHO = g("rho_Al_kg_mm3"); E_GPa = g("E_MPa") / 1e3; nu = g("nu"); Rp02 = g("Rp02_MPa") / 1e3; Rm = g("Rm_MPa") / 1e3; Au = g("Bruchdehnung"); b_h = (Rm - Rp02) / Au
# ---------------- Schalengeometrie (alle Flaechen, dann fragment => konforme Knoten)
gmsh.initialize(); gmsh.option.setNumber("General.Terminal", 0); gmsh.model.add("x3"); oc = gmsh.model.occ
def quad(p0, p1, p2, p3):
    ps = [oc.addPoint(*p) for p in (p0, p1, p2, p3)]; ls = [oc.addLine(ps[i], ps[(i + 1) % 4]) for i in range(4)]
    return oc.addPlaneSurface([oc.addCurveLoop(ls)])
surf = []   # (tag, gruppe)
def add(s, grp): surf.append((s, grp))
yL = B - ym; yR = B - yi   # Mittelflaechen rechts: aussen B-ym, innen B-yi ... (yi von links gespiegelt)
for (ya, yb) in ((ym, yi), (B - yi, B - ym)):                     # Laengsprofile links/rechts: Aussen-, Innenwand, Stege
    for y in (ya, yb): add(quad((0, y, z0), (L, y, z0), (L, y, z1), (0, y, z1)), "RAHMEN")
    for i in range(1, nk): zz = z0 + t + i * (hk + t) - t / 2; add(quad((0, ya, zz), (L, ya, zz), (L, yb, zz), (0, yb, zz)), "RAHMEN")
for (xa, xb) in ((ym, yi), (L - yi, L - ym)):                      # Querprofile vorn/hinten (zwischen den Innenwaenden der Laengsprofile)
    for x in (xa, xb): add(quad((x, yi, z0), (x, B - yi, z0), (x, B - yi, z1), (x, yi, z1)), "RAHMEN")
    for i in range(1, nk): zz = z0 + t + i * (hk + t) - t / 2; add(quad((xa, yi, zz), (xb, yi, zz), (xb, B - yi, zz), (xa, B - yi, zz)), "RAHMEN")
for x0 in qx:                                                       # Querträger: Kasten 26 x 54, Wand 2,5, zwischen den Innenwaenden
    xa, xb = x0 + tq / 2, x0 + qb - tq / 2; za, zz = qz[0] + tq / 2, qz[1] - tq / 2
    for x in (xa, xb): add(quad((x, yi, za), (x, B - yi, za), (x, B - yi, zz), (x, yi, zz)), "QUER")
    for z in (za, zz): add(quad((xa, yi, z), (xb, yi, z), (xb, B - yi, z), (xa, B - yi, z)), "QUER")
for z in zp: add(quad((yi, yi, z), (L - yi, yi, z), (L - yi, B - yi, z), (yi, B - yi, z)), "PLATTE")   # Kuehlplatten (Ersatzschale)
add(quad((0, 0, z0), (L, 0, z0), (L, B, z0), (0, B, z0)), "BODEN")                                      # Boden in der Ebene der Rahmenunterkante
add(quad((0, 0, z1), (L, 0, z1), (L, B, z1), (0, B, z1)), "DECKEL")                                     # Deckel in der Ebene der Rahmenoberkante
zu = tu / 2; hh = g("ufs_huelse_mm") / 2
add(quad((0, 0, zu), (L, 0, zu), (L, B, zu), (0, B, zu)), "UFS")
nb = int(g("befestigung_n_je_seite")); rx = g("befestigung_rand_x_mm"); bxy = [(rx + i * (L - 2 * rx) / (nb - 1), y) for y in (rand / 2, B - rand / 2) for i in range(nb)]
for (x, y) in bxy:                                                                                      # Huelsen Unterfahrschutz-Boden als Vierkantrohr (Modellvereinfachung)
    for (a, b_, c, d) in (((x - hh, y - hh), (x + hh, y - hh), None, None), ((x + hh, y - hh), (x + hh, y + hh), None, None), ((x + hh, y + hh), (x - hh, y + hh), None, None), ((x - hh, y + hh), (x - hh, y - hh), None, None)):
        add(quad((a[0], a[1], zu), (b_[0], b_[1], zu), (b_[0], b_[1], z0), (a[0], a[1], z0)), "HUELSE")
oc.synchronize()
allf = [(2, s) for s, _ in surf]; res, outmap = oc.fragment(allf, []); oc.synchronize()
gname = {}
for (s, grp_), om in zip(surf, outmap):
    for (_, nt) in om: gname.setdefault(nt, grp_)
f = gmsh.model.mesh.field
f.add("MathEval", 1); f.setString(1, "F", f"{HN}+({HF}-{HN})*Min(1,Max(0,(Sqrt((x-{xp})^2+0.25*y^2)-150)/300))"); f.setAsBackgroundMesh(1)
for k_, v_ in (("MeshSizeExtendFromBoundary", 0), ("MeshSizeFromPoints", 0), ("MeshSizeFromCurvature", 0), ("Algorithm", 8), ("RecombineAll", 1), ("RecombinationAlgorithm", 1), ("ElementOrder", 1)): gmsh.option.setNumber("Mesh." + k_, v_)
gmsh.model.mesh.generate(2)
ntags, ncoord, _ = gmsh.model.mesh.getNodes(); ncoord = ncoord.reshape(-1, 3); node = {int(a): c for a, c in zip(ntags, ncoord)}
shells = {}; eid = 0
for (_, s) in gmsh.model.getEntities(2):
    grp_ = gname.get(s, "RAHMEN"); types, etags, enodes = gmsh.model.mesh.getElements(2, s)
    for ty, et, en in zip(types, etags, enodes):
        if ty not in (2, 3): raise SystemExit(f"Elementtyp {ty}")
        npn = 4 if ty == 3 else 3
        for row in np.array(en, dtype=int).reshape(-1, npn):
            eid += 1; nn = [int(x) for x in row] + ([int(row[-1])] if npn == 3 else [])
            cxy = np.mean([node[n] for n in nn], axis=0); grp2 = grp_
            if grp_ in ("BODEN", "DECKEL") and (cxy[0] < yi or cxy[0] > L - yi or cxy[1] < yi or cxy[1] > B - yi): grp2 += "_RAND"
            shells.setdefault(grp2, []).append((eid, nn))
gmsh.finalize()
usedS = sorted({n for g_ in shells.values() for _, nn in g_ for n in nn})
# ---------------- Zellreihen (Hex-Volumen)
cnode = {}; bricks = []; NID = 400000; BID = 400000; cnodes_all = []; blkinfo = []
for (bx0, bx1, by0, by1, fg) in BLK:
    nx = max(1, int(round((bx1 - bx0) / NXZ))); ny = max(2, int(round((by1 - by0) / HY)))
    ids = np.zeros((nx + 1, ny + 1, NZ + 1), dtype=int)
    for i in range(nx + 1):
        for j in range(ny + 1):
            for k in range(NZ + 1):
                NID += 1; ids[i, j, k] = NID; cnode[NID] = (bx0 + i * (bx1 - bx0) / nx, by0 + j * (by1 - by0) / ny, cz0 + k * (cz1 - cz0) / NZ)
    for i in range(nx):
        for j in range(ny):
            for k in range(NZ):
                n = [ids[i, j, k], ids[i + 1, j, k], ids[i + 1, j + 1, k], ids[i, j + 1, k], ids[i, j, k + 1], ids[i + 1, j, k + 1], ids[i + 1, j + 1, k + 1], ids[i, j + 1, k + 1]]
                BID += 1; bricks.append((BID, [int(x) for x in n]))
cnodes_all = sorted(cnode)
Zv = sum((b[1] - b[0]) * (b[3] - b[2]) for b in BLK) * (cz1 - cz0); FG = sum((b[1] - b[0]) * (b[3] - b[2]) * b[4] for b in BLK) / sum((b[1] - b[0]) * (b[3] - b[2]) for b in BLK); RHO_Z = g("zellmasse_gesamt_kg") / Zv   # Dichte aus Masse CAD / Hüllvolumen
NUZ = g("zelle_nu")
SENS = {"a_s10": 0.010, "a_s40": 0.040}
EZ = float(os.environ.get("X3_ZE_GPA", g("zelle_E_GPa"))) * FG; SZ = float(os.environ.get("X3_ZS_GPA", SENS.get(lf, g("zelle_fliess_GPa")))) * FG   # NMC: homogener Block, E und Fliessgrenze x Fuellgrad (Nachtrag 1 Punkt 5); NUZ = g("zelle_nu")
# ---------------- Deck
PARTS = {"RAHMEN": (1, t), "QUER": (2, tq), "BODEN": (3, tb), "BODEN_RAND": (4, tb + t), "DECKEL": (5, td), "DECKEL_RAND": (6, td + t), "UFS": (7, tu), "HUELSE": (8, tu), "PLATTE": (9, tp)}
PZ = 10
def lst(ids, per=10): return "\n".join("".join(f"{x:10d}" for x in ids[i:i + per]) for i in range(0, len(ids), per))
def matcard(i, name, rho, E, nu_, sy, b, n, smax):
    return (f"/MAT/PLAS_JOHNS/{i}\n{name}\n#              RHO_I\n{rho:20.8g}{0:20d}\n#                  E                  Nu     Iflag\n{E:20.8g}{nu_:20.8g}{0:10d}\n#                  a                   b                   n           EPS_p_max            SIG_max0\n"
            f"{sy:20.8g}{b:20.8g}{n:20.8g}{0:20d}{smax:20.8g}\n#                  c           EPS_DOT_0       ICC   Fsmooth               F_cut               Chard\n{0:20d}{0:20d}{0:10d}{0:10d}{0:20d}{0:20d}\n#                  m              T_melt              rhoC_p                 T_r\n{0:20d}{0:20d}{0:20d}{0:20d}")
NPOLE = 900000; yc = -0.5 - Rp - t / 2 + t / 2   # Pfahlfläche 0,5 mm vor der Aussenfläche der Aussenwand (y = 0); Kontakt an der Mittelfläche (y = t/2)
yc = -0.5 - Rp
rad = []; w = rad.append
w("#RADIOSS STARTER\n/BEGIN\nX3                                                                              \n      2019         0\n                  kg                  mm                  ms\n                  kg                  mm                  ms")
w(f"/TITLE\nKI-generiert (Claude Sonnet) Entwurf X3 Crash G5 {var} Lastfall {lf}")
w("/NODE")
for n in usedS: w(f"{n:10d}{node[n][0]:20.8g}{node[n][1]:20.8g}{node[n][2]:20.8g}")
for n in cnodes_all: w(f"{n:10d}{cnode[n][0]:20.8g}{cnode[n][1]:20.8g}{cnode[n][2]:20.8g}")
if LFB == "b":
    QP = g("quetschplatte"); Rq = QP["halbzylinder_R_mm"]; VB = QP["geschw_mm_ms"]; dxq = 2 * Rq + QP["abstand_mm"]; NPOLES = [NPOLE + i for i in range(QP["anzahl"])]; xs = [xp + (i - (QP["anzahl"] - 1) / 2) * dxq for i in range(QP["anzahl"])]; yc = -0.5 - Rq
    for npn, xq in zip(NPOLES, xs): w(f"{npn:10d}{xq:20.8g}{yc:20.8g}{-50.0:20.8g}")
else: w(f"{NPOLE:10d}{xp:20.8g}{yc:20.8g}{-50.0:20.8g}")
w(matcard(1, "Al6082T6_bilinear", RHO, E_GPa, nu, Rp02, b_h, 1.0, Rm))
w(matcard(2, "Zellblock_Platzhalter", RHO_Z, EZ, NUZ, SZ, 0.0, 1.0, SZ))
for gname_, (pid, th) in PARTS.items():
    w(f"/PROP/TYPE1/{pid}\n{gname_}\n#   Ishell    Ismstr     Ish3n    Idrill                            P_thick_fail\n        24         4         2         0                                       0\n#                 hm                  hf                  hr                  dm                  dn\n{0:20d}{0:20d}{0:20d}{0:20d}{0:20d}\n#        N   Istrain               Thick              Ashear              Ithick     Iplas\n         5         1{th:20.8g}{0:20d}{1:20d}{1:10d}")
    w(f"/PART/{pid}\n{gname_}\n{pid:10d}{1:10d}{0:10d}")
w(f"/PROP/TYPE14/{PZ}\nZellblock\n#   Isolid    Ismstr               Icpre     Inpts Itetra4 Itetra10      Imas    Iframe\n        24         0                   0         0         0         0         0         1\n#                 qa                  qb                   h\n{0:20d}{0:20d}{0.1:20.8g}\n#           LAMBDA_V                MU_V                  dn\n{0:20d}{0:20d}{0:20d}\n#             dt_min\n{0:20d}")
w(f"/PART/{PZ}\nZellblock\n{PZ:10d}{2:10d}{0:10d}")
for gname_, (pid, th) in PARTS.items():
    if gname_ not in shells: continue
    w(f"/SHELL/{pid}")
    for i, nn in shells[gname_]: w(f"{i:10d}" + "".join(f"{x:10d}" for x in nn))
w(f"/BRICK/{PZ}")
for i, nn in bricks: w(f"{i:10d}" + "".join(f"{x:10d}" for x in nn))
if g("lager") == "huelsen" and os.environ.get("X3_LAGER", "") != "gegenseite":
    hs = {n for _, nn in shells["HUELSE"] for n in nn}; fix = sorted(n for n in hs if abs(node[n][2] - zu) < 1e-6)   # Nachtrag 1 Punkt 1: nur die 12 Huelsen, unteres Ende (Fahrzeugseite)
else: fix = sorted(n for n in usedS if node[n][1] > B - ym - 1e-6)
w("/GRNOD/NODE/1\nrandbedingung_gegenseite\n" + lst(fix)); w("/BCS/1\nfest\n#  Tra rot   skew_ID  grnod_ID\n   111 111         0         1")
near = sorted(n for n in usedS if node[n][1] < 450)
w("/GRNOD/NODE/2\nkontaktknoten_pfahl\n" + lst(near))
if LFB == "b":
    for i, (npn, xq) in enumerate(zip(NPOLES, xs)):
        w(f"/RWALL/CYL/{npn}\nQuetschzylinder_{i + 1}_R75\n#  node_ID     Slide grnod_ID1 grnod_ID2\n{npn:10d}{0:10d}{2:10d}{0:10d}\n#           D_search                fric            Diameter                ffac       ifq\n{0:20d}{0:20d}{2 * Rq:20.8g}{0:20d}{0:10d}\n#               Mass                VX_0                VY_0                VZ_0\n{0:20d}{0:20d}{VB:20.8g}{0:20d}\n#               X_M1                Y_M1                Z_M1\n{xq:20.8g}{yc:20.8g}{z1 + 100.0:20.8g}")
else:
    NPOLES = [NPOLE]; w(f"/RWALL/CYL/{NPOLE}\nPfahl_D254_1500kg\n#  node_ID     Slide grnod_ID1 grnod_ID2\n{NPOLE:10d}{0:10d}{2:10d}{0:10d}\n#           D_search                fric            Diameter                ffac       ifq\n{0:20d}{0:20d}{2 * Rp:20.8g}{0:20d}{0:10d}\n#               Mass                VX_0                VY_0                VZ_0\n{MP:20.8g}{0:20d}{V0:20.8g}{0:20d}\n#               X_M1                Y_M1                Z_M1\n{xp:20.8g}{yc:20.8g}{z1 + 100.0:20.8g}")
shell_pids = [pid for gname_, (pid, _) in PARTS.items() if gname_ in shells]
w("/GRNOD/NODE/3\nzellknoten\n" + lst(cnodes_all)); w("/GRNOD/NODE/4\nrahmen_innen_nahe_pfahl\n" + lst(sorted(n for n in usedS if node[n][1] < 450 and abs(node[n][0] - xp) < 600)))
w("/SURF/PART/1\nschalen\n" + lst(shell_pids))   # Flaeche aus Solid-Part (SURF/PART) liefert Fehler 1104 in dieser Version: nur Zellknoten gegen Schalen
GM = float(os.environ.get("X3_GAP", 1.0))
ISTF, INACTI = 0, 0   # Nachtrag 4 verworfen (Nachtrag 5): Werte 0 wie in allen Faellen a
def t7(i, name, sl, ma):
    return (f"/INTER/TYPE7/{i}\n{name}\n#  Slav_id   Mast_id      Istf      Ithe      Igap                Ibag      Idel     Icurv      Iadm\n{sl:10d}{ma:10d}{ISTF:10d}{0:10d}{0:10d}{0:20d}{0:10d}{0:10d}{0:10d}\n#          Fscalegap             Gap_max             Fpenmax\n{0:20d}{0:20d}{0:20d}\n#              Stmin               Stmax          %mesh_size               dtmin  Irem_gap   Irem_i2\n{0:20d}{0:20d}{0:20d}{0:20d}{0:10d}{0:10d}\n#              Stfac                Fric              Gapmin              Tstart               Tstop\n{0:20d}{0:20d}{GM:20.8g}{0:20d}{0:20d}\n#      IBC                        Inacti                VisS                VisF              Bumult\n       000{INACTI:30d}{0:20d}{0:20d}{0:20d}\n#    Ifric    Ifiltr               Xfreq     Iform   sens_ID   fct_IDf             AscaleF   fric_ID\n{0:10d}{0:10d}{0:20d}{0:10d}{0:10d}{0:10d}{0:20d}{0:10d}")
w(t7(1, "zellknoten_gegen_schalen", 3, 1))
dnode = lambda xx, yy, zz, src: min(src, key=lambda n: (node[n][0] - xx) ** 2 + (node[n][1] - yy) ** 2 + (node[n][2] - zz) ** 2)
n_in = dnode(xp, yi, (z0 + z1) / 2, usedS)
rows_near = min((b[0] for b in BLK), key=lambda x: abs(x - xp)); jn = [n for n in cnodes_all if abs(cnode[n][1] - cy0) < 1e-6 and abs(cnode[n][0] - xp) < 600]
n_cell = min(jn, key=lambda n: (cnode[n][0] - xp) ** 2 + (cnode[n][2] - (cz0 + cz1) / 2) ** 2)
for i, npn in enumerate(NPOLES): w(f"/TH/RWALL/{i + 1}\nrwall\nDEF\n{npn:10d}")
w(f"/TH/NODE/12\ninnenwand_mitte\nDEF\n{n_in:10d}"); w(f"/TH/NODE/13\npfahlknoten\nDEF\n{NPOLE:10d}"); w(f"/TH/NODE/14\nzellblock_vorderseite\nDEF\n{n_cell:10d}")
w("/END")
(T / "X3_0000.rad").write_text("\n".join(rad) + "\n")
for k in range(1, NSEG + 1):
    eng = f"/RUN/X3/{k}\n{TSTOP * k / NSEG:20.8g}\n/ANIM/DT\n0.0 {TSTOP / float(os.environ.get('X3_NANIM', 50)):.6g}\n/ANIM/GZIP\n/ANIM/VECT/DISP\n/ANIM/ELEM/EPSP\n/TFILE/4\n0.05\n/PRINT/-1/50\n/DT\n0.9 0.0\n/PARITH/ON\n"
    (T / f"X3_{k:04d}.rad").write_text(eng)
json.dump({"var": var, "lastfall": lf, "xp": xp, "yc": yc, "Rp": Rp, "v0_mm_ms": V0, "M_kg": MP, "E_J": EJ, "tstop_ms": TSTOP, "nseg": NSEG, "L": L, "B": B, "z0": z0, "z1": z1, "n_knoten_schale": len(usedS), "n_schalen": eid, "n_bricks": len(bricks),
           "n_zellknoten": len(cnodes_all), "NPOLE": NPOLE, "cy0": cy0, "cy1": cy1, "zeile_zelle_x": rows_near, "knoten_innenwand": n_in, "knoten_zelle": n_cell, "rho_zelle": RHO_Z, "zelle_E_GPa": EZ, "fuellgrad": FG, "lastfall_art": LFB, "nrwall": len(NPOLES), "geschw_b_mm_ms": (g("quetschplatte")["geschw_mm_ms"] if LFB == "b" else None), "zelle_fliess_GPa": SZ, "hn": HN, "hf": HF, "hy": HY, "herkunft": "x3.py, eingaben.json"}, open(T / "modell.json", "w"))
print("Deck", T, "Schalenknoten", len(usedS), "Schalen", eid, "Bricks", len(bricks), "v0", round(V0, 3))
