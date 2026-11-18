# KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. C2 Bilder und Zahlen aus ergebnis_*.json / kalibrierung_pulse.csv. Zahlen in Titeln aus den Daten.
import json, numpy as np, pandas as pd, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
O="/home/cae/hermes/batterie/sim/chemie/c2_kalibrierung/"
B=json.load(open(O+"ergebnis_blade.json")); D=json.load(open(O+"ergebnis_dcir.json")); SL=json.load(open(O+"ergebnis_schnellladen_lfp.json")); SN=json.load(open(O+"ergebnis_schnellladen_n4680.json"))
T=pd.read_csv(O+"kalibrierung_pulse.csv"); WM=json.load(open("/home/cae/cae_projekte/batterie/c2/blade_wellen_modell.json"))
Z={}
# 1 Kalibrierung Blade: Messung gg. Modell
f,ax=plt.subplots(1,2,figsize=(12,4.8))
col=["C0","C1","C2","C3"]
a=ax[0]; s=T[(T.satz=="p25")&(T.sweep==0)]
for c,soc in zip(col,(0.8,0.5,0.2,0.05)):
    r=s.iloc[(s.SOC-soc).abs().argsort()[:1]].iloc[0]; w=WM[r.puls]; t=np.array(w["t"]); dd=np.array(w["dd"]); dm=np.array(w["dm"])
    a.plot(t,dd,"o",color=c,ms=4,label=f"Messung {100*r.SOC:.0f} % SOC, {abs(r.I_A):.0f} A"); a.plot(t,dm,"-",color=c,label=(f"Modell (RMS {r.rms_mV:.0f} mV)" if r.rms_mV==r.rms_mV else "Modell: Abbruch (U<2,6 V)"))
    a.fill_between(t,dd-0.015,dd+0.015,color=c,alpha=.12)
a.set(xlabel="Zeit im Puls [s]",ylabel="Spannung gegen Ruhe [V]"); a.set_title(f"Blade 25 °C: RMS Kalibriersatz {B['rms_b_nachher_mV']:.1f} mV (Ziel ≤ 15, verfehlt > 30)",fontsize=9); a.legend(fontsize=6.5,loc="lower left"); a.grid(alpha=.3)
a.text(.02,.95,"Zielband: Schatten = ±15 mV um die Messung",transform=a.transAxes,fontsize=8,color="g")
a=ax[1]; Ts=T[(T.sweep==0)&(abs(T.SOC-0.5)<0.03)]
for c,k,lab in zip(["C0","C2","C1","C3"],["m10","p00","p25","p40"],["−10 °C","0 °C","25 °C","40 °C"]):
    r=Ts[Ts.satz==k]
    if len(r)==0: continue
    r=r.iloc[0]; w=WM[r.puls]; t=np.array(w["t"]); a.plot(t,w["dd"],"o",color=c,ms=4,label=f"Messung {lab} (Zelle {r.T_C:.0f} °C, {abs(r.I_A):.0f} A)"); a.plot(t,w["dm"],"-",color=c,label=f"Modell (RMS {r.rms_mV:.0f} mV)")
a.set(xlabel="Zeit im Puls [s]",ylabel="Spannung gegen Ruhe [V]"); a.set_title(f"Temperaturreihe 50 % SOC, RMS Kalibriersatz {B['rms_c_nachher_mV']:.1f} mV: verfehlt",fontsize=9); a.legend(fontsize=6.5,loc="center right"); a.grid(alpha=.3)
f.tight_layout(); f.savefig(O+"kalibrierung_blade.png",dpi=130); plt.close(f)
# 2 DCIR-Vergleich
f,a=plt.subplots(figsize=(9,4.8))
lab=[];val=[];cl=[]
for T_ in (-10,0,25,40):
    mm=T[(T.sweep==0)&(abs(T.SOC-0.5)<0.03)&(T.satz=={-10:"m10",0:"p00",25:"p25",40:"p40"}[T_])]
    lab.append(f"Blade {T_} °C\nMessung"); val.append(mm.R10_mess_mOhm.mean() if len(mm) else np.nan); cl.append("0.6")
    lab.append(f"Blade {T_} °C\nModell"); val.append(D[f"blade135_{T_}"]["R10_mOhm"]); cl.append("C0")
