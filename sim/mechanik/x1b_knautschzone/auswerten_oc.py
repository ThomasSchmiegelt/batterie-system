#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-18), Entwurf. Auftrag X1b/X2-OC. Aufruf: auswerten_oc.py [Fall ...]  (Standard: alle Ordner lauf_oc/*)
Liest lauf_oc/<Fall>/{X2T01 (TH), X2A*.gz (Animation), modell.json, X2_0000.rad}, schreibt ergebnis_oc.json, kraft_eindringung_oc.png, energiebilanz_oc.png, verformung_oc_<Fall>.png.
Einheiten mm, ms, kg (kN, J). Eindringung = Pfahlweg ab erster Knotenberuehrung (Pfahlflaeche trifft die Mittelflaeche der Aussenwand nach 1,5 mm)."""
import sys, json, csv, gzip, subprocess, os, shutil, re
from pathlib import Path
import numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
D = Path(__file__).parent; OC = "/home/cae/cae_projekte/werkzeuge/opencourant"; EX = OC + "/OpenCourant/exec"
E_ZIEL = 5000.0; F_ZIEL = 100.0; GAPS = {"1": "Zellverbinder (LFP)", "4": "Zellkoerper (LFP)"}; KONTAKT_MM = 1.5
EV = json.load(open(D / "energieverlust.json"))["ergebnis"]
def th(d):
    tmp = d / "_th"; tmp.mkdir(exist_ok=True); rows = []; h = None; tl = -1.0
    for f in sorted(d.glob("X2T0*")):   # ein TH-File je Abschnitt (Restart), Zeiten laufen weiter
        shutil.copy(f, tmp / f.name); subprocess.run([EX + "/th_to_csv_linux64_gf", f.name], cwd=tmp, capture_output=True)
        r = list(csv.reader(open(tmp / (f.name + ".csv")))); h = h or r[0]
        for row in r[1:]:
            v = [float(x) for x in row]
            if v[0] > tl + 1e-9: rows.append(v); tl = v[0]
    return h, np.array(rows)
def vtk(d, gz):
    tmp = d / "_th"; tmp.mkdir(exist_ok=True); raw = tmp / gz.stem
    with gzip.open(gz, "rb") as f, open(raw, "wb") as o: o.write(f.read())
    out = subprocess.run([EX + "/anim_to_vtk_linux64_gf", raw.name], cwd=tmp, capture_output=True, text=True).stdout
    L = out.split("\n"); t = float(L[6]); idx = {}
    for k, x in enumerate(L):
        for key in ("POINTS", "VECTORS Displacement", "SCALARS NODE_ID", "CELLS", "SCALARS PART_ID"):
            if key not in idx and x.startswith(key): idx[key] = k
        if "2DELEM_Plastic_Strain" in x and "pe" not in idx: idx["pe"] = k
    n = int(L[idx["POINTS"]].split()[1]); i = idx["POINTS"]
    P = np.array([L[i + 1 + k].split() for k in range(n)], dtype=float); j = idx["VECTORS Displacement"]; U = np.array([L[j + 1 + k].split() for k in range(n)], dtype=float)
    ids = np.array([int(L[idx["SCALARS NODE_ID"] + 2 + k]) for k in range(n)]); c = idx["CELLS"]; nc = int(L[c].split()[1]); C = [[int(v) for v in L[c + 1 + k].split()[1:]] for k in range(nc)]
    pe = np.array([float(L[idx["pe"] + 2 + k]) for k in range(nc)]); pid = np.array([int(L[idx["SCALARS PART_ID"] + 2 + k]) for k in range(nc)])
    return t, P, U, ids, C, pe, pid
def fall(name):
    d = D / "lauf_oc" / name; M = json.load(open(d / "modell.json")); h, a = th(d); t = a[:, 0]
    IE, KE, HG, CE, PW, TOT = a[:, 1], a[:, 2], a[:, 12], a[:, 11], a[:, 16], a[:, 23]
    imp = a[:, 25]; dy_p = a[:, 37]; dy_i = a[:, 31]
    k = 20; Fy = -np.gradient(np.convolve(imp, np.ones(k) / k, mode="same"), t); Fy[:k] = 0; Fy[-k:] = Fy[-k - 1]
    pen = np.maximum(dy_p - KONTAKT_MM, 0.0)
    ipk = int(np.argmax(dy_p)); bei = {}
    for g in GAPS:
        idx = next((i for i, v in enumerate(dy_i) if v >= float(g)), None)
        bei[g] = None if idx is None else {"zeit_ms": float(t[idx]), "eindringung_mm": float(pen[idx]), "energie_J": float(IE[idx]), "kraft_kN": float(Fy[idx])}
    # Animation: max Innenwand-Verschiebung ueber alle Knoten, PEEQ
    inn = set(int(x) for x in re.findall(r"\d+", re.search(r"/GRNOD/NODE/9\n[^\n]*\n(.*?)(?=\n/|\Z)", (d / "X2_0000.rad").read_text(), re.S).group(1)))
    fr = []; sel = None; yi = 30.0 - M["ym"]
    for gz in sorted(d.glob("X2A*.gz")):
        try: tt, P, U, ids, C, pe, pid = vtk(d, gz)
        except Exception as e: continue
        if sel is None:   # Messknoten aus den unverformten Koordinaten: Innenwand/Rahmenaussenwand/Profilaussenwand in Pfahlmitte, Innenwand 150 mm daneben
            P0 = P - U; hm = M["h"] / 2
            def nn(x, y): return int(np.argmin((P0[:, 0] - x) ** 2 + (P0[:, 1] - y) ** 2 + (P0[:, 2] - hm) ** 2))
            sel = {"in": nn(M["xp"], yi), "out": nn(M["xp"], M["ym"]), "prof": nn(M["xp"], M["yo"]), "in150": nn(M["xp"] - 150, yi)}
        m = np.array([i in inn for i in ids]); fr.append({"t": tt, "u_in": float(U[sel["in"], 1]), "u_out": float(U[sel["out"], 1]), "u_prof": float(U[sel["prof"], 1]), "u_in150": float(U[sel["in150"], 1]), "uy_innen_max": float(U[m, 1].max()), "peeq_max_knaut": float(pe[pid == 1].max()) if (pid == 1).any() else 0.0, "peeq_max_rahmen": float(pe[pid == 2].max()) if (pid == 2).any() else 0.0, "_": (P, U, ids, C, pe, pid)})
    zer = {}
    if fr:
        ft = np.array([f["t"] for f in fr]); ui = np.array([f["u_in"] for f in fr])
        for g in GAPS:
            ix = next((i for i, v in enumerate(ui) if v >= float(g)), None)
            if ix is None: continue
            i0 = max(ix - 1, 0); wt = 0 if ix == 0 else (float(g) - ui[i0]) / (ui[ix] - ui[i0]); tg = ft[i0] + wt * (ft[ix] - ft[i0]); ip = lambda key: float(np.interp(tg, ft, [f[key] for f in fr]))
            p = float(np.interp(tg, t, pen)); uo = ip("u_out"); up_ = ip("u_prof")
            zer[g] = {"zeit_ms": float(tg), "eindringung_mm": p, "energie_J": float(np.interp(tg, t, IE)), "innenwand_mitte_mm": float(g), "innenwand_150mm_daneben_mm": ip("u_in150"),
                      "rahmen_aussenwand_mm": uo, "profil_stauchung_mm": up_ - uo, "rahmen_kammern_stauchung_mm": uo - float(g), "profil_aussenwand_verschiebung_mm": up_}
    kfr = int(np.argmin([abs(f["t"] - t[ipk]) for f in fr])) if fr else None
    Fmax = float(Fy.max()); Fmit = float(np.interp(M["w"], pen[:ipk + 1], IE[:ipk + 1]) / M["w"]) if pen[ipk] >= M["w"] else None
    ccx = None
    try:
        R = json.load(open(D / "ergebnis.json"))["laeufe"].get(f"{M['var']}_w{int(M['w'])}")
        if R:
            f_oc = float(np.interp(2.0, pen[:ipk + 1], Fy[:ipk + 1])); f_cx = float(np.interp(2.0, R["kurve"]["s_mm"], R["kurve"]["F_kN"])); ccx = {"F_oc_kN_bei_2mm": f_oc, "F_ccx_kN_bei_2mm": f_cx, "abw_proz": (f_oc - f_cx) / f_cx * 100}
    except Exception: pass
    res = {"fall": name, "w": M["w"], "var": M["var"], "v0_m_s": M["v0_mm_ms"], "energie_start_J": float(TOT[0]), "energie_total_ende_J": float(TOT[-1]), "energiefehler_proz_max": float(np.abs(TOT - TOT[0]).max() / TOT[0] * 100),
           "hourglass_max_J": float(HG.max()), "hourglass_max_proz_IE": float((HG / np.maximum(IE, 1)).max() * 100), "kontaktenergie_max_J": float(CE.max()), "zeitschritt_min_ms": float(a[:, 7].min()), "zyklen": None,
           "eindringung_max_mm": float(pen[ipk]), "zeit_max_ms": float(t[ipk]), "energie_intern_bei_max_J": float(IE[ipk]), "kraft_max_kN": Fmax, "kraft_mittel_bis_w_kN": Fmit, "innenwand_dy_max_mm_TH": float(dy_i.max()),
           "innenwand_dy_max_mm_Anim": max((f["uy_innen_max"] for f in fr), default=None), "peeq_max_knaut": max((f["peeq_max_knaut"] for f in fr), default=None), "peeq_max_rahmen": max((f["peeq_max_rahmen"] for f in fr), default=None),
           "zellberuehrung": bei, "zerlegung_bei_zellberuehrung": zer, "ccx_gegenpruefung": ccx, "energieverlust_proz": EV[M["var"]][str(int(M["w"]))]["Energieverlust_proz"] if str(int(M["w"])) in EV[M["var"]] else None,
           "kurve": {"t": t[::5].round(4).tolist(), "pen": pen[::5].round(3).tolist(), "F": Fy[::5].round(2).tolist(), "IE": IE[::5].round(1).tolist(), "KE": KE[::5].round(1).tolist(), "dy_innen": dy_i[::5].round(3).tolist(), "PW": PW[::5].round(1).tolist(), "TOT": TOT[::5].round(2).tolist()}}
    lg = sorted(d.glob("engine_*.log"), key=lambda p: int(re.findall(r"\d+", p.stem)[0]))
    if lg:
        tx = lg[-1].read_text(); m_ = re.search(r"TOTAL NUMBER OF CYCLES\s*:\s*(\d+)", tx); res["zyklen"] = sum(int(re.search(r"TOTAL NUMBER OF CYCLES\s*:\s*(\d+)", p.read_text()).group(1)) for p in lg if re.search(r"TOTAL NUMBER OF CYCLES\s*:\s*(\d+)", p.read_text())); res["normal_ende"] = all("NORMAL TERMINATION" in p.read_text() for p in lg); res["abschnitte"] = len(lg)
        el = 0.0
        for p in lg:
            e = re.findall(r"ELAPSED TIME=\s*([\d.]+) s", p.read_text()); el += float(e[-1]) if e else 0.0
        res["laufzeit_s_summe"] = el
    return res, fr, kfr, M, (a, h)
def bild_verformung(name, fr, kfr, M, res):
    if kfr is None: return
    t, (P, U, ids, C, pe, pid) = fr[kfr]["t"], fr[kfr]["_"]; X = P; xp = M["xp"]; w = M["w"]
    cen = np.array([X[c].mean(axis=0) for c in C]); hmid = M["h"] / 2
    fig, axs = plt.subplots(2, 1, figsize=(11, 8), gridspec_kw={"height_ratios": [1, 1.1]}, layout="constrained")
    vmax = max(10, pe.max() * 100)
    m1 = np.abs(cen[:, 2] - hmid) < 12; m2 = cen[:, 1] > 22
    sc = axs[0].scatter(cen[m1, 0], cen[m1, 1], c=pe[m1] * 100, s=9, cmap="viridis", vmin=0, vmax=vmax); axs[0].set_aspect("equal"); axs[0].set_xlim(xp - 160, xp + 160)
    axs[1].scatter(cen[m2, 0], cen[m2, 2], c=pe[m2] * 100, s=9, cmap="viridis", vmin=0, vmax=vmax); axs[1].set_aspect("equal"); axs[1].set_xlim(xp - 160, xp + 160)
    yc_t = M["yc"] + res["eindringung_max_mm"] + KONTAKT_MM; th_ = np.linspace(-1.2, 1.2, 200)
    axs[0].plot(xp + M["Rp"] * np.sin(th_), yc_t + M["Rp"] * np.cos(th_), color="k", lw=1.5, label="Pfahl Ø254 (Lage bei maximaler Eindringung)"); axs[0].legend(fontsize=8, loc="lower right")
    axs[0].set_ylim(-w - 6, 60); axs[0].axhline(30, color="r", ls=":", lw=1); axs[0].text(xp - 155, 38, "rote Linie: Rahmeninnenseite Soll y = 30 mm (Zelle dahinter), Ziel: Wand bleibt links davon", color="r", fontsize=8)
    axs[0].axhline(0, color="orange", ls=":", lw=1); axs[0].text(xp - 155, 3, "orange: Rahmenaußenseite y = 0, davor die Knautschzone", color="darkorange", fontsize=8)
    axs[0].set_title(f"{name}: Draufsicht (x/y), Schnittband in halber Höhe, bei maximaler Eindringung t = {t:.1f} ms, Eindringung {res['eindringung_max_mm']:.1f} mm, Elementmitten verformt (1:1)", fontsize=9)
    axs[1].set_title("Seitenansicht (x/z) der Elemente mit y > 22 mm, also Innenwand des Rahmens: Dehnung dort (Zelle dahinter)", fontsize=9); axs[0].set_xlabel("x (mm)"); axs[0].set_ylabel("y (mm)"); axs[1].set_xlabel("x (mm)"); axs[1].set_ylabel("z (mm)")
    cb = fig.colorbar(sc, ax=axs, pad=0.02, shrink=0.8); cb.set_label("plastische Dehnung PEEQ (%); Bruchdehnung 10 % (rot)"); cb.ax.axhline(10, color="r", lw=2)
    fig.savefig(D / f"verformung_oc_{name}.png", dpi=110); plt.close(fig)
if __name__ == "__main__":
    namen = sys.argv[1:] or sorted(p.name for p in (D / "lauf_oc").iterdir() if (p / "X2T01").exists())
    R = {"hinweis": "KI-generiert, Entwurf. Aus lauf_oc/<Fall>/X2T01 und X2A*.gz (OpenCourant). Kraft = negative Ableitung des Wandimpulses (TH-Variable der Pfahlwand), geglaettet 1 ms."}; alle = {}
    for n in namen:
        try: res, fr, kfr, M, _ = fall(n)
        except Exception as e: print("Fehler", n, repr(e)); continue
        R[n] = res; alle[n] = res; bild_verformung(n, fr, kfr, M, res)
    json.dump(R, open(D / "ergebnis_oc.json", "w"), indent=1, ensure_ascii=False)
    if alle:
        col = {15: "#1f77b4", 20: "#2ca02c", 30: "#d62728"}; ls = {"LFP": "-", "NMC": "--"}
        fig, ax = plt.subplots(3, 1, figsize=(10, 12), sharex=True)
        for n, r in alle.items():
            c = r["kurve"]; kw = dict(color=col.get(int(r["w"]), "k"), ls=ls[r["var"]], lw=2, label=n)
            ax[0].plot(c["pen"], c["F"], **kw); ax[1].plot(c["pen"], np.array(c["IE"]) / 1e3, **kw); ax[2].plot(c["pen"], c["dy_innen"], **kw)
            for g, mk in (("1", "o"), ("4", "s")):
                b = r["zellberuehrung"].get(g)
                if b: ax[0].plot(b["eindringung_mm"], b["kraft_kN"], mk, color=kw["color"], mfc="none", ms=9); ax[1].plot(b["eindringung_mm"], b["energie_J"] / 1e3, mk, color=kw["color"], mfc="none", ms=9)
        ax[0].axhspan(F_ZIEL, max(160, ax[0].get_ylim()[1]), color="green", alpha=0.12, label="Zielband: Kraft ab 100 kN (Restkraft, Annahme)"); ax[0].set_ylabel("Pfahlkraft (kN)")
        ax[1].axhspan(E_ZIEL / 1e3, 5.5, color="green", alpha=0.12, label="Zielband: 5 kJ aufgenommen (Annahme, Restenergie)"); ax[1].axhline(E_ZIEL / 1e3, color="k", ls=":"); ax[1].set_ylabel("innere Energie (kJ)")
        ax[2].axhspan(0, 1, color="green", alpha=0.12, label="Zielband: Innenwand bleibt unter 1 mm (Spalt Zellverbinder LFP)"); ax[2].axhline(1, color="k", ls=":"); ax[2].axhline(4, color="k", ls="--"); ax[2].text(0.5, 4.1, "4 mm Spalt Zellkörper (LFP)", fontsize=8); ax[2].set_ylabel("Verschiebung Innenwand Mitte (mm)"); ax[2].set_xlabel("Eindringung des Pfahls ab Berührung (mm)")
        ax[0].set_title("X1b/X2 explizit (OpenCourant): Pfahl 1500 kg, 5 kJ, Ø254; Kreis = Spalt 1 mm, Quadrat = 4 mm erreicht"); [(a.legend(fontsize=8, loc="upper left"), a.grid(alpha=0.3)) for a in ax]
        fig.tight_layout(); fig.savefig(D / "kraft_eindringung_oc.png", dpi=130); plt.close(fig)
        fig, ax = plt.subplots(1, 2, figsize=(13, 5.5))
        for var, mk in (("LFP", "o"), ("NMC", "^")):
            rs = sorted([r for r in alle.values() if r["var"] == var], key=lambda r: r["w"])
            for g, ls_ in (("1", "--"), ("4", "-")):
                pts = [(r["w"], r["zerlegung_bei_zellberuehrung"].get(g, {}).get("energie_J")) for r in rs if r["zerlegung_bei_zellberuehrung"].get(g)]
                if pts: ax[0].plot([p[0] for p in pts], [p[1] / 1e3 for p in pts], ls_, marker=mk, lw=2, label=f"{var}, Spalt {g} mm erreicht")
        ax[0].axhspan(5.0, 5.5, color="green", alpha=0.15, label="Zielband: Zellberührung erst ab 5 kJ"); ax[0].axhline(5.0, color="k", ls=":"); ax[0].set_xlabel("Breite der Knautschzone w (mm)"); ax[0].set_ylabel("Energie bis Zellberührung (kJ)")
        ax[0].set_title("Energie bis Zellberührung über w"); ax[0].legend(fontsize=8); ax[0].grid(alpha=0.3); ax[0].set_ylim(0, 5.6)
        ws = sorted(alle.values(), key=lambda r: (r["var"], r["w"])); xs = np.arange(len(ws)); bot = np.zeros(len(ws))
        for key, lab in (("profil_stauchung_mm", "Profil gestaucht"), ("rahmen_kammern_stauchung_mm", "Rahmenkammern gestaucht"), ("innenwand_mitte_mm", "Innenwand nach innen (Rahmen insgesamt verschoben, Biegung)")):
            v = np.array([r["zerlegung_bei_zellberuehrung"].get("4", {}).get(key, 0.0) for r in ws]); ax[1].bar(xs, v, bottom=bot, label=lab); bot += v
        ax[1].set_xticks(xs); ax[1].set_xticklabels([f"{r['var']} w{int(r['w'])}" for r in ws]); ax[1].set_ylabel("Weg der Profil-Außenwand bis Spalt 4 mm erreicht (mm)"); ax[1].set_title("Woher kommt der Pfahlweg bis zur Zellberührung (Spalt 4 mm)?"); ax[1].legend(fontsize=8); ax[1].grid(alpha=0.3, axis="y")
        fig.tight_layout(); fig.savefig(D / "energie_bis_zellberuehrung_ueber_w.png", dpi=130); plt.close(fig)
        fig, ax = plt.subplots(figsize=(10, 5.5))
        for n, r in alle.items():
            c = r["kurve"]; ax.plot(c["t"], np.array(c["IE"]) / 1e3, label=f"{n} innere Energie", lw=2); ax.plot(c["t"], np.array(c["KE"]) / 1e3, "--", lw=1.5, label=f"{n} kinetische Energie"); ax.plot(c["t"], np.array(c["TOT"]) / 1e3, ":", color="k")
        ax.axhspan(4.75, 5.25, color="green", alpha=0.12, label="Zielband: Summe 5 kJ ± 5 %"); ax.set_xlabel("Zeit (ms)"); ax.set_ylabel("Energie (kJ)"); ax.set_title("Energiebilanz (Summe = gepunktet); Hourglass-Energie siehe ergebnis_oc.json"); ax.legend(fontsize=8); ax.grid(alpha=0.3)
        fig.tight_layout(); fig.savefig(D / "energiebilanz_oc.png", dpi=130); plt.close(fig)
    print(json.dumps({n: {k: v for k, v in r.items() if k != "kurve"} for n, r in alle.items()}, indent=1, ensure_ascii=False)[:5000])
