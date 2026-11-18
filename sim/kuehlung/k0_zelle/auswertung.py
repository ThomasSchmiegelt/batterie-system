#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. Auftrag K0.
Liest elmer/fall_*/ (scalars.dat, case_t*.vtu, meta.json) -> ergebnis.json und Bilder. Keine Deutung."""
import json, os, glob, re, math
import numpy as np, meshio
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.tri import Triangulation
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import rechnen as RC
HIER = RC.HIER
ZIEL_T = RC.E["ziele"]["T_max_C"][0]; ZIEL_DT = RC.E["ziele"]["dT_zelle_K"][0]
F = RC.faelle()
HEX_TET = [(0, 1, 3, 4), (1, 2, 3, 6), (1, 4, 5, 6), (3, 4, 6, 7), (1, 3, 4, 6)]
HEX_FACES = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]

def lies(name, vtu=None):
    fn = f"{HIER}/elmer/fall_{name}"
    meta = json.load(open(f"{fn}/meta.json"))
    sc = np.atleast_2d(np.loadtxt(f"{fn}/scalars.dat"))
    vt = sorted(glob.glob(f"{fn}/case_t*.vtu"))
    return fn, meta, sc, vt

def KERN_IDS(meta):
    n = 4 if meta["v"] == "LFP" else 3 + 48
    return set(range(3, n))

def kernknoten(meta, m):
    # GeometryIds = Index der Body-Sektion in case.sif; rechnen.py schreibt zuerst Gehaeuse (1), Luft (2), dann die Kern-Koerper (>= 3)
    kern = KERN_IDS(meta)
    gi = m.cell_data["GeometryIds"]
    idx = [i for i, c in enumerate(m.cells) if c.type == "hexahedron"][0]
    hexc = m.cells[idx].data; ids = np.asarray(gi[idx])
    kc = hexc[np.isin(ids, list(kern))]
    return hexc, ids, np.unique(kc), kc

def hexvol(P, hexc):
    v = 0
    for t in HEX_TET:
        a, b, c, d = (P[hexc[:, i]] for i in t)
        v = v + np.abs(np.einsum("ij,ij->i", np.cross(b - a, c - a), d - a)) / 6.0
    return v

def feldwerte(meta, vtufile):
    m = meshio.read(vtufile); T = np.asarray(m.point_data["temperature"], dtype=float).ravel()
    hexc, ids, kn, kc = kernknoten(meta, m)
    return dict(T_max=float(T.max()), T_min=float(T.min()), T_kern_max=float(T[kn].max()), T_kern_min=float(T[kn].min()), m=m, T=T, hexc=hexc, ids=ids, kc=kc)

def auswerten():
    erg = {}
    for name in F:
        if not os.path.exists(f"{HIER}/elmer/fall_{name}/scalars.dat"): continue
        fn, meta, sc, vt = lies(name)
        fw = feldwerte(meta, vt[-1])
        P = meta["P_W"]; r = dict(meta={k: meta[k] for k in ("v", "kuehl", "last", "lam", "C_rate", "I_A", "R_mOhm", "P_W", "h", "k_kern", "orient", "kuehlrand", "A_kuehlrand_mm2", "n_knoten", "laufzeit_s", "spalt", "f")})
        r["T_max_C"] = fw["T_max"]; r["T_min_C"] = fw["T_min"]; r["dT_gesamt_K"] = fw["T_max"] - fw["T_min"]
        r["T_kern_max_C"] = fw["T_kern_max"]; r["T_kern_min_C"] = fw["T_kern_min"]; r["dT_kern_K"] = fw["T_kern_max"] - fw["T_kern_min"]
        Qaus = -sc[-1, 2]; r["Q_quelle_W"] = P; r["Q_kuehlrand_W"] = float(Qaus)
        if not meta["transient"]:
            r["bilanz_abw_prozent"] = 100 * (Qaus - P) / P
        else:
            t = 10.0 * np.arange(1, len(sc) + 1); r["n_zeitschritte"] = int(len(sc))
            r["t_s"] = [0.0] + t.tolist(); r["T_max_t_C"] = [meta["T_kuehl"]] + sc[:, 0].tolist()
            Qt = np.concatenate([[0.0], -sc[:, 2]]); E_out = float(np.trapezoid(Qt, np.concatenate([[0.0], t])))
            # gespeicherte Energie: rho*cp*Integral (T-T0) dV ueber alle Zellen (Dichte nur im Kern, laut Modell)
            m = fw["m"]; Pn = m.points; hv = hexvol(Pn, fw["hexc"]); Tc = fw["T"][fw["hexc"]].mean(1)
            kern_mask = np.isin(fw["ids"], list(KERN_IDS(meta)))
            E_sp = float(meta["rho_kern"] * meta["cp"] * np.sum(hv[kern_mask] * (Tc[kern_mask] - meta["T_kuehl"])))
            Ez = float(P * t[-1]); r["E_quelle_J"] = Ez; r["E_kuehlrand_J"] = E_out; r["E_gespeichert_J"] = E_sp
            r["bilanz_transient_abw_prozent"] = 100 * (E_out + E_sp - Ez) / Ez
            # dT_kern(t) aus den VTU (jeder 4. Schritt)
            ts, dts, tm = [], [], []
            for f_ in vt[3::4]:
                k = int(re.search(r"_t(\d+)\.vtu", f_).group(1)); w = feldwerte(meta, f_)
                ts.append(k * 10.0); dts.append(w["T_kern_max"] - w["T_kern_min"]); tm.append(w["T_kern_max"])
            r["dTkern_t_s"] = ts; r["dTkern_t_K"] = dts
            r["t_Tmax45_s"] = next((tt for tt, T in zip(r["t_s"], r["T_max_t_C"]) if T >= ZIEL_T), None)
            r["t_dT5_s"] = next((tt for tt, d in zip(ts, dts) if d >= ZIEL_DT), None)
        # Symmetriepruefung K1-NMC (Achsensymmetrie): Streuung der Randtemperatur am Mantel auf halber Hoehe
        if meta["v"] == "NMC" and meta["kuehl"] == "K1":
            Pn = fw["m"].points; rr = np.hypot(Pn[:, 0], Pn[:, 1]); z0_ = Pn[np.argmin(abs(Pn[:, 2] - 0.04)), 2]; sel = (rr > 0.0229) & (abs(Pn[:, 2] - z0_) < 1e-9)
            Tsel = fw["T"][sel]; r["achsensymmetrie_streuung_K"] = float(Tsel.max() - Tsel.min())
        erg[name] = r
    return erg

def netzstudie(erg):
    out = {}
    for n in ("LFP_K1", "NMC_K1", "NMC_K2"):
        a, b = erg.get(f"{n}_L1"), erg.get(f"{n}_L1_f2")
        if a and b: out[n] = dict(T_max_f1=a["T_max_C"], T_max_f2=b["T_max_C"], diff_K=b["T_max_C"] - a["T_max_C"], dT_f1=a["dT_kern_K"], dT_f2=b["dT_kern_K"],
                                  knoten_f1=a["meta"]["n_knoten"], knoten_f2=b["meta"]["n_knoten"])
    return out

# ---------------- Bilder -----------------
def hlp(ax, txt): ax.text(0.01, 0.99, txt, transform=ax.transAxes, va="top", fontsize=7, color="0.25")

def bild_schnitt(name, erg, vmax):
    fn, meta, sc, vt = lies(name); fw = feldwerte(meta, vt[-1]); P = fw["m"].points * 1e3; T = fw["T"]
    v = meta["v"]; fig, axs = plt.subplots(1, 2, figsize=(14, 4.6) if v == "LFP" else (11, 5.2), gridspec_kw={"width_ratios": [4, 1.3] if v == "LFP" else [1, 1]})
    lev = np.linspace(25, vmax, 60)
    if v == "LFP":
        zmid = P[:, 2].max() / 2; s = np.abs(P[:, 2] - zmid) < 1e-6
        tri = Triangulation(P[s, 0], P[s, 1]); c = axs[0].tricontourf(tri, T[s], levels=lev, cmap="inferno", extend="both")
        axs[0].set_xlabel("Länge x (mm)"); axs[0].set_ylabel("Höhe y (mm)  [Boden = Kühlplatte bei y = 0]"); axs[0].set_aspect("equal"); axs[0].set_title("Schnitt Mitte Dicke (Draufsicht auf die Zellplatte)", fontsize=9)
        xm = P[:, 0].max() / 2; s2 = np.abs(P[:, 0] - xm) < 1.0
        tri2 = Triangulation(P[s2, 2], P[s2, 1]); axs[1].tricontourf(tri2, T[s2], levels=lev, cmap="inferno", extend="both")
        axs[1].set_xlabel("Dicke z (mm)"); axs[1].set_title("Querschnitt Mitte Länge", fontsize=9); axs[1].set_aspect("equal")
        cs = [axs[0], axs[1]]; tris = [(tri, T[s]), (tri2, T[s2])]
    else:
        s = np.abs(P[:, 1]) < 1e-6
        tri = Triangulation(P[s, 0], P[s, 2]); c = axs[0].tricontourf(tri, T[s], levels=lev, cmap="inferno", extend="both")
        axs[0].set_xlabel("x (mm)"); axs[0].set_ylabel("Zellachse z (mm)  [Boden bei z = 0]"); axs[0].set_aspect("equal"); axs[0].set_title("Längsschnitt durch die Zellachse", fontsize=9)
        zmid = P[np.argmin(abs(P[:, 2] - 40.0)), 2]; s2 = np.abs(P[:, 2] - zmid) < 1e-6
        tri2 = Triangulation(P[s2, 0], P[s2, 1]); axs[1].tricontourf(tri2, T[s2], levels=lev, cmap="inferno", extend="both")
        axs[1].set_xlabel("x (mm)"); axs[1].set_ylabel("y (mm)"); axs[1].set_aspect("equal"); axs[1].set_title("Querschnitt halbe Höhe (z = %.0f mm)" % zmid + (" (Kühlband: Viertel rechts oben)" if meta["kuehl"] == "K2" else ""), fontsize=9)
        tris = [(tri, T[s]), (tri2, T[s2])]; cs = axs
    for a, (tr, Tv) in zip(cs, tris):
        if Tv.max() >= ZIEL_T: a.tricontour(tr, Tv, levels=[ZIEL_T], colors="cyan", linewidths=1.6)
    cb = fig.colorbar(c, ax=list(axs), shrink=0.85, label="Temperatur (°C)"); cb.ax.axhline(ZIEL_T, color="cyan", lw=2)
    r = erg[name]
    fig.suptitle(f"{name.replace('_', ' ')}: T_max {r['T_max_C']:.1f} °C, T_min {r['T_min_C']:.1f} °C, ΔT Kern {r['dT_kern_K']:.1f} K "
                 f"(Vorgabe REQ-P09: T ≤ {ZIEL_T:g} °C, ΔT ≤ {ZIEL_DT:g} K)", fontsize=10)
    fig.text(0.5, 0.005, "KI-generiert, Entwurf. Quelle: sim/kuehlung/k0_zelle/ergebnis.json. Türkise Linie = 45-°C-Vorgabe (REQ-P09) (nur wenn im Bild erreicht).", ha="center", fontsize=7, color="0.3")
    fig.savefig(f"{HIER}/temperatur_{name}.png", dpi=130, bbox_inches="tight"); plt.close(fig)

def bild_3d(name, erg, vmax):
    fn, meta, sc, vt = lies(name); fw = feldwerte(meta, vt[-1]); P = fw["m"].points * 1e3; T = fw["T"]; hexc = fw["hexc"]
    v = meta["v"]; c = P[hexc].mean(1)
    keep = c[:, 2] <= P[:, 2].max() / 2 if v == "LFP" else c[:, 1] <= 0.0   # Schnitt: LFP halbe Dicke, NMC halber Zylinder
    hk = hexc[keep]; fl = {}
    for h in hk:
        for f in HEX_FACES:
            q = tuple(h[list(f)]); fl.setdefault(tuple(sorted(q)), []).append(q)
    faces = [v_[0] for v_ in fl.values() if len(v_) == 1]
    polys = [P[list(q)] for q in faces]; col = [T[list(q)].mean() for q in faces]
    fig = plt.figure(figsize=(9, 5.5)); ax = fig.add_subplot(111, projection="3d")
    pc = Poly3DCollection(polys, cmap="inferno", linewidths=0.0); pc.set_array(np.array(col)); pc.set_clim(25, vmax); ax.add_collection3d(pc)
    lo, hi = P.min(0), P.max(0); sp = (hi - lo)
    if v == "LFP": ax.set_box_aspect((1, 0.5, 0.35)); 
    else: ax.set_box_aspect((1, 1, 1.7))
    ax.set_xlim(lo[0], hi[0]); ax.set_ylim(lo[1], hi[1]); ax.set_zlim(lo[2], hi[2])
    ax.set_xlabel("x (mm)"); ax.set_ylabel("y (mm)"); ax.set_zlabel("z (mm)")
    ax.view_init(25, -60 if v == "LFP" else -50)
    cb = fig.colorbar(pc, ax=ax, shrink=0.65, label="Temperatur (°C)"); cb.ax.axhline(ZIEL_T, color="cyan", lw=2)
    r = erg[name]
    ax.set_title(f"{name.replace('_', ' ')}, aufgeschnitten (matplotlib; pvpython nicht installiert)\nT_max {r['T_max_C']:.1f} °C, ΔT Kern {r['dT_kern_K']:.1f} K; Vorgabe {ZIEL_T:g} °C (cyan an der Farbskala)", fontsize=9)
    fig.text(0.5, 0.01, "KI-generiert, Entwurf. Quelle: sim/kuehlung/k0_zelle/ergebnis.json", ha="center", fontsize=7, color="0.3")
    fig.savefig(f"{HIER}/temperatur3d_{name}.png", dpi=130, bbox_inches="tight"); plt.close(fig)

def bild_verlauf(erg):
    fig, ax = plt.subplots(figsize=(10, 5.2)); ax2 = ax.twinx()
    farben = {"LFP_K1_L2": "tab:blue", "NMC_K1_L2": "tab:red", "NMC_K2_L2": "tab:orange"}
    for n, cc in farben.items():
        if n not in erg: continue
        r = erg[n]; lab = n.replace("_L2", "").replace("_", " ")
        ax.plot(np.array(r["t_s"]) / 60, r["T_max_t_C"], color=cc, lw=2, label=f"T_max {lab}")
        ax2.plot(np.array([0] + r["dTkern_t_s"]) / 60, [0] + r["dTkern_t_K"], color=cc, lw=1.5, ls="--", label=f"ΔT Kern {lab}")
    ax.axhline(ZIEL_T, color="k", lw=1.5); ax.text(0.2, ZIEL_T + 0.4, f"Vorgabe T_max {ZIEL_T:g} °C (REQ-P09)", fontsize=8)
    ax2.axhline(ZIEL_DT, color="gray", lw=1.5, ls=":"); ax2.text(12, ZIEL_DT + 0.3, f"Vorgabe ΔT {ZIEL_DT:g} K (REQ-P09)", fontsize=8, color="gray")
    ax.set_xlabel("Zeit (min), Schnellladen 10→80 % in 20 min (≈ 2,1 C)"); ax.set_ylabel("T_max der Zelle (°C), durchgezogen"); ax2.set_ylabel("ΔT im Kern (K), gestrichelt")
    ax.grid(alpha=0.3); h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels(); ax.legend(h1 + h2, l1 + l2, fontsize=7, loc="lower right")
    ax.set_title("Zelltemperatur beim Schnellladen (K1 = Boden gekühlt, K2 = Mantelband), Start 25 °C", fontsize=10)
    fig.text(0.5, 0.005, "KI-generiert, Entwurf. Quelle: sim/kuehlung/k0_zelle/ergebnis.json (Kühlmitteltemperatur 25 °C und h 500 W/(m²K) sind Annahmen; Grenzen = Vorgabe REQ-P09)", ha="center", fontsize=7, color="0.3")
    fig.savefig(f"{HIER}/verlauf_L2.png", dpi=130, bbox_inches="tight"); plt.close(fig)

def tornado(erg):
    fig, axs = plt.subplots(1, 2, figsize=(13, 4.8)); tab = {}
    spec = {"LFP": [("Innenwiderstand R", "Rtief", "Rhoch"), ("Wärmeübergang h (200…1000)", "hhoch", "htief"), ("Leitfähigkeit: Schichtmischung statt W18", None, "lam_mischung")],
            "NMC": [("Innenwiderstand R", "Rtief", "Rhoch"), ("Wärmeübergang h (200…1000)", "hhoch", "htief"), ("Leitfähigkeit (Stoffbänder)", "lam_hoch", "lam_tief"), ("Bodenspalt Luft (Modellvariante)", None, "spalt")]}
    for ax, v in zip(axs, ("LFP", "NMC")):
        b = erg[f"{v}_K1_L1"]["dT_kern_K"]; ys = []
        for i, (lab, lo, hi) in enumerate(spec[v][::-1]):
            vl = erg[f"{v}_K1_L1_{lo}"]["dT_kern_K"] if lo else b; vh = erg[f"{v}_K1_L1_{hi}"]["dT_kern_K"] if hi else b
            ax.barh(i, vl - b, left=b, color="tab:green"); ax.barh(i, vh - b, left=b, color="tab:red")
            ax.text(min(vl, vh) - 0.05, i, f"{min(vl, vh):.1f}", ha="right", va="center", fontsize=8); ax.text(max(vl, vh) + 0.05, i, f"{max(vl, vh):.1f}", ha="left", va="center", fontsize=8)
            tab.setdefault(v, []).append(dict(parameter=lab, dT_tief_K=vl, dT_hoch_K=vh))
        ax.set_yticks(range(len(spec[v]))); ax.set_yticklabels([s[0] for s in spec[v][::-1]], fontsize=8)
        ax.axvline(b, color="k", lw=1); ax.axvline(ZIEL_DT, color="gray", ls=":", lw=1.5); ax.text(ZIEL_DT, -0.62, f"Vorgabe ΔT {ZIEL_DT:g} K", fontsize=8, color="gray", ha="center")
        ax.set_xlabel("ΔT im Kern bei 1 C, Boden gekühlt (K); senkrechte Linie = Hauptfall"); ax.set_title(f"{v}: Hauptfall ΔT = {b:.1f} K", fontsize=10); ax.grid(alpha=0.3, axis="x")
        ax.set_xlim(0, max(ZIEL_DT * 1.15, ax.get_xlim()[1]))
    fig.suptitle("Empfindlichkeit L1 (jeweils ein Parameter im Band, Rest wie Hauptfall); grün = kleineres, rot = größeres ΔT als Hauptfall", fontsize=10)
    fig.text(0.5, 0.005, "KI-generiert, Entwurf. Quelle: sim/kuehlung/k0_zelle/ergebnis.json. Bänder aus eingaben.json (Annahmen).", ha="center", fontsize=7, color="0.3")
    fig.savefig(f"{HIER}/empfindlichkeit_K0.png", dpi=130, bbox_inches="tight"); plt.close(fig); return tab

if __name__ == "__main__":
    erg = auswerten(); ns = netzstudie(erg)
    out = dict(hinweis="KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. Erzeugt von auswertung.py aus elmer/fall_*/. Keine Deutung.", ziel_T_max_C=ZIEL_T, ziel_dT_K=ZIEL_DT, faelle=erg, netzstudie=ns)
    haupt = [n for n in ("LFP_K1_L1", "LFP_K1_L2", "NMC_K1_L1", "NMC_K1_L2", "NMC_K2_L1", "NMC_K2_L2") if n in erg]
    vmax = float(math.ceil(max(max(erg[n]["T_max_C"] for n in haupt), ZIEL_T + 3)))
    out["farbskala_max_C"] = vmax
    for n in haupt: bild_schnitt(n, erg, vmax)
    for n in haupt:
        if n.endswith("L2"): bild_3d(n, erg, vmax)
    bild_verlauf(erg)
    out["tornado"] = tornado(erg)
    for r in out["faelle"].values():
        for k in ("t_s", "T_max_t_C"): r.pop(k, None) if False else None
    json.dump(out, open(f"{HIER}/ergebnis.json", "w"), indent=1, default=float)
    print("ok", len(erg))
