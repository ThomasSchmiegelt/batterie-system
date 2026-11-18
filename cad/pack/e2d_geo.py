# KI-generiert (Claude Sonnet, 2026-11-18), Entwurf. Auftrag E2 Fortsetzung 5 (Detailierung Konstruktionsstand).
"""Hilfsfunktionen für pack_e2d.py (FreeCAD): Biegebahnen mit Radius, Stromschienen, Schrumpfschlauch, Kabelschichten, Clips, Schrauben.
Alle Maße kommen als Argumente aus pack_e2d.py (Akten, Block A_e2d_*). Keine eigenen Maße in dieser Datei."""
import math
import Part
from FreeCAD import Vector as V


def box(x0, y0, z0, x1, y1, z1):
    return Part.makeBox(x1 - x0, y1 - y0, z1 - z0, V(x0, y0, z0))


def cyl(x, y, z0, z1, r):
    return Part.makeCylinder(r, z1 - z0, V(x, y, z0))


def fillet_edges(pts, Rc, to3d):
    """Polylinie pts [(s,z),...] mit Ausrundung Rc an jeder inneren Ecke. to3d(s,z) -> Vector. Gibt (Kanten, Länge) zurück."""
    P = [pts[0]]
    for p in pts[1:]:
        if abs(p[0] - P[-1][0]) > 1e-9 or abs(p[1] - P[-1][1]) > 1e-9: P.append(p)
    # kollineare innere Punkte entfernen
    Q = [P[0]]
    for i in range(1, len(P) - 1):
        a = (P[i][0] - Q[-1][0], P[i][1] - Q[-1][1]); b = (P[i + 1][0] - P[i][0], P[i + 1][1] - P[i][1])
        if abs(a[0] * b[1] - a[1] * b[0]) > 1e-9: Q.append(P[i])
    Q.append(P[-1]); P = Q
    edges = []; cur = P[0]; L = 0.0
    for i in range(1, len(P) - 1):
        a, c, b = P[i - 1], P[i], P[i + 1]
        u1 = (c[0] - a[0], c[1] - a[1]); l1 = math.hypot(*u1); u1 = (u1[0] / l1, u1[1] / l1)
        u2 = (b[0] - c[0], b[1] - c[1]); l2 = math.hypot(*u2); u2 = (u2[0] / l2, u2[1] / l2)
        cosang = max(-1, min(1, u1[0] * u2[0] + u1[1] * u2[1])); ang = math.acos(cosang)      # Ablenkwinkel
        tl = Rc * math.tan(ang / 2)
        if tl > min(l1, l2) * (1.0 if i in (1, len(P) - 2) else 0.5) + 1e-6: raise ValueError(f"Biegung zu kurz: Schenkel {l1:.1f}/{l2:.1f} mm, Tangentenlänge {tl:.1f} mm")
        p1 = (c[0] - u1[0] * tl, c[1] - u1[1] * tl); p2 = (c[0] + u2[0] * tl, c[1] + u2[1] * tl)
        if math.hypot(p1[0] - cur[0], p1[1] - cur[1]) > 1e-9: edges.append(Part.makeLine(to3d(*cur), to3d(*p1))); L += math.hypot(p1[0] - cur[0], p1[1] - cur[1])
        dv = (u2[0] - u1[0], u2[1] - u1[1]); ld = math.hypot(*dv); dist_c = Rc / math.cos(ang / 2)
        cen = (c[0] + dv[0] / ld * dist_c, c[1] + dv[1] / ld * dist_c)
        mv = (c[0] - cen[0], c[1] - cen[1]); lm = math.hypot(*mv); pm = (cen[0] + mv[0] / lm * Rc, cen[1] + mv[1] / lm * Rc)
        edges.append(Part.Arc(to3d(*p1), to3d(*pm), to3d(*p2)).toShape()); L += Rc * ang; cur = p2
    edges.append(Part.makeLine(to3d(*cur), to3d(*P[-1]))); L += math.hypot(P[-1][0] - cur[0], P[-1][1] - cur[1])
    return edges, L


