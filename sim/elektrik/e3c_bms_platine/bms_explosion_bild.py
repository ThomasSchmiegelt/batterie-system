#!/usr/bin/env python3
"""E3c Beschriftung der Blender-Explosionsansicht (explosion_roh.png, explosion_anker.json) und des Einbaubilds (einbau_roh.png, einbau_anker.json). KI-generiert (Claude Sonnet, 2026-11-24), Entwurf.
Zahlen: ergebnis_platine.json."""
import json, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from PIL import Image
H = "/home/cae/hermes/batterie/sim/elektrik/e3c_bms_platine"; O = "/home/cae/cae_projekte/batterie/e3c"; r = json.load(open(f"{H}/ergebnis_platine.json")); sz = r["sperrzone"]
BOX = dict(boxstyle="round,pad=0.25", fc="white", ec="0.6", alpha=0.92)
# ---- Explosion
a = json.load(open(f"{H}/explosion_anker.json")); A = a["anker"]; im = Image.open(f"{O}/roh/explosion_roh.png"); w, h = im.size
fig = plt.figure(figsize=(14, 14 * h / w / 1.42 + 1.5)); ax = fig.add_axes([0, 0.1, 1, 0.82]); ax.imshow(im); ax.axis("off"); ax.set_xlim(-0.06 * w, 1.42 * w)
L = [("Bauteile", f"Bauteile oben: {r['teile']} Teile (Rechner, CAN, Schützansteuerung,\nShunt-ADC, Daisy-Master, Übertrager, Isolatoren, Stecker)", 0.08),
     ("F.Cu", "F.Cu: Bahnen und Lötflächen, 70 µm (Annahme wie E3)", 0.21), ("Substrat", f"Substrat FR4, {r['lagen']} Lagen, 1,6 mm (BT-311, ENT-190)", 0.33),
     ("In1.Cu", "In1.Cu: Masseflächen, links GND (NV), rechts HV_GND (HV),\ndazwischen kupferfrei", 0.45), ("In2.Cu", "In2.Cu: Signale und Versorgung (keine Fläche)", 0.57),
     ("B.Cu", "B.Cu: Masseflächen wie In1 (GND links, HV_GND rechts)", 0.69)]
for k, txt, y in L:
    ax.annotate(txt, xy=(A[k][0] * w, A[k][1] * h), xytext=(w * 1.03, A[k][1] * h), fontsize=8.3, ha="left", va="center", arrowprops=dict(arrowstyle="-", color="0.25", lw=0.8), bbox=BOX)
ax.annotate(f"Sperrzone HV/NV (rot): {sz['breite_mm']:g} mm breit, durchgehend über alle Lagen,\nKriechstrecke gemessen {sz['abstand_nv_hv_kupfer_mm']:g} mm (Soll >= {sz['kriech_mm']:g} mm, ENT-191)", xy=(A["Sperrzone"][0] * w, A["Sperrzone"][1] * h), xytext=(w * 0.02, 0.10 * h),
            fontsize=8.6, ha="left", va="center", color="darkred", arrowprops=dict(arrowstyle="-", color="darkred", lw=1.0), bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="darkred", alpha=0.92))
ax.annotate(f"Vias als dünne Stäbe durch alle Lagen: {a['vias_gesamt']} gesamt", xy=(A["Vias"][0] * w, A["Vias"][1] * h), xytext=(w * 0.02, 0.93 * h), fontsize=8.3, ha="left", va="center", arrowprops=dict(arrowstyle="-", color="0.25", lw=0.8), bbox=BOX)
fig.text(0.5, 0.965, "E3c BMS-Platine BT-311: Explosionsansicht nach Lagen (Blender) mit hervorgehobener Sperrzone. Akten BT-311, ENT-188…191", ha="center", fontsize=10.5, fontweight="bold")
fig.text(0.5, 0.062, "Lesehilfe: Die Lagen der Platine sind nach oben auseinandergezogen (Abstand je Lage 11 mm, nur Darstellung). Die rot durchsichtige Platte ist die Sperrzone: Hier gibt es auf keiner Lage Kupfer.\n"
         f"Nur {len(sz['bruecken'])} Bauteile (2 Übertrager, 2 digitale Isolatoren) ragen über die Platte. Kupferdicke überhöht (0,35 mm statt 0,07 mm). Zielband: entfällt (Geometriebild), Sperrzone und Soll stehen in der Beschriftung.", ha="center", fontsize=8, va="center")
