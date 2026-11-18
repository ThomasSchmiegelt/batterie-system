# KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. Auftrag G2: PNG je Variante aus der Tessellierung (netz_<V>.json) und ergebnis_<V>.json; Zahlen nur aus ergebnis.
import json, os, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entwurf")
FARBE = {"Gehaeuse": "#8aa4b8", "Pol_plus": "#c0392b", "Pol_minus": "#1f3a5f"}

def teile(t, maxl):
    """Dreiecke so lange unterteilen, bis die längste Kante <= maxl ist (nur für saubere Tiefensortierung im Bild)."""
    aus = []; stapel = [t]
    while stapel:
        a, b, c = stapel.pop(); k = [np.linalg.norm(a-b), np.linalg.norm(b-c), np.linalg.norm(c-a)]
        if max(k) <= maxl: aus.append(np.array([a, b, c])); continue
        i = int(np.argmax(k)); P = [a, b, c]; m = (P[i] + P[(i+1) % 3]) / 2
        stapel += [(P[i], m, P[(i+2) % 3]), (m, P[(i+1) % 3], P[(i+2) % 3])]
    return aus

def zeichne(ax, netz, lim, aspekt):
    tris, fc, ec = [], [], []
    for n, m in netz.items():
        p = np.array(m["punkte"]); t = np.array(m["dreiecke"]); fein = [x for tr in p[t] for x in teile(tr, 8.0)]; tris.append(np.array(fein)); fc += [FARBE[n]] * len(fein); ec += ["#2b2b2b" if n != "Gehaeuse" else "#6b8296"] * len(fein)
    pc = Poly3DCollection(np.concatenate(tris), facecolors=fc, edgecolors=ec, linewidths=0.05)  # eine Sammlung: gemeinsame Tiefensortierung
    ax.add_collection3d(pc)
    ax.set_xlim(*lim[0]); ax.set_ylim(*lim[1]); ax.set_zlim(*lim[2]); ax.set_box_aspect(aspekt); ax.view_init(elev=24, azim=-58)
    ax.set_xlabel("x [mm]"); ax.set_ylabel("y [mm]"); ax.set_zlabel("z [mm]")

for v in ("LFP", "NMC"):
    e = json.load(open(f"{D}/ergebnis_{v}.json")); netz = json.load(open(f"{D}/netz_{v}.json"))
    a = e["annahmen"]; me = e["masse_eingabe"]
    fig = plt.figure(figsize=(13, 6.2))
    fig.suptitle("Entwurf – Akten vorgeschlagen", fontsize=15, fontweight="bold", color="#b03a2e")
    if v == "LFP":
        L, B, Dk = me["laenge_mm"], me["breite_mm"], me["dicke_mm"]; h = a["ANNAHME_POL_HOEHE_MM"]
        ax1 = fig.add_subplot(121, projection="3d")
        zeichne(ax1, netz, [(-h, L + h), (0, B), (0, Dk)], (L, B * 3, Dk * 3))
        ax1.set_title(f"LFP verkürzte Blade, gesamt (maßstäblich in x; y, z überhöht)", fontsize=10)
        ax2 = fig.add_subplot(122, projection="3d")
        zeichne(ax2, netz, [(L - 40, L + h), (0, B), (0, Dk)], (40 + h, B, Dk))
        ax2.set_title("Ausschnitt Pluspol-Stirnseite (Pol = Annahme)", fontsize=10)
        txt = (f"L × B × D = {L:.0f} × {B:.0f} × {Dk:.0f} mm, Wand {e['wandstaerke_mm']} mm\n"
               f"Außenvolumen {e['aussenvolumen_L']:.3f} L; {e['energie_Wh']:.1f} Wh → {e['Wh_pro_L']:.1f} Wh/L\n"
               f"Pole ANNAHME: Ø {a['ANNAHME_POL_DURCHMESSER_MM']} mm, {a['ANNAHME_POL_HOEHE_MM']} mm Überstand, beidseitig")
    else:
        Dm, H = me["durchmesser_mm"], me["hoehe_mm"]; h = a["ANNAHME_NMC_POL_HOEHE_MM"]
        ax1 = fig.add_subplot(121, projection="3d")
        zeichne(ax1, netz, [(-Dm/2, Dm/2), (-Dm/2, Dm/2), (0, H + h)], (1, 1, (H + h) / Dm))
        ax1.set_title("NMC 4680 Rundzelle (Becher, Wand dargestellt)", fontsize=10)
        ax2 = fig.add_subplot(122, projection="3d")
        zeichne(ax2, netz, [(-Dm/2, Dm/2), (-Dm/2, Dm/2), (H - 15, H + h)], (1, 1, (15 + h) / Dm * 0.6))
        ax2.set_title("Ausschnitt Kopf: Pluspol oben (Annahme); Minus = Becherrand", fontsize=10)
        txt = (f"Ø × H = {Dm:.0f} × {H:.0f} mm, Wand {e['wandstaerke_mm']} mm\n"
               f"Außenvolumen {e['aussenvolumen_L']:.4f} L; {e['energie_Wh']:.1f} Wh → {e['Wh_pro_L']:.1f} Wh/L\n"
               f"Pluspol ANNAHME: Ø {a['ANNAHME_NMC_POL_DURCHMESSER_MM']} mm, {a['ANNAHME_NMC_POL_HOEHE_MM']} mm Überstand; Minuspol = Becherrand (kein eigenes Maß)")
    fig.text(0.5, 0.04, txt, ha="center", va="bottom", fontsize=10, bbox=dict(boxstyle="round", fc="#fdf2e9", ec="#b03a2e"))
    fig.text(0.5, 0.005, "KI-generiert (Claude Sonnet), Entwurf, nicht freigegeben. Quelle: cad/zelle/entwurf/ergebnis_%s.json" % v, ha="center", fontsize=8, color="#555")
    fig.subplots_adjust(top=0.9, bottom=0.2, left=0.02, right=0.98, wspace=0.05)
    fig.savefig(f"{D}/zelle_{v}.png", dpi=130); plt.close(fig); print("png", v)
