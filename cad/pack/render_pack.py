# KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. Auftrag G4. Blender CPU (Cycles), Stil wie cad/zelle/render_detail.py.
# Aufruf (über render_pack.sh): PACK_VARIANTE=LFP RENDER_SAMPLES=24 $BLENDER -b -P cad/pack/render_pack.py
# Liest entwurf/netz_<V>*.json (von pack.py), schreibt entwurf/roh_<V>_<ansicht>.png und roh_<V>_<ansicht>.json (2D-Anker für die Beschriftung).
# Ansichten: gesamt, explosion, laengs, quer, schnitt (Viertel). Keine Maße im Code außer Ansichtsparametern.
import bpy, os, json, math
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
R = os.environ.get("BATTERIE", "/home/cae/hermes/batterie"); OUT = f"{R}/cad/pack/entwurf"; VAR = os.environ["PACK_VARIANTE"]
S = int(os.environ.get("RENDER_SAMPLES", "24")); MM = 0.001
ERG = json.load(open(f"{OUT}/ergebnis_{VAR}.json")); LG, BB, HH = ERG["gehaeuse_L_mm"], 1430.0, ERG["hoehe_stapel_mm"]
BB = ERG["breite_mm"]
FARBE = {"Zellen": (0.1, 0.35, 0.8), "Quertraeger": (0.9, 0.4, 0.05), "Seitenrahmen": (0.55, 0.57, 0.6), "Boden": (0.65, 0.67, 0.7),
 "Deckel": (0.75, 0.77, 0.8), "Unterfahrschutz": (0.3, 0.3, 0.33), "Kuehlplatte": (0.1, 0.65, 0.65), "Pad": (0.9, 0.85, 0.2),
 "Zellverbinder": (0.95, 0.45, 0.25), "Gruppenverbinder": (0.95, 0.45, 0.25), "Gruppenbruecke": (0.85, 0.15, 0.55), "Zellabgriff": (0.9, 0.9, 0.9), "Zelltraeger": (0.5, 0.2, 0.6), "Verguss": (0.2, 0.7, 0.2)}
EXPL = {"Unterfahrschutz": 0, "Boden": 1, "Seitenrahmen": 2, "Zelltraeger": 3, "Verguss": 3.5, "Quertraeger": 4, "Zellen": 4, "Zellverbinder": 5, "Zellabgriff": 5, "Gruppenverbinder": 5.5, "Gruppenbruecke": 5.5, "Deckel": 8}
EXPL_PL = {"Kuehlplatte": (1.4, 6.5), "Pad": (2.2, 5.6)}
ST = 70.0   # Abstand je Explosionsstufe in mm (nur Darstellung)
# Ansicht: (netzdatei-suffix, explosion, Blickrichtung, ortho_scale_mm, Auflösung, Shift_y, nur_gruppen_beschriften)
ANS = {"gesamt": ("", False, (0.75, -1.0, 0.45), 1.25 * LG, (1600, 900), 0.0, ("Deckel", "Seitenrahmen", "Unterfahrschutz", "Boden")),
       "explosion": ("", True, (0.75, -1.0, 0.5), 1.7 * LG, (1600, 1100), 0.03, None),
       "laengs": ("_laengs", False, (0.0, -1.0, 0.0), 1.04 * LG, (2000, 520), 0.0, None),
       "quer": ("_quer", False, (-1.0, 0.0, 0.0), 1.04 * BB, (1800, 520), 0.0, None),
       "schnitt": ("_schnitt", False, (0.75, -1.0, 0.5), 380.0, (1600, 900), 0.0, None),
       "ecke": ("_halb", False, (0.9, -0.45, 0.4), 300.0, (1600, 900), 0.0, None)}   # Viertelschnitt, Kamera an der Außenwand (Verbinder der äußeren Zellenden)
