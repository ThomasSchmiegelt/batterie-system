#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. Auftrag K1 (Schnellladen).
Faelle aus eingaben.json (K1) + K0-Modell (K0-Dateien werden nur gelesen/importiert). Elmer-Eingabe schreiben, ElmerSolver starten,
danach aus den VTU T_max(t), dT_Kern(t) ziehen (verlauf.json) und die Zwischen-VTU loeschen (nur letzter Schritt bleibt).
Aufruf: python3 k1_rechnen.py <fall> [...] | --liste"""
import json, os, sys, time, subprocess, glob, re
import numpy as np, meshio
HIER = os.path.dirname(os.path.abspath(__file__)); K0 = os.path.join(os.path.dirname(HIER), "k0_zelle")
sys.path.insert(0, K0)
import rechnen as RC            # K0 (unveraendert), nur Funktionen waermequelle, kern_k, ids_aus_names, E
import geometrie as G0
sys.path.insert(0, HIER)
import k1_geometrie as G
E = json.load(open(f"{HIER}/eingaben.json")); BASIS = E["basis"]

def faelle():
    F = {}
    def add(v, p, k):
        n = f"{v}_{p}" + ("" if k == "K1h500" else f"_{k}"); F[n] = dict(name=n, v=v, profil=p, kuehl=k)
    for v in ("LFP", "NMC"):
        for p in E["faelle"]["Profile"]: add(v, p, "K1h500")
        for k in E["faelle"]["Kuehlfaelle_mit_P0"]: add(v, "P0", k)
        for p, k, vs in E["faelle"]["Kombinationen"]:
            if v in vs: add(v, p, k)
    for p, k in E["faelle"].get("K1b", []): add("NMC", p, k)
    for n, d in E.get("K1c", {}).get("faelle", {}).items(): F[n] = dict(name=n, v=d["v"], profil=d["profil"], kuehl=d["kuehl"], k1c=d)
    return F

def k1c_quelle(d):
    """K1c: Waermequelle Q(t) aus C2-CSV (Spalte Q_W, 1,5C), optional skaliert auf I*dU-Mittel. liefert (t, P_W, I_A, skal)"""
    import csv
    Q = E["K1c"]
    rows = [r for r in csv.DictReader(open(os.path.join(HIER, Q["csv"]))) if r["zelle"] == "4680" and float(r["C_start"]) == Q["C_start"]]
    t = np.array([float(r["t_s"]) for r in rows]); P = np.array([float(r["Q_W"]) for r in rows]); I = np.array([float(r["I_A"]) for r in rows])
    skal = 1.0
    if d["quelle"] == "idu":
        j = json.load(open(os.path.join(HIER, Q["json_mittel"]))); r15 = [x for x in j["N4680"] if x["C_start"] == Q["C_start"]][0]
        skal = r15["waerme_mittel_IdU_W"] / r15["waerme_mittel_gesamt_W"]
    return t, P * skal, I, skal

def profil_tabelle(p, Ah, Rm, Vk, rho):
    """liefert (T_end, dt, Punkte [(t, I_A)], stufen) ; Strom-Wert gilt auf (t_a, t_b]"""
    P = E["profile"][p]; dt = P["zeitschritt_s"]
    pts = []
    if "puls" in P:
        pu = P["puls"]; C_an = pu["dsoc_an_gesamt"] / (pu["dauer_s"] / pu["takt_s"] * pu["an_s"] / 3600.0)
        stufen = []
        n = int(pu["dauer_s"] // pu["takt_s"])
        for i in range(n):
            t0 = i * pu["takt_s"]; stufen.append((t0, t0 + pu["an_s"], C_an)); stufen.append((t0 + pu["an_s"], t0 + pu["takt_s"], 0.0))
        T_end = pu["dauer_s"]
    else:
        t = 0.0; stufen = []
        for dur, ds in P["stufen_dauer_s_dsoc"]:
            stufen.append((t, t + dur, ds / (dur / 3600.0))); t += dur
        T_end = t
    return T_end, dt, stufen

def schreibe(c):
    v = c["v"]; Ah, R0, Rb = RC.waermequelle(v, 1); k1c = c.get("k1c")
    if k1c and k1c.get("R_mOhm"): R0 = k1c["R_mOhm"]
    Rm = R0 * 1e-3
    kc = E["kuehlung"][c["kuehl"]]
    csvq = None
    if k1c and k1c.get("quelle") in ("gesamt", "idu"):
        tc, Pc, Ic, skal = k1c_quelle(k1c); csvq = (tc, Pc, Ic, skal); T_end = float(tc[-1]); n_ = int(round(T_end / 10.0)); dt = round(T_end / n_, 6)
        stufen = [(float(tc[i]), float(tc[i + 1]), 1.5, float(Ic[i]), None) for i in range(len(tc) - 1)]
    else: T_end, dt, stufen = profil_tabelle(c["profil"], Ah, Rm, None, None)
    nd = f"{HIER}/elmer/netz_{v}_f1"
    info = json.load(open(f"{nd}/netzinfo.json"))
    bod, rnd = RC.ids_aus_names(nd)
    Vk = info["V_kern_mm3"] * 1e-9
    m_kg = RC.E["waermekapazitaet"]["masse_g"][v][0] * 1e-3; cp = RC.E["waermekapazitaet"][f"{v}_J_kgK"][0]; rho = m_kg / Vk
    kg = RC.E["waermeleitung_W_mK"]["gehaeuse"]["al" if v == "LFP" else "stahl"]; kl = 0.026
    lam = "W18" if v == "LFP" else "mischung"; kk = RC.kern_k(v, lam)
    # Waermequelle-Tabelle (W/kg); Wert auf (t_a, t_b], Sprung ueber 0,01 s
    tab = []; qs = []
    if csvq:
        tc, Pc, Ic, skal = csvq; qs = [(float(tc[i]), float(tc[i + 1]), 1.5, float(Ic[i]), float(np.trapezoid(Pc[i:i + 2], tc[i:i + 2]) / (tc[i + 1] - tc[i]))) for i in range(len(tc) - 1)]
        tab = [(float(a), float(b) / (Vk * rho)) for a, b in zip(tc, Pc)]
    for (ta, tb, C) in ([] if csvq else stufen):
        I = C * Ah; q = I * I * Rm / Vk / rho; qs.append((ta, tb, C, I, q * rho * Vk))
        tab.append((ta + (0.01 if ta > 0 else 0.0), q)); tab.append((tb, q))
    n = int(round(T_end / dt))
    # Integral der Quelle wie Elmer sie auswertet (Wert bei Schrittende, implizit) und exakt
    tn = [dt * (i + 1) for i in range(n)]
    def Pat(t):
        if csvq: return float(np.interp(t, csvq[0], csvq[1]))
        for ta, tb, C, I, Pw in qs:
            if ta < t <= tb + 1e-9: return Pw
        return 0.0
    E_tab = sum(Pat(t) * dt for t in tn); E_exakt = float(np.trapezoid(csvq[1], csvq[0])) if csvq else sum((tb - ta) * Pw for ta, tb, C, I, Pw in qs)
    fn = f"{HIER}/elmer/fall_{c['name']}"; os.makedirs(fn, exist_ok=True)
    s = []
    s.append("Header\n  CHECK KEYWORDS Warn\n  Mesh DB \"%s\" \"netz\"\n  Results Directory \"%s\"\nEnd\n" % (nd, fn))
    s.append("Simulation\n  Coordinate System = Cartesian 3D\n  Coordinate Mapping(3) = 1 2 3\n  Coordinate Scaling = 0.001\n  Simulation Type = Transient\n  Timestepping Method = BDF\n  BDF Order = 2\n  Timestep Intervals = %d\n  Timestep Sizes = %.6g\n  Output Intervals = 1\nEnd\n" % (n, dt))
    s.append("Constants\n  Stefan Boltzmann = 5.67e-8\nEnd\n")
    s.append("Equation 1\n  Active Solvers(3) = 1 2 3\nEnd\n")
    ls = "  Linear System Solver = Iterative\n  Linear System Iterative Method = BiCGStab\n  Linear System Preconditioning = ILU2\n  Linear System Max Iterations = 2000\n  Linear System Convergence Tolerance = 1.0e-12\n  Linear System Abort Not Converged = True\n"
    s.append("Solver 1\n  Equation = Heat Equation\n  Procedure = \"HeatSolve\" \"HeatSolver\"\n  Variable = Temperature\n  Calculate Loads = Logical True\n  Exec Solver = Always\n" + ls + "  Nonlinear System Max Iterations = 1\n  Steady State Convergence Tolerance = 1.0e-8\nEnd\n")
    s.append("Solver 2\n  Equation = SaveScalars\n  Procedure = \"SaveData\" \"SaveScalars\"\n  Filename = scalars.dat\n  File Append = Logical True\n  Exec Solver = After Timestep\n  Variable 1 = Temperature\n  Operator 1 = max\n  Variable 2 = Temperature\n  Operator 2 = min\n  Variable 3 = Temperature Loads\n  Operator 3 = boundary sum\n  Variable 4 = Temperature\n  Operator 4 = boundary mean\n  Variable 5 = Temperature\n  Operator 5 = int mean\nEnd\n")
    s.append("Solver 3\n  Equation = ResultOutput\n  Procedure = \"ResultOutputSolve\" \"ResultOutputSolver\"\n  Exec Solver = After Timestep\n  Exec Intervals = 1\n  Output File Name = case\n  Vtu Format = Logical True\n  Binary Output = Logical True\n  Single Precision = Logical True\n  Save Geometry Ids = Logical True\n  Output Directory = \"%s\"\nEnd\n" % fn)
    cap = lambda r, cc: "  Density = %.8g\n  Heat Capacity = %.8g\n" % (r, cc)
    nul = lambda: "  Density = 1.0\n  Heat Capacity = 1.0e-6\n"
    mats = []; bodies = []
    def mat(txt): mats.append(txt); return len(mats)
    mg = mat("  Name = \"Gehaeuse\"\n" + nul() + "  Heat Conductivity = %.8g\n" % kg); ml = mat("  Name = \"Luft\"\n" + nul() + "  Heat Conductivity = %.8g\n" % kl)
    bodies.append((bod["Gehaeuse"], mg, 0)); bodies.append((bod["Luft"], ml, 0))
    import math
    if v == "LFP":
        mk = mat("  Name = \"Kern\"\n" + cap(rho, cp) + "  Heat Conductivity(3,3) = Real %.8g 0 0  0 %.8g 0  0 0 %.8g\n" % tuple(kk)); bodies.append((bod["Kern"], mk, 1))
    else:
        ka, kt, kr = kk; N = info["sektoren"]
        for sct in range(N):
            ph = 2 * math.pi * (sct + 0.5) / N; cc, ss = math.cos(ph), math.sin(ph)
            kxx = kt + (kr - kt) * cc * cc; kyy = kt + (kr - kt) * ss * ss; kxy = (kr - kt) * cc * ss
            mk = mat("  Name = \"Kern_S%d\"\n" % sct + cap(rho, cp) + "  Heat Conductivity(3,3) = Real %.8g %.8g 0  %.8g %.8g 0  0 0 %.8g\n" % (kxx, kxy, kxy, kyy, ka))
            bodies.append((bod[f"Kern_Sektor_{sct}"], mk, 1))
    tabinfo = None
    if v == "NMC":
        g = (info["H"] - info["wandstaerke_mm"]) - info["kern_z_von_bis"][1]   # mm
        if c["kuehl"] in ("K3", "K3h1000") or c["kuehl"].startswith("K3b"):
            T_ = E["nmc_tabscheibe"]; kxy = (T_["al_dicke_mm"] * T_["k_al"] + (g - T_["al_dicke_mm"]) * kl) / g
            kz = g / (T_["kontakt_dicke_mm"] / T_["k_kontakt"] + (g - T_["kontakt_dicke_mm"]) / T_["k_al"]); tabinfo = dict(g_mm=g, k_xy=kxy, k_z=kz)
            mo = mat("  Name = \"Tabscheibe\"\n" + nul() + "  Heat Conductivity(3,3) = Real %.8g 0 0  0 %.8g 0  0 0 %.8g\n" % (kxy, kxy, kz))
        else: mo = ml
        bodies.append((bod["Luft_oben"], mo, 0))
    for i, mt in enumerate(mats, 1): s.append("Material %d\n%sEnd\n" % (i, mt))
    s.append("Body Force 1\n  Heat Source = Variable Time\n    Real\n" + "".join("      %.6f %.10g\n" % (t, q) for t, q in tab) + "    End\nEnd\n")
    s.append("Initial Condition 1\n  Temperature = %.8g\nEnd\n" % kc["T_start"])
    for i, (b, m, bf) in enumerate(bodies, 1):
        s.append("Body %d\n  Target Bodies(1) = %d\n  Equation = 1\n  Material = %d\n  Initial Condition = 1\n%sEnd\n" % (i, b, m, "  Body Force = 1\n" if bf else ""))
    for j, gk in enumerate(kc["raender"], 1):
        s.append("Boundary Condition %d\n  Name = \"Kuehlrand_%s\"\n  Target Boundaries(1) = %d\n  Heat Transfer Coefficient = %.8g\n  External Temperature = %.8g\n  Save Scalars = Logical True\nEnd\n" % (j, gk, rnd[gk], kc.get("h_rand", {}).get(gk, kc["h"]), kc["T_kuehl"]))
    open(f"{fn}/case.sif", "w").write("\n".join(s))
    A = info["A_boden_mm2"] * (len(kc["raender"]))
    meta = dict(c, R_mOhm=Rm * 1e3, Ah=Ah, h=kc["h"], h_rand=kc.get("h_rand"), T_start=kc["T_start"], T_kuehl=kc["T_kuehl"], raender=kc["raender"], A_kuehlrand_mm2=A,
                stufen=[dict(t_von=a, t_bis=b, C=C, I_A=I, P_W=Pw) for a, b, C, I, Pw in qs], k1c=k1c, skal_Q=(csvq[3] if csvq else None), T_end_s=T_end, dt_s=dt, n_schritte=n,
                E_quelle_tab_J=E_tab, E_quelle_exakt_J=E_exakt, tabscheibe=tabinfo, V_kern_m3=Vk, rho_kern=rho, cp=cp, k_kern=list(kk), netz=nd, n_knoten=info["n_knoten"])
    json.dump(meta, open(f"{fn}/meta.json", "w"), indent=1)
    return fn, meta

def nachlauf(fn, meta):
    sys.path.insert(0, K0)
    vt = sorted(glob.glob(f"{fn}/case_t*.vtu"))
    m0 = meshio.read(vt[0]); gi = m0.cell_data["GeometryIds"]
    idx = [i for i, c in enumerate(m0.cells) if c.type == "hexahedron"][0]; hexc = m0.cells[idx].data; ids = np.asarray(gi[idx])
    kern = set(range(3, 4 if meta["v"] == "LFP" else 3 + 48)); kn = np.unique(hexc[np.isin(ids, list(kern))])
    t, Tm, Kx, Kn = [], [], [], []
    for f in vt:
        k = int(re.search(r"_t(\d+)\.vtu", f).group(1)); T = np.asarray(meshio.read(f).point_data["temperature"], dtype=float).ravel()
        t.append(k * meta["dt_s"]); Tm.append(float(T.max())); Kx.append(float(T[kn].max())); Kn.append(float(T[kn].min()))
    json.dump(dict(t_s=t, T_max_C=Tm, T_kern_max_C=Kx, T_kern_min_C=Kn, dT_kern_K=[a - b for a, b in zip(Kx, Kn)]), open(f"{fn}/verlauf.json", "w"))
    for f in vt[:-1]: os.remove(f)
    # Hinweis: letzter Schritt bleibt fuer Bilder/Energiebilanz

def lauf(name):
    c = faelle()[name]; fn, meta = schreibe(c)
    t = time.time()
    for fz in os.listdir(fn):
        if fz.endswith((".vtu", ".pvtu")) or fz.startswith("scalars.dat"): os.remove(f"{fn}/{fz}")
    p = subprocess.run(["ElmerSolver", "case.sif"], cwd=fn, capture_output=True, text=True)
    open(f"{fn}/solver.log", "w").write(p.stdout + p.stderr)
    meta["laufzeit_s"] = round(time.time() - t, 1); meta["returncode"] = p.returncode
    if p.returncode == 0: nachlauf(fn, meta)
    meta["laufzeit_gesamt_s"] = round(time.time() - t, 1)
    json.dump(meta, open(f"{fn}/meta.json", "w"), indent=1)
    print(name, "rc", p.returncode, meta["laufzeit_s"], "s (mit Nachlauf", meta["laufzeit_gesamt_s"], "s)", flush=True)

if __name__ == "__main__":
    a = sys.argv[1:]; F = faelle()
    if a == ["--liste"]: print("\n".join(F)); sys.exit()
    for n in a: lauf(n)
