# KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. C2 Schritt 1: Blade-Pulse aus Test#5 (Rohdaten nur lesen).
# Quelle: Borealis doi:10.5683/SP3/RPCWBY (CC BY 4.0), Test#5 BYD Blade 135 Ah.
import pandas as pd, numpy as np, os, json
D="/home/cae/cae_projekte/batterie/c2/"; O="/home/cae/hermes/batterie/sim/chemie/c2_kalibrierung/"
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
Q={"p25":("t5/Test#5/JC_BYD_SOP_Feb_27_Channel_1_Wb_1.CSV","csv"),"m10":("csv/m10.csv","c"),"p00":("csv/p00.csv","c"),"p40":("csv/p40.csv","c")}
COLS=["Test_Time(s)","Current(A)","Voltage(V)","SOC","Aux_Temperature_1(thermocouple1(C))"]
rows=[]; wave={}
for k,(f,typ) in Q.items():
    if not os.path.exists(D+f): print("fehlt",k); continue
    df=pd.read_csv(D+f,encoding="utf-8-sig",usecols=COLS if typ=="csv" else None); df.columns=["t","I","V","SOC","T"]
    big=np.abs(df.I.values)>200; seg=np.cumsum(np.r_[0,np.diff(big.astype(int))!=0]); n=0
    for g in np.unique(seg[big]):
        ix=np.where((seg==g)&big)[0]; i0,i1=ix[0],ix[-1]
        if i0<3 or i1-i0<6: continue
        pre=df.iloc[i0-1]; p=df.iloc[i0:i1+1]; t=p.t.values-p.t.values[0]
        if t[-1]<8: continue
        Ir=float(np.median(p.I)); V10=float(np.interp(10.0,t,p.V.values)) if t[-1]>=10 else float(p.V.values[-1])
        V1=float(np.interp(1.0,t,p.V.values)); V01=float(np.interp(0.1,t,p.V.values)); t10=min(10.0,float(t[-1]))
        nm=f"{k}_{n}"; n+=1
        wave[nm]=np.c_[t,p.V.values,p.I.values]
        rows.append(dict(satz=k,puls=nm,t_start_s=float(p.t.values[0]),I_A=Ir,SOC=float(pre.SOC),T_C=float(p["T"].mean()),V_ruhe=float(pre.V),V_0p1s=V01,V_1s=V1,V_10s=V10,dauer_s=float(t[-1]),
          R_0p1s_mOhm=1e3*(pre.V-V01)/abs(Ir),R_1s_mOhm=1e3*(pre.V-V1)/abs(Ir),R_10s_mOhm=1e3*(pre.V-V10)/abs(Ir)))
print(len(rows)); R=pd.DataFrame(rows); R.to_csv(O+"blade_pulse.csv",index=False)
np.savez_compressed(D+"blade_wellen.npz",**wave)
print(R.groupby("satz").size()); print(R[(R.satz=="p25")&(R.I_A<-400)][["SOC","T_C","I_A","V_ruhe","R_10s_mOhm"]].round(4).to_string())
# Bild
f,a=plt.subplots(1,2,figsize=(11,4.5))
for k,c in zip(["m10","p00","p25","p40"],["C0","C2","C1","C3"]):
    r=R[(R.satz==k)&(R.I_A<-250)]
    if len(r)==0: continue
    a[0].plot(100*r.SOC,r.R_10s_mOhm,"o",alpha=.6,color=c,ms=4,label=f"{ {"m10":"−10","p00":"0","p25":"25","p40":"40"}[k] } °C (Zelle ≈ {r['T_C'].mean():.0f} °C), Entladepuls"); a[1].plot(100*r.SOC,r.V_ruhe,".",color=c)
a[0].axhspan(0.8,1.2,color="g",alpha=.15,label="Zielband ERWARTUNG: 0,8–1,2 mΩ (25 °C, 50 % SOC)")
a[0].set(xlabel="SOC [%]",ylabel="10-s-Widerstand [mΩ]",title="Blade 135 Ah: Widerstand je SOC, 10-s-Entladepuls"); a[0].legend(fontsize=7); a[0].grid(alpha=.3)
a[1].set(xlabel="SOC [%]",ylabel="Ruhespannung vor Puls [V]",title="Spannung vor dem Puls (Rohdaten)"); a[1].grid(alpha=.3)
f.tight_layout(); f.savefig(O+"blade_widerstand.png",dpi=130)
