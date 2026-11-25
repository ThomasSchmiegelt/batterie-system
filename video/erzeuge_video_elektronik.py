# KI-generiert (Claude Sonnet 5.5, 2026-11-25), Entwurf. Auftrag video/AUFTRAG_VIDEO_ELEKTRONIK.md (Nachtrag 1), REQ-D13, BAT-DOC-13c.
# Baut Einzelbilder (CPU, Pillow) aus vorhandenen PNG und der Graph-Bildfolge von graph_zeitraffer.py. Zahlen nur aus video/elektronik/daten.json.
# Aufruf: python3 video/erzeuge_video_elektronik.py [erstes letztes] ; vorhandene Bilder werden übersprungen.
import os, sys, json, math, textwrap
from PIL import Image, ImageDraw, ImageFont
R = "/home/cae/hermes/batterie"; G = "/home/cae/cae_projekte/batterie_video/wissen/graph"; OUT = "/home/cae/cae_projekte/batterie_video/elektronik/bilder"
LAY = "/home/cae/cae_projekte/batterie_video/elektronik/layout.json"
FPS = 25; NF = 165 * FPS; W, H = 1280, 720
D = json.load(open(f"{R}/video/elektronik/daten.json"))
FA = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"; FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
_f = {}
def F(s, b=False):
    k = (s, b)
    if k not in _f: _f[k] = ImageFont.truetype(FB if b else FA, s)
    return _f[k]
Z = {z["name"]: z for z in D["zahlen"]}
def zahl(n): return Z[n]["wert"]
def pct(x): return f"{x*100:.2f}".replace(".", ",") + " %"
def num(x, nd=2): return f"{x:.{nd}f}".replace(".", ",")
FM = json.load(open(f"{R}/sim/elektrik/e3d_fmeda/ergebnis.json"))
SPFM = pct(FM["cmu"]["LFP"]["SG-01"]["SPFM"]); LFM = pct(FM["cmu"]["LFP"]["SG-01"]["LFM"])
ZS, ZL = pct(FM["ziel"]["SG-01"]["SPFM"]).replace(",00", ""), pct(FM["ziel"]["SG-01"]["LFM"]).replace(",00", "")
KOMM = {"REQ-P01": "1500 kg Anhaltswert", "REQ-P03": "720–880 V", "REQ-P04": "P_dauer ≥ 60 kW", "REQ-P05": "LFP 20 min, NMC 30 min", "REQ-P15": "Zellspannung, Temperatur, Isolation",
        "REQ-P17": "EMV BMS, CMU, Schütz", "REQ-P18": "ISO 26262", "REQ-P19": "Luft- und Kriechstrecken", "REQ-P20": "Umwelt, Qualifikation", "REQ-P21": "Cybersicherheit BMS"}
HOCH = {"REQ-P15", "REQ-P17", "REQ-P18", "REQ-P19", "REQ-P20", "REQ-P21"}
PFAD = {b["pfad"] for b in D["bilder"]}
VF = "/home/cae/cae_projekte/batterie_video/frames/2749.png"   # echtes Blender-Rendering aus dem ersten Video (Pack geschlossen, Schaltbox, Kabel)
def bild(p):
    assert p in PFAD or p == VF, p
    return p
_c = {}
def lade(p, w, h):
    k = (p, w, h)
    if k not in _c:
        im = Image.open(bild(p) if p.startswith("/") else f"{R}/{p}").convert("RGB"); s = min(w / im.width, h / im.height)
        _c[k] = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.LANCZOS)
    return _c[k]
def clamp(x): return max(0.0, min(1.0, x))
def dim(im, a):
    return Image.blend(im, Image.new("RGB", im.size, (12, 14, 18)), a)

def tafel(d, text, x, y, fs=28, fg=(255, 255, 255), bg=(15, 20, 30, 215), a=1.0, b=False):
    f = F(fs, b); w = d.textlength(text, font=f)
    d.rounded_rectangle([x, y, x + w + 28, y + fs + 20], 10, fill=(bg[0], bg[1], bg[2], int(bg[3] * a)), outline=(200, 200, 210, int(160 * a)))
    d.text((x + 14, y + 8), text, font=f, fill=fg + (int(255 * a),))
    return y + fs + 28

