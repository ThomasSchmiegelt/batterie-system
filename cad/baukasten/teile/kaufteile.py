# KI-generiert (Claude Sonnet, 2026-11-19), Entwurf. Auftrag G5.4 (cad/baukasten/AUFTRAG_G5_4.md), Modul kaufteile.
"""Kaufteile: Schütze, Vorlade, Sicherungen, Stecker, Gassensor, Trennstecker (NMC), Druckausgleich, Entgasungsventil, Typschild, Kühlmittelfühler.
Jedes Teil wird in lokalen Koordinaten gebaut (PLAN §3a: Ursprung = Mitte der Befestigungsfläche, +z = Normale, +x = Richtung der Anschlüsse) und mit kern.setze()
an den Einbauort gesetzt. Maße und Klemmen der Geräte in der Schaltbox kommen aus ctx.schaltbox['geraete'] (eine Quelle mit schaltbox.py und elektronik.py);
Gehäuse und Kühlung legen ihre Einbauorte erst nach diesem Modul fest, deshalb bleiben Druckausgleich, Entgasungsventil, Typschild und Kühlmittelfühler
ohne Einbauort leer (0 Teile, gemeldet). Massen: Annahmen ERW-E2 N1 (A_e2_*_masse_kg), Stufe F; Bolzen A_e2d_schuetz_bolzen_*."""
import math
from kern import teil, p, a, Teil, quader, quader_r, zylinder, bohrungen, setze, einbau, VAR, Part, V
import FreeCAD
from teile.verbinder import _verb


def _sb(ctx):
    from teile.schaltbox import _layout
    return _layout(ctx)


def _bolzen(k):
    """Bolzen Ø A_e2d_schuetz_bolzen_d_mm × A_e2d_schuetz_bolzen_h_mm an Klemme k = (name, x, y, z, richtung), lokal."""
    d, h = a("A_e2d_schuetz_bolzen_d_mm"), a("A_e2d_schuetz_bolzen_h_mm")
    return Part.makeCylinder(d / 2, h, V(k[1], k[2], k[3]), V(*k[4]))


def _fuss_schrauben(ctx, pl, pts_lokal, d, l, bt):
    for (x, y, z) in pts_lokal:
        ctx.schrauben.append(dict(typ="Sechskant", d=d, l=l, placement=pl.multiply(FreeCAD.Placement(V(x, y, z), FreeCAD.Rotation(V(0, 0, 1), 30))), bt=bt, **{"in": ["BT-710"]}))


def _geraet_teile(ctx, namen, kopf):
    """Teile für die Geräte `namen` (Schaltbox): Körper je nach kopf(name, g) (lokale Form), Bolzen an den Klemmen, gesetzt an ctx.schaltbox['lagen'][name]."""
    S = _sb(ctx); out = []
    for n in namen:
        if n not in S["lagen"]:
            print(f"  kaufteile: kein Einbauort für {n}"); continue
        g = S["geraete"][n]; shp, werk, masse, extra = kopf(n, g)
        for k in g["klemmen"]: shp = shp.fuse(_bolzen(k))
        out.append(Teil(n, setze(shp.removeSplitter(), S["lagen"][n]), werk, masse_kg=masse))
        if extra: extra(ctx, S["lagen"][n], g)
    return out


@teil("kaufteile.schuetz_haupt", "BT-711", "F")
def schuetz_haupt(ctx, pos):
    """Hauptschütze BT-711 (2: Plus, Minus; ENT-123/124): liegend (Bolzenachse lokal +x), Körper A_e2_schuetz_mm als lx × ly × lz aus ctx.schaltbox['geraete'],
    2 Bolzen Ø A_e2d_schuetz_bolzen_d_mm × A_e2d_schuetz_bolzen_h_mm an den Klemmen, 2 Fußlaschen A_g54_schuetz_fusslasche_mm (hinten, Schraube M5 in den Boxboden,
    ctx.schrauben). Masse A_e2_schuetz_masse_kg. Stufe F."""
    fl = a("A_g54_schuetz_fusslasche_mm"); gw = int(a("A_e2d_schuetz_fusslaschen_n")); sd = a("A_e2d_schuetz_fusslasche_gewinde_mm")
    def kopf(n, g):
        lx, ly, lz = g["l"]; s = quader(-lx / 2, -ly / 2, 0, lx / 2, ly / 2, lz); ys = [-20.0, 20.0][:gw]
        for y in ys: s = s.fuse(quader(-lx / 2 - fl[1], y - fl[0] / 2, 0, -lx / 2, y + fl[0] / 2, fl[2]))
        s = s.cut(Part.makeCompound([zylinder(sd / 2, fl[2] + 2, -lx / 2 - fl[1] / 2, y, -1) for y in ys]))
        def extra(ctx_, pl, g_): _fuss_schrauben(ctx_, pl, [(-lx / 2 - fl[1] / 2, y, fl[2]) for y in ys], sd, fl[2] + a("A_e2_box_wand_mm"), "BT-711")
        return s, "Stahl", a("A_e2_schuetz_masse_kg"), extra
    return _geraet_teile(ctx, ("Hauptschuetz_plus", "Hauptschuetz_minus"), kopf)


