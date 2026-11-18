#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-18), Entwurf. Auftrag E2 Fortsetzung 5. Beschriftung (PIL) der Rohbilder aus render_e2d.py -> sim/elektrik/e2_elektronik/e2d_<V>_<ansicht>.png.
Zahlen (Maße, Höhen, Kollisionen) nur aus cad/pack/entwurf/ergebnis_<V>_e2d.json. Aufruf: python3 label_e2d.py [LFP,NMC]"""
import json, sys, os
from PIL import Image, ImageDraw, ImageFont
R = "/home/cae/hermes/batterie"; OUT = f"{R}/cad/pack/entwurf"; NZ = "/home/cae/cae_projekte/batterie/e2/render"; ZIEL = f"{R}/sim/elektrik/e2_elektronik"
TITEL = {"boxoffen": "Schaltbox offen (Deckel abgenommen)", "stecker": "Stecker und Durchführungen an der Schaltbox", "bruecke_offen": "Trennbrücke, Servicedeckel abgenommen",
         "bruecke_zu": "Trennbrücke, Servicedeckel montiert", "detail": "Nahaufnahme Zellverbinder, FPC, Ni-Tab, NTC (hinterstes Feld)", "kabel": "HV-Leitungsweg Zelle zur Schaltbox (Draufsicht)", "gesamt": "Gesamtansicht (Zellen ausgeblendet)"}
LEG = [((217, 13, 13), "CMU-Platine"), ((255, 191, 0), "FPC-Messleitung"), ((255, 230, 51), "Ni-Tab, NTC, FPC-Stecker"), ((153, 77, 26), "Daisy-Chain"), ((217, 0, 179), "HV-Leitung (4 Schichten)"), ((204, 128, 51), "Kabelschuh"),
       ((26, 140, 64), "Schaltbox, Inhalt"), ((242, 140, 38), "Stromschiene (Al/Cu)"), ((26, 26, 26), "Schrumpfschlauch, Dichtung"), ((255, 120, 0), "Anschlusslasche Al"), ((0, 200, 230), "Trennbrücke (LFP)"),
       ((89, 102, 230), "Servicedeckel (LFP)"), ((0, 115, 242), "Stecker (HV 250 A, HV 40 A, NV, Sensor)"), ((140, 140, 150), "Zellverbinder, Zellen, Pad, Deckel (grau)")]
def font(sz, b=False):
    f = "/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf" % ("-Bold" if b else "")
    return ImageFont.truetype(f, sz) if os.path.exists(f) else ImageFont.load_default()
def main(v, a):
    r = json.load(open(f"{OUT}/ergebnis_{v}_e2d.json")); e = r["e2"]; J = json.load(open(f"{NZ}/roh_{v}_e2d_{a}.json")); im = Image.open(f"{NZ}/roh_{v}_e2d_{a}.png").convert("RGB")
    W, H = im.size; P = 470; kopf = 84; fuss = 44; c = Image.new("RGB", (W + P, H + kopf + fuss), (255, 255, 255)); c.paste(im, (0, kopf)); d = ImageDraw.Draw(c)
    d.text((16, 8), f"Pack {v}: {TITEL[a]}", font=font(26, True), fill=(20, 20, 20))
    d.text((16, 46), f"Schaltbox außen {e['schaltbox_aussen_mit_flansch_L_mm']:.0f} x {e['schaltbox_aussen_mit_flansch_B_mm']:.0f} mm (mit Flansch), Höhe bis Deckel {e['schaltbox_H_bis_deckel_mm']:.0f} mm, Kollisionen {r['anzahl_kollisionen']}, Teile {r['teile']}", font=font(16), fill=(60, 60, 60))
    d.rectangle([W + P - 330, 8, W + P - 10, 40], outline=(160, 20, 20), width=2, fill=(255, 235, 235)); d.text((W + P - 322, 13), "KI-generiert · Entwurf", font=font(18, True), fill=(160, 20, 20))
    y = kopf + 20
    for col, t in LEG: d.rectangle([W + 14, y, W + 34, y + 18], fill=col, outline=(60, 60, 60)); d.text((W + 44, y), t, font=font(14), fill=(20, 20, 20)); y += 28
    y += 10; d.text((W + 14, y), "Zielband (Annahme/Grenze, nicht freigegeben):", font=font(14, True), fill=(20, 20, 20)); y += 24
    for txt, ist, soll in ((f"Innenhöhe Schaltbox ≤ {e['schaltbox_hoehe_max_N1_mm']:.0f} mm (N1)", e["schaltbox_innenhoehe_mm"], e["schaltbox_hoehe_max_N1_mm"]), (f"Packhöhe vorn ≤ {e['hoehe_max_A_mm']:.0f} mm (M0)", e["hoehe_vorn_mm"], e["hoehe_max_A_mm"])):
        col = (0, 120, 0) if ist <= soll else (190, 0, 0); d.text((W + 14, y), f"{txt}: Ist {ist:.0f} mm {'ok' if ist <= soll else 'ÜBER'}", font=font(13, True), fill=col); y += 22
    if a == "kabel":
        for h in e["hv"]: d.text((W + 14, y), f"{h['strecke']}: {h['laenge_mm']:.0f} mm", font=font(13), fill=(20, 20, 20)); y += 20
        d.text((W + 14, y), f"HV intern {e['hv_laenge_gesamt_m']:.2f} m, {e['hv_verlust_W']:.1f} W", font=font(13), fill=(20, 20, 20)); y += 22
        pm = J["res"][0] / J["scale_mm"]; bar = 200 * pm; x0 = 20; yb = H + kopf - 28; d.rectangle([x0, yb, x0 + bar, yb + 8], fill=(20, 20, 20)); d.text((x0 + bar + 8, yb - 5), "200 mm", font=font(14), fill=(20, 20, 20))
    d.text((16, H + kopf + 12), f"KI-generiert (Claude Sonnet, 2026-11-18), Entwurf, nicht freigegeben. Quelle: cad/pack/entwurf/ergebnis_{v}_e2d.json; Farben nur zur Unterscheidung. Lesehilfe: lesehilfe.md", font=font(13), fill=(90, 90, 90))
    c.save(f"{ZIEL}/e2d_{v}_{a}.png")
for v in (sys.argv[1] if len(sys.argv) > 1 else "LFP,NMC").split(","):
    for a in TITEL:
        if os.path.exists(f"{NZ}/roh_{v}_e2d_{a}.png"): main(v, a)
