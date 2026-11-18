#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-18), Entwurf. Auftrag X1. Liest lauf/<V>_<LF>_<netz>/{x1.dat,x1.frd,modell.json}, schreibt ergebnis.json und Bilder.
Aufruf: auswerten.py <netz>   (Hauptnetz, Standard m12)"""
import sys, json, re
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).parent)); import frd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
D = Path(__file__).parent; EI = json.load(open(D / "eingaben.json")); netz = sys.argv[1] if len(sys.argv) > 1 else "m12"
LAST_KN = EI["last_restkraft_kN"]["wert"]; GAPS = [1.0, 4.0, 24.0]
def dat(fn):
    t = []; F = []; tx = open(fn).read().split("total force (fx,fy,fz) for set NBACK and time")[1:]
    for b in tx:
        l = [x for x in b.strip().split("\n") if x.strip()]
        if len(l) < 2 or len(l[1].split()) < 3: continue
        t.append(float(l[0])); F.append(abs(float(l[1].split()[1])) / 1e3)
    return np.array(t), np.array(F)
def auswerten(var, lf, nz):
    d = D / "lauf" / f"{var}_{lf}_{nz}"; m = json.load(open(d / "modell.json")); sp = EI["varianten"][var]["quertraeger_spiel_mm"]
    t, F = dat(d / "x1.dat"); s = t * m["umax"] - m["cl"]
    nodes, fr = frd.lies(d / "x1.frd")
    pole = {int(l.split(",")[0]) for l in open(d / "x1.inp") if l.count(",") == 3 and l.split(",")[0].strip().isdigit() and 1000000 <= int(l.split(",")[0]) < 2000000}
    inn = [i for i, c in nodes.items() if i not in pole and abs(c[1] - 30) < 1e-3 and abs(c[0] - m["xp"]) < 500 and c[2] > 0
           and not any(x0 - sp - 0.01 <= c[0] <= x0 + m["qb"] + sp + 0.01 for x0 in m["quer_x0"])]
    fa = {}
    for b in fr:
        for k, v in b.items():
            if k != "t": fa.setdefault(round(b["t"], 6), {})[k] = v
    ts = sorted(fa); uy = []; pe = []; ploc = []
    for tt in ts:
        U = fa[tt]["DISP"]; P = fa[tt]["PE"]; uy.append(max(U[i][1] for i in inn))
        k = max((i for i in P if i not in pole), key=lambda i: P[i][0]); pe.append(P[k][0]); c = nodes[k]; u = U[k]; ploc.append([round(c[0], 1), round(c[1], 1), round(c[2], 1)])
    ss = np.interp(ts, t, s); FF = np.interp(ts, t, F)
    # Energie: Fläche unter F(s) ab s=0 (Kontaktbeginn), F in kN, s in mm -> J
    s0 = np.concatenate([[0.0], s[s > 0]]); F0 = np.concatenate([[0.0], F[s > 0]])
    En = np.concatenate([[0.0], np.cumsum(0.5 * (F0[1:] + F0[:-1]) * np.diff(s0))])   # J (kN*mm)
    bei = {}
    for g in GAPS:
        idx = next((i for i, u in enumerate(uy) if u >= g), None)
        if idx is None: bei[f"{g:g}"] = None; continue
        i0 = max(idx - 1, 0); w = 0 if idx == 0 else (g - uy[i0]) / (uy[idx] - uy[i0]); sg = ss[i0] + w * (ss[idx] - ss[i0])
        bei[f"{g:g}"] = {"pfahlweg_mm": round(float(sg), 3), "kraft_kN": round(float(np.interp(sg, s0, F0)), 2), "energie_J": round(float(np.interp(sg, s0, En)), 1),
                         "peeq_max": round(float(pe[i0] + w * (pe[idx] - pe[i0])), 4), "peeq_ort_xyz_mm": ploc[idx]}
    return dict(var=var, lf=lf, netz=nz, xp=m["xp"], pfahlweg_ende_mm=float(s[-1]), kraft_ende_kN=float(F[-1]), kraft_max_kN=float(F.max()), energie_ende_J=float(En[-1]), peeq_max_ende=float(pe[-1]), peeq_ort_ende=ploc[-1],
                kurve={"s_mm": [round(float(x), 3) for x in s0], "F_kN": [round(float(x), 3) for x in F0], "E_J": [round(float(x), 1) for x in En]},
                frames={"t": ts, "s_mm": [round(float(x), 3) for x in ss], "uy_innen_max_mm": [round(float(x), 3) for x in uy], "peeq_max": [round(float(x), 4) for x in pe]}, zellberuehrung_bei_spalt_mm=bei)
R = {"hinweis": "KI-generiert, Entwurf. Aus lauf/*/x1.dat und x1.frd. Zellberührung = grösste y-Verschiebung der Rahmeninnenseite (ausserhalb Querträgerzonen, |x-xp| < 500) erreicht den Spalt (mm).",
     "netz": netz, "spalt_herkunft": EI["frei_weg"], "läufe": {}}
for v in ("LFP", "NMC"):
    for lf in ("LF1", "LF2"):
        if "fertig" in (D / "lauf" / f"{v}_{lf}_{netz}" / "ccx.log").read_text()[-200:]: R["läufe"][f"{v}_{lf}"] = auswerten(v, lf, netz)
# Netzstudie LFP LF1: Vergleich mit g8 (feineres Netz, Ende 5 mm)
if (D / "lauf/LFP_LF1_g8/x1.dat").exists() and "LFP_LF1" in R["läufe"]:
    g = auswerten("LFP", "LF1", "g8"); h = R["läufe"]["LFP_LF1"]; st = {}
    for sx in (1.4, 4.4):
        a = np.interp(sx, h["kurve"]["s_mm"], h["kurve"]["F_kN"]); b = np.interp(sx, g["kurve"]["s_mm"], g["kurve"]["F_kN"])
        st[f"s={sx}"] = {"F_Hauptnetz_kN": round(float(a), 2), "F_fein_kN": round(float(b), 2), "abw_proz": round(float((a - b) / b * 100), 1)}
    R["netzstudie_LFP_LF1"] = {"haupt_h_nah_mm": 12, "fein_h_nah_mm": 8, "vergleich": st, "fein_ergebnis": {"zellberuehrung": g["zellberuehrung_bei_spalt_mm"], "kraft_ende_kN": g["kraft_ende_kN"], "pfahlweg_ende_mm": g["pfahlweg_ende_mm"]}}
json.dump(R, open(D / "ergebnis.json", "w"), indent=1, ensure_ascii=False)
# Bild Kraft-Weg
fig, ax = plt.subplots(figsize=(9, 5.5)); col = {"LFP_LF1": "#1f77b4", "LFP_LF2": "#2ca02c", "NMC_LF1": "#d62728", "NMC_LF2": "#ff7f0e"}
for k, r in R["läufe"].items(): ax.plot(r["kurve"]["s_mm"], r["kurve"]["F_kN"], label=k, color=col[k], lw=2)
ax.axhline(LAST_KN, color="k", ls="--", label=f"{LAST_KN} kN Restkraft (Annahme)"); ax.axhspan(30, 80, color="grey", alpha=0.15, label="Erwartung LF1 30-80 kN")
for g_, st_ in (("1", ":"), ("4", "-.")): pass
ax.set_xlabel("Pfahlweg ab Berührung des Rahmens (mm)"); ax.set_ylabel("Pfahlkraft (kN)"); ax.set_title("X1 Seitenpfahl: Kraft über Weg, Pfahl Ø254 mm quasistatisch"); ax.grid(alpha=0.3); ax.legend(fontsize=8)
for k, r in R["läufe"].items():
    for g_, ma in (("1", "o"), ("4", "s")):
        b = r["zellberuehrung_bei_spalt_mm"].get(g_)
        if b: ax.plot(b["pfahlweg_mm"], b["kraft_kN"], ma, color=col[k], mfc="none", ms=8)
ax.text(0.02, 0.88, "Kreis = Spalt 1 mm erreicht (LFP: Zellverbinder), Quadrat = 4 mm (LFP: Zellkörper)", transform=ax.transAxes, va="top", fontsize=8)
fig.tight_layout(); fig.savefig(D / "kraft_weg.png", dpi=130); plt.close(fig)
# Verformungsbilder (Draufsicht, Farbe PEEQ, letzter Rahmen)
for k, r in R["läufe"].items():
    v, lf = k.split("_"); d = D / "lauf" / f"{v}_{lf}_{netz}"; nodes, fr = frd.lies(d / "x1.frd"); fa = {}
    for b in fr:
        for kk, vv in b.items():
            if kk != "t": fa.setdefault(round(b["t"], 6), {})[kk] = vv
    tt = max(fa); U = fa[tt]["DISP"]; P = fa[tt]["PE"]; pn = {int(l.split(",")[0]) for l in open(d / "x1.inp") if l.count(",") == 3 and l.split(",")[0].strip().isdigit() and 1000000 <= int(l.split(",")[0]) < 2000000}
    ids = [i for i in nodes if i in U and i in P and i not in pn]
    ÜF = 5.0
    X = np.array([[nodes[i][0] + ÜF * U[i][0], nodes[i][1] + ÜF * U[i][1], nodes[i][2] + ÜF * U[i][2]] for i in ids]); pe = np.array([P[i][0] for i in ids]) * 100; o = np.argsort(pe); X = X[o]; pe = pe[o]; Y0 = np.array([nodes[i][1] for i in ids])[o]
    fig, axs = plt.subplots(2, 1, figsize=(11, 7.5), gridspec_kw={"height_ratios": [1, 1.6]}, layout="constrained"); xp = r["xp"]
    for a, (ix, iy) in zip(axs, ((0, 1), (0, 2))):
        mk = (Y0 < 31) if iy == 2 else np.ones(len(pe), bool)
        sc = a.scatter(X[mk, ix], X[mk, iy], c=pe[mk], s=7, cmap="viridis", vmin=0, vmax=max(10, pe.max())); a.set_aspect("equal"); a.set_xlim(xp - 160, xp + 160)
    axs[0].set_ylim(-3, 50); axs[0].set_title(f"{k}: Draufsicht (x/y), Verformung 5-fach überhöht, Weg {r['pfahlweg_ende_mm']:.1f} mm, {r['kraft_ende_kN']:.0f} kN, PEEQ max {r['peeq_max_ende']*100:.1f} %")
    axs[0].axhline(30, color="r", ls=":", lw=1); axs[0].text(xp - 155, 44, "rote Linie: Rahmeninnenseite Soll y = 30 mm (LFP: Zellverbinder bei 31)", color="r", fontsize=8)
    axs[0].set_title(axs[0].get_title(), fontsize=9)
    axs[1].set_title("Seitenansicht (x/z), nur Seitenrahmen", fontsize=9); axs[0].set_xlabel("x (mm)"); axs[0].set_ylabel("y (mm)"); axs[1].set_xlabel("x (mm)"); axs[1].set_ylabel("z (mm)")
    cb = fig.colorbar(sc, ax=axs, pad=0.02, shrink=0.8); cb.set_label("plastische Dehnung PEEQ (%); Zielband: unter Bruchdehnung 10 %"); cb.ax.axhline(10, color="r", lw=2)
    fig.savefig(D / f"verformung_{k}.png", dpi=110); plt.close(fig)
print(json.dumps({k: {"ende_s": r["pfahlweg_ende_mm"], "F_ende": r["kraft_ende_kN"], "bei": r["zellberuehrung_bei_spalt_mm"]} for k, r in R["läufe"].items()}, indent=1)[:3000])
