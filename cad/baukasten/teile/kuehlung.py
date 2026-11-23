# KI-generiert (Claude Opus, 2026-11-19; G5.9 ergänzt Claude Sonnet, 2026-11-23), Entwurf. G5.3 Kühlung (Stufe K/F). Version 2: Blechplatte mit Mäander (Autor-Vorschlag ENT-152).
# G5.9 (ENT-158, ENT-159): kanalfuehrung == "gruppiert_k2" teilt jede Platte in zwei Mäander zu je 4 Bahnen mit Trennsteg. Je Hälfte ein
# Ein- und ein Austrittsblock hinten (4 Blöcke je Platte-Paar), gespeist aus Verteilerrohr (Ein) und Sammelrohr (Aus), Innen-Ø verteilerrohr_d_mm,
# Z-Anordnung: Einspeisung am y-kleinen Ende, Abfluss am y-großen Ende. Beide Platten sind weiter parallel geschaltet, Ober-/Unterplatte
# teilen sich die Steigblöcke (gegenläufige Durchströmung ist im CAD NICHT abgebildet, Frage an Opus). Alte Logik bleibt für andere Werte.
"""Kühlung: Kühlplatten BT-610 (unten, oben), Verteiler/Sammler BT-620, Anschlüsse BT-630, Kühlkreis außen BT-661…665.

Kühlplatte (ENT-152…156): Al-Blech A_g5_blech_mm oben und unten, dazwischen Wasserraum (Dicke − 2 × Blech = 4 mm). Gelötete Stege
A_g5_kanal_steg_mm teilen den Wasserraum in n Mäander-Bahnen (längs, in x), jede Bahn aus parallelen Teilkanälen kanal_breite_mm.
An den Bahnenden verbinden Umlenkkammern (A_g5_umlenk_mm) je zwei Nachbarbahnen. Bahn 1 beginnt hinten links (Verteiler), bei
gerader Bahnzahl endet die letzte Bahn hinten rechts (Sammler). Beide Platten sind parallel geschaltet.
Kühlkreis außen (Kühlmodul hinter der Rückwand, Länge darf wachsen, Autor 2026-11-17):
  Austritt Pack → Ausgleichsbehälter (durchströmt) → Pumpe → 3/2-Wege-Ventil → Chiller → T-Stück → Eintritt Pack; Ventil-Bypass → T-Stück.
"""
import math
from kern import teil, p, a, Teil, quader, quader_r, zylinder, rohr, VAR, FreeCAD, Part, V


def _gruppiert():
    """G5.9: True bei ENT-158 (zwei parallele Mäander zu je 4 Bahnen)."""
    return p("BT-610", "kanalfuehrung", roh=True) == "gruppiert_k2"


