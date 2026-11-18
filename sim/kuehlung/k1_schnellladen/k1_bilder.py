#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. Auftrag K1. Bilder aus ergebnis.json und eingaben.json (Zahlen in Titeln aus dem Ergebnis)."""
import json, os, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
HIER = os.path.dirname(os.path.abspath(__file__))
E = json.load(open(f"{HIER}/eingaben.json")); R = json.load(open(f"{HIER}/ergebnis.json")); F = R["faelle"]
ZT, ZD = R["ziel_T_max_C"], R["ziel_dT_K"]
KURZ = {"P0": "konstant 2,1C, 20 min", "P1": "Stufen 3C/2C/1,38C, 20 min", "P2": "Puls 4,2C 30 s an/aus, 20 min", "P3": "konstant 1,68C, 25 min", "P4": "konstant 1,4C, 30 min"}
COL = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#D55E00", "#56B4E9", "#7F7F7F", "#000000", "#A6761D"]
KAI = "KI-generiert (Claude Sonnet), Entwurf, nicht vom Menschen freigegeben. Quelle: sim/kuehlung/k1_schnellladen/ergebnis.json"
def fuss(fig): fig.text(0.01, 0.005, KAI, fontsize=7, color="#555")

def profil_kurve(p):
    P = E["profile"][p]
    import k1_rechnen as RC
    T_end, dt, st = RC.profil_tabelle(p, 1, 1, None, None)
    t, C = [], []
    for a, b, c in st: t += [a, b]; C += [c, c]
    soc = [10.0]; ts = [0.0]
    for a, b, c in st: ts += [a, b]; soc += [soc[-1], soc[-1] + c * (b - a) / 3600 * 100]
    return t, C, ts, soc, P["name"]

def bild_profile():
    fig, ax = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    for i, p in enumerate(E["profile"]):
        t, C, ts, soc, nm = profil_kurve(p)
        ax[0].plot(np.array(t) / 60, C, color=COL[i], lw=1.4, label=f"{p}: {nm}")
        ax[1].plot(np.array(ts) / 60, soc, color=COL[i], lw=1.8, label=p)
    ax[0].set_ylim(-0.2, 6.0); ax[0].set_ylabel("Ladestrom in C (1C = Zellkapazität pro Stunde)"); ax[0].legend(fontsize=7.5, loc="upper right", ncol=2); ax[0].grid(alpha=.3)
    ax[0].set_title("Ladeprofile P0 bis P4 (alle laden von 10 % auf 80 %)")
    ax[1].axhline(80, color="#009E73", ls="--"); ax[1].text(0.3, 81, "Ziel 80 % Ladezustand", color="#009E73", fontsize=8)
    ax[1].axhline(10, color="#777", ls=":"); ax[1].text(0.3, 11, "Start 10 %", color="#555", fontsize=8)
    ax[1].set_ylabel("Ladezustand in %"); ax[1].set_xlabel("Zeit in min"); ax[1].legend(fontsize=8, ncol=5, loc="lower right"); ax[1].grid(alpha=.3)
    fuss(fig); fig.tight_layout(rect=(0, .02, 1, 1)); fig.savefig(f"{HIER}/profile.png", dpi=130); plt.close(fig)

