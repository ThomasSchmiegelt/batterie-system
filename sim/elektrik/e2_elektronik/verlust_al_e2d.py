#!/usr/bin/env python3
# KI-generiert (Claude Sonnet, 2026-11-18), Entwurf. Auftrag E2 Fortsetzung 5, Schritt 1: Verlust der Al-Verbinder je Variante, Querschnitt aus der Akte (pm/bauteile/parameter.json BT-420 breite_mm x dicke_mm), rho_Al aus E1 (2,82e-8 Ohm m). Längen aus ergebnis_<V>_e2d.json.
# Liest: ../e1_querschnitte/eingaben.json und ergebnis.json (Strom, Stoffwerte, Methode), cad/pack/entwurf/ergebnis_<V>_e2.json (Längen aus dem CAD). Schreibt verlust_al_e2d.json.
import json, os
D = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(f"{D}/../../..")
E1i = json.load(open(f"{R}/sim/elektrik/e1_querschnitte/eingaben.json")); E1 = json.load(open(f"{R}/sim/elektrik/e1_querschnitte/ergebnis.json"))
PJ = json.load(open(f"{R}/pm/bauteile/parameter.json")); AKTE_B = PJ["parameter"]["BT-420"]["breite_mm"]["wert"]; AKTE_D = PJ["parameter"]["BT-420"]["dicke_mm"]["wert"]; AKTE_A = AKTE_B * AKTE_D
rho = E1i["stoffe"]["rho_Al_Ohm_m"]; out = {"akte_querschnitt_mm": [AKTE_B, AKTE_D], "akte_A_mm2": AKTE_A, "akte_quelle": "pm/bauteile/parameter.json BT-420 breite_mm (ENT-096), dicke_mm (ENT-097)", "rho_Al_Ohm_m": rho, "herkunft": "e1_querschnitte/eingaben.json stoffe.rho_Al_Ohm_m (Stoffwert, Opus-Auftrag 2,82e-8)"}
def R_(L_mm, A_mm2): return rho * L_mm * 1e-3 / (A_mm2 * 1e-6)
# ---------- LFP
e = json.load(open(f"{R}/cad/pack/entwurf/ergebnis_LFP_e2d.json"))["e2"]; lf = E1["lastfaelle"]["LFP"]
Id = max(lf["Laden 10-80 % (Pack)"]["pack_A"], lf["Dauer bei Entladeschluss"]["pack_A"]); Is = lf["Spitze 10 s bei Entladeschluss"]["pack_A"]
a = E1["arten"]["LFP Zell-/Reihenverbinder (BT-410/420)"]; A = AKTE_A; Lz = a["laenge_mm"]; n_link = a["stueck"] - 1   # 249 Verbinder in E1; einer davon ist jetzt der Querverbinder
st = e["stecker_lfp"]; Lq = st["querverbinder_laenge_mm"]; Aq = AKTE_A
las = st["laschen"]; 
P = {}
P["Zellverbinder (248 x L 15 mm, 25 x 3 = 75 mm2)"] = (n_link, R_(Lz, A))
P["Querverbinder Mitte (Al 25 x 3, 2 Haelften, ohne Bruecke)"] = (1, R_(Lq, Aq))
P["Anschlusslaschen Plus/Minus (Al 25 x 3)"] = (2, R_(las[0]["pfad_mm"], las[0]["querschnitt_mm2"]))
def summ(P, I): return {k: dict(stueck=n, R_uOhm=r * 1e6, verlust_W=n * I * I * r) for k, (n, r) in P.items()}
out["LFP"] = dict(strom_dauer_A=Id, strom_spitze_A=Is, dauer=summ(P, Id), spitze=summ(P, Is))
out["LFP"]["summe_dauer_W"] = sum(v["verlust_W"] for v in out["LFP"]["dauer"].values()); out["LFP"]["summe_spitze_W"] = sum(v["verlust_W"] for v in out["LFP"]["spitze"].values())
out["LFP"]["e1_vergleich_Al_dauer_W"] = a["verlust_gesamt_W"]; out["LFP"]["e1_vergleich_Al_spitze_W"] = a["verlust_spitze_gesamt_W"]
out["LFP"]["erwartung_W"] = 50.0; out["LFP"]["abweichung_prozent_gegen_erwartung_dauer"] = 100 * (out["LFP"]["summe_dauer_W"] - 50.0) / 50.0
# ---------- NMC
e = json.load(open(f"{R}/cad/pack/entwurf/ergebnis_NMC_e2d.json")); v = e["e2"]["verschaltung"]; nm = E1["lastfaelle"]["NMC"]
Id = max(nm["Laden 10-80 % (Pack)"]["pack_A"], nm["Dauer bei Entladeschluss"]["pack_A"]); Is = nm["Spitze 10 s bei Entladeschluss"]["pack_A"]
g = E1["arten"]["NMC Gruppenverbinder (BT-420)"]; z = E1["arten"]["NMC Zellabgriff (BT-410)"]
pitch_e1 = E1i["geometrie_mm"]["NMC_pitch"]["wert"]; zus = g["laenge_mm"] - 3 * pitch_e1        # E1: Sammellänge 192 = 3 Schritte + 1 Pitch (Endscheiben): gleiche Zugabe wie E1
sam = [sum(s) + zus for s in v["al_sammel_schritte_mm"]]; br = v["al_bruecken_mm"]
res = {}
for lab, Ag in (("A_E1_45mm2", g["A_mm2"]), ("A_CAD_75mm2", AKTE_A)):
    d = {}
    for nm_, I in (("dauer", Id), ("spitze", Is)):
        Vs = sum(I * I * R_(L, Ag) / 3 for L in sam); Vb = sum(I * I * R_(L, Ag) for L in br)
        d[nm_] = dict(sammel_W=Vs, bruecke_W=Vb, gruppen_W=Vs + Vb, zellabgriff_W=(z["verlust_gesamt_W"] if nm_ == "dauer" else z["verlust_spitze_gesamt_W"]))
        d[nm_]["Al_summe_W"] = d[nm_]["gruppen_W"] + d[nm_]["zellabgriff_W"]
    res[lab] = d
