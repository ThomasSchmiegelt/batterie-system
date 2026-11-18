#!/usr/bin/env python3
# KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. Auftrag G2-D Teil 2.
"""Beschriftet die Rohbilder von render_detail.py (Pfeil + Name, Maßstabsbalken, Titel, Fußzeile) mit PIL.
Aufruf: RENDER_ROH=<Ordner mit Roh-PNG/JSON> python3 cad/zelle/render_detail_beschriftung.py
Zahlen im Titel kommen aus ergebnis_detail_<V>.json."""
import os, json, sys
from PIL import Image, ImageDraw, ImageFont
R = os.environ.get("BATTERIE", "/home/cae/hermes/batterie")
DET = f"{R}/cad/zelle/entwurf/detail"; ROH = os.environ.get("RENDER_ROH", f"{DET}/roh")
EL = json.load(open(f"{DET}/ergebnis_detail_LFP.json")); EN = json.load(open(f"{DET}/ergebnis_detail_NMC.json"))
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"; FONTB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def f(s, b=False): return ImageFont.truetype(FONTB if b else FONT, s)
ANN_L = ", ".join(f"{k[2:]} {v:g}" for k, v in EL["annahmen"].items() if k in ("A_POL_D", "A_BB_DICKE_MM", "A_HALTER_BREITE_MM", "A_BEUTEL_MM", "A_PET_FOLIE_MM"))
ANN_N = ", ".join(f"{k[6:]} {v:g}" for k, v in EN["annahmen"].items() if k in ("A_NMC_TABSCHEIBE_R", "A_NMC_RAND_MM", "A_NMC_DECKEL_MM", "A_NMC_DICHTRING_BREITE"))
st, w = EL["stapel"], EN["wickel"]
TITEL = {
 "LFP_gesamt": ("LFP-Zelle außen (Detailmodell)", "Aluminiumgehäuse mit blauer PET-Folie, zwei Pole, Ventil, Füllstopfen", 100, "LFP"),
 "LFP_schnitt": ("LFP-Zelle: Längsschnitt am Pluspol-Ende", f"Stapel: {st['kathoden']} Kathoden, {st['anoden']} Anoden, {st['separatorlagen']} Separatorlagen = {st['stapeldicke_mm']:.2f} mm in {st['innendicke_mm']:.1f} mm Innendicke (Rest {st['rest_zur_innendicke_mm']:.2f} mm). Oben links: Schichtfolge, Dicken x20 überhöht", 10, "LFP"),
 "LFP_explosion": ("LFP-Zelle: Explosionsdarstellung der Endzone (Pluspol-Seite)", "Teile entlang der Zellachse und nach oben auseinandergezogen; Gehäuse und Beutel nur als Hälfte", 10, "LFP"),
 "NMC_gesamt": ("4680-Zelle außen (Detailmodell)", "Stahlbecher (Minus), Deckel mit Pluspol; Cu-Blindniet und Ventil sitzen im Boden (im Viertelschnitt sichtbar)", 20, "NMC"),
 "NMC_viertelschnitt": ("4680-Zelle: Viertelschnitt", f"Spirale aus 4 Bändern: {w['windungen_kathode']:.1f} Windungen (Kathode), Kern Ø {2*w['kern_radius_mm']:g} mm, flächentreue Spirale, Abstand Wickel zu Becher {w['abstand_wickel_zu_becher_mm']:.2f} mm", 10, "NMC"),
 "NMC_draufsicht": ("4680-Zelle: Draufsicht auf den Wickelquerschnitt (Schnitt auf halber Höhe)", f"Archimedische Spirale, flächentreu (Steigung nimmt nach Bandende ab), {w['windungen_kathode']:.1f} Windungen Kathode", 10, "NMC"),
 "NMC_ausschnitt": ("4680-Zelle: Ausschnitt 6 mm am Becherrand (Wickelquerschnitt)", "Schichtfolge von außen nach innen: Becher, Separator, Anode (Cu + 2 x Graphit), Separator, Kathode (Al + 2 x NMC)", 1, "NMC"),
}

