#!/usr/bin/env python3
"""E3c Ergebnisse zusammenführen -> ergebnis_platine.json. KI-generiert (Claude Sonnet, 2026-11-24), Entwurf.
Masse: Dichten FR4 1,85 g/cm3, Cu 8,96 g/cm3 und Bauteilmassen R_0603/C_0603/SOT-23 aus ERWARTUNG e3_platine Nachtrag 6 (Annahme Opus); alle übrigen Bauteile = STEP-Volumen x 1,4 g/cm3
(Methode Nachtrag 6 für Stecker, hier auf alle Bauteile ausgedehnt: Sonnet, zur Bestätigung durch Opus). Kupfer 70 um auf allen Lagen (wie E3, Annahme). Keine Abzüge für Überlappungen (obere Schranke)."""
import json, re, pathlib
H = pathlib.Path(__file__).resolve().parent; R = H.parents[2]; O = pathlib.Path("/home/cae/cae_projekte/batterie/e3c")
pr = json.load(open(H / "_pruefung_roh.json")); mv = json.load(open(H / "_modellvolumen.json")); drc = json.load(open(O / "bms_drc.json")); info = json.load(open(H / "layout_info.json"))
kr = json.load(open(H / "ergebnis_kriechstrecke.json")); par = json.load(open(R / "pm/bauteile/parameter.json"))["parameter"]; bt = json.load(open(O / "bauteile.json"))
pk = json.load(open(R / "cad/pack/entwurf/ergebnis_LFP_e2d_e3.json"))["e2"]
RHO_FR4, RHO_CU, RHO_BT = 1.85e-3, 8.96e-3, 1.4e-3; T_CU, T_BOARD = 0.07, 1.6
MT = {"R_0603_1608Metric": 0.005, "C_0603_1608Metric": 0.005, "SOT-23": 0.01}   # g je Stück, Nachtrag 6
acu = {n: sum(d.values()) for n, d in pr["flaeche_cu_mm2"].items()}; vcu = sum(acu.values()) * T_CU
area = info["platine_mm"][0] * info["platine_mm"][1]
m_cu = vcu * RHO_CU; m_fr4 = (area * T_BOARD - vcu) * RHO_FR4
bauteile = {}; offen = []
for fp, k in pr["footprints"].items():
    if fp in MT: bauteile[fp] = k * MT[fp]
    elif fp in mv["volumen_mm3"]: bauteile[fp] = k * mv["volumen_mm3"][fp] * RHO_BT
    else: offen.append(f"{k}x {fp}")
m_bt = sum(bauteile.values())
b310 = {m: par["BT-310"][m]["wert"] for m in ("laenge_mm", "breite_mm", "hoehe_mm")}
hoehe = bt["step_bbox"][5] - bt["platine_bbox"][2]
L, B = info["platine_mm"]
res = dict(variante="BMS BT-311", laenge_mm=L, breite_mm=B, lagen=info["lagen"], teile=pr["teile"], teile_nach_footprint=pr["footprints"], bahnsegmente=pr["bahnsegmente"], vias=pr["vias"],
  drc_verstoesse=len(drc["violations"]), drc_unverbunden=len(drc["unconnected_items"]),
  passt=dict(bt310_mm=b310, platine_h_mm=round(hoehe, 2), laenge_ok=L <= b310["laenge_mm"], breite_ok=B <= b310["breite_mm"], hoehe_ok=hoehe <= b310["hoehe_mm"],
             schaltbox_innen_mm=[pk["schaltbox_wanne_L_mm"], pk["schaltbox_wanne_B_mm"], pk["schaltbox_innenhoehe_mm"]], quelle="parameter.json BT-310 (ENT-139/140/141); ergebnis_LFP_e2d_e3.json e2.schaltbox_*"),
  sperrzone=dict(x_mm=pr["sperrzone_x_mm"], breite_mm=pr["sperrzone_breite_mm"], laenge_mm=B, objekte_in_sperrzone=pr["objekte_in_sperrzone"], abstand_nv_hv_kupfer_mm=pr["abstand_nv_hv_kupfer_mm"],
                 nv_kupfer_max_x_mm=pr["nv_kupfer_max_x_mm"], hv_kupfer_min_x_mm=pr["hv_kupfer_min_x_mm"], bruecken=pr["bruecken"], kriech_mm=kr["hv_nv"]["kriech_mm"], luft_mm=kr["hv_nv"]["luft_mm"], kriech_ge_luft=kr["hv_nv"]["ok"]),
  masse=dict(fr4_g=round(m_fr4, 2), kupfer_g=round(m_cu, 2), bauteile_g=round(m_bt, 2), gesamt_g=round(m_fr4 + m_cu + m_bt, 2), bauteile_je_footprint_g={k: round(v, 3) for k, v in bauteile.items()}, nicht_angesetzt=offen,
             cu_flaeche_mm2={n: round(v, 1) for n, v in acu.items()}, quelle="bms_pruefung.py -> _pruefung_roh.json; bms_masse_modelle.py -> _modellvolumen.json; Dichten ERWARTUNG e3_platine Nachtrag 6"))
json.dump(res, open(H / "ergebnis_platine.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps({k: v for k, v in res.items() if k not in ("teile_nach_footprint",)}, ensure_ascii=False)[:1800])
