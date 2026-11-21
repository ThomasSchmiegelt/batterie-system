# KI-generiert (Claude Sonnet, 2026-11-19), Entwurf. Auftrag G5.8. Blender -b, Cycles CPU.
# Aufruf: PACK_VARIANTE=LFP RENDER_SAMPLES=32 [RENDER_NUR=gesamt,schnitt] blender -b -P cad/baukasten/render_g5.py
# Liest ausgabe/netz/<V>/ (render_g5_export.py), farben.json; schreibt bilder/roh_g5_<V>_<ansicht>.png und .json (2D-Anker). Beschriftung: label_g5.py.
import bpy, bmesh, os, json, math, random, struct
import numpy as np
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
R = "/home/cae/hermes/batterie/cad/baukasten"; V = os.environ["PACK_VARIANTE"]; S = int(os.environ.get("RENDER_SAMPLES", "32")); MM = 0.001
def lade_idx(d): return json.load(open(f"{R}/ausgabe/netz/{d}/index.json"))
IDX = lade_idx(V); WS = json.load(open(f"{R}/farben.json"))["werkstoffe"]; ERG = json.load(open(f"{R}/ausgabe/ergebnis_{V}.json"))
L, B = ERG["laenge_mm"], ERG["breite_mm"]; ST = 70.0
def stl(fn):
    with open(fn, "rb") as f: f.seek(80); n = struct.unpack("<I", f.read(4))[0]; a = np.frombuffer(f.read(50 * n), dtype=np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")]))
    return a["v"].astype(np.float64)   # (n,3,3)
# Explosionsstufen (Vielfache von ST in z); Kühlkreis zusätzlich in x nach hinten (mm)
EZ = {"BT-550": 0, "BT-510": 1, "BT-540": 2, "BT-530": 2, "BT-560": 2, "BT-610u": 3, "BT-230u": 3.7, "BT-100": 4.6, "BT-220": 4.6, "BT-250": 4.6, "BT-260": 4.6, "BT-3": 5.4, "BT-4": 5.4,
      "BT-450": 5.4, "BT-230o": 5.5, "BT-610o": 6.3, "BT-520": 7.3, "BT-580": 7.3, "BT-570": 7.3, "BT-590": 7.3, "BT-7": 8.4}
EX = {"BT-620": 300, "BT-630": 300, "BT-640": 300, "BT-65": 300, "BT-661": 520, "BT-662": 520, "BT-663": 520, "BT-664": 420, "BT-665": 520}
def ez(bt, tag):
    for k in (bt + tag, bt, bt[:4], bt[:5]):
        if k in EZ: return EZ[k]
    return 0
def ex(bt):
    for k in (bt, bt[:5]):
        if k in EX: return EX[k]
    return 0
# Ansichten: (explosion, Blickrichtung, Ziel (mm) oder None=Mitte, Maßstab mm, Auflösung, ausblenden-Funktion, Schnitt, Anker-BT)
ALLE_KK = ("BT-620", "BT-630", "BT-640", "BT-661", "BT-662", "BT-663", "BT-664", "BT-665")
ANS = {
 "gesamt": dict(expl=False, d=(0.75, -1.0, 0.55), z=None, sc=1.2 * L, res=(1600, 900), hide=lambda bt, ws, n: False, cut=False,
                lab=("BT-520", "BT-540", "BT-710", "BT-662", "BT-661", "BT-664", "BT-550")),
 "explosion": dict(expl=True, d=(0.75, -1.0, 0.5), z=None, sc=1.55 * L, res=(1600, 1150), hide=lambda bt, ws, n: bt == "BT-590" and ws == "Stahl", cut=False, shy=0.0,
                lab=("BT-550", "BT-510", "BT-540", "BT-610", "BT-100", "BT-520", "BT-710", "BT-620", "BT-661", "BT-662", "BT-664")),
 "schnitt": dict(expl=False, d=(0.8, -1.0, 0.2), z="cut", sc=280.0, res=(1600, 900), hide=lambda bt, ws, n: bt in ("BT-520", "BT-590", "BT-710", "BT-570") or bt[:5] in ("BT-71", "BT-72", "BT-73", "BT-74", "BT-75", "BT-77", "BT-78"), cut=False, netz="_schnitt",
                lab=("BT-610", "BT-230", "BT-100", "BT-220", "BT-250", "BT-260", "BT-540", "BT-510", "BT-550", "BT-420", "BT-360")),
 "ecke": dict(expl=False, d=(0.9, -0.5, 0.5), z=(2090.0, 150.0, 85.0), sc=520.0, res=(1600, 900), hide=lambda bt, ws, n: bt in ("BT-520",) or (bt == "BT-590" and ws == "Stahl"), cut=False,
                lab=("BT-620", "BT-630", "BT-640", "BT-664", "BT-540", "BT-610", "BT-440", "BT-360", "BT-430")),
 "schaltbox": dict(expl=False, d=(0.45, -0.7, 1.0), z=(1786.0, 715.0, 180.0), sc=700.0, res=(1600, 900), hide=lambda bt, ws, n: (bt == "BT-710" and ws == "Al_eloxiert") or (bt == "BT-590" and ws == "Stahl"), cut=False,
                lab=("BT-711", "BT-712", "BT-713", "BT-720", "BT-730", "BT-770")),
 "kuehlkreis": dict(expl=False, d=(1.0, -0.3, 0.7), z=(2150.0, 715.0, 70.0), sc=1500.0, res=(1600, 900), hide=lambda bt, ws, n: bt[:3] in ("BT-1", "BT-2", "BT-3", "BT-4") or bt in ("BT-520", "BT-590", "BT-570", "BT-580", "BT-430", "BT-440") or bt[:5] in ("BT-71", "BT-72", "BT-73", "BT-74", "BT-75", "BT-77", "BT-78") or bt == "BT-710", cut=False,
                lab=("BT-610", "BT-620", "BT-630", "BT-640", "BT-661", "BT-662", "BT-663", "BT-664", "BT-665")),
 "draufsicht": dict(expl=False, d=(0.0, -0.0001, 1.0), z="mitte", scf=1.06, res=(2000, 1300), oben_weg=True, hide=lambda bt, ws, n: bt in ("BT-520", "BT-570", "BT-580") or (bt == "BT-590" and ws == "Stahl") or (bt == "BT-710" and ws in ("Al_eloxiert", "PA66GF30")), cut=False,
                lab=("BT-320", "BT-360", "BT-430", "BT-440", "BT-710", "BT-620", "BT-420", "BT-100")),
 "kabelplan": dict(expl=False, d=(0.0, -0.0001, 1.0), z="mitte", scf=1.06, res=(2000, 1300), oben_weg=True, hide=lambda bt, ws, n: bt in ("BT-520", "BT-570", "BT-580") or (bt == "BT-590" and ws == "Stahl") or (bt == "BT-710" and ws in ("Al_eloxiert", "PA66GF30")), cut=False,
                alpha=lambda bt, ws: 1.0 if bt in ("BT-430", "BT-360", "BT-361", "BT-320", "BT-440") else 0.35 if bt == "BT-710" else 0.15,
                lab=("BT-320", "BT-360", "BT-430", "BT-440", "BT-710")),
 "bruecke": dict(expl=False, d=(0.25, -0.6, 1.0), z="bruecke", sc=330.0, res=(1600, 900), hide=lambda bt, ws, n: bt in ("BT-520", "BT-570", "BT-580") or (bt == "BT-590" and ws == "Stahl") or bt[:5] in ("BT-71", "BT-73", "BT-74", "BT-75", "BT-77", "BT-78"), cut=False,
                lab=("BT-720", "BT-440", "BT-420", "BT-610")),
}
XC, YC = L / 2, B / 2
def clip(bm, co, no, keep):   # keep: Seite, die bleibt (clear_outer/inner)
    g = bm.verts[:] + bm.edges[:] + bm.faces[:]
    bmesh.ops.bisect_plane(bm, geom=g, plane_co=co, plane_no=no, clear_inner=(keep == "outer"), clear_outer=(keep == "inner"))
def objekt(sc, name, tris, ws, farbe, rau, metall, anz, bt, backflaeche=False, alpha=1.0):
    n = len(tris)
    if n == 0: return None
    me = bpy.data.meshes.new(name); me.vertices.add(3 * n); me.vertices.foreach_set("co", (tris * MM).reshape(-1).astype(np.float32))
    me.loops.add(3 * n); me.loops.foreach_set("vertex_index", np.arange(3 * n, dtype=np.int32)); me.polygons.add(n)
    me.polygons.foreach_set("loop_start", np.arange(0, 3 * n, 3, dtype=np.int32)); me.polygons.foreach_set("loop_total", np.full(n, 3, dtype=np.int32)); me.update(); me.validate()
    ob = bpy.data.objects.new(name, me); sc.collection.objects.link(ob); ob["bt"] = bt; ob["ws"] = ws
    mt = bpy.data.materials.new(name); mt.use_nodes = True; b = mt.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*farbe, 1); b.inputs["Metallic"].default_value = 0.3 * metall; b.inputs["Roughness"].default_value = rau
    if backflaeche:
        nt = mt.node_tree; ge = nt.nodes.new("ShaderNodeNewGeometry"); em = nt.nodes.new("ShaderNodeEmission"); em.inputs[0].default_value = (*[min(1, 0.85 * x + 0.05) for x in farbe], 1); em.inputs[1].default_value = 0.9
        mx = nt.nodes.new("ShaderNodeMixShader"); nt.links.new(ge.outputs["Backfacing"], mx.inputs[0]); nt.links.new(b.outputs[0], mx.inputs[1]); nt.links.new(em.outputs[0], mx.inputs[2])
        nt.links.new(mx.outputs[0], nt.nodes["Material Output"].inputs[0])
    if alpha < 1.0:
        nt = mt.node_tree; tr = nt.nodes.new("ShaderNodeBsdfTransparent"); mx = nt.nodes.new("ShaderNodeMixShader"); mx.inputs[0].default_value = alpha
        b.inputs["Base Color"].default_value = (0.55, 0.55, 0.57, 1); b.inputs["Metallic"].default_value = 0.0
        nt.links.new(tr.outputs[0], mx.inputs[1]); nt.links.new(b.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], nt.nodes["Material Output"].inputs[0])
    ob.data.materials.append(mt); return ob