x=np.arange(len(lab)); a.bar(x,val,color=cl); a.set_xticks(x); a.set_xticklabels(lab,fontsize=6.5)
a.axhspan(0.8,1.2,color="g",alpha=.15,label="Zielband Blade 25 °C, 50 % SOC: 0,8–1,2 mΩ")
for k,(T_,c) in enumerate(((25,"C1"),)): a.axhline(D[f"lfp92_{T_}"]["R10_mOhm"],color="C1",ls="--",label=f"LFP 92,4 Ah Modell 25 °C: {D['lfp92_25']['R10_mOhm']:.2f} mΩ (Band 1,2–1,75)")
a.axhspan(1.2,1.75,color="orange",alpha=.12)
a.set(ylabel="10-s-Widerstand 50 % SOC [mΩ]",title="Blade: Messung gegen Modell; 4680 siehe Zahlentabelle: "+f"{D['n4680_25']['R10_mOhm']:.2f} mΩ (Band 5,4–7)"); a.legend(fontsize=7); a.grid(alpha=.3,axis="y")
f.tight_layout(); f.savefig(O+"dcir_vergleich.png",dpi=130); plt.close(f)
# 3 Schnellladen 4680
sel=[r for r in SN["N4680"] if r["C_start"] in (1.3,1.5,1.8)]
f,ax=plt.subplots(2,2,figsize=(12,7)); ax=ax.ravel()
for r,c in zip(sel,["C0","C1","C3"]):
    t=np.array(r["t_s"])/60; q=np.array(r["Q_Ah"])/23.125*100+10
    ax[0].plot(t,np.abs(r["I_A"]),c,label=f"Start {r['C_start']} C ({r['I_start_A']:.0f} A)"); ax[1].plot(t,r["U_V"],c); ax[2].plot(t,r["phi_an_V"],c); ax[3].plot(t,q,c,label=f"{r['zeit_10_80_min']:.1f} min bis 80 %")
for a,tt in zip(ax,("Strom [A]","Spannung [V]","Anodenpotential gegen Li [V]","SOC [%] (aus Ah, Start 10 %)")): a.set(xlabel="Zeit [min]",ylabel=tt); a.axvline(30,color="g",ls="--"); a.grid(alpha=.3)
ax[2].axhline(0,color="r",lw=1.5); ax[2].text(.02,.06,"Plating-Grenze 0 V (rot)",transform=ax[2].transAxes,color="r",fontsize=8); ax[0].legend(fontsize=8); ax[3].legend(fontsize=8)
ax[3].axhline(80,color="g",ls=":"); ax[3].text(.55,.12,"Zielband: 80 % bis 30 min (grüne Linie)",transform=ax[3].transAxes,color="g",fontsize=8)
f.suptitle("4680 (Chen2020, unkalibriert) CC-CV bis 4,3 V, 10→80 %, Zelle lumped, Kühlung K0/K1-Annahme"); f.tight_layout(); f.savefig(O+"schnellladen_4680.png",dpi=130); plt.close(f)
# 4 Waermevergleich
f,a=plt.subplots(figsize=(8,4.8))
n=[r for r in SN["N4680"] if r["C_start"]==1.5][0]
items=[(f"LFP 92,4 Ah 2,1C\nnur CC bis 3,65 V ({SL['LFP']['CC_ende_min']:.1f} min)",SL["LFP"]["waerme_mittel_CC_W"],55.0),("4680 1,5C\nModell gesamt",n["waerme_mittel_gesamt_W"],6.7),("4680 1,5C\nModell I·ΔU",n["waerme_mittel_IdU_W"],6.7)]
for i,(nm,v,ref) in enumerate(items):
    a.bar(i,v,color="C0",width=.35); a.plot([i-.3,i+.3],[ref,ref],"C3--"); a.fill_between([i-.3,i+.3],ref/1.5,ref*1.5,color="g",alpha=.15)
    a.text(i,v,f"{v:.1f} W",ha="center",va="bottom",fontsize=8)
a.set_xticks(range(3)); a.set_xticklabels([i[0] for i in items],fontsize=8); a.set_yscale("log")
a.plot([],[],"C3--",label="K1-Annahme (55 W LFP, 6,7 W 4680)"); a.fill_between([],[],[],color="g",alpha=.15,label="Zielband Faktor 1,5 um die Annahme"); a.legend(fontsize=8)
a.set(ylabel="mittlere Zellwärme [W]",title="Wärme beim Schnellladen: Modell gegen K1-Annahme"); a.grid(alpha=.3,axis="y"); f.tight_layout(); f.savefig(O+"waerme_vergleich.png",dpi=130); plt.close(f)
