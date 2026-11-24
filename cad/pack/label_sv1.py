#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-24), Entwurf. SV1: Beschriftung (PIL) der Rohbilder aus render_sv1.py -> sim/mechanik/sv1_stecker_verschraubung/sv1_<V>_<ansicht>.png.
Zahlen nur aus cad/pack/entwurf/ergebnis_<V>_e2d_e3c_sv1.json. Aufruf: python3 label_sv1.py [LFP,NMC]"""
import json, sys, os
from PIL import Image, ImageDraw, ImageFont
R = "/home/cae/hermes/batterie"; NZ = "/home/cae/cae_projekte/batterie/e2/render"; ZIEL = f"{R}/sim/mechanik/sv1_stecker_verschraubung"
TITEL = {"schaltbox": "Schaltbox offen mit Steckern, Gegenstücken, Steckfreigängen", "endzone": "Endzone hinten: CMU-Stecker, Steckfreigänge, M3-Schrauben"}
LEG = [((0, 128, 255), "Stecker (beweglich, transparent)"), ((13, 38, 115), "Gegenstück (fest)"), ((242, 13, 13), "Steckfreigang (rot, halbtransparent)"), ((255, 217, 0), "Schrauben, Bolzen"), ((153, 158, 166), "übrige Teile (grau)")]
LESE = ["Lesehilfe: Ein Stecker braucht Platz, um gesteckt und", "gezogen zu werden. Dieser Raum (rot) darf nicht von festen", "Teilen belegt sein. Ragt ein festes Teil in einen roten", "Körper, steht es in der Tabelle im Ergebnis (Verletzung)."]
def font(sz, b=False):
    f = "/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf" % ("-Bold" if b else ""); return ImageFont.truetype(f, sz) if os.path.exists(f) else ImageFont.load_default()
for v in (sys.argv[1] if len(sys.argv) > 1 else "LFP,NMC").split(","):
    r = json.load(open(f"{R}/cad/pack/entwurf/ergebnis_{v}_e2d_e3c_sv1.json")); s = r["e2"]["sv1"]
    for a in TITEL:
        p = f"{NZ}/roh_{v}_sv1_{a}.png"
        if not os.path.exists(p): continue
        im = Image.open(p).convert("RGB"); W, H = im.size; P = 480; kopf = 84; fuss = 44; c = Image.new("RGB", (W + P, H + kopf + fuss), (255, 255, 255)); c.paste(im, (0, kopf)); d = ImageDraw.Draw(c)
        d.text((16, 8), f"Pack {v}: {TITEL[a]}", font=font(26, True), fill=(20, 20, 20))
        d.text((16, 46), f"Steckfreigang-Verletzungen {r['anzahl_steckfreigang_verletzungen']}, harte Kollisionen {r['anzahl_kollisionen']}, Zusatzmasse {s['masse_zusatz_kg']:.2f} kg, Stecker {s['anzahl_stecker']}, Schrauben/Bolzen {s['anzahl_schrauben_bolzen']}", font=font(15), fill=(20, 20, 20))
        d.rectangle([W + P - 330, 8, W + P - 10, 40], outline=(160, 20, 20), width=2, fill=(255, 235, 235)); d.text((W + P - 322, 13), "KI-generiert · Entwurf", font=font(18, True), fill=(160, 20, 20))
        y = kopf + 20
        for col, t in LEG: d.rectangle([W + 14, y, W + 34, y + 18], fill=col, outline=(60, 60, 60)); d.text((W + 44, y), t, font=font(14), fill=(20, 20, 20)); y += 28
        y += 14
        for t in LESE: d.text((W + 14, y), t, font=font(14), fill=(20, 20, 20)); y += 22
        y += 12; d.text((W + 14, y), "Zielband: 0 Verletzungen (Erwartung 1-3, Annahme", font=font(13, True), fill=(20, 20, 20)); d.text((W + 14, y + 20), "ERW-SV1, nicht freigegeben)", font=font(13, True), fill=(20, 20, 20))
        d.text((16, H + kopf + 12), f"KI-generiert (Claude Sonnet, 2026-11-24), Entwurf, nicht freigegeben. Quelle: cad/pack/entwurf/ergebnis_{v}_e2d_e3c_sv1.json; Maße sind Annahmen ERW-SV1. Lesehilfe oben rechts.", font=font(13), fill=(90, 90, 90))
        c.save(f"{ZIEL}/sv1_{v}_{a}.png")
