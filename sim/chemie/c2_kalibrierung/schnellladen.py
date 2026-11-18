# KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. C2 Schritt 4: Schnellladen LFP (2,1C) und 4680 (CC-CV, Startstrom-Scan, Plating-Pruefung). Eingaben nur aus eingaben.json / ergebnis_blade.json / C1-eingaben.json.
import json, numpy as np, pybamm, time, sys
from kern import *
O="/home/cae/hermes/batterie/sim/chemie/c2_kalibrierung/"; C1=json.load(open("/home/cae/hermes/batterie/sim/chemie/c1_zellmodell/eingaben.json"))
MODE=sys.argv[1]  # lfp | n4680
if MODE=="lfp": B=json.load(open(O+"ergebnis_blade.json")); xf=B["x_final"]; ab=B["ocv_abbildung_verwendet"]
res={"start":time.strftime("%Y-%m-%d %H:%M:%S")}
if MODE=='lfp':
    # ---------- LFP 92,4 Ah (Blade-Satz, nur Flaeche skaliert), 2,1C von 10 auf 80 %
    bL=B["breite_m"]*92.4/135.0; QL=92.4; I=2.1*QL
    c0n,c0p=stoich(float(np.clip(ab["a"]+ab["b"]*0.10,0.001,0.999)))
    p=blade_params(bL); p.update({"Nominal cell capacity [A.h]":QL},check_already_exists=False)
    m=pybamm.lithium_ion.SPMe({"contact resistance":"true"})
    inp=basis(); inp.update(dict(Rc=xf["Rc"]*135/92.4 if False else xf["Rc"],fk=xf["fk"],fjp=xf["fjp"],fjn=xf["fjn"],fDp=xf["fDp"],fDn=xf["fDn"],
        fTk=arr(xf["Ea_k"],25),fTDp=arr(xf["Ea_Dp"],25),fTDn=arr(xf["Ea_Dn"],25),c0n=c0n,c0p=c0p))
    # Kontaktwiderstand ist an die 135-Ah-Zelle gebunden; fuer die kleinere Zelle Skalierung 135/92,4 (Annahme: Widerstand ~ 1/Flaeche)
    inp["Rc"]=xf["Rc"]*135/92.4
    s=pybamm.Simulation(m,parameter_values=p,experiment=pybamm.Experiment([f"Charge at {I:.4f} A for 40 minutes or until 3.65 V","Hold at 3.65 V for 60 minutes"]),solver=pybamm.CasadiSolver(mode="safe"))
    sol=s.solve(initial_soc=None,inputs=inp) if False else s.solve(inputs=inp)
    t=sol["Time [s]"].entries; Vv=sol["Terminal voltage [V]"].entries; Iv=sol["Current [A]"].entries; Qd=sol["Discharge capacity [A.h]"].entries; U0=sol["Battery open-circuit voltage [V]"].entries
    Qch=-(Qd-Qd[0]); k=int(np.argmax(Qch>=0.7*QL)) if (Qch>=0.7*QL).any() else len(t)-1
    qh=np.abs(Iv)*np.abs(U0-Vv)
    kcc=int(np.argmax(Vv>=3.65-1e-3)) if (Vv>=3.65-1e-3).any() else len(t)-1
    res["LFP"]=dict(CC_ende_min=float(t[kcc]/60),waerme_mittel_CC_W=float(np.trapezoid(qh[:kcc+1],t[:kcc+1])/t[kcc]),Q_Ah_ende_CC=float(Qch[kcc]),Q_Ah_ende_Lauf=float(Qch[-1]),t_ende_min=float(t[-1]/60),strom_A=I,C_rate=2.1,Q_nenn_Ah=QL,zeit_10_80_min=float(t[k]/60),erreicht_80=bool((Qch>=0.7*QL).any()),U_max_V=float(Vv.max()),U_Ende_V=float(Vv[k]),
        waerme_mittel_W=float(np.trapezoid(qh[:k+1],t[:k+1])/t[k]),waerme_max_W=float(qh[:k+1].max()),I_A_kurve=Iv[:k+1][::10].tolist(),t_s=t[:k+1][::10].tolist(),U_V=Vv[:k+1][::10].tolist(),
        Q_h_W=qh[:k+1][::10].tolist(),Q_Ah=Qch[:k+1][::10].tolist(),
        anpassung="Rc auf 135/92,4 skaliert (Annahme: Widerstand ~ 1/Flaeche); Breite = Blade-Breite*92,4/135")
    json.dump(res,open(O+"ergebnis_schnellladen_lfp.json","w"),indent=1)
    print("LFP",{k_:v for k_,v in res["LFP"].items() if not isinstance(v,list)},flush=True)
