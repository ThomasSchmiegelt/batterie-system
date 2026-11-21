# KI-generiert (Claude Opus, 2026-11-19), Entwurf. G5.3 Schaltbox (Stufe K), Überarbeitung E2 Punkt 1 (Schütze liegend).
"""Schaltbox BT-710 auf dem Deckel hinten (ENT-144) mit liegenden Geräten. Legt die Einbauorte und Klemmen fest, die
kaufteile.py, elektronik.py und verbinder.py lesen (PLAN §3a). Geräte selbst baut kaufteile.py/elektronik.py.

Warum liegend: Die stehenden Schütze (75 mm) und der stehende Sicherungshalter (95 mm) mit den Schienen darüber ergaben
116 mm Innenhöhe gegen 90 mm Ziel (E2 v1.1). Liegend bestimmt die kleinste Gerätekante die Höhe (Schütz 60 mm).

Anordnung (Draufsicht, x nach hinten, y quer):     Reihe A (Plus-Seite, kleines y): Pyrosicherung, Schmelzsicherung
                                                   Reihe B: Hauptschütz +, Vorladeschütz, Vorladewiderstand, Hauptschütz −
                                                   Reihe C (Minus-Seite, großes y): Shunt, BMS-Platine, Isolationswächter, Gassensor
Klemmen der Schütze zeigen zur Reihe A (−y), dort laufen die Schienen in der Höhe der Klemmen. HV-Leitungen kommen durch die
Seitenwände (Plus bei y min, Minus bei y max), knapp über dem Boxboden, also ohne zusätzliche Höhe. Stecker HV 250 A, HV 40 A, NV
stehen vor der Box auf dem Deckel und zeigen nach vorn (−x, Kabelbaum des Fahrzeugs).

Gerätetabelle GERAETE: lokale Maße (lx in Klemmenrichtung, ly, lz Höhe über der Befestigungsfläche) und Klemmen lokal.
kaufteile.py MUSS genau diese Maße und Klemmlagen bauen (eine Quelle: ctx.schaltbox["geraete"]).
"""
import math
from kern import teil, p, a, Teil, quader, quader_r, zylinder, bohrungen, einbau, VAR, FreeCAD, Part, V


def _geraete():
    """Lokale Maße l = (lx, ly, lz) und Klemmen je Gerät. Lokales System (PLAN §3a): Ursprung = Mitte der Befestigungsfläche,
    Körper x ∈ [−lx/2, lx/2], y ∈ [−ly/2, ly/2], z ∈ [0, lz]. Klemme = (name, x, y, z, richtung): Fußpunkt auf der Körperfläche,
    richtung = nach außen (dort sitzt der Bolzen A_e2d_schuetz_bolzen_* bzw. die Lasche)."""
    sL, sB, sH = a("A_e2_schuetz_mm")              # stehend: L × B × H, Bolzen oben
    bab = a("A_e2d_schuetz_bolzen_abstand_mm")
    vL, vB, vH = a("A_e2_vorladeschuetz_mm"); wL, wB, wH = a("A_e2_vorladewiderstand_mm")
    pL, pB, pH = a("A_e2_pyro_mm"); hL, hB, hH = a("A_e2d_schmelz_halter_mm"); shL, shB, shH = a("A_e2_shunt_mm")
    bL, bB, bH = p("BT-310", "laenge_mm"), p("BT-310", "breite_mm"), p("BT-310", "hoehe_mm")
    iL, iB, iH = a("A_g5_isolationswaechter_mm"); gL, gB, gH = a("A_e2_gas_mm")
    g = {}
    # Schütz liegend: stehende Höhe H → lx (Bolzenachse, Bolzen auf der +x-Fläche), Länge L → ly, Breite B → Höhe lz
    for n in ("Hauptschuetz_plus", "Hauptschuetz_minus"):
        g[n] = dict(bt="BT-711", l=(sH, sL, sB), klemmen=[("a", sH / 2, -bab / 2, sB / 2, (1, 0, 0)), ("b", sH / 2, bab / 2, sB / 2, (1, 0, 0))])
    g["Vorladeschuetz"] = dict(bt="BT-712", l=(vH, vL, vB), klemmen=[("a", vH / 2, -vL / 4, vB / 2, (1, 0, 0)), ("b", vH / 2, vL / 4, vB / 2, (1, 0, 0))])
    g["Vorladewiderstand"] = dict(bt="BT-712", l=(wB, wL, wH), klemmen=[("a", wB / 2, -wL / 2 + wB / 2, wH / 2, (1, 0, 0)), ("b", wB / 2, wL / 2 - wB / 2, wH / 2, (1, 0, 0))])
    # Sicherungen liegend, Achse = ly, Laschen an den Stirnseiten
    g["Pyrosicherung"] = dict(bt="BT-713", l=(pB, pH, pB), klemmen=[("a", 0, -pH / 2, pB / 2, (0, -1, 0)), ("b", 0, pH / 2, pB / 2, (0, 1, 0))])
    g["Schmelzsicherung"] = dict(bt="BT-713", l=(hB, hH, hB), klemmen=[("a", 0, -hH / 2, hB / 2, (0, -1, 0)), ("b", 0, hH / 2, hB / 2, (0, 1, 0))])
    g["Shunt"] = dict(bt="BT-340", l=(shB, shL, shH), klemmen=[("a", 0, -shL / 2 + shL / 8, shH, (0, 0, 1)), ("b", 0, shL / 2 - shL / 8, shH, (0, 0, 1))])
    g["BMS_Platine"] = dict(bt="BT-310", l=(bB, bL, bH), klemmen=[])
    g["Isolationswaechter"] = dict(bt="BT-350", l=(iB, iL, iH), klemmen=[])
    g["Gassensor"] = dict(bt="BT-770", l=(gB, gL, gH), klemmen=[])
    return g


