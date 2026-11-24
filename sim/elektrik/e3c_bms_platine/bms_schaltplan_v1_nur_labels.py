#!/usr/bin/env python3
"""E3c hierarchischer KiCad-Schaltplan (.kicad_sch) der BMS-Platine BT-311 aus bms_teile.json (dieselbe Quelle wie das Layout, bms_skidl.py).
KI-generiert (Claude Sonnet, 2026-11-24), Entwurf. Muster: sim/elektrik/e3_platine/schaltplan.py (Aufbau, hier angepasst, dort unverändert).
Blätter: Deckblatt, Versorgung 12 V, Rechner, CAN, Schützansteuerung, Daisy-Master mit Isolation (mit Sekundärpfad), Strommessung HV-Seite.
Verbindung nur über Netznamen (globale Labels). HV/NV-Trennung als Rahmen mit Isolationsvermerk. Werte Kriech-/Luftstrecke aus ergebnis_platine.json.
Aufruf: source umgebung.sh; python3 bms_schaltplan.py -> /home/cae/cae_projekte/batterie/e3c/schaltplan/*.kicad_sch"""
import json, uuid, re, pathlib
H = pathlib.Path(__file__).resolve().parent; OUT = pathlib.Path("/home/cae/cae_projekte/batterie/e3c/schaltplan"); OUT.mkdir(parents=True, exist_ok=True)
PK = "bms_schaltplan"; U = lambda: str(uuid.uuid4()); sn = lambda x: round(round(x / 2.54) * 2.54, 4)
def q(s): return '"' + str(s).replace('"', "'") + '"'
FONT = "(effects (font (size 1.27 1.27)))"
sz = json.load(open(H / "ergebnis_platine.json"))["sperrzone"]; KR, LU = sz["kriech_mm"], sz["luft_mm"]
f0 = lambda x: f"{x:g}"
ISO = f"verstärkte Isolation {f0(KR)}/{f0(LU)} mm (Kriechstrecke/Luftstrecke, ENT-191)"
teile = json.load(open(H / "bms_teile.json"))["teile"]; ROOT = U()

def blatt_von(tag):
    if tag.startswith(("J_VERSORGUNG", "Q_VERPOL", "R_VERPOL", "D_VERPOL", "D_TVS", "L_VERSORGUNG", "C_VBAT", "U_SBC", "R_KL15", "C_SBC")) and not tag.startswith("D_TVS_DAISY"): return "versorgung"
    if tag.startswith(("U_MCU", "C_MCU", "C_RESET", "Y_MCU", "C_XTAL", "J_DEBUG", "D_LED", "R_LED", "R_NTC")): return "rechner"
    if tag.startswith(("U_CAN", "R_STB", "L_CAN", "R_TERM", "C_TERM", "D_ESD", "C_CAN", "J_CAN")): return "can"
    if tag.startswith(("U_AND", "C_AND", "U_HS", "R_HS", "Q_LS", "R_LS", "R_SENSE", "R_I_", "C_I_", "D_FREI", "D_ZENER", "J_SPULE")): return "schuetz"
    if tag.startswith(("U_DM", "C_DM", "T_DAISY", "J_DAISY", "D_TVS_DAISY", "R_DC", "U_ISO_SEK", "R_SEK", "C_ISO2", "J_SEKUNDAER")): return "daisy"
    if tag.startswith(("J_SHUNT", "R_SHF", "C_SHF", "U_ADC", "C_ADC", "U_ISO_SHUNT", "C_ISO1")): return "strom"
    raise SystemExit("Blatt fehlt für " + tag)
for t in teile: t["blatt"] = blatt_von(t["tag"])
assert sorted(t["ref"] for t in teile) == sorted(set(t["ref"] for t in teile))

def akte(t):
    if t["seite"] == "BR": return "ENT-191 (Brücke über die Sperrzone, verstärkte Isolation), ERW-E3c"
    if t["seite"] == "HV": return "BT-311 ENT-188..191, ERW-E3c (HV-Seite)"
    return "BT-311 ENT-188..191, ERW-E3c"
