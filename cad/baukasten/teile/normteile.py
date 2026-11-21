# KI-generiert (Claude Sonnet, 2026-11-19), Entwurf. Auftrag G5.4 (cad/baukasten/AUFTRAG_G5_4.md), Modul normteile.
"""Normteile: Schrauben (alle Schraubstellen aus ctx.schrauben), Kabelschuhe, Clips, Schrumpfschlauch, Dichtungen. Läuft nach allen Modulen, die Schraubstellen melden
(MODULFOLGE: zelle, schaltbox, verbinder, elektronik, kaufteile, normteile, gehaeuse, kuehlung): die Deckelschrauben von gehaeuse.py (ctx.deckelschrauben) und die Löcher-Schrauben
der Kühlung kommen erst danach und fehlen hier (Wunsch an Opus, siehe Rückgabe). Stückzahlen kommen aus der Geometrie (menge_quelle CAD, Stückliste übernimmt sie).
Schraubenlage: Placement mit Ursprung in der Kopfauflage, +z vom Material weg, Schaft nach −z (wie schaltbox.py). Normmaße: A_g54_iso7380_mm, _iso4017_mm, _iso10642_mm, _mutter_mm."""
import math
import FreeCAD
from kern import teil, p, a, Teil, quader, zylinder, sechskant, flachkopf, setze, einbau, VAR, Part, V
from teile.verbinder import _verb, _kabel, _schienen, _service


def _tripel(name, d):
    t = a(name)
    for i in range(0, len(t), 3):
        if abs(t[i] - d) < 1e-6: return t[i + 1], t[i + 2]
    raise SystemExit(f"FEHLT Normmaß {name} für M{d:g}")


def _schraubenform(typ, d, l):
    """Lokale Form: Kopfauflage bei z = 0, Schaft nach −z."""
    if typ == "Sechskant":
        s, k = _tripel("A_g54_iso4017_mm", d); return sechskant(s, k, 0, 0, 0).fuse(zylinder(d / 2, l, 0, 0, -l))
    if typ == "Linsenkopf":
        dk, k = _tripel("A_g54_iso7380_mm", d); return flachkopf(d, k, dk, 0, 0, 0, l)
    if typ == "Senkkopf":
        dk, k = a("A_g54_iso10642_mm")[1:]; return Part.makeCone(d / 2, dk / 2, k, V(0, 0, -k), V(0, 0, 1)).fuse(zylinder(d / 2, l - k, 0, 0, -l))
    if typ == "Mutter":
        dn, s, m = a("A_g54_mutter_mm"); return sechskant(s, m, 0, 0, 0).cut(zylinder(dn / 2, m + 2, 0, 0, -1))
    raise SystemExit(f"Schraubentyp unbekannt: {typ}")


@teil("normteile.schraube", "BT-590", "F")
def schraube(ctx, pos):
    """Schrauben und Muttern BT-590 (Stahl): eine Form je Schraubstelle aus ctx.schrauben (dict typ Sechskant/Linsenkopf/Senkkopf/Mutter, d, l, placement[, bt, in]).
    Kopfformen nach A_g54_iso4017_mm (Sechskant), A_g54_iso7380_mm (Linsenkopf), A_g54_iso10642_mm (Senkkopf), Mutter A_g54_mutter_mm. Schraubenlöcher in Fremdteilen: Schlüssel 'in' = [BT …]
    schneidet den Schaft dort aus (ctx.schneide). Werkstoff Stahl (Dichte farben.json). Stufe F."""
    teile = []; cache = {}
    for i, sp in enumerate(ctx.schrauben):
        key = (sp["typ"], sp["d"], round(sp["l"], 3))
        if key not in cache: cache[key] = _schraubenform(*key)
        s = setze(cache[key], sp["placement"])
        teile.append(Teil(f"{sp['typ']}_{i:03d}_M{sp['d']:g}_{sp.get('bt', '')}", s, "Stahl"))
        if sp.get("in") and sp["l"] > 0:
            ctx.schneide(setze(zylinder(sp["d"] / 2, sp["l"], 0, 0, -sp["l"]), sp["placement"]), list(sp["in"]), "schraube")
    return teile