def _ports(ctx):
    """Anschlussorte der Platte hinten: Liste dict(name, rolle ein|aus, y, bahn). Alt: Eintritt/Austritt in den Ecken. G5.9: je Hälfte
    Eintritt an Bahn 0 bzw. 4, Austritt an Bahn 3 bzw. 7 (Bahnenden hinten)."""
    by = a("A_g5_verteiler_mm")[1]
    if not _gruppiert():
        return [dict(name="Verteiler_links", rolle="ein", y=ctx.rand + by / 2, bahn=0), dict(name="Sammler_rechts", rolle="aus", y=ctx.B - ctx.rand - by / 2, bahn=-1)]
    M = _maeander(ctx); g = M["gruppe"]; out = []
    for h in range(M["n"] // g):
        for rolle, jj in (("ein", 0), ("aus", g - 1)):
            j = h * g + jj; y0, y1 = M["bahnen"][j]["y"]
            out.append(dict(name=("Verteiler_" if rolle == "ein" else "Sammler_") + "AB"[h], rolle=rolle, y=(y0 + y1) / 2, bahn=j))
    return out


def _ecken(ctx):
    """Steigblöcke: (x0, x1, y0, y1) AUSSEN hinter der Rückwand (Opus 2026-11-19: in der Endzone ist kein
    Platz, LFP 16 mm mit CMU, NMC 0 mm). Die Kühlplatten greifen mit einer flachen Lasche durch einen Schlitz im Rahmen hinein."""
    bx, by = a("A_g5_verteiler_mm"); L = ctx.L
    return [(L, L + bx, q["y"] - by / 2, q["y"] + by / 2) for q in _ports(ctx)]


def _rohrgeo(ctx):
    """G5.9 Verteiler-/Sammelrohr: Achse in y bei x_p, Verteilerrohr (Ein) bei z_ein, Sammelrohr (Aus) bei z_aus (Abstand = Außen-Ø + Spalt)."""
    di = p("BT-610", "verteilerrohr_d_mm"); w = a("A_g5_verteilerrohr_wand_mm"); da = di + 2 * w
    bx = a("A_g5_verteiler_mm")[0]; ab = a("A_g5_verteilerrohr_abstand_mm"); sp = a("A_g5_verteilerrohr_spalt_mm"); zc = ctx.z_mitte_zelle
    dz = (da + sp) / 2
    return dict(di=di, da=da, w=w, x_p=ctx.L + bx + ab + da / 2, z_ein=zc + dz, z_aus=zc - dz)


def _laschen(ctx, z0):
    """Plattenlaschen je Ecke: Vollkörper (x von Rahmeninnenkante bis Blockmitte) und Wasserkanal darin."""
    kp, tb = ctx.kp, a("A_g5_blech_mm"); rw = a("A_g5_sammler_mm")[1]; out = []
    for (x0, x1, y0, y1) in _ecken(ctx):
        xm = (x0 + x1) / 2
        voll = quader(ctx.L - ctx.rand - 1, y0, z0, xm, y1, z0 + kp)
        kanal = quader(ctx.L - ctx.rand - 2, y0 + rw, z0 + tb, xm - rw, y1 - rw, z0 + kp - tb)
        out.append((voll, kanal))
    return out


def _maeander(ctx):
    """Bahnen (y0, y1) und Teilkanäle (y0, y1) je Bahn, x-Bereich der Bahnen. Eine Quelle für Platte und Bericht."""
    m = a("A_g5_maeander"); n = int(p("BT-610", "kanal_anzahl")); w = p("BT-610", "kanal_breite_mm")
    assert m["fuehrung"] == "laengs" and n % 2 == 0, m
    s = a("A_g5_kanal_steg_mm"); rw = a("A_g5_sammler_mm")[1]; ul = a("A_g5_umlenk_mm"); bx = a("A_g5_verteiler_mm")[0]
    r = ctx.rand; y_a, y_b = r + rw, ctx.B - r - rw
    g = n // 2 if _gruppiert() else n                           # Bahnen je Mäander; G5.9: zwei Mäander (k = 2) mit Trennsteg dazwischen
    ts = a("A_g5_trennsteg_mm") if _gruppiert() else s
    assert g % 2 == 0 and n % g == 0, (n, g)
    extra = ts - s                                              # Trennsteg breiter als der Bahnsteg
    bb = (y_b - y_a - (n - 1) * s - (n // g - 1) * extra) / n
    x_a = r + rw + ul                           # vorn: Umlenkkammer davor
    x_b = ctx.L - r - bx - ul                   # hinten: Umlenkkammer / Verteiler dahinter
    bahnen = []
    for j in range(n):
        y0 = y_a + j * (bb + s) + (j // g) * extra; y1 = y0 + bb
        k = int((bb + s) // (w + s)); rest = bb - (k * w + (k - 1) * s)
        kan = [(y0 + rest / 2 + i * (w + s), y0 + rest / 2 + i * (w + s) + w) for i in range(k)]
        bahnen.append(dict(y=(y0, y1), kanaele=kan))
    return dict(n=n, gruppe=g, trennsteg=ts, w=w, bahnbreite=bb, x=(x_a, x_b), ul=ul, rw=rw, bahnen=bahnen, teilkanaele=sum(len(b["kanaele"]) for b in bahnen))


def _platte(ctx, z0, name):
    kp, tb = ctx.kp, a("A_g5_blech_mm"); hw = kp - 2 * tb
    assert abs(hw - p("BT-610", "kanal_hoehe_mm")) < 1e-6, ("Wasserraum ≠ Akte", hw)
    M = _maeander(ctx); r = ctx.rand; (x_a, x_b), ul = M["x"], M["ul"]
    zc0, zc1 = z0 + tb, z0 + tb + hw
    hohl = []
    for j, b in enumerate(M["bahnen"]):
        for (y0, y1) in b["kanaele"]:
            hohl.append(quader(x_a, y0, zc0, x_b, y1, zc1))
        y0, y1 = b["y"]
        # Umlenkung: vorn zwischen Bahn j und j+1 für gerade j, hinten für ungerade j (Bahn 0 läuft hinten → vorn)
        if j % M["gruppe"] < M["gruppe"] - 1:                  # kein Übergang zwischen den Mäandern (Trennsteg)
            yb1 = M["bahnen"][j + 1]["y"][1]
            if j % 2 == 0: hohl.append(quader(x_a - ul, y0, zc0, x_a + 1, yb1, zc1))
            else:          hohl.append(quader(x_b - 1, y0, zc0, x_b + ul, yb1, zc1))
    # Eintritt (Bahn 0) und Austritt (letzte Bahn): Kammer hinten bis in den Verteilerblock
    xr = ctx.L - r
    for q in _ports(ctx):
        b = M["bahnen"][q["bahn"]]
        hohl.append(quader(x_b - 1, b["y"][0], zc0, xr - a("A_g5_sammler_mm")[1], b["y"][1], zc1))
    for (vl, kn) in _laschen(ctx, z0):
        hohl.append(kn)
    void = hohl[0].multiFuse(hohl[1:]).removeSplitter()
    # Durchführungen anderer Module (HV-Leitung, Schraubenköpfe, Laschen): um jede ein Kragen ohne Wasser, damit nichts ausläuft
    kr = a("A_g5_kragen_kuehlplatte_mm"); kragen = []
    for shp, ziele, von in ctx.ausschnitte:
        if "BT-610" not in ziele or von == "verteiler": continue
        bb = shp.BoundBox
        if bb.ZMax < z0 or bb.ZMin > z0 + kp: continue
        kragen.append(quader(bb.XMin - kr, bb.YMin - kr, z0 - 1, bb.XMax + kr, bb.YMax + kr, z0 + kp + 1))
    if kragen: void = void.cut(Part.makeCompound(kragen))
    voll = quader(r, r, z0, ctx.L - r, ctx.B - r, z0 + kp)
    for (vl, kn) in _laschen(ctx, z0):
        voll = voll.fuse(vl)
        ctx.schneide(quader(ctx.L - r - 1, vl.BoundBox.YMin, z0, ctx.L + 1, vl.BoundBox.YMax, z0 + kp), ["BT-540"], "plattenlasche")   # Schlitz im Rahmen
    return Teil(name, voll.removeSplitter().cut(void), "Al_Kuehlplatte")


@teil("kuehlung.kuehlplatte", "BT-610", "K")
def kuehlplatte(ctx, pos):
    """Kühlplatten BT-610, 2 Stück (ENT-089): Blech A_g5_blech_mm + Wasserraum kanal_hoehe_mm (ENT-152/154), Mäander mit
    kanal_anzahl Bahnen (ENT-156) aus Teilkanälen kanal_breite_mm (ENT-155), Stege A_g5_kanal_steg_mm, Umlenkkammern A_g5_umlenk_mm.
    Masse = Volumen ohne Wasserraum × ρ_Al. Die Verteilerblöcke schneiden ihre Ecken aus (ctx.schneide)."""
    u = _platte(ctx, ctx.z_boden_ok, "Kuehlplatte_unten")
    o = _platte(ctx, ctx.z_kp_o_u, "Kuehlplatte_oben")
    M = _maeander(ctx); ctx.kuehlplatte = dict(bahnen=M["n"], maeander=M["n"] // M["gruppe"], bahnen_je_maeander=M["gruppe"], trennsteg_mm=M["trennsteg"], teilkanaele_je_platte=M["teilkanaele"], bahnbreite_mm=round(M["bahnbreite"], 1))
    return [u, o]


@teil("kuehlung.verteiler", "BT-620", "K")
def verteiler(ctx, pos):
    """Steigblöcke BT-620 (alt: Verteiler links, Sammler rechts; G5.9: je Hälfte ein Ein- und ein Austrittsblock, 4 Stück): Al-Block A_g5_verteiler_mm
    außen hinter der Rückwand, von der Unterkante der unteren bis zur Oberkante der oberen Kühlplatte. Die Plattenlaschen stecken in Schlitzen
    des Blocks; eine senkrechte Bohrung verbindet beide Laschenkanäle, eine waagerechte führt nach hinten (alt: Anschlussstutzen auf Höhe der
    Zellmitte; G5.9: Ein auf Höhe Verteilerrohr, Aus auf Höhe Sammelrohr)."""
    di = a("A_g5_anschluss_mm")[1]; z0, z1 = ctx.z_boden_ok, ctx.z_kp_o_u + ctx.kp; tb = a("A_g5_blech_mm")
    teile = []; ps = _ports(ctx); n = len(ps)
    las = _laschen(ctx, ctx.z_boden_ok) + _laschen(ctx, ctx.z_kp_o_u)
    rg = _rohrgeo(ctx) if _gruppiert() else None
    for k, (q, (x0, x1, y0, y1)) in enumerate(zip(ps, _ecken(ctx))):
        blk = quader_r(x0, y0, z0, x1, y1, z1, a("A_g5_kantenradius_profil_mm"), "x")
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        for vl, kn in (las[k], las[k + n]): blk = blk.cut(vl)
        zh = ctx.z_mitte_zelle if rg is None else (rg["z_ein"] if q["rolle"] == "ein" else rg["z_aus"])
        blk = blk.cut(zylinder(di / 2, z1 - z0 - 2 * tb, cx, cy, z0 + tb))
        blk = blk.cut(zylinder(di / 2, x1 - cx + 1, cx, cy, zh, "x"))
        teile.append(Teil(q["name"], blk, "Al"))
    return teile


def _stutzen(ctx):
    """Welt-Lage der Stutzenenden: ein, aus. Alt: Rückseite der Ecklöcher. G5.9: Rückseite von Verteiler- bzw. Sammelrohr
    (Einspeisung am Rohrende bei y des ersten Eintritts, Abfluss bei y des letzten Austritts: Z-Anordnung)."""
    da, di, ue = a("A_g5_anschluss_mm"); zc = ctx.z_mitte_zelle
    if not _gruppiert():
        return {n: (x1 + ue, (y0 + y1) / 2, zc) for n, (x0, x1, y0, y1) in zip(("ein", "aus"), _ecken(ctx))}
    rg = _rohrgeo(ctx); ps = _ports(ctx); xo = rg["x_p"] + rg["da"] / 2 + ue
    return dict(ein=(xo, [q for q in ps if q["rolle"] == "ein"][0]["y"], rg["z_ein"]), aus=(xo, [q for q in ps if q["rolle"] == "aus"][-1]["y"], rg["z_aus"]))


def _rohrkoerper(rg, y0, y1, xs_blk, ys_nippel, z, da_n, di_n):
    """Rohr (Achse y bei x_p, z) von y0 bis y1 mit Endkappen (Wand w), Nippel Ø da_n/di_n von der Blockfläche xs_blk zu den y in ys_nippel."""
    r_a, r_i, w = rg["da"] / 2, rg["di"] / 2, rg["w"]
    k = zylinder(r_a, y1 - y0, rg["x_p"], y0, z, "y")
    inn = zylinder(r_i, y1 - y0 - 2 * w, rg["x_p"], y0 + w, z, "y")
    for yn in ys_nippel:
        k = k.fuse(zylinder(da_n / 2, rg["x_p"] - xs_blk, xs_blk, yn, z, "x"))
    k = k.cut(inn)
    for yn in ys_nippel:
        k = k.cut(zylinder(di_n / 2, rg["x_p"] - xs_blk + 1, xs_blk - 1, yn, z, "x"))
    return k


@teil("kuehlung.verteilerrohr", "BT-620", "K")
def verteilerrohr(ctx, pos):
    """G5.9 (ENT-159): Verteilerrohr (Ein) und Sammelrohr (Aus), Al-Rohr Innen-Ø verteilerrohr_d_mm, Wand A_g5_verteilerrohr_wand_mm, Achse in y
    hinter den Steigblöcken, Ein oben / Aus unten (Spalt A_g5_verteilerrohr_spalt_mm). Je Steigblock ein Nippel (Außen-/Innen-Ø wie Anschlussstutzen).
    Loch für den Anschlussstutzen am Rohrende wird hier ausgespart. Nur für kanalfuehrung gruppiert_k2."""
    if not _gruppiert(): return []
    rg = _rohrgeo(ctx); da, di, ue = a("A_g5_anschluss_mm"); ps = _ports(ctx); bx = a("A_g5_verteiler_mm")[0]; x_blk = ctx.L + bx; S = _stutzen(ctx)
    teile = []
    for nm, rolle, z, sk in (("Verteilerrohr", "ein", rg["z_ein"], "ein"), ("Sammelrohr", "aus", rg["z_aus"], "aus")):
        ys = [q["y"] for q in ps if q["rolle"] == rolle]
        y0, y1 = min(ys + [S[sk][1]]) - rg["da"] / 2, max(ys + [S[sk][1]]) + rg["da"] / 2
        k = _rohrkoerper(rg, y0, y1, x_blk, ys, z, da, di)
        k = k.cut(zylinder(da / 2, rg["da"] / 2 + 1, rg["x_p"], S[sk][1], z, "x"))      # Loch für den Anschlussstutzen (+x)
        teile.append(Teil(nm, k, "Al"))
    return teile


@teil("kuehlung.anschluss", "BT-630", "K")
def anschluss(ctx, pos):
    """Anschlussstutzen BT-630 Ein/Aus: Al-Rohr A_g5_anschluss_mm mit Schlauchwulst. Alt: auf der Rückseite von Verteiler/Sammler.
    G5.9: radial am Ende von Verteiler- bzw. Sammelrohr nach hinten (+x)."""
    da, di, ue = a("A_g5_anschluss_mm"); zc = ctx.z_mitte_zelle
    teile = []; S = _stutzen(ctx)
    if _gruppiert():
        rg = _rohrgeo(ctx)
        for nm, sk in (("Anschluss_ein", "ein"), ("Anschluss_aus", "aus")):
            xe, cy, z = S[sk]; xa = rg["x_p"] + math.sqrt(max(0.0, (rg["di"] / 2) ** 2 - (da / 2) ** 2))   # Stutzen beginnt an der Rohrinnenwand
            r_ = rohr(da / 2, di / 2, xe - xa, xa, cy, z, "x")
            wulst = rohr(da / 2 + da / 8, di / 2, da / 8, xe - da / 2, cy, z, "x")
            teile.append(Teil(nm, r_.fuse(wulst), "Al"))
        return teile
    for nm, (x0, x1, y0, y1) in zip(("Anschluss_ein", "Anschluss_aus"), _ecken(ctx)):
        cy = (y0 + y1) / 2
        r_ = rohr(da / 2, di / 2, ue, x1, cy, zc, "x")
        wulst = rohr(da / 2 + da / 8, di / 2, da / 8, x1 + ue - da / 2, cy, zc, "x")
        teile.append(Teil(nm, r_.fuse(wulst), "Al"))
    return teile


# ------------------------------------------------------------------ Kühlkreis außen (Kühlmodul hinter der Rückwand)
def _modul(ctx):
    """Lage der Geräte im Kühlmodul und die Spitzen ihrer Stutzen (Welt). Geräte in einer Reihe quer (y), Mitte auf Stutzenhöhe.
    Reihenfolge in y (vom Eintritt links zum Austritt rechts): Chiller, Ventil, Pumpe, Ausgleichsbehälter; Nachbarn sind über
    kurze gerade Schläuche verbunden (Stutzen auf den y-Flächen). Vor den Geräten (zwischen Stutzenende Pack und Geräten) liegt die
    Gasse für Bypass und T-Stück."""
    if getattr(ctx, "kuehlmodul", None): return ctx.kuehlmodul
    S = _stutzen(ctx); zc = ctx.z_mitte_zelle; gap = a("A_g5_kuehlmodul_teilabstand_mm"); g = a("A_g5_kuehlmodul_abstand_mm")
    st = gap / 4                                                     # Stutzenlänge an den Geräten
    xs = S["ein"][0]; x0 = xs + g
    cx_, cy_, cz_ = a("A_g5_chiller_mm"); vx, vy, vz = a("A_g5_ventil_mm"); pd, pl = a("A_g5_pumpe_mm"); bx, by, bz = a("A_g5_behaelter_mm")
    breiten = [cy_, vy, pl, by]; ges = sum(breiten) + 3 * gap
    y = ctx.B / 2 - ges / 2; lage = {}
    for nm, b in zip(("chiller", "ventil", "pumpe", "behaelter"), breiten):
        lage[nm] = (y, y + b); y += b + gap
    (yc0, yc1), (yv0, yv1), (yp0, yp1), (yb0, yb1) = (lage[k] for k in ("chiller", "ventil", "pumpe", "behaelter"))
    xk = x0 + pd / 2                                                 # gemeinsame Stutzenachse der Kette Behälter–Pumpe–Ventil–Chiller (gerade Schläuche)
    xd = dict(chiller=x0, ventil=xk - vx / 2, pumpe=x0, behaelter=xk - bx / 2)
    xv, xp, xb, xc = xk, xk, xk, x0 + cx_ / 2
    P = dict(chiller_ein=(xv, yc1 + st, zc), chiller_aus=(xc, yc0 - st, zc),
             ventil_ein=(xv, yv1 + st, zc), ventil_a=(xv, yv0 - st, zc), ventil_b=(xd["ventil"] - st, (yv0 + yv1) / 2, zc),
             pumpe_druck=(xp, yp0 - st, zc), pumpe_saug=(xp, yp1 + st, zc),
             behaelter_aus=(xb, yb0 - st, zc), behaelter_ein=(xb, yb1 + st, zc))
    Lt = 3 * a("A_g5_schlauch_mm")[0]                               # T-Stück: Schenkellänge je Seite Lt/2
    P["t_stueck"] = (xs + g / 2, yc0 - st - gap - Lt / 2, zc)
    ctx.kuehlmodul = dict(x0=x0, xd=xd, lage=lage, punkte=P, stutzen=S, st=st, Lt=Lt)
    return ctx.kuehlmodul


@teil("kuehlung.pumpe", "BT-661", "F")
def pumpe(ctx, pos):
    """Elektrische Kühlmittelpumpe BT-661 (Pierburg CWA100-3 gewählt: 25 L/min bei 1 bar, Datenblatt S. 1; Maße A_g5_pumpe_mm Annahme):
    Zylinder (Motor + Pumpenkopf) quer, Saugstutzen zum Behälter, Druckstutzen zum Ventil, Stecker 3-polig, Halteschelle."""
    M = _modul(ctx); d, l = a("A_g5_pumpe_mm"); y0, y1 = M["lage"]["pumpe"]; x = M["x0"] + d / 2; zc = ctx.z_mitte_zelle
    sd = a("A_g5_anschluss_mm")[0]
    k = zylinder(d / 2, l * 0.6, x, y0 + l * 0.4, zc, "y").fuse(zylinder(d / 2 * 0.85, l * 0.4, x, y0, zc, "y"))   # Motor + Pumpenkopf
    st = M["st"]; k = k.fuse(zylinder(sd / 2, st, x, y1, zc, "y")).fuse(zylinder(sd / 2, st, x, y0 - st, zc, "y"))
    k = k.fuse(quader(x - d / 6, y0 + l * 0.6, zc + d / 2 - 1, x + d / 6, y0 + l * 0.8, zc + d / 2 + d / 6))      # Stecker
    t = Teil("Kuehlmittelpumpe", k, "Al", masse_kg=a("A_g5_pumpe_masse_kg")); return [t]


@teil("kuehlung.ventil", "BT-663", "F")
def ventil(ctx, pos):
    """3/2-Wege-Kühlmittelventil BT-663 (Pierburg-Bauform, Maße A_g5_ventil_mm Annahme): Ventilkörper mit 3 Stutzen (Ein von der Pumpe,
    A zum Chiller, B Bypass zum T-Stück) und aufgesetztem Stellmotor."""
    M = _modul(ctx); vx, vy, vz = a("A_g5_ventil_mm"); y0, y1 = M["lage"]["ventil"]; x0 = M["xd"]["ventil"]; zc = ctx.z_mitte_zelle
    sd = a("A_g5_anschluss_mm")[0]; P = M["punkte"]
    k = quader_r(x0, y0, zc - vz / 2, x0 + vx, y1, zc + vz / 4, vz / 8, "alle")
    k = k.fuse(quader_r(x0 + vx / 6, y0 + vy / 6, zc + vz / 4, x0 + vx * 5 / 6, y1 - vy / 6, zc + vz / 2, vz / 10, "z"))   # Stellmotor
    st = M["st"]; k = k.fuse(zylinder(sd / 2, st, P["ventil_ein"][0], y1, zc, "y"))
    k = k.fuse(zylinder(sd / 2, st, P["ventil_a"][0], y0 - st, zc, "y")).fuse(zylinder(sd / 2, st, x0 - st, P["ventil_b"][1], zc, "x"))
    return [Teil("Kuehlmittelventil_3_2", k, "Al", masse_kg=a("A_g5_ventil_masse_kg"))]


@teil("kuehlung.chiller", "BT-662", "F")
def chiller(ctx, pos):
    """Chiller BT-662 (Platten-Wärmetauscher Kältemittel/Kühlmittel, Maße A_g5_chiller_mm Annahme, kein Datenblatt): Plattenpaket mit
    Grund- und Deckplatte, Kühlmittelstutzen zur Packseite (−x), Kältemittelstutzen A_g5_kaeltemittel_stutzen_mm zur Fahrzeugseite (+x)."""
    M = _modul(ctx); cx, cy, cz = a("A_g5_chiller_mm"); y0, y1 = M["lage"]["chiller"]; x0 = M["x0"]; zc = ctx.z_mitte_zelle
    sd = a("A_g5_anschluss_mm")[0]; kd, kl = a("A_g5_kaeltemittel_stutzen_mm"); P = M["punkte"]
    k = quader_r(x0, y0, zc - cz / 2, x0 + cx, y1, zc + cz / 2, cz / 10, "alle")
    k = k.fuse(quader(x0 - 1, y0 - 1, zc - cz / 2 - 2, x0 + cx + 1, y1 + 1, zc - cz / 2 + 1))     # Grundplatte (Löthaut)
    st = M["st"]; k = k.fuse(zylinder(sd / 2, st, P["chiller_ein"][0], y1, zc, "y")).fuse(zylinder(sd / 2, st, P["chiller_aus"][0], y0 - st, zc, "y"))
    for dy in (cy / 3, 2 * cy / 3):
        k = k.fuse(zylinder(kd / 2, kl, x0 + cx, y0 + dy, zc, "x"))
    return [Teil("Chiller", k, "Al", masse_kg=a("A_g5_chiller_masse_kg"))]


@teil("kuehlung.ausgleichsbehaelter", "BT-665", "F")
def ausgleichsbehaelter(ctx, pos):
    """Durchströmter Ausgleichsbehälter BT-665 (≈ 1 L, Maße A_g5_behaelter_mm Annahme, kein Datenblatt): PP-Behälter mit gerundeten
    Kanten, Einfüllstutzen mit Deckel oben, Ein- (vom Pack) und Austritt (zur Pumpe) unten seitlich. Masse ohne Kühlmittel."""
    M = _modul(ctx); bx, by, bz = a("A_g5_behaelter_mm"); y0, y1 = M["lage"]["behaelter"]; x0 = M["xd"]["behaelter"]; zc = ctx.z_mitte_zelle
    sd = a("A_g5_anschluss_mm")[0]
    k = quader_r(x0, y0, zc - bz / 2, x0 + bx, y1, zc + bz / 2, bz / 8, "alle")
    k = k.cut(quader_r(x0 + 2, y0 + 2, zc - bz / 2 + 2, x0 + bx - 2, y1 - 2, zc + bz / 2 - 2, bz / 8 - 2, "alle"))   # Wand 2 mm (hohl)
    k = k.fuse(zylinder(bx / 5, bz / 8, x0 + bx / 2, (y0 + y1) / 2, zc + bz / 2, "z"))                                  # Deckel
    st = M["st"]; k = k.fuse(zylinder(sd / 2, st, x0 + bx / 2, y1, zc, "y")).fuse(zylinder(sd / 2, st, x0 + bx / 2, y0 - st, zc, "y"))
    return [Teil("Ausgleichsbehaelter", k, "Kunststoff", masse_kg=a("A_g5_behaelter_masse_kg"))]


def _schlauch(punkte, da, di):
    """Schlauch als Polygonzug mit Bögen (Radius A_g5_schlauch_biegeradius_mm, an kurzen Stücken kleiner), Außen-Ø da, Innen-Ø di.
    Bogen statt B-Spline: robust beim Rohrzug (MakePipeShell) und der Biegeradius ist ablesbar."""
    R0 = a("A_g5_schlauch_biegeradius_mm")
    P = [V(*q) for q in punkte]
    P = [q for k, q in enumerate(P) if k == 0 or (q - P[k - 1]).Length > 1e-6]
    kanten = []; start = P[0]
    for k in range(1, len(P) - 1):
        A, B, C = P[k - 1], P[k], P[k + 1]
        u1, u2 = (A - B), (C - B)
        l1, l2 = u1.Length, u2.Length; u1.normalize(); u2.normalize()
        th = math.acos(max(-1.0, min(1.0, u1.dot(u2))))            # Innenwinkel
        if th > math.pi - 1e-3 or th < 0.05: continue             # gerade durch bzw. Umkehr (Punkt wird übergangen)
        # Endstücke (erstes/letztes Segment) darf der Bogen ganz aufbrauchen, innere Segmente teilen sich zwei Bögen
        tmax = min(l1 * (1.0 if k == 1 else 0.49), l2 * (1.0 if k == len(P) - 2 else 0.49)); r = R0; tt = r / math.tan(th / 2)
        if tt > tmax: tt = tmax; r = tt * math.tan(th / 2)
        if tt < 0.5: continue                                     # zu kurz für einen Bogen: Ecke bleibt (nur bei Hilfspunkten)
        T1, T2 = B + u1 * tt, B + u2 * tt
        bis = u1 + u2; bis.normalize(); mid = B + bis * (r / math.sin(th / 2) - r)
        if (T1 - start).Length > 1e-6: kanten.append(Part.LineSegment(start, T1).toShape())
        kanten.append(Part.Arc(T1, mid, T2).toShape()); start = T2
    if (P[-1] - start).Length > 1e-6: kanten.append(Part.LineSegment(start, P[-1]).toShape())
    w = Part.Wire(kanten); t0 = kanten[0].tangentAt(kanten[0].FirstParameter)
    def rohr_(d):
        return w.makePipeShell([Part.Wire([Part.makeCircle(d / 2, P[0], t0)])], True, False)
    return rohr_(da).cut(rohr_(di))


@teil("kuehlung.schlauch", "BT-664", "F")
def schlauch(ctx, pos):
    """Kühlmittelschläuche BT-664 (EPDM A_g5_schlauch_mm) und T-Stück: Pack-Austritt → Behälter → Pumpe → Ventil → Chiller → T → Pack-Eintritt,
    Ventil-Bypass → T. Führung als glatte Kurve über Zwischenpunkte in der Stutzenebene (Biegeradius aus dem Abstand der Punkte)."""
    M = _modul(ctx); P, S = M["punkte"], M["stutzen"]; da, di = a("A_g5_schlauch_mm"); x0 = M["x0"]; g = a("A_g5_kuehlmodul_abstand_mm")
    zc = ctx.z_mitte_zelle; ue = a("A_g5_anschluss_mm")[2]; xs = ctx.L + ue
    def mitte(p1, p2, dx=0.0, dy=0.0): return ((p1[0] + p2[0]) / 2 + dx, (p1[1] + p2[1]) / 2 + dy, zc)
    st, Lt = M["st"], M["Lt"]; tx, ty, _ = P["t_stueck"]; d = g / 3       # d: gerades Auslaufstück vor jedem Stutzen (Tangente)
    R = {"behaelter_ein": (0, 1), "behaelter_aus": (0, -1), "pumpe_saug": (0, 1), "pumpe_druck": (0, -1), "ventil_ein": (0, 1),
         "ventil_a": (0, -1), "ventil_b": (-1, 0), "chiller_ein": (0, 1), "chiller_aus": (0, -1)}
    def ende(n, f=1.0):
        q = P[n]; r = R[n]; return [q, (q[0] + r[0] * d * f, q[1] + r[1] * d * f, zc)]
    T_o, T_u, T_x = (tx, ty + Lt / 2, zc), (tx, ty - Lt / 2, zc), (tx + Lt / 2, ty, zc)
    zuege = {   # Endpunkte = Stutzenspitzen (Schlauch stößt an), je Ende ein gerades Auslaufstück in Stutzenrichtung
        "Schlauch_Pack_Behaelter": [S["aus"], (S["aus"][0] + d, S["aus"][1], S["aus"][2])] + ende("behaelter_ein", 2)[::-1],
        "Schlauch_Behaelter_Pumpe": ende("behaelter_aus") + ende("pumpe_saug")[::-1],
        "Schlauch_Pumpe_Ventil": ende("pumpe_druck") + ende("ventil_ein")[::-1],
        "Schlauch_Ventil_Chiller": ende("ventil_a") + ende("chiller_ein")[::-1],
        "Schlauch_Chiller_T": ende("chiller_aus", 2) + [(T_x[0] + d, ty, zc), T_x],
        "Schlauch_Bypass_T": ende("ventil_b", 2) + [(tx, P["ventil_b"][1] - g, zc), (tx, T_o[1] + d, zc), T_o],
        "Schlauch_T_Pack": [T_u, (tx, T_u[1] - d, zc), (S["ein"][0] + d, S["ein"][1], S["ein"][2]), S["ein"]],
    }
    teile = [Teil(nm, _schlauch(z, da, di), "EPDM") for nm, z in zuege.items()]
    L_ = Lt   # T-Stück: Durchgang in y (Bypass oben, Pack unten), Abzweig +x zum Chiller
    tst = zylinder(da / 2, L_, tx, ty - L_ / 2, zc, "y").fuse(zylinder(da / 2, L_ / 2, tx, ty, zc, "x"))
    tst = tst.cut(zylinder(di / 2, L_ + 2, tx, ty - L_ / 2 - 1, zc, "y")).cut(zylinder(di / 2, L_ / 2 + 1, tx, ty, zc, "x"))
    teile.append(Teil("T_Stueck", tst, "PA66GF30"))
    return teile
