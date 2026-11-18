# KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. Auftrag G2-D (cad/zelle/AUFTRAG_DETAIL.md).
"""Detailliertes Zellmodell (Innenaufbau) in FreeCAD, headless.
Aufruf: ZELLE_VARIANTE=LFP|NMC [ZELLE_PARAMETER=datei] [ZELLE_AUSGABE=ordner] $FREECAD_APPIMAGE freecadcmd cad/zelle/zelle_detail.py
Maße NUR aus cad/zelle/entwurf/parameter_<V>_entwurf.json (Akten ENT-015, 024, 031..080; Fahnenbreite LFP aus aufbau_W20.json).
Alles, was dort nicht steht, ist ANNAHME (A_*, oben) und wird im Bild als Annahme genannt.
Koordinaten LFP: X Länge (Anode x=0, Kathode/Plus x=L, wie zelle.py), Y Breite, Z Dicke. NMC: Z = Achse, Boden z=0.
Ausgaben nach entwurf/detail/: zelle_<V>_detail.FCStd/.step, ergebnis_detail_<V>.json, render/*.obj (Sätze voll, schnitt, ende, lagen)."""
import os, json, math
import FreeCAD, Part
from FreeCAD import Vector as V

# ---------------- ANNAHMEN (keine Akte, keine Quelle) ----------------
A_POL_D, A_POL_H = 10.0, 3.0              # LFP-Pol: wie zelle.py
A_PET_FOLIE_MM = 0.05                     # PET-Außenfolie LFP, Dicke
A_BEUTEL_MM = 0.10                        # Isolationsbeutel LFP, Wand
A_BB_DICKE_MM = 1.0                       # Stromschiene LFP, Dicke
A_HALTER_BREITE_MM = 40.0                 # Kunststoffhalter LFP, Breite quer (Y)
A_ORING_R_MM = 1.0                        # O-Ring-Schnurradius LFP
A_VENTIL_D_MM, A_VENTIL_H_MM, A_VENTIL_Y_MM = 8.0, 0.5, 25.0   # LFP-Ventil neben Kathodenpol (Y-Versatz von Mitte)
A_STOPFEN_D_MM, A_STOPFEN_H_MM, A_STOPFEN_Y_MM = 3.0, 1.5, -25.0  # Gummistopfen Füllöffnung, Anodenseite
A_UEBERHOEHUNG = 20.0                     # nur Lagenmodell (Schichtdicken x20, Darstellung, keine Messung)
A_NMC_POL_D, A_NMC_POL_H = 12.0, 1.0      # wie zelle.py
A_NMC_RAND_MM = 0.3                       # gefalteter Rand (Ringscheibe) oben/unten, Dicke
A_NMC_TABSCHEIBE_MM = 0.3                 # Tab-Scheibe Dicke
A_NMC_TABSCHEIBE_R = 21.0                 # Tab-Scheibe Außenradius
A_NMC_TAB_SEKTOR_GRAD = 50.0              # 6 Dreiecksflächen je 50 Grad (Lücke 10 Grad)
A_NMC_DICHTRING_BREITE, A_NMC_DICHTRING_H = 2.0, 1.0   # Dichtring am Deckelrand
A_NMC_DECKEL_MM = 0.4                     # Deckeldicke
A_NMC_ISOLIERRING_H = 0.7                 # Anoden-Kathoden-Isolation (Ring) Dicke
A_NMC_POST_D = 4.0                        # Verbindung Tab-Scheibe - Pluspol
A_NMC_NIET_D = 8.0                        # Cu-Blindniet Ø
A_NMC_NIET_H = 0.5                        # Überstand Blindniet außen
A_NMC_VENTIL_D, A_NMC_VENTIL_X = 10.0, 12.0   # Bodenventil Ø und Versatz von der Achse
A_NMC_KLEBE_H, A_NMC_KLEBE_DICKE = 8.0, 0.05  # Klebestreifen Höhe und Dicke
A_NMC_BAND_START_VERSATZ_MM = 0.0         # Start-/Endversatz der Bänder (Abb. 5B nicht in aufbau_W20.json): alle Bänder beginnen gemeinsam am Kern
A_PUNKTE_JE_WINDUNG = 72                  # Tessellierung der Spirale (numerisch)
A_ENDZONE_FENSTER_MM = 110.0              # LFP: Ausschnitt Endzone für Schnitt/Explosion
R = os.environ.get("BATTERIE", "/home/cae/hermes/batterie")
ENT = f"{R}/cad/zelle/entwurf"

