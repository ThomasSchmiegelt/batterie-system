# KI-generiert (Claude Sonnet, 2026-11-18), Entwurf. Auftrag E2 Fortsetzung 5 (E2D, Konstruktionsstand). Blender CPU (Cycles). Aufruf: PACK_VARIANTE=LFP|NMC $BLENDER -b -P cad/pack/render_e2.py
# Liest ergebnis_<V>_e2.json (cad/pack/entwurf) und Netze aus /home/cae/cae_projekte/batterie/e2/ (von pack.py PACK_E2=1). E2-Teile farbig, Rest grau-transparent.
# Ausgabe: /home/cae/cae_projekte/batterie/e2/render/roh_<V>_<ansicht>.png und .json (Pixelabbildung für die Beschriftung).
import bpy, os, json, math
from mathutils import Vector
R = os.environ.get("BATTERIE", "/home/cae/hermes/batterie"); OUT = f"{R}/cad/pack/entwurf"; NZ = "/home/cae/cae_projekte/batterie/e2"; VAR = os.environ["PACK_VARIANTE"]; VO = VAR + "_e2d"
S = int(os.environ.get("RENDER_SAMPLES", "32")); MM = 0.001
ERG = json.load(open(f"{OUT}/ergebnis_{VO}.json")); E = ERG["e2"]; LG = ERG["gehaeuse_L_mm"]; BB = ERG["breite_mm"]
FARBE = {"E2_CMU": (0.85, 0.05, 0.05), "E2_FPC": (1.0, 0.75, 0.0), "E2_FPC_Detail": (1.0, 0.9, 0.2), "E2_FPC_Halter": (0.9, 0.6, 0.1), "E2_Daisy": (0.6, 0.3, 0.1), "E2_HV_Leitung": (0.85, 0.0, 0.7), "E2_Schaltbox": (0.1, 0.55, 0.25), "E2_Schaltbox_Deckel": (0.3, 0.7, 0.4),
         "E2_Schaltbox_Inhalt": (0.2, 0.85, 0.45), "E2_Stecker_Sensor": (0.0, 0.45, 0.95), "E2_Lasche": (1.0, 0.47, 0.0), "E2_Trennbruecke": (0.0, 0.78, 0.9), "E2_Trennbrueckenschraube": (0.0, 0.5, 0.6), "E2_Servicedeckel": (0.35, 0.4, 0.9),
         "E2_Stromschiene": (0.95, 0.55, 0.15), "E2_Schrumpfschlauch": (0.1, 0.1, 0.1), "E2_Schraube": (0.35, 0.35, 0.4), "E2_Dichtung": (0.05, 0.05, 0.05), "E2_Kabelschuh": (0.8, 0.5, 0.2), "E2_Clip": (0.9, 0.9, 0.9), "E2_Beruehrschutz": (0.9, 0.2, 0.2)}
GRAU = (0.55, 0.57, 0.6)
bx0, by0, bz0 = E["schaltbox_x0_y0_z0_mm"]; zbox = bz0
def bbox(netz, gr, filt=None):
    P = [p for g in gr if g in netz for p in netz[g]["punkte"] if (filt is None or filt(p))]
    return [(min(p[i] for p in P), max(p[i] for p in P)) for i in range(3)]
_ng = json.load(open(f"{NZ}/netz_{VO}_gesamt.json"))
_ctr = lambda bb: tuple((a_ + b_) / 2 for a_, b_ in bb)
_bx = bbox(_ng, ["E2_Schaltbox"]); _st = bbox(_ng, ["E2_Stecker_Sensor"]); _hv = bbox(_ng, ["E2_HV_Leitung"])
_fx0, _fx1 = E["fenster_x_mm"]
_fp = bbox(_ng, ["E2_FPC_Detail"], lambda p: _fx0 - 20 <= p[0] <= _fx1 + 20)
_bs = _ctr(_bx); _scl_box = 1.35 * max(_bx[0][1] - _bx[0][0], _bx[1][1] - _bx[1][0])
_hc = _ctr(bbox(_ng, ["E2_HV_Leitung", "E2_Stromschiene", "E2_Schaltbox"])); _hspan = bbox(_ng, ["E2_HV_Leitung", "E2_Lasche", "E2_Schaltbox"])
ANS = {"boxoffen": ("_boxoffen", (0.25, -0.55, 0.8), _scl_box, (1700, 1200), (_bs[0], _bs[1], 150.0), 0.18),
       "stecker": ("_gesamt", (-0.75, -0.55, 0.45) if VAR == "LFP" else (0.0, -1.0, 0.45), 330.0, (1700, 1000), _ctr(_st), 0.20),
       "detail": ("_ohnedeckel", (0.3, -0.75, 0.55) if VAR == "LFP" else (0.25, -0.5, 0.85), 110.0 if VAR == "LFP" else 200.0, (1700, 1000), ((_fx0 + _fx1) / 2, _fp[1][0] + (10.0 if VAR == "LFP" else 60.0), 85.0 if VAR == "LFP" else 105.0), 0.35),
       "kabel": ("_boxoffen", (0.0, 0.0, 1.0), 1.08 * max(_hspan[0][1] - _hspan[0][0], (_hspan[1][1] - _hspan[1][0]) * 1900 / 1450), (1900, 1450), (_ctr(_hspan)[0], _ctr(_hspan)[1], 100.0), 0.25),
       "gesamt": ("_gesamt", (0.85, -1.0, 0.6), 1.2 * LG, (1700, 1000), None, 0.20)}
