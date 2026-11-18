#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. Auftrag E1 (Opus), ERW-E1. Liest NUR eingaben.json. Laufzeit: Sekunden, CPU."""
import json, os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
D=os.path.dirname(os.path.abspath(__file__)); E=json.load(open(os.path.join(D,"eingaben.json"),encoding="utf-8"))
S=E["stoffe"]; G=E["grenzen"]; WP=E["waermepfad"]; N=E["normreihen"]; GM=E["geometrie_mm"]; ST=E["stueck"]
t=WP["pad_dicke_mm"]["wert"]*1e-3; lam=WP["pad_lambda_W_mK"]["wert"]; dTmax=G["dT_max_K"]
# Lastfaelle
lf=E["lade"]["LFP"]; nm=E["lade"]["NMC"]; F=E["fahren"]; U=E["spannung_V"]
I_lade_LFP=lf["C"]*lf["ah"]["wert"]; I_lade_NMC=nm["C"]*nm["ah_gruppe"]["wert"]; p_nmc=nm["p"]
def lastfaelle(var,I_lade,Uend,p):
    L={"Laden 10-80 % (Pack)":I_lade,
       "Spitze 10 s bei Nennspannung":F["spitze_kW"]*1e3/U["nenn"],"Spitze 10 s bei Entladeschluss":F["spitze_kW"]*1e3/Uend,
       "Dauer bei Nennspannung":F["dauer_kW"]*1e3/U["nenn"],"Dauer bei Entladeschluss":F["dauer_kW"]*1e3/Uend}
    return {k:{"pack_A":v,"zelle_A":v/p} for k,v in L.items()}
LF={"LFP":lastfaelle("LFP",I_lade_LFP,U["entladeschluss_LFP"],1),"NMC":lastfaelle("NMC",I_lade_NMC,U["entladeschluss_NMC"],p_nmc)}
def dauer(var): L=LF[var]; return max(L["Laden 10-80 % (Pack)"]["pack_A"],L["Dauer bei Entladeschluss"]["pack_A"])
def spitze(var): return LF[var]["Spitze 10 s bei Entladeschluss"]["pack_A"]
def waehle_Al(I,L_mm):
    Jmax=G["J_Al_A_mm2"][1]; Jmin=G["J_Al_A_mm2"][0]; rho=S["rho_Al_Ohm_m"]; best=None
    for d in N["dicke_mm"]:
        for w in N["breite_mm"]:
            A=w*d; J=I/A; dT=I**2*rho*t/((A*1e-6)*(w*1e-3)*lam)
            if J<=Jmax and dT<=dTmax:
                if best is None or A<best[0] or (A==best[0] and w<best[1]): best=(A,w,d)
    A,w,d=best; return dict(werkstoff="Al",breite_mm=w,dicke_mm=d,A_mm2=A,laenge_mm=L_mm,
        A_aus_J_max_mm2=I/Jmax,A_aus_J_min_mm2=I/Jmin,
        J_A_mm2=I/A,
        dT_K=I**2*rho*t/((A*1e-6)*(w*1e-3)*lam),
        dT_K_lambda={str(l):I**2*rho*t/((A*1e-6)*(w*1e-3)*l) for l in [WP["pad_lambda_W_mK"]["band"][0],lam,WP["pad_lambda_W_mK"]["band"][1]]},
        R_uOhm=rho*L_mm*1e-3/(A*1e-6)*1e6, dichte=S["dichte_Al"], rho=rho, c=S["c_Al"])
def waehle_Cu(I,L_mm):
    Jmax=G["J_Cu_A_mm2"][1]; Jmin=G["J_Cu_A_mm2"][0]; rho=S["rho_Cu_Ohm_m"]
    A=min(a for a in N["hv_mm2"] if I/a<=Jmax)
    return dict(werkstoff="Cu",A_mm2=A,laenge_mm=L_mm,A_aus_J_max_mm2=I/Jmax,A_aus_J_min_mm2=I/Jmin,J_A_mm2=I/A,
        R_uOhm=rho*L_mm*1e-3/(A*1e-6)*1e6,dichte=S["dichte_Cu"],rho=rho,c=S["c_Cu"])
def verluste(art,n,I_dauer,I_sp):
    R=art["R_uOhm"]*1e-6
    art["stueck"]=n; art["strom_dauer_A"]=I_dauer; art["strom_spitze_A"]=I_sp
    art["verlust_je_W"]=I_dauer**2*R; art["verlust_gesamt_W"]=n*I_dauer**2*R
    art["verlust_spitze_gesamt_W"]=n*I_sp**2*R
    art["spannungsabfall_V"]=n*I_dauer*R; art["masse_gesamt_kg"]=n*art["A_mm2"]*1e-6*art["laenge_mm"]*1e-3*art["dichte"]
    art["dT_adiabat_Spitze_10s_K"]=(I_sp/(art["A_mm2"]*1e-6))**2*art["rho"]*F["spitze_s"]/(art["dichte"]*art["c"])
    return art
