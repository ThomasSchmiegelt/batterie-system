# KI-generiert (Claude Sonnet 5.5, 2026-11-25), Entwurf. Auftrag video/AUFTRAG_VIDEO_ELEKTRONIK.md (Nachtrag 1, Stufe 2), REQ-D13, BAT-DOC-13c.
# Aufruf: SZENE=pack|cmu|bms [VIDEO_STEP=2] blender -b -P video/szenen_elektronik3d.py -- [erstes letztes]   (EEVEE, 1280x720, 25 fps, RGBA mit durchsichtigem Grund)
# Einzelbilder nach /home/cae/cae_projekte/batterie_video/elektronik3d/<SZENE>/%04d.png, vorhandene werden übersprungen.
# Quellen (nur lesen): Pack-Netze cad/pack e2d_e3c (Kopie in /home/cae/cae_projekte/batterie/e2/netz_LFP_e2d_e3c_gesamt.json, FreeCAD-Tessellierung aus pack_LFP_e2d_e3c.FCStd, wie E3),
#   Zellen STL (video netz_LFP, aus pack_LFP.FCStd), CMU: e3/bauteile_LFP.json + e3/explosion_LFP.json, BMS: e3c/bauteile.json + e3c/explosion.json (aus den KiCad-STEP, Muster explosion_blender.py).
# Darstellung (keine Rechengröße): Lagenabstand 11 mm, Kupferdicke überhöht 0,35 mm, Farben, Zeitplan, Kamerapfade. Maße der Teile stammen aus den Netzen.
import bpy, os, sys, json, math, struct
import numpy as np
from mathutils import Vector, Matrix
MM = 0.001; DV = "/home/cae/cae_projekte/batterie_video"; E2 = "/home/cae/cae_projekte/batterie/e2"
SZ = os.environ["SZENE"]; STEP = int(os.environ.get("VIDEO_STEP", "1")); SAMP = int(os.environ.get("VIDEO_SAMPLES", "24"))
NFR = {"pack": 750, "steuer": 750}[SZ]; FPS = 25
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

