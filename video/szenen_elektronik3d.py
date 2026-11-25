# KI-generiert (Claude Sonnet 5.5, 2026-11-25), Entwurf. Auftrag video/AUFTRAG_VIDEO_ELEKTRONIK.md (Nachtrag 1, Stufe 2), REQ-D13, BAT-DOC-13c.
# Aufruf: SZENE=pack|cmu|bms [VIDEO_STEP=2] blender -b -P video/szenen_elektronik3d.py -- [erstes letztes]   (EEVEE, 1280x720, 25 fps, RGBA mit durchsichtigem Grund)
# Einzelbilder nach /home/cae/cae_projekte/batterie_video/elektronik3d/<SZENE>/%04d.png, vorhandene werden übersprungen.
# Quellen (nur lesen): Pack-Netze cad/pack e2d_e3c (Kopie in /home/cae/cae_projekte/batterie/e2/netz_LFP_e2d_e3c_gesamt.json, FreeCAD-Tessellierung aus pack_LFP_e2d_e3c.FCStd, wie E3),
#   Zellen STL (video netz_LFP, aus pack_LFP.FCStd), CMU: e3/bauteile_LFP.json + e3/explosion_LFP.json, BMS: e3c/bauteile.json + e3c/explosion.json (aus den KiCad-STEP, Muster explosion_blender.py).
# Darstellung (keine Rechengröße): Lagenabstand 11 mm, Kupferdicke überhöht 0,35 mm, Farben, Zeitplan, Kamerapfade. Maße der Teile stammen aus den Netzen.
import bpy, os, sys, json, math, struct
import numpy as np
from mathutils import Vector
MM = 0.001; DV = "/home/cae/cae_projekte/batterie_video"; E2 = "/home/cae/cae_projekte/batterie/e2"
SZ = os.environ["SZENE"]; STEP = int(os.environ.get("VIDEO_STEP", "1")); SAMP = int(os.environ.get("VIDEO_SAMPLES", "24"))
NFR = {"pack": 750, "cmu": 375, "bms": 375}[SZ]; FPS = 25
arg = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene; sc.render.engine = "BLENDER_EEVEE"; sc.render.resolution_x, sc.render.resolution_y = 1280, 720; sc.render.fps = FPS
sc.view_settings.view_transform = "Standard"; sc.eevee.use_soft_shadows = True; sc.eevee.use_gtao = True; sc.eevee.gtao_distance = 0.15; sc.eevee.taa_render_samples = SAMP
sc.render.image_settings.file_format = "PNG"; sc.render.image_settings.color_mode = "RGBA"; sc.render.film_transparent = True
sc.render.filepath = f"{DV}/elektronik3d/{SZ}/"; sc.render.use_overwrite = False; sc.render.use_placeholder = True; sc.frame_step = STEP
wd = bpy.data.worlds.new("w"); sc.world = wd; wd.use_nodes = True; bg = wd.node_tree.nodes["Background"]; bg.inputs[0].default_value = (0.80, 0.84, 0.90, 1); bg.inputs[1].default_value = 0.45

def mat(name, col, alpha=1.0, metal=0.0, rough=0.5, emit=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*col, 1); b.inputs["Metallic"].default_value = metal; b.inputs["Roughness"].default_value = rough; b.inputs["Alpha"].default_value = alpha
    if emit: b.inputs["Emission Color"].default_value = (*col, 1); b.inputs["Emission Strength"].default_value = emit
    m.blend_method = "HASHED"; m.shadow_method = "HASHED"; m.diffuse_color = (*col, 1); return m
def mesh(name, P, T, m, faces=None, parent=None):
    me = bpy.data.meshes.new(name); me.from_pydata(np.asarray(P, dtype=np.float64).tolist(), [], T if faces else np.asarray(T).tolist()); me.update()
    ob = bpy.data.objects.new(name, me); sc.collection.objects.link(ob); ob.data.materials.append(m)
    if parent: ob.parent = parent
    else: ob.scale = (MM, MM, MM)
    return ob
