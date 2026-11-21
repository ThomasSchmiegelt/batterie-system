# KI-generiert (Claude Sonnet, 2026-11-19), Entwurf. Auftrag G5.4 (cad/baukasten/AUFTRAG_G5_4.md), Modul verbinder.
"""Verbinder: Zellverbinder/Abgriffe/Gruppenverbinder (BT-410/420), HV-Leitung BT-430, Pol-Lasche und Stromschiene BT-440, Berührschutz BT-450,
Trennbrücke BT-720/721, Servicedeckel BT-520 (Pos 520.2, LFP). Verschaltung aus teile/_verdrahtung.py (LFP Schleife ENT-148, NMC Mäander ENT-145).
Logik der Lage aus cad/pack/pack_e2d.py; Maße nur über p() und a(). Stufe K, HV-Leitung F."""
import math
from kern import teil, p, a, Teil, quader, zylinder, bohrungen, rohr, setze, einbau, VAR, Part, V
from teile._verdrahtung import verdr


def _verb(ctx):
    """Gemeinsamer Zustand der Verbinder-Generatoren (dict, damit Ctx.als_dict ihn nicht ins JSON nimmt; ein Lauf = ein Ctx)."""
    if not hasattr(ctx, "verb"): ctx.verb = {}
    return ctx.verb


# ------------------------------------------------------------------ Hilfen
def _rohr_pfad(pts, R, r):
    """Rohrzug: Polygonzug pts mit Rundung R an den Ecken, Kreisquerschnitt r. Rückgabe (Solid, Länge, Geradenstücke[(P,Q)])."""
    P = [V(*q) for q in pts]; edges = []; cur = P[0]; gerade = []
    for i in range(1, len(P) - 1):
        d1 = P[i] - P[i - 1]; d1.normalize(); d2 = P[i + 1] - P[i]; d2.normalize()
        ang = math.acos(max(-1.0, min(1.0, d1.dot(d2)))); t = R * math.tan(ang / 2)
        s = P[i] - d1 * t; e = P[i] + d2 * t
        assert (s - cur).dot(d1) > -1e-6 and (P[i + 1] - e).dot(d2) > -1e-6, ("Rohrzug: Ecke %d zu kurz für Radius %.0f" % (i, R), pts)
        n = d2 - d1 * d1.dot(d2); n.normalize(); cen = s + n * R
        mv = (s - cen) + (e - cen); mv.normalize(); m = cen + mv * R
        if (s - cur).Length > 1e-6: edges.append(Part.makeLine(cur, s)); gerade.append((cur, s))
        edges.append(Part.Arc(s, m, e).toShape()); cur = e
    edges.append(Part.makeLine(cur, P[-1])); gerade.append((cur, P[-1]))
    w = Part.Wire(edges); d0 = P[1] - P[0]; d0.normalize()
    prof = Part.Wire(Part.makeCircle(r, P[0], d0))
    s_ = w.makePipeShell([prof], True, True)
    L = sum(e.Length for e in edges)
    return s_, L, gerade


def _bohr(cx, cy, z0, z1, r): return zylinder(r, z1 - z0, cx, cy, z0)


def _ax(v): return max(range(3), key=lambda i: abs(v[i]))


# ------------------------------------------------------------------ Lagen der Anschlüsse (rein aus ctx)
def _anschluesse(ctx):
    """Lage der Pole an den Reihenenden: dict name -> dict(cell, band 'u'/'o', ...). LFP: Plus = kette[0] (Plus-Fahne oben), Minus = kette[-1] (Minus-Fahne unten).
    NMC: Zellen des Mäanders (verdr: ans)."""
    R = verdr(ctx)
    if VAR == "NMC": return {k: dict(cell=v) for k, v in R["ans"].items()}
    return {"Plus": dict(cell=R["kette"][0], band="o"), "Minus": dict(cell=R["kette"][-1], band="u")}


