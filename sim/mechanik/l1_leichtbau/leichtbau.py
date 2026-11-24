#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-24), Entwurf. Auftrag L1 (ERWARTUNG.md ERW-L1, Opus). Nur Rechnung, kein CAD.
Eingang (nur lesen): cad/pack/entwurf/ergebnis_<V>_e2d_e3c.json, parameter_<V>.json.
Hebelspannen H1..H7 stehen als 'Schätzung Opus' in ERWARTUNG.md und werden hier als Eingabe übernommen (keine eigenen Annahmen).
Ausgabe: ergebnis.json, wasserfall_<V>.png, wasserfall_lesehilfe.md"""
import json, os, math
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")); D = f"{R}/cad/pack/entwurf"; O = os.path.dirname(os.path.abspath(__file__))
ZIEL = {"LFP": 528.0, "NMC": 370.0}   # REQ-P07, docs/01_lastenheft.md Zeile REQ-P07
# Schätzung Opus (ERWARTUNG.md, Tabelle Hebel): (von, bis) in kg Einsparung; gruppe = Bezug
HEBEL = {"H1": ("Kühlplatte dünner / Strangpressprofil", "Kuehlplatte", (15, 25)), "H2": ("Boden + Kühlplatte zusammenlegen", "Boden", (10, 20)),
         "H3": ("Unterfahrschutz dünner / Verbund", "Unterfahrschutz", (5, 10)), "H4": ("Deckel aus Verbund", "Deckel", (5, 8)),
         "H5": ("Pad nur unter den Zellen / dünner", "Pad", (4, 7)), "H6": ("Seitenrahmen Kammerprofil", "Seitenrahmen", (5, 10)),
         "H7": ("NMC Verguss nur oben", "Verguss", (5, 8))}
RES, PAR = {}, {}
for v in ("LFP", "NMC"):
    RES[v] = json.load(open(f"{D}/ergebnis_{v}_e2d_e3c.json")); PAR[v] = json.load(open(f"{D}/parameter_{v}.json"))
def bisect(f, lo, hi):
    for _ in range(80):
        m = (lo + hi) / 2
        if (f(lo) > 0) == (f(m) > 0): lo = m
        else: hi = m
    return (lo + hi) / 2
aus = {}
for v in RES:
    r, A, P = RES[v], {k: x["wert"] for k, x in PAR[v]["A"].items()}, PAR[v]["parameter"]
    g = {k: x["masse_kg"] for k, x in r["gruppen"].items()}
    L, B, rand, rho = r["gehaeuse_L_mm"], r["breite_mm"], A["A_rand_mm"], A["A_alu_dichte_kg_m3"] * 1e-9
    Ai = (L - 2 * rand) * (B - 2 * rand); Ag = L * B
    nz = int(A["A_quertraeger_anzahl"]); qb, qh, qw = A["A_quertraeger_breite_mm"], A["A_quertraeger_hoehe_mm"], A["A_quertraeger_wand_mm"]
    # (b) Nachrechnung je Gruppe >= 3 kg
    vol_rf = r["gruppen"]["Seitenrahmen"]["volumen_cm3"] * 1e3; hr = vol_rf / (Ag - Ai)
    wr, nk = A["A_seitenrahmen_wand_mm"], int(A["A_seitenrahmen_kammern"])
    fr = lambda w: (2 * rand * w + (nk + 1) * (hr - 2 * w) * w) / (rand * hr)
    m_voll_rf = vol_rf * rho
    nach = {"Unterfahrschutz": Ag * A["A_unterfahrschutz_mm"] * rho, "Boden": Ag * A["A_boden_mm"] * rho, "Deckel": Ag * A["A_deckel_mm"] * rho,
            "Kuehlplatte": 2 * Ai * A["A_kuehlplatte_mm"] * rho * A["A_KUEHLPLATTE_FUELLGRAD"],
            "Seitenrahmen": m_voll_rf * fr(wr), "Pad": 2 * Ai * A["A_pad_mm"] * A["A_dichte_pad_kg_m3"] * 1e-9,
            "Quertraeger": nz * (B - 2 * rand) * (qb * qh - (qb - 2 * qw) * (qh - 2 * qw)) * rho}
    if v == "NMC":
        nach["Verguss"] = r["gruppen"]["Verguss"]["volumen_cm3"] * 1e3 * A["A_dichte_verguss_kg_m3"] * 1e-9
        for k_ in ("Gruppenverbinder", "Gruppenbruecke"): nach[k_] = r["gruppen"][k_]["volumen_cm3"] * 1e3 * rho   # nur Volumen x Dichte (Konsistenz)
        nach["Zelltraeger"] = r["gruppen"]["Zelltraeger"]["volumen_cm3"] * 1e3 * A["A_dichte_zelltraeger_kg_m3"] * 1e-9
    tab = []
    for k, x in r["gruppen"].items():
        if x["masse_kg"] >= 3 and k != "Zellen":
            n = nach.get(k); tab.append({"gruppe": k, "masse_kg": x["masse_kg"], "nachgerechnet_kg": n, "abw_prozent": None if n is None else 100 * (n / x["masse_kg"] - 1), "werkstoff": x["werkstoff"]})
    zellen = g["Zellen"]; rest = r["masse_bekannt_kg"] - zellen
    # Geometrie H5: Pad nur unter Zellen
    if v == "LFP":
        Lc, Dc = float(P["BT-100"]["laenge_mm"]["wert"]), float(P["BT-100"]["dicke_mm"]["wert"]); fuss = r["zellen"] * Lc * Dc
    else:
        fuss = r["zellen"] * math.pi / 4 * float(P["BT-100"]["durchmesser_mm"]["wert"]) ** 2
    apad = r["gruppen"]["Pad"]["volumen_cm3"] * 1e3 / (2 * A["A_pad_mm"])
    h5_geo = g["Pad"] * (1 - fuss / apad)
    # Rückrechnung Hebelspanne -> Parameter
    rueck = {}
    eq = A["A_kuehlplatte_mm"] * A["A_KUEHLPLATTE_FUELLGRAD"]
    rueck["H1"] = {"aequiv_dicke_ist_mm": eq, "fuellgrad_ist": A["A_KUEHLPLATTE_FUELLGRAD"], "masse_6mm_voll_kg": 2 * Ai * 6 * rho,
                   "fuellgrad_fuer_spanne": [A["A_KUEHLPLATTE_FUELLGRAD"] * (1 - s / g["Kuehlplatte"]) for s in HEBEL["H1"][2]],
                   "aequiv_dicke_fuer_spanne_mm": [eq * (1 - s / g["Kuehlplatte"]) for s in HEBEL["H1"][2]]}
    rueck["H2"] = {"anteil_boden_prozent": [100 * s / g["Boden"] for s in HEBEL["H2"][2]], "obergrenze_boden_entfaellt_kg": g["Boden"], "hoehe_gewinn_mm": A["A_boden_mm"] + A["A_luft_mm"]}
    rueck["H3"] = {"anteil_prozent": [100 * s / g["Unterfahrschutz"] for s in HEBEL["H3"][2]], "aequiv_al_dicke_mm": [A["A_unterfahrschutz_mm"] * (1 - s / g["Unterfahrschutz"]) for s in HEBEL["H3"][2]], "werkstoff_ist": r["gruppen"]["Unterfahrschutz"]["werkstoff"]}
    rueck["H4"] = {"anteil_prozent": [100 * s / g["Deckel"] for s in HEBEL["H4"][2]], "aequiv_al_dicke_mm": [A["A_deckel_mm"] * (1 - s / g["Deckel"]) for s in HEBEL["H4"][2]]}
    rueck["H5"] = {"pad_flaeche_cm2": apad / 100, "zellfussflaeche_cm2": fuss / 100, "einsparung_geometrie_kg": h5_geo, "anteil_prozent": 100 * (1 - fuss / apad)}
    ws = [bisect(lambda w: fr(w) * m_voll_rf - (g["Seitenrahmen"] - s), 0.05, wr) for s in HEBEL["H6"][2]]
    rueck["H6"] = {"hr_mm": hr, "masse_vollprofil_kg": m_voll_rf, "faktor_ist": fr(wr), "wand_fuer_spanne_mm": ws, "ist_bereits_kammerprofil": True,
                   "masse_wand_2mm_kg": m_voll_rf * fr(2.0)}
    if v == "NMC":
        a0 = A["A_vergusshoehe_anteil_NMC"]
        rueck["H7"] = {"vergusshoehe_anteil_ist": a0, "anteil_fuer_spanne": [a0 * (1 - s / g["Verguss"]) for s in HEBEL["H7"][2]], "ist_bereits_halbe_hoehe": True}
    # Summen
    hs = {h: x for h, x in HEBEL.items() if h != "H7" or v == "NMC"}
    lo = sum(x[2][0] for x in hs.values()); hi = sum(x[2][1] for x in hs.values()); m0 = r["masse_bekannt_kg"]
    aus[v] = {"masse_ist_kg": m0, "zellen_kg": zellen, "rest_kg": rest, "zellanteil_ist_prozent": 100 * zellen / m0, "ziel_kg": ZIEL[v], "zellanteil_ziel_prozent": 100 * zellen / ZIEL[v],
              "rest_max_fuer_ziel_kg": ZIEL[v] - zellen, "rest_muss_sinken_um_kg": rest - (ZIEL[v] - zellen), "gruppen": tab,
              "hebel": {h: {"name": x[0], "gruppe": x[1], "masse_gruppe_kg": g.get(x[1]), "spanne_kg": list(x[2])} for h, x in hs.items()},
              "rueckrechnung": rueck, "summe_spanne_kg": [lo, hi], "masse_neu_kg": [m0 - hi, m0 - lo], "masse_neu_mitte_kg": m0 - (lo + hi) / 2,
              "zellanteil_neu_prozent": [100 * zellen / (m0 - lo), 100 * zellen / (m0 - hi)], "luecke_zum_ziel_kg": [m0 - hi - ZIEL[v], m0 - lo - ZIEL[v]],
              "ziel_erreicht_mit_oberer_spanne": (m0 - hi) <= ZIEL[v], "hoehe_stapel_mm": r["hoehe_stapel_mm"], "hoehe_max_mm": r["hoehe_max_mm"]}
aus["quellen"] = ["cad/pack/entwurf/ergebnis_LFP_e2d_e3c.json", "cad/pack/entwurf/ergebnis_NMC_e2d_e3c.json", "cad/pack/entwurf/parameter_LFP.json", "cad/pack/entwurf/parameter_NMC.json",
                  "sim/mechanik/l1_leichtbau/ERWARTUNG.md (Hebelspannen: Schätzung Opus)", "docs/01_lastenheft.md (REQ-P07)"]
aus["w51"] = {"band": None, "stand": "offen: forschung/ergebnis/W51.md fehlt (nur W51.err, W51.jsonl), keine bestandene Zitatprüfung"}
json.dump(aus, open(f"{O}/ergebnis.json", "w"), indent=1, ensure_ascii=False)
# ---- Wasserfall
for v in ("LFP", "NMC"):
    a = aus[v]; fig, ax = plt.subplots(figsize=(11, 6.2)); x = 0; labels = []
    ax.bar(x, a["masse_ist_kg"], 0.6, color="#7f7f7f"); ax.text(x, a["masse_ist_kg"] + 6, f"Ist {a['masse_ist_kg']:.0f}", ha="center", fontsize=9, fontweight="bold"); labels.append("Ist\n(CAD)")
    cur = a["masse_ist_kg"]
    for h, d in a["hebel"].items():
        x += 1; lo, hi = d["spanne_kg"]; mid = (lo + hi) / 2
        ax.bar(x, mid, 0.6, bottom=cur - mid, color="#2ca02c"); ax.errorbar(x, cur - mid, yerr=[[hi - mid], [mid - lo]], color="black", capsize=4, lw=1.2)
        ax.text(x, cur + 6, f"−{lo}…−{hi}", ha="center", fontsize=8); cur -= mid; labels.append(h)
        if h == "H5": ax.plot(x, cur + mid - a["rueckrechnung"]["H5"]["einsparung_geometrie_kg"], marker="D", color="red", ls="", label="H5 aus Geometrie (Pad nur unter Zellfläche)")
    x += 1; lo_m, hi_m = a["masse_neu_kg"]
    ax.bar(x, a["masse_neu_mitte_kg"], 0.6, color="#1f77b4"); ax.errorbar(x, a["masse_neu_mitte_kg"], yerr=[[a["masse_neu_mitte_kg"] - lo_m], [hi_m - a["masse_neu_mitte_kg"]]], color="black", capsize=5)
    ax.text(x, hi_m + 8, f"neu {lo_m:.0f}…{hi_m:.0f}", ha="center", fontsize=9, fontweight="bold"); labels.append("neu\n(Spanne)")
    ax.axhspan(0, a["ziel_kg"], color="green", alpha=0.12); ax.axhline(a["ziel_kg"], color="green", lw=2.5)
    ax.text(0.2, a["ziel_kg"] - 14, f"Zielband REQ-P07: Masse ≤ {a['ziel_kg']:.0f} kg", color="darkgreen", fontsize=10, fontweight="bold")
    ax.axhline(a["zellen_kg"], color="#1f77b4", ls="--", lw=1.2); ax.text(len(a["hebel"]) / 2 + 0.5, a["zellen_kg"] + 4, f"Zellen allein {a['zellen_kg']:.0f} kg", color="#1f77b4", fontsize=9, ha="center")
    ax.text(0.01, 0.97, "Band aus W51 (Serien-Zellanteil): offen, W51 nicht fertig", transform=ax.transAxes, fontsize=8, va="top", color="gray")
    ax.set_xticks(range(len(labels))); ax.set_xticklabels(labels); ax.set_ylabel("Packmasse [kg]"); ax.set_ylim(max(0, a["zellen_kg"] - 100), a["masse_ist_kg"] + 45)
    ax.set_title(f"L1 Leichtbau {v}: Ist {a['masse_ist_kg']:.0f} kg, mit Hebeln H1–H{len(a['hebel'])} {lo_m:.0f}…{hi_m:.0f} kg, Ziel {a['ziel_kg']:.0f} kg (Spannen: Schätzung Opus)", fontsize=10)
    if v == "LFP": ax.legend(loc="upper right", fontsize=8)
    fig.text(.01, .01, f"KI-generiert (Claude Sonnet), Entwurf. Quelle: sim/mechanik/l1_leichtbau/ergebnis.json (aus cad/pack/entwurf/ergebnis_{v}_e2d_e3c.json). Achse beginnt nicht bei 0.", fontsize=7)
    fig.tight_layout(); fig.savefig(f"{O}/wasserfall_{v}.png", dpi=110); plt.close(fig)
L, N = aus["LFP"], aus["NMC"]
open(f"{O}/wasserfall_lesehilfe.md", "w", encoding="utf-8").write(f"""> **KI-generiert** (Claude Sonnet, 2026-11-24), Entwurf.

