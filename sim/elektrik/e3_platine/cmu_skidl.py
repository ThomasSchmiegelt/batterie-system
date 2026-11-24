#!/usr/bin/env python3
"""E3 CMU-Schaltplan als Code (SKiDL). KI-generiert (Claude Sonnet, 2026-11-24), Entwurf.
Werte aus den ENT-Akten (Status entschieden ODER vorgeschlagen, je Variante), sonst A_* mit Herkunft ERW-E3.
Ausgabe je Variante: cmu_<V>.net (KiCad-Netzliste), cmu_<V>_bom.csv, cmu_<V>_teile.json (Teile + Netze fürs Layout), cmu_<V>_erc.txt.
Aufruf: source umgebung.sh; python3 cmu_skidl.py"""
import re, json, csv, sys, pathlib, io, contextlib
H = pathlib.Path(__file__).resolve().parent; ROOT = H.parents[2]
# Annahmen Opus, Herkunft ERW-E3 N2 (Auftrag E3 Routing): je AFE-Versorgungspin 100 nF, 1 TVS je Daisy-Chain-Stecker (Eingang, Ausgang), Daisy-Stecker 2-polig (nur Daten, N3: GND/VCC entfernt)
A_VCC_PINS = 4; A_C_ENTK_NF = 100.0; A_TVS_JE_STECKER = 1

def akten():
    """merkmal-Werte je (BT, merkmal, variante) aus pm/entscheidungen, nur Status entschieden/vorgeschlagen."""
    d = {}
    for f in sorted((ROOT / "pm/entscheidungen").glob("ENT-*.md")):
        t = f.read_text(); m = re.match(r"---\n(.*?)\n---", t, re.S)
        if not m: continue
        y = {}
        for z in m.group(1).splitlines():
            k, _, v = z.partition(":"); y[k.strip()] = re.sub(r"\s+#.*$", "", v).strip()
        if not (y.get("status", "").startswith(("entschieden", "vorgeschlagen"))): continue
        w = y.get("wert", "").strip('"')
        try: w = float(w)
        except ValueError: pass
        var = re.findall(r"[A-Z]+", y.get("variante", "")) if y.get("variante", "null") != "null" else [None]
        for bt in re.findall(r"BT-\d+", y.get("bauteile", "")):
            for v in var: d[(bt, y.get("merkmal"), v)] = (w, y["id"])
    return d
AK = akten()
def wert(bt, m, v, default=None):
    for key in ((bt, m, v), (bt, m, None)):
        if key in AK: return AK[key]
    if default is None: sys.exit(f"Wert fehlt: {bt} {m} {v}")
    return (default, "A_*: ERW-E3")