def _lasche(ctx):
    """Geometrie der Pol-Laschen und Kabelfüße (gemeinsam für pol_lasche und hv_leitung). Ergebnis in _verb(ctx)['lasche'] (dict)."""
    if "lasche" in _verb(ctx): return _verb(ctx)["lasche"]
    lw, lt = a("A_e2_lasche_mm"); bo = a("A_e2_lasche_bohrung_mm") / 2; zc = ctx.z_mitte_zelle; out = {}
    pw, ph, pt = a("A_g54_pol_lfp_mm") if VAR == "LFP" else (0, 0, 0); dz = a("A_g54_pol_lfp_versatz_mm") if VAR == "LFP" else 0
    gt = a("A_zellverbinder_LFP_mm")[1]; rs = a("A_g54_lasche_lfp_riser_mm"); Dc = ctx.zell_mass["D"]; Lc = ctx.zell_mass.get("L", 0)
    for nm, an in _anschluesse(ctx).items():
        c = an["cell"]
        if VAR == "NMC":
            z0 = ctx.z_pad_o_u; sh = quader(c["cx"] - lw / 2, c["cy"] - lw / 2, z0, c["cx"] + lw / 2, c["cy"] + lw / 2, z0 + lt)
            sh = sh.cut(_bohr(c["cx"], c["cy"], z0 - 1, z0 + lt + 1, bo))
            out[nm] = dict(shape=sh, loch=(c["cx"], c["cy"]), z_oben=z0 + lt, plate=quader(c["cx"] - lw / 2, c["cy"] - lw / 2, z0, c["cx"] + lw / 2, c["cy"] + lw / 2, z0 + lt))
        else:
            row = c["reihe"]; sg = 1 if row == 0 else -1                    # sg = Richtung nach innen (+y für Reihe 0)
            ytip = c["cy"] - Lc / 2 - pt if row == 0 else c["cy"] + Lc / 2 + pt
            ya, yb = (ytip - gt, ytip) if row == 0 else (ytip, ytip + gt)
            zb = (zc + dz - ph / 2, zc + dz + ph / 2) if an["band"] == "o" else (zc - dz - ph / 2, zc - dz + ph / 2)
            xe = c["cx"] + Dc / 2; z0 = ctx.z_zelle_o; fh = a("A_e2_fpc_halter_mm")
            yin = (ctx.rand + fh + 0.2) if row == 0 else (ctx.B - ctx.rand - fh - 0.2)      # hinter dem FPC-Stapel im Seitenspalt
            ys0, ys1 = (ya, yin + rs) if row == 0 else (yin - rs, yb)
            foot = quader(c["cx"] - pw / 2, ya, zb[0], xe + rs, yb, zb[1])
            stufe = quader(xe, ys0, zb[0], xe + rs, ys1, zb[1])                                 # auf Fahnenhöhe zwischen den FPC-Spuren nach innen
            riser = quader(xe, min(yin, yin + sg * rs), zb[0], xe + rs, max(yin, yin + sg * rs), z0 + lt)
            ypl0, ypl1 = (yin, yin + lw) if row == 0 else (yin - lw, yin)
            plate = quader(xe + rs - lw, ypl0, z0, xe + rs, ypl1, z0 + lt)
            hx, hy = xe + rs - lw / 2, (ypl0 + ypl1) / 2
            sh = foot.fuse(stufe).fuse(riser).fuse(plate.cut(_bohr(hx, hy, z0 - 1, z0 + lt + 1, bo))).removeSplitter()
            out[nm] = dict(shape=sh, loch=(hx, hy), z_oben=z0 + lt, plate=plate, riser=riser)
    _verb(ctx)["lasche"] = out
    return out


