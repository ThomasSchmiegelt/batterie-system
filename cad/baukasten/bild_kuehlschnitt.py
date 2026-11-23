# KI-generiert (Claude Opus, 2026-11-19). Schnittbild Kühlplatte + Kühlmodul. Aufruf: PACK_VARIANTE=LFP $FREECAD_APPIMAGE freecadcmd -c "exec(open('cad/baukasten/bild_kuehlschnitt.py').read())"
import sys; sys.path.insert(0,'/home/cae/hermes/batterie/cad/baukasten')
import kern as K
from teile import kuehlung as Q
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
c=K.Ctx(); c.schrauben=[]
pl=Q.kuehlplatte(c,{})[0]; vt=Q.verteiler(c,{}); an=Q.anschluss(c,{}); vr=Q.verteilerrohr(c,{})
mod=[f(c,{})[0] for f in (Q.pumpe,Q.ventil,Q.chiller,Q.ausgleichsbehaelter)]; sch=Q.schlauch(c,{})
z=c.z_boden_ok+c.kp/2
c._rg=Q._rohrgeo(c) if Q._gruppiert() else {}
from matplotlib.patches import Rectangle
M=Q._maeander(c); gr=Q._gruppiert()
fig,(ax,ax2,ax3)=plt.subplots(1,3,figsize=(20,8),gridspec_kw=dict(width_ratios=[1.7,0.9,0.9]))
def zeichne(shape,fc,ec='k',lw=0.3,zz=None,axs=None):
    zz=z if zz is None else zz
    for w in shape.slice(K.V(0,0,1),zz):
        pts=[(v.x,v.y) for v in w.discretize(200)]
        for a_ in axs: a_.add_patch(Polygon(pts,closed=True,fc=fc,ec=ec,lw=lw))
AX=(ax,ax2,ax3)
zeichne(pl.shape,'#b0bcc8',axs=AX)
for t in vt+an: zeichne(t.shape,'#7a8a99',zz=c.z_mitte_zelle,axs=AX)
for t in mod: zeichne(t.shape,'#333333',zz=c.z_mitte_zelle,axs=AX)
for t in sch: zeichne(t.shape,'#e07020',zz=c.z_mitte_zelle,axs=AX)
for t in vr:     # Rohre: Draufsicht-Fläche (Hohlzylinder im Schnitt wäre nur ein Strich), Verteilerrohr oben (blau), Sammelrohr unten (rot-violett)
    bb=t.shape.BoundBox; col='#1f77d0' if t.name=='Verteilerrohr' else '#b03a8c'
    for a_ in AX: a_.add_patch(Rectangle((bb.XMin,bb.YMin),bb.XMax-bb.XMin,bb.YMax-bb.YMin,fc=col,ec='k',lw=0.4,alpha=0.55,hatch=('' if t.name=='Verteilerrohr' else '///')))
if gr:
    ys=[(b['y'][0]+b['y'][1])/2 for b in M['bahnen']]; yt=(M['bahnen'][M['gruppe']-1]['y'][1]+M['bahnen'][M['gruppe']]['y'][0])/2
    for a_ in AX: a_.axhline(yt,xmin=0,color='#d62728',lw=0.8,ls='--')
    ax.annotate(f"Trennsteg {M['trennsteg']:g} mm\n(Mäander 1 unten, Mäander 2 oben)",(900,yt),(900,yt+130),color='#d62728',fontsize=9,ha='center',arrowprops=dict(arrowstyle='->',color='#d62728'))
    ps=Q._ports(c)
    for q in ps: ax2.text(c.L+8,q['y']+22,('Ein' if q['rolle']=='ein' else 'Aus')+f" Bahn {q['bahn']+1}",fontsize=8,color='#d62728',ha='left')
    ax2.text(c._rg['x_p'],ps[0]['y']-70,'Verteilerrohr Ø25 innen\n(Ein, oben)',fontsize=8,color='#1f77d0',ha='center',va='top')
    ax2.text(c._rg['x_p']+60,ps[-1]['y']+40,'Sammelrohr Ø25 innen\n(Aus, unten)',fontsize=8,color='#b03a8c',ha='left',va='bottom')
ax.set_xlim(0,c.L+700); ax.set_ylim(0,1430); ax.set_aspect('equal')
ax3.set_xlim(20,340); ax3.set_ylim(560,880); ax3.set_aspect('equal'); ax3.set_title('Ausschnitt vorn: Trennsteg zwischen den Mäandern (Umlenkung nur innerhalb jedes Mäanders)',fontsize=8); ax3.set_xlabel('x mm')
ax2.set_xlim(c.L-250,c.L+330); ax2.set_ylim(0,1430); ax2.set_aspect('equal'); ax2.set_title('Ausschnitt hinten: Steigblöcke, Verteiler-/Sammelrohr, Stutzen',fontsize=9)
ax.set_title(f"G5 Kühlplatte unten (Schnitt Wassermitte): {M['n']//M['gruppe']} Mäander zu je {M['gruppe']} Bahnen, Teilkanäle {M['w']:g} mm; rechts Kühlmodul (Schnitt Stutzenhöhe)",fontsize=9)
fig.suptitle("Zielbild: zwei getrennte Mäander (Trennsteg rot gestrichelt), jeder mit eigenem Ein- und Austritt hinten. Platte oben liegt gleich; gegenläufige Durchströmung ist im CAD nicht abgebildet.\nLesehilfe: Blau = Verteilerrohr (kaltes Wasser kommt hinein), violett = Sammelrohr (warmes Wasser geht ab). Beide Rohre liegen hinter dem Rahmen übereinander (Draufsicht überlagert, Sammelrohr schraffiert).",fontsize=8)
ax.set_xlabel('x mm (hinten rechts)'); ax.set_ylabel('y mm'); ax2.set_xlabel('x mm')
plt.savefig('/home/cae/hermes/batterie/cad/baukasten/bilder/kuehlplatte_maeander_schnitt.png',dpi=90,bbox_inches='tight')