def wert(P, bt, m):
    w = P["parameter"][bt][m]["wert"]
    if w is None: raise SystemExit(f"FEHLT: {bt}/{m} (Auftrag: zurück an Opus)")
    return float(w)

def box(x0, x1, y0, y1, z0, z1): return Part.makeBox(x1 - x0, y1 - y0, z1 - z0, V(x0, y0, z0))
def comp(l): return Part.makeCompound(list(l))

# ======================= LFP =======================
def lfp(P, W):
    wand = wert(P, "BT-120", "wandstaerke_mm"); L, B, D = (wert(P, "BT-100", k) for k in ("laenge_mm", "breite_mm", "dicke_mm"))
    ks = ("laenge_mm", "breite_mm", "beschichtung_um", "folie_um", "anzahl", "fahne_mm")
    k = {m: wert(P, "BT-111", m) for m in ks}; a = {m: wert(P, "BT-112", m) for m in ks}
    s = {m: wert(P, "BT-113", m) for m in ("laenge_mm", "breite_mm", "dicke_um", "lagen")}
    kf_breit = W["LFP_original"]["kathode"]["fahne_mm"][0][0]; af_breit = W["LFP_original"]["anode"]["fahne_mm"][0][0]  # 27,1 / 20,5 (Abb.5A, Deutung als Fahnenbreite unsicher)
    um = 1e-3
    tk_c, tk_f, ta_c, ta_f, ts = k["beschichtung_um"]*um, k["folie_um"]*um, a["beschichtung_um"]*um, a["folie_um"]*um, s["dicke_um"]*um
    nK, nA, nS = int(k["anzahl"]), int(a["anzahl"]), int(s["lagen"])
    t_K, t_A = 2*tk_c + tk_f, 2*ta_c + ta_f
    stapel = nK*t_K + nA*t_A + nS*ts
    innen_d = D - 2*wand; rest = innen_d - stapel
    xc, yc, zc = L/2, B/2, D/2
    z0 = zc - stapel/2
    G = {n: [] for n in ("Kathode_Beschichtung", "Al_Folie", "Anode_Beschichtung", "Cu_Folie", "Separator", "Separator_Falz")}
    folge = ["S"]            # S A S C S A S ... A S
    for i in range(nK): folge += ["A", "S", "C", "S"]
    folge += ["A", "S"]
    if folge.count("A") != nA or folge.count("S") != nS: raise SystemExit(f"Lagenzahl passt nicht: A {folge.count('A')} (Akte {nA}), S {folge.count('S')} (Akte {nS}) -> OPUS")
    z = z0; zS = []; elek = []
    for t in folge:
        if t == "S":
            G["Separator"].append(box(xc - s["laenge_mm"]/2, xc + s["laenge_mm"]/2, yc - s["breite_mm"]/2, yc + s["breite_mm"]/2, z, z + ts)); zS.append((z, z + ts)); z += ts
        elif t == "C":
            x0, x1 = xc - k["laenge_mm"]/2, xc + k["laenge_mm"]/2; y0, y1 = yc - k["breite_mm"]/2, yc + k["breite_mm"]/2
            G["Kathode_Beschichtung"] += [box(x0, x1, y0, y1, z, z + tk_c), box(x0, x1, y0, y1, z + tk_c + tk_f, z + t_K)]
            G["Al_Folie"] += [box(x0, x1, y0, y1, z + tk_c, z + tk_c + tk_f), box(x1, x1 + k["fahne_mm"], yc - kf_breit/2, yc + kf_breit/2, z + tk_c, z + tk_c + tk_f)]
            elek.append("C"); z += t_K
        else:
            x0, x1 = xc - a["laenge_mm"]/2, xc + a["laenge_mm"]/2; y0, y1 = yc - a["breite_mm"]/2, yc + a["breite_mm"]/2
            G["Anode_Beschichtung"] += [box(x0, x1, y0, y1, z, z + ta_c), box(x0, x1, y0, y1, z + ta_c + ta_f, z + t_A)]
            G["Cu_Folie"] += [box(x0, x1, y0, y1, z + ta_c, z + ta_c + ta_f), box(x0 - a["fahne_mm"], x0, yc - af_breit/2, yc + af_breit/2, z + ta_c, z + ta_c + ta_f)]
            elek.append("A"); z += t_A
    stapel_z1 = z
    # Z-Faltung: Falzbogen vereinfacht als senkrechtes Band (Dicke ts); um Anoden rechts, um Kathoden links (Fahnen auf der Gegenseite)
    sx0, sx1 = xc - s["laenge_mm"]/2, xc + s["laenge_mm"]/2
    for i in range(len(zS) - 1):
        rechts = (elek[i] == "A")
        G["Separator_Falz"].append(box(sx1 - ts, sx1, yc - s["breite_mm"]/2, yc + s["breite_mm"]/2, zS[i][0], zS[i + 1][1]) if rechts
                                   else box(sx0, sx0 + ts, yc - s["breite_mm"]/2, yc + s["breite_mm"]/2, zS[i][0], zS[i + 1][1]))
    xk_tip = xc + k["laenge_mm"]/2 + k["fahne_mm"]       # Kathodenfahne (Plus, x groß)
    xa_tip = xc - a["laenge_mm"]/2 - a["fahne_mm"]       # Anodenfahne (Minus, x klein)
    bbK = box(xk_tip, xk_tip + A_BB_DICKE_MM, yc - kf_breit/2, yc + kf_breit/2, z0, stapel_z1)
    bbA = box(xa_tip - A_BB_DICKE_MM, xa_tip, yc - af_breit/2, yc + af_breit/2, z0, stapel_z1)
    polK = Part.makeCylinder(A_POL_D/2, (L + A_POL_H) - (xk_tip + A_BB_DICKE_MM), V(xk_tip + A_BB_DICKE_MM, yc, zc), V(1, 0, 0))
    polA = Part.makeCylinder(A_POL_D/2, (xa_tip - A_BB_DICKE_MM) + A_POL_H, V(-A_POL_H, yc, zc), V(1, 0, 0))
    bz0, bz1 = wand + A_BEUTEL_MM, D - wand - A_BEUTEL_MM
    hy0, hy1 = yc - A_HALTER_BREITE_MM/2, yc + A_HALTER_BREITE_MM/2
    def halter(xa_, xb_):
        loch = Part.makeCylinder(A_POL_D/2, xb_ - xa_, V(xa_, yc, zc), V(1, 0, 0))
        return box(xa_, xb_, hy0, hy1, bz0, zc).cut(loch), box(xa_, xb_, hy0, hy1, zc, bz1).cut(loch)
    hK = halter(xk_tip + A_BB_DICKE_MM, L - wand); hA = halter(wand, xa_tip - A_BB_DICKE_MM)
    beutel = box(wand, L - wand, wand, B - wand, wand, D - wand).cut(box(wand - 1, L - wand + 1, wand + A_BEUTEL_MM, B - wand - A_BEUTEL_MM, wand + A_BEUTEL_MM, D - wand - A_BEUTEL_MM))
    gh = box(0, L, 0, B, 0, D).cut(box(wand, L - wand, wand, B - wand, wand, D - wand))
    r_loch = A_POL_D/2 + A_ORING_R_MM*2
    for x in (0, L - wand):
        gh = gh.cut(Part.makeCylinder(r_loch, wand, V(x, yc, zc), V(1, 0, 0)))
    gh = gh.cut(Part.makeCylinder(A_STOPFEN_D_MM/2, wand, V(0, yc + A_STOPFEN_Y_MM, zc), V(1, 0, 0)))
    oringe = [Part.makeTorus(A_POL_D/2 + A_ORING_R_MM, A_ORING_R_MM, V(wand/2, yc, zc), V(1, 0, 0)),
              Part.makeTorus(A_POL_D/2 + A_ORING_R_MM, A_ORING_R_MM, V(L - wand/2, yc, zc), V(1, 0, 0))]
    pet = box(0, L, -A_PET_FOLIE_MM, B + A_PET_FOLIE_MM, -A_PET_FOLIE_MM, D + A_PET_FOLIE_MM).cut(box(-1, L + 1, 0, B, 0, D))
    ventil = Part.makeCylinder(A_VENTIL_D_MM/2, A_VENTIL_H_MM, V(L, yc + A_VENTIL_Y_MM, zc), V(1, 0, 0))
    stopfen = Part.makeCylinder(A_STOPFEN_D_MM/2, A_STOPFEN_H_MM, V(wand - A_STOPFEN_H_MM, yc + A_STOPFEN_Y_MM, zc), V(1, 0, 0))
    gruppen = {k_: comp(v) for k_, v in G.items()}
    gruppen.update({"Stromschiene_Al_Kathode": bbK, "Stromschiene_Cu_Anode": bbA, "Pol_plus_Al": polK, "Pol_minus_Cu": polA,
                    "Halter_Kathode": comp(hK), "Halter_Anode": comp(hA), "Isolationsbeutel": beutel, "Gehaeuse_Al": gh,
                    "O_Ringe": comp(oringe), "PET_Folie": pet, "Ventil": ventil, "Stopfen": stopfen})
    # Lagenmodell (Dicke x A_UEBERHOEHUNG) als eigener Satz
    lm = {n: [] for n in ("Kathode_Beschichtung", "Al_Folie", "Anode_Beschichtung", "Cu_Folie", "Separator")}
    f = A_UEBERHOEHUNG; zz = 0.0; lx, ly = 16.0, 12.0
    for t in ["S", "A", "S", "C", "S", "A", "S"]:
        if t == "S": lm["Separator"].append(box(0, lx, 0, ly, zz, zz + ts*f)); zz += ts*f
        elif t == "C":
            lm["Kathode_Beschichtung"] += [box(0, lx - 2, 0, ly, zz, zz + tk_c*f), box(0, lx - 2, 0, ly, zz + (tk_c + tk_f)*f, zz + t_K*f)]
            lm["Al_Folie"].append(box(0, lx + 3, 0, ly, zz + tk_c*f, zz + (tk_c + tk_f)*f)); zz += t_K*f
        else:
            lm["Anode_Beschichtung"] += [box(0, lx - 1, 0, ly, zz, zz + ta_c*f), box(0, lx - 1, 0, ly, zz + (ta_c + ta_f)*f, zz + t_A*f)]
            lm["Cu_Folie"].append(box(-3, lx - 1, 0, ly, zz + ta_c*f, zz + (ta_c + ta_f)*f)); zz += t_A*f
    lagen = {n: comp(v) for n, v in lm.items() if v}
    wf = A_ENDZONE_FENSTER_MM
    fenster_ende = box(L - wf, L + A_POL_H + 1, -1, B + 1, -1, D + 1)
    fenster_schnitt = box(L - wf, L + A_POL_H + 1, -1, yc, -1, D + 1)
    ergebnis = {
        "variante": "LFP",
        "stapel": {"kathoden": nK, "anoden": nA, "separatorlagen": nS, "dicke_kathode_mm": t_K, "dicke_anode_mm": t_A, "dicke_separator_mm": ts,
                   "stapeldicke_mm": stapel, "innendicke_mm": innen_d, "rest_zur_innendicke_mm": rest,
                   "rest_nach_beutel_mm": innen_d - 2*A_BEUTEL_MM - stapel, "stapel_z_von_bis_mm": [z0, stapel_z1]},
        "laengen_mm": {"zelle": L, "separator": s["laenge_mm"], "endzone_je_seite_ab_separator": (L - 2*wand - s["laenge_mm"])/2,
                       "fahnenspitze_kathode_x": xk_tip, "fahnenspitze_anode_x": xa_tip,
                       "innen_platz_stromschiene_bis_wand_kathode": (L - wand) - (xk_tip + A_BB_DICKE_MM),
                       "innen_platz_stromschiene_bis_wand_anode": (xa_tip - A_BB_DICKE_MM) - wand},
        "fahnenbreite_aus_aufbau_W20_mm": {"kathode": kf_breit, "anode": af_breit, "hinweis": "Abb.5A, Deutung als Breite unsicher"},
        "annahmen": {n: v for n, v in globals().items() if n.startswith("A_") and not n.startswith("A_NMC") and n != "A_PUNKTE_JE_WINDUNG"},
        "nicht_modelliert": ["Isolierrand Kathode 6,5 mm (BT-114)", "Klebeband/Kunststoffschiene BT-116", "Faltbögen nur als gerades Band", "Fahnen nicht zu Bündeln verdichtet"],
        "volumen_je_teil_cm3": {n: s_.Volume/1e3 for n, s_ in gruppen.items()},
    }
    return gruppen, lagen, fenster_ende, fenster_schnitt, ergebnis

