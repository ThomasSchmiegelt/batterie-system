#!/usr/bin/env python3
"""E3c hierarchischer KiCad-Schaltplan (.kicad_sch) der BMS-Platine BT-311 mit Drähten aus bms_teile.json (dieselbe Quelle wie das Layout, bms_skidl.py).
KI-generiert (Claude Sonnet, 2026-11-24), Entwurf. Muster: sim/elektrik/e3_platine/schaltplan.py (dort unverändert); Version 2 mit Drähten (Auftrag Opus).
Blätter: Deckblatt (Blattpins mit den Verbindungen), Versorgung 12 V, Rechner, CAN, Schützansteuerung, Daisy-Master mit Isolation, Strommessung HV-Seite.
Innerhalb eines Blattes sind Netze mit Drähten gezeichnet (Spalten von links nach rechts = Signalfluss; je Spalte-Lücke senkrechte Sammelleitungen).
Netznamen nur für Versorgung/GND (globale Labels) und für Verbindungen zwischen Blättern (hierarchische Labels, Blattpins, Drähte auf dem Deckblatt).
Aufruf: source umgebung.sh; python3 bms_schaltplan.py -> /home/cae/cae_projekte/batterie/e3c/schaltplan/*.kicad_sch (Kopie nach schaltplan_quelle/ macht das Aufrufskript)"""
import json, uuid, re, pathlib, collections
H = pathlib.Path(__file__).resolve().parent; OUT = pathlib.Path("/home/cae/cae_projekte/batterie/e3c/schaltplan"); OUT.mkdir(parents=True, exist_ok=True)
PK = "bms_schaltplan"; U = lambda: str(uuid.uuid4()); G = 1.27
sn = lambda x: round(round(x / G) * G, 4)
def q(s): return '"' + str(s).replace('"', "'") + '"'
FONT = "(effects (font (size 1.27 1.27)))"
sz = json.load(open(H / "ergebnis_platine.json"))["sperrzone"]; KR, LU = sz["kriech_mm"], sz["luft_mm"]
f0 = lambda x: f"{x:g}"
ISO = f"verstärkte Isolation {f0(KR)}/{f0(LU)} mm (Kriechstrecke/Luftstrecke, ENT-191)"
teile = json.load(open(H / "bms_teile.json"))["teile"]; ROOT = U(); BY = {t["tag"]: t for t in teile}
SUPPLY = {"GND", "HV_GND", "+3V3", "+5V", "VBAT_F", "HV_VDD"}   # Versorgung/Masse: globale Labels

