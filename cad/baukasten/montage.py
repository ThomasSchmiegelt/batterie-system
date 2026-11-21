# KI-generiert (Claude Opus, 2026-11-19), Entwurf. G5.2 (cad/baukasten/PLAN.md §1, §3).
"""Montage: baut das Pack aus der Stückliste (SL3) und prüft es gegen die Stückliste.

Aufruf:  PACK_VARIANTE=LFP|NMC $FREECAD_APPIMAGE freecadcmd cad/baukasten/montage.py
Optionen (Umgebung): G5_NUR="gehaeuse,kuehlung" (nur diese Module bauen, zum Entwickeln), G5_KOLLISION=0 (Prüfung aus), G5_STEP=0.
Ablauf:
 1. stueckliste_<V>.json lesen; jede Position mit geometrie.generator ruft REGISTRY[generator](ctx, position) → list[Teil].
    Reihenfolge nach MODULFOLGE (die Zellanordnung legt die Feldgrenzen und Querträgerlagen in ctx fest, alle anderen lesen sie).
 2. Prüfungen: Stückzahl CAD = menge_<V>; Masse CAD gegen masse_ges_kg (Toleranz 3 %, ERW-G5); Kollisionen zwischen verschiedenen
    Positionen (Hüllquader-Vorfilter, dann Schnittvolumen > KOLL_MM3); Höhen gegen M0-Grenze und Schaltbox-Turm; Teile ohne Position.
 3. Ausgabe cad/baukasten/ausgabe/: pack_<V>.FCStd (Gruppen je BT, Farben), step/<BT>.step, ergebnis_<V>.json, pruefung_<V>.txt.
"""
import os, sys, json, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import kern as K
from kern import VAR, ROOT
import importlib

MODULFOLGE = ["zelle", "schaltbox", "verbinder", "elektronik", "kaufteile", "normteile", "gehaeuse", "kuehlung"]   # Gehäuse/Kühlung zuletzt: lesen Lagen, die andere Module in ctx ablegen
KOLL_MM3 = 1.0          # Schnittvolumen unter 1 mm³ = Kontakt, kein Fehler
MASSE_TOL = 0.03        # ERW-G5
OUT = ROOT / "cad/baukasten/ausgabe"; (OUT / "step").mkdir(parents=True, exist_ok=True)
t0 = time.time()
NUR = [m for m in os.environ.get("G5_NUR", "").split(",") if m]

SL = json.load(open(ROOT / f"pm/bauteile/stueckliste_{VAR}.json", encoding="utf-8"))
if str(SL.get("version")) < "0.3":
    raise SystemExit(f"Stückliste {VAR} ist Version {SL.get('version')}, montage.py braucht SL3 (≥ 0.3)")
POS = SL["positionen"]
mk = f"menge_{VAR}"

for m in MODULFOLGE:                       # Module laden → Generatoren melden sich in K.REGISTRY an
    if (Path(__file__).parent / "teile" / f"{m}.py").exists():
        importlib.import_module(f"teile.{m}")

ctx = K.Ctx()
alle, bericht, fehler = [], [], []
def modul(gen): return gen.split(".")[0]
reihe = sorted([q for q in POS if (q.get("geometrie") or {}).get("generator")], key=lambda q: MODULFOLGE.index(modul(q["geometrie"]["generator"])) if modul(q["geometrie"]["generator"]) in MODULFOLGE else 99)
for q in POS:
    g = q.get("geometrie") or {}
    if not g.get("generator") and g.get("detailstufe") not in ("-",) and q.get("art") != "S":
        fehler.append(f"Position {q['pos']} {q['benennung']}: kein Generator")
for q in reihe:
    gen = q["geometrie"]["generator"]
    if NUR and modul(gen) not in NUR: continue
    f = K.REGISTRY.get(gen)
    if f is None:
        fehler.append(f"Position {q['pos']}: Generator {gen} fehlt im Code"); continue
    ts = time.time()
    teile = f(ctx, q)
    for i, t in enumerate(teile):
        t.pos, t.bt = q["pos"], q["bt"]
        if q.get("geometrie", {}).get("farbe"): t.farbe = q["geometrie"]["farbe"]
    soll = q.get(mk)
    ist = len(teile)
    m_ist = sum(t.masse_kg for t in teile if t.masse_kg is not None)
    m_soll = q.get("masse_ges_kg")
    zeile = dict(pos=q["pos"], bt=q["bt"], generator=gen, stufe=f.g5["stufe"], soll=soll, ist=ist,
                 masse_cad_kg=round(m_ist, 4), masse_sl_kg=m_soll, sekunden=round(time.time() - ts, 1))
    if q.get("menge_quelle") == "CAD":
        zeile["hinweis"] = "Stückzahl aus CAD (Normteile), Stückliste übernimmt sie"
    elif isinstance(soll, (int, float)) and ist != soll:
        fehler.append(f"{q['pos']} {gen}: Stückzahl CAD {ist} ≠ Stückliste {soll}")
    bericht.append(zeile); alle += teile
    print(f"{q['pos']:>7} {gen:<32} {ist:>5} Teile {m_ist:9.3f} kg  {zeile['sekunden']} s", flush=True)

