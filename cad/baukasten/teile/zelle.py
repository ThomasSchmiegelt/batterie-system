# KI-generiert (Claude Sonnet, 2026-11-19), Entwurf. Auftrag G5.4 (cad/baukasten/AUFTRAG_G5_4.md), Modul zelle.
"""Zelle, Zwischenlage, Pad, Verguss, Zellträger (PLAN §3). Lagen aus ctx.zellen / ctx.felder (kern.Ctx.anordnung, gleiche Anordnung wie G4/E2).
Quelle der Logik: cad/pack/pack_e2d.py (Zellen, Pad, Zellträger, Verguss) und cad/zelle/zelle.py (Polmaße als Annahme).
Maße: nur p() (Akten) und a() (annahmen.json, annahmen_g5.json). Pole: Annahmen A_g54_*."""
from kern import teil, p, a, Teil, quader, quader_r, zylinder, rohr, VAR, Part, V


def _versetzt(shape, dx, dy, dz=0.0):
    s = shape.copy(); s.translate(V(dx, dy, dz)); return s


@teil("zelle.zelle_prismatisch", "BT-100", "F")
def zelle_prismatisch(ctx, pos):
    """Blade-Zelle LFP BT-100 (250 Stück): Quader laenge × dicke × breite (Akte BT-100, ENT-033…), Kanten gerundet (A_g54_zelle_eckradius_mm),
    je zwei Polfahnen an der äußeren Stirnseite (Plus oben, Minus unten, A_g54_pol_lfp_mm / _versatz_mm). Masse aus der Akte (BT-100 masse_g).
    Lage: ctx.zellen, Reihe 0 außen bei kleinem y, Reihe 1 außen bei großem y. Stufe F."""
    if VAR != "LFP": return []
    m = ctx.zell_mass; Lc, Dc, H = m["L"], m["D"], m["H"]; r = a("A_g54_zelle_eckradius_mm")
    pw, ph, pt = a("A_g54_pol_lfp_mm"); dz = a("A_g54_pol_lfp_versatz_mm"); zc = ctx.z_mitte_zelle; masse = p("BT-100", "masse_g") / 1000
    master = {}
    for reihe in (0, 1):
        k = quader_r(-Dc / 2, -Lc / 2, ctx.z_zelle_u, Dc / 2, Lc / 2, ctx.z_zelle_o, r, "alle")
        ya, yb = (-Lc / 2 - pt, -Lc / 2) if reihe == 0 else (Lc / 2, Lc / 2 + pt)
        for s in (dz, -dz): k = k.fuse(quader(-pw / 2, ya, zc + s - ph / 2, pw / 2, yb, zc + s + ph / 2))
        master[reihe] = k.removeSplitter()
    return [Teil(f"Zelle_{i:03d}", _versetzt(master[c["reihe"]], c["cx"], c["cy"]), "Zelle_LFP", masse_kg=masse) for i, c in enumerate(ctx.zellen)]


@teil("zelle.zelle_rund", "BT-100", "F")
def zelle_rund(ctx, pos):
    """Rundzelle 4680 NMC BT-100 (868 Stück): Zylinder Ø durchmesser_mm × hoehe_mm (Akte BT-100), obere Außenkante gerundet (Schulter,
    A_g54_nmc_kopfrundung_mm), Ringnut um den Pluspol (A_g54_nmc_nut_mm). Beide Pole liegen oben (Plus mittig, Minus = Becherrand, ENT-140);
    die Abgriffe sitzen als Scheiben darauf (verbinder.zellabgriff). Masse aus der Akte. Stufe F."""
    if VAR != "NMC": return []
    d, H = ctx.zell_mass["D"], ctx.zell_mass["H"]; rr = a("A_g54_nmc_kopfrundung_mm"); ni, na, nt = a("A_g54_nmc_nut_mm")
    k = zylinder(d / 2, H, 0, 0, ctx.z_zelle_u)
    top = [e for e in k.Edges if abs(e.Vertexes[0].Point.z - ctx.z_zelle_o) < 1e-6 and e.Curve.__class__.__name__ == "Circle"]
    k = k.makeFillet(rr, top).cut(rohr(na / 2, ni / 2, nt + 1, 0, 0, ctx.z_zelle_o - nt))
    masse = p("BT-100", "masse_g") / 1000
    return [Teil(f"Zelle_{i:03d}", _versetzt(k, c["cx"], c["cy"]), "Zelle_NMC", masse_kg=masse) for i, c in enumerate(ctx.zellen)]


