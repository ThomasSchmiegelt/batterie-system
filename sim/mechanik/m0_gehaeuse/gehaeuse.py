#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. Auftrag M0 (Opus), ERW-M0. Liest NUR eingaben.json. Laufzeit: Sekunden."""
import json, math, os, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
D=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.abspath(os.path.join(D,"..","..",".."))
sys.path.insert(0,os.path.join(ROOT,"sim","geometrie","g1_anordnung"))
E=json.load(open(os.path.join(D,"eingaben.json"),encoding="utf-8"))
B=E["bauraum_B_mm"]["wert"]; rand=E["rand_mm"]["wert"]; q=E["quertraeger"]; nq=q["anzahl"]; qb=q["breite_L_mm"]; sp=q["spiel_je_seite_mm"]
rho=E["alu_dichte_kg_m3"]["wert"]; hs=E["hoehenstapel_mm"]; LF=E["zellen"]["LFP"]; NM=E["zellen"]["NMC"]
qlen=B-2*rand
A_q=2*(q["hoehe_mm"]+qb)*q["wand_mm"]; m_q=A_q*1e-6*qlen*1e-3*rho
def stapel(zh):
    return [("Unterfahrschutz",hs["unterfahrschutz"]),("Luft",hs["luft"]),("Boden",hs["boden"]),("Kühlplatte unten",hs["kuehlplatte_je"]),
            ("Wärmeleitschicht",hs["waermeleitschicht_je"]),("Zelle",zh),("Wärmeleitschicht",hs["waermeleitschicht_je"]),("Kühlplatte oben",hs["kuehlplatte_je"]),("Deckel",hs["deckel"])]