las_n = (R_(12.5, AKTE_A)); res["laschen_NMC_W_dauer"] = 4 * Id * Id * las_n   # 4 Laschen 25 x 25 x 3 (Pfad 12,5 mm bis zur Leitungsmitte, Querschnitt 25 x 3)
res["strom_dauer_A"] = Id; res["strom_spitze_A"] = Is; res["gruppen"] = len(sam); res["bruecken"] = len(br); res["sammel_laenge_mittel_mm"] = sum(sam) / len(sam); res["bruecke_laenge_mittel_mm"] = sum(br) / len(br); res["bruecke_laenge_max_mm"] = max(br)
res["e1_vergleich"] = dict(gruppen_dauer_W=g["verlust_gesamt_W"], gruppen_spitze_W=g["verlust_spitze_gesamt_W"], zellabgriff_dauer_W=z["verlust_gesamt_W"], al_summe_dauer_W=g["verlust_gesamt_W"] + z["verlust_gesamt_W"], al_summe_spitze_W=g["verlust_spitze_gesamt_W"] + z["verlust_spitze_gesamt_W"], summe_inkl_HV_dauer_W=E1["NMC_summe"]["verlust_W"])
res["erwartung_W"] = 385.0
for lab in ("A_E1_45mm2", "A_CAD_75mm2"): res[lab]["abweichung_prozent_Al_dauer_gegen_E1_Al"] = 100 * (res[lab]["dauer"]["Al_summe_W"] - res["e1_vergleich"]["al_summe_dauer_W"]) / res["e1_vergleich"]["al_summe_dauer_W"]; res[lab]["abweichung_prozent_Al_dauer_gegen_385"] = 100 * (res[lab]["dauer"]["Al_summe_W"] - 385.0) / 385.0
out["NMC"] = res
json.dump(out, open(f"{D}/verlust_al_e2d.json", "w"), indent=1, ensure_ascii=False); print(json.dumps(out, indent=1, ensure_ascii=False))