@teil("normteile.kabelschuh", "BT-590", "F")
def kabelschuh(ctx, pos):
    """Kabelschuhe BT-590 (Cu) an beiden Enden jeder HV-Leitung mit Kabelschuh (Plus, Minus; die NMC-Mittenleitungen enden direkt am Trennstecker): Palme
    A_e2d_kabelschuh_lasche_mm (20 breit × 4) × A_e2d_kabelschuh_lasche_laenge_mm (20) mit Bohrung M8, Hülse A_e2d_kabelschuh_huelse_mm (40) mit Außen-Ø = Leitungs-Ø + 2 × A_g54_kabelschuh_huelse_wand_mm.
    Zellseite: Palme liegend auf der Pol-Lasche, Hülse senkrecht; Boxseite: Palme senkrecht vor dem Schienen-Pad, Hülse zur Wand. Stufe F."""
    pw, pt = a("A_e2d_kabelschuh_lasche_mm"); pl = a("A_e2d_kabelschuh_lasche_laenge_mm"); hu = a("A_e2d_kabelschuh_huelse_mm"); w = a("A_g54_kabelschuh_huelse_wand_mm"); bo = a("A_e2_lasche_bohrung_mm") / 2
    teile = []
    for nm, k in _kabel(ctx).items():
        if not k["palme"]: continue
        rh = k["d"] / 2 + w; P = k["palme"]; hx, hy = P["loch"]; fx, fy = P["fuss"]; z0 = P["z"]
        y0, y1 = min(hy - pl / 2, fy - k["d"] / 2), max(hy + pl / 2, fy + k["d"] / 2)
        pal = quader(hx - pw / 2, y0, z0, hx + pw / 2, y1, z0 + pt).cut(zylinder(bo, pt + 2, hx, hy, z0 - 1))
        teile.append(Teil(f"Kabelschuh_{nm}_Zelle", pal.fuse(zylinder(rh, hu, fx, fy, z0 + pt)), "Cu"))
        xi, yE, zin, d = k["ende_b"]; sg = P["sg"]; yc, tb = P["yc"], P["tb"]
        ya, yb = sorted((yc - sg * tb / 2, yc - sg * (tb / 2 + pt)))
        pal2 = quader(xi - pw / 2, ya, zin - pl / 2, xi + pw / 2, yb, zin + pl / 2).cut(Part.makeCylinder(bo, pt + 2, V(xi, yc - sg * (tb / 2 - 1), zin), V(0, -sg, 0)))
        teile.append(Teil(f"Kabelschuh_{nm}_Box", pal2.fuse(Part.makeCylinder(rh, hu, V(xi, yc - sg * (tb / 2 + pt), zin), V(0, -sg, 0))), "Cu"))
    return teile


@teil("normteile.clip", "BT-590", "F")
def clip(ctx, pos):
    """Kabelclips BT-590 (Kunststoff): alle A_e2d_clip_abstand_mm (200) mm auf den waagerechten Geradenstücken der HV-Leitung in Höhe des Eintritts, Auflage
    A_e2d_clip_mm 20 (längs) × 15 (quer) × 10 hoch bis zur Leitungsachse, aus der Deckeloberfläche, mit Rille für die Leitung. Stufe F."""
    cl, cb, ch = a("A_e2d_clip_mm"); ab = a("A_e2d_clip_abstand_mm"); teile = []; zd = ctx.z_deckel_o; n = 0
    for nm, k in _kabel(ctx).items():
        if k["ende_b"] is None: continue
        zin = k["ende_b"][2]; r = k["d"] / 2
        for (P, Q) in k["gerade"]:
            if abs(P.z - zin) > 1e-6 or abs(Q.z - zin) > 1e-6: continue
            Ln = (Q - P).Length; u = (Q - P); u.normalize(); s = ab
            while s < Ln - cl:
                c = P + u * s; ex = abs(u.y) > 0.5
                bx = quader(c.x - cb / 2, c.y - cl / 2, max(zd, zin - ch), c.x + cb / 2, c.y + cl / 2, zin) if ex else quader(c.x - cl / 2, c.y - cb / 2, max(zd, zin - ch), c.x + cl / 2, c.y + cb / 2, zin)
                rille = Part.makeCylinder(r, cl * 3, V(c.x, c.y, zin) - u * 1.5 * cl, u)
                teile.append(Teil(f"Clip_{nm}_{n:02d}", bx.cut(rille), "Kunststoff")); n += 1; s += ab
    return teile