@teil("kaufteile.schuetz_vorlade", "BT-712", "F")
def schuetz_vorlade(ctx, pos):
    """Vorladung BT-712 (2: Vorladeschütz und Vorladewiderstand; ENT-125/126): Quader A_e2_vorladeschuetz_mm und A_e2_vorladewiderstand_mm (liegend, lx × ly × lz aus
    ctx.schaltbox['geraete']), 2 Bolzen je Gerät. Masse je Gerät A_e2_vorlade_masse_kg / 2. Stufe F."""
    def kopf(n, g):
        lx, ly, lz = g["l"]; return quader(-lx / 2, -ly / 2, 0, lx / 2, ly / 2, lz), "Stahl", a("A_e2_vorlade_masse_kg") / 2, None
    return _geraet_teile(ctx, ("Vorladeschuetz", "Vorladewiderstand"), kopf)


@teil("kaufteile.sicherungen", "BT-713", "F")
def sicherungen(ctx, pos):
    """Sicherungen BT-713 (2; ENT-127/128/129): Pyrosicherung als Zylinder Ø30 × 80 (A_e2_pyro_mm, Achse lokal y), Schmelzsicherung als Halter 40 × 40 × 95
    (A_e2d_schmelz_halter_mm, Kunststoff; Sicherung 30 × 30 × 85 sitzt im Halter und ist nicht getrennt gezeichnet). Laschen vereinfacht als Bolzen
    an den Stirnseiten (A_g54_schiene_pad_abstand_mm). Masse A_e2_pyro_masse_kg und A_e2_schmelz_masse_kg. Stufe F."""
    def kopf(n, g):
        lx, ly, lz = g["l"]
        if n == "Pyrosicherung": return Part.makeCylinder(lx / 2, ly, V(0, -ly / 2, lz / 2), V(0, 1, 0)), "Stahl", a("A_e2_pyro_masse_kg"), None
        return quader_r(-lx / 2, -ly / 2, 0, lx / 2, ly / 2, lz, 3.0, "z"), "Kunststoff", a("A_e2_schmelz_masse_kg"), None
    return _geraet_teile(ctx, ("Pyrosicherung", "Schmelzsicherung"), kopf)


def _stecker_teil(ctx, n, abm, fl_k, schr, koerper, masse, bt):
    S = _sb(ctx); pl = S["stecker"][n]; sl, sb, sh = a(abm); fx, fy, fd = a(fl_k); ns, ds = a(schr)
    s = quader_r(-fx / 2, -fy / 2, 0, fx / 2, fy / 2, fd, 2.0, "z")
    ein = a("A_e2d_stecker_koerper_einzug_mm")
    if koerper: kx, ky = a(koerper); s = s.fuse(quader(-sl / 2, -ky / 2, fd, -sl / 2 + kx, ky / 2, sh))
    else: s = s.fuse(quader(-sl / 2, -sb / 2 + ein, fd, sl / 2 - ein, sb / 2 - ein, sh))
    if n == "HV250":
        hl, hb, hh = a("A_e2d_hv250_hebel_mm"); hx = a("A_g54_hv250_hebel_x_mm"); s = s.fuse(quader(-sl / 2 + hx, -hb / 2, sh, -sl / 2 + hx + hl, hb / 2, sh + hh))
    pts = {"HV250": [(x, y) for x in (12, 36) for y in (-27, 27)], "HV40": [(sx * 19, sy * 16) for sx in (-1, 1) for sy in (-1, 1)], "NV": [(21, -8), (21, 8)]}[n][:int(ns)]      # Schrauben neben dem Körper (Kopf Ø nach ISO 7380), nicht an den Ecken
    s = bohrungen(s, [(x, y, -1) for x, y in pts], ds / 2, fd + 2)
    for sg, dy in (("plus", -sb / 4), ("minus", sb / 4)):
        if n != "NV": s = s.fuse(Part.makeCylinder(a("A_e2d_schuetz_bolzen_d_mm") / 2, a("A_e2d_schuetz_bolzen_h_mm"), V(-sl / 2, dy, sh / 2), V(-1, 0, 0)))
    for x, y in pts:
        ctx.schrauben.append(dict(typ="Linsenkopf", d=ds, l=fd + min(a("A_e2d_stecker_schraube_einzug_mm"), ctx.dec - 0.2), placement=pl.multiply(FreeCAD.Placement(V(x, y, fd), FreeCAD.Rotation())), bt=bt, **{"in": ["BT-520"]}))
    return Teil(n, setze(s.removeSplitter(), pl), "PA66GF30", masse_kg=masse)


