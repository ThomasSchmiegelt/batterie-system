# KI-generiert (Claude Sonnet, 2026-11-24), Entwurf. Beschriftet die Blender-Explosionsansicht (explosion_<V>_roh.png, _anker.json). Zahlen: ergebnis_platine.json, thermovias_<V>.json, explosion_<V>_anker.json.
import json, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from PIL import Image
H = "/home/cae/hermes/batterie/sim/elektrik/e3_platine"; P = json.load(open(f"{H}/ergebnis_platine.json"))
for V in ("LFP", "NMC"):
    r = P[V]; a = json.load(open(f"{H}/explosion_{V}_anker.json")); A = a["anker"]; t = r["thermovias"]; im = Image.open(f"/home/cae/cae_projekte/batterie/e3/roh/explosion_{V}_roh.png"); w, h = im.size
    fig = plt.figure(figsize=(12, 12 * h / w + 1.5)); ax = fig.add_axes([0, 0.1, 1, 0.82]); ax.imshow(im); ax.axis("off")
    L = [("Bauteile", f"Bauteile oben: {r['teile']} Teile\n(Widerstände 2512, FETs, AFE, Übertrager, Stecker)", 0.10),
         ("F.Cu", "F.Cu: Kupfer 70 µm, Bahn 0,2 mm,\nAbstand 0,2 mm (ENT-168)", 0.20),
         ("Substrat", "Substrat FR4, 4 Lagen, 1,6 mm (BT-321)", 0.30),
         ("In1.Cu", "In1.Cu: Innenlage", 0.40), ("In2.Cu", "In2.Cu: Innenlage", 0.50),
         ("B.Cu", f"B.Cu: je Widerstandsnetz eine Kupferfläche\nunter dem Paar (ENT-187), {t['flaechen_bcu']} Flächen", 0.60),
         ("Pad", "Wärmeleitpad 1,0 mm (ENT-185), elektrisch isolierend", 0.71),
         ("Rahmen", "Al-Rahmen mit Ausschnitt für die CMU\n(Darstellung, Maß = Platine)", 0.86)]
    for k, txt, y in L:
        x0, y0 = A[k][0] * w, A[k][1] * h
        ax.annotate(txt, xy=(x0, y0), xytext=(w * 0.70, (y) * h), fontsize=8.3, ha="left", va="center", arrowprops=dict(arrowstyle="-", color="0.25", lw=0.8), bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="0.6", alpha=0.92))
    ax.annotate(f"Vias 0,6/0,3 mm als Stäbe (Kupfer, dünn), {a['vias_gesamt']} gesamt", xy=(A["Vias"][0] * w, A["Vias"][1] * h), xytext=(w * 0.02, 0.93 * h), fontsize=8.3, ha="left", va="center", arrowprops=dict(arrowstyle="-", color="0.25", lw=0.8), bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="0.6", alpha=0.92))
    ax.annotate(f"Thermovias (orange): {t['vias_gesetzt']} von {t['vias_soll']} (ENT-187, 8 je Widerstandspaar)", xy=(A["Thermovias"][0] * w, A["Thermovias"][1] * h), xytext=(w * 0.02, 0.985 * h), fontsize=8.3, ha="left", va="center", color="#b03000", arrowprops=dict(arrowstyle="-", color="#b03000", lw=0.8), bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="#b03000", alpha=0.92))
    fig.text(0.5, 0.965, f"E3 CMU-Platine {V}: Explosionsansicht nach Lagen (Blender). Akten BT-321, ENT-168, ENT-185, ENT-187", ha="center", fontsize=10.5, fontweight="bold")
    fig.text(0.5, 0.062, "Lesehilfe: Die Lagen der Platine sind nach oben auseinandergezogen (Abstand je Lage 11 mm, nur Darstellung). Kupfer ist kupferfarben, die orangen Stäbe sind die Thermovias unter den Ausgleichswiderständen,\n"
             "sie leiten die Wärme durch alle Lagen auf die Kupferflächen unten und von dort ins Wärmeleitpad und den Al-Rahmen. Kupferdicke überhöht (0,35 mm statt 0,07 mm). Zielband: entfällt (Geometriebild).", ha="center", fontsize=8, va="center")
    fig.text(0.5, 0.018, f"KI-generiert (Claude Sonnet, 2026-11-24), Entwurf. Quelle: cmu_{V}.kicad_pcb, cmu_{V}.step, thermovias_{V}.json. Blender-Datei: cae_projekte/batterie/e3/explosion_{V}.blend", ha="center", fontsize=8)
    fig.savefig(f"{H}/platine_{V}_explosion.png", dpi=110); plt.close(fig)