res={"hinweis":"KI-generiert (Claude Sonnet), Entwurf. Quelle: eingaben.json via querschnitte.py","lastfaelle":LF,"pad_lambda_W_mK":lam,"arten":{}}
# LFP
Id=dauer("LFP"); Is=spitze("LFP")
a=verluste(waehle_Al(Id,GM["LFP_pitch"]["wert"]),ST["LFP_reihenverbinder"],Id,Is); res["arten"]["LFP Zell-/Reihenverbinder (BT-410/420)"]=a
h=verluste(waehle_Cu(Id,GM["LFP_laenge_gehaeuse"]["wert"]),ST["HV"],Id,Is); res["arten"]["LFP HV-Hauptleitung (BT-430)"]=h
res["LFP_summe"]=dict(verlust_W=a["verlust_gesamt_W"]+h["verlust_gesamt_W"],spannungsabfall_V=a["spannungsabfall_V"]+h["spannungsabfall_V"])
# NMC
Id=dauer("NMC"); Is=spitze("NMC"); Ic=Id/p_nmc; Isc=Is/p_nmc
g=verluste(waehle_Al(Id,GM["NMC_gruppe_laenge"]["wert"]),ST["NMC_gruppenverbinder"],Id,Is); res["arten"]["NMC Gruppenverbinder (BT-420)"]=g
# Nachtrag Methode (Opus 2026-11-17): Sammelstrecke 217 x Strom 0->I (Verlust I^2R/3, Spannungsabfall I R/2), Bruecke 216 x voller Strom
Rs=g["R_uOhm"]*1e-6; Rb=Rs*GM["NMC_gruppe_bruecke"]["wert"]/GM["NMC_gruppe_laenge"]["wert"]; ns=ST["NMC_gruppenverbinder"]+1; nb=ST["NMC_gruppenverbinder"]
g["methode"]="Sammelstrecke: 217 Stueck, I^2R/3; Bruecke: 216 Stueck, voller Strom"
g["verlust_alt_konservativ_W"]=g["verlust_gesamt_W"]; g["verlust_sammel_W"]=ns*Id**2*Rs/3; g["verlust_bruecke_W"]=nb*Id**2*Rb
g["verlust_gesamt_W"]=g["verlust_sammel_W"]+g["verlust_bruecke_W"]; g["verlust_je_W"]=g["verlust_gesamt_W"]/nb
g["verlust_spitze_gesamt_W"]=ns*Is**2*Rs/3+nb*Is**2*Rb
g["spannungsabfall_V"]=ns*Id*Rs/2+nb*Id*Rb
g["masse_gesamt_kg"]=(ns*GM["NMC_gruppe_laenge"]["wert"]+nb*GM["NMC_gruppe_bruecke"]["wert"])*1e-3*g["A_mm2"]*1e-6*g["dichte"]
z=verluste(waehle_Al(Ic,GM["NMC_zellabgriff_laenge"]["wert"]),ST["NMC_zellabgriff"],Ic,Isc); res["arten"]["NMC Zellabgriff (BT-410)"]=z
# Spannungsabfall Zellabgriff: je Gruppe Strom einer Zelle durch 2 Abgriffe in Reihe
z["spannungsabfall_V"]=ST["NMC_gruppenverbinder"]+1; z["spannungsabfall_V"]=(ST["NMC_gruppenverbinder"]+1)*2*Ic*z["R_uOhm"]*1e-6
h2=verluste(waehle_Cu(Id,GM["NMC_laenge_gehaeuse"]["wert"]),ST["HV"],Id,Is); res["arten"]["NMC HV-Hauptleitung (BT-430)"]=h2
res["NMC_summe"]=dict(verlust_W=g["verlust_gesamt_W"]+z["verlust_gesamt_W"]+h2["verlust_gesamt_W"],spannungsabfall_V=g["spannungsabfall_V"]+z["spannungsabfall_V"]+h2["spannungsabfall_V"])
for v in ("LFP","NMC"):
    s=res[v+"_summe"]; s["spannungsabfall_prozent_Nenn"]=100*s["spannungsabfall_V"]/U["nenn"]; s["verlust_prozent_150kW"]=100*s["verlust_W"]/(F["spitze_kW"]*1e3)
    s["masse_kg"]=sum(a["masse_gesamt_kg"] for k,a in res["arten"].items() if k.startswith(v))
    s["masse_Al_kg"]=sum(a["masse_gesamt_kg"] for k,a in res["arten"].items() if k.startswith(v) and a["werkstoff"]=="Al")
    s["masse_Cu_kg"]=sum(a["masse_gesamt_kg"] for k,a in res["arten"].items() if k.startswith(v) and a["werkstoff"]=="Cu")
# Pruefung gegen Baender
B=E["baender_mm2"]; key={"LFP Zell-/Reihenverbinder (BT-410/420)":"LFP_Reihenverbinder","NMC Gruppenverbinder (BT-420)":"NMC_Gruppenverbinder","NMC Zellabgriff (BT-410)":"NMC_Zellabgriff","LFP HV-Hauptleitung (BT-430)":"HV_Cu","NMC HV-Hauptleitung (BT-430)":"HV_Cu"}
for k,a in res["arten"].items():
    b=B[key[k]]; a["band_mm2"]=b; a["im_band"]=b[0]<=a["A_mm2"]<=b[1]; a["ausserhalb_ueber_50_prozent"]=a["A_mm2"]<b[0]*0.5 or a["A_mm2"]>b[1]*1.5
