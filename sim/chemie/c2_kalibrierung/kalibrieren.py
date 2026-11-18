# KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. C2 Schritt 3: Blade-Kalibrierung (a) OCV/Kapazitaet, (b) 10-s-Puls 25 C, (c) Temperatur.
import json, numpy as np, pandas as pd, pybamm, sys, time
from scipy.optimize import least_squares
from kern import *
O="/home/cae/hermes/batterie/sim/chemie/c2_kalibrierung/"; W=np.load("/home/cae/cae_projekte/batterie/c2/blade_wellen.npz")
R=pd.read_csv(O+"blade_pulse.csv"); R=R[(R.I_A<-250)].copy()
# Sweeps: neuer Sweep, wenn SOC gegenueber Vorgaenger steigt
R["sweep"]=0
for k,g in R.groupby("satz"):
    sw=np.cumsum(np.r_[0,(np.diff(g.SOC.values)>0.2)]); R.loc[g.index,"sweep"]=sw
out={"start":time.strftime("%Y-%m-%d %H:%M:%S")}
# --- Breite auf 135 Ah (C/20, Prada-Fenster 2,6 V) skalieren
c0n,c0p=stoich(1.0); breite=130.0
for it in range(2):
    s=pybamm.Simulation(pybamm.lithium_ion.SPMe({"contact resistance":"true"}),parameter_values=blade_params(breite),solver=pybamm.IDAKLUSolver())
    inp=basis(); inp.update(Iin=135/20,c0n=c0n,c0p=c0p); sol=s.solve(np.linspace(0,3600*30,3000),inputs=inp)
    V=sol["Terminal voltage [V]"].entries; Q=sol["Discharge capacity [A.h]"].entries; q=float(np.interp(2.6,V[::-1],Q[::-1]))
    breite*=135/q
out["breite_m"]=breite; out["kapazitaet_C20_Ah_vor_Anpassung"]=q
s=pybamm.Simulation(pybamm.lithium_ion.SPMe({"contact resistance":"true"}),parameter_values=blade_params(breite),solver=pybamm.IDAKLUSolver())
for nm,Ic in (("C20",135/20),("1C",135.0)):
    inp=basis(); inp.update(Iin=Ic,c0n=c0n,c0p=c0p); sol=s.solve(np.linspace(0,3600*30/(Ic/6.75),3000),inputs=inp)
    V=sol["Terminal voltage [V]"].entries; Q=sol["Discharge capacity [A.h]"].entries; out["kapazitaet_"+nm+"_Ah"]=float(np.interp(2.6,V[::-1],Q[::-1]))
print(out,flush=True)
b=breite
def dv_data(nm):
    w=W[nm]; t=w[:,0]; return t,w[:,1]-w[0,1]  # Vergleich gegen Spannung am ersten Pulspunkt NICHT; siehe unten
