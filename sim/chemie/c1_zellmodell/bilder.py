# KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. Bilder und Zahlen C1 aus ergebnis*.json. Zahlen in Titeln aus den Daten.
import json, numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
H=json.load(open("eingaben.json")); A=json.load(open("ergebnis.json"))
K=json.load(open("ergebnis_LFP_kap.json"))["LFP_kap"]; NL=json.load(open("ergebnis_NMC_lumped.json"))["NMC"]
I2R=H["I2R_Annahme_W"]
Z={}
def stat(s,key):
    t=np.array(s["t_s"]); q=np.array(s[key]); cv=s["CV_beginn_s"]
    m=(t<=cv) if cv else np.ones_like(t,bool)
    return dict(mittel_ges=float(np.trapezoid(q,t)/t[-1]),mittel_cc=float(np.trapezoid(q[m],t[m])/(t[m][-1]-t[m][0])),max=float(q.max()))
sets={"LFP_Akten(isotherm)":A["LFP"],"LFP_kap(isotherm)":K,"NMC(isotherm)":A["NMC"],"NMC(lumped)":NL}
for n,r in sets.items():
    s=r["schnellladen"]; Z[n]={"kapazitaet_Ah":r["kapazitaet_C20_Ah"],"abw_proz":r["abw_prozent"],"strom_A":r["strom_A"],"dauer_min":s["dauer_min"],"CV_beginn_s":s["CV_beginn_s"],
      "U_max_V":s["U_max_V"],"Q_pruef_I_dU":stat(s,"Q_pruef_W"),"Q_modell_gesamt":stat(s,"Q_gesamt_W"),"Q_irr":stat(s,"Q_irr_W"),"Q_rev":stat(s,"Q_rev_W"),"T_ende_C":s["T_ende_C"],
      "dcir_mOhm":{T:d.get("R_10s_mOhm") for T,d in r["dcir"].items()}}
json.dump(Z,open("ergebnis_zahlen.json","w"),indent=1)
def waerme(name,r,key,ref,fn,tit):
    s=r["schnellladen"]; t=np.array(s["t_s"])/60; q=np.array(s[key]); st=stat(s,key)
    f,a=plt.subplots(figsize=(8,4.5)); a.plot(t,q,label="Modell (PyBaMM)",lw=2)
    a.axhline(ref,color="C3",ls="--",label=f"I²R-Annahme K0/K1: {ref} W")
    a.axhspan(ref/1.5,ref*1.5,color="g",alpha=.15,label="Zielband: Faktor 1,5 um die Annahme")
    if s["CV_beginn_s"]: a.axvline(s["CV_beginn_s"]/60,color="gray",ls=":",label="Beginn Konstantspannung")
    a.set(xlabel="Zeit [min]",ylabel="Wärme je Zelle [W]",title=f"{tit}: Mittel bis CV {st['mittel_cc']:.1f} W, Spitze {st['max']:.1f} W"); a.legend(fontsize=8); a.grid(alpha=.3)
    f.tight_layout(); f.savefig(fn,dpi=130); plt.close(f)
waerme("LFP",K,"Q_pruef_W",I2R["LFP"],"waerme_LFP.png",f"LFP 92,4 Ah, {Z['LFP_kap(isotherm)']['strom_A']:.0f} A (nur irreversibel, I·ΔU)")
waerme("NMC",NL,"Q_gesamt_W",I2R["NMC"],"waerme_NMC.png",f"NMC 23,1 Ah, {Z['NMC(lumped)']['strom_A']:.1f} A (gesamt, lumped)")
f,a=plt.subplots(figsize=(8,4.5))
for n,r,c in (("LFP_kap",K,"C0"),("NMC",A["NMC"],"C1")):
    for T,ls in (("10","-"),("25","--"),("40",":")):
        d=r["dcir"][T]; a.plot(d["t_s"],np.array(d["U_V"])-d["U0_V"],c,ls=ls,label=f"{n} {T} °C: {d['R_10s_mOhm']:.2f} mΩ")
a.set(xlabel="Zeit im 10-s-Puls [s]",ylabel="Spannungsabfall gegen Ruhe [V]",title="DCIR 10 s, 50 % SOC, 1C-Entladepuls")
a.axhline(0,color="k",lw=.5); a.legend(fontsize=7); a.grid(alpha=.3)
a.text(.02,.04,"Zielband (ERWARTUNG): LFP 1–2 mΩ, NMC 5–8 mΩ (25 °C)",transform=a.transAxes,fontsize=8,color="g"); f.tight_layout(); f.savefig("dcir.png",dpi=130); plt.close(f)
f,ax=plt.subplots(1,2,figsize=(11,4.5))
for a,(n,r) in zip(ax,(("LFP_kap",K),("NMC lumped",NL))):
    s=r["schnellladen"]; t=np.array(s["t_s"])/60; a.plot(t,s["U_V"],"C0",label="Spannung [V]"); a.set(xlabel="Zeit [min]",ylabel="Spannung [V]",title=f"{n}: {s['dauer_min']:.1f} min bis 80 % (Ziel 20 min)")
    b=a.twinx(); b.plot(t,s["I_A"],"C3",label="Strom [A]"); b.set_ylabel("Strom [A]"); a.axvline(20,color="g",ls="--",label="Zielzeit 20 min"); a.legend(loc="lower right",fontsize=8); a.grid(alpha=.3)
f.tight_layout(); f.savefig("ladekurve.png",dpi=130); plt.close(f)
