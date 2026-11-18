#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. Auftrag K1 (Kopie aus K0, ergaenzt um Rand 15 = Oben/Deckel fuer Kuehlfall K3; sonst unveraendert).
Netz je Variante (gmsh, strukturiert, Hexaeder/Prismen) -> Elmer-Netz (ElmerGrid).
Alle Masse aus cad/zelle/entwurf/parameter_<V>_entwurf.json (BT-100/110/111/115/120) und
cad/zelle/entwurf/detail/ergebnis_detail_NMC.json (Kernhoehe z). Keine Zahl im Code ausser Netzfeinheit.
Aufruf: python3 geometrie.py LFP|NMC [Feinheit f=1|2] [--bodenspalt]
Achsen LFP: x = Laenge, y = Breite (90 mm, senkrecht, Boden y=0 = gekuehlte Schmalseite), z = Dicke.
Achsen NMC: z = Zellachse, Boden z=0.
Koerper: 1 Kern (LFP) | 101.. Kern-Sektoren (NMC) ; 2 Gehaeuse ; 3 Luft.  Raender: 11 Boden, 12 Mantel (Kuehlband 25 %, NMC), 13 Mantel Rest, 14 Rest."""
import sys, os, json, math, subprocess
import numpy as np
import gmsh
HIER = os.path.dirname(os.path.abspath(__file__))
R = os.path.abspath(os.path.join(HIER, "..", "..", ".."))

def lade(v):
    d = json.load(open(f"{R}/cad/zelle/entwurf/parameter_{v}_entwurf.json"))["parameter"]
    w = lambda bt, k: d[bt][k]["wert"]
    return d, w

def netz(v, f=1, bodenspalt_luft=False, name=None):
    d, w = lade(v)
    gmsh.initialize(); gmsh.option.setNumber("General.Terminal", 0)
    gmsh.model.add(v); g = gmsh.model.geo
    wand = w("BT-120", "wandstaerke_mm")
    vol_tags = {}   # physical tag -> [volume tags]
    info = {"variante": v, "feinheit": f, "wandstaerke_mm": wand}
    def vol(tag, vt): vol_tags.setdefault(tag, []).append(vt)
    if v == "LFP":
        L, B, T = w("BT-100", "laenge_mm"), w("BT-100", "breite_mm"), w("BT-100", "dicke_mm")
        Lk = w("BT-111", "laenge_mm")
        ez = (L - Lk) / 2.0
        xs = [0, wand, ez, ez + Lk, L - wand, L]; ys = [0, wand, B - wand, B]; zs = [0, wand, T - wand, T]
        nx = [1, 2 * f, 24 * f, 2 * f, 1]; ny = [1, 24 * f, 1]; nz = [1, 4 * f, 1]
        info.update(L=L, B=B, T=T, Kernlaenge=Lk, endzone_je_seite=ez)
        P = [[g.addPoint(x, y, 0) for x in xs] for y in ys]
        H = [[g.addLine(P[j][i], P[j][i + 1]) for i in range(len(xs) - 1)] for j in range(len(ys))]
        V = [[g.addLine(P[j][i], P[j + 1][i]) for j in range(len(ys) - 1)] for i in range(len(xs))]
        for j in range(len(ys)):
            for i in range(len(xs) - 1): g.mesh.setTransfiniteCurve(H[j][i], nx[i] + 1)
        for i in range(len(xs)):
            for j in range(len(ys) - 1): g.mesh.setTransfiniteCurve(V[i][j], ny[j] + 1)
        for i in range(len(xs) - 1):
            for j in range(len(ys) - 1):
                cl = g.addCurveLoop([H[j][i], V[i + 1][j], -H[j + 1][i], -V[i][j]])
                s = g.addPlaneSurface([cl]); g.mesh.setTransfiniteSurface(s); g.mesh.setRecombine(2, s)
                top = s
                for k in range(3):
                    out = g.extrude([(2, top)], 0, 0, zs[k + 1] - zs[k], [nz[k]], [], True)
                    top = out[0][1]
                    rand = (i in (0, len(xs) - 2)) or (j in (0, len(ys) - 2)) or (k in (0, 2))
                    if rand: tag = 2
                    elif i in (1, 3): tag = 3
                    else: tag = 1
                    vol(tag, out[1][1])
    else:
        Dm, Hh = w("BT-100", "durchmesser_mm"), w("BT-100", "hoehe_mm")
        Ra = Dm / 2.0; ri = w("BT-115", "durchmesser_mm") / 2.0; rk = Ra - wand
        dd = json.load(open(f"{R}/cad/zelle/entwurf/detail/ergebnis_detail_NMC.json"))
        z0, z1 = dd["wickel"]["hoehe_z_von_bis_mm"]
        z_gap_top = wand  # Becherboden-Oberseite
        N = 48; m = f; nr = 8 * f; nw = 1
        info.update(D=Dm, H=Hh, r_loch=ri, r_kern_aussen=rk, kern_z_von_bis=[z0, z1], sektoren=N)
        # z-Lagen: Boden | Spalt (Boden..Kernanfang) | Kern | Luft oben | Deckel
        lag = [(0, wand, "boden"), (wand, z0, "spalt"), (z0, z1, "kern"), (z1, Hh - wand, "oben"), (Hh - wand, Hh, "deckel")]
        nzl = {"boden": 1, "spalt": 1, "kern": 20 * f, "oben": 2 * f, "deckel": 1}
        c = g.addPoint(0, 0, 0)
        pt = lambda r, s: g.addPoint(r * math.cos(2 * math.pi * s / N), r * math.sin(2 * math.pi * s / N), 0)
        Pi = [pt(ri, s) for s in range(N)]; Pk = [pt(rk, s) for s in range(N)]; Po = [pt(Ra, s) for s in range(N)]
        arc = lambda Pp: [g.addCircleArc(Pp[s], c, Pp[(s + 1) % N]) for s in range(N)]
        Ai, Ak, Ao = arc(Pi), arc(Pk), arc(Po)
        R1 = [g.addLine(Pi[s], Pk[s]) for s in range(N)]; R2 = [g.addLine(Pk[s], Po[s]) for s in range(N)]
        for s in range(N):
            for a in (Ai[s], Ak[s], Ao[s]): g.mesh.setTransfiniteCurve(a, m + 1)
            g.mesh.setTransfiniteCurve(R1[s], nr + 1); g.mesh.setTransfiniteCurve(R2[s], nw + 1)
        flaechen = []   # (surface, art, sektor)
        s_hole = g.addPlaneSurface([g.addCurveLoop(Ai)]); g.mesh.setRecombine(2, s_hole); flaechen.append((s_hole, "loch", -1))
        for s in range(N):
            s1 = (s + 1) % N
            sk = g.addPlaneSurface([g.addCurveLoop([Ai[s], R1[s1], -Ak[s], -R1[s]])])
            sw = g.addPlaneSurface([g.addCurveLoop([Ak[s], R2[s1], -Ao[s], -R2[s]])])
            for sf, art in ((sk, "kern"), (sw, "wand")):
                g.mesh.setTransfiniteSurface(sf); g.mesh.setRecombine(2, sf); flaechen.append((sf, art, s))
        for sf, art, s in flaechen:
            top = sf
            for (za, zb, lname) in lag:
                out = g.extrude([(2, top)], 0, 0, zb - za, [nzl[lname]], [], True); top = out[0][1]
                if art == "wand" or lname in ("boden", "deckel"): tag = 2
                elif lname == "spalt": tag = (101 + s) if (art == "kern" and not bodenspalt_luft) else 3
                elif lname == "kern": tag = (101 + s) if art == "kern" else 3
                elif lname == "oben": tag = 4   # Nachtrag K1: eigener Koerper (Luft oder Tab-Scheibe je Fall)
                else: tag = 3
                vol(tag, out[1][1])
        info["bodenspalt_luft"] = bodenspalt_luft
    g.synchronize()
    # Randflaechen klassifizieren
    surf = {11: [], 12: [], 13: [], 14: [], 15: []}
    Hmax = (info["H"] if v == "NMC" else None)
    for (dim, t) in gmsh.model.getEntities(2):
        bb = gmsh.model.getBoundingBox(dim, t); com = gmsh.model.occ.getCenterOfMass(dim, t) if False else None
        x0, y0, z0_, x1, y1, z1_ = bb
        if v == "LFP":
            if abs(y1) < 1e-6: surf[11].append(t)
            elif abs(y0 - info["B"]) < 1e-6 and abs(y1 - info["B"]) < 1e-6: surf[15].append(t)
            elif abs(y0 - info["B"]) < 1e-6 or abs(x0) < 1e-6 or abs(x1 - info["L"]) < 1e-6 or abs(z0_) < 1e-6 or abs(z1_ - info["T"]) < 1e-6:
                surf[14].append(t)
        else:
            if abs(z1_) < 1e-6: surf[11].append(t)
            elif abs(z0_ - info["H"]) < 1e-6: surf[15].append(t)
            elif z1_ - z0_ > 1e-6 and max(math.hypot(x0, y0), math.hypot(x1, y1), math.hypot(x0, y1), math.hypot(x1, y0)) > Ra - 1e-6 and abs(z0_) > -1:
                # lateraler Mantel-Aussenflaeche: Mittelpunkt liegt nahe R
                cx, cy, cz = (x0 + x1) / 2, (y0 + y1) / 2, 0
                pts = gmsh.model.getBoundary([(2, t)], oriented=False, recursive=True)
                rr = [math.hypot(*gmsh.model.getValue(0, p[1], [])[:2]) for p in pts]
                if min(rr) > Ra - 1e-6:
                    ang = math.degrees(math.atan2(cy, cx)) % 360
                    surf[12 if ang < 90 else 13].append(t)
    names = {11: "Boden", 12: "Mantel_Kuehlband", 13: "Mantel_Rest", 14: "Rest", 15: "Oben"}
    for k, ts in surf.items():
        if ts: gmsh.model.addPhysicalGroup(2, ts, k); gmsh.model.setPhysicalName(2, k, names[k])
    vnames = {1: "Kern", 2: "Gehaeuse", 3: "Luft", 4: "Luft_oben"}
    for k, ts in vol_tags.items():
        gmsh.model.addPhysicalGroup(3, ts, k); gmsh.model.setPhysicalName(3, k, vnames.get(k, f"Kern_Sektor_{k-101}"))
    gmsh.option.setNumber("Mesh.MshFileVersion", 2.2)
    gmsh.model.mesh.generate(3)
    ordner = f"{HIER}/elmer/netz_{name or v}_f{f}"; os.makedirs(ordner, exist_ok=True)
    msh = f"{ordner}/netz.msh"; gmsh.write(msh)
    # Volumina je Koerper-Gruppe und Randflaechen (aus Netz)
    def qsum(dim, ts):
        s = 0.0
        for t in ts:
            et, tags, _ = gmsh.model.mesh.getElements(dim, t)
            for e in tags:
                s += float(np.sum(gmsh.model.mesh.getElementQualities(list(map(int, e)), "volume")))
        return s
    info["V_luft_oben_mm3"] = qsum(3, vol_tags.get(4, [])) if 4 in vol_tags else 0.0
    kern_tags = [t for k, ts in vol_tags.items() if (k == 1 or k >= 101) for t in ts]
    info["V_kern_mm3"] = qsum(3, kern_tags)
    info["V_gehaeuse_mm3"] = qsum(3, vol_tags.get(2, []))
    info["V_luft_mm3"] = qsum(3, vol_tags.get(3, []))
    info["A_boden_mm2"] = qsum(2, surf[11]); info["A_kuehlband_mm2"] = qsum(2, surf[12]); info["A_oben_mm2"] = qsum(2, surf[15])
    info["n_knoten"] = len(gmsh.model.mesh.getNodes()[0])
    info["n_elemente_3d"] = int(sum(len(e) for dd_ in [gmsh.model.mesh.getElements(3)[1]] for e in dd_))
    gmsh.finalize()
    json.dump(info, open(f"{ordner}/netzinfo.json", "w"), indent=1)
    subprocess.run(["ElmerGrid", "14", "2", "netz.msh", "-autoclean"], cwd=ordner, check=True, capture_output=True)
    return ordner, info

if __name__ == "__main__":
    v = sys.argv[1]; f = int(sys.argv[2]) if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else 1
    spalt = "--bodenspalt" in sys.argv
    o, i = netz(v, f, spalt, name=v + ("_spalt" if spalt else ""))
    print(o); print(json.dumps(i, indent=1))
