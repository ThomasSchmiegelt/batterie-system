# KI-generiert (Claude Sonnet, 2026-11-23), Entwurf. Auftrag video/AUFTRAG_VIDEO.md (REQ-D13).
# Aufruf: blender -b -P video/szenen.py -- [erstes_bild letztes_bild]   Renderer EEVEE, 1280x720, 25 fps.
# Netze: /home/cae/cae_projekte/batterie_video/netz_LFP (Kopie von cad/baukasten/ausgabe/netz/LFP, Export render_g5_export.py aus pack_LFP.FCStd, Maße aus parameter.json).
# Einzelbilder nach .../frames/%05d.png, vorhandene werden übersprungen (use_overwrite=False).
import bpy, os, sys, json, math, struct
import numpy as np
from mathutils import Vector
D = "/home/cae/cae_projekte/batterie_video"; R = "/home/cae/hermes/batterie"; MM = 0.001; ST = 70.0
IDX = json.load(open(f"{D}/netz_LFP/index.json")); WS = json.load(open(f"{R}/cad/baukasten/farben.json"))["werkstoffe"]
ERG = json.load(open(f"{R}/cad/baukasten/ausgabe/ergebnis_LFP.json")); L, B = ERG["laenge_mm"], ERG["breite_mm"]
arg = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
# Szenen: (Name, erstes Bild, letztes Bild, Bauteil-Präfixe, die in dieser Szene erscheinen)
SZ = [("S1_Zelle", 0, 299, ("BT-100",)), ("S2_Stack", 300, 599, ("BT-2",)), ("S3_BMS", 600, 849, ("BT-3",)), ("S4_Kabel", 850, 1099, ("BT-4",)),
      ("S5_Struktur", 1100, 1449, ("BT-5",)), ("S6_Kuehlung", 1450, 1799, ("BT-6",)), ("S7_Zusatz", 1800, 2049, ("BT-7",)), ("S8_Gesamt", 2050, 2749, ())]
NF = 2750; E0, E1, E2, E3 = 2330, 2450, 2560, 2680    # Explosion: Start, voll, Rückfahrt-Beginn, zusammen
EZ = {"BT-550": 0, "BT-510": 1, "BT-540": 2, "BT-530": 2, "BT-560": 2, "BT-610u": 3, "BT-230u": 3.7, "BT-100": 4.6, "BT-220": 4.6, "BT-250": 4.6, "BT-260": 4.6, "BT-3": 5.4, "BT-4": 5.4,
      "BT-450": 5.4, "BT-230o": 5.5, "BT-610o": 6.3, "BT-520": 7.3, "BT-580": 7.3, "BT-570": 7.3, "BT-590": 7.3, "BT-7": 8.4}   # Stufen wie render_g5.py (Explosionsbild G5.8)
EX = {"BT-620": 300, "BT-630": 300, "BT-640": 300, "BT-65": 300, "BT-661": 520, "BT-662": 520, "BT-663": 520, "BT-664": 420, "BT-665": 520}
def ez(bt, tag):
    for k in (bt + tag, bt, bt[:4], bt[:5]):
        if k in EZ: return EZ[k]
    return 0
def ex(bt):
    for k in (bt, bt[:5]):
        if k in EX: return EX[k]
    return 0
def szene_von(bt):
    for i, s in enumerate(SZ):
        if any(bt.startswith(p) for p in s[3]): return i
    return 0