@teil("zelle.zwischenlage", "BT-220", "K")
def zwischenlage(ctx, pos):
    """Zwischenlage BT-220 (LFP, 242 Stück, Opus 2026-11-19): Schaumplatte (Werkstoff Schaum_Zwischenlage, Opus 2026-11-19) in jedem Spalt zwischen zwei Nachbarzellen derselben Reihe und
    desselben Feldes (2 Reihen × 4 Felder: 250 − 8 = 242). Dicke = A_zellabstand_LFP_mm, Fläche = Zellfläche laenge × breite. Stufe K."""
    if VAR != "LFP": return []
    m = ctx.zell_mass; Lc, Dc = m["L"], m["D"]; teile = []
    gruppen = {}
    for c in ctx.zellen: gruppen.setdefault((c["feld"], c["reihe"]), []).append(c)
    for (f, r), cs in sorted(gruppen.items()):
        cs.sort(key=lambda c: c["cx"])
        for c1, c2 in zip(cs, cs[1:]):
            x0, x1 = c1["cx"] + Dc / 2, c2["cx"] - Dc / 2
            teile.append(Teil(f"Zwischenlage_f{f}r{r}_{len(teile):03d}", quader(x0, c1["cy"] - Lc / 2, ctx.z_zelle_u, x1, c1["cy"] + Lc / 2, ctx.z_zelle_o), "Schaum_Zwischenlage"))
    return teile


@teil("zelle.pad", "BT-230", "F")
def pad(ctx, pos):
    """Wärmeleitpad BT-230, 2 Stück (unten und oben): Platte über die ganze Innenfläche (Rahmen innen), Dicke A_pad_mm. Unten zwischen
    unterer Kühlplatte und Zellen, oben zwischen Zellen (bzw. Abgriffen) und oberer Kühlplatte. Ausschnitte (Lasche, Verteiler, Service)
    schneiden andere Module über ctx.schneide(…, ['BT-230']). Stufe F."""
    x0, x1, y0, y1 = ctx.rand, ctx.L - ctx.rand, ctx.rand, ctx.B - ctx.rand
    return [Teil("Pad_unten", quader(x0, y0, ctx.z_kp_u_ok, x1, y1, ctx.z_zelle_u), "Pad"),
            Teil("Pad_oben", quader(x0, y0, ctx.z_pad_o_u, x1, y1, ctx.z_kp_o_u), "Pad")]


def _lochplatte(ctx, f, z0, z1):
    d = ctx.zell_mass["D"]; xs = [c["cx"] for c in ctx.zellen if c["feld"] == f]
    fx0, fx1 = max(ctx.felder[f][0], min(xs) - d / 2), min(ctx.felder[f][1], max(xs) + d / 2)   # nur über den Zellen: der freie Rand im Feld gehört CMU, FPC, Daisy
    plat = quader(fx0, ctx.rand, z0, fx1, ctx.B - ctx.rand, z1)
    tool = Part.makeCompound([zylinder(d / 2, z1 - z0 + 2, c["cx"], c["cy"], z0 - 1) for c in ctx.zellen if c["feld"] == f])
    return plat.cut(tool)


@teil("zelle.zelltraeger", "BT-250", "K")
def zelltraeger(ctx, pos):
    """Zellträger BT-250 (NMC, 4 Stück, ENT-092 Träger unten + Verguss): Lochplatte je Feld unter den Zellen, Dicke A_traeger_dicke_NMC_mm,
    Löcher = Zellkontur. Werkstoff PC (farben.json). Stufe K."""
    if VAR != "NMC": return []
    t = a("A_traeger_dicke_NMC_mm")
    return [Teil(f"Zelltraeger_f{f}", _lochplatte(ctx, f, ctx.z_zelle_u, ctx.z_zelle_u + t), "PC") for f in range(len(ctx.felder))]


@teil("zelle.verguss", "BT-220", "K")
def verguss(ctx, pos):
    """Verguss BT-220 (NMC, 4 Stück, ENT-092): Lochkörper je Feld über dem Zellträger bis A_vergusshoehe_anteil_NMC × Zellhöhe, Löcher = Zellkontur
    (PU-Schaum, farben.json). Stufe K."""
    if VAR != "NMC": return []
    t = a("A_traeger_dicke_NMC_mm"); hv = a("A_vergusshoehe_anteil_NMC") * ctx.h_zelle
    return [Teil(f"Verguss_f{f}", _lochplatte(ctx, f, ctx.z_zelle_u + t, ctx.z_zelle_u + hv), "PU_Schaum") for f in range(len(ctx.felder))]
