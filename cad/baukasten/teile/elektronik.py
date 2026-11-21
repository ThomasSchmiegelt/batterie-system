# KI-generiert (Claude Sonnet, 2026-11-19), Entwurf. Auftrag G5.4 (cad/baukasten/AUFTRAG_G5_4.md), Modul elektronik.
"""Elektronik: CMU BT-320, FPC BT-360, FPC-Halter BT-361, FPC-Details (Tabs, Stecker), Daisy-Chain, NTC BT-330; BMS-Platine BT-310, Shunt BT-340,
Isolationswächter BT-350 (diese drei lokal gebaut und an ctx.schaltbox["lagen"] gesetzt, Maße und Klemmen aus ctx.schaltbox["geraete"], PLAN §3a).
Logik der Lage: cad/pack/pack_e2d.py (CMU hochkant in den Endzonen, FPC-Spuren, Daisy-Kabel) über teile/_verdrahtung.py; die Rechnung ist gleich.
Massen der Platinen und Kaufteile: Annahmen ERW-E2 N1 (A_e2_*_masse_kg), wie in SL3 (Quelle „Annahme“)."""
import math
from kern import teil, p, a, Teil, quader, zylinder, bohrungen, setze, VAR, Part, V
from teile._verdrahtung import verdr


def _geraet(ctx, name):
    """Gerätemaße und Einbauort aus schaltbox.py (eine Quelle). None, wenn nicht vorhanden."""
    try:
        from teile.schaltbox import _layout
        S = _layout(ctx)
    except Exception as e:
        print("  elektronik: schaltbox.py nicht lesbar:", e); return None, None
    if name not in S["lagen"]:
        print(f"  elektronik: kein Einbauort für {name}"); return None, None
    return S["geraete"][name], S["lagen"][name]


@teil("elektronik.cmu", "BT-320", "F")
def cmu(ctx, pos):
    """Zellüberwachung CMU BT-320 (LFP 14, NMC 13; ENT-116/117): Leiterplatte (A_e2d_bms_platine_dicke_mm) hochkant an den Rahmen gelehnt in der
    vorderen oder hinteren Endzone (Maße A_e2_cmu_mm 120 × 60 × 10, Seite und y-Lage aus _verdrahtung), mit zwei Bausteinen (A_g54_cmu_bauteile_mm)
    und vier Befestigungsbohrungen (A_g54_cmu_bohrung_mm). Masse A_e2_cmu_masse_kg (Annahme ERW-E2 N1). Stufe F."""
    R = verdr(ctx); cL, cB = R["cmuL"], R["cmuB"]; zc = ctx.z_mitte_zelle; pd = a("A_e2d_bms_platine_dicke_mm")
    iy, iz, ix = a("A_g54_cmu_bauteile_mm"); bd, be = a("A_g54_cmu_bohrung_mm"); teile = []
    for j in range(R["ncmu"]):
        x0, x1 = R["cmu_x"][R["seite"][j]]; y = R["ypos"][j]; vorn = R["seite"][j] == "vorn"
        xb0, xb1 = (x0, x0 + pd) if vorn else (x1 - pd, x1)
        s = quader(xb0, y - cL / 2, zc - cB / 2, xb1, y + cL / 2, zc + cB / 2)
        s = bohrungen(s, [(xb0 - 1, y + sy * (cL / 2 - be), zc + sz * (cB / 2 - be)) for sy in (-1, 1) for sz in (-1, 1)], bd / 2, pd + 2, "x")
        xc0, xc1 = (xb1, xb1 + ix) if vorn else (xb0 - ix, xb0)
        for dy in (-cL / 4, cL / 4): s = s.fuse(quader(xc0, y + dy - iy / 2, zc - iz / 2, xc1, y + dy + iy / 2, zc + iz / 2))
        teile.append(Teil(f"CMU_{j:02d}", s.removeSplitter(), "Leiterplatte", masse_kg=a("A_e2_cmu_masse_kg")))
    return teile


