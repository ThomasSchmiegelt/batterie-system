#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-21), Entwurf. K4: Elmer-Waermeleitung des LFP-Packs (homogenisierter Zellblock) mit Kuehlplatten-Randbedingung.
Aufruf: python3 k4_elmer.py netz | sif | rechnen | auswerten   [--probe: grobes Netz, 3 Schritte]
Schichten (z): Blech - Pad - Zellblock (6 Lagen) - Pad - Blech; Plan = Plattenflaeche. Aussenflaechen adiabat (Annahme, Rahmen/Boden/Deckel nicht modelliert).
Randbedingung Blech aussen: Robin, h_eff aus K3 (h_fx, eta aus K2b), T_Fluid(Ort) linear entlang des Maeanders (8 Bahnen laengs, wechselnde Richtung, Ober-/Unterplatte gleichsinnig = Annahme).
V4 nach ENT-158, Auftrag Opus 2026-11-23: gruppierte Parallelfuehrung (Nachtrag 1 ERWARTUNG K5; k = bestes k aus ../k5_parallel/ergebnis_verteiler.json, je 8/k Bahnen in Reihe, Gruppen gleich durchstroemt), Fluidtemperatur linear ueber den Gruppenweg,
Durchfluss x3, obere Platte gegenlaeufig; h aus K3-Korrelation (kuehlplatte.kanal) fuer Q/(k*m_teilkanaele) je Teilkanal.
Alle Zahlen aus eingaben.json (Herkunft dort) und Ergebnisdateien. Zwischenstand je Segment (restart.dat), STOP-Pruefung zwischen Segmenten."""
import json, os, sys, subprocess, math, glob
import numpy as np
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(os.path.join(H, "../../.."))
E = json.load(open(f"{H}/eingaben.json")); K4 = E["k4"]; probe = "--probe" in sys.argv
arg = lambda n, d: sys.argv[sys.argv.index(n)+1] if n in sys.argv else d
FALL = arg("--fall", "LFP_P0"); VAR = arg("--var", "V0"); VF = "LFP" if FALL.startswith("LFP") else "NMC"; DAUER = FALL.endswith("_DAUER")
K2FALL = "LFP_P0" if VF == "LFP" else "NMC_P4"; V_GEGEN = VAR in ("V1", "V3", "V4"); V_FLOW = 3.0 if VAR in ("V4", "V4p") else 2.0 if VAR in ("V2", "V3") else 1.0; PARALLEL = VAR in ("V4", "V4p")   # V4p (Opus 2026-11-23): wie V4, aber ohne Gegenlauf (gebautes CAD G5.9, V_GEGEN False)
KG = json.load(open(f"{R}/sim/kuehlung/k5_parallel/ergebnis_verteiler.json"))["gruppen"]["bestes"] if PARALLEL else None   # z. B. "k2_d25_x3"
KGRP = int(KG.split("_")[0][1:]) if PARALLEL else 1        # Zahl paralleler Gruppen k (je 8/k Bahnen in Reihe); k = 8 = Einzelbahnen parallel
D = f"{H}/elmer_{FALL}_{VAR}{'_probe' if probe else ''}"; os.makedirs(D, exist_ok=True)
P = json.load(open(f"{R}/cad/pack/entwurf/parameter_{VF}.json"))["A"]; PG = json.load(open(f"{R}/cad/pack/entwurf/ergebnis_{VF}.json"))
rand = P["A_rand_mm"]["wert"]; Lx, Ly = PG["laenge_mm"]-2*rand, PG["breite_mm"]-2*rand           # Plattenflaeche (wie k2 platte())
zl = json.load(open(f"{R}/cad/pack/entwurf/parameter_{VF}.json"))["parameter"]["BT-100"]
if VF == "LFP":
    cl, cb, cd = zl["laenge_mm"]["wert"], zl["breite_mm"]["wert"], zl["dicke_mm"]["wert"]        # Zelle: Laenge 681 (y), Breite=Hoehe 90 (z), Dicke 14 (x)
    pitch = cd+P["A_zellabstand_LFP_mm"]["wert"]; n_row = P["A_zellzahl_LFP"]["wert"]//2
    bx, by = n_row*pitch, 2*cl
else:
    cb = zl["hoehe_mm"]["wert"]; bx, by = Lx, Ly          # NMC: Block = ganze Plattenflaeche, Hoehe 80 mm, homogenisiert (siehe stoffe())
x0, y0 = (Lx-bx)/2, (Ly-by)/2
tb, tp = K4["blech_mm"], P["A_pad_mm"]["wert"]; nz_z = 6
def linien(a, b, h):
    n = max(1, int(math.ceil((b-a)/h))); return list(np.linspace(a, b, n+1))
def netz():
    import gmsh
    h = K4["h_probe_mm"] if probe else K4["h_plan_mm"]
    xs = sorted(set(linien(0, x0, 1e9)[:-1]+linien(x0, x0+bx, h)+linien(x0+bx, Lx, 1e9)))
    lane = Ly/8; yl = set([0, Ly, y0, y0+by])
    for i in range(8): yl |= set(linien(i*lane, (i+1)*lane, h))
    ys = sorted(yl); ys = [y for k, y in enumerate(ys) if k == 0 or y-ys[k-1] > 1e-6]
    zs = [0, tb, tb+tp]+[tb+tp+(k+1)*cb/nz_z for k in range(nz_z)]+[tb+tp+cb+tp, tb+tp+cb+tp+tb]; zdicke = [zs[i+1]-zs[i] for i in range(len(zs)-1)]
    # strukturiertes Hexaedernetz direkt als gmsh-msh 2.2 schreiben (gmsh-geo war zu langsam bei > 1000 Zellen)
    zc = np.concatenate([[0], np.cumsum(zdicke)]); nx, ny, nzz = len(xs), len(ys), len(zc)
    nid = lambda i, j, k: 1+i+nx*(j+ny*k)
    L = ["$MeshFormat", "2.2 0 8", "$EndMeshFormat", "$Nodes", str(nx*ny*nzz)]
    for k in range(nzz):
        for j in range(ny):
            for i in range(nx): L.append(f"{nid(i,j,k)} {xs[i]:.6f} {ys[j]:.6f} {zc[k]:.6f}")
    L.append("$EndNodes"); el = []
    for k in range(len(zdicke)):
        tag = 1 if k in (0, len(zdicke)-1) else 2 if k in (1, len(zdicke)-2) else None
        for j in range(ny-1):
            for i in range(nx-1):
                t = tag or (3 if (xs[i] >= x0-1e-6 and xs[i+1] <= x0+bx+1e-6 and ys[j] >= y0-1e-6 and ys[j+1] <= y0+by+1e-6) else 4)
                el.append((5, t, [nid(i,j,k), nid(i+1,j,k), nid(i+1,j+1,k), nid(i,j+1,k), nid(i,j,k+1), nid(i+1,j,k+1), nid(i+1,j+1,k+1), nid(i,j+1,k+1)]))
    for k, off in ((0, 100), (nzz-1, 110)):
        for j in range(ny-1):
            ln = min(7, int(((ys[j]+ys[j+1])/2)//lane))
            for i in range(nx-1): el.append((3, off+ln, [nid(i,j,k), nid(i+1,j,k), nid(i+1,j+1,k), nid(i,j+1,k)] if k == 0 else [nid(i,j,k), nid(i,j+1,k), nid(i+1,j+1,k), nid(i+1,j,k)]))
    L += ["$Elements", str(len(el))]
    for n, (typ, t, nd_) in enumerate(el): L.append(f"{n+1} {typ} 2 {t} {t} " + " ".join(map(str, nd_)))
    L.append("$EndElements")
    nd = f"{D}/netz"; os.makedirs(nd, exist_ok=True); open(f"{nd}/netz.msh", "w").write("\n".join(L)+"\n")
    info = dict(n_knoten=nx*ny*nzz, n_hex=sum(1 for e in el if e[0] == 5), plan_mm=[Lx, Ly], block_mm=[bx, by, cb], block_start_mm=[x0, y0], lagen_z_mm=zdicke, xs=nx-1, ys=ny-1)
    subprocess.run(["ElmerGrid", "14", "2", "netz.msh", "-autoclean"], cwd=nd, check=True, capture_output=True)
    json.dump(info, open(f"{D}/netzinfo.json", "w"), indent=1); print(info)
def stoffe():
    m = K4["stoffe"]; z = json.load(open(f"{R}/sim/kuehlung/k0_zelle/eingaben.json"))
    if VF == "LFP":
        kk = z["waermeleitung_W_mK"]["LFP_gemessen_W18"]; kin1, kin2, kq = kk["in_ebene"][0], kk["in_ebene"][1], kk["quer"]; kschaum = m["k_schaum_W_mK"]
        kx = (cd+P["A_zellabstand_LFP_mm"]["wert"])/(cd/kq+P["A_zellabstand_LFP_mm"]["wert"]/kschaum)   # in Stapelrichtung (Dicke): Reihe Zelle/Schaum
        return dict(kx=kx, ky=kin1, kz=kin2)
    sys.path.insert(0, f"{R}/sim/kuehlung/k0_zelle"); import rechnen as RC
    ka, kt, kr = RC.kern_k("NMC", "mischung"); N = P["A_zellzahl_NMC"]["wert"]; Dz = zl["durchmesser_mm"]["wert"]
    phi = N*math.pi*(Dz/2)**2/(Lx*Ly)                  # Flaechenanteil der Zellen im Block
    return dict(kx=phi*kr+(1-phi)*K4["stoffe"]["k_zwischenraum_NMC"], ky=phi*kr+(1-phi)*K4["stoffe"]["k_zwischenraum_NMC"], kz=phi*ka+(1-phi)*K4["stoffe"]["k_zwischenraum_NMC"], phi=phi)
def sif(segment=0):
    ks = stoffe(); info = json.load(open(f"{D}/netzinfo.json")); sys.path.insert(0, f"{R}/sim/kuehlung/k0_zelle"); import rechnen as RC
    z0 = json.load(open(f"{R}/sim/kuehlung/k0_zelle/eingaben.json")); m_kg = z0["waermekapazitaet"]["masse_g"][VF][0]*1e-3; cp = z0["waermekapazitaet"][f"{VF}_J_kgK"][0]
    ncell = P[f"A_zellzahl_{VF}"]["wert"]
    if DAUER:
        Ah, R0, Rb = RC.waermequelle(VF, 1); Qz = (1.0*Ah)**2*R0*1e-3                     # 1C: I = Ah, Q = I^2 R0 (K0/K1-Methode)
    else:
        K1 = json.load(open(f"{R}/sim/kuehlung/k1_schnellladen/ergebnis.json"))["faelle"][K2FALL]; Qz = K1["E_quelle_exakt_J"]/K4["dauer_s"][VF]   # W je Zelle
    Vz = (cl*cb*pitch if VF == "LFP" else bx*by*cb/ncell)*1e-9; rho = m_kg/Vz; q = Qz/m_kg                      # W/kg, Dichte so, dass rho*q = Q/V
    sys.path.insert(0, f"{R}/sim/kuehlung/k2_kuehlplatte"); import kuehlplatte as KP
    k2 = [f for f in json.load(open(f"{R}/sim/kuehlung/k2_kuehlplatte/ergebnis_k2b.json"))["faelle"] if f["fall"] == K2FALL and f["fuehrung"] == "laengs" and f["n_bahnen"] == 8 and f["breite_mm"] == 8][0]
    Vp = k2["V_pack_L_min"]/2/6e4*V_FLOW; rk = KP.kanal(0.008, Lx/1000, Vp/(k2["m_teilkanaele"]*KGRP), 0.004); kal = 237; mm_ = math.sqrt(2*rk["h"]/(kal*0.003)); eta = math.tanh(mm_*0.004)/(mm_*0.004)
    h_kanal = rk["h"]; h_eff = h_kanal*(8+2*eta*4)/(8+3); dT = Qz*ncell/2/(KP.rho*KP.c*Vp); Tin = K4["T_ein_C"]; Lm = Lx/1000; S = 8*Lm; lane = Ly/8   # tx(0) in Metern (Coordinate Scaling 0.001)
    s = []
    nstep = 3 if probe else (1 if DAUER else int(K4["dauer_s"][VF]/K4["dt_s"])); seg = nstep if not probe else 3
    s.append(f'Header\n  Mesh DB "{D}/netz" "netz"\n  Results Directory "{D}"\nEnd\n')
    s.append(f'Simulation\n  Coordinate System = Cartesian 3D\n  Coordinate Scaling = 0.001\n  Simulation Type = {"Steady State" if DAUER else "Transient"}\n  Timestepping Method = BDF\n  BDF Order = 2\n  Timestep Intervals = {(seg if not DAUER else 1)}\n  Timestep Sizes = {K4["dt_s"]}\n  Output Intervals = 1\n  Steady State Max Iterations = 1\n  Output File = "restart_{segment}.dat"\n  Post File = "k4_{segment}.vtu"\n  Initialize Dirichlet Conditions = Logical True\n' + (f'  Restart File = "restart.dat"\n  Restart Position = 0\n' if segment > 0 else '') + 'End\n')
    s.append("Constants\n  Stefan Boltzmann = 5.67e-8\nEnd\nEquation 1\n  Active Solvers(3) = 1 2 3\nEnd\n")
    s.append('Solver 1\n  Equation = Heat Equation\n  Procedure = "HeatSolve" "HeatSolver"\n  Variable = Temperature\n  Exec Solver = Always\n  Linear System Solver = Iterative\n  Linear System Iterative Method = BiCGStab\n  Linear System Preconditioning = ILU1\n  Linear System Max Iterations = 3000\n  Linear System Convergence Tolerance = 1e-9\n  Nonlinear System Max Iterations = 1\nEnd\n')
    s.append(f'Solver 2\n  Equation = ResultOutput\n  Procedure = "ResultOutputSolve" "ResultOutputSolver"\n  Exec Solver = After Simulation\n  Output File Name = k4_{segment}\n  Vtu Format = Logical True\n  Save Geometry Ids = Logical True\nEnd\n')
    s.append(f'Solver 3\n  Equation = SaveScalars\n  Procedure = "SaveData" "SaveScalars"\n  Filename = scalars_{segment}.dat\n  Exec Solver = After Timestep\n  Variable 1 = Temperature\n  Operator 1 = max\n  Variable 2 = Temperature\n  Operator 2 = min\nEnd\n')
    mat = lambda n, r, c, k: f'Material {n[0]}\n  Name = "{n[1]}"\n  Density = {r}\n  Heat Capacity = {c}\n  Heat Conductivity{k}\nEnd\n'
    st_ = K4["stoffe"]
    s.append(mat((1, "Blech"), st_["rho_Al"], st_["cp_Al"], f' = {st_["k_Al"]}')); s.append(mat((2, "Pad"), st_["rho_pad"], st_["cp_pad"], f' = {st_["k_pad"]}'))
    s.append(mat((3, "Zellblock"), rho, cp, f'(3,3) = Real {ks["kx"]} 0 0  0 {ks["ky"]} 0  0 0 {ks["kz"]}')); s.append(mat((4, "Luft"), 1.0, 1e-6, " = 0.026"))
    for b in (1, 2, 3, 4): s.append(f"Body {b}\n  Target Bodies(1) = {b}\n  Material = {b}\n  Equation = 1\n  Initial Condition = 1\n" + (f"  Body Force = 1\n" if b == 3 else "") + "End\n")
    s.append(f"Initial Condition 1\n  Temperature = {Tin}\nEnd\nBody Force 1\n  Heat Source = {q}\nEnd\n")
    for ln in range(8):
        Tf = (f"{Tin}+{dT}*({ln}*{Lm}+tx(0))/{S}" if ln % 2 == 0 else f"{Tin}+{dT}*({ln+1}*{Lm}-tx(0))/{S}")
        if PARALLEL:   # V4 (verallgemeinert, k Gruppen): T linear ueber den Gruppenweg Sg = (8/k) Bahnen, alle Gruppen gleich, Bahnwechsel wie V0 innerhalb der Gruppe
            nb = 8//KGRP; l = ln % nb; Sg = nb*Lm
            Tf = (f"{Tin}+{dT}*({l}*{Lm}+tx(0))/{Sg}" if l % 2 == 0 else f"{Tin}+{dT}*({l+1}*{Lm}-tx(0))/{Sg}")
            Tf_top = (f"{Tin}+{dT}*({Sg}-({l}*{Lm}+tx(0)))/{Sg}" if l % 2 == 0 else f"{Tin}+{dT}*({Sg}-({l+1}*{Lm}-tx(0)))/{Sg}") if V_GEGEN else Tf   # V4p: ohne Gegenlauf (Korrektur Sonnet 2026-11-23: V_GEGEN wurde im Parallelzweig nicht abgefragt)
        else: Tf_top = (f"{Tin}+{dT}*({S}-({ln}*{Lm}+tx(0)))/{S}" if ln % 2 == 0 else f"{Tin}+{dT}*({S}-({ln+1}*{Lm}-tx(0)))/{S}") if V_GEGEN else Tf   # V1: obere Platte gegensinnig durchstroemt (s -> S - s)
        for bnd, tag in ((1, 1+ln), (2, 9+ln)):   # ElmerGrid nummeriert die Rand-Gruppen 100..107 -> 1..8, 110..117 -> 9..16 neu
            s.append(f'Boundary Condition {bnd+2*ln}\n  Target Boundaries(1) = {tag}\n  Heat Transfer Coefficient = {h_eff}\n  External Temperature = Variable Coordinate 1\n    Real MATC "{Tf if bnd == 1 else Tf_top}"\nEnd\n')
    open(f"{D}/k4_{segment}.sif", "w").write("\n".join(s))
    return dict(Q_je_Zelle_W=Qz, fall=FALL, var=VAR, h_eff_Verhaeltnis_k2b=h_eff/(k2["h_Kanal"]*(8+2*k2["eta_steg"]*4)/11), q_W_kg=q, rho_block=rho, h_kanal_fx=h_kanal, Re_kanal=rk["Re"], u_kanal_m_s=rk["u_m_s"], h_eff=h_eff, dT_fluid_K=dT, nstep=nstep, seg=seg, k=ks)
def rechnen():
    info = sif(0); seg = info["seg"]
    if PARALLEL: print("V4 Gruppe", KG, "k", KGRP, "Kanal: Re", info["Re_kanal"], "u", info["u_kanal_m_s"], "m/s, h_Kanal", info["h_kanal_fx"], "W/m2K, h_eff", info["h_eff"], "dT_Fluid", info["dT_fluid_K"], "K")
    n_seg = int(math.ceil(info["nstep"]/seg)); stop = os.environ.get("RECHNEN_STOP", "")
    fertig = len(glob.glob(f"{D}/k4_*.vtu*"))     # Segmente, die schon da sind, werden uebersprungen (restart.dat = letzter Stand)
    done = sorted(glob.glob(f"{D}/segment_*.fertig")); k0 = len(done)
    for k in range(k0, n_seg):
        if stop and os.path.exists(stop): print("STOP, Segment", k); sys.exit(75)
        sif(k)
        r = subprocess.run(["ElmerSolver", f"k4_{k}.sif"], cwd=D, capture_output=True, text=True); open(f"{D}/solver_{k}.log", "w").write(r.stdout[-6000:]+r.stderr[-2000:])
        if r.returncode: print("ElmerSolver Fehler", k); sys.exit(1)
        open(f"{D}/segment_{k}.fertig", "w").write("ok")
    print("fertig", n_seg, "Segmente")
def auswerten():
    import meshio
    f = sorted(glob.glob(f"{D}/k4_*_t*.vtu"))[-1]; m = meshio.read(f); T = m.point_data["temperature"].ravel(); X = m.points
    zmin, zmax = X[:, 2].min(), X[:, 2].max(); bz = json.load(open(f"{D}/netzinfo.json"))
    out = dict(datei=f, T_max_C=float(T.max()), T_min_C=float(T.min()), x_Tmax_mm=float(X[T.argmax(), 0]*1000), y_Tmax_mm=float(X[T.argmax(), 1]*1000))
    zb = (X[:, 2]*1000 > sum(bz["lagen_z_mm"][:3])+0.1) & (X[:, 2]*1000 < sum(bz["lagen_z_mm"][:-2])-0.1)
    out["T_max_Zellblock_C"] = float(T[zb].max()); out["dT_Zellblock_K"] = float(T[zb].max()-T[zb].min())
    json.dump(out, open(f"{D}/ergebnis.json", "w"), indent=1); print(out)
if __name__ == "__main__": {"netz": netz, "sif": lambda: print(sif(0)), "rechnen": rechnen, "auswerten": auswerten}[sys.argv[1]]()
