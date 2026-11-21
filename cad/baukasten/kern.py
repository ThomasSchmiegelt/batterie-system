# KI-generiert (Claude Opus, 2026-11-19), Entwurf. G5.2 (cad/baukasten/PLAN.md §3).
"""Kern des Geometrie-Baukastens: Parameterzugriff, Registry der Generatoren, Teil-Objekt, Formhelfer.

Datenfluss:  Akten → cad/pack/entwurf/parameter_<V>_e2d.json ("parameter": entschieden + vorgeschlagen)  → p(bt, merkmal)
             cad/baukasten/annahmen.json (G5.1, Sonnet) und annahmen_g5.json (Opus, neue Detailmaße)    → a(name)
             Stückliste pm/bauteile/stueckliste_<V>.json (SL3)                                            → montage.py
Regel: Jede Länge im Teilecode kommt aus p() oder a(). Zahlen im Code nur als 0, 1, 2, π oder Zähler.
Koordinaten mm: X Länge (0 = Vorderkante Gehäuse), Y Breite (0 = linke Außenkante), Z Höhe (0 = Unterkante Unterfahrschutz).
Läuft nur in FreeCAD (freecadcmd); der Parameterteil (p, a, Registry) auch in normalem Python (ohne Part).
"""
import os, json, math
from pathlib import Path

ROOT = Path(os.environ.get("BATTERIE", "/home/cae/hermes/batterie"))
HIER = ROOT / "cad/baukasten"
VAR = os.environ.get("PACK_VARIANTE", "LFP")
try:
    import FreeCAD, Part
    from FreeCAD import Vector as V
except ImportError:          # Parameterprüfung ohne FreeCAD
    FreeCAD = Part = None
    V = lambda *x: x

# ---------------------------------------------------------------- Parameter
_PJ = json.load(open(ROOT / f"cad/pack/entwurf/parameter_{VAR}_e2d.json", encoding="utf-8"))   # nur noch für den A-Block (Altbestand)

def _akten_lesen():
    """Akten direkt aus pm/entscheidungen (entschieden + vorgeschlagen, ersetzte fallen weg, Variantenakten überschreiben
    allgemeine) – gleiche Regel wie cad/pack/entwurf_parameter.py, aber immer aktuell (z. B. ENT-152 ersetzt ENT-090)."""
    import sys as _s; _s.path.insert(0, str(ROOT / "pm")); import pm as PM
    ok = lambda e: (str(e.get("status", "")).startswith(("entschieden", "vorgeschlagen"))) and e.get("merkmal") not in (None, "-")
    alle = PM.alle(); ers = {e.get("ersetzt") for e in alle}; akten = [e for e in alle if ok(e) and e["id"] not in ers]
    out = {b: {m: {"wert": None, "entscheidung": None} for m in d["merkmale"]} for b, d in PM.struktur().items()}
    for gruppe in (False, True):
        for e in akten:
            if bool(e.get("variante")) != gruppe or (gruppe and VAR not in PM.vset(e)): continue
            for b in e.get("bauteile") or []:
                out.setdefault(b, {})[e["merkmal"]] = {"wert": e.get("wert"), "einheit": e.get("einheit"), "entscheidung": e["id"], "status": e.get("status")}
    return out
_P = _akten_lesen()
_A = {}
for quelle in (_PJ.get("A", {}), HIER / "annahmen.json", HIER / "annahmen_g5.json", HIER / "annahmen_datenblatt.json"):   # spätere Quelle überschreibt frühere
    d = quelle if isinstance(quelle, dict) else (json.load(open(quelle, encoding="utf-8")) if quelle.exists() else {})
    for k, v in d.items():
        if k.startswith("_"): continue
        w = v.get("wert") if isinstance(v, dict) else v
        if isinstance(w, dict) and VAR in w: w = w[VAR]      # Wert je Variante
        if isinstance(v, dict) and v.get("varianten") and VAR not in v["varianten"]: continue
        _A[k] = w