def _fpc_stuecke(ctx):
    """FPC-Stücke (Hüllquader, Länge, Meta) nach pack_e2d.py (LFP: Seitenspalt, 2 Spuren × bis 4 Lagen; NMC: Verbinderebene unter dem Pad). Gecached."""
    if hasattr(ctx, "fpc_stuecke"): return ctx.fpc_stuecke["s"], ctx.fpc_stuecke["h"]      # dict, damit Ctx.als_dict es nicht als Liste ins JSON nimmt
    R = verdr(ctx); fw = p("BT-360", "breite_mm"); ft = a("A_e2_fpc_dicke_mm"); kg_m = a("A_e2_fpc_masse_kg_m"); cL, cB, cD = R["cmuL"], R["cmuB"], R["cmuD"]
    zc = ctx.z_mitte_zelle; xv_in, xh_in = R["xv_in"], R["xh_in"]; taps, grp_t, seite, ypos, lane = R["taps"], R["grp_t"], R["seite"], R["ypos"], R["lane"]
    face = {"vorn": xv_in + cD, "hinten": xh_in - cD}; out = []; halter = []
    if VAR == "NMC":
        zf0 = ctx.z_pad_o_u + a("A_e2d_fpc_tab_mm")[2]
        for j in range(R["ncmu"]):
            s = seite[j]; yl = lane[j]; xf = face[s]; xs_t = [taps[i][0] for i in grp_t[j]]; xfar = max(xs_t) if s == "vorn" else min(xs_t)
            stub = sum(abs(taps[i][1] - yl) for i in grp_t[j]); zlink = zf0 - (zc + cB / 2); Lx = abs(xfar - xf); Ltot = zlink + Lx + stub
            xa, xb = sorted((xf, xfar)); va = xf if s == "vorn" else xf - ft
            shp = quader(xa, yl - fw / 2, zf0, xb, yl + fw / 2, zf0 + ft).fuse(quader(va, yl - fw / 2, zc + cB / 2, va + ft, yl + fw / 2, zf0 + ft))
            out.append(dict(name=f"FPC_{j:02d}", shape=shp, masse=kg_m * Ltot / 1000, laenge=Ltot, cmu=j, platziert=True))
    else:
        ymin, ymax, yg, hh, nl = R["ymin"], R["ymax"], R["yg"], R["hh"], R["nl"]; tap_row = R["tap_row"]; Hc = ctx.zell_mass["H"]
        lanes = [(zc + Hc / 2 + 1.0 - fw, zc + Hc / 2 + 1.0), (zc - Hc / 2, zc - Hc / 2 + fw)]      # obere Spur 1 mm über der Zelloberkante (Rille im Pad), damit die Zellverbinder-Bögen über den Querträgern (bis zc + qh/2 + 3) frei bleiben
        ylay = lambda rw, l: ((ymin + hh + l * ft, ymin + hh + (l + 1) * ft) if rw == 0 else (ymax - hh - (l + 1) * ft, ymax - hh - l * ft))
        x_vorn_frei = min(c["cx"] for c in ctx.zellen) - ctx.zell_mass["D"] / 2 - xv_in
        x_hinten_frei = xh_in - max(c["cx"] + ctx.zell_mass["D"] / 2 for c in ctx.zellen)
        stripes = []
        for j in range(R["ncmu"]):
            for rw in (0, 1):
                ids = [i for i in grp_t[j] if tap_row[i] == rw]
                if not ids: continue
                s = seite[j]; xf = face[s]; xs_t = [taps[i][0] for i in ids]; xfar = max(xs_t) if s == "vorn" else min(xs_t)
                stripes.append((j, rw, s, xf, xfar, abs(ypos[j] - yg[rw]), abs(xfar - xf), min(xf, xfar), max(xf, xfar)))
        slot = {"vorn": 0, "hinten": 0}; placed = []
        for (j, rw, s, xf, xfar, Ly, Lx, xa, xb) in sorted(stripes, key=lambda q: -q[6]):
            sx = slot[s] * ft; cx0 = xf + sx if s == "vorn" else xf - sx - ft; cx1 = cx0 + ft
            sa, sb = (xa, cx1) if s == "hinten" else (cx0, xb)
            frei = (cx1 <= xv_in + x_vorn_frei + 1e-6) if s == "vorn" else (cx0 >= xh_in - x_hinten_frei - 1e-6)
            pos_ = None
            for lane_i in (0, 1):
                for ly in range(nl):
                    if not frei: break
                    bad = False
                    for q in placed:
                        if q["rw"] != rw or q["lane"] != lane_i: continue
                        if q["layer"] == ly and not (sb < q["xa"] - 1e-6 or sa > q["xb"] + 1e-6): bad = True
                        if q["layer"] > ly and q["xa"] - 1e-6 <= cx1 and q["xb"] + 1e-6 >= cx0: bad = True
                        if ly > q["layer"] and sa - 1e-6 <= q["cx1"] and sb + 1e-6 >= q["cx0"]: bad = True
                    if not bad: pos_ = (lane_i, ly); break
                if pos_: break
            Ltot = Ly + Lx
            if pos_ is None:
                out.append(dict(name=f"FPC_{j:02d}_R{rw}", shape=None, masse=kg_m * Ltot / 1000, laenge=Ltot, cmu=j, platziert=False)); continue
            lane_i, ly = pos_; slot[s] += 1; placed.append(dict(rw=rw, lane=lane_i, layer=ly, xa=sa, xb=sb, cx0=cx0, cx1=cx1)); z0, z1 = lanes[lane_i]
            ya, yb_ = ylay(rw, ly); yc0, yc1 = (ya, ypos[j]) if rw == 0 else (ypos[j], yb_)
            shp = quader(sa, ya, z0, sb, yb_, z1).fuse(quader(cx0, yc0, z0, cx1, yc1, z1))
            out.append(dict(name=f"FPC_{j:02d}_R{rw}", shape=shp, masse=kg_m * Ltot / 1000, laenge=Ltot, cmu=j, platziert=True))
        for rw in (0, 1):
            for lane_i in (0, 1):
                qs = [q for q in placed if q["rw"] == rw and q["lane"] == lane_i]
                if not qs: continue
                hy = (ymin, ymin + hh) if rw == 0 else (ymax - hh, ymax)
                halter.append(dict(name=f"FPC_Halter_R{rw}_S{lane_i}", shape=quader(min(q["xa"] for q in qs), hy[0], lanes[lane_i][0], max(q["xb"] for q in qs), hy[1], lanes[lane_i][1])))
    ctx.fpc_stuecke = dict(s=out, h=halter)
    return out, halter