REIHEN = [["Pyrosicherung", "Schmelzsicherung"],
          ["Hauptschuetz_plus", "Vorladeschuetz", "Vorladewiderstand", "Hauptschuetz_minus"],
          ["Shunt", "BMS_Platine", "Isolationswaechter", "Gassensor"]]
# Verbindungen (Stromlaufplan E2, ERGEBNIS v1.0): Plus → Pyro → HS+ → HV250+ ; Vorladung parallel zu HS+ ; HS+ Ausgang → Schmelz → HV40+
#                                                 Minus → Shunt → HS− → HV250− ; HV40− an HS− Ausgang
SCHIENEN = [("HV_ein_plus", "Pyrosicherung.a"), ("Pyrosicherung.b", "Hauptschuetz_plus.a"), ("Pyrosicherung.b", "Vorladeschuetz.a"),
            ("Vorladeschuetz.b", "Vorladewiderstand.a"), ("Vorladewiderstand.b", "Hauptschuetz_plus.b"), ("Hauptschuetz_plus.b", "Schmelzsicherung.a"),
            ("Hauptschuetz_plus.b", "HV250.plus"), ("Schmelzsicherung.b", "HV40.plus"),
            ("HV_ein_minus", "Shunt.a"), ("Shunt.b", "Hauptschuetz_minus.a"), ("Hauptschuetz_minus.b", "HV250.minus"), ("Hauptschuetz_minus.b", "HV40.minus")]


