# KI-generiert (Claude Sonnet, 2026-11-24), Entwurf. Muster: e3_platine/explosion_blender.py. Blender (CPU, Cycles): Explosionsansicht der BMS-Platine nach Lagen mit hervorgehobener Sperrzone. Aufruf: $BLENDER -b -P bms_explosion_blender.py
# Eingang: /home/cae/cae_projekte/batterie/e3/explosion_<V>.json (explosion_daten.py), bauteile_<V>.json (bauteile_netz.py). Ausgabe: explosion_<V>_roh.png und explosion_<V>_anker.json (2D-Anker), .blend im selben Ordner.
# Darstellung (keine Rechengröße): Lagenabstand 11 mm, Kupferdicke überhöht auf 0,35 mm; Substrat 1,6 mm (ENT-167), Pad 1,0 mm (ENT-185).
import bpy, os, json, math
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
O = "/home/cae/cae_projekte/batterie/e3c"; D = json.load(open(f"{O}/explosion.json")); B = json.load(open(f"{O}/bauteile.json")); ZX0, ZX1 = 100.0, 110.0
S = 11.0; TC = 0.35; TSUB = 1.6; TPAD = 1.0; W, H = D["w"], D["h"]
def lx(x): return x - D["x0"]
def ly(y): return D["y0"] + H - y
# Lagenhöhen (Mitte): Bauteile oben ... Rahmen unten
Z = {"Bauteile": 5 * S, "F.Cu": 4 * S, "Substrat": 3 * S, "In1.Cu": 2 * S, "In2.Cu": 1 * S, "B.Cu": 0.0}
FARBE = {"cu": (0.85, 0.42, 0.22), "thermo": (1.0, 0.25, 0.05), "fr4": (0.12, 0.45, 0.2), "pad": (0.85, 0.7, 0.12), "al": (0.42, 0.45, 0.5), "bt": (0.18, 0.18, 0.2)}
bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene; sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = int(os.environ.get("RENDER_SAMPLES", "96")); sc.cycles.use_denoising = False
sc.render.resolution_x, sc.render.resolution_y = 2000, 1350; sc.view_settings.view_transform = "Standard"
wd = bpy.data.worlds.new("w"); sc.world = wd; wd.use_nodes = True; wd.node_tree.nodes["Background"].inputs[1].default_value = 0.9; wd.node_tree.nodes["Background"].inputs[0].default_value = (0.95, 0.96, 0.97, 1)
def mat(name, col, metal=0.0, rough=0.4, alpha=1.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]; b.inputs["Base Color"].default_value = (*col, 1); b.inputs["Metallic"].default_value = metal; b.inputs["Roughness"].default_value = rough
    if alpha < 1: b.inputs["Alpha"].default_value = alpha; m.blend_method = "BLEND" if hasattr(m, "blend_method") else None
    return m
M = {k: mat(k, v, 0.9 if k in ("cu", "thermo", "al") else 0.0, 0.3 if k in ("cu", "thermo") else 0.5, 0.3 if k == "fr4" else 1.0) for k, v in FARBE.items()}
def mesh(name, verts, faces, m):
    me = bpy.data.meshes.new(name); me.from_pydata(verts, [], faces); me.update(); ob = bpy.data.objects.new(name, me); sc.collection.objects.link(ob); ob.data.materials.append(m); return ob
def quader(name, x0, y0, z0, x1, y1, z1, m):
    v = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    return mesh(name, v, [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)], m)
def rohr(name, x, y, z0, z1, r, m, n=10):
    v = [(x + r * math.cos(2 * math.pi * i / n), y + r * math.sin(2 * math.pi * i / n), z) for z in (z0, z1) for i in range(n)]
    f = [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)] + [tuple(range(n))[::-1], tuple(range(n, 2 * n))]
    return mesh(name, v, f, m)
def segment(name, x1, y1, x2, y2, w, z, m):
    dx, dy = x2 - x1, y2 - y1; L = math.hypot(dx, dy) or 1e-6; nx, ny = -dy / L * w / 2, dx / L * w / 2; ex, ey = dx / L * w / 2, dy / L * w / 2
    p = [(x1 - ex + nx, y1 - ey + ny), (x2 + ex + nx, y2 + ey + ny), (x2 + ex - nx, y2 + ey - ny), (x1 - ex - nx, y1 - ey - ny)]
    v = [(a, b, z - TC / 2) for a, b in p] + [(a, b, z + TC / 2) for a, b in p]
    return mesh(name, v, [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)], m)
def sammel(name, objs, m):   # viele Objekte zu einem Netz zusammenfassen (schneller Render)
    for o in bpy.context.view_layer.objects: o.select_set(False)
    for o in objs: o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]; bpy.ops.object.join(); ob = bpy.context.view_layer.objects.active; ob.name = name; return ob