def zeichne(name):
    t, unter, balken_mm, var = TITEL[name]
    im = Image.open(f"{ROH}/{name}.png").convert("RGB"); J = json.load(open(f"{ROH}/{name}.json")); W, H = im.size
    d = ImageDraw.Draw(im, "RGBA"); S = W/1600
    # Titelkasten
    d.rectangle([0, 0, W, int(70*S) + 2], fill=(255, 255, 255, 235))
    d.text((int(16*S), int(8*S)), t, font=f(int(26*S), True), fill=(20, 20, 20))
    d.text((int(16*S), int(42*S)), unter, font=f(int(15*S)), fill=(50, 50, 50))
    d.rectangle([W - int(330*S), int(8*S), W - int(10*S), int(36*S)], outline=(160, 20, 20), width=2, fill=(255, 235, 235))
    d.text((W - int(322*S), int(11*S)), "KI-GENERIERT, ENTWURF", font=f(int(18*S), True), fill=(160, 20, 20))
    # Beschriftungen: Pfeil + Name; Kästen oben/unten abwechselnd, ohne Überdeckung
    pts = J["anker"]; belegt = []
    def frei(r): return all(r[2] < q[0] - 6 or r[0] > q[2] + 6 or r[3] < q[1] - 4 or r[1] > q[3] + 4 for q in belegt)
    fs = f(int(16*S), True)
    for i in sorted(range(len(pts)), key=lambda k: pts[k]["x"]):
        a = pts[i]; x, y = a["x"], a["y"]
        if not (0 <= x <= W and 0 <= y <= H): continue
        auf = (i % 2 == 0)
        bb0 = d.textbbox((0, 0), a["text"], font=fs); bw, bh = bb0[2] - bb0[0] + 10, bb0[3] - bb0[1] + 8
        if name.startswith("NMC") and name != "NMC_ausschnitt" or name == "NMC_ausschnitt":   # hohe/zentrierte Objekte: Beschriftung links/rechts auf Höhe des Ankers
            links = auf
            tx = 14 if links else W - bw - 14
            ty = int(min(max(y - bh/2, 80*S), H - 50*S - bh)); r = [tx, ty, tx + bw, ty + bh]
            while not frei(r) and r[1] < H - 40*S: r = [r[0], r[1] + bh + 6, r[2], r[3] + bh + 6]
            belegt.append(r)
            ax = r[2] if links else r[0]; ay = (r[1] + r[3])/2
            d.line([ax, ay, x, y], fill=(200, 30, 30, 255), width=max(2, int(2*S)))
            d.ellipse([x - 5, y - 5, x + 5, y + 5], outline=(200, 30, 30, 255), fill=(255, 255, 255, 255), width=2)
            d.rectangle(r, fill=(255, 255, 255, 235), outline=(30, 30, 30, 255)); d.text((r[0] + 5, r[1] + 3), a["text"], font=fs, fill=(10, 10, 10))
            continue
        tx = int(max(8, min(W - bw - 8, x - bw/2)))
        ty = int(86*S) if auf else H - int(60*S) - bh
        r = [tx, ty, tx + bw, ty + bh]
        while not frei(r) and 0 < r[1] < H:
            dy = (bh + 6) if auf else -(bh + 6); r = [r[0], r[1] + dy, r[2], r[3] + dy]
        belegt.append(r)
        ax = min(max(x, r[0] + 4), r[2] - 4); ay = r[3] if auf else r[1]
        d.line([ax, ay, x, y], fill=(200, 30, 30, 255), width=max(2, int(2*S)))
        d.ellipse([x - 5, y - 5, x + 5, y + 5], outline=(200, 30, 30, 255), fill=(255, 255, 255, 255), width=2)
        d.rectangle(r, fill=(255, 255, 255, 235), outline=(30, 30, 30, 255)); d.text((r[0] + 5, r[1] + 3), a["text"], font=fs, fill=(10, 10, 10))
    # Maßstabsbalken
    pm = J["px_pro_mm"]; bl = balken_mm*pm; bx = int(30*S); by = H - int(38*S)
    d.rectangle([bx - 8, by - 24, bx + bl + 70, by + 26], fill=(255, 255, 255, 220))
    d.rectangle([bx, by, bx + bl/2, by + 10], fill=(20, 20, 20)); d.rectangle([bx + bl/2, by, bx + bl, by + 10], fill=(245, 245, 245), outline=(20, 20, 20))
    d.text((bx, by - 22), "Maßstab (orthografisch)", font=f(int(13*S)), fill=(30, 30, 30))
    d.text((bx + bl + 8, by - 3), f"{balken_mm:g} mm", font=f(int(16*S), True), fill=(20, 20, 20))
    # Fußzeile
    ann = ANN_L if var == "LFP" else ANN_N
    fz = f"Entwurf – Akten vorgeschlagen, KI-generiert. Annahmen (keine Quelle, mm): {ann}. Farben/Werkstoffe = Anmutung, keine Messung. Fundstelle Aufbau: Zerlegung W20."
    d.rectangle([0, H - int(22*S), W, H], fill=(255, 235, 235, 240))
    d.text((int(8*S), H - int(20*S)), fz, font=f(int(12*S)), fill=(120, 15, 15))
    im.save(f"{DET}/{name}.png"); print("OK", name)

for n in TITEL:
    if os.path.exists(f"{ROH}/{n}.png") and (len(sys.argv) < 2 or n in sys.argv[1:]): zeichne(n)