def _layout(ctx):
    """Box-Maße und Gerätelagen. Ergebnis in ctx.schaltbox (einmal je Lauf)."""
    if ctx.schaltbox.get("fertig"): return ctx.schaltbox
    g = _geraete(); gap, wd, rm = a("A_e2_box_teilabstand_mm"), a("A_e2_box_wand_mm"), a("A_e2_box_rand_mm")
    fl, fd, dk = a("A_e2d_box_flansch_mm"), a("A_e2d_box_flansch_dicke_mm"), a("A_e2d_box_deckel_mm")
    dg_w, dg_h = a("A_e2d_box_dichtung_mm"); frei = a("A_g5_box_freiraum_oben_mm")
    ext = a("A_e2d_lasche_pyro_schmelz_mm")[2]     # Laschen der Sicherungen kragen an beiden Stirnseiten aus
    def fuss(n):
        """Fußabdruck in Welt-x, Welt-y. Alle Geräte: lokale y-Achse liegt in Welt-x. Sicherungen: + 2 Laschen."""
        lx, ly, lz = g[n]["l"]; return ly + (2 * ext if g[n]["bt"] == "BT-713" else 0), lx
    rb = [sum(fuss(n)[0] for n in r) + gap * (len(r) - 1) for r in REIHEN]
    tiefe = [max(fuss(n)[1] for n in r) for r in REIHEN]
    iL = max(rb); iB = sum(tiefe) + a("A_g5_schienengasse_mm") + gap * (len(REIHEN) - 2)
    iH = max(g[n]["l"][2] for r in REIHEN for n in r) + frei
    bL, bB = iL + 2 * rm, iB + 2 * rm
    x1 = ctx.L - ctx.rand - fl; x0 = x1 - bL
    y0 = ctx.B / 2 - bB / 2
    z0 = ctx.z_deckel_o; zf = z0 + wd
    # HV-Eintritt (Opus 2026-11-19): auf Höhe Hülsenende + Biegeradius, damit die Leitung nach dem 90°-Bogen waagerecht durch die
    # Seitenwand geht (vorher Eintritt knapp über dem Boden → Schlaufe bis z ≈ 275). Die Box wird dafür höher, wenn nötig.
    from teile.verbinder import _lasche
    rhv = a(f"A_e2_hv_aussendurchmesser_{VAR}_mm") / 2; abst = a("A_g5_hv_eingang_abstand_mm")
    la = _lasche(ctx); zE = max(la[n]["z_oben"] for n in ("Plus", "Minus")) + a("A_e2d_kabelschuh_lasche_mm")[1] + a("A_e2d_kabelschuh_huelse_mm")
    zin = max(zf + rhv + abst, zE + p("BT-430", "biegeradius_min_mm"))
    iH = max(iH, zin + rhv + abst - zf)
    zw = zf + iH                                                     # Box steht auf dem Deckel, Boden wd
    if VAR == "NMC":   # Trennstecker NMC über den Reihenmitten (ENT-131): Box in y daneben setzen, wenn sie ihn in x überdeckt
        from teile._verdrahtung import verdr
        R_ = verdr(ctx); A_, B_ = R_["ans"]["Mitte_A_Ende_Band2"], R_["ans"]["Mitte_B_Anfang_Band3"]
        px, py = (A_["cx"] + B_["cx"]) / 2, (A_["cy"] + B_["cy"]) / 2; tl, tb_, th = a("A_e2_trennstecker_mm")
        if px + tl / 2 + gap > x0 - fl and px - tl / 2 - gap < x1 + fl and py + tb_ / 2 + gap > y0 - fl and py - tb_ / 2 - gap < y0 + bB + fl:
            y0 = py + tb_ / 2 + gap + fl
            assert y0 + bB + fl <= ctx.B - ctx.rand, ("Schaltbox passt neben dem Trennstecker nicht in die Breite", y0, bB)
        ctx.einbau["BT-720"] = [einbau(px, py, ctx.z_deckel_o)]
    lagen = {}; klemmen = {}
    gasse = a("A_g5_schienengasse_mm")            # Gasse zwischen Reihe A und B für Bolzen und Schienen
    yy = y0 + rm
    for ri, r in enumerate(REIHEN):
        xx = x0 + rm
        for n in r:
            fx, fy = fuss(n); lx, ly, lz = g[n]["l"]
            # Reihe B (Schütze): lokal +x → Welt −y (Klemmen zur Gasse), lokal y → Welt +x  (Drehung −90°)
            # Reihen A, C:       lokal +x → Welt +y, lokal y → Welt −x                     (Drehung +90°)
            dreh = -90.0 if ri == 1 else 90.0
            pl = einbau(xx + fx / 2, yy + fy / 2, zf, (0, 0, 1), dreh)
            lagen[n] = pl
            for (kn, kx, ky, kz, kr) in g[n]["klemmen"]:
                w = pl.multVec(V(kx, ky, kz)); rv = pl.Rotation.multVec(V(*kr))
                klemmen[f"{n}.{kn}"] = (w.x, w.y, w.z, (round(rv.x, 6), round(rv.y, 6), round(rv.z, 6)))
            xx += fx + gap
        yy += tiefe[ri] + (gasse if ri == 0 else gap)
    xin_p = klemmen["Pyrosicherung.a"][0]; xin_m = klemmen["Shunt.a"][0]
    klemmen["HV_ein_plus"] = (xin_p, y0, zin, (0, -1, 0)); klemmen["HV_ein_minus"] = (xin_m, y0 + bB, zin, (0, 1, 0))
    # Stecker vor der Box auf dem Deckel, zeigen nach vorn
    st = {"HV250": a("A_e2_hv250_mm"), "HV40": a("A_e2_hv40_mm"), "NV": a("A_e2_nv_mm")}
    ys = y0; stecker = {}
    for n, (sl, sb, sh) in st.items():
        pl = einbau(x0 - fl - gap - sl / 2, ys + sb / 2, z0, (0, 0, 1), 180.0)
        stecker[n] = pl
        if n != "NV":
            for pol, dy in (("plus", -sb / 4), ("minus", sb / 4)):
                w = pl.multVec(V(-sl / 2, dy, sh / 2)); klemmen[f"{n}.{pol}"] = (w.x, w.y, w.z, (1, 0, 0))
        ys += sb + gap
    ctx.schaltbox.update(dict(fertig=True, geraete=g, lagen=lagen, klemmen=klemmen, schienen=SCHIENEN, stecker=stecker,
                              box=(x0, y0, z0, x0 + bL, y0 + bB, zw), innen=(x0 + wd, y0 + wd, zf, x0 + bL - wd, y0 + bB - wd, zw),
                              innenhoehe_mm=iH, flansch=(fl, fd), deckel=dk, dichtung=(dg_w, dg_h), z_deckel_o=zw + dg_h + dk,
                              hv_eingang={"Plus": klemmen["HV_ein_plus"][:3], "Minus": klemmen["HV_ein_minus"][:3]}))
    for n, pl in lagen.items(): ctx.einbau.setdefault(g[n]["bt"], []).append(pl)
    for n, pl in stecker.items(): ctx.einbau.setdefault("BT-740" if n == "NV" else "BT-730", []).append(pl)
    from teile.gehaeuse import einbau_aussen
    einbau_aussen(ctx)                     # Einbauorte außen (Druckausgleich, Entgasung, Typschild, Kühlmittelfühler) und Deckelschrauben vor kaufteile/normteile
    return ctx.schaltbox


