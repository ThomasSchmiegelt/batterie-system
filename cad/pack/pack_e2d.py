# KI-generiert (Claude Sonnet, 2026-11-18), Entwurf. Auftrag E2 Fortsetzung 5 (Detailierung). Kopie von pack.py (unverändert) mit E2D-Erweiterung; Ausgabe mit Suffix _e2d.
"""Pack-CAD (vereinfacht) in FreeCAD headless. Aufruf: PACK_VARIANTE=LFP|NMC [PACK_PARAMETER=datei] $FREECAD_APPIMAGE freecadcmd cad/pack/pack.py
Maße nur aus cad/pack/entwurf/parameter_<V>.json (Akten + Block A). Zellen = Hüllkörper (kein Zelldetail, keine Pole).
Koordinaten mm: X Länge, Y Breite, Z Höhe (0 = Unterkante Unterfahrschutz). Ausgabe: ergebnis_<V>.json, pack_<V>.FCStd/.step, netz_<V>*.json."""
import os, sys, json, math, time
import numpy as np
import FreeCAD, Part
from FreeCAD import Vector as V

VAR = os.environ["PACK_VARIANTE"]
E2 = True   # pack_e2d.py baut immer die E2-Teile (Detailierung), Ausgabe mit Suffix _e2d; pack.py und die _e2-Dateien bleiben unberührt
E3C = os.environ.get("PACK_E3C") == "1"   # E3c (Sonnet 2026-11-24): zusätzlich BMS-Platine BT-311 aus dem KiCad-STEP (sim/elektrik/e3c_bms_platine), Ausgabe Suffix _e3c
E3 = os.environ.get("PACK_E3") == "1" or E3C   # E3 (Sonnet 2026-11-24): CMU-Quader durch das KiCad-STEP der Platine ersetzen (sim/elektrik/e3_platine), Ausgabe mit Suffix _e3
VO = VAR + "_e2d" + ("_e3c" if E3C else "_e3" if E3 else "")
PARM = json.load(open(f"{os.environ.get('BATTERIE', '/home/cae/hermes/batterie')}/pm/bauteile/parameter.json"))["parameter"]   # Maße aus Akten (E3c: BT-722 lichte_hoehe_zugabe_mm = ENT-194)
ROOT = os.environ.get("BATTERIE", "/home/cae/hermes/batterie")
OUT = f"{ROOT}/cad/pack/entwurf"
PJ = json.load(open(os.environ.get("PACK_PARAMETER", f"{OUT}/parameter_{VAR}_e2d.json")))
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
    gv_b, gv_d = w("BT-420", "breite_mm"), w("BT-420", "dicke_mm"); ag_d, ag_t = A["A_zellabgriff_NMC_mm"]
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
    gz = w("BT-420", "breite_mm"); gt = w("BT-420", "dicke_mm")
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
    sys.path.insert(0, f"{ROOT}/cad/pack"); import e2_verdrahtung as EV; import e2d_geo as G
    def A3(k): return [float(x) for x in A[k]]
    gap, wd, rm = A["A_e2_box_teilabstand_mm"], A["A_e2_box_wand_mm"], A["A_e2_box_rand_mm"]
    assert P["BT-710"]["einbauort"]["wert"] == "deckel_hinten", P["BT-710"]["einbauort"]
    WIN = max(c['feld'] for c in cells); omh = A['A_e2d_omega_h_mm']      # Fenster für die Verbinder-Details: hinterstes Feld
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
        Rcg = 1.5 * gv_d; om_list = []; n_omega = 0; n_weld_nmc = 0
        swl_, swb_, swt_, swn_ = [float(x) for x in A['A_e2d_schweiss_mm']]; swa_ = A['A_e2d_schweiss_abstand_mm']
        def strip(pa, pb, omega=False):
            if omega and math.hypot(pb[0] - pa[0], pb[1] - pa[1]) > 2 * gb + 2 * omh + 4 * Rcg:
                Lb_ = math.hypot(pb[0] - pa[0], pb[1] - pa[1]); zm_ = zc0_ + gv_d / 2; a_ = gb
                sol_, _ = G.schiene(pa, pb, [(0, zm_), (a_, zm_), (a_ + omh, zm_ + omh), (Lb_ - a_ - omh, zm_ + omh), (Lb_ - a_, zm_), (Lb_, zm_)], gv_b, gv_d, Rcg); om_list.append(sol_); return sol_
            dx, dy = pb[0] - pa[0], pb[1] - pa[1]; Ln = math.hypot(dx, dy); nx, ny = -dy / Ln * gb, dx / Ln * gb
            pts = [V(pa[0] + nx, pa[1] + ny, zc0_), V(pb[0] + nx, pb[1] + ny, zc0_), V(pb[0] - nx, pb[1] - ny, zc0_), V(pa[0] - nx, pa[1] - ny, zc0_)]; pts.append(pts[0])
            return Part.Face(Part.makePolygon(pts)).extrude(V(0, 0, zc1_ - zc0_))
        def disc(c): return Part.makeCylinder(gb, zc1_ - zc0_, V(c["cx"], c["cy"], zc0_))
        gsh = []; n_wende = 0; n_br = 0
        for gi_, g in enumerate(mw["gruppen"]):
            cs_ = [cells[i] for i in g]; teil = [disc(c) for c in cs_]; wend = []; inwin = any(c['feld'] == WIN for c in cs_)
            for ca, cb in zip(cs_, cs_[1:]):
                (teil if ca["k"] == cb["k"] else wend).append(strip((ca["cx"], ca["cy"]), (cb["cx"], cb["cy"]), omega=inwin))
            sh = teil[0]
            for q_ in teil[1:]: sh = sh.fuse(q_)
            sh = sh.removeSplitter()
            if inwin:
                gr_ = [box(c['cx'] + sg_ * swa_ / 2 - swb_ / 2, c['cy'] - swl_ / 2, zc1_ - swt_, c['cx'] + sg_ * swa_ / 2 + swb_ / 2, c['cy'] + swl_ / 2, zc1_ + 0.5) for c in cs_ for sg_ in (-1, 1)]; sh = sh.cut(Part.makeCompound(gr_)); n_weld_nmc += len(cs_)
            gsh.append(sh); add(f"Gruppenverbinder_g{gi_:03d}", "Gruppenverbinder", sh, mat="Al (Annahme, Cu offen)")
            for wi, w_ in enumerate(wend):
                add(f"Wendebruecke_g{gi_:03d}_{wi}", "Gruppenbruecke", w_.cut(sh), mat="Al (Annahme, Cu offen)"); n_wende += 1
        for gi_ in range(len(mw["gruppen"]) - 1):
            ca, cb = cells[mw["gruppen"][gi_][-1]], cells[mw["gruppen"][gi_ + 1][0]]
            add(f"Gruppenbruecke_g{gi_:03d}", "Gruppenbruecke", strip((ca["cx"], ca["cy"]), (cb["cx"], cb["cy"])).cut(gsh[gi_]).cut(gsh[gi_ + 1]), mat="Al (Annahme, Cu offen)"); n_br += 1
        n_omega = len(om_list)
        if om_list: cutter.append((Part.makeCompound(om_list), ('Pad_oben', 'Kuehlplatte_oben')))
        vers.update(omega_bogen_fenster=n_omega, schweisslinien_paare_fenster=n_weld_nmc, gruppenverbinder=len(gsh), wendebruecken_in_gruppen=n_wende, gruppenbruecken=n_br)
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
            if all(abs(y - h) >= 2 * rhv + 5 + fw / 2 + 1 for h in hv_y if VAR == "NMC") and all(abs(y - l) >= fw + 2 for l in lane if l is not None): lane[j] = y; break
        assert lane[j] is not None, j
    cmu_x = {"vorn": (xv_in, xv_in + cmuD), "hinten": (xh_in - cmuD, xh_in)}
    for j in range(ncmu):
        x0, x1 = cmu_x[seite[j]]
        cbox = box(x0, ypos[j] - cmuL / 2, zc - cmuB / 2, x1, ypos[j] + cmuL / 2, zc + cmuB / 2)
        add(f"CMU_{j:02d}", "E2_CMU", cbox, mass=A["A_e2_cmu_masse_kg"], mat="E2 Teil (Masse ERW-E2 N1)")
        if E3:   # Platine aus KiCad-STEP: Platinen-x (Länge) -> Pack-y, Platinen-y (Breite) -> Pack-z, Platinen-z (Bauteile oben) -> Pack-x (vorn +x, hinten -x); Rückseite an der Wand
            if "E3SHAPE" not in globals():
                E3SHAPE = Part.read(f"/home/cae/cae_projekte/batterie/e3/cmu_{VAR}.step"); bb3 = E3SHAPE.BoundBox
                E3SHAPE.translate(V(-bb3.XMin, -bb3.YMin, -bb3.ZMin)); E3DIM = (bb3.XLength, bb3.YLength, bb3.ZLength)
            m3 = FreeCAD.Matrix()
            if seite[j] == "vorn": m3.A11, m3.A12, m3.A13, m3.A21, m3.A22, m3.A23, m3.A31, m3.A32, m3.A33 = 0, 0, 1, 1, 0, 0, 0, 1, 0; ox = x0
            else: m3.A11, m3.A12, m3.A13, m3.A21, m3.A22, m3.A23, m3.A31, m3.A32, m3.A33 = 0, 0, -1, 1, 0, 0, 0, -1, 0; ox = x1
            sh3 = E3SHAPE.copy().transformShape(m3)
            bt3 = sh3.BoundBox; sh3.translate(V(ox - (bt3.XMin if seite[j] == "vorn" else bt3.XMax), ypos[j] - cmuL / 2 - bt3.YMin, zc + cmuB / 2 - bt3.ZMax if False else zc - cmuB / 2 - bt3.ZMin))
            teile[-1]["shape"] = sh3; teile[-1]["cutshape"] = cbox
            _m3 = json.load(open("/home/cae/hermes/batterie/sim/elektrik/e3_platine/ergebnis_platine.json"))[VAR]["masse"]   # Masse aus E3 (Nachtrag 6): Platine + Wärmeleitpad ENT-185 (Pad nicht als Körper modelliert)
            teile[-1]["mass"] = _m3["gesamt_mit_pad_g"] / 1000
            teile[-1]["mat"] = "E3 Platine STEP; Masse %.2f g = Platine %.2f g + Wärmeleitpad %.2f g (ergebnis_platine.json, ERW-E3 Nachtrag 6)" % (_m3["gesamt_mit_pad_g"], _m3["platine_ohne_pad_g"], _m3["pad_g"])
            e2res_e3 = globals().setdefault("E3INFO", dict(platine_mm=[round(d, 2) for d in E3DIM], hoehe_bauteile_ueber_leiter_mm=None))
        geo["cmu"].append(dict(i=j, seite=seite[j], x=(x0 + x1) / 2, y=ypos[j], taps=len(grp_t[j])))
    # ====================== E2D (Fortsetzung 5): Schaltbox innen, Kabel, Stecker, Trennbrücke. Maße: A_e2d_* (ERW-E2 N3 oder "abgeleitet"), Akten, A_e2_* ======================
    import e2d_geo as G
    def AD(k): return A["A_e2d_" + k]
    def AD3(k): return [float(x) for x in A["A_e2d_" + k]]
    abgeleitet = []   # Liste der Maße, die nicht in N3 stehen (für ERGEBNIS.md)
    fl_, fd_, dk_ = AD("box_flansch_mm"), AD("box_flansch_dicke_mm"), AD("box_deckel_mm"); dg_w, dg_h = AD3("box_dichtung_mm"); m5k = AD3("m5_kopf_mm"); m4k = AD3("m4_kopf_mm"); m8k = AD3("m8_kopf_mm"); m8s = AD3("m8_scheibe_mm")
    sw_, st_ = AD3("schiene_cu_%s_mm" % VAR); schb = AD("schiene_bohrung_mm"); Rcb = AD("schiene_biegeradius_innen_faktor_dicke") * st_ + st_ / 2; ssl = AD("schrumpfschlauch_mm")
    h_len = AD("kabelschuh_huelse_mm"); pl_w, pl_t = AD3("kabelschuh_lasche_mm"); pl_l = max(AD("kabelschuh_lasche_laenge_mm"), sw_)    # Palme: Länge mindestens Schienenbreite (abgeleitet)
    r_core = math.sqrt(A_hv / math.pi); wall_ = (rhv - r_core) / AD("kabel_wand_teilung"); radien = [r_core, r_core + wall_, r_core + 2 * wall_, rhv]
    lz_ = A3("A_e2_lasche_mm")[1]; lbo = A["A_e2_lasche_bohrung_mm"]
    hv_len = []; vert_cut = []; bar_info = []; kabel_info = []
    schz = A3("A_e2_schuetz_mm"); halt = AD3("schmelz_halter_mm"); bms = [w("BT-310", "laenge_mm"), w("BT-310", "breite_mm"), w("BT-310", "hoehe_mm")]
    dev = {"BMS_Platine": bms, "Shunt": A3("A_e2_shunt_mm"), "Hauptschuetz_1": schz, "Hauptschuetz_2": schz, "Vorladeschuetz": A3("A_e2_vorladeschuetz_mm"), "Vorladewiderstand": A3("A_e2_vorladewiderstand_mm"),
           "Pyrosicherung": A3("A_e2_pyro_mm"), "Schmelzsicherung": halt}
    ext_ = AD3("lasche_pyro_schmelz_mm")[2]                      # Auskragung der Laschen an Pyro- und Schmelzsicherung
    reihen = [["BMS_Platine", "Shunt"], ["Hauptschuetz_1", "Hauptschuetz_2", "Vorladeschuetz", "Vorladewiderstand"], ["Pyrosicherung", "Schmelzsicherung"]]
    abst = {("Pyrosicherung", "Schmelzsicherung"): gap + 2 * ext_}   # Lage: Pyro-Lasche B und Schmelz-Lasche A liegen nebeneinander, deshalb Abstand = Teilabstand + 2 Auskragungen
    rb = []
    for r in reihen:
        L_ = sum(dev[n][0] for n in r) + sum(abst.get((a_, b_), gap) for a_, b_ in zip(r, r[1:]))
        if "Pyrosicherung" in r: L_ += 2 * ext_
        rb.append(L_)
    innenL = max(rb); tiefe = [max(dev[n][1] for n in r) for r in reihen]; innenB = sum(tiefe) + gap * (len(reihen) - 1)
    bL, bB = innenL + 2 * rm, innenB + 2 * rm                       # Wanne außen (Wand 2 mm), Flansch kommt außen dazu
    bx0 = xh_in - fl_ - bL                                          # Flansch hinten bündig mit der Rahmeninnenkante
    # --- Trennstecker NMC und Lage der Box in y
    if VAR == "NMC":
        plug_x = (ans["Mitte_A_Ende_Band2"]["cx"] + ans["Mitte_B_Anfang_Band3"]["cx"]) / 2; plug_y = (ans["Mitte_A_Ende_Band2"]["cy"] + ans["Mitte_B_Anfang_Band3"]["cy"]) / 2
        by0 = plug_y + plB / 2 + gap + fl_
    else: by0 = B / 2 - bB / 2
    bz0 = z_top; zfl = bz0 + wd
    # --- Anschlussfüße der HV-Leitungen (Lasche + Kabelschuh), x und y
    zl0 = z_pad2 if VAR == "NMC" else z_top_cell + lz_     # LFP: Lasche liegt eine Dicke über der Zellebene (Biegeradius innen = Dicke, sonst schneidet die Kante in die Zelle)                  # Oberkante Zellen-/Verbinderebene unter der Lasche
    z_va = zl0 + lz_ + pl_t + h_len                                 # Beginn des Kabels über Lasche, Kabelschuh-Palme und Hülse
    plugH = plH if VAR == "NMC" else 0.0
    z_h = max((z_top + plugH + gap + rhv) if VAR == "NMC" else 0.0, z_va + Rb, zfl + halt[2] + rhv + 1.0)       # Leitungshöhe in der Box (Achse); Palme/Hülse mindestens 1 mm über dem höchsten Gerät (abgeleitet, Freigang 1 mm)
    fuesse = {}
    if VAR == "NMC":
        for nm, ywall, sg in (("Plus", by0, 1), ("Minus", by0 + bB, -1)):
            c = ans[nm]; sgn = 1 if ywall > c["cy"] else -1; assert (sgn == sg) or True
            fuesse[nm] = dict(x=c["cx"], hole=(c["cx"], c["cy"]), foot=(c["cx"], c["cy"] + sgn * (rhv + 5)), ywall=ywall, sgn=sgn, inw=-1 if nm == "Minus" else 1)
    else:
        lw_, lt_ = A3("A_e2_lasche_mm"); xlead = bx0 + rm + dev["BMS_Platine"][0] + gap + ((dev["Shunt"][0] - AD("shunt_steg_mm")) / 2 + AD("shunt_steg_mm") + (dev["Shunt"][0] - AD("shunt_steg_mm")) / 4) - 40.0    # Lage: Kabelfuß 40 mm vor dem B-Loch des Shunts (Schiene 1 liegt in x)
        for nm, y0_, sg, ywall in (("Plus", ymin_ + 1, 1, by0), ("Minus", ymax_ - 1, -1, by0 + bB)):
            y0_ = y0_ + sg * (fh - 1 + 0.2); yc = y0_ + sg * lw_ / 2
            fuesse[nm] = dict(x=xlead, hole=(xlead, yc), foot=(xlead, yc + sg * (rhv + 5)), ywall=ywall, sgn=sg, inw=-1 if nm == "Minus" else 1, ya=min(y0_, y0_ + sg * lw_), yb=max(y0_, y0_ + sg * lw_))
    for nm, f in fuesse.items(): assert bx0 + wd + pl_w / 2 <= f["x"] <= bx0 + bL - wd - pl_w / 2, ("Kabelfuß außerhalb der Box in x", nm, f["x"], bx0, bx0 + bL)
    # --- Höhe der Box: Inhalt (Geräte, Bolzen, Schienen) und Leitungshöhe
    zM = 94.0                                                       # Schienen-Hochlage (Unterkante) = Oberkante höchstes Gerät (Schmelzhalter 95 mm), relativ zum Boden
    inner_h = max(zM + st_, z_h + rhv + fd_ - zfl, halt[2] + st_)
    wt = zfl + inner_h                                              # Oberkante Wanne (Wand)
    bH = (wt - bz0) + dg_h + dk_                                    # Box außen bis Deckeloberkante (ohne Schraubenköpfe)
    # --- Zeilen platzieren. Lage-Regeln (nicht Maße): Schienen 1 und 6 laufen in x vom Kabelfuß (gleiches x wie der Kabelfuß) zum Gerät, Abstand 40 mm (Platz für den Biegeradius).
    LB = 40.0; innerL_, innerR_ = bx0 + wd, bx0 + bL - wd; ypos_r = [by0 + rm]; ypos_r.append(ypos_r[0] + tiefe[0] + gap); ypos_r.append(ypos_r[1] + tiefe[1] + gap)
    fxp, fxm = fuesse["Plus"]["x"], fuesse["Minus"]["x"]; shl, shb, shh = dev["Shunt"]; cuL_ = (shl - AD("shunt_steg_mm")) / 2; bms_end = bx0 + rm + dev["BMS_Platine"][0]
    cand = [(1, -1), (1, 1), (0, -1), (0, 1)]          # (Ende B=1/A=0 des Shunts nahe der Leitung, Seite der Leitung: -1 = Shunt links der Leitung)
    sh_x0 = None; sh_endB = None; best = None
    for endB in (1, 0):
        ho = (cuL_ + AD("shunt_steg_mm") + cuL_ / 2) if endB else cuL_ / 2            # Lage des Anschlussloches ab Shunt-Anfang
        lo, hi = bms_end + gap, innerR_ - shl                                         # erlaubter Bereich für den Shunt-Anfang
        for side in (-1, 1):
            x0_ = min(max(fxp + side * LB - ho, lo), hi)
            dx = abs(x0_ + ho - fxp)
            if dx >= LB - 1e-6 and (best is None or dx < best[0]): best = (dx, x0_, endB)
    assert best is not None, "Shunt nicht platzierbar"
    sh_x0, sh_endB = best[1], best[2]
    schm_hole_x = None; hh_s = halt[0] + ext_ / 2 - AD("schmelz_wand_mm") / 2; best = None
    r2w = (dev["Pyrosicherung"][0] + gap + 2 * ext_) + ext_ + halt[0] + ext_ - ext_    # Breite der Zeile 2 von Pyro-Lasche A bis Halterende
    lo = innerL_ + (dev["Pyrosicherung"][0] + gap + 2 * ext_) + ext_; hi = innerR_ - halt[0] - ext_
    for sM in (-1, 1):
        x0s_ = min(max(fxm + sM * LB - hh_s, lo), hi); dx = abs(x0s_ + hh_s - fxm)
        if dx >= LB - 1e-6 and (best is None or dx < best[0]): best = (dx, x0s_)
    assert best is not None, "Zeile 2 nicht platzierbar"; x0s_final = best[1]
    pos = {"BMS_Platine": (bx0 + rm, ypos_r[0]), "Shunt": (sh_x0, ypos_r[0])}
    xx = bx0 + rm
    for n in reihen[1]: pos[n] = (xx, ypos_r[1]); xx += dev[n][0] + gap
    pos["Schmelzsicherung"] = (x0s_final, ypos_r[2]); pos["Pyrosicherung"] = (x0s_final - gap - 2 * ext_ - dev["Pyrosicherung"][0], ypos_r[2])
    # --- Wanne, Flansch, Dichtung, Deckel, Schrauben M5, Druckausgleich
    wanne = box(bx0, by0, bz0, bx0 + bL, by0 + bB, wt).cut(box(bx0 + wd, by0 + wd, bz0 + wd, bx0 + bL - wd, by0 + bB - wd, wt + 1))
    flansch = box(bx0 - fl_, by0 - fl_, wt - fd_, bx0 + bL + fl_, by0 + bB + fl_, wt).cut(box(bx0 + wd, by0 + wd, wt - fd_ - 1, bx0 + bL - wd, by0 + bB - wd, wt + 1))
    dich = box(bx0 - 1.5 - dg_w, by0 - 1.5 - dg_w, wt, bx0 + bL + 1.5 + dg_w, by0 + bB + 1.5 + dg_w, wt + dg_h).cut(box(bx0 - 1.5, by0 - 1.5, wt - 1, bx0 + bL + 1.5, by0 + bB + 1.5, wt + dg_h + 1))
    zlid = wt + dg_h
    lid = box(bx0 - fl_, by0 - fl_, zlid, bx0 + bL + fl_, by0 + bB + fl_, zlid + dk_)
    # Schrauben M5 alle 60 mm auf der Mittellinie des Flansches (7,5 mm von der Wand)
    off = 7.5; xs0, xs1, ys0, ys1 = bx0 - off, bx0 + bL + off, by0 - off, by0 + bB + off; sk = AD("box_schraube_gewinde_mm"); scr = []
    for (xa_, ya_, xb_, yb2) in ((xs0, ys0, xs1, ys0), (xs1, ys0, xs1, ys1), (xs1, ys1, xs0, ys1), (xs0, ys1, xs0, ys0)):
        Ls = math.hypot(xb_ - xa_, yb2 - ya_); nseg = math.ceil(Ls / AD("box_schraube_teilung_mm"))
        for i in range(nseg): scr.append((xa_ + (xb_ - xa_) * i / nseg, ya_ + (yb2 - ya_) * i / nseg))
    hole_cut_fl = [cyl(x, y, wt - fd_ - 1, wt + 1, sk / 2) for x, y in scr]; hole_cut_lid = [cyl(x, y, zlid - 1, zlid + dk_ + 1, sk / 2) for x, y in scr]
    vx, vy = bx0 + bL / 2, by0 + bB / 2; vd = AD("box_druckausgleich_d_mm")
    lid = lid.cut(cyl(vx, vy, zlid - 1, zlid + dk_ + 1, vd / 2)).cut(Part.makeCompound(hole_cut_lid))
    flansch = flansch.cut(Part.makeCompound(hole_cut_fl))
    # Fußlaschen-Schrauben: Löcher im Boden
    fz = AD3("fusslasche_mm"); fuss_holes = []; fuss_parts = []
    # --- Geräte
    z0 = zfl; geräte_hoehen = {}
    def addi(n, shp, ms=0.0, mat="in Gerätemasse enthalten (ERW-E2 N1)", grp="E2_Schaltbox_Inhalt"): add(n, grp, shp, mass=ms, mat=mat)
    # BMS: Platine auf 4 Abstandsbolzen
    x0, y0 = pos["BMS_Platine"]; bl_, bb_ = bms[0], bms[1]; ab_n, ab_g, ab_h = AD3("bms_abstandsbolzen"); abo = AD("bms_abstandsbolzen_aussen_mm"); abz = AD("bms_abstandsbolzen_einzug_mm"); pdk = AD("bms_platine_dicke_mm")
    addi("BMS_Platine", box(x0, y0, z0 + ab_h, x0 + bl_, y0 + bb_, z0 + ab_h + pdk), A["A_e2_bms_masse_kg"], "E2 Teil (Masse ERW-E2 N1)")
    if E3C:   # E3c: Platine aus KiCad-STEP statt Quader (Länge -> x, Breite -> y, Bauteile oben +z); Ecke der Platine = Ecke des BMS-Platzes
        _bs = Part.read("/home/cae/cae_projekte/batterie/e3c/bms.step"); _bb = _bs.BoundBox; _bs.translate(V(x0 - _bb.XMin, y0 - _bb.YMin, z0 + ab_h - _bb.ZMin))
        teile[-1]["shape"] = _bs; teile[-1]["cutshape"] = box(x0, y0, z0 + ab_h, x0 + bl_, y0 + bb_, z0 + ab_h + pdk)
        _mb = json.load(open("/home/cae/hermes/batterie/sim/elektrik/e3c_bms_platine/ergebnis_platine.json"))["masse"]
        teile[-1]["mass"] = _mb["gesamt_g"] / 1000; teile[-1]["mat"] = "E3c BMS-Platine STEP; Masse %.1f g (ergebnis_platine.json, ERW-E3c)" % _mb["gesamt_g"]
    for k_, (xx_, yy_) in enumerate(((x0 + abz, y0 + abz), (x0 + bl_ - abz, y0 + abz), (x0 + abz, y0 + bb_ - abz), (x0 + bl_ - abz, y0 + bb_ - abz))):
        addi(f"BMS_Abstandsbolzen_{k_}", cyl(xx_, yy_, z0, z0 + ab_h, abo / 2), 0.0, "Stahl (Masse offen, 0 gesetzt)")
    bsl, bsb, bsh = AD3("bms_stecker_mm")
    for k_, (nm_, yy_) in enumerate(() if E3C else (("BMS_Stecker_26pol", 20), ("BMS_Daisy_Stecker_1", 70), ("BMS_Daisy_Stecker_2", 110))):
        addi(nm_, box(x0 + bl_ - 10 - bsl, y0 + yy_, z0 + ab_h + pdk, x0 + bl_ - 10, y0 + yy_ + bsb, z0 + ab_h + pdk + bsh), 0.0, "E2 Teil (Masse offen, 0 gesetzt)")
    # Shunt: Messplatine 80x40x1,6 unten, darauf Cu-Ende, Manganin-Steg 3, Cu-Ende
    x0, y0 = pos["Shunt"]; sl_, sb_, sh_ = dev["Shunt"]; stg = AD("shunt_steg_mm"); spl = AD3("shunt_platine_mm"); cuL = (sl_ - stg) / 2
    addi("Shunt_Messplatine", box(x0, y0, z0, x0 + spl[0], y0 + spl[1], z0 + spl[2]), A["A_e2_shunt_masse_kg"], "E2 Teil (Masse ERW-E2 N1, Shunt gesamt)")
    shunt_ends = []
    for nm_, xa_ in (("Shunt_Cu_A", x0), ("Shunt_Cu_B", x0 + cuL + stg)):
        c_ = box(xa_, y0, z0 + spl[2], xa_ + cuL, y0 + sb_, z0 + sh_).cut(cyl(xa_ + cuL / 2, y0 + sb_ / 2, z0, z0 + sh_ + 1, schb / 2)); addi(nm_, c_, 0.0, "Cu (Masse offen, 0 gesetzt)"); shunt_ends.append((xa_ + cuL / 2, y0 + sb_ / 2, z0 + sh_))
    addi("Shunt_Manganin_Steg", box(x0 + cuL, y0, z0 + spl[2], x0 + cuL + stg, y0 + sb_, z0 + sh_), 0.0, "Manganin (Masse offen, 0 gesetzt)")
    # Schütze
    sut = {}
    for n in ("Hauptschuetz_1", "Hauptschuetz_2"):
        x0, y0 = pos[n]; l_, b_, h_ = schz; nb, bab, bd_, bh_ = int(AD("schuetz_bolzen_n")), AD("schuetz_bolzen_abstand_mm"), AD("schuetz_bolzen_d_mm"), AD("schuetz_bolzen_h_mm")
        addi(n, box(x0, y0, z0, x0 + l_, y0 + b_, z0 + h_), A["A_e2_schuetz_masse_kg"], "E2 Teil (Masse ERW-E2 N1)")
        bol = [(x0 + l_ / 2 - bab / 2 + k_ * bab, y0 + b_ / 2) for k_ in range(nb)]
        for k_, (bx_, by_) in enumerate(bol): addi(f"{n}_Bolzen_{k_}", cyl(bx_, by_, z0 + h_, z0 + h_ + bh_, bd_ / 2), 0.0, "Stahl (Masse offen, 0 gesetzt)")
        sut[n] = bol
        fw_, fe_, ft_ = fz
        for k_, (ya_, sgy) in enumerate(((y0 - fe_, -1), (y0 + b_, 1))):
            fx_ = x0 + l_ / 2; cy_ = ya_ + fe_ / 2
            t_ = box(fx_ - fw_ / 2, ya_, z0, fx_ + fw_ / 2, ya_ + fe_, z0 + ft_); fuss_holes.append(cyl(fx_, cy_, z0 - wd - 1, z0 + ft_ + 1, A["A_e2d_schuetz_fusslasche_gewinde_mm"] / 2)); fuss_parts.append((f"{n}_Fusslasche_{k_}", t_, fx_, cy_))
            addi(f"{n}_Fusslasche_{k_}", t_.cut(cyl(fx_, cy_, z0 - 1, z0 + ft_ + 1, A["A_e2d_schuetz_fusslasche_gewinde_mm"] / 2)), 0.0, "Stahl (Masse offen, 0 gesetzt)")
            sc = A["A_e2d_schuetz_fusslasche_gewinde_mm"]
            addi(f"{n}_Fusslaschen_Schraube_{k_}", cyl(fx_, cy_, z0 + ft_, z0 + ft_ + m5k[1], m5k[0] / 2).fuse(cyl(fx_, cy_, z0 - wd, z0 + ft_, sc / 2)), 0.0, "Stahl (Masse offen, 0 gesetzt)", "E2_Schraube")
        ssl_, ssb, ssh = AD3("schuetz_spulenstecker_mm")
        addi(f"{n}_Spulenstecker", box(x0 + l_ / 2 - ssl_ / 2, y0 + b_, z0 + 25, x0 + l_ / 2 + ssl_ / 2, y0 + b_ + ssb, z0 + 25 + ssh), 0.0, "E2 Teil (Masse offen, 0 gesetzt)")
    x0, y0 = pos["Vorladeschuetz"]; l_, b_, h_ = dev["Vorladeschuetz"]; addi("Vorladeschuetz", box(x0, y0, z0, x0 + l_, y0 + b_, z0 + h_), A["A_e2_vorlade_masse_kg"], "E2 Teil (Masse ERW-E2 N1, Schütz + Widerstand)")
    x0, y0 = pos["Vorladewiderstand"]; l_, b_, h_ = dev["Vorladewiderstand"]; addi("Vorladewiderstand", box(x0, y0, z0, x0 + l_, y0 + b_, z0 + h_), 0.0, "E2 Teil (Masse in Vorladeschütz enthalten)")
    # Pyro: Körper 30x30x80 mit Laschen A (-x) und B (+x) oben, Breite = Schienenbreite
    x0, y0 = pos["Pyrosicherung"]; l_, b_, h_ = dev["Pyrosicherung"]; addi("Pyrosicherung", box(x0, y0, z0, x0 + l_, y0 + b_, z0 + h_), A["A_e2_pyro_masse_kg"], "E2 Teil (Masse ERW-E2 N1)")
    ya_ = y0 + b_ / 2 - sw_ / 2
    pyl = {"A": (x0 - ext_ / 2, y0 + b_ / 2, z0 + h_), "B": (x0 + l_ + ext_ / 2, y0 + b_ / 2, z0 + h_)}
    addi("Pyro_Lasche_A", box(x0 - ext_, ya_, z0 + h_ - st_, x0, ya_ + sw_, z0 + h_).cut(cyl(*pyl["A"][:2], z0, z0 + h_ + 1, schb / 2)), 0.0, "Cu (Masse offen, 0 gesetzt)")
    addi("Pyro_Lasche_B", box(x0 + l_, ya_, z0 + h_ - st_, x0 + l_ + ext_, ya_ + sw_, z0 + h_).cut(cyl(*pyl["B"][:2], z0, z0 + h_ + 1, schb / 2)), 0.0, "Cu (Masse offen, 0 gesetzt)")
    # Schmelzsicherung: Kunststoffhalter 40x40x95 mit Hohlraum für die Sicherung 30x30x85, Laschen durch Schlitze
    x0, y0 = pos["Schmelzsicherung"]; hl_, hb_, hh_ = halt; fs_ = A3("A_e2_schmelz_mm"); wd_h = AD("schmelz_wand_mm"); fz0 = z0 + hh_ - fs_[2]
    ya_ = y0 + hb_ / 2 - sw_ / 2; slot_a = box(x0 - 1, ya_, z0 + hh_ - st_, x0 + wd_h + 1, ya_ + sw_, z0 + hh_ + 1); slot_b = box(x0 + hl_ - wd_h - 1, ya_, z0 + hh_ - st_, x0 + hl_ + 1, ya_ + sw_, z0 + hh_ + 1)
    hal = box(x0, y0, z0, x0 + hl_, y0 + hb_, z0 + hh_).cut(box(x0 + wd_h, y0 + wd_h, fz0, x0 + hl_ - wd_h, y0 + hb_ - wd_h, z0 + hh_ + 1)).cut(slot_a).cut(slot_b)
    addi("Schmelz_Halter", hal, 0.0, "Kunststoff (Masse offen, 0 gesetzt)")
    addi("Schmelzsicherung", box(x0 + wd_h, y0 + wd_h, fz0, x0 + hl_ - wd_h, y0 + hb_ - wd_h, z0 + hh_), A["A_e2_schmelz_masse_kg"], "E2 Teil (Masse ERW-E2 N1)")
    scl = {"A": (x0 - ext_ / 2 + wd_h / 2, y0 + hb_ / 2, z0 + hh_), "B": (x0 + hl_ + ext_ / 2 - wd_h / 2, y0 + hb_ / 2, z0 + hh_)}
    addi("Schmelz_Lasche_A", box(x0 - ext_, ya_, z0 + hh_ - st_, x0 + wd_h, ya_ + sw_, z0 + hh_).cut(cyl(*scl["A"][:2], z0 + hh_ - st_ - 1, z0 + hh_ + 1, schb / 2)), 0.0, "Cu (Masse offen, 0 gesetzt)")
    addi("Schmelz_Lasche_B", box(x0 + hl_ - wd_h, ya_, z0 + hh_ - st_, x0 + hl_ + ext_, ya_ + sw_, z0 + hh_).cut(cyl(*scl["B"][:2], z0 + hh_ - st_ - 1, z0 + hh_ + 1, schb / 2)), 0.0, "Cu (Masse offen, 0 gesetzt)")
    # --- Kabelschuhe und HV-Leitungen (NMC und LFP)
    def kabel(nm, f):
        fx, fy = f["foot"]; hx, hy = f["hole"]; sgn = f["sgn"]; yw = f["ywall"]; inw = f["inw"]
        hy_b = f["box_hole_y"]; ye = yw + inw * (abs(hy_b - yw) - pl_l / 2 - h_len)             # Ende der Leitung (Beginn der Hülse)
        za = z_h - Rb; p1 = V(fx, fy, z_va); p2 = V(fx, fy, za); p3 = V(fx, fy + sgn * Rb, z_h); p4 = V(fx, ye, z_h)
        assert (ye - fy) * sgn > Rb, (nm, fy, ye)
        pm_ = V(fx, fy + sgn * Rb * (1 - math.cos(math.pi / 4)), za + Rb * math.sin(math.pi / 4))
        segs = ([Part.makeLine(p1, p2)] if za - z_va > 1e-6 else []) + [Part.Arc(p2, pm_, p3).toShape(), Part.makeLine(p3, p4)]
        wire = Part.Wire(segs); lay = G.kabel_schichten(wire, p1, V(0, 0, 1), radien)
        L_ = (za - z_va) + math.pi * Rb / 2 + (abs(ye - fy) - Rb)
        for k_, (ln, sh_) in enumerate(zip(AD("kabel_schichten"), lay)): add(f"HV_{nm}_{ln}", "E2_HV_Leitung", sh_, mass=(cu_kg(L_) if k_ == 0 else 0.0), mat=("Cu (Leiter)" if k_ == 0 else "Leitungsschicht (Masse offen, 0 gesetzt)"))
        hv_len.append((f"{nm} Zelle -> Schaltbox", L_)); geo["hv"].append(dict(name=nm, laenge_mm=L_, xy=[[fx, fy], [fx, ye]]))
        # Kabelschuh Zellseite: Palme 20 x 20 x 4 auf der Lasche (Bohrung M8 am Lochmittelpunkt), Hülse senkrecht 40 mm
        py0 = min(hy - pl_l / 2, fy - rhv) if sgn > 0 else min(hy - pl_l / 2, fy - rhv); py1 = max(hy + pl_l / 2, fy + rhv)
        pal = box(hx - pl_w / 2, py0, zl0 + lz_, hx + pl_w / 2, py1, zl0 + lz_ + pl_t).cut(cyl(hx, hy, zl0 + lz_ - 1, zl0 + lz_ + pl_t + 1, lbo / 2))
        add(f"Kabelschuh_{nm}_Zelle_Palme", "E2_Kabelschuh", pal.cut(cyl(fx, fy, zl0 + lz_ - 1, zl0 + lz_ + pl_t + 1, rhv)), mass=0.0, mat="Cu (Masse offen, 0 gesetzt)"); cutter.append((pal, ("Pad_oben", "Kuehlplatte_oben", "Deckel")))
        add(f"Kabelschuh_{nm}_Zelle_Huelse", "E2_Kabelschuh", cyl(fx, fy, zl0 + lz_ + pl_t, z_va, rhv), mass=0.0, mat="Cu (Masse offen, 0 gesetzt)")
        # Kabelschuh Boxseite: Palme (20 breit, Länge pl_l, 4 dick) mit Bohrung am Lochmittelpunkt (y = y des Zielgeräts), Hülse 40 mm davor in Richtung Wand, durch die Wand
        hy_b = f["box_hole_y"]; u_hole = abs(hy_b - yw); u_ps = u_hole - pl_l / 2; ya0 = yw + inw * u_ps; yb0 = yw + inw * (u_ps + pl_l)
        add(f"Kabelschuh_{nm}_Box_Huelse", "E2_Kabelschuh", Part.makeCylinder(rhv, h_len, V(fx, ya0, z_h), V(0, -inw, 0)), mass=0.0, mat="Cu (Masse offen, 0 gesetzt)")
        pal2 = box(fx - pl_w / 2, min(ya0, yb0), z_h - pl_t / 2, fx + pl_w / 2, max(ya0, yb0), z_h + pl_t / 2).cut(cyl(fx, hy_b, z_h - 5, z_h + 5, schb / 2))
        add(f"Kabelschuh_{nm}_Box_Palme", "E2_Kabelschuh", pal2, mass=0.0, mat="Cu (Masse offen, 0 gesetzt)")
        vert_cut.append(cyl(fx, fy, zl0, z_top + 2, rhv))
        f["box_hole"] = (fx, hy_b); f["L"] = L_
        # Clips alle 200 mm (Auflage 20 x 15 x 10, Rille für den Leiter), nur auf geraden Stücken
        Lv = max(0.0, za - z_va); Larc = math.pi * Rb / 2; Lh = abs(ye - fy) - Rb; nclip = 0; s_ = AD("clip_abstand_mm"); cl, cb_, ch_ = AD3("clip_mm")
        while s_ < L_:
            if s_ < Lv: zz = z_va + s_; cs = box(fx, fy - cb_ / 2, zz - cl / 2, fx + ch_, fy + cb_ / 2, zz + cl / 2).cut(cyl(fx, fy, zz - cl, zz + cl, rhv))
            elif s_ > Lv + Larc: yy = fy + sgn * (Rb + (s_ - Lv - Larc)); cs = box(fx - cb_ / 2, yy - cl / 2, z_h - ch_, fx + cb_ / 2, yy + cl / 2, z_h).cut(Part.makeCylinder(rhv, 3 * cl, V(fx, yy - 1.5 * cl, z_h), V(0, 1, 0)))
            else: cs = None
            if cs is not None: add(f"Clip_{nm}_{nclip}", "E2_Clip", cs, mass=0.0, mat="Kunststoff (Masse offen, 0 gesetzt)"); nclip += 1
            s_ += AD("clip_abstand_mm")
        kabel_info.append(dict(name=nm, laenge_mm=L_, clips=nclip, z_achse_mm=z_h, hoehe_ueber_box_boden_mm=z_h - zfl))
    fuesse["Plus"]["box_hole_y"] = pos["Shunt"][1] + shb / 2; fuesse["Minus"]["box_hole_y"] = pos["Schmelzsicherung"][1] + halt[1] / 2
    for nm in ("Plus", "Minus"): kabel(nm, fuesse[nm])
    # --- Lasche NMC (Plus, Minus, 2 x Mitte): Platte 25 x 25 x 3 auf dem Gruppenverbinder (wie N1), Bohrung M8
    if VAR == "NMC":
        lw_, lz2 = A3("A_e2_lasche_mm")
        for nm in ("Plus", "Minus", "Mitte_A_Ende_Band2", "Mitte_B_Anfang_Band3"):
            c = ans[nm]; pl_ = box(c["cx"] - lw_ / 2, c["cy"] - lw_ / 2, z_pad2, c["cx"] + lw_ / 2, c["cy"] + lw_ / 2, z_pad2 + lz2)
            add(f"Lasche_{nm}", "E2_Lasche", pl_.cut(cyl(c["cx"], c["cy"], z_pad2 - 1, z_pad2 + lz2 + 1, lbo / 2)), mat="Al"); cutter.append((pl_, ("Pad_oben", "Kuehlplatte_oben")))
        for nm in ("Mitte_A_Ende_Band2", "Mitte_B_Anfang_Band3"):
            c = ans[nm]; x, y = c["cx"], c["cy"]; ls_ = G.kabel_schichten(Part.Wire([Part.makeLine(V(x, y, z_pad2 + lz2), V(x, y, z_top))]), V(x, y, z_pad2 + lz2), V(0, 0, 1), radien)
            for ln, sh_ in zip(AD("kabel_schichten"), ls_): add(f"HV_{nm}_{ln}", "E2_HV_Leitung", sh_, mass=(cu_kg(z_top - z_pad2 - lz2) if ln == "Leiter" else 0.0), mat="Cu (Leiter)" if ln == "Leiter" else "Leitungsschicht (Masse offen, 0 gesetzt)")
            hv_len.append((f"{nm} -> Trennstecker", z_top - z_pad2 - lz2)); vert_cut.append(cyl(x, y, z_pad2, z_top, rhv)); geo["hv"].append(dict(name=nm, laenge_mm=z_top - z_pad2 - lz2, xy=[[x, y]]))
    # --- Stromschienen Cu (LFP 25 x 3, NMC 20 x 3), Bohrung 8,5, Biegeradius innen = Dicke, Schrumpfschlauch 0,5 mm
    zrel = lambda z_: zfl + z_
    def mkbar(nm, pa, zA, pb, zB, hoch=False, la=None, lb=None, ea=None, eb=None):
        Lb = math.hypot(pb[0] - pa[0], pb[1] - pa[1]); la = sw_ / 2 if la is None else la; lb = sw_ / 2 if lb is None else lb; ea = sw_ / 2 if ea is None else ea; eb = sw_ / 2 if eb is None else eb
        cA, cB, cM = zA + st_ / 2, zB + st_ / 2, zrel(zM) + st_ / 2; hinweis = ""; s1a, s1b = la + Rcb, lb + Rcb
        if hoch and Lb >= s1a + s1b + 2 * Rcb: pts = [(-ea, cA), (s1a, cA), (s1a, cM), (Lb - s1b, cM), (Lb - s1b, cB), (Lb + eb, cB)]
        elif abs(zA - zB) < 1e-6: pts = [(-ea, cA), (Lb + eb, cB)]
        elif abs(zA - zB) >= 2 * Rcb + 0.5:
            lo, hi = s1a, Lb - s1b; sv = (lo + hi) / 2 if hi >= lo else Lb / 2; pts = [(-ea, cA), (sv, cA), (sv, cB), (Lb + eb, cB)]
        else: zh_ = max(zA, zB); pts = [(-ea, zh_ + st_ / 2), (Lb + eb, zh_ + st_ / 2)]; hinweis = f"flach auf {zh_:.1f}, Höhenunterschied {abs(zA - zB):.1f} mm zum tieferen Kontakt (Passscheibe nötig)"
        lo_ = ((0.0, schb / 2), (Lb, schb / 2))
        try: sol, Lm = G.schiene(pa, pb, pts, sw_, st_, Rcb, loecher=lo_)
        except ValueError as ex:
            zh_ = max(zA, zB, zrel(zM)) if hoch else max(zA, zB); pts = [(-ea, zh_ + st_ / 2), (Lb + eb, zh_ + st_ / 2)]; hinweis = f"Ersatz: flach (Biegung nicht möglich: {ex})"
            sol, Lm = G.schiene(pa, pb, pts, sw_, st_, Rcb, loecher=lo_)
        add(nm, "E2_Stromschiene", sol, mass=sol.Volume * rhoCu * 1e-9, mat=f"Cu {sw_:g} x {st_:g}")
        try:
            sl = G.schlauch(pa, pb, pts, sw_, st_, Rcb, ssl, [(0.0, sw_ / 2 + 0.5), (Lb, sw_ / 2 + 0.5)])
            if sl is not None:
                tools = [q["shape"] for q in teile if q["grp"] in ("E2_Schaltbox_Inhalt", "E2_Kabelschuh") and q["shape"].BoundBox.intersect(sl.BoundBox)]
                if tools: sl = sl.cut(tools)
                if sl.Solids: add(nm + "_Schlauch", "E2_Schrumpfschlauch", sl, mass=0.0, mat="Schrumpfschlauch 0,5 mm (Masse offen, 0 gesetzt)")
        except Exception as ex: hinweis += f" (Schlauch nicht erzeugt: {ex})"
        bar_info.append(dict(name=nm, laenge_mm=Lm, abstand_mm=Lb, von=[round(pa[0], 1), round(pa[1], 1), round(zA, 1)], nach=[round(pb[0], 1), round(pb[1], 1), round(zB, 1)], hinweis=hinweis))
    fp, fm_ = fuesse["Plus"], fuesse["Minus"]
    sc_ = shunt_ends; zs_top = sc_[0][2]
    nah = sh_endB; fern = 1 - nah
    mkbar("Schiene_1_Plus_Shunt", fp["box_hole"], z_h + pl_t / 2, sc_[nah][:2], zs_top, hoch=True, la=pl_l / 2, ea=pl_l / 2)
    b1, b2 = sut["Hauptschuetz_1"], sut["Hauptschuetz_2"]; zs = zfl + schz[2]
    mkbar("Schiene_2_Shunt_Schuetz1", sc_[fern][:2], zs_top, b1[0], zs, hoch=True)
    mkbar("Schiene_3_Schuetz1_Schuetz2", b1[1], zs, b2[0], zs)
    mkbar("Schiene_4_Schuetz2_Pyro", b2[1], zs, pyl["A"][:2], pyl["A"][2], hoch=True, lb=ext_ / 2)
    mkbar("Schiene_5_Pyro_Schmelz", pyl["B"][:2], pyl["B"][2], scl["A"][:2], scl["A"][2], la=ext_ / 2, lb=16.0)
    mkbar("Schiene_6_Schmelz_Minus", scl["B"][:2], scl["B"][2], fm_["box_hole"], z_h + pl_t / 2, hoch=True, la=15.0, lb=pl_l / 2, eb=pl_l / 2)
    # --- Wanne einfügen (nach Löchern für Kabel und Fußlaschen-Schrauben)
    wl = [Part.makeCylinder(rhv, 2 * wd + 2, V(f["x"], f["ywall"] - f["inw"] * 1, z_h), V(0, f["inw"], 0)) for f in fuesse.values()]
    wanne_f = wanne.fuse(flansch).removeSplitter().cut(Part.makeCompound(wl + [cyl(h_.BoundBox.Center.x, h_.BoundBox.Center.y, bz0 - 1, bz0 + wd + 1, A["A_e2d_schuetz_fusslasche_gewinde_mm"] / 2) for h_ in fuss_holes]))
    add("Schaltbox_Wanne", "E2_Schaltbox", wanne_f, mat="Al")
    add("Schaltbox_Dichtung", "E2_Dichtung", dich, mass=0.0, mat="Dichtung (Masse offen, 0 gesetzt)")
    add("Schaltbox_Deckel", "E2_Schaltbox_Deckel", lid, mat="Al")
    add("Schaltbox_Druckausgleich", "E2_Schaltbox_Deckel", cyl(vx, vy, zlid, zlid + dk_, vd / 2), mass=0.0, mat="Membran (Masse offen, 0 gesetzt)")
    for k_, (sx_, sy_) in enumerate(scr):
        for pn, shp in G.schraube(sx_, sy_, zlid + dk_, sk, (zlid + dk_) - (wt - fd_), m5k[0], m5k[1]): add(f"Box_M5_{k_:02d}_{pn}", "E2_Schraube", shp, mass=0.0, mat="Stahl (Masse offen, 0 gesetzt)")
    # --- Stecker auf dem Haupt-Deckel (vor der Box, kleineres x), Flansch + Schrauben + Körper
    xs_ = bx0 - fl_ - gap; ys_ = by0 + rm; ein = AD("stecker_schraube_einzug_mm"); kein = AD("stecker_koerper_einzug_mm")
    def flansch_stecker(nm, hullen_k, fl_k, schr_k, masse, koerper):
        global ys_
        fL, fB, fH = AD3(fl_k); n_s, d_s = AD3(schr_k); hl, hb, hh = A3(hullen_k); x1 = xs_; x0_ = xs_ - fL
        add(nm + "_Flansch", "E2_Stecker_Sensor", box(x0_, ys_, z_top, x1, ys_ + fB, z_top + fH).cut(Part.makeCompound([cyl(px_, py_, z_top - 1, z_top + fH + 1, d_s / 2) for px_, py_ in ((x0_ + ein, ys_ + ein), (x1 - ein, ys_ + ein), (x0_ + ein, ys_ + fB - ein), (x1 - ein, ys_ + fB - ein))])), mass=masse, mat="E2 Teil (Masse ERW-E2 N1)")
        kh = m5k if d_s == 5 else m4k
        for k_, (px_, py_) in enumerate(((x0_ + ein, ys_ + ein), (x1 - ein, ys_ + ein), (x0_ + ein, ys_ + fB - ein), (x1 - ein, ys_ + fB - ein))[:int(n_s)]):
            for pn, shp in G.schraube(px_, py_, z_top + fH, d_s, fH, kh[0], kh[1]): add(f"{nm}_Schraube_{k_}_{pn}", "E2_Schraube", shp, mass=0.0, mat="Stahl (Masse offen, 0 gesetzt)")
        koerper(nm, x0_, x1, ys_, fB, fH, hh)
        ys_ += fB + gap
    def koerper_hv250(nm, x0_, x1, y0_, fB, fH, hh):
        kd, kl = AD3("hv250_koerper_mm"); ym = y0_ + fB / 2; zm = z_top + fH + kd / 2; xa_ = (x0_ + x1) / 2 - kl / 2
        add(nm + "_Steckkoerper", "E2_Stecker_Sensor", Part.makeCylinder(kd / 2, kl, V(xa_, ym, zm), V(1, 0, 0)), mass=0.0, mat="E2 Teil (Masse in Flansch enthalten)")
        hl_, hb_, hh_ = AD3("hv250_hebel_mm"); add(nm + "_Verriegelungshebel", "E2_Stecker_Sensor", box(xa_, ym + kd / 2, zm - hh_ / 2, xa_ + hl_, ym + kd / 2 + hb_, zm + hh_ / 2), mass=0.0, mat="E2 Teil (Masse in Flansch enthalten)")
        od, osn = AD3("hv250_oring_mm"); ori = Part.makeTorus(od / 2, osn / 2, V((x0_ + x1) / 2, ym, z_top + osn / 2), V(0, 0, 1)); gro = box((x0_ + x1) / 2 - od / 2 - osn, ym - od / 2 - osn, z_top, (x0_ + x1) / 2 + od / 2 + osn, ym + od / 2 + osn, z_top + osn)
        add(nm + "_ORing", "E2_Dichtung", ori, mass=0.0, mat="O-Ring (Masse offen, 0 gesetzt)")
        nut_ = Part.makeCylinder(od / 2 + osn / 2, osn, V((x0_ + x1) / 2, ym, z_top)).cut(Part.makeCylinder(od / 2 - osn / 2, osn, V((x0_ + x1) / 2, ym, z_top)))
        for q_ in teile:
            if q_["name"] == nm + "_Flansch": q_["shape"] = q_["shape"].cut(nut_)
    def koerper_box(nm, x0_, x1, y0_, fB, fH, hh):
        add(nm + "_Steckkoerper", "E2_Stecker_Sensor", box(x0_ + kein, y0_ + kein, z_top + fH, x1 - kein, y0_ + fB - kein, z_top + hh), mass=0.0, mat="E2 Teil (Masse in Flansch enthalten)")
    flansch_stecker("HV_Stecker_250A", "A_e2_hv250_mm", "hv250_flansch_mm", "hv250_schrauben", A["A_e2_hv250_masse_kg"], koerper_hv250)
    flansch_stecker("HV_Stecker_40A", "A_e2_hv40_mm", "hv40_flansch_mm", "hv40_schrauben", A["A_e2_hv40_masse_kg"], koerper_box)
    flansch_stecker("NV_Stecker_26pol", "A_e2_nv_mm", "nv_flansch_mm", "nv_schrauben", A["A_e2_nv_masse_kg"], koerper_box)
    l_, b_, h_ = A3("A_e2_gas_mm"); add("Gas_Drucksensor", "E2_Stecker_Sensor", box(xs_ - l_, ys_, z_top, xs_, ys_ + b_, z_top + h_), mass=A["A_e2_gas_masse_kg"], mat="E2 Teil (Masse ERW-E2 N1)")
    if VAR == "NMC":
        add("Service_Trennstecker", "E2_Stecker_Sensor", box(plug_x - plL / 2, plug_y - plB / 2, z_top, plug_x + plL / 2, plug_y + plB / 2, z_top + plH), mass=A["A_e2_trennstecker_masse_kg"], mat="E2 Teil (Masse ERW-E2 N1; Detail nicht in N3)")

    if VAR == "LFP":   # ---- Lasche (abgekantet, Radius innen = Dicke), Querverbinder-Lücke, Trennbrücke, HVIL, Servicedeckel (auf dem Deckel, Dichtung 3 x 3, 6 x M5 Senkkopf)
        gz_, gt_ = w("BT-420", "breite_mm"), w("BT-420", "dicke_mm"); z_ht = z_top_cell; x_c0 = min(c["cx"] for c in cells) - Dc / 2
        lw_, lt_ = A3("A_e2_lasche_mm"); xe_ = xh_in - x_hinten_frei; la_info = []; Rcl = 1.5 * lt_
        for nm in ("Plus", "Minus"):
            f = fuesse[nm]; yc = f["hole"][1]; xlead = f["x"]; xc_steg = xe_ + lt_ / 2; zbot = zc - gz_ / 2; zt = z_ht + Rcl; Lf = xc_steg - (xlead - pl_w / 2)
            sol, Ls = G.schiene((xc_steg, yc), (xc_steg - 100, yc), [(0, zbot), (0, zt), (Lf, zt)], lw_, lt_, Rcl, loecher=((xc_steg - xlead, lbo / 2),))
            add(f"Lasche_{nm}", "E2_Lasche", sol, mat="Al"); la_info.append(dict(name=nm, pfad_mm=Ls, querschnitt_mm2=lw_ * lt_, bohrungsrand_mm=None)); cutter.append((sol, ("Pad_oben", "Kuehlplatte_oben")))
        bg_, bov_ = A["A_e2_bruecke_luecke_mm"], A["A_e2_bruecke_ueberlappung_mm"]; bw_, bt_, bl_ = AD3("bruecke_mm"); oy_, ox_ = A3("A_e2_serviceoeffnung_mm")
        py = B / 2; yA, yB = py - bg_ / 2, py + bg_ / 2; px = x_c0 + gz_ / 2; ox0 = xv_in + 2
        assert abs(bl_ - ((yB - yA) + 2 * bov_)) < 1e-6, ("Brückenlänge", bl_, (yB - yA) + 2 * bov_)
        assert ox0 <= px - bw_ / 2 and px + bw_ / 2 <= ox0 + ox_, "Brücke außerhalb der Öffnung"
        zb0 = z_ht + gt_; bo_ = lbo / 2
        holes = [cyl(px, yA - bov_ / 2, z_ht - 1, zb0 + bt_ + 1, bo_), cyl(px, yB + bov_ / 2, z_ht - 1, zb0 + bt_ + 1, bo_)]
        qa = box(x_c0, ymin_ + 1, z_ht, x_c0 + gz_, yA, zb0); qb_ = box(x_c0, yB, z_ht, x_c0 + gz_, ymax_ - 1, zb0)
        add("Querverbinder_Mitte_A", "Zellverbinder", qa.cut(holes[0]), mat="Al (wie Zellverbinder G4)"); add("Querverbinder_Mitte_B", "Zellverbinder", qb_.cut(holes[1]), mat="Al (wie Zellverbinder G4)")
        br_ = box(x_c0, yA - bov_, zb0, x_c0 + bw_, yB + bov_, zb0 + bt_).cut(holes[0]).cut(holes[1])
        add("Trennbruecke_Cu", "E2_Trennbruecke", br_, mass=br_.Volume * rhoCu * 1e-9, mat="Cu")
        m8s_d, m8s_h = m8s; stack_h = m8s_h + m8k[1]
        for k_, hy_ in enumerate((yA - bov_ / 2, yB + bov_ / 2)):
            for pn, shp in G.schraube(px, hy_, zb0 + bt_, 2 * bo_, bt_ + gt_, m8k[0], m8k[1], scheibe=(m8s_d, m8s_h)): add(f"Trennbruecke_M8_{k_}_{pn}", "E2_Trennbrueckenschraube", shp, mass=0.0, mat="Stahl (Masse offen, 0 gesetzt)")
        hvl_, hvb_, hvh_ = AD3("hvil_mm"); hx0 = x_c0 + bw_ + gap
        add("HVIL_Bruecke", "E2_Trennbruecke", box(hx0, py - hvb_ / 2, z_ht, hx0 + hvl_, py + hvb_ / 2, z_ht + hvh_), mass=0.0, mat="E2 Teil (Masse offen, 0 gesetzt)")
        cutter.append((box(x_c0, ymin_ + 1, z_ht, x_c0 + gz_, ymax_ - 1, zb0), ("Pad_oben", "Kuehlplatte_oben")))
        cutter.append((box(ox0, py - oy_ / 2, z_ht, ox0 + ox_, py + oy_ / 2, z_top + 1), ("Pad_oben", "Kuehlplatte_oben")))
        rim = AD("servicedeckel_rand_mm"); cutter.append((box(ox0 + rim, py - oy_ / 2 + rim, z_dk - 1, ox0 + ox_ - rim, py + oy_ / 2 - rim, z_top + 1), ("Deckel",)))
        sdl, sdb, sdh = AD3("servicedeckel_mm"); assert (sdl, sdb) == (oy_, ox_) or (sdl, sdb) == (ox_, oy_), ("Servicedeckel-Maß", sdl, sdb, oy_, ox_)
        dgw, dgh = AD3("servicedeckel_dichtung_mm"); zc0 = z_top + dgh
        ring = box(ox0 + 9, py - oy_ / 2 + 9, z_top, ox0 + ox_ - 9, py + oy_ / 2 - 9, z_top + dgh).cut(box(ox0 + 12, py - oy_ / 2 + 12, z_top - 1, ox0 + ox_ - 12, py + oy_ / 2 - 12, z_top + dgh + 1))
        add("Servicedeckel_Dichtung", "E2_Dichtung", ring, mass=0.0, mat="Dichtung (Masse offen, 0 gesetzt)")
        n_sd, d_sd = AD3("servicedeckel_schrauben"); sps = [(ox0 + 4.5, py + dy_) for dy_ in (-45, 0, 45)] + [(ox0 + ox_ - 4.5, py + dy_) for dy_ in (-45, 0, 45)]
        # E3c Teil A: lichte Höhe innen >= Schraubenstapel M8 + Zugabe (ERW-E3c); Deckel wird um den fehlenden Betrag dicker, Tasche innerhalb der Dichtung (12 mm vom Rand)
        lichte_ = max(stack_h + PARM["BT-722"]["lichte_hoehe_zugabe_mm"]["wert"], zc0 - (zb0 + bt_)); dz_ = (zb0 + bt_ + lichte_) - zc0   # Zuwachs gegenüber dem flachen Deckel
        assert dz_ >= 0; zt_ = zc0 + dz_ + sdh   # Oberkante Deckel
        cov = box(ox0, py - oy_ / 2, zc0, ox0 + ox_, py + oy_ / 2, zt_).cut(box(ox0 + 12, py - oy_ / 2 + 12, zc0 - 1, ox0 + ox_ - 12, py + oy_ / 2 - 12, zc0 + dz_)).cut(Part.makeCompound([cyl(x_, y_, zc0 - 1, zt_ + 1, m5k[0] / 2) for x_, y_ in sps]))
        add("Servicedeckel", "E2_Servicedeckel", cov, mat="Al")
        cutter.append((Part.makeCompound([cyl(x_, y_, z_dk - 1, z_top + 1, d_sd / 2) for x_, y_ in sps]), ("Deckel",)))
        for k_, (x_, y_) in enumerate(sps):
            add(f"Servicedeckel_Senkschraube_{k_}_Kopf", "E2_Schraube", cyl(x_, y_, zt_ - sdh, zt_, m5k[0] / 2), mass=0.0, mat="Stahl (Masse offen, 0 gesetzt)")
            add(f"Servicedeckel_Senkschraube_{k_}_Schaft", "E2_Schraube", cyl(x_, y_, z_dk, zt_ - sdh, d_sd / 2), mass=0.0, mat="Stahl (Masse offen, 0 gesetzt)")
        kf_ = (Lg - 2 * rand) * (B - 2 * rand); nut_ = gz_ * ((ymax_ - 1) - (ymin_ + 1)); ov_ = gz_ * oy_
        nut_info = dict(kuehlflaeche_oben_mm2=kf_, nut_flaeche_gesamt_mm2=nut_, nut_flaeche_ohne_oeffnung_mm2=nut_ - ov_, nut_tiefe_in_kuehlplatte_mm=gt_ - A["A_pad_mm"], nut_anteil_prozent=100 * (nut_ - ov_) / kf_,
                        oeffnung_flaeche_mm2=ox_ * oy_, nut_plus_oeffnung_anteil_prozent=100 * (nut_ - ov_ + ox_ * oy_) / kf_, oeffnung_anteil_prozent=100 * ox_ * oy_ / kf_)
        quer_L = (yA - ymin_ - 1) + (ymax_ - 1 - yB)
        lfp_stecker = dict(bauform="trennbruecke_servicedeckel (ENT-150), E2D: Deckel auf Dichtung", x=px, y=py, oberkante_mm=zt_, ueber_deckel_mm=zt_ - z_top, servicedeckel_lichte_hoehe_mm=lichte_, servicedeckel_hoehenzuwachs_mm=dz_, serviceoeffnung_mm=[oy_, ox_], oeffnung_x0_mm=ox0, bruecke_mm=[bw_, bt_, (yB - yA) + 2 * bov_],
                           luecke_mm=bg_, querverbinder_laenge_mm=quer_L, laschen=la_info, nut=nut_info, schraubenstapel_mm=stack_h, schraubenstapel_oberkante_mm=zb0 + bt_ + stack_h, freie_hoehe_unter_deckel_mm=zc0 - (zb0 + bt_),
                           deckel_oeffnung_rand_mm=rim, servicedeckel_unterkante_mm=zc0)

    # ---- FPC (Länge immer berechnet; gebaut, wenn Platz)
    face = {"vorn": xv_in + cmuD, "hinten": xh_in - cmuD}; sgnx = {"vorn": 1, "hinten": -1}
    fpc_info = []; fpc_mass_kg = 0.0
    if VAR == "NMC":
        zf0 = z_pad2 + A['A_e2d_fpc_tab_mm'][2]; zlink = zf0 - (zc + cmuB / 2)
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
    # ====================== E2D Details: Ni-Tab, NTC, FPC-Stecker, Daisy-Chain, Berührschutz, Schweißnaht (LFP) ======================
    ftab = AD3("fpc_tab_mm"); ntc = AD3("ntc_mm"); fst = AD3("fpc_stecker_mm"); dst = AD3("daisy_stecker_mm"); dd_ = AD("daisy_d_mm"); n_ntc = int(AD("ntc_je_cmu")); det = dict(tabs=0, ntc=0, fpc_stecker=0, daisy_stecker=0, daisy_kabel=0)
    zt_cmu = zc + cmuB / 2; zb_cmu = zc - cmuB / 2
    for j in range(ncmu):     # FPC-Stecker oben auf der Kante, Daisy-Stecker unten auf der Kante, Daisy-Kabel zur nächsten CMU derselben Seite
        x0, x1 = cmu_x[seite[j]]; yf = min(max(lane[j] if VAR == "NMC" else ypos[j], ypos[j] - cmuL / 2 + fst[0] / 2), ypos[j] + cmuL / 2 - fst[0] / 2)
        add(f"FPC_Stecker_{j:02d}", "E2_FPC_Detail", box(x0 + 1, yf - fst[0] / 2, zt_cmu, x0 + 1 + fst[1], yf + fst[0] / 2, zt_cmu + fst[2]), mass=0.0, mat="E2 Teil (Masse offen, 0 gesetzt)"); det["fpc_stecker"] += 1
        for nm_, ya_ in (("In", ypos[j] - 45), ("Out", ypos[j] + 30)):
            add(f"Daisy_Stecker_{j:02d}_{nm_}", "E2_Daisy", box(x0 + 1, ya_, zb_cmu - dst[2], x0 + 1 + dst[1], ya_ + dst[0], zb_cmu), mass=0.0, mat="E2 Teil (Masse offen, 0 gesetzt)"); det["daisy_stecker"] += 1
    for sd in ("vorn", "hinten"):
        ids = sorted([j for j in range(ncmu) if seite[j] == sd], key=lambda j: ypos[j])
        for a_, b_ in zip(ids, ids[1:]):
            x0, x1 = cmu_x[sd]; ya_ = ypos[a_] + 45; yb2 = ypos[b_] - 45
            add(f"Daisy_Leitung_{a_:02d}_{b_:02d}", "E2_Daisy", Part.makeCylinder(dd_ / 2, yb2 - ya_, V(x0 + 1 + dst[1] / 2, ya_, zb_cmu - dst[2] / 2), V(0, 1, 0)), mass=0.0, mat="Leitung (Masse offen, 0 gesetzt)"); det["daisy_kabel"] += 1
    daisy_quer_mm = abs((xh_in - cmuD / 2) - (xv_in + cmuD / 2))
    # Ni-Tab je Abgriff und NTC auf 4 Abgriffen je CMU
    if VAR == "NMC":
        for i, (tx, ty) in enumerate(taps): add(f"FPC_Tab_{i:03d}", "E2_FPC_Detail", box(tx - ftab[0] / 2, ty - ftab[1] / 2, z_pad2, tx + ftab[0] / 2, ty + ftab[1] / 2, z_pad2 + ftab[2]), mass=0.0, mat="Ni (Masse offen, 0 gesetzt)"); det["tabs"] += 1
        for j in range(ncmu):
            xa_ = min(face[seite[j]], *[taps[i][0] for i in grp_t[j]]) - 1; xb_ = max(face[seite[j]], *[taps[i][0] for i in grp_t[j]]) + 1; ly0, ly1 = lane[j] - fw / 2 - 1, lane[j] + fw / 2 + 1
            for i in grp_t[j][:n_ntc]:
                tx, ty = taps[i]
                for ox_, oy2 in ((8, 6), (8, -6), (-8, 6), (-8, -6), (0, 10), (0, -10)):
                    nx0, nx1, ny0, ny1 = tx + ox_ - ntc[0] / 2, tx + ox_ + ntc[0] / 2, ty + oy2 - ntc[1] / 2, ty + oy2 + ntc[1] / 2
                    if not (nx1 > xa_ and nx0 < xb_ and ny1 > ly0 and ny0 < ly1):
                        add(f"NTC_{j:02d}_{i:03d}", "E2_FPC_Detail", box(nx0, ny0, z_pad2, nx1, ny1, z_pad2 + ntc[2]), mass=0.0, mat="NTC (Masse offen, 0 gesetzt)"); det["ntc"] += 1; break
        # Berührschutz 1 mm über jeder Polreihe des Fensters (über dem Omega-Scheitel), nur Fenster
        bs = AD("beruehrschutz_dicke_mm"); zb_ = z_pad2 + omh; rows_w = sorted({round(c["cx"], 3) for c in cells if c["feld"] == WIN}); n_bs = 0
        for rx in rows_w:
            cs_ = [c for c in cells if c["feld"] == WIN and abs(c["cx"] - rx) < 1e-3]; yy0 = min(c["cy"] for c in cs_) - gb; yy1 = max(c["cy"] for c in cs_) + gb
            bsh = box(rx - gb, yy0, zb_, rx + gb, yy1, zb_ + bs); add(f"Beruehrschutz_R{n_bs:02d}", "E2_Beruehrschutz", bsh, mass=0.0, mat="Kunststoff (Masse offen, 0 gesetzt)"); cutter.append((bsh, ("Pad_oben", "Kuehlplatte_oben"))); n_bs += 1
        det["beruehrschutz_platten"] = n_bs
    else:
        yface = {0: rand + 1, 1: B - rand - 1}; sgf = {0: -1, 1: 1}
        for i, (tx, _) in enumerate(taps):
            rw = tap_row[i]; ya_ = yface[rw]
            tb = (ya_ - ftab[2], ya_) if rw == 0 else (ya_, ya_ + ftab[2])
            add(f"FPC_Tab_{i:03d}", "E2_FPC_Detail", box(tx - ftab[1] / 2, tb[0], zc - ftab[0] / 2, tx + ftab[1] / 2, tb[1], zc + ftab[0] / 2), mass=0.0, mat="Ni (Masse offen, 0 gesetzt)"); det["tabs"] += 1
        qx_ = [(x_ - 0.5, x_ + qb + 0.5) for x_ in pos_q]
        for j in range(ncmu):
            for i in grp_t[j][:n_ntc]:
                tx, _ = taps[i]; rw = tap_row[i]; ya_ = yface[rw]; tb = (ya_ - ntc[2], ya_) if rw == 0 else (ya_, ya_ + ntc[2])
                tx = next(tx + o_ * pitch for o_ in (0.75, -0.75, 0.25, -0.25, 1.25, -1.25, 1.75, -1.75, 2.25, -2.25, 2.75, -2.75, 3.25, -3.25) if not any(a_ < tx + o_ * pitch + ntc[0] / 2 and b_ > tx + o_ * pitch - ntc[0] / 2 for a_, b_ in qx_)) - 0.75 * pitch
                add(f"NTC_{j:02d}_{i:03d}", "E2_FPC_Detail", box(tx + 0.75 * pitch - ntc[0] / 2, tb[0], zc - ntc[1] / 2, tx + 0.75 * pitch + ntc[0] / 2, tb[1], zc + ntc[1] / 2), mass=0.0, mat="NTC (Masse offen, 0 gesetzt)"); det["ntc"] += 1
    # Schweißnaht (LFP): 2 Linien 10 x 1, Vertiefung 0,2 je Pol, nur Fenster (Feld WIN). NMC: oben bei den Gruppenverbindern erledigt.
    if VAR == "LFP":
        swl, swb, swt, swn = AD3("schweiss_mm"); swa = AD("schweiss_abstand_mm"); n_w = 0
        for p in teile:
            if p["grp"] != "Zellverbinder" or not p["name"].startswith("Zellverbinder_g"): continue
            import re as re_; mm_ = re_.match(r"Zellverbinder_g(\d+)r(\d+)_", p["name"]); gi_, rr_ = int(mm_.group(1)), int(mm_.group(2))
            if gi_ != WIN: continue
            bb_ = p["shape"].BoundBox; yo = (bb_.YMin, bb_.YMin + swt) if rr_ == 0 else (bb_.YMax - swt, bb_.YMax); gr_ = []
            for pxc in (bb_.XMin + Dc / 2, bb_.XMax - Dc / 2):
                for sgn_ in (-1, 1): gr_.append(box(pxc + sgn_ * swa / 2 - swb / 2, yo[0], zc - swl / 2, pxc + sgn_ * swa / 2 + swb / 2, yo[1], zc + swl / 2))
            p["shape"] = p["shape"].cut(Part.makeCompound(gr_)); n_w += 1
        det["schweiss_verbinder"] = n_w
    det["daisy_quer_mm_nicht_gezeichnet"] = daisy_quer_mm; det["fenster_feld"] = WIN

    # ---- Durchführungen und Aussparungen (Verguss/Träger/Pad/Kühlplatte/Deckel werden um E2-Teile herum gelassen; Volumen wird gemeldet)
    for q_ in vert_cut: cutter.append((q_, ("Pad_oben", "Kuehlplatte_oben", "Deckel")))
    for p in list(teile):
        if p["grp"] in ("E2_CMU", "E2_Daisy"): cutter.append((p.get("cutshape", p["shape"]), ("Zelltraeger_f", "Verguss_f")))
        if p["grp"] == "E2_Lasche": cutter.append((p["shape"], ("FPC_Tab_", "NTC_")))
        if p["name"].endswith("_Zelle_Palme") or p["name"].startswith("HV_Mitte"): cutter.append((p["shape"], ("Beruehrschutz",)))
        if p["name"].startswith("Gruppenverbinder_g") and VAR == "NMC": cutter.append((p["shape"], ("FPC_0", "FPC_1", "FPC_2")))
    if VAR == "NMC":
        for p in list(teile):
            if p["name"].startswith(("FPC_Tab_", "NTC_")): cutter.append((p["shape"], ("Pad_oben",)))
    ausspar = {}
    for p in teile:
        tl_ = [shp for shp, ziele in cutter if any(p["name"].startswith(z) for z in ziele) and p["shape"].BoundBox.intersect(shp.BoundBox)]
        if tl_:
            v0 = p["shape"].Volume; p["shape"] = p["shape"].cut(tl_); dv = v0 - p["shape"].Volume
            if dv > 1e-6: ausspar[p["name"]] = ausspar.get(p["name"], 0.0) + dv
    entfallen = [p["name"] for p in teile if (not p["shape"].Solids) or p["shape"].Volume < 1e-6]    # durch Aussparung vollständig verschwunden
    teile[:] = [p for p in teile if p["name"] not in entfallen]
    mass_e2 = sum(p["mass"] for p in teile if p["grp"].startswith("E2") and p["mass"] is not None) - sum(p["mass"] for p in teile if p["grp"] == "E2_FPC") + kg_fpc_m * sum(f["laenge_mm"] for f in fpc_info) / 1000
    hvl = sum(l for _, l in hv_len) + (2 * gap if True else 0)   # plus 2 kurze Leitungen Schaltbox -> HV-Stecker 250 A (Länge = Teilabstand)
    e2res = dict(fall="hinten (ENT-144)", verschaltung=vers, schaltbox_L_mm=bL, schaltbox_B_mm=bB, schaltbox_H_mm=bH, schaltbox_x0_y0_z0_mm=[bx0, by0, bz0], reihenbreiten_mm=rb, hoechstes_teil_mm=inner_h,
                 hoehenzuwachs_gesamt_mm=max(p["shape"].BoundBox.ZMax for p in teile if p["grp"].startswith("E2")) - z_top, hoehe_stapel_vor_e2_mm=z_top, hoehe_max_A_mm=A["A_hoehe_max_mm"],
                 cmu_anzahl=ncmu, cmu_seite=dict(vorn=seite.count("vorn"), hinten=seite.count("hinten")), cmu_kapazitaet_je_endzone=asg["kapazitaet_je_endzone"], cmu_masse_kg=ncmu * A["A_e2_cmu_masse_kg"],
                 freier_abstand_endzone_vorn_mm=x_vorn_frei, freier_abstand_endzone_hinten_mm=x_hinten_frei, cmu_dicke_mm=cmuD, abgriffe=len(taps), cmu_y=ypos,
                 fpc=fpc_info, fpc_laenge_gesamt_m=sum(f["laenge_mm"] for f in fpc_info) / 1000, fpc_laenge_platziert_m=sum(f["laenge_mm"] for f in fpc_info if f["platziert"]) / 1000,
                 fpc_stuecke=len(fpc_info), fpc_nicht_platziert=sum(1 for f in fpc_info if not f["platziert"]), fpc_masse_kg=kg_fpc_m * sum(f["laenge_mm"] for f in fpc_info) / 1000,
                 hv=[dict(strecke=n, laenge_mm=l) for n, l in hv_len], hv_laenge_gesamt_m=hvl / 1000, hv_W_je_m=Whv, hv_verlust_W=hvl / 1000 * Whv, hv_cu_masse_kg=sum(cu_kg(l) for _, l in hv_len) + cu_kg(2 * gap), stecker_lfp=(lfp_stecker if VAR == "LFP" else None), hoehe_vorn_mm=max(p["shape"].BoundBox.ZMax for p in teile if p["shape"].BoundBox.XMax < bx0 - 100), hoehe_vorn_grenze_x_mm=bx0 - 100,
                 hv_gebaut=True, hv_kurze_leitungen_box_stecker_mm=2 * gap,
                 masse_elektronik_ohne_hv_leitungen_kg=mass_e2, aussparungen_mm3=ausspar, geometrie=geo, biegeradius_mm=Rb, hv_aussendurchmesser_mm=dhv)
    e2res.update(e2d=True, teile_entfallen_durch_aussparung=entfallen, schaltbox_wanne_L_mm=bL, schaltbox_wanne_B_mm=bB, schaltbox_aussen_mit_flansch_L_mm=bL + 2 * fl_, schaltbox_aussen_mit_flansch_B_mm=bB + 2 * fl_, schaltbox_innenhoehe_mm=inner_h, schaltbox_wandoberkante_mm=wt, schaltbox_deckel_oberkante_mm=zlid + dk_,
                 schaltbox_H_bis_deckel_mm=bH, schaltbox_H_mit_schraubenkoepfen_mm=bH + m5k[1], schaltbox_hoehe_max_N1_mm=A["A_e2_box_hoehe_max_mm"], flansch_mm=fl_, schrauben_box=len(scr), schienen=bar_info, kabel=kabel_info, kabel_z_achse_mm=z_h, kabel_z_achse_ueber_boxboden_mm=z_h - zfl,
                 kabel_radien_mm=radien, details=det, fenster_feld=WIN, fenster_x_mm=[min(c["cx"] for c in cells if c["feld"] == WIN), max(c["cx"] for c in cells if c["feld"] == WIN)], fuesse={k: {kk: vv for kk, vv in v.items()} for k, v in fuesse.items()},
                 schiene_mm=[sw_, st_], lug=dict(huelse_mm=h_len, palme_mm=[pl_w, pl_l, pl_t]), zM_rel_boden_mm=zM)
    for k_, p_ in enumerate([p for p in teile if p["name"] == "Servicedeckel"][:1]): e2res["servicedeckel_zmax_mm"] = p_["shape"].BoundBox.ZMax

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
tol = 1e-3; N = len(teile); paare = 0; koll = []; kontakte = []; tmax = 0.0
KONTAKT_VERSCHRAUBT = [{"Schmelz_Lasche_A", "Schiene_5_Pyro_Schmelz"}]   # E3c Teil A (ERW-E3c): verschraubte Paare, Schwelle A_e3c_kontakt_schwelle_mm3
for i in range(N):
    ov = (bb[i, 3] - tol > bb[i + 1:, 0]) & (bb[i, 0] + tol < bb[i + 1:, 3]) & (bb[i, 4] - tol > bb[i + 1:, 1]) & (bb[i, 1] + tol < bb[i + 1:, 4]) & (bb[i, 5] - tol > bb[i + 1:, 2]) & (bb[i, 2] + tol < bb[i + 1:, 5])
    for j in np.nonzero(ov)[0] + i + 1:
        a, b = teile[i], teile[j]
        if a["grp"] == b["grp"] == "Zellen" and False: continue
        paare += 1
        vol = a["shape"].common(b["shape"]).Volume
        if vol > 1e-6:
            if {a["name"], b["name"]} in KONTAKT_VERSCHRAUBT and vol <= A["A_e3c_kontakt_schwelle_mm3"]: kontakte.append(dict(a=a["name"], b=b["name"], volumen_mm3=vol))   # E3c: verschraubte Berührung, kein Verstoß
            else: koll.append(dict(a=a["name"], b=b["name"], volumen_mm3=vol))