if VAR == "LFP":
    _tb = bbox(_ng, ["E2_Trennbruecke"]); ANS["bruecke_zu"] = ("_gesamt", (0.55, -0.6, 0.65), 260.0, (1700, 1000), _ctr(_tb), 0.35); ANS["bruecke_offen"] = ("_bruecke_offen", (0.55, -0.6, 0.65), 260.0, (1700, 1000), _ctr(_tb), 0.35)
else:
    _tb = None
_NAHAUF = ("detail", "bruecke_zu", "bruecke_offen", "stecker")
def bau(name):
    suf, dirv, scale, res, ctr, alpha = ANS[name]
    netz = json.load(open(f"{NZ}/netz_{VO}{suf}.json"))
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
        if name == "detail" and not e2 and g not in ("Zellen", "Zellverbinder", "Gruppenverbinder", "Gruppenbruecke", "Zellabgriff", "Quertraeger", "Verguss", "Zelltraeger", "Pad"): continue
        if g == "Zellen": continue
        if name == "gesamt" and g in ("E2_Schaltbox_Inhalt",): pass
        me = bpy.data.meshes.new(g); me.from_pydata([(p[0] * MM, p[1] * MM, p[2] * MM) for p in pts], [], tri); me.update()
        ob = bpy.data.objects.new(g, me); sc.collection.objects.link(ob); ob["gruppe"] = g
        mt = bpy.data.materials.new(g); mt.use_nodes = True; b = mt.node_tree.nodes["Principled BSDF"]
        b.inputs["Base Color"].default_value = (*(FARBE[g] if e2 else tuple(0.75 * c_ for c_ in GRAU)), 1); b.inputs["Roughness"].default_value = 0.4
        if e2: b.inputs["Metallic"].default_value = 0.2
        if e2 and g == "E2_Beruehrschutz" and name == "detail": b.inputs["Alpha"].default_value = 0.3; mt.blend_method = "BLEND" if hasattr(mt, "blend_method") else None
        elif name in _NAHAUF and g in ("Zellen", "Zellverbinder", "Gruppenverbinder", "Gruppenbruecke", "Zellabgriff", "Quertraeger", "Verguss", "Zelltraeger", "Pad", "Kuehlplatte", "Deckel"): pass   # opak
        else:
            b.inputs["Alpha"].default_value = alpha if g not in ("Zellen",) else min(alpha, 0.35); mt.blend_method = "BLEND" if hasattr(mt, "blend_method") else None
        ob.data.materials.append(mt); obs.append(ob)
    if False: pass
    elif ctr: c = Vector((ctr[0] * MM, ctr[1] * MM, ctr[2] * MM))
    else:
        allp = [ob.matrix_world @ Vector(v) for ob in obs for v in ob.bound_box]
        c = (Vector((min(p.x for p in allp), min(p.y for p in allp), min(p.z for p in allp))) + Vector((max(p.x for p in allp), max(p.y for p in allp), max(p.z for p in allp)))) / 2
    cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); sc.collection.objects.link(cam); sc.camera = cam
    cam.data.type = "ORTHO"; cam.data.ortho_scale = scale * MM; cam.data.clip_end = 100
    cam.location = c + Vector(dirv).normalized() * 10; cam.rotation_euler = (c - cam.location).to_track_quat("-Z", "Y").to_euler()
    for az, en in ((35, 1.3), (-120, 0.6)):
        l = bpy.data.objects.new("l", bpy.data.lights.new("l", "SUN")); l.data.energy = en; l.rotation_euler = (math.radians(50), 0, math.radians(az)); sc.collection.objects.link(l)
    bpy.context.view_layer.update()
    sc.render.filepath = f"{NZ}/render/roh_{VAR}_e2d_{name}.png"; bpy.ops.render.render(write_still=True)
    json.dump({"res": res, "scale_mm": scale, "centre_mm": [c.x / MM, c.y / MM, c.z / MM], "dir": dirv}, open(f"{NZ}/render/roh_{VAR}_e2d_{name}.json", "w"))
for a in (os.environ.get("RENDER_NUR") or ",".join(ANS)).split(","): bau(a)
print("RENDER FERTIG", VAR)