@teil("elektronik.fpc", "BT-360", "F")
def fpc(ctx, pos):
    """Flexleiterplatte FPC BT-360 (LFP 14, NMC 13; ENT-149 Breite): ein Streifen je CMU (und Reihe) vom CMU-Rand zu den Abgriffen, Dicke A_e2_fpc_dicke_mm,
    Masse = Länge × A_e2_fpc_masse_kg_m. LFP im Seitenspalt Rahmen-Zelle (oben/unten, bis 4 Lagen), NMC in der Verbinderebene unter dem oberen Pad
    (schneidet das Pad über ctx.schneide). Stücke ohne Platz werden nicht gebaut und gemeldet. Stufe F."""
    stuecke, _ = _fpc_stuecke(ctx); teile = []
    for q in stuecke:
        if not q["platziert"]: print("  elektronik.fpc: kein Platz für", q["name"]); continue
        teile.append(Teil(q["name"], q["shape"], "FPC", masse_kg=q["masse"]))
        ctx.schneide(q["shape"], ["BT-230"], "fpc")
    return teile


@teil("elektronik.fpc_halter", "BT-361", "F")
def fpc_halter(ctx, pos):
    """FPC-Halter BT-361 (LFP): Kunststoffstreifen je Reihe und Spur im Seitenspalt, hält den FPC-Stapel (Stapelhöhe A_e2_fpc_halter_mm). NMC: keine
    (FPC liegt unter dem Pad). Werkstoff Kunststoff (farben.json). Stufe F."""
    if VAR != "LFP": return []
    _, halter = _fpc_stuecke(ctx)
    for h in halter: ctx.schneide(h["shape"], ["BT-230"], "fpc_halter")
    return [Teil(h["name"], h["shape"], "Kunststoff") for h in halter]


def _tab_ort(ctx, rw):
    """LFP: y-Lage der Tabs/NTC am Zellende (Ebene der Polfahnen; zwischen den Fahnen, in Höhe der Zellmitte frei)."""
    pt = a("A_g54_pol_lfp_mm")[2]; Lc = ctx.zell_mass["L"]
    ys = [c["cy"] for c in ctx.zellen if c["reihe"] == rw]; yc = sum(ys) / len(ys)
    return (yc - Lc / 2 - pt) if rw == 0 else (yc + Lc / 2 + pt)        # Ebene, in der die Fahnen an die Verbinder stoßen


