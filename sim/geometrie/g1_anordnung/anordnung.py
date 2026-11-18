#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-17). Auftrag G1-V (Opus), Dok. ERW-G1. Status: Entwurf.
Liest NUR eingaben.json. Schreibt ergebnis.json, anordnung.png, anordnung_lesehilfe.md, ERGEBNIS.md, ERGEBNIS_kurz.txt,
praesentation/bausteine/G1.md. Laufzeit: Sekunden. Die Prüfgrenzen im Abgleich stammen aus ERWARTUNG.md (Abschnitt „Verfehlte Erwartung“)."""
import json, math, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle

D = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(D, "..", "..", ".."))
E = json.load(open(os.path.join(D, "eingaben.json"), encoding="utf-8"))
v = lambda k: E[k]["wert"]
BASIS = dict(
    bauraum=v("bauraum_mm"), rand=v("rand_je_seite_mm"), h_unten=v("hoehe_unten_mm"), h_oben=v("hoehe_oben_mm"),
    gap_lfp=E["LFP"]["zellabstand_mm"]["wert"], gap_nmc=E["NMC"]["zellabstand_mm"]["wert"])
BAND = dict(rand=E["rand_je_seite_mm"]["band"], h_unten=E["hoehe_unten_mm"]["band"], h_oben=E["hoehe_oben_mm"]["band"],
            gap_lfp=E["LFP"]["zellabstand_mm"]["band"], gap_nmc=E["NMC"]["zellabstand_mm"]["band"])
L_ = E["LFP"]; N_ = E["NMC"]
S = L_["s"]; UN = L_["nennspannung_V"]
FALL_E = {"A": {"LFP": E["energie_kWh"]["A"], "NMC": E["energie_kWh"]["A"]},
          "B": {"LFP": E["energie_kWh"]["B_LFP"], "NMC": E["energie_kWh"]["B_NMC"]}}
NMC_Z = {"A": N_["zellen"]["A"], "B": N_["zellen"]["B"]}

def stapel(n, dicke, gap):   # Länge von n Zellen in einer Reihe mit Abstand gap dazwischen
    return n * dicke + max(n - 1, 0) * gap

def lfp(p, fall):
    Lb, Bb, Hb = p["bauraum"]; Li, Bi = Lb - 2 * p["rand"], Bb - 2 * p["rand"]
    H = L_["querschnitt_hoehe_mm"]["wert"] + p["h_unten"] + p["h_oben"]
    ah = FALL_E[fall]["LFP"] * 1000 / (S * UN)
    # Längenregel aus eingaben.json (laenge_regel): Elektrodenlänge ∝ Ah, dazu feste Endzone = laenge_ref - elektrode_ref
    endzone = L_["laenge_ref_mm"]["wert"] - L_["elektrode_ref_mm"]["wert"]
    laenge = L_["elektrode_ref_mm"]["wert"] * ah / L_["kapazitaet_ref_Ah"]["wert"] + endzone
    dk, g = L_["dicke_mm"]["wert"], p["gap_lfp"]
    lage = {}
    for name, quer_ist_B in (("Länge quer (B)", True), ("gedreht, Länge in L", False)):
        lang_ri, stap_ri = (Bi, Li) if quer_ist_B else (Li, Bi)   # Richtung der Zelllänge, Richtung der Stapelung
        n_reihen = int(lang_ri // laenge)
        if n_reihen < 1:
            lage[name] = dict(reihen=0, je_reihe=None, laenge_belegt_mm=laenge, stapel_belegt_mm=None,
                              reserve_Zelllaenge_mm=lang_ri - laenge, reserve_Stapel_mm=None, passt=False,
                              reserve_L_mm=(lang_ri - laenge) if not quer_ist_B else None,
                              reserve_B_mm=(lang_ri - laenge) if quer_ist_B else None)
            continue
        je = math.ceil(S / n_reihen); st = stapel(je, dk, g)
        res_l = lang_ri - n_reihen * laenge; res_s = stap_ri - st
        lage[name] = dict(reihen=n_reihen, je_reihe=je, laenge_belegt_mm=n_reihen * laenge, stapel_belegt_mm=st,
                          reserve_Zelllaenge_mm=res_l, reserve_Stapel_mm=res_s, passt=(res_l >= 0 and res_s >= 0),
                          reserve_L_mm=res_s if quer_ist_B else res_l, reserve_B_mm=res_l if quer_ist_B else res_s)
    # beste Lage: passt, sonst kleinste Überschreitung (größtes min. Reserve)
    def guete(k):
        d = lage[k]; r = [x for x in (d["reserve_L_mm"], d["reserve_B_mm"]) if x is not None]
        return (d["passt"], min(r) if r else -1e9)
    beste = max(lage, key=guete)
    bl = lage[beste]
    res_h = Hb - H
    return dict(energie_kWh=FALL_E[fall]["LFP"], ah=ah, laenge_mm=laenge, dicke_mm=dk, innen_L_mm=Li, innen_B_mm=Bi,
                hoehe_noetig_mm=H, reserve_H_mm=res_h, lagen=lage, beste_lage=beste,
                passt_L=(bl["reserve_L_mm"] is not None and bl["reserve_L_mm"] >= 0),
                passt_B=(bl["reserve_B_mm"] is not None and bl["reserve_B_mm"] >= 0), passt_H=res_h >= 0,
                reserve_L_mm=bl["reserve_L_mm"], reserve_B_mm=bl["reserve_B_mm"],
                passt=bool(bl["passt"] and res_h >= 0))

def hex_plaetze(W, Hh, d, t):
    """Sechseckpackung, Reihen entlang W; Mittelpunkte mit Abstand >= d/2 zum Rand. Gibt (Plätze, Reihenzahl, n_gerade, n_ungerade)."""
    rp = t * math.sqrt(3) / 2
    if W < d or Hh < d: return 0, 0, 0, 0
    n_g = int((W - d) // t) + 1
    n_u = int((W - d - t / 2) // t) + 1 if W - d - t / 2 >= 0 else 0
    reihen = int((Hh - d) // rp) + 1
    gesamt = sum(n_g if i % 2 == 0 else n_u for i in range(reihen))
    return gesamt, reihen, n_g, n_u

def nmc(p, fall):
    Lb, Bb, Hb = p["bauraum"]; Li, Bi = Lb - 2 * p["rand"], Bb - 2 * p["rand"]
    d = N_["durchmesser_mm"]["wert"]; t = d + p["gap_nmc"]
    H = N_["hoehe_mm"]["wert"] + p["h_unten"] + p["h_oben"]
    o1 = hex_plaetze(Li, Bi, d, t); o2 = hex_plaetze(Bi, Li, d, t)
    (pl, reihen, n_g, n_u), richt = (o1, "Reihen entlang L") if o1[0] >= o2[0] else (o2, "Reihen entlang B")
    z = NMC_Z[fall]; res_h = Hb - H
    return dict(energie_kWh=FALL_E[fall]["NMC"], zellen=z, teilung_mm=t, innen_L_mm=Li, innen_B_mm=Bi, hoehe_noetig_mm=H,
                reserve_H_mm=res_h, plaetze_L_Reihen=o1[0], plaetze_B_Reihen=o2[0], plaetze=pl, richtung=richt,
                reihen=reihen, je_gerade_reihe=n_g, je_ungerade_reihe=n_u, belegung_prozent=100 * z / pl if pl else None,
                reserve_plaetze=pl - z, passt_Flaeche=pl >= z, passt_H=res_h >= 0, passt=bool(pl >= z and res_h >= 0))

def alle(p):
    return {"LFP": {f: lfp(p, f) for f in "AB"}, "NMC": {f: nmc(p, f) for f in "AB"}}

basis = alle(BASIS)
# Empfindlichkeit: je Annahme einzeln auf Bandenden, andere bleiben auf Basis
emp = []
for key in ("rand", "gap_lfp", "gap_nmc", "h_unten", "h_oben"):
    for w in BAND[key]:
        p = dict(BASIS); p[key] = w; r = alle(p)
        zeile = {"annahme": key, "wert": w, "basis_wert": BASIS[key], "urteil": {}, "kippt": []}
        for var in ("LFP", "NMC"):
            for f in "AB":
                u = r[var][f]["passt"]; zeile["urteil"][f"{var}_{f}"] = u
                if u != basis[var][f]["passt"]: zeile["kippt"].append(f"{var}_{f}")
        emp.append(zeile)
kipper = sorted({(z["annahme"], k) for z in emp for k in z["kippt"]})
ERG = {"hinweis": "KI-generiert (Claude Sonnet, 2026-11-17). Aus eingaben.json durch anordnung.py. Längen-Abstandsregel: n Zellen = n*Dicke + (n-1)*Abstand.",
       "basis": BASIS, "baender": BAND, "ergebnis": basis, "empfindlichkeit": emp, "kippende_annahmen": [list(k) for k in kipper]}
json.dump(ERG, open(os.path.join(D, "ergebnis.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)

# ---------- Bild
fig, axs = plt.subplots(2, 2, figsize=(15, 9.5))
Lb, Bb, Hb = BASIS["bauraum"]; r = BASIS["rand"]
def rahmen(ax, titel, extra_x=0, extra_y=0):
    ax.add_patch(Rectangle((0, 0), Lb, Bb, fill=False, ec="k", lw=1.5))
    ax.add_patch(Rectangle((r, r), Lb - 2 * r, Bb - 2 * r, fill=False, ec="red", ls="--", lw=1.5))
    ax.set_xlim(-60, Lb + 60 + extra_x); ax.set_ylim(-60, Bb + 60 + extra_y); ax.set_aspect("equal")
    ax.set_title(titel, fontsize=9); ax.set_xlabel("L [mm]"); ax.set_ylabel("B [mm]")
for i, f in enumerate("AB"):
    a = axs[i][0]; d = basis["LFP"][f]; lg = d["lagen"][d["beste_lage"]]
    ow = max(0, (lg["stapel_belegt_mm"] or 0) - d["innen_L_mm"]) if d["beste_lage"].startswith("Länge quer") else 0
    # Zeichnen: Reihen
    quer = d["beste_lage"].startswith("Länge quer")
    ex = 0; ey = 0
    if lg["reihen"] > 0:
        if quer:
            ex = max(0, lg["stapel_belegt_mm"] - d["innen_L_mm"]); ey = 0
        else:
            ey = max(0, lg["stapel_belegt_mm"] - d["innen_B_mm"])
    rahmen(a, f"LFP Fall {f}: {d['energie_kWh']:.1f} kWh, {d['ah']:.1f} Ah, Zelle {d['laenge_mm']:.0f} x {d['dicke_mm']:.0f} mm; Lage: {d['beste_lage']}; "
              f"{'passt' if d['passt'] else 'passt NICHT'}", ex, ey)
    if lg["reihen"] > 0:
        pitch = d["dicke_mm"] + BASIS["gap_lfp"]
        n_gez = 0
        for rr in range(lg["reihen"]):
            for k in range(lg["je_reihe"]):
                if n_gez >= S: break
                n_gez += 1
                if quer: x = r + k * pitch; y = r + rr * d["laenge_mm"]; w, h = d["dicke_mm"], d["laenge_mm"]
                else: x = r + rr * d["laenge_mm"]; y = r + k * pitch; w, h = d["laenge_mm"], d["dicke_mm"]
                a.add_patch(Rectangle((x, y), w, h, fc="#1f77b4", ec="white", lw=0.2, alpha=.8))
        if quer: a.annotate("", (r + lg["stapel_belegt_mm"], r - 25), (r, r - 25), arrowprops=dict(arrowstyle="<->", color="k"))
        a.text(Lb / 2, -50, f"Stapel {lg['stapel_belegt_mm']:.0f} mm gegen innen {d['innen_L_mm'] if quer else d['innen_B_mm']:.0f} mm; "
               f"Reserve L {d['reserve_L_mm']:.0f} / B {d['reserve_B_mm']:.0f} / H {d['reserve_H_mm']:.0f} mm", ha="center", fontsize=8)
    else:
        a.text(Lb / 2, Bb / 2, f"Zelllänge {d['laenge_mm']:.0f} mm > Innenmaß quer und längs", ha="center", color="red")
    a = axs[i][1]; d = basis["NMC"][f]
    rahmen(a, f"NMC Fall {f}: {d['zellen']} Zellen auf {d['plaetze']} Plätzen = {d['belegung_prozent']:.0f} % belegt; Höhe Reserve {d['reserve_H_mm']:.0f} mm; "
              f"{'passt' if d['passt'] else 'passt NICHT'}")
    dd = N_["durchmesser_mm"]["wert"]; t = d["teilung_mm"]; rp = t * math.sqrt(3) / 2
    along_L = d["richtung"] == "Reihen entlang L"
    W, Hh = (d["innen_L_mm"], d["innen_B_mm"]) if along_L else (d["innen_B_mm"], d["innen_L_mm"])
    n = 0
    for rr in range(d["reihen"]):
        cnt = d["je_gerade_reihe"] if rr % 2 == 0 else d["je_ungerade_reihe"]
        off = dd / 2 + (0 if rr % 2 == 0 else t / 2)
        for k in range(cnt):
            u = off + k * t; w_ = dd / 2 + rr * rp
            x, y = (r + u, r + w_) if along_L else (r + w_, r + u)
            n += 1
            a.add_patch(Circle((x, y), dd / 2, fc="#d95f02" if n <= d["zellen"] else "none", ec="#d95f02", lw=0.3, alpha=.85 if n <= d["zellen"] else .5))
    a.text(Lb / 2, -50, f"Innen {d['innen_L_mm']:.0f} x {d['innen_B_mm']:.0f} mm, Teilung {t:.0f} mm; leere Kreise = freie Plätze", ha="center", fontsize=8)
fig.suptitle(f"G1-Vorprüfung: Zellen im Bauraum {Lb:.0f} x {Bb:.0f} mm (schwarz), Innenrand nach Rand {r:.0f} mm gestrichelt rot (Annahme)", fontsize=11)
fig.text(0.01, 0.005, "KI-generiert (Claude Sonnet), Entwurf. Quelle: ergebnis.json. Obere Zeile Fall A, untere Zeile Fall B. LFP: so viele Zellen wie nach Rechnung gezeichnet; bei Überschreitung ragen sie über den roten Rand.", fontsize=7)
fig.tight_layout(rect=(0, 0.02, 1, 0.96)); fig.savefig(os.path.join(D, "anordnung.png"), dpi=120)

# ---------- Texte
B_ = basis
def fmt(x, n=0): return "-" if x is None else f"{x:.{n}f}"
def urteil(x): return "passt" if x else "passt nicht"
zeilen_tab = []
for var in ("LFP", "NMC"):
    for f in "AB":
        d = B_[var][f]
        if var == "LFP":
            zeilen_tab.append(f"| LFP | {f} | {d['ah']:.1f} Ah, {d['laenge_mm']:.0f} mm | {d['beste_lage']}, {d['lagen'][d['beste_lage']]['reihen']} Reihen x {d['lagen'][d['beste_lage']]['je_reihe']} | L {fmt(d['reserve_L_mm'])} / B {fmt(d['reserve_B_mm'])} / H {fmt(d['reserve_H_mm'])} | {urteil(d['passt'])} |")
        else:
            zeilen_tab.append(f"| NMC | {f} | {d['zellen']} Zellen | {d['plaetze']} Plätze ({d['richtung']}), {d['belegung_prozent']:.0f} % belegt | Plätze {d['reserve_plaetze']} / H {fmt(d['reserve_H_mm'])} | {urteil(d['passt'])} |")
tab = "| Variante | Fall | Zelle | Anordnung | Reserve in mm | Urteil |\n|---|---|---|---|---|---|\n" + "\n".join(zeilen_tab)
kipp_txt = "; ".join(f"{a} kippt {k}" for a, k in kipper) or "keine einzelne Bandänderung kippt ein Urteil"

# Abgleich mit ERWARTUNG.md
LA, LB = B_["LFP"]["A"], B_["LFP"]["B"]; NA, NB = B_["NMC"]["A"], B_["NMC"]["B"]
def lfp_a_gap05():
    p = dict(BASIS); p["gap_lfp"] = 0.5; return lfp(p, "A")
g05 = lfp_a_gap05()
abg = []
def punkt(txt, ok, ist): abg.append((txt, ok, ist))
lg = LA["lagen"]["Länge quer (B)"]
punkt("1a LFP A Länge 680-682 mm (Erwartung Nachtrag Lauf 3: 681)", 680 <= LA["laenge_mm"] <= 682, f"{LA['laenge_mm']:.1f} mm ({LA['ah']:.1f} Ah)")
punkt("1b zwei Reihen quer, 2 x Länge <= B innen (Nachtrag Lauf 3: 1362 <= 1370)", lg["reihen"] == 2 and lg["reserve_Zelllaenge_mm"] >= 0, f"{lg['reihen']} Reihen, Reserve B {lg['reserve_Zelllaenge_mm']:.0f} mm")
punkt("1c bei 1 mm Abstand passt knapp NICHT in L (125 Zellen)", (lg["je_reihe"] == 125) and (lg["reserve_Stapel_mm"] < 0), f"{lg['je_reihe']} Zellen je Reihe, Stapel {lg['stapel_belegt_mm']:.0f} mm, Reserve L {lg['reserve_Stapel_mm']:.0f} mm (Erwartung rechnete 125 x 15 = 1875; hier n*14+(n-1)*1 = {lg['stapel_belegt_mm']:.0f})")
g05l = g05["lagen"]["Länge quer (B)"]
punkt("1d bei 0,5 mm Abstand passt es", g05["passt"], f"Stapel {g05l['stapel_belegt_mm']:.0f} mm, Reserve L {g05l['reserve_Stapel_mm']:.0f} mm, passt={g05['passt']}")
punkt("1e Höhe 120 <= 130 passt", LA["passt_H"] and abs(LA["hoehe_noetig_mm"] - 120) < 1e-9, f"{LA['hoehe_noetig_mm']:.0f} mm, Reserve {LA['reserve_H_mm']:.0f} mm")
punkt("2 LFP B passt nicht (nicht verfehlt, wenn passt=False)", not LB["passt"], f"Zelle {LB['laenge_mm']:.0f} mm ({LB['ah']:.1f} Ah bei {LB['energie_kWh']} kWh; Erwartung nannte 111 Ah/790 mm), beste Lage {LB['beste_lage']}, passt={LB['passt']}")
punkt("3a NMC A Plätze 1100-1300 (Erwartung etwa 1200)", 1100 <= NA["plaetze"] <= 1300, f"{NA['plaetze']} Plätze ({NA['je_gerade_reihe']}/{NA['je_ungerade_reihe']} je Reihe, {NA['reihen']} Reihen)")
punkt("3b NMC A passt mit Reserve, rund 70 % belegt", NA["passt"] and 60 <= NA["belegung_prozent"] <= 80, f"{NA['belegung_prozent']:.0f} % belegt, passt={NA['passt']}")
punkt("3c NMC A Höhe 110 mm, 20 mm frei", abs(NA["reserve_H_mm"] - 20) < 1e-9, f"{NA['hoehe_noetig_mm']:.0f} mm, Reserve {NA['reserve_H_mm']:.0f} mm")
punkt("4 NMC B passt knapp (1085 <= etwa 1200)", NB["passt"], f"{NB['zellen']} auf {NB['plaetze']} Plätzen = {NB['belegung_prozent']:.0f} %")
punkt("5 stärkste Annahme: LFP Zellabstand/Rand, NMC Zellabstand", True, "Kipper: " + kipp_txt)
verfehlt = []
if not 680 <= LA["laenge_mm"] <= 682: verfehlt.append("LFP-Länge Fall A außerhalb 680-682 (Nachtrag Lauf 3)")
if not 1100 <= NA["plaetze"] <= 1300: verfehlt.append("NMC-Plätze außerhalb 1100-1300")
if LB["passt"]: verfehlt.append("LFP Fall B passt")
abg_txt = "\n".join(f"- {'ERFÜLLT' if ok else 'ABWEICHUNG'}: {t}. Ist: {i}" for t, ok, i in abg)
abg_txt += "\n- Verfehlte-Erwartung-Kriterien (ERWARTUNG.md): " + ("; ".join(verfehlt) if verfehlt else "keines eingetreten")

emp_txt = "| Annahme | Basis | Bandwert | kippt Urteil |\n|---|---|---|---|\n" + "\n".join(
    f"| {z['annahme']} | {z['basis_wert']} | {z['wert']} | {', '.join(z['kippt']) or '-'} |" for z in emp)

open(os.path.join(D, "ERGEBNIS.md"), "w", encoding="utf-8").write(f"""| Dok.-Nr. | ERG-G1 | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Ergebnis G1-Vorprüfung Zellanordnung | Ersteller | Claude Sonnet (KI) | Prüfer | Opus (Rohdaten) |

