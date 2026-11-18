#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-18), Entwurf. Auftrag X1b (Auswertung nach ../x1_seitencrash/auswerten.py).
Liest lauf/<V>_LF1_w<w>/{x1.dat,x1.frd,modell.json,x1.inp}, energieverlust.json; schreibt ergebnis.json, kraft_weg_w.png, verformung_<V>_w<w>.png."""
import sys, json
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).parent)); import frd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
D = Path(__file__).parent; EI = json.load(open(D.parent / "x1_seitencrash" / "eingaben.json")); EV = json.load(open(D / "energieverlust.json"))["ergebnis"]
LAST_KN = 100.0; E_ZIEL_J = 2000.0; GAPS = [1.0, 4.0]; WS = (15, 20, 30)
def dat(fn):
    t = []; F = []
    for b in open(fn).read().split("total force (fx,fy,fz) for set NBACK and time")[1:]:
        l = [x for x in b.strip().split("\n") if x.strip()]
        if len(l) < 2 or len(l[1].split()) < 3: continue
        t.append(float(l[0])); F.append(abs(float(l[1].split()[1])) / 1e3)
    return np.array(t), np.array(F)
def auswerten(var, w):
    d = D / "lauf" / f"{var}_LF1_w{w}"; m = json.load(open(d / "modell.json")); sp = EI["varianten"][var]["quertraeger_spiel_mm"]
    jobs = ["x1"] + sorted((p.stem for p in d.glob("x1r*.inp")), key=lambda x: int(x[3:])); tt_ = []; FF_ = []; fr = []; tgr = {}
    for j in jobs:   # x1 und Fortsetzungen zusammenfuehren; Daten eines Jobs nach dem Startpunkt des Nachfolgers werden verworfen
        if j != "x1" and (d / f"{j}.meta").exists(): tgr[j] = json.load(open(d / f"{j}.meta"))["t_start"]
    for i, j in enumerate(jobs):
        tmax = tgr.get(jobs[i + 1], 1e9) + 1e-6 if i + 1 < len(jobs) else 1e9
        if (d / f"{j}.dat").exists() and (d / f"{j}.dat").stat().st_size > 0:
            a, b = dat(d / f"{j}.dat"); k = a <= tmax; tt_ += list(a[k]); FF_ += list(b[k])
        if (d / f"{j}.frd").exists():
            nd, f_ = frd.lies(d / f"{j}.frd"); fr += [x for x in f_ if x["t"] <= tmax]
            if j == "x1": nodes = nd
    t = np.array(tt_); F = np.array(FF_); s = t * m["umax"] - m["cl"]
    pole = {int(l.split(",")[0]) for l in open(d / "x1.inp") if l.count(",") == 3 and l.split(",")[0].strip().isdigit() and 1000000 <= int(l.split(",")[0]) < 2000000}
    inn = [i for i, c in nodes.items() if i not in pole and abs(c[1] - 30) < 1e-3 and abs(c[0] - m["xp"]) < 500 and c[2] > 0
           and not any(x0 - sp - 0.01 <= c[0] <= x0 + m["qb"] + sp + 0.01 for x0 in m["quer_x0"])]
    fa = {}
    for b in fr:
        for k, v in b.items():
            if k != "t": fa.setdefault(round(b["t"], 6), {})[k] = v
    ts = sorted(k for k in fa if "DISP" in fa[k] and "PE" in fa[k]); uy = []; pe = []; pef = []; ploc = []   # Teilläufe: nur Frames mit Verschiebung und PEEQ
    for tt in ts:
        U = fa[tt]["DISP"]; P = fa[tt]["PE"]; uy.append(max(U[i][1] for i in inn))
        k = max((i for i in P if i not in pole), key=lambda i: P[i][0]); pe.append(P[k][0]); c = nodes[k]; ploc.append([round(c[0], 1), round(c[1], 1), round(c[2], 1)])
        pef.append(max(P[i][0] for i in P if i not in pole and nodes[i][1] > 1.0))
    ss = np.interp(ts, t, s); FF = np.interp(ts, t, F)
    s0 = np.concatenate([[0.0], s[s > 0]]); F0 = np.concatenate([[0.0], F[s > 0]])
    En = np.concatenate([[0.0], np.cumsum(0.5 * (F0[1:] + F0[:-1]) * np.diff(s0))])   # J (kN*mm)
    bei = {}
    for g in GAPS:
        idx = next((i for i, u in enumerate(uy) if u >= g), None)
        if idx is None: bei[f"{g:g}"] = None; continue
        i0 = max(idx - 1, 0); wt = 0 if idx == 0 else (g - uy[i0]) / (uy[idx] - uy[i0]); sg = ss[i0] + wt * (ss[idx] - ss[i0])
        bei[f"{g:g}"] = {"pfahlweg_mm": round(float(sg), 3), "kraft_kN": round(float(np.interp(sg, s0, F0)), 2), "energie_J": round(float(np.interp(sg, s0, En)), 1),
                         "peeq_max_gesamt": round(float(pe[i0] + wt * (pe[idx] - pe[i0])), 4), "peeq_max_rahmen": round(float(pef[i0] + wt * (pef[idx] - pef[i0])), 4)}
    return dict(var=var, w=w, xp=m["xp"], pfahlweg_ende_mm=float(s[-1]), kraft_ende_kN=float(F[-1]), kraft_max_kN=float(F.max()), energie_ende_J=float(En[-1]),
                kraft_mittel_bis_w_kN=float(np.interp(w, s0, En) / w) if s0[-1] >= w else None, energie_bei_w_J=float(np.interp(w, s0, En)) if s0[-1] >= w else None,
                peeq_max_ende=float(pe[-1]), peeq_max_rahmen_ende=float(pef[-1]), peeq_ort_ende=ploc[-1], uy_innen_ende_mm=float(uy[-1]), n_frames=len(ts),
                kurve={"s_mm": [round(float(x), 3) for x in s0], "F_kN": [round(float(x), 3) for x in F0], "E_J": [round(float(x), 1) for x in En]},
                frames={"s_mm": [round(float(x), 3) for x in ss], "uy_innen_max_mm": [round(float(x), 3) for x in uy]}, zellberuehrung_bei_spalt_mm=bei,
                energieverlust_proz=EV[var][str(w)]["Energieverlust_proz"])
R = {"hinweis": "KI-generiert, Entwurf. Aus lauf/*/x1.dat, x1.frd. Zellberuehrung = groesste y-Verschiebung der Rahmeninnenseite (|x-xp|<500, ausser Querträgerzonen) erreicht den Spalt (LFP 1 mm Verbinder, 4 mm Zellkoerper, NMC 0 mm, Naeherung 1 mm).", "laeufe": {}}
for v in ("LFP", "NMC"):
    for w in WS:
        lg = D / "lauf" / f"{v}_LF1_w{w}" / "ccx.log"
        if lg.exists() and (D / "lauf" / f"{v}_LF1_w{w}" / "x1.dat").stat().st_size > 0:
            try: R["laeufe"][f"{v}_w{w}"] = auswerten(v, w); R["laeufe"][f"{v}_w{w}"]["fertig"] = "Job finished" in lg.read_text()[-3000:]
            except Exception as e: print("Fehler", v, w, e)
json.dump(R, open(D / "ergebnis.json", "w"), indent=1, ensure_ascii=False)
col = {15: "#1f77b4", 20: "#2ca02c", 30: "#d62728"}; ls = {"LFP": "-", "NMC": "--"}
fig, (a1, a2) = plt.subplots(2, 1, figsize=(10, 9), sharex=True)
for k, r in R["laeufe"].items():
    a1.plot(r["kurve"]["s_mm"], r["kurve"]["F_kN"], ls[r["var"]], color=col[r["w"]], lw=2, label=f"{k}")
    a2.plot(r["kurve"]["s_mm"], np.array(r["kurve"]["E_J"]) / 1e3, ls[r["var"]], color=col[r["w"]], lw=2)
    for g, ma in (("1", "o"), ("4", "s")):
        b = r["zellberuehrung_bei_spalt_mm"].get(g)
        if b: a1.plot(b["pfahlweg_mm"], b["kraft_kN"], ma, color=col[r["w"]], mfc="none", ms=9); a2.plot(b["pfahlweg_mm"], b["energie_J"] / 1e3, ma, color=col[r["w"]], mfc="none", ms=9)
a1.axhspan(LAST_KN, max(160, a1.get_ylim()[1]), color="green", alpha=0.12, label="Zielband: Kraft ab 100 kN (Restkraft, Annahme)"); a1.axhline(LAST_KN, color="k", ls=":")
a2.axhspan(E_ZIEL_J / 1e3, max(4, a2.get_ylim()[1]), color="green", alpha=0.12, label="Zielband: Energie ab 2 kJ (Annahme)"); a2.axhline(E_ZIEL_J / 1e3, color="k", ls=":")
a1.set_ylabel("Pfahlkraft (kN)"); a2.set_ylabel("aufgenommene Energie (kJ)"); a2.set_xlabel("Pfahlweg ab Berührung des Knautschprofils (mm)")
a1.set_title("X1b: Knautschzone, Seitenpfahl Ø254 quasistatisch, LF1; durchgezogen LFP, gestrichelt NMC"); a1.legend(fontsize=8, loc="upper left"); a2.legend(fontsize=8, loc="upper left")
for a in (a1, a2): a.grid(alpha=0.3)
a1.text(0.99, 0.02, "Kreis = Spalt 1 mm, Quadrat = 4 mm an der Rahmeninnenseite erreicht", transform=a1.transAxes, ha="right", fontsize=8)
fig.tight_layout(); fig.savefig(D / "kraft_weg_w.png", dpi=130); plt.close(fig)
for k, r in R["laeufe"].items():
    v, w = r["var"], r["w"]; d = D / "lauf" / f"{v}_LF1_w{w}"; nodes, fr = frd.lies(d / "x1.frd"); fa = {}
    for jx in sorted((p.stem for p in d.glob("x1r*.inp")), key=lambda x: int(x[3:])):
        if (d / f"{jx}.frd").exists() and (d / f"{jx}.frd").stat().st_size > 100:
            _, f2 = frd.lies(d / f"{jx}.frd")
            if f2: fr = f2
    for b in fr:
        for kk, vv in b.items():
            if kk != "t": fa.setdefault(round(b["t"], 6), {})[kk] = vv
    tt = max(k for k in fa if "DISP" in fa[k] and "PE" in fa[k]); U = fa[tt]["DISP"]; P = fa[tt]["PE"]; pn = {int(l.split(",")[0]) for l in open(d / "x1.inp") if l.count(",") == 3 and l.split(",")[0].strip().isdigit() and 1000000 <= int(l.split(",")[0]) < 2000000}
    ids = [i for i in nodes if i in U and i in P and i not in pn]
    X = np.array([[nodes[i][j] + U[i][j] for j in range(3)] for i in ids]); pe = np.array([P[i][0] for i in ids]) * 100; o = np.argsort(pe); X = X[o]; pe = pe[o]; Y0 = np.array([nodes[i][1] for i in ids])[o]
    xp = r["xp"]; fig, axs = plt.subplots(2, 1, figsize=(11, 8), gridspec_kw={"height_ratios": [1, 1.4]}, layout="constrained")
    for a, (ix, iy) in zip(axs, ((0, 1), (0, 2))):
        mk = (Y0 < 5) if iy == 2 else np.ones(len(pe), bool)
        sc = a.scatter(X[mk, ix], X[mk, iy], c=pe[mk], s=8, cmap="viridis", vmin=0, vmax=max(10, pe.max())); a.set_aspect("equal"); a.set_xlim(xp - 130, xp + 130)
    axs[0].set_ylim(-w - 8, 50); axs[0].axhline(30, color="r", ls=":", lw=1); axs[0].text(xp - 125, 42, "rote Linie: Rahmeninnenseite Soll y = 30 mm (Zelle dahinter)", color="r", fontsize=8)
    axs[0].axhline(0, color="orange", ls=":", lw=1); axs[0].text(xp - 125, 3, "orange: Rahmenaußenseite y = 0, davor Knautschprofil", color="darkorange", fontsize=8)
    axs[0].set_title(f"{k}: Draufsicht (x/y), Verformung maßstäblich (1:1), Pfahlweg {r['pfahlweg_ende_mm']:.1f} mm, {r['kraft_ende_kN']:.0f} kN, PEEQ max {r['peeq_max_ende']*100:.0f} %", fontsize=9)
    axs[1].set_title("Seitenansicht (x/z), nur Knautschzone und Rahmenaußenseite (y < 5 mm)", fontsize=9); axs[0].set_xlabel("x (mm)"); axs[0].set_ylabel("y (mm)"); axs[1].set_xlabel("x (mm)"); axs[1].set_ylabel("z (mm)")
    cb = fig.colorbar(sc, ax=axs, pad=0.02, shrink=0.8); cb.set_label("plastische Dehnung PEEQ (%); Bruchdehnung 10 % (rot)"); cb.ax.axhline(10, color="r", lw=2)
    fig.savefig(D / f"verformung_{v}_w{w}.png", dpi=110); plt.close(fig)
print(json.dumps({k: {"ende_s": r["pfahlweg_ende_mm"], "F_ende": r["kraft_ende_kN"], "E_ende": r["energie_ende_J"], "fertig": r["fertig"], "bei": r["zellberuehrung_bei_spalt_mm"]} for k, r in R["laeufe"].items()}, indent=1)[:3500])
