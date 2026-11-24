# KI-generiert (Claude Sonnet, 2026-11-24), Entwurf. Beschriftet die Einbau-Renderings (einbau_<V>_uebersicht_roh.png, einbau_<V>_nah_roh.png, einbau_<V>_anker.json). Zahlen: cad/pack/entwurf/ergebnis_<V>_e2d_e3.json, ergebnis_platine.json.
import json, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from PIL import Image
H = "/home/cae/hermes/batterie/sim/elektrik/e3_platine"; R = "/home/cae/hermes/batterie/cad/pack/entwurf"; P = json.load(open(f"{H}/ergebnis_platine.json"))
for V in ("LFP", "NMC"):
    pk = json.load(open(f"{R}/ergebnis_{V}_e2d_e3.json")); e3 = pk["e3"]; A = json.load(open(f"{H}/einbau_{V}_anker.json")); m = P[V]["masse"]
    a, b = Image.open(f"/home/cae/cae_projekte/batterie/e3/roh/einbau_{V}_uebersicht_roh.png"), Image.open(f"/home/cae/cae_projekte/batterie/e3/roh/einbau_{V}_nah_roh.png")
    fig = plt.figure(figsize=(12, 11.4)); ax1 = fig.add_axes([0.02, 0.56, 0.96, 0.36]); ax1.imshow(a); ax1.axis("off"); ax2 = fig.add_axes([0.02, 0.11, 0.96, 0.43]); ax2.imshow(b); ax2.axis("off")
    ov = A["uebersicht"]; w1, h1 = a.size; w2, h2 = b.size
    for k, (cx, cy) in enumerate(ov["cluster"]):
        ax1.annotate("CMU-Platinen (orange) in den Endzonen" if k == 0 else "", xy=(cx * w1, cy * h1), xytext=(w1 * 0.04, h1 * 0.93) if k == 0 else (w1 * 0.04, h1 * 0.93), fontsize=9, arrowprops=dict(arrowstyle="-", lw=0.9, color="0.2"), bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="0.6") if k == 0 else None)
    n = A["nah"]
    ax2.annotate(f"CMU-Platinen in der Endzone (je {e3['platine_mm'][0]:g} x {e3['platine_mm'][1]:g} mm,\n{e3['platine_mm'][2]:g} mm hoch mit Bauteilen; Wärmeleitpad ENT-185 dahinter)", xy=(n["cmu"][0] * w2, n["cmu"][1] * h2), xytext=(w2 * 0.52, h2 * 0.12), fontsize=9, arrowprops=dict(arrowstyle="-", lw=0.9, color="0.2"), bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="0.6"))
    ax2.annotate("Boden/Rahmen (grau, durchsichtig)", xy=(n["boden"][0] * w2, n["boden"][1] * h2), xytext=(w2 * 0.05, h2 * 0.92), fontsize=9, arrowprops=dict(arrowstyle="-", lw=0.9, color="0.2"), bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="0.6"))
    fig.text(0.5, 0.965, f"E3 CMU am Einbauort im Pack {V}: {e3['anzahl_cmu']} CMU in den Endzonen (Blender). Pack {pk['laenge_mm']:.0f} x {pk['breite_mm']:.0f} mm", ha="center", fontsize=10.5, fontweight="bold")
    fig.text(0.5, 0.06, f"Lesehilfe: Oben das ganze Pack von schräg oben, Zellen und Deckel ausgeblendet, alles außer den CMU grau und durchsichtig. Die orangen Streifen sind die Platinen (je {m['gesamt_mit_pad_g']:.1f} g mit Wärmeleitpad, {m['platine_ohne_pad_g']:.1f} g ohne).\n"
             f"Unten die Platinen einer Endzone aus der Nähe. Kollisionen im Pack mit CMU: {sum(1 for k in pk['kollisionen'] if k['a'].startswith('CMU') or k['b'].startswith('CMU'))}. Zielband: entfällt (Geometriebild).", ha="center", fontsize=8, va="center")
    fig.text(0.5, 0.018, f"KI-generiert (Claude Sonnet, 2026-11-24), Entwurf. Quelle: cad/pack/entwurf/ergebnis_{V}_e2d_e3.json, pack_{V}_e2d_e3.step, ergebnis_platine.json", ha="center", fontsize=8)
    fig.savefig(f"{H}/platine_{V}_einbau.png", dpi=110); plt.close(fig)