# ---------------- Blattaufteilung: Zeilen -> Spalten -> Tags (Signalfluss von links nach rechts)
def S(*x): return list(x)
SPEC = {
 "versorgung": dict(papier="A3", zeilen=[("Verpolschutz, Wecken, Systembasis, Filter", [S("J_VERSORGUNG"), S("R_KL15", "Q_VERPOL", "R_VERPOL", "D_VERPOL"), S("U_SBC", "D_TVS", "L_VERSORGUNG"), S("C_SBC_OUT0", "C_SBC_OUT1", "C_SBC_VS", "C_VBAT0", "C_VBAT1", "C_VBAT_ELKO", "C_VBAT_HF")])]),
 "rechner": dict(papier="A2", lblR=True, zeilen=[("Rechner mit Takt, Debug, Leuchtdioden, Temperatur", [S("Y_MCU", "C_XTAL0", "C_XTAL1"), S("U_MCU"), S("J_DEBUG", "R_LED1", "R_LED2", "R_LED3", "R_NTC", "R_NTC_PU"), S("D_LED1", "D_LED2", "D_LED3")]),
        ("Abblockung (Versorgung +3V3/GND)", [S(*[f"C_MCU{i}" for i in range(1, 5)]), S(*[f"C_MCU{i}" for i in range(5, 9)]), S("C_MCU9", "C_MCU10", "C_MCUA0", "C_MCUA1"), S("C_MCUA2", "C_MCUB0", "C_MCUB1", "C_RESET")])]),
 "can": dict(papier="A2", zeilen=[("CAN-FD Kanal 1", [S("R_STB1"), S("U_CAN1"), S("L_CAN1"), S("D_ESD1_0", "R_TERM1_0", "R_TERM1_1", "C_TERM1", "D_ESD1_1", "J_CAN1"), S("C_CAN1_0", "C_CAN1_1")]),
        ("CAN-FD Kanal 2", [S("R_STB2"), S("U_CAN2"), S("L_CAN2"), S("D_ESD2_0", "R_TERM2_0", "R_TERM2_1", "C_TERM2", "D_ESD2_1", "J_CAN2"), S("C_CAN2_0", "C_CAN2_1")])]),
 "schuetz": dict(papier="A2", zeilen=[
    ("Kanal P (Plus-Hauptschütz): UND -> High-Side -> Spule -> Low-Side -> Shunt; Zener-Löschpfad parallel zur Spule", [S("U_AND1", "C_AND1"), S("R_HS_PD_P", "U_HS_P", "R_LS_G_P", "R_LS_PD_P"), S("J_SPULE_P", "D_FREI_P", "D_ZENER_P", "Q_LS_P"), S("R_SENSE_P", "R_I_P", "C_I_P")]),
    ("Kanal M (Minus-Hauptschütz)", [S(), S("R_HS_PD_M", "U_HS_M", "R_LS_G_M", "R_LS_PD_M"), S("J_SPULE_M", "D_FREI_M", "D_ZENER_M", "Q_LS_M"), S("R_SENSE_M", "R_I_M", "C_I_M")]),
    ("Kanal V (Vorladeschütz)", [S("U_AND2", "C_AND2"), S("R_HS_PD_V", "U_HS_V", "R_LS_G_V", "R_LS_PD_V"), S("J_SPULE_V", "D_FREI_V", "D_ZENER_V", "Q_LS_V"), S("R_SENSE_V", "R_I_V", "C_I_V")])]),
 "daisy": dict(papier="A3", zonen=[("Niedervoltseite (NV)", 0, 0, "0 0 150"), ("Trennung HV/NV", 1, 1, "194 0 0"), ("Hochvoltseite (HV)", 2, 2, "180 100 0")], zeilen=[
    ("Daisy-Chain zu den Zellüberwachungen", [S("U_DM", "C_DM"), S("T_DAISY1", "T_DAISY2"), S("J_DAISY1", "D_TVS_DAISY1", "R_DC1", "J_DAISY2", "D_TVS_DAISY2", "R_DC2")]),
    ("Sekundärpfad (Abschaltsignal der Zellüberwachungen, verstärkt isoliert)", [S("R_SEK_NV", "C_ISO2_NV"), S("U_ISO_SEK"), S("J_SEKUNDAER", "R_SEK_HV", "C_ISO2_HV")])]),
 "strom": dict(papier="A3", zonen=[("Niedervoltseite (NV)", 0, 0, "0 0 150"), ("Trennung HV/NV", 1, 1, "194 0 0"), ("Hochvoltseite (HV)", 2, 4, "180 100 0")], zeilen=[
    ("Strommessung: Shunt -> Filter -> Shunt-ADC -> digitaler Isolator -> Rechner", [S("C_ISO1_NV"), S("U_ISO_SHUNT", "C_ISO1_HV"), S("U_ADC", "C_ADC0", "C_ADC1"), S("R_SHF0", "R_SHF1", "C_SHF_D", "C_SHF0", "C_SHF1"), S("J_SHUNT")])]),
}
TITEL = {"versorgung": ("Versorgung 12 V", "Verpolschutz, Überspannungsschutz, Filter, Systembasis-IC mit Watchdog"), "rechner": ("Rechner", "Sicherheitsrechner (Lockstep), Takt, Reset, Debug, Leuchtdioden, NTC"),
         "can": ("CAN", "2 CAN-FD-Kanäle mit Gleichtaktdrossel, ESD, Abschluss"), "schuetz": ("Schützansteuerung", "3 Kanäle, High-Side und Low-Side, Zener-Löschung, Hardware-UND Sekundärpfad"),
         "daisy": ("Daisy-Master mit Isolation", "Daisy-Master, 2 Übertrager verstärkt, Sekundärpfad mit digitalem Isolator"), "strom": ("Strommessung HV-Seite", "Shunt-ADC auf der HV-Seite, digitaler Isolator verstärkt")}
ORDER = ["versorgung", "rechner", "can", "schuetz", "daisy", "strom"]
SHEET_OF = {}
for sh, sp in SPEC.items():
    for _, cols in sp["zeilen"]:
        for c in cols:
            for tag in c: SHEET_OF[tag] = sh
assert set(SHEET_OF) == set(BY), (set(BY) - set(SHEET_OF), set(SHEET_OF) - set(BY))
alias = {}
def netn(n):
    if n is None: return None
    if n.startswith("N$"): alias.setdefault(n, "N_" + n[2:])
    return alias.get(n, n)
