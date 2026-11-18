#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. Schreibt ERGEBNIS.md, k2_lesehilfe.md und den Folienbaustein aus ergebnis.json (keine Zahl von Hand)."""
import json, os
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(f"{H}/../../..")
O = json.load(open(f"{H}/ergebnis.json")); E = json.load(open(f"{H}/eingaben.json")); Z = E["ziele"]; F = O["faelle"]
def sel(fn, **kw): return [x for x in F if x["fall"] == fn and all(x[k] == v for k, v in kw.items())]
def best_h(fn): return max(sel(fn), key=lambda x: x["h_W_m2K"])
def mm(fn, k): v = [x[k] for x in sel(fn)]; return min(v), max(v)
kopf = "| Dok.-Nr. | ERG-K2 | Version | 1.0 | Status | Entwurf |\n|---|---|---|---|---|---|\n| Titel | Ergebnis K2: Kühlplatten, 1D-Hydraulik und Wärmeübergang | Ersteller | Claude Sonnet (KI) | Prüfer | Opus (offen) |\n\n> **KI-generiert** (Claude Sonnet, 2026-11-17), Entwurf, nicht von Opus geprüft. Quelle aller Zahlen: sim/kuehlung/k2_kuehlplatte/ergebnis.json (Skript kuehlplatte.py, Eingaben eingaben.json).\n\n"
s = kopf + "## 1 Eingaben\n| Fall | Wärme je Zelle | Zellen | Wärme Pack | je Platte (hälftig) | Quelle |\n|---|---|---|---|---|---|\n"
for fn, w in O["waerme"].items(): s += f"| {fn} | {w['W_je_zelle']:.2f} W | {w['zellen']} | {w['W_pack']/1000:.2f} kW | {w['W_je_platte']/1000:.2f} kW | {w['quelle']} |\n"
for v, p in O["platten"].items(): s += f"\nPlatte {v}: {p['L']*1000:.0f} x {p['B']*1000:.0f} mm, 2 Stück ({p['quelle']}). "
s += f"\nKühlmittel: ρ {E['kuehlmittel']['rho_kg_m3']}, c {E['kuehlmittel']['c_J_kgK']}, μ {E['kuehlmittel']['mu_Pa_s']*1000:.0f} mPa·s, k {E['kuehlmittel']['k_W_mK']} W/(m·K) (NEU, Annahme Sonnet, nicht in ERWARTUNG.md), Pr {O['Pr']:.1f}. Kanal 5 mm hoch, Stege 3 mm, Zuschlag 30 % (AUFTRAG).\n\n## 2 Ergebnis (Kanal 20 mm, beste Breite für h; Führung quer; alle Zeilen in ergebnis.json)\n| Fall | ΔT | Durchfluss Pack | Kanäle je Platte | Re | h [W/(m²K)] | Δp [bar] | hydr. Leistung [W] |\n|---|---|---|---|---|---|---|---|\n"
for fn in O["waerme"]:
    for x in sel(fn, breite_mm=20, fuehrung="quer"): s += f"| {fn} | {x['dT_K']} K | {x['V_pack_L_min']:.1f} L/min | {x['n_kanaele']} | {x['Re']:.0f} | {x['h_W_m2K']:.0f} | {x['dp_bar']:.4f} | {x['P_hyd_W']:.2f} |\n"
s += "\n## 3 Abgleich mit ERWARTUNG.md\n| Erwartung | Rechnung | Ergebnis |\n|---|---|---|\n"
a = sel("LFP_P0", dT_K=5)[0]; b = sel("NMC_P4", dT_K=5)[0]
s += f"| Durchfluss 5 K: LFP ≈ 47, NMC ≈ 20 L/min | LFP {a['V_pack_L_min']:.1f}, NMC (P4) {b['V_pack_L_min']:.1f} L/min | getroffen |\n"
for fn in ("LFP_P0", "NMC_P4"):
    lo, hi = mm(fn, "dp_bar"); rl, rh = mm(fn, "Re"); hl, hh = mm(fn, "h_W_m2K")
    s += f"| {fn}: Δp 0,1-0,4 bar (LFP) / < 0,1 bar (NMC) | Δp {lo:.4f} bis {hi:.4f} bar | {'LFP: weit darunter (Erwartung verfehlt, günstig)' if fn=='LFP_P0' else 'NMC: erfüllt (weit darunter)'} |\n| {fn}: Re 500-2000, h 500-1000 | Re {rl:.0f} bis {rh:.0f}, h {hl:.0f} bis {hh:.0f} W/(m²K) | **Erwartung verfehlt**; h im Verfehlt-Bereich ({'unter' if hh<300 else 'um'} 300) |\n"