# 1) Substrat (Platinenkörper)
quader("Substrat", 0, 0, Z["Substrat"] - TSUB / 2, W, H, Z["Substrat"] + TSUB / 2, M["fr4"])
# Lagenträger: sehr dünne, fast durchsichtige Platten zeigen die Lagenebenen (nur Darstellung)
mt = mat("lage", (0.75, 0.82, 0.9), 0.0, 0.5, 0.12)
for L in ("F.Cu", "In1.Cu", "In2.Cu", "B.Cu"): quader("Ebene_" + L, 0, 0, Z[L] - 0.05, W, H, Z[L] + 0.05, mt)
# 2) Kupfer je Lage
lay = {"F.Cu": [], "In1.Cu": [], "In2.Cu": [], "B.Cu": []}
for L, x1, y1, x2, y2, w in D["bahn"]: lay[L].append(segment("b", lx(x1), ly(y1), lx(x2), ly(y2), w, Z[L], M["cu"]))
for L, x, y, w, h, ref in D["pads"]: lay[L].append(quader("p", lx(x) - w / 2, ly(y) - h / 2, Z[L] - TC / 2, lx(x) + w / 2, ly(y) + h / 2, Z[L] + TC / 2, M["cu"]))
for L, net, pts in D["zonen"]:
    if len(pts) < 3: continue
    v = [(lx(a), ly(b), Z[L] - TC / 2) for a, b in pts] + [(lx(a), ly(b), Z[L] + TC / 2) for a, b in pts]; n = len(pts)
    f = [tuple(range(n))[::-1], tuple(range(n, 2 * n))] + [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
    lay[L].append(mesh("z", v, f, M["cu"]))
for L, objs in lay.items():
    if objs: sammel("Cu_" + L, objs, M["cu"])
# 3) Vias als Stäbe
vn = [rohr("v", lx(x), ly(y), Z["B.Cu"] - TC / 2, Z["F.Cu"] + TC / 2, d / 2 * 0.17, M["cu"]) for x, y, d, dr, net in D["vias"]]
if vn: sammel("Vias", vn, M["cu"])
vt = []; nth = 0
# 3b) Sperrzone: rot durchsichtige Platte über alle Ebenen, volle Plattenhöhe
mz = mat("sperr", (1.0, 0.05, 0.05), 0.0, 0.5, 0.28)
quader("Sperrzone", ZX0, 0, Z["B.Cu"] - 4, ZX1, H, Z["Bauteile"] + 14, mz)
# 4) Bauteile (STEP-Netz; Höhe 0 = Oberkante Platinenkörper)
pb = B["platine_bbox"]; zt = pb[5]
pts = [(p[0] - pb[0], p[1] - pb[1], p[2] - zt + Z["Bauteile"]) for p in B["punkte"]]
bo = mesh("Bauteile", pts, B["dreiecke"], M["bt"])
sc.collection.objects.link(bo) if bo.name not in sc.collection.objects else None
# Kamera (orthogonal, von schräg oben), Licht
allp = [Vector(o.matrix_world @ Vector(v)) for o in sc.objects for v in o.bound_box]
lo = Vector((min(p.x for p in allp), min(p.y for p in allp), min(p.z for p in allp))); hi = Vector((max(p.x for p in allp), max(p.y for p in allp), max(p.z for p in allp))); c = (lo + hi) / 2
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); sc.collection.objects.link(cam); sc.camera = cam; cam.data.type = "ORTHO"; cam.data.ortho_scale = 235.0; cam.data.shift_x = 0.10
dirv = Vector((0.55, -1.0, 0.7)).normalized(); cam.location = c + dirv * 600; cam.rotation_euler = (c - cam.location).to_track_quat("-Z", "Y").to_euler()
for az, en in ((35, 3.0), (-120, 1.2)):
    l = bpy.data.objects.new("l", bpy.data.lights.new("l", "SUN")); l.data.energy = en; l.rotation_euler = (math.radians(50), 0, math.radians(az)); sc.collection.objects.link(l)
bpy.context.view_layer.update()
os.makedirs(f"{O}/roh", exist_ok=True); sc.render.filepath = f"{O}/roh/explosion_roh.png"; bpy.ops.render.render(write_still=True)
def anker(p): q = world_to_camera_view(sc, cam, p); return [q.x, 1 - q.y]
A = {"Bauteile": anker(Vector((W, H * 0.5, Z["Bauteile"] + 3))), "F.Cu": anker(Vector((W, H * 0.5, Z["F.Cu"]))), "Substrat": anker(Vector((W, H * 0.5, Z["Substrat"]))), "In1.Cu": anker(Vector((W, H * 0.5, Z["In1.Cu"]))),
     "In2.Cu": anker(Vector((W, H * 0.5, Z["In2.Cu"]))), "B.Cu": anker(Vector((W, H * 0.5, Z["B.Cu"]))), "Sperrzone": anker(Vector(((ZX0 + ZX1) / 2, H, Z["Bauteile"] + 14))), "Vias": anker(Vector((lx(D["vias"][0][0]), ly(D["vias"][0][1]), (Z["F.Cu"] + Z["Substrat"]) / 2)))}
json.dump(dict(anker=A, vias_gesamt=len(D["vias"]), z=Z), open("/home/cae/hermes/batterie/sim/elektrik/e3c_bms_platine/explosion_anker.json", "w"))
bpy.ops.wm.save_as_mainfile(filepath=f"{O}/explosion.blend")