def soup(name, tri, m):   # Dreieckssuppe (n,3,3) in mm, wie szenen.py
    n = len(tri); me = bpy.data.meshes.new(name); me.vertices.add(3 * n); me.vertices.foreach_set("co", tri.reshape(-1))
    me.loops.add(3 * n); me.loops.foreach_set("vertex_index", np.arange(3 * n, dtype=np.int32)); me.polygons.add(n)
    me.polygons.foreach_set("loop_start", np.arange(0, 3 * n, 3, dtype=np.int32)); me.update(); me.validate()
    ob = bpy.data.objects.new(name, me); sc.collection.objects.link(ob); ob.data.materials.append(m); ob.scale = (MM, MM, MM); return ob
def stl(fn):
    with open(fn, "rb") as f: f.seek(80); n = struct.unpack("<I", f.read(4))[0]; a = np.frombuffer(f.read(50 * n), dtype=np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")]))
    return a["v"].astype(np.float32)
def ease(ob):
    if ob.animation_data and ob.animation_data.action:
        for fc in ob.animation_data.action.fcurves:
            for kp in fc.keyframe_points:
                if fc.data_path != "hide_render": kp.interpolation = "BEZIER"; kp.handle_left_type = kp.handle_right_type = "AUTO_CLAMPED"
                else: kp.interpolation = "CONSTANT"
def fr(t): return int(round(t * FPS))
def erscheint(ob, t0, drop=0.30, dt=1.0, alpha_ins=None):
    """Teil erscheint bei t0 s: sichtbar ab t0, fällt von oben (drop m), oder blendet über Alpha ein (alpha_ins = Material)."""
    f0 = fr(t0); ob.hide_render = True; ob.keyframe_insert("hide_render", frame=0); ob.hide_render = False; ob.keyframe_insert("hide_render", frame=f0)
    if alpha_ins is not None:
        al = alpha_ins.node_tree.nodes["Principled BSDF"].inputs["Alpha"]; a1 = al.default_value; al.default_value = 0.0; al.keyframe_insert("default_value", frame=f0); al.default_value = a1; al.keyframe_insert("default_value", frame=f0 + fr(dt))
    elif drop:
        z = ob.location.z; ob.location.z = z + drop; ob.keyframe_insert("location", index=2, frame=f0); ob.location.z = z; ob.keyframe_insert("location", index=2, frame=f0 + fr(dt))
    ease(ob)
def kamera(name, poses, t_off=0.0):
    """poses: (t s, Ziel, Azimut, Höhe, Abstand m); az 0 = Blick von -y, 90 = von +x."""
    cam = bpy.data.objects.new(name, bpy.data.cameras.new(name)); sc.collection.objects.link(cam); cam.data.lens = 35; cam.data.clip_end = 50; cam.data.clip_start = 0.01
    tg = bpy.data.objects.new(name + "_ziel", None); sc.collection.objects.link(tg); tc = cam.constraints.new("TRACK_TO"); tc.target = tg; tc.track_axis = "TRACK_NEGATIVE_Z"; tc.up_axis = "UP_Y"
    for t, ziel, az, el, d in poses:
        a, e = math.radians(az), math.radians(el); f = fr(t_off + t); tg.location = ziel; tg.keyframe_insert("location", frame=f)
        cam.location = Vector(ziel) + d * Vector((math.sin(a) * math.cos(e), -math.cos(a) * math.cos(e), math.sin(e))); cam.keyframe_insert("location", frame=f)
    ease(cam); ease(tg); return cam
for az, en, rot in ((35, 1.8, 50), (-120, 0.6, 60)):
    l = bpy.data.objects.new("l", bpy.data.lights.new("l", "SUN")); l.data.energy = en; l.rotation_euler = (math.radians(rot), 0, math.radians(az)); sc.collection.objects.link(l)

# ---------------- Pack ----------------
FARBE = {"Unterfahrschutz": ((0.3, 0.3, 0.33), 0.5, 0.4), "Boden": ((0.5, 0.52, 0.56), 0.6, 0.4), "Seitenrahmen": ((0.55, 0.57, 0.62), 0.7, 0.4), "Kuehlplatte": ((0.7, 0.74, 0.8), 0.9, 0.3),
         "Pad": ((0.9, 0.55, 0.2), 0.0, 0.7), "Deckel": ((0.45, 0.48, 0.52), 0.6, 0.4), "Zellverbinder": ((0.85, 0.5, 0.25), 0.9, 0.3), "Quertraeger": ((0.6, 0.62, 0.66), 0.6, 0.4),
         "E2_CMU": ((0.95, 0.45, 0.05), 0.0, 0.4), "E2_Schaltbox_Inhalt": ((0.2, 0.55, 0.3), 0.2, 0.5), "E2_Schraube": ((0.35, 0.35, 0.38), 0.8, 0.4), "E2_HV_Leitung": ((0.85, 0.15, 0.1), 0.0, 0.6),
         "E2_Kabelschuh": ((0.8, 0.5, 0.3), 0.9, 0.3), "E2_Clip": ((0.2, 0.2, 0.22), 0.0, 0.6), "E2_Stromschiene": ((0.85, 0.5, 0.25), 0.9, 0.3), "E2_Schrumpfschlauch": ((0.1, 0.1, 0.12), 0.0, 0.6),
         "E2_Schaltbox": ((0.25, 0.28, 0.33), 0.7, 0.4), "E2_Dichtung": ((0.08, 0.08, 0.08), 0.0, 0.8), "E2_Schaltbox_Deckel": ((0.3, 0.33, 0.38), 0.7, 0.4), "E2_Stecker_Sensor": ((0.15, 0.15, 0.18), 0.0, 0.5),
         "E2_Lasche": ((0.85, 0.5, 0.25), 0.9, 0.3), "E2_Trennbruecke": ((0.85, 0.5, 0.25), 0.9, 0.3), "E2_Trennbrueckenschraube": ((0.35, 0.35, 0.38), 0.8, 0.4), "E2_Servicedeckel": ((0.3, 0.33, 0.38), 0.7, 0.4),
         "E2_FPC": ((0.9, 0.65, 0.1), 0.0, 0.5), "E2_FPC_Halter": ((0.2, 0.2, 0.22), 0.0, 0.6), "E2_FPC_Detail": ((0.9, 0.65, 0.1), 0.0, 0.5), "E2_Daisy": ((0.1, 0.4, 0.2), 0.0, 0.5)}
CEN = (1.025, 0.715, 0.08)

def pack_laden(nur_gehaeuse=False):
    N = json.load(open(f"{E2}/netz_LFP_e2d_e3c_gesamt.json")); ob = {}
    for g, v in N.items():
        if not v["punkte"]: continue
        col, me_, ro = FARBE.get(g, ((0.5, 0.5, 0.5), 0.3, 0.5)); m = mat(g, col, 1.0, 0.3 * me_, ro, 0.0); ob[g] = mesh(g, v["punkte"], v["dreiecke"], m)
    return N, ob

if SZ == "pack":
    N, ob = pack_laden()
    # Zellen (Hüllkörper aus pack_LFP.FCStd-Netz), in 6 Bändern entlang x
    t = stl(f"{DV}/netz_LFP/BT-100__Zelle_LFP.stl"); cx = t[:, :, 0].mean(1); x0, x1 = float(cx.min()), float(cx.max()); mz = mat("zelle", (0.30, 0.50, 0.85), 1.0, 0.0, 0.4)
    NB = 6; zb = []
    for k in range(NB):
        sel = (cx >= x0 + (x1 - x0) * k / NB) & (cx <= x0 + (x1 - x0) * (k + 1) / NB + (1e-3 if k == NB - 1 else -1e-3)); zb.append(soup(f"Zellen_{k}", t[sel], mz))
    ZT = {"Unterfahrschutz": 0.5, "Boden": 0.8, "Seitenrahmen": 1.1, "Kuehlplatte": 8.6, "Pad": 9.3, "Zellverbinder": 10.0, "Quertraeger": 10.7, "E2_CMU": 11.6, "E2_FPC": 12.4, "E2_FPC_Halter": 12.4, "E2_FPC_Detail": 12.4, "E2_Daisy": 12.4,
          "E2_Schaltbox": 13.2, "E2_Dichtung": 13.5, "E2_Schaltbox_Inhalt": 13.8, "E2_Stromschiene": 14.2, "E2_Schrumpfschlauch": 14.2, "E2_Schraube": 14.4, "E2_HV_Leitung": 14.8, "E2_Kabelschuh": 14.8, "E2_Clip": 15.0,
          "E2_Lasche": 15.0, "E2_Stecker_Sensor": 15.6, "E2_Trennbruecke": 15.9, "E2_Trennbrueckenschraube": 16.1, "E2_Servicedeckel": 16.3, "E2_Schaltbox_Deckel": 18.4}
    for g_ in ("Kuehlplatte", "Pad"): ob[g_].data.materials[0].node_tree.nodes["Principled BSDF"].inputs["Alpha"].default_value = 0.22   # obere Kühlplatte durchsichtig, sonst verdeckt sie Zellen und CMU (Darstellung)
    for k, o in enumerate(zb): erscheint(o, 2.0 + 1.1 * k, 0.35)
    for g, o in ob.items():
        if g == "Deckel": erscheint(o, 17.0, 0, 1.2, alpha_ins=o.data.materials[0]); continue
        erscheint(o, ZT.get(g, 12.0), 0.30 if g not in ("E2_CMU",) else 0.45)
    # Deckel öffnet: Klappe um die hintere Längskante (y = 1430 mm, z = 119 mm), Schaltboxdeckel hebt ab
    hinge = bpy.data.objects.new("scharnier", None); sc.collection.objects.link(hinge); hinge.location = (1.025, 1.43, 0.119)
    bpy.context.view_layer.update(); d = ob["Deckel"]; d.parent = hinge; d.matrix_parent_inverse = hinge.matrix_world.inverted()
    hinge.rotation_euler = (0, 0, 0); hinge.keyframe_insert("rotation_euler", frame=fr(22)); hinge.rotation_euler = (-math.radians(60), 0, 0); hinge.keyframe_insert("rotation_euler", frame=fr(25.6)); ease(hinge)
    sd = ob["E2_Schaltbox_Deckel"]; z = sd.location.z; sd.keyframe_insert("location", index=2, frame=fr(25.0)); sd.location.z = z + 0.30; sd.keyframe_insert("location", index=2, frame=fr(27.5)); ease(sd)
    cam = kamera("cam", [(0, CEN, -50, 28, 3.8), (8, CEN, -35, 30, 3.5), (16, CEN, -10, 32, 3.4), (22, CEN, 5, 42, 3.9), (26, (1.1, 0.8, 0.2), 25, 46, 3.8), (30, (1.3, 0.8, 0.2), 45, 46, 3.5)]); sc.camera = cam

# ---------------- Platinen-Modell ----------------
def quader_v(x0, y0, z0, x1, y1, z1):
    v = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    return v, [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
class Akku:
    def __init__(s): s.v = []; s.f = []
    def add(s, v, f): o = len(s.v); s.v += v; s.f += [tuple(i + o for i in q) for q in f]
def platine(prefix, Dd, Bd, off, S=11.0, TC=0.35, zone=None, mitte_pad=False):
    """Platine in mm (Wurzel-Leer mit Maßstab 1e-3 bei off). Gibt Wurzel, Ebenen (Name -> (Objekt, Index im Explosionsstapel)) und Maße zurück."""
    W, H = Dd["w"], Dd["h"]; root = bpy.data.objects.new(prefix + "_wurzel", None); sc.collection.objects.link(root); root.location = off; root.scale = (MM, MM, MM)
    lx = lambda x: x - Dd["x0"]; ly = lambda y: Dd["y0"] + H - y
    ZC = {"F.Cu": 1.51 + TC / 2, "In1.Cu": 1.0, "In2.Cu": 0.55, "B.Cu": 0.0 - TC / 2 + TC / 2 + 0.0}
    mcu = mat(prefix + "cu", (0.85, 0.42, 0.22), 1.0, 0.9, 0.3); mfr = mat(prefix + "fr4", (0.12, 0.45, 0.2), 0.55, 0.0, 0.5); mbt = mat(prefix + "bt", (0.18, 0.18, 0.2), 1.0, 0.0, 0.5)
    L = {}; ak = {k: Akku() for k in ("F.Cu", "In1.Cu", "In2.Cu", "B.Cu")}
    for ln, x1, y1, x2, y2, w in Dd["bahn"]:
        x1, y1, x2, y2 = lx(x1), ly(y1), lx(x2), ly(y2); dx, dy = x2 - x1, y2 - y1; Ln = math.hypot(dx, dy) or 1e-6; nx, ny = -dy / Ln * w / 2, dx / Ln * w / 2; ex, ey = dx / Ln * w / 2, dy / Ln * w / 2
        p = [(x1 - ex + nx, y1 - ey + ny), (x2 + ex + nx, y2 + ey + ny), (x2 + ex - nx, y2 + ey - ny), (x1 - ex - nx, y1 - ey - ny)]; z = ZC[ln]
        ak[ln].add([(a, b, z - TC / 2) for a, b in p] + [(a, b, z + TC / 2) for a, b in p], [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)])
    for ln, x, y, w, h, ref in Dd["pads"]:
        v, f = quader_v(lx(x) - w / 2, ly(y) - h / 2, ZC[ln] - TC / 2, lx(x) + w / 2, ly(y) + h / 2, ZC[ln] + TC / 2); ak[ln].add(v, f)
    for ln, net, pts in Dd["zonen"]:
        n = len(pts)
        if n < 3: continue
        ak[ln].add([(lx(a), ly(b), ZC[ln] - TC / 2) for a, b in pts] + [(lx(a), ly(b), ZC[ln] + TC / 2) for a, b in pts], [tuple(range(n))[::-1], tuple(range(n, 2 * n))] + [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)])
    idx = {"Pad": 0, "B.Cu": 1, "In2.Cu": 2, "In1.Cu": 3, "Substrat": 4, "F.Cu": 5, "Bauteile": 6} if mitte_pad else {"B.Cu": 0, "In2.Cu": 1, "In1.Cu": 2, "Substrat": 3, "F.Cu": 4, "Bauteile": 5}
    for ln, a in ak.items():
        if a.v: L[ln] = (mesh(prefix + ln, a.v, a.f, mcu, faces=True, parent=root), idx[ln])
    v, f = quader_v(0, 0, 0.0, W, H, 1.51); L["Substrat"] = (mesh(prefix + "Substrat", v, f, mfr, faces=True, parent=root), idx["Substrat"])
    if mitte_pad:
        mp = mat(prefix + "pad", (0.85, 0.7, 0.12), 1.0, 0.0, 0.5); v, f = quader_v(0, 0, -1.2, W, H, -0.2); L["Pad"] = (mesh(prefix + "Pad", v, f, mp, faces=True, parent=root), idx["Pad"])
    pb = Bd["platine_bbox"]; pts = [(p[0] - pb[0], p[1] - pb[1], p[2]) for p in Bd["punkte"]]; L["Bauteile"] = (mesh(prefix + "Bauteile", pts, Bd["dreiecke"], mbt, parent=root), idx["Bauteile"])
    if zone:
        mzn = mat(prefix + "sperr", (1.0, 0.05, 0.05), 0.28, 0.0, 0.5); v, f = quader_v(zone[0], 0, -4, zone[1], H, 6 * S + 10); L["Sperrzone"] = (mesh(prefix + "Sperrzone", v, f, mzn, faces=True, parent=root), -1)
    return root, L, (W, H)
