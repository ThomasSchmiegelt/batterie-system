# KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. Auftrag G2-D (cad/zelle/AUFTRAG_DETAIL.md), Teil 2.
"""Rendert das Detailmodell (OBJ aus zelle_detail.py) mit Blender Cycles auf der CPU (orthografische Kamera, Maßstabsbalken exakt).
Schreibt Rohbilder nach $RENDER_ROH (Default Scratchpad/roh) und Anker-JSON (2D-Lage der Beschriftungspunkte) daneben;
Beschriftung, Balken, Fußzeile macht render_detail_beschriftung.py (PIL).
Aufruf: RENDER_SAMPLES=64 [RENDER_NUR=name] $BLENDER -b -P cad/zelle/render_detail.py
Maße: nur aus OBJ (mm), parameter_<V>_entwurf.json und ergebnis_detail_<V>.json."""
import bpy, os, json, math
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

R = os.environ.get("BATTERIE", "/home/cae/hermes/batterie")
ENT = f"{R}/cad/zelle/entwurf"; DET = f"{ENT}/detail"; RD = f"{DET}/render"
ROH = os.environ.get("RENDER_ROH", f"{DET}/roh")
os.makedirs(ROH, exist_ok=True)
SAMPLES = int(os.environ.get("RENDER_SAMPLES", "64"))
MM = 0.001
EL = json.load(open(f"{DET}/ergebnis_detail_LFP.json")); EN = json.load(open(f"{DET}/ergebnis_detail_NMC.json"))
PL = json.load(open(f"{ENT}/parameter_LFP_entwurf.json"))["parameter"]; PN = json.load(open(f"{ENT}/parameter_NMC_entwurf.json"))["parameter"]
L, B, D = (PL["BT-100"][k]["wert"] for k in ("laenge_mm", "breite_mm", "dicke_mm"))
Dm, H = PN["BT-100"]["durchmesser_mm"]["wert"], PN["BT-100"]["hoehe_mm"]["wert"]
YC, ZC = B/2, D/2

def reset(res=(1600, 900)):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene; sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = SAMPLES; sc.cycles.use_denoising = False
    sc.cycles.transparent_max_bounces = 16
    sc.render.resolution_x, sc.render.resolution_y = res; sc.render.resolution_percentage = 100
    sc.view_settings.view_transform = "Standard"
    w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
    nt = w.node_tree; bg = nt.nodes["Background"]; bg.inputs[1].default_value = 0.55
    tc = nt.nodes.new("ShaderNodeTexCoord"); sp = nt.nodes.new("ShaderNodeSeparateXYZ"); cr = nt.nodes.new("ShaderNodeValToRGB")
    nt.links.new(tc.outputs["Generated"], sp.inputs[0]); nt.links.new(sp.outputs["Z"], cr.inputs[0]); nt.links.new(cr.outputs[0], bg.inputs[0])
    cr.color_ramp.elements[0].position = 0.3; cr.color_ramp.elements[0].color = (0.30, 0.32, 0.36, 1)
    cr.color_ramp.elements[1].position = 0.8; cr.color_ramp.elements[1].color = (0.75, 0.77, 0.80, 1)
    return sc

