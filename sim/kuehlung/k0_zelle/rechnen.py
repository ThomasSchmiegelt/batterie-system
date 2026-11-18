#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. Auftrag K0.
Faelle definieren, Elmer-Eingabe (.sif) schreiben, ElmerSolver starten. Zahlen nur aus eingaben.json und den Parameterdateien.
Aufruf: python3 rechnen.py <fallname> [...]   |  python3 rechnen.py alle   |  --liste"""
import json, os, re, sys, math, subprocess, time
import geometrie as G
HIER = G.HIER; R = G.R
E = json.load(open(f"{HIER}/eingaben.json"))
W = E["waermeleitung_W_mK"]; ST = W["schichtmischung"]["stoff"]

def mischung(v, band="nenn"):
    """Schichtmischung (Annahme Opus, eingaben.json): parallel (Ebene/axial/tangential), seriell (quer/radial). Volumengewichtet."""
    d, w = G.lade(v)
    st = {k: x[0] for k, x in ST.items()}
    if band in ("tief", "hoch"):
        i = 0 if band == "tief" else 1
        for k in ("lfp_kathode", "nmc_kathode", "graphit_anode", "separator_nass"): st[k] = ST[k][1][i]
    kat = st["lfp_kathode"] if v == "LFP" else st["nmc_kathode"]
    def schicht(bt, k_kollektor, k_besch, kollektor_key="folie_um"):
        L, b = w(bt, "laenge_mm"), w(bt, "breite_mm"); n = w(bt, "anzahl")
        return [(L * b * n * w(bt, kollektor_key) * 1e-3, k_kollektor), (L * b * n * 2 * w(bt, "beschichtung_um") * 1e-3, k_besch)]
    teile = schicht("BT-111", st["al"], kat) + schicht("BT-112", st["cu"], st["graphit_anode"])
    L, b = w("BT-113", "laenge_mm"), w("BT-113", "breite_mm")
    teile.append((L * b * w("BT-113", "lagen") * w("BT-113", "dicke_um") * 1e-3, st["separator_nass"]))
    Vs = sum(t[0] for t in teile)
    par = sum(t[0] * t[1] for t in teile) / Vs
    ser = Vs / sum(t[0] / t[1] for t in teile)
    return par, ser

def kern_k(v, lam):
    """liefert (k_in1,k_in2,k_quer) fuer LFP bzw. (k_axial,k_tangential,k_radial) fuer NMC"""
    if lam == "W18":
        a = W["LFP_gemessen_W18"]; return (a["in_ebene"][0], a["in_ebene"][1], a["quer"])
    band = {"mischung": "nenn", "tief": "tief", "hoch": "hoch"}[lam]
    p, s = mischung(v, band)
    return (p, p, s)

def waermequelle(v, C):
    d, w = G.lade(v); Ah = w("BT-100", "kapazitaet_Ah")
    Ri = E["innenwiderstand_mOhm"]
    if v == "LFP":
        k = [x for x in Ri if x.startswith("Blade_")][0]; Ah0 = float(re.search(r"(\d+)Ah", k).group(1))
        R0 = Ri[k]["wert"] * Ah0 / Ah; Rband = [b * Ah0 / Ah for b in Ri[k]["band"]]
    else:
        R0 = Ri["NMC_4680"]["wert"]; Rband = Ri["NMC_4680"]["band"]
    return Ah, R0, Rband

def fall(name, v, kuehl, last, lam, R_mOhm=None, h=None, spalt=False, f=1):
    return dict(name=name, v=v, kuehl=kuehl, last=last, lam=lam, R=R_mOhm, h=h, spalt=spalt, f=f)

def faelle():
    F = {}
    def add(c): F[c["name"]] = c
    # Hauptfaelle (Leitfaehigkeit: LFP W18, NMC Schichtmischung)
    for last in ("L1", "L2"):
        add(fall(f"LFP_K1_{last}", "LFP", "K1", last, "W18"))
        add(fall(f"LFP_K1_{last}_mischung", "LFP", "K1", last, "mischung"))
        add(fall(f"NMC_K1_{last}", "NMC", "K1", last, "mischung"))
        add(fall(f"NMC_K2_{last}", "NMC", "K2", last, "mischung"))
    # Netzstudie (L1, Feinheit 2)
    for n, v, k, lam in (("LFP_K1", "LFP", "K1", "W18"), ("NMC_K1", "NMC", "K1", "mischung"), ("NMC_K2", "NMC", "K2", "mischung")):
        add(fall(f"{n}_L1_f2", v, k, "L1", lam, f=2))
    # Empfindlichkeit L1 (einzeln)
    Ri = E["innenwiderstand_mOhm"]; hb = E["kuehlung"]["K1"]["h_W_m2K"][1]
    for v, lam_b in (("LFP", ["mischung"]), ("NMC", ["tief", "hoch"])):
        Ah, R0, Rb = waermequelle(v, 1)
        lam0 = "W18" if v == "LFP" else "mischung"
        add(fall(f"{v}_K1_L1_Rtief", v, "K1", "L1", lam0, R_mOhm=Rb[0]))
        add(fall(f"{v}_K1_L1_Rhoch", v, "K1", "L1", lam0, R_mOhm=Rb[1]))
        add(fall(f"{v}_K1_L1_htief", v, "K1", "L1", lam0, h=hb[0]))
        add(fall(f"{v}_K1_L1_hhoch", v, "K1", "L1", lam0, h=hb[1]))
        for b in lam_b: add(fall(f"{v}_K1_L1_lam_{b}", v, "K1", "L1", b))
    add(fall("NMC_K1_L1_spalt", "NMC", "K1", "L1", "mischung", spalt=True))
    add(fall("NMC_K1_L2_spalt", "NMC", "K1", "L2", "mischung", spalt=True))
    return F

def ids_aus_names(ordner):
    txt = open(f"{ordner}/netz/mesh.names").read()
    bod, rnd = {}, {}; cur = None
    for z in txt.splitlines():
        if "bodies" in z: cur = bod
        elif "boundaries" in z: cur = rnd
        m = re.match(r"\$ (\S+) = (\d+)", z)
        if m: cur[m.group(1)] = int(m.group(2))
    return bod, rnd

def schreibe(c):
    v = c["v"]; Ah, R0, Rb = waermequelle(v, 1)
    Rm = (c["R"] if c["R"] is not None else R0) * 1e-3
    zeit = E["lastfaelle"]["L2"]
    if c["last"] == "L1": C = 1.0; trans = False
    else:
        C = (80 - 10) / 100.0 / (1200.0 / 3600.0); trans = True      # 10->80 % in 1200 s (Startsatz, eingaben.json)
    I = C * Ah; Pel = I * I * Rm
    spalt_name = v + ("_spalt" if c["spalt"] else "")
    nd = f"{HIER}/elmer/netz_{spalt_name}_f{c['f']}"
    if not os.path.exists(f"{nd}/netzinfo.json"): G.netz(v, c["f"], c["spalt"], name=spalt_name)
    info = json.load(open(f"{nd}/netzinfo.json"))
    bod, rnd = ids_aus_names(nd)
    Vk = info["V_kern_mm3"] * 1e-9
    q = Pel / Vk                                    # W/m3
    m_kg = E["waermekapazitaet"]["masse_g"][v][0] * 1e-3
    cp = E["waermekapazitaet"][f"{v}_J_kgK"][0]
    rho = m_kg / Vk                                  # gesamte Zellmasse im Kern (Vereinfachung)
    kg = E["waermeleitung_W_mK"]["gehaeuse"]["al" if v == "LFP" else "stahl"]
    kl = 0.026                                       # Luft, Annahme laut Auftrag
    kk = kern_k(v, c["lam"])
    kuehl = E["kuehlung"]["K1"]; h = c["h"] if c["h"] is not None else kuehl["h_W_m2K"][0]; Tk = kuehl["T_kuehl_C"]
    fn = f"{HIER}/elmer/fall_{c['name']}"; os.makedirs(fn, exist_ok=True)
    s = []
    s.append("Header\n  CHECK KEYWORDS Warn\n  Mesh DB \"%s\" \"netz\"\n  Results Directory \"%s\"\nEnd\n" % (nd, fn))
    sim = "  Coordinate System = Cartesian 3D\n  Coordinate Mapping(3) = 1 2 3\n  Coordinate Scaling = 0.001\n  Simulation Type = %s\n" % ("Transient" if trans else "Steady State")
    if trans: sim += "  Timestepping Method = BDF\n  BDF Order = 2\n  Timestep Intervals = 120\n  Timestep Sizes = 10.0\n  Output Intervals = 1\n"
    else: sim += "  Steady State Max Iterations = 1\n  Output Intervals = 1\n"
    sim += "End\n"
    s.append("Simulation\n" + sim)
    s.append("Constants\n  Stefan Boltzmann = 5.67e-8\nEnd\n")
    s.append("Equation 1\n  Active Solvers(3) = 1 2 3\nEnd\n")
    ls = ("  Linear System Solver = Iterative\n  Linear System Iterative Method = BiCGStab\n  Linear System Preconditioning = ILU2\n  Linear System Max Iterations = 2000\n  Linear System Convergence Tolerance = 1.0e-12\n  Linear System Abort Not Converged = True\n" if (trans or c["f"] >= 2)
          else "  Linear System Solver = Direct\n  Linear System Direct Method = Umfpack\n")
    s.append("Solver 1\n  Equation = Heat Equation\n  Procedure = \"HeatSolve\" \"HeatSolver\"\n  Variable = Temperature\n  Calculate Loads = Logical True\n  Exec Solver = Always\n" + ls +
             "  Nonlinear System Max Iterations = 1\n  Steady State Convergence Tolerance = 1.0e-8\nEnd\n")
    s.append("Solver 2\n  Equation = SaveScalars\n  Procedure = \"SaveData\" \"SaveScalars\"\n  Filename = scalars.dat\n  File Append = %s\n  Exec Solver = After Timestep\n"
             "  Variable 1 = Temperature\n  Operator 1 = max\n  Variable 2 = Temperature\n  Operator 2 = min\n"
             "  Variable 3 = Temperature Loads\n  Operator 3 = boundary sum\n  Variable 4 = Temperature\n  Operator 4 = boundary mean\n  Variable 5 = Temperature\n  Operator 5 = int mean\nEnd\n" % ("Logical True" if trans else "Logical False"))
    s.append("Solver 3\n  Equation = ResultOutput\n  Procedure = \"ResultOutputSolve\" \"ResultOutputSolver\"\n  Exec Solver = After Timestep\n  Exec Intervals = %d\n  Output File Name = case\n  Vtu Format = Logical True\n  Binary Output = Logical True\n  Single Precision = Logical True\n  Save Geometry Ids = Logical True\n  Output Directory = \"%s\"\nEnd\n" % (1, fn))
    # Materialien: eine je Kern-Koerper (NMC je Sektor gedreht), Gehaeuse, Luft
    cap = lambda r, cc: "  Density = %.8g\n  Heat Capacity = %.8g\n" % (r, cc)
    nul = lambda: "  Density = 1.0\n  Heat Capacity = 1.0e-6\n"
    mats = []; bodies = []
    def mat(txt): mats.append(txt); return len(mats)
    mg = mat("  Name = \"Gehaeuse\"\n" + nul() + "  Heat Conductivity = %.8g\n" % kg)
    ml = mat("  Name = \"Luft\"\n" + nul() + "  Heat Conductivity = %.8g\n" % kl)
    bodies.append((bod["Gehaeuse"], mg, 0)); bodies.append((bod["Luft"], ml, 0))
    if v == "LFP":
        mk = mat("  Name = \"Kern\"\n" + cap(rho, cp) + "  Heat Conductivity(3,3) = Real %.8g 0 0  0 %.8g 0  0 0 %.8g\n" % (kk[0], kk[1], kk[2]))
        bodies.append((bod["Kern"], mk, 1)); orient = "x=Laenge %.4g, y=Hoehe(Boden y=0) %.4g, z=Dicke %.4g" % tuple(kk)
    else:
        ka, kt, kr = kk; N = info["sektoren"]
        for sct in range(N):
            ph = 2 * math.pi * (sct + 0.5) / N; cc, ss = math.cos(ph), math.sin(ph)
            kxx = kt + (kr - kt) * cc * cc; kyy = kt + (kr - kt) * ss * ss; kxy = (kr - kt) * cc * ss
            mk = mat("  Name = \"Kern_S%d\"\n" % sct + cap(rho, cp) + "  Heat Conductivity(3,3) = Real %.8g %.8g 0  %.8g %.8g 0  0 0 %.8g\n" % (kxx, kxy, kxy, kyy, ka))
            bodies.append((bod[f"Kern_Sektor_{sct}"], mk, 1))
        orient = "axial %.4g, tangential %.4g, radial %.4g" % (ka, kt, kr)
    for i, mt in enumerate(mats, 1): s.append("Material %d\n%s\nEnd\n" % (i, mt.rstrip()) if False else "Material %d\n%sEnd\n" % (i, mt))
    s.append("Body Force 1\n  Heat Source = %.10g\nEnd\n" % (q / rho))
    s.append("Initial Condition 1\n  Temperature = %.8g\nEnd\n" % Tk if trans else "Initial Condition 1\n  Temperature = %.8g\nEnd\n" % Tk)
    for i, (b, m, bf) in enumerate(bodies, 1):
        s.append("Body %d\n  Target Bodies(1) = %d\n  Equation = 1\n  Material = %d\n  Initial Condition = 1\n%sEnd\n" % (i, b, m, "  Body Force = 1\n" if bf else ""))
    gk = "Boden" if c["kuehl"] == "K1" else "Mantel_Kuehlband"
    s.append("Boundary Condition 1\n  Name = \"Kuehlrand\"\n  Target Boundaries(1) = %d\n  Heat Transfer Coefficient = %.8g\n  External Temperature = %.8g\n  Save Scalars = Logical True\nEnd\n" % (rnd[gk], h, Tk))
    open(f"{fn}/case.sif", "w").write("\n".join(s))
    meta = dict(c, C_rate=C, I_A=I, R_mOhm=Rm * 1e3, P_W=Pel, q_W_m3=q, V_kern_m3=Vk, rho_kern=rho, cp=cp, h=h, T_kuehl=Tk, k_kern=kk, orient=orient,
                k_gehaeuse=kg, k_luft=kl, kuehlrand=gk, A_kuehlrand_mm2=info["A_boden_mm2"] if c["kuehl"] == "K1" else info["A_kuehlband_mm2"], transient=trans, netz=nd, n_knoten=info["n_knoten"])
    json.dump(meta, open(f"{fn}/meta.json", "w"), indent=1)
    return fn, meta

def lauf(name):
    c = faelle()[name]; fn, meta = schreibe(c)
    t = time.time()
    for fz in ("scalars.dat", "scalars.dat.names"):
        if os.path.exists(f"{fn}/{fz}"): os.remove(f"{fn}/{fz}")
    for fz in os.listdir(fn):
        if fz.endswith(".vtu") or fz.endswith(".pvtu"): os.remove(f"{fn}/{fz}")
    p = subprocess.run(["ElmerSolver", "case.sif"], cwd=fn, capture_output=True, text=True)
    open(f"{fn}/solver.log", "w").write(p.stdout + p.stderr)
    meta["laufzeit_s"] = round(time.time() - t, 1); meta["returncode"] = p.returncode
    json.dump(meta, open(f"{fn}/meta.json", "w"), indent=1)
    print(name, "rc", p.returncode, meta["laufzeit_s"], "s")

if __name__ == "__main__":
    a = sys.argv[1:]
    F = faelle()
    if a == ["--liste"]: print("\n".join(F)); sys.exit()
    if a == ["alle"]: a = list(F)
    for n in a: lauf(n)
