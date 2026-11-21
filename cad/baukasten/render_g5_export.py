# KI-generiert (Claude Sonnet, 2026-11-19), Entwurf. Auftrag G5.8. Aufruf: PACK_VARIANTE=LFP freecadcmd cad/baukasten/render_g5_export.py
# Liest ausgabe/pack_<V>.FCStd, schreibt je (BT, Werkstoff) ein Binär-STL (Toleranz 0,3 mm) nach ausgabe/netz/<V>/ und index.json.
import FreeCAD, os, json, struct
R = "/home/cae/hermes/batterie/cad/baukasten"; V = os.environ["PACK_VARIANTE"]; TOL = 0.3
SCHNITT = os.environ.get("G5_SCHNITT") == "1"   # Viertelschnitt: Quadrant x>L/2, y<B/2 wegschneiden (echte Boole-Schnitte, mit Schnittflächen)
FN = json.load(open(f"{R}/farben.json")); NAMEN = FN.get("farbnamen", {}); WS = FN["werkstoffe"]
doc = FreeCAD.openDocument(f"{R}/ausgabe/pack_{V}.FCStd"); out = f"{R}/ausgabe/netz/{V}" + ("_schnitt" if SCHNITT else ""); os.makedirs(out, exist_ok=True)
for f in os.listdir(out): os.remove(f"{out}/{f}")
grp = {}
import Part
if SCHNITT:
    ERG = json.load(open(f"{R}/ausgabe/ergebnis_{V}.json")); XC, YC = ERG["laenge_mm"] / 2, ERG["breite_mm"] / 2
    BOX = Part.makeBox(ERG["laenge_mm"] + 500, YC + 500, 1000, FreeCAD.Vector(XC, -500, -200)); BBX = BOX.BoundBox
for o in doc.Objects:
    if o.TypeId != "Part::Feature" or not hasattr(o, "Werkstoff"): continue
    bt = next((p.Name for p in o.InList if p.TypeId == "App::DocumentObjectGroup"), "BT_x").replace("_", "-")
    g = grp.setdefault((bt, o.Werkstoff), {"farbe": o.Farbe, "tri": [], "teile": [], "bb": [1e9, 1e9, 1e9, -1e9, -1e9, -1e9]})
    sh = o.Shape
    if SCHNITT:
        b = sh.BoundBox
        if b.XMax > XC and b.YMin < YC:
            if b.XMin >= XC and b.YMax <= YC: continue   # ganz im Quadranten
            try: sh = sh.cut(BOX)
            except Exception as ex: print("Schnitt fehlgeschlagen", o.Label, ex)
            if sh.isNull() or sh.Volume < 1e-6: continue
    pts, tri = sh.tessellate(TOL)
    for t in tri: g["tri"].append((pts[t[0]], pts[t[1]], pts[t[2]]))
    g["teile"].append(o.Label); b = o.Shape.BoundBox
    g["bb"] = [min(g["bb"][0], b.XMin), min(g["bb"][1], b.YMin), min(g["bb"][2], b.ZMin), max(g["bb"][3], b.XMax), max(g["bb"][4], b.YMax), max(g["bb"][5], b.ZMax)]
idx = []
for (bt, ws), g in sorted(grp.items()):
    fn = f"{bt}__{ws}.stl".replace("/", "_")
    with open(f"{out}/{fn}", "wb") as fh:
        fh.write(b"KI-generiert G5.8".ljust(80, b" ")); fh.write(struct.pack("<I", len(g["tri"])))
        for a, b_, c in g["tri"]:
            fh.write(struct.pack("<12fH", 0, 0, 0, a.x, a.y, a.z, b_.x, b_.y, b_.z, c.x, c.y, c.z, 0))
    try: fa = json.loads(g["farbe"])
    except Exception: fa = g["farbe"]
    if isinstance(fa, str): fa = NAMEN.get(fa, [0.5, 0.5, 0.5])
    w = WS.get(ws, {})
    idx.append(dict(bt=bt, werkstoff=ws, farbe=fa, rauheit=w.get("rauheit", 0.5), metall=w.get("metall", 0), datei=fn, anzahl_teile=len(g["teile"]), beispiel=g["teile"][:3], bbox_mm=[round(x, 1) for x in g["bb"]], dreiecke=len(g["tri"])))
json.dump(idx, open(f"{out}/index.json", "w"), ensure_ascii=False, indent=1)
print("EXPORT FERTIG", V, len(idx), "Netze")