# ------------------------------------------------------------------ Zellverbinder LFP
@teil("verbinder.zellverbinder_lfp", "BT-420", "K")
def zellverbinder_lfp(ctx, pos):
    """Zellverbinder LFP BT-420 (249 = 248 Zell-Zell-Verbinder + 1 Querverbinder Reihenmitte; ENT-096…098, ENT-148 Schleife 2 Reihen): Al-Blech Breite
    25 (Akte BT-420) × Dicke 3 an der äußeren Stirnseite (Polebene), als Z-Streifen: unteres Stück auf der Minus-Fahne der einen, oberes auf der Plus-Fahne der
    nächsten Zelle (A_g54_pol_lfp_mm, Versatz A_g54_pol_lfp_versatz_mm). Über einen Querträger: Bogen über den Querträger (z = Querträgeroberkante + 1,
    A_quertraeger_spiel_mm Steg). Querverbinder: A (Minus der vordersten Zelle Reihe 0) und B (Plus der vordersten Zelle Reihe 1) als ein Teil, Lücke
    A_e2_bruecke_luecke_mm, überbrückt von verbinder.trennbruecke; Ausschnitt in Pad/Kühlplatte über der Platte (ctx.schneide). Stufe K.
    Nicht umgesetzt: Omega-Dehnbogen und Schweißlinien (K-Detail, offen)."""
    if VAR != "LFP": return []
    R = verdr(ctx); K = R["kette"]; nr0 = R["nr0"]; m = ctx.zell_mass; Dc, Lc = m["D"], m["L"]; zc = ctx.z_mitte_zelle
    pw, ph, pt = a("A_g54_pol_lfp_mm"); dz = a("A_g54_pol_lfp_versatz_mm"); gt = a("A_zellverbinder_LFP_mm")[1]; sp = a("A_quertraeger_spiel_mm")
    qh = p("BT-530", "hoehe_mm"); zl = (zc - dz - ph / 2, zc - dz + ph / 2); zu = (zc + dz - ph / 2, zc + dz + ph / 2)
    za0 = zc + qh / 2; qx = [(x, x + ctx.qb) for x in ctx.quertraeger_x]; teile = []
    def ebene(c): return (c["cy"] - Lc / 2 - pt - gt, c["cy"] - Lc / 2 - pt) if c["reihe"] == 0 else (c["cy"] + Lc / 2 + pt, c["cy"] + Lc / 2 + pt + gt)
    for i in range(len(K) - 1):
        if i == nr0 - 1: continue
        c1, c2 = K[i], K[i + 1]; ya, yb = ebene(c1); d = 1 if c2["cx"] > c1["cx"] else -1
        xm = (c1["cx"] + c2["cx"]) / 2; box = lambda xa, xb, za, zb: quader(min(xa, xb), ya, za, max(xa, xb), yb, zb)
        q = [qq for qq in qx if min(c1["cx"], c2["cx"]) < qq[0] < max(c1["cx"], c2["cx"])]
        if not q:
            s = box(c1["cx"] - d * pw / 2, xm + d * gt / 2, zl[0], zl[1]).fuse(box(xm - gt / 2, xm + gt / 2, zl[0], zu[1])).fuse(box(xm - d * gt / 2, c2["cx"] + d * pw / 2, zu[0], zu[1]))
        else:
            q0, q1 = q[0]; nah, fern = (q0, q1) if d > 0 else (q1, q0)
            r1 = (nah - d * sp, nah); r2 = (fern, fern + d * sp)
            s = box(c1["cx"] - d * pw / 2, r1[0], zl[0], zl[1]).fuse(box(r1[0], r1[1], zl[0], za0 + gt)).fuse(box(r1[0], r2[1], za0, za0 + gt)) \
                .fuse(box(r2[0], r2[1], zu[0], za0 + gt)).fuse(box(r2[1], c2["cx"] + d * pw / 2, zu[0], zu[1]))
        teile.append(Teil(f"Zellverbinder_{i:03d}", s.removeSplitter(), "Al"))
    # Querverbinder (Reihenmitte, vorn): Streifen auf Fahnenhöhe längs y (frei zwischen CMU und FPC-Stegen), Steg nach oben, Platte auf den Zellen
    cA, cB = K[nr0 - 1], K[nr0]; x_c0 = min(c["cx"] for c in ctx.zellen) - Dc / 2; ro, rt = a("A_g54_querverbinder_riser_mm"); bw = p("BT-420", "breite_mm")
    gap = a("A_e2_bruecke_luecke_mm"); ov = a("A_e2_bruecke_ueberlappung_mm"); py = _quer_y(ctx); z0 = ctx.z_zelle_o; xs = x_c0 + ro; stuecke = []
    _verb(ctx)["quer"] = dict(x0=xs + 7, x1=xs + 7 + bw, py=py, gap=gap, z_oben=z0 + gt)
    xc = xs + 7 + bw / 2; ys_b = (py - gap / 2 - ov / 2, py + gap / 2 + ov / 2); bo = a("A_e2d_schiene_bohrung_mm") / 2
    for c, band, yE, ysch in ((cA, zl, py - gap / 2, ys_b[0]), (cB, zu, py + gap / 2, ys_b[1])):
        ya, yb = ebene(c); lo = c is cA
        s = quader(xs, ya, band[0], c["cx"] + pw / 2, yb, band[1])                                           # Fuß auf der Fahne
        s = s.fuse(quader(xs, ya if lo else yE, band[0], xs + rt, yE if lo else yb, band[1]))                # Streifen längs y
        s = s.fuse(quader(xs, yE - rt if lo else yE, band[0], xs + rt, yE if lo else yE + rt, z0 + gt))      # Steg nach oben
        pl = quader(xs, yE - ov if lo else yE, z0, xs + bw + 7, yE if lo else yE + ov, z0 + gt).cut(_bohr(xc, ysch, z0 - 1, z0 + gt + 1, bo))
        s = s.fuse(pl); stuecke.append(s.removeSplitter()); ctx.schneide(s, ["BT-230", "BT-610"], "querverbinder")
    teile.append(Teil("Querverbinder_Mitte", Part.makeCompound(stuecke), "Al"))
    return teile


def _quer_y(ctx):
    """y-Lage der Querverbinder-Lücke: möglichst mittig (B/2), Stege frei von den vorderen CMU (Abstand ≥ halbe CMU-Länge + 2)."""
    if "quer_y" in _verb(ctx): return _verb(ctx)["quer_y"]
    R = verdr(ctx); gap = a("A_e2_bruecke_luecke_mm"); cL = R["cmuL"]; rt = a("A_g54_querverbinder_riser_mm")[1]
    yv = [R["ypos"][j] for j in range(R["ncmu"]) if R["seite"][j] == "vorn"]; y0 = ctx.B / 2; best = None
    for k in range(0, 400):
        for sg in ((1, -1) if k else (1,)):
            y = y0 + sg * k * 2.5; ri = [(y - gap / 2 - rt, y - gap / 2), (y + gap / 2, y + gap / 2 + rt)]
            if all(abs((lo + hi) / 2 - c) >= cL / 2 + 2 + rt for lo, hi in ri for c in yv): best = y; break
        if best is not None: break
    assert best is not None, "keine freie y-Lage für den Querverbinder"
    _verb(ctx)["quer_y"] = best
    return best


# ------------------------------------------------------------------ NMC
@teil("verbinder.zellabgriff", "BT-410", "K")
def zellabgriff(ctx, pos):
    """Zellabgriff NMC BT-410 (1736 = 2 je Zelle; ENT-093/094/099): Scheibe A_zellabgriff_NMC_mm Ø12 × 1 auf jedem Pol. Plus mittig auf dem Pluspol (in der Ringnut
    der Zelle), Minus am Becherrand (Mittelpunkt A_g54_nmc_minus_abgriff_mm von der Achse, quer zum Pfad, Vorzeichen wechselnd). Laserschweißung nicht modelliert. Stufe K."""
    if VAR != "NMC": return []
    dd, tt = a("A_zellabgriff_NMC_mm"); off = a("A_g54_nmc_minus_abgriff_mm"); z0 = ctx.z_zelle_o; teile = []
    for i, c in enumerate(ctx.zellen):
        teile.append(Teil(f"Abgriff_Plus_{i:03d}", zylinder(dd / 2, tt, c["cx"], c["cy"], z0), "Al"))
        teile.append(Teil(f"Abgriff_Minus_{i:03d}", zylinder(dd / 2, tt, c["cx"], c["cy"] + (off if i % 2 == 0 else -off), z0), "Al"))
    return teile


