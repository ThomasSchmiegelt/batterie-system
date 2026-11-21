# KI-generiert (Claude Opus, 2026-11-19), Entwurf. G5.3 Gehäuse (Stufe K).
"""Gehäuse: Unterfahrschutz BT-550, Wanne/Boden BT-510, Seitenrahmen BT-540, Querträger BT-530, Deckel BT-520, Servicedeckel 520.2,
Befestigungspunkte BT-560. Höhenebenen kommen aus kern.Ctx (ein Ort für alle Module).

Aufbau von unten: Unterfahrschutz (0 … ufs) · Luft · Boden · Seitenrahmen-Ring (Oberkante Boden … Unterkante Deckel) mit Kühlplatten,
Pads und Zellen innen · Deckel. Seitenrahmen: 3-Kammer-Strangpressprofil, Kammern übereinander (ENT-151: Rahmen trägt, baut keine
Energie ab; Seitenkraft geht über die waagerechten Stege in den Schweller). Befestigung: Stahlhülsen senkrecht durch den Rahmen,
weil die Breite 1430 mm fest ist (kein Außenflansch).
"""
import math
from kern import teil, p, a, Teil, einbau, quader, quader_r, zylinder, rohr, bohrungen, profil_extrudiert, rechteck, VAR, Part, V


def _platte(ctx, z0, z1, r):
    return quader_r(0, 0, z0, ctx.L, ctx.B, z1, r, "z")


def _befestigung_xy(ctx):
    n = int(a("A_g5_befestigung_n_je_seite")); rx = a("A_g5_befestigung_rand_x_mm")
    xs = [rx + i * (ctx.L - 2 * rx) / (n - 1) for i in range(n)]
    ys = (ctx.rand / 2, ctx.B - ctx.rand / 2)
    return [(x, y) for y in ys for x in xs]


@teil("gehaeuse.unterfahrschutz", "BT-550", "K")
def unterfahrschutz(ctx, pos):
    """Unterfahrschutz BT-550: Al-Platte über die ganze Grundfläche, Ecken gerundet, Bohrungen für die 12 Befestigungshülsen.
    Maße: A_unterfahrschutz_mm (M0), A_g5_eckradius_platte_mm, A_g5_befestigung_*. Akten: ENT-030 (Breite), ENT-147/LFP-Länge."""
    s = _platte(ctx, 0, ctx.ufs, a("A_g5_eckradius_platte_mm"))
    di = a("A_g5_befestigung_huelse_mm")[1]
    s = bohrungen(s, [(x, y, -1) for x, y in _befestigung_xy(ctx)], di / 2, ctx.ufs + 2)
    return [Teil("Unterfahrschutz", s, "Al")]


@teil("gehaeuse.wanne", "BT-510", "K")
def wanne(ctx, pos):
    """Boden der Wanne BT-510: Al-Blech unter Rahmen und Kühlplatte, Ecken gerundet. Die Hülsen der Befestigung gehen hindurch
    (Ausschnitt über ctx.schneide in befestigung()). Maße: A_boden_mm, A_luft_mm (M0)."""
    s = _platte(ctx, ctx.ufs + ctx.luft, ctx.z_boden_ok, a("A_g5_eckradius_platte_mm"))
    return [Teil("Wannenboden", s, "Al")]


def _rahmenprofil(ctx):
    """Querschnitt (u = quer zur Wand von außen nach innen, w = z): Außenrechteck rand × Höhe, n Kammern übereinander."""
    z0, z1 = ctx.z_boden_ok, ctx.z_deckel_u
    t = a("A_seitenrahmen_wand_mm"); n = int(a("A_seitenrahmen_kammern")); b = ctx.rand
    assert a("A_g5_rahmen_kammern_lage") == "uebereinander"
    hk = (z1 - z0 - (n + 1) * t) / n
    kammern = [rechteck(t, z0 + t + i * (hk + t), b - t, z0 + t + i * (hk + t) + hk) for i in range(n)]
    return rechteck(0, z0, b, z1), kammern