res["verfehlt_verlust_ueber_300W"]=any(res[v+"_summe"]["verlust_W"]>E["verlust_band_W"]["verfehlt_ab"] for v in ("LFP","NMC"))
json.dump(res,open(os.path.join(D,"ergebnis.json"),"w",encoding="utf-8"),indent=1,ensure_ascii=False)
# Bilder
arten=list(res["arten"].keys()); lab=[k.replace(" (","\n(") for k in arten]
fig,ax=plt.subplots(figsize=(11,5.5)); x=range(len(arten))
for i,k in enumerate(arten):
    a=res["arten"][k]; b=a["band_mm2"]
    ax.add_patch(plt.Rectangle((i-0.42,b[0]),0.84,b[1]-b[0],color="#2ca02c",alpha=0.25,label="Zielband (Erwartung)" if i==0 else None))
    ax.bar(i,a["A_mm2"],width=0.4,color="#1f77b4" if a["werkstoff"]=="Al" else "#d62728",label=None)
    ax.hlines([a["A_aus_J_min_mm2"],a["A_aus_J_max_mm2"]],i-0.3,i+0.3,colors="k",linestyles=["--",":"],label=None)
    ax.text(i,a["A_mm2"]+1.5,f"{a['A_mm2']:g} mm²"+(f"\n{a['breite_mm']:g}×{a['dicke_mm']:g}" if a["werkstoff"]=="Al" else ""),ha="center",fontsize=9)
ax.plot([],[],"k--",label="Stromdichte-Untergrenze (Al 2 / Cu 4 A/mm²)"); ax.plot([],[],"k:",label="obere Grenze (Al 3 / Cu 5 A/mm²), Mindestquerschnitt")
ax.add_patch(plt.Rectangle((0,0),0,0,color="#1f77b4",label="gewählt Al")); ax.add_patch(plt.Rectangle((0,0),0,0,color="#d62728",label="gewählt Cu"))
ax.set_xticks(list(x)); ax.set_xticklabels(lab,fontsize=8); ax.set_ylabel("Querschnitt mm²")
ax.set_title(f"E1: gewählte Querschnitte; Dauerstrom LFP {res['arten'][arten[0]]['strom_dauer_A']:.0f} A, NMC {res['arten'][arten[2]]['strom_dauer_A']:.0f} A (Pack)",fontsize=10)
ax.legend(fontsize=8,loc="upper right"); fig.text(0.5,0.005,"KI-generiert (Claude Sonnet), Entwurf. Quelle: sim/elektrik/e1_querschnitte/ergebnis.json",ha="center",fontsize=7)
fig.tight_layout(rect=(0,0.02,1,1)); fig.savefig(os.path.join(D,"querschnitte.png"),dpi=130); plt.close(fig)
fig,ax=plt.subplots(figsize=(11,5.5)); w=0.38
dv=[res["arten"][k]["verlust_gesamt_W"] for k in arten]; sv=[res["arten"][k]["verlust_spitze_gesamt_W"] for k in arten]
ax.bar([i-w/2 for i in x],dv,w,label="Dauerstrom (Laden/Dauer)",color="#1f77b4"); ax.bar([i+w/2 for i in x],sv,w,label="Spitze 10 s",color="#ff7f0e")
ax.axhspan(0,E["verlust_band_W"]["erwartet_max"],color="#2ca02c",alpha=0.2,label=f"Zielband < {E['verlust_band_W']['erwartet_max']} W (Erwartung)")
ax.axhline(E["verlust_band_W"]["verfehlt_ab"],color="r",ls="--",label=f"Grenze verfehlt {E['verlust_band_W']['verfehlt_ab']} W")
for i,(d,s) in enumerate(zip(dv,sv)): ax.text(i-w/2,d,f"{d:.1f}",ha="center",va="bottom",fontsize=8); ax.text(i+w/2,s,f"{s:.1f}",ha="center",va="bottom",fontsize=8)
ax.set_xticks(list(x)); ax.set_xticklabels(lab,fontsize=8); ax.set_ylabel("Verlustleistung W (alle Stück der Art)")
ax.set_title(f"E1: Verluste je Verbinderart; Summe LFP {res['LFP_summe']['verlust_W']:.1f} W, NMC {res['NMC_summe']['verlust_W']:.1f} W (Dauerstrom)",fontsize=10)
ax.legend(fontsize=8); fig.text(0.5,0.005,"KI-generiert (Claude Sonnet), Entwurf. Quelle: sim/elektrik/e1_querschnitte/ergebnis.json",ha="center",fontsize=7)
fig.tight_layout(rect=(0,0.02,1,1)); fig.savefig(os.path.join(D,"verluste.png"),dpi=130); plt.close(fig)
print("ok")
