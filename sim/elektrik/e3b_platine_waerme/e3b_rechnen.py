#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-24), Entwurf. E3b: stationaere Temperatur der CMU-Platine (Elmer), Auftrag Opus, Grundlage ERWARTUNG.md.
Aufruf: python3 e3b_rechnen.py FALL VAR NETZ [SENS]   FALL a|b|c, VAR LFP|NMC, NETZ grob|fein, SENS cu0 (Kupferflaechen ohne Beitrag, lambda_xy = 0,8) oder leer
Alle Werte aus ERWARTUNG.md (Annahmen Opus 'ERW-E3b'), P aus ../e3_platine/ergebnis_ausgleich.json, Lage der Quellen aus dem kicad_pcb (Footprints R_2512, SOT-23).
Geometrie: Plan x (Platinenlaenge 120) y (60) wie im kicad_pcb; z = 0 Unterseite Pad (Wand), Pad 1 mm, Platine 1,6 mm. Heizflaechen = Footprint-Flaeche auf der Oberseite (Flussrandbedingung)."""
import json, os, re, sys, math, subprocess
import numpy as np
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(os.path.join(H, "../../.."))
FALL, VAR, NETZ = sys.argv[1:4]; SENS = sys.argv[4] if len(sys.argv) > 4 else ""
E3 = json.load(open(f"{R}/sim/elektrik/e3_platine/ergebnis_ausgleich.json"))[VAR]
# ---- Eingaben (ERW-E3b)
EIN = dict(lam_fr4_z=0.3, lam_fr4_xy=0.8, lam_cu=390.0, cu_um=[70, 35, 35, 70], t_pcb=1.6, t_pad=1.0, lam_pad=3.0, T_wand=45.0, T_umg=45.0, h=5.0, eps=0.9,
           vias_je_paar=8, via_d_mm=0.3, laenge=120.0, breite=60.0, R_fp_mm=(3.2, 6.3), Q_fp_mm=(2.9, 1.3))
P_R, P_Q = E3["P_Widerstand_je_Umax_W"], E3["P_FET_Umax_W"]
lam_xy = EIN["lam_fr4_xy"] if SENS == "cu0" else (EIN["lam_fr4_xy"]*(EIN["t_pcb"]-sum(EIN["cu_um"])/1000)+EIN["lam_cu"]*sum(EIN["cu_um"])/1000)/EIN["t_pcb"]
# ---- Lage der Waermequellen aus dem kicad_pcb
t = open(f"/home/cae/cae_projekte/batterie/e3/cmu_{VAR}.kicad_pcb").read(); res, fet = [], []
for b in re.split(r"\n\t\(footprint ", t)[1:]:
    n = re.match(r'"([^"]+)"', b).group(1); a = re.search(r"\(at ([\-\d\.]+) ([\-\d\.]+)(?: ([\-\d\.]+))?\)", b)
    x, y, rot = float(a.group(1)), float(a.group(2)), float(a.group(3) or 0)
    if n.startswith("R_2512"): res.append((x, y, rot))
    if n.startswith("SOT-23"): fet.append((x, y, rot))
assert len(res) == 36 and len(fet) == 18
rect = lambda x, y, d: (x-d[0]/2, y-d[1]/2, x+d[0]/2, y+d[1]/2)
RR = [rect(x, y, EIN["R_fp_mm"] if abs(rot) % 180 == 90 and False else (EIN["R_fp_mm"])) for x, y, rot in res]   # 2512 gedreht 90 Grad im Layout: x 3,2 / y 6,3 (R_fp_mm bereits so)
QQ = [rect(x, y, EIN["Q_fp_mm"]) for x, y, rot in fet]
pairs = []
for y0 in sorted(set(r[1] for r in res)):
    xs = sorted(r[0] for r in res if r[1] == y0)
    for i in range(0, len(xs), 2): pairs.append((xs[i]-1.6, y0-3.15, xs[i+1]+1.6, y0+3.15))
assert len(pairs) == 18
A_via = (pairs[0][2]-pairs[0][0])*(pairs[0][3]-pairs[0][1]); f_via = EIN["vias_je_paar"]*math.pi*(EIN["via_d_mm"]/2)**2/A_via
lam_via_z = EIN["lam_fr4_z"]+f_via*EIN["lam_cu"]    # gefuellte Vias = Obergrenze (Hülsenwand nicht angenommen)
h_mesh = dict(grob=0.8, fein=0.5)[NETZ]
D = f"{H}/lauf/{FALL}_{VAR}_{NETZ}{'_'+SENS if SENS else ''}"; os.makedirs(D, exist_ok=True)
def netz2():
    import gmsh
    gmsh.initialize(["-nopopup"]); gmsh.option.setNumber("General.Terminal", 0); gm = gmsh.model; oc = gm.occ
    z0 = 0.0 if FALL == "c" else EIN["t_pad"]; zt = z0+EIN["t_pcb"]; Lx, Ly = EIN["laenge"], EIN["breite"]
    objs = []
    if FALL != "c": objs.append((3, oc.addBox(0, 0, 0, Lx, Ly, EIN["t_pad"])))
    objs.append((3, oc.addBox(0, 0, z0, Lx, Ly, EIN["t_pcb"])))
    tools = [(3, oc.addBox(p[0], p[1], z0, p[2]-p[0], p[3]-p[1], EIN["t_pcb"])) for p in pairs]
    tools += [(2, oc.addRectangle(r[0], r[1], zt, r[2]-r[0], r[3]-r[1])) for r in RR+QQ]
    # Via-Boxen schneiden die Platine; Platine ohne Via = Rest. Fragment liefert Teilvolumen.
    oc.fragment(objs, tools); oc.synchronize()
    gmsh.option.setNumber("Mesh.MeshSizeMax", h_mesh); gmsh.option.setNumber("Mesh.MeshSizeMin", h_mesh/4)
    gmsh.option.setNumber("Mesh.MeshSizeFromPoints", 0); gmsh.option.setNumber("Mesh.MeshSizeExtendFromBoundary", 1); gmsh.option.setNumber("Mesh.Algorithm3D", 1)
    inb = lambda x, y, r: r[0]-1e-6 <= x <= r[2]+1e-6 and r[1]-1e-6 <= y <= r[3]+1e-6
    tags = {"pad": [], "pcb": [], "via": [], "top": [], "res": [], "fet": [], "wand": [], "unten": [], "seite": []}
    for d, s in gm.getEntities(3):
        c = oc.getCenterOfMass(3, s); z = c[2]
        if z < z0 - 1e-6 and FALL != "c": tags["pad"].append(s)
        elif any(inb(c[0], c[1], p) for p in pairs) and FALL != "x": tags["via"].append(s)
        else: tags["pcb"].append(s)
    for d, s in gm.getEntities(2):
        c = oc.getCenterOfMass(2, s); bb = gm.getBoundingBox(2, s); dz = bb[5]-bb[2]
        if dz > 1e-6: tags["seite"].append(s); continue
        z = c[2]
        if abs(z-zt) < 1e-6:
            tags["res" if any(inb(c[0], c[1], r) for r in RR) else "fet" if any(inb(c[0], c[1], q) for q in QQ) else "top"].append(s)
        elif abs(z) < 1e-6: tags["wand" if FALL != "c" else "unten"].append(s)
    ID = dict(pad=1, pcb=2, via=3, top=10, res=11, fet=12, wand=20, unten=21, seite=30)
    for k, v in tags.items():
        if v: gm.addPhysicalGroup(3 if k in ("pad", "pcb", "via") else 2, v, ID[k], name=k)
    gm.mesh.generate(3); gmsh.write(f"{D}/netz.msh"); n_el = len(gm.mesh.getElementsByType(4)[0]); n_nod = len(gm.mesh.getNodes()[0]); gmsh.finalize()
    subprocess.run(["ElmerGrid", "14", "2", f"{D}/netz.msh", "-autoclean", "-out", D, "-names"], check=True, stdout=subprocess.DEVNULL)
    return dict(tets=n_el, knoten=n_nod, gruppen={k: len(v) for k, v in tags.items()})
def sif():
    # Elmer ElmerGrid -names: Ordner = D/netz
    A_R = (EIN["R_fp_mm"][0]*EIN["R_fp_mm"][1])*1e-6; A_Q = (EIN["Q_fp_mm"][0]*EIN["Q_fp_mm"][1])*1e-6
    Tk = lambda c: c+273.15
    s = [f'Header\n  Mesh DB "{D}" "."\n  Results Directory "{D}"\nEnd\n',
         'Simulation\n  Coordinate System = Cartesian 3D\n  Coordinate Scaling = 0.001\n  Simulation Type = Steady State\n  Steady State Max Iterations = 1\n  Output Intervals = 1\n  Post File = "e3b.vtu"\nEnd\n',
         'Constants\n  Stefan Boltzmann = 5.670374e-8\nEnd\nEquation 1\n  Active Solvers(2) = 1 2\nEnd\n',
         'Solver 1\n  Equation = Heat Equation\n  Procedure = "HeatSolve" "HeatSolver"\n  Variable = Temperature\n  Calculate Loads = True\n  Linear System Solver = Iterative\n  Linear System Iterative Method = BiCGStab\n  Linear System Max Iterations = 5000\n  Linear System Convergence Tolerance = 1.0e-10\n  Linear System Preconditioning = ILU1\n  Nonlinear System Max Iterations = 60\n  Nonlinear System Convergence Tolerance = 1.0e-7\n  Nonlinear System Newton After Iterations = 3\n  Nonlinear System Newton After Tolerance = 1.0e-2\n  Steady State Convergence Tolerance = 1.0e-7\nEnd\n',
         f'Solver 2\n  Equation = SaveScalars\n  Procedure = "SaveData" "SaveScalars"\n  Filename = scalars.dat\n  Variable 1 = Temperature\n  Operator 1 = max\n  Operator 2 = min\n'+("  Variable 3 = Temperature Loads\n  Operator 3 = boundary sum\n" if FALL != "c" else "")+'End\n',
         f'Solver 3\n  Exec Solver = After Simulation\n  Equation = ResultOutput\n  Procedure = "ResultOutputSolve" "ResultOutputSolver"\n  Output File Name = e3b\n  Vtu Format = Logical True\n  Save Geometry Ids = Logical True\nEnd\n',
         f'Material 1\n  Name = "Pad"\n  Heat Conductivity = {EIN["lam_pad"]}\nEnd\n',
         f'Material 2\n  Name = "Platine"\n  Heat Conductivity(3,3) = Real {lam_xy} 0 0  0 {lam_xy} 0  0 0 {EIN["lam_fr4_z"]}\nEnd\n',
         f'Material 3\n  Name = "Platine_Vias"\n  Heat Conductivity(3,3) = Real {lam_xy} 0 0  0 {lam_xy} 0  0 0 {lam_via_z if FALL == "a" else EIN["lam_fr4_z"]}\nEnd\n']
    s[2] = s[2].replace("Active Solvers(2) = 1 2", "Active Solvers(3) = 1 2 3")
    for b in (1, 2, 3): s.append(f"Body {b}\n  Target Bodies(1) = {b}\n  Equation = 1\n  Material = {b}\n  Initial Condition = 1\nEnd\n")
    s.append(f"Initial Condition 1\n  Temperature = {Tk(EIN['T_umg'])+20}\nEnd\n")
    rob = f"  Radiation = Idealized\n  Emissivity = {EIN['eps']}\n  Radiation External Temperature = {Tk(EIN['T_umg'])}\n  Heat Transfer Coefficient = {EIN['h']}\n  External Temperature = {Tk(EIN['T_umg'])}\n"
    bc = [("top", 10, rob), ("res", 11, rob+f"  Heat Flux = {P_R/A_R}\n"), ("fet", 12, rob+f"  Heat Flux = {P_Q/A_Q}\n")]
    bc += [("wand", 20, f"  Temperature = {Tk(EIN['T_wand'])}\n  Save Scalars = True\n")] if FALL != "c" else [("unten", 21, rob)]
    nm = {m.group(1): int(m.group(2)) for m in re.finditer(r"\$ (\w+) = (\d+)", open(f"{D}/mesh.names").read().split("boundaries")[1])}
    for i, (n, tg, body) in enumerate(bc): tg = nm[n]; s.append(f"Boundary Condition {i+1}\n  Target Boundaries(1) = {tg}\n{body}End\n")
    open(f"{D}/e3b.sif", "w").write("\n".join(s)); open(f"{D}/ELMERSOLVER_STARTINFO", "w").write("e3b.sif\n")
if __name__ == "__main__":
    info = netz2(); sif(); info.update(lam_xy=lam_xy, lam_via_z=lam_via_z, f_via=f_via, A_via_paar_mm2=A_via)
    json.dump(info, open(f"{D}/netzinfo.json", "w"), indent=1); print(info)