# ======================= NMC =======================
def nmc(P, W):
    wand = wert(P, "BT-120", "wandstaerke_mm"); Dm, H = wert(P, "BT-100", "durchmesser_mm"), wert(P, "BT-100", "hoehe_mm")
    ks = ("laenge_mm", "breite_mm", "beschichtung_um", "folie_um", "fahne_mm")
    k = {m: wert(P, "BT-111", m) for m in ks}; a = {m: wert(P, "BT-112", m) for m in ks}
    s = {m: wert(P, "BT-113", m) for m in ("laenge_mm", "breite_mm", "dicke_um")}
    kern_d = wert(P, "BT-115", "durchmesser_mm"); um = 1e-3
    Rm = Dm/2; Rin = Rm - wand; r0 = kern_d/2
    tkc, tkf, tac, taf, ts = k["beschichtung_um"]*um, k["folie_um"]*um, a["beschichtung_um"]*um, a["folie_um"]*um, s["dicke_um"]*um
    tK, tA = 2*tkc + tkf, 2*tac + taf
    pitch = tK + tA + 2*ts   # nur Anzeige: Steigung solange alle vier Bänder vorhanden sind
    zW0 = wand + A_NMC_RAND_MM + A_NMC_TABSCHEIBE_MM; zW1 = zW0 + s["breite_mm"]
    zK = (zW0 + (s["breite_mm"] - k["breite_mm"])/2, zW0 + (s["breite_mm"] + k["breite_mm"])/2)
    zA = (zW0 + (s["breite_mm"] - a["breite_mm"])/2, zW0 + (s["breite_mm"] + a["breite_mm"])/2)
    # Flächentreue Spirale: R(theta) = Außenradius des Wickels mit pi*(R^2 - r0^2) = Summe (Dicke x Länge) aller bisher gewickelten Bänder.
    # Bänder (von innen): K, S1, A, S2, alle beginnen bei theta=0 am Kern (A_NMC_BAND_START_VERSATZ_MM = 0); Innenradius eines Bandes = R - Dicke aller Bänder von ihm nach außen (einschließlich).
    BANDER = [("K", tK, k["laenge_mm"]), ("S1", ts, s["laenge_mm"]), ("A", tA, a["laenge_mm"]), ("S2", ts, s["laenge_mm"])]
    NS = 720; dth = 2*math.pi/NS
    R_ = r0 + 1e-9; th = 0.0; arc = {n: 0.0 for n, _, _ in BANDER}; ende = {}; spur = {n: [] for n, _, _ in BANDER}; r_min_innen = 1e9; R_max = 0.0
    while len(ende) < len(BANDER):
        pres = [(n, tt, LL) for n, tt, LL in BANDER if n not in ende]; aussen = 0.0; dArea = 0.0; neu = []
        for n, tt, LL in reversed(pres):
            aussen += tt; rin = R_ - aussen; ds = (rin + tt/2)*dth; f = 1.0
            spur[n].append((th, rin))
            if arc[n] + ds >= LL:
                f = (LL - arc[n])/ds; ende[n] = th + f*dth; spur[n].append((th + f*dth, rin + (R_ - aussen - rin)))
            arc[n] += ds*f; dArea += tt*ds*f; r_min_innen = min(r_min_innen, rin); R_max = max(R_max, rin + tt)
        R_ += dArea/(2*math.pi*R_); th += dth
    def band(n, off, tt, z0, z1):
        sp = spur[n]; idx = list(range(0, len(sp) - 1, NS//A_PUNKTE_JE_WINDUNG)) + [len(sp) - 1]
        ri = [sp[i][1] + off for i in idx]; ths = [sp[i][0] for i in idx]; ro = [r + tt for r in ri]
        pts = [V(r*math.cos(q), r*math.sin(q), z0) for r, q in zip(ri, ths)] + [V(r*math.cos(q), r*math.sin(q), z0) for r, q in zip(reversed(ro), reversed(ths))]
        pts.append(pts[0])
        return Part.Face(Part.makePolygon(pts)).extrude(V(0, 0, z1 - z0))
    thK, thA, thS1, thS2 = ende["K"], ende["A"], ende["S1"], ende["S2"]
    G = {}
    G["Kathode_Beschichtung"] = comp([band("K", 0, tkc, *zK), band("K", tkc + tkf, tkc, *zK)])
    G["Al_Folie"] = band("K", tkc, tkf, *zK)
    G["Anode_Beschichtung"] = comp([band("A", 0, tac, *zA), band("A", tac + taf, tac, *zA)])
    G["Cu_Folie"] = band("A", tac, taf, *zA)
    G["Separator"] = comp([band("S1", 0, ts, zW0, zW1), band("S2", 0, ts, zW0, zW1)])
    def r_ende(n): return spur[n][-1][1] + dict((x[0], x[1]) for x in BANDER)[n]
    R_w = R_max
    def rin_bei(n, th_x):   # Innenradius des Bandes n beim Winkel th_x (lineare Interpolation der Spur)
        sp = spur[n]
        for (t0, r_a), (t1, r_b) in zip(sp, sp[1:]):
            if t0 <= th_x <= t1 and t1 > t0: return r_a + (r_b - r_a)*(th_x - t0)/(t1 - t0)
        return None
    th_probe = 2*math.pi*32.5
    lagen_probe = {n: rin_bei(n, th_probe) for n, _, _ in BANDER}
    becher = Part.makeCylinder(Rm, H).cut(Part.makeCylinder(Rin, H - wand, V(0, 0, wand)))
    zO = zW1
    def ring(r_a, r_i, h, z): return Part.makeCylinder(r_a, h, V(0, 0, z)).cut(Part.makeCylinder(r_i, h, V(0, 0, z)))
    rand_u = ring(min(R_w, Rin), r0, A_NMC_RAND_MM, wand); rand_o = ring(min(R_w, Rin), r0, A_NMC_RAND_MM, zO)
    def tabscheibe(z):
        teile = [Part.makeCylinder(5.0, A_NMC_TABSCHEIBE_MM, V(0, 0, z))]
        for i in range(6):
            a1 = math.radians(60*i - A_NMC_TAB_SEKTOR_GRAD/2); a2 = math.radians(60*i + A_NMC_TAB_SEKTOR_GRAD/2)
            pts = [V(0, 0, z), V(A_NMC_TABSCHEIBE_R*math.cos(a1), A_NMC_TABSCHEIBE_R*math.sin(a1), z), V(A_NMC_TABSCHEIBE_R*math.cos(a2), A_NMC_TABSCHEIBE_R*math.sin(a2), z), V(0, 0, z)]
            teile.append(Part.Face(Part.makePolygon(pts)).extrude(V(0, 0, A_NMC_TABSCHEIBE_MM)))
        return comp(teile)
    tab_u = tabscheibe(wand + A_NMC_RAND_MM)
    z_tab_o = zO + A_NMC_RAND_MM; tab_o = tabscheibe(z_tab_o); z_tab_o_top = z_tab_o + A_NMC_TABSCHEIBE_MM
    z_dk_u = H - A_NMC_DICHTRING_H; z_dk_o = z_dk_u + A_NMC_DECKEL_MM
    dichtring = ring(Rin, Rin - A_NMC_DICHTRING_BREITE, A_NMC_DICHTRING_H, z_dk_u)
    deckel = Part.makeCylinder(Rin - A_NMC_DICHTRING_BREITE, A_NMC_DECKEL_MM, V(0, 0, z_dk_u))
    pluspol = Part.makeCylinder(A_NMC_POL_D/2, A_NMC_POL_H + (H - z_dk_o), V(0, 0, z_dk_o)).fuse(Part.makeCylinder(A_NMC_POST_D/2, z_dk_u - z_tab_o_top, V(0, 0, z_tab_o_top)))
    isolierring = ring(Rin, A_NMC_TABSCHEIBE_R, A_NMC_ISOLIERRING_H, z_tab_o_top)
    niet = Part.makeCylinder(A_NMC_NIET_D/2, wand + A_NMC_NIET_H, V(0, 0, -A_NMC_NIET_H))
    ventil = Part.makeCylinder(A_NMC_VENTIL_D/2, 0.2, V(A_NMC_VENTIL_X, 0, -0.2))
    ro_kl = min(R_w, Rin)
    klebe = comp([ring(ro_kl + A_NMC_KLEBE_DICKE, ro_kl, A_NMC_KLEBE_H, zW0), ring(ro_kl + A_NMC_KLEBE_DICKE, ro_kl, A_NMC_KLEBE_H, zW1 - A_NMC_KLEBE_H)])
    G.update({"Becher_Stahl": becher, "Rand_Al_oben": rand_o, "Rand_Cu_unten": rand_u, "TabScheibe_Al_Kathode": tab_o, "TabScheibe_Cu_Anode": tab_u,
              "Dichtring": dichtring, "Deckel": deckel, "Pol_plus_Al": pluspol, "Isolierring": isolierring, "Blindniet_Cu": niet, "Ventil": ventil, "Klebestreifen": klebe})
    render = dict(G)   # Wickel am Becher-Innenzylinder geschnitten (nur Darstellung)
    if R_w > Rin:
        zyl = Part.makeCylinder(Rin, H)
        for n in ("Kathode_Beschichtung", "Al_Folie", "Anode_Beschichtung", "Cu_Folie", "Separator"):
            render[n] = comp([x.common(zyl) for x in G[n].Solids])
    f_viertel = box(-Rm - 2, Rm + 2, -Rm - 2, Rm + 2, -2, H + 3).cut(box(0, Rm + 2, 0, Rm + 2, -3, H + 4))
    f_oben = box(-Rm - 2, Rm + 2, -Rm - 2, Rm + 2, -2, (zW0 + zW1)/2)
    ergebnis = {
        "variante": "NMC",
        "wickel": {"kern_radius_mm": r0, "modell": "flaechentreu (pi*(R^2-r0^2) = Summe Dicke x Laenge), Baender gemeinsam am Kern", "dicke_je_windung_voll_mm": pitch, "windungen_kathode": thK/(2*math.pi), "windungen_anode": thA/(2*math.pi),
                   "windungen_separator1": thS1/(2*math.pi), "windungen_separator2": thS2/(2*math.pi),
                   "aussenradius_kathode_mm": r_ende("K"), "aussenradius_anode_mm": r_ende("A"),
                   "aussenradius_separator_mm": max(r_ende("S1"), r_ende("S2")),
                   "aussenradius_wickel_max_mm": R_w, "aussenradius_flaechenformel_mm": math.sqrt(r0**2 + (tK*k["laenge_mm"] + tA*a["laenge_mm"] + 2*ts*s["laenge_mm"])/math.pi),
                   "kleinster_innenradius_mm": r_min_innen, "innenradius_je_band_bei_32,5_windungen_mm": lagen_probe, "becher_innenradius_mm": Rin, "abstand_wickel_zu_becher_mm": Rin - R_w,
                   "hoehe_z_von_bis_mm": [zW0, zW1], "freie_hoehe_oben_bis_deckel_mm": z_dk_u - z_tab_o_top},
        "annahmen": {n: v for n, v in globals().items() if n.startswith("A_NMC") or n == "A_PUNKTE_JE_WINDUNG"},
        "nicht_modelliert": ["Foliensteg der Fahnen (5 / 7,5 mm) einzeln: durch Ringscheibe 'gefalteter Rand' angedeutet (ANNAHME Dicke)", "Elektrolyt", "Deckel nur als Scheibe, Sicken und Bördelung fehlen"],
        "darstellung": "Satz render: Wickel mit Becher-Innenzylinder geschnitten, weil der Wickel (aus Akten) den Becher überragt. Volumina sind die ungeschnittenen." if R_w > Rin else "Wickel passt in den Becher",
        "volumen_je_teil_cm3": {n: s_.Volume/1e3 for n, s_ in G.items()},
    }
    return G, render, f_viertel, f_oben, ergebnis

def obj(pfad, name, shape, tol=0.02):
    pts, tri = shape.tessellate(tol)
    with open(pfad, "w") as f:
        f.write(f"# KI-generiert, Entwurf, mm, {name}\n")
        for p in pts: f.write(f"v {p.x:.5f} {p.y:.5f} {p.z:.5f}\n")
        for t in tri: f.write(f"f {t[0]+1} {t[1]+1} {t[2]+1}\n")
    return len(pts), len(tri)

def schneiden(shape, fenster):
    teile = [x.common(fenster) for x in (shape.Solids or [shape])]
    teile = [t for t in teile if not t.isNull() and t.Volume > 1e-9]
    return comp(teile) if teile else None

def main():
    var = os.environ.get("ZELLE_VARIANTE")
    if var not in ("LFP", "NMC"): raise SystemExit("ZELLE_VARIANTE=LFP|NMC setzen")
    pf = os.environ.get("ZELLE_PARAMETER") or f"{ENT}/parameter_{var}_entwurf.json"
    out = os.environ.get("ZELLE_AUSGABE") or f"{ENT}/detail"; rd = f"{out}/render"; os.makedirs(rd, exist_ok=True)
    P = json.load(open(pf)); W = json.load(open(f"{R}/cad/zelle/aufbau_W20.json"))
    doc = FreeCAD.newDocument(f"zelle_{var}_detail")
    if var == "LFP":
        G, extra, f1, f2, erg = lfp(P, W)
        sets = {"voll": (G, None), "ende": (G, f1), "schnitt": (G, f2), "lagen": (extra, None)}
    else:
        G, render, f1, f2, erg = nmc(P, W)
        sets = {"voll": (render, None), "viertel": (render, f1), "oben": (render, f2)}
    for n, s in G.items():
        doc.addObject("Part::Feature", n).Shape = s
    doc.recompute()
    doc.saveAs(f"{out}/zelle_{var}_detail.FCStd")
    Part.export(list(doc.Objects), f"{out}/zelle_{var}_detail.step")
    erg["gueltig"] = {n: bool(s.isValid()) for n, s in G.items()}
    erg["obj"] = {}
    for sn, (gr, fen) in sets.items():
        for n, s in gr.items():
            sh = s if fen is None else schneiden(s, fen)
            if sh is None: continue
            erg["obj"][f"{sn}_{n}"] = obj(f"{rd}/{var}_{sn}_{n}.obj", f"{var} {sn} {n}", sh)
    json.dump(erg, open(f"{out}/ergebnis_detail_{var}.json", "w"), indent=1, ensure_ascii=False)
    print("FERTIG", var)
main()