> **KI-generiert.** Claude Sonnet, 2026-11-17, Auftrag G1-V. Entwurf, nicht vom Menschen freigegeben. Quelle aller Zahlen: `sim/geometrie/g1_anordnung/ergebnis.json` (aus `eingaben.json` durch `anordnung.py`).

## Ergebnis (Basiswerte)
Bauraum {Lb:.0f} x {Bb:.0f} x {Hb:.0f} mm, Rand {BASIS['rand']} mm je Seite, Innen {LA['innen_L_mm']:.0f} x {LA['innen_B_mm']:.0f} mm; Höhe unten/oben {BASIS['h_unten']}/{BASIS['h_oben']} mm. Alle Randwerte sind Annahmen (`eingaben.json`).

{tab}

Reserve negativ = fehlt. LFP: Stapellänge n Zellen = n*Dicke + (n-1)*Abstand. Beide Lagen (quer und gedreht) wurden geprüft, die bessere ist angegeben. Bild: `anordnung.png`, Lesehilfe: `anordnung_lesehilfe.md`.

## Empfindlichkeit (je Annahme einzeln auf Bandende)
{emp_txt}

Kippende Annahmen: {kipp_txt}.

## Abgleich ERWARTUNG.md Punkt für Punkt
{abg_txt}

## Offene Punkte
- Die Erwartung nennt für LFP Fall B 111 Ah / etwa 790 mm; `eingaben.json` gibt E = {LB['energie_kWh']} kWh (B_LFP), das ergibt {LB['ah']:.1f} Ah / {LB['laenge_mm']:.0f} mm. Das Urteil „passt nicht“ ändert sich dadurch nicht. Opus prüft, welcher Wert gelten soll.
- Gemischte Anordnungen (Zellen in zwei Lagen, Restreihen) und Zellverbinder-/Kühlplatzbedarf sind nicht modelliert.