def pack_laden(masken=()):
    """Pack-Netz laden. masken: (Gruppe, neuer Name, untere Ecke, obere Ecke in mm): Dreiecke mit Schwerpunkt in der Box werden als eigenes Objekt abgetrennt (gleiches Material)."""
    N = json.load(open(f"{E2}/netz_LFP_e2d_e3c_gesamt.json")); ob = {}; mats = {}
    for gname, nm, lo, hi in masken:
        v = N[gname]; P = np.array(v["punkte"]); T = np.array(v["dreiecke"]); c = P[T].mean(1); m = np.all((c >= np.array(lo)) & (c <= np.array(hi)), axis=1)
        pp = P[T[m]].reshape(-1, 3); print("MASKE", nm, int(m.sum()), "Dreiecke, bbox", pp.min(0).round(2).tolist(), pp.max(0).round(2).tolist(), flush=True)
        N[gname] = dict(punkte=v["punkte"], dreiecke=T[~m].tolist()); N[nm] = dict(punkte=v["punkte"], dreiecke=T[m].tolist(), _mat=gname)
    for g, v in N.items():
        if not v["punkte"]: continue
        gm = v.get("_mat", g)
        if gm not in mats: col, me_, ro = FARBE.get(gm, ((0.5, 0.5, 0.5), 0.3, 0.5)); mats[gm] = mat(gm, col, 1.0, 0.3 * me_, ro, 0.0)
        ob[g] = mesh(g, v["punkte"], v["dreiecke"], mats[gm])
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
    W, H = Dd["w"], Dd["h"]; root = bpy.data.objects.new(prefix + "_wurzel", None); sc.collection.objects.link(root); root.matrix_basis = off   # off: 4x4 (Lage im Pack-Koordinatensystem, Maßstab mm -> m)
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
    # Vias als dünne Kupferstäbe (Muster explosion_blender.py E3: Thermovias = Via im Pad eines 2512-Widerstands, orange); Stab Höhe 1, Skalierung in z folgt dem Lagenabstand
    mth = mat(prefix + "thermo", (1.0, 0.25, 0.05), 1.0, 0.9, 0.3); rp = [(p[1], p[2], p[3], p[4]) for p in Dd["pads"] if p[5].startswith("R") and p[3] > 3.0]
    va, vt = Akku(), Akku()
    for x, y, d, dr, net in Dd["vias"]:
        th = any(abs(x - px) <= w / 2 and abs(y - py) <= h / 2 for px, py, w, h in rp); r = d / 2 * (0.55 if th else 0.35); xx, yy = lx(x), ly(y); n = 6
        (vt if th else va).add([(xx + r * math.cos(2 * math.pi * i / n), yy + r * math.sin(2 * math.pi * i / n), z) for z in (0.0, 1.0) for i in range(n)],
                               [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)] + [tuple(range(n))[::-1], tuple(range(n, 2 * n))])
    viao = {}
    idx = {"Pad": 0, "B.Cu": 1, "In2.Cu": 2, "In1.Cu": 3, "Substrat": 4, "F.Cu": 5, "Bauteile": 6} if mitte_pad else {"B.Cu": 0, "In2.Cu": 1, "In1.Cu": 2, "Substrat": 3, "F.Cu": 4, "Bauteile": 5}
    for ln, a in ak.items():
        if a.v: L[ln] = (mesh(prefix + ln, a.v, a.f, mcu, faces=True, parent=root), idx[ln])
    v, f = quader_v(0, 0, 0.0, W, H, 1.51); L["Substrat"] = (mesh(prefix + "Substrat", v, f, mfr, faces=True, parent=root), idx["Substrat"])
    if mitte_pad:
        mp = mat(prefix + "pad", (0.85, 0.7, 0.12), 1.0, 0.0, 0.5); v, f = quader_v(0, 0, -1.2, W, H, -0.2); L["Pad"] = (mesh(prefix + "Pad", v, f, mp, faces=True, parent=root), idx["Pad"])
    if va.v: L["Vias"] = (mesh(prefix + "Vias", va.v, va.f, mcu, faces=True, parent=root), -2)
    if vt.v: L["Thermovias"] = (mesh(prefix + "Thermovias", vt.v, vt.f, mth, faces=True, parent=root), -2)
    for k_ in ("Vias", "Thermovias"):
        if k_ in L: L[k_][0].scale.z = 1.51 + TC
    pb = Bd["platine_bbox"]; pts = [(p[0] - pb[0], p[1] - pb[1], p[2]) for p in Bd["punkte"]]; L["Bauteile"] = (mesh(prefix + "Bauteile", pts, Bd["dreiecke"], mbt, parent=root), idx["Bauteile"])
    if zone:
        mzn = mat(prefix + "sperr", (1.0, 0.05, 0.05), 0.28, 0.0, 0.5); v, f = quader_v(zone[0], 0, -4, zone[1], H, 6 * S + 10); L["Sperrzone"] = (mesh(prefix + "Sperrzone", v, f, mzn, faces=True, parent=root), -1)
    return root, L, (W, H)
def explodieren(L, t0, t1, t2, t3, S=11.0, niveau=None):
    """Lagen fahren von t0 bis t1 auseinander, bleiben bis t2, fahren bis t3 zusammen (s)."""
    top = L["F.Cu"][1]
    for k, (o, i) in L.items():
        if i == -2:   # Via-Stäbe wachsen mit dem Lagenabstand (Stab von B.Cu bis F.Cu)
            o.scale.z = 1.51 + 0.35; o.keyframe_insert("scale", index=2, frame=fr(t0)); o.scale.z = top * S + 1.51 + 0.35; o.keyframe_insert("scale", index=2, frame=fr(t1))
            o.keyframe_insert("scale", index=2, frame=fr(t2)); o.scale.z = 1.51 + 0.35; o.keyframe_insert("scale", index=2, frame=fr(t3)); ease(o); continue
        if i < 0: continue
        o.location.z = 0; o.keyframe_insert("location", index=2, frame=fr(t0)); o.location.z = i * S; o.keyframe_insert("location", index=2, frame=fr(t1))
        o.keyframe_insert("location", index=2, frame=fr(t2)); o.location.z = 0; o.keyframe_insert("location", index=2, frame=fr(t3)); ease(o)