def verlaufbild(v, namen, titel, datei, stil=None):
    fig, ax = plt.subplots(2, 1, figsize=(10, 8.4), sharex=True)
    for i, (n, lab) in enumerate(namen):
        r = F.get(f"{v}_{n}")
        if r is None: continue
        t = np.array(r["t_s"]) / 60; ls = "--" if "P0" not in n else "-"
        ax[0].plot(t, r["T_max_t_C"], color=COL[i % len(COL)], ls=ls if i < len(COL) else ":", lw=1.6, label=f"{lab} (Spitze {r['T_max_Spitze_C']:.1f} °C)")
        ax[1].plot(t, r["dT_kern_t_K"], color=COL[i % len(COL)], ls=ls if i < len(COL) else ":", lw=1.2, label=f"{lab} (Spitze {r['dT_Spitze_K']:.1f} K)")
    ymax = ax[0].get_ylim()[1]; ymin = min(min(F[f"{v}_{n}"]["T_max_t_C"]) for n, _ in namen if f"{v}_{n}" in F)
    ax[0].axhspan(0, ZT, color="#009E73", alpha=.10); ax[0].set_ylim(bottom=ymin - 2); ax[0].axhline(ZT, color="#009E73", lw=1.8)
    ax[0].text(t[-1] if False else max(max(F[f"{v}_{n}"]["t_s"]) for n, _ in namen if f"{v}_{n}" in F) / 60, ZT + 0.4, f"Vorgabe T_max ≤ {ZT:g} °C (REQ-P09, Annahme); grün = Zielband", color="#007A5A", fontsize=8.5, ha="right", bbox=dict(fc="white", ec="none", alpha=.8, pad=1))
    ax[0].set_ylim(top=max(ymax, ZT + 4)); ax[0].set_ylabel("T_max in der Zelle in °C"); ax[0].grid(alpha=.3); ax[0].legend(fontsize=7.5, loc="upper left", bbox_to_anchor=(0.0, 0.93))
    ax[1].axhspan(0, ZD, color="#009E73", alpha=.10); ax[1].axhline(ZD, color="#009E73", lw=1.8)
    ax[1].text(max(max(F[f"{v}_{n}"]["t_s"]) for n, _ in namen if f"{v}_{n}" in F) / 60, ZD + 0.3, f"Vorgabe Spreizung ≤ {ZD:g} K (REQ-P09, Annahme); grün = Zielband", color="#007A5A", fontsize=8.5, ha="right", bbox=dict(fc="white", ec="none", alpha=.8, pad=1))
    ax[1].set_ylabel("Spreizung ΔT im Zellkern in K"); ax[1].set_xlabel("Zeit in min"); ax[1].grid(alpha=.3); ax[1].legend(fontsize=7.5, loc="upper left", bbox_to_anchor=(0.0, 0.88)); ax[1].set_ylim(bottom=0)
    ax[0].set_title(titel); fuss(fig); fig.tight_layout(rect=(0, .02, 1, 1)); fig.savefig(f"{HIER}/{datei}", dpi=130); plt.close(fig)