@teil("normteile.schrumpfschlauch", "BT-590", "F")
def schrumpfschlauch(ctx, pos):
    """Schrumpfschlauch BT-590 (Kunststoff): Hülle A_e2d_schrumpfschlauch_mm (0,5 mm) um das längste gerade Stück jeder Stromschiene (ohne die Endbereiche von Breite + 10 mm),
    Querschnitt Schiene + 2 × 0,5 an den Seiten und oben, unten offen (Geräte liegen bis zur Schiene). Schienen mit zu kurzem Mittelstück bekommen keinen. Stufe F."""
    dd = a("A_e2d_schrumpfschlauch_mm"); teile = []; alle = Part.makeCompound([x["shape"] for x in _schienen(ctx)])
    for s in _schienen(ctx):
        w = s["w"]; best = None
        for lo, hi, u, Ln in s["beine"]:
            if u != 2 and (best is None or Ln > best[3]): best = (lo, hi, u, Ln)       # nur waagerechte Stücke in der Leitungsebene
        if best is None: continue
        lo, hi, u, Ln = best
        if hi[u] - lo[u] < 2 * (w + 10) + 10: continue
        lo = list(lo); hi = list(hi); lo[u] += w + 10; hi[u] -= w + 10
        inn = quader(*lo, *hi)      # unten offen (Auflage auf den Geräten)
        lo2 = [lo[k] - (dd if k not in (u, 2) else 0) for k in range(3)]; hi2 = [hi[k] + (dd if k != u else 0) for k in range(3)]
        sl = quader(*lo2, *hi2).cut(alle); teile.append(Teil(f"Schrumpfschlauch_{s['name']}", sl, "Kunststoff")); ctx.schneide(sl, ["BT-710"], "wanddurchfuehrung")
    return teile


@teil("normteile.dichtung", "BT-580", "F")
def dichtung(ctx, pos):
    """Dichtungen BT-580 (EPDM, Schnur A_e2d_box_dichtung_mm / A_e2d_servicedeckel_dichtung_mm 3 × 3): Schaltbox (Rahmen auf dem Flansch, 3 mm von der Außenkante nach innen) und
    Servicedeckel (LFP; Rahmen 9 mm nach innen von der Deckelkante, zwischen Schrauben und Öffnung). Eine Deckel-Dichtung am Rahmen gibt es nicht (kein Spalt im Stapel,
    Deckel liegt direkt auf dem Rahmen). Stufe F."""
    S = ctx.schaltbox; teile = []
    def ring(x0, y0, x1, y1, w, z0, h, nm):
        return Teil(nm, quader(x0, y0, z0, x1, y1, z0 + h).cut(quader(x0 + w, y0 + w, z0 - 1, x1 - w, y1 - w, z0 + h + 1)), "EPDM")
    if S.get("fertig"):
        x0, y0, z0, x1, y1, zw = S["box"]; fl, fd = S["flansch"]; dw, dh = S["dichtung"]
        o = fl - dw - 0.5                                                   # Mitte des Flanschrandes außen, frei von den Schraubenlöchern (Flansch außen 12, Schrauben ~5 vom Boxrand)
        teile.append(ring(x0 - fl + 0.5, y0 - fl + 0.5, x1 + fl - 0.5, y1 + fl - 0.5, dw, zw, dh, "Dichtung_Schaltbox"))
    if VAR == "LFP":
        g = _service(ctx); teile.append(ring(g["x0"] + 7.5, g["py"] - g["sl"] / 2 + 7.5, g["x0"] + g["sb"] - 7.5, g["py"] + g["sl"] / 2 - 7.5, g["dgw"], ctx.z_deckel_o, g["dgh"], "Dichtung_Servicedeckel"))
    return teile
