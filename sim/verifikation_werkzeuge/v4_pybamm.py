#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-23), Entwurf. QN1 V4: PyBaMM mit den Parametersaetzen des Projekts (C1: sim/chemie/c1_zellmodell, gleiche params()).
(a) Konstantstromentladung C/20 bis Abschaltspannung: entnommene Ladung Q = I t (aus Strom und Zeit integriert, nicht PyBaMM-Kapazitaetsgroesse) gegen Nennkapazitaet des Satzes
    (Zielkapazitaet der Akte = 'Nominal cell capacity' im Satz); (b) SPM gegen DFN bei C/20: max |U_SPM - U_DFN| ueber gleicher entnommener Ladung.
Modell des Projekts C1: SPMe isotherm. Aufruf: python3 v4_pybamm.py"""
import json, numpy as np, pybamm
from vcommon import *
C1 = json.load(open(f"{R}/sim/chemie/c1_zellmodell/eingaben.json")); CR = w("V4_C_rate")
def params(v, fb=1.0):     # wie zellmodell.py params() (gekuerzt auf Groessen, die die Kapazitaet bestimmen)
    e = C1[v.split('_')[0]]; p = pybamm.ParameterValues("Prada2013" if v.startswith("LFP") else "Chen2020")
    p.update({"Electrode height [m]": e["elektrodenhoehe_m"], "Electrode width [m]": e["elektrodenbreite_m"]*fb,
              "Nominal cell capacity [A.h]": e["kapazitaet_ziel_Ah"], "Ambient temperature [K]": 273.15+e["T_kuehl_C"], "Initial temperature [K]": 273.15+e["T_kuehl_C"]}, check_already_exists=False)
    return p
def entlade(v, modell, fb=1.0):
    p = params(v, fb); vmin = p["Lower voltage cut-off [V]"]; Qn = p["Nominal cell capacity [A.h]"]
    m = {"SPMe": pybamm.lithium_ion.SPMe, "SPM": pybamm.lithium_ion.SPM, "DFN": pybamm.lithium_ion.DFN}[modell]({"thermal": "isothermal"})
    s = pybamm.Simulation(m, parameter_values=p, experiment=pybamm.Experiment([f"Discharge at C/{round(1/CR)} for 25 hours or until {vmin} V"], period="60 seconds"))
    sol = s.solve(initial_soc=1.0)
    t = sol["Time [s]"].entries; I = sol["Current [A]"].entries; U = sol["Terminal voltage [V]"].entries
    Q_int = float(np.trapezoid(I, t)/3600); Q_pb = float(sol["Discharge capacity [A.h]"].entries[-1])
    return dict(modell=modell, Q_integriert_Ah=Q_int, Q_pybamm_Ah=Q_pb, I_A=float(I.mean()), t_ende_h=float(t[-1]/3600), U_ende_V=float(U[-1]), Qn_Ah=Qn, vmin=vmin, t=t, I=I, U=U, Qd=np.cumsum(np.r_[0, 0.5*(I[1:]+I[:-1])*np.diff(t)])/3600)
res = {}; ok = True; kurven = {}
for v in w("V4_parametersaetze"):
    sp, df, spme = entlade(v, "SPM"), entlade(v, "DFN"), entlade(v, "SPMe")
    # Spannung ueber gleicher entnommener Ladung vergleichen (bis zur kleineren Gesamtladung)
    Qm = min(sp["Qd"][-1], df["Qd"][-1]); g = np.linspace(0, Qm, 400); dU = np.abs(np.interp(g, sp["Qd"], sp["U"])-np.interp(g, df["Qd"], df["U"]))*1000
    ab = {m["modell"]: 100*(m["Q_integriert_Ah"]/m["Qn_Ah"]-1) for m in (sp, df, spme)}
    r = dict(parametersatz="Prada2013 (Literatur)" if v == "LFP" else "Chen2020 (Literatur)", Nennkapazitaet_Ah=spme["Qn_Ah"], abschaltspannung_V=spme["vmin"], strom_A=spme["I_A"],
             ladung_Ah={m["modell"]: m["Q_integriert_Ah"] for m in (sp, df, spme)}, ladung_pybamm_Ah={m["modell"]: m["Q_pybamm_Ah"] for m in (sp, df, spme)}, abw_ladung_pct=ab,
             abw_ladung_projektmodell_SPMe_pct=ab["SPMe"], spm_dfn_dU_max_mV=float(dU.max()), spm_dfn_dU_mittel_mV=float(dU.mean()), spm_dfn_dU_bei_Q_Ah=float(g[dU.argmax()]),
             bestanden_ladung=bool(abs(ab["SPMe"]) < TOL["V4_ladung_pct"]), bestanden_spm_dfn=bool(dU.max() < TOL["V4_spm_dfn_mV"]))
    res[v] = r; ok &= r["bestanden_ladung"] and r["bestanden_spm_dfn"]
    kurven[v] = dict(SPM=(sp["Qd"].tolist(), sp["U"].tolist()), DFN=(df["Qd"].tolist(), df["U"].tolist()), SPMe=(spme["Qd"].tolist(), spme["U"].tolist()), Qn=spme["Qn_Ah"])
# Zusatz (nur Information, nicht in 'bestanden'): LFP mit Elektrodenbreite auf Zielkapazitaet skaliert (wie C1 zusatz_lfp_kap.py; Faktor aus dem eigenen LFP-Ergebnis, daher nicht unabhaengig)
f = res["LFP"]["Nennkapazitaet_Ah"]/res["LFP"]["ladung_Ah"]["SPMe"]; z = entlade("LFP", "SPMe", f)
zusatz = dict(faktor_breite=f, Q_integriert_Ah=z["Q_integriert_Ah"], abw_pct=100*(z["Q_integriert_Ah"]/z["Qn_Ah"]-1), Quelle_Vergleich="sim/chemie/c1_zellmodell/ergebnis_LFP_kap.json (93,08 Ah)")
out = dict(hinweis="KI-generiert (Claude Sonnet, 2026-11-23), Entwurf. Erzeugt von v4_pybamm.py.", pybamm=pybamm.__version__, c_rate=CR, saetze=res, zusatz_LFP_skaliert=zusatz,
           abweichung_fein_pct=max(abs(r["abw_ladung_projektmodell_SPMe_pct"]) for r in res.values()), spm_dfn_dU_max_mV=max(r["spm_dfn_dU_max_mV"] for r in res.values()), ordnung_beobachtet=None,
           toleranz_ladung_pct=TOL["V4_ladung_pct"], toleranz_spm_dfn_mV=TOL["V4_spm_dfn_mV"], bestanden=bool(ok))
speichere("V4", out); json.dump(kurven, open(f"{H}/lauf_V4_kurven.json", "w"))