def landkarte():
    # Reihenfolge: Profile, Kuehlfaelle P0, Kombinationen
    prof = [p for p in E["profile"]]; kuehl = [f"P0_{k}" for k in E["faelle"]["Kuehlfaelle_mit_P0"]]
    komb = [f"{p}_{k}" for p, k, _ in E["faelle"]["Kombinationen"]] + [f"{p}_{k}" for p, k in E["faelle"].get("K1b", [])] + [n.split("_", 1)[1] for n in E.get("K1c", {}).get("faelle", {})]
    zeilen = prof + kuehl + komb
    KK = {"Kh1000": "Boden h 1000", "Kh2000": "Boden h 2000", "K3": "beidseitig h 500", "K3h1000": "beidseitig h 1000", "V15": "Start 15 °C"}
    beschr = {p: f"{p} {KURZ[p]}" for p in prof}
    for k in E["faelle"]["Kuehlfaelle_mit_P0"]: beschr[f"P0_{k}"] = f"P0 + {KK[k]}"
    for p, k, _ in E["faelle"]["Kombinationen"]: beschr[f"{p}_{k}"] = f"{p} + {KK[k]} (Kombination)"
    for p, k in E["faelle"].get("K1b", []):
        kc = E["kuehlung"][k]; beschr[f"{p}_{k}"] = f"{p} + K1b oben über Verbinder/Pad: φ {kc['phi']:g}, k_pad {kc['k_pad']:g} (h_eff {kc['h_rand']['Oben']:.0f})"
    for n, d in E.get("K1c", {}).get("faelle", {}).items():
        beschr[n.split("_", 1)[1]] = {"gesamt": "K1c NMC K3b mit C2-Q(t) 1,5C, Modell gesamt", "idu": "K1c NMC K3b mit C2-Q(t) 1,5C, I·ΔU (konservativ)", "R": "K1c LFP P0 K3 mit R 1,28 mΩ (C2/Test#5)"}[d["quelle"]]
    fig, ax = plt.subplots(figsize=(12.5, 0.55 * len(zeilen) + 3.2)); ax.set_xlim(0, 6); ax.set_ylim(len(zeilen), -1.3); ax.axis("off")
    kopf = ["LFP T_max-Spitze", "LFP ΔT-Spitze", "NMC T_max-Spitze", "NMC ΔT-Spitze"]
    gr, ro, ge, gw = "#8fd19e", "#f2a0a0", "#f5dc8a", "#e8e8e8"
    x0 = 2.2; bw = (6 - x0 - 1.0) / 4
    for j, k in enumerate(kopf): ax.text(x0 + bw * (j + .5), -0.75, k, ha="center", va="center", fontsize=8.5, fontweight="bold")
    ax.text(6 - .5, -0.75, "Ampel\nbeide Vorgaben", ha="center", va="center", fontsize=8.5, fontweight="bold")
    ax.text(0.05, -0.75, "Fall (Start 25 °C, h 500 wenn nicht anders)", va="center", fontsize=8.5, fontweight="bold")
    def fallname(v, z):
        if z in prof: return f"{v}_{z}"
        return f"{v}_{z}"
    for i, z in enumerate(zeilen):
        ax.text(0.05, i + .5, beschr[z], va="center", fontsize=8.3)
        amp = {}
        for vi, v in enumerate(("LFP", "NMC")):
            r = F.get(fallname(v, z))
            for k, (key, lim, fm) in enumerate((("T_max_Spitze_C", ZT, "{:.1f} °C"), ("dT_Spitze_K", ZD, "{:.1f} K"))):
                j = vi * 2 + k; x = x0 + bw * j
                if r is None: ax.add_patch(plt.Rectangle((x, i + .04), bw - .04, .92, color=gw)); ax.text(x + bw / 2, i + .5, "nicht gerechnet", ha="center", va="center", fontsize=7, color="#666"); continue
                ok = r[key] <= lim; amp.setdefault(v, []).append(ok)
                ax.add_patch(plt.Rectangle((x, i + .04), bw - .04, .92, color=gr if ok else ro)); ax.text(x + bw / 2, i + .5, fm.format(r[key]), ha="center", va="center", fontsize=9)
        ax.text(0, 0, "")
        xa = 6 - 1.0
        for vi, v in enumerate(("LFP", "NMC")):
            if v not in amp: continue
            n = sum(amp[v]); col = gr if n == 2 else (ge if n == 1 else ro)
            ax.add_patch(plt.Rectangle((xa + vi * .5, i + .04), .46, .92, color=col)); ax.text(xa + vi * .5 + .23, i + .5, v, ha="center", va="center", fontsize=8)
    ax.set_title(f"Landkarte Schnellladen: Spitzenwerte je Fall gegen Vorgabe REQ-P09 (T_max ≤ {ZT:g} °C, ΔT ≤ {ZD:g} K)", fontsize=11, loc="left")
    leg = [Patch(color=gr, label="Vorgabe eingehalten"), Patch(color=ro, label="Vorgabe verfehlt"), Patch(color=ge, label="Ampel gelb: nur eine der beiden Vorgaben erfüllt"), Patch(color=gw, label="nicht gerechnet")]
    ax.legend(handles=leg, loc="lower center", bbox_to_anchor=(0.5, -0.12), ncol=4, fontsize=8, frameon=False)
    fuss(fig); fig.tight_layout(rect=(0, .02, 1, 1)); fig.savefig(f"{HIER}/landkarte.png", dpi=130); plt.close(fig)

if __name__ == "__main__":
    bild_profile()
    for v in ("LFP", "NMC"):
        verlaufbild(v, [(p, f"{p} {KURZ[p]}") for p in E["profile"]], f"{v}: Temperatur und Spreizung je Ladeprofil (Kühlung Boden, h 500, Start 25 °C)", f"verlauf_profile_{v}.png")
        k = [("P0", "P0 (Basis K1 h 500)")] + [(f"P0_{x}", f"P0 + {x}") for x in E["faelle"]["Kuehlfaelle_mit_P0"]] + [(f"{p}_{x}", f"{p} + {x}") for p, x, vs in E["faelle"]["Kombinationen"] if v in vs] + ([(f"{p}_{x}", f"{p} + {x}") for p, x in E["faelle"].get("K1b", []) if p == "P0"] if v == "NMC" else [])
        verlaufbild(v, k, f"{v}: Temperatur und Spreizung je Kühlfall (Profil P0 wenn nicht anders; gestrichelt = Änderung/Kombination)", f"verlauf_kuehlung_{v}.png")
    landkarte(); print("Bilder fertig")