def _strip(ctx, pa, pb, z0, z1, gb):
    dx, dy = pb[0] - pa[0], pb[1] - pa[1]; Ln = math.hypot(dx, dy); nx, ny = -dy / Ln * gb, dx / Ln * gb
    pts = [V(pa[0] + nx, pa[1] + ny, z0), V(pb[0] + nx, pb[1] + ny, z0), V(pb[0] - nx, pb[1] - ny, z0), V(pa[0] - nx, pa[1] - ny, z0)]; pts.append(pts[0])
    return Part.Face(Part.makePolygon(pts)).extrude(V(0, 0, z1 - z0))


def _nmc_gruppen(ctx):
    if "gruppen" in _verb(ctx): return _verb(ctx)["gruppen"]
    R = verdr(ctx); cells = R["cells"]; gb = p("BT-420", "breite_mm") / 2; dd, tt = a("A_zellabgriff_NMC_mm"); gv = p("BT-420", "dicke_mm")
    z0 = ctx.z_zelle_o + tt; z1 = z0 + gv; gsh = []
    for g in R["mw"]["gruppen"]:
        cs = [cells[i] for i in g]; sh = [Part.makeCylinder(gb, z1 - z0, V(c["cx"], c["cy"], z0)) for c in cs]
        for ca, cb in zip(cs, cs[1:]): sh.append(_strip(ctx, (ca["cx"], ca["cy"]), (cb["cx"], cb["cy"]), z0, z1, gb))
        s = sh[0]
        for q in sh[1:]: s = s.fuse(q)
        gsh.append(s.removeSplitter())
    _verb(ctx)["gruppen"] = (gsh, z0, z1, gb)
    return _verb(ctx)["gruppen"]


@teil("verbinder.gruppenverbinder", "BT-420", "K")
def gruppenverbinder(ctx, pos):
    """Gruppenverbinder NMC BT-420 (217, je 4 parallele Zellen, ENT-096…098, Mäander ENT-145): Al-Streifen Breite 25 (Akte BT-420), Dicke 3, als Scheiben Ø25 über jedem
    Pluspol-Abgriff, verbunden durch Streifen entlang des Mäanders (auch an den Spaltenwechseln). Nicht umgesetzt: Omega-Dehnbogen und Schweißlinien im
    Fenster (K-Detail, offen). Stufe K."""
    if VAR != "NMC": return []
    gsh, z0, z1, gb = _nmc_gruppen(ctx)
    return [Teil(f"Gruppenverbinder_{i:03d}", s, "Al") for i, s in enumerate(gsh)]


@teil("verbinder.gruppenbruecke", "BT-420", "K")
def gruppenbruecke(ctx, pos):
    """Gruppenbrücke NMC BT-420 (216): Streifen zwischen letzter Zelle einer Gruppe und erster der nächsten (Mäander-Folge), ohne die Gruppenverbinder (ausgeschnitten). Stufe K."""
    if VAR != "NMC": return []
    R = verdr(ctx); cells = R["cells"]; gsh, z0, z1, gb = _nmc_gruppen(ctx); gr = R["mw"]["gruppen"]; teile = []
    for i in range(len(gr) - 1):
        ca, cb = cells[gr[i][-1]], cells[gr[i + 1][0]]
        s = _strip(ctx, (ca["cx"], ca["cy"]), (cb["cx"], cb["cy"]), z0, z1, gb).cut(gsh[i]).cut(gsh[i + 1])
        teile.append(Teil(f"Gruppenbruecke_{i:03d}", s, "Al"))
    return teile


@teil("verbinder.beruehrschutz", "BT-450", "K")
def beruehrschutz(ctx, pos):
    """Berührschutz NMC BT-450 (Kunststoff 1 mm, A_e2d_beruehrschutz_dicke_mm): eine Platte je Zellreihe (x) im hintersten Feld über den Gruppenverbindern
    (Fenster wie e2d), schneidet Pad und Kühlplatte aus. Ohne Omega-Bogen 1 mm über der Verbinderoberkante (A_g54_beruehrschutz_z_mm), über FPC, Tabs und NTC. Stufe K."""
    if VAR != "NMC": return []
    bs = a("A_e2d_beruehrschutz_dicke_mm"); gsh, z0, z1, gb = _nmc_gruppen(ctx); win = max(c["feld"] for c in ctx.zellen); teile = []
    rows = sorted({round(c["cx"], 3) for c in ctx.zellen if c["feld"] == win})
    for k, rx in enumerate(rows):
        cs = [c for c in ctx.zellen if c["feld"] == win and abs(c["cx"] - rx) < 1e-3]
        s = quader(rx - gb, min(c["cy"] for c in cs) - gb, z1 + a("A_g54_beruehrschutz_z_mm"), rx + gb, max(c["cy"] for c in cs) + gb, z1 + a("A_g54_beruehrschutz_z_mm") + bs)
        ctx.schneide(s, ["BT-230", "BT-610"], "beruehrschutz"); teile.append(Teil(f"Beruehrschutz_R{k:02d}", s, "Kunststoff"))
    return teile


