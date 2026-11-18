# KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. C1 Zellmodell PyBaMM. Alle Eingaben aus eingaben.json.
import copy,json, sys, numpy as np, pybamm
import copy
H = json.load(open("eingaben.json")); out = {}
H["LFP_kap"]=copy.deepcopy(H["LFP"]); H["LFP_kap"]["elektrodenbreite_m"]*=1.9000655904422978; H["LFP_kap"]["kapazitaet_ziel_Ah"]=H["LFP"]["kapazitaet_ziel_Ah"]; H["zellvolumen_m3"]["LFP_kap"]=H["zellvolumen_m3"]["LFP"]
TH = "isothermal"
def params(v):
    e = H[v]; p = pybamm.ParameterValues("Prada2013" if v.startswith("LFP") else "Chen2020")
    p.update({"Electrode height [m]": e["elektrodenhoehe_m"], "Electrode width [m]": e["elektrodenbreite_m"],
              "Cell volume [m3]": e["elektrodenhoehe_m"]*e["elektrodenbreite_m"]*sum(p.get(k,0) for k in ("Negative current collector thickness [m]","Negative electrode thickness [m]","Separator thickness [m]","Positive electrode thickness [m]","Positive current collector thickness [m]")), "Cell cooling surface area [m2]": e["kuehlflaeche_m2"],
              "Total heat transfer coefficient [W.m-2.K-1]": e["h_W_m2K"],
              "Nominal cell capacity [A.h]": e["kapazitaet_ziel_Ah"], "Ambient temperature [K]": 273.15+e["T_kuehl_C"], "Initial temperature [K]": 273.15+e["T_kuehl_C"]},
             check_already_exists=False)
    return p
def model(th="isothermal"):
    return pybamm.lithium_ion.SPMe({"thermal": th})
def sim(v, exp, th="isothermal", T=None):
    p = params(v)
    if T is not None:
        p.update({"Ambient temperature [K]":273.15+T,"Initial temperature [K]":273.15+T}, check_already_exists=False)
    s = pybamm.Simulation(model(th), parameter_values=p, experiment=exp)
    return s
for v in ("LFP_kap",):
    e = H[v]; p = params(v); vmax = p["Upper voltage cut-off [V]"]; vmin = p["Lower voltage cut-off [V]"]; r = {}
    # C/20-Kapazitaet (entladen von voll)
    m = model("isothermal"); s = pybamm.Simulation(m, parameter_values=p, experiment=pybamm.Experiment([f"Discharge at C/20 for 25 hours or until {vmin} V"]))
    sol = s.solve(initial_soc=1.0); Qm = float(sol["Discharge capacity [A.h]"].entries[-1])
    r["kapazitaet_C20_Ah"] = Qm; r["kapazitaet_ziel_Ah"] = e["kapazitaet_ziel_Ah"]; r["abw_prozent"] = 100*(Qm/e["kapazitaet_ziel_Ah"]-1)
    print(v, "Kapazitaet", Qm, flush=True)
    # Schnellladen 10->80 %: Strom = C * Aktenkapazitaet; SOC-Fenster ueber Modellkapazitaet
    I = e["C_rate_schnell"]*e["kapazitaet_ziel_Ah"]; r["strom_A"] = I
    tcc = 0.7*Qm/I*3600
    exp = pybamm.Experiment([(f"Charge at {I} A for {int(tcc*1.0)+1} s or until {vmax} V", f"Hold at {vmax} V for {int(tcc*2)} s or until C/20")],period="10 seconds")
    s = sim(v, exp, th=TH); sol = s.solve(initial_soc=0.1)
    t = sol["Time [s]"].entries; Iv = sol["Current [A]"].entries
    ahin = np.concatenate([[0],np.cumsum(-0.5*(Iv[1:]+Iv[:-1])*np.diff(t))])/3600  # Laden: Strom negativ in PyBaMM
    soc = 0.1 + np.abs(ahin)/Qm
    k = int(np.argmax(soc>=0.8)) if soc.max()>=0.8 else len(t)-1
    sl = slice(0,k+1)
    def q(n): return sol[n].entries
    Qt, Qirr, Qrev = q("Total heating [W]")[sl], (q("Ohmic heating [W]")+q("Irreversible electrochemical heating [W]"))[sl], q("Reversible heating [W]")[sl]
    Vv = q("Terminal voltage [V]")[sl]; Tv = q("Volume-averaged cell temperature [K]")[sl]-273.15
    tt = t[sl]
    cv_start = int(np.argmax(Vv>=vmax-1e-3)) if (Vv>=vmax-1e-3).any() else None
    r["schnellladen"] = {"t_s":tt.tolist(),"I_A":np.abs(Iv[sl]).tolist(),"U_V":Vv.tolist(),"soc":soc[sl].tolist(),"Q_gesamt_W":Qt.tolist(),"Q_irr_W":Qirr.tolist(),"Q_rev_W":Qrev.tolist(),"T_C":Tv.tolist(),"Q_pruef_W":(np.abs(Iv[sl])*np.abs(q("Terminal voltage [V]")[sl]-q("Battery open-circuit voltage [V]")[sl])).tolist(),
        "soc_ende":float(soc[k]),"dauer_min":float(tt[-1]/60),"ziel_dauer_CC_min":tcc/60,"CV_beginn_s":(None if cv_start is None else float(tt[cv_start])),
        "Q_mittel_W":float(np.trapezoid(Qt,tt)/tt[-1]),"Q_irr_mittel_W":float(np.trapezoid(Qirr,tt)/tt[-1]),"Q_rev_mittel_W":float(np.trapezoid(Qrev,tt)/tt[-1]),
        "Q_max_W":float(Qt.max()),"T_ende_C":float(Tv[-1]),"U_max_V":float(Vv.max()),"vmax_erreicht": bool(cv_start is not None)}
    print(v,"laden",{k_:x for k_,x in r["schnellladen"].items() if not isinstance(x,list)},flush=True)
    # DCIR 10 s Puls bei 50 % SOC
    r["dcir"]={}
    for Tc in H["dcir"]["T_C"]:
        Ip = e["kapazitaet_ziel_Ah"]*1.0
        try:
            exp = pybamm.Experiment([f"Discharge at {Ip} A for {H['dcir']['puls_s']} s"],period="1 second")
            s = sim(v, exp, th="isothermal", T=Tc); sol = s.solve(initial_soc=0.5)
            U = sol["Terminal voltage [V]"].entries; t0 = sol["Time [s]"].entries
            # Ruhespannung zu t=0 (vor Strom) ueber OCV bei 50 %: Spannung bei t=0 enthaelt schon Strom -> eigener Nullstromlauf
            exp0 = pybamm.Experiment(["Rest for 1 second"],period="1 second")
            s0 = sim(v, exp0, th="isothermal", T=Tc); U0 = float(s0.solve(initial_soc=0.5)["Terminal voltage [V]"].entries[0])
            r["dcir"][str(Tc)] = {"U0_V":U0,"U10s_V":float(U[-1]),"I_A":Ip,"R_10s_mOhm":float((U0-U[-1])/Ip*1000),"t_s":t0.tolist(),"U_V":U.tolist()}
            print(v,"DCIR",Tc,r["dcir"][str(Tc)]["R_10s_mOhm"],flush=True)
        except Exception as ex:
            r["dcir"][str(Tc)] = {"fehler":str(ex)[:300]}; print(v,"DCIR Fehler",Tc,ex,flush=True)
    out[v]=r
json.dump(out,open("ergebnis_LFP_kap.json","w"))