*KI-generiert, Entwurf. Dokument ERG-G1, Version 1.0.*
""")

open(os.path.join(D, "anordnung_lesehilfe.md"), "w", encoding="utf-8").write(f"""> **KI-generiert** (Claude Sonnet, 2026-11-17), Entwurf.

**Lesehilfe zu anordnung.png.** Das Bild zeigt von oben, wie die Zellen in den Bauraum (schwarzer Rahmen, {Lb:.0f} x {Bb:.0f} mm) passen sollen. Der rote gestrichelte Rahmen ist der nutzbare Innenraum nach Abzug von {BASIS['rand']} mm Wand je Seite (eine Annahme). Obere Zeile: Fall A ({LA['energie_kWh']} kWh), untere Zeile: Fall B. Links die LFP-Blade-Zellen (lange flache Rechtecke, stehend nebeneinander gestapelt), rechts die runden NMC-Zellen im Sechseck-Muster. Ragen blaue Zellen über den roten Rahmen, passt die Anordnung nicht. Bei NMC sind gefüllte Kreise belegte Plätze, leere Kreise freie Plätze. Ergebnis: LFP A {urteil(LA['passt'])} (Reserve in L {fmt(LA['reserve_L_mm'])} mm), LFP B {urteil(LB['passt'])}, NMC A {urteil(NA['passt'])} ({NA['belegung_prozent']:.0f} % der Plätze belegt), NMC B {urteil(NB['passt'])} ({NB['belegung_prozent']:.0f} %). Es ist eine Vorprüfung mit Annahmen für Rand und Abstände.