def stl(fn):
    with open(fn, "rb") as f: f.seek(80); n = struct.unpack("<I", f.read(4))[0]; a = np.frombuffer(f.read(50 * n), dtype=np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")]))
    return a["v"].astype(np.float32)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene; sc.render.engine = "BLENDER_EEVEE"; sc.render.resolution_x, sc.render.resolution_y = 1280, 720; sc.render.fps = 25
if os.environ.get("VIDEO_ENGINE") == "CYCLES": sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = int(os.environ.get("VIDEO_SAMPLES", "12")); sc.cycles.use_denoising = False; sc.cycles.threads = 6   # nur Test ohne GPU
sc.frame_start, sc.frame_end = 0, NF - 1; sc.view_settings.view_transform = "Standard"
sc.eevee.use_soft_shadows = True; sc.eevee.use_gtao = True; sc.eevee.gtao_distance = 0.15; sc.eevee.taa_render_samples = 16; sc.eevee.shadow_cube_size = "1024"; sc.eevee.shadow_cascade_size = "2048"
sc.render.image_settings.file_format = "PNG"; sc.render.filepath = f"{D}/frames/"; sc.render.use_overwrite = False; sc.render.use_placeholder = True
wd = bpy.data.worlds.new("w"); sc.world = wd; wd.use_nodes = True; bg = wd.node_tree.nodes["Background"]; bg.inputs[0].default_value = (0.80, 0.84, 0.90, 1); bg.inputs[1].default_value = 0.45
def key(ob, path, fr, val, idx=-1, const=False):
    setattr(ob, path, val) if idx < 0 else ob.__setattr__(path, val)
    ob.keyframe_insert(path, frame=fr, index=idx)
def ease(a):
    for fc in a.animation_data.action.fcurves:
        for kp in fc.keyframe_points: kp.interpolation = "BEZIER"; kp.handle_left_type = kp.handle_right_type = "AUTO_CLAMPED"
def const(a, nm):
    for fc in a.animation_data.action.fcurves:
        if fc.data_path == nm:
            for kp in fc.keyframe_points: kp.interpolation = "CONSTANT"
obs = []
for e in IDX:
    bt, ws = e["bt"], e["werkstoff"]
    if bt == "BT-590" and ws == "Stahl": continue    # Befestigungsmaterial, 176k Dreiecke, verdeckt die Innenteile
    t = stl(f"{D}/netz_LFP/{e['datei']}"); w = WS.get(ws, {}); col = w.get("farbe", [0.5, 0.5, 0.5])
    teile = {"": t}
    if bt == "BT-100":   # erste Zelle (x-Dicke 14 mm, eine von zwei Zellen in y) einzeln, Rest als zweites Netz
        c = t.mean(1); ein = (c[:, 0] < t[:, :, 0].min() + 14.5) & (c[:, 1] < t[:, :, 1].min() + 685.0); teile = {"e": t[ein], "r": t[~ein]}
    if bt in ("BT-610", "BT-230"): zc = t[:, :, 2].mean(1); zm = (zc.min() + zc.max()) / 2; teile = {"u": t[zc < zm], "o": t[zc >= zm]}
    for tag, tt in teile.items():
        n = len(tt)
        if n == 0: continue
        me = bpy.data.meshes.new(f"{bt}{tag}"); me.vertices.add(3 * n); me.vertices.foreach_set("co", (tt * MM).reshape(-1))
        me.loops.add(3 * n); me.loops.foreach_set("vertex_index", np.arange(3 * n, dtype=np.int32)); me.polygons.add(n)
        me.polygons.foreach_set("loop_start", np.arange(0, 3 * n, 3, dtype=np.int32)); me.polygons.foreach_set("loop_total", np.full(n, 3, dtype=np.int32)); me.update(); me.validate()
        ob = bpy.data.objects.new(f"{bt}_{ws}{tag}", me); sc.collection.objects.link(ob)
        mt = bpy.data.materials.new(ob.name); mt.use_nodes = True; b = mt.node_tree.nodes["Principled BSDF"]
        b.inputs["Base Color"].default_value = (*col, 1); b.inputs["Metallic"].default_value = 0.3 * w.get("metall", 0); b.inputs["Roughness"].default_value = w.get("rauheit", 0.5)
        mt.diffuse_color = (*col, 1); ob.data.materials.append(mt); obs.append((ob, bt, tag))
print("Objekte", len(obs), flush=True)
# Einblenden je Szene (Absenken von oben), Deckel BT-520 liegt in S5 auf und hebt in S6 ab; Explosion in S8
DROP = 0.30; FD = 28
for ob, bt, tag in obs:
    si = szene_von(bt); f0 = SZ[si][1] + 12 + 14 * (int(bt[3:6]) % 10 if bt[3] != "1" else 0) % 70
    if bt == "BT-100" and tag == "r": f0 = 120   # erst die einzelne Zelle, dann der Rest
    spaet = (bt == "BT-610" and tag == "o") or (bt == "BT-710" and ob.name.endswith("Al_eloxiert"))   # Deckelteile (obere Kühlplattenhälfte, Schaltboxdeckel) erscheinen erst in der Explosion, sonst verdecken sie den Inhalt
    lid = bt == "BT-520" or (bt == "BT-230" and tag == "o")   # Deckel und obere Pad-Lage verdecken sonst den Zellblock; erscheinen mit der Struktur (S5), heben in S6 ab
    lidz = ez(bt, tag) * ST * MM
    if lid: f0 = 1330 if bt == "BT-520" else 1300
    if spaet:
        ob.hide_render = True; ob.keyframe_insert("hide_render", frame=0); ob.keyframe_insert("hide_render", frame=E0 - 2)
        ob.hide_render = False; ob.keyframe_insert("hide_render", frame=E0 - 1); ob.location = (0, 0, 0); ob.keyframe_insert("location", frame=E0)
        ob.location = (ex(bt) * MM, 0, ez(bt, tag) * ST * MM); ob.keyframe_insert("location", frame=E1); ob.keyframe_insert("location", frame=E2)
        ob.location = (0, 0, 0); ob.keyframe_insert("location", frame=E3); ease(ob); const(ob, "hide_render"); continue
    ob.hide_render = True; ob.keyframe_insert("hide_render", frame=0)
    ob.hide_render = False; ob.keyframe_insert("hide_render", frame=f0)
    ob.location = (0, 0, DROP); ob.keyframe_insert("location", frame=f0)
    ob.location = (0, 0, 0); ob.keyframe_insert("location", frame=f0 + FD)
    if lid:   # abheben vor S6, auf Explosionshöhe stehen lassen und ausblenden
        ob.location = (0, 0, 0); ob.keyframe_insert("location", frame=1450); ob.location = (0, 0, lidz); ob.keyframe_insert("location", frame=1490)
        ob.hide_render = True; ob.keyframe_insert("hide_render", frame=1491); ob.hide_render = False; ob.keyframe_insert("hide_render", frame=E0 - 1)
        ob.location = (0, 0, lidz); ob.keyframe_insert("location", frame=E1); ob.keyframe_insert("location", frame=E2); ob.location = (0, 0, 0); ob.keyframe_insert("location", frame=E3)
    else:
        ob.location = (0, 0, 0); ob.keyframe_insert("location", frame=E0)
        ob.location = (ex(bt) * MM, 0, ez(bt, tag) * ST * MM); ob.keyframe_insert("location", frame=E1); ob.keyframe_insert("location", frame=E2)
        ob.location = (0, 0, 0); ob.keyframe_insert("location", frame=E3)
    ease(ob); const(ob, "hide_render")
# Kamera: Pose (Ziel, Azimut, Höhe, Abstand) je Eckbild, glatte Interpolation (az 0 = Blick von -y, 90 = von +x)
C = (1.03, 0.715, 0.06)
ZC = (0.05, 0.37, 0.06)
P = [(0, ZC, -50, 25, 1.5), (100, ZC, -25, 25, 1.4), (200, C, -35, 30, 4.4), (299, C, -20, 30, 3.4), (599, C, 20, 32, 3.4), (610, (1.35, 0.72, 0.1), 20, 45, 3.6), (849, (1.3, 0.72, 0.1), 0, 55, 3.4),
     (860, (1.8, 0.7, 0.15), 0, 50, 1.1), (1099, (1.8, 0.7, 0.15), -30, 45, 1.3), (1110, C, -30, 30, 3.0), (1449, C, -100, 30, 3.6),
     (1460, (2.2, 0.715, 0.07), 40, 35, 1.7), (1799, (2.2, 0.715, 0.07), 90, 35, 1.9), (1810, (1.78, 0.72, 0.17), 90, 40, 1.1), (2049, (1.78, 0.72, 0.17), 20, 40, 1.2),
     (2060, C, 20, 30, 3.2), (2329, C, 380, 30, 3.2), (E1, (1.15, 0.715, 0.40), 410, 22, 5.2), (E2, (1.15, 0.715, 0.40), 440, 22, 5.2), (E3, C, 470, 30, 3.2), (2749, C, 500, 32, 3.0)]
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); sc.collection.objects.link(cam); sc.camera = cam; cam.data.lens = 35; cam.data.clip_end = 50; cam.data.clip_start = 0.05
tg = bpy.data.objects.new("tg", None); sc.collection.objects.link(tg)
tc = cam.constraints.new("TRACK_TO"); tc.target = tg; tc.track_axis = "TRACK_NEGATIVE_Z"; tc.up_axis = "UP_Y"
for f, t, az, el, d in P:
    a, e = math.radians(az), math.radians(el); tg.location = t; tg.keyframe_insert("location", frame=f)
    cam.location = Vector(t) + d * Vector((math.sin(a) * math.cos(e), -math.cos(a) * math.cos(e), math.sin(e))); cam.keyframe_insert("location", frame=f)