GENUTZT = {"p": set(), "a": set()}   # für den Prüfbericht: welche Akten/Annahmen hat ein Lauf gelesen

def p(bt, merkmal, roh=False):
    """Wert aus einer Akte (entschieden oder vorgeschlagen). Fehlt er, bricht der Lauf ab (kein stiller Ersatzwert)."""
    e = _P.get(bt, {}).get(merkmal)
    if e is None or e.get("wert") is None:
        raise SystemExit(f"FEHLT Akte: {bt}/{merkmal} (Variante {VAR})")
    GENUTZT["p"].add(f"{bt}/{merkmal} ← {e.get('entscheidung')}")
    w = e["wert"]
    return w if roh or not isinstance(w, (int, float)) else float(w)

def a(name):
    """Detailmaß ohne eigene Akte (Herkunft steht in annahmen*.json bzw. im A-Block). Fehlt es, bricht der Lauf ab."""
    if name not in _A:
        raise SystemExit(f"FEHLT Annahme: {name} (Variante {VAR}) → in annahmen_g5.json mit Herkunft eintragen")
    GENUTZT["a"].add(name)
    w = _A[name]
    return [float(x) for x in w] if isinstance(w, list) else (float(w) if isinstance(w, (int, float)) else w)

def hat_a(name): return name in _A

# ---------------------------------------------------------------- Werkstoffe und Farben
FARBEN = json.load(open(HIER / "farben.json", encoding="utf-8"))

def dichte_kg_mm3(werkstoff):
    """Dichte aus farben.json["werkstoffe"] (kg/m³ → kg/mm³). None, wenn unbekannt (Masse dann aus der Stückliste)."""
    w = FARBEN["werkstoffe"].get(werkstoff)
    return None if w is None or w.get("dichte_kg_m3") is None else w["dichte_kg_m3"] * 1e-9

# ---------------------------------------------------------------- Teil und Registry
class Teil:
    """Ein Körper im Modell. pos = Stücklistenposition (wird von montage.py gesetzt), bt = Bauteil."""
    __slots__ = ("name", "bt", "pos", "shape", "werkstoff", "farbe", "masse_kg", "masse_quelle")
    def __init__(self, name, shape, werkstoff, farbe=None, masse_kg=None, bt=None):
        self.name, self.shape, self.werkstoff = name, shape, werkstoff
        self.farbe = farbe or FARBEN["werkstoffe"].get(werkstoff, {}).get("farbe", "grau")
        self.bt, self.pos = bt, None
        if masse_kg is not None:
            self.masse_kg, self.masse_quelle = masse_kg, "Akte/Stückliste"
        else:
            rho = dichte_kg_mm3(werkstoff)
            self.masse_kg = None if rho is None else shape.Volume * rho
            self.masse_quelle = "CAD-Volumen" if rho else "offen"
    def verschoben(self, dx=0, dy=0, dz=0, name=None):
        s = self.shape.copy(); s.translate(V(dx, dy, dz))
        t = Teil(name or self.name, s, self.werkstoff, self.farbe, None, self.bt)
        t.masse_kg, t.masse_quelle = self.masse_kg, self.masse_quelle
        return t

REGISTRY = {}   # "modul.funktion" → Funktion(ctx) → list[Teil]

def teil(name, bt, stufe):
    """Dekorator: meldet einen Generator an. stufe K/F/H wie PLAN §3. Der Docstring der Funktion geht in den Katalog."""
    def reg(f):
        f.g5 = dict(name=name, bt=bt, stufe=stufe)
        REGISTRY[name] = f
        return f
    return reg

# ---------------------------------------------------------------- Formhelfer
def quader(x0, y0, z0, x1, y1, z1):
    """Achsparalleler Quader zwischen zwei Ecken."""
    return Part.makeBox(x1 - x0, y1 - y0, z1 - z0, V(x0, y0, z0))