if MODE=='n4680':
    # ---------- 4680 (Chen2020, C1-Geometrie), CC-CV Startstrom-Scan, lumped thermisch wie C1
    e=C1["NMC"]; QN=e["kapazitaet_ziel_Ah"]; Umax=4.3  # W20 Spannungsfenster 4680 2,5-4,3 V (bestanden)
    def pN():
        p=pybamm.ParameterValues("Chen2020")
        p.update({"Electrode height [m]":e["elektrodenhoehe_m"],"Electrode width [m]":e["elektrodenbreite_m"],
          "Cell volume [m3]":e["elektrodenhoehe_m"]*e["elektrodenbreite_m"]*sum(p.get(k,0) for k in ("Negative current collector thickness [m]","Negative electrode thickness [m]","Separator thickness [m]","Positive electrode thickness [m]","Positive current collector thickness [m]")),
          "Cell cooling surface area [m2]":e["kuehlflaeche_m2"],"Total heat transfer coefficient [W.m-2.K-1]":e["h_W_m2K"],"Nominal cell capacity [A.h]":QN,
          "Ambient temperature [K]":273.15+25,"Initial temperature [K]":273.15+25,"Upper voltage cut-off [V]":Umax},check_already_exists=False)
        p.set_initial_state if False else None
        return p
    rN=[]
    for Cr in (1.0,1.3,1.5,1.7,1.8,1.9,2.0,2.3):
        p=pN(); I0=Cr*QN
        m=pybamm.lithium_ion.SPMe({"thermal":"lumped"})
        ex=pybamm.Experiment([f"Charge at {I0:.4f} A until {Umax} V",f"Hold at {Umax} V for 40 minutes"])
        s=pybamm.Simulation(m,parameter_values=p,experiment=ex,solver=pybamm.CasadiSolver(mode='safe'))
        try: sol=s.solve(initial_soc=0.10)
        except Exception as ex_: print("fehler",Cr,ex_,flush=True); continue
        t=sol["Time [s]"].entries; Qd=sol["Discharge capacity [A.h]"].entries; Qch=-(Qd-Qd[0]); Iv=sol["Current [A]"].entries; Vv=sol["Terminal voltage [V]"].entries
        ph=sol["Negative electrode surface potential difference at separator interface [V]"].entries.min(axis=0) if sol["Negative electrode surface potential difference at separator interface [V]"].entries.ndim>1 else sol["Negative electrode surface potential difference at separator interface [V]"].entries
        U0=sol["Battery open-circuit voltage [V]"].entries; Qtot=sol["Total heating [W]"].entries; Tc=sol["Volume-averaged cell temperature [C]"].entries
        ok=(Qch>=0.7*QN).any(); k=int(np.argmax(Qch>=0.7*QN)) if ok else len(t)-1
        cv=np.where(Vv>=Umax-1e-3)[0]; tcv=float(t[cv[0]]) if len(cv) else None
        r=dict(C_start=Cr,I_start_A=I0,erreicht_80=bool(ok),zeit_10_80_min=float(t[k]/60),CV_beginn_s=tcv,phi_an_min_V=float(ph[:k+1].min()),phi_an_min_CC_V=float(ph[:max(1,(cv[0] if len(cv) else k))].min()),
           waerme_mittel_gesamt_W=float(np.trapezoid(Qtot[:k+1],t[:k+1])/t[k]),waerme_mittel_IdU_W=float(np.trapezoid((np.abs(Iv)*np.abs(U0-Vv))[:k+1],t[:k+1])/t[k]),T_max_C=float(Tc[:k+1].max()),abbruch=str(sol.termination),t_ende_s=float(t[-1]),solver_ok=bool(t[-1]>=39*60 or ok),
           t_s=t[:k+1][::5].tolist(),I_A=Iv[:k+1][::5].tolist(),U_V=Vv[:k+1][::5].tolist(),phi_an_V=ph[:k+1][::5].tolist(),Q_Ah=Qch[:k+1][::5].tolist(),Q_W=Qtot[:k+1][::5].tolist())
        rN.append(r); print({k_:v for k_,v in r.items() if not isinstance(v,list)},flush=True)
    res["N4680"]=rN; res["N4680_Umax_V"]=Umax
    json.dump(res,open(O+f"ergebnis_schnellladen_{MODE}.json","w"),indent=1); print("fertig",time.strftime("%H:%M:%S"))