ease(cam); ease(tg)
for fc in list(cam.animation_data.action.fcurves) + list(tg.animation_data.action.fcurves):   # Szenenwechsel: lineare Übergänge zwischen 599→610 usw. sind kurz (11 Bilder), ok
    pass
for az, en, rot in ((35, 1.8, 50), (-120, 0.6, 60)):
    l = bpy.data.objects.new("l", bpy.data.lights.new("l", "SUN")); l.data.energy = en; l.rotation_euler = (math.radians(rot), 0, math.radians(az)); sc.collection.objects.link(l)
bpy.ops.mesh.primitive_plane_add(size=30, location=(1.03, 0.715, -0.004)); fl = bpy.context.object; fm = bpy.data.materials.new("boden"); fm.use_nodes = True
fm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.55, 0.57, 0.6, 1); fm.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.9; fl.data.materials.append(fm)
a0, a1 = (int(arg[0]), int(arg[1])) if len(arg) >= 2 else (0, NF - 1)
sc.frame_start, sc.frame_end = a0, a1
if os.environ.get("VIDEO_TEST"): sc.render.filepath = f"{D}/test_{a0:04d}.png"; sc.frame_set(a0); bpy.ops.render.render(write_still=True, animation=False); sys.exit()
bpy.ops.render.render(animation=True)
print("RENDER FERTIG", a0, a1, flush=True)
