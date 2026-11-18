#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. Auftrag K1.
Liest elmer/fall_*/ (meta.json, verlauf.json, scalars.dat, letzte VTU) -> ergebnis.json. Keine Deutung. Bilder/Berichte: k1_bilder.py, k1_bericht.py."""
import json, os, glob, sys
import numpy as np, meshio
HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import k1_rechnen as RC
E = RC.E; ZT = E["basis"]["ziele"]["T_max_C"][0]; ZD = E["basis"]["ziele"]["dT_zelle_K"][0]
HEX_TET = [(0, 1, 3, 4), (1, 2, 3, 6), (1, 4, 5, 6), (3, 4, 6, 7), (1, 3, 4, 6)]

def hexvol(P, hexc):
    v = 0
    for t in HEX_TET:
        a, b, c, d = (P[hexc[:, i]] for i in t)
        v = v + np.abs(np.einsum("ij,ij->i", np.cross(b - a, c - a), d - a)) / 6.0
    return v

def zeit_ueber(t, y, schwelle):
    """Zeit (s), in der die linear interpolierte Kurve y(t) > schwelle liegt"""
    s = 0.0
    for i in range(len(t) - 1):
        a, b = y[i] - schwelle, y[i + 1] - schwelle; dt = t[i + 1] - t[i]
        if a > 0 and b > 0: s += dt
        elif a > 0 >= b: s += dt * a / (a - b)
        elif b > 0 >= a: s += dt * b / (b - a)
    return s

def auswerten():
    erg = {}
    for name, c in RC.faelle().items():
        fn = f"{HIER}/elmer/fall_{name}"
        if not os.path.exists(f"{fn}/verlauf.json"): continue
        meta = json.load(open(f"{fn}/meta.json")); vz = json.load(open(f"{fn}/verlauf.json"))
        t = np.array([0.0] + vz["t_s"]); Tm = np.array([meta["T_start"]] + vz["T_max_C"]); dT = np.array([0.0] + vz["dT_kern_K"])
        Kx = np.array([meta["T_start"]] + vz["T_kern_max_C"])
        r = dict(meta={k: meta[k] for k in ("v", "profil", "kuehl", "h", "raender", "T_start", "T_kuehl", "R_mOhm", "dt_s", "n_schritte", "laufzeit_s", "laufzeit_gesamt_s", "n_knoten", "A_kuehlrand_mm2", "returncode")})
        r["meta"]["stufen"] = meta["stufen"]; r["tabscheibe"] = meta.get("tabscheibe")
        r["T_max_Spitze_C"] = float(Tm.max()); r["t_T_max_Spitze_s"] = float(t[Tm.argmax()])
        r["dT_Spitze_K"] = float(dT.max()); r["t_dT_Spitze_s"] = float(t[dT.argmax()])
        r["T_max_Ende_C"] = float(Tm[-1]); r["dT_Ende_K"] = float(dT[-1])
        r["dT_mittel_K"] = float(np.trapezoid(dT, t) / t[-1])
        r["t_ueber_45C_s"] = zeit_ueber(t, Tm, ZT); r["t_ueber_5K_s"] = zeit_ueber(t, dT, ZD)
        r["ladezeit_s"] = meta["T_end_s"]
        r["E_quelle_tab_J"] = meta["E_quelle_tab_J"]; r["E_quelle_exakt_J"] = meta["E_quelle_exakt_J"]
        # Energiebilanz (wie K0): Kuehlrand-Integral + gespeichert = Quelle
        sc = np.atleast_2d(np.loadtxt(f"{fn}/scalars.dat")); tt = meta["dt_s"] * np.arange(1, len(sc) + 1)
        Qt = np.concatenate([[0.0], -sc[:, 2]]); E_out = float(np.trapezoid(Qt, np.concatenate([[0.0], tt])))
        m = meshio.read(sorted(glob.glob(f"{fn}/case_t*.vtu"))[-1]); T = np.asarray(m.point_data["temperature"], dtype=float).ravel()
        idx = [i for i, cc in enumerate(m.cells) if cc.type == "hexahedron"][0]; hexc = m.cells[idx].data; ids = np.asarray(m.cell_data["GeometryIds"][idx])
        kern = list(range(3, 4 if meta["v"] == "LFP" else 3 + 48)); hv = hexvol(m.points, hexc); Tc = T[hexc].mean(1); km = np.isin(ids, kern)
        E_sp = float(meta["rho_kern"] * meta["cp"] * np.sum(hv[km] * (Tc[km] - meta["T_kuehl"])))
        r["E_kuehlrand_J"] = E_out; r["E_gespeichert_J"] = E_sp; r["bilanz_abw_prozent"] = 100 * (E_out + E_sp - meta["E_quelle_tab_J"]) / meta["E_quelle_tab_J"]
        r["T_max_ende_vtu_C"] = float(T.max())
        r["t_s"] = t.tolist(); r["T_max_t_C"] = Tm.tolist(); r["dT_kern_t_K"] = dT.tolist()
        erg[name] = r
    # Waermeintegral relativ zu P0 derselben Variante, gegen Tabelle ERWARTUNG
    for name, r in erg.items():
        v, p = r["meta"]["v"], r["meta"]["profil"]
        if p in E["profile"] and f"{v}_P0" in erg:
            rel = r["E_quelle_tab_J"] / erg[f"{v}_P0"]["E_quelle_tab_J"]; soll = E["profile"][p]["waerme_rel_erwartet"]
            r["waerme_rel_P0"] = rel; r["waerme_rel_tabelle"] = soll; r["waerme_abw_prozent"] = 100 * (rel - soll) / soll
    # Soll-Kontrolle gegen die aus Stufen berechnete Energie (exakt vs. Schrittsumme)
    for r in erg.values(): r["E_tab_vs_exakt_prozent"] = 100 * (r["E_quelle_tab_J"] - r["E_quelle_exakt_J"]) / r["E_quelle_exakt_J"]
    k0 = json.load(open(f"{HIER}/../k0_zelle/ergebnis.json"))["faelle"]
    abgleich = {}
    for v in ("LFP", "NMC"):
        a, b = erg[f"{v}_P0"], k0[f"{v}_K1_L2"]
        abgleich[v] = dict(T_max_K1=a["T_max_Ende_C"], T_max_K0=b["T_max_C"], dT_K1=a["dT_Ende_K"], dT_K0=b["dT_kern_K"],
                           abw_T_K=a["T_max_Ende_C"] - b["T_max_C"], abw_dT_K=a["dT_Ende_K"] - b["dT_kern_K"], quelle_K0="sim/kuehlung/k0_zelle/ergebnis.json faelle." + f"{v}_K1_L2")
    out = dict(hinweis="KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. Erzeugt von k1_auswertung.py aus elmer/fall_*. dT = Kern max - min (wie K0 dT_kern). T_max = Maximum im ganzen Modell.",
               ziel_T_max_C=ZT, ziel_dT_K=ZD, abgleich_P0_K0=abgleich, faelle=erg)
    json.dump(out, open(f"{HIER}/ergebnis.json", "w"), indent=1)
    return out

if __name__ == "__main__":
    o = auswerten(); print(len(o["faelle"]), "Faelle"); print(json.dumps(o["abgleich_P0_K0"], indent=1))
