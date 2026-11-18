# KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. Auftrag K0 Ergaenzung. Laeuft in Blender (CPU, Workbench-Renderer, kein GPU):
#   blender -b -P render_blender.py -- <export.npz> <ausgabeordner> <vmin> <vmax> <schritt> [<schritt> ...]
# Liest Oberflaechennetz + Knotentemperaturen (von bilder_render.py aus den Elmer-VTU exportiert), faerbt Knoten (Inferno), rendert ohne Text.
import sys, os, numpy as np, bpy, mathutils
a = sys.argv[sys.argv.index("--") + 1:]; npz, aus, vmin, vmax = a[0], a[1], float(a[2]), float(a[3]); schritte = [int(s) for s in a[4:]]
d = np.load(npz); P = d["P"]; F = d["F"]; TT = d["T"]; steps = list(d["steps"]); nmc = bool(d["nmc"]); lut = d["lut"]    # lut: 256x3 sRGB
os.makedirs(aus, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
me = bpy.data.meshes.new("zelle"); me.from_pydata((P * 1e-3).tolist(), [], F.tolist()); me.update()
ob = bpy.data.objects.new("zelle", me); sc = bpy.context.scene; sc.collection.objects.link(ob)
ca = me.color_attributes.new("T", "FLOAT_COLOR", "POINT")
sc.render.engine = "BLENDER_WORKBENCH"; sc.render.resolution_x = 1000; sc.render.resolution_y = 700
sh = sc.display.shading; sh.light = "FLAT"; sh.color_type = "VERTEX"; sh.show_object_outline = False; sh.show_cavity = False
sc.view_settings.view_transform = "Standard"; sc.display_settings.display_device = "sRGB"
w = bpy.data.worlds.new("w"); w.color = (1, 1, 1); sc.world = w
c = (P.min(0) + P.max(0)) / 2 * 1e-3; ext = (P.max(0) - P.min(0)) * 1e-3
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); sc.collection.objects.link(cam); sc.camera = cam; cam.data.type = "ORTHO"
dirn = mathutils.Vector((0.45, -0.80, 0.55)) if not nmc else mathutils.Vector((0.9, -0.9, 0.7))
dirn.normalize(); cam.location = mathutils.Vector(c) + dirn * 2.0
cam.rotation_euler = (mathutils.Vector(c) - cam.location).to_track_quat("-Z", "Y").to_euler()
cam.data.ortho_scale = float(np.linalg.norm(ext) * (0.80 if not nmc else 1.25)); cam.data.clip_end = 10.0
cam.data.shift_y = -0.02 if not nmc else 0.0
for st in schritte:
    T = TT[steps.index(st)]; x = np.clip((T - vmin) / (vmax - vmin), 0, 1); col = lut[(x * 255).astype(int)] ** 2.2
    rgba = np.concatenate([col, np.ones((len(T), 1))], 1).astype(np.float32)
    ca.data.foreach_set("color", rgba.ravel()); me.update()
    sc.render.filepath = f"{aus}/roh_{st:04d}.png"; bpy.ops.render.render(write_still=True)
