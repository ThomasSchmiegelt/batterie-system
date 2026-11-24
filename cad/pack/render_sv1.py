# KI-generiert (Claude Sonnet, 2026-11-24), Entwurf. SV1 (ERW-SV1): Blender CPU (Cycles). Aufruf: PACK_VARIANTE=LFP|NMC $BLENDER -b -P cad/pack/render_sv1.py
# Liest Netze aus /home/cae/cae_projekte/batterie/e2/ (von pack_e2d.py PACK_SV1=1). Stecker transparent, Gegenstück fest, Steckfreigang rot halbtransparent, Schrauben sichtbar. Ausgabe roh_<V>_sv1_<ansicht>.png/.json
import bpy, os, json, math
from mathutils import Vector
R = "/home/cae/hermes/batterie"; NZ = "/home/cae/cae_projekte/batterie/e2"; VAR = os.environ["PACK_VARIANTE"]; VO = VAR + "_e2d_e3c_sv1"; MM = 0.001; S = int(os.environ.get("RENDER_SAMPLES", "24"))
os.makedirs(f"{NZ}/render", exist_ok=True)
FARBE = {"SV1_Stecker": ((0.0, 0.5, 1.0), 0.35), "SV1_Gegenstueck": ((0.05, 0.15, 0.45), 1.0), "E2_Steckfreigang": ((0.95, 0.05, 0.05), 0.22), "SV1_Schraube": ((1.0, 0.85, 0.0), 1.0),
         "E2_Stecker_Sensor": ((0.1, 0.25, 0.6), 1.0), "E2_Schaltbox": ((0.35, 0.37, 0.4), 1.0), "E2_Schaltbox_Inhalt": ((0.2, 0.7, 0.4), 1.0), "E2_CMU": ((0.8, 0.8, 0.3), 1.0), "E2_FPC": ((1, 0.75, 0), 0.8), "E2_FPC_Detail": ((1, 0.9, 0.2), 1.0), "E2_Daisy": ((0.6, 0.3, 0.1), 1.0),
         "E2_Stromschiene": ((0.95, 0.55, 0.15), 1.0), "E2_HV_Leitung": ((0.85, 0.0, 0.7), 1.0), "E2_Schraube": ((0.6, 0.6, 0.65), 1.0)}
GRAU = (0.6, 0.62, 0.65)
def laden(suf): return json.load(open(f"{NZ}/netz_{VO}{suf}.json"))
def bb(netz, grp, filt=lambda p: True):
    P = [p for g in grp if g in netz for p in netz[g]["punkte"] if filt(p)]; return [(min(p[i] for p in P), max(p[i] for p in P)) for i in range(3)]
ng = laden("_gesamt"); Lg = max(p[0] for p in ng["Deckel"]["punkte"])
sb = bb(ng, ["E2_Schaltbox"]); ctr_box = tuple((a + b) / 2 for a, b in sb)
cm = bb(ng, ["E2_CMU"], lambda p: p[0] > Lg - 60); ctr_end = tuple((a + b) / 2 for a, b in cm)
ANS = {"schaltbox": ("_boxoffen", (-0.5, -0.9, 0.8), 520.0, (1700, 1100), (ctr_box[0] - 60, ctr_box[1], ctr_box[2] - 20), False),
       "endzone": ("_ohnedeckel", (-0.9, -0.5, 0.7), 330.0, (1700, 1100), ctr_end, True)}
def bau(name):
    suf, dirv, scale, res, ctr, grau = ANS[name]; netz = laden(suf)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene; sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = S; sc.cycles.use_denoising = False
    sc.render.resolution_x, sc.render.resolution_y = res; sc.view_settings.view_transform = "Standard"
    wd = bpy.data.worlds.new("w"); sc.world = wd; wd.use_nodes = True; wd.node_tree.nodes["Background"].inputs[1].default_value = 0.9; wd.node_tree.nodes["Background"].inputs[0].default_value = (0.97, 0.97, 0.98, 1)
    for g, m in netz.items():
        pts, tri = m["punkte"], m["dreiecke"]
        if not pts or g == "Zellen": continue
        if name == "endzone" and g in ("Deckel",): continue
        me = bpy.data.meshes.new(g); me.from_pydata([(p[0] * MM, p[1] * MM, p[2] * MM) for p in pts], [], tri); me.update()
        ob = bpy.data.objects.new(g, me); sc.collection.objects.link(ob)
        mt = bpy.data.materials.new(g); mt.use_nodes = True; b = mt.node_tree.nodes["Principled BSDF"]
        col, al = FARBE.get(g, (GRAU, 0.18 if grau else 0.5)) if g in FARBE else (GRAU, 0.15 if grau else 0.6)
        b.inputs["Base Color"].default_value = (*col, 1); b.inputs["Roughness"].default_value = 0.4; b.inputs["Alpha"].default_value = al
        if al < 1: mt.blend_method = "BLEND" if hasattr(mt, "blend_method") else None
        if g == "E2_Steckfreigang" and hasattr(mt, "use_backface_culling"): mt.use_backface_culling = False
        ob.data.materials.append(mt)
    c = Vector((ctr[0] * MM, ctr[1] * MM, ctr[2] * MM))
    cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); sc.collection.objects.link(cam); sc.camera = cam
    cam.data.type = "ORTHO"; cam.data.ortho_scale = scale * MM; cam.data.clip_end = 100
    cam.location = c + Vector(dirv).normalized() * 10; cam.rotation_euler = (c - cam.location).to_track_quat("-Z", "Y").to_euler()
    for az, en in ((35, 1.3), (-120, 0.6)):
        l = bpy.data.objects.new("l", bpy.data.lights.new("l", "SUN")); l.data.energy = en; l.rotation_euler = (math.radians(50), 0, math.radians(az)); sc.collection.objects.link(l)
    bpy.context.view_layer.update(); sc.render.filepath = f"{NZ}/render/roh_{VAR}_sv1_{name}.png"; bpy.ops.render.render(write_still=True)
    json.dump({"res": res, "scale_mm": scale}, open(f"{NZ}/render/roh_{VAR}_sv1_{name}.json", "w"))
for a in ANS: bau(a)
print("RENDER FERTIG", VAR)