def bauen(v):
    from skidl import Part, Net, Pin, TEMPLATE, SKIDL, generate_netlist, ERC, reset, KICAD9, SchLib
    reset()
    herk = {}
    def W(bt, m, default=None):
        w, h = wert(bt, m, v, default); herk[f"{bt}.{m}"] = f"{w} ({h})"; return w
    Rw = W("BT-323", "widerstand_Ohm"); kan = int(W("BT-322", "kanaele")); Rf = W("BT-323", "filter_R_Ohm"); Cf = W("BT-323", "filter_C_nF")
    R_je = {"LFP": 47, "NMC": 64.9}[v]  # Einzelwert E96/E24 aus Akten-Titel (ENT-171/172): 2 parallel = widerstand_Ohm
    assert abs(R_je / 2 - Rw) < 0.01, (R_je, Rw)
    herk.update(A_VCC_PINS=f"{A_VCC_PINS} (A_*, ERW-E3 N2)", A_C_ENTK_NF=f"{A_C_ENTK_NF} (A_*, ERW-E3 N2)", A_TVS_JE_STECKER=f"{A_TVS_JE_STECKER} (A_*, ERW-E3 N2)")
    herk["R_Einzel_Ohm"] = f"{R_je} (Titel ENT-171/172, 2 parallel = {Rw})"
    for m, bt in (("kriechstrecke_mm", "BT-321"), ("kriechstrecke_daisy_mm", "BT-321"), ("schwelle_V", "BT-325"), ("verzoegerung_ms", "BT-325"), ("pruefspannung_V", "BT-324"), ("bauform", "BT-325")): W(bt, m)
    fp = dict(R_2512="Resistor_SMD:R_2512_6332Metric", R_0603="Resistor_SMD:R_0603_1608Metric", C_0603="Capacitor_SMD:C_0603_1608Metric",
              SOT23="Package_TO_SOT_SMD:SOT-23", QFP="Package_QFP:LQFP-80_12x12mm_P0.5mm", SOIC16="Package_SO:SOIC-16W_7.5x10.3mm_P1.27mm",
              SOT363="Package_TO_SOT_SMD:SOT-363_SC-70-6", TSSOP16="Package_SO:TSSOP-16_4.4x5mm_P0.65mm", FPC="Connector_FFC-FPC:Hirose_FH12-24S-0.5SH_1x24-1MP_P0.50mm_Horizontal",
              DC="Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical_SMD_Pin1Left", SOD323="Diode_SMD:D_SOD-323", NTC="Connector_JST:JST_SH_SM02B-SRSS-TB_1x02-1MP_P1.00mm_Horizontal")
    def tpl(name, pins, fpn, ref):
        return Part(name=name, tool=SKIDL, dest=TEMPLATE, ref_prefix=ref, pins=[Pin(num=i + 1, name=n, func=Pin.types.PASSIVE) for i, n in enumerate(pins)], footprint=fp[fpn])
    R2512 = tpl("R", ["1", "2"], "R_2512", "R"); R0603 = tpl("R", ["1", "2"], "R_0603", "R"); C0603 = tpl("C", ["1", "2"], "C_0603", "C")
    FET = tpl("Doppel_NMOS_generisch", ["S1", "G1", "D2", "S2", "G2", "D1"], "SOT363", "Q")   # SOT-363: 1 S1, 2 G1, 3 D2, 4 S2, 5 G2, 6 D1 (ERW-E3 N7, ENT-192)
    AFE_pins = [f"S{k}" for k in range(kan + 1)] + [f"G{k}" for k in range(1, kan + 1)] + [f"H{k}" for k in range(1, kan + 1)] + ["VCC1", "VCC2", "VCC3", "VCC4", "GND", "NTC1", "NTC2", "NTC3", "NTC4", "TXA", "TXB", "RXA", "RXB", "ABSCHALT_IN"]
    AFE = tpl("AFE_generisch_18K", AFE_pins, "QFP", "U")
    XF = tpl("Uebertrager_generisch", ["P1", "P2", "S1", "S2"], "SOIC16", "T")
    SEK = tpl("OVP6_generisch", [f"IN{i}" for i in range(7)] + ["ABSCHALT", "GND"], "TSSOP16", "U")   # 6-Zellen-Überspannungsschutz, 7 Messeingänge (ERW-E3 N7, ENT-193)
    FPC = tpl("FPC_24", [f"T{k}" for k in range(kan + 1)] + ["ABSCHALT", "GND", "NC1", "NC2", "NC3"], "FPC", "J")
    DCs = tpl("Daisy_Stecker", ["A", "B"], "NTC", "J"); TVS = tpl("TVS_generisch", ["A", "K"], "SOD323", "D"); NTC = tpl("NTC_Eingang", ["1", "2"], "NTC", "J")
    T = [Net(f"T{k}") for k in range(kan + 1)]; S = [Net(f"S{k}") for k in range(kan + 1)]; GND = Net("GND"); VCC = Net("VCC"); OFF = Net("ABSCHALT")
    fpc = FPC(value="FPC 24-polig (Zellabgriffe)"); afe = AFE(value="AFE generisch 18 Kanaele, ASIL-D-faehig (BT-322)")
    for k in range(kan + 1): fpc[f"T{k}"] += T[k]; afe[f"S{k}"] += S[k]
    fpc["ABSCHALT"] += OFF; fpc["GND"] += GND; afe["GND"] += GND; [afe[f"VCC{i}"].__iadd__(VCC) for i in range(1, A_VCC_PINS + 1)]; afe["ABSCHALT_IN"] += OFF
    rf = []
    for k in range(kan + 1):
        r = R0603(value=f"{Rf:g}"); r[1] += T[k]; r[2] += S[k]
    for k in range(1, kan + 1):
        c = C0603(value=f"{Cf:g}n"); c[1] += S[k]; c[2] += S[k - 1]
        G = Net(f"G{k}"); Hn = Net(f"H{k}"); M = Net(f"M{k}"); D = Net(f"D{k}"); afe[f"G{k}"] += G; afe[f"H{k}"] += Hn
        for _ in range(2):
            rb = R2512(value=f"{R_je:g}"); rb[1] += T[k]; rb[2] += D
        q = FET(value="Doppel-NMOS generisch SOT-363, zwei FET in Reihe, Logikpegel, RDSon<=0,5 Ohm je FET, AEC-Q101"); q["G1"] += G; q["G2"] += Hn; q["D1"] += D; q["S1"] += M; q["D2"] += M; q["S2"] += T[k - 1]
    for i in range(4):
        n = NTC(value=f"NTC {i+1} (extern)"); n[1] += afe[f"NTC{i+1}"]; n[2] += GND
    for i in range(2):   # 2 Übertrager, je einer je Richtung der Daisy-Chain
        x = XF(value="Uebertrager generisch 1,5 kV Basisisolierung"); d = DCs(value=f"Daisy-Chain {'oben' if i==0 else 'unten'}")
        a, b = ("TXA", "TXB") if i == 0 else ("RXA", "RXB")
        x["P1"] += afe[a]; x["P2"] += afe[b]; x["S1"] += d["A"]; x["S2"] += d["B"]
        tv = TVS(value=f"TVS generisch (Annahme ERW-E3 N2) {"Eingang" if i==0 else "Ausgang"}"); tv["A"] += d["A"]; tv["K"] += d["B"]
    for g in range(3):   # je OVP 6 Zellen, 7 Messeingänge: T(6g) .. T(6g+6); Ausgänge wired-OR auf ABSCHALT
        sk = SEK(value=f"6-Zellen-Ueberspannungsschutz generisch, Schwelle je Zelle {W('BT-325','schwelle_V'):g} V, {W('BT-325','verzoegerung_ms'):g} ms")
        for i in range(7): sk[f"IN{i}"] += T[6 * g + i]
        sk["ABSCHALT"] += OFF; sk["GND"] += GND
    for j in range(A_VCC_PINS):
        c = C0603(value=f"{A_C_ENTK_NF:g}n (Entkopplung je Versorgungspin, ERW-E3 N2)"); c[1] += VCC; c[2] += GND
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf): ERC()
    (H / f"cmu_{v}_erc.txt").write_text(buf.getvalue())
    generate_netlist(file_=str(H / f"cmu_{v}.net"), tool=KICAD9)
    import builtins; default_circuit = builtins.default_circuit
    teile = []; 
    for p in default_circuit.parts:
        teile.append(dict(ref=p.ref, name=p.name, value=str(p.value), footprint=str(p.footprint), pins={str(pi.num): (pi.net.name if pi.net else None) for pi in p.pins}, pinnamen={str(pi.num): pi.name for pi in p.pins}))
    json.dump(dict(variante=v, herkunft=herk, teile=teile), open(H / f"cmu_{v}_teile.json", "w"), indent=1, ensure_ascii=False)
    with open(H / f"cmu_{v}_bom.csv", "w", newline="") as f:
        w = csv.writer(f, delimiter=";"); w.writerow(["Ref", "Wert", "Footprint", "Bauteilklasse"])
        for t in teile: w.writerow([t["ref"], t["value"], t["footprint"], t["name"]])
    return teile, buf.getvalue()

for v in ("LFP", "NMC"):
    teile, erc = bauen(v); print(v, "Teile:", len(teile), "ERC-Zeilen:", len([z for z in erc.splitlines() if z.startswith("ERC")]), "ERC-ERROR:", erc.count("ERC ERROR"))