def sperr_ein(L, t0, t1):
    o = L["Sperrzone"][0]; al = o.data.materials[0].node_tree.nodes["Principled BSDF"].inputs["Alpha"]; a1 = al.default_value
    al.default_value = 0; al.keyframe_insert("default_value", frame=fr(t0)); al.default_value = a1; al.keyframe_insert("default_value", frame=fr(t1))

# ---------------- Steuergeräte am Einbauort: eine durchgehende Kamerafahrt (Pack -> CMU in der Endzone -> BMS in der Schaltbox) ----------------
if SZ == "steuer":
    # Lage aus dem Pack-STEP e2d_e3c (pack_e2d.py): CMU hinten: Platinen-x -> Pack-y, Platinen-y -> -Pack-z, Platinen-z (Bauteile) -> -Pack-x, Rückseite innen; BMS: Platinen-x,y,z -> Pack-x,y,z, Ecke bei bms_platine_bbox_mm
    BMSB = json.load(open("/home/cae/hermes/batterie/cad/pack/entwurf/ergebnis_LFP_e2d_e3c.json"))["e2"]["bms_platine_bbox_mm"]
    N, ob = pack_laden(masken=[("E2_CMU", "CMU_eins", (0, 30, 35), (1025, 150, 95)), ("E2_Schaltbox_Inhalt", "BMS_alt", tuple(v - 0.2 for v in BMSB[:3]), tuple(v + 0.2 for v in BMSB[3:]))])
    P = np.array(N["CMU_eins"]["punkte"]); T = np.array(N["CMU_eins"]["dreiecke"]); pc = P[T].reshape(-1, 3); cmin, cmax = pc.min(0), pc.max(0)
    ob["Deckel"].hide_render = True
    mc = ob["E2_CMU"].data.materials[0]; bsd = mc.node_tree.nodes["Principled BSDF"]; bsd.inputs["Emission Color"].default_value = (1.0, 0.45, 0.05, 1); es = bsd.inputs["Emission Strength"]
    for t, v in ((0, 0.0), (1.0, 1.0), (2.5, 0.3), (4.0, 0.9), (6.0, 0.3), (8.0, 0.3)): es.default_value = v; es.keyframe_insert("default_value", frame=fr(t))
    # Zellen als Bänder (Hüllkörper)
    t_ = stl(f"{DV}/netz_LFP/BT-100__Zelle_LFP.stl"); cx = t_[:, :, 0].mean(1); x0_, x1_ = float(cx.min()), float(cx.max()); mz = mat("zelle", (0.30, 0.50, 0.85), 1.0, 0.0, 0.4)
    zb_ = []
    for k in range(6):
        sel = (cx >= x0_ + (x1_ - x0_) * k / 6) & (cx <= x0_ + (x1_ - x0_) * (k + 1) / 6 + (1e-3 if k == 5 else -1e-3)); zb_.append(soup(f"Zellen_{k}", t_[sel], mz))
    def alpha_key(m, t0, a0_, t1, a1_):
        al = m.node_tree.nodes["Principled BSDF"].inputs["Alpha"]; al.default_value = a0_; al.keyframe_insert("default_value", frame=fr(t0)); al.default_value = a1_; al.keyframe_insert("default_value", frame=fr(t1))
    GH = {"Seitenrahmen": .10, "Boden": 0, "Unterfahrschutz": 0, "Kuehlplatte": 0, "Pad": 0, "Zellverbinder": 0, "Quertraeger": .10, "E2_Daisy": .25, "E2_FPC": .25, "E2_FPC_Detail": .25, "E2_FPC_Halter": .25,
          "E2_Schaltbox": .12, "E2_Schaltbox_Deckel": .10, "E2_Dichtung": .10, "E2_Servicedeckel": .10, "E2_HV_Leitung": .25, "E2_Kabelschuh": .25, "E2_Clip": .25, "E2_Lasche": .25, "E2_Trennbruecke": .2, "E2_Trennbrueckenschraube": .2,
          "E2_Stecker_Sensor": .3, "E2_Schraube": .2}
    for g, a_end in GH.items():
        if g in ob: m_ = ob[g].data.materials[0]; a_st = 0.22 if g in ("Kuehlplatte", "Pad") else 1.0; alpha_key(m_, 2.0, a_st, 5.0, a_end)
    alpha_key(mz, 2.0, 1.0, 4.5, 0.0)   # Zellen blenden aus und werden ausgeblendet (viele gestapelte Alpha-Flächen sähen sonst wie ein dunkler Block aus)
    for o in zb_: o.hide_render = False; o.keyframe_insert("hide_render", frame=0); o.keyframe_insert("hide_render", frame=fr(4.5)); o.hide_render = True; o.keyframe_insert("hide_render", frame=fr(4.6)); ease(o)
    for g in ("E2_Schaltbox_Inhalt", "E2_Stromschiene", "E2_Schrumpfschlauch", "BMS_alt"):   # Umgebung der BMS-Platine wird durchsichtig, bevor die Kamera ankommt
        if g in ob and g != "BMS_alt": alpha_key(ob[g].data.materials[0], 16.0, 1.0, 19.0, 0.25)
    # CMU: Platine am Einbauort
    rotC = Matrix(((0, 0, 1, 0), (1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 1)))   # Spalten: X -> +y, Y -> +z, Z -> +x (Seite 'vorn' im Code = kleines x; Platinenrücken an der Wand, Bauteile zum Packinneren; geprüft an der Flächenverteilung des Pack-Netzes)
    OC = Vector((cmin[0], cmin[1], cmin[2])) * MM
    DdC = json.load(open("/home/cae/cae_projekte/batterie/e3/explosion_LFP.json")); BdC = json.load(open("/home/cae/cae_projekte/batterie/e3/bauteile_LFP.json"))
    rootC, LC, (WC, HC) = platine("cmu", DdC, BdC, Matrix.Translation(OC) @ rotC @ Matrix.Diagonal((MM, MM, MM, 1)))
    cC = rootC.matrix_basis @ Vector((WC / 2, HC / 2, 1.0, 1.0)); cC = Vector(cC[:3])
    # BMS: Platine in der Schaltbox
    OB = Vector(BMSB[:3]) * MM; DdB = json.load(open("/home/cae/cae_projekte/batterie/e3c/explosion.json")); BdB = json.load(open("/home/cae/cae_projekte/batterie/e3c/bauteile.json"))
    rootB, LB, (WB, HB) = platine("bms", DdB, BdB, Matrix.Translation(OB) @ Matrix.Diagonal((MM, MM, MM, 1)), zone=(100.0, 110.0))
    cB = Vector((rootB.matrix_basis @ Vector((WB / 2, HB / 2, 1.0, 1.0)))[:3])
    print("ZENTRUM CMU", cC, "BMS", cB, flush=True)
    TC0, TC1 = 8.4, 9.0; TB0 = 20.0; NX = 10   # Überblendung über 10 Bilder
    def bbox_welt(objs):
        pts = []
        for o in objs:
            n = len(o.data.vertices); v = np.zeros(n * 3); o.data.vertices.foreach_get("co", v); v = v.reshape(-1, 3)
            M_ = np.array(o.parent.matrix_basis @ o.matrix_basis) if o.parent else np.array(o.matrix_basis)
            pts.append((np.c_[v, np.ones(n)] @ M_.T)[:, :3])
        pts = np.vstack(pts) / MM; return pts.min(0), pts.max(0)
    def bbox_pts(objs):
        r = []
        for o in objs:
            n = len(o.data.vertices); v = np.zeros(n * 3); o.data.vertices.foreach_get("co", v); v = v.reshape(-1, 3); M_ = np.array(o.parent.matrix_basis @ o.matrix_basis); r.append((np.c_[v, np.ones(n)] @ M_.T)[:, :3] / MM)
        return np.unique(np.vstack(r), axis=0)
    def lagepruefung(name, piece, L_):
        d0, d1 = bbox_welt([L_[k][0] for k in ("Substrat", "Bauteile")]); pp_ = np.array(N[piece.name]["punkte"])[np.array(N[piece.name]["dreiecke"]).reshape(-1)]; p0, p1 = pp_.min(0), pp_.max(0)   # nur die benutzten Punkte des abgetrennten Pack-Teils dev = max(np.abs(d0 - p0).max(), np.abs(d1 - p1).max())
        dev = max(np.abs(d0 - p0).max(), np.abs(d1 - p1).max())
        sw = np.abs(np.unique(pp_, axis=0).mean(0) - bbox_pts([L_["Bauteile"][0]]).mean(0)).max(); print(f"  Schwerpunkt der Bauteil-Punkte, Abweichung {sw:.3f} mm", flush=True); 
        tt_ = np.array(N[piece.name]["punkte"])[np.array(N[piece.name]["dreiecke"])]; ar_ = np.linalg.norm(np.cross(tt_[:, 1] - tt_[:, 0], tt_[:, 2] - tt_[:, 0]), axis=1) / 2; bg_ = tt_[ar_ > 500].reshape(-1, 3)
        s0, s1 = bbox_welt([L_["Substrat"][0]]); ds = max(np.abs(bg_.min(0) - s0).max(), np.abs(bg_.max(0) - s1).max()); print(f"  Platinenkörper (große Flächen des Pack-Teils) gegen Substrat: Abweichung {ds:.3f} mm", flush=True); assert ds < 0.5, f"Substrat {ds}"
        print(f"LAGEPRUEFUNG {name}: Pack-Teil bbox {p0.round(2).tolist()} bis {p1.round(2).tolist()} mm; Detailmodell {d0.round(2).tolist()} bis {d1.round(2).tolist()} mm; max. Abweichung {dev:.3f} mm", flush=True)
        assert dev < 1.0, f"Lageabweichung {dev} mm"
    lagepruefung("CMU (erste Endzone hinten)", ob["CMU_eins"], LC); lagepruefung("BMS", ob["BMS_alt"], LB)
    def ueberblenden(L_, piece, t0):
        """Pack-Teil (eigene Materialkopie) blendet über NX Bilder aus, Detailmodell gleichzeitig ein (gleiche Lage)."""
        f0 = fr(t0); mp_ = piece.data.materials[0].copy(); piece.data.materials[0] = mp_; alpha_key(mp_, t0, 1.0, t0 + NX / FPS, 0.0)
        piece.hide_render = False; piece.keyframe_insert("hide_render", frame=0); piece.keyframe_insert("hide_render", frame=f0 + NX); piece.hide_render = True; piece.keyframe_insert("hide_render", frame=f0 + NX + 1); ease(piece)
        for k, (o, _i) in L_.items():
            m_ = o.data.materials[0]; a1 = m_.node_tree.nodes["Principled BSDF"].inputs["Alpha"].default_value; alpha_key(m_, t0, 0.0, t0 + NX / FPS, a1)
            o.hide_render = True; o.keyframe_insert("hide_render", frame=0); o.hide_render = False; o.keyframe_insert("hide_render", frame=f0); ease(o)
    ueberblenden(LC, ob["CMU_eins"], TC0); ueberblenden(LB, ob["BMS_alt"], TB0)
    explodieren(LC, 10.0, 12.2, 13.4, 14.6); explodieren(LB, 22.0, 24.2, 25.6, 27.0); sperr_ein(LB, TB0 + 0.5, TB0 + 2.0)
    camp = [(0, CEN, -40, 32, 3.8), (3.0, CEN, -45, 30, 3.6), (6.0, (0.5, 0.3, 0.1), 60, 28, 1.4), (8.4, tuple(cC), 68, 22, 0.30), (10.0, tuple(cC), 68, 22, 0.30), (12.2, tuple(cC), 66, 22, 0.42), (14.0, tuple(cC), 66, 22, 0.42),
            (17.0, (1.2, 0.5, 0.15), -30, 40, 1.4), (20.0, tuple(cB), -25, 50, 0.45), (24.0, tuple(cB), -25, 38, 0.55), (27.5, tuple(cB), -25, 38, 0.55), (30.0, tuple(cB), -25, 40, 0.6)]
    cam = kamera("cam", camp); sc.camera = cam

a0, a1 = (int(arg[0]), int(arg[1])) if len(arg) >= 2 else (0, NFR - 1)
sc.frame_start, sc.frame_end = a0, a1
if os.environ.get("VIDEO_TEST"):
    for f in [int(x) for x in os.environ["VIDEO_TEST"].split(",")]:
        sc.render.filepath = f"{DV}/elektronik3d/test_{SZ}_{f:04d}.png"; sc.frame_set(f); bpy.ops.render.render(write_still=True)
    sys.exit()
bpy.ops.render.render(animation=True)
print("RENDER FERTIG", SZ, a0, a1, flush=True)