def quader_r(x0, y0, z0, x1, y1, z1, r, kanten="z"):
    """Quader mit gerundeten Kanten. kanten = "z" (senkrechte Kanten), "alle". r wird auf < halbe kleinste Kante begrenzt."""
    s = quader(x0, y0, z0, x1, y1, z1)
    r = min(r, 0.49 * min(x1 - x0, y1 - y0, z1 - z0))
    if r <= 0: return s
    if kanten == "z":
        es = [e for e in s.Edges if abs(e.Vertexes[0].Point.z - e.Vertexes[1].Point.z) > 1e-6]
    else:
        es = s.Edges
    return s.makeFillet(r, es)

def fase(shape, d, auswahl=None):
    """Fase an allen (oder ausgewählten) Kanten."""
    return shape.makeChamfer(d, auswahl or shape.Edges)

def zylinder(r, h, x, y, z, achse="z"):
    """Zylinder, Grundfläche bei (x, y, z), Achse x/y/z."""
    d = {"x": V(1, 0, 0), "y": V(0, 1, 0), "z": V(0, 0, 1)}[achse]
    return Part.makeCylinder(r, h, V(x, y, z), d)

def bohrungen(shape, punkte, r, h, achse="z"):
    """Durchgangsbohrungen an Punkten (x, y, z = Startpunkt), Tiefe h."""
    if not punkte: return shape
    return shape.cut(Part.makeCompound([zylinder(r, h, *pt, achse=achse) for pt in punkte]))

def profil_extrudiert(punkte_2d, laenge, ebene="yz", start=0.0, loecher=()):
    """Strangpressprofil: geschlossener Polygonzug in der Ebene (yz → Extrusion in x, xz → in y), Kammern als weitere Polygone."""
    def flaeche(pts):
        if ebene == "yz": v = [V(start, u, w) for u, w in pts]
        else: v = [V(u, start, w) for u, w in pts]
        return Part.Face(Part.makePolygon(v + [v[0]]))
    f = flaeche(punkte_2d)
    for l in loecher: f = f.cut(flaeche(l))
    vec = V(laenge, 0, 0) if ebene == "yz" else V(0, laenge, 0)
    return f.extrude(vec)

def rechteck(u0, w0, u1, w1): return [(u0, w0), (u1, w0), (u1, w1), (u0, w1)]

def rohr(ra, ri, h, x, y, z, achse="z"):
    """Rohrstück (Hohlzylinder)."""
    return zylinder(ra, h, x, y, z, achse).cut(zylinder(ri, h, x, y, z, achse))

def sechskant(s, h, x, y, z):
    """Sechskant mit Schlüsselweite s (Mutter, Schraubenkopf), Achse z."""
    r = s / math.sqrt(3)
    pts = [V(x + r * math.cos(k * math.pi / 3), y + r * math.sin(k * math.pi / 3), z) for k in range(6)]
    return Part.Face(Part.makePolygon(pts + [pts[0]])).extrude(V(0, 0, h))

def flachkopf(d, k, dk, x, y, z, schaft_l=0.0):
    """Flachkopfschraube (Form ISO 7380, Linsenkopf vereinfacht als flacher Kegelstumpf), Kopf auf z, Schaft nach unten."""
    kopf = Part.makeCone(dk / 2, dk / 2 * 0.6, k, V(x, y, z))
    if schaft_l > 0: kopf = kopf.fuse(zylinder(d / 2, schaft_l, x, y, z - schaft_l))
    return kopf

def setze(shape, placement):
    """Kaufteil aus lokalen Koordinaten an einen Einbauort setzen (Kopie). Lokal: Ursprung = Mitte der Befestigungsfläche,
    +z = Normale der Befestigungsfläche (weg vom Träger), +x = Hauptachse (Richtung der Anschlüsse)."""
    s = shape.copy(); s.Placement = placement.multiply(s.Placement); return s

def einbau(x, y, z, achse_z=(0, 0, 1), drehung_deg=0.0):
    """Placement für einen Einbauort: Punkt, Normale der Befestigungsfläche, Drehung um diese Normale."""
    r = FreeCAD.Rotation(V(0, 0, 1), V(*achse_z)).multiply(FreeCAD.Rotation(V(0, 0, 1), drehung_deg))
    return FreeCAD.Placement(V(x, y, z), r)