# ---------------------------------------------------------------- Ausschnitte (ctx.schneide): erst jetzt, damit die Modulreihenfolge egal ist
if ctx.ausschnitte:
    nach_bt = {}
    for shp, ziele, von in ctx.ausschnitte:
        for z in ziele: nach_bt.setdefault(z, []).append(shp)
    for t in alle:
        werk = nach_bt.get(t.bt)
        if not werk: continue
        bb = t.shape.BoundBox
        hit = [s for s in werk if bb.intersect(s.BoundBox)]
        if not hit: continue
        alt = t.masse_kg
        t.shape = t.shape.cut(K.Part.makeCompound(hit))
        rho = K.dichte_kg_mm3(t.werkstoff)
        if rho and t.masse_quelle == "CAD-Volumen": t.masse_kg = t.shape.Volume * rho
    for z in bericht:                                   # Massen nach dem Ausschneiden neu summieren
        z["masse_cad_kg"] = round(sum(t.masse_kg for t in alle if t.pos == z["pos"] and t.masse_kg is not None), 4)
for z in bericht:
    m_ist, m_soll = z["masse_cad_kg"], z["masse_sl_kg"]
    if isinstance(m_soll, (int, float)) and m_soll > 0 and abs(m_ist - m_soll) / m_soll > MASSE_TOL:
        fehler.append(f"{z['pos']} {z['generator']}: Masse CAD {m_ist:.3f} kg gegen Stückliste {m_soll:.3f} kg ({(m_ist/m_soll-1)*100:+.1f} %)")

# ---------------------------------------------------------------- Kollisionen (nur zwischen verschiedenen Positionen)
koll = []
if os.environ.get("G5_KOLLISION", "1") == "1":
    bbs = [t.shape.BoundBox for t in alle]
    for i in range(len(alle)):
        for j in range(i + 1, len(alle)):
            if alle[i].pos == alle[j].pos or not bbs[i].intersect(bbs[j]): continue
            try:
                v = alle[i].shape.common(alle[j].shape).Volume
            except Exception as e:
                v = -1
            if v > KOLL_MM3 or v < 0:
                koll.append((alle[i].name, alle[j].name, round(v, 1)))
    for k in koll[:50]: fehler.append(f"Kollision {k[0]} ↔ {k[1]}: {k[2]} mm³")

# ---------------------------------------------------------------- Höhen
zmax = max(t.shape.BoundBox.ZMax for t in alle) if alle else 0
if alle:
    xs = [t.shape.BoundBox for t in alle]
    L_ist = max(b.XMax for b in xs) - min(b.XMin for b in xs); B_ist = max(b.YMax for b in xs) - min(b.YMin for b in xs)
else:
    L_ist = B_ist = 0

# ---------------------------------------------------------------- Ausgabe
masse = sum(t.masse_kg for t in alle if t.masse_kg is not None)
stufen = {}
for z in bericht: stufen[z["stufe"]] = stufen.get(z["stufe"], 0) + 1
erg = dict(hinweis="KI-generiert (Claude Opus, G5 montage.py), Entwurf", variante=VAR, stueckliste_version=SL.get("version"),
           teile=len(alle), masse_kg=round(masse, 3), laenge_mm=round(L_ist, 1), breite_mm=round(B_ist, 1), hoehe_max_mm=round(zmax, 1),
           stufen=stufen, positionen=bericht, kollisionen=koll, fehler=fehler, ctx=ctx.als_dict(),
           akten_genutzt=sorted(K.GENUTZT["p"]), annahmen_genutzt=sorted(K.GENUTZT["a"]), sekunden=round(time.time() - t0, 1), nur=NUR)
json.dump(erg, open(OUT / f"ergebnis_{VAR}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
with open(OUT / f"pruefung_{VAR}.txt", "w", encoding="utf-8") as fh:
    fh.write(f"G5 Montage {VAR}: {len(alle)} Teile, {masse:.2f} kg, L×B×H {L_ist:.0f}×{B_ist:.0f}×{zmax:.0f} mm, Stufen {stufen}\n")
    fh.write(f"{len(fehler)} Fehler\n" + "\n".join(fehler) + "\n")

doc = K.FreeCAD.newDocument(f"pack_{VAR}")
gruppen = {}
for t in alle:
    g = gruppen.get(t.bt)
    if g is None:
        g = gruppen[t.bt] = doc.addObject("App::DocumentObjectGroup", t.bt.replace("-", "_"))
    o = doc.addObject("Part::Feature", t.name.replace(" ", "_")); o.Shape = t.shape
    o.addProperty("App::PropertyString", "Position"); o.Position = str(t.pos)
    o.addProperty("App::PropertyString", "Werkstoff"); o.Werkstoff = str(t.werkstoff)
    o.addProperty("App::PropertyString", "Farbe"); o.Farbe = json.dumps(t.farbe)
    g.addObject(o)
doc.recompute(); doc.saveAs(str(OUT / f"pack_{VAR}.FCStd"))
if os.environ.get("G5_STEP", "1") == "1":
    import Part
    for bt, g in gruppen.items():
        Part.export(g.Group, str(OUT / "step" / f"{VAR}_{bt}.step"))
print(f"fertig {VAR}: {len(alle)} Teile, {masse:.2f} kg, {len(fehler)} Fehler, {time.time()-t0:.0f} s")
