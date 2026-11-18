# KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. Auftrag G2-R (cad/zelle/AUFTRAG_RENDER.md).
"""Rendert die Zellen (OBJ aus export_mesh.py) mit Blender Cycles auf der CPU.
Aufruf: RENDER_SAMPLES=96 RENDER_PROZENT=100 $BLENDER -b -P cad/zelle/render_blender.py
Maße: nur aus den OBJ (mm) und entwurf/ergebnis_<V>.json (Beschriftung). Werkstoffe = Anmutung, keine Messung.
Orthografische Kamera: Maßstabsbalken ist exakt maßstäblich."""
import bpy, os, json, math
from mathutils import Vector

R = os.environ.get("BATTERIE", "/home/cae/hermes/batterie")
ENT = f"{R}/cad/zelle/entwurf"; RD = f"{ENT}/render"
SAMPLES = int(os.environ.get("RENDER_SAMPLES", "96")); PROZ = int(os.environ.get("RENDER_PROZENT", "100"))
MM = 0.001  # OBJ in mm -> Blender in m
ERG = {v: json.load(open(f"{ENT}/ergebnis_{v}.json")) for v in ("LFP", "NMC")}
CAPTION = "Entwurf – Akten vorgeschlagen, KI-generiert"

def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"
    sc.cycles.samples = SAMPLES; sc.cycles.use_denoising = False  # Blender-Build ohne OpenImageDenoise
    sc.render.resolution_x = 1600; sc.render.resolution_y = 900; sc.render.resolution_percentage = PROZ
    sc.render.film_transparent = False
    sc.view_settings.view_transform = "Filmic"
    sc.render.threads_mode = "AUTO"
    w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
    nt = w.node_tree; bg = nt.nodes["Background"]; bg.inputs[1].default_value = 0.8
    # Studio-Verlauf (dunkler Horizont, helles Zenit), damit Metall Kontrast spiegelt
    tc = nt.nodes.new("ShaderNodeTexCoord"); sp = nt.nodes.new("ShaderNodeSeparateXYZ"); cr = nt.nodes.new("ShaderNodeValToRGB")
    nt.links.new(tc.outputs["Generated"], sp.inputs[0]); nt.links.new(sp.outputs["Z"], cr.inputs[0]); nt.links.new(cr.outputs[0], bg.inputs[0])
    cr.color_ramp.elements[0].position = 0.35; cr.color_ramp.elements[0].color = (0.03, 0.03, 0.035, 1)
    cr.color_ramp.elements[1].position = 0.75; cr.color_ramp.elements[1].color = (0.9, 0.92, 0.95, 1)
    return sc

