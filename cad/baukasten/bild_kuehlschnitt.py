# KI-generiert (Claude Opus, 2026-11-19). Schnittbild Kühlplatte + Kühlmodul. Aufruf: PACK_VARIANTE=LFP $FREECAD_APPIMAGE freecadcmd -c "exec(open('cad/baukasten/bild_kuehlschnitt.py').read())"
import sys; sys.path.insert(0,'/home/cae/hermes/batterie/cad/baukasten')
import kern as K
from teile import kuehlung as Q
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
c=K.Ctx(); c.schrauben=[]
pl=Q.kuehlplatte(c,{})[0]; vt=Q.verteiler(c,{}); an=Q.anschluss(c,{})
mod=[f(c,{})[0] for f in (Q.pumpe,Q.ventil,Q.chiller,Q.ausgleichsbehaelter)]; sch=Q.schlauch(c,{})
z=c.z_boden_ok+c.kp/2
fig,ax=plt.subplots(figsize=(14,8))
def zeichne(shape,fc,ec='k',lw=0.3,zz=None):
    zz=z if zz is None else zz
    for w in shape.slice(K.V(0,0,1),zz):
        pts=[(v.x,v.y) for v in w.discretize(200)]
        ax.add_patch(Polygon(pts,closed=True,fc=fc,ec=ec,lw=lw))
zeichne(pl.shape,'#b0bcc8')
for t in vt+an: zeichne(t.shape,'#7a8a99',zz=c.z_mitte_zelle)
for t in mod: zeichne(t.shape,'#333333',zz=c.z_mitte_zelle)
for t in sch: zeichne(t.shape,'#e07020',zz=c.z_mitte_zelle)
ax.set_xlim(0,2320); ax.set_ylim(0,1430); ax.set_aspect('equal')
ax.set_title('G5 Kühlplatte unten (Schnitt Wassermitte): 8 Bahnen längs, Teilkanäle 8 mm, Umlenkungen; rechts Kühlmodul (Schnitt Stutzenhöhe)',fontsize=10)
ax.set_xlabel('x mm (hinten rechts)'); ax.set_ylabel('y mm')
plt.savefig('/home/cae/hermes/batterie/cad/baukasten/bilder/kuehlplatte_maeander_schnitt.png',dpi=90,bbox_inches='tight')