*KI-generiert, Entwurf, nicht vom Menschen freigegeben.*
""")

kurz = [f"G1-V Ergebnis (KI-generiert, Entwurf), Quelle sim/geometrie/g1_anordnung/ergebnis.json",
        f"LFP A: {LA['ah']:.1f} Ah, Länge {LA['laenge_mm']:.0f} mm, {urteil(LA['passt'])} (Reserve L {fmt(LA['reserve_L_mm'])}, B {fmt(LA['reserve_B_mm'])}, H {fmt(LA['reserve_H_mm'])} mm)",
        f"LFP B: {LB['ah']:.1f} Ah, Länge {LB['laenge_mm']:.0f} mm, {urteil(LB['passt'])} (beste Lage: {LB['beste_lage']}; Reserve L {fmt(LB['reserve_L_mm'])}, B {fmt(LB['reserve_B_mm'])} mm)",
        f"NMC A: {NA['zellen']} Zellen / {NA['plaetze']} Plätze = {NA['belegung_prozent']:.0f} %, {urteil(NA['passt'])}, H-Reserve {NA['reserve_H_mm']:.0f} mm",
        f"NMC B: {NB['zellen']} Zellen / {NB['plaetze']} Plätze = {NB['belegung_prozent']:.0f} %, {urteil(NB['passt'])}",
        f"LFP A bei Zellabstand 0,5 mm: {urteil(g05['passt'])}",
        f"Kippende Annahmen: {kipp_txt}",
        f"Erwartung verfehlt: {('; '.join(verfehlt)) if verfehlt else 'nein'}; Abweichung: LFP B Ah/Länge {LB['ah']:.1f}/{LB['laenge_mm']:.0f} statt 111/790 (Eingabe 93,0 kWh)",
        "Details: ERGEBNIS.md"]
open(os.path.join(D, "ERGEBNIS_kurz.txt"), "w", encoding="utf-8").write("\n".join(kurz) + "\n")

bd = os.path.join(ROOT, "praesentation", "bausteine"); os.makedirs(bd, exist_ok=True)
open(os.path.join(bd, "G1.md"), "w", encoding="utf-8").write(f"""> **KI-generiert** (Claude Sonnet, 2026-11-17), Entwurf. Folienbaustein Vorgang G1 (Vorprüfung Zellanordnung).

