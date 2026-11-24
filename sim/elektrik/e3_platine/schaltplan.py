#!/usr/bin/env python3
"""E3 hierarchischer KiCad-Schaltplan (.kicad_sch) aus cmu_<V>_teile.json (derselbe Quelltext wie das Layout, cmu_skidl.py). KI-generiert (Claude Sonnet, 2026-11-24), Entwurf.
Blätter: Deckblatt, Kanäle (18 x Blatt Kanal), AFE und Versorgung, Sekundärschutz, Daisy-Chain, NTC und Stecker. Verbindung nur über Netznamen (globale Labels, im Kanalblatt hierarchische Labels).
Aufruf: python3 schaltplan.py  -> /home/cae/cae_projekte/batterie/e3/schaltplan_<V>/*.kicad_sch"""
import json, uuid, re, pathlib
H = pathlib.Path(__file__).resolve().parent; OUT = pathlib.Path("/home/cae/cae_projekte/batterie/e3")
U = lambda: str(uuid.uuid4())
sn = lambda x: round(round(x / 2.54) * 2.54, 4)   # Raster 2,54 mm
def q(s): return '"' + str(s).replace('"', "'") + '"'
FONT = "(effects (font (size 1.27 1.27)))"
HIERNETS = {"ABSCHALT", "TXA", "TXB", "RXA", "RXB", "NTC1", "NTC2", "NTC3", "NTC4"}   # Netze, die auf dem Deckblatt über Blattpins laufen
AKTE = {"R_2512": {"LFP": "ENT-171", "NMC": "ENT-172"}, "Filter_R": "ENT-181", "Filter_C": "ENT-182", "Doppel_NMOS_generisch": "ENT-192", "OVP6_generisch": "ENT-193, ENT-175/176/177",
        "AFE_generisch_18K": "BT-322 ENT-169", "Uebertrager_generisch": "ENT-174", "Daisy_Stecker": "ENT-183", "TVS_generisch": "ERW-E3 N2", "NTC_Eingang": "ERW-E3 N2", "FPC_24": "BT-320/321 ERW-E3", "Entkopplung": "ERW-E3 N2"}