def panel(im, p, box, titel=None, quelle=None, a=1.0):
    """Bild p mittig in box (x,y,w,h) auf weißem Feld; Quelle klein unten."""
    x, y, w, h = box; pim = lade(p, w - 16, h - 16)
    lay = Image.new("RGB", (w, h), (250, 250, 250)); lay.paste(pim, ((w - pim.width) // 2, (h - pim.height) // 2))
    a = 1.0
    if a < 1: lay = Image.blend(im.crop((x, y, x + w, y + h)), lay, a)
    im.paste(lay, (x, y)); d = ImageDraw.Draw(im, "RGBA")
    d.rectangle([x, y, x + w, y + h], outline=(230, 230, 240, 255), width=2)
    q = quelle or p; d.text((x + 6, y + h + 4), q, font=F(16), fill=(200, 200, 205, 255))
    return im

O3 = "/home/cae/cae_projekte/batterie_video/elektronik3d"
def lage3d(im, sz, t):
    """3D-Szene sz (pack|cmu|bms) bei t s (lokal) als RGBA über das Bild legen; fehlende Bilder: nächstes früheres."""
    f = int(t * FPS)
    while f > 0 and not os.path.exists(f"{O3}/{sz}/{f:04d}.png"): f -= 1
    L = Image.open(f"{O3}/{sz}/{f:04d}.png").convert("RGBA")
    im.paste(Image.alpha_composite(im.convert("RGBA"), L).convert("RGB")); return im
def graph_index(f):
    if f < 3050: return int(f * 2680 / 3050)
    return min(3150, 2680 + int((f - 3050) * 470 / 1075))
_lay = None
def layout():
    global _lay
    if _lay is None: _lay = json.load(open(LAY))
    return _lay
def knoten_pos(gi, nid):
    L = layout(); k = L["ids"].index(nid); P = L["P"][k]
    zoom = 1.0 + 0.04 * min(1.0, gi / 3149)
    return P[0] * 560 * zoom + 640 + 6 * math.sin(gi / 260.0), P[1] * 318 * zoom + 360 + 4 * math.cos(gi / 310.0)

KETTEN = [(("Anforderung/REQ-P18", "REQ-P18"), ("Entscheidung/ENT-192", "ENT-192 (vorgeschlagen)"), ("Bauteil/BT-323", "BT-323 Ausgleichskreis"), ("Baustein/E3d", "FMEDA E3d"), ("Befund/B-BAT-055", "B-BAT-055")),
          (("Anforderung/REQ-P19", "REQ-P19"), ("Entscheidung/ENT-195", "ENT-195 (entschieden)"), ("Bauteil/BT-311", "BT-311 BMS-Leiterplatte")),
          (("Anforderung/REQ-P15", "REQ-P15"), ("Entscheidung/ENT-184", "ENT-184 (entschieden, Mensch)"), ("Bauteil/BT-321", "BT-321 CMU-Leiterplatte"), ("Befund/B-BAT-051", "B-BAT-051"))]
KANTEN = {0: [(0, 1), (1, 2), (1, 3), (1, 4)], 1: [(0, 1), (1, 2)], 2: [(0, 1), (1, 2), (1, 3)]}
FARBK = [(255, 90, 90), (90, 210, 255), (255, 210, 60)]

def kette(im, gi, t, i, t0, dt, tr=lambda p: p):
    """Kette i: Knoten erscheinen nacheinander ab t0 innerhalb dt s, Kanten werden gezeichnet."""
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); K = KETTEN[i]; c = FARBK[i]
    n = len(K); sicht = [clamp((t - (t0 + dt * k / n)) / 0.5) for k in range(n)]
    P = [tr(knoten_pos(gi, k[0])) for k in K]
    for a, b in KANTEN[i]:
        w = min(sicht[a], sicht[b])
        if w > 0: d.line([P[a], P[b]], fill=c + (int(255 * w),), width=4)
    for k in range(n):
        w = sicht[k]
        if w <= 0: continue
        x, y = P[k]; r = 11 * (1 + 0.6 * (1 - w)); d.ellipse([x - r, y - r, x + r, y + r], outline=c + (int(255 * w),), width=4, fill=c + (int(120 * w),))
        lab = K[k][1]; fw = d.textlength(lab, font=F(22, True)); gk = sum(len(KETTEN[j]) for j in range(i)) + k
        lx, ly = 14, 74 + gk * 40
        d.line([(lx + fw + 14, ly + 13), (x, y)], fill=c + (int(150 * w),), width=2)
        d.rounded_rectangle([lx, ly - 4, lx + fw + 14, ly + 30], 8, fill=(10, 12, 18, int(235 * w)), outline=c + (int(255 * w),))
        d.text((lx + 7, ly), lab, font=F(22, True), fill=(255, 255, 255, int(255 * w)))
    im.paste(Image.alpha_composite(im.convert("RGBA"), lay).convert("RGB"))

def kopf(im, titel, nr=None):
    d = ImageDraw.Draw(im, "RGBA"); d.rectangle([0, 0, W, 54], fill=(10, 12, 18, 200))
    d.text((24, 10), titel, font=F(30, True), fill=(255, 255, 255, 255))
    d.text((W - 24 - d.textlength("KI-generiert · Entwurf", font=F(22)), 16), "KI-generiert · Entwurf", font=F(22), fill=(230, 200, 120, 255))

def kurz(s, n):
    s = s.split("(")[0].split(";")[0].strip()
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"

# ---------- Szenen ----------
def s1(im, t):
    kopf(im, "Anforderungen und Normen")
    d = ImageDraw.Draw(im, "RGBA")
    if t < 15:
        d.rounded_rectangle([40, 70, W - 40, 640], 14, fill=(12, 16, 24, 190), outline=(200, 200, 210, 180))
        A = {a["id"]: a for a in D["anforderungen"]}; ids = ["REQ-P01", "REQ-P03", "REQ-P04", "REQ-P05", "REQ-P15", "REQ-P17", "REQ-P18", "REQ-P19", "REQ-P20", "REQ-P21", "REQ-D13"]
        d.text((60, 82), "Nummer", font=F(22, True), fill=(180, 180, 190, 255)); d.text((190, 82), "Kurztitel", font=F(22, True), fill=(180, 180, 190, 255))
        d.text((650, 82), "Wert", font=F(22, True), fill=(180, 180, 190, 255)); d.text((1010, 82), "Status", font=F(22, True), fill=(180, 180, 190, 255))
        for k, i in enumerate(ids):
            w = clamp((t - 0.5 - k * 1.1) / 0.5)
            if w <= 0: continue
            a = A[i]; y = 122 + k * 47; hc = (255, 190, 80) if i in HOCH else (235, 235, 240)
            if i in HOCH: d.rectangle([50, y - 3, W - 50, y + 40], fill=(120, 80, 10, int(110 * w)))
            al = int(255 * w); wert = KOMM.get(i, "")
            d.text((60, y), i, font=F(24, True), fill=hc + (al,)); d.text((190, y), kurz(a["titel"], 33), font=F(22), fill=hc + (al,))
            d.text((650, y), kurz(wert, 24), font=F(22), fill=hc + (al,)); d.text((1010, y), kurz(a["status"], 18), font=F(22), fill=hc + (al,))
        d.text((60, 648), "Hervorgehoben: REQ-P15, P17…P21 (Elektronik)   Quelle: pm/anforderungen.json", font=F(18), fill=(200, 200, 205, 255))
    else:
        d.rounded_rectangle([40, 70, W - 40, 640], 14, fill=(12, 16, 24, 190), outline=(200, 200, 210, 180))
        d.text((60, 82), "Normen (docs/07_normen_und_vorschriften.md)", font=F(26, True), fill=(255, 255, 255, 255))
        for k, n in enumerate(D["normen"]):
            w = clamp((t - 15.3 - k * 0.9) / 0.5)
            if w <= 0: continue
            y = 135 + k * 80; frei = n["verfuegbar"].startswith("frei"); c = (110, 220, 140) if frei else (255, 120, 110); al = int(255 * w)
            d.text((60, y), kurz(n["norm"], 52), font=F(26, True), fill=(255, 255, 255, al))
            d.text((60, y + 34), kurz(n["verfuegbar"], 62), font=F(22), fill=c + (al,))
            d.text((W - 290, y), "frei" if frei else "kostenpflichtig", font=F(22, True), fill=c + (al,))
    return im

def s3(im, t):
    kopf(im, "Zelle LFP prismatisch (Blade)  [REQ-P06]")
    bl = [(0, 8, "cad/zelle/entwurf/render/zelle_LFP_render.png", "Zelle LFP prismatisch, Blade  [REQ-P06]"),
          (8, 15, "sim/chemie/c1_zellmodell/ladekurve.png", "Ladekurve LFP und NMC bis 80 % mit Zielzeit  [sim/chemie/c1_zellmodell]"),
          (15, 20, "sim/chemie/c1_zellmodell/dcir.png", "DCIR: Spannungsabfall im 10-s-Puls bei 10, 25, 40 °C  [sim/chemie/c1_zellmodell]"),
          (20, 25, "sim/chemie/c1_zellmodell/waerme_LFP.png", "Wärme je Zelle über der Zeit (LFP, Modell) mit Zielband  [sim/chemie/c1_zellmodell]")]
    for a, b, p, cap in bl:
        if a <= t < b:
            panel(im, p, (110, 80, 1060, 520), quelle=p, a=clamp(min((t - a) / 0.5, 1))); d = ImageDraw.Draw(im, "RGBA"); tafel(d, cap, 110, 626, 26)
    return im

def s4(im, t):
    kopf(im, "Pack baut sich auf  [REQ-P07]")
    im = lage3d(im, "pack", t); kopf(im, "Pack baut sich auf  [REQ-P07]")
    d = ImageDraw.Draw(im, "RGBA"); cap = [(0, 8, "Zellen, Rahmen, Kühlplatte"), (8, 17, "CMU, Schaltbox, Verbindungen"), (17, 22, "Deckel schließt"), (22, 30, "Deckel öffnet")]
    for a, b, c in cap:
        if a <= t < b: tafel(d, c + "  [cad/pack/entwurf, e2d_e3c]", 40, 626, 26, a=clamp(min((t - a) / 0.5, 1)))
    pk = [(12, 16.5, "sim/kuehlung/k3_gesamt/k3_vergleich.png", "Kühlung K3, K4  [REQ-P12]", (30, 90)), (19, 23.5, "sim/mechanik/x3_crash_g5/energie_LFP_a.png", "Crash Pfahl 5 kJ  [REQ-P14]", (700, 90))]
    for a, b, p, cap, (x, y) in pk:
        if a <= t < b:
            w = clamp(min((t - a) / 0.5, (b - t) / 0.5)); pim = lade(p, 520, 300); bx = Image.new("RGB", (pim.width + 8, pim.height + 8), (250, 250, 250)); bx.paste(pim, (4, 4))
            im.paste(Image.blend(im.crop((x, y, x + bx.width, y + bx.height)), bx, w), (x, y)); d = ImageDraw.Draw(im, "RGBA")
            d.rectangle([x, y, x + bx.width, y + bx.height], outline=(255, 210, 60, 255), width=3); tafel(d, cap, x, y + bx.height + 8, 22, a=w)
            d.text((x + 2, y + bx.height + 52), p, font=F(14), fill=(200, 200, 205, int(255 * w)))
    if t >= 24:
        d = ImageDraw.Draw(im, "RGBA"); m = zahl("Packmasse LFP masse_bekannt_kg"); tafel(d, f"Packmasse LFP {num(m)} kg", 780, 626, 26, a=clamp((t - 24) / 0.5))
    return im

def inset(im, p, t, a, b, cap):
    """Schaltplan als Bild-in-Bild unten rechts zwischen a und b s."""
    if not (a <= t < b): return
    w = clamp(min((t - a) / 0.5, (b - t) / 0.5)); x, y = 700, 90; pim = lade(p, 540, 330); bx = Image.new("RGB", (pim.width + 8, pim.height + 8), (250, 250, 250)); bx.paste(pim, (4, 4))
    im.paste(Image.blend(im.crop((x, y, x + bx.width, y + bx.height)), bx, w), (x, y)); d = ImageDraw.Draw(im, "RGBA"); d.rectangle([x, y, x + bx.width, y + bx.height], outline=(255, 210, 60, 255), width=3)
    tafel(d, cap, x, y + bx.height + 8, 22, a=w); d.text((x + 2, y + bx.height + 52), p, font=F(14), fill=(200, 200, 205, int(255 * w)))

def s5(im, t, gi):
    ts = t - 80
    if ts < 30:
        tit = "Steuergerät 1: CMU-Platine in der Endzone  [REQ-P15]" if ts < 15 else "Steuergerät 2: BMS-Platine in der Schaltbox  [REQ-P19]"
        kopf(im, tit); im = lage3d(im, "steuer", ts); kopf(im, tit); d = ImageDraw.Draw(im, "RGBA")
        cap = [(0, 8.4, "Zellen und Umgebung werden durchsichtig, Anflug auf die erste CMU"), (8.4, 10, f"CMU am Einbauort (Endwand, hochkant): {zahl('CMU LFP lagen')} Lagen, {zahl('CMU LFP teile')} Teile, DRC {zahl('CMU LFP drc_verstoesse')}"),
               (10, 15, "CMU: Explosion nach Lagen, Vias als Stäbe"), (15, 20, "Weiter zur Schaltbox, Umgebung durchsichtig"),
               (20, 22, f"BMS-Platine in der Schaltbox: {zahl('BMS teile')} Teile, DRC {zahl('BMS drc_verstoesse')}, rote HV/NV-Sperrzone"), (22, 30, "BMS: Explosion nach Lagen")]
        for a_, b_, c in cap:
            if a_ <= ts < b_: tafel(d, c, 40, 626, 26, a=clamp(min((ts - a_) / 0.5, 1)))
        inset(im, "sim/elektrik/e3_platine/schaltplan_LFP_kanal.png", ts, 10.5, 14.5, "Schaltplanblatt Kanal"); inset(im, "sim/elektrik/e3c_bms_platine/schaltplan_bms_blatt-1.png", ts, 22.5, 29, "Schaltplanblatt BMS"); return im
    elif ts < 45:
        ts -= 30; kopf(im, "Rechnungen zur Elektronik")
        bl = [(0, 4, "sim/elektrik/e3_platine/spice_ausgleich_vorladung.png", f"SPICE Vorladung, U_V {num(zahl('SPICE Vorladung U_V'), 0)} V"),
              (4, 8, "sim/elektrik/e3c_bms_platine/spice_schuetz.png", f"SPICE Schütz, Zener-Spannung {num(zahl('SPICE Schuetz zener_anzug v_n_max_V'))} V"),
              (8, 11.5, "sim/elektrik/e3b_platine_waerme/e3b_temperatur.png", "Elmer-Wärme E3b"),
              (11.5, 15, "sim/elektrik/e3d_fmeda/e3d_fmeda.png", f"FMEDA CMU LFP SG-01: SPFM {SPFM}, LFM {LFM} (Ziel ASIL D {ZS}, {ZL})")]
    else:
        ts -= 45
        src = im.copy(); WIN = [(0, 4.5), (4.5, 8), (8, 11.5)]; cur = None; tgt = []
        for K in KETTEN:
            pt = [knoten_pos(gi, k[0]) for k in K]; xs = [q[0] for q in pt]; ys = [q[1] for q in pt]
            zm = min(4.0, 330 / (max(xs) - min(xs) + 12), 330 / (max(ys) - min(ys) + 12)); tgt.append(((max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2, zm))
        ci = 0 if ts < 4.5 else (1 if ts < 8 else 2); t_in = ts - WIN[ci][0]
        prev = (640.0, 360.0, 1.0) if ci == 0 else tgt[ci - 1]; w = clamp(t_in / 1.0); w = w * w * (3 - 2 * w)
        cx, cy, ZM = [prev[k] + (tgt[ci][k] - prev[k]) * w for k in range(3)]
        tx, ty = 700, 380; x0, y0 = cx - tx / ZM, cy - ty / ZM
        big = Image.new('RGB', (2 * W, 2 * H), (24, 24, 24)); big.paste(src, (W // 2, H // 2))
        im.paste(big.crop((int(x0) + W // 2, int(y0) + H // 2, int(x0 + W / ZM) + W // 2, int(y0 + H / ZM) + H // 2)).resize((W, H), Image.LANCZOS))
        tr = lambda p: ((p[0] - int(x0)) * ZM, (p[1] - int(y0)) * ZM)
        kopf(im, "Nachverfolgung: REQ → ENT → BT → Nachweis")
        for i, (a, b2) in enumerate(WIN):
            if ts >= a + 0.8: kette(im, gi, ts, i, a + 0.8, (b2 - a - 1.2) * 0.8, tr)
        if ts < 11.5: return im
        ts -= 11.5; d = ImageDraw.Draw(im, "RGBA"); d.rounded_rectangle([700, 64, W - 14, 664], 12, fill=(10, 14, 22, 225), outline=(200, 200, 210, 160))
        d.text((716, 70), "Sicherheitsziele (HARA)", font=F(24, True), fill=(255, 255, 255, 255))
        for k, s in enumerate(D["sicherheitsziele"]):
            w = clamp((ts - 0.2 - k * 0.2) / 0.3)
            if w <= 0: continue
            y = 98 + k * 66; al = int(255 * w); c = {"D": (255, 90, 90), "C": (255, 170, 60), "B": (240, 220, 90)}[s["asil"]]
            d.text((716, y), f"{s['sg']}  ASIL {s['asil']}", font=F(22, True), fill=c + (al,))
            for j, ln in enumerate(textwrap.wrap(s["kurztext"], 46)[:2]): d.text((716, y + 25 + j * 21), ln, font=F(19), fill=(235, 235, 240, al))
        d.text((716, 646), "docs/24_gefahrenanalyse_hara.md", font=F(14), fill=(200, 200, 205, 255))
        return im
    for a, b, p, cap in bl:
        if a <= ts < b:
            panel(im, p, (60, 80, 1160, 520), quelle=p, a=clamp(min((ts - a) / 0.5, 1))); d = ImageDraw.Draw(im, "RGBA"); tafel(d, cap, 60, 626, 24)
    return im

def s6(im, t, gimg):
    """t seit 140 s. 0–10 Halt mit Zahlen, 10–18 durchsichtig, 18–25 nur Graph."""
    a = 1.0 - clamp((t - 10) / 8.0)
    if a > 0:
        im2 = dim(im, 0.45); pk = lade(VF, 1000, 440)
        box = Image.new("RGB", (pk.width, pk.height)); box.paste(pk)
        x, y = (W - pk.width) // 2, 70; base = im2.crop((x, y, x + pk.width, y + pk.height)); im2.paste(Image.blend(base, box, a), (x, y)); ImageDraw.Draw(im2).text((x, y + pk.height + 2), "Blender-Rendering aus abschluss.mp4, Bild 2749", font=F(14), fill=(200, 200, 205))
        im.paste(im2); d = ImageDraw.Draw(im, "RGBA"); w = clamp((t - 0.5) / 1.0) * clamp(a * 2)
        kopf(im, "Batterie fertig: BT-000 LFP")
        z = [f"Packmasse LFP {num(zahl('Packmasse LFP masse_bekannt_kg'))} kg", f"CMU {zahl('CMU LFP teile')} Teile, BMS {zahl('BMS teile')} Teile",
             f"DRC {zahl('CMU LFP drc_verstoesse')} (CMU und BMS)", f"FMEDA SG-01: SPFM {SPFM}"]
        for k, s in enumerate(z): tafel(d, s, 60 + (k % 2) * 560, 528 + (k // 2) * 58, 26, a=w * clamp((t - 0.5 - k * 0.6) / 0.6) if False else clamp((t - 0.5 - k * 0.6) / 0.6) * clamp(a * 2))
    if t >= 18:
        d = ImageDraw.Draw(im, "RGBA"); w = clamp((t - 18.5) / 1.0); tafel(d, "Wissensgraph: Anforderungen, Entscheidungen, Bauteile, Nachweise", 190, 604, 26, a=w)
        tafel(d, "KI-generiert (Claude, Kolibri 1). Entwurf. Autor: Konstrukteur", 250, 548, 22, a=w)
    return im

def einbild(f):
    p = f"{OUT}/{f:04d}.png"
    if os.path.exists(p): return
    t = f / FPS; gi = graph_index(f)
    im = Image.open(f"{G}/{gi:04d}.png").convert("RGB")
    if t < 125: im = dim(im, 0.35 if t < 140 else 0.2)
    elif t < 140: im = dim(im, 0.1)
    if t < 25: im = s1(im, t)
    elif t < 50: im = s3(im, t - 25)
    elif t < 80: im = s4(im, t - 50)
    elif t < 140: im = s5(im, t, gi)
    else: im = s6(im, t - 140, None)
    d = ImageDraw.Draw(im, "RGBA"); n = "Thomas Schmiegelt"; fw = d.textlength(n, font=F(30))
    d.text(((W - fw) / 2, H - 52), n, font=F(30), fill=(255, 255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0, 180))
    d.text((W - 150, H - 24), "KI-generiert", font=F(16), fill=(230, 200, 120, 255))
    im.save(p)

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    a0, a1 = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (0, NF - 1)
    if len(sys.argv) > 3 and sys.argv[3] == "seq":
        for f in range(a0, a1 + 1): einbild(f)
    else:
        from multiprocessing import Pool
        with Pool(6) as pl: pl.map(einbild, range(a0, a1 + 1), chunksize=10)
    print("BILDER FERTIG", a0, a1)
