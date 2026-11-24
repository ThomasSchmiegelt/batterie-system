# KI-generiert (Claude Sonnet, 2026-11-24), Entwurf. Blender (CPU, Cycles): CMU am Einbauort im Pack (Endzone), Rest grau durchsichtig. Aufruf: E3V=NMC $BLENDER -b -P einbau_blender.py
# Eingang: /home/cae/cae_projekte/batterie/e3/pack_netz_<V>.json (Kopie von e2/netz_<V>_e2d_e3_gesamt.json aus cad/pack/pack_e2d.py PACK_E3=1; Zellen sind darin ausgeblendet).
# Ausgabe: einbau_<V>_uebersicht_roh.png, einbau_<V>_nah_roh.png, einbau_<V>_anker.json.
import bpy, os, json, math
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
V = os.environ["E3V"]; H = "/home/cae/hermes/batterie/sim/elektrik/e3_platine"; N = json.load(open(f"/home/cae/cae_projekte/batterie/e3/pack_netz_{V}.json")); MM = 0.001
bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene; sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = int(os.environ.get("RENDER_SAMPLES", "40")); sc.cycles.use_denoising = False
sc.view_settings.view_transform = "Standard"; sc.cycles.transparent_max_bounces = 16
wd = bpy.data.worlds.new("w"); sc.world = wd; wd.use_nodes = True; wd.node_tree.nodes["Background"].inputs[1].default_value = 0.9; wd.node_tree.nodes["Background"].inputs[0].default_value = (0.95, 0.96, 0.97, 1)
def mat(name, col, alpha=1.0, metal=0.0, rough=0.5):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]; b.inputs["Base Color"].default_value = (*col, 1); b.inputs["Metallic"].default_value = metal; b.inputs["Roughness"].default_value = rough; b.inputs["Alpha"].default_value = alpha; return m
M_REST = mat("rest", (0.45, 0.48, 0.52), 0.07); M_CMU = mat("cmu", (0.95, 0.45, 0.05), 1.0, 0.0, 0.4); M_RAH = mat("rahmen", (0.4, 0.42, 0.47), 0.30, 0.3)
HIDE = ("Deckel", "E2_Schaltbox_Deckel", "Zellen")
NAH_HIDE = tuple(g for g in N if g.startswith("E2_") and g not in ("E2_CMU", "E2_FPC", "E2_Daisy")) + ("Zellverbinder",)   # in der Nahansicht nur Rahmen, Kühlplatte, CMU, FPC, Daisy (Darstellung)   # Deckel ausgeblendet, damit man hineinsieht
objs = {}
def add(name, g, m):
    pts, tri = N[g]["punkte"], N[g]["dreiecke"]
    if not pts: return None
    me = bpy.data.meshes.new(name); me.from_pydata([(p[0] * MM, p[1] * MM, p[2] * MM) for p in pts], [], tri); me.update(); ob = bpy.data.objects.new(name, me); sc.collection.objects.link(ob); ob.data.materials.append(m); objs[name] = ob; return ob
for g in N:
    if g in HIDE or g == "E2_CMU": continue
    add(g, g, M_RAH if g in ("Seitenrahmen", "Boden", "Quertraeger", "Unterfahrschutz") else M_REST)
cm = add("E2_CMU", "E2_CMU", M_CMU)
allp = [ob.matrix_world @ Vector(v) for ob in objs.values() for v in ob.bound_box]
lo = Vector((min(p.x for p in allp), min(p.y for p in allp), min(p.z for p in allp))); hi = Vector((max(p.x for p in allp), max(p.y for p in allp), max(p.z for p in allp))); c = (lo + hi) / 2
# Platinen-Schwerpunkte der CMU (Netzpunkte nach x-Seite gruppiert, y/z-Mitte je Platine über zusammenhängende y-Cluster)
cp = [Vector((p[0], p[1], p[2])) * MM for p in N["E2_CMU"]["punkte"]]; xs = sorted(set(round(p.x, 1) for p in cp))
vorn = [p for p in cp if p.x > c.x]; hinten = [p for p in cp if p.x <= c.x]
def mitte(L): return Vector((sum(p.x for p in L) / len(L), (min(p.y for p in L) + max(p.y for p in L)) / 2, (min(p.z for p in L) + max(p.z for p in L)) / 2))
cv = mitte(vorn); ch = mitte(hinten)
viel = hinten if len(hinten) > len(vorn) else vorn; ymin = min(p.y for p in viel); eine = [p for p in viel if p.y < ymin + 0.13]; ce = mitte(eine); seite_viel = 'hinten' if viel is hinten else 'vorn'
for az, en in ((35, 3.0), (-120, 1.5)):
    l = bpy.data.objects.new("l", bpy.data.lights.new("l", "SUN")); l.data.energy = en; l.rotation_euler = (math.radians(50), 0, math.radians(az)); sc.collection.objects.link(l)
def kamera(name, ziel, richtung, skala, res, abstand=8.0):
    cam = bpy.data.objects.new(name, bpy.data.cameras.new(name)); sc.collection.objects.link(cam); cam.data.type = "ORTHO"; cam.data.ortho_scale = skala; cam.data.clip_end = 100
    cam.location = ziel + Vector(richtung).normalized() * abstand; cam.rotation_euler = (ziel - cam.location).to_track_quat("-Z", "Y").to_euler(); sc.camera = cam
    sc.render.resolution_x, sc.render.resolution_y = res; bpy.context.view_layer.update(); return cam
A = {}
cam = kamera("uebersicht", c, (0.55, -1.0, 0.7), 1.25 * (hi.x - lo.x), (2000, 1000))
if os.environ.get("E3NUR") not in ("nah", "anker"): sc.render.filepath = f"/home/cae/cae_projekte/batterie/e3/roh/einbau_{V}_uebersicht_roh.png"; bpy.ops.render.render(write_still=True)
f = lambda q: [world_to_camera_view(sc, cam, q).x, 1 - world_to_camera_view(sc, cam, q).y]
cl = {}
for p in cp: cl.setdefault((p.x > c.x, p.y > c.y), []).append(p)
A["uebersicht"] = dict(cluster=[f(mitte(L)) for L in cl.values()], vorn=f(cv), hinten=f(ch), L_mm=(hi.x - lo.x) / MM, B_mm=(hi.y - lo.y) / MM, H_mm=(hi.z - lo.z) / MM)
# Nahansicht: Endzone vorn (Blick von innen in Richtung Stirnwand, schräg)
for g_, ob_ in objs.items():
    if g_ in NAH_HIDE: ob_.hide_render = True
dx = float(os.environ.get("E3DX", "1.0")) * (1 if seite_viel == "hinten" else -1)
ziel = ce; cam2 = kamera("nah", ziel, (dx, -0.9, 0.5), 0.5, (1800, 1100)); 
if os.environ.get("E3NUR") != "anker": sc.render.filepath = f"/home/cae/cae_projekte/batterie/e3/roh/einbau_{V}_nah_roh.png"; bpy.ops.render.render(write_still=True)
f2 = lambda q: [world_to_camera_view(sc, cam2, q).x, 1 - world_to_camera_view(sc, cam2, q).y]
A["nah"] = dict(cmu=f2(ce), boden=f2(Vector((ce.x, ce.y, lo.z))), seite=seite_viel)
json.dump(A, open(f"{H}/einbau_{V}_anker.json", "w"))
