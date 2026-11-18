#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. Auftrag K1. ERGEBNIS.md und ERGEBNIS_kurz.txt aus ergebnis.json. Keine Deutung."""
import json, os, datetime
HIER = os.path.dirname(os.path.abspath(__file__))
E = json.load(open(f"{HIER}/eingaben.json")); R = json.load(open(f"{HIER}/ergebnis.json")); F = R["faelle"]; ZT, ZD = R["ziel_T_max_C"], R["ziel_dT_K"]
f1 = lambda x: f"{x:.1f}"; f2 = lambda x: f"{x:.2f}"
def g(v, n): return F.get(f"{v}_{n}")
def rng(x, a, b): return a <= x <= b
def ok(b): return "erfüllt" if b else "verfehlt"
Z = []   # Zeilen
def z(s=""): Z.append(s)
datum = datetime.date.today().isoformat()
z("""| Dok.-Nr. | ERG-K1 | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Ergebnis K1: Schnellladen, Ladeprofile, Kühlvarianten (Elmer, Fortsetzung K0) | Ersteller | Claude Sonnet (KI), Auftrag Opus | Prüfer | – (Opus offen) |

> **KI-generiert.** Entwurf, nicht vom Menschen freigegeben. Stand %s. Alle Zahlen aus `sim/kuehlung/k1_schnellladen/ergebnis.json` (erzeugt von `k1_auswertung.py` aus `elmer/fall_*/`). Keine Deutung; Vergleich mit `ERWARTUNG.md` Punkt für Punkt unten. Vorgabe REQ-P09 (Annahme, offen): T_max ≤ %g °C, Spreizung ≤ %g K. ΔT = Kernmaximum minus Kernminimum (wie K0 `dT_kern`).
""" % (datum, ZT, ZD))
z("## 1 Abgleich P0 mit K0 L2 (Stoppkriterium > 0,3 K)\n\n| Variante | T_max K1 P0 | T_max K0 L2 | Abw. | ΔT K1 P0 | ΔT K0 L2 | Abw. | Fundstelle K0 |\n|---|---|---|---|---|---|---|---|")
for v, a in R["abgleich_P0_K0"].items(): z(f"| {v} | {a['T_max_K1']:.3f} °C | {a['T_max_K0']:.3f} °C | {a['abw_T_K']:+.4f} K | {a['dT_K1']:.3f} K | {a['dT_K0']:.3f} K | {a['abw_dT_K']:+.4f} K | {a['quelle_K0']} |")
z("\nNMC-Netz: nach dem Nachtrag (Abschnitt 7) auf dem aktuellen CAD-Stand (Kernloch r 6,25 mm, V_kern 111 711 mm³). Der erste Lauf (K0-Stand r 7,0 mm) steht in `ergebnis_vor_nachtrag.json` / `ERGEBNIS_vor_nachtrag.md`. Die NMC-Abweichung zu K0 L2 oben ist deshalb Geometrie, nicht Rechenfehler.\n")
def tab(v):
    z(f"\n### {v}\n\n| Fall | I-Profil | Ladezeit | T_max-Spitze (t) | ΔT-Spitze (t) | T_max Ladeende | ΔT Ladeende | ΔT Mittel | t > {ZT:g} °C | t > {ZD:g} K | ∫Q dt | Q rel. P0 | Bilanz | Laufzeit |\n|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for n, r in F.items():
        if r["meta"]["v"] != v: continue
        m = r["meta"]; prof = "; ".join(f"{s['C']:.3g}C {s['t_von']:.0f}-{s['t_bis']:.0f}s" for s in m["stufen"][:3]) + (" …(Takt 60 s)" if len(m["stufen"]) > 3 else "")
        z(f"| {n} | {prof} | {r['ladezeit_s']/60:.0f} min | {f1(r['T_max_Spitze_C'])} °C ({r['t_T_max_Spitze_s']:.0f} s) | {f1(r['dT_Spitze_K'])} K ({r['t_dT_Spitze_s']:.0f} s) | {f1(r['T_max_Ende_C'])} °C | {f1(r['dT_Ende_K'])} K | {f1(r['dT_mittel_K'])} K | {r['t_ueber_45C_s']:.0f} s | {r['t_ueber_5K_s']:.0f} s | {r['E_quelle_tab_J']/1000:.2f} kJ | {r.get('waerme_rel_P0', float('nan')):.3f} | {r['bilanz_abw_prozent']:+.3f} % | {m['laufzeit_gesamt_s']:.0f} s |")
z("## 2 Ergebnistabellen (alle Fälle)\n\nKühlung Boden h 500 und Start 25 °C, wenn im Fallnamen nichts anderes steht (Kh = h in W/(m²K), K3 = Boden und Oben gekühlt, V15 = Start und Kühlmittel 15 °C). t > Schwelle: linear interpolierte Zeit über der Schwelle. Bilanz: (Kühlrand-Integral + gespeicherte Energie − ∫Q dt) / ∫Q dt.")
tab("LFP"); tab("NMC")
z("\n## 3 Wärmeintegral gegen Tabelle (Prüfung ±2 %)\n\n| Fall | ∫Q dt (Schrittsumme) | ∫Q dt exakt aus Stufen | Q rel. P0 | Tabelle ERWARTUNG | Abw. | Prüfung |\n|---|---|---|---|---|---|---|")
vmax = 0
for n, r in F.items():
    if "waerme_rel_P0" not in r or r["meta"]["kuehl"] != "K1h500" : continue
    a = r["waerme_abw_prozent"]; vmax = max(vmax, abs(a))
    z(f"| {n} | {r['E_quelle_tab_J']:.1f} J | {r['E_quelle_exakt_J']:.1f} J | {r['waerme_rel_P0']:.4f} | {r['waerme_rel_tabelle']} | {a:+.2f} % | {'≤ 2 % erfüllt' if abs(a) <= 2 else '> 2 % VERFEHLT'} |")
z(f"\nGrößte Abweichung: {vmax:.2f} %. (Tabellenwerte in `eingaben.json` aus ERWARTUNG; P1 letzte Stufe 1,3846C = 0,15/(390/3600), Tabelle 1,385C.)")
# Abgleich
z("\n## 4 Abgleich mit ERWARTUNG.md, Punkt für Punkt\n\nBereichsangaben (a–b) werden mit erfüllt/verfehlt bewertet; Angaben mit „≈“ nur als Abweichung (keine Toleranz in ERWARTUNG festgelegt). Deutung bleibt bei Opus.\n")
z("### Profile\n\n| Punkt | Erwartung (ERWARTUNG.md) | Ergebnis | Bewertung |\n|---|---|---|---|")
def rng(x, a, b): return a <= x <= b
for v in ("LFP", "NMC"):
    p0 = g(v, "P0"); exp = {"LFP": (43.1, 10.6), "NMC": (53.6, 16.0)}[v]
    z(f"| {v} P0 | {exp[0]} °C / {exp[1]} K | {f1(p0['T_max_Ende_C'])} °C / {f1(p0['dT_Ende_K'])} K | ≈: Abw. {p0['T_max_Ende_C']-exp[0]:+.1f} K / {p0['dT_Ende_K']-exp[1]:+.1f} K |")
for v in ("LFP", "NMC"):
    p0, p1 = g(v, "P0"), g(v, "P1")
    if v == "LFP": z(f"| LFP P1 | Spitze ΔT ≈ 10–12 K (während 3C), Ende ≈ 5–7 K; T_max ± 2 K zu P0 | Spitze {f1(p1['dT_Spitze_K'])} K bei {p1['t_dT_Spitze_s']:.0f} s; Ende {f1(p1['dT_Ende_K'])} K; T_max-Ende {f1(p1['T_max_Ende_C'])} (P0 {f1(p0['T_max_Ende_C'])}, Diff {p1['T_max_Ende_C']-p0['T_max_Ende_C']:+.1f} K), Spitze {f1(p1['T_max_Spitze_C'])} | Spitze ΔT 10–12: {ok(rng(p1['dT_Spitze_K'],10,12))}; Ende 5–7: {ok(rng(p1['dT_Ende_K'],5,7))}; T_max ±2 K: {ok(abs(p1['T_max_Ende_C']-p0['T_max_Ende_C'])<=2)} |")
    else: z(f"| NMC P1 | ähnlich, Spitze ΔT ≈ 15–18 K | Spitze {f1(p1['dT_Spitze_K'])} K bei {p1['t_dT_Spitze_s']:.0f} s; Ende {f1(p1['dT_Ende_K'])} K; T_max-Ende {f1(p1['T_max_Ende_C'])} (P0 {f1(p0['T_max_Ende_C'])}) | Spitze ΔT 15–18: {ok(rng(p1['dT_Spitze_K'],15,18))} |")
for v, tr, dtv in (("LFP", "55–60", 20), ("NMC", "75–85", None)):
    p = g(v, "P2"); a, b = (55, 60) if v == "LFP" else (75, 85)
    mn = min(p["dT_kern_t_K"][len(p["dT_kern_t_K"])//2:])
    z(f"| {v} P2 | T_max ≈ {tr} °C" + (f", ΔT schwankt um ≈ 20 K" if v == "LFP" else ", schlechter als P0") + f" | T_max-Spitze {f1(p['T_max_Spitze_C'])} °C (Ende {f1(p['T_max_Ende_C'])}); ΔT Spitze {f1(p['dT_Spitze_K'])} K, Mittel {f1(p['dT_mittel_K'])} K, Min in 2. Hälfte {f1(mn)} K | T_max {a}–{b}: {ok(rng(p['T_max_Spitze_C'], a, b))}" + (f"; schlechter als P0 (P0 {f1(g(v,'P0')['T_max_Spitze_C'])} °C): {ok(p['T_max_Spitze_C']>g(v,'P0')['T_max_Spitze_C'])}" if v == 'NMC' else f"; ΔT-Mittel ≈ 20: Abw. {p['dT_mittel_K']-20:+.1f} K") + " |")
for pn, (le, ne) in (("P3", (("≈ 40 °C / ≈ 7–8 K", (40, None, 7, 8)), ("≈ 47–50 °C / ≈ 11–13 K", (47, 50, 11, 13)))), ("P4", (("≈ 37 °C / ≈ 5–6 K", (37, None, 5, 6)), ("≈ 42–44 °C / ≈ 8–9 K", (42, 44, 8, 9))))):
    for v, (txt, (t0, t1, d0, d1)) in (("LFP", le), ("NMC", ne)):
        p = g(v, pn); Tt, dd = p["T_max_Ende_C"], p["dT_Ende_K"]
        bew = (f"T_max {t0}–{t1}: {ok(rng(Tt,t0,t1))}; " if t1 else f"T_max Abw. {Tt-t0:+.1f} K; ") + f"ΔT {d0}–{d1}: {ok(rng(dd,d0,d1))}"
        z(f"| {v} {pn} | {txt} | {f1(Tt)} °C / {f1(dd)} K (Spitze ΔT {f1(p['dT_Spitze_K'])} K) | {bew} |")
z("\nNicht gerechnet in K1 (nicht Teil des Auftrags): „Stationär nötig für 5 K: LFP ≤ 1,29C, NMC ≤ 1,02C“.\n")
z("### Kühlung (Profil P0, Differenz zu P0 derselben Variante)\n\n| Punkt | Erwartung | Ergebnis | Bewertung |\n|---|---|---|---|")
for v in ("LFP", "NMC"):
    p0 = g(v, "P0")
    for k, ex in (("Kh1000", {"LFP": "T_max −3…−5 K, ΔT unverändert", "NMC": "T_max −8…−10 K, ΔT unverändert"}), ("Kh2000", {"LFP": "T_max −5…−8 K, ΔT unverändert", "NMC": "T_max ≈ 41–44 °C ✓, ΔT ≈ 16 K ✗"})):
        r = g(v, f"P0_{k}"); dT_ = r["T_max_Ende_C"] - p0["T_max_Ende_C"]; dD = r["dT_Ende_K"] - p0["dT_Ende_K"]
        rg = {("LFP", "Kh1000"): (-5, -3), ("NMC", "Kh1000"): (-10, -8), ("LFP", "Kh2000"): (-8, -5)}.get((v, k))
        bew = (f"T_max-Änderung {rg[0]}…{rg[1]}: {ok(rng(dT_, *rg))}; " if rg else f"T_max 41–44: {ok(rng(r['T_max_Ende_C'],41,44))}; ΔT ≈ 16: Abw. {r['dT_Ende_K']-16:+.1f} K; ") + "ΔT-Änderung " + f"{dD:+.2f} K"
        z(f"| {v} {k} | {ex[v]} | T_max {f1(r['T_max_Ende_C'])} °C ({dT_:+.1f} K), ΔT {f1(r['dT_Ende_K'])} K ({dD:+.2f} K) | {bew} |")
    r = g(v, "P0_K3"); ex = {"LFP": "ΔT ≈ ÷4 → ≈ 3 K ✓, T_max ≈ 35 °C ✓", "NMC": "ΔT ≈ 4–5 K (knapp), T_max ≈ 38–40 °C ✓"}[v]
    bew = f"ΔT-Verhältnis K3/P0 = {r['dT_Ende_K']/p0['dT_Ende_K']:.3f}; " + (f"verfehlt-Kriterium „ΔT sinkt um weniger als die Hälfte“: {'EINGETRETEN' if r['dT_Ende_K']>0.5*p0['dT_Ende_K'] else 'nicht eingetreten'}; ΔT ≈ 3: Abw. {r['dT_Ende_K']-3:+.1f} K; T_max ≈ 35: Abw. {r['T_max_Ende_C']-35:+.1f} K" if v == "LFP" else f"ΔT 4–5: {ok(rng(r['dT_Ende_K'],4,5))}; T_max 38–40: {ok(rng(r['T_max_Ende_C'],38,40))}")
    z(f"| {v} K3 | {ex} | T_max {f1(r['T_max_Ende_C'])} °C, ΔT {f1(r['dT_Ende_K'])} K | {bew} |")
    r = g(v, "P0_V15"); dT_ = r["T_max_Ende_C"] - p0["T_max_Ende_C"]; dD = r["dT_Ende_K"] - p0["dT_Ende_K"]
    z(f"| {v} V15 | T_max −10 K, ΔT unverändert | T_max {f1(r['T_max_Ende_C'])} °C ({dT_:+.2f} K), ΔT {f1(r['dT_Ende_K'])} K ({dD:+.3f} K) | T_max −10: {ok(abs(dT_+10)<0.05)}; ΔT-Änderung {dD:+.3f} K |")
z("\nModellfakt zu NMC K3 (Nachtrag): Zwischen Wickel (z 76 mm) und Deckel (z 79,6 mm) liegt bei K3/K3h1000 die Tab-Scheibe statt Luft (Abschnitt 7); bei allen anderen NMC-Fällen bleibt Luft (k = 0,026). Bei LFP liegt der Kern mit Gehäusewand (0,3 mm Al) direkt an Boden und Oben.\n")
z("\n### Kombinationen\n\n| Fall | Erwartung | Ergebnis (Ladeende; Spitzen) | Vorgaben T_max ≤ 45 °C / ΔT ≤ 5 K (Spitzenwerte) |\n|---|---|---|---|")
ex = {"LFP_P1_K3": "LFP K3 erfüllt beides bei 20 min", "LFP_P0_K3h1000": "LFP K3 erfüllt beides bei 20 min", "NMC_P1_K3": "NMC braucht K3 + h ≥ 1000 oder K3 + P3", "NMC_P0_K3h1000": "NMC braucht K3 + h ≥ 1000 oder K3 + P3", "NMC_P3_Kh2000": "(Kombination aus ERWARTUNG; Einzelwert nicht angegeben)", "NMC_P3_K3": "NMC K3 + P3 (Erwartung: reicht)"}
for n in ("LFP_P0_K3", "LFP_P1_K3", "LFP_P0_K3h1000", "NMC_P0_K3", "NMC_P1_K3", "NMC_P0_K3h1000", "NMC_P3_K3", "NMC_P3_Kh2000"):
    r = F.get(n)
    if r: z(f"| {n} | {ex.get(n, 'siehe oben (K3 allein)')} | T_max {f1(r['T_max_Ende_C'])} °C (Spitze {f1(r['T_max_Spitze_C'])}), ΔT {f1(r['dT_Ende_K'])} K (Spitze {f1(r['dT_Spitze_K'])}) | T_max {ok(r['T_max_Spitze_C']<=ZT)}; ΔT {ok(r['dT_Spitze_K']<=ZD)} |")
z("\n### Als „Verfehlt“ in ERWARTUNG definiert\n")
vm = max(abs(r["waerme_abw_prozent"]) for r in F.values() if "waerme_abw_prozent" in r and r["meta"]["kuehl"] == "K1h500")
z(f"- Wärmeintegral > 2 % von Tabelle: größte Abweichung {vm:.2f} % → {'nicht eingetreten' if vm<=2 else 'EINGETRETEN'}.")
for v, a in R["abgleich_P0_K0"].items(): z(f"- P0 weicht > 0,3 K von K0 L2 ab ({v}): Abw. T {a['abw_T_K']:+.4f} K, ΔT {a['abw_dT_K']:+.4f} K → {'nicht eingetreten' if max(abs(a['abw_T_K']),abs(a['abw_dT_K']))<=0.3 else 'EINGETRETEN'}.")
r = g("LFP", "P0_K3"); p0 = g("LFP", "P0"); z(f"- K3 senkt ΔT bei LFP um weniger als die Hälfte: ΔT {f1(p0['dT_Ende_K'])} → {f1(r['dT_Ende_K'])} K (−{100*(1-r['dT_Ende_K']/p0['dT_Ende_K']):.0f} %) → {'EINGETRETEN' if r['dT_Ende_K']>0.5*p0['dT_Ende_K'] else 'nicht eingetreten'}.")
z("\n## 7 Nachtrag (Auftrag Opus): NMC-Netz aktuell, NMC K3 mit Tab-Scheibe\n")
O = json.load(open(f"{HIER}/ergebnis_vor_nachtrag.json"))["faelle"]; T_ = E["nmc_tabscheibe"]
ti = F["NMC_P0_K3"]["tabscheibe"]
z(f"- Änderung 1: NMC-Netz auf aktuelles CAD (Kernloch r 6,25 mm statt 7,0 mm), alle 13 NMC-Fälle neu gerechnet; LFP unverändert.")
a = R["abgleich_P0_K0"]["NMC"]
z(f"- Neuer Abgleich NMC P0 (K1, neues Netz) gegen K0 L2 (altes Netz, `{a['quelle_K0']}`): T_max {a['T_max_K1']:.3f} gegen {a['T_max_K0']:.3f} °C ({a['abw_T_K']:+.3f} K), ΔT {a['dT_K1']:.3f} gegen {a['dT_K0']:.3f} K ({a['abw_dT_K']:+.3f} K). Die 0,3-K-Grenze gilt für gleiches Netz (Abgleich vorher: 0,0000 K); hier ist die Abweichung die Wirkung der Geometrieänderung.")
z(f"- Änderung 2: NMC K3/K3h1000: Raum Wickel–Deckel (Höhe g = {ti['g_mm']:.1f} mm) statt Luft als Tab-Scheibe. Annahme Opus: {T_['al_dicke_mm']} mm Al flächig (k {T_['k_al']}) plus Kontaktschicht {T_['kontakt_dicke_mm']} mm, k {T_['k_kontakt']:g} W/(m K). Unten liegt im Modell keine Luft (Raum Becherboden–Wickel ist Kernmaterial), dort daher keine Scheibe. Umsetzung (Annahme des Umsetzers, bitte prüfen): in der Ebene k_xy = {ti['k_xy']:.2f}, senkrecht k_z = {ti['k_z']:.2f} W/(m K) (Scheibe überbrückt den Raum als Leiter, Kontaktschicht in Reihe).")
z("\n| NMC-Fall | vorher (K0-Netz, K3 mit Luft) T_max / ΔT (Spitze) | jetzt (neues Netz, K3 mit Tab) T_max / ΔT (Spitze) | Differenz T_max / ΔT |\n|---|---|---|---|")
for n in sorted(k for k in F if k.startswith("NMC")):
    r, o = F[n], O.get(n)
    if o: z(f"| {n} | {o['T_max_Spitze_C']:.1f} °C / {o['dT_Spitze_K']:.1f} K | {r['T_max_Spitze_C']:.1f} °C / {r['dT_Spitze_K']:.1f} K | {r['T_max_Spitze_C']-o['T_max_Spitze_C']:+.1f} K / {r['dT_Spitze_K']-o['dT_Spitze_K']:+.1f} K |")
    else: z(f"| {n} (neu) | – | {r['T_max_Spitze_C']:.1f} °C / {r['dT_Spitze_K']:.1f} K | – |")
z("\nVorgaben (Spitzenwerte T_max ≤ 45 °C, ΔT ≤ 5 K) für die K3-Fälle: " + "; ".join(f"{n}: T_max {ok(F[n]['T_max_Spitze_C']<=ZT)}, ΔT {ok(F[n]['dT_Spitze_K']<=ZD)}" for n in ("NMC_P0_K3","NMC_P0_K3h1000","NMC_P3_K3","NMC_P1_K3")) + ".")
z("\nHinweis: Die Bewertungen in Abschnitt 4 gelten für die neuen Zahlen. Bilder und Landkarte sind aktualisiert.")
z("\n## 5 Laufzeiten\n"); lz = sum(r["meta"]["laufzeit_gesamt_s"] for r in F.values())
z(f"Summe Einzelläufe (Elmer + Nachlauf) {lz/60:.1f} min CPU, 4 Läufe parallel (nice 10, 1 Kern je Lauf); P0-Gate separat. Je Fall: Tabelle in Abschnitt 2, Spalte Laufzeit.")
z("\n## 6 Bilder\n\n`profile.png`, `verlauf_profile_LFP.png`, `verlauf_profile_NMC.png`, `verlauf_kuehlung_LFP.png`, `verlauf_kuehlung_NMC.png`, `landkarte.png` (Lesehilfe `k1_lesehilfe.md`); Render (Blender Cycles CPU, Endzustand): `bilder/render_LFP_P0_K3h1000_ende.png` (Fall mit niedrigster T_max unter den beide-erfüllenden LFP-Fällen), `bilder/render_NMC_P4_ende.png` (kein NMC-Fall erfüllt beide; bester = T_max ≤ 45 °C mit kleinster ΔT-Spitze); Lesehilfe `bilder/render_lesehilfe.md`. Die obere Kühlplatte (K3) ist im Render nicht gezeichnet; LFP-Render wirkt dunkel wegen der festen Skala 25–55 °C.")

# ---- Abschnitt 8: Nachtrag K1b
KB = E["faelle"].get("K1b", [])
if KB:
    import re
    z("\n## 8 Nachtrag K1b: 4680 obere Kühlung über Verbinder und Isolierpad (Annahme Opus, ENT-092…095 vorgeschlagen)\n")
    z("Modell: unten Boden h 500 über Becherboden + Tab-Scheibe (wie K3), oben Robin-Rand mit Ersatz-Wärmeübergang h_eff = φ / (1/h + t_pad/k_pad + t_v/k_v), h 500, t_pad 1 mm, Verbinder Al 1,5 mm (k 237). Werte in `eingaben.json` (Herkunft „Annahme Opus“, ERWARTUNG.md Nachtrag K1b). h_eff-Kontrolle: Wert aus `elmer/fall_*/case.sif` (Rand „Kuehlrand_Oben“) gegen Formel.\n")
    z("| Fall | φ | k_pad W/(m K) | h_eff Formel | h_eff in case.sif | Abw. | T_max-Spitze | ΔT-Spitze | T_max Ende | ΔT Ende | Bilanz | Laufzeit |\n|---|---|---|---|---|---|---|---|---|---|---|---|")
    hmax = 0
    for p_, k in KB:
        n = f"NMC_{p_}_{k}"; r = F.get(n)
        if not r: z(f"| {n} | nicht gerechnet |"); continue
        kc = E["kuehlung"][k]; hf = kc["phi"] / (1 / kc["h_fluid"] + kc["t_pad_m"] / kc["k_pad"] + kc["t_v_m"] / kc["k_v"])
        sif = open(f"{HIER}/elmer/fall_{n}/case.sif").read(); m = re.search(r'Name = "Kuehlrand_Oben"\n.*?Heat Transfer Coefficient = ([0-9.eE+-]+)', sif, re.S); hs = float(m.group(1)); ab = 100 * (hs - hf) / hf; hmax = max(hmax, abs(ab))
        z(f"| {n} | {kc['phi']:g} | {kc['k_pad']:g} | {hf:.1f} | {hs:.1f} | {ab:+.2f} % | {f1(r['T_max_Spitze_C'])} °C | {f1(r['dT_Spitze_K'])} K | {f1(r['T_max_Ende_C'])} °C | {f1(r['dT_Ende_K'])} K | {r['bilanz_abw_prozent']:+.3f} % | {r['meta']['laufzeit_gesamt_s']:.0f} s |")
    z(f"\nGrößte h_eff-Abweichung Modell/Formel: {hmax:.2f} % (Verfehlt-Kriterium > 1 %: {'EINGETRETEN' if hmax > 1 else 'nicht eingetreten'}).\n")
    z("### Abgleich mit ERWARTUNG.md Nachtrag K1b\n\n| Punkt | Erwartung | Ergebnis (Spitze T_max / ΔT) | Bewertung |\n|---|---|---|---|")
    a, b, c = F.get("NMC_P0_K3b"), F.get("NMC_P3_K3b"), F.get("NMC_P4_K3b")
    if a: z(f"| NMC P0 K3b | 44–46 °C / 8–10 K (zwischen K1 53,6/16,0 und K3 38,9/5,8) | {f1(a['T_max_Spitze_C'])} °C / {f1(a['dT_Spitze_K'])} K | T_max 44–46: {ok(rng(a['T_max_Spitze_C'],44,46))}; ΔT 8–10: {ok(rng(a['dT_Spitze_K'],8,10))}; Verfehlt-Kriterium (T_max außerhalb 41–49): {'EINGETRETEN' if not rng(a['T_max_Spitze_C'],41,49) else 'nicht eingetreten'} |")
    if b: z(f"| NMC P3 K3b | 38–40 °C / 5,5–7 K → 5 K knapp verfehlt | {f1(b['T_max_Spitze_C'])} °C / {f1(b['dT_Spitze_K'])} K | T_max 38–40: {ok(rng(b['T_max_Spitze_C'],38,40))}; ΔT 5,5–7: {ok(rng(b['dT_Spitze_K'],5.5,7))}; ΔT ≤ 5 K: {ok(b['dT_Spitze_K']<=ZD)} |")
    if c: z(f"| NMC P4 K3b | ≈ 35 °C / ≈ 4,5–5 K → knapp erfüllt | {f1(c['T_max_Spitze_C'])} °C / {f1(c['dT_Spitze_K'])} K | T_max Abw. zu 35: {c['T_max_Spitze_C']-35:+.1f} K; ΔT 4,5–5: {ok(rng(c['dT_Spitze_K'],4.5,5))}; ΔT ≤ 5 K: {ok(c['dT_Spitze_K']<=ZD)} |")
    z("\nEmpfindlichkeit (Profil P3, Spitzenwerte; Vorgaben T_max ≤ 45 °C, ΔT ≤ 5 K):\n\n| Fall | φ | k_pad | h_eff | T_max | ΔT | T_max-Vorgabe | ΔT-Vorgabe |\n|---|---|---|---|---|---|---|---|")
    for k in ("K3b_phi03", "K3b", "K3b_phi07", "K3b_kpad1", "K3b_kpad6"):
        r = F.get(f"NMC_P3_{k}")
        if r: kc = E["kuehlung"][k]; z(f"| NMC_P3_{k} | {kc['phi']:g} | {kc['k_pad']:g} | {kc['h_rand']['Oben']:.1f} | {f1(r['T_max_Spitze_C'])} °C | {f1(r['dT_Spitze_K'])} K | {ok(r['T_max_Spitze_C']<=ZT)} | {ok(r['dT_Spitze_K']<=ZD)} |")
    z("\nVorgaben für alle K3b-Fälle (Spitzenwerte): " + "; ".join(f"{n}: T_max {ok(F[n]['T_max_Spitze_C']<=ZT)}, ΔT {ok(F[n]['dT_Spitze_K']<=ZD)}" for n in sorted(F) if "K3b" in n and "_C2" not in n) + ". Bilder: `landkarte.png` und `verlauf_kuehlung_NMC.png` enthalten NMC_P0_K3b bzw. die K3b-Zeilen. Keine Deutung (bei Opus).")
# ---- Abschnitt 9: Nachtrag K1c
K1C = E.get("K1c", {}).get("faelle", {})
if K1C:
    z("\n## 9 Nachtrag K1c: Wärme aus C2 statt I²R-Schätzung (Annahme Opus, ERWARTUNG.md Nachtrag K1c)\n")
    z("Eingaben: LFP R 1,28 mΩ (Herkunft C2 `ergebnis_blade.json`, Test#5 Blade 10 s, 25 °C, 0,877 mΩ × 135/92,4); NMC Q(t) aus `sim/chemie/c2_kalibrierung/schnellladen_Q_t.csv` (4680, 1,5C, 7 Stützpunkte, linear interpoliert, Laufzeit bis letzter Stützpunkt 1720,8 s; 10→80 % wären 1780,8 s, die letzten 60 s fehlen in der CSV). Fall „I·ΔU“: CSV-Verlauf mit konstantem Faktor skaliert, sodass das Mittel dem I·ΔU-Mittel aus `ergebnis_schnellladen_n4680.json` entspricht (Faktor " + f"{json.load(open(f'{HIER}/elmer/fall_NMC_C2idu_K3b/meta.json'))['skal_Q']:.4f}" + "); der Zeitverlauf von I·ΔU ist in C2 nicht gespeichert, die Skalierung ist eine Annahme. Kühlung NMC wie K3b (φ 0,5, k_pad 3).\n")
    z("| Fall | Quelle | ∫Q dt Elmer-Schrittsumme | ∫Q dt CSV (Trapez, ggf. skaliert) | Abw. | T_max-Spitze (t) | ΔT-Spitze | T_max Ende | ΔT Ende | Bilanz | Vorgabe T_max ≤ 45 / ΔT ≤ 5 K | Laufzeit |\n|---|---|---|---|---|---|---|---|---|---|---|---|")
    for n, d in K1C.items():
        r = F.get(n)
        if not r: z(f"| {n} | nicht gerechnet |"); continue
        ab = 100 * (r["E_quelle_tab_J"] - r["E_quelle_exakt_J"]) / r["E_quelle_exakt_J"]
        z(f"| {n} | {d['herkunft']} | {r['E_quelle_tab_J']:.1f} J | {r['E_quelle_exakt_J']:.1f} J | {ab:+.2f} % | {f1(r['T_max_Spitze_C'])} °C ({r['t_T_max_Spitze_s']:.0f} s) | {f2(r['dT_Spitze_K'])} K | {f1(r['T_max_Ende_C'])} °C | {f2(r['dT_Ende_K'])} K | {r['bilanz_abw_prozent']:+.3f} % | T_max {ok(r['T_max_Spitze_C']<=ZT)}; ΔT {ok(r['dT_Spitze_K']<=ZD)} | {r['meta']['laufzeit_gesamt_s']:.0f} s |")
    z("\n### Abgleich mit ERWARTUNG.md Nachtrag K1c\n\n| Punkt | Erwartung | Ergebnis (Spitze) | Bewertung |\n|---|---|---|---|")
    a, b, c = F.get("LFP_P0_K3_R128"), F.get("NMC_C2gesamt_K3b"), F.get("NMC_C2idu_K3b"); a0 = F.get("LFP_P0_K3")
    if a: z(f"| LFP P0 K3, R 1,28 mΩ | ≈ 32,8 °C / ≈ 4,0 K (Skalierung ~0,87) | {f1(a['T_max_Spitze_C'])} °C / {f2(a['dT_Spitze_K'])} K (R 1,46: {f1(a0['T_max_Spitze_C'])} / {f2(a0['dT_Spitze_K'])}); Wärme-Verhältnis {a['E_quelle_tab_J']/a0['E_quelle_tab_J']:.3f} | T_max Abw. zu 32,8: {a['T_max_Spitze_C']-32.8:+.2f} K; ΔT Abw. zu 4,0: {a['dT_Spitze_K']-4.0:+.2f} K |")
    if b: z(f"| NMC K3b, Q gesamt (mittel 7,4 W) | ≈ 34–35 °C / 4,2–4,6 K (knapp erfüllt) | {f1(b['T_max_Spitze_C'])} °C / {f2(b['dT_Spitze_K'])} K | T_max 34–35: {ok(rng(b['T_max_Spitze_C'],34,35))}; ΔT 4,2–4,6: {ok(rng(b['dT_Spitze_K'],4.2,4.6))}; ΔT ≤ 5 K: {ok(b['dT_Spitze_K']<=ZD)} |")
    if c: z(f"| NMC K3b, I·ΔU (mittel 11,5 W) | ≈ 38–40 °C / 6–7 K (5 K verfehlt) | {f1(c['T_max_Spitze_C'])} °C / {f2(c['dT_Spitze_K'])} K | T_max 38–40: {ok(rng(c['T_max_Spitze_C'],38,40))}; ΔT 6–7: {ok(rng(c['dT_Spitze_K'],6,7))}; ΔT ≤ 5 K: {ok(c['dT_Spitze_K']<=ZD)} |")
    vm = max(abs(100 * (F[n]["E_quelle_tab_J"] - F[n]["E_quelle_exakt_J"]) / F[n]["E_quelle_exakt_J"]) for n in K1C if n in F)
    z(f"\nVerfehlt-Kriterium „Wärmeintegral ≠ CSV ± 2 %“: größte Abweichung {vm:.2f} % → {'nicht eingetreten' if vm<=2 else 'EINGETRETEN'}. Bilder: `landkarte.png` enthält die drei K1c-Zeilen. Offen für Opus: (a) CSV endet bei 1720,8 s, Ladeende 80 % erst bei 1780,8 s; (b) I·ΔU-Verlauf nur als skalierte Form; (c) R 1,28 mΩ gilt bei 25 °C, 50 % SOC, 10 s (Temperaturabhängigkeit nicht berücksichtigt). Keine Deutung (bei Opus).")

z("\n---\n*KI-generiert (Claude Sonnet), Entwurf, nicht vom Menschen freigegeben. Erzeugt von k1_bericht.py.*\n")
open(f"{HIER}/ERGEBNIS.md", "w", encoding="utf-8").write("\n".join(Z))
print("ok")
