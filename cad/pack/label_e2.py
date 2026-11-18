#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-18), Entwurf. Auftrag E2 Fortsetzung 2. Beschriftung (PIL) der Rohbilder aus render_e2.py -> sim/elektrik/e2_elektronik/e2_<V>_<ansicht>.png.
Zahlen (Maße, Höhen) nur aus cad/pack/entwurf/ergebnis_<V>_e2.json. Aufruf: python3 label_e2.py [LFP,NMC]"""
import json, sys, os
from PIL import Image, ImageDraw, ImageFont
R = "/home/cae/hermes/batterie"; OUT = f"{R}/cad/pack/entwurf"; NZ = "/home/cae/cae_projekte/batterie/e2/render"; ZIEL = f"{R}/sim/elektrik/e2_elektronik"
TITEL = {"gesamt": "Gesamtansicht (Zellen ausgeblendet)", "draufsicht": "Draufsicht ohne Deckel: CMU, FPC, HV-Leitungen", "schnitt": "Schnitt durch die Schaltbox (Ebene durch die Boxmitte)", "detail": "Detail: CMU und FPC an der Endzone (Deckel, Kühlplatte oben, Pad oben ausgeblendet)"}
LEG = [((217, 13, 13), "CMU-Platine (hochkant)"), ((255, 191, 0), "FPC-Messleitung"), ((217, 0, 179), "HV-Leitung"), ((26, 140, 64), "Schaltbox (Gehäuse)"), ((51, 217, 115), "Inhalt Schaltbox"), ((0, 115, 242), "Stecker, Sensor, Trennstecker"), ((140, 145, 153), "übrige Teile (grau, teils transparent)")]
def font(sz, b=False):
    f = "/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf" % ("-Bold" if b else "")
    return ImageFont.truetype(f, sz) if os.path.exists(f) else ImageFont.load_default()
def main(v, a):
    r = json.load(open(f"{OUT}/ergebnis_{v}_e2.json")); e = r["e2"]; J = json.load(open(f"{NZ}/roh_{v}_{a}.json")); im = Image.open(f"{NZ}/roh_{v}_{a}.png").convert("RGB")
    W, H = im.size; P = 380; kopf = 84; fuss = 40; c = Image.new("RGB", (W + P, H + kopf + fuss), (255, 255, 255)); c.paste(im, (0, kopf)); d = ImageDraw.Draw(c)
    d.text((16, 8), f"Pack {v}: {TITEL[a]}", font=font(26, True), fill=(20, 20, 20))
    d.text((16, 46), f"Gehäuse {r['gehaeuse_L_mm']:.0f} x {r['breite_mm']:.0f} mm, Schaltbox hinten {e['schaltbox_L_mm']:.0f} x {e['schaltbox_B_mm']:.0f} x {e['schaltbox_H_mm']:.0f} mm, Packhöhe mit Turm {r['hoehe_mm']:.0f} mm, {r['anzahl_kollisionen']} Kollisionen", font=font(15), fill=(50, 50, 50))
    d.rectangle([W + P - 330, 8, W + P - 10, 40], outline=(160, 20, 20), width=2, fill=(255, 235, 235)); d.text((W + P - 322, 13), "KI-generiert · Entwurf", font=font(18, True), fill=(160, 20, 20))
    y = kopf + 20
    for col, t in LEG: d.rectangle([W + 14, y, W + 34, y + 18], fill=col, outline=(60, 60, 60)); d.text((W + 44, y), t, font=font(14), fill=(20, 20, 20)); y += 30
    pm = J["res"][0] / J["scale_mm"]; cx, cy, cz = J["centre_mm"]
    if a in ("draufsicht", "schnitt"):
        bar = 200 * pm; x0 = 20; yb = H + kopf - 28; d.rectangle([x0, yb, x0 + bar, yb + 8], fill=(20, 20, 20)); d.text((x0 + bar + 8, yb - 5), "200 mm", font=font(14), fill=(20, 20, 20))
    if a == "schnitt":
        hmax = e["hoehe_max_A_mm"]; ztop = r["hoehe_mm"]
        for z, txt, col in ((hmax, f"{hmax:.0f} mm: Höhengrenze M0 (Annahme)", (200, 0, 0)), (ztop, f"{ztop:.0f} mm: Packhöhe mit Turm (unter Rücksitzbank erlaubt, ENT-144)", (0, 90, 200))):
            yy = kopf + H / 2 - (z - cz) * pm
            for xx in range(0, W, 24): d.line([(xx, yy), (xx + 12, yy)], fill=col, width=2)
            d.text((20, yy - 20), txt, font=font(14, True), fill=col)
        d.rectangle([W + 14, y + 4, W + 34, y + 22], outline=(200, 0, 0)); d.text((W + 44, y + 4), "gestrichelt = Zielband/Grenze Höhe", font=font(13), fill=(20, 20, 20))
    if a == "draufsicht":
        d.text((W + 14, y + 4), f"Bauraumbreite {r['breite_mm']:.0f} mm (fest, ENT-030)", font=font(13), fill=(20, 20, 20))
        d.text((W + 14, y + 26), f"FPC gesamt {e['fpc_laenge_gesamt_m']:.1f} m ({e['fpc_nicht_platziert']} Stücke ohne Platz)", font=font(13), fill=(20, 20, 20))
        if e["hv_gebaut"]: d.text((W + 14, y + 48), f"HV intern {e['hv_laenge_gesamt_m']:.2f} m, {e['hv_verlust_W']:.1f} W", font=font(13), fill=(20, 20, 20))
        else: d.text((W + 14, y + 48), "HV intern nicht gebaut (Verschaltung nicht machbar)", font=font(13), fill=(160, 0, 0))
    d.text((16, H + kopf + 10), f"KI-generiert (Claude Sonnet, 2026-11-18), Entwurf, nicht freigegeben. Quelle: cad/pack/entwurf/ergebnis_{v}_e2.json; Farben nur zur Unterscheidung. Lesehilfe: lesehilfe.md", font=font(13), fill=(90, 90, 90))
    c.save(f"{ZIEL}/e2_{v}_{a}.png")
for v in (sys.argv[1] if len(sys.argv) > 1 else "LFP,NMC").split(","):
    for a in TITEL:
        if os.path.exists(f"{NZ}/roh_{v}_{a}.png"): main(v, a)
