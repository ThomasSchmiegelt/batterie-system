#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-19), Entwurf. Auftrag G5.8. Beschriftung (PIL) der Rohbilder aus render_g5.py -> cad/baukasten/bilder/g5_<V>_<ansicht>.png.
Zahlen nur aus cad/baukasten/ausgabe/ergebnis_<V>.json; BT-Namen aus pm/bauteile/struktur.json. Aufruf: python3 label_g5.py [LFP,NMC]"""
import json, sys, os
from PIL import Image, ImageDraw, ImageFont
R = "/home/cae/hermes/batterie"; BD = f"{R}/cad/baukasten/bilder"
NAMEN = {}
def walk(n):
    if isinstance(n, dict):
        if str(n.get("id", "")).startswith("BT-"): NAMEN[n["id"]] = n.get("name", "")
        for v in n.values(): walk(v)
    elif isinstance(n, list):
        for v in n: walk(v)
walk(json.load(open(f"{R}/pm/bauteile/struktur.json")))
TITEL = {"gesamt": "Gesamtansicht", "explosion": "Explosion", "schnitt": "Viertelschnitt: Kühlplatte, Pad, Zellen",
         "ecke": "Rückwand mit Verteiler, Laschen, Fühler", "schaltbox": "Schaltbox ohne Deckel", "kuehlkreis": "Kühlkreis außen", "draufsicht": "Draufsicht ohne Deckel", "kabelplan": "Kabelplan (Draufsicht)", "bruecke": "Trennbrücke / Service-Trennstecker, Deckel abgenommen"}
LESE = {"gesamt": "Das ganze Pack von schräg oben. Rechts hinten sitzen Schaltbox (Deckel) und der Kühlkreis außerhalb der Wanne.",
        "explosion": "Alle Schichten auseinandergezogen, unten Schutzplatte und Wanne, in der Mitte Kühlplatte und Zellen, oben Deckel und Schaltbox. Der Kühlkreis (rechts vorn) ist nach hinten (+x) versetzt. Abstände sind nur Darstellung.",
        "schnitt": "Das Pack ist an einer Ecke aufgeschnitten. Man sieht die Schichten Blech-Kühlplatte, Pad und die Zellen im Schnitt.",
        "ecke": "Hinterer Rahmen von außen: Verteiler (Al-Profil) mit Anschlüssen, Kühlmittelfühler, Schlauch mit T-Stück sowie HV-Leitung und Laschen.",
        "schaltbox": "Blick in die Schaltbox ohne Deckel: Schütze, Vorladung, Sicherung, Stromschienen, Steuerplatine (grün).",
        "draufsicht": "Blick von oben, Deckel, Servicedeckel und Schaltboxdeckel sowie die obere Kühlplatte weggelassen. CMU-Platinen (grün), flache Messleitung FPC (gelb), HV-Leitung (orange), Stromschienen (Kupfer); die Schaltbox liegt hinten, der Verteiler außen am hinteren Rahmen. Kein Zielband, das Bild zeigt Lage und Leitungsweg.",
        "kabelplan": "Gleiche Draufsicht, aber nur die Leitungen hervorgehoben: HV-Leitung, Messleitung FPC mit Daisy-Kette, CMU-Platinen und Stromschienen. Alles andere ist grau und durchscheinend (15 %), die Schaltbox nur als Umriss. Kein Zielband (Plan).",
        "bruecke": "Nahaufnahme der Trennbrücke (Kupfer) mit abgenommenem Deckel. Kein Zielband, das Bild zeigt die Lage.",
        "kuehlkreis": "Der Kühlkreis außen am Pack: Pumpe, Ausgleichsbehälter, Ventil, Chiller und die Schläuche (Frontansicht, Zellen und Elektrik ausgeblendet)."}
def font(sz, b=False):
    f = "/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf" % ("-Bold" if b else "")
    return ImageFont.truetype(f, sz) if os.path.exists(f) else ImageFont.load_default()
def main(v, a):
    e = json.load(open(f"{R}/cad/baukasten/ausgabe/ergebnis_{v}.json")); J = json.load(open(f"{BD}/roh_g5_{v}_{a}.json")); im = Image.open(f"{BD}/roh_g5_{v}_{a}.png").convert("RGB")
    W, H = im.size; kopf, fuss = 84, 100; c = Image.new("RGB", (W, H + kopf + fuss), (255, 255, 255)); c.paste(im, (0, kopf)); d = ImageDraw.Draw(c)
    d.text((16, 8), f"Pack {v} (G5-Baukasten): {TITEL[a]}", font=font(26, True), fill=(20, 20, 20))
    d.text((16, 46), f"Maße L x B x H = {e['laenge_mm']:.0f} x {e['breite_mm']:.0f} x {e['hoehe_max_mm']:.0f} mm, Masse {e['masse_kg']:.1f} kg, {e['teile']} Teile (Stückliste v{e['stueckliste_version']}); Breite 1430 mm durch Fahrzeug fest", font=font(16), fill=(60, 60, 60))
    d.rectangle([W - 330, 8, W - 10, 40], outline=(160, 20, 20), width=2, fill=(255, 235, 235)); d.text((W - 322, 13), "KI-generiert · Entwurf", font=font(18, True), fill=(160, 20, 20))
    an = sorted(J["anker"], key=lambda q: q["y"]); links = [q for q in an if q["x"] < W / 2]; rechts = [q for q in an if q["x"] >= W / 2]
    for seite, lst in ((0, links), (1, rechts)):
        n = len(lst)
        for i, q in enumerate(lst):
            ty = kopf + 40 + i * (H - 80) / max(n - 1, 1) if n > 1 else kopf + H / 2
            txt = f"{q['bt']} {NAMEN.get(q['bt'], '')}"; f = font(16, True); w = d.textlength(txt, font=f)
            tx = 12 if seite == 0 else W - w - 20
            ax, ay = q["x"], q["y"] + kopf
            ex = tx + w + 8 if seite == 0 else tx - 6
            d.line([(ex, ty + 10), (ax, ay)], fill=(200, 30, 30), width=2); d.ellipse([ax - 5, ay - 5, ax + 5, ay + 5], fill=(200, 30, 30), outline=(255, 255, 255))
            d.rectangle([tx - 4, ty - 2, tx + w + 4, ty + 22], fill=(255, 255, 255), outline=(200, 30, 30)); d.text((tx, ty), txt, font=f, fill=(20, 20, 20))
    d.rectangle([0, H + kopf, W, H + kopf + fuss], fill=(245, 245, 245)); import textwrap
    for i, z in enumerate(textwrap.wrap("Lesehilfe: " + LESE[a], int(W / 8.6))[:3]): d.text((16, H + kopf + 6 + 20 * i), z, font=font(15), fill=(20, 20, 20))
    d.text((16, H + kopf + 72), f"KI-generiert (Claude Sonnet, 2026-11-19), Entwurf, nicht freigegeben. Quelle: cad/baukasten/ausgabe/ergebnis_{v}.json; Farben nur zur Unterscheidung (cad/baukasten/farben.json).", font=font(13), fill=(90, 90, 90))
    c.save(f"{BD}/g5_{v}_{a}.png")
for v in (sys.argv[1] if len(sys.argv) > 1 else "LFP,NMC").split(","):
    for a in TITEL:
        if os.path.exists(f"{BD}/roh_g5_{v}_{a}.png"): main(v, a)