def mat(name, base, metal=0.0, rough=0.5, alpha=1.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nd = m.node_tree.nodes; b = nd["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*base, 1); b.inputs["Metallic"].default_value = metal; b.inputs["Roughness"].default_value = rough
    if "Specular IOR Level" in b.inputs and name.startswith(("Kathode", "Anode")): b.inputs["Specular IOR Level"].default_value = 0.05
    if alpha < 1.0:   # Separator: halbtransparent
        b.inputs["Alpha"].default_value = alpha
    return m

M = {}
def werkstoffe():
    M.update({
        "kathode": mat("Kathode_dunkelgrau", (0.08, 0.08, 0.09), 0.0, 0.7), "anode": mat("Anode_schwarz", (0.012, 0.012, 0.014), 0.0, 0.6),
        "al": mat("Al_Folie_silber", (0.85, 0.86, 0.88), 1.0, 0.25), "cu": mat("Cu_Folie_kupfer", (0.95, 0.46, 0.30), 1.0, 0.25),
        "sep": mat("Separator_weiss", (0.97, 0.97, 0.95), 0.0, 0.4, alpha=0.45), "kunststoff": mat("Kunststoff_hellgrau", (0.38, 0.39, 0.40), 0.0, 0.5),
        "dicht": mat("Dichtung_schwarz", (0.015, 0.015, 0.015), 0.0, 0.7), "pet": mat("PET_Folie_blau", (0.01, 0.06, 0.45), 0.0, 0.2),
        "stahl": mat("Stahl_vernickelt", (0.62, 0.61, 0.58), 1.0, 0.18), "alu_gehaeuse": mat("Aluminium_Gehaeuse", (0.80, 0.81, 0.83), 1.0, 0.33),
        "beutel": mat("Isolationsbeutel", (0.8, 0.9, 1.0), 0.0, 0.2, alpha=0.22), "ventil": mat("Ventil_messing", (0.85, 0.65, 0.2), 1.0, 0.3),
        "bar_d": mat("Balken_dunkel", (0.02, 0.02, 0.02)), "bar_h": mat("Balken_hell", (0.95, 0.95, 0.95)),
    })
    for k in ("sep", "beutel"):   # Blend-Modus für Transparenz
        M[k].blend_method = "BLEND"
        nt = M[k].node_tree; b = nt.nodes["Principled BSDF"]
werkstoffe_fn = werkstoffe

WERKSTOFF = {  # Gruppenname -> Werkstoff
    "Kathode_Beschichtung": "kathode", "Anode_Beschichtung": "anode", "Al_Folie": "al", "Cu_Folie": "cu", "Separator": "sep", "Separator_Falz": "sep",
    "Stromschiene_Al_Kathode": "al", "Stromschiene_Cu_Anode": "cu", "Pol_plus_Al": "al", "Pol_minus_Cu": "cu", "Halter_Kathode": "kunststoff", "Halter_Anode": "kunststoff",
    "Isolationsbeutel": "beutel", "Gehaeuse_Al": "alu_gehaeuse", "O_Ringe": "dicht", "PET_Folie": "pet", "Ventil": "ventil", "Stopfen": "dicht",
    "Becher_Stahl": "stahl", "Rand_Al_oben": "al", "Rand_Cu_unten": "cu", "TabScheibe_Al_Kathode": "al", "TabScheibe_Cu_Anode": "cu", "Dichtring": "dicht",
    "Deckel": "stahl", "Isolierring": "kunststoff", "Blindniet_Cu": "cu", "Klebestreifen": "kunststoff",
}

def lade(var, satz, gruppe, offset=(0, 0, 0), ursprung=(0, 0, 0)):
    pf = f"{RD}/{var}_{satz}_{gruppe}.obj"
    if not os.path.exists(pf): return None
    bpy.ops.wm.obj_import(filepath=pf, global_scale=MM, forward_axis="Y", up_axis="Z")
    o = bpy.context.selected_objects[0]; o.name = f"{var}_{satz}_{gruppe}"
    o.location = (Vector(offset) - Vector(ursprung)) * MM
    # OBJ-Import legt Ursprung auf 0: mm-Koordinaten bleiben, Verschiebung über location
    o.data.materials.clear(); o.data.materials.append(M[WERKSTOFF[gruppe]] if gruppe != "Pol_plus_Al" or var == "LFP" else M["al"])
    bpy.ops.object.shade_smooth(); o.data.use_auto_smooth = True; o.data.auto_smooth_angle = math.radians(30)
    return o

def kamera(sc, ziel, richtung, skala, up=(0, 0, 1), res=None):
    d = bpy.data.cameras.new("cam"); d.type = "ORTHO"; d.ortho_scale = skala; d.clip_start = 0.01; d.clip_end = 20
    cam = bpy.data.objects.new("cam", d); sc.collection.objects.link(cam)
    rich = Vector(richtung).normalized(); cam.location = Vector(ziel)*MM + rich*3
    cam.rotation_euler = (0, 0, 0) if abs(rich.z) > 0.999 else (-rich).to_track_quat("-Z", "Y").to_euler()
    sc.camera = cam; bpy.context.view_layer.update()
    return cam

def licht(sc, ziel_mm, ls):
    for name, loc, e, size in ls:
        dd = bpy.data.lights.new(name, "AREA"); dd.energy = e; dd.size = size
        o = bpy.data.objects.new(name, dd); sc.collection.objects.link(o); o.location = Vector(loc)
        tr = o.constraints.new("TRACK_TO"); tg = bpy.data.objects.new(name + "_z", None); sc.collection.objects.link(tg)
        tg.location = Vector(ziel_mm)*MM; tr.target = tg; tr.track_axis = "TRACK_NEGATIVE_Z"; tr.up_axis = "UP_Y"

def boden(z_mm, groesse_mm=2000):
    bpy.ops.mesh.primitive_plane_add(size=groesse_mm*MM); o = bpy.context.active_object; o.location = (0, 0, z_mm*MM)
    m = mat("boden", (0.22, 0.23, 0.25), 0, 0.8); o.data.materials.append(m)

def schiene(name, mn, mx, mt):
    bpy.ops.mesh.primitive_cube_add(); o = bpy.context.active_object; o.name = name
    c = [(a + b)/2 for a, b in zip(mn, mx)]; dd = [b - a for a, b in zip(mn, mx)]
    o.location = Vector(c)*MM; o.scale = Vector(dd)*MM/2; o.data.materials.append(mt)

def rendern(name, ankers, ziel_mm, richtung, skala_mm, objekte, res=(1600, 900), lichtziel=None, extra=None, boden_z=None, samples=None):
    """objekte: Liste (var,satz,gruppe,offset). Anker: Liste (Text, Punkt_mm_in_Weltkoordinaten). Schreibt Rohbild und Anker-JSON."""
    sc = reset(res); werkstoffe()
    if samples: sc.cycles.samples = samples
    for var, satz, gr, off in objekte: lade(var, satz, gr, off)
    if extra: extra()
    if boden_z is not None: boden(boden_z)
    cam = kamera(sc, ziel_mm, richtung, skala_mm*MM)
    lz = lichtziel or ziel_mm
    licht(sc, lz, [("Key", (Vector(richtung).normalized()*1.4 + Vector((0.5, 0.0, 1.0)))[:], 25, 1.8), ("Fill", (-0.9, 0.8, 0.6), 10, 2.5), ("Rim", (0.5, 1.4, 1.1), 15, 1.4)])
    sc.render.filepath = f"{ROH}/{name}.png"; bpy.ops.render.render(write_still=True)
    pts = []
    for t, p in ankers:
        v = world_to_camera_view(sc, cam, Vector(p)*MM)
        pts.append({"text": t, "x": v.x*res[0], "y": (1 - v.y)*res[1]})
    json.dump({"aufloesung": list(res), "px_pro_mm": res[0]/skala_mm if res[0] >= res[1] else res[1]/skala_mm, "anker": pts}, open(f"{ROH}/{name}.json", "w"), ensure_ascii=False, indent=1)
    print("FERTIG", name)

# ----------------- Ansichten LFP -----------------
def lfp_ansichten(nur):
    ap = EL["annahmen"]; apol = ap["A_POL_H"]
    alle = ["Kathode_Beschichtung", "Anode_Beschichtung", "Al_Folie", "Cu_Folie", "Separator", "Separator_Falz", "Stromschiene_Al_Kathode", "Stromschiene_Cu_Anode",
            "Pol_plus_Al", "Pol_minus_Cu", "Halter_Kathode", "Halter_Anode", "Isolationsbeutel", "Gehaeuse_Al", "O_Ringe", "PET_Folie", "Ventil", "Stopfen"]
    if nur in (None, "LFP_gesamt"):
        ob = [("LFP", "voll", g, (0, 0, 0)) for g in ("Gehaeuse_Al", "PET_Folie", "Pol_plus_Al", "Pol_minus_Cu", "Ventil", "Stopfen", "O_Ringe")]
        an = [("Pol plus (Kathode, Al)", (L + apol, YC, ZC)), ("Pol minus (Anode, Cu)", (-apol, YC, ZC)), ("Ventil (Kathodenseite)", (L + 0.5, YC + ap["A_VENTIL_Y_MM"], ZC)),
              ("Gummistopfen Füllöffnung", (-1.0, YC + ap["A_STOPFEN_Y_MM"], ZC)), ("PET-Folie (blau) auf Al-Gehäuse", (L*0.55, 0, D*0.8))]
        rendern("LFP_gesamt", an, (L/2, YC, ZC), (-0.35, -0.75, 0.55), 800, ob, lichtziel=(L/2, YC, ZC), boden_z=-0.5)
    if nur in (None, "LFP_schnitt"):
        ob = [("LFP", "schnitt", g, (0, 0, 0)) for g in alle if g not in ("Pol_minus_Cu", "Stromschiene_Cu_Anode", "Halter_Anode", "Stopfen")]
        # Lagenmodell (Dicke x20) über dem Schnitt
        lx, lz = L - 52, D + 6
        ob += [("LFP", "lagen", g, (lx, YC - 6, lz)) for g in ("Kathode_Beschichtung", "Anode_Beschichtung", "Al_Folie", "Cu_Folie", "Separator")]
        xk = EL["laengen_mm"]["fahnenspitze_kathode_x"]
        an = [("Al-Gehäuse 0,3 mm", (L - 12, YC, 0.0)), ("Stapel (Schnitt)", (L - 48, YC, ZC - 3)), ("Kathodenfahnen (Al)", (xk - 4, YC, ZC + 3)),
              ("Stromschiene Al", (xk + 0.5, YC, ZC - 4)), ("Kunststoffhalter (2-teilig)", (xk + 12, YC, ZC + 3.2)), ("Pol plus", (L + 2, YC, ZC)),
              ("O-Ring", (L - 0.15, YC, ZC + 6.2)), ("Isolationsbeutel", (L - 40, YC, D - 0.45)), ("PET-Folie", (L - 25, YC, D + 0.02)),
              ("Separator-Falz", (L - 24.6, YC, ZC - 3)),
              ("Anode: Graphit-Beschichtung", (lx + 4, YC + 6, lz + 0.24 + 0.65)), ("Cu-Folie", (lx + 10, YC + 6, lz + 0.24 + 1.4)), ("Separator", (lx + 12, YC + 6, lz + 0.12)),
              ("Kathode: LFP-Beschichtung", (lx + 9, YC + 6, lz + 0.24 + 2.8 + 0.24 + 0.7)), ("Al-Folie", (lx + 17, YC + 6, lz + 0.24 + 2.8 + 0.24 + 1.6))]
        rendern("LFP_schnitt", an, (L - 25, YC, ZC + 9), (0.06, 0.97, 0.06), 60, ob, extra=None, boden_z=-0.5, lichtziel=(L - 25, YC, ZC))
    if nur in (None, "LFP_explosion"):
        dxs = {"Pol_plus_Al": 60, "O_Ringe": 38, "Halter_Kathode": 22, "Stromschiene_Al_Kathode": 8}
        ob = []
        for g in ("Kathode_Beschichtung", "Anode_Beschichtung", "Al_Folie", "Cu_Folie", "Separator", "Separator_Falz"):
            ob.append(("LFP", "ende", g, (0, 0, 0)))
        for g, dx in dxs.items(): ob.append(("LFP", "ende", g, (dx, 0, 0)))
        ob.append(("LFP", "schnitt", "Isolationsbeutel", (0, 0, 22))); ob.append(("LFP", "schnitt", "Gehaeuse_Al", (0, 0, 46))); ob.append(("LFP", "schnitt", "PET_Folie", (0, 0, 46)))
        ob.append(("LFP", "schnitt", "Ventil", (0, 0, 46)))
        xk = EL["laengen_mm"]["fahnenspitze_kathode_x"]
        an = [("Pol plus (Al)", (L - 5 + 60, YC, ZC)), ("O-Ring", (L - 0.15 + 38, YC, ZC + 6)), ("Kunststoffhalter (2 Teile, hier zusammen)", (xk + 12 + 22, YC, ZC + 4)),
              ("Stromschiene Al", (xk + 0.5 + 8, YC, ZC)), ("Stapel mit Fahnen", (L - 60, YC, ZC)),
              ("Isolationsbeutel (Hälfte)", (L - 30, YC, D - 0.4 + 22)), ("Al-Gehäuse + PET (Hälfte)", (L - 20, YC, D + 46))]
        rendern("LFP_explosion", an, (L - 22, YC, ZC + 24), (0.12, 0.92, 0.38), 200, ob, boden_z=-0.5, lichtziel=(L - 22, YC, ZC + 20), samples=128)

# ----------------- Ansichten NMC -----------------
def nmc_ansichten(nur):
    Rm = Dm/2
    if nur in (None, "NMC_gesamt"):
        ob = [("NMC", "voll", g, (0, 0, 0)) for g in ("Becher_Stahl", "Pol_plus_Al", "Deckel", "Dichtring")]
        an = [("Pluspol (Al)", (0, 0, H + 1)), ("Deckel mit Dichtring", (Rm - 1.5, 0, H - 0.2)), ("Becher = Minuspol (Stahl 0,4 mm)", (Rm, 0, H*0.45))]
        rendern("NMC_gesamt", an, (0, 0, H/2), (0.45, -0.7, 0.6), 185, ob, boden_z=-0.6)
    if nur in (None, "NMC_viertelschnitt"):
        gr = ["Becher_Stahl", "Kathode_Beschichtung", "Anode_Beschichtung", "Al_Folie", "Cu_Folie", "Separator", "Rand_Al_oben", "Rand_Cu_unten", "TabScheibe_Al_Kathode", "TabScheibe_Cu_Anode",
              "Dichtring", "Deckel", "Pol_plus_Al", "Isolierring", "Blindniet_Cu", "Ventil", "Klebestreifen"]
        ob = [("NMC", "viertel", g, (0, 0, 0)) for g in gr]
        w = EN["wickel"]; zo = w["hoehe_z_von_bis_mm"][1]
        an = [("Wickel (Spirale)", (-12, 0, H*0.6)), ("Kern (leer)", (-3.5, 0, H*0.6)), ("Becher", (-Rm + 0.2, 0, H*0.3)),
              ("Tab-Scheibe Al (6 Dreiecke)", (-12, 0, zo + 0.45)), ("Tab-Scheibe Cu (6 Dreiecke)", (-12, 0, 0.6 + 0.3)),
              ("Deckel + Pluspol", (0, 0, H + 0.5)), ("Dichtring", (-Rm + 1.4, 0, H - 0.5)), ("Isolierring", (-Rm + 1.5, 0, zo + 0.8)),
              ("Boden mit Blindniet", (0, 0, -0.3))]
        rendern("NMC_viertelschnitt", an, (0, 0, H/2), (0.55, 0.62, 0.60), 175, ob, boden_z=-0.6, samples=96)
    if nur in (None, "NMC_draufsicht"):
        gr = ["Becher_Stahl", "Kathode_Beschichtung", "Anode_Beschichtung", "Al_Folie", "Cu_Folie", "Separator", "Klebestreifen"]
        ob = [("NMC", "oben", g, (0, 0, 0)) for g in gr]
        w = EN["wickel"]
        an = [("Becher (Stahl)", (-Rm + 0.2, 0, 20)), ("Wickelkern (leer, Becherboden darunter)", (0, 0, 20)), ("Wickel: Spirale aus 4 Bändern", (8, 14, 20)), ("Kathode, Anode, Separator: siehe Ausschnitt", (0, -16, 20))]
        rendern("NMC_draufsicht", an, (0, 0, 20), (0, 0, 1), 52, ob, res=(1400, 1400), boden_z=-0.6, lichtziel=(0, 0, 20), samples=96)
    if nur in (None, "NMC_ausschnitt"):
        gr = ["Becher_Stahl", "Kathode_Beschichtung", "Anode_Beschichtung", "Al_Folie", "Cu_Folie", "Separator", "Klebestreifen"]
        ob = [("NMC", "oben", g, (0, 0, 0)) for g in gr]
        # Schichtlagen bei Winkel 180 Grad + 32 Windungen (alle Bänder vorhanden); Radien aus Parametern, nicht geschätzt
        um = 1e-3; kc, kf = PN["BT-111"]["beschichtung_um"]["wert"]*um, PN["BT-111"]["folie_um"]["wert"]*um
        ac, af = PN["BT-112"]["beschichtung_um"]["wert"]*um, PN["BT-112"]["folie_um"]["wert"]*um; ts = PN["BT-113"]["dicke_um"]["wert"]*um
        LP = EN["wickel"]["innenradius_je_band_bei_32,5_windungen_mm"]; rK, rS1, rA, rS2 = LP["K"], LP["S1"], LP["A"], LP["S2"]; rb = rK
        def pkt(r, y): return (-math.sqrt(r*r - y*y), y, 20)
        an = [("Becher 0,4 mm", (-Rm + 0.2, 0, 20)),
              ("Kathode: Al-Folie 20 µm", pkt(rK + kc + kf/2, -1.2)), ("Kathode: NMC-Beschichtung 75 µm", pkt(rK + kc + kf + kc/2, 1.6)),
              ("Separator 10 µm", pkt(rS1 + ts/2, -2.2)), ("Anode: Graphit 125 µm", pkt(rA + ac/2, 2.4)),
              ("Anode: Cu-Folie 10 µm", pkt(rA + ac + af/2, 0.0))]
        rendern("NMC_ausschnitt", an, (-(rb + 0.2), 0, 20), (0, 0, 1), 6.0, ob, res=(1400, 1400), boden_z=-0.6, lichtziel=(-rb, 0, 20), samples=128)

nur = os.environ.get("RENDER_NUR")
if not nur or nur.startswith("LFP"): lfp_ansichten(nur)
if not nur or nur.startswith("NMC"): nmc_ansichten(nur)
