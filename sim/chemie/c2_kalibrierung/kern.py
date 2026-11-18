# KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. C2: Hilfsfunktionen Pulsrechnung Blade.
import numpy as np, pybamm, pandas as pd
from parameter_blade import *
_m=pybamm.lithium_ion.SPMe({"contact resistance":"true"}); _sims={}
def sim(breite):
    if breite not in _sims:
        _sims[breite]=pybamm.Simulation(_m,parameter_values=blade_params(breite),solver=pybamm.IDAKLUSolver(rtol=1e-6,atol=1e-8))
    return _sims[breite]
def basis(): return dict(Iin=0.0,Rc=0.0,fk=1.0,fjp=1.0,fjn=1.0,fDp=1.0,fDn=1.0,fTk=1.0,fTDp=1.0,fTDn=1.0)
def puls(breite,soc_m,I_A,T_C,teval,x):
    """x: dict Rc,fk,fjp,fjn,fDp,fDn,Ea_k,Ea_Dp,Ea_Dn. Rueckgabe V(t), V0 (OCV). Entladung I_A>0."""
    c0n,c0p=stoich(soc_m); inp=basis(); inp.update(dict(Iin=I_A,Rc=x["Rc"]*arr(x.get("Ea_Rc",0),T_C),fk=x["fk"],fjp=x["fjp"],fjn=x["fjn"],fDp=x["fDp"],fDn=x["fDn"],
        fTk=arr(x.get("Ea_k",0),T_C),fTDp=arr(x.get("Ea_Dp",0),T_C),fTDn=arr(x.get("Ea_Dn",0),T_C),c0n=c0n,c0p=c0p))
    s=sim(breite); s.parameter_values  # noqa
    s.model  # noqa
    sol=s.solve(np.asarray(teval,float),inputs=inp)
    V=sol["Terminal voltage [V]"](teval)
    i0=dict(inp); i0["Iin"]=0.0; sol0=s.solve(np.array([0.0,1.0]),inputs=i0); V0=float(sol0["Terminal voltage [V]"](0.0))
    return np.asarray(V),V0
