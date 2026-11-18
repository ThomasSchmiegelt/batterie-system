#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. Auftrag BILD-1.
Liest nur ergebnis.json (varianten_lfp_nmc/ und vergleich_lfp_nmc/), rechnet nichts neu.
Erzeugt bauraum.png, empfindlichkeit.png, kriterien.png. Zahlen in Titeln/Beschriftung aus dem Ergebnis."""
import json, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

HIER = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HIER, "ergebnis.json")))
V = json.load(open(os.path.join(HIER, "..", "vergleich_lfp_nmc", "ergebnis.json")))  # gelesen, Vergleichswerte siehe Lesehilfe
FUSS = "KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. Quelle: sim/chemie/varianten_lfp_nmc/ergebnis.json"
GRUEN, GELB, ROT, GRAU = "#2e8b57", "#e6b800", "#c0392b", "#bbbbbb"
FARBE = {"erfüllt": GRUEN, "knapp": GELB, "nicht erfüllt": ROT, "unsicher": GRAU}

def farbe(urteil):
    for k in ("nicht erfüllt", "knapp", "erfüllt", "unsicher"):
        if urteil.startswith(k):
            return FARBE[k]
    return GRAU

def fuss(fig):
    fig.text(0.01, 0.005, FUSS, fontsize=7, color="#555")

# ---------- 1. Bauraum ----------
fig, axs = plt.subplots(1, 2, figsize=(11, 5.6), sharey=True)
for ax, fall in zip(axs, "AB"):
    for i, var in enumerate(("LFP", "NMC")):
        f = D["varianten"][var]["faelle"][fall]
        br = f["hauptwert"].get("bauraum", f["bauraum"])
        noetig = f["hauptwert"].get("pack_Wh_L_noetig", f["pack_Wh_L_noetig"])
        # untere Grenze (schlechteste Volumennutzung) als Balken, Band bis beste
        b0 = br[0]
        ax.bar(i, b0["verfuegbar_Wh_L"], 0.55, color=farbe(b0["urteil"]), edgecolor="k")
        ax.text(i, b0["verfuegbar_Wh_L"] / 2, f'{b0["verfuegbar_Wh_L"]:.0f}\n({b0["volumennutzung"]*100:.0f} % Nutzung)\n{b0["urteil"]}',
                ha="center", va="center", color="white", fontsize=8, fontweight="bold")
        if len(br) > 1:
            b1 = br[-1]
            ax.bar(i, b1["verfuegbar_Wh_L"] - b0["verfuegbar_Wh_L"], 0.55, bottom=b0["verfuegbar_Wh_L"],
                   color=farbe(b1["urteil"]), alpha=0.35, edgecolor="k", hatch="//")
            ax.text(i, b1["verfuegbar_Wh_L"] + 6, f'bis {b1["verfuegbar_Wh_L"]:.0f} ({b1["volumennutzung"]*100:.0f} %)', ha="center", fontsize=8)
        ax.hlines(noetig, i - 0.42, i + 0.42, colors="k", linestyles="--", linewidth=2)
        ax.text(i + 0.44, noetig, f"nötig\n{noetig:.0f}", va="center", fontsize=8)
    ax.set_xticks([0, 1]); ax.set_xticklabels(["LFP", "NMC"])
    ax.set_xlim(-0.6, 1.85)
    ax.set_title(f"Fall {fall}")
    ax.set_xlabel("Variante")
axs[0].set_ylabel("Pack-Energiedichte [Wh/L]")
fig.suptitle(f'Bauraum {D["bauraum_Liter"]} L: nötige gegen verfügbare Pack-Energiedichte\n'
             "Zielbereich: gestrichelte Linie = nötig für 400 km im Bauraum (Rechnung, Fall A/B); "
             "NMC-Band 40-60 % Volumennutzung = Annahme", fontsize=10)
fig.legend(handles=[Patch(color=GRUEN, label="passt"), Patch(color=GELB, label="knapp (±2 %)"),
                    Patch(color=ROT, label="passt nicht"), Patch(facecolor="grey", alpha=.35, hatch="//", label="Band bis 60 % (NMC)")],
           loc="lower center", ncol=4, fontsize=8, bbox_to_anchor=(0.5, 0.03))
fig.tight_layout(rect=(0, 0.1, 1, 0.92)); fuss(fig)
fig.savefig(os.path.join(HIER, "bauraum.png"), dpi=140); plt.close(fig)

# ---------- 2. Empfindlichkeit (Tornado) ----------
NAMEN = {"k": "Packfaktor k (0,65-0,85)", "w": "Zellwert 160 → 210 Wh/kg", "a": "Massenanteil Verbrauch (0,3-0,7)"}
fig, axs = plt.subplots(1, 2, figsize=(12, 4.8))
for ax, var in zip(axs, ("LFP", "NMC")):
    f = D["varianten"][var]["faelle"]["B"]
    h = f["hauptwert"]
    mitte = h["m_pack_kg"]            # Hauptwert (LFP 160 Wh/kg gemessen; NMC gemessen)
    gr = D["grenze_batterieanteil"] * h["gesamtmasse_kg"]   # 30 % der Gesamtmasse des Hauptwert-Falls
    if var == "LFP":
        emp = {"k": {"0.65": f["gitter"]["w160_k0.65"]["m_pack_kg"], "0.85": f["gitter"]["w160_k0.85"]["m_pack_kg"]},
               "w": {"160": f["empfindlichkeit_kg"]["w"]["160"], "210": f["empfindlichkeit_kg"]["w"]["210"]},
               "a": h["empfindlichkeit_a_kg"]}
    else:
        emp = {"k": f["empfindlichkeit_kg"]["k"]}
    hub = {k: max(v.values()) - min(v.values()) for k, v in emp.items()}
    f = dict(f, empfindlichkeit_hub_kg=hub)
    keys = sorted(emp, key=lambda k: hub[k])
    bm = f["mitte"]["m_pack_kg"]
    for j, k in enumerate(keys):
        vs = emp[k]; lo, hi = min(vs.values()), max(vs.values())
        ax.barh(j, hi - lo, left=lo, color="#4a78b5", edgecolor="k", height=0.5)
        ax.text(lo, j + 0.33, f"{lo:.0f}", ha="right", fontsize=8, va="center")
        ax.text(hi, j + 0.33, f"{hi:.0f}", ha="left", fontsize=8, va="center", bbox=dict(fc="white", ec="none", pad=0.5))
    ax.set_yticks(range(len(keys))); ax.set_yticklabels([NAMEN[k] + f'\nHub {f["empfindlichkeit_hub_kg"][k]:.0f} kg' for k in keys], fontsize=8)
    ax.axvline(mitte, color="k", linewidth=1.2); ax.text(mitte, len(keys) - 0.35, f"Hauptwert {mitte:.0f}", ha="right" if mitte > gr else "left", fontsize=8)
    ax.axvline(gr, color="red", linestyle="--", linewidth=2)
    ax.text(gr, -0.62, f"30 % der Gesamtmasse = {gr:.0f} kg (Annahme)", color="red", ha="right" if mitte > gr else "right", fontsize=8)
    xs = [x for v in emp.values() for x in v.values()] + [gr, mitte]
    if var == "LFP":
        ax.text(0.99, 0.02, f"Bandmitte 185 Wh/kg: {bm:.0f} kg (nur Zusatz)", transform=ax.transAxes, ha="right", va="bottom", fontsize=7)
    ax.set_xlim(min(xs) - 80, max(xs) + 80); ax.set_ylim(-0.8, len(keys) - 0.2)
    ax.set_title(f"{var}, Fall B"); ax.set_xlabel("Pack-Masse [kg]")
fig.suptitle("Empfindlichkeit der Pack-Masse (Fall B): Hub je Annahme um den Hauptwert (LFP 160 Wh/kg gemessen)\n"
             "Zielbereich: rote Linie = 30 % der Gesamtmasse (Annahme, je Variante).\nNMC: Zellwert gemessen, kein Hub; NMC-Massenanteil-Hub 0, deshalb nicht gezeigt",
             fontsize=9)
fig.tight_layout(rect=(0, 0.03, 1, 0.9)); fuss(fig)
fig.savefig(os.path.join(HIER, "empfindlichkeit.png"), dpi=140); plt.close(fig)

# ---------- 3. Kriterien ----------
zeilen = ["Masse A", "Masse B", "Bauraum A", "Bauraum B", "Zyklen", "Zellzahl"]
zellen = {}
for var in ("LFP", "NMC"):
    x = D["varianten"][var]
    for fall in "AB":
        f = x["faelle"][fall]
        m = f["hauptwert"]; mb = f["mitte"]
        u = "erfüllt" if f["anteil_unter_grenze"] else "nicht erfüllt"
        zusatz = f'\nBandmitte 185: {mb["m_pack_kg"]:.0f} kg' if var == "LFP" else ""
        zellen[(f"Masse {fall}", var)] = (f'{m["m_pack_kg"]:.0f} kg (Hauptwert, Anteil {m["batterieanteil"]*100:.0f} %)\nSpanne {f["m_pack_spanne_kg"][0]:.0f}-{f["m_pack_spanne_kg"][1]:.0f}{zusatz}\nGrenze 30 % der Gesamtmasse', u)
        b = f["hauptwert"].get("bauraum", f["bauraum"])[0]
        nt = f["hauptwert"].get("pack_Wh_L_noetig", f["pack_Wh_L_noetig"])
        zellen[(f"Bauraum {fall}", var)] = (f'verfügbar {b["verfuegbar_Wh_L"]:.0f} / nötig {nt:.0f} Wh/L\nAbw. {b["abweichung"]*100:+.1f} % ({b["volumennutzung"]*100:.0f} % Nutzung)', f["hauptwert"].get("bauraum_urteil", f["bauraum_urteil"]))
    zb = x["zyklen_band"]
    zellen[("Zyklen", var)] = (f'{zb[0]}-{zb[1]} (Bedarf {D["zyklenbedarf"]:.0f})', x["zyklen_urteil"])
    za, zbf = x["faelle"]["A"]["mitte"]["zellen"], x["faelle"]["B"]["mitte"]["zellen"]
    zellen[("Zellzahl", var)] = (f"A {za}, B {zbf}\n(Reihe {x['reihe_s']} in Serie)", "unsicher")
fig, ax = plt.subplots(figsize=(10, 8.2))
ax.set_xlim(0, 3); ax.set_ylim(0, len(zeilen) + 1); ax.axis("off")
for c, name in enumerate(("LFP", "NMC")):
    ax.text(1.5 + c * 1.0 + 0.0 - 0.0, len(zeilen) + 0.5, name, ha="center", va="center", fontsize=12, fontweight="bold")
for r, z in enumerate(zeilen):
    y = len(zeilen) - 1 - r
    ax.text(0.45, y + 0.5, z, ha="right", va="center", fontsize=10, fontweight="bold")
    for c, var in enumerate(("LFP", "NMC")):
        txt, u = zellen[(z, var)]
        if z == "Zellzahl":
            fc = "#dddddd"; u = "kein Urteil"
        else:
            fc = farbe(u)
        ax.add_patch(plt.Rectangle((1.0 + c * 1.0 + 0.5 - 0.5 + 0.0, y + 0.05), 0.95, 0.9, facecolor=fc, edgecolor="k", alpha=0.85))
        ax.text(1.475 + c * 1.0 + 0.0, y + 0.5, f"{u}\n{txt}", ha="center", va="center", fontsize=8,
                color="white" if fc in (GRUEN, ROT) else "black")
ax.set_xlim(-0.3, 3.1)
fig.suptitle("Bewertung der Varianten nach Kriterien (ohne Gewichtung, ohne Gesamtnote)\n"
             "Zielbereich je Zeile: Masse = Batterie ≤ 30 % Gesamtmasse (Annahme); Bauraum = verfügbar ≥ nötig (±2 % knapp);\nZyklen ≥ Bedarf; Zellzahl ohne Grenze", fontsize=9)
fig.legend(handles=[Patch(color=GRUEN, label="erfüllt"), Patch(color=GELB, label="knapp"), Patch(color=ROT, label="nicht erfüllt"),
                    Patch(color=GRAU, label="unsicher / kein Urteil")], loc="lower center", ncol=4, fontsize=8, bbox_to_anchor=(0.5, 0.03))
fig.tight_layout(rect=(0, 0.08, 1, 0.92)); fuss(fig)
fig.savefig(os.path.join(HIER, "kriterien.png"), dpi=140); plt.close(fig)
print("ok")