def explodieren(L, t0, t1, t2, t3, S=11.0, niveau=None):
    """Lagen fahren von t0 bis t1 auseinander, bleiben bis t2, fahren bis t3 zusammen (s)."""
    for k, (o, i) in L.items():
        if i < 0: continue
        o.location.z = 0; o.keyframe_insert("location", index=2, frame=fr(t0)); o.location.z = i * S; o.keyframe_insert("location", index=2, frame=fr(t1))
        o.keyframe_insert("location", index=2, frame=fr(t2)); o.location.z = 0; o.keyframe_insert("location", index=2, frame=fr(t3)); ease(o)
def sperr_ein(L, t0, t1):
    o = L["Sperrzone"][0]; al = o.data.materials[0].node_tree.nodes["Principled BSDF"].inputs["Alpha"]; a1 = al.default_value
    al.default_value = 0; al.keyframe_insert("default_value", frame=fr(t0)); al.default_value = a1; al.keyframe_insert("default_value", frame=fr(t1))

# ---------------- CMU: Pack mit Endzonen, Anflug, dann Platine mit Leiterbahnen ----------------
def gehaeuse_blass(N, ob):
    for g, o in ob.items():
        if g in ("E2_CMU",): continue
        mm_ = o.data.materials[0]; b = mm_.node_tree.nodes["Principled BSDF"]
        a = 0.10 if g in ("Seitenrahmen", "E2_Schaltbox", "E2_Schaltbox_Inhalt", "E2_FPC", "E2_FPC_Detail") else 0.0
        b.inputs["Alpha"].default_value = a
        if a == 0.0: o.hide_render = True