s += f"\n## 4 Auswahl (kleinster Δp mit h ≥ {Z['h_min_W_m2K']})\n"
if all(v is None for v in O["auswahl"].values()): s += "**Keine Variante erfüllt h ≥ 500.** Auswahl nach AUFTRAG nicht möglich. Höchstes h je Fall (nur zur Information):\n\n"
for fn in O["waerme"]:
    x = best_h(fn); s += f"- {fn}: {x['breite_mm']} mm, {x['fuehrung']}, ΔT {x['dT_K']} K: h {x['h_W_m2K']:.0f} W/(m²K), Δp {x['dp_bar']:.4f} bar, {x['V_pack_L_min']:.1f} L/min\n"
s += "\n## 5 Deutung (Entwurf, Opus prüft)\n- Der Druckverlust ist durch die vielen parallelen Kanäle (59 bis 151 je Platte) vernachlässigbar; Zielband Δp ≤ 0,5 bar wird um mehr als zwei Größenordnungen unterschritten.\n- Die Strömung ist stark laminar (Re ≈ 30 bis 190). Dort hängt h nur von Kanalform und Kühlmittel-k ab (Nu ≈ 4-5), nicht vom Durchfluss: Mehr Pumpen hilft nicht.\n- h ≈ 260 bis 316 W/(m²K) liegt unter der K0/K1-Annahme 500, bei LFP am Rand und bei NMC im Verfehlt-Bereich unter 300. K1 rechnete mit h 500; mit den hier erreichbaren h wären die K1-Temperaturen höher (K1 Kühlfall h 500 gegen K1 Kh1000 in sim/kuehlung/k1_schnellladen/ergebnis.json). Das ist keine neue Rechnung hier.\n- Die Kühlmittelseite wirkt nur über h, die Zelle-Platte-Kette (Pad, Kontakt) ist nicht Teil von K2.\n\n## 6 Offene Fragen an Opus\n1. Wärmeleitfähigkeit Kühlmittel k = 0,40 W/(m·K) ist neu (nicht in ERWARTUNG.md). h ist proportional zu k; für h 500 bräuchte es k ≈ 0,63 (rechnerisch aus Verhältnis, ohne Neurechnung).\n2. Erwartung Re 500-2000 und h 500-1000 verfehlt. Ursache vermutlich: viele parallele Kanäle (Annahme 3 mm Stege über die ganze Plattenfläche). Für h ≥ 500 müsste Dh kleiner (schmale/flache Kanäle) oder Mikrokanal/Turbulator gewählt werden: Entscheidung Opus (keine Variante im Auftrag).\n3. K1/K3 nutzte h 500 als Annahme; soll K1 mit dem hier gerechneten h (ca. 300) wiederholt werden?\n4. Nu-Korrelation: Nu_H1 (konstanter Wärmestrom, allseitig beheizt) statt einseitiger Beheizung; Korrelationen aus dem Gedächtnis (Annahme, kein abgerufener Beleg).\n5. ΔT-Ziel ≤ 5 K ist nur beim Durchfluss 46,7 L/min (LFP) bzw. 20,1 L/min (NMC P4) erfüllt (ok_dT in ergebnis.json); die Auswahlregel allein ginge nicht darauf ein.\n6. Pumpenwirkungsgrad nicht angenommen; nur hydraulische Leistung.\n7. Kühlmittelseitige Spreizung als Beitrag zu REQ-P09 (ERWARTUNG Punkt 4): offen beim Autor, hier nicht gerechnet.\n\n## 7 Dateien\nkuehlplatte.py, eingaben.json, ergebnis.json, bilder.py, bericht.py, durchfluss_druck.png, platte_LFP.png, platte_NMC.png, k2_lesehilfe.md, praesentation/bausteine/K2.md\n\n---\n*KI-generiert (Claude Sonnet, 2026-11-17), Entwurf.*\n"
open(f"{H}/ERGEBNIS.md", "w").write(s)
l = a_ = None
lh = kopf.replace("ERG-K2", "LH-K2").replace("Ergebnis K2: Kühlplatten, 1D-Hydraulik und Wärmeübergang", "Lesehilfe zu den Bildern K2")
lh += "**Lesehilfe zu durchfluss_druck.png.** Oben der Druckverlust, unten der Wärmeübergang (h) im Kanal, jeweils über der Menge Kühlmittel, die pro Minute durch das ganze Pack fließt. Links LFP, Mitte und rechts die 4680-Zelle (NMC) in zwei Ladefällen. Jede Linie ist eine Kanalbreite (Farbe) und Führung (durchgezogen quer, gestrichelt längs); Punkte markieren die Kühlmittelerwärmung 5, 8 und 10 K. Grün ist das Zielband (Annahme aus ERWARTUNG.md): oben höchstens 0,5 bar, unten h mindestens 500. Rot ist verfehlt (über 1 bar, unter h 300). Der Druckverlust liegt weit im grünen Bereich (Achse logarithmisch), h aber im roten bis weißen Bereich unter dem Ziel. Ein höherer Durchfluss verbessert h kaum, weil die Strömung laminar ist.\n\n"
lh += "**Lesehilfe zu platte_LFP.png und platte_NMC.png.** Draufsicht auf eine der beiden Kühlplatten maßstäblich: viele parallele Kanäle (blau) zwischen Vorlauf (unten) und Rücklauf (oben), Stege weiß. Die Zahlen im Titel stammen aus ergebnis.json. Die gezeigte Variante (20 mm quer, ΔT 5 K) hat das höchste h der Rechnung und verfehlt das Ziel trotzdem.\n\n---\n*KI-generiert (Claude Sonnet, 2026-11-17), Entwurf.*\n"
open(f"{H}/k2_lesehilfe.md", "w").write(lh)
a = best_h("LFP_P0"); b = best_h("NMC_P4"); c = best_h("NMC_P3"); lo, hi = mm("LFP_P0", "dp_bar"); no, nh = mm("NMC_P4", "dp_bar")
bs = f"""> **KI-generiert** (Claude Sonnet, 2026-11-17), Entwurf. Folienbaustein Vorgang K2 (Kühlplatten: Hydraulik und Wärmeübergang).

# Kühlplatte: Druck kein Problem, Wärmeübergang ist die Grenze
**Kernaussage: Die Platten brauchen kaum Pumpendruck (LFP höchstens {hi:.3f} bar, NMC höchstens {nh:.3f} bar bei ≤ 0,5 bar Ziel), aber die laminare Strömung in den 5-mm-Kanälen liefert nur h ≈ {min(a['h_W_m2K'],b['h_W_m2K']):.0f} bis {max(a['h_W_m2K'],b['h_W_m2K'],c['h_W_m2K']):.0f} W/(m²K) statt der angenommenen 500 (Entwurf, Opus prüft).**

**Bild:** sim/kuehlung/k2_kuehlplatte/durchfluss_druck.png (Zielband dp ≤ 0,5 bar und h ≥ 500 beschriftet), platte_LFP.png, platte_NMC.png

**Zahlen** (Quelle sim/kuehlung/k2_kuehlplatte/ergebnis.json):
- Durchfluss bei ΔT 5 K: LFP {sel('LFP_P0', dT_K=5)[0]['V_pack_L_min']:.1f} L/min, NMC (P4) {sel('NMC_P4', dT_K=5)[0]['V_pack_L_min']:.1f} L/min
- Re {mm('LFP_P0','Re')[0]:.0f} bis {mm('LFP_P0','Re')[1]:.0f} (LFP), {mm('NMC_P4','Re')[0]:.0f} bis {mm('NMC_P4','Re')[1]:.0f} (NMC P4): laminar
- Beste Variante nach h: LFP {a['breite_mm']} mm {a['fuehrung']}, h {a['h_W_m2K']:.0f}; NMC {b['breite_mm']} mm {b['fuehrung']}, h {b['h_W_m2K']:.0f}; keine erreicht h ≥ 500
- Annahmen: Kühlmittel-k 0,40 (neu, Sonnet), Zuschlag 30 %, gleichmäßige Verteilung, Lehrbuchkorrelationen; Entwurf, noch nicht von Opus geprüft

*KI-generiert, Entwurf.*
"""
open(f"{R}/praesentation/bausteine/K2.md", "w").write(bs)

