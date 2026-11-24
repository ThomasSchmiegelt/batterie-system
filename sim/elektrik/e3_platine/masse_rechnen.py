# KI-generiert (Claude Sonnet, 2026-11-24), Entwurf. Masse aus _masse_roh_<V>.json (masse_platine.py) und Nachtrag 6 der ERWARTUNG.md -> ergebnis_platine.json[V]["masse"].
import json
H = "/home/cae/hermes/batterie/sim/elektrik/e3_platine"
RHO_FR4, RHO_CU, RHO_CONN, RHO_PAD = 1.85e-3, 8.96e-3, 1.4e-3, 3e-3   # g/mm3 (Nachtrag 6; Pad ENT-185 Annahme 3 g/cm3)
T_CU, T_PAD, T_BOARD = 0.07, 1.0, 1.6                                    # mm (70 um außen ERWARTUNG; Pad ENT-185; 1,6 mm ENT-167)
VOL_CONN = {"Hirose_FH12-24S-0.5SH_1x24-1MP_P0.50mm_Horizontal": 164.221, "JST_SH_SM02B-SRSS-TB_1x02-1MP_P1.00mm_Horizontal": 31.639}  # mm3, STEP-Modelle KiCad-Bibliothek (vol.py)
MT = {"R_2512_6332Metric": 0.045, "R_0603_1608Metric": 0.005, "C_0603_1608Metric": 0.005, "SOT-23": 0.01, "LQFP-64_10x10mm_P0.5mm": 0.35, "SOT-363_SC-70-6": 0.006, "TSSOP-16_4.4x5mm_P0.65mm": 0.06, "LQFP-80_12x12mm_P0.5mm": 0.45, "SOIC-16W_7.5x10.3mm_P1.27mm": 1.0}
P = json.load(open(f"{H}/ergebnis_platine.json"))
for V in ("LFP", "NMC"):
    r = json.load(open(f"{H}/_masse_roh_{V}.json")); acu = {n: sum(d.values()) for n, d in r["flaeche_cu_mm2"].items()}
    aussen = sum(v for n, v in acu.items() if n in ("F.Cu", "B.Cu")); innen = sum(v for n, v in acu.items() if n.startswith("In"))
    vcu = (aussen + innen) * T_CU; m_cu = vcu * RHO_CU; m_fr4 = (r["platine_flaeche_mm2"] * T_BOARD - vcu) * RHO_FR4
    m_cu_aussen = aussen * T_CU * RHO_CU
    bt = {}; offen = []
    for fp, k in r["footprints"].items():
        if fp in MT: bt[fp] = k * MT[fp]
        elif fp in VOL_CONN: bt[fp] = k * VOL_CONN[fp] * RHO_CONN
        else: offen.append(f"{k}x {fp}")
    m_bt = sum(bt.values()); m_pad = r["platine_flaeche_mm2"] * T_PAD * RHO_PAD
    P[V]["masse"] = dict(fr4_g=round(m_fr4, 2), kupfer_g=round(m_cu, 2), kupfer_nur_aussen_g=round(m_cu_aussen, 2), bauteile_g=round(m_bt, 2), platine_ohne_pad_g=round(m_fr4 + m_cu + m_bt, 2),
        pad_g=round(m_pad, 2), gesamt_mit_pad_g=round(m_fr4 + m_cu + m_bt + m_pad, 2),
        cu_flaeche_mm2={n: round(v, 1) for n, v in acu.items()}, cu_anteil_je_lage={n: round(v / r["platine_flaeche_mm2"], 3) for n, v in acu.items()}, bauteile_je_footprint_g={k: round(v, 3) for k, v in bt.items()},
        nicht_angesetzt=offen, quelle="masse_platine.py -> _masse_roh_%s.json; Dichten und Bauteilmassen ERWARTUNG.md Nachtrag 6 und 8 (N8: SOT-363 0,006 g, TSSOP-16 0,06 g, LQFP-80 0,45 g)" % V)
    t = json.load(open(f"{H}/thermovias_{V}.json")); P[V]["thermovias"] = t
json.dump(P, open(f"{H}/ergebnis_platine.json", "w"), indent=1, ensure_ascii=False)
for V in ("LFP", "NMC"): print(V, json.dumps({k: v for k, v in P[V]["masse"].items() if k.endswith("_g") or k == "nicht_angesetzt"}, ensure_ascii=False), P[V]["thermovias"])