def cmu_zentrum(N, links=True):
    P = np.array(N["E2_CMU"]["punkte"]); T = np.array(N["E2_CMU"]["dreiecke"]); c = P[T].mean(1); cx = 1025.0; cy = 715.0
    sel = ((c[:, 0] < cx) if links else (c[:, 0] >= cx)) & (c[:, 1] < cy); p = P[T[sel]].reshape(-1, 3); return (p.min(0) + p.max(0)) / 2 * MM, p.min(0) * MM, p.max(0) * MM

if SZ == "cmu":
    N, ob = pack_laden(); gehaeuse_blass(N, ob)
    cz, lo, hi = cmu_zentrum(N); mc = ob["E2_CMU"].data.materials[0]; bsd = mc.node_tree.nodes["Principled BSDF"]
    erscheint(ob["E2_CMU"], 0.8, 0.0, 1.0, alpha_ins=mc)
    bsd.inputs["Emission Color"].default_value = (1.0, 0.45, 0.05, 1); es = bsd.inputs["Emission Strength"]
    for t, v in ((0.8, 0.0), (1.8, 1.2), (3.0, 0.3), (4.2, 1.0), (5.5, 0.3), (6.4, 0.3)): es.default_value = v; es.keyframe_insert("default_value", frame=fr(t))
    camA = kamera("camA", [(0, CEN, -40, 32, 3.8), (3.2, CEN, -28, 30, 3.5), (6.4, tuple(cz), -42, 28, 0.42)])
    OFF = Vector((8.0, 0.0, 0.0)); Dd = json.load(open("/home/cae/cae_projekte/batterie/e3/explosion_LFP.json")); Bd = json.load(open("/home/cae/cae_projekte/batterie/e3/bauteile_LFP.json"))
    root, L, (W, H) = platine("cmu", Dd, Bd, OFF, mitte_pad=True); w_, h_ = W * MM, H * MM; B0 = Vector((OFF.x, OFF.y, OFF.z + 0.002))
    # Kamera B: Überflug der Leiterbahnen (Oberseite), Annäherung an die Kanäle, dann Rückzug zur Explosion (10,3 bis 14 s)
    camB = kamera("camB", [(6.5, tuple(B0 + Vector((0.02, 0.03, 0.0))), -35, 38, 0.22), (8.6, tuple(B0 + Vector((0.05, 0.03, 0.0))), -22, 42, 0.12), (10.2, tuple(B0 + Vector((0.07, 0.025, 0.0))), -30, 35, 0.10),
                          (11.5, tuple(B0 + Vector((0.06, 0.03, 0.03))), -35, 28, 0.30), (14.0, tuple(B0 + Vector((0.06, 0.03, 0.03))), -45, 25, 0.32), (15, tuple(B0 + Vector((0.06, 0.03, 0.03))), -50, 25, 0.34)])
    explodieren(L, 10.4, 12.8, 14.0, 14.99)
    # CMU-Teile der Platine erscheinen erst mit Kamera B; Kamera-Umschaltung per Marker
    sc.camera = camA; m = sc.timeline_markers.new("A", frame=0); m.camera = camA; m = sc.timeline_markers.new("B", frame=fr(6.5)); m.camera = camB
    for o, _i in L.values():
        o.hide_render = True; o.keyframe_insert("hide_render", frame=0); o.hide_render = False; o.keyframe_insert("hide_render", frame=fr(6.5)); ease(o)
    for k, o in ob.items(): o.hide_render = o.hide_render
    # Pack-Teile ab 6,5 s ausblenden
    for k, o in ob.items():
        if k == "E2_CMU" or o.hide_render is False:
            o.hide_render = False; o.keyframe_insert("hide_render", frame=fr(6.4)); o.hide_render = True; o.keyframe_insert("hide_render", frame=fr(6.5)); ease(o)