NETSHEETS = collections.defaultdict(set)
for t in teile:
    for p, n in t["pins"].items():
        if n: NETSHEETS[n].add(SHEET_OF[t["tag"]])
def label_net(n): return n in SUPPLY or len(NETSHEETS[n]) > 1
def akte(t):
    if t["seite"] == "BR": return "ENT-191 (Brücke über die Sperrzone), ERW-E3c"
    return "BT-311 ENT-188..197, ERW-E3c" + (" (HV-Seite)" if t["seite"] == "HV" else "")
KIND = lambda t: "R" if t["name"] in ("R", "R_Sense") else "C" if t["name"] in ("C", "C_8", "C_12", "C_Elko") else "D" if t["name"] in ("Z_Diode_Gate", "TVS_ISO7637", "ESD_Diode", "TVS_Daisy", "Diode_Freilauf", "Z_Diode_Loeschung", "LED") else "box"
ANODE = {"Z_Diode_Gate": "A", "TVS_ISO7637": "A", "ESD_Diode": "A", "TVS_Daisy": "A", "Diode_Freilauf": "A", "Z_Diode_Loeschung": "A", "LED": "A"}
def short(v):
    v = v.split(" (")[0]; return v[:26]

# ================= Kern: Elemente, Seiten, Spaltenlayout mit Drähten =================
class It:
    def __init__(s, key, kind, row, col, pins, t=None, titel=None):
        s.key, s.kind, s.row, s.col, s.pins, s.t, s.titel = key, kind, row, col, pins, t, titel   # pins: Liste (num, name, net)
        s.side = {}; s.loop = None; s.dir = "R"; s.cx = s.cy = 0.0; s.pos = {}; s.order = [p[0] for p in pins]
    @property
    def pn(s): return {n: nm for n, nm, _ in s.pins}
    @property
    def net(s): return {n: nt for n, _, nt in s.pins}

class Seite:
    def __init__(s, titel, datei, papier="A3"): s.titel, s.datei, s.papier = titel, datei, papier; s.el = []; s.libs = {}; s.uuid = ROOT if datei == f"{PK}.kicad_sch" else U(); s.sheet_uuid = U(); s.xmax = s.ymax = 0
    def ext(s, x, y): s.xmax = max(s.xmax, x); s.ymax = max(s.ymax, y)
    def text(s, txt, x, y, gr=1.8, ang=0):
        s.el.append(f'(text {q(txt)} (exclude_from_sim no) (at {x} {y} {ang}) (effects (font (size {gr} {gr})) (justify left)) (uuid {q(U())}))')
    def rahmen(s, x0, y0, x1, y1, farbe="194 0 0", stil="dash", w=0.3):
        r, g, b = farbe.split(); s.el.append(f'(rectangle (start {x0} {y0}) (end {x1} {y1}) (stroke (width {w}) (type {stil}) (color {r} {g} {b} 1)) (fill (type none)) (uuid {q(U())}))')
    def draht(s, x1, y1, x2, y2):
        if (round(x1, 3), round(y1, 3)) == (round(x2, 3), round(y2, 3)): return
        s.el.append(f'(wire (pts (xy {round(x1, 4)} {round(y1, 4)}) (xy {round(x2, 4)} {round(y2, 4)})) (stroke (width 0) (type default)) (uuid {q(U())}))'); s.ext(max(x1, x2), max(y1, y2))
    def junction(s, x, y): s.el.append(f'(junction (at {round(x, 4)} {round(y, 4)}) (diameter 0) (color 0 0 0 0) (uuid {q(U())}))')
    def nc(s, x, y): s.el.append(f'(no_connect (at {round(x, 4)} {round(y, 4)}) (uuid {q(U())}))')
    def label(s, name, x, y, ang, art):
        j = "right" if ang == 180 else "left"; s.ext(x + (0 if ang == 180 else len(name) * 1.5 + 3), y)
        if art == "global": s.el.append(f'(global_label {q(name)} (shape passive) (at {round(x, 4)} {round(y, 4)} {ang}) (fields_autoplaced yes) (effects (font (size 1.27 1.27)) (justify {j})) (uuid {q(U())}) (property "Intersheetrefs" "${{INTERSHEET_REFS}}" (at {x} {y} 0) (effects (font (size 1.27 1.27)) hide)))')
        else: s.el.append(f'(hierarchical_label {q(name)} (shape bidirectional) (at {round(x, 4)} {round(y, 4)} {ang}) (effects (font (size 1.27 1.27)) (justify {j})) (uuid {q(U())}))')
    def schreiben(s):
        lib = "\n".join(s.libs.values())
        tb = f'(title_block (title {q("BMS-Platine BT-311: " + s.titel)}) (date "2026-11-24") (rev "0.2") (company "KI-generiert (Claude Sonnet), Entwurf, nicht freigegeben") (comment 1 "Dok.-Nr. SCH-E3c, Version 0.2, Status Entwurf, Pruefer Opus offen") (comment 2 "KI-generiert (Claude Sonnet, 2026-11-24)") (comment 3 "Quelle: sim/elektrik/e3c_bms_platine/bms_skidl.py -> bms_teile.json, Akten ENT-188..197, ERW-E3c"))'
        s.rahmen(10, 8, 150, 19, "0 0 0", "solid", 0.4); s.text("KI-generiert (Claude Sonnet, 2026-11-24), Entwurf, nicht freigegeben", 12, 13.5, 2.0)
        ph = {"A3": 285, "A2": 408}[s.papier]
        s.text("KI-generiert (Claude Sonnet, 2026-11-24), Entwurf. Dok.-Nr. SCH-E3c v0.2. Werte: ERW-E3c, Passivwerte offen.", 12, ph, 1.8)
        txt = f'(kicad_sch (version 20250114) (generator "eeschema") (generator_version "10.0") (uuid {q(s.uuid)}) (paper {q(s.papier)})\n{tb}\n(lib_symbols\n{lib}\n)\n' + "\n".join(s.el) + "\n(embedded_fonts no)\n)\n"
        (OUT / s.datei).write_text(txt)