@teil("elektronik.fpc_detail", "BT-360", "F")
def fpc_detail(ctx, pos):
    """FPC-Details BT-360: Ni-Tab je Abgriff (A_e2d_fpc_tab_mm 8 × 4 × 0,2) und FPC-Stecker je CMU (A_e2d_fpc_stecker_mm 25 × 8 × 6, auf der CMU-Oberkante).
    LFP: Tab auf der Fahnenebene zwischen zwei Fahnen (x an der Zellgrenze, Dicke 0,2 nach innen); NMC: auf der Verbinderebene unter dem Pad
    (schneidet das Pad). Stückzahl aus der Geometrie (menge_quelle CAD). Stufe F."""
    R = verdr(ctx); ftab = a("A_e2d_fpc_tab_mm"); fst = a("A_e2d_fpc_stecker_mm"); zc = ctx.z_mitte_zelle; teile = []
    for i, (tx, ty) in enumerate(R["taps"]):
        if VAR == "NMC":
            s = quader(tx - ftab[0] / 2, ty - ftab[1] / 2, ctx.z_pad_o_u, tx + ftab[0] / 2, ty + ftab[1] / 2, ctx.z_pad_o_u + ftab[2]); ctx.schneide(s, ["BT-230"], "fpc_tab")
        else:
            rw = R["tap_row"][i]; ye = _tab_ort(ctx, rw)
            y0, y1 = (ye, ye + ftab[2]) if rw == 0 else (ye - ftab[2], ye)
            s = quader(tx - ftab[1] / 2, y0, zc - ftab[0] / 2, tx + ftab[1] / 2, y1, zc + ftab[0] / 2)
        teile.append(Teil(f"FPC_Tab_{i:03d}", s, "Cu_verzinnt"))
    zt = zc + R["cmuB"] / 2
    for j in range(R["ncmu"]):
        x0, _ = R["cmu_x"][R["seite"][j]]; y = R["ypos"][j]
        yf = min(max(R["lane"][j] if VAR == "NMC" else y, y - R["cmuL"] / 2 + fst[0] / 2), y + R["cmuL"] / 2 - fst[0] / 2)
        teile.append(Teil(f"FPC_Stecker_{j:02d}", quader(x0 + 1, yf - fst[0] / 2, zt, x0 + 1 + fst[1], yf + fst[0] / 2, zt + fst[2]), "Kunststoff"))
    return teile