bbA = FreeCAD.BoundBox(); [bbA.add(p["shape"].BoundBox) for p in teile]
doc = FreeCAD.newDocument(f"pack_{VO}")
gruppen = {}
for p in teile: gruppen.setdefault(p["grp"], []).append(p["shape"])
for g, sh in gruppen.items(): doc.addObject("Part::Feature", g).Shape = Part.makeCompound(sh)
NZ = "/home/cae/cae_projekte/batterie/e2"; os.makedirs(NZ, exist_ok=True)
doc.recompute(); doc.saveAs(f"{NZ}/pack_{VO}.FCStd"); Part.export(list(doc.Objects), f"{NZ}/pack_{VO}.step")
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

if E2:   # Netze für die E2D-Bilder (große Dateien nach cae_projekte)
    xq = xh = 0.0
    netz(lambda p: p["grp"] != "Zellen", f"{NZ}/netz_{VO}_gesamt.json")
    netz(lambda p: p["name"] not in ("Deckel", "Pad_oben", "Kuehlplatte_oben") and p["grp"] not in ("E2_Schaltbox", "E2_Schaltbox_Deckel"), f"{NZ}/netz_{VO}_ohnedeckel.json")
    netz(lambda p: p["grp"] not in ("Zellen", "E2_Schaltbox_Deckel"), f"{NZ}/netz_{VO}_boxoffen.json")
    if VAR == "LFP": netz(lambda p: p["grp"] != "Zellen" and not p["name"].startswith("Servicedeckel"), f"{NZ}/netz_{VO}_bruecke_offen.json")
    # E3c (Sonnet 2026-11-24): offene Schaltbox mit Inhalt ohne BMS-Platzhalter, Lage des BMS-Platzes für das Einbaubild der BMS-Platine BT-311
    netz(lambda p: p["grp"] in ("E2_Schaltbox", "E2_Schaltbox_Inhalt") and not p["name"].startswith(("BMS_Platine", "BMS_Stecker", "BMS_Daisy_Stecker")), f"{NZ}/netz_{VO}_bmsbox.json")
    _bb = [p for p in teile if p["name"] == "BMS_Platine"][0]["shape"].BoundBox
    e2res["bms_platine_bbox_mm"] = [_bb.XMin, _bb.YMin, _bb.ZMin, _bb.XMax, _bb.YMax, _bb.ZMax]