@teil("gehaeuse.seitenrahmen", "BT-540", "K")
def seitenrahmen(ctx, pos):
    """Seitenrahmen BT-540: vier Strangpressprofile (2 Längs, 2 Quer) mit 3 Kammern übereinander, Wand A_seitenrahmen_wand_mm.
    Längsprofile über die ganze Länge, Querprofile dazwischen (stumpf, geschweißt; Naht nicht modelliert).
    Akten: ENT-082…091 (Breite 30 = A_rand_mm), ENT-151 (keine Knautschzone). Stückzahl 4."""
    aussen, kammern = _rahmenprofil(ctx)
    L, B, b = ctx.L, ctx.B, ctx.rand
    teile = []
    # Längsprofile: Profil in yz-Ebene, Extrusion in x. Links u = y, rechts u gespiegelt.
    links = profil_extrudiert(aussen, L, "yz", 0.0, kammern)
    rechts = links.mirror(V(0, B / 2, 0), V(0, 1, 0))
    # Querprofile: Profil in xz-Ebene (u = x), Extrusion in y zwischen den Längsprofilen
    vorn = profil_extrudiert(aussen, B - 2 * b, "xz", b, kammern)
    hinten = vorn.mirror(V(L / 2, 0, 0), V(1, 0, 0))
    for nm, s in (("Rahmen_links", links), ("Rahmen_rechts", rechts), ("Rahmen_vorn", vorn), ("Rahmen_hinten", hinten)):
        teile.append(Teil(nm, s, "Al"))
    return teile


@teil("gehaeuse.quertraeger", "BT-530", "K")
def quertraeger(ctx, pos):
    """Querträger BT-530: Al-Hohlprofil breite × hoehe × wand (ENT-082…084), Außenkanten gerundet (A_g5_kantenradius_profil_mm),
    quer zwischen den Längsprofilen, Mitte auf Zellmitte. Lage aus der Zellanordnung (ctx.quertraeger_x)."""
    qb, qh, qw = p("BT-530", "breite_mm"), p("BT-530", "hoehe_mm"), p("BT-530", "wandstaerke_mm")
    r = a("A_g5_kantenradius_profil_mm"); zc = ctx.z_mitte_zelle; b = ctx.rand; lq = ctx.B - 2 * b
    teile = []
    for i, x in enumerate(ctx.quertraeger_x):
        aussen = quader_r(x, b, zc - qh / 2, x + qb, b + lq, zc + qh / 2, r, "alle")
        # Rundung nur an den Längskanten (y-Richtung) ist fertigungstreu; "alle" rundet auch die Stirnkanten leicht – vernachlässigbar
        innen = quader(x + qw, b - 1, zc - qh / 2 + qw, x + qb - qw, b + lq + 1, zc + qh / 2 - qw)
        teile.append(Teil(f"Quertraeger_{i + 1}", aussen.cut(innen), "Al"))
    return teile


@teil("gehaeuse.deckel", "BT-520", "K")
def deckel(ctx, pos):
    """Deckel BT-520: Al-Blech A_deckel_mm über die ganze Grundfläche, Ecken gerundet, Schraubenreihe M6 auf der Rahmenmitte
    (A_g5_deckelschraube_mm). Durchbrüche (Schaltbox, Servicedeckel, Stecker) melden andere Module über ctx.schneide an."""
    s = _platte(ctx, ctx.z_deckel_u, ctx.z_deckel_o, a("A_g5_eckradius_platte_mm"))
    d = a("A_g5_deckelschraube_mm")[0]
    pts = [(x, y, ctx.z_deckel_u - 1) for x, y in (getattr(ctx, "deckelschrauben", None) or _deckelschrauben(ctx))]
    s = bohrungen(s, pts, d / 2, ctx.dec + 2)
    return [Teil("Deckel", s, "Al")]


@teil("gehaeuse.befestigung", "BT-560", "K")
def befestigung(ctx, pos):
    """Befestigungspunkte BT-560: Stahlhülsen senkrecht durch Seitenrahmen, Boden und Unterfahrschutz (M10 von unten in die
    Karosserie). Anzahl 2 × A_g5_befestigung_n_je_seite, Hülse A_g5_befestigung_huelse_mm. Die Hülse schneidet ihr Volumen aus
    Rahmen, Boden und Unterfahrschutz aus (ctx.schneide)."""
    da, di = a("A_g5_befestigung_huelse_mm"); h = ctx.z_deckel_u
    teile = []
    for i, (x, y) in enumerate(_befestigung_xy(ctx)):
        teile.append(Teil(f"Befestigungshuelse_{i + 1:02d}", rohr(da / 2, di / 2, h, x, y, 0), "Stahl_verzinkt"))
        ctx.schneide(zylinder(da / 2, h, x, y, 0), ["BT-540", "BT-510", "BT-550"], "befestigung")
    return teile