# ------------------------------------------------------------------ Pol-Laschen, HV-Leitung
@teil("verbinder.pol_lasche", "BT-440", "K")
def pol_lasche(ctx, pos):
    """Pol-Lasche BT-440 (LFP 2: Plus, Minus; NMC 4: Plus, Minus, 2 × Reihenmitte; M8, Überlappung 25): Al, Breite 25 × Dicke 3 (A_e2_lasche_mm), Bohrung
    A_e2_lasche_bohrung_mm. LFP: Fuß auf der freien Fahne der Reihenendzelle hinten, Steg, Platte über den Zellen; NMC: Platte 25 × 25 auf dem Gruppenverbinder. Schneidet Pad und
    Kühlplatte aus; legt die Schraubstelle M8 für den Kabelschuh in ctx.schrauben. Stufe K."""
    teile = []
    for nm, L in _lasche(ctx).items():
        teile.append(Teil(f"Lasche_{nm}", L["shape"], "Al"))
        ctx.schneide(L["plate"], ["BT-230", "BT-610", "BT-450"], "lasche")
    return teile


def _kabel(ctx):
    """Kabelwege (Plus, Minus; NMC zusätzlich Reihenmitte A, B) → _verb(ctx)['kabel']: dict name -> dict(shape, L, gerade, ende_a, ende_b, pad, d, palme)."""
    if "kabel" in _verb(ctx): return _verb(ctx)["kabel"]
    from teile.schaltbox import _layout
    S = _layout(ctx)
    rhv = a(f"A_e2_hv_aussendurchmesser_{VAR}_mm") / 2; R = p("BT-430", "biegeradius_min_mm"); hu = a("A_e2d_kabelschuh_huelse_mm"); pw_, pl_t = a("A_e2d_kabelschuh_lasche_mm")
    pl_l = a("A_e2d_kabelschuh_lasche_laenge_mm"); wd = a("A_e2_box_wand_mm"); dpal = a("A_g54_kabelschuh_box_abstand_mm"); out = {}; lasch = _lasche(ctx)
    tb = a(f"A_e2d_schiene_cu_{VAR}_mm")[1]; yb0, yb1 = S["box"][1], S["box"][4]
    for nm in ("Plus", "Minus"):
        L = lasch[nm]; hx, hy = L["loch"]; zE = L["z_oben"] + pl_t + hu
        xi, yw, zin, _ = S["klemmen"]["HV_ein_" + nm.lower()]; sg = 1 if nm == "Plus" else -1       # sg: Richtung von der Wand ins Box-Innere
        ywall = yb0 if nm == "Plus" else yb1; yc = ywall + sg * (wd + dpal)                            # Mitte des Schienen-Pads (y); Palme zwischen Wand und Pad
        yE = yc - sg * (tb / 2 + pl_t + hu)                                                            # Ende des Leiters = Hülsenende außen an der Wand
        fy = hy + (1 if hy < ctx.B / 2 else -1) * (rhv + a("A_g54_kabelschuh_huelse_wand_mm") + a("A_g54_iso4017_mm")[10] / math.sqrt(3) + 1.0)                                            # Kabelfuß neben der Bohrung, zur Plattenmitte hin (e2d: Fuß rhv + 5 neben dem Loch)
        zt = max(zin, zE + R)    # Opus 2026-11-19: Eintritt liegt jetzt auf Höhe zE + R (schaltbox._layout) → waagerecht hinein, keine Schlaufe
        pts = [(hx, fy, zE), (hx, fy, zt), (xi, fy, zt), (xi, yE, zt)] if abs(zt - zin) < 1e-6 else [(hx, fy, zE), (hx, fy, zt), (xi, fy, zt), (xi, fy, zin), (xi, yE, zin)]
        sol, Ln, ger = _rohr_pfad(pts, R, rhv)
        out[nm] = dict(shape=sol, L=Ln, gerade=ger, ende_a=(hx, fy, zE, (0, 0, 1)), ende_b=(xi, yE, zin, (0, sg, 0)), pad=(xi, yc, zin, (0, sg, 0)), d=2 * rhv, palme=dict(loch=(hx, hy), fuss=(hx, fy), z=L["z_oben"], yc=yc, sg=sg, tb=tb))
    if VAR == "NMC":
        zd = ctx.z_deckel_o
        for nm in ("Mitte_A_Ende_Band2", "Mitte_B_Anfang_Band3"):
            L = lasch[nm]; x, y = L["loch"]; zs = L["z_oben"]
            out[nm] = dict(shape=zylinder(rhv, zd - zs, x, y, zs), L=zd - zs, gerade=[(V(x, y, zs), V(x, y, zd))], ende_a=(x, y, zs, (0, 0, 1)), ende_b=None, pad=None, d=2 * rhv, palme=None)
    for nm, k in out.items():
        x, y, z, _ = k["ende_a"]
        ctx.schneide(zylinder(rhv + a("A_g54_kabelschuh_huelse_wand_mm"), ctx.z_deckel_o + 2 - ctx.z_pad_o_u, x, y, ctx.z_pad_o_u), ["BT-230", "BT-610", "BT-520"], "kabelbohrung")
        if k["palme"]:
            hx, hy = k["palme"]["loch"]; zo = k["palme"]["z"]
            fx, fy_ = k["palme"]["fuss"]; rr = max(pw_ / 2, k["d"] / 2) + a("A_g54_kabelschuh_huelse_wand_mm")   # Opus 2026-11-20: ganzer Kabelschuh (Palme Loch→Fuß) frei, Kragen in der Kühlplatte
            ctx.schneide(quader(min(hx, fx) - rr, min(hy, fy_) - rr, zo, max(hx, fx) + rr, max(hy, fy_) + rr, ctx.z_deckel_o + 2), ["BT-230", "BT-610", "BT-520"], "kabelschuh")
            ctx.schneide(zylinder(a("A_e2d_m8_kopf_mm")[0] / 2 + 1, ctx.z_deckel_o + 2 - zo, hx, hy, zo), ["BT-230", "BT-610", "BT-520"], "schraubenkopf")
            ctx.schrauben.append(dict(typ="Sechskant", d=a("A_e2_lasche_bohrung_mm"), l=pl_t + a("A_e2_lasche_mm")[1] - (a("A_e2d_fpc_tab_mm")[2] if VAR == "NMC" else 0.0), placement=einbau(hx, hy, zo + pl_t), bt="BT-440"))      # NMC: Schaft endet über dem Ni-Tab (0,2) unter der Lasche
    _verb(ctx)["kabel"] = out
    return out


