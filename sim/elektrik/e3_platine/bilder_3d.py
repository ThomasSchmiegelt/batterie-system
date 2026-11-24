#!/usr/bin/env python3
"""E3 3D-Bilder aus KiCad-Renderings mit Kopfzeile und Lesehilfe. KI-generiert (Claude Sonnet, 2026-11-24), Entwurf. Zahlen aus ergebnis_platine.json."""
import json, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from PIL import Image
O = "/home/cae/cae_projekte/batterie/e3"; H = "/home/cae/hermes/batterie/sim/elektrik/e3_platine"; p = json.load(open(f"{H}/ergebnis_platine.json"))
T = {"iso": ("Schrägansicht", "Die Platine von schräg oben: Bauteile, daneben die hellen Linien der Leiterbahnen und gelben Ringe der Durchkontaktierungen."),
     "top": ("Oberseite", "Draufsicht auf die Bestückung. Die Leiterbahnen auf F.Cu schimmern durch die grüne Lötstoppmaske."),
     "bottom": ("Unterseite", "Die Unterseite trägt keine Bauteile. Zu sehen sind nur die Bahnen auf B.Cu und die Durchkontaktierungen (Punkte)."),
     "nah": ("Nahaufnahme Ausgleichskanal", "Ein Ausgleichskanal: zwei große Widerstände (verheizen Ladung), kleiner Schalter (FET), Filter. Die Vias unter den Widerständen leiten Wärme in die unteren Lagen.")}
for V in ("LFP", "NMC"):
    r = p[V]
    for k, (t, lh) in T.items():
        im = Image.open(f"{O}/r3d_{V}_{k}.png"); w, h = im.size
        fig = plt.figure(figsize=(10, 10 * h / w + 1.2)); ax = fig.add_axes([0, 0.1, 1, 0.8]); ax.imshow(im); ax.axis("off")
        fig.text(0.5, 0.96, f"E3 CMU-Platine {V}: {t} (KiCad 3D). Umriss {r['laenge_mm']:g} x {r['breite_mm']:g} mm, 4 Lagen, DRC {r['drc_verstoesse']} Verstöße, {r['drc_unverbunden']} offen", ha="center", fontsize=10)
        fig.text(0.5, 0.045, f"Lesehilfe: {lh}", ha="center", fontsize=8.5, wrap=True)
        fig.text(0.5, 0.012, "KI-generiert (Claude Sonnet, 2026-11-24), Entwurf. Quelle: cmu_" + V + ".kicad_pcb (Opus-Akten ENT-163…193)", ha="center", fontsize=8)
        fig.savefig(f"{H}/platine_{V}_3d_{k}.png", dpi=110); plt.close(fig)
