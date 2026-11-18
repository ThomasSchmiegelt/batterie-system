#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-16). Auftrag C0b (Opus), Variantenvergleich LFP-Blade / NMC-4680 mit Messwerten.
Dokument AUFTRAG C0b / ERW-C0b. Status: Entwurf. Rechenweg wie sim/chemie/vergleich_lfp_nmc/vergleich.py (Funktionen dort übernommen),
Grundannahmen aus ../vergleich_lfp_nmc/eingaben.json, Zellwerte aus eingaben.json hier. Laufzeit: Sekunden.
Schreibt ergebnis.json, packmasse.png, packmasse_lesehilfe.md. Mitte eines Bandes = arithmetisches Mittel.
"""
import json, math, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

D = os.path.dirname(os.path.abspath(__file__))
E = json.load(open(os.path.join(D, "eingaben.json"), encoding="utf-8"))
G = json.load(open(os.path.join(D, "..", "vergleich_lfp_nmc", "eingaben.json"), encoding="utf-8"))
an = G["annahmen"]; vg = E["vorgaben"]
M0 = vg["fahrzeugmasse_kg"]["wert"]; R = vg["reichweite_km"]["wert"]; USYS = vg["systemspannung_V"]["wert"]
VREF = an["verbrauch_ref_kWh_100km"]["wert"]; MREF = an["referenzmasse_kg"]["wert"]
A0 = an["massenanteil_verbrauch"]["wert"]; ABAND = an["massenanteil_verbrauch"]["band"]
RES = an["reserve"]["wert"]; KML = an["km_leben"]["wert"]; SZ = an["sicherheit_zyklen"]["wert"]
L, B, H = (E.get("bauraum_L_B_H_m") or an["bauraum_L_B_H_m"])["wert"]; GR = an["grenze_batterieanteil"]["wert"]
K0 = E["zelle_zu_pack_masse"]["wert"]; KBAND = E["zelle_zu_pack_masse"]["band"]
V = E["varianten"]; VN = E["volumennutzung_pack"]
KS = [KBAND[0], K0, KBAND[1]]
LFP_W = [160, 185, 210]   # Auftrag: unten, Mitte = Bandmitte, oben; Hauptwert 160 (gemessen)

def verbrauch(m, a): return VREF * (1 + a * (m - MREF) / MREF)
def energie(m, a):
    En = R * verbrauch(m, a) / 100; return En / (1 - RES), En

def lfp(w, k, a, fall, s, U):
    """p = 1; Ah = E_brutto/(s*U)."""
    def calc(m):
        Eb, En = energie(m, a); mp = Eb * 1000 / (w * k)
        return mp, Eb, En
    n = 0
    if fall == "A":
        mp, Eb, En = calc(M0); m = M0
    else:
        mp = 0.0
        for n in range(1, 51):
            mp_neu, Eb, En = calc(M0 + mp)
            if abs(mp_neu - mp) < 0.1: mp = mp_neu; break
            mp = mp_neu
        else: raise RuntimeError("konvergiert nicht (50 Schritte)")
        m = M0 + mp; Eb, En = energie(m, a)
    ah = Eb * 1000 / (s * U)
    return dict(w_Wh_kg=w, k=k, a=a, p=1, zellen=s, E_ist_kWh=Eb, ah_noetig=ah, m_pack_kg=mp, E_brutto_kWh=Eb, E_netto_kWh=En,
                verbrauch_kWh_100km=verbrauch(m, a), gesamtmasse_kg=m, batterieanteil=mp / m, schritte=n)

def nmc(k, a, fall, s, U, ah, mz_g):
    def calc(m):
        Eb, En = energie(m, a); p = math.ceil(Eb * 1000 / (s * U * ah))
        Eist = s * p * U * ah / 1000; mp = s * p * mz_g / 1000 / k
        return mp, Eb, En, p, Eist
    n = 0
    if fall == "A":
        mp, Eb, En, p, Eist = calc(M0); m = M0 + 0
    else:
        mp = 0.0
        for n in range(1, 51):
            mp_neu, Eb, En, p, Eist = calc(M0 + mp)
            if abs(mp_neu - mp) < 0.1: mp = mp_neu; break
            mp = mp_neu
        else: raise RuntimeError("konvergiert nicht (50 Schritte)")
        m = M0 + mp; Eb, En = energie(m, a)
    # Fall A: Gesamtmasse bleibt 1500 (Vorgabe), Batterieanteil mp/1500
    m = M0 if fall == "A" else m
    return dict(w_Wh_kg=Eist * 1000 / (mp * k) if mp else None, k=k, a=a, p=p, zellen=s * p, E_ist_kWh=Eist, ah_noetig=ah,
                m_pack_kg=mp, E_brutto_kWh=Eb, E_netto_kWh=En, verbrauch_kWh_100km=verbrauch(m, a),
                gesamtmasse_kg=m, batterieanteil=mp / m, schritte=n, zellmasse_kg=s * p * mz_g / 1000)

def bau(wh_l, zelle_wh_l, vn):
    """Urteil je Volumennutzung: Verfügbar = Zelle_Wh_L*vn gegen nötig. knapp = innerhalb ±2 % des Bedarfs."""
    v = zelle_wh_l * vn; d = v / wh_l - 1
    return dict(volumennutzung=vn, verfuegbar_Wh_L=v, abweichung=d, urteil="knapp (±2 %)" if abs(d) <= 0.02 else "erfüllt" if d > 0 else "nicht erfüllt")

bedarf_z = KML / R * SZ
ERG = {"hinweis": "KI-generiert (Claude Sonnet, 2026-11-16). Aus eingaben.json (hier und ../vergleich_lfp_nmc) durch varianten.py. Mitte = arithmetisches Mittel.",
       "bauraum_Liter": L * B * H * 1000, "grenze_batterieanteil": GR, "zyklenbedarf": bedarf_z, "systemspannung_V": USYS, "varianten": {}}
for c, cd in V.items():
    U = cd["nennspannung_V"]["wert"]; s = math.ceil(USYS / U)
    zb = cd["zyklen"]["band"]
    r = {"nennspannung_V": U, "reihe_s": s, "zyklen_band": zb,
         "zyklen_urteil": "erfüllt" if zb[0] >= bedarf_z else "unsicher" if zb[1] >= bedarf_z else "nicht erfüllt", "faelle": {}}
    for f in ("A", "B"):
        if c == "LFP":
            r["w_stuetzstellen"] = LFP_W
            grid = {f"w{w}_k{k}": lfp(w, k, A0, f, s, U) for w in LFP_W for k in KS}
            mit = grid[f"w185_k{K0}"]; haupt = grid[f"w160_k{K0}"]
            emp = {"k": {str(k): lfp(185, k, A0, f, s, U)["m_pack_kg"] for k in (KS[0], KS[2])},
                   "w": {str(w): lfp(w, K0, A0, f, s, U)["m_pack_kg"] for w in (160, 210)}}
            if f == "B": emp["a"] = {str(a): lfp(185, K0, a, f, s, U)["m_pack_kg"] for a in ABAND}
        else:
            ah = cd["kapazitaet_Ah"]["wert"]; mz = cd["zellmasse_g"]["wert"]
            grid = {f"k{k}": nmc(k, A0, f, s, U, ah, mz) for k in KS}
            mit = grid[f"k{K0}"]; haupt = mit
            emp = {"k": {str(k): nmc(k, A0, f, s, U, ah, mz)["m_pack_kg"] for k in (KS[0], KS[2])}}
            if f == "B": emp["a"] = {str(a): nmc(K0, a, f, s, U, ah, mz)["m_pack_kg"] for a in ABAND}
        spr = {g: abs(max(v.values()) - min(v.values())) for g, v in emp.items()}
        spanne = [min(g["m_pack_kg"] for g in grid.values()), max(g["m_pack_kg"] for g in grid.values())]
        wh_l = mit["E_brutto_kWh"] * 1000 / (L * B * H * 1000)
        if c == "LFP":
            bz = [bau(wh_l, cd["zelle_Wh_L"]["wert"], VN["LFP"]["wert"])]
        else:
            bz = [bau(wh_l, cd["zelle_Wh_L"]["wert"], vn) for vn in VN["NMC"]["band"]]
        urteile = {b["urteil"] for b in bz}
        if c == "LFP":   # Zusatz (Opus 2026-11-17): Kennwerte für den Hauptwert w=160, gleicher Code wie für die Bandmitte
            haupt = dict(haupt)
            wh_l_h = haupt["E_brutto_kWh"] * 1000 / (L * B * H * 1000)
            bz_h = [bau(wh_l_h, cd["zelle_Wh_L"]["wert"], VN["LFP"]["wert"])]
            haupt.update(pack_Wh_L_noetig=wh_l_h, bauraum=bz_h, bauraum_urteil=bz_h[0]["urteil"])
            if f == "B":
                ea = {str(a): lfp(160, K0, a, f, s, U)["m_pack_kg"] for a in ABAND}
                haupt.update(empfindlichkeit_a_kg=ea, empfindlichkeit_a_hub_kg=abs(max(ea.values()) - min(ea.values())))
        r["faelle"][f] = {"mitte": mit, "hauptwert": haupt, "gitter": grid, "m_pack_spanne_kg": spanne,
            "grenze_kg": GR * mit["gesamtmasse_kg"], "anteil_unter_grenze": mit["batterieanteil"] <= GR,
            "anteil_spanne": [min(g["batterieanteil"] for g in grid.values()), max(g["batterieanteil"] for g in grid.values())],
            "pack_Wh_L_noetig": wh_l, "bauraum": bz, "bauraum_urteil": urteile.pop() if len(urteile) == 1 else "unsicher (Band: " + " / ".join(b["urteil"] for b in bz) + ")",
            "empfindlichkeit_kg": emp, "empfindlichkeit_hub_kg": spr, "staerkste_annahme": max(spr, key=spr.get), "schritte": mit["schritte"]}
    ERG["varianten"][c] = r
json.dump(ERG, open(os.path.join(D, "ergebnis.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)

# ---- Bild
C = ERG["varianten"]; farben = {"LFP": "#1f77b4", "NMC": "#d95f02"}
fig, ax = plt.subplots(figsize=(9.5, 6.4))
x = 0; pos = []; lab = []; first = True
for f in ("A", "B"):
    for c in ("LFP", "NMC"):
        d = C[c]["faelle"][f]; mp = d["hauptwert"]["m_pack_kg"]
        klo = min(g["m_pack_kg"] for g in d["gitter"].values() if g["w_Wh_kg"] == d["hauptwert"]["w_Wh_kg"]) if c == "LFP" else d["m_pack_spanne_kg"][0]
        khi = max(g["m_pack_kg"] for g in d["gitter"].values() if g["w_Wh_kg"] == d["hauptwert"]["w_Wh_kg"]) if c == "LFP" else d["m_pack_spanne_kg"][1]
        ax.bar(x, mp, 0.6, color=farben[c], yerr=[[mp - klo], [khi - mp]], capsize=6, ecolor="k",
               label="Fehlerbalken: Packfaktor k 0,65–0,85" if first else None); first = False
        ax.text(x + 0.33, mp, f"{mp:.0f}", va="center", fontsize=9)
        if c == "LFP":
            for w in (185, 210):
                v = d["gitter"][f"w{w}_k{K0}"]["m_pack_kg"]
                ax.plot([x - 0.3, x + 0.3], [v, v], color="k", lw=1.5, ls=":")
                ax.text(x - 0.33, v, f"{w}", ha="right", va="center", fontsize=8)
        g = d["grenze_kg"]
        ax.hlines(g, x - 0.42, x + 0.42, colors="red", linestyles="--", lw=2,
                  label="30 % der Gesamtmasse (Annahme)" if (f, c) == ("A", "LFP") else None)
        ax.text(x + 0.0, g + 6, f"Grenze {g:.0f}", ha="center", va="bottom", fontsize=8, color="red", bbox=dict(fc="white", ec="red", lw=0.5, pad=1.2), zorder=6)
        pos.append(x); lab.append(f"{c}\nFall {f}"); x += 1
    x += 0.6
ax.set_xticks(pos); ax.set_xticklabels(lab); ax.set_ylabel("Packmasse [kg]")
ax.set_ylim(0, max(g["m_pack_kg"] for c in C for d in C[c]["faelle"].values() for g in d["gitter"].values()) * 1.2)
ea = C["LFP"]["faelle"]["A"]["hauptwert"]["E_brutto_kWh"]
ax.set_title(f"Packmasse für {R} km bei {USYS:.0f} V: Brutto-Energie {ea:.1f} kWh (Fall A)\n"
             f"LFP: Balken = gemessen {LFP_W[0]} Wh/kg, gepunktet = Bandenden {LFP_W[1]}/{LFP_W[2]}; NMC 4680: gemessen", fontsize=10)
ax.legend(loc="upper left", fontsize=8); ax.grid(axis="y", alpha=.3)
fig.text(0.01, 0.01, "KI-generiert (Claude Sonnet), Entwurf. Quelle: ergebnis.json. A: 1500 kg inkl. Batterie; B: 1500 kg ohne Batterie.", fontsize=7)
fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(os.path.join(D, "packmasse.png"), dpi=140)

def z(c, f, k="m_pack_kg", key="hauptwert"): return C[c]["faelle"][f][key][k]
open(os.path.join(D, "packmasse_lesehilfe.md"), "w", encoding="utf-8").write(
f"""> **KI-generiert** (Claude Sonnet, 2026-11-16), Entwurf.