def sweep_rect(pts, Rc, to3d, wvec, w, t, tvec_first=None):
    """Rechteckprofil (Breite w entlang wvec, Dicke t in der Bahnebene) entlang der ausgerundeten Polylinie. Gibt (Solid, Bahnlänge)."""
    edges, L = fillet_edges(pts, Rc, to3d)
    wire = Part.Wire(edges)
    p0 = to3d(*pts[0]); p1 = None
    for p in pts[1:]:
        if abs(p[0] - pts[0][0]) > 1e-9 or abs(p[1] - pts[0][1]) > 1e-9: p1 = to3d(*p); break
    T = (p1 - p0); T.normalize()
    W = V(*wvec); W.normalize(); N = T.cross(W); N.normalize()
    c = [p0 + W * (w / 2) + N * (t / 2), p0 - W * (w / 2) + N * (t / 2), p0 - W * (w / 2) - N * (t / 2), p0 + W * (w / 2) - N * (t / 2)]
    prof = Part.makePolygon(c + [c[0]])
    return wire.makePipeShell([prof], True, True, 1), L


def schiene(pa, pb, pts_sz, w, t, Rc, bohr_r=None, loecher=()):
    """Stromschiene zwischen Punkten pa=(x,y), pb=(x,y) (Draufsicht). pts_sz = [(s,z),...] Mittellinie, s = Abstand entlang pa->pb.
    Gibt (Solid, Länge Mittellinie)."""
    dx, dy = pb[0] - pa[0], pb[1] - pa[1]; Ln = math.hypot(dx, dy); d = (dx / Ln, dy / Ln)
    to3d = lambda s, z: V(pa[0] + d[0] * s, pa[1] + d[1] * s, z)
    sol, L = sweep_rect(pts_sz, Rc, to3d, (-d[1], d[0], 0), w, t)
    for (s, r) in loecher:
        zs = [p[1] for p in pts_sz]; sol = sol.cut(cyl(pa[0] + d[0] * s, pa[1] + d[1] * s, min(zs) - t - 2, max(zs) + t + 2, r))
    return sol, L


def schlauch(pa, pb, pts_sz, w, t, Rc, dicke, frei):
    """Schrumpfschlauch (Wanddicke dicke) um die Schiene, ohne die Kontaktflächen (frei = [(s, halbbreite)]); gibt Solid oder None."""
    dx, dy = pb[0] - pa[0], pb[1] - pa[1]; Ln = math.hypot(dx, dy); d = (dx / Ln, dy / Ln)
    to3d = lambda s, z: V(pa[0] + d[0] * s, pa[1] + d[1] * s, z)
    kern, _ = sweep_rect(pts_sz, Rc, to3d, (-d[1], d[0], 0), w, t)
    gross, _ = sweep_rect(pts_sz, Rc, to3d, (-d[1], d[0], 0), w + 2 * dicke, t + 2 * dicke)
    sl = gross.cut(kern); zs = [p[1] for p in pts_sz]
    for (s, hb) in frei:
        sl = sl.cut(box(pa[0] + d[0] * s - hb, pa[1] + d[1] * s - hb, min(zs) - t - 3, pa[0] + d[0] * s + hb, pa[1] + d[1] * s + hb, max(zs) + t + 3))
    return sl if sl.Solids else None


def kabel_schichten(wire, p0, tang, radien):
    """Konzentrische Schichten (radien aufsteigend: Leiter, Isolierung, Schirm, Mantel) als Vollkörper-Differenzen. Gibt Liste von Solids."""
    vol = []
    for r in radien: vol.append(wire.makePipeShell([Part.Wire(Part.makeCircle(r, p0, tang))], True, True))
    out = [vol[0]]
    for i in range(1, len(vol)): out.append(vol[i].cut(vol[i - 1]))
    return out


def schraube(x, y, z_top_unter, schaft_d, schaft_l, kopf_d, kopf_h, scheibe=None):
    """Schraube (Zylinderkopf): Kopf-Unterkante bei z_top_unter (Auflagefläche), optional Scheibe (d, h) zwischen Auflage und Kopf, Schaft nach unten (Länge schaft_l ab Auflage).
    Gibt Liste (Teilname, Solid)."""
    out = []; z = z_top_unter; zk = z
    if scheibe:
        sd, sh = scheibe; out.append(("Scheibe", cyl(x, y, z, z + sh, sd / 2).cut(cyl(x, y, z - 1, z + sh + 1, schaft_d / 2)))); zk = z + sh
    out.append(("Kopf", cyl(x, y, zk, zk + kopf_h, kopf_d / 2)))
    out.append(("Schaft", cyl(x, y, z - schaft_l, zk, schaft_d / 2)))
    return out
