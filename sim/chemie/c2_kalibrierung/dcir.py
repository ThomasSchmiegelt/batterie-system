# KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. C2: 10-s-DCIR (50 % SOC, Entladepuls) Blade-Modell, LFP 92,4 Ah, 4680 (Chen2020, unkalibriert) gegen Band W24.
import json, numpy as np, pybamm
from kern import *
O="/home/cae/hermes/batterie/sim/chemie/c2_kalibrierung/"; B=json.load(open(O+"ergebnis_blade.json")); xf=B["x_final"]; ab=B["ocv_abbildung_verwendet"]; C1=json.load(open("/home/cae/hermes/batterie/sim/chemie/c1_zellmodell/eingaben.json"))["NMC"]
out={}
t=np.linspace(0,10,41)
def dcir_blade(breite,Q,Rfac,I,T):
    x=dict(xf); x["Rc"]=xf["Rc"]*Rfac; V,V0=puls(breite,float(np.clip(ab["a"]+ab["b"]*0.5,0.001,0.999)),I,T,t,x); return dict(R10_mOhm=float(1e3*(V0-V[-1])/I),R0_mOhm=float(1e3*(V0-V[0])/I),t_s=t.tolist(),dV=(V-V0).tolist())
for T in (-10,0,25,40):
    out[f"blade135_{T}"]=dcir_blade(B["breite_m"],135,1,135.0,T)
    out[f"lfp92_{T}"]=dcir_blade(B["breite_m"]*92.4/135,92.4,135/92.4,92.4,T)
# 4680 Chen2020 isotherm, 1C Aktenkapazitaet, 50 % SOC (wie C1)
QN=C1["kapazitaet_ziel_Ah"]
for T in (10,25,40):
    p=pybamm.ParameterValues("Chen2020"); p.update({"Electrode height [m]":C1["elektrodenhoehe_m"],"Electrode width [m]":C1["elektrodenbreite_m"],"Nominal cell capacity [A.h]":QN,"Current function [A]":QN,"Ambient temperature [K]":273.15+T,"Initial temperature [K]":273.15+T},check_already_exists=False)
    s=pybamm.Simulation(pybamm.lithium_ion.SPMe(),parameter_values=p); sol=s.solve(t,initial_soc=0.5)
    V=sol["Terminal voltage [V]"](t); U0=sol["Battery open-circuit voltage [V]"](0.0)
    out[f"n4680_{T}"]=dict(R10_mOhm=float(1e3*(U0-V[-1])/QN),R0_mOhm=float(1e3*(U0-V[0])/QN),t_s=t.tolist(),dV=(V-U0).tolist())
for k,v in out.items(): print(k,round(v["R10_mOhm"],3))
json.dump(out,open(O+"ergebnis_dcir.json","w"),indent=1)
