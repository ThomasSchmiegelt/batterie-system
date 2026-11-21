#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-20), Entwurf. Auftrag X3. Aufruf: auswerten.py <Fall z.B. LFP_a> [film]
Liest lauf/<Fall>/{X3T0*, X3A*.gz, modell.json, engine_*.log}, schreibt ergebnis.json, kraft_weg_<Fall>.png, energie_<Fall>.png, verformung_<Fall>.png (+ film_<Fall>.mp4 mit 'film') und fuellt ERGEBNIS.md (Block zwischen den Marken ZAHLEN)."""
import sys, json, csv, gzip, subprocess, shutil, re
from pathlib import Path
import numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
D = Path(__file__).parent; EX = "/home/cae/cae_projekte/werkzeuge/opencourant/OpenCourant/exec"; KONTAKT = 1.25   # Pfahlflaeche trifft Mittelflaeche der Aussenwand nach t/2
ZIEL_PEN = (40, 70); ZIEL_ZELLE = (10, 40); E_FEHLER = 5.0   # ERWARTUNG.md X3 Punkte 1 und 2
def th(d):
    tmp = d / "_th"; tmp.mkdir(exist_ok=True); rows = []; tl = -1.0; h = None
    for f in sorted(d.glob("X3T0*")):
        shutil.copy(f, tmp / f.name); subprocess.run([EX + "/th_to_csv_linux64_gf", f.name], cwd=tmp, capture_output=True)
        r = list(csv.reader(open(tmp / (f.name + ".csv")))); h = r[0]
        for row in r[1:]:
            v = [float(x) for x in row]
            if v[0] > tl + 1e-9: rows.append(v); tl = v[0]
    return np.array(rows), h
def vtk(d, gz):
    tmp = d / "_th"; tmp.mkdir(exist_ok=True); raw = tmp / gz.stem
    with gzip.open(gz, "rb") as f, open(raw, "wb") as o: o.write(f.read())
    out = subprocess.run([EX + "/anim_to_vtk_linux64_gf", raw.name], cwd=tmp, capture_output=True, text=True).stdout; L = out.split("\n"); t = float(L[6]); idx = {}
    for k, x in enumerate(L):
        for key in ("POINTS", "VECTORS Displacement", "SCALARS NODE_ID"):
            if key not in idx and x.startswith(key): idx[key] = k
    n = int(L[idx["POINTS"]].split()[1]); i = idx["POINTS"]
    P = np.array([L[i + 1 + k].split() for k in range(n)], dtype=float); j = idx["VECTORS Displacement"]; U = np.array([L[j + 1 + k].split() for k in range(n)], dtype=float)
    ids = np.array([int(L[idx["SCALARS NODE_ID"] + 2 + k]) for k in range(n)]); return t, P - U, U, ids
def zahlen(name):
    d = D / "lauf" / name; M = json.load(open(d / "modell.json")); a, h = th(d); t = a[:, 0]; nm = [x.strip() for x in h]; col = lambda p: next(i for i, x in enumerate(nm) if x.startswith(p)); rw = [i for i, x in enumerate(nm) if x.startswith("rwall")][1::6]
    IE, KE, TOT, HG, CE = a[:, 1], a[:, 2], a[:, 23], a[:, 12], a[:, 11]; imp = sum(a[:, i] for i in rw); dy_i = a[:, col("innenwand_mitte") + 1]; dy_p = a[:, col("pfahlknoten") + 1]; dy_c = a[:, col("zellblock_vorderseite") + 1]; BQ = M.get("lastfall_art") == "b"
    if BQ: dy_p = M["geschw_b_mm_ms"] * t   # masselose Wand mit vorgegebener Geschwindigkeit: Wandweg = v*t (Knoten wird nicht bewegt ausgegeben)
    k = min(20, max(1, len(t) // 4)); Fy = -np.gradient(np.convolve(imp, np.ones(k) / k, mode="same"), t); Fy[:k] = 0; Fy[-k:] = Fy[-k - 1]
    pen = np.maximum(dy_p - KONTAKT, 0.0); ip = int(np.argmax(dy_p))
    M["_vpe"] = 0.0 if BQ else float((dy_p[-1] - dy_p[-6]) / (t[-1] - t[-6]))   # Pfahlgeschwindigkeit am Ende (mm/ms = m/s), Opus 2026-11-21
    f100 = None
    if BQ:
        i1 = next((i for i, v in enumerate(Fy) if v >= 100.0), None)
        if i1 is not None: f100 = {"zeit_ms": float(t[i1]), "weg_platte_mm": float(pen[i1]), "innenwand_mitte_mm": float(dy_i[i1]), "zellblock_vorderseite_mm": float(dy_c[i1]), "kraft_kN": float(Fy[i1])}
    res = {"fall": name, "lastfall": M.get("lastfall_art"), "bei_100kN": f100, "hinweis": "KI-generiert, Entwurf; Quelle lauf/<Fall>/X3T0*, X3A*.gz", "v0_m_s": M["v0_mm_ms"], "energie_start_J": float(TOT[0]), "energie_total_ende_J": float(TOT[-1]),
           "energiefehler_proz_max": (None if BQ else float(np.abs(TOT - TOT[0]).max() / TOT[0] * 100)), "hourglass_max_J": float(HG.max()), "kontaktenergie_max_J": float(CE.max()), "zeitschritt_min_ms": float(a[:, 7].min()),
           "pfahl_eindringung_max_mm": float(pen[ip]), "zeit_max_ms": float(t[ip]), "energie_intern_bei_max_J": float(IE[ip]), "kraft_max_kN": float(Fy.max()),
           "innenwand_mitte_dy_max_mm": float(dy_i.max()), "zellblock_vorderseite_dy_max_mm": float(dy_c.max()), "zellreihe_eindringung_mm_Tiefste": float(dy_c.max()), "t_ende_ms": float(t[-1]),
           "kurve": {"t": t[::5].round(4).tolist(), "pen": pen[::5].round(3).tolist(), "F": Fy[::5].round(2).tolist(), "IE": IE[::5].round(1).tolist(), "KE": KE[::5].round(1).tolist(), "TOT": TOT[::5].round(1).tolist(), "dy_zelle": dy_c[::5].round(3).tolist()}}
    lg = sorted(d.glob("engine_*.log"), key=lambda p: int(re.findall(r"\d+", p.stem)[0])); res["zyklen"] = sum(int(m.group(1)) for p in lg for m in [re.search(r"TOTAL NUMBER OF CYCLES\s*:\s*(\d+)", p.read_text())] if m)
    res["laufzeit_s_summe"] = sum(float((re.findall(r"ELAPSED TIME=\s*([\d.]+) s", p.read_text()) or [0])[-1]) for p in lg)
    return res, M, d
def bilder(res, name):
    c = res["kurve"]
    fig, ax = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    ax[0].plot(c["pen"], c["F"], lw=2, label="Pfahlkraft"); ax[0].set_ylabel("Pfahlkraft (kN)"); ax[0].axvspan(*ZIEL_PEN, color="green", alpha=0.12, label="Erwartungsband Eindringung (ERWARTUNG Nachtrag 1)"); ax[0].legend(); ax[0].grid(alpha=.3)
    ax[1].plot(c["pen"], np.array(c["dy_zelle"]), lw=2, color="C1", label="Zellblock-Vorderseite, Weg in y"); ax[1].axhspan(*ZIEL_ZELLE, color="green", alpha=0.12, label="Erwartung 10-40 mm (Zellreihe eingedrückt)"); ax[1].axhline(0, color="k", lw=.5)
    ax[1].set_ylabel("Zellblock Weg (mm)"); ax[1].set_xlabel("Pfahleindringung (mm)"); ax[1].legend(); ax[1].grid(alpha=.3); ax[0].set_title(f"X3 {name}: Pfahl 1500 kg, 5 kJ, D254 auf Mitte Längsseite. Lesehilfe: grün = Erwartung vor der Rechnung")
    fig.tight_layout(); fig.savefig(D / f"kraft_weg_{name}.png", dpi=120); plt.close(fig)
    fig, ax = plt.subplots(figsize=(10, 5.5)); ax.plot(c["t"], np.array(c["IE"]) / 1e3, label="innere Energie"); ax.plot(c["t"], np.array(c["KE"]) / 1e3, label="kinetische Energie"); ax.plot(c["t"], np.array(c["TOT"]) / 1e3, "k:", label="Summe")
    ax.axhspan(5 * (1 - E_FEHLER / 100), 5 * (1 + E_FEHLER / 100), color="green", alpha=0.15, label="Zielband: Summe 5 kJ ± 5 % (Pflicht)"); ax.set_xlabel("Zeit (ms)"); ax.set_ylabel("Energie (kJ)"); ax.legend(); ax.grid(alpha=.3); ax.set_title(f"X3 {name}: Energiebilanz")
    fig.tight_layout(); fig.savefig(D / f"energie_{name}.png", dpi=120); plt.close(fig)
def frame(M, P0, U, ids, tt, ax=None, pen=None, ziel=True):
    k_ = ids < 900000; P0, U, ids = P0[k_], U[k_], ids[k_]; cell = ids >= 400000; X = P0 + U; mag = np.linalg.norm(U, axis=1)
    fig, axs = plt.subplots(2, 1, figsize=(13, 9), gridspec_kw={"height_ratios": [1.0, 0.55]}, layout="constrained")
    bz = np.abs(P0[:, 2] - (M["z0"] + M["z1"]) / 2) < 22
    sc = axs[0].scatter(X[cell & bz, 0], X[cell & bz, 1], c=mag[cell & bz], s=2, cmap="viridis", vmin=0, vmax=60); axs[0].scatter(X[~cell & bz, 0], X[~cell & bz, 1], c=mag[~cell & bz], s=1.5, cmap="viridis", vmin=0, vmax=60, alpha=.7)
    th_ = np.linspace(-np.pi / 2 - 1.3, -np.pi / 2 + 1.3, 200); yc_t = M["yc"] + (pen or 0) + 1.25; axs[0].plot(M["xp"] + M["Rp"] * np.cos(th_ + np.pi / 2 + 0) * 0 + M["Rp"] * np.sin(np.linspace(-1.3, 1.3, 200)), yc_t + M["Rp"] * np.cos(np.linspace(-1.3, 1.3, 200)), "k", lw=1.5)
    axs[0].axhline(M["cy0"], color="r", ls=":", lw=1); axs[0].text(30, M["cy0"] + 12, "rot gepunktet: Zellblock-Vorderseite im Ausgangszustand (y = 33 mm); Ziel: Zellen bleiben rechts davon", color="r", fontsize=8)
    axs[0].set_aspect("equal"); axs[0].set_title(f"Draufsicht (x/y), Band in Packmitte (z), verformt 1:1, t = {tt:.1f} ms, Pfahlweg {pen or 0:.0f} mm; Farbe = Verschiebung (mm). Zellen und Rahmen", fontsize=9)
    bs = X[:, 1] < 200; axs[1].scatter(X[bs, 0], X[bs, 2], c=mag[bs], s=2, cmap="viridis", vmin=0, vmax=60); axs[1].set_aspect("equal"); axs[1].set_title("Seitenansicht (x/z), Knoten mit y < 200 mm (Pfahlseite)", fontsize=9)
    for a_ in axs: a_.set_xlabel("x (mm)")
    axs[0].set_ylabel("y (mm)"); axs[1].set_ylabel("z (mm)"); cb = fig.colorbar(sc, ax=axs, shrink=.8, pad=.01); cb.set_label("Verschiebung (mm)")
    return fig
if __name__ == "__main__":
    name = sys.argv[1]; res, M, d = zahlen(name); ZIEL_PEN = {"a2": (50, 120), "b": (0, 0)}.get(M["lastfall"], (25, 60)); res["ziel_eindringung_mm"] = ZIEL_PEN; bilder(res, name)   # ERWARTUNG Nachtrag 1: a 25-60, a2 50-120 mm
    gz = sorted(d.glob("X3A*.gz")); film = len(sys.argv) > 2 and sys.argv[2] == "film"; pf = d / "_film"
    if film: pf.mkdir(exist_ok=True)
    tt_ = np.array(res["kurve"]["t"]); pen_ = np.array(res["kurve"]["pen"]); sel = [gz[-1]] if not film else gz; last = None; mx = {"cell_uy": 0.0}
    umax = 0.0   # Nachtrag 3: max |U| der Zellknoten ueber alle Frames
    for i, g_ in enumerate(gz):
        if not film and g_ != gz[-1]:
            try: tt, P0, U, ids = vtk(d, g_); cm = (ids >= 400000) & (ids < 900000); umax = max(umax, float(np.linalg.norm(U[cm], axis=1).max()))
            except Exception as e: print("Anim", g_, repr(e))
            continue
        try: tt, P0, U, ids = vtk(d, g_)
        except Exception as e: print("Anim", g_, repr(e)); continue
        cm = (ids >= 400000) & (ids < 900000); umax = max(umax, float(np.linalg.norm(U[cm], axis=1).max()))
        cell = ids >= 400000; near = cell & (np.abs(P0[:, 1] - M["cy0"]) < 1e-3); mx["cell_uy"] = max(mx["cell_uy"], float(U[near, 1].max())); last = (tt, P0, U, ids)
        if film:
            f = frame(M, P0, U, ids, tt, pen=float(np.interp(tt, tt_, pen_))); f.savefig(pf / f"f{i:04d}.png", dpi=70); plt.close(f)
    if last:
        f = frame(M, last[1], last[2], last[3], last[0], pen=res["pfahl_eindringung_max_mm"]); f.savefig(D / f"verformung_{name}.png", dpi=110); plt.close(f)
        near = (last[3] >= 400000) & (np.abs(last[1][:, 1] - M["cy0"]) < 1e-3); res["zellblock_vorderseite_uy_max_Anim_mm"] = mx["cell_uy"]
    if film and any(pf.glob("f*.png")):
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "10", "-i", str(pf / "f%04d.png"), "-pix_fmt", "yuv420p", "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2", str(D / f"film_{name}.mp4")]); res["film"] = f"film_{name}.mp4"
    res["erwartung_pruefung"] = {"energiebilanz_unter_5_proz": (None if res["energiefehler_proz_max"] is None else res["energiefehler_proz_max"] < E_FEHLER), "pfahl_eindringung_20_100_mm": 20 <= res["pfahl_eindringung_max_mm"] <= 120, "pfahl_eindringung_im_Erwartungsband": ZIEL_PEN[0] <= res["pfahl_eindringung_max_mm"] <= ZIEL_PEN[1],
                                 "zellreihe_ab_Rahmenbreite_30mm_eingedrueckt": res["zellblock_vorderseite_dy_max_mm"] > 0.0}
    if res.get("bei_100kN"): res["erwartung_pruefung"].update({"b_rahmen_unter_10mm": res["bei_100kN"]["innenwand_mitte_mm"] < 10, "b_zellen_unter_2mm": res["bei_100kN"]["zellblock_vorderseite_mm"] < 2})
    a_, h_ = th(d); kin = float((a_[-1, 2] - 0.5 * M["M_kg"] * M.get("_vpe", 0.0) ** 2) / a_[0, 23] * 100); pw = res["pfahl_eindringung_max_mm"]; BQ_ = M.get("lastfall_art") == "b"   # kin ohne Rueckprall-Energie des Pfahls (Opus, Kriterium Nachtrag 3 praezisiert)
    res["zell_U_max_mm"] = umax; res["kin_ende_proz"] = kin; res["pruef_modell_ok"] = bool(umax <= 1.5 * pw and (BQ_ or kin < 5.0))
    allj = {}
    try: allj = json.load(open(D / "ergebnis.json"))
    except Exception: pass
    allj[name] = res; json.dump(allj, open(D / "ergebnis.json", "w"), indent=1, ensure_ascii=False)
    print(json.dumps({k: v for k, v in res.items() if k != "kurve"}, indent=1, ensure_ascii=False))
