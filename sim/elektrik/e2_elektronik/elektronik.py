# KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. Auftrag E2 Punkte 1-4, 6 (Rechenteil). Werte nur aus eingaben.json.
import json, os
d = os.path.dirname(os.path.abspath(__file__)); e = json.load(open(f"{d}/eingaben.json")); out = {}
for v in ("LFP", "NMC"):
    x = e[v]; r = {}
    r["spannungsabgriffe"] = x["s"] + 1
    I_a = e["ausgleich"].get("strom_A_" + v, e["ausgleich"]["strom_A"]); r["ausgleich_strom_A"] = I_a   # NMC: ENT-146
    dQ = e["ausgleich"]["kapazitaetsunterschied"] * x["ah_reihe"]; r["ausgleich_dQ_Ah"] = dQ
    r["ausgleich_h"] = dQ / I_a
    uz = x["U_nenn_V"] / x["s"]; r["U_zelle_nenn_V"] = uz
    r["cmu_W_alle_kanaele_nenn"] = x["cmu_kanaele"] * I_a * uz
    r["cmu_W_alle_kanaele_umax"] = x["cmu_kanaele"] * I_a * e["u_max_V"][v]; r["cmu_W_umax_urteil"] = "<= 10 W" if r["cmu_W_alle_kanaele_umax"] <= e["erwartung"]["cmu_W_max"] else "> 10 W"
    C, R, U = e["vorladung"]["C_F"], e["vorladung"]["R_Ohm"], x["U_nenn_V"]
    r["vor_I_A"] = U / R; r["vor_E_J"] = 0.5 * C * U * U; r["vor_tau_ms"] = R * C * 1e3; r["vor_t95_ms"] = 3 * R * C * 1e3
    m = x["zellen"] * x["zellmasse_kg"]; r["zellmasse_kg"] = m
    h = e["heizung"]; r["heiz_E_MJ"] = m * h["c_J_kgK"] * h["dT_K"] / 1e6; r["heiz_min"] = r["heiz_E_MJ"] * 1e6 / h["P_W"] / 60
    rho = e["stoffe"]["rho_Cu_Ohm_m"]; r["hv_W_je_m_Leiter_laden"] = x["I_laden_A"] ** 2 * rho / (x["A_HV_mm2"] * 1e-6)
    r["hv_Laenge_Leiter_gesamt_m_fuer_15W"] = e["erwartung"]["hv_verlust_W_max"] / r["hv_W_je_m_Leiter_laden"]
    r["hv_verlust_W_bei_3m_5m"] = [r["hv_W_je_m_Leiter_laden"] * L for L in e["erwartung"]["hv_L_m"]]
    out[v] = r
json.dump(out, open(f"{d}/ergebnis.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps(out, indent=1))