class Sym:   # Bibliothekssymbol (eingebettet) aus Pinliste
    def __init__(self, name, pins, kind="box", prefix="U"):
        self.name, self.kind, self.prefix = name, kind, prefix; self.pins = {}   # num -> (name, x, y, winkel)
        if kind in ("R", "C", "D"):
            self.w, self.h = 2.54, 5.08; (n1, p1), (n2, p2) = pins
            self.pins[p1] = (n1, 0, 5.08, 270); self.pins[p2] = (n2, 0, -5.08, 90)
        else:
            L = [p for p in pins if p[2] == "L"]; Rr = [p for p in pins if p[2] == "R"]; n = max(len(L), len(Rr), 2)
            self.h = 2 * 2.54 * -(-(n + 1) // 2); self.w = 15.24
            for i, (nm, num, s) in enumerate(L): self.pins[num] = (nm, -(self.w / 2 + 5.08), self.h / 2 - 2.54 * (i + 1), 0)
            for i, (nm, num, s) in enumerate(Rr): self.pins[num] = (nm, self.w / 2 + 5.08, self.h / 2 - 2.54 * (i + 1), 180)
    def lib(self):
        w, h = self.w, self.h; nm = "cmu:" + self.name
        body = {"R": f'(rectangle (start -1.016 -2.54) (end 1.016 2.54) (stroke (width 0.254) (type default)) (fill (type none)))',
                "C": '(polyline (pts (xy 0 2.54) (xy 0 0.762)) (stroke (width 0.254) (type default)) (fill (type none))) (polyline (pts (xy 0 -2.54) (xy 0 -0.762)) (stroke (width 0.254) (type default)) (fill (type none))) (polyline (pts (xy -2.032 0.762) (xy 2.032 0.762)) (stroke (width 0.508) (type default)) (fill (type none))) (polyline (pts (xy -2.032 -0.762) (xy 2.032 -0.762)) (stroke (width 0.508) (type default)) (fill (type none)))',
                "D": '(polyline (pts (xy -1.27 1.27) (xy 1.27 1.27) (xy 0 -1.27) (xy -1.27 1.27)) (stroke (width 0.254) (type default)) (fill (type none))) (polyline (pts (xy -1.27 -1.27) (xy 1.27 -1.27)) (stroke (width 0.254) (type default)) (fill (type none)))'}.get(self.kind,
                f'(rectangle (start {-w/2} {-h/2}) (end {w/2} {h/2}) (stroke (width 0.254) (type default)) (fill (type background)))')
        ps = "\n".join(f'    (pin passive line (at {x} {y} {a}) (length 2.54) (name {q(n)} (effects (font (size 1.0 1.0)))) (number {q(num)} (effects (font (size 1.0 1.0)))))' for num, (n, x, y, a) in self.pins.items())
        if self.kind in ("R", "C", "D"):   # Pinlänge: Pinende bei +-7.62, Pin zeigt zum Körper: Anschlusspunkt = (x, y)
            pass
        return f'''  (symbol {q(nm)} (pin_names (offset 0.5) hide) (exclude_from_sim no) (in_bom yes) (on_board yes)
    (property "Reference" {q(self.prefix)} (at 0 {h/2+2} 0) {FONT})
    (property "Value" "" (at 0 {-h/2-2} 0) {FONT})
    (property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
    (property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
    (symbol {q(self.name + "_0_1")} {body})
    (symbol {q(self.name + "_1_1")}
{ps}
    )
  )'''

def build(V):
    d = json.load(open(H / f"cmu_{V}_teile.json")); teile = d["teile"]; ROOT = U(); pk = f"cmu_{V}"
    kan = 18; by = {}
    for t in teile: by.setdefault(t["name"], []).append(t)
    netsof = lambda t: {n for n in t["pins"].values() if n}
    def san(n): return re.sub(r"[^A-Za-z0-9_+-]", "_", n)
    SYMS = {}
    def symfor(t, kind=None, prefix=None):
        key = (t["name"], t["footprint"] if t["name"] in ("R", "C") else "", kind)
        if key in SYMS: return SYMS[key]
        pn = [(t["pinnamen"][n], n) for n in sorted(t["pins"], key=int)]
        if kind in ("R", "C", "D"): s = Sym(t["name"] + ("_2512" if "2512" in t["footprint"] else ""), [(pn[0][0], pn[0][1]), (pn[1][0], pn[1][1])], kind, prefix)
        else:
            def side(nm):
                if t["name"].startswith("AFE"): return "L" if re.match(r"^(S\d+|G\d+)$", nm) else "R"
                if t["name"] == "Doppel_NMOS_generisch": return "L" if nm in ("G1", "S1", "D2") else "R"
                if t["name"] == "OVP6_generisch": return "L" if nm.startswith("IN") else "R"
                if t["name"] == "Uebertrager_generisch": return "L" if nm in ("P1", "P2") else "R"
                if t["name"] == "FPC_24": return "R"
                if t["name"] == "NTC_Eingang" or t["name"] == "Daisy_Stecker": return "L"
                if t["name"] == "TVS_generisch": return "L" if nm in ("1", "A") else "R"
                return "L"
            pl = [(nm, num, side(nm)) for nm, num in pn]
            if t["name"] == "Doppel_NMOS_generisch":
                o = ["D1", "G1", "G2", "S2", "S1", "D2"]; pl = sorted(pl, key=lambda p: o.index(p[0])); pl = [(nm, num, "L" if nm in o[:3] else "R") for nm, num, _ in pl]
            s = Sym(t["name"], pl, "box", prefix or "U")
        SYMS[key] = s; return s
    def akte(t):
        if t["name"] == "R": return AKTE["R_2512"][V] if "2512" in t["footprint"] else AKTE["Filter_R"]
        if t["name"] == "C": return AKTE["Entkopplung"] if "Entkopplung" in t["value"] else AKTE["Filter_C"]
        return AKTE.get(t["name"], "ERW-E3")
    class Blatt:
        def __init__(s, titel, datei, seite, papier="A3"): s.titel, s.datei, s.seite, s.papier = titel, datei, seite, papier; s.el = []; s.libs = {}; s.uuid = U() if datei != f"{pk}.kicad_sch" else ROOT
        def label(s, name, x, y, ang, art="global", form="passive"):
            j = {0: "left", 180: "right"}.get(ang, "left")
            s.__dict__.setdefault("hier", set())
            if art == "global" and name in HIERNETS: art = "hier"
            if art == "hier": s.hier.add(name)
            if art == "global": s.el.append(f'(global_label {q(name)} (shape {form}) (at {x} {y} {ang}) (fields_autoplaced yes) (effects (font (size 1.27 1.27)) (justify {j})) (uuid {q(U())}) (property "Intersheetrefs" "${{INTERSHEET_REFS}}" (at {x} {y} 0) (effects (font (size 1.27 1.27)) hide)))')
            elif art == "hier": s.el.append(f'(hierarchical_label {q(name)} (shape bidirectional) (at {x} {y} {ang}) (effects (font (size 1.27 1.27)) (justify {j})) (uuid {q(U())}))')
            else: s.el.append(f'(label {q(name)} (at {x} {y} {ang}) (effects (font (size 1.27 1.27)) (justify {j} bottom)) (uuid {q(U())}))')
        def wire(s, *pts):
            for (x1, y1), (x2, y2) in zip(pts, pts[1:]): s.el.append(f'(wire (pts (xy {x1} {y1}) (xy {x2} {y2})) (stroke (width 0) (type default)) (uuid {q(U())}))')
        def junc(s, x, y): s.el.append(f'(junction (at {x} {y}) (diameter 0) (color 0 0 0 0) (uuid {q(U())}))')
        def text(s, txt, x, y, gr=1.8): s.el.append(f'(text {q(txt)} (exclude_from_sim no) (at {x} {y} 0) (effects (font (size {gr} {gr})) (justify left)) (uuid {q(U())}))')
        def teil(s, t, sym, cx, cy, netname, instances, art="global", akt=None, anz_ref=True, noconn=True, skip=()):
            """Symbol setzen; Pins bekommen Labels (netname(pinnummer) -> Name, ang). instances: Liste (pfad, ref)."""
            cx, cy = sn(cx), sn(cy)
            s.libs[sym.name] = sym
            ins = "".join(f'(path {q(p)} (reference {q(r)}) (unit 1))' for p, r in instances)
            bx = sym.kind == "box"; rx, ry = (cx, cy - sym.h / 2 - 3.0) if bx else (cx + sym.w / 2 + 1.5, cy - 1.5); vx, vy = (cx, cy + sym.h / 2 + 2.0) if bx else (cx + sym.w / 2 + 1.5, cy + 0.5); ax_, ay_ = (cx, cy + sym.h / 2 + 4.0) if bx else (cx + sym.w / 2 + 1.5, cy + 2.5)
            jj = "" if bx else " (justify left)"
            props = f'(property "Reference" {q(instances[0][1])} (at {rx} {ry} 0) (effects (font (size 1.27 1.27)){jj}))\n' \
                    f'(property "Value" {q(t["value"].split(" (")[0][:24])} (at {vx} {vy} 0) (effects (font (size 1.0 1.0)){jj}))\n' \
                    f'(property "Footprint" {q(t["footprint"])} (at {cx} {cy} 0) (effects (font (size 1.27 1.27)) hide))\n' \
                    f'(property "Datasheet" "" (at {cx} {cy} 0) (effects (font (size 1.27 1.27)) hide))\n' \
                    f'(property "Akte" {q(akt or akte(t))} (at {ax_} {ay_} 0) (effects (font (size 1.0 1.0)){jj}))'
            pins = "".join(f'(pin {q(n)} (uuid {q(U())}))' for n in sym.pins)
            s.el.append(f'(symbol (lib_id {q("cmu:" + sym.name)}) (at {cx} {cy} 0) (unit 1) (exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no) (fields_autoplaced yes) (uuid {q(U())})\n{props}\n{pins}\n(instances (project {q(pk)} {ins})))')
            for num, (nm, px, py, a) in sym.pins.items():
                net = netname(num)
                if num in skip: continue
                if net: s.label(net, cx + px, cy - py, 180 if a == 0 else 0 if a == 180 else 0, art)   # Label am Pinende, Text weg vom Symbol
                elif noconn: s.el.append(f'(no_connect (at {cx + px} {cy - py}) (uuid {q(U())}))')
        def schreiben(s, pfad, extra=""):
            lib = "\n".join(y.lib() for y in s.libs.values())
            tb = f'(title_block (title {q(s.titel + " (" + V + ")")}) (date "2026-11-24") (rev "0.1") (company "KI-generiert, Entwurf") (comment 1 "Dok.-Nr. SCH-E3-{V}, Version 0.1, Status Entwurf") (comment 2 "KI-generiert (Claude Sonnet, 2026-11-24), nicht freigegeben, Prüfer Opus offen") (comment 3 "Quelle: sim/elektrik/e3_platine/cmu_skidl.py -> cmu_{V}_teile.json, Akten ENT-163..193"))'
            body = "\n".join(s.el)
            txt = f'(kicad_sch (version 20250114) (generator "eeschema") (generator_version "10.0") (uuid {q(s.uuid)}) (paper {q(s.papier)})\n{tb}\n(lib_symbols\n{lib}\n)\n{body}\n(embedded_fonts no)\n)\n'
            (pfad / s.datei).write_text(txt)
    ordner = OUT / f"schaltplan_{V}"; ordner.mkdir(exist_ok=True)
    for f in ordner.glob("*.kicad_sch"): f.unlink()
    seiten = iter(range(1, 100))
    root = Blatt("Deckblatt", f"{pk}.kicad_sch", next(seiten), "A3")
    kanaele = Blatt("Kanäle (18 x Blatt Kanal)", "kanaele.kicad_sch", next(seiten)); kanal = Blatt("Kanal", "kanal.kicad_sch", 0, "A4")
    afe = Blatt("AFE und Versorgung", "afe.kicad_sch", 0); ovp = Blatt("Sekundärschutz 3 x 6 Zellen", "sekundaerschutz.kicad_sch", 0)
    dc = Blatt("Daisy-Chain", "daisy.kicad_sch", 0); ntc = Blatt("NTC und Stecker", "ntc_stecker.kicad_sch", 0)
    # ---- Teilezuordnung
    R = by["R"]; C = by["C"]; fets = {int([n for n in t["pins"].values() if n.startswith("G")][0][1:]): t for t in by["Doppel_NMOS_generisch"]}
    ch = {k: {} for k in range(1, kan + 1)}; r0 = None; entk = []
    for t in R:
        nn = netsof(t)
        if "2512" in t["footprint"]:
            k = int([n for n in nn if n.startswith("D")][0][1:]); ch[k].setdefault("rb", []).append(t)
        else:
            k = int([n for n in nn if n.startswith("T")][0][1:])
            if k == 0: r0 = t
            else: ch[k]["rf"] = t
    for t in C:
        nn = [n for n in t["pins"].values() if n]
        if nn[0].startswith("S"): ch[int(nn[0][1:])]["c"] = t
        else: entk.append(t)
    for k in ch: ch[k]["q"] = fets[k]; assert len(ch[k]["rb"]) == 2 and "rf" in ch[k] and "c" in ch[k], k
    # ---- Pfade
    kan_sheet_in_root = U(); kanal_inst = {k: U() for k in range(1, kan + 1)}; pg = {}
    afe.uuid_in_root, ovp.uuid_in_root, dc.uuid_in_root, ntc.uuid_in_root = U(), U(), U(), U()
    pr = f"/{ROOT}"; pk_ = lambda k: f"{pr}/{kan_sheet_in_root}/{kanal_inst[k]}"
    # ---- Kanalblatt (einmal gezeichnet), lokale Netze TH TL SH SL G H D M
    tk = ch[1]; inst = lambda key, idx=None: [(pk_(k), (ch[k][key][idx] if idx is not None else ch[k][key])["ref"]) for k in ch]
    sR = symfor(tk["rb"][0], "R", "R"); sRf = symfor(tk["rf"], "R", "R"); sC = symfor(tk["c"], "C", "C"); sQ = symfor(tk["q"], "box", "Q")
    # Pins: R: pin1 oben, pin2 unten (Anschluss bei y=+-7.62: Label am Pinende)
    def nm_rb(num): return "TH" if num == "1" else "D"
    kanal.teil(tk["rf"], sRf, 50.8, 60.96, lambda n: "TH" if n == "1" else "SH", inst("rf"), "hier") if False else None
    def lab(s, t, sym, cx, cy, mapping, instances, art_of=lambda n: "local"):
        cx, cy = sn(cx), sn(cy); s.libs[sym.name] = sym; s.teil(t, sym, cx, cy, lambda num: None, instances, noconn=False)
        for num, (nm, px, py, a) in sym.pins.items():
            net = mapping[num]; hier = net in ("TH", "TL", "SH", "SL", "G", "H")
            s.label(net, cx + px, cy - py, 180 if a == 0 else 0 if a == 180 else 0, "hier" if hier else "local")
    # Platzierung (A3 420 x 297): Filter-R oben links, C, 2 Rb, FET
    kanal.text("Kanal: Filter-RC am Abgriff, zwei Ausgleichswiderstände parallel, Doppel-N-FET mit zwei Schaltern in Reihe (ENT-192). Dieses Blatt wird 18-mal verwendet.", 12.7, 20.32, 1.4)
    for t_, sy_, cx_, cy_, ins_ in ((tk["rf"], sRf, 60.96, 60.96, inst("rf")), (tk["rb"][0], sR, 127, 60.96, inst("rb", 0)), (tk["rb"][1], sR, 147.32, 60.96, inst("rb", 1)), (tk["c"], sC, 76.2, 81.28, inst("c")), (tk["q"], sQ, 190.5, 76.2, inst("q"))):
        kanal.libs[sy_.name] = sy_; kanal.teil(t_, sy_, cx_, cy_, lambda num: None, ins_, noconn=False)
    K = kanal; K.label("TH", 25.4, 45.72, 180, "hier")
    K.wire((25.4, 45.72), (147.32, 45.72)); K.wire((60.96, 45.72), (60.96, 55.88)); K.wire((127, 45.72), (127, 55.88)); K.wire((147.32, 45.72), (147.32, 55.88))
    K.junc(60.96, 45.72); K.junc(127, 45.72)
    K.wire((60.96, 66.04), (60.96, 71.12), (101.6, 71.12)); K.wire((76.2, 71.12), (76.2, 76.2)); K.junc(76.2, 71.12); K.label("SH", 101.6, 71.12, 0, "hier")
    K.wire((76.2, 86.36), (76.2, 91.44), (101.6, 91.44)); K.label("SL", 101.6, 91.44, 0, "hier")
    K.wire((127, 66.04), (127, 73.66), (177.8, 73.66)); K.wire((147.32, 66.04), (147.32, 73.66)); K.junc(147.32, 73.66)
    K.wire((177.8, 76.2), (165.1, 76.2)); K.label("G", 165.1, 76.2, 180, "hier"); K.wire((177.8, 78.74), (165.1, 78.74)); K.label("H", 165.1, 78.74, 180, "hier")
    K.wire((203.2, 73.66), (228.6, 73.66)); K.label("TL", 228.6, 73.66, 0, "hier")
    K.wire((203.2, 76.2), (210.82, 76.2), (210.82, 78.74), (203.2, 78.74))
    K.text("Filter-RC: Abgriff -> Filter-R -> AFE-Eingang SH, Kondensator gegen SL", 40, 38, 1.4); K.text("Ausgleich: Abgriff -> 2 Widerstände parallel -> Doppel-FET (2 Schalter in Reihe) -> Abgriff n-1 (TL)", 100, 38, 1.4) if False else None
    K.text("Ausgleich: Abgriff -> 2 Widerstände parallel -> Doppel-FET, 2 Schalter in Reihe (ENT-192) -> Abgriff n-1 (TL)", 112, 100, 1.4)
    K.text("TH = Abgriff dieses Kanals, TL = Abgriff darunter, SH/SL = Messeingänge, G/H = Gates vom AFE", 40, 125, 1.27)
    # ---- Kanäle-Blatt: 18 Blattsymbole mit Sheet-Pins und globalen Labels
    kanaele.text("18 Messkanäle: je ein Blatt Kanal; die Pins hängen an den globalen Netzen T, S, G, H (AFE, Sekundärschutz, Stecker).", 25.4, 25.4)
    pins6 = [("TH", 0, 0), ("TL", 0, 1), ("SH", 0, 2), ("SL", 0, 3), ("G", 0, 4), ("H", 0, 5)]
    for k in range(1, kan + 1):
        col, row = (k - 1) % 3, (k - 1) // 3; sx, sy = sn(40 + 130 * col), sn(35 + 33 * row); w, h = 50.8, 22.86
        sp = []
        for nm, side, i in pins6:
            y = sy + 5.08 + 2.54 * i - (0 if i < 6 else 0); sp.append(f'(pin {q(nm)} bidirectional (at {sx} {y} 180) (uuid {q(U())}) (effects (font (size 1.27 1.27)) (justify left)))')
        glob = {"TH": f"T{k}", "TL": f"T{k-1}", "SH": f"S{k}", "SL": f"S{k-1}", "G": f"G{k}", "H": f"H{k}"}
        for nm, side, i in pins6: kanaele.label(glob[nm], sx, sy + 5.08 + 2.54 * i, 180, "global")
        kanaele.el.append(f'(sheet (at {sx} {sy}) (size {w} {h}) (exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no) (fields_autoplaced yes) (stroke (width 0.1524) (type solid)) (fill (color 0 0 0 0.0)) (uuid {q(kanal_inst[k])})\n'
                           f'(property "Sheetname" {q(f"Kanal {k}")} (at {sx} {sy - 1} 0) (effects (font (size 1.27 1.27)) (justify left bottom)))\n(property "Sheetfile" "kanal.kicad_sch" (at {sx} {sy + h + 1} 0) (effects (font (size 1.27 1.27)) (justify left top)))\n'
                           + "\n".join(sp) + f'\n(instances (project {q(pk)} (path {q(pr + "/" + kan_sheet_in_root)} (page {q(str(100 + k))}))))\n)')
    # ---- AFE-Blatt
    a = by["AFE_generisch_18K"][0]; sA = symfor(a, "box", "U"); net_of = lambda t: (lambda num: san(t["pins"][num]) if t["pins"].get(num) else None)
    def netname_auto(t):
        # unbenannte SKiDL-Netze (N$..) bekommen den Pinnamen des AFE als Netzname (nur Darstellung)
        def f(num):
            n = t["pins"].get(num)
            if not n: return None
            return n
        return f
    # Netznamen global eindeutig machen: N$ -> Pinname der AFE-Seite, sonst N<nr>
    alias = {}
    for t in teile:
        for num, n in t["pins"].items():
            if n and n.startswith("N$") and t["name"] == "AFE_generisch_18K": alias[n] = t["pinnamen"][num]
    ncount = [0]
    def net(n):
        if n is None: return None
        if n in alias: return alias[n]
        if n.startswith("N$"): alias[n] = "DC" + n[2:]; return alias[n]
        return n
    # AFE ist die Quelle der Aliase: zuerst alle AFE-Pins durchgehen
    afe_inst = [(f"{pr}/{afe.uuid_in_root}", a["ref"])]
    afe.teil(a, sA, 150, 148.5, lambda num: net(a["pins"].get(num)), afe_inst, skip=("1", "56", "57", "58", "59", "60"))
    Ax, Ay = sn(150), sn(148.5); pp = lambda n: (round(Ax + sA.pins[n][1], 4), round(Ay - sA.pins[n][2], 4))
    afe.text("AFE generisch, 18 Kanäle, ASIL-D-fähig (BT-322, ENT-169); zweiter Gate-Ausgang H je Kanal generisch (ENT-192). Versorgung 4 x 100 nF, Filter-R des Abgriffs T0.", 25.4, 20)
    ai = [(f"{pr}/{afe.uuid_in_root}", "")]
    # Filter-R des Abgriffs T0: T0 -> R1 -> Eingang S0
    sR1 = symfor(r0, "R", "R"); s0x, s0y = pp("1"); rx, ry = sn(s0x - 25.4), sn(s0y - 10.16)
    afe.teil(r0, sR1, rx, ry, lambda num: None, [(f"{pr}/{afe.uuid_in_root}", r0["ref"])], noconn=False)
    afe.wire((rx, ry + 5.08), (rx, s0y), (s0x, s0y)); afe.label("T0", rx, ry - 5.08, 180, "global")
    afe.wire((rx + 7.62, s0y), (rx + 7.62, s0y - 5.08)); afe.junc(rx + 7.62, s0y); afe.label("S0", rx + 7.62, s0y - 5.08, 0, "global")
    # Versorgung: 4 VCC-Pins verbunden, 4 Entkopplungs-C an VCC und GND
    vx, v1 = pp("56"); v4 = pp("59")[1]; gx, gy = pp("60")
    afe.wire((vx, v1), (vx, v4)); afe.junc(vx, pp("57")[1]); afe.junc(vx, pp("58")[1]); xs = [sn(vx + 20.32 + 12.7 * i) for i in range(len(entk))]
    afe.wire((vx, v1), (xs[-1], v1)); afe.wire((gx, gy), (xs[-1], gy))
    for i, t in enumerate(entk):
        afe.teil(t, symfor(t, "C", "C"), xs[i], v1 + 5.08, lambda num: None, [(f"{pr}/{afe.uuid_in_root}", t["ref"])], noconn=False)
        afe.junc(xs[i], v1); afe.junc(xs[i], gy) if i < len(entk) - 1 else None
    afe.wire((xs[-1], gy), (xs[-1], gy)) if False else None
    afe.label("VCC", xs[-1] + 5.08, v1, 0, "global"); afe.wire((xs[-1], v1), (xs[-1] + 5.08, v1)); afe.label("GND", xs[-1] + 5.08, gy, 0, "global"); afe.wire((xs[-1], gy), (xs[-1] + 5.08, gy))
    # ---- Sekundärschutz
    ovp.text("3 x generischer 6-Zellen-Überspannungsschutz (je 7 Messeingänge an den T-Netzen), Ausgänge wired-OR auf ABSCHALT (FSR-06). Schwelle je Zelle (ENT-175/176), Verzögerung ENT-177, Bauform ENT-193.", 25.4, 20)
    ou = sorted(by["OVP6_generisch"], key=lambda x: x["ref"]); sO = symfor(ou[0], "box", "U"); ocx = [sn(100 + 80 * i) for i in range(3)]; ocy = sn(100)
    for i, t in enumerate(ou): ovp.teil(t, sO if t is ou[0] else symfor(t, "box", "U"), ocx[i], ocy, lambda num, t=t: net(t["pins"].get(num)), [(f"{pr}/{ovp.uuid_in_root}", t["ref"])], skip=("8", "9"))
    pa = lambda i, n: (round(ocx[i] + sO.pins[n][1], 4), round(ocy - sO.pins[n][2], 4)); yb, yg = ocy - sO.h / 2 - 10.16, ocy + sO.h / 2 + 10.16
    for i in range(3):
        x8, y8 = pa(i, "8"); x9, y9 = pa(i, "9")
        ovp.wire((x8, y8), (x8 + 5.08, y8), (x8 + 5.08, yb)); ovp.wire((x9, y9), (x9 + 7.62, y9), (x9 + 7.62, yg))
        if i: ovp.junc(x8 + 5.08, yb) if i < 2 else None; ovp.junc(x9 + 7.62, yg) if i < 2 else None
    ovp.wire((pa(0, "8")[0] + 5.08, yb), (pa(2, "8")[0] + 5.08, yb)); ovp.wire((pa(0, "9")[0] + 7.62, yg), (pa(2, "9")[0] + 7.62, yg))
    ovp.junc(pa(1, "8")[0] + 5.08, yb); ovp.junc(pa(1, "9")[0] + 7.62, yg)
    ovp.label("ABSCHALT", pa(2, "8")[0] + 5.08, yb, 0, "global"); ovp.wire((pa(2, "8")[0] + 5.08, yb), (pa(2, "8")[0] + 10.16, yb)) if False else None
    ovp.label("GND", pa(2, "9")[0] + 7.62, yg, 0, "global")
    ovp.text("Ausgänge wired-OR: jeder Schutz zieht ABSCHALT; GND gemeinsam", 25.4, yb - 7.62, 1.4)
    # ---- Daisy
    dc.text("Daisy-Chain: 2 Übertrager (1,5 kV Prüfspannung, ENT-174), 2 Stecker 2-polig, 2 TVS. Kriechstrecke Trennstelle 2,5 mm (ENT-183).", 25.4, 20)
    Ts = sorted(by["Uebertrager_generisch"], key=lambda x: x["ref"]); Js = sorted(by["Daisy_Stecker"], key=lambda x: x["ref"]); Ds = sorted(by["TVS_generisch"], key=lambda x: x["ref"])
    for i in range(2):
        cy = sn(80 + 80 * i); tx, jx, dx_ = sn(70), sn(190), sn(150)
        dc.teil(Ts[i], symfor(Ts[i], "box", "T"), tx, cy, lambda num, t=Ts[i]: net(t["pins"].get(num)), [(f"{pr}/{dc.uuid_in_root}", Ts[i]["ref"])], skip=("3", "4"))
        dc.teil(Js[i], symfor(Js[i], "box", "J"), jx, cy, lambda num: None, [(f"{pr}/{dc.uuid_in_root}", Js[i]["ref"])], noconn=False)
        sT, sJ = symfor(Ts[i], "box", "T"), symfor(Js[i], "box", "J")
        ya = cy - sT.pins["3"][2]; yb_ = cy - sT.pins["4"][2]; xe = tx + sT.pins["3"][1]; xj = jx + sJ.pins["1"][1]
        dc.wire((xe, ya), (xj, ya)); dc.wire((xe, yb_), (xj, yb_))
        sD = symfor(Ds[i], "D", "D"); dcy = yb_ + 12.7
        dc.teil(Ds[i], sD, dx_, dcy, lambda num: None, [(f"{pr}/{dc.uuid_in_root}", Ds[i]["ref"])], noconn=False)
        dc.wire((dx_, ya), (dx_, dcy - 5.08)); dc.junc(dx_, ya)
        dc.wire((dx_, dcy + 5.08), (dx_ + 7.62, dcy + 5.08), (dx_ + 7.62, yb_)); dc.junc(dx_ + 7.62, yb_)
    # ---- NTC und Stecker
    ntc.text("Zellabgriff-Stecker J1 (24-polig, T0..T18, ABSCHALT, GND) und 4 externe NTC-Eingänge (2-polig).", 25.4, 20)
    j1 = by["FPC_24"][0]; ntc.teil(j1, symfor(j1, "box", "J"), 100, 150, lambda num: net(j1["pins"].get(num)), [(f"{pr}/{ntc.uuid_in_root}", j1["ref"])])
    for i, t in enumerate(sorted(by["NTC_Eingang"], key=lambda x: x["ref"])): ntc.teil(t, symfor(t, "box", "J"), 250, 60 + 40 * i, lambda num, t=t: net(t["pins"].get(num)), [(f"{pr}/{ntc.uuid_in_root}", t["ref"])])
    # ---- Deckblatt
    root.text("CMU-Platine BT-321, 120 x 60 mm, 18 Zellen, passiver Ausgleich. KI-generiert (Claude Sonnet, 2026-11-24), Entwurf, nicht freigegeben.", 25.4, 20, 2.5)
    root.text("Blockübersicht: Zellabgriff-Stecker J1 -> Kanäle (Filter, Ausgleich) -> AFE (Messung, Gates) -> Daisy-Chain; Sekundärschutz (3 x 6 Zellen) -> ABSCHALT.", 25.4, 30)
    root.text(f"Akten: Widerstand {AKTE['R_2512'][V]}, Filter ENT-181/182, Doppel-FET ENT-192, Sekundärschutz ENT-193/175/176/177, AFE ENT-169, Übertrager ENT-174, Daisy ENT-183, Kriechstrecke ENT-168, Thermovias ENT-187.", 25.4, 36)
    root.text("Die Zellabgriffe T0..T18, Messeingänge S0..S18 und Gates G/H der 18 Kanäle laufen über globale Netznamen zwischen den Blättern (Kanäle, AFE, Sekundärschutz, Stecker).", 25.4, 42)
    def blatt_el(nm, b, uid, sx, sy, w, pins_l, pins_r, seite):
        h = 2.54 * max(len(pins_l), len(pins_r), 2) + 10.16; sp = []
        for k_, p_ in enumerate(pins_l): sp.append(f'(pin {q(p_)} bidirectional (at {sx} {sy + 5.08 + 2.54 * k_} 180) (uuid {q(U())}) (effects (font (size 1.27 1.27)) (justify left)))')
        for k_, p_ in enumerate(pins_r): sp.append(f'(pin {q(p_)} bidirectional (at {sx + w} {sy + 5.08 + 2.54 * k_} 0) (uuid {q(U())}) (effects (font (size 1.27 1.27)) (justify right)))')
        root.el.append(f'(sheet (at {sx} {sy}) (size {w} {h}) (exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no) (fields_autoplaced yes) (stroke (width 0.1524) (type solid)) (fill (color 0 0 0 0.0)) (uuid {q(uid)})\n'
                       f'(property "Sheetname" {q(nm)} (at {sx} {sy - 1} 0) (effects (font (size 1.27 1.27)) (justify left bottom)))\n(property "Sheetfile" {q(b.datei)} (at {sx} {sy + h + 1} 0) (effects (font (size 1.27 1.27)) (justify left top)))\n' + "\n".join(sp) + f'\n(instances (project {q(pk)} (path {q(pr)} (page {q(str(seite))}))))\n)')
    hs = lambda b: sorted(b.hier)
    sxA = sn(160); wA = 50.8; sxN = sn(40); wN = 50.8; sxD = sn(300); sy0 = sn(100)
    ntcp = ["ABSCHALT", "NTC1", "NTC2", "NTC3", "NTC4"]; afel = ntcp; afer = ["RXA", "RXB", "TXA", "TXB"]
    assert set(hs(ntc)) == set(ntcp), hs(ntc); assert set(hs(afe)) == set(afel + afer), hs(afe); assert set(hs(dc)) == set(afer), hs(dc); assert hs(ovp) == ["ABSCHALT"], hs(ovp)
    blatt_el("NTC und Stecker", ntc, ntc.uuid_in_root, sxN, sy0, wN, [], ntcp, 6)
    blatt_el("AFE und Versorgung", afe, afe.uuid_in_root, sxA, sy0, wA, afel, afer, 3)
    blatt_el("Daisy-Chain", dc, dc.uuid_in_root, sxD, sy0, wN, afer, [], 5)
    blatt_el("Sekundärschutz", ovp, ovp.uuid_in_root, sxN, sn(50), wN, [], ["ABSCHALT"], 4)
    blatt_el("Kanäle", kanaele, kan_sheet_in_root, sxA, sn(180), wA, [], [], 2)
    for k_ in range(5): root.wire((sxN + wN, sy0 + 5.08 + 2.54 * k_), (sxA, sy0 + 5.08 + 2.54 * k_))
    for k_ in range(4): root.wire((sxA + wA, sy0 + 5.08 + 2.54 * k_), (sxD, sy0 + 5.08 + 2.54 * k_))
    jx_ = sn(120); root.wire((sxN + wN, sn(50) + 5.08), (jx_, sn(50) + 5.08), (jx_, sy0 + 5.08)); root.junc(jx_, sy0 + 5.08)
    root.text("ABSCHALT (wired-OR aus Sekundärschutz und AFE)", jx_ - 38, sy0 + 3.2, 1.0); root.text("Daisy-Chain TX/RX zum Nachbarmodul", sxA + wA + 4, sy0 - 3, 1.0)
    for b in (root, kanaele, kanal, afe, ovp, dc, ntc): b.schreiben(ordner)
    # kanaele.kicad_sch ist Unterblatt von root: die Seitenzahlen der 18 Kanalinstanzen stehen oben (100+k)
    return d
if __name__ == "__main__":
    for V in ("LFP", "NMC"): build(V); print(V, "geschrieben")