def vereinige(shapes):
    s = shapes[0]
    for t in shapes[1:]: s = s.fuse(t)
    return s.removeSplitter() if hasattr(s, "removeSplitter") else s

# ---------------------------------------------------------------- Kontext für die Generatoren
class Ctx:
    """Gemeinsame abgeleitete Maße (Höhenstapel, Gehäuselänge, Feldgrenzen). Ein Ort, damit alle Teile dieselben Ebenen sehen.
    Wird von montage.py einmal je Variante erzeugt und an jeden Generator gegeben."""
    def __init__(self):
        self.var = VAR
        self.B = p("BT-000", "bauraum_breite_mm")
        self.L = p("BT-000", "bauraum_laenge_mm")
        self.rand = a("A_rand_mm")                       # = Seitenrahmenbreite innen bis Zellfeld (M0)
        self.ufs, self.luft, self.bod = a("A_unterfahrschutz_mm"), a("A_luft_mm"), a("A_boden_mm")
        self.kp, self.pad, self.dec = p("BT-610", "dicke_mm"), a("A_pad_mm"), a("A_deckel_mm")   # Plattendicke aus der Akte (ENT-152 statt A_kuehlplatte_mm)
        self.z_boden_ok = self.ufs + self.luft + self.bod          # Oberkante Boden
        self.z_kp_u_ok = self.z_boden_ok + self.kp                 # Oberkante untere Kühlplatte
        self.z_zelle_u = self.z_kp_u_ok + self.pad                 # Zellunterkante
        if VAR == "LFP":
            self.h_zelle = p("BT-100", "breite_mm"); self.h_ueber = 0.0
        else:
            self.h_zelle = p("BT-100", "hoehe_mm")
            ag_d, ag_t = a("A_zellabgriff_NMC_mm"); self.h_ueber = ag_t + p("BT-420", "dicke_mm")
        self.z_zelle_o = self.z_zelle_u + self.h_zelle
        self.z_pad_o_u = self.z_zelle_o + self.h_ueber             # Unterkante oberes Pad
        self.z_kp_o_u = self.z_pad_o_u + self.pad                  # Unterkante obere Kühlplatte
        self.z_deckel_u = self.z_kp_o_u + self.kp
        self.z_deckel_o = self.z_deckel_u + self.dec
        self.z_mitte_zelle = self.z_zelle_u + self.h_zelle / 2
        self.einbau = {}               # BT → [FreeCAD.Placement]: Einbauorte für Kaufteile (Schnittstelle PLAN §3a), gesetzt von schaltbox/gehaeuse/kuehlung
        self.schrauben = []            # Schraubstellen aller Module: dict(typ, d, l, placement[, bt]); normteile.schraube baut sie (G5.4)
        self.schaltbox = {}            # Lagen aus schaltbox.py (hv_eingang Plus/Minus, Innenraum, Deckelausschnitt)
        self.ausschnitte = []          # (shape, [Ziel-BT …], von) – montage.py schneidet sie am Ende aus den Ziel-Teilen (z. B. Laschen durch Pad, obere Kühlplatte, Deckel)
        self.anordnung()

    def schneide(self, shape, ziele, von=""):
        """Ausschnitt anmelden. ziele = BT-Nummern, aus deren Teilen das Volumen entfernt wird (Reihenfolge der Module egal)."""
        self.ausschnitte.append((shape, list(ziele), von))

    def anordnung(self):
        """Zellanordnung und Querträgerlagen (übernommen aus cad/pack/pack_e2d.py, gleiche Ergebnisse wie G4/E2):
        LFP: 2 Reihen Blade-Zellen quer (Länge in Y), Zellpaket mittig in X, Felder zwischen nq Querträgern.
        NMC: 4680 hexagonal je Feld, Feldlänge aus Gehäuselänge, je Feld n/(nq+1) Zellen, Startreihe zentriert.
        Ergebnis: self.zellen = [dict(cx, cy, feld, reihe)], self.quertraeger_x = [x Vorderkante], self.felder = [(x0, x1)]."""
        nq = int(a("A_quertraeger_anzahl")); qb, sp = a("A_quertraeger_breite_mm"), a("A_quertraeger_spiel_mm")
        rand, Lg, B = self.rand, self.L, self.B
        self.nq, self.qb = nq, qb
        self.zellen, self.quertraeger_x, self.felder = [], [], []
        if VAR == "LFP":
            Lc, Dc = p("BT-100", "laenge_mm"), p("BT-100", "dicke_mm")
            n = int(a("A_zellzahl_LFP")); ab = a("A_zellabstand_LFP_mm"); nz = n // 2; pitch = Dc + ab
            Lg_calc = nz * Dc + (nz - 1) * ab + nq * (qb + 2 * sp) + 2 * rand
            assert Lg >= Lg_calc, (Lg, Lg_calc)
            self.zell_mass = dict(L=Lc, D=Dc, H=self.h_zelle, pitch=pitch)
            x = rand + (Lg - Lg_calc) / 2; self.zellpaket_x0 = x
            grp = [nz // (nq + 1) + (1 if i < nz % (nq + 1) else 0) for i in range(nq + 1)]
            y_luecke = (B - 2 * rand - 2 * Lc) / 2              # alter Code: rand + 4 (Luft zur Wand), hier symmetrisch hergeleitet
            for gi, g in enumerate(grp):
                x_feld0 = x
                for rr in range(2):
                    y0 = rand + y_luecke + rr * Lc
                    for k in range(g):
                        self.zellen.append(dict(cx=x + k * pitch + Dc / 2, cy=y0 + Lc / 2, feld=gi, reihe=rr, k=k))
                x += g * pitch - ab
                self.felder.append((x_feld0, x)); x += sp
                if gi < nq: self.quertraeger_x.append(x); x += qb + sp
            self.zellpaket_x1 = x - sp
        else:
            d, H = p("BT-100", "durchmesser_mm"), self.h_zelle
            n = int(a("A_zellzahl_NMC")); ab = a("A_zellabstand_NMC_mm")
            t = d + ab; rp = t * math.sqrt(3) / 2
            feld = (Lg - 2 * rand - nq * qb - nq * 2 * sp) / (nq + 1)
            Bi = B - 2 * rand; ng = int((Bi - d) // t) + 1; nu = int((Bi - d - t / 2) // t) + 1; rows = int((feld - d) // rp) + 1
            je = n // (nq + 1); assert je * (nq + 1) == n
            self.zell_mass = dict(D=d, H=H, teilung=t, reihenabstand=rp)
            x = rand; self.zellpaket_x0 = x
            for f in range(nq + 1):
                need = cnt = 0
                while cnt < je: cnt += ng if need % 2 == 0 else nu; need += 1
                r0 = (rows - need) // 2; k_f = 0
                for r in range(r0, rows):
                    c_ = ng if r % 2 == 0 else nu; off = d / 2 + (0 if r % 2 == 0 else t / 2)
                    for k in range(c_):
                        if k_f == je: break
                        self.zellen.append(dict(cx=x + d / 2 + r * rp, cy=rand + off + k * t, feld=f, reihe=r, k=k)); k_f += 1
                assert k_f == je
                self.felder.append((x, x + feld)); x += feld + sp
                if f < nq: self.quertraeger_x.append(x); x += qb + sp
            self.zellpaket_x1 = x - sp
        self.endzone_vorn = (rand, self.zellpaket_x0)
        self.endzone_hinten = (self.zellpaket_x1, Lg - rand)

    def als_dict(self):
        einfach = lambda v: isinstance(v, (int, float, str)) or (isinstance(v, (list, tuple)) and all(isinstance(x, (int, float, str)) or (isinstance(x, (list, tuple)) and all(isinstance(y, (int, float)) for y in x)) for x in v))
        d = {k: v for k, v in self.__dict__.items() if einfach(v)}
        d["zellen_anzahl"] = len(self.zellen)
        return d
