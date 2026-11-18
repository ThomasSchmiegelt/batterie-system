# KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. Auftrag G2 (cad/zelle/AUFTRAG.md).
"""Parametrische Zelle in FreeCAD (headless).
Aufruf:  ZELLE_VARIANTE=LFP|NMC [ZELLE_PARAMETER=datei.json] [ZELLE_AUSGABE=ordner] $FREECAD_APPIMAGE freecadcmd cad/zelle/zelle.py
(Alternativ nach `--`: --variante V --parameter datei; freecadcmd meldet dann eine harmlose Ladewarnung für die Datei.)
Maße kommen nur aus der Parameterdatei (BT-100 Maße/Format, BT-120 Wand). Alles, was dort nicht steht
(Polmaße), steht als ANNAHME_* hier und wird im Bild als Annahme beschriftet."""
import sys, os, json
import FreeCAD, Part, Mesh, MeshPart
from FreeCAD import Vector as V

# ---- Annahmen (keine Akte, keine Quelle; Opus entscheidet über Akte) ----
ANNAHME_POL_DURCHMESSER_MM = 10.0   # LFP: Polstummel an beiden Stirnseiten
ANNAHME_POL_HOEHE_MM = 3.0          # LFP: Überstand je Pol über die Stirnseite
ANNAHME_NMC_POL_DURCHMESSER_MM = 12.0  # NMC: Pluspol oben mittig
ANNAHME_NMC_POL_HOEHE_MM = 1.0         # NMC: Überstand Pluspol; Minus = Becherrand (Gehäuse), kein eigenes Maß

def args():
    a = sys.argv[1:]
    if "--" in a: a = a[a.index("--") + 1:]
    o = {k: os.environ.get("ZELLE_" + k.upper()) for k in ("variante", "parameter", "ausgabe")}  # freecadcmd öffnet Dateinamen in argv: besser per Umgebung
    for i, x in enumerate(a):
        if x.startswith("--") and x[2:] in o and i + 1 < len(a): o[x[2:]] = a[i + 1]
    return o

def wert(P, bt, m):
    w = P["parameter"][bt][m]["wert"]
    if w is None: raise SystemExit(f"FEHLT: {bt}/{m} in Parameterdatei (Auftrag: zurück an Opus)")
    return float(w)

def main():
    o = args(); var = o["variante"]
    if var not in ("LFP", "NMC"): raise SystemExit("--variante LFP|NMC angeben")
    R = os.environ.get("BATTERIE", "/home/cae/hermes/batterie")
    pf = o["parameter"] or f"{R}/pm/bauteile/parameter_{var}.json"
    out = o["ausgabe"] or f"{R}/cad/zelle/entwurf"; os.makedirs(out, exist_ok=True)
    P = json.load(open(pf)); doc = FreeCAD.newDocument(f"zelle_{var}")
    wand = wert(P, "BT-120", "wandstaerke_mm"); Ah = wert(P, "BT-100", "kapazitaet_Ah"); U = wert(P, "BT-100", "nennspannung_V")
    if var == "LFP":
        L, B, D = (wert(P, "BT-100", k) for k in ("laenge_mm", "breite_mm", "dicke_mm"))
        aussen = Part.makeBox(L, B, D)
        gehaeuse = aussen.cut(Part.makeBox(L - 2*wand, B - 2*wand, D - 2*wand, V(wand, wand, wand)))
        d, h = ANNAHME_POL_DURCHMESSER_MM, ANNAHME_POL_HOEHE_MM
        pol_plus = Part.makeCylinder(d/2, h, V(L, B/2, D/2), V(1, 0, 0))
        pol_minus = Part.makeCylinder(d/2, h, V(0, B/2, D/2), V(-1, 0, 0))
        pole = {"Pol_plus": pol_plus, "Pol_minus": pol_minus}
        masse = {"laenge_mm": L, "breite_mm": B, "dicke_mm": D}
    else:
        Dm, H = wert(P, "BT-100", "durchmesser_mm"), wert(P, "BT-100", "hoehe_mm")
        aussen = Part.makeCylinder(Dm/2, H)
        gehaeuse = aussen.cut(Part.makeCylinder(Dm/2 - wand, H - 2*wand, V(0, 0, wand)))
        pole = {"Pol_plus": Part.makeCylinder(ANNAHME_NMC_POL_DURCHMESSER_MM/2, ANNAHME_NMC_POL_HOEHE_MM, V(0, 0, H))}
        masse = {"durchmesser_mm": Dm, "hoehe_mm": H}
    teile = {"Gehaeuse": gehaeuse, **pole}
    for n, s in teile.items():
        doc.addObject("Part::Feature", n).Shape = s
    doc.recompute()
    alle = Part.makeCompound(list(teile.values())); bb = alle.BoundBox
    v_aussen_L = aussen.Volume / 1e6
    ergebnis = {
        "hinweis": "KI-generiert, ENTWURF (Akten vorgeschlagen), nicht freigegeben. Erzeugt von cad/zelle/zelle.py",
        "variante": var, "parameterdatei": os.path.relpath(pf, R), "wandstaerke_mm": wand, "masse_eingabe": masse,
        "kapazitaet_Ah": Ah, "nennspannung_V": U,
        "annahmen": {"ANNAHME_POL_DURCHMESSER_MM": ANNAHME_POL_DURCHMESSER_MM, "ANNAHME_POL_HOEHE_MM": ANNAHME_POL_HOEHE_MM} if var == "LFP"
                    else {"ANNAHME_NMC_POL_DURCHMESSER_MM": ANNAHME_NMC_POL_DURCHMESSER_MM, "ANNAHME_NMC_POL_HOEHE_MM": ANNAHME_NMC_POL_HOEHE_MM},
        "aussenvolumen_L": v_aussen_L,
        "bbox_mit_polen_mm": [bb.XLength, bb.YLength, bb.ZLength],
        "gehaeuse_materialvolumen_cm3": gehaeuse.Volume / 1e3,
        "polvolumen_cm3": sum(s.Volume for s in pole.values()) / 1e3,
        "energie_Wh": Ah * U, "Wh_pro_L": Ah * U / v_aussen_L,
        "gueltig_solid": bool(gehaeuse.isValid()),
    }
    json.dump(ergebnis, open(f"{out}/ergebnis_{var}.json", "w"), indent=1, ensure_ascii=False)
    doc.saveAs(f"{out}/zelle_{var}.FCStd")
    Part.export(list(doc.Objects), f"{out}/zelle_{var}.step")
    # Tessellierung für das Bild (matplotlib in zelle_bild.py)
    mesh = {}
    for n, s in teile.items():
        pts, tri = s.tessellate(0.5)
        mesh[n] = {"punkte": [[p.x, p.y, p.z] for p in pts], "dreiecke": [list(t) for t in tri]}
    json.dump(mesh, open(f"{out}/netz_{var}.json", "w"))
    print("FERTIG", var, ergebnis["aussenvolumen_L"], ergebnis["Wh_pro_L"])
main()
