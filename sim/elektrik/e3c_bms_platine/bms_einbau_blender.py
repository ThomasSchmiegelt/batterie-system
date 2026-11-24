# KI-generiert (Claude Sonnet, 2026-11-24), Entwurf. Muster: e3_platine/einbau_blender.py. Blender (CPU, Cycles): BMS-Platine BT-311 in der offenen Schaltbox (LFP-Pack).
# Aufruf: RENDER_SAMPLES=48 $BLENDER -b -P bms_einbau_blender.py. Eingang: e2/netz_LFP_e2d_e3_bmsbox.json (cad/pack/pack_e2d.py PACK_E3=1), e3c/bauteile.json (bms_bauteile_netz.py), ergebnis_LFP_e2d_e3.json (bms_platine_bbox_mm).
# Ausgabe: e3c/roh/einbau_roh.png, einbau_anker.json. Die Platine liegt mit ihrer Ecke auf der Ecke des BMS-Platzes (BT-310, 200 x 150 mm); die Platzhalter des E2-Modells (BMS-Platine, BMS-Stecker) sind ausgeblendet.
import bpy, os, json, math
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
O = "/home/cae/cae_projekte/batterie/e3c"; R = "/home/cae/hermes/batterie"
N = json.load(open("/home/cae/cae_projekte/batterie/e2/netz_LFP_e2d_e3_bmsbox.json")); B = json.load(open(f"{O}/bauteile.json")); PK = json.load(open(f"{R}/cad/pack/entwurf/ergebnis_LFP_e2d_e3.json"))["e2"]["bms_platine_bbox_mm"]
res = json.load(open(f"{R}/sim/elektrik/e3c_bms_platine/ergebnis_platine.json")); LP, BP = res["laenge_mm"], res["breite_mm"]; ZX0, ZX1 = res["sperrzone"]["x_mm"]
X0, Y0, Z0 = PK[0], PK[1], PK[2]; SL, SB = PK[3] - PK[0], PK[4] - PK[1]
bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene; sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = int(os.environ.get("RENDER_SAMPLES", "48")); sc.cycles.use_denoising = False
sc.view_settings.view_transform = "Standard"; sc.cycles.transparent_max_bounces = 16; sc.render.resolution_x, sc.render.resolution_y = 2000, 1350
wd = bpy.data.worlds.new("w"); sc.world = wd; wd.use_nodes = True; wd.node_tree.nodes["Background"].inputs[1].default_value = 0.9; wd.node_tree.nodes["Background"].inputs[0].default_value = (0.95, 0.96, 0.97, 1)
def mat(name, col, alpha=1.0, metal=0.0, rough=0.5):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]; b.inputs["Base Color"].default_value = (*col, 1); b.inputs["Metallic"].default_value = metal; b.inputs["Roughness"].default_value = rough; b.inputs["Alpha"].default_value = alpha; return m
M_BOX = mat("box", (0.45, 0.48, 0.52), 0.12, 0.3, 0.4); M_IN = mat("inhalt", (0.55, 0.58, 0.62), 0.45); M_FR4 = mat("fr4", (0.10, 0.50, 0.22)); M_BT = mat("bt", (0.15, 0.15, 0.17)); M_ZS = mat("zs", (1.0, 0.05, 0.05), 0.35); M_SL = mat("slot", (0.9, 0.1, 0.1), 1.0)
def mesh(name, verts, faces, m):
    me = bpy.data.meshes.new(name); me.from_pydata(verts, [], faces); me.update(); ob = bpy.data.objects.new(name, me); sc.collection.objects.link(ob); ob.data.materials.append(m); return ob
def quader(name, x0, y0, z0, x1, y1, z1, m):
    v = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    return mesh(name, v, [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)], m)
for g, m in (("E2_Schaltbox", M_BOX), ("E2_Schaltbox_Inhalt", M_IN)):
    if g in N and N[g]["punkte"]: mesh(g, [tuple(p) for p in N[g]["punkte"]], N[g]["dreiecke"], m)
pb = B["platine_bbox"]; pts = [(p[0] - pb[0] + X0, p[1] - pb[1] + Y0, p[2] - pb[2] + Z0) for p in B["punkte"]]
mesh("BMS_Bauteile", pts, B["dreiecke"], M_BT)
quader("BMS_Platine", X0, Y0, Z0, X0 + LP, Y0 + BP, Z0 + (pb[5] - pb[2]), M_FR4)
quader("Sperrzone", X0 + ZX0, Y0, Z0, X0 + ZX1, Y0 + BP, Z0 + 14, M_ZS)
for nm, a in (("a", (X0, Y0 + SB - 0.8, X0 + SL, Y0 + SB)), ("b", (X0, Y0, X0 + SL, Y0 + 0.8)), ("c", (X0, Y0, X0 + 0.8, Y0 + SB)), ("d", (X0 + SL - 0.8, Y0, X0 + SL, Y0 + SB))): quader("Platz_" + nm, a[0], a[1], Z0 - 0.5, a[2], a[3], Z0 + 0.3, M_SL)
allp = [Vector(v.co) for o in sc.objects if o.name in ("E2_Schaltbox",) for v in o.data.vertices]
lo = Vector((min(p.x for p in allp), min(p.y for p in allp), min(p.z for p in allp))); hi = Vector((max(p.x for p in allp), max(p.y for p in allp), max(p.z for p in allp))); c = (lo + hi) / 2
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); sc.collection.objects.link(cam); sc.camera = cam; cam.data.type = "ORTHO"; cam.data.clip_start = 10; cam.data.clip_end = 20000; cam.data.ortho_scale = max(hi.x - lo.x, hi.y - lo.y) * 1.25
dirv = Vector((0.35, -0.8, 1.0)).normalized(); cam.location = c + dirv * 1500; cam.rotation_euler = (c - cam.location).to_track_quat("-Z", "Y").to_euler()
for az, en in ((35, 3.0), (-120, 1.2)):
    l = bpy.data.objects.new("l", bpy.data.lights.new("l", "SUN")); l.data.energy = en; l.rotation_euler = (math.radians(50), 0, math.radians(az)); sc.collection.objects.link(l)
bpy.context.view_layer.update()
os.makedirs(f"{O}/roh", exist_ok=True); sc.render.filepath = f"{O}/roh/einbau_roh.png"; bpy.ops.render.render(write_still=True)
def anker(p): q = world_to_camera_view(sc, cam, p); return [q.x, 1 - q.y]
A = dict(platine=anker(Vector((X0 + LP / 2, Y0 + BP / 2, Z0 + 6))), sperrzone=anker(Vector((X0 + (ZX0 + ZX1) / 2, Y0 + BP, Z0 + 14))), platz=anker(Vector((X0 + SL, Y0 + SB, Z0))), box=anker(Vector((hi.x, lo.y, hi.z))))
json.dump(dict(anker=A, platz_mm=[SL, SB], box_mm=[hi.x - lo.x, hi.y - lo.y]), open(f"{R}/sim/elektrik/e3c_bms_platine/einbau_anker.json", "w"))
bpy.ops.wm.save_as_mainfile(filepath=f"{O}/einbau.blend")