@teil("kaufteile.hv_stecker", "BT-730", "F")
def hv_stecker(ctx, pos):
    """HV-Stecker BT-730 (2: HV250 90 × 70 × 8 Flansch und HV40 50 × 40 × 6; ENT-132/133): Flansch mit Eckbohrungen (A_e2d_hv250_schrauben / hv40_schrauben), Körper
    (HV250: A_e2d_hv250_koerper_mm, mit Hebel A_e2d_hv250_hebel_mm; HV40: Flansch abzüglich Einzug A_e2d_stecker_koerper_einzug_mm), Gesamthöhe A_e2_hv250_mm bzw. A_e2_hv40_mm,
    2 Bolzen an der Vorderfläche an den Polen aus ctx.schaltbox['klemmen']. Schrauben in den Deckel (ctx.schrauben, schneiden BT-520). Masse A_e2_hv250_masse_kg / A_e2_hv40_masse_kg. Stufe F."""
    return [_stecker_teil(ctx, "HV250", "A_e2_hv250_mm", "A_e2d_hv250_flansch_mm", "A_e2d_hv250_schrauben", "A_e2d_hv250_koerper_mm", a("A_e2_hv250_masse_kg"), "BT-730"),
            _stecker_teil(ctx, "HV40", "A_e2_hv40_mm", "A_e2d_hv40_flansch_mm", "A_e2d_hv40_schrauben", None, a("A_e2_hv40_masse_kg"), "BT-730")]


@teil("kaufteile.nv_stecker", "BT-740", "F")
def nv_stecker(ctx, pos):
    """NV-Stecker BT-740 (1, 26-polig; ENT-134): Flansch 50 × 30 × 5 (A_e2d_nv_flansch_mm) mit 2 Schrauben (A_e2d_nv_schrauben), Körper bis Höhe A_e2_nv_mm. Masse A_e2_nv_masse_kg. Stufe F."""
    return [_stecker_teil(ctx, "NV", "A_e2_nv_mm", "A_e2d_nv_flansch_mm", "A_e2d_nv_schrauben", None, a("A_e2_nv_masse_kg"), "BT-740")]


@teil("kaufteile.gassensor", "BT-770", "F")
def gassensor(ctx, pos):
    """Gassensor BT-770 (1; ENT-137): Quader A_e2_gas_mm, Lage aus ctx.schaltbox['lagen']. Masse A_e2_gas_masse_kg. Stufe F."""
    def kopf(n, g):
        lx, ly, lz = g["l"]; return quader(-lx / 2, -ly / 2, 0, lx / 2, ly / 2, lz), "PA66GF30", a("A_e2_gas_masse_kg"), None
    return _geraet_teile(ctx, ("Gassensor",), kopf)


@teil("kaufteile.trennstecker", "BT-720", "F")
def trennstecker(ctx, pos):
    """Trennstecker NMC BT-720 (1, Service, ENT-131): Quader A_e2_trennstecker_mm 80 × 50 × 60 auf dem Deckel mittig über den beiden Reihenmitten-Laschen (Mitte der Zellen
    Mitte_A_Ende_Band2 und Mitte_B_Anfang_Band3, wie e2d). Einbauort: ctx.einbau['BT-720'], sonst aus den Zellen abgeleitet. Masse A_e2_trennstecker_masse_kg. Stufe F."""
    if VAR != "NMC": return []
    from teile._verdrahtung import verdr
    pls = ctx.einbau.get("BT-720")
    if pls: pl = pls[0]
    else:
        R = verdr(ctx); A_, B_ = R["ans"]["Mitte_A_Ende_Band2"], R["ans"]["Mitte_B_Anfang_Band3"]
        pl = einbau((A_["cx"] + B_["cx"]) / 2, (A_["cy"] + B_["cy"]) / 2, ctx.schaltbox["z_deckel_o"] if False else ctx.z_deckel_o)
    l, b, h = a("A_e2_trennstecker_mm")
    return [Teil("Trennstecker", setze(quader(-l / 2, -b / 2, 0, l / 2, b / 2, h), pl), "PA66GF30", masse_kg=a("A_e2_trennstecker_masse_kg"))]