def lib_symbol(it):
    """Bibliothekssymbol je Instanz (Name bms:<key>)."""
    nm = it.key; L = [n for n in it.order if it.side[n] == "L"]; R = [n for n in it.order if it.side[n] == "R"]
    pins = []
    if it.kind == "box":
        w, h = it.w, it.h; body = f'(rectangle (start {-w/2} {-h/2}) (end {w/2} {h/2}) (stroke (width 0.254) (type default)) (fill (type background)))'
        for i, n in enumerate(L): pins.append((n, -(w / 2 + 2.54), h / 2 - 2.54 * (i + 1), 0, 2.54))
        for i, n in enumerate(R): pins.append((n, w / 2 + 2.54, h / 2 - 2.54 * (i + 1), 180, 2.54))
        hide = ""
    else:
        a = it.order[0]; left = L[0]; right = R[0]
        if it.kind == "R": body = '(rectangle (start -2.54 -1.016) (end 2.54 1.016) (stroke (width 0.254) (type default)) (fill (type none)))'; ln = 2.54
        elif it.kind == "C": body = '(polyline (pts (xy -0.762 2.032) (xy -0.762 -2.032)) (stroke (width 0.508) (type default)) (fill (type none))) (polyline (pts (xy 0.762 2.032) (xy 0.762 -2.032)) (stroke (width 0.508) (type default)) (fill (type none)))'; ln = 4.318
        else:
            if it.dir == "R": body = '(polyline (pts (xy -1.27 1.27) (xy -1.27 -1.27) (xy 1.27 0) (xy -1.27 1.27)) (stroke (width 0.254) (type default)) (fill (type none))) (polyline (pts (xy 1.27 1.27) (xy 1.27 -1.27)) (stroke (width 0.254) (type default)) (fill (type none)))'
            else: body = '(polyline (pts (xy 1.27 1.27) (xy 1.27 -1.27) (xy -1.27 0) (xy 1.27 1.27)) (stroke (width 0.254) (type default)) (fill (type none))) (polyline (pts (xy -1.27 1.27) (xy -1.27 -1.27)) (stroke (width 0.254) (type default)) (fill (type none)))'
            ln = 3.81
        pins = [(left, -5.08, 0, 0, ln), (right, 5.08, 0, 180, ln)]; hide = "hide"
    ps = "\n".join(f'    (pin passive line (at {x} {y} {a}) (length {ln}) (name {q(it.pn[n])} (effects (font (size 0.9 0.9)){" hide" if it.kind != "box" else ""})) (number {q(n)} (effects (font (size 0.8 0.8)){" hide" if it.kind != "box" else ""})))' for n, x, y, a, ln in pins)
    return f'''  (symbol {q("bms:" + nm)} (pin_names (offset 0.5)) (exclude_from_sim no) (in_bom yes) (on_board yes)
    (property "Reference" "U" (at 0 {it.h/2+2} 0) {FONT})
    (property "Value" "" (at 0 {-it.h/2-2} 0) {FONT})
    (property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
    (property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
    (symbol {q(nm + "_0_1")} {body})
    (symbol {q(nm + "_1_1")}
{ps}
    )
  )''', {n: (x, y) for n, x, y, a, ln in pins}

