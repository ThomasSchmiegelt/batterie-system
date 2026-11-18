# KI-generiert (Claude Sonnet, 2026-11-18), Entwurf. Auftrag E2 Fortsetzung 2. Blender CPU (Cycles). Aufruf: PACK_VARIANTE=LFP|NMC $BLENDER -b -P cad/pack/render_e2.py
# Liest ergebnis_<V>_e2.json (cad/pack/entwurf) und Netze aus /home/cae/cae_projekte/batterie/e2/ (von pack.py PACK_E2=1). E2-Teile farbig, Rest grau-transparent.
# Ausgabe: /home/cae/cae_projekte/batterie/e2/render/roh_<V>_<ansicht>.png und .json (Pixelabbildung für die Beschriftung).
import bpy, os, json, math
from mathutils import Vector
R = os.environ.get("BATTERIE", "/home/cae/hermes/batterie"); OUT = f"{R}/cad/pack/entwurf"; NZ = "/home/cae/cae_projekte/batterie/e2"; VAR = os.environ["PACK_VARIANTE"]; VO = VAR + "_e2"
S = int(os.environ.get("RENDER_SAMPLES", "32")); MM = 0.001
ERG = json.load(open(f"{OUT}/ergebnis_{VO}.json")); E = ERG["e2"]; LG = ERG["gehaeuse_L_mm"]; BB = ERG["breite_mm"]
FARBE = {"E2_CMU": (0.85, 0.05, 0.05), "E2_FPC": (1.0, 0.75, 0.0), "E2_HV_Leitung": (0.85, 0.0, 0.7), "E2_Schaltbox": (0.1, 0.55, 0.25), "E2_Schaltbox_Inhalt": (0.2, 0.85, 0.45), "E2_Stecker_Sensor": (0.0, 0.45, 0.95)}
GRAU = (0.55, 0.57, 0.6)
bx0, by0, bz0 = E["schaltbox_x0_y0_z0_mm"]; zbox = bz0
ANS = {"gesamt": ("", (0.85, -1.0, 0.6), 1.2 * LG, (1700, 1000), None, 0.20),
       "draufsicht": ("_ohnedeckel", (0.0, 0.0, 1.0), 1.06 * LG, (1900, 1450), None, 0.25),
       "schnitt": ("_boxschnitt", (0.0, -1.0, 0.0), 700.0, (1700, 900), (bx0 + 150.0, by0 + E["schaltbox_B_mm"] / 2, 100.0), 0.30),
       "detail": ("_ohnedeckel", (-0.7, -0.45, 0.85), 300.0, (1700, 1000), "detail", 0.35)}
def bau(name):
    suf, dirv, scale, res, ctr, alpha = ANS[name]
    netz = json.load(open(f"{NZ}/netz_{VO}{suf}.json" if suf else f"{OUT}/netz_{VO}.json"))
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene; sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = S; sc.cycles.use_denoising = False
    sc.render.resolution_x, sc.render.resolution_y = res; sc.render.resolution_percentage = 100; sc.view_settings.view_transform = "Standard"
    wd = bpy.data.worlds.new("w"); sc.world = wd; wd.use_nodes = True
    wd.node_tree.nodes["Background"].inputs[1].default_value = 0.9; wd.node_tree.nodes["Background"].inputs[0].default_value = (0.97, 0.97, 0.98, 1)
    obs = []
    for g, m in netz.items():
        pts, tri = m["punkte"], m["dreiecke"]
        if not pts: continue
        e2 = g in FARBE
        if name == "detail" and not e2 and g not in ("Zellen", "Zellverbinder", "Gruppenverbinder", "Gruppenbruecke", "Zellabgriff", "Quertraeger", "Verguss", "Zelltraeger"): continue
        if name == "gesamt" and g == "Zellen": continue          # Zellen verdecken sonst alles
        me = bpy.data.meshes.new(g); me.from_pydata([(p[0] * MM, p[1] * MM, p[2] * MM) for p in pts], [], tri); me.update()
        ob = bpy.data.objects.new(g, me); sc.collection.objects.link(ob); ob["gruppe"] = g
        mt = bpy.data.materials.new(g); mt.use_nodes = True; b = mt.node_tree.nodes["Principled BSDF"]
        b.inputs["Base Color"].default_value = (*(FARBE[g] if e2 else GRAU), 1); b.inputs["Roughness"].default_value = 0.4
        if e2: b.inputs["Metallic"].default_value = 0.2
        elif name in ("draufsicht", "detail") and g in ("Zellen", "Zellverbinder", "Gruppenverbinder", "Gruppenbruecke", "Zellabgriff", "Quertraeger", "Verguss", "Zelltraeger"): pass   # opak
        else:
            b.inputs["Alpha"].default_value = alpha if g not in ("Zellen",) else min(alpha, 0.35); mt.blend_method = "BLEND" if hasattr(mt, "blend_method") else None
        ob.data.materials.append(mt); obs.append(ob)
    if ctr == "detail":   # Ecke hinten bei der ersten hinteren CMU (sonst vorn), Mitte in Zellhöhe
        sd = "hinten" if any(c["seite"] == "hinten" for c in E["geometrie"]["cmu"]) else "vorn"; cm = [c for c in E["geometrie"]["cmu"] if c["seite"] == sd][0]
        c = Vector((cm["x"] * MM - (0.02 if sd == "hinten" else -0.02) , (cm["y"] + 30) * MM, ERG["hoehe_stapel_mm"] * 0.35 * MM))
    elif ctr: c = Vector((ctr[0] * MM, ctr[1] * MM, ctr[2] * MM))
    else:
        allp = [ob.matrix_world @ Vector(v) for ob in obs for v in ob.bound_box]
        c = (Vector((min(p.x for p in allp), min(p.y for p in allp), min(p.z for p in allp))) + Vector((max(p.x for p in allp), max(p.y for p in allp), max(p.z for p in allp)))) / 2
    cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); sc.collection.objects.link(cam); sc.camera = cam
    cam.data.type = "ORTHO"; cam.data.ortho_scale = scale * MM; cam.data.clip_end = 100
    cam.location = c + Vector(dirv).normalized() * 10; cam.rotation_euler = (c - cam.location).to_track_quat("-Z", "Y").to_euler()
    for az, en in ((35, 1.8), (-120, 0.8)):
        l = bpy.data.objects.new("l", bpy.data.lights.new("l", "SUN")); l.data.energy = en; l.rotation_euler = (math.radians(50), 0, math.radians(az)); sc.collection.objects.link(l)
    bpy.context.view_layer.update()
    sc.render.filepath = f"{NZ}/render/roh_{VAR}_{name}.png"; bpy.ops.render.render(write_still=True)
    json.dump({"res": res, "scale_mm": scale, "centre_mm": [c.x / MM, c.y / MM, c.z / MM], "dir": dirv}, open(f"{NZ}/render/roh_{VAR}_{name}.json", "w"))
for a in (os.environ.get("RENDER_NUR") or ",".join(ANS)).split(","): bau(a)
print("RENDER FERTIG", VAR)