# --- (a) OCV: Ruhespannung vor Puls gegen Modell-OCV, affine SOC-Abbildung
A=R[(R.satz=="p25")&(R.sweep==0)&(R.SOC>0.04)&(R.SOC<0.96)]
x0=dict(Rc=0,fk=1,fjp=1,fjn=1,fDp=1,fDn=1)
def ocv(socm): return puls(b,float(np.clip(socm,0.001,0.999)),1e-6,25,np.array([0.0,1.0]),x0)[1]
def res_a(q): return np.array([ocv(q[0]+q[1]*s)-v for s,v in zip(A.SOC,A.V_ruhe)])
r0=res_a([0,1]); out["ocv_rms_mV_vorher"]=float(1e3*np.sqrt(np.mean(r0**2))); print("OCV vorher",out["ocv_rms_mV_vorher"],flush=True)
fa=least_squares(res_a,[0,1],bounds=([-0.2,0.5],[0.2,1.5]),diff_step=1e-3)
out["ocv_abbildung"]={"a":float(fa.x[0]),"b":float(fa.x[1])}; out["ocv_rms_mV_nachher"]=float(1e3*np.sqrt(np.mean(fa.fun**2))); print("OCV nachher",out["ocv_rms_mV_nachher"],fa.x,flush=True)
ab=np.array([0.0,1.0])  # Fit stiess an Grenze a=0,2 (Stoechiometrie >1 abgeschnitten): Abbildung NICHT verwendet, SOC = Messung (Annahme, begruendet in ERGEBNIS.md)
out["ocv_abbildung_verwendet"]={"a":0.0,"b":1.0,"grund":"Fit a an Grenze 0,2, Modell-SOC >0,999 fuer Messung 0,90-0,95 abgeschnitten"}
out["ocv_rms_mV_identitaet"]=float(1e3*np.sqrt(np.mean(r0**2)))
out["ocv_punkte"]={"soc":A.SOC.tolist(),"V_gemessen":A.V_ruhe.tolist(),"V_modell_vorher":(r0+A.V_ruhe.values).tolist(),"V_modell_nachher":(fa.fun+A.V_ruhe.values).tolist()}
def pulsmodell(row,x):
    w=W[row.puls]; t=w[:,0]; sel=t<=10.0; t=t[sel]; I=-float(np.median(w[sel,2]))
    try: V,V0=puls(b,float(np.clip(ab[0]+ab[1]*row.SOC,0.001,0.999)),I,row.T_C,t,x)
    except Exception: return t,np.full(len(t),np.nan),w[sel,1]-row.V_ruhe   # Modell bricht ab (Mindestspannung)
    dm=V-V0
    return t,dm,w[sel,1]-row.V_ruhe
# --- (b) 25 C: freie Parameter Rc, fk, fjp, fjn, fDp, fDn (6)
B=R[(R.satz=="p25")&(R.sweep==0)&(R.SOC>0.04)&(R.SOC<0.96)]
def xb(q): return dict(Rc=q[0]*1e-3,fk=10**q[1],fjp=10**q[2],fjn=10**q[3],fDp=10**q[4],fDn=10**q[5])
def res_b(q,Bs=None):
    x=xb(q); r=[]
    for _,row in (B if Bs is None else Bs).iterrows():
        t,dm,dd=pulsmodell(row,x); r.append(np.nan_to_num(dm-dd,nan=-1.0))   # Abbruch: Strafe 1 V
    return np.concatenate(r)
PREV=json.load(open(O+"ergebnis_blade_lauf1.json")) if "--c" in sys.argv else None
t0=time.time(); q0=[0.3,0,0,0,0,0]; rb0=res_b(q0); out["rms_b_vorher_mV"]=float(1e3*np.sqrt(np.mean(rb0**2))); print("b vorher",out["rms_b_vorher_mV"],time.time()-t0,flush=True)
B1=B[(B.SOC>=0.15)&(B.SOC<=0.9)]   # Phase 1 ohne Pulse, bei denen das unkalibrierte Modell die Mindestspannung reisst
if PREV is None: fb1=least_squares(lambda q:res_b(q,B1),q0,bounds=([0,-2,-2,-2,-3,-3],[3,2,2,2,3,3]),diff_step=1e-2,max_nfev=30)
else:
    pb=PREV["b_parameter"]; qq=np.array([pb["Rc"]*1e3]+[np.log10(pb[k_]) for k_ in ("fk","fjp","fjn","fDp","fDn")])
    from types import SimpleNamespace as _NS
    fb1=_NS(x=qq,fun=res_b(qq,B1))