def geometrie(it):
    L = [n for n in it.order if it.side[n] == "L"]; R = [n for n in it.order if it.side[n] == "R"]
    if it.kind == "box":
        m = max(len(L), len(R), 1); it.w = 27.94; it.h = 2.54 * (m + 1); it.lext = it.rext = it.w / 2 + 2.54; it.hh = it.h; it.top = 14; it.bot = 4
    elif it.kind == "sheet":
        m = max(len(L), len(R), 1); it.w = 60.96; it.h = 2.54 * (m + 2); it.lext = it.rext = it.w / 2; it.hh = it.h; it.top = 10; it.bot = 8
    else: it.w, it.h = 10.16, 4.06; it.lext = it.rext = 5.08; it.hh = 4.06; it.top = 10; it.bot = 6

def layout(items, wired, ncols, lblr, x0=20, y0=44, rowtitles=None):
    """Positioniert Elemente; wired: dict net -> (cmin, [(item, num)]). Gibt Spaltenmaße, Trackzuordnung zurück."""
    for it in items: geometrie(it)
    rows = sorted({it.row for it in items})
    # Labelbreiten je Spalte/Seite
    lw = {}
    for it in items:
        for n in it.order:
            net = it.net[n]
            if net and (net not in wired):
                key = (it.col, it.side[n]); lw[key] = max(lw.get(key, 0), len(netn(net)) * 1.55 + 6.5)
    colL = {c: max([it.lext + lw.get((c, "L"), 0) for it in items if it.col == c] + [11.0]) for c in range(ncols)}
    colR = {c: max([it.rext + lw.get((c, "R"), 0) for it in items if it.col == c] + [11.0]) for c in range(ncols)}
    ntr = collections.Counter(cmin for cmin, _ in wired.values()); tracks = {}; cnt = collections.Counter()
    for n in wired: c = wired[n][0]; tracks[n] = cnt[c]; cnt[c] += 1
    gap = {c: 2.54 * (ntr[c] + 2) for c in range(ncols)}
    xc = {}; x = x0 + colL[0]
    for c in range(ncols):
        xc[c] = sn(x); x = xc[c] + colR[c] + gap[c] + (colL[c + 1] if c + 1 < ncols else 0)
    # Zeilenhöhe
    y = y0; rowy = {}
    for r in rows:
        rowy[r] = y + (9 if rowtitles else 0); colh = []
        for c in range(ncols):
            yy = rowy[r]
            for it in sorted([i for i in items if i.row == r and i.col == c], key=lambda i: i.seq):
                it.cx = xc[c]; it.cy = sn(yy + it.top + it.hh / 2); yy += it.top + it.hh + it.bot
            colh.append(yy)
        y = max(colh + [rowy[r] + 10]) + 6
    trackx = {n: sn(xc[wired[n][0]] + colR[wired[n][0]] + 2.54 * (tracks[n] + 1)) for n in wired}
    for it in items:   # Pinkoordinaten (Schaltplan, y nach unten)
        s, pins = lib_symbol(it) if it.kind != "sheet" else (None, None)
        it.pos = {}
        if it.kind != "sheet":
            for n, (px, py) in pins.items(): it.pos[n] = (round(it.cx + px, 4), round(it.cy - py, 4))
        else:
            L = [n for n in it.order if it.side[n] == "L"]; R = [n for n in it.order if it.side[n] == "R"]
            for i, n in enumerate(L): it.pos[n] = (it.cx - it.w / 2, it.cy - (it.h / 2 - 2.54 * (i + 1)))
            for i, n in enumerate(R): it.pos[n] = (it.cx + it.w / 2, it.cy - (it.h / 2 - 2.54 * (i + 1)))
    return dict(xc=xc, colL=colL, colR=colR, rowy=rowy, trackx=trackx, y1=y, gap=gap)