@teil("elektronik.ntc", "BT-330", "F")
def ntc(ctx, pos):
    """Temperaturfühler NTC BT-330 (LFP 56, NMC 52; ENT-116/117): 4 je CMU auf Abgriffen (A_e2d_ntc_je_cmu), Maße A_e2d_ntc_mm 3 × 2 × 1.
    NMC: auf der Verbinderebene neben dem Abgriff, nicht unter dem FPC-Streifen (wie e2d, Versätze ±8/±6/±10 mm, dazu ±14 mm als Ausweichplätze neben einer Pol-Lasche); LFP: an der Fahnenebene neben dem Abgriff,
    seitlich versetzt um Teilungen, nicht im Querträgerbereich. Stufe F."""
    R = verdr(ctx); nm = a("A_e2d_ntc_mm"); n_je = int(a("A_e2d_ntc_je_cmu")); fw = p("BT-360", "breite_mm"); zc = ctx.z_mitte_zelle; teile = []
    if VAR == "NMC":
        for j in range(R["ncmu"]):
            xf = R["cmu_x"][R["seite"][j]][0 if R["seite"][j] == "vorn" else 1]
            xs_ = [xf] + [R["taps"][i][0] for i in R["grp_t"][j]]; xa, xb = min(xs_) - 1, max(xs_) + 1; ly0, ly1 = R["lane"][j] - fw / 2 - 1, R["lane"][j] + fw / 2 + 1
            gesetzt = 0
            for i in R["grp_t"][j]:
                if gesetzt >= n_je: break
                tx, ty = R["taps"][i]
                for ox, oy in ((8, 6), (8, -6), (-8, 6), (-8, -6), (0, 10), (0, -10), (14, 0), (-14, 0), (0, 14), (0, -14)):
                    x0, x1, y0, y1 = tx + ox - nm[0] / 2, tx + ox + nm[0] / 2, ty + oy - nm[1] / 2, ty + oy + nm[1] / 2
                    lw_ = a("A_e2_lasche_mm")[0] / 2
                    if any(x1 > c_["cx"] - lw_ and x0 < c_["cx"] + lw_ and y1 > c_["cy"] - lw_ and y0 < c_["cy"] + lw_ for c_ in R["ans"].values()): continue     # nicht unter einer Pol-Lasche (Platte 25 × 25); fällt ein Abgriff weg, nimmt die CMU den nächsten Abgriff ihrer Gruppe
                    if not (x1 > xa and x0 < xb and y1 > ly0 and y0 < ly1):
                        s = quader(x0, y0, ctx.z_pad_o_u, x1, y1, ctx.z_pad_o_u + nm[2]); ctx.schneide(s, ["BT-230"], "ntc")
                        teile.append(Teil(f"NTC_{j:02d}_{i:03d}", s, "Kunststoff")); gesetzt += 1; break
    else:
        pitch = ctx.zell_mass["pitch"]; qx = [(x - 0.5, x + ctx.qb + 0.5) for x in ctx.quertraeger_x]
        for j in range(R["ncmu"]):
            for i in R["grp_t"][j][:n_je]:
                tx = R["taps"][i][0]; rw = R["tap_row"][i]; ye = _tab_ort(ctx, rw)
                xn = next(tx + o * pitch for o in (0.75, -0.75, 0.25, -0.25, 1.25, -1.25, 1.75, -1.75, 2.25, -2.25, 2.75, -2.75, 3.25, -3.25)
                          if not any(a_ < tx + o * pitch + nm[0] / 2 and b_ > tx + o * pitch - nm[0] / 2 for a_, b_ in qx))
                y0, y1 = (ye, ye + nm[2]) if rw == 0 else (ye - nm[2], ye)
                teile.append(Teil(f"NTC_{j:02d}_{i:03d}", quader(xn - nm[0] / 2, y0, zc - nm[1] / 2, xn + nm[0] / 2, y1, zc + nm[1] / 2), "Kunststoff"))
    return teile


@teil("elektronik.daisy_kette", "BT-360", "F")
def daisy_kette(ctx, pos):
    """Daisy-Chain BT-360: Kabel Ø A_e2d_daisy_d_mm zwischen benachbarten CMU derselben Endzone (unter der CMU-Unterkante) mit Steckern
    A_e2d_daisy_stecker_mm (In/Out je CMU). Ein Teil je Kabel (mit seinen zwei Steckern), die Endstecker der Kette hängen am ersten/letzten Kabel.
    Die Querverbindung zwischen den Endzonen (e2d: nicht gezeichnet, 1880…1980 mm) fehlt auch hier. Stufe F."""
    R = verdr(ctx); dst = a("A_e2d_daisy_stecker_mm"); dd = a("A_e2d_daisy_d_mm"); zc = ctx.z_mitte_zelle; zb = zc - R["cmuB"] / 2; teile = []
    def stecker(j, y0):
        x0 = R["cmu_x"][R["seite"][j]][0]
        return quader(x0 + 1, y0, zb - dst[2], x0 + 1 + dst[1], y0 + dst[0], zb)
    for sd in ("vorn", "hinten"):
        ids = sorted([j for j in range(R["ncmu"]) if R["seite"][j] == sd], key=lambda j: R["ypos"][j])
        kabel = []
        for a_, b_ in zip(ids, ids[1:]):
            x0 = R["cmu_x"][sd][0]; ya, yb = R["ypos"][a_] + 45, R["ypos"][b_] - 45
            k = Part.makeCylinder(dd / 2, yb - ya, V(x0 + 1 + dst[1] / 2, ya, zb - dst[2] / 2), V(0, 1, 0))
            k = Part.makeCompound([k, stecker(a_, R["ypos"][a_] + 30), stecker(b_, R["ypos"][b_] - 45)]); kabel.append(k)
        if not kabel: continue
        kabel[0] = Part.makeCompound([kabel[0], stecker(ids[0], R["ypos"][ids[0]] - 45)])
        kabel[-1] = Part.makeCompound([kabel[-1], stecker(ids[-1], R["ypos"][ids[-1]] + 30)])
        for k in kabel: teile.append(Teil(f"Daisy_{sd}_{len(teile):02d}", k, "Kunststoff"))
    return teile