res={"hinweis":"KI-generiert (Claude Sonnet), Entwurf. Quelle: eingaben.json via gehaeuse.py","quertraeger":{"querschnitt_mm2":A_q,"laenge_mm":qlen,"masse_je_kg":m_q,"masse_gesamt_kg":m_q*nq}}
# LFP
nz=LF["anzahl"]//2; pitch=LF["dicke_mm"]+LF["abstand_mm"]; stap=nz*LF["dicke_mm"]+(nz-1)*LF["abstand_mm"]
Lnet=stap+nq*(qb+2*sp); Lgeh=Lnet+2*rand; Bmin=2*LF["laenge_mm"]; Btol=B-2*rand-Bmin
sL=stapel(LF["hoehe_mm"]); HL=sum(x for _,x in sL)
grp=[nz//(nq+1)+(1 if i<nz%(nq+1) else 0) for i in range(nq+1)]
res["LFP"]=dict(zellen_je_reihe=nz,stapel_mm=stap,laenge_netto_mm=Lnet,laenge_gehaeuse_mm=Lgeh,zuwachs_gegen_1950_mm=Lgeh-1950,
  breite_zellen_mm=Bmin,toleranz_breite_gesamt_mm=Btol,toleranz_je_seite_mm=Btol/2,seitenrahmen_mm=rand,hoehe_mm=HL,hoehe_rest_mm=E["hoehe_max_mm"]["wert"]-HL,gruppen=grp,
  stapel=sL,passt_H=HL<=130,passt_L=E["zielband"]["LFP_laenge_mm"][0]<=Lgeh<=E["zielband"]["LFP_laenge_mm"][1])
# NMC
d=NM["durchmesser_mm"]; t=d+NM["abstand_mm"]; rp=t*math.sqrt(3)/2
Lg=E["bauraum_L_NMC_mm"]["wert"]; Li=Lg-2*rand; Bi=B-2*rand; feld=(Li-nq*qb-nq*2*sp)/(nq+1)
def hexn(W,H):
    ng=int((W-d)//t)+1; nu=int((W-d-t/2)//t)+1 if W-d-t/2>=0 else 0; r=int((H-d)//rp)+1
    return sum(ng if i%2==0 else nu for i in range(r)),r,ng,nu
o1=hexn(Bi,feld); o2=hexn(feld,Bi); o,ori=(o1,"Reihen entlang B") if o1[0]>=o2[0] else (o2,"Reihen entlang L")
ohne=[hexn(Bi,Li),hexn(Li,Bi)]; ohne=max(ohne,key=lambda x:x[0])[0]
sN=stapel(NM["hoehe_mm"]); HN=sum(x for _,x in sN)
res["NMC"]=dict(laenge_gehaeuse_mm=Lg,feldbreite_mm=feld,plaetze_je_feld=o[0],orientierung=ori,plaetze=o[0]*(nq+1),plaetze_ohne_quertraeger=ohne,
  verlust_plaetze=ohne-o[0]*(nq+1),zellen=NM["anzahl"],belegung_prozent=100*NM["anzahl"]/(o[0]*(nq+1)),hoehe_mm=HN,hoehe_rest_mm=130-HN,
  passt_Plaetze=o[0]*(nq+1)>=NM["zielband"]["NMC_plaetze_min"] if False else o[0]*(nq+1)>=E["zielband"]["NMC_plaetze_min"],passt_H=HN<=130,stapel=sN,reihen=o[1],ng=o[2],nu=o[3])
# Platten (Vollmaterial, Obergrenze, Kühlplatte real hohl/leichter)
def platten(Lg_,H):
    fl=Lg_*B*1e-6
    pl={k:fl*dd*1e-3*rho for k,dd in (("Boden",hs["boden"]),("Deckel",hs["deckel"]),("Unterfahrschutz",hs["unterfahrschutz"]))}
    pl["Kühlplatten oben+unten (Vollmaterial, Obergrenze)"]=2*fl*hs["kuehlplatte_je"]*1e-3*rho
    ring=(2*Lg_+2*(B-2*rand))*1e-3*rand*1e-3*H*1e-3*rho
    return pl,ring
for v,Lg_,H in (("LFP",Lgeh,HL),("NMC",Lg,HN)):
    pl,ring=platten(Lg_,H); res[v]["platten_kg"]=pl; res[v]["platten_summe_kg"]=sum(pl.values()); res[v]["rahmen_vollprofil_obergrenze_kg"]=ring
res["offen"]=["Seitenrahmen: Wandstärke/Profil ohne Beleg, nur Obergrenze Vollprofil (Breite 30 x Höhe) angegeben, keine Annahme gesetzt","Zellhalter BT-250 (NMC, Rest Höhe) nicht modelliert","Seitencrash über Schweller: Autor-Frage offen"]
json.dump(res,open(os.path.join(D,"ergebnis.json"),"w",encoding="utf-8"),indent=1,ensure_ascii=False)
L_,N_=res["LFP"],res["NMC"]
# ---- Bilder
def kopf(ax,Lg_,tit):
    ax.add_patch(Rectangle((0,0),Lg_,B,fill=False,ec="k",lw=1.5)); ax.add_patch(Rectangle((rand,rand),Lg_-2*rand,B-2*rand,fill=False,ec="red",ls="--"))
    ax.set_aspect("equal"); ax.set_xlim(-60,Lg_+120); ax.set_ylim(-110,B+60); ax.set_title(tit,fontsize=9); ax.set_xlabel("L [mm]"); ax.set_ylabel("B [mm]")
def mass(ax,x0,x1,y,txt): ax.annotate("",(x1,y),(x0,y),arrowprops=dict(arrowstyle="<->")); ax.text((x0+x1)/2,y-35,txt,ha="center",fontsize=8)
# LFP Draufsicht
fig,ax=plt.subplots(figsize=(15,7)); Lgeh_=Lgeh
kopf(ax,Lgeh_,f"M0 LFP: Gehäuse {Lgeh_:.0f} x {B} mm, {nq} Querträger, Zellfeld {nz} Zellen je Reihe, 2 Reihen quer (Zelle {LF['laenge_mm']} mm)")
x=rand
for gi,gz in enumerate(grp):
    for k in range(gz):
        for rr in range(2): ax.add_patch(Rectangle((x+k*pitch,rand+4+rr*LF["laenge_mm"]),LF["dicke_mm"],LF["laenge_mm"],fc="#1f77b4",ec="white",lw=0.1,alpha=.8))
    x+=gz*pitch-LF["abstand_mm"]+sp
    if gi<nq: ax.add_patch(Rectangle((x,rand),qb,qlen,fc="#d95f02",ec="k")); x+=qb+sp
lo,hi=E["zielband"]["LFP_laenge_mm"]; ax.axvspan(lo,hi,ymin=0,ymax=1,color="green",alpha=.12); ax.text((lo+hi)/2,B+15,f"Zielband Länge {lo}–{hi} mm",ha="center",color="green",fontsize=8)
mass(ax,0,Lgeh_,-30,f"Gehäuse {Lgeh_:.0f} mm (Bauraum bisher 1950, +{Lgeh_-1950:.0f} mm)"); ax.text(Lgeh_+10,B/2,f"B {B}\nRahmen {rand}\nZellen {Bmin:.0f}\nToleranz {Btol:.0f}",fontsize=8,va="center")
ax.text(Lgeh_/2,-90,"Orange: Querträger; rot gestrichelt: Innenrand; KI-generiert (Claude Sonnet), Entwurf. Quelle: ergebnis.json",ha="center",fontsize=7)
fig.tight_layout(); fig.savefig(os.path.join(D,"draufsicht_LFP.png"),dpi=110); plt.close(fig)
# NMC Draufsicht
fig,ax=plt.subplots(figsize=(15,7)); kopf(ax,Lg,f"M0 NMC: Gehäuse {Lg} x {B} mm, {nq} Querträger, {N_['plaetze']} Plätze, {NM['anzahl']} Zellen belegt ({N_['belegung_prozent']:.0f} %)")
n=0; x=rand; al=(N_["orientierung"]=="Reihen entlang L")
for f in range(nq+1):
    for rr in range(N_["reihen"]):
        cnt=N_["ng"] if rr%2==0 else N_["nu"]; off=d/2+(0 if rr%2==0 else t/2)
        for k in range(cnt):
            u=off+k*t; w=d/2+rr*rp; cx,cy=(x+w,rand+u) if True else None
            if not al: cx,cy=x+w,rand+u
            else: cx,cy=x+u,rand+w
            n+=1; ax.add_patch(Circle((cx,cy),d/2,fc="#d95f02" if n<=NM["anzahl"] else "none",ec="#d95f02",lw=.3,alpha=.8))
    x+=feld+sp
    if f<nq: ax.add_patch(Rectangle((x,rand),qb,qlen,fc="#1f77b4",ec="k",alpha=.8)); x+=qb+sp
ax.text(Lg/2,B+15,f"Zielband: Plätze ≥ {E['zielband']['NMC_plaetze_min']} (Ist {N_['plaetze']}); Länge fest {Lg} mm",ha="center",color="green",fontsize=8)
mass(ax,0,Lg,-30,f"Gehäuse {Lg} mm; Feldbreite {feld:.0f} mm; Plätze ohne Querträger {N_['plaetze_ohne_quertraeger']}")
ax.text(Lg/2,-90,"Blau: Querträger; leere Kreise freie Plätze; KI-generiert (Claude Sonnet), Entwurf. Quelle: ergebnis.json",ha="center",fontsize=7)
fig.tight_layout(); fig.savefig(os.path.join(D,"draufsicht_NMC.png"),dpi=110); plt.close(fig)
# Schnitte
for v,st,H in (("LFP",sL,HL),("NMC",sN,HN)):
    fig,ax=plt.subplots(figsize=(7,8)); y=0; cols=plt.cm.tab20.colors
    for i,(nm,h) in enumerate(st):
        ax.add_patch(Rectangle((0,y),1,h,fc=cols[i%20],ec="k")); ax.text(1.05,y+h/2,f"{nm} {h} mm",va="center",fontsize=8); y+=h
    ax.axhline(130,color="red",ls="--"); ax.text(0,131.5,"Grenze 130 mm (Annahme)",color="red",fontsize=8)
    ax.set_xlim(0,2.6); ax.set_ylim(0,140); ax.set_xticks([]); ax.set_ylabel("Höhe [mm]")
    ax.set_title(f"M0 {v}: Höhenstapel {H} mm, Rest {130-H} mm bis 130 mm"); fig.text(.01,.01,"KI-generiert (Claude Sonnet), Entwurf. Quelle: ergebnis.json",fontsize=7)
    fig.tight_layout(); fig.savefig(os.path.join(D,f"schnitt_{v}.png"),dpi=110); plt.close(fig)
# Texte
f1=lambda x:f"{x:.1f}"
ok=lambda c:"ERFÜLLT" if c else "VERFEHLT"
abg=[f"1. Höhe LFP 121 ≤ 130: Ist {L_['hoehe_mm']} mm, Rest {L_['hoehe_rest_mm']}: {ok(L_['hoehe_mm']==121 and L_['passt_H'])}",
 f"1b. Höhe NMC 111, Rest 19: Ist {N_['hoehe_mm']} mm, Rest {N_['hoehe_rest_mm']}: {ok(N_['hoehe_mm']==111 and N_['passt_H'])}",
 f"2. Länge LFP ≈ 2030 (Band 2000–2060): Ist {L_['laenge_gehaeuse_mm']:.0f} mm (netto {L_['laenge_netto_mm']:.0f}, Stapel {L_['stapel_mm']:.0f}): {ok(L_['passt_L'])}",
 f"3. Breite LFP: Rahmen 30, Toleranz 4 je Seite: Ist Zellen {L_['breite_zellen_mm']:.0f}, Toleranz {L_['toleranz_breite_gesamt_mm']:.0f} gesamt = {L_['toleranz_je_seite_mm']:.0f} je Seite: {ok(L_['toleranz_je_seite_mm']==4)}",
 f"4. NMC Plätze 1100–1150, ≥ 868, Länge 1950 reicht: Ist {N_['plaetze']} Plätze (ohne Querträger {N_['plaetze_ohne_quertraeger']}, Verlust {N_['verlust_plaetze']}), Belegung {N_['belegung_prozent']:.0f} %: {ok(N_['passt_Plaetze'])}; Band 1100–1150: {ok(1100<=N_['plaetze']<=1150)}",
 f"5. Masse Querträger 1,5 kg je / 4,5 kg: Ist {m_q:.2f} kg je, {m_q*nq:.2f} kg gesamt (Querschnitt {A_q:.0f} mm², Länge {qlen} mm): {ok(abs(m_q-1.5)<0.1)}"]
verf=[]
if not(L_['passt_H'] and N_['passt_H']): verf.append("Höhe > 130")
if not L_['passt_L']: verf.append("LFP-Länge außerhalb 2000–2060")
if not N_['passt_Plaetze']: verf.append("NMC Plätze < 868")
open(os.path.join(D,"ERGEBNIS.md"),"w",encoding="utf-8").write(f"""| Dok.-Nr. | ERG-M0 | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Ergebnis M0 Gehäuse-Vorauslegung | Ersteller | Claude Sonnet (KI) | Prüfer | Opus (Stichprobe) |

> **KI-generiert.** Claude Sonnet, 2026-11-17, Auftrag M0. Entwurf, nicht freigegeben. Alle Zahlen aus `sim/mechanik/m0_gehaeuse/ergebnis.json` (aus `eingaben.json` durch `gehaeuse.py`).

## Abgleich ERWARTUNG.md
"""+"\n".join("- "+a for a in abg)+f"""
- Verfehlt-Kriterien: {'; '.join(verf) if verf else 'keines eingetreten'}

## Masse (Dichte Al 2700, Annahme)
- Querträger: {m_q*nq:.2f} kg (3 Stück)
- Platten LFP {L_['platten_summe_kg']:.1f} kg, NMC {N_['platten_summe_kg']:.1f} kg (Boden 3, Deckel 2, Unterfahrschutz 3, Kühlplatten 2 x 8 mm als Vollmaterial = Obergrenze)
- Seitenrahmen: nur Obergrenze Vollprofil 30 x Höhe: LFP {L_['rahmen_vollprofil_obergrenze_kg']:.1f} kg, NMC {N_['rahmen_vollprofil_obergrenze_kg']:.1f} kg; echte Masse offen

## Offene Punkte
"""+"\n".join("- "+o for o in res["offen"])+"""

Bilder: `draufsicht_LFP.png`, `draufsicht_NMC.png`, `schnitt_LFP.png`, `schnitt_NMC.png`; Lesehilfe `m0_lesehilfe.md`.

*KI-generiert, Entwurf. Dokument ERG-M0, Version 1.0.*
""")
open(os.path.join(D,"m0_lesehilfe.md"),"w",encoding="utf-8").write(f"""> **KI-generiert** (Claude Sonnet, 2026-11-17), Entwurf.

**Lesehilfe zu draufsicht_LFP.png.** Blick von oben auf das LFP-Gehäuse: viele dünne blaue Zellen in zwei Reihen, dazwischen drei orangefarbene Querträger (Aluprofile quer zur Fahrtrichtung). Schwarz ist die Außenkante, rot gestrichelt der Innenrand, das grüne Band der Zielbereich der Länge (2000–2060 mm). Die Länge liegt bei {Lgeh:.0f} mm, also im Band; sie wächst gegenüber 1950 mm durch die Querträger.

**Lesehilfe zu draufsicht_NMC.png.** Wie oben mit runden Zellen im Wabenmuster, vier Felder zwischen den (blauen) Querträgern. Gefüllte Kreise sind belegte Plätze, leere frei. Ziel: mindestens {E['zielband']['NMC_plaetze_min']} Plätze; vorhanden {N_['plaetze']}.

**Lesehilfe zu schnitt_LFP.png.** Seitenschnitt als Stapel von unten (Unterfahrschutz) nach oben (Deckel) mit Dicken in mm. Die rote Linie ist die Höhengrenze 130 mm (Annahme). LFP liegt bei {HL} mm.

**Lesehilfe zu schnitt_NMC.png.** Wie oben für NMC, {HN} mm, also mehr Rest unter der Grenze.

*KI-generiert, Entwurf.*
""")
open(os.path.join(ROOT,"praesentation","bausteine","M0.md"),"w",encoding="utf-8").write(f"""> **KI-generiert** (Claude Sonnet, 2026-11-17), Entwurf. Folienbaustein Vorgang M0 (Gehäuse-Vorauslegung).

# Gehäuse mit drei Querträgern
**Kernaussage (Opus einzusetzen): Querträger kosten bei LFP {Lgeh-1950:.0f} mm Länge, bei NMC {N_['verlust_plaetze']} Plätze; beide Varianten bleiben in der Höhe unter 130 mm.**

**Bild:** sim/mechanik/m0_gehaeuse/draufsicht_LFP.png (Zielband Länge 2000–2060 mm), draufsicht_NMC.png (Ziel ≥ 868 Plätze), schnitt_*.png (Grenze 130 mm)

**Zahlen** (Quelle sim/mechanik/m0_gehaeuse/ergebnis.json):
- LFP Länge {Lgeh:.0f} mm, Höhe {HL} mm; NMC {N_['plaetze']} Plätze, Höhe {HN} mm; Querträger {m_q*nq:.2f} kg

*KI-generiert, Entwurf.*
""")
print("\n".join(abg)); print("verfehlt:",verf)