LOKAL = set()   # Netze, die nicht verdrahtet werden konnten (Spannweite > 1 Spalte): blattintern per Label
def verdrahten(sp, items, wired, geo, art):
    """Drähte, Junctions, Labels, No-Connect auf Seite sp."""
    for n, (cmin, pl) in wired.items():
        TX = geo["trackx"][n]; ys = set(); stubs = collections.Counter()
        for it, num in pl:
            px, py = it.pos[num]; side = it.side[num]; want = "R" if it.col == cmin else "L"
            if it.kind in ("R", "C", "D") and side != want:   # Schleife unter dem Bauteil
                yl = sn(py + 3.81); ox = px + (2.54 if side == "R" else -2.54)
                sp.draht(px, py, ox, py); sp.draht(ox, py, ox, yl); sp.draht(ox, yl, TX, yl); ys.add(yl); stubs[yl] += 1
            else: sp.draht(px, py, TX, py); ys.add(py); stubs[py] += 1
        ymin, ymax = min(ys), max(ys); yl = sorted(ys)
        for a, b in zip(yl, yl[1:]): sp.draht(TX, a, TX, b)
        for y in yl:
            deg = (1 if y > ymin else 0) + (1 if y < ymax else 0) + stubs[y]
            if deg >= 3: sp.junction(TX, y)
    for it in items:
        for n in it.order:
            net = it.net[n]; px, py = it.pos[n]; side = it.side[n]
            if net is None:
                if it.kind == "box": sp.nc(px, py)
            elif net not in wired:
                nm = netn(net); a = "global" if (net in SUPPLY or net in LOKAL) else "hier"
                sp.label(nm, px, py, 180 if side == "L" else 0, a)

def ordnen(items, wired):
    """Pins je Seite nach Höhe der Partner sortieren (zweiter Durchlauf); order = links (oben->unten) + rechts."""
    for it in items:
        if it.kind in ("R", "C", "D"): continue
        res = []
        for sd in ("L", "R"):
            ns = [n for n in it.order if it.side[n] == sd]
            def key(n):
                net = it.net[n]
                if net in wired:
                    ys = [o.cy for o, m in wired[net][1] if o is not it]
                    if ys: return (0, sum(ys) / len(ys), n.zfill(4))
                return (1, 0, n.zfill(4))
            res += sorted(ns, key=key)
        it.order = res
def symbol_instanz(sp, it, pfad):
    lib, _ = lib_symbol(it); sp.libs[it.key] = lib; t = it.t; cx, cy = it.cx, it.cy
    if it.kind == "box": tx, ty = cx - it.w / 2, [cy - it.h / 2 - 9.5, cy - it.h / 2 - 7.0, cy - it.h / 2 - 4.5]
    else: tx, ty = cx - 5.08, [cy - 8.9, cy - 6.6, cy - 4.8]
    props = f'(property "Reference" {q(t["ref"])} (at {tx} {ty[0]} 0) (effects (font (size 1.27 1.27)) (justify left)))\n' \
            f'(property "Value" {q(short(t["value"]))} (at {tx} {ty[1]} 0) (effects (font (size 1.0 1.0)) (justify left)))\n' \
            f'(property "Footprint" {q(t["footprint"])} (at {cx} {cy} 0) (effects (font (size 1.27 1.27)) hide))\n(property "Datasheet" "" (at {cx} {cy} 0) (effects (font (size 1.27 1.27)) hide))\n' \
            f'(property "Tag" {q(t["tag"])} (at {cx} {cy} 0) (effects (font (size 1.0 1.0)) hide))\n' \
            f'(property "Akte" {q(akte(t))} (at {tx} {ty[2]} 0) (effects (font (size 0.9 0.9)) (justify left){"" if it.kind == "box" else " hide"}))'
    pins = "".join(f'(pin {q(n)} (uuid {q(U())}))' for n in it.order)
    sp.el.append(f'(symbol (lib_id {q("bms:" + it.key)}) (at {cx} {cy} 0) (unit 1) (exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no) (fields_autoplaced yes) (uuid {q(U())})\n{props}\n{pins}\n'
                 f'(instances (project {q(PK)} (path {q(pfad)} (reference {q(t["ref"])}) (unit 1)))))')
    sp.ext(cx + it.rext + 20, cy + it.hh / 2 + 6)

def seitenwahl(items, wired, lblr, labelnet_fn):
    for it in items: it.side = {}
    for n, (cmin, pl) in wired.items():
        for it, num in pl: it.side[num] = "R" if it.col == cmin else "L"
    for it in items:
        nums = it.order
        if it.kind in ("R", "C", "D"):
            a, b = nums; sa, sb = it.side.get(a), it.side.get(b)
            if sa and sb and sa == sb: it.side[b] = "L" if sa == "R" else "R"; it.loop = b
            elif sa and not sb: it.side[b] = "L" if sa == "R" else "R"
            elif sb and not sa: it.side[a] = "L" if sb == "R" else "R"
            elif not sa and not sb: it.side[a], it.side[b] = "L", "R"
            if it.kind == "D":
                ak = [n for n in nums if it.pn[n] == ANODE[it.t["name"]]][0]; it.dir = "R" if it.side[ak] == "L" else "L"
        else:
            for num in nums:
                if num in it.side: continue
                nt = it.net[num]
                it.side[num] = "R" if (nt is None) else ("L" if nt in SUPPLY else ("R" if lblr else "L"))