@teil("elektronik.bms_platine", "BT-310", "F")
def bms_platine(ctx, pos):
    """BMS-Platine BT-310 (Akte BT-310 laenge/breite/hoehe, ENT-144 Einbauort): lokal x ∈ ±lx/2, y ∈ ±ly/2 (Maße aus ctx.schaltbox["geraete"]), Platine
    A_e2d_bms_platine_dicke_mm auf 4 Abstandsbolzen M4 (A_e2d_bms_abstandsbolzen*), drei Stecker A_e2d_bms_stecker_mm. Masse A_e2_bms_masse_kg. Stufe F."""
    g, pl = _geraet(ctx, "BMS_Platine")
    if g is None: return []
    lx, ly, lz = g["l"]; pd = a("A_e2d_bms_platine_dicke_mm"); n, d, h = a("A_e2d_bms_abstandsbolzen"); ao = a("A_e2d_bms_abstandsbolzen_aussen_mm"); ez = a("A_e2d_bms_abstandsbolzen_einzug_mm")
    sl, sb, sh = a("A_e2d_bms_stecker_mm"); ys = a("A_g54_bms_stecker_y_mm")
    s = quader(-lx / 2, -ly / 2, h, lx / 2, ly / 2, h + pd)
    for sx in (-1, 1):
        for sy in (-1, 1): s = s.fuse(zylinder(ao / 2, h, sx * (lx / 2 - ez), sy * (ly / 2 - ez), 0))
    for yy in ys: s = s.fuse(quader(lx / 2 - 10 - sb, -ly / 2 + yy, h + pd, lx / 2 - 10, -ly / 2 + yy + sl, h + pd + sh))
    return [Teil("BMS_Platine", setze(s.removeSplitter(), pl), "Leiterplatte", masse_kg=a("A_e2_bms_masse_kg"))]


@teil("elektronik.shunt", "BT-340", "F")
def shunt(ctx, pos):
    """Shunt BT-340 (Strommessung): Messplatine A_e2d_shunt_platine_mm, darauf zwei Cu-Enden mit Bohrung A_e2d_schiene_bohrung_mm an den Klemmen aus
    ctx.schaltbox["geraete"] und Manganin-Steg A_e2d_shunt_steg_mm in der Mitte (lokal y = Längsrichtung). Masse A_e2_shunt_masse_kg. Stufe F."""
    g, pl = _geraet(ctx, "Shunt")
    if g is None: return []
    lx, ly, lz = g["l"]; stg = a("A_e2d_shunt_steg_mm"); spl = a("A_e2d_shunt_platine_mm"); sb = a("A_e2d_schiene_bohrung_mm")
    s = quader(-lx / 2, -ly / 2, 0, lx / 2, ly / 2, spl[2])
    for sg in (-1, 1):
        ya, yb = (stg / 2, ly / 2) if sg > 0 else (-ly / 2, -stg / 2)
        cu = quader(-lx / 2, ya, spl[2], lx / 2, yb, lz)
        ky = next(k[2] for k in g["klemmen"] if (k[2] > 0) == (sg > 0))
        s = s.fuse(cu.cut(zylinder(sb / 2, lz, 0, ky, 0)))
    s = s.fuse(quader(-lx / 2, -stg / 2, spl[2], lx / 2, stg / 2, lz))
    return [Teil("Shunt", setze(s.removeSplitter(), pl), "Cu", masse_kg=a("A_e2_shunt_masse_kg"))]


@teil("elektronik.isolationswaechter", "BT-350", "H")
def isolationswaechter(ctx, pos):
    """Isolationswächter BT-350 (ENT-120): Stufe H (keine Formangabe außer der Hüllgröße A_g5_isolationswaechter_mm), Gehäuse mit gerundeten Kanten
    (A_g54_isolationsw_eckradius_mm), sitzt in der Schaltbox an der von schaltbox.py gesetzten Lage. Werkstoff Leiterplatte (Masse offen, aus Volumen)."""
    g, pl = _geraet(ctx, "Isolationswaechter")
    if g is None: return []
    from kern import quader_r
    lx, ly, lz = g["l"]
    return [Teil("Isolationswaechter", setze(quader_r(-lx / 2, -ly / 2, 0, lx / 2, ly / 2, lz, a("A_g54_isolationsw_eckradius_mm"), "alle"), pl), "Leiterplatte")]