# Zellanordnung im Bauraum {Lb:.0f} x {Bb:.0f} x {Hb:.0f} mm
**Kernaussage (Opus): <von Opus einzusetzen>. Rechenstand: NMC-4680 Fall A {urteil(NA['passt'])} ({NA['belegung_prozent']:.0f} % der Plätze), LFP-Blade Fall A {urteil(LA['passt'])}, Fall B LFP {urteil(LB['passt'])}.**

**Bild:** sim/geometrie/g1_anordnung/anordnung.png (Zielband: Innenrand nach {BASIS['rand']} mm Wand, Annahme)

**Zahlen** (Quelle sim/geometrie/g1_anordnung/ergebnis.json):
- LFP A: {LA['ah']:.1f} Ah, Länge {LA['laenge_mm']:.0f} mm, Reserve L {fmt(LA['reserve_L_mm'])} mm
- LFP B: Länge {LB['laenge_mm']:.0f} mm, {urteil(LB['passt'])}
- NMC A: {NA['zellen']} Zellen auf {NA['plaetze']} Plätzen; NMC B: {NB['zellen']} auf {NB['plaetze']}
- Kippende Annahmen: {kipp_txt}

*KI-generiert, Entwurf.*
""")
print("\n".join(kurz))

# ---- Lauf 3 (Endzone-Längenregel, Bauraum 1950 x 1430): Vergleich mit gesichertem Lauf 2 an ERGEBNIS.md anhängen (Zahlen nur aus den ergebnis*.json) ----
_l2 = os.path.join(D, "ergebnis_lauf2.json")
if os.path.exists(_l2):
    B2 = json.load(open(_l2, encoding="utf-8"))["ergebnis"]; b2 = json.load(open(_l2, encoding="utf-8"))["basis"]
    def _z(Bx, v, f):
        x = Bx[v][f]
        return (f"{x['ah']:.1f} Ah, {x['laenge_mm']:.0f} mm, {urteil(x['passt'])} (Reserve L {fmt(x['reserve_L_mm'])} / B {fmt(x['reserve_B_mm'])})" if v == "LFP"
                else f"{x['zellen']} / {x['plaetze']} Plätze = {x['belegung_prozent']:.0f} %, {urteil(x['passt'])}")
    abschn = [f"\n## Lauf 3 (Längenregel mit fester Endzone, Bauraum {BASIS['bauraum'][0]:.0f} x {BASIS['bauraum'][1]:.0f} mm)",
              f"KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. Längenregel `laenge_regel` aus `eingaben.json`: Elektrodenlänge ∝ Ah plus feste Endzone ({L_['laenge_ref_mm']['wert'] - L_['elektrode_ref_mm']['wert']:.1f} mm). Lauf-2-Stand: `ergebnis_lauf2.json` (Bauraum {b2['bauraum'][0]:.0f} x {b2['bauraum'][1]:.0f} mm).",
              "", "| Größe | Lauf 2 | Lauf 3 |", "|---|---|---|"]
    for v, f in (("LFP", "A"), ("LFP", "B"), ("NMC", "A"), ("NMC", "B")):
        abschn.append(f"| {v} {f} | {_z(B2, v, f)} | {_z(B_, v, f)} |")
    lgA = LA["lagen"][LA["beste_lage"]]
    abschn += ["", "Abgleich mit dem Nachtrag in `ERWARTUNG.md` (Lauf 3):",
               f"1. LFP A Zelle 681 mm, zwei Reihen quer 1362 ≤ 1370 mm, Reserve B etwa 8 mm, L 16 mm: Ist {LA['laenge_mm']:.1f} mm, {lgA['reihen']} Reihen, belegt {lgA['laenge_belegt_mm']:.1f} mm, Reserve B {fmt(LA['reserve_B_mm'], 1)} mm, L {fmt(LA['reserve_L_mm'])} mm: **{'erfüllt' if 680 <= LA['laenge_mm'] <= 682 and LA['passt'] and lgA['reihen'] == 2 else 'verfehlt'}**",
               f"2. LFP B Zelle etwa 840 mm, passt weiter nicht: Ist {LB['laenge_mm']:.0f} mm, {urteil(LB['passt'])}: **{'erfüllt' if not LB['passt'] and 835 <= LB['laenge_mm'] <= 845 else 'verfehlt'}**",
               f"3. NMC etwa eine Reihe mehr (etwa 1270 Plätze), Belegung A etwa 68 %: Ist {NA['plaetze']} Plätze (Lauf 2: {B2['NMC']['A']['plaetze']}), {NA['belegung_prozent']:.0f} % belegt: **{'erfüllt' if 1250 <= NA['plaetze'] <= 1290 and 67 <= NA['belegung_prozent'] <= 70 else 'verfehlt'}** (Erwartung nannte etwa 1270, gerechnet {NA['plaetze']})",
               "Verfehlt-Kriterium des Nachtrags (LFP A passt nicht): " + ("nicht eingetreten." if LA["passt"] else "EINGETRETEN."), ""]
    with open(os.path.join(D, "ERGEBNIS.md"), "a", encoding="utf-8") as fh: fh.write("\n".join(abschn) + "\n")