def _schrauben_xy(x0, y0, x1, y1, off, teilung):
    pts = []
    for (xa, ya, xb, yb) in ((x0 - off, y0 - off, x1 + off, y0 - off), (x1 + off, y0 - off, x1 + off, y1 + off),
                             (x1 + off, y1 + off, x0 - off, y1 + off), (x0 - off, y1 + off, x0 - off, y0 - off)):
        n = math.ceil(math.hypot(xb - xa, yb - ya) / teilung)
        pts += [(xa + (xb - xa) * i / n, ya + (yb - ya) * i / n) for i in range(n)]
    return pts


@teil("schaltbox.gehaeuse", "BT-710", "K")
def gehaeuse(ctx, pos):
    """Schaltbox-Wanne BT-710: Al, Wand A_e2_box_wand_mm, Innenmaß aus den liegenden Geräten (Reihen A/B/C + A_e2_box_rand_mm +
    A_e2_box_teilabstand_mm), Innenhöhe = höchstes liegendes Gerät + A_g5_box_freiraum_oben_mm. Umlaufender Flansch
    A_e2d_box_flansch_mm mit M5-Bohrungen (A_e2d_box_schraube_*), senkrechte Kanten innen gerundet, Durchführungen für die
    HV-Leitungen in den Seitenwänden. Akten: ENT-144 (Deckel hinten), ENT-109 ersetzt."""
    S = _layout(ctx); x0, y0, z0, x1, y1, zw = S["box"]; wd = a("A_e2_box_wand_mm"); fl, fd = S["flansch"]
    r = a("A_g5_box_eckradius_mm")
    aussen = quader_r(x0, y0, z0, x1, y1, zw, r, "z")
    innen = quader_r(x0 + wd, y0 + wd, z0 + wd, x1 - wd, y1 - wd, zw + 1, max(r - wd, 0.5), "z")
    fla = quader_r(x0 - fl, y0 - fl, zw - fd, x1 + fl, y1 + fl, zw, r + fl, "z").cut(quader(x0 + wd, y0 + wd, zw - fd - 1, x1 - wd, y1 - wd, zw + 1))
    s = aussen.cut(innen).fuse(fla).removeSplitter()
    sk = a("A_e2d_box_schraube_gewinde_mm"); pts = _schrauben_xy(x0, y0, x1, y1, fl / 2 + wd / 2 - wd, a("A_e2d_box_schraube_teilung_mm"))
    rhv = a(f"A_e2_hv_aussendurchmesser_{VAR}_mm") / 2
    # Opus 2026-11-20: keine Flanschschraube direkt über dem HV-Eintritt (Kabelschuh außen an der Wand)
    hv = [S["klemmen"][k][:2] for k in ("HV_ein_plus", "HV_ein_minus")]
    pts = [(x, y) for x, y in pts if not any(abs(x - hx) < rhv + sk + 10 and abs(y - hy) < fl + wd + 5 for hx, hy in hv)]
    S["schrauben_xy"] = pts
    s = bohrungen(s, [(x, y, zw - fd - 1) for x, y in pts], sk / 2, fd + 2)
    for k in ("HV_ein_plus", "HV_ein_minus"):
        x, y, z, d = S["klemmen"][k]
        s = s.cut(zylinder(rhv + a("A_g5_hv_eingang_abstand_mm") / 2, 3 * wd, x, y - 1.5 * wd, z, "y"))
    for x, y in pts:
        ctx.schrauben.append(dict(typ="Linsenkopf", d=sk, l=fd + S["dichtung"][1] + S["deckel"] + sk, placement=einbau(x, y, S["z_deckel_o"]), bt="BT-710")) if hasattr(ctx, "schrauben") else None
    return [Teil("Schaltbox_Wanne", s, "Al")]