# Nachtrag
Nj = json.load(open(f"{H}/ergebnis_nachtrag.json")); A = Nj["auswahl"]
t = "\n\n## 8 Nachtrag (Opus-Auftrag): U_gesamt auf Plattengrundfläche und Zusatzvarianten\n"
t += "Methode (eingaben.json, Abschnitt nachtrag): h_eff = h_Kanal·(w + 2·η·H)/(w + Steg), η Rippenwirkungsgrad Steg (Al k 237, Steg 3 mm, Annahme Opus), in Reihe mit Pad 1 mm (k 3) und Blech 1,5 mm Al. Varianten: Breite 4/6/8/10/15/20 mm, Höhe 3/5 mm, Durchgänge 1/2/4/6, quer/längs, ΔT 5/8/10 K (864 Zeilen in ergebnis_nachtrag.json). k_Kühlmittel 0,40 als Annahme in eingaben.json eingetragen.\n\n"
t += "| Fall | Regel | Breite x Höhe | Durchg. | Führung | ΔT | Pack L/min | Re | h_Kanal | η | h_eff | U_gesamt | Δp bar | P_hyd W |\n|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n"
for k, x in A.items():
    fn, r = k.split("|")
    if x: t += f"| {fn} | {r} | {x['breite_mm']} x {x['hoehe_mm']} mm | {x['durchgaenge']} | {x['fuehrung']} | {x['dT_K']} K | {x['V_pack_L_min']:.1f} | {x['Re']:.0f} | {x['h_Kanal']:.0f} | {x['eta_steg']:.3f} | {x['h_eff_Grund']:.0f} | {x['U_gesamt']:.0f} | {x['dp_bar']:.4f} | {x['P_hyd_W']:.2f} |\n"
    else: t += f"| {fn} | {r} | keine Variante | | | | | | | | | | | |\n"
