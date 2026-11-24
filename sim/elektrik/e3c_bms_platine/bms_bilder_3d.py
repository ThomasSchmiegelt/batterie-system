#!/usr/bin/env python3
"""E3c 3D-Bilder aus KiCad-Renderings mit Kopfzeile und Lesehilfe (Muster: e3_platine/bilder_3d.py). KI-generiert (Claude Sonnet, 2026-11-24), Entwurf. Zahlen aus ergebnis_platine.json."""
import json, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from PIL import Image
O = "/home/cae/cae_projekte/batterie/e3c"; H = "/home/cae/hermes/batterie/sim/elektrik/e3c_bms_platine"; r = json.load(open(f"{H}/ergebnis_platine.json"))
T = {"iso": ("Schrägansicht", "Die BMS-Platine von schräg oben. Links der große Rechner-Chip, unten die drei Schützkanäle, rechts hinter dem glatten Streifen die Hochvoltseite. Die vier hellen Blöcke überbrücken die Sperrzone."),
     "top": ("Oberseite", "Draufsicht auf die Bestückung. Die Leiterbahnen schimmern durch die grüne Lötstoppmaske. In der Mitte rechts die Sperrzone: ein 10 mm breiter Streifen ohne Kupfer."),
     "bottom": ("Unterseite", "Die Unterseite trägt keine Bauteile, nur Leiterbahnen, Durchkontaktierungen und die große Massefläche (Spiegelbild der Oberseite: der Streifen ohne Kupfer ist die Sperrzone)."),
     "nah": ("Nahaufnahme Sperrzone", "Ausschnitt an der Sperrzone: Die hellen Blöcke (Übertrager und Isolator) sind die einzigen Teile, die den kupferfreien Streifen überbrücken. Alles andere endet davor.")}
for k, (t, lh) in T.items():
    im = Image.open(f"{O}/r3d_{k}.png"); w, h = im.size
    fig = plt.figure(figsize=(10, 10 * h / w + 1.2)); ax = fig.add_axes([0, 0.1, 1, 0.8]); ax.imshow(im); ax.axis("off")
    fig.text(0.5, 0.96, f"E3c BMS-Platine BT-311: {t} (KiCad 3D). Umriss {r['laenge_mm']:g} x {r['breite_mm']:g} mm, {r['lagen']} Lagen, DRC {r['drc_verstoesse']} Verstöße, {r['drc_unverbunden']} offen", ha="center", fontsize=10)
    fig.text(0.5, 0.045, f"Lesehilfe: {lh}", ha="center", fontsize=8.0, wrap=True)
    fig.text(0.5, 0.012, "KI-generiert (Claude Sonnet, 2026-11-24), Entwurf. Quelle: bms.kicad_pcb (Akten ENT-188…191, ERW-E3c)", ha="center", fontsize=8)
    fig.savefig(f"{H}/platine_bms_3d_{k}.png", dpi=110); plt.close(fig)