@teil("verbinder.hv_leitung", "BT-430", "F")
def hv_leitung(ctx, pos):
    """HV-Leitung BT-430 (LFP 2, NMC 4; ENT-100/101, ENT-142/143, Verlegung ENT-144): Rohrzug Ø = A_e2_hv_aussendurchmesser_<V>_mm mit Biegeradius
    BT-430 biegeradius_min_mm. Plus/Minus: vom Kabelschuh auf der Pol-Lasche (Hülse A_e2d_kabelschuh_huelse_mm senkrecht) nach oben bis zZ = max(Eintritt + 2 R, Hülsenende + R),
    seitlich zur Box, 90° nach unten und in die Box (Eintrittslage ctx.schaltbox['klemmen']['HV_ein_*']). NMC zusätzlich 2 senkrechte Mittenleitungen zum Trennstecker.
    Masse = Länge × BT-430 querschnitt_mm2 × Dichte Cu (Leiter, Isolierung ohne Wert). Bohrungen durch Pad, Kühlplatte, Deckel über ctx.schneide. Stufe F."""
    teile = []; q = p("BT-430", "querschnitt_mm2"); rho = 8960e-9
    for nm, k in _kabel(ctx).items(): teile.append(Teil(f"HV_{nm}", k["shape"], "PA_HV", masse_kg=k["L"] * q * rho))
    return teile


