# KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. Auftrag G4 (cad/pack/AUFTRAG.md).
"""Pack-CAD (vereinfacht) in FreeCAD headless. Aufruf: PACK_VARIANTE=LFP|NMC [PACK_PARAMETER=datei] $FREECAD_APPIMAGE freecadcmd cad/pack/pack.py
Maße nur aus cad/pack/entwurf/parameter_<V>.json (Akten + Block A). Zellen = Hüllkörper (kein Zelldetail, keine Pole).
Koordinaten mm: X Länge, Y Breite, Z Höhe (0 = Unterkante Unterfahrschutz). Ausgabe: ergebnis_<V>.json, pack_<V>.FCStd/.step, netz_<V>*.json."""
import os, sys, json, math, time
import numpy as np
import FreeCAD, Part
from FreeCAD import Vector as V

VAR = os.environ["PACK_VARIANTE"]
E2 = os.environ.get("PACK_E2") == "1"   # Schalter E2: Schaltbox usw. (Fall b) dazu; Ausgabe mit Suffix _e2, G4-Dateien bleiben unberührt
VO = VAR + ("_e2" if E2 else "")
ROOT = os.environ.get("BATTERIE", "/home/cae/hermes/batterie")
OUT = f"{ROOT}/cad/pack/entwurf"
PJ = json.load(open(os.environ.get("PACK_PARAMETER", f"{OUT}/parameter_{VAR}.json")))
P, A = PJ["parameter"], {k: v["wert"] for k, v in PJ["A"].items()}
def w(bt, m):
    x = P[bt][m]["wert"]
    if x is None: raise SystemExit(f"FEHLT {bt}/{m}")
    return float(x)
t0 = time.time()
B = w("BT-000", "bauraum_breite_mm"); rand = A["A_rand_mm"]; nq = int(A["A_quertraeger_anzahl"])
qb, qh, qw, sp = A["A_quertraeger_breite_mm"], A["A_quertraeger_hoehe_mm"], A["A_quertraeger_wand_mm"], A["A_quertraeger_spiel_mm"]
rho = A["A_alu_dichte_kg_m3"] * 1e-9  # kg/mm3
pad, kp, bod, dec, ufs, luft = (A[k] for k in ("A_pad_mm", "A_kuehlplatte_mm", "A_boden_mm", "A_deckel_mm", "A_unterfahrschutz_mm", "A_luft_mm"))
qlen = B - 2 * rand
teile = []   # (name, gruppe, shape, masse_kg oder None, material)
def add(name, grp, shp, mass=None, mat="Al"): teile.append(dict(name=name, grp=grp, shape=shp, mass=mass, mat=mat))
def box(x0, y0, z0, x1, y1, z1): return Part.makeBox(x1 - x0, y1 - y0, z1 - z0, V(x0, y0, z0))
def hohl_q(x, zc):  # Hohlprofil 26 (X) x 54 (Z), Wand 2,5, Länge Y
    a = box(x, rand, zc - qh / 2, x + qb, rand + qlen, zc + qh / 2)
    return a.cut(box(x + qw, rand - 1, zc - qh / 2 + qw, x + qb - qw, rand + qlen + 1, zc + qh / 2 - qw))

z_ku = ufs + luft + bod            # Oberkante Boden
z_cell0 = z_ku + kp + pad          # Zellunterkante
if VAR == "LFP":
    Lc, Bc, Dc = w("BT-100", "laenge_mm"), w("BT-100", "breite_mm"), w("BT-100", "dicke_mm")
    Hc = Bc; mcell = w("BT-100", "masse_g") / 1000; n = int(A["A_zellzahl_LFP"]); ab = A["A_zellabstand_LFP_mm"]
    nz = n // 2; pitch = Dc + ab
    Lg_calc = nz * Dc + (nz - 1) * ab + nq * (qb + 2 * sp) + 2 * rand
    Lg = w("BT-000", "bauraum_laenge_mm"); assert Lg >= Lg_calc, (Lg, Lg_calc)   # Gehäuse = Bauraum (ENT-102), Zellpaket mittig
    z_top_cell = z_cell0 + Hc; extra_top = 0.0
else:
    Dm, Hc = w("BT-100", "durchmesser_mm"), w("BT-100", "hoehe_mm"); mcell = w("BT-100", "masse_g") / 1000; n = int(A["A_zellzahl_NMC"])
    ab = A["A_zellabstand_NMC_mm"]; Lg = w("BT-000", "bauraum_laenge_mm")
    gv_b, gv_d = A["A_gruppenverbinder_NMC_mm"]; ag_d, ag_t = A["A_zellabgriff_NMC_mm"]
    z_top_cell = z_cell0 + Hc; extra_top = ag_t + gv_d   # Abgriff + Gruppenverbinder über der Zelle (Zusatzhöhe, weicht von M0 ab)
z_pad2 = z_top_cell + extra_top
z_ko = z_pad2 + pad; z_dk = z_ko + kp; z_top = z_dk + dec; H = z_top
zc_q = z_cell0 + Hc / 2

# ---- Gehäuse
add("Unterfahrschutz", "Unterfahrschutz", box(0, 0, 0, Lg, B, ufs), mat="Al")
add("Boden", "Boden", box(0, 0, ufs + luft, Lg, B, z_ku), mat="Al")
ring = box(0, 0, z_ku, Lg, B, z_dk).cut(box(rand, rand, z_ku - 1, Lg - rand, B - rand, z_dk + 1))
add("Seitenrahmen", "Seitenrahmen", ring, mat="Al (Vollprofil, Obergrenze)")
inner = lambda z0, z1: box(rand, rand, z0, Lg - rand, B - rand, z1)
add("Kuehlplatte_unten", "Kuehlplatte", inner(z_ku, z_ku + kp), mat="Al (Vollmaterial, Obergrenze)")
add("Pad_unten", "Pad", inner(z_ku + kp, z_cell0), mat="Pad", mass=None)
add("Pad_oben", "Pad", inner(z_pad2, z_ko), mat="Pad")
add("Kuehlplatte_oben", "Kuehlplatte", inner(z_ko, z_dk), mat="Al (Vollmaterial, Obergrenze)")
add("Deckel", "Deckel", box(0, 0, z_dk, Lg, B, z_top), mat="Al")