# ================= Hauptteil =================
def pinliste(t): return [(n, t["pinnamen"][n], t["pins"][n]) for n in sorted(t["pins"], key=int)]
def netze_der_seite(items, only=None):
    d = collections.defaultdict(list)
    for it in items:
        for n, nm, net in it.pins:
            if net and (only is None or only(net)): d[net].append((it, n))
    return d
def gruppiere(items, cand):
    wired = {}
    for net, pl in cand.items():
        if len(pl) < 2: continue
        cols = [it.col for it, _ in pl]; cmin, cmax = min(cols), max(cols)
        if cmax - cmin > 1: LOKAL.add(net); print("  Spannweite > 1 Spalte, Label:", net, cmin, cmax); continue
        wired[net] = (cmin, pl)
    return wired
def layout_zwei_durchlaeufe(items, wired, ncols, lblr, rowtitles):
    seitenwahl(items, wired, lblr, None)
    for it in items: it.cy = 0
    geo = layout(items, wired, ncols, lblr, rowtitles=rowtitles); ordnen(items, wired); seitenwahl_nach_ordnen = None
    geo = layout(items, wired, ncols, lblr, rowtitles=rowtitles); ordnen(items, wired)
    return layout(items, wired, ncols, lblr, rowtitles=rowtitles)

SEITEN = {}; ALLE = {}
for sh in ORDER:
    sp = SPEC[sh]; items = []; seq = 0
    for r, (title, cols) in enumerate(sp["zeilen"]):
        for c, tags in enumerate(cols):
            for tag in tags:
                t = BY[tag]; it = It(t["ref"], KIND(t), r, c, pinliste(t), t); it.seq = seq; seq += 1; items.append(it)
    ncols = max(len(cols) for _, cols in sp["zeilen"])
    cand = netze_der_seite(items, lambda n: not label_net(n))
    wired = gruppiere(items, cand); print(sh, len(items), "Teile,", len(wired), "verdrahtete Netze")
    geo = layout_zwei_durchlaeufe(items, wired, ncols, sp.get("lblR", False), True)
    seite = Seite(TITEL[sh][0], sh + ".kicad_sch", sp["papier"]); SEITEN[sh] = seite; ALLE[sh] = (items, wired, geo)
    pfad = f"/{ROOT}/{seite.sheet_uuid}"
    seite.text(f"{TITEL[sh][0]}: {TITEL[sh][1]}. Drähte innerhalb des Blattes; Netznamen nur für Versorgung/GND (global) und zwischen den Blättern (hierarchisch, Blattpins auf dem Deckblatt).", 12, 25, 1.8)
    for r, (title, cols) in enumerate(sp["zeilen"]): seite.text(title, 14, geo["rowy"][r] - 5, 2.0)
    for it in items: symbol_instanz(seite, it, pfad)
    verdrahten(seite, items, wired, geo, None)
    for nm, ca, cb, farbe in sp.get("zonen", []):
        xa, xb = geo["xc"][ca] - geo["colL"][ca] - 5, geo["xc"][cb] + geo["colR"][cb] + 5; ya = 32 + 8
        seite.rahmen(xa, ya, xb, geo["y1"] + 2, farbe, "dash", 0.4 if "Trennung" in nm else 0.2); seite.text(nm, xa + 2, ya + 3, 2.0)
        if "Trennung" in nm: seite.text("verstärkte Isolation", xa + 2, ya + 8, 1.8); seite.text(f"{f0(KR)}/{f0(LU)} mm (Kriech-/Luftstrecke)", xa + 2, ya + 11.5, 1.5); seite.text("ENT-191", xa + 2, ya + 15, 1.5)
    print("  Ausdehnung x/y:", round(seite.xmax), round(seite.ymax), seite.papier)

# ---- Deckblatt: Blattsymbole mit Blattpins und Drähten
root = Seite("Deckblatt", f"{PK}.kicad_sch", "A3"); SEITEN["root"] = root
colroot = {"versorgung": 0, "rechner": 1, "can": 2, "schuetz": 2, "daisy": 2, "strom": 2}
rit = []; seq = 0
for sh in ["versorgung", "rechner", "can", "schuetz", "daisy", "strom"]:
    nets = sorted({n for it in ALLE[sh][0] for _, _, n in it.pins if n and n not in SUPPLY and len(NETSHEETS[n]) > 1})
    pins = [(n, n, n) for n in nets]; it = It(sh, "sheet", 0, colroot[sh], pins, None, TITEL[sh][0]); it.seq = seq; seq += 1; rit.append(it)