b0 = [x for x in Nj["faelle"] if x["fall"] == "LFP_P0" and x["hoehe_mm"] == 5 and x["breite_mm"] == 20 and x["durchgaenge"] == 1 and x["fuehrung"] == "quer" and x["dT_K"] == 5][0]
t += f"\nVergleich Basis (20 x 5 mm, quer, ΔT 5 K, LFP_P0): h_Kanal {b0['h_Kanal']:.0f}, h_eff {b0['h_eff_Grund']:.0f}, U_gesamt {b0['U_gesamt']:.0f} W/(m²K) (ergebnis_nachtrag.json). Auswahl-Regel U ≥ 500 und Δp ≤ 0,5 bar, kleinste Pumpenleistung: siehe Zeilen \"alle_dT\" (ΔT frei) und \"dT_max_5K\".\n\n"
t += "Befunde (Entwurf, Opus prüft): Die Stegfläche hebt h auf der Grundfläche etwa auf das Doppelte (η ≈ 0,99). Mit schmalen Kanälen (4 mm, 5 mm hoch) liegt U_gesamt über 500; die Obergrenze setzt das Pad (1 mm/k 3 → 3000 W/(m²K) allein). Mäander (mehr Durchgänge) bringt kein nennenswert höheres U, nur mehr Δp und Pumpenleistung; die Umlenkverluste sind darin nur über den 30-%-Zuschlag erfasst (bei 4-6 Durchgängen vermutlich zu klein, Annahme). Der Re-Anstieg bei Mäander ist reine Kanalverlängerung bei weniger parallelen Kanälen. Offene Frage: Kontaktwiderstand Zelle-Pad und Pad-Blech nicht enthalten; ΔT-Wahl (Opus/Autor); Auswahl 4 mm-Kanäle fertigungstechnisch (Stege 3 mm, 281 Kanäle je Platte) bewerten.\n\nBild: nachtrag_U_leistung.png (Zielband U ≥ 500 beschriftet). Lesehilfe in k2_lesehilfe.md.\n"
open(f"{H}/ERGEBNIS.md", "a").write(t)
open(f"{H}/k2_lesehilfe.md", "a").write("\n**Lesehilfe zu nachtrag_U_leistung.png.** Jeder Punkt ist eine Bauvariante (Farbe Kanalbreite, Kreis 5 mm Höhe, Dreieck 3 mm). Waagerecht steht die Pumpenleistung (logarithmisch, nur Varianten unter 0,5 bar), senkrecht der Gesamtwärmedurchgang von der Zelle über Pad und Blech ins Kühlmittel, bezogen auf die Plattenfläche. Oberhalb der grünen Linie (500, Annahme aus K0/K1) ist das Ziel erreicht. Je weiter links, desto weniger Pumpenleistung. Der schwarze Ring ist die Auswahl für ΔT ≤ 5 K.\n")
s_ = open(f"{R}/praesentation/bausteine/K2.md").read().replace("*KI-generiert, Entwurf.*", f"- Nachtrag (U auf Grundfläche, Quelle sim/kuehlung/k2_kuehlplatte/ergebnis_nachtrag.json): Auswahl LFP {A['LFP_P0|dT_max_5K']['breite_mm']} x {A['LFP_P0|dT_max_5K']['hoehe_mm']} mm, U {A['LFP_P0|dT_max_5K']['U_gesamt']:.0f}, {A['LFP_P0|dT_max_5K']['P_hyd_W']:.2f} W; NMC P4 U {A['NMC_P4|dT_max_5K']['U_gesamt']:.0f}, {A['NMC_P4|dT_max_5K']['P_hyd_W']:.2f} W (Bild nachtrag_U_leistung.png, Zielband U ≥ 500)\n\n*KI-generiert, Entwurf.*") if "Nachtrag" not in open(f"{R}/praesentation/bausteine/K2.md").read() else None
if s_: open(f"{R}/praesentation/bausteine/K2.md", "w").write(s_)