@teil("schaltbox.deckel", "BT-710", "K")
def deckel(ctx, pos):
    """Schaltbox-Deckel BT-710 (2 Teile laut SL3: Deckel und Druckausgleich-Kappe): Al A_e2d_box_deckel_mm auf der Dichtung,
    Kontur = Flansch, Bohrungen M5 wie der Flansch, Bohrung A_e2d_box_druckausgleich_d_mm in der Mitte mit Schutzkappe."""
    S = _layout(ctx); x0, y0, z0, x1, y1, zw = S["box"]; fl, fd = S["flansch"]; dk = S["deckel"]; dg_h = S["dichtung"][1]
    r = a("A_g5_box_eckradius_mm"); zl = zw + dg_h
    s = quader_r(x0 - fl, y0 - fl, zl, x1 + fl, y1 + fl, zl + dk, r + fl, "z")
    sk = a("A_e2d_box_schraube_gewinde_mm"); vd = a("A_e2d_box_druckausgleich_d_mm")
    pts = S.get("schrauben_xy") or _schrauben_xy(x0, y0, x1, y1, fl / 2, a("A_e2d_box_schraube_teilung_mm"))
    s = bohrungen(s, [(x, y, zl - 1) for x, y in pts], sk / 2, dk + 2)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    s = s.cut(zylinder(vd / 2, dk + 2, cx, cy, zl - 1))
    kappe = zylinder(vd / 2 + vd / 4, vd / 4, cx, cy, zl + dk).fuse(zylinder(vd / 2 - dk, dk, cx, cy, zl))   # Kappe mit Zapfen in der Bohrung
    return [Teil("Schaltbox_Deckel", s, "Al_eloxiert"), Teil("Schaltbox_Druckausgleich_Kappe", kappe, "PA66GF30")]