def bau(name):
    suf, expl, dirv, scale, res, shy, nur = ANS[name]
    netz = json.load(open(f"{OUT}/netz_{VAR}{suf}.json"))
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene; sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = S; sc.cycles.use_denoising = False
    sc.render.resolution_x, sc.render.resolution_y = res; sc.render.resolution_percentage = 100; sc.view_settings.view_transform = "Standard"
    wd = bpy.data.worlds.new("w"); sc.world = wd; wd.use_nodes = True
    wd.node_tree.nodes["Background"].inputs[1].default_value = 0.9; wd.node_tree.nodes["Background"].inputs[0].default_value = (0.93, 0.94, 0.96, 1)
    obs = []
    for g, m in netz.items():
        pts, tri = m["punkte"], m["dreiecke"]
        if not pts or (name in ("schnitt", "ecke") and g == "Deckel"): continue   # Deckel im Viertelschnitt weggelassen
        if g in EXPL_PL:
            zmid = (min(p[2] for p in pts) + max(p[2] for p in pts)) / 2
            parts = {" unten": [t for t in tri if sum(pts[i][2] for i in t) / 3 < zmid], " oben": [t for t in tri if sum(pts[i][2] for i in t) / 3 >= zmid]}
            offs = {" unten": EXPL_PL[g][0] * ST if expl else 0, " oben": EXPL_PL[g][1] * ST if expl else 0}
        else: parts = {"": tri}; offs = {"": EXPL[g] * ST if expl else 0}
        for k, tr in parts.items():
            if not tr: continue
            me = bpy.data.meshes.new(g + k); me.from_pydata([(p[0] * MM, p[1] * MM, (p[2] + offs[k]) * MM) for p in pts], [], tr); me.update()
            ob = bpy.data.objects.new(g + k, me); sc.collection.objects.link(ob); ob["gruppe"] = g
            mt = bpy.data.materials.new(g); mt.use_nodes = True; b = mt.node_tree.nodes["Principled BSDF"]
            b.inputs["Base Color"].default_value = (*FARBE[g], 1); b.inputs["Metallic"].default_value = 0.4 if g not in ("Zellen", "Pad", "Verguss") else 0.0; b.inputs["Roughness"].default_value = 0.4
            ob.data.materials.append(mt); obs.append(ob)
    allp = [ob.matrix_world @ Vector(v) for ob in obs for v in ob.bound_box]
    lo = Vector((min(p.x for p in allp), min(p.y for p in allp), min(p.z for p in allp))); hi = Vector((max(p.x for p in allp), max(p.y for p in allp), max(p.z for p in allp)))
    c = (lo + hi) / 2
    if name == "schnitt": c = Vector((LG / 2 * MM, BB / 2 * MM, HH / 2 * MM))
    if name == "ecke": c = Vector((ERG["schnittebene_halb_x_mm"] * MM, (BB - ERG["annahmen"]["A_rand_mm"]["wert"] - 70) * MM, HH / 2 * MM))   # Kamera auf die Schnittecke
    cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); sc.collection.objects.link(cam); sc.camera = cam
    cam.data.type = "ORTHO"; cam.data.ortho_scale = scale * MM if name != 'schnitt' else scale * MM; cam.data.shift_y = shy
    cam.location = c + Vector(dirv).normalized() * 10; cam.rotation_euler = (c - cam.location).to_track_quat("-Z", "Y").to_euler()
    for az, en in ((35, 1.6), (-120, 0.6)):
        l = bpy.data.objects.new("l", bpy.data.lights.new("l", "SUN")); l.data.energy = en; l.rotation_euler = (math.radians(50), 0, math.radians(az)); sc.collection.objects.link(l)
    bpy.context.view_layer.update()
    # Anker aus der Teilegeometrie: sichtbare Eckpunkte (Strahltest Kamera -> Punkt trifft das Teil selbst); Teile ohne sichtbaren Punkt werden nicht beschriftet
    import numpy as np, random
    dg = bpy.context.evaluated_depsgraph_get(); dv = (c - cam.location).normalized(); random.seed(1)
    anker = []; sel = [ob for ob in obs if not nur or ob["gruppe"] in nur]
    for i, ob in enumerate(sel):
        polys = list(ob.data.polygons); random.shuffle(polys); vis = []
        for pl in polys[:3000]:   # Flächenmittelpunkte der Dreiecke als Kandidaten
            w3 = ob.matrix_world @ pl.center; p2 = world_to_camera_view(sc, cam, w3)
            if not (0.02 < p2.x < 0.98 and 0.02 < p2.y < 0.98): continue
            hit, loc, nor, idx, hob, mat = sc.ray_cast(dg, w3 - dv * 5.0, dv)
            if hit and hob is not None and hob.name == ob.name and (loc - w3).length < 5e-4: vis.append((p2.x, p2.y))
        if not vis: continue
        xs = np.array([q[0] for q in vis]); ys = np.array([q[1] for q in vis])
        if name in ("laengs", "quer"):   # Schnitte: Ankerpunkte entlang x verteilen
            tx = np.quantile(xs, 0.1 + 0.8 * ((i * 5) % len(sel)) / max(len(sel) - 1, 1)); ty = np.median(ys)
        elif name in ("schnitt", "ecke"): tx, ty = 0.5, 0.5   # nächster sichtbarer Punkt zur Bildmitte (Schnittecke)
        else: tx, ty = np.median(xs), np.median(ys)
        k = int(np.argmin((xs - tx) ** 2 + (ys - ty) ** 2))
        anker.append({"name": ob.name, "gruppe": ob["gruppe"], "x": float(xs[k]) * res[0], "y": (1 - float(ys[k])) * res[1]})
    sc.render.filepath = f"{OUT}/roh_{VAR}_{name}.png"; bpy.ops.render.render(write_still=True)
    json.dump({"anker": anker, "res": res, "px_je_mm": res[0] / (scale if name in ("laengs", "quer") else 1e9) if name in ("laengs", "quer") else None}, open(f"{OUT}/roh_{VAR}_{name}.json", "w"))
for a in (os.environ.get("RENDER_NUR") or ",".join(ANS)).split(","): bau(a)
print("RENDER FERTIG", VAR)