def bau(name):
    A = ANS[name]; random.seed(1)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene; sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = S; sc.cycles.use_denoising = False; sc.cycles.threads = 6; sc.cycles.transparent_max_bounces = 12
    sc.render.resolution_x, sc.render.resolution_y = A["res"]; sc.render.resolution_percentage = 100; sc.view_settings.view_transform = "Standard"
    wd = bpy.data.worlds.new("w"); sc.world = wd; wd.use_nodes = True
    nt = wd.node_tree; bg = nt.nodes["Background"]; bg.inputs[1].default_value = 0.45; bg.inputs[0].default_value = (0.93, 0.94, 0.96, 1)
    b2 = nt.nodes.new("ShaderNodeBackground"); b2.inputs[1].default_value = 1.0; b2.inputs[0].default_value = (0.95, 0.95, 0.97, 1)
    lp = nt.nodes.new("ShaderNodeLightPath"); mx = nt.nodes.new("ShaderNodeMixShader"); nt.links.new(lp.outputs["Is Camera Ray"], mx.inputs[0])
    nt.links.new(bg.outputs[0], mx.inputs[1]); nt.links.new(b2.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], nt.nodes["World Output"].inputs[0])
    obs = []; boden = None
    nd = V + A.get("netz", "")
    for e in (IDX if not A.get("netz") else lade_idx(nd)):
        bt, ws = e["bt"], e["werkstoff"]
        if A["hide"](bt, ws, name): continue
        t = stl(f"{R}/ausgabe/netz/{nd}/{e['datei']}"); w = WS.get(ws, {}); col = w.get("farbe", [0.5, 0.5, 0.5]); rau = w.get("rauheit", 0.5); met = w.get("metall", 0)
        teile = {"": t}
        if A.get("oben_weg") and bt in ("BT-610", "BT-230"):
            zc = t[:, :, 2].mean(1); zm = (zc.min() + zc.max()) / 2; teile = {"u": t[zc < zm]}
        if A["expl"] and bt in ("BT-610", "BT-230"):
            zc = t[:, :, 2].mean(1); zm = (zc.min() + zc.max()) / 2; teile = {"u": t[zc < zm], "o": t[zc >= zm]}
        for tag, tt in teile.items():
            if A["expl"]:
                tt = tt.copy(); tt[:, :, 2] += ez(bt, tag) * ST; tt[:, :, 0] += ex(bt)
            if A["cut"]:
                me = bpy.data.meshes.new("t"); n = len(tt)
                parts = []
                for k in range(2):
                    bm = bmesh.new()
                    for tri in tt:
                        vs = [bm.verts.new(tuple(p * MM)) for p in tri]
                        try: bm.faces.new(vs)
                        except ValueError: pass
                    if k == 0: clip(bm, (XC * MM, 0, 0), (1, 0, 0), "inner")
                    else:
                        clip(bm, (XC * MM, 0, 0), (1, 0, 0), "outer"); clip(bm, (0, YC * MM, 0), (0, 1, 0), "outer")
                    arr = np.array([[v.co[:] for v in f.verts] for f in bm.faces if len(f.verts) == 3]).reshape(-1, 3, 3) / MM if len(bm.faces) else np.zeros((0, 3, 3))
                    bm.free(); parts.append(arr)
                tts = [p for p in parts if len(p)]
                tt = np.concatenate(tts) if tts else np.zeros((0, 3, 3))
            ob = objekt(sc, f"{bt}_{ws}{tag}", tt, ws, col, rau, met, e["anzahl_teile"], bt, A["cut"], A["alpha"](bt, ws) if "alpha" in A else 1.0)
            if ob: obs.append(ob)
    allp = np.array([(ob.matrix_world @ Vector(v))[:] for ob in obs for v in ob.bound_box])
    lo, hi = allp.min(0), allp.max(0); c = Vector((lo + hi) / 2)
    if A["z"] == "mitte": c = Vector((L / 2, B / 2, 60.0)) * MM
    elif A["z"] == "bruecke": b7 = [e["bbox_mm"] for e in IDX if e["bt"] == "BT-720"]; c = Vector(((min(q[0] for q in b7) + max(q[3] for q in b7)) / 2, (min(q[1] for q in b7) + max(q[4] for q in b7)) / 2, 110.0)) * MM
    elif A["z"] == "cut": c = Vector((XC * MM, YC * MM, 0.07))
    elif name == "schaltbox": b7 = [e["bbox_mm"] for e in IDX if e["bt"] == "BT-710"]; c = Vector(((min(q[0] for q in b7) + max(q[3] for q in b7)) / 2, (min(q[1] for q in b7) + max(q[4] for q in b7)) / 2, 180.0)) * MM   # Mitte BT-710
    elif name in ("ecke", "kuehlkreis"):   # relativ zum Verteiler BT-620 (x-Lage hängt von der Variante ab)
        b6 = [e["bbox_mm"] for e in IDX if e["bt"] == "BT-620"]; x0 = min(q[0] for q in b6); x1 = max(q[3] for q in b6); y0 = min(q[1] for q in b6)
        c = (Vector((x1, y0 + 120, 85.0)) if name == "ecke" else Vector((x0 + 100, 715.0, 70.0))) * MM
    elif A["z"]: c = Vector(A["z"]) * MM
    cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); sc.collection.objects.link(cam); sc.camera = cam
    cam.data.type = "ORTHO"; cam.data.ortho_scale = (A["scf"] * L if "scf" in A else A["sc"]) * MM; cam.data.shift_y = A.get("shy", 0.0); cam.data.clip_end = 100
    cam.location = c + Vector(A["d"]).normalized() * 10; cam.rotation_euler = (c - cam.location).to_track_quat("-Z", "Y").to_euler()
    for az, en in ((35, 1.5), (-120, 0.5)):
        l = bpy.data.objects.new("l", bpy.data.lights.new("l", "SUN")); l.data.energy = en; l.rotation_euler = (math.radians(50), 0, math.radians(az)); sc.collection.objects.link(l)
    bpy.context.view_layer.update()
    # Anker: sichtbare Flächenpunkte je gewünschtem BT (Strahltest), nächster zur Schwerpunkt-Projektion der sichtbaren Punkte
    dg = bpy.context.evaluated_depsgraph_get(); dv = (c - cam.location).normalized(); res = A["res"]; anker = []
    for bt in A["lab"]:
        vis = []
        for ob in [o for o in obs if o["bt"] == bt]:
            polys = list(ob.data.polygons)
            if len(polys) > 2500: polys = random.sample(polys, 2500)
            for pl in polys:
                w3 = ob.matrix_world @ pl.center; p2 = world_to_camera_view(sc, cam, w3)
                if not (0.03 < p2.x < 0.97 and 0.03 < p2.y < 0.97): continue
                hit, loc, nor, idx, hob, mat = sc.ray_cast(dg, w3 - dv * 5.0, dv)
                if hit and hob is not None and hob.name == ob.name and (loc - w3).length < 5e-4: vis.append((p2.x, p2.y))
        if not vis: continue
        xs = np.array([q[0] for q in vis]); ys = np.array([q[1] for q in vis]); k = int(np.argmin((xs - np.median(xs)) ** 2 + (ys - np.median(ys)) ** 2))
        anker.append({"bt": bt, "x": float(xs[k]) * res[0], "y": (1 - float(ys[k])) * res[1]})
    sc.render.filepath = f"{R}/bilder/roh_g5_{V}_{name}.png"; bpy.ops.render.render(write_still=True)
    json.dump({"anker": anker, "res": res, "sc_mm": A["scf"] * L if "scf" in A else A["sc"]}, open(f"{R}/bilder/roh_g5_{V}_{name}.json", "w"))
for a in (os.environ.get("RENDER_NUR") or ",".join(ANS)).split(","): bau(a); print("ANSICHT FERTIG", V, a, flush=True)
print("RENDER FERTIG", V)