# ---- Zellen, Querträger, Verbinder
pos_q = []; cells = []   # cells: dict(name, shape, feld, cx, cy)
if VAR == "LFP":
    x = rand + (Lg - Lg_calc) / 2; grp = [nz // (nq + 1) + (1 if i < nz % (nq + 1) else 0) for i in range(nq + 1)]
    gz = 25.0; gt = 3.0
    zb0 = zc_q - gz / 2
    ci = 0
    for gi, g in enumerate(grp):
        for rr in range(2):
            y0 = rand + 4 + rr * Lc
            for k in range(g):
                xk = x + k * pitch
                cells.append(dict(name=f"Zelle_{ci:03d}", shape=box(xk, y0, z_cell0, xk + Dc, y0 + Lc, z_cell0 + Hc), feld=gi, cx=xk + Dc / 2, cy=y0 + Lc / 2, rr=rr)); ci += 1
            # Zellverbinder 25 x 3 am äußeren Zellende, je zwei Nachbarzellen (vereinfacht, ohne Polarität)
            yb = rand + 1 if rr == 0 else B - rand - 1 - gt
            for k in range(0, g, 2):
                xk = x + k * pitch; xe = x + min(k + 1, g - 1) * pitch + Dc
                add(f"Zellverbinder_g{gi}r{rr}_{k//2:02d}", "Zellverbinder", box(xk, yb, zc_q - gz / 2, xe, yb + gt, zc_q + gz / 2), mat="Al")
        x += g * pitch - ab + sp
        if gi < nq: pos_q.append(x); x += qb + sp
else:
    d = Dm; t = d + ab; rp = t * math.sqrt(3) / 2
    feld = (Lg - 2 * rand - nq * qb - nq * 2 * sp) / (nq + 1)
    Bi = B - 2 * rand; ng = int((Bi - d) // t) + 1
    nu = int((Bi - d - t / 2) // t) + 1; rows = int((feld - d) // rp) + 1
    je = n // (nq + 1); assert je * (nq + 1) == n
    x = rand; ci = 0
    for f in range(nq + 1):
        pl = []
        for r in range(rows):
            cnt = ng if r % 2 == 0 else nu; off = d / 2 + (0 if r % 2 == 0 else t / 2)
            for k in range(cnt): pl.append((r, x + d / 2 + r * rp, rand + off + k * t))
        # Zellen mittig im Feld: so viele Reihen wie nötig, Startreihe zentriert (sonst Schwerpunkt-Versatz, Erstlauf: ergebnis_NMC_erstbelegung_links.json)
        need = 0; cnt_ = 0
        while cnt_ < je: cnt_ += ng if need % 2 == 0 else nu; need += 1
        r0 = (rows - need) // 2
        pl = [q for q in pl if q[0] >= r0][:je]; assert len(pl) == je, (len(pl), je)
        for (r, cx, cy) in pl:
            cells.append(dict(name=f"Zelle_{ci:03d}", shape=Part.makeCylinder(d / 2, Hc, V(cx, cy, z_cell0)), feld=f, cx=cx, cy=cy, row=r)); ci += 1
            add(f"Abgriff_{ci-1:03d}", "Zellabgriff", Part.makeCylinder(ag_d / 2, ag_t, V(cx, cy, z_top_cell)), mat="Al")
        # Gruppenverbinder 25 x 3 (wie E1-Nachtrag): je Gruppe von 4 Zellen eine kurze Sammelschiene über den Abgriffen
        # (von Abgriffmitte zu Abgriffmitte +- Abgriffradius), dazu eine Reihenbrücke zur Nachbargruppe der Reihe (stößt an, Länge = Zellteilung - Abgriffdurchmesser)
        ra = ag_d / 2
        for r in ([] if E2 else sorted({p[0] for p in pl})):   # E2: Verbinder nach Mäander-Folge (unten), nicht nach G4
            sel = sorted([p for p in pl if p[0] == r], key=lambda q: q[2]); cx = sel[0][1]
            ch = [sel[k:k + 4] for k in range(0, len(sel), 4)]
            for gi_, gr in enumerate(ch):
                add(f"Gruppenverbinder_f{f}r{r}g{gi_}", "Gruppenverbinder", box(cx - gv_b / 2, gr[0][2] - ra, z_top_cell + ag_t, cx + gv_b / 2, gr[-1][2] + ra, z_top_cell + ag_t + gv_d), mat="Al (Annahme, Cu offen)")
                if gi_ < len(ch) - 1:
                    add(f"Gruppenbruecke_f{f}r{r}g{gi_}", "Gruppenbruecke", box(cx - gv_b / 2, gr[-1][2] + ra, z_top_cell + ag_t, cx + gv_b / 2, ch[gi_ + 1][0][2] - ra, z_top_cell + ag_t + gv_d), mat="Al (Annahme, Cu offen)")
        # Zellträger unten (Lochplatte), Verguss bis halbe Zellhöhe darüber (Lochkörper)
        tdk = A["A_traeger_dicke_NMC_mm"]; hv = A["A_vergusshoehe_anteil_NMC"] * Hc
        fc = [c for c in cells if c["feld"] == f]
        tool = Part.makeCompound([c["shape"] for c in fc])
        tr = box(x, rand, z_cell0, x + feld, B - rand, z_cell0 + tdk).cut(tool)
        vg = box(x, rand, z_cell0 + tdk, x + feld, B - rand, z_cell0 + hv).cut(tool)
        add(f"Zelltraeger_f{f}", "Zelltraeger", tr, mat="offen (Werkstoff/Dichte fehlt)")
        add(f"Verguss_f{f}", "Verguss", vg, mat="offen (Dichte fehlt)")
        x += feld + sp
        if f < nq: pos_q.append(x); x += qb + sp
for i, xq in enumerate(pos_q):
    add(f"Quertraeger_{i+1}", "Quertraeger", hohl_q(xq, zc_q), mat="Al")
for c in cells: add(c["name"], "Zellen", c["shape"], mass=mcell, mat="Zelle (Masse aus Akte)")


# ---- E2 (Schalter PACK_E2=1), Auftrag E2 Fortsetzung 2: Schaltbox hinten als Turm (ENT-144), CMU hochkant in den Endzonen, FPC, HV intern (NMC Mäander ENT-145).
# Maße aus Akten (w(...)) und Block A (A_e2_*, Herkunft ERW-E2 N1). Verdrahtungslogik: cad/pack/e2_verdrahtung.py.
e2res = {}
if E2:
    sys.path.insert(0, f"{ROOT}/cad/pack"); import e2_verdrahtung as EV
    def A3(k): return [float(x) for x in A[k]]
    gap, wd, rm = A["A_e2_box_teilabstand_mm"], A["A_e2_box_wand_mm"], A["A_e2_box_rand_mm"]
    assert P["BT-710"]["einbauort"]["wert"] == "deckel_hinten", P["BT-710"]["einbauort"]
    cmuL, cmuB, cmuD = A3("A_e2_cmu_mm"); plL, plB, plH = A3("A_e2_trennstecker_mm")      # CMU hochkant: Länge 120 in y, Breite 60 in z, Dicke 10 in x
    fw, ft, fh = w("BT-360", "breite_mm"), A["A_e2_fpc_dicke_mm"], A["A_e2_fpc_halter_mm"]  # FPC: Breite, Dicke, Halter (Halter 3 mm zusätzlich zur Dicke)
    dhv = A[f"A_e2_hv_aussendurchmesser_{VAR}_mm"]; rhv = dhv / 2; Rb = w("BT-430", "biegeradius_min_mm")
    ncmu, nkan = int(w("BT-320", "anzahl")), int(w("BT-320", "kanaele")); kg_fpc_m = A["A_e2_fpc_masse_kg_m"]
    Whv = json.load(open(f"{ROOT}/sim/elektrik/e2_elektronik/ergebnis.json"))[VAR]["hv_W_je_m_Leiter_laden"]
    EIN = json.load(open(f"{ROOT}/sim/elektrik/e2_elektronik/eingaben.json")); rhoCu = EIN["stoffe"]["rho_Cu_kg_m3"]; A_hv = w("BT-430", "querschnitt_mm2")
    def cu_kg(L_mm): return rhoCu * A_hv * L_mm * 1e-9      # kg = kg/m3 * mm2 * mm * 1e-9 (nur Kupfer, Isolierung ohne Wert)
    ymin_, ymax_ = rand, B - rand; Bi_ = ymax_ - ymin_; xv_in, xh_in = rand, Lg - rand; zc = zc_q
    def cyl(x, y, z0, z1, r): return Part.makeCylinder(r, z1 - z0, V(x, y, z0))
    geo = dict(cmu=[], fpc=[], hv=[], taps=[]); cutter = []   # cutter: (shape, ziel-Namen) für Durchführungen und Aussparungen
    # ---- Abgriffe und Verschaltung
    if VAR == "NMC":
        mw = EV.nmc_maeander(cells, Dm, Dm + ab, rand); taps = mw["taps"]; tap_row = None
        ans = {a["name"]: cells[a["zelle"]] for a in mw["anschluesse"]}
        xmax_k = {k: max(c["cx"] for c in cells if c["k"] == k) for k in {c["k"] for c in cells}}
        alle_hinten = all(abs(c["cx"] - xmax_k[c["k"]]) < 1e-6 for c in ans.values())
        vers = dict(variante="NMC", machbar=True, alle_anschluesse_hinten=alle_hinten, bänder=len(mw["gruppen_je_band"]), gruppen_je_band=mw["gruppen_je_band"], gruppen_hälfte_A=mw["hälfte_A_gruppen"], gruppen_hälfte_B=mw["hälfte_B_gruppen"],
                    schritt_zellen_normal_mm=mw["schritt_normal_mm"], schritt_zellen_max_mm=mw["schritt_max_mm"], schritte_über_1p05_teilung=mw["bruecken_ueber_1p05t"],
                    anschluesse={k: dict(x=c["cx"], y=c["cy"]) for k, c in ans.items()})
        x_vorn_frei = min(c["cx"] for c in cells) - Dm / 2 - xv_in; x_hinten_frei = xh_in - max(c["cx"] + Dm / 2 for c in cells)
    else:
        r0c = sorted([c for c in cells if c["rr"] == 0], key=lambda c: -c["cx"]); r1c = sorted([c for c in cells if c["rr"] == 1], key=lambda c: c["cx"]); kette = r0c + r1c
        nl = 4; hh = fh - nl * ft      # Nachtrag 2: bis 4 FPC übereinander, 4 x 0,3 mm + Halter <= 3 mm (A_e2_fpc_halter_mm = 3,0 mm Stapel)
        yg = {0: ymin_ + hh + ft / 2, 1: ymax_ - hh - ft / 2}; taps = []; tap_row = []; nr0 = len(r0c)
        for i in range(len(kette) + 1):
            if i == 0: x, rw = kette[0]["cx"], 0
            elif i == len(kette): x, rw = kette[-1]["cx"], 1
            elif i == nr0: x, rw = kette[i - 1]["cx"], 0           # Übergang vorn von Reihe 0 auf Reihe 1
            else: x, rw = (kette[i - 1]["cx"] + kette[i]["cx"]) / 2, (0 if i < nr0 else 1)
            taps.append((x, yg[rw])); tap_row.append(rw)
        vers = dict(variante="LFP", machbar=True, konzept="schleife_2reihen (ENT-148)", reihen_physisch=2, zellen_je_reihe=nr0,
                    kette="Plus hinten Reihe 0 -> vorn, Querverbinder vorn (Mitte, Service-Trennstecker in der Deckelöffnung), Reihe 1 -> hinten Minus",
                    mitte_vorn_x=kette[nr0 - 1]["cx"], plus_hinten_x=kette[0]["cx"], minus_hinten_x=kette[-1]["cx"])
        x_vorn_frei = min(c["cx"] for c in cells) - Dc / 2 - xv_in; x_hinten_frei = xh_in - max(c["cx"] + Dc / 2 for c in cells)
    if VAR == "NMC":   # Fortsetzung 3: Gruppenverbinder nach Mäander-Folge (Gruppe = 4 aufeinanderfolgende Zellen), Brücken an den Wendestellen (Spaltenwechsel) und zwischen den Gruppen
        gb = gv_b / 2; zc0_, zc1_ = z_top_cell + ag_t, z_top_cell + ag_t + gv_d
        def strip(pa, pb):
            dx, dy = pb[0] - pa[0], pb[1] - pa[1]; Ln = math.hypot(dx, dy); nx, ny = -dy / Ln * gb, dx / Ln * gb
            pts = [V(pa[0] + nx, pa[1] + ny, zc0_), V(pb[0] + nx, pb[1] + ny, zc0_), V(pb[0] - nx, pb[1] - ny, zc0_), V(pa[0] - nx, pa[1] - ny, zc0_)]; pts.append(pts[0])
            return Part.Face(Part.makePolygon(pts)).extrude(V(0, 0, zc1_ - zc0_))
        def disc(c): return Part.makeCylinder(gb, zc1_ - zc0_, V(c["cx"], c["cy"], zc0_))
        gsh = []; n_wende = 0; n_br = 0
        for gi_, g in enumerate(mw["gruppen"]):
            cs_ = [cells[i] for i in g]; teil = [disc(c) for c in cs_]; wend = []
            for ca, cb in zip(cs_, cs_[1:]):
                (teil if ca["k"] == cb["k"] else wend).append(strip((ca["cx"], ca["cy"]), (cb["cx"], cb["cy"])))
            sh = teil[0]
            for q_ in teil[1:]: sh = sh.fuse(q_)
            sh = sh.removeSplitter(); gsh.append(sh); add(f"Gruppenverbinder_g{gi_:03d}", "Gruppenverbinder", sh, mat="Al (Annahme, Cu offen)")
            for wi, w_ in enumerate(wend):
                add(f"Wendebruecke_g{gi_:03d}_{wi}", "Gruppenbruecke", w_.cut(sh), mat="Al (Annahme, Cu offen)"); n_wende += 1
        for gi_ in range(len(mw["gruppen"]) - 1):
            ca, cb = cells[mw["gruppen"][gi_][-1]], cells[mw["gruppen"][gi_ + 1][0]]
            add(f"Gruppenbruecke_g{gi_:03d}", "Gruppenbruecke", strip((ca["cx"], ca["cy"]), (cb["cx"], cb["cy"])).cut(gsh[gi_]).cut(gsh[gi_ + 1]), mat="Al (Annahme, Cu offen)"); n_br += 1
        vers.update(gruppenverbinder=len(gsh), wendebruecken_in_gruppen=n_wende, gruppenbruecken=n_br)
        dd_ = lambda a, b: math.hypot(cells[a]["cx"] - cells[b]["cx"], cells[a]["cy"] - cells[b]["cy"])      # Abstände Zellmitte-Zellmitte entlang der Mäander-Folge (für Verlustrechnung Al, verlust_al.py)
        vers["al_sammel_schritte_mm"] = [[dd_(a_, b_) for a_, b_ in zip(g_, g_[1:])] for g_ in mw["gruppen"]]; vers["al_bruecken_mm"] = [dd_(mw["gruppen"][i][-1], mw["gruppen"][i + 1][0]) for i in range(len(mw["gruppen"]) - 1)]
    geo["taps"] = [[t[0], t[1]] for t in taps]
    # ---- CMU: Zuordnung, Lage (hochkant, an den Rahmen gelehnt)
    asg = EV.cmu_zuordnung(taps, ncmu, nkan, xv_in + cmuD / 2, xh_in - cmuD / 2, ymin_, ymax_, cmuL)
    grp_t, seite = asg["gruppen"], asg["seite"]; mean_y = [sum(taps[i][1] for i in g) / len(g) for g in grp_t]
    ypos = [None] * ncmu
    for sd in ("vorn", "hinten"):      # CMU je Endzone so nah wie möglich an der mittleren y-Lage ihrer Abgriffe, Mindestabstand = CMU-Länge, innerhalb der Innenbreite
        ids = sorted([j for j in range(ncmu) if seite[j] == sd], key=lambda j: mean_y[j]); n = len(ids)
        if n == 0: continue
        ys = []
        for j in ids: ys.append(max(mean_y[j], ys[-1] + cmuL) if ys else max(mean_y[j], ymin_ + cmuL / 2))
        for i in range(n - 1, -1, -1): ys[i] = min(ys[i], (ys[i + 1] - cmuL) if i < n - 1 else ymax_ - cmuL / 2)
        for j, y in zip(ids, ys): ypos[j] = y
    lane = [None] * ncmu     # y der FPC-Spur (NMC): innerhalb der CMU-Kante (+-(L/2-fw/2)), Abstand zu HV-Leitungen und zu anderen Spuren
    hv_y = [c["cy"] for c in ans.values()] if VAR == "NMC" else []
    for j in sorted(range(ncmu), key=lambda j: ypos[j]):
        for dd in sorted(range(-int(cmuL / 2 - fw / 2), int(cmuL / 2 - fw / 2) + 1), key=abs):
            y = ypos[j] + dd
            if all(abs(y - h) >= max(rhv, A3("A_e2_lasche_mm")[0] / 2) + fw / 2 + 1 for h in hv_y if VAR == "NMC") and all(abs(y - l) >= fw + 2 for l in lane if l is not None): lane[j] = y; break
        assert lane[j] is not None, j
    cmu_x = {"vorn": (xv_in, xv_in + cmuD), "hinten": (xh_in - cmuD, xh_in)}
    for j in range(ncmu):
        x0, x1 = cmu_x[seite[j]]
        add(f"CMU_{j:02d}", "E2_CMU", box(x0, ypos[j] - cmuL / 2, zc - cmuB / 2, x1, ypos[j] + cmuL / 2, zc + cmuB / 2), mass=A["A_e2_cmu_masse_kg"], mat="E2 Teil (Masse ERW-E2 N1)")
        geo["cmu"].append(dict(i=j, seite=seite[j], x=(x0 + x1) / 2, y=ypos[j], taps=len(grp_t[j])))
    # ---- HV-Leitungen intern (nur NMC, Mäander); Lage Stecker und Schaltbox (Plus/Minus an die Box, Mitte an den Service-Trennstecker)
    hv_len = []; vert_cut = []
    bms = [w("BT-310", "laenge_mm"), w("BT-310", "breite_mm"), w("BT-310", "hoehe_mm")]
    inh = [("BMS_Platine", bms, A["A_e2_bms_masse_kg"]), ("Shunt", A3("A_e2_shunt_mm"), A["A_e2_shunt_masse_kg"]),
           ("Hauptschuetz_1", A3("A_e2_schuetz_mm"), A["A_e2_schuetz_masse_kg"]), ("Hauptschuetz_2", A3("A_e2_schuetz_mm"), A["A_e2_schuetz_masse_kg"]),
           ("Vorladeschuetz", A3("A_e2_vorladeschuetz_mm"), A["A_e2_vorlade_masse_kg"]), ("Vorladewiderstand", A3("A_e2_vorladewiderstand_mm"), 0.0),
           ("Pyrosicherung", A3("A_e2_pyro_mm"), A["A_e2_pyro_masse_kg"]), ("Schmelzsicherung", A3("A_e2_schmelz_mm"), A["A_e2_schmelz_masse_kg"])]
    reihen = [["BMS_Platine", "Shunt"], ["Hauptschuetz_1", "Hauptschuetz_2", "Vorladeschuetz", "Vorladewiderstand"], ["Pyrosicherung", "Schmelzsicherung"]]
    d_ = {n: (m, ms) for n, m, ms in inh}
    rb = [sum(d_[n][0][0] for n in r) + gap * (len(r) - 1) for r in reihen]; innenL = max(rb)
    tiefe = [max(d_[n][0][1] for n in r) for r in reihen]; innenB = sum(tiefe) + gap * (len(reihen) - 1)
    hoch = max(d_[n][0][2] for n in d_); bL, bB, bH = innenL + 2 * rm, innenB + 2 * rm, hoch + 2 * wd
    bx0 = xh_in - bL                                         # hinten bündig mit der Rahmeninnenkante
    if VAR == "NMC":
        plug_x = (ans["Mitte_A_Ende_Band2"]["cx"] + ans["Mitte_B_Anfang_Band3"]["cx"]) / 2; plug_y = (ans["Mitte_A_Ende_Band2"]["cy"] + ans["Mitte_B_Anfang_Band3"]["cy"]) / 2
        by0 = plug_y + plB / 2 + gap                         # Box neben dem Trennstecker (+y), der über den Mittenanschlüssen sitzt
    else: by0 = B / 2 - bB / 2
    bz0 = z_top
    outer = box(bx0, by0, bz0, bx0 + bL, by0 + bB, bz0 + bH)
    add("Schaltbox_Gehaeuse", "E2_Schaltbox", outer.cut(box(bx0 + wd, by0 + wd, bz0 + wd, bx0 + bL - wd, by0 + bB - wd, bz0 + bH - wd)), mat="Al")
    yy = by0 + rm
    for r, t_ in zip(reihen, tiefe):
        xx = bx0 + rm
        for n in r:
            (l_, b_, h_), ms = d_[n]
            add(n, "E2_Schaltbox_Inhalt", box(xx, yy, bz0 + wd, xx + l_, yy + b_, bz0 + wd + h_), mass=ms, mat="E2 Teil (Masse ERW-E2 N1)"); xx += l_ + gap
        yy += t_ + gap
    xs_ = bx0 - gap; ys_ = by0 + rm                          # Stecker und Sensor vor der Box (kleineres x) auf dem Deckel, in Reihe entlang y
    for n, k, mk in (("HV_Stecker_250A", "A_e2_hv250_mm", "A_e2_hv250_masse_kg"), ("HV_Stecker_40A", "A_e2_hv40_mm", "A_e2_hv40_masse_kg"), ("NV_Stecker_26pol", "A_e2_nv_mm", "A_e2_nv_masse_kg"), ("Gas_Drucksensor", "A_e2_gas_mm", "A_e2_gas_masse_kg")):
        l_, b_, h_ = A3(k); add(n, "E2_Stecker_Sensor", box(xs_ - l_, ys_, z_top, xs_, ys_ + b_, z_top + h_), mass=A[mk], mat="E2 Teil (Masse ERW-E2 N1)"); ys_ += b_ + gap
    if VAR == "NMC":
        add("Service_Trennstecker", "E2_Stecker_Sensor", box(plug_x - plL / 2, plug_y - plB / 2, z_top, plug_x + plL / 2, plug_y + plB / 2, z_top + plH), mass=A["A_e2_trennstecker_masse_kg"], mat="E2 Teil (Masse ERW-E2 N1)")
        z_h = z_top + plH + gap + rhv                         # Höhe der Leitung über dem Trennstecker (Abstand = Teilabstand-Platzhalter)
        lw_, lz_ = A3("A_e2_lasche_mm"); lbo = A["A_e2_lasche_bohrung_mm"]      # NMC Anschlusslasche: Platte 25 x 25 x 3 auf dem Gruppenverbinder (Überlappung 25 mm), Bohrung M8 im Zellmittelpunkt
        for nm in ("Plus", "Minus", "Mitte_A_Ende_Band2", "Mitte_B_Anfang_Band3"):
            c = ans[nm]; pl_ = box(c["cx"] - lw_ / 2, c["cy"] - lw_ / 2, z_pad2, c["cx"] + lw_ / 2, c["cy"] + lw_ / 2, z_pad2 + lz_)
            add(f"Lasche_{nm}", "E2_Lasche", pl_.cut(cyl(c["cx"], c["cy"], z_pad2 - 1, z_pad2 + lz_ + 1, lbo / 2)), mat="Al"); cutter.append((pl_, ("Pad_oben", "Kuehlplatte_oben")))
        for nm, ywall, sgn in (("Plus", by0, 1), ("Minus", by0 + bB, -1)):
            c = ans[nm]; x, y = c["cx"], c["cy"]; z0 = z_pad2 + lz_; za = z_h - Rb
            assert abs(ywall - y) > Rb, (nm, y, ywall)
            p1, p2 = V(x, y, z0), V(x, y, za); p3 = V(x, y + sgn * Rb, z_h); p4 = V(x, ywall, z_h)
            pm_ = V(x, y + sgn * Rb * (1 - math.cos(math.pi / 4)), za + Rb * math.sin(math.pi / 4))
            wire = Part.Wire([Part.makeLine(p1, p2), Part.Arc(p2, pm_, p3).toShape(), Part.makeLine(p3, p4)])
            shp = wire.makePipeShell([Part.Wire(Part.makeCircle(rhv, p1, V(0, 0, 1)))], True, True)
            L_ = (za - z0) + math.pi * Rb / 2 + (abs(ywall - y) - Rb)
            add(f"HV_{nm}", "E2_HV_Leitung", shp, mass=cu_kg(L_), mat="Cu (Leiter, Isolierung ohne Wert)"); hv_len.append((f"{nm} Zelle -> Schaltbox", L_)); vert_cut.append(cyl(x, y, z0, z_top, rhv))
            geo["hv"].append(dict(name=nm, laenge_mm=L_, xy=[[x, y], [x, ywall]]))
        for nm in ("Mitte_A_Ende_Band2", "Mitte_B_Anfang_Band3"):
            c = ans[nm]; x, y = c["cx"], c["cy"]
            add(f"HV_{nm}", "E2_HV_Leitung", cyl(x, y, z_pad2 + lz_, z_top, rhv), mass=cu_kg(z_top - z_pad2 - lz_), mat="Cu (Leiter, Isolierung ohne Wert)"); hv_len.append((f"{nm} -> Trennstecker", z_top - z_pad2 - lz_)); vert_cut.append(cyl(x, y, z_pad2, z_top, rhv))
            geo["hv"].append(dict(name=nm, laenge_mm=z_top - z_pad2 - lz_, xy=[[x, y]]))
    else:   # LFP (ENT-148): Plus/Minus hinten zur Box; Mitte vorn: Querverbinder (Flachschiene auf den vordersten Zellen) -> 2 Leitungen -> Service-Trennstecker in der Deckelöffnung
        gz_, gt_ = A["A_zellverbinder_LFP_mm"]; z_ht = z_top_cell; x_c0 = min(c["cx"] for c in cells) - Dc / 2
        zl_ = A3("A_e2_lasche_mm")[1]; xlead = xh_in - x_hinten_frei / 2; z_h = z_ht + zl_ + Rb      # Leitungsfuß liegt auf dem Flansch der Lasche (3 mm über Zellober-/FPC-Ebene)
        assert z_top + wd + rhv <= z_h <= z_top + bH - wd - rhv, ("Leitungshöhe außerhalb der Box", z_h - z_top, bH)
        for nm, y, ywall, sgn in (("Plus", ymin_ + 1 + rhv, by0, 1), ("Minus", ymax_ - 1 - rhv, by0 + bB, -1)):
            za = z_h - Rb; p2 = V(xlead, y, za); p3 = V(xlead, y + sgn * Rb, z_h); p4 = V(xlead, ywall, z_h)
            pm_ = V(xlead, y + sgn * Rb * (1 - math.cos(math.pi / 4)), za + Rb * math.sin(math.pi / 4)); p1 = V(xlead, y, z_ht + zl_)
            segs = ([Part.makeLine(p1, p2)] if za - z_ht - zl_ > 1e-6 else []) + [Part.Arc(p2, pm_, p3).toShape(), Part.makeLine(p3, p4)]
            shp = Part.Wire(segs).makePipeShell([Part.Wire(Part.makeCircle(rhv, p1, V(0, 0, 1)))], True, True)
            L_ = (za - z_ht - zl_) + math.pi * Rb / 2 + (abs(ywall - y) - Rb)
            add(f"HV_{nm}", "E2_HV_Leitung", shp, mass=cu_kg(L_), mat="Cu (Leiter, Isolierung ohne Wert)"); hv_len.append((f"{nm} Zelle -> Schaltbox", L_)); cutter.append((shp, ("Pad_oben", "Kuehlplatte_oben", "Deckel")))
            geo["hv"].append(dict(name=nm, laenge_mm=L_, xy=[[xlead, y], [xlead, ywall]]))
        # Laschen Plus/Minus (ERW-E2 N3): Platte 25 breit (y) x 3 dick (x) am Ende des hintersten Zellverbinders (Stumpfstoß, Überlappung 25 mm im Seitenspalt nicht darstellbar), Steg hoch bis unter den Leitungsfuß, Flansch 3 mm unter dem Leitungsfuß mit Bohrung M8
        lw_, lt_ = A3("A_e2_lasche_mm"); lbo = A["A_e2_lasche_bohrung_mm"]; xe_ = xh_in - x_hinten_frei; la_info = []
        for nm, y0_, sg in (("Plus", ymin_ + 1, 1), ("Minus", ymax_ - 1, -1)):
            y0_ = y0_ + sg * (fh - 1 + 0.2)        # hinter dem FPC-Stapel (Stapel 3 mm ab Rahmeninnenkante), Lasche beginnt 0,2 mm danach
            ya, yb_ = (y0_, y0_ + lw_) if sg == 1 else (y0_ - lw_, y0_)
            steg = box(xe_, ya, zc - gz_ / 2, xe_ + lt_, yb_, z_ht + lt_); fl = box(xe_, ya, z_ht, xlead + rhv, yb_, z_ht + lt_)
            las = steg.fuse(fl).removeSplitter().cut(cyl(xlead, ymin_ + 1 + rhv if sg == 1 else ymax_ - 1 - rhv, z_ht - 1, z_ht + lt_ + 1, lbo / 2))
            add(f"Lasche_{nm}", "E2_Lasche", las, mat="Al"); la_info.append(dict(name=nm, pfad_mm=(z_ht + lt_ - (zc - gz_ / 2)) + (xlead - xe_), querschnitt_mm2=lw_ * lt_)); cutter.append((fl, ("Pad_oben", "Kuehlplatte_oben")))
        # Service-Trennbrücke (ENT-150): Querverbinder mit Lücke, Cu-Brücke 25 x 3 darüber (Überlappung je Seite), 2 x M8, Öffnung 120 (y) x 80 (x) bis unter den Servicedeckel
        bg_, bov_, (bw_, bt_) = A["A_e2_bruecke_luecke_mm"], A["A_e2_bruecke_ueberlappung_mm"], A3("A_e2_bruecke_querschnitt_mm"); oy_, ox_ = A3("A_e2_serviceoeffnung_mm")
        py = B / 2; yA, yB = py - bg_ / 2, py + bg_ / 2; px = x_c0 + gz_ / 2; ox0 = xv_in + 2
        assert ox0 <= px - bw_ / 2 and px + bw_ / 2 <= ox0 + ox_, "Brücke außerhalb der Öffnung"
        zb0 = z_ht + gt_; bo_ = (lbo / 2)
        holes = [cyl(px, yA - bov_ / 2, z_ht - 1, zb0 + bt_ + 1, bo_), cyl(px, yB + bov_ / 2, z_ht - 1, zb0 + bt_ + 1, bo_)]
        qa = box(x_c0, ymin_ + 1, z_ht, x_c0 + gz_, yA, zb0); qb_ = box(x_c0, yB, z_ht, x_c0 + gz_, ymax_ - 1, zb0)
        add("Querverbinder_Mitte_A", "Zellverbinder", qa.cut(holes[0]), mat="Al (wie Zellverbinder G4)"); add("Querverbinder_Mitte_B", "Zellverbinder", qb_.cut(holes[1]), mat="Al (wie Zellverbinder G4)")
        br_ = box(x_c0, yA - bov_, zb0, x_c0 + bw_, yB + bov_, zb0 + bt_).cut(holes[0]).cut(holes[1])
        add("Trennbruecke_Cu", "E2_Trennbruecke", br_, mass=br_.Volume * rhoCu * 1e-9, mat="Cu"); sch_ = [add(f"Schraube_M8_{k}", "E2_Trennbruecke", h_.common(box(px - 10, 0, z_ht, px + 10, B, zb0 + bt_)), mass=0.0, mat="Stahl (Masse offen, 0 gesetzt)") for k, h_ in enumerate(holes)]
        cutter.append((box(x_c0, ymin_ + 1, z_ht, x_c0 + gz_, ymax_ - 1, zb0), ("Pad_oben", "Kuehlplatte_oben")))   # Schiene 3 mm dick, Pad dünner: Nut in der oberen Kühlplatte
        cutter.append((box(ox0, py - oy_ / 2, z_ht, ox0 + ox_, py + oy_ / 2, z_top + 1), ("Pad_oben", "Kuehlplatte_oben", "Deckel")))   # Serviceöffnung durch Pad, Kühlplatte, Deckel
        add("Servicedeckel", "E2_Servicedeckel", box(ox0, py - oy_ / 2, z_dk, ox0 + ox_, py + oy_ / 2, z_top), mat="Al")
        kf_ = (Lg - 2 * rand) * (B - 2 * rand); nut_ = gz_ * ((ymax_ - 1) - (ymin_ + 1)); ov_ = gz_ * oy_
        nut_info = dict(kuehlflaeche_oben_mm2=kf_, nut_flaeche_gesamt_mm2=nut_, nut_flaeche_ohne_oeffnung_mm2=nut_ - ov_, nut_tiefe_in_kuehlplatte_mm=gt_ - A["A_pad_mm"], nut_anteil_prozent=100 * (nut_ - ov_) / kf_,
                        oeffnung_flaeche_mm2=ox_ * oy_, nut_plus_oeffnung_anteil_prozent=100 * (nut_ - ov_ + ox_ * oy_) / kf_, oeffnung_anteil_prozent=100 * ox_ * oy_ / kf_)
        quer_L = (yA - ymin_ - 1) + (ymax_ - 1 - yB); lfp_stecker = dict(bauform="trennbruecke_servicedeckel (ENT-150)", x=px, y=py, oberkante_mm=z_top, ueber_deckel_mm=0.0, serviceoeffnung_mm=[oy_, ox_], oeffnung_x0_mm=ox0, bruecke_mm=[bw_, bt_, (yB - yA) + 2 * bov_], luecke_mm=bg_, querverbinder_laenge_mm=quer_L, laschen=la_info, nut=nut_info)
    # ---- FPC (Länge immer berechnet; gebaut, wenn Platz)
    face = {"vorn": xv_in + cmuD, "hinten": xh_in - cmuD}; sgnx = {"vorn": 1, "hinten": -1}
    fpc_info = []; fpc_mass_kg = 0.0
    if VAR == "NMC":
        zf0 = z_pad2; zlink = zf0 - (zc + cmuB / 2)
        for j in range(ncmu):
            s = seite[j]; yl = lane[j]; xf = face[s]; xs_t = [taps[i][0] for i in grp_t[j]]; xfar = max(xs_t) if s == "vorn" else min(xs_t)
            stub = sum(abs(taps[i][1] - yl) for i in grp_t[j]); Lx = abs(xfar - xf); Ltot = zlink + Lx + stub
            xa, xb = sorted((xf, xfar)); parts = [box(xa, yl - fw / 2, zf0, xb, yl + fw / 2, zf0 + ft)]
            va = xf if s == "vorn" else xf - ft; parts.append(box(va, yl - fw / 2, zc + cmuB / 2, va + ft, yl + fw / 2, zf0 + ft))
            shp = parts[0].fuse(parts[1]); m_ = kg_fpc_m * Ltot / 1000; fpc_mass_kg += m_
            add(f"FPC_{j:02d}", "E2_FPC", shp, mass=m_, mat="FPC (Masse ERW-E2 N1)")
            fpc_info.append(dict(cmu=j, seite=s, laenge_mm=Ltot, davon_x_mm=Lx, davon_stichleitungen_mm=stub, davon_senkrecht_mm=zlink, platziert=True, ebene="Verbinderebene unter dem Pad"))
            geo["fpc"].append(dict(cmu=j, xy=[[xf, yl], [xfar, yl]], stub=[[taps[i][0], taps[i][1]] for i in grp_t[j]]))
            cutter.append((shp, ("Pad_oben",)))
    else:   # LFP: Seitenspalt, 2 Spuren (oben/unten, z) mit je bis zu 4 Lagen (y, Nachtrag 2); FPC-Breite nach ENT-149
        Hc_ = Hc; lanes = [(zc + Hc_ / 2 - fw, zc + Hc_ / 2), (zc - Hc_ / 2, zc - Hc_ / 2 + fw)]
        ylay = lambda rw, l: ((ymin_ + hh + l * ft, ymin_ + hh + (l + 1) * ft) if rw == 0 else (ymax_ - hh - (l + 1) * ft, ymax_ - hh - l * ft))
        stripes = []
        for j in range(ncmu):
            for rw in (0, 1):
                ids = [i for i in grp_t[j] if tap_row[i] == rw]
                if not ids: continue
                s = seite[j]; xf = face[s]; xs_t = [taps[i][0] for i in ids]; xfar = max(xs_t) if s == "vorn" else min(xs_t)
                Ly = abs(ypos[j] - yg[rw]); Lx = abs(xfar - xf); stripes.append((j, rw, s, xf, xfar, Ly, Lx, min(xf, xfar), max(xf, xfar)))
        slot = {"vorn": 0, "hinten": 0}; placed = []
        for (j, rw, s, xf, xfar, Ly, Lx, xa, xb) in sorted(stripes, key=lambda q: -q[6]):      # lange Stücke zuerst: nächster Platz an der CMU, niedrigste Lage
            sx = slot[s] * ft; cx0 = xf + sx if s == "vorn" else xf - sx - ft; cx1 = cx0 + ft
            sa, sb = (xa, cx1) if s == "hinten" else (cx0, xb)      # Streifen beginnt am Quersteg (nicht an der CMU-Fläche)
            frei = (cx1 <= xv_in + x_vorn_frei + 1e-6) if s == "vorn" else (cx0 >= xh_in - x_hinten_frei - 1e-6)
            pos = None
            for lane_i in (0, 1):
                for ly in range(nl):
                    if not frei: break
                    bad = False
                    for q in placed:
                        if q["rw"] != rw or q["lane"] != lane_i: continue
                        if q["layer"] == ly and not (sb < q["xa"] - 1e-6 or sa > q["xb"] + 1e-6): bad = True
                        if q["layer"] > ly and q["xa"] - 1e-6 <= cx1 and q["xb"] + 1e-6 >= cx0: bad = True      # mein Quersteg läuft durch deren Lage
                        if ly > q["layer"] and sa - 1e-6 <= q["cx1"] and sb + 1e-6 >= q["cx0"]: bad = True      # deren Quersteg läuft durch meine Lage
                    if not bad: pos = (lane_i, ly); break
                if pos: break
            Ltot = Ly + Lx; m_ = kg_fpc_m * Ltot / 1000; fpc_mass_kg += m_
            info = dict(cmu=j, reihe=rw, seite=s, laenge_mm=Ltot, davon_x_mm=Lx, davon_y_mm=Ly, platziert=pos is not None, spur=(pos[0] if pos else None), lage=(pos[1] if pos else None))
            fpc_info.append(info); ylc = (sum(ylay(rw, pos[1])) / 2) if pos else yg[rw]; geo["fpc"].append(dict(cmu=j, reihe=rw, xy=[[xf, ypos[j]], [xf, ylc], [xfar, ylc]], platziert=pos is not None))
            if pos is None: continue
            lane_i, ly = pos; slot[s] += 1; placed.append(dict(rw=rw, lane=lane_i, layer=ly, xa=sa, xb=sb, cx0=cx0, cx1=cx1)); z0, z1 = lanes[lane_i]
            ya, yb_ = ylay(rw, ly); yc0, yc1 = (ya, ypos[j]) if rw == 0 else (ypos[j], yb_)
            shp = box(sa, ya, z0, sb, yb_, z1).fuse(box(cx0, yc0, z0, cx1, yc1, z1)); add(f"FPC_{j:02d}_R{rw}", "E2_FPC", shp, mass=m_, mat="FPC (Masse ERW-E2 N1)")
        for rw in (0, 1):      # Halter je Reihe und Spur (Stapel insgesamt fh = 3 mm); Masse im FPC-Wert (kg/m) nicht getrennt ausgewiesen
            for lane_i in (0, 1):
                qs_ = [q for q in placed if q["rw"] == rw and q["lane"] == lane_i]
                if not qs_: continue
                hy = (ymin_, ymin_ + hh) if rw == 0 else (ymax_ - hh, ymax_)
                add(f"FPC_Halter_R{rw}_S{lane_i}", "E2_FPC_Halter", box(min(q["xa"] for q in qs_), hy[0], lanes[lane_i][0], max(q["xb"] for q in qs_), hy[1], lanes[lane_i][1]), mass=0.0, mat="Halter (Masse offen, 0 gesetzt)")
    # ---- Durchführungen und Aussparungen (Verguss/Träger/Pad/Kühlplatte/Deckel werden um E2-Teile herum gelassen; Volumen wird gemeldet)
    for q_ in vert_cut: cutter.append((q_, ("Pad_oben", "Kuehlplatte_oben", "Deckel")))
    for p in list(teile):
        if p["grp"] == "E2_CMU": cutter.append((p["shape"], ("Zelltraeger_f", "Verguss_f")))
    ausspar = {}
    for p in teile:
        for shp, ziele in cutter:
            if any(p["name"].startswith(z) for z in ziele) and p["shape"].BoundBox.intersect(shp.BoundBox):
                v0 = p["shape"].Volume; p["shape"] = p["shape"].cut(shp); dv = v0 - p["shape"].Volume
                if dv > 1e-6: ausspar[p["name"]] = ausspar.get(p["name"], 0.0) + dv
    mass_e2 = sum(p["mass"] for p in teile if p["grp"].startswith("E2") and p["mass"] is not None) - sum(p["mass"] for p in teile if p["grp"] == "E2_FPC") + kg_fpc_m * sum(f["laenge_mm"] for f in fpc_info) / 1000
    hvl = sum(l for _, l in hv_len) + (2 * gap if True else 0)   # plus 2 kurze Leitungen Schaltbox -> HV-Stecker 250 A (Länge = Teilabstand)
    e2res = dict(fall="hinten (ENT-144)", verschaltung=vers, schaltbox_L_mm=bL, schaltbox_B_mm=bB, schaltbox_H_mm=bH, schaltbox_x0_y0_z0_mm=[bx0, by0, bz0], reihenbreiten_mm=rb, hoechstes_teil_mm=hoch,
                 hoehenzuwachs_gesamt_mm=max(p["shape"].BoundBox.ZMax for p in teile if p["grp"].startswith("E2")) - z_top, hoehe_stapel_vor_e2_mm=z_top, hoehe_max_A_mm=A["A_hoehe_max_mm"],
                 cmu_anzahl=ncmu, cmu_seite=dict(vorn=seite.count("vorn"), hinten=seite.count("hinten")), cmu_kapazitaet_je_endzone=asg["kapazitaet_je_endzone"], cmu_masse_kg=ncmu * A["A_e2_cmu_masse_kg"],
                 freier_abstand_endzone_vorn_mm=x_vorn_frei, freier_abstand_endzone_hinten_mm=x_hinten_frei, cmu_dicke_mm=cmuD, abgriffe=len(taps), cmu_y=ypos,
                 fpc=fpc_info, fpc_laenge_gesamt_m=sum(f["laenge_mm"] for f in fpc_info) / 1000, fpc_laenge_platziert_m=sum(f["laenge_mm"] for f in fpc_info if f["platziert"]) / 1000,
                 fpc_stuecke=len(fpc_info), fpc_nicht_platziert=sum(1 for f in fpc_info if not f["platziert"]), fpc_masse_kg=kg_fpc_m * sum(f["laenge_mm"] for f in fpc_info) / 1000,
                 hv=[dict(strecke=n, laenge_mm=l) for n, l in hv_len], hv_laenge_gesamt_m=hvl / 1000, hv_W_je_m=Whv, hv_verlust_W=hvl / 1000 * Whv, hv_cu_masse_kg=sum(cu_kg(l) for _, l in hv_len) + cu_kg(2 * gap), stecker_lfp=(lfp_stecker if VAR == "LFP" else None), hoehe_vorn_mm=max(p["shape"].BoundBox.ZMax for p in teile if p["shape"].BoundBox.XMax < bx0 - 100), hoehe_vorn_grenze_x_mm=bx0 - 100,
                 hv_gebaut=True, hv_kurze_leitungen_box_stecker_mm=2 * gap,
                 masse_elektronik_ohne_hv_leitungen_kg=mass_e2, aussparungen_mm3=ausspar, geometrie=geo, biegeradius_mm=Rb, hv_aussendurchmesser_mm=dhv)

# ---- Massen, Schwerpunkt
def com(s):
    so = s.Solids
    if len(so) == 1: return so[0].CenterOfMass
    v = sum(x.Volume for x in so)
    return [sum(x.Volume * x.CenterOfMass[i] for x in so) / v for i in range(3)]
for p in teile:
    p["vol"] = p["shape"].Volume
    g_ = p["grp"]
    if g_ == "Kuehlplatte": p["mass"] = p["vol"] * rho * A["A_KUEHLPLATTE_FUELLGRAD"]
    elif g_ == "Seitenrahmen":   # Mehrkammerprofil: Querschnittsanteil gegenüber Vollprofil (30 x h): 2 Gurte + (Kammern+1) Stege
        wr, nk, hr = A["A_seitenrahmen_wand_mm"], int(A["A_seitenrahmen_kammern"]), z_dk - z_ku
        p["mass"] = p["vol"] * rho * (2 * rand * wr + (nk + 1) * (hr - 2 * wr) * wr) / (rand * hr)
    elif g_ == "Pad": p["mass"] = p["vol"] * A["A_dichte_pad_kg_m3"] * 1e-9
    elif g_ == "Zelltraeger": p["mass"] = p["vol"] * A["A_dichte_zelltraeger_kg_m3"] * 1e-9
    elif g_ == "Verguss": p["mass"] = p["vol"] * A["A_dichte_verguss_kg_m3"] * 1e-9
    elif p["mass"] is None and p["mat"].startswith("Al"): p["mass"] = p["vol"] * rho
    p["com"] = com(p["shape"])
tot = sum(p["mass"] for p in teile if p["mass"] is not None)
cg = [sum(p["mass"] * p["com"][i] for p in teile if p["mass"] is not None) / tot for i in range(3)]
gm = {}
for p in teile:
    g = gm.setdefault(p["grp"], dict(anzahl=0, volumen_cm3=0.0, masse_kg=0.0, masse_bekannt=True, werkstoff=p["mat"]))
    g["anzahl"] += 1; g["volumen_cm3"] += p["vol"] / 1e3
    if p["mass"] is None: g["masse_bekannt"] = False
    else: g["masse_kg"] += p["mass"]

# ---- Kollisionsprüfung: Paare mit überlappender Bounding Box (> 1e-3 mm), dann Schnittvolumen
bb = np.array([[p["shape"].BoundBox.XMin, p["shape"].BoundBox.YMin, p["shape"].BoundBox.ZMin, p["shape"].BoundBox.XMax, p["shape"].BoundBox.YMax, p["shape"].BoundBox.ZMax] for p in teile])
tol = 1e-3; N = len(teile); paare = 0; koll = []; tmax = 0.0
for i in range(N):
    ov = (bb[i, 3] - tol > bb[i + 1:, 0]) & (bb[i, 0] + tol < bb[i + 1:, 3]) & (bb[i, 4] - tol > bb[i + 1:, 1]) & (bb[i, 1] + tol < bb[i + 1:, 4]) & (bb[i, 5] - tol > bb[i + 1:, 2]) & (bb[i, 2] + tol < bb[i + 1:, 5])
    for j in np.nonzero(ov)[0] + i + 1:
        a, b = teile[i], teile[j]
        if a["grp"] == b["grp"] == "Zellen" and False: continue
        paare += 1
        vol = a["shape"].common(b["shape"]).Volume
        if vol > 1e-6: koll.append(dict(a=a["name"], b=b["name"], volumen_mm3=vol))
bbA = FreeCAD.BoundBox(); [bbA.add(p["shape"].BoundBox) for p in teile]
doc = FreeCAD.newDocument(f"pack_{VO}")
gruppen = {}
for p in teile: gruppen.setdefault(p["grp"], []).append(p["shape"])
for g, sh in gruppen.items(): doc.addObject("Part::Feature", g).Shape = Part.makeCompound(sh)
doc.recompute(); doc.saveAs(f"{OUT}/pack_{VO}.FCStd"); Part.export(list(doc.Objects), f"{OUT}/pack_{VO}.step")
def netz(sel, datei):
    m = {}
    for g in gruppen:
        pts_all, tri_all = [], []
        for p in teile:
            if p["grp"] != g or not sel(p): continue
            s = p["shape"]
            if p.get("cut") is not None: s = p["cut"]
            pts, tri = s.tessellate(1.0 if g != "Zellen" else 2.0)
            o = len(pts_all); pts_all += [[q.x, q.y, q.z] for q in pts]; tri_all += [[a + o for a in t3] for t3 in tri]
        m[g] = {"punkte": pts_all, "dreiecke": tri_all}
    json.dump(m, open(datei, "w"))
netz(lambda p: True, f"{OUT}/netz_{VO}.json")
# Schnitte: Bereich (Box) wird entfernt; Zellen/Verbinder mit Mittelpunkt im Bereich entfallen, Platten/Profile werden geschnitten
def schnitt(box_, datei):
    m = {}; cs = {}
    for p in teile:
        c = p["shape"].BoundBox.Center
        inb = (box_.XMin <= c.x <= box_.XMax and box_.YMin <= c.y <= box_.YMax)
        if p["grp"] in ("Zellen", "Zellverbinder", "Zellabgriff", "Gruppenverbinder", "Gruppenbruecke", "E2_CMU", "E2_FPC"):
            cs[p["name"]] = None if inb else p["shape"]
        else: cs[p["name"]] = p["shape"].cut(Part.makeBox(box_.XLength, box_.YLength, bbA.ZMax + 2, V(box_.XMin, box_.YMin, -1)))
    for g in gruppen:
        pts_all, tri_all = [], []
        for p in teile:
            sh = cs[p["name"]]
            if p["grp"] != g or sh is None or not sh.Solids: continue
            pts, tri = sh.tessellate(1.0 if g != "Zellen" else 2.0)
            o = len(pts_all); pts_all += [[q.x, q.y, q.z] for q in pts]; tri_all += [[a + o for a in t3] for t3 in tri]
        m[g] = {"punkte": pts_all, "dreiecke": tri_all}
    json.dump(m, open(datei, "w"))
xq = pos_q[1] + qb / 2 if len(pos_q) > 1 else pos_q[0] + qb / 2   # Mitte eines Querträgers
if not E2:
    schnitt(FreeCAD.BoundBox(Lg / 2, -1, -1, Lg + 1, B / 2, H + 1), f"{OUT}/netz_{VO}_schnitt.json")     # Viertel
    zv = [p["shape"].BoundBox.Center.x for p in teile if p["grp"] == "Zellverbinder"]
    xh = (min(zv, key=lambda x: abs(x - (Lg / 2 + 150))) + 3) if zv else Lg / 2 + 150   # LFP: Schnittebene mitten durch einen Zellverbinder
    schnitt(FreeCAD.BoundBox(xh, -1, -1, Lg + 1, B + 1, H + 1), f"{OUT}/netz_{VO}_halb.json")        # Halbschnitt x = Lg/2 (Ansicht "ecke")
    schnitt(FreeCAD.BoundBox(-1, -1, -1, Lg + 1, B / 2, H + 1), f"{OUT}/netz_{VO}_laengs.json")       # Längsschnitt y = B/2
    schnitt(FreeCAD.BoundBox(-1, -1, -1, xq, B + 1, H + 1), f"{OUT}/netz_{VO}_quer.json")            # Querschnitt durch Querträger

if E2:   # Netze für die E2-Bilder (große Dateien nach cae_projekte)
    NZ = "/home/cae/cae_projekte/batterie/e2"; xq = xh = 0.0
    netz(lambda p: p["name"] not in ("Deckel", "Pad_oben", "Kuehlplatte_oben") and p["grp"] != "E2_Schaltbox", f"{NZ}/netz_{VO}_ohnedeckel.json")
    schnitt(FreeCAD.BoundBox(-1, -1, -1, Lg + 1, e2res["schaltbox_x0_y0_z0_mm"][1] + e2res["schaltbox_B_mm"] / 2, bbA.ZMax + 1), f"{NZ}/netz_{VO}_boxschnitt.json")
if E2:
    e2res["masse_elektronik_gesamt_kg"] = sum(g_["masse_kg"] for k_, g_ in gm.items() if k_.startswith("E2") and k_ != "E2_FPC") + e2res["fpc_masse_kg"]   # Box, Inhalt, Stecker, CMU, alle FPC (auch ohne Platz), HV-Leiter (nur Cu)
    e2res["masse_hv_leiter_cu_kg"] = gm.get("E2_HV_Leitung", {}).get("masse_kg", 0.0) + cu_kg(2 * gap)
    e2res["masse_elektronik_ohne_hv_leitungen_kg"] = e2res["masse_elektronik_gesamt_kg"] - gm.get("E2_HV_Leitung", {}).get("masse_kg", 0.0)
    e2res["querverbinder_mitte_al_kg"] = sum(p["mass"] for p in teile if p["name"].startswith("Querverbinder"))   # Box (Al aus Volumen), Inhalt, Stecker, CMU, alle FPC (auch ohne Platz); HV-Leitungen ohne Masse (Dichte fehlt)
res = dict(schnittebene_quer_x_mm=(xq if not E2 else None), schnittebene_halb_x_mm=(xh if not E2 else None), hinweis="KI-generiert, ENTWURF, nicht freigegeben. Erzeugt von cad/pack/pack.py aus cad/pack/entwurf/parameter_%s.json" % VAR,
  variante=VAR, laenge_mm=bbA.XLength, breite_mm=bbA.YLength, hoehe_mm=bbA.ZLength, hoehe_stapel_mm=H, hoehe_max_mm=A["A_hoehe_max_mm"],
  gehaeuse_L_mm=Lg, zellen=len(cells), quertraeger_x_mm=pos_q, zellmasse_je_kg=mcell,
  gruppen=gm, masse_bekannt_kg=tot, schwerpunkt_mm=cg, mitte_mm=[Lg / 2, B / 2], schwerpunkt_abw_mm=[cg[0] - Lg / 2, cg[1] - B / 2],
  teile=len(teile), kollisionspaare_geprueft=paare, kollisionen=koll, anzahl_kollisionen=len(koll), rechenzeit_s=time.time() - t0,
  e2=e2res, annahmen={k: PJ["A"][k] for k in PJ["A"]})
json.dump(res, open(f"{OUT}/ergebnis_{VO}.json", "w"), indent=1, ensure_ascii=False)
print("FERTIG", VAR, "Teile", len(teile), "Paare", paare, "Koll", len(koll), "t", round(time.time() - t0))
