#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-16). Auftrag C0 (Opus), Vorgang Chemievergleich LFP/NMC.
Dokument ERW-C0 / AUFTRAG C0. Status: Entwurf. Liest NUR eingaben.json (keine eigenen Werte).
Schreibt ergebnis.json, packmasse.png, packmasse_lesehilfe.md. Laufzeit: Sekunden.
Mitte eines Bandes = arithmetisches Mittel (Festlegung des Skripts, im Ergebnis genannt).
"""
import json, math, os, itertools
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

D = os.path.dirname(os.path.abspath(__file__))
E = json.load(open(os.path.join(D, "eingaben.json"), encoding="utf-8"))
an = E["annahmen"]; vg = E["vorgaben"]
M0 = vg["fahrzeugmasse_kg"]["wert"]; R = vg["reichweite_km"]["wert"]
VREF = an["verbrauch_ref_kWh_100km"]["wert"]; MREF = an["referenzmasse_kg"]["wert"]
A0 = an["massenanteil_verbrauch"]["wert"]; ABAND = an["massenanteil_verbrauch"]["band"]
RES = an["reserve"]["wert"]
K0 = an["zelle_zu_pack_masse"]["wert"]; KBAND = an["zelle_zu_pack_masse"]["band"]
U = an["systemspannung_V"]["wert"]; KML = an["km_leben"]["wert"]; SZ = an["sicherheit_zyklen"]["wert"]
L, B, H = an["bauraum_L_B_H_m"]["wert"]; GR = an["grenze_batterieanteil"]["wert"]

def mitte(b): return (b[0] + b[1]) / 2

def verbrauch(m, a): return VREF * (1 + a * (m - MREF) / MREF)

def packmasse(w, k, a, fall):
    """gibt (m_pack, E_brutto, E_netto, V, Gesamtmasse, Schritte)"""
    if fall == "A":
        m = M0; V = verbrauch(m, a)
        En = R * V / 100; Eb = En / (1 - RES)
        return Eb * 1000 / (w * k), Eb, En, V, M0, 0
    mp = 0.0
    for n in range(1, 51):
        m = M0 + mp; V = verbrauch(m, a)
        En = R * V / 100; Eb = En / (1 - RES)
        mp_neu = Eb * 1000 / (w * k)
        if abs(mp_neu - mp) < 0.1:
            m = M0 + mp_neu; V = verbrauch(m, a); En = R * V / 100; Eb = En / (1 - RES)
            return mp_neu, Eb, En, V, m, n
        mp = mp_neu
    raise RuntimeError("konvergiert nicht (50 Schritte)")

def punkt(w, k, a, fall):
    mp, Eb, En, V, m, n = packmasse(w, k, a, fall)
    return dict(w_Wh_kg=w, k=k, a=a, m_pack_kg=mp, E_brutto_kWh=Eb, E_netto_kWh=En,
                verbrauch_kWh_100km=V, gesamtmasse_kg=m, batterieanteil=mp / m, schritte=n)

ERG = {"hinweis": "KI-generiert (Claude Sonnet, 2026-11-16). Aus eingaben.json durch vergleich.py. Mitte = arithmetisches Mittel des Bandes.",
       "eingaben": "eingaben.json", "bauraum_Liter": L * B * H * 1000, "grenze_batterieanteil": GR,
       "zyklenbedarf": KML / R * SZ, "chemie": {}}
bedarf = ERG["zyklenbedarf"]
ks = [KBAND[0], K0, KBAND[1]]
for c, cd in E["chemie"].items():
    wb = cd["zelle_Wh_kg"]["band"]; ws = [wb[0], mitte(wb), wb[1]]
    U_z = cd["nennspannung_V"]["wert"]
    r = {"w_stuetzstellen": ws, "k_stuetzstellen": ks, "nennspannung_V": U_z,
         "reihe_s": math.ceil(U / U_z), "faelle": {}}
    if "band" in cd["nennspannung_V"]:
        r["reihe_s_band_spannung"] = [math.ceil(U / u) for u in cd["nennspannung_V"]["band"]]
    zb = cd["zyklen"]["band"]
    r["zyklen_band"] = zb
    r["zyklen_urteil"] = ("erfüllt" if zb[0] >= bedarf else "unsicher" if zb[1] >= bedarf else "nicht erfüllt")
    for f in ("A", "B"):
        grid = {}
        for iw, w in enumerate(ws):
            for ik, k in enumerate(ks):
                grid[f"w{iw}_k{ik}"] = punkt(w, k, A0, f)
        mit = grid["w1_k1"]
        spanne = [min(g["m_pack_kg"] for g in grid.values()), max(g["m_pack_kg"] for g in grid.values())]
        Eb = mit["E_brutto_kWh"]
        wh_l = Eb * 1000 / (L * B * H * 1000)
        zl = cd["zelle_Wh_L"]
        if zl.get("wert") is None and "band" not in zl:
            bau = "offen (keine Quelle)"
        else:
            zbd = zl["band"]
            bau = (f"Zellband {zbd[0]}–{zbd[1]} Wh/L (Zelle, nicht Pack; allgemein Li-Ion): "
                   + ("Bedarf unter Bandanfang" if wh_l < zbd[0] else "Bedarf im Band" if wh_l <= zbd[1] else "Bedarf über Band"))
        # Empfindlichkeit (je Größe einzeln, andere in der Mitte)
        emp = {}
        emp["k"] = {str(k): packmasse(ws[1], k, A0, f)[0] for k in KBAND}
        emp["w"] = {str(w): packmasse(w, K0, A0, f)[0] for w in (wb[0], wb[1])}
        if f == "B":
            emp["a"] = {str(a): packmasse(ws[1], K0, a, f)[0] for a in ABAND}
        spr = {g: abs(max(v.values()) - min(v.values())) for g, v in emp.items()}
        r["faelle"][f] = {"mitte": mit, "gitter": grid, "m_pack_spanne_kg": spanne,
            "grenze_kg": GR * mit["gesamtmasse_kg"], "anteil_unter_grenze": mit["batterieanteil"] <= GR,
            "anteil_spanne": [min(g["batterieanteil"] for g in grid.values()), max(g["batterieanteil"] for g in grid.values())],
            "pack_Wh_L_noetig": wh_l, "bauraum_urteil": bau,
            "empfindlichkeit_kg": emp, "empfindlichkeit_hub_kg": spr,
            "staerkste_annahme": max(spr, key=spr.get), "schritte": mit["schritte"]}
    ERG["chemie"][c] = r
json.dump(ERG, open(os.path.join(D, "ergebnis.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)

# ---- Bild
C = ERG["chemie"]; farben = {"LFP": "#1f77b4", "NMC": "#d95f02"}
fig, ax = plt.subplots(figsize=(9, 6.2))
x = 0; pos = []; lab = []
for f in ("A", "B"):
    for c in ("LFP", "NMC"):
        d = C[c]["faelle"][f]; mp = d["mitte"]["m_pack_kg"]; lo, hi = d["m_pack_spanne_kg"]
        ax.bar(x, mp, 0.6, color=farben[c], yerr=[[mp - lo], [hi - mp]], capsize=6, ecolor="k")
        ax.text(x + 0.33, mp, f"{mp:.0f}", va="center", fontsize=9)
        g = d["grenze_kg"]
        ax.hlines(g, x - 0.42, x + 0.42, colors="red", linestyles="--", lw=2,
                  label="30 % der Gesamtmasse (Annahme)" if (f, c) == ("A", "LFP") else None)
        ax.text(x - 0.28, g - 10, f"Grenze {g:.0f}", ha="left", va="top", fontsize=8, color="red", zorder=5, bbox=dict(fc="white", ec="red", lw=0.5, pad=1.5))   # geändert 2026-11-16 Sonnet: Beschriftung lesbar, unter der Linie
        pos.append(x); lab.append(f"{c}\nFall {f}"); x += 1
    x += 0.6
ax.set_xticks(pos); ax.set_xticklabels(lab); ax.set_ylabel("Packmasse [kg]")
ax.set_ylim(0, max(d["m_pack_spanne_kg"][1] for c in C for d in C[c]["faelle"].values()) * 1.18)
a_ = C["LFP"]["faelle"]["A"]["mitte"]["E_brutto_kWh"]
bs = [C[c]["faelle"]["B"]["mitte"]["E_brutto_kWh"] for c in C]
ax.set_title(f"Packmasse für {vg['reichweite_km']['wert']} km: Brutto-Energie {a_:.1f} kWh (Fall A), {min(bs):.1f}–{max(bs):.1f} kWh (Fall B)\n"
             "Balken = Mitte des Zellbands, Fehlerbalken = Spanne über Zellband und Packfaktor", fontsize=10)
ax.legend(loc="upper left"); ax.grid(axis="y", alpha=.3)
fig.text(0.01, 0.01, "KI-generiert (Claude Sonnet), Entwurf. Quelle: ergebnis.json. A: 1500 kg inkl. Batterie; B: 1500 kg ohne Batterie.", fontsize=7)
fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(os.path.join(D, "packmasse.png"), dpi=140)

def z(c, f, k="m_pack_kg"): return C[c]["faelle"][f]["mitte"][k]
open(os.path.join(D, "packmasse_lesehilfe.md"), "w", encoding="utf-8").write(
f"""> **KI-generiert** (Claude Sonnet, 2026-11-16), Entwurf.

