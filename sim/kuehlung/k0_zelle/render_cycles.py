# KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. Auftrag K0-R (sim/kuehlung/k0_zelle/AUFTRAG_RENDER.md). Wiederverwendbar fuer K1.
# Blender 4.0.2 Cycles, nur CPU. Aufruf (Argumente nach "--"):
#   nice -n 10 $BLENDER -b -P render_cycles.py -- --npz <export.npz> --aus <ordner> --vmin 25 --vmax 54 --variante lfp|nmc --kuehl platte|band \
#        --schritte 0 30 60 ... --samples 128 [--lupe 1] [--aufloesung 1800 600]
# npz (von bilder_cycles.py): P (mm, Blender-Achsen: Z = Hoehe), F (Dreiecke/Vierecke Oberflaeche), T (Schritte x Knoten, degC), steps, lut (256x3 sRGB).
# Schattierung: Mischung Emission (Farbe = Skala) + Diffus (Form lesbar). Rohbilder roh_<kamera>_<schritt>.png und anker.json.
import sys, os, json, math, argparse, numpy as np, bpy, mathutils
from bpy_extras.object_utils import world_to_camera_view
ap = argparse.ArgumentParser(); ap.add_argument("--npz"); ap.add_argument("--aus"); ap.add_argument("--vmin", type=float); ap.add_argument("--vmax", type=float)
ap.add_argument("--variante"); ap.add_argument("--kuehl", default="platte"); ap.add_argument("--schritte", type=int, nargs="+"); ap.add_argument("--samples", type=int, default=128)
ap.add_argument("--lupe", type=int, default=0); ap.add_argument("--aufloesung", type=int, nargs=2, default=None); ap.add_argument("--emission", type=float, default=0.7)
a = ap.parse_args(sys.argv[sys.argv.index("--") + 1:])
if a.aufloesung is None: a.aufloesung = [1800, 600] if a.variante == "lfp" else [1000, 900]
d = np.load(a.npz); P = d["P"] * 1e-3; F = d["F"]; TT = d["T"]; steps = list(d["steps"]); lut = d["lut"]; lfp = a.variante == "lfp"
os.makedirs(a.aus, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene
sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = a.samples
try: sc.cycles.use_denoising = True; sc.cycles.denoiser = "OPENIMAGEDENOISE"
except Exception: sc.cycles.use_denoising = False
sc.render.resolution_x, sc.render.resolution_y = a.aufloesung; sc.render.resolution_percentage = 100
sc.view_settings.view_transform = "Standard"; sc.display_settings.display_device = "sRGB"
# Welt: wie render_detail.py (Verlauf grau, Strahlkraft 0.55)
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True; nt = w.node_tree; bg = nt.nodes["Background"]; bg.inputs[1].default_value = 0.35
tc = nt.nodes.new("ShaderNodeTexCoord"); sp = nt.nodes.new("ShaderNodeSeparateXYZ"); cr = nt.nodes.new("ShaderNodeValToRGB")
nt.links.new(tc.outputs["Generated"], sp.inputs[0]); nt.links.new(sp.outputs["Z"], cr.inputs[0]); nt.links.new(cr.outputs[0], bg.inputs[0])
cr.color_ramp.elements[0].position = 0.3; cr.color_ramp.elements[0].color = (0.30, 0.32, 0.36, 1); cr.color_ramp.elements[1].position = 0.8; cr.color_ramp.elements[1].color = (0.75, 0.77, 0.80, 1)
# Zelle
me = bpy.data.meshes.new("zelle"); me.from_pydata(P.tolist(), [], F.tolist()); me.update()
ob = bpy.data.objects.new("zelle", me); sc.collection.objects.link(ob)
for p in me.polygons: p.use_smooth = False
ca = me.color_attributes.new("T", "FLOAT_COLOR", "POINT")
m = bpy.data.materials.new("T"); m.use_nodes = True; n = m.node_tree.nodes; l = m.node_tree.links; n.clear()
at = n.new("ShaderNodeVertexColor"); at.layer_name = "T"; em = n.new("ShaderNodeEmission"); df = n.new("ShaderNodeBsdfDiffuse"); mx = n.new("ShaderNodeMixShader"); out = n.new("ShaderNodeOutputMaterial")
mx.inputs[0].default_value = 1.0 - a.emission   # Anteil Diffus
l.new(at.outputs["Color"], em.inputs["Color"]); l.new(at.outputs["Color"], df.inputs["Color"]); l.new(em.outputs[0], mx.inputs[1]); l.new(df.outputs[0], mx.inputs[2]); l.new(mx.outputs[0], out.inputs[0])
ob.data.materials.append(m)
def mat_grau(name, rgb, alpha=1.0, rough=0.5, metal=0.0):
    mm = bpy.data.materials.new(name); mm.use_nodes = True; b = mm.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Roughness"].default_value = rough; b.inputs["Metallic"].default_value = metal; b.inputs["Alpha"].default_value = alpha
    if alpha < 1: mm.blend_method = "BLEND"
    return mm
def box(name, lo, hi, mt):
    v = [(x, y, z) for x in (lo[0], hi[0]) for y in (lo[1], hi[1]) for z in (lo[2], hi[2])]
    f = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
    e = bpy.data.meshes.new(name); e.from_pydata(v, [], f); e.update(); o = bpy.data.objects.new(name, e); sc.collection.objects.link(o); o.data.materials.append(mt); return o
def schale(name, r_i, r_a, w0, w1, z0, z1, mt, nseg=48):
    """Zylinderschale (Winkel w0..w1 Grad) als Netz."""
    v, f = [], []; ws = np.radians(np.linspace(w0, w1, nseg + 1))
    for w_ in ws:
        for r in (r_i, r_a):
            for z in (z0, z1): v.append((r * math.cos(w_), r * math.sin(w_), z))
    for i in range(nseg):
        b = i * 4; c = (i + 1) * 4
        f += [(b + 2, c + 2, c + 3, b + 3), (b + 0, b + 1, c + 1, c + 0), (b + 0, c + 0, c + 2, b + 2), (b + 1, b + 3, c + 3, c + 1)]
    f += [(0, 1, 3, 2), (nseg * 4 + 0, nseg * 4 + 2, nseg * 4 + 3, nseg * 4 + 1)]
    e = bpy.data.meshes.new(name); e.from_pydata(v, [], f); e.update(); o = bpy.data.objects.new(name, e); sc.collection.objects.link(o); o.data.materials.append(mt); return o
lo, hi = P.min(0), P.max(0); ctr = (lo + hi) / 2
plat = mat_grau("Kuehlplatte", (0.62, 0.64, 0.68), rough=0.45, metal=0.0)
if lfp:
    box("kuehlplatte", (lo[0] - 0.012, lo[1] - 0.012, lo[2] - 0.010), (hi[0] + 0.012, hi[1] + 0.012, lo[2]), plat)
else:
    mgl = mat_grau("Huelle", (0.7, 0.75, 0.8), alpha=0.05, rough=0.1)
    R = max(hi[0], -lo[0])
    schale("huelle_weg", R - 0.0005, R + 0.0006, 270, 360, lo[2], hi[2], mgl)   # weggeschnittenes Viertel (x>0, y<0) als durchsichtige Huelle
    if a.kuehl == "platte": box("kuehlplatte", (-0.034, -0.034, lo[2] - 0.008), (0.034, 0.034, lo[2]), plat)
    else:
        schale("kuehlband", R + 0.0006, R + 0.004, 0, 90, lo[2] + 0.003, hi[2] - 0.003, plat)
        box("kuehlplatte_aus", (-9, -9, -9), (-8.99, -8.99, -8.99), plat)
# Licht: zwei Sonnen (Staerke so, dass der Diffus-Anteil etwa die Farbe selbst ergibt; Farbtreue wird in der Pixelpruefung gemessen)
def sonne(name, richtung, st):
    ld = bpy.data.lights.new(name, "SUN"); ld.energy = st; ld.angle = math.radians(8)
    o = bpy.data.objects.new(name, ld); sc.collection.objects.link(o)
    o.rotation_euler = mathutils.Vector((-richtung[0], -richtung[1], -richtung[2])).to_track_quat("-Z", "Y").to_euler()
    return o
ext = hi - lo
sonne("key", (-0.5, -0.8, 0.9), float(os.environ.get("K0_KEY", "2.2"))); sonne("fill", (0.9, -0.4, 0.3), float(os.environ.get("K0_FILL", "0.6")))
# Kameras
def kamera(name, richtung, ziel, ortho, shift=(0, 0)):
    cd = bpy.data.cameras.new(name); cd.type = "ORTHO"; cd.ortho_scale = ortho; cd.clip_end = 20; cd.shift_x, cd.shift_y = shift
    co = bpy.data.objects.new(name, cd); sc.collection.objects.link(co); dv = mathutils.Vector(richtung).normalized()
    co.location = mathutils.Vector(ziel) + dv * 3.0; co.rotation_euler = (mathutils.Vector(ziel) - co.location).to_track_quat("-Z", "Y").to_euler(); return co
anker = {}
if lfp:
    # Schnittflaeche (Normale +Y im Blender-System, Schnitt bei halber Dicke) schraeg von vorn-oben
    cam = kamera("haupt", (0.05, -0.95, 0.50), tuple(ctr + np.array([0, 0, -0.004])), 0.74)
    sc.camera = cam; kams = [("haupt", cam)]
    if a.lupe:
        lc = (0.060, ctr[1], 0.030)   # Ausschnitt x 0..~0.12 m, Boden bis ~0.06 m Hoehe
        lup = kamera("lupe", (0.15, -0.9, 0.5), lc, 0.115); kams.append(("lupe", lup))
        # Rechteck der Lupe im Hauptbild (Bildbruchteile)
        sc.camera = cam; bpy.context.view_layer.update()
        pts = [world_to_camera_view(sc, cam, mathutils.Vector((x, ctr[1], z))) for x in (0.0, 0.12) for z in (0.0, 0.06)]
        anker["lupe_rect"] = [min(p.x for p in pts), min(p.y for p in pts), max(p.x for p in pts), max(p.y for p in pts)]
else:
    cam = kamera("haupt", (0.9, -0.9, 1.0), tuple(ctr), 0.125); sc.camera = cam; kams = [("haupt", cam)]
json.dump(anker, open(f"{a.aus}/anker.json", "w"))
for st in a.schritte:
    T = TT[steps.index(st)]; x = np.clip((T - a.vmin) / (a.vmax - a.vmin), 0, 1); col = lut[(x * 255).astype(int)] ** 2.2
    ca.data.foreach_set("color", np.concatenate([col, np.ones((len(T), 1))], 1).astype(np.float32).ravel()); me.update()
    for kn, ko in kams:
        sc.camera = ko
        if kn == "lupe": sc.render.resolution_x, sc.render.resolution_y = 700, 500
        else: sc.render.resolution_x, sc.render.resolution_y = a.aufloesung
        sc.render.filepath = f"{a.aus}/roh_{kn}_{st:04d}.png"; bpy.ops.render.render(write_still=True)