# ---------------- BMS: Schaltbox öffnet, dann Platine mit Sperrzone ----------------
if SZ == "bms":
    N, ob = pack_laden(); gehaeuse_blass(N, ob)
    for k in ("E2_Schaltbox", "E2_Schaltbox_Inhalt"):
        b = ob[k].data.materials[0].node_tree.nodes["Principled BSDF"]; b.inputs["Alpha"].default_value = 1.0; ob[k].hide_render = False
    bm = ob["E2_Schaltbox_Inhalt"].data.materials[0].node_tree.nodes["Principled BSDF"]; bm.inputs["Emission Color"].default_value = (0.2, 0.9, 0.4, 1); es = bm.inputs["Emission Strength"]
    for t, v in ((0.0, 0.0), (3.0, 0.0), (4.0, 1.2), (5.0, 0.2), (6.4, 0.2)): es.default_value = v; es.keyframe_insert("default_value", frame=fr(t))
    for k in ("E2_Schaltbox_Deckel", "E2_Dichtung", "E2_Servicedeckel", "E2_Schraube", "E2_Stecker_Sensor", "E2_Stromschiene", "E2_Schrumpfschlauch"):
        if k in ob: ob[k].hide_render = False; ob[k].data.materials[0].node_tree.nodes["Principled BSDF"].inputs["Alpha"].default_value = 1.0
    sd = ob["E2_Schaltbox_Deckel"]; z = sd.location.z; sd.keyframe_insert("location", index=2, frame=fr(0.8)); sd.location.z = z + 0.35; sd.keyframe_insert("location", index=2, frame=fr(2.8))
    sd.hide_render = False; sd.keyframe_insert("hide_render", frame=fr(3.0)); sd.hide_render = True; sd.keyframe_insert("hide_render", frame=fr(3.01)); ease(sd)
    sb = N["E2_Schaltbox"]["punkte"]; P = np.array(N["E2_Schaltbox_Inhalt"]["punkte"]) * MM; bc = (P.min(0) + P.max(0)) / 2
    camA = kamera("camA", [(0, tuple(bc), -35, 38, 1.2), (3.0, tuple(bc), -20, 42, 0.8), (6.4, tuple(bc), -10, 50, 0.45)])
    OFF = Vector((8.0, 0.0, 0.0)); Dd = json.load(open("/home/cae/cae_projekte/batterie/e3c/explosion.json")); Bd = json.load(open("/home/cae/cae_projekte/batterie/e3c/bauteile.json"))
    root, L, (W, H) = platine("bms", Dd, Bd, OFF, zone=(100.0, 110.0)); B0 = Vector((OFF.x, OFF.y, OFF.z + 0.002))
    camB = kamera("camB", [(6.5, tuple(B0 + Vector((0.08, 0.05, 0.0))), -35, 40, 0.30), (9.5, tuple(B0 + Vector((0.10, 0.05, 0.0))), -20, 45, 0.20), (10.5, tuple(B0 + Vector((0.08, 0.05, 0.03))), -35, 30, 0.38),
                          (14.0, tuple(B0 + Vector((0.08, 0.05, 0.03))), -45, 25, 0.40), (15, tuple(B0 + Vector((0.08, 0.05, 0.03))), -50, 25, 0.42)])
    explodieren(L, 10.4, 12.8, 14.0, 14.99); sperr_ein(L, 7.0, 8.5)
    sc.camera = camA; m = sc.timeline_markers.new("A", frame=0); m.camera = camA; m = sc.timeline_markers.new("B", frame=fr(6.5)); m.camera = camB
    for o, _i in L.values():
        o.hide_render = True; o.keyframe_insert("hide_render", frame=0); o.hide_render = False; o.keyframe_insert("hide_render", frame=fr(6.5)); ease(o)
    for k, o in ob.items():
        if not o.hide_render:
            o.hide_render = False; o.keyframe_insert("hide_render", frame=fr(6.4)); o.hide_render = True; o.keyframe_insert("hide_render", frame=fr(6.5)); ease(o)

a0, a1 = (int(arg[0]), int(arg[1])) if len(arg) >= 2 else (0, NFR - 1)
sc.frame_start, sc.frame_end = a0, a1
if os.environ.get("VIDEO_TEST"):
    for f in [int(x) for x in os.environ["VIDEO_TEST"].split(",")]:
        sc.render.filepath = f"{DV}/elektronik3d/test_{SZ}_{f:04d}.png"; sc.frame_set(f); bpy.ops.render.render(write_still=True)
    sys.exit()
bpy.ops.render.render(animation=True)
print("RENDER FERTIG", SZ, a0, a1, flush=True)