# ------------------------------------------------------------------ Stromschienen der Schaltbox
def _schienen(ctx):
    """Stromschienen der Schaltbox: je Verbindung aus ctx.schaltbox['schienen'] Pad (Breite × Breite × Dicke, Bohrung) an jedem Ende 12 mm vor der Gerätefläche
    (A_g54_schiene_pad_abstand_mm), senkrechte Stücke zur Leitungsebene über allen Geräten, dort waagerecht (erst x, dann y), zwei Ebenen im Wechsel. Ebene Stücke, keine Biegung (Stufe K).
    Pads mit Normale z (Shunt) bekommen ein Stück von Breite in +x vor dem senkrechten Stück."""
    if "schienen" in _verb(ctx): return _verb(ctx)["schienen"]
    from teile.schaltbox import _layout
    S = _layout(ctx); K = dict(S["klemmen"]); w, t = a(f"A_e2d_schiene_cu_{VAR}_mm"); e = a("A_g54_schiene_pad_abstand_mm"); bo = a("A_e2d_schiene_bohrung_mm") / 2
    kab = _kabel(ctx); res = []
    hmax = max(g["l"][2] for g in S["geraete"].values() if g["klemmen"]); zf = S["innen"][2]
    def term(n):
        if n in ("HV_ein_plus", "HV_ein_minus"):
            k = kab["Plus" if n.endswith("plus") else "Minus"]; x, y, z, d = k["pad"]; return V(x, y, z), V(*d), False
        x, y, z, d = K[n]; dv = V(*d); return V(x, y, z) + dv * e, dv, True
    for i, (na, nb) in enumerate(S["schienen"]):
        A, da, bolzA = term(na); B, db, bolzB = term(nb); zr = zf + hmax + t / 2
        pts = [A]
        def hoch(P, d):
            if _ax(d) == 2:                                                   # Pad liegt waagerecht: erst w seitwärts (+x), dann senkrecht
                Q = V(P.x + w, P.y, P.z); return [Q, V(Q.x, Q.y, zr)]
            return [V(P.x, P.y, zr)]
        pa_ = hoch(A, da); pb_ = hoch(B, db)
        pts += pa_; last = pa_[-1]
        mid = [V(pb_[-1].x, last.y, zr), V(pb_[-1].x, pb_[-1].y, zr)]
        pts += [q for q in mid if (q - pts[-1]).Length > 1e-6]
        pts += list(reversed(pb_[:-1])) if False else []
        # Rückweg zum Pad B: senkrecht nach unten
        for q in reversed([V(*c) for c in [(B.x, B.y, B.z)]] + (pb_[:-1][::-1] if len(pb_) > 1 else [])):
            pass
        ab = ([V(q.x, q.y, q.z) for q in reversed(pb_[:-1])] + [B]) if len(pb_) > 1 else [B]
        pts += [q for q in ab if (q - pts[-1]).Length > 1e-6]
        shapes = []; beine = []
        for j in range(len(pts) - 1):
            P_, Q_ = pts[j], pts[j + 1]; u = _ax(Q_ - P_)
            if u == 2:                                                         # senkrechtes Stück: Normale = Padnormale des nächstgelegenen Endes
                dd = da if j < len(pts) / 2 else db; n = _ax(dd) if _ax(dd) != 2 else 0
            else: n = 2
            m_ = 3 - u - n; lo = [min(P_[k], Q_[k]) for k in range(3)]; hi = [max(P_[k], Q_[k]) for k in range(3)]
            lo[u] -= t / 2; hi[u] += t / 2
            lo[n] = P_[n] - t / 2; hi[n] = P_[n] + t / 2; lo[m_] = P_[m_] - w / 2; hi[m_] = P_[m_] + w / 2
            shapes.append(quader(*lo, *hi)); beine.append((list(lo), list(hi), u, (P_ - Q_).Length))
        for c_, d_ in ((A, da), (B, db)):
            ax = _ax(d_); lo = [c_[k] - w / 2 for k in range(3)]; hi = [c_[k] + w / 2 for k in range(3)]; lo[ax] = c_[ax] - t / 2; hi[ax] = c_[ax] + t / 2
            shapes.append(quader(*lo, *hi))
        sh = shapes[0]
        for q in shapes[1:]: sh = sh.fuse(q)
        for c_, d_ in ((A, da), (B, db)): sh = sh.cut(Part.makeCylinder(bo, 3 * t, c_ - d_ * 1.5 * t, d_))
        sh = sh.common(quader(S["innen"][0] - 1000, S["innen"][1] - 1000, zf, S["innen"][3] + 1000, S["innen"][4] + 1000, zf + 1000))      # nicht unter den Boxboden (Wannenboden bleibt)
        res.append(dict(name=f"{na}__{nb}", shape=sh.removeSplitter(), A=(A, da, bolzA), B=(B, db, bolzB), pts=pts, w=w, t=t, beine=beine))
    _verb(ctx)["schienen"] = res
    return res


@teil("verbinder.stromschiene", "BT-440", "K")
def stromschiene(ctx, pos):
    """Stromschiene BT-440 in der Schaltbox (Cu 25 × 3 LFP / 20 × 3 NMC, A_e2d_schiene_cu_<V>_mm; Bohrung A_e2d_schiene_bohrung_mm 8,5): eine je Verbindung aus
    ctx.schaltbox['schienen'] (12 Stück, Stromlaufplan E2). Pad (Breite × Breite) 12 mm vor der Gerätefläche auf dem Bolzen, dazwischen rechtwinkliger Zug
    aus ebenen Stücken (Biegung nicht modelliert, Stufe K). Legt je Pad eine Mutter M8 in ctx.schrauben. Hinweis: Stückzahl 12, nicht 6 wie SL3 (Stückzahl aus CAD)."""
    teile = []
    for s in _schienen(ctx):
        teile.append(Teil("Schiene_" + s["name"], s["shape"], "Cu"))
        ctx.schneide(s["shape"], ["BT-710"], "wanddurchfuehrung")      # Durchführung der Schiene durch die Boxwand (Stecker liegen vor der Box)
        for (c_, d_, bolz) in (s["A"], s["B"]):
            if bolz: ctx.schrauben.append(dict(typ="Mutter", d=a("A_g54_mutter_mm")[0], l=0.0, placement=einbau(c_.x, c_.y, c_.z, (d_.x, d_.y, d_.z)).multiply(__import__("FreeCAD").Placement(V(0, 0, s["t"] / 2), __import__("FreeCAD").Rotation())), bt="BT-440"))
    return teile


