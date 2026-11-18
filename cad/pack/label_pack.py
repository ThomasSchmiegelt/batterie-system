#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. Auftrag G4. Beschriftung (PIL) der Rohbilder aus render_pack.py -> entwurf/pack_<V>_<ansicht>.png.
Zahlen (Länge, Höhe, Teile) nur aus entwurf/ergebnis_<V>.json."""
import json, sys, os
from PIL import Image, ImageDraw, ImageFont
R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")); OUT = f"{R}/cad/pack/entwurf"
NAME = {"Zellen": "Zellen (Hüllkörper)", "Quertraeger": "Querträger (Hohlprofil)", "Seitenrahmen": "Seitenrahmen (Mehrkammerprofil, Annahme)", "Boden": "Boden (Wanne)",
 "Deckel": "Deckel", "Unterfahrschutz": "Unterfahrschutz", "Kuehlplatte unten": "Kühlplatte unten", "Kuehlplatte oben": "Kühlplatte oben",
 "Pad unten": "Wärmeleitpad unten", "Pad oben": "Wärmeleitpad oben", "Zellverbinder": "Zellverbinder 25 x 3", "Gruppenverbinder": "Gruppenverbinder 25 x 3 (je 4 Zellen)", "Gruppenbruecke": "Reihenbrücke zur Nachbargruppe",
 "Zellabgriff": "Zellabgriffe 12 x 1", "Zelltraeger": "Zellträger (Annahme)", "Verguss": "Verguss bis halbe Zellhöhe (Annahme)"}
TITEL = {"gesamt": "Gesamtansicht", "explosion": "Explosionsdarstellung", "laengs": "Längsschnitt (Ebene y = Breite/2)", "quer": "Querschnitt durch einen Querträger", "schnitt": "Viertelschnitt", "ecke": "Viertelschnitt, Außenecke (äußere Zellenden)"}
def font(sz, b=False):
    for f in ("/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf" % ("-Bold" if b else ""),): 
        if os.path.exists(f): return ImageFont.truetype(f, sz)
    return ImageFont.load_default()
def lab(n):
    for k in sorted(NAME, key=len, reverse=True):
        if n.replace("Kuehlplatte", "Kuehlplatte").startswith(k): return NAME[k]
    return n
def main(v, a):
    E = json.load(open(f"{OUT}/ergebnis_{v}.json")); im = Image.open(f"{OUT}/roh_{v}_{a}.png").convert("RGB"); J = json.load(open(f"{OUT}/roh_{v}_{a}.json"))
    W, H = im.size; P = 460; kopf = 78; fuss = 34
    c = Image.new("RGB", (W + P, H + kopf + fuss), (255, 255, 255)); c.paste(im, (0, kopf)); d = ImageDraw.Draw(c)
    d.text((16, 8), f"Pack {v}: {TITEL[a]}", font=font(26, True), fill=(20, 20, 20))
    d.text((16, 44), f"Gehäuse {E['gehaeuse_L_mm']:.0f} x {E['breite_mm']:.0f} x {E['hoehe_mm']:.0f} mm, {E['zellen']} Zellen, vereinfachtes Entwurfsmodell (Akten vorgeschlagen)", font=font(15), fill=(50, 50, 50))
    d.rectangle([W + P - 330, 8, W + P - 10, 38], outline=(160, 20, 20), width=2, fill=(255, 235, 235)); d.text((W + P - 322, 13), "KI-generiert · Entwurf", font=font(18, True), fill=(160, 20, 20))
    seen = {}
    for q in J["anker"]: seen.setdefault(lab(q["name"]), q)
    items = sorted(seen.items(), key=lambda kv: kv[1]["y"]); n = len(items); y0 = kopf + 20; step = min(34, (H - 40) / max(n, 1))
    for i, (t, q) in enumerate(items):
        ly = y0 + i * step; ax, ay = q["x"], q["y"] + kopf
        d.line([(ax, ay), (W + 14, ly + 10)], fill=(40, 40, 40), width=1); d.ellipse([ax - 4, ay - 4, ax + 4, ay + 4], fill=(200, 30, 30))
        d.text((W + 18, ly), t, font=font(15), fill=(20, 20, 20))
    if J.get("px_je_mm"):
        pm = J["px_je_mm"]; bar = 200 * pm; x0 = 20; y = H + kopf - 24
        d.rectangle([x0, y, x0 + bar, y + 8], fill=(20, 20, 20)); d.text((x0 + bar + 8, y - 4), "200 mm", font=font(14), fill=(20, 20, 20))
    d.text((16, H + kopf + 8), "KI-generiert (Claude Sonnet), Entwurf, nicht freigegeben. Quelle: cad/pack/entwurf/ergebnis_%s.json, Farben nur zur Unterscheidung." % v, font=font(13), fill=(90, 90, 90))
    c.save(f"{OUT}/pack_{v}_{a}.png")
for v in sys.argv[1].split(","):
    for a in (sys.argv[2].split(",") if len(sys.argv) > 2 else TITEL): main(v, a)