def _deckelschrauben(ctx):
    d, tl = a("A_g5_deckelschraube_mm"); m = ctx.rand / 2; pts = []
    nx = int((ctx.L - 2 * m) // tl); ny = int((ctx.B - 2 * m) // tl)
    for i in range(nx + 1):
        x = m + i * (ctx.L - 2 * m) / nx; pts += [(x, m), (x, ctx.B - m)]
    for j in range(1, ny):
        y = m + j * (ctx.B - 2 * m) / ny; pts += [(m, y), (ctx.L - m, y)]
    return pts


def einbau_aussen(ctx):
    """Einbauorte der Kaufteile am Gehäuse (PLAN §3a), aufgerufen aus schaltbox._layout, also vor kaufteile/normteile:
    BT-570 Druckausgleich (Gore AVS 70) und BT-750 Entgasungsventil (Vernay VoltaVent) an der Rückwand außen, ±Versatz neben der Mitte;
    BT-640 Kühlmittelfühler (Kyocera AVX 94082, M12 × 1,5) durch die Rückwand in Verteiler und Sammler; BT-780 Typschild vorn auf dem Deckel.
    Bohrungen über ctx.schneide. Dazu die Deckelschrauben M6 in ctx.schrauben (normteile baut sie). Lagen: A_g5_aussen_teile."""
    if getattr(ctx, "einbau_aussen_fertig", False): return
    o = a("A_g5_aussen_teile"); L, B, zc = ctx.L, ctx.B, ctx.z_mitte_zelle; r = ctx.rand
    yd, ye = B / 2 + o["druckausgleich_y_versatz_mm"], B / 2 + o["entgasung_y_versatz_mm"]
    ctx.einbau["BT-570"] = [einbau(L, yd, zc, (1, 0, 0))]
    ctx.schneide(zylinder(a("A_g5_druckausgleich_mm")[2] / 2, r + 2, L - r - 1, yd, zc, "x"), ["BT-540"], "druckausgleich")
    el, eb, eh = a("A_g5_entgasungsventil_mm")
    ctx.einbau["BT-750"] = [einbau(L, ye, zc, (1, 0, 0), 90.0)]
    ctx.schneide(zylinder(min(el, eb) / 4, r + 2, L - r - 1, ye, zc, "x"), ["BT-540"], "entgasung")
    dm = a("A_g5_kuehlmittelfuehler_mm")[0]; bx, by = a("A_g5_verteiler_mm")
    ys = (r + by / 2, B - r - by / 2); zt = ctx.z_kp_o_u + ctx.kp          # Oberseite der Verteilerblöcke (außen hinter der Rückwand)
    xf = L + 3 * bx / 4                    # Opus 2026-11-20: hinter der Plattenlasche (reicht bis L + bx/2), Gewinde trifft die senkrechte Bohrung
    ctx.einbau["BT-640"] = [einbau(xf, y, zt, (0, 0, 1)) for y in ys]
    for y in ys:
        ctx.schneide(zylinder(dm / 2, zt - ctx.z_mitte_zelle, xf, y, ctx.z_mitte_zelle), ["BT-620"], "kuehlmittelfuehler")
    ctx.einbau["BT-780"] = [einbau(o["typschild_x_mm"], B - r - o["typschild_rand_mm"], ctx.z_deckel_o)]
    ctx.deckelschrauben = _deckelschrauben(ctx)
    d = a("A_g5_deckelschraube_mm")[0]
    for x, y in ctx.deckelschrauben:
        ctx.schrauben.append(dict(typ="Linsenkopf", d=d - 0.4, l=ctx.dec + a("A_seitenrahmen_wand_mm") + d, placement=einbau(x, y, ctx.z_deckel_o), bt="BT-520"))
        ctx.schneide(zylinder(d / 2, a("A_seitenrahmen_wand_mm") + d + 1, x, y, ctx.z_deckel_u - a("A_seitenrahmen_wand_mm") - d), ["BT-540"], "gewinde_deckel")   # Gewindebohrung M6 im Rahmen (Kerndurchmesser vereinfacht = d)
    ctx.einbau_aussen_fertig = True