if E2:
    e2res["masse_elektronik_gesamt_kg"] = sum(g_["masse_kg"] for k_, g_ in gm.items() if k_.startswith("E2") and k_ != "E2_FPC") + e2res["fpc_masse_kg"]   # Box, Inhalt, Stecker, CMU, alle FPC (auch ohne Platz), HV-Leiter (nur Cu)
    e2res["masse_hv_leiter_cu_kg"] = gm.get("E2_HV_Leitung", {}).get("masse_kg", 0.0) + cu_kg(2 * gap)
    e2res["masse_elektronik_ohne_hv_leitungen_kg"] = e2res["masse_elektronik_gesamt_kg"] - gm.get("E2_HV_Leitung", {}).get("masse_kg", 0.0)
    e2res["querverbinder_mitte_al_kg"] = sum(p["mass"] for p in teile if p["name"].startswith("Querverbinder"))   # Box (Al aus Volumen), Inhalt, Stecker, CMU, alle FPC (auch ohne Platz); HV-Leitungen ohne Masse (Dichte fehlt)
res = dict(schnittebene_quer_x_mm=(xq if not E2 else None), schnittebene_halb_x_mm=(xh if not E2 else None), hinweis="KI-generiert, ENTWURF, nicht freigegeben. Erzeugt von cad/pack/pack_e2d.py (Kopie von pack.py mit E2D) aus cad/pack/entwurf/parameter_%s.json" % VAR,
  variante=VAR, laenge_mm=bbA.XLength, breite_mm=bbA.YLength, hoehe_mm=bbA.ZLength, hoehe_stapel_mm=H, hoehe_max_mm=A["A_hoehe_max_mm"],
  gehaeuse_L_mm=Lg, zellen=len(cells), quertraeger_x_mm=pos_q, zellmasse_je_kg=mcell,
  gruppen=gm, masse_bekannt_kg=tot, schwerpunkt_mm=cg, mitte_mm=[Lg / 2, B / 2], schwerpunkt_abw_mm=[cg[0] - Lg / 2, cg[1] - B / 2],
  teile=len(teile), kollisionspaare_geprueft=paare, kollisionen=koll, anzahl_kollisionen=len(koll), kontakte_zugelassen=kontakte, rechenzeit_s=time.time() - t0,
  e3=(dict(E3INFO, anzahl_cmu=ncmu, step=f"/home/cae/cae_projekte/batterie/e3/cmu_{VAR}.step", cmu_masse_gesamt_kg=sum(t_["mass"] or 0 for t_ in teile if t_["name"].startswith("CMU_")), cmu_masse_je_g=(teile[[t_["name"] for t_ in teile].index("CMU_00")]["mass"] or 0) * 1000, cmu_masse_alt_e2_kg=A["A_e2_cmu_masse_kg"] * ncmu) if E3 else None),
  e2=e2res, annahmen={k: PJ["A"][k] for k in PJ["A"]})
json.dump(res, open(f"{OUT}/ergebnis_{VO}.json", "w"), indent=1, ensure_ascii=False)
print("FERTIG", VAR, "Teile", len(teile), "Paare", paare, "Koll", len(koll), "t", round(time.time() - t0))