cand = collections.defaultdict(list)
for it in rit:
    for n, nm, net in it.pins: cand[net].append((it, n))
rwired = gruppiere(rit, cand)
for it in rit: it.sh = it.key
# Sheet-Seitenwahl: Pins zeigen zu den Partnern
for it in rit: it.side = {}
for n, (cmin, pl) in rwired.items():
    for it, num in pl: it.side[num] = "R" if it.col == cmin else "L"
for it in rit:
    for n in it.order: it.side.setdefault(n, "R")
rgeo = None
for _ in range(2):
    rgeo = layout(rit, rwired, 3, False, rowtitles=False); ordnen(rit, rwired)
rgeo = layout(rit, rwired, 3, False, rowtitles=False)
root.text("BMS-Platine BT-311 (Batteriemanagement-Steuerplatine), 160 x 100 mm, 4 Lagen (ENT-188, ENT-189, ENT-190), Kriechstrecke HV/NV 10 mm (ENT-191), Luftstrecke 8 mm (ENT-195).", 12, 25, 2.0)
root.text("KI-generiert (Claude Sonnet, 2026-11-24), Entwurf, nicht freigegeben. Quelle: bms_skidl.py (wie das Layout). Passivwerte und Footprintgrößen offen/Platzhalter (ERGEBNIS.md).", 12, 31, 1.6)
root.text(f"Blattpins = Verbindungen zwischen den Blöcken (Drähte). Versorgung (GND, +3V3, +5V, VBAT_F, HV_GND, HV_VDD) über globale Labels. HV/NV-Trennung (rot gestrichelt): {ISO}.", 12, 37, 1.6)
for it in rit:
    sh = it.key; sp = SEITEN[sh]; sx, sy = it.cx - it.w / 2, it.cy - it.h / 2; L = [n for n in it.order if it.side[n] == "L"]; R = [n for n in it.order if it.side[n] == "R"]
    spins = []
    for i, n in enumerate(L): spins.append(f'(pin {q(n)} bidirectional (at {sx} {round(it.cy - (it.h / 2 - 2.54 * (i + 1)), 4)} 180) (uuid {q(U())}) (effects (font (size 1.27 1.27)) (justify left)))')
    for i, n in enumerate(R): spins.append(f'(pin {q(n)} bidirectional (at {round(sx + it.w, 4)} {round(it.cy - (it.h / 2 - 2.54 * (i + 1)), 4)} 0) (uuid {q(U())}) (effects (font (size 1.27 1.27)) (justify right)))')
    page = ORDER.index(sh) + 2
    root.el.append(f'(sheet (at {sx} {sy}) (size {it.w} {it.h}) (exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no) (fields_autoplaced yes) (stroke (width 0.1524) (type solid)) (fill (color 0 0 0 0.0)) (uuid {q(sp.sheet_uuid)})\n'
                   f'(property "Sheetname" {q(it.titel)} (at {sx} {sy - 1} 0) (effects (font (size 1.27 1.27)) (justify left bottom)))\n(property "Sheetfile" {q(sp.datei)} (at {sx} {round(sy + it.h + 1, 4)} 0) (effects (font (size 1.27 1.27)) (justify left top)))\n'
                   + "\n".join(spins) + f'\n(instances (project {q(PK)} (path {q("/" + ROOT)} (page {q(str(page))}))))\n)')
    root.ext(sx + it.w + 20, sy + it.h + 8)
    if sh in ("daisy", "strom"): root.rahmen(sx - 3, sy - 8, sx + it.w + 3, sy + it.h + 3, "194 0 0", "dash", 0.3); root.text("enthält HV/NV-Trennung", sx + 1, sy - 4.5, 1.4)
LOKAL_ROOT = set()
verdrahten(root, rit, rwired, rgeo, None)
print("Deckblatt Ausdehnung:", round(root.xmax), round(root.ymax))
for s in SEITEN.values(): s.schreiben()
json.dump({"blatt_von_ref": {t["ref"]: SHEET_OF[t["tag"]] for t in teile}, "anzahl_teile": len(teile), "alias": alias, "nicht_verdrahtet": sorted(LOKAL)}, open(H / "schaltplan_zuordnung.json", "w"), indent=1)
print("geschrieben", len(teile), "Teile")