KIND = lambda t: "R" if t["name"] in ("R", "R_Sense") else "C" if t["name"] in ("C", "C_8", "C_12", "C_Elko") else "D" if t["name"] in ("Z_Diode_Gate", "TVS_ISO7637", "ESD_Diode", "TVS_Daisy", "Diode_Freilauf", "Z_Diode_Loeschung", "LED") else "box"

class Sym:
    def __init__(self, name, t, kind):
        self.name, self.kind = name, kind; self.pins = {}; nums = sorted(t["pins"], key=int); nm = lambda n: t["pinnamen"][n]
        if kind != "box":
            self.w, self.h = 2.54, 10.16; self.pins[nums[0]] = (nm(nums[0]), 0, 5.08, 270); self.pins[nums[1]] = (nm(nums[1]), 0, -5.08, 90)
        else:
            n = len(nums); k = -(-n // 2) if n > 4 else n; Lp, Rp = (nums[:k], nums[k:]) if n > 4 else (nums[:-(n // 2)] if n > 1 else nums, nums[-(n // 2):] if n > 1 else [])
            m = max(len(Lp), len(Rp), 2); self.h = 2 * 2.54 * -(-(m + 1) // 2); self.w = 25.4
            for i, p in enumerate(Lp): self.pins[p] = (nm(p), -(self.w / 2 + 2.54), self.h / 2 - 2.54 * (i + 1), 0)
            for i, p in enumerate(Rp): self.pins[p] = (nm(p), self.w / 2 + 2.54, self.h / 2 - 2.54 * (i + 1), 180)
    def lib(self):
        w, h = self.w, self.h
        body = {"R": '(rectangle (start -1.016 -2.54) (end 1.016 2.54) (stroke (width 0.254) (type default)) (fill (type none)))',
                "C": '(polyline (pts (xy -2.032 0.762) (xy 2.032 0.762)) (stroke (width 0.508) (type default)) (fill (type none))) (polyline (pts (xy -2.032 -0.762) (xy 2.032 -0.762)) (stroke (width 0.508) (type default)) (fill (type none)))',
                "D": '(polyline (pts (xy -1.27 1.27) (xy 1.27 1.27) (xy 0 -1.27) (xy -1.27 1.27)) (stroke (width 0.254) (type default)) (fill (type none))) (polyline (pts (xy -1.27 -1.27) (xy 1.27 -1.27)) (stroke (width 0.254) (type default)) (fill (type none)))'
                }.get(self.kind, f'(rectangle (start {-w/2} {-h/2}) (end {w/2} {h/2}) (stroke (width 0.254) (type default)) (fill (type background)))')
        hide = "hide" if self.kind != "box" else ""
        ps = "\n".join(f'    (pin passive line (at {x} {y} {a}) (length 2.54) (name {q(n)} (effects (font (size 0.9 0.9)))) (number {q(num)} (effects (font (size 0.9 0.9)))))' for num, (n, x, y, a) in self.pins.items())
        return f'''  (symbol {q("bms:" + self.name)} (pin_names (offset 0.5) {hide}) (exclude_from_sim no) (in_bom yes) (on_board yes)
    (property "Reference" "U" (at 0 {h/2+2} 0) {FONT})
    (property "Value" "" (at 0 {-h/2-2} 0) {FONT})
    (property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
    (property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
    (symbol {q(self.name + "_0_1")} {body})
    (symbol {q(self.name + "_1_1")}
{ps}
    )
  )'''
SYMS = {}
def symfor(t):
    k = (t["name"], KIND(t))
    if k not in SYMS: SYMS[k] = Sym(t["name"], t, KIND(t))
    return SYMS[k]
alias = {}
def net(n):
    if n is None: return None
    if n.startswith("N$"): alias.setdefault(n, "N_" + n[2:])
    return alias.get(n, n)

class Blatt:
    def __init__(s, titel, datei, kurz): s.titel, s.datei, s.kurz = titel, datei, kurz; s.el = []; s.libs = {}; s.uuid = ROOT if datei == f"{PK}.kicad_sch" else U(); s.sheet_uuid = U()
    def text(s, txt, x, y, gr=1.8, farbe=None):
        s.el.append(f'(text {q(txt)} (exclude_from_sim no) (at {x} {y} 0) (effects (font (size {gr} {gr})) (justify left)) (uuid {q(U())}))')
    def rahmen(s, x0, y0, x1, y1, farbe="194 0 0", stil="dash", w=0.3):
        r, g, b = farbe.split(); s.el.append(f'(rectangle (start {x0} {y0}) (end {x1} {y1}) (stroke (width {w}) (type {stil}) (color {r} {g} {b} 1)) (fill (type none)) (uuid {q(U())}))')
    def label(s, name, x, y, ang):
        j = "right" if ang == 180 else "left"
        s.el.append(f'(global_label {q(name)} (shape passive) (at {x} {y} {ang}) (fields_autoplaced yes) (effects (font (size 1.27 1.27)) (justify {j})) (uuid {q(U())}) (property "Intersheetrefs" "${{INTERSHEET_REFS}}" (at {x} {y} 0) (effects (font (size 1.27 1.27)) hide)))')
    def teil(s, t, cx, cy):
        sym = symfor(t); cx, cy = sn(cx), sn(cy); s.libs[sym.name] = sym
        pr = f"/{ROOT}/{s.sheet_uuid}"
        tx = cx + sym.w / 2 + 2.0; ty = [cy - 2.5, cy - 0.5, cy + 1.5, cy + 3.5]
        if sym.kind == "box": tx = cx - sym.w / 2; ty = [cy - sym.h / 2 - 9.5, cy - sym.h / 2 - 7.0, cy - sym.h / 2 - 4.5, cy - sym.h / 2 - 2.5]
        props = f'(property "Reference" {q(t["ref"])} (at {tx} {ty[0]} 0) (effects (font (size 1.27 1.27)) (justify left)))\n' \
                f'(property "Value" {q(t["value"][:60])} (at {tx} {ty[1]} 0) (effects (font (size 1.0 1.0)) (justify left)))\n' \
                f'(property "Footprint" {q(t["footprint"])} (at {cx} {cy} 0) (effects (font (size 1.27 1.27)) hide))\n(property "Datasheet" "" (at {cx} {cy} 0) (effects (font (size 1.27 1.27)) hide))\n' \
                f'(property "Tag" {q(t["tag"])} (at {tx} {ty[2]} 0) (effects (font (size 1.0 1.0)) (justify left)))\n' \
                f'(property "Akte" {q(akte(t))} (at {tx} {ty[3]} 0) (effects (font (size 0.9 0.9)) (justify left)))'
        pins = "".join(f'(pin {q(n)} (uuid {q(U())}))' for n in sym.pins)
        s.el.append(f'(symbol (lib_id {q("bms:" + sym.name)}) (at {cx} {cy} 0) (unit 1) (exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no) (fields_autoplaced yes) (uuid {q(U())})\n{props}\n{pins}\n'
                    f'(instances (project {q(PK)} (path {q(pr)} (reference {q(t["ref"])}) (unit 1)))))')
        for num, (nm, px, py, a) in sym.pins.items():
            n = net(t["pins"].get(num))
            if n: s.label(n, cx + px, cy - py, 180 if a == 0 else 0)
            else: s.el.append(f'(no_connect (at {cx + px} {cy - py}) (uuid {q(U())}))')
    def schreiben(s):
        lib = "\n".join(y.lib() for y in s.libs.values())
        tb = f'(title_block (title {q("BMS-Platine BT-311: " + s.titel)}) (date "2026-11-24") (rev "0.1") (company "KI-generiert (Claude Sonnet), Entwurf, nicht freigegeben") (comment 1 "Dok.-Nr. SCH-E3c, Version 0.1, Status Entwurf, Pruefer Opus offen") (comment 2 "KI-generiert (Claude Sonnet, 2026-11-24)") (comment 3 "Quelle: sim/elektrik/e3c_bms_platine/bms_skidl.py -> bms_teile.json, Akten ENT-188..191, ERW-E3c"))'
        s.rahmen(10, 8, 150, 19, "0 0 0", "solid", 0.4); s.text("KI-generiert (Claude Sonnet, 2026-11-24), Entwurf, nicht freigegeben", 12, 13.5, 2.0)
        s.text("KI-generiert (Claude Sonnet, 2026-11-24), Entwurf. Dok.-Nr. SCH-E3c v0.1. Zahlen und Werte: ERW-E3c, Passivwerte offen.", 12, 288, 1.8)
        txt = f'(kicad_sch (version 20250114) (generator "eeschema") (generator_version "10.0") (uuid {q(s.uuid)}) (paper "A3")\n{tb}\n(lib_symbols\n{lib}\n)\n' + "\n".join(s.el) + "\n(embedded_fonts no)\n)\n"
        (OUT / s.datei).write_text(txt)

def flow(b, items, x0, x1, y0):
    """Teile in Regionen [x0,x1] zeilenweise platzieren, Rückgabe unterer Rand."""
    items = sorted(items, key=lambda t: (KIND(t) != "box", -len(t["pins"]), t["ref"]))
    x, y, rh = x0, y0, 0
    for t in items:
        sym = symfor(t)
        if sym.kind == "box": wid, hei = sym.w + 5.08 + 2 * 34 + 20, sym.h + 26; ox = wid / 2; oy = 14 + sym.h / 2
        else: wid, hei = 52, 30; ox = 6; oy = 14
        if x + wid > x1 and x > x0: x = x0; y += rh; rh = 0
        b.teil(t, x + ox, y + oy); x += wid; rh = max(rh, hei)
    return y + rh

SH = {"versorgung": ("Versorgung 12 V", "versorgung.kicad_sch", "Verpolschutz, Überspannungsschutz, Filter, Systembasis-IC mit Watchdog"),
      "rechner": ("Rechner", "rechner.kicad_sch", "Sicherheitsrechner (Lockstep), Takt, Reset, Debug, Leuchtdioden, NTC"),
      "can": ("CAN", "can.kicad_sch", "2 CAN-FD-Kanäle mit Gleichtaktdrossel, ESD, Abschluss"),
      "schuetz": ("Schützansteuerung", "schuetz.kicad_sch", "3 Kanäle (High-Side und Low-Side, Zener-Löschung), Hardware-UND Sekundärpfad"),
      "daisy": ("Daisy-Master mit Isolation", "daisy.kicad_sch", "Daisy-Master, 2 Übertrager verstärkt, Sekundärpfad mit digitalem Isolator, HV/NV-Trennung"),
      "strom": ("Strommessung HV-Seite", "strom.kicad_sch", "Shunt-ADC auf HV-Seite, digitaler Isolator verstärkt, HV/NV-Trennung")}
B = {k: Blatt(v[0], v[1], v[2]) for k, v in SH.items()}; root = Blatt("Deckblatt", f"{PK}.kicad_sch", "")
for k, b in B.items():
    ts = [t for t in teile if t["blatt"] == k]; hv = any(t["seite"] != "NV" for t in ts)
    b.text(f"{b.titel}: {b.kurz}. Schaltung nur über globale Netznamen verbunden; Kopf je Teil: Referenz, Wert, Tag, Akte.", 12, 25, 1.8)
    if not hv:
        b.text("Niedervoltseite (NV)", 14, 36, 2.0); b.rahmen(12, 38, 408, 282, "0 0 150", "dash", 0.2); flow(b, ts, 16, 404, 42)
    else:
        nv = [t for t in ts if t["seite"] == "NV"]; hvt = [t for t in ts if t["seite"] == "HV"]; br = [t for t in ts if t["seite"] == "BR"]
        XN0, XN1, XB0, XB1, XH0, XH1 = 14, 165, 170, 270, 275, 406
        b.text("Niedervoltseite (NV)", XN0 + 2, 36, 2.0); b.rahmen(XN0 - 2, 38, XN1 + 2, 282, "0 0 150", "dash", 0.2)
        b.text("Hochvoltseite (HV)", XH0 + 2, 36, 2.0); b.rahmen(XH0 - 2, 38, XH1 + 2, 282, "180 100 0", "dash", 0.2)
        b.rahmen(XB0, 38, XB1, 282, "194 0 0", "dash", 0.4); b.text("Trennung HV/NV", XB0 + 3, 36, 2.0, None)
        b.text(ISO, XB0 + 3, 42, 1.6); b.text("nur Isolatoren/Uebertrager ueberbruecken", XB0 + 3, 46, 1.6)
        flow(b, nv, XN0 + 2, XN1, 52); flow(b, br, XB0 + 2, XB1, 52); flow(b, hvt, XH0 + 2, XH1, 52)
for b in B.values(): b.schreiben()
# ---- Deckblatt
root.text("BMS-Platine BT-311 (Batteriemanagement-Steuerplatine), 160 x 100 mm, 4 Lagen (ENT-188, ENT-189, ENT-190), Kriechstrecke HV/NV 10 mm (ENT-191).", 12, 25, 2.2)
root.text("KI-generiert (Claude Sonnet, 2026-11-24), Entwurf, nicht freigegeben. Quelle: bms_skidl.py (wie das Layout). Passivwerte und Footprintgrößen sind offen/Platzhalter (siehe ERGEBNIS.md).", 12, 31, 1.6)
root.text("Blockübersicht: 12-V-Versorgung -> Rechner <-> CAN, Schützansteuerung (3 Kanäle, Hardware-UND Sekundärpfad); Rechner <-> Daisy-Master (Übertrager) zu den Zellüberwachungen; Rechner <- Strommessung HV (Shunt-ADC, Isolator).", 12, 37, 1.6)
root.text(f"HV/NV-Trennung: Rahmen auf den Blättern Daisy-Master mit Isolation und Strommessung HV-Seite; {ISO}.", 12, 43, 1.6)
order = ["versorgung", "rechner", "can", "schuetz", "daisy", "strom"]
for i, k in enumerate(order):
    sx, sy = sn(30 + 130 * (i % 2)), sn(60 + 38 * (i // 2)); b = B[k]
    hvmark = k in ("daisy", "strom")
    if hvmark: root.rahmen(sx - 4, sy - 4, sx + 108, sy + 28, "194 0 0", "dash", 0.3); root.text("enthält HV/NV-Trennung", sx + 64, sy - 1.5, 1.2)
    root.el.append(f'(sheet (at {sx} {sy}) (size 60.96 15.24) (exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no) (fields_autoplaced yes) (stroke (width 0.1524) (type solid)) (fill (color 0 0 0 0.0)) (uuid {q(b.sheet_uuid)})\n'
                   f'(property "Sheetname" {q(b.titel)} (at {sx} {sy - 1} 0) (effects (font (size 1.27 1.27)) (justify left bottom)))\n(property "Sheetfile" {q(b.datei)} (at {sx} {sy + 16.5} 0) (effects (font (size 1.27 1.27)) (justify left top)))\n'
                   f'(instances (project {q(PK)} (path {q("/" + ROOT)} (page {q(str(i + 2))}))))\n)')
root.schreiben()
json.dump({"blatt_von_ref": {t["ref"]: t["blatt"] for t in teile}, "anzahl_teile": len(teile), "alias": alias}, open(H / "schaltplan_zuordnung.json", "w"), indent=1)
print("geschrieben", len(teile), "Teile,", {k: sum(t["blatt"] == k for t in teile) for k in B})