# ------------------------------------------------------------------ Trennbrücke und Servicedeckel (LFP)
@teil("verbinder.trennbruecke", "BT-720", "K")
def trennbruecke(ctx, pos):
    """Trennbrücke LFP BT-720/BT-721 (2 Teile: Cu-Brücke 25 × 3 × 80 und HVIL-Brücke; ENT-130, ENT-150): Brücke auf dem Querverbinder (Lücke A_e2_bruecke_luecke_mm,
    Überlappung A_e2_bruecke_ueberlappung_mm je Seite), zwei M8-Bohrungen A_e2d_bruecke_schrauben; Schrauben M8 (Kopf ohne Scheibe, weil Scheibe 1,6 + Kopf 5,3 über der Brücke den Servicedeckel träfen) in ctx.schrauben. HVIL-Brücke
    A_e2d_hvil_mm 15 × 10 × 8 daneben auf den Zellen (Masse offen). Ausschnitt in Pad, Kühlplatte, Deckel (Serviceöffnung A_e2_serviceoeffnung_mm abzüglich A_e2d_servicedeckel_rand_mm). Stufe K."""
    if VAR != "LFP": return []
    zq = _verb(ctx).get("quer") or verbinder_quer(ctx)
    bw, bt, bl = a("A_e2d_bruecke_mm"); ov = a("A_e2_bruecke_ueberlappung_mm"); n, md = a("A_e2d_bruecke_schrauben"); py = zq["py"]; gap = zq["gap"]
    z0 = zq["z_oben"]; x0 = zq["x0"]; gt_q = a("A_zellverbinder_LFP_mm")[1]
    br = quader(x0, py - gap / 2 - ov, z0, x0 + bw, py + gap / 2 + ov, z0 + bt)
    ys = (py - gap / 2 - ov / 2, py + gap / 2 + ov / 2); xc = x0 + bw / 2
    br = bohrungen(br, [(xc, y, z0 - 1) for y in ys], a("A_e2d_schiene_bohrung_mm") / 2, bt + 2)
    for y in ys: ctx.schrauben.append(dict(typ="Sechskant", d=md, l=bt + gt_q, placement=einbau(xc, y, z0 + bt), bt="BT-720"))
    hl, hb, hh = a("A_e2d_hvil_mm"); hx = x0 + bw + 10
    hv = quader(hx, py - hb / 2, ctx.z_zelle_o, hx + hl, py + hb / 2, ctx.z_zelle_o + hh)
    oy, ox = a("A_e2_serviceoeffnung_mm"); rim = a("A_e2d_servicedeckel_rand_mm"); ox0 = ctx.rand + 2
    g = _service(ctx)
    for x, y in g["pts"]: ctx.schrauben.append(dict(typ="Linsenkopf", d=g["d"], l=g["sh"] + g["dgh"] + ctx.dec * 0.5, placement=einbau(x, y, g["z0"] + g["sh"]), bt="BT-520", **{"in": ["BT-520"]}))
    ctx.schneide(quader(min(ox0 + rim, x0 - 2), py - oy / 2 + rim, ctx.z_zelle_o, ox0 + ox - rim, py + oy / 2 - rim, ctx.z_deckel_o + 1), ["BT-230", "BT-610", "BT-520"], "serviceoeffnung")   # Opus 2026-11-19: Öffnung reicht bis 2 mm vor die Brücke (vorher Überlappung 1,5 mm mit der Kühlplatte)
    return [Teil("Trennbruecke_Cu", br, "Cu"), Teil("HVIL_Bruecke", hv, "Kunststoff")]


def verbinder_quer(ctx):
    zellverbinder_lfp(ctx, None); return _verb(ctx)["quer"]


def _service(ctx):
    """Lage des Servicedeckels (LFP) und seiner Schraubstellen; rein aus ctx (kern.Ctx: Rahmen, Deckel)."""
    sl, sb, sh = a("A_e2d_servicedeckel_mm"); dgw, dgh = a("A_e2d_servicedeckel_dichtung_mm"); n, d = a("A_e2d_servicedeckel_schrauben"); py = _quer_y(ctx); ox0 = ctx.rand + 2
    pts = [(ox0 + 4.5, py + dy) for dy in (-45, 0, 45)] + [(ox0 + sb - 4.5, py + dy) for dy in (-45, 0, 45)]
    return dict(sl=sl, sb=sb, sh=sh, dgw=dgw, dgh=dgh, d=d, py=py, x0=ox0, z0=ctx.z_deckel_o + dgh, pts=pts)


@teil("gehaeuse.servicedeckel", "BT-520", "K")
def servicedeckel(ctx, pos):
    """Servicedeckel BT-520 (Pos 520.2, LFP; hier registriert, weil er an der Trennbrücke liegt; ENT-150): Al-Blech A_e2d_servicedeckel_mm 120 × 80 × 2 auf der Dichtung
    (A_e2d_servicedeckel_dichtung_mm 3 × 3, normteile.dichtung) über der Serviceöffnung im Deckel, 6 Löcher M5 (A_e2d_servicedeckel_schrauben); die Senkschrauben meldet
    verbinder.trennbruecke (läuft vor normteile). Lage x ab Rahmen + 2 (wie e2d), y mittig. Stufe K."""
    if VAR != "LFP": return []
    g = _service(ctx); z0 = g["z0"]
    s = quader(g["x0"], g["py"] - g["sl"] / 2, z0, g["x0"] + g["sb"], g["py"] + g["sl"] / 2, z0 + g["sh"])
    s = bohrungen(s, [(x, y, z0 - 1) for x, y in g["pts"]], g["d"] / 2, g["sh"] + 2)
    return [Teil("Servicedeckel", s, "Al")]