**Lesehilfe zu wasserfall_LFP.png.** Links der heutige Pack aus dem CAD ({L['masse_ist_kg']:.0f} kg), dann je eine grüne Stufe pro Leichtbau-Hebel H1 bis H6 (Stufe = Mitte der Schätzung von Opus, schwarzer Strich = Spanne von–bis), rechts die Masse danach als Spanne ({L['masse_neu_kg'][0]:.0f} bis {L['masse_neu_kg'][1]:.0f} kg). Die grüne Fläche mit dicker Linie ist das Ziel aus REQ-P07 (höchstens {L['ziel_kg']:.0f} kg). Liegt der blaue Balken samt Strich über der Linie, reichen die Hebel nicht. Die rote Raute bei H5 ist die Einsparung, die sich allein aus der Geometrie ergibt. Das Band aus W51 fehlt noch. Die Achse beginnt nicht bei null.

**Lesehilfe zu wasserfall_NMC.png.** Gleiche Darstellung für den NMC-Pack (Ist {N['masse_ist_kg']:.0f} kg, Ziel {N['ziel_kg']:.0f} kg) mit sieben Hebeln (H7: Verguss). Die gestrichelte blaue Linie zeigt die Masse der Zellen allein ({N['zellen_kg']:.0f} kg): nur {N['rest_max_fuer_ziel_kg']:.0f} kg blieben für alles andere, der Rest wiegt heute {N['rest_kg']:.0f} kg.

*KI-generiert, Entwurf.*
""")
print(json.dumps({v: {k: aus[v][k] for k in ("masse_ist_kg", "summe_spanne_kg", "masse_neu_kg", "luecke_zum_ziel_kg", "zellanteil_neu_prozent", "rest_muss_sinken_um_kg")} for v in ("LFP", "NMC")}, indent=1))
