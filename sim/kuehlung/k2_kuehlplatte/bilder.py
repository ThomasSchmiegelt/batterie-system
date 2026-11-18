#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. Bilder K2 aus ergebnis.json (Punkte) und kuehlplatte.py (Kurven)."""
import json, os, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import kuehlplatte as K
H = K.H; O = json.load(open(f"{H}/ergebnis.json")); Z = K.E["ziele"]; zus = K.zus
FALL = [("LFP_P0", "LFP, Fall LFP_P0 (20 min)"), ("NMC_P4", "NMC, Fall NMC_P4 (30 min)"), ("NMC_P3", "NMC, Fall NMC_P3 (25 min)")]
col = {10: "#1b6ca8", 15: "#e08a00", 20: "#2a9d4b"}; ls = {"quer": "-", "laengs": "--"}
fig, ax = plt.subplots(2, 3, figsize=(16, 9))
for j, (fn, tit) in enumerate(FALL):
    W = O["waerme"][fn]; P = O["platten"][W["var"]]
    Vs = np.linspace(0.5, 1.6, 2) ; dTs = np.linspace(3, 12, 60)
    for w in K.kan["breiten_mm"]:
        for fh in ("quer", "laengs"):
            Lk, Bq = (P["B"], P["L"]) if fh == "quer" else (P["L"], P["B"]); n = int(Bq/(w/1000+K.st))
            V, h, dp = [], [], []
            for dT in dTs:
                Vp = W["W_je_platte"]/(K.rho*K.c*dT); r = K.kanal(w/1000, Lk, Vp/n)
                V.append(2*Vp*6e4); h.append(r["h"]); dp.append((1+zus)*r["dp_kanal_Pa"]/1e5)
            ax[0, j].plot(V, dp, ls[fh], color=col[w], label=f"{w} mm {fh}"); ax[1, j].plot(V, h, ls[fh], color=col[w])
    for x in O["faelle"]:
        if x["fall"] == fn and x["fuehrung"] == "quer":
            ax[0, j].plot(x["V_pack_L_min"], x["dp_bar"], "o", color=col[x["breite_mm"]], ms=4); ax[1, j].plot(x["V_pack_L_min"], x["h_W_m2K"], "o", color=col[x["breite_mm"]], ms=4)
    for dT in K.kan["dT_kuehlmittel_K"]:
        Vm = 2*W["W_je_platte"]/(K.rho*K.c*dT)*6e4; ax[0, j].axvline(Vm, color="grey", lw=.6, ls=":"); ax[0, j].text(Vm, 1.6e-4, f"{dT} K", ha="center", fontsize=8, color="grey")
    ax[0, j].axhspan(1e-4, Z["dp_max_bar_je_pack"], color="#2a9d4b", alpha=.15); ax[0, j].axhline(Z["dp_max_bar_je_pack"], color="#2a9d4b")
    ax[0, j].text(0.02, 0.55, f"Zielband dp <= {Z['dp_max_bar_je_pack']} bar (Annahme)", transform=ax[0, j].transAxes, color="#1d6b34", fontsize=9)
    ax[0, j].axhline(1.0, color="#c0392b", ls="-."); ax[0, j].text(0.02, 0.90, "verfehlt ab 1 bar (Annahme)", transform=ax[0, j].transAxes, color="#c0392b", fontsize=9)
    ax[0, j].set_yscale('log'); ax[0, j].set_ylim(1e-4, 3); ax[0, j].set_title(tit); ax[0, j].set_ylabel("Druckverlust je Pack [bar], log"); ax[0, j].set_xlabel("Durchfluss Pack [L/min] (Punkte: dT 5/8/10 K)")
    ax[1, j].axhspan(Z["h_min_W_m2K"], 1000, color="#2a9d4b", alpha=.15); ax[1, j].axhline(Z["h_min_W_m2K"], color="#2a9d4b")
    ax[1, j].text(0.02, 0.93, f"Zielband h >= {Z['h_min_W_m2K']} W/(m2K) (K0/K1-Annahme)", transform=ax[1, j].transAxes, color="#1d6b34", fontsize=9)
    ax[1, j].axhspan(0, 300, color="#c0392b", alpha=.12); ax[1, j].text(0.02, 0.05, "verfehlt unter 300 (Annahme)", transform=ax[1, j].transAxes, color="#c0392b", fontsize=9)
    ax[1, j].set_ylim(0, 1000); ax[1, j].set_ylabel("Wärmeübergang h im Kanal [W/(m²K)]"); ax[1, j].set_xlabel("Durchfluss Pack [L/min]")
ax[0, 0].legend(fontsize=8, title="Kanalbreite, Führung", loc="lower right")
fig.suptitle("K2 Kühlplatten: Druckverlust und Wärmeübergang über dem Durchfluss (1D-Rechnung, Annahmen siehe eingaben.json)", fontsize=11)
fig.text(0.5, 0.005, "KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. Quelle: sim/kuehlung/k2_kuehlplatte/ergebnis.json", ha="center", fontsize=8)
fig.tight_layout(rect=(0, .02, 1, .97)); fig.savefig(f"{H}/durchfluss_druck.png", dpi=130); plt.close(fig)