fig.text(0.5, 0.018, "KI-generiert (Claude Sonnet, 2026-11-24), Entwurf. Quelle: bms.kicad_pcb, bms.step, ergebnis_platine.json. Blender-Datei: cae_projekte/batterie/e3c/explosion.blend", ha="center", fontsize=8)
fig.savefig(f"{H}/platine_bms_explosion.png", dpi=110); plt.close(fig)
# ---- Einbau
import os
if os.path.exists(f"{O}/roh/einbau_roh.png"):
    e = json.load(open(f"{H}/einbau_anker.json")); A = e["anker"]; im = Image.open(f"{O}/roh/einbau_roh.png"); w, h = im.size; pa = r["passt"]
    fig = plt.figure(figsize=(12, 12 * h / w + 1.5)); ax = fig.add_axes([0, 0.1, 1, 0.82]); ax.imshow(im); ax.axis("off")
    ax.annotate(f"BMS-Platine BT-311, {r['laenge_mm']:g} x {r['breite_mm']:g} mm, Bauhöhe {pa['platine_h_mm']:g} mm", xy=(A["platine"][0] * w, A["platine"][1] * h), xytext=(w * 0.03, 0.06 * h), fontsize=9, ha="left", va="center", arrowprops=dict(arrowstyle="-", color="0.2", lw=1), bbox=BOX)
    ax.annotate(f"Zielband (rot): Platz des BMS in der Schaltbox = BT-310, {pa['bt310_mm']['laenge_mm']:g} x {pa['bt310_mm']['breite_mm']:g} mm, Höhe {pa['bt310_mm']['hoehe_mm']:g} mm (ENT-139/140/141)", xy=(A["platz"][0] * w, A["platz"][1] * h), xytext=(w * 0.03, 0.12 * h), fontsize=9, ha="left", va="center", color="darkred", arrowprops=dict(arrowstyle="-", color="darkred", lw=1), bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="darkred", alpha=0.92))
    ax.annotate(f"Sperrzone {sz['breite_mm']:g} mm", xy=(A["sperrzone"][0] * w, A["sperrzone"][1] * h), xytext=(w * 0.60, 0.06 * h), fontsize=9, ha="left", va="center", color="darkred", arrowprops=dict(arrowstyle="-", color="darkred", lw=1), bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="darkred", alpha=0.92))
    ok = "passt" if pa["laenge_ok"] and pa["breite_ok"] and pa["hoehe_ok"] else "passt nicht"
    fig.text(0.5, 0.965, f"E3c BMS-Platine BT-311 in der offenen Schaltbox (LFP-Pack, Deckel abgenommen): {ok}", ha="center", fontsize=10.5, fontweight="bold")
    fig.text(0.5, 0.062, "Lesehilfe: Blick von schräg oben in die geöffnete Schaltbox (Wanne durchsichtig, Inhalt grau). Die grüne Platine mit ihren Bauteilen liegt in der Ecke des BMS-Platzes (rote Umrandung = Zielband).\n"
             "Die rote durchsichtige Platte ist die Sperrzone zwischen Niedervolt- und Hochvoltseite. Die Platine ist kleiner als der Platz, der Rest bleibt frei. Der graue Inhalt (Schütze, Shunt, Sicherungen) stammt aus dem E2-Modell.", ha="center", fontsize=8, va="center")
    fig.text(0.5, 0.018, "KI-generiert (Claude Sonnet, 2026-11-24), Entwurf. Quelle: cad/pack/entwurf/ergebnis_LFP_e2d_e3.json (BMS-Platz), ergebnis_platine.json. Darstellung: Platinenecke = Ecke des BMS-Platzes (Lage nicht festgelegt).", ha="center", fontsize=8)
    fig.savefig(f"{H}/platine_bms_einbau.png", dpi=110); plt.close(fig)