**Lesehilfe zu packmasse.png.** Jeder Balken zeigt, wie schwer die Batterie sein müsste, damit das Auto {R} km weit fährt, wenn man die gemessenen Zellwerte nimmt (LFP {z('LFP','A'):.0f} kg / NMC {z('NMC','A'):.0f} kg in Fall A, {z('LFP','B'):.0f} kg / {z('NMC','B'):.0f} kg in Fall B). Beim LFP ist der Balken der gemessene Zellwert {LFP_W[0]} Wh/kg; die gepunkteten Striche zeigen die Bandenden {LFP_W[1]} und {LFP_W[2]} Wh/kg (Herstellerangaben). Der schwarze Strich am Balken zeigt die Unsicherheit beim Anteil der Zellen am Pack (65 bis 85 %). Die rote gestrichelte Linie ist eine Annahme, keine Vorschrift: die Batterie soll höchstens 30 % der Gesamtmasse wiegen. Liegt der Balken darunter, ist die Annahme eingehalten. Fall A heißt, 1500 kg sind das ganze Auto, Fall B heißt, 1500 kg sind das Auto ohne Batterie.

*KI-generiert, Entwurf, nicht vom Menschen freigegeben.*
""")
for c in C:
    for f in "AB":
        d = C[c]["faelle"][f]; m = d["mitte"]
        print(c, f, f"m_pack={m['m_pack_kg']:.1f} kg, E_brutto={m['E_brutto_kWh']:.2f}, p={m['p']}, Zellen={m['zellen']}, E_ist={m['E_ist_kWh']:.2f}, Schritte={d['schritte']}, Bauraum={d['bauraum_urteil']}")
