# KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. C2: Parametersatz BYD Blade 135 Ah (Herkunft siehe eingaben.json).
import json, numpy as np, pybamm
E=json.load(open("/home/cae/hermes/batterie/sim/chemie/c2_kalibrierung/eingaben.json"))["blade"]
IN=["Iin","Rc","fk","fjp","fjn","fDp","fDn","fTk","fTDp","fTDn","c0n","c0p"]   # Eingaben (kalibrierbar bzw. je Puls gesetzt)
def blade_params(breite_m=None):
    p=pybamm.ParameterValues("Prada2013")
    I=lambda n: pybamm.InputParameter(n)
    k0=p["Electrolyte conductivity [S.m-1]"]; jp0=p["Positive electrode exchange-current density [A.m-2]"]; jn0=p["Negative electrode exchange-current density [A.m-2]"]
    upd={"Electrode height [m]":E["elektrodenhoehe_m"],"Electrode width [m]":breite_m or 1.0,
         "Upper voltage cut-off [V]":E["U_max_V"],"Lower voltage cut-off [V]":E["U_min_V"],
         "Nominal cell capacity [A.h]":E["kapazitaet_Ah"],"Current function [A]":I("Iin"),"Contact resistance [Ohm]":I("Rc"),
         "Electrolyte conductivity [S.m-1]":lambda c,T: k0(c,T)*I("fk")*I("fTk"),
         "Positive electrode exchange-current density [A.m-2]":lambda ce,cs,cm,T: jp0(ce,cs,cm,T)*I("fjp"),
         "Negative electrode exchange-current density [A.m-2]":lambda ce,cs,cm,T: jn0(ce,cs,cm,T)*I("fjn"),
         "Positive particle diffusivity [m2.s-1]":5.9e-18*I("fDp")*I("fTDp"),
         "Negative particle diffusivity [m2.s-1]":3e-15*I("fDn")*I("fTDn"),
         "Initial concentration in negative electrode [mol.m-3]":I("c0n"),"Initial concentration in positive electrode [mol.m-3]":I("c0p")}
    p.update(upd,check_already_exists=False); return p
def stoich(soc):
    p=pybamm.ParameterValues("Prada2013"); p.set_initial_stoichiometries(soc)
    return float(p["Initial concentration in negative electrode [mol.m-3]"]),float(p["Initial concentration in positive electrode [mol.m-3]"])
def arr(Ea,T_C): return float(np.exp(Ea/8.314*(1/298.15-1/(273.15+T_C))))
