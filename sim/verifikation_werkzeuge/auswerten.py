#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-23), Entwurf. QN1: fuegt ergebnis_V1..V5.json zu ergebnis.json zusammen und zeichnet die Bilder (Zielband = Toleranz der ERWARTUNG).
Aufruf: python3 auswerten.py"""
import json, os
import numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.ticker; import matplotlib.pyplot as plt
from vcommon import *
GR, RT, GA = "#2a9d4f", "#c0392b", "#888888"
Rs = {f: json.load(open(f"{H}/ergebnis_{f}.json")) for f in ("V1", "V2", "V3", "V4", "V5") if os.path.exists(f"{H}/ergebnis_{f}.json")}
def dreieck(ax, x, y, p=2, fx=2.0):
    x2 = x*fx; y2 = y*fx**p; ax.plot([x, x2, x2, x], [y, y, y2, y], color=GA, lw=1); ax.text(x2*1.05, (y*y2)**0.5, f"Steigung {p}", color=GA, fontsize=8, va="center")
def band(ax, tol, label):
    ax.axhspan(1e-12, tol, color=GR, alpha=0.12); ax.axhline(tol, color=GR, lw=1.5); ax.text(0.02, tol*1.15, label, transform=ax.get_yaxis_transform(), color=GR, fontsize=8)
# V1
if "V1" in Rs:
    r = Rs["V1"]; fig, ax = plt.subplots(figsize=(6.2, 4.4)); u = r["reihe_ungerade"]
    h = [x["h_m"]*1000 for x in u]; e = [abs(x["abw_pct"]) for x in u]
    ax.loglog(h, e, "o-", color=GR if r["bestanden"] else RT, label="Elmer, Q4, ungerade Elementzahl")
    for x in u: ax.annotate(f"N={x['N']}", (x["h_m"]*1000, abs(x["abw_pct"])), textcoords="offset points", xytext=(5, 5), fontsize=8)
    band(ax, r["toleranz_pct"], f"Zielband &lt; {r['toleranz_pct']:g} %".replace("&lt;", "<")); dreieck(ax, h[-1]*1.0, e[-1]*0.35, 2)
    ax.set_xlabel("Elementgröße h [mm]"); ax.set_ylabel("|Abweichung T_max| [%]"); ax.set_ylim(0.05, 10)
    ax.set_title(f"V1 Elmer Wärmeleitung: Abweichung fein {r['abweichung_fein_pct']:+.2f} %, Ordnung {r['ordnung_beobachtet'][-1]:.2f}\n({'bestanden' if r['bestanden'] else 'verfehlt'}; Wärmestrom {r['waermestrom_abw_fein_pct']:+.3f} %)", fontsize=10); ax.legend(fontsize=8, loc="lower right"); ax.grid(True, which="both", alpha=0.25)
    fig.text(0.01, 0.005, "KI-generiert (Claude Sonnet, 2026-11-23), Entwurf", fontsize=6, color=GA); fig.tight_layout(); fig.savefig(f"{H}/v1_konvergenz.png", dpi=150); plt.close(fig)
# V2
if "V2" in Rs:
    r = Rs["V2"]; fig, axs = plt.subplots(1, 2, figsize=(11, 4.6))
    ax = axs[0]
    for tag, c, lab in (("tauK3", RT, "ν wie K3 (τ = 0,532)"), ("tau0p8", "#2c6fbb", "ν = 0,1 (τ = 0,8), Zusatz")):
        s = r["reihen"][tag]["stufen"]; ax.loglog([x["h"] for x in s], [max(abs(x["abw_u_mittel_pct"]), 1e-3) for x in s], "o-", color=c, label=lab)
    band(ax, r["toleranz_pct"], f"Zielband < {r['toleranz_pct']:g} % (ab h = 20 Zellen)"); ax.axvline(20, color=GA, ls=":", lw=1); ax.text(20.5, 15, "h = 20", color=GA, fontsize=8)
    ax.axvspan(4, 5, color="#f0a030", alpha=0.2); ax.text(4.9, 0.02, "K3: ca. 4–5\nZellen", fontsize=7, color="#a06010")
    s = r["reihen"]["tauK3"]["stufen"]; dreieck(ax, 16, abs(s[3]["abw_u_mittel_pct"])*0.3, 2, 2.0) if False else None
    ax.invert_xaxis(); ax.set_xlabel("Zellen über dem Spalt h (rechts grob, links fein)".replace("rechts grob, links fein", "links fein = hoch")); ax.set_ylabel("|Abweichung u_mittel| [%]  (= Abweichung Δp)")
    ax.set_xlabel("Auflösung h [Zellen über dem Spalt]"); ax.invert_xaxis(); ax.set_title(f"V2 FluidX3D: Abweichung über Auflösung\n(h = 32: {s[-1]['abw_u_mittel_pct']:+.2f} %, Ordnung 8→16→32: {r['ordnung_beobachtet'][0]:.2f}/{r['ordnung_beobachtet'][1]:.2f}, {'bestanden' if r['bestanden'] else 'verfehlt'})", fontsize=10)
    ax.legend(fontsize=8, loc="upper right"); ax.grid(True, which="both", alpha=0.25); ax.set_xticks([4, 5, 8, 16, 32]); ax.set_xticklabels([4, 5, 8, 16, 32]); ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter()); ax.set_ylim(1e-2, 30)
    ax = axs[1]
    for x, c in zip(r["reihen"]["tauK3"]["stufen"], plt.cm.viridis(np.linspace(0, 0.9, 5))):
        h = x["h"]; yc = (np.arange(h)+0.5)/h; ua = x["G"]*(yc*h)*(h-yc*h)/(2*x["nu"]); ax.plot(yc, np.array(x["profil_uz"])/x["u_max_ana_exakt"], "o", ms=3, color=c, label=f"h = {h}")
    yy = np.linspace(0, 1, 100); ax.plot(yy, 4*yy*(1-yy), "k-", lw=1, label="analytisch (Parabel)"); ax.set_xlabel("y / h"); ax.set_ylabel("u / u_max,analytisch"); ax.set_title("Profile (ν wie K3)", fontsize=10); ax.legend(fontsize=8); ax.grid(alpha=0.25)
    fig.text(0.01, 0.005, "KI-generiert (Claude Sonnet, 2026-11-23), Entwurf", fontsize=6, color=GA); fig.tight_layout(); fig.savefig(f"{H}/v2_aufloesung.png", dpi=150); plt.close(fig)
# V3, V4, V5, Einzelbilder als Balken gegen Zielband
def balken(fall, titel, werte, tol, einheit, fn, ok):
    fig, ax = plt.subplots(figsize=(5.6, 3.8)); xs = range(len(werte)); cs = [GR if abs(v) < t else RT for (_, v), t in zip(werte, tol)]
    ax.bar(xs, [abs(v) for _, v in werte], color=cs); ax.set_xticks(list(xs)); ax.set_xticklabels([n for n, _ in werte], fontsize=8)
    for i, ((_, v), t) in enumerate(zip(werte, tol)): ax.hlines(t, i-0.45, i+0.45, color="k", lw=2); ax.text(i, t*1.5, f"Zielband < {t:g} {einheit}", ha="center", fontsize=7)
    for i, (_, v) in enumerate(werte): ax.text(i, abs(v)*1.15, f"{v:+.3g}", ha="center", color="k", fontsize=8, fontweight="bold")
    ax.set_ylabel(f"|Abweichung| [{einheit}]"); ax.set_yscale("log"); ax.set_ylim(1e-6 if fall == "V5" else 1e-6, 100); ax.set_title(titel, fontsize=9); ax.grid(axis="y", alpha=0.25)
    fig.text(0.01, 0.005, "KI-generiert (Claude Sonnet, 2026-11-23), Entwurf", fontsize=6, color=GA); fig.tight_layout(); fig.savefig(f"{H}/{fn}", dpi=150); plt.close(fig)
if "V3" in Rs:
    r = Rs["V3"]; balken("V3", f"V3 OpenRadioss Kragbalken: {r['delta_werkzeug_mm']:.5f} mm gegen {r['delta_analytisch_mm']:.5f} mm ({'bestanden' if r['bestanden'] else 'verfehlt'})", [("Durchbiegung [%]", r["abweichung_fein_pct"]), ("Energiebilanz [%]", r["energiefehler_max_pct"])], [r["toleranz_delta_pct"], r["toleranz_energie_pct"]], "%", "v3_kragbalken.png", r["bestanden"])
if "V4" in Rs:
    r = Rs["V4"]; w_ = [(f"{k}\nLadung [%]", v["abw_ladung_projektmodell_SPMe_pct"]) for k, v in r["saetze"].items()]+[(f"{k}\nSPM-DFN [mV]", v["spm_dfn_dU_max_mV"]) for k, v in r["saetze"].items()]
    tol = [r["toleranz_ladung_pct"]]*len(r["saetze"])+[r["toleranz_spm_dfn_mV"]]*len(r["saetze"]); fig, ax = plt.subplots(figsize=(6.4, 4))
    cs = [GR if abs(v) < t else RT for (_, v), t in zip(w_, tol)]; ax.bar(range(len(w_)), [max(abs(v), 1e-3) for _, v in w_], color=cs); ax.set_yscale("log"); ax.set_ylim(1e-2, 200); ax.set_xticks(range(len(w_))); ax.set_xticklabels([n for n, _ in w_], fontsize=8)
    for i, ((_, v), t) in enumerate(zip(w_, tol)): ax.hlines(t, i-0.45, i+0.45, color="k", lw=2); ax.text(i, t*1.5, f"< {t:g}", ha="center", fontsize=7); ax.text(i, max(abs(v), 1e-3)*1.12, f"{v:+.3g}", ha="center", color="k", fontsize=8, fontweight="bold")
    ax.set_ylabel("|Abweichung| (% bzw. mV)"); ax.set_title(f"V4 PyBaMM C/20: Ladung gegen Nennkapazität, SPM gegen DFN ({'bestanden' if r['bestanden'] else 'verfehlt'})", fontsize=9); ax.grid(axis="y", alpha=0.25)
    fig.text(0.01, 0.005, "KI-generiert (Claude Sonnet, 2026-11-23), Entwurf. Schwarze Linie = Zielband", fontsize=6, color=GA); fig.tight_layout(); fig.savefig(f"{H}/v4_pybamm.png", dpi=150); plt.close(fig)
    if os.path.exists(f"{H}/lauf_V4_kurven.json"):
        K = json.load(open(f"{H}/lauf_V4_kurven.json")); fig, axs = plt.subplots(1, 2, figsize=(10, 4))
        for ax, (k, v) in zip(axs, K.items()):
            for m, c in (("SPM", "#2c6fbb"), ("DFN", RT), ("SPMe", GR)): ax.plot(*v[m], color=c, lw=1.5, ls="--" if m == "SPMe" else "-", label=m)
            ax.axvline(v["Qn"], color="k", lw=1, ls=":"); ax.text(v["Qn"], ax.get_ylim()[0]+0.02, " Nennkapazität", fontsize=8, ha="right"); ax.set_title(f"{k}: C/20-Entladung", fontsize=10); ax.set_xlabel("entnommene Ladung [Ah]"); ax.set_ylabel("Klemmenspannung [V]"); ax.legend(fontsize=8); ax.grid(alpha=0.25)
        fig.text(0.01, 0.005, "KI-generiert (Claude Sonnet, 2026-11-23), Entwurf", fontsize=6, color=GA); fig.tight_layout(); fig.savefig(f"{H}/v4_kurven.png", dpi=150); plt.close(fig)
if "V5" in Rs:
    r = Rs["V5"]; balken("V5", f"V5 Verteiler-1D Einzelkanal {r['kanal_mm'][0]:g}x{r['kanal_mm'][1]:g} mm: Δp gegen exakte Reihe ({'bestanden' if r['bestanden'] else 'verfehlt'})",
                         [(f"Re {f['Re']:.0f}\nexakt", f["abw_werkzeug_gegen_exakt_pct"]) for f in r["faelle"]]+[(f"Re {f['Re']:.0f}\nShah-London", max(abs(f["abw_werkzeug_gegen_shahlondon_pct"]), 1e-6)) for f in r["faelle"]], [r["toleranz_pct"]]*(2*len(r["faelle"])), "%", "v5_verteiler.png", r["bestanden"])
# Sammelbild
fig, ax = plt.subplots(figsize=(7.5, 4.4)); namen = []; vals = []; tols = []; oks = []
def add(n, v, t, ok): namen.append(n); vals.append(max(abs(v), 1e-3)); tols.append(t); oks.append(ok)
if "V1" in Rs: r = Rs["V1"]; add("V1 Elmer\nT_max", r["abweichung_fein_pct"], r["toleranz_pct"], abs(r["abweichung_fein_pct"]) < r["toleranz_pct"])
if "V2" in Rs: r = Rs["V2"]; add("V2 FluidX3D\nh = 32", r["abweichung_fein_pct"], r["toleranz_pct"], r["bestanden"])
if "V3" in Rs: r = Rs["V3"]; add("V3 Radioss\nDurchbiegung", r["abweichung_fein_pct"], r["toleranz_delta_pct"], abs(r["abweichung_fein_pct"]) < r["toleranz_delta_pct"])
if "V4" in Rs: r = Rs["V4"]; l = r["saetze"]["LFP"]; n_ = r["saetze"]["NMC"]; add("V4 PyBaMM\nLadung LFP", l["abw_ladung_projektmodell_SPMe_pct"], r["toleranz_ladung_pct"], l["bestanden_ladung"]); add("V4 PyBaMM\nLadung NMC", n_["abw_ladung_projektmodell_SPMe_pct"], r["toleranz_ladung_pct"], n_["bestanden_ladung"])
if "V5" in Rs: r = Rs["V5"]; add("V5 Verteiler\nΔp Kanal", r["abweichung_fein_pct"], r["toleranz_pct"], r["bestanden"])
ax.bar(range(len(vals)), vals, color=[GR if o else RT for o in oks]); ax.set_yscale("log"); ax.set_xticks(range(len(vals))); ax.set_xticklabels(namen, fontsize=8)
for i, (v, t, o) in enumerate(zip(vals, tols, oks)): ax.hlines(t, i-0.45, i+0.45, color="k", lw=2); ax.text(i, t*1.5, f"Zielband < {t:g} %", ha="center", fontsize=7); ax.text(i, v*1.15, f"{v:.3g} %", ha="center", color="k", fontsize=8, fontweight="bold")
ax.set_ylim(2e-2, 200); ax.set_ylabel("|Abweichung| gegen analytische Lösung [%]"); ax.set_title("QN1 Werkzeugprüfung: grün bestanden, rot verfehlt (schwarz = Toleranz der ERWARTUNG)", fontsize=9); ax.grid(axis="y", alpha=0.25)
fig.text(0.01, 0.005, "KI-generiert (Claude Sonnet, 2026-11-23), Entwurf", fontsize=6, color=GA); fig.tight_layout(); fig.savefig(f"{H}/qn1_sammelbild.png", dpi=150); plt.close(fig)
ges = dict(hinweis="KI-generiert (Claude Sonnet, 2026-11-23), Entwurf. Zusammenfassung aus ergebnis_V1..V5.json (auswerten.py).",
           faelle={f: dict(bestanden=r["bestanden"], abweichung_fein_pct=r["abweichung_fein_pct"], ordnung_beobachtet=r["ordnung_beobachtet"], datei=f"ergebnis_{f}.json") for f, r in Rs.items()},
           alle_bestanden=all(r["bestanden"] for r in Rs.values()), toleranz=TOL)
json.dump(ges, open(f"{H}/ergebnis.json", "w"), indent=1); print({f: v["bestanden"] for f, v in ges["faelle"].items()})