print("b phase1",float(1e3*np.sqrt(np.mean(fb1.fun**2))),fb1.x,time.time()-t0,flush=True)
fb=fb1   # Kalibrierbereich SOC 15-90 %; ausserhalb bricht das Modell mit den gefundenen Parametern ab (siehe ERGEBNIS.md), keine Phase 2
out["b_parameter"]=xb(fb.x); out["rms_b_nachher_mV"]=float(1e3*np.sqrt(np.mean(fb1.fun**2))); out["kalibrierbereich_SOC"]=[0.15,0.9]; print("b nachher",out["rms_b_nachher_mV"],out["b_parameter"],time.time()-t0,flush=True)
# --- (c) Temperatur: Ea_k, Ea_Dp, Ea_Dn (3), Pulse 1. Sweep bei m10/p00/p40
Ts=R[(R.satz.isin(["m10","p00","p40"]))&(R.sweep==0)&(R.SOC>=0.15)&(R.SOC<=0.9)]
def res_c(q):
    x=dict(xb(fb.x)); x.update(Ea_k=q[0]*1e3,Ea_Dp=q[1]*1e3,Ea_Dn=q[2]*1e3,Ea_Rc=q[3]*1e3); r=[]
    for _,row in Ts.iterrows():
        t,dm,dd=pulsmodell(row,x); r.append(np.nan_to_num(dm-dd,nan=-1.0))   # Abbruch: Strafe 1 V
    return np.concatenate(r)
rc0=res_c([0,0,0,0]); out["rms_c_vorher_mV"]=float(1e3*np.sqrt(np.mean(rc0**2))); print("c vorher",out["rms_c_vorher_mV"],flush=True)
fc=least_squares(res_c,[10,10,10,10],bounds=([0,0,0,0],[80,150,150,100]),diff_step=1e-2,max_nfev=40)
out["c_Ea_kJ_mol"]=dict(k=float(fc.x[0]),Dp=float(fc.x[1]),Dn=float(fc.x[2]),Rc=float(fc.x[3])); out["rms_c_nachher_mV"]=float(1e3*np.sqrt(np.mean(fc.fun**2))); print("c nachher",out["rms_c_nachher_mV"],out["c_Ea_kJ_mol"],flush=True)
xf=dict(xb(fb.x)); xf.update(Ea_k=fc.x[0]*1e3,Ea_Dp=fc.x[1]*1e3,Ea_Dn=fc.x[2]*1e3,Ea_Rc=fc.x[3]*1e3); out["x_final"]=xf
# --- Auswertung: je Pulssatz (alle Sweeps) RMS, R10 Modell gegen Messung, Wellen
tab=[]; wav={}
for _,row in R.iterrows():
    try: t,dm,dd=pulsmodell(row,xf)
    except Exception as e: print("fehler",row.puls,e); continue
    tab.append(dict(puls=row.puls,satz=row.satz,sweep=int(row.sweep),SOC=row.SOC,T_C=row.T_C,I_A=row.I_A,rms_mV=float(1e3*np.sqrt(np.mean((dm-dd)**2))) if np.all(np.isfinite(dm)) else float('nan'),abbruch=bool(not np.all(np.isfinite(dm))),
        R10_mess_mOhm=row.R_10s_mOhm,R10_modell_mOhm=float(1e3*(-dm[-1])/abs(row.I_A)) ,t_end=float(t[-1]),kalibriert=bool(row.sweep==0 and 0.15<=row.SOC<=0.9)))
    wav[row.puls]=dict(t=t.tolist(),dm=dm.tolist(),dd=dd.tolist())
T=pd.DataFrame(tab); T.to_csv(O+"kalibrierung_pulse.csv",index=False)
out["pulse_n"]=len(T); out["rms_je_satz_mV"]=T.groupby(["satz","kalibriert"]).rms_mV.agg(["mean","max","count"]).reset_index().to_dict("records")
out["R10_50pct"]={k:dict(mess=float(g.R10_mess_mOhm.mean()),modell=float(g.R10_modell_mOhm.mean()),T=float(g.T_C.mean())) for k,g in T[(abs(T.SOC-0.5)<0.02)].groupby("satz")}
json.dump(out,open(O+"ergebnis_blade.json","w"),indent=1); json.dump(wav,open("/home/cae/cae_projekte/batterie/c2/blade_wellen_modell.json","w"))
print("fertig",time.strftime("%H:%M:%S"),flush=True)