**Lesehilfe zu packmasse.png.** Jeder Balken zeigt, wie schwer die Batterie sein müsste, damit das Auto {R} km weit fährt (Mitte der Datenlage: LFP {z('LFP','A'):.0f} kg / NMC {z('NMC','A'):.0f} kg in Fall A, {z('LFP','B'):.0f} kg / {z('NMC','B'):.0f} kg in Fall B). Der schwarze Strich am Balken zeigt, wie unsicher das ist: die Zellen können besser oder schlechter sein als angenommen. Die rote gestrichelte Linie ist eine Annahme, keine Vorschrift: die Batterie soll höchstens 30 % der Gesamtmasse wiegen. Liegt der Balken darunter, ist die Annahme eingehalten. Fall A heißt, 1500 kg sind das ganze Auto, Fall B heißt, 1500 kg sind das Auto ohne Batterie.

*KI-generiert, Entwurf, nicht vom Menschen freigegeben.*
""")

# ---- Konsolenausgabe
for c in C:
    for f in "AB":
        d = C[c]["faelle"][f]
        print(c, f, f"m_pack={d['mitte']['m_pack_kg']:.1f} kg, E_brutto={d['mitte']['E_brutto_kWh']:.2f}, Schritte={d['schritte']}, stärkste={d['staerkste_annahme']}")