def mat(name, base, metal, rough, coat=0.0, brushed=False):
    m = bpy.data.materials.new(name); m.use_nodes = True
    n = m.node_tree.nodes; l = m.node_tree.links; b = n["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*base, 1); b.inputs["Metallic"].default_value = metal
    b.inputs["Roughness"].default_value = rough
    if coat: b.inputs["Coat Weight"].default_value = coat; b.inputs["Coat Roughness"].default_value = 0.05
    if brushed:  # gebürstet: Rauschen, längs der X-Achse gestreckt, als Bump
        tc = n.new("ShaderNodeTexCoord"); mp = n.new("ShaderNodeMapping"); no = n.new("ShaderNodeTexNoise"); bu = n.new("ShaderNodeBump")
        mp.inputs["Scale"].default_value = (3, 2500, 2500); no.inputs["Scale"].default_value = 40; no.inputs["Detail"].default_value = 6
        bu.inputs["Strength"].default_value = 0.12
        l.new(tc.outputs["Object"], mp.inputs["Vector"]); l.new(mp.outputs["Vector"], no.inputs["Vector"])
        l.new(no.outputs["Fac"], bu.inputs["Height"]); l.new(bu.outputs["Normal"], b.inputs["Normal"])
    return m

def werkstoffe():
    return {
        "alu": mat("Aluminium_gebuerstet", (0.86, 0.87, 0.89), 1.0, 0.33, brushed=True),
        "folie": mat("PET_Folie_blau", (0.008, 0.05, 0.40), 0.0, 0.16, coat=0.6),
        "nickel": mat("Stahl_vernickelt", (0.62, 0.61, 0.58), 1.0, 0.14),
        "kupfer": mat("Kupfer", (0.95, 0.46, 0.30), 1.0, 0.25),
        "boden": mat("Boden", (0.30, 0.31, 0.33), 0.0, 0.8),
        "bar_d": mat("Balken_dunkel", (0.02, 0.02, 0.02), 0.0, 0.6),
        "bar_h": mat("Balken_hell", (0.95, 0.95, 0.95), 0.0, 0.6),
    }

def lade(var, name, ort, M):
    pf = f"{RD}/{var}_{name}.obj"
    bpy.ops.wm.obj_import(filepath=pf, global_scale=MM, forward_axis="Y", up_axis="Z")
    o = bpy.context.selected_objects[0]; o.name = f"{var}_{name}"
    o.location = Vector(ort) * MM
    bpy.context.view_layer.objects.active = o; o.select_set(True)
    bpy.ops.object.shade_smooth(); o.data.use_auto_smooth = True; o.data.auto_smooth_angle = math.radians(35)
    return o

def zuweisen(o, M, wahl):  # wahl: Funktion(Flächennormale)-> Werkstoffname
    o.data.materials.clear()
    namen = []
    for p in o.data.polygons:
        k = wahl(p.normal)
        if k not in namen: namen.append(k); o.data.materials.append(M[k])
        p.material_index = namen.index(k)

def zelle(var, ort, M):
    teile = []
    g = lade(var, "Gehaeuse", ort, M)
    if var == "LFP":  # Stirnflächen (±X) Aluminium, übrige Flächen blaue PET-Folie (ENT-023)
        zuweisen(g, M, lambda n: "alu" if abs(n.x) > 0.9 else "folie")
        p = lade(var, "Pol_plus", ort, M); zuweisen(p, M, lambda n: "alu")
        q = lade(var, "Pol_minus", ort, M); zuweisen(q, M, lambda n: "kupfer")
        teile = [g, p, q]
    else:  # 4680: Stahlbecher vernickelt (ENT-028), Pluspol Deckel Aluminium
        zuweisen(g, M, lambda n: "nickel")
        p = lade(var, "Pol_plus", ort, M); zuweisen(p, M, lambda n: "alu")
        teile = [g, p]
    return teile

def box(name, mn, mx, m):
    bpy.ops.mesh.primitive_cube_add(); o = bpy.context.active_object; o.name = name
    c = [(a + b) / 2 for a, b in zip(mn, mx)]; d = [b - a for a, b in zip(mn, mx)]
    o.location = Vector(c) * MM; o.scale = Vector(d) * MM / 2; o.data.materials.append(m)
    return o

def text(s, size, loc_cam, cam, farbe=(0.04, 0.04, 0.04), align="LEFT"):
    bpy.ops.object.text_add(); t = bpy.context.active_object; t.data.body = s; t.data.size = size
    t.data.align_x = align; t.data.align_y = "BOTTOM"
    t.rotation_euler = cam.rotation_euler; t.location = cam.matrix_world @ Vector(loc_cam)
    m = bpy.data.materials.new("txt"); m.use_nodes = True; nd = m.node_tree.nodes
    nd.remove(nd["Principled BSDF"]); e = nd.new("ShaderNodeEmission"); e.inputs[0].default_value = (*farbe, 1); e.inputs[1].default_value = 1.0
    m.node_tree.links.new(e.outputs[0], nd["Material Output"].inputs[0]); t.data.materials.append(m)
    t.visible_shadow = False
    return t

def szene(titelzeilen, zellen, balken_mm, balken_x0, balken_y, ziel):
    sc = reset(); M = werkstoffe(); objs = []
    for var, ort in zellen: objs += zelle(var, ort, M)
    # Boden
    bpy.ops.mesh.primitive_plane_add(size=20); bo = bpy.context.active_object; bo.data.materials.append(M["boden"])
    # Maßstabsbalken (zwei Hälften dunkel/hell), auf dem Boden vor den Zellen
    h = balken_mm / 14; t = balken_mm / 14
    b1 = box("Balken1", (balken_x0, balken_y, 0), (balken_x0 + balken_mm / 2, balken_y + t, h), M["bar_d"])
    b2 = box("Balken2", (balken_x0 + balken_mm / 2, balken_y, 0), (balken_x0 + balken_mm, balken_y + t, h), M["bar_h"])
    objs += [b1, b2]
    # Kamera (orthografisch, isometrisch-schräg)
    cam_d = bpy.data.cameras.new("cam"); cam_d.type = "ORTHO"; cam_d.clip_start = 0.01; cam_d.clip_end = 50
    cam = bpy.data.objects.new("cam", cam_d); sc.collection.objects.link(cam); sc.camera = cam
    rich = Vector((0.62, -0.78, 0.62)).normalized()  # Blickrichtung von Ziel zur Kamera
    # Ausdehnung in Kamerakoordinaten
    cam.location = rich * 5; 
    fwd = -rich; cam.rotation_euler = fwd.to_track_quat("-Z", "Y").to_euler(); bpy.context.view_layer.update()
    inv = cam.matrix_world.inverted()
    xs, ys = [], []
    for o in objs:
        for c in o.bound_box:
            v = inv @ (o.matrix_world @ Vector(c)); xs.append(v.x); ys.append(v.y)
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2; w, hh = max(xs) - min(xs), max(ys) - min(ys)
    S = max(w * 1.14, hh * 16 / 9 * 1.55)
    cam.location = cam.matrix_world @ Vector((cx, cy + 0.06 * S, 0)); cam_d.ortho_scale = S; bpy.context.view_layer.update()
    # Licht (3 Punkt)
    def licht(name, kind, loc, energie, groesse, farbe=(1, 1, 1)):
        d = bpy.data.lights.new(name, kind); d.energy = energie; d.color = farbe
        if kind == "AREA": d.size = groesse
        o = bpy.data.objects.new(name, d); sc.collection.objects.link(o); o.location = Vector(loc)
        tr = o.constraints.new("TRACK_TO"); tgt = bpy.data.objects.new(name + "_z", None); sc.collection.objects.link(tgt)
        tgt.location = Vector((0.3, -0.05, 0.02)); tr.target = tgt; tr.track_axis = "TRACK_NEGATIVE_Z"; tr.up_axis = "UP_Y"
    licht("Key", "AREA", (1.4, -1.6, 1.8), 260, 1.6, (1.0, 0.97, 0.92))
    licht("Fill", "AREA", (-1.2, -1.4, 0.9), 90, 2.2, (0.9, 0.95, 1.0))
    licht("Rim", "AREA", (0.3, 1.8, 1.2), 170, 1.2)
    # Texte (Kamerakoordinaten: x rechts, y oben, z = -Abstand)
    zl = -1.0
    for i, s in enumerate(titelzeilen):
        text(s, 0.028 * S, (-S / 2 + 0.03 * S, S * 9 / 32 - 0.05 * S - i * 0.04 * S, zl), cam)
    text(CAPTION, 0.020 * S, (-S / 2 + 0.03 * S, -S * 9 / 32 + 0.025 * S, zl), cam, farbe=(0.25, 0.05, 0.05))
    inv = cam.matrix_world.inverted()
    bc = inv @ Vector(((balken_x0 + balken_mm / 2) * MM, balken_y * MM, 0))
    text(f"{balken_mm:g} mm", 0.024 * S, (bc.x, bc.y - 0.05 * S, zl), cam, align="CENTER")
    sc.render.filepath = ziel
    bpy.ops.render.render(write_still=True)

def beschr(v):
    e = ERG[v]; m = e["masse_eingabe"]
    if v == "LFP": g = f"{m['laenge_mm']:g} x {m['breite_mm']:g} x {m['dicke_mm']:g} mm"
    else: g = f"Durchmesser {m['durchmesser_mm']:g} x {m['hoehe_mm']:g} mm"
    return f"{v}: {g}, {e['kapazitaet_Ah']:g} Ah"

LFPpos = (0, 0, 0); NMCpos = (-70, -60, 0)
ansichten = {
  "zellen_vergleich": ([("LFP", LFPpos), ("NMC", NMCpos)], ["Zellen im selben Maßstab", beschr("LFP"), beschr("NMC")], 100, 230, -105),
  "zelle_LFP_render": ([("LFP", LFPpos)], [beschr("LFP")], 100, 280, -45),
  "zelle_NMC_render": ([("NMC", (0, 0, 0))], [beschr("NMC")], 20, -80, 15),
}
nur = os.environ.get("RENDER_NUR")
for k, (zl, tz, bm, bx, by) in ansichten.items():
    if nur and k != nur: continue
    szene(tz, zl, bm, bx, by / 1.0, f"{RD}/{k}.png")
    print("FERTIG", k)