# Draufsicht je Variante: Auswahlkandidat = hoechstes h (kein Fall erfuellt h>=500), quer, 20 mm, dT 5 K
for v, fn in (("LFP", "LFP_P0"), ("NMC", "NMC_P4")):
    P = O["platten"][v]; x = [q for q in O["faelle"] if q["fall"] == fn and q["breite_mm"] == 20 and q["fuehrung"] == "quer" and q["dT_K"] == 5][0]
    L, B = P["L"]*1000, P["B"]*1000; w, st = 20, K.kan["steg_mm"]; n = x["n_kanaele"]
    fig, a = plt.subplots(figsize=(14, 6.5)); a.add_patch(Rectangle((0, 0), L, B, fc="#e8eef3", ec="k"))
    for i in range(n):
        y0 = st/2 + i*(w+st)+ (L-n*(w+st)+st)/2 if False else None
    # quer: Kanaele laufen ueber die Breite B, nebeneinander entlang L
    for i in range(n):
        x0 = (L-n*(w+st)+st)/2 + i*(w+st); a.add_patch(Rectangle((x0, 20), w, B-40, fc="#7fb8e0", ec="none"))
    a.add_patch(Rectangle((0, 0), L, 20, fc="#1b6ca8", alpha=.8)); a.add_patch(Rectangle((0, B-20), L, 20, fc="#c0392b", alpha=.8))
    a.text(L/2, 8, "Verteiler (Vorlauf), Annahme 20 mm", ha="center", va="center", color="w", fontsize=9); a.text(L/2, B-12, "Sammler (Rücklauf), Annahme 20 mm", ha="center", va="center", color="w", fontsize=9)
    a.annotate("", xy=(L*.2, B-30), xytext=(L*.2, 30), arrowprops=dict(arrowstyle="->", lw=2)); a.text(L*.2+15, B/2, "Strömung", fontsize=10)
    a.set_xlim(-60, L+60); a.set_ylim(-60, B+90); a.set_aspect("equal"); a.set_xlabel("Länge [mm]"); a.set_ylabel("Breite [mm]")
    a.set_title(f"Kühlplatte {v} (eine von 2), Draufsicht, Variante quer, {w} mm Kanäle, {n} parallel, Stege {st} mm, Plattenmaß {L:.0f} x {B:.0f} mm (Quelle {P['quelle']})\n"
                f"Fall {fn}: dT 5 K -> {x['V_pack_L_min']:.1f} L/min Pack, Re {x['Re']:.0f}, h {x['h_W_m2K']:.0f} W/(m²K) (Ziel >= {Z['h_min_W_m2K']}: verfehlt), dp {x['dp_bar']:.3f} bar (Ziel <= {Z['dp_max_bar_je_pack']}: erfüllt)", fontsize=9)
    fig.text(0.5, 0.01, "KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. Zahlen aus ergebnis.json. Kanäle maßstäblich, Verteiler nur schematisch.", ha="center", fontsize=8)
    fig.tight_layout(rect=(0, .03, 1, 1)); fig.savefig(f"{H}/platte_{v}.png", dpi=130); plt.close(fig)
print("ok")

# Nachtrag: U_gesamt ueber hydraulischer Leistung
N = json.load(open(f"{H}/ergebnis_nachtrag.json"))
fig, ax = plt.subplots(1, 3, figsize=(16, 5.5), sharey=True)
colw = {4: "#7b2d8e", 6: "#1b6ca8", 8: "#2a9d4b", 10: "#e08a00", 15: "#c0392b", 20: "#555555"}
for j, (fn, tit) in enumerate(FALL):
    for x in N["faelle"]:
        if x["fall"] != fn or x["dp_bar"] > 0.5: continue
        ax[j].scatter(x["P_hyd_W"], x["U_gesamt"], s=14 if x["hoehe_mm"] == 5 else 14, marker="o" if x["hoehe_mm"] == 5 else "^", color=colw[x["breite_mm"]], alpha=.6)
    ax[j].axhspan(Z["h_min_W_m2K"], 2000, color="#2a9d4b", alpha=.15); ax[j].axhline(Z["h_min_W_m2K"], color="#2a9d4b")
    ax[j].text(0.02, 0.93, f"Zielband U >= {Z['h_min_W_m2K']} W/(m2K) (K0/K1-Annahme)", transform=ax[j].transAxes, color="#1d6b34", fontsize=9)
    a_ = N["auswahl"][f"{fn}|dT_max_5K"]
    if a_: ax[j].scatter(a_["P_hyd_W"], a_["U_gesamt"], s=140, facecolors="none", edgecolors="k", lw=2); ax[j].annotate(f"Auswahl (dT<=5 K): {a_['breite_mm']} mm x {a_['hoehe_mm']} mm, {a_['durchgaenge']} Durchg., {a_['fuehrung']}", (a_["P_hyd_W"], a_["U_gesamt"]), xytext=(0.03, 0.8), textcoords="axes fraction", fontsize=8, arrowprops=dict(arrowstyle="->"))
    ax[j].set_xscale("log"); ax[j].set_ylim(0, max(x["U_gesamt"] for x in N["faelle"])*1.15); ax[j].set_title(tit); ax[j].set_xlabel("Pumpenleistung hydr. [W], log (dp <= 0,5 bar)")
ax[0].set_ylabel("U_gesamt Zelle-Pad-Blech-Kühlmittel [W/(m²K)], bezogen auf Plattenfläche")
from matplotlib.lines import Line2D
ax[2].legend(handles=[Line2D([], [], marker="o", ls="", color=colw[w], label=f"{w} mm") for w in colw]+[Line2D([], [], marker="o", ls="", color="k", label="Höhe 5 mm"), Line2D([], [], marker="^", ls="", color="k", label="Höhe 3 mm")], fontsize=8, title="Kanalbreite", loc="lower right")
fig.suptitle("K2 Nachtrag: Gesamtwärmedurchgang je Variante (Breite, Höhe, Durchgänge, Führung, ΔT)", fontsize=11)
fig.text(0.5, 0.005, "KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. Quelle: sim/kuehlung/k2_kuehlplatte/ergebnis_nachtrag.json", ha="center", fontsize=8)
fig.tight_layout(rect=(0, .02, 1, .95)); fig.savefig(f"{H}/nachtrag_U_leistung.png", dpi=130); plt.close(fig)