def _ohne_ort(bt, name):
    pls = None
    print(f"  kaufteile: kein Einbauort ctx.einbau['{bt}'] für {name}: 0 Teile (Wunsch an Opus: Einbauort vorab festlegen)")
    return []


@teil("kaufteile.druckausgleich", "BT-570", "F")
def druckausgleich(ctx, pos):
    """Druckausgleichselement BT-570 (1; Maße A_g5_druckausgleich_mm 17 × 12,9 × 7,8): Quader an ctx.einbau['BT-570'] (Rückwand). Ohne Einbauort 0 Teile. Stufe F."""
    pls = ctx.einbau.get("BT-570")
    if not pls: return _ohne_ort("BT-570", "Druckausgleich")
    l, b, h = a("A_g5_druckausgleich_mm"); return [Teil("Druckausgleich", setze(quader(-l / 2, -b / 2, 0, l / 2, b / 2, h), pls[0]), "PA66GF30")]


@teil("kaufteile.entgasungsventil", "BT-750", "H")
def entgasungsventil(ctx, pos):
    """Entgasungsventil BT-750 (1; Maße A_g5_entgasungsventil_mm 77 × 55 × 22,5): Quader an ctx.einbau['BT-750'] (Rückwand). Ohne Einbauort 0 Teile. Stufe H."""
    pls = ctx.einbau.get("BT-750")
    if not pls: return _ohne_ort("BT-750", "Entgasungsventil")
    l, b, h = a("A_g5_entgasungsventil_mm"); return [Teil("Entgasungsventil", setze(quader(-l / 2, -b / 2, 0, l / 2, b / 2, h), pls[0]), "PA66GF30")]


@teil("kaufteile.typschild", "BT-780", "H")
def typschild(ctx, pos):
    """Typschild BT-780 (1, Kennzeichnung auf dem Deckel vorn): Al-Folie A_g5_typschild_mm, Einbauort ctx.einbau['BT-780'] (gehaeuse.einbau_aussen). Stufe H."""
    pls = ctx.einbau.get("BT-780")
    if not pls: return _ohne_ort("BT-780", "Typschild")
    l, b, h = a("A_g5_typschild_mm")
    return [Teil("Typschild", setze(quader(-l / 2, -b / 2, 0, l / 2, b / 2, h), pls[0]), "Al")]


@teil("kaufteile.temperaturfuehler_kuehlmittel", "BT-640", "H")
def temperaturfuehler_kuehlmittel(ctx, pos):
    """Temperaturfühler Kühlmittel BT-640 (2: Ein, Aus; Kyocera AVX 94082, Datenblatt S. 3): Gewinde M12 × 1,5 nach unten in Verteiler/Sammler,
    Sechskant, Körper, Stecker. Einbauorte ctx.einbau['BT-640'] (gehaeuse.einbau_aussen, Oberseite der Blöcke). Maße A_g5_kuehlmittelfuehler_*. Stufe F."""
    pls = ctx.einbau.get("BT-640")
    if not pls: return _ohne_ort("BT-640", "Temperaturfühler Kühlmittel")
    dm, _, lg = a("A_g5_kuehlmittelfuehler_mm"); f = a("A_g5_kuehlmittelfuehler_form_mm"); from kern import sechskant
    sl, sb, sh = f["stecker"]; hk = lg - f["gewinde_l"] - f["sechskant_h"] - sh
    s = zylinder(dm / 2 - 0.2, f["gewinde_l"], 0, 0, -f["gewinde_l"])
    s = s.fuse(sechskant(f["sw"], f["sechskant_h"], 0, 0, 0))
    s = s.fuse(zylinder(f["koerper_d"] / 2, hk, 0, 0, f["sechskant_h"]))
    s = s.fuse(quader(-sl / 2, -sb / 2, f["sechskant_h"] + hk, sl / 2, sb / 2, lg - f["gewinde_l"])).removeSplitter()
    return [Teil(f"Kuehlmittelfuehler_{n}", setze(s, pl), "PA66GF30", masse_kg=a("A_g5_kuehlmittelfuehler_masse_kg")) for n, pl in zip(("ein", "aus"), pls)]
