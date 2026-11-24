#!/usr/bin/env python3
"""E3c BMS-Leiterplatte BT-311 als Code (SKiDL). KI-generiert (Claude Sonnet, 2026-11-24), Entwurf.
Grundlage: ERWARTUNG.md Teil B (alle Blöcke und Annahmen von Opus, Herkunft ERW-E3c). Werte der Akten ENT-188…191 werden aus pm/entscheidungen gelesen.
Passiv-Werte sind Platzhalter (Wert offen, nicht in der Erwartung genannt); Footprintgrößen sind Platzhalter (Sonnet, zur Bestätigung durch Opus).
Ausgabe: bms.net, bms_bom.csv, bms_teile.json (Teile mit Tag, Pins, Netz, Seite HV/NV), bms_erc.txt. Aufruf: source umgebung.sh; python3 bms_skidl.py"""
import re, json, csv, sys, pathlib, io, contextlib
H = pathlib.Path(__file__).resolve().parent; ROOT = H.parents[2]

def akten():
    d = {}
    for f in sorted((ROOT / "pm/entscheidungen").glob("ENT-*.md")):
        t = f.read_text(); m = re.match(r"---\n(.*?)\n---", t, re.S)
        if not m: continue
        y = {}
        for z in m.group(1).splitlines():
            k, _, v = z.partition(":"); y[k.strip()] = re.sub(r"\s+#.*$", "", v).strip()
        if not y.get("status", "").startswith(("entschieden", "vorgeschlagen")): continue
        w = y.get("wert", "").strip('"')
        try: w = float(w)
        except ValueError: pass
        for bt in re.findall(r"BT-\d+", y.get("bauteile", "")): d[(bt, y.get("merkmal"))] = (w, y["id"])
    return d
AK = akten()
def wert(bt, m):
    if (bt, m) not in AK: sys.exit(f"Wert fehlt: {bt} {m}")
    return AK[(bt, m)]

from skidl import Part, Net, Pin, TEMPLATE, SKIDL, generate_netlist, ERC, reset, KICAD9
import builtins
reset()
herk = {}
for m in ("laenge_mm", "breite_mm", "lagen", "kriechstrecke_hv_nv_mm"):
    w, h = wert("BT-311", m); herk[f"BT-311.{m}"] = f"{w} ({h})"
FP = dict(
 R0603="Resistor_SMD:R_0603_1608Metric", C0603="Capacitor_SMD:C_0603_1608Metric", C0805="Capacitor_SMD:C_0805_2012Metric", C1206="Capacitor_SMD:C_1206_3216Metric",
 CP="Capacitor_SMD:CP_Elec_6.3x7.7", L1210="Inductor_SMD:L_1210_3225Metric", SOT23="Package_TO_SOT_SMD:SOT-23", SOT235="Package_TO_SOT_SMD:SOT-23-5",
 SOD323="Diode_SMD:D_SOD-323", SOD123="Diode_SMD:D_SOD-123", SMA="Diode_SMD:D_SMA", SMB="Diode_SMD:D_SMB", LED="LED_SMD:LED_0603_1608Metric",
 SOIC8="Package_SO:SOIC-8_3.9x4.9mm_P1.27mm", SOIC14="Package_SO:SOIC-14_3.9x8.7mm_P1.27mm", SOIC16="Package_SO:SOIC-16_3.9x9.9mm_P1.27mm",
 LQFP48="Package_QFP:LQFP-48_7x7mm_P0.5mm", LQFP144="Package_QFP:LQFP-144_20x20mm_P0.5mm", XTAL="Crystal:Crystal_SMD_3225-4Pin_3.2x2.5mm",
 CMC="Inductor_SMD:L_CommonModeChoke_Coilcraft_1812CAN", PH2="Connector_JST:JST_PH_S2B-PH-SM4-TB_1x02-1MP_P2.00mm_Horizontal", PH4="Connector_JST:JST_PH_S4B-PH-SM4-TB_1x04-1MP_P2.00mm_Horizontal",
 SH2="Connector_JST:JST_SH_SM02B-SRSS-TB_1x02-1MP_P1.00mm_Horizontal", SH4="Connector_JST:JST_SH_SM04B-SRSS-TB_1x04-1MP_P1.00mm_Horizontal", SH3="Connector_JST:JST_SH_SM03B-SRSS-TB_1x03-1MP_P1.00mm_Horizontal",
 DBG="Connector_PinHeader_1.27mm:PinHeader_2x05_P1.27mm_Vertical_SMD",
 ISO8="E3c:ISO_Bruecke_8", TRF4="E3c:Uebertrager_Bruecke_4")
def tpl(name, pins, fp, ref):
    """pins: Liste von Namen (Pad 1..n) oder dict {Pad: Name}"""
    if isinstance(pins, dict): pl = [Pin(num=str(k), name=v, func=Pin.types.PASSIVE) for k, v in pins.items()]
    else: pl = [Pin(num=i + 1, name=n, func=Pin.types.PASSIVE) for i, n in enumerate(pins)]
    return Part(name=name, tool=SKIDL, dest=TEMPLATE, ref_prefix=ref, pins=pl, footprint=FP[fp])
R = tpl("R", ["1", "2"], "R0603", "R"); C = tpl("C", ["1", "2"], "C0603", "C"); C8 = tpl("C_8", ["1", "2"], "C0805", "C"); C12 = tpl("C_12", ["1", "2"], "C1206", "C"); CPe = tpl("C_Elko", ["1", "2"], "CP", "C")
L = tpl("L_Drossel", ["1", "2"], "L1210", "L"); RS = tpl("R_Sense", ["1", "2"], "R0603", "R")
QP = tpl("PMOS_Verpolschutz", ["G", "S", "D"], "SOT23", "Q"); QN = tpl("NMOS_Low_Side", ["G", "S", "D"], "SOT23", "Q")
DZ3 = tpl("Z_Diode_Gate", ["A", "K"], "SOD123", "D"); DTVS = tpl("TVS_ISO7637", ["A", "K"], "SMB", "D"); DESD = tpl("ESD_Diode", ["A", "K"], "SOD323", "D"); DTV2 = tpl("TVS_Daisy", ["A", "K"], "SOD323", "D")
DBLK = tpl("Diode_Freilauf", ["A", "K"], "SMA", "D"); DZL = tpl("Z_Diode_Loeschung", ["A", "K"], "SMA", "D"); LED = tpl("LED", ["K", "A"], "LED", "D")
SBC = tpl("SBC_generisch_Watchdog", {1: "VS1", 2: "VS2", 3: "GND1", 4: "GND2", 5: "V1", 6: "V2", 7: "RSTN", 8: "WDI", 9: "WAKE", 10: "INTN", 11: "EN"}, "LQFP48", "U")
HS = tpl("HighSide_Schalter_generisch", {1: "IN", 2: "GND", 3: "DIAG", 4: "OUT", 5: "VS"}, "SOT235", "U")
CAN = tpl("CAN_FD_Transceiver", {1: "TXD", 2: "GND", 3: "VCC", 4: "RXD", 5: "VIO", 6: "CANL", 7: "CANH", 8: "STB"}, "SOIC8", "U")
CMC = tpl("CAN_Gleichtaktdrossel", {1: "A1", 2: "B1", 3: "B2", 4: "A2"}, "CMC", "L")
AND = tpl("UND_Gatter_4fach", {1: "A1", 2: "B1", 3: "Y1", 4: "A2", 5: "B2", 6: "Y2", 7: "GND", 8: "Y3", 9: "A3", 10: "B3", 11: "Y4", 12: "A4", 13: "B4", 14: "VCC"}, "SOIC14", "U")
DM = tpl("Daisy_Master_generisch", {1: "VDD", 2: "GND", 3: "SCK", 4: "MOSI", 5: "MISO", 6: "CS", 7: "TXA", 8: "TXB", 9: "RXA", 10: "RXB"}, "SOIC16", "U")
ADC = tpl("Shunt_ADC_generisch_HV", {1: "INP", 2: "INN", 3: "VDD", 4: "GND", 5: "MCLK", 6: "MDAT"}, "SOIC16", "U")
ISO = tpl("Digital_Isolator_verstaerkt", {1: "VDD2", 2: "GND2", 3: "OUT_A", 4: "OUT_B", 5: "IN_B", 6: "IN_A", 7: "GND1", 8: "VDD1"}, "ISO8", "U")
TRF = tpl("Uebertrager_verstaerkt", {1: "P1", 2: "P2", 3: "S1", 4: "S2"}, "TRF4", "T")
XT = tpl("Quarz", {1: "X1", 2: "G1", 3: "X2", 4: "G2"}, "XTAL", "Y")
J2 = tpl("Stecker_2", ["1", "2"], "PH2", "J"); J3 = tpl("Stecker_3_HV", ["1", "2", "3"], "SH3", "J"); J4 = tpl("Stecker_4", ["1", "2", "3", "4"], "PH4", "J"); JS4 = tpl("Stecker_4_HV", ["1", "2", "3", "4"], "SH4", "J"); JD2 = tpl("Daisy_Stecker", ["A", "B"], "SH2", "J")
JDBG = tpl("Debug_Stecker", {1: "VREF", 2: "SWDIO", 3: "GND", 4: "SWCLK", 5: "GND2", 6: "SWO", 9: "GND3", 10: "NRST"}, "DBG", "J")
# MCU: Pad -> Funktion (Seite je Zielrichtung, KiCad-Zählung: links 1-36 oben->unten, unten 37-72 links->rechts, rechts 73-108 unten->oben, oben 109-144 rechts->links)
mcu_pins = {}
VDDP = [6, 14, 22, 30, 41, 53, 65, 76, 88, 100]; VSSP = [8, 16, 24, 32, 43, 55, 67, 78, 90, 102]
for i, p in enumerate(VDDP): mcu_pins[p] = f"VDD{i+1}"
for i, p in enumerate(VSSP): mcu_pins[p] = f"VSS{i+1}"
mcu_pins.update({3: "VDDA", 4: "VSSA", 5: "VREF", 133: "XTAL1", 135: "XTAL2", 10: "NRST", 12: "WDI", 18: "INTN", 20: "SWDIO", 21: "SWCLK", 26: "SWO", 28: "NTC_ADC", 34: "LED1", 35: "LED2", 36: "LED3",
  # unten: Schütz-Kanäle P, M, V (je HS-Freigabe, LS-Freigabe, HS-Diagnose, Strommessung)
  46: "P_HS_EN", 47: "P_LS_EN", 48: "P_DIAG", 49: "P_I", 56: "M_HS_EN", 57: "M_LS_EN", 58: "M_DIAG", 59: "M_I", 61: "V_HS_EN", 62: "V_LS_EN", 63: "V_DIAG", 64: "V_I",
  # rechts: Daisy-Master-SPI, Shunt-Daten, Sekundärpfad
  80: "DM_SCK", 81: "DM_MOSI", 82: "DM_MISO", 83: "DM_CS", 92: "SH_CLK", 93: "SH_DAT", 96: "SEK_OK", 98: "SEK_STATUS",
  # oben: CAN
  112: "CAN2_TX", 113: "CAN2_RX", 116: "CAN1_TX", 117: "CAN1_RX"})
MCU = tpl("MCU_ASIL_D_Lockstep_generisch", mcu_pins, "LQFP144", "U")

teile_tags = []   # (part, tag, seite)
def mk(t, tag, value, seite="NV"):
    p = t(value=value); teile_tags.append((p, tag, seite)); return p
GND = Net("GND"); V33 = Net("+3V3"); V5 = Net("+5V"); VBAT_IN = Net("VBAT_IN"); VBAT = Net("VBAT"); VBATF = Net("VBAT_F"); KL15 = Net("KL15")
HGND = Net("HV_GND"); HVDD = Net("HV_VDD")
# ---- Versorgung 12 V: Verpolschutz, TVS, Drossel, Systembasis-IC
j1 = mk(J4, "J_VERSORGUNG", "Stecker 12 V (VBAT, GND, KL15)"); j1[1] += VBAT_IN; j1[2] += GND; j1[3] += KL15
q1 = mk(QP, "Q_VERPOL", "PMOS Verpolschutz generisch"); q1["D"] += VBAT_IN; q1["S"] += VBAT
rg = mk(R, "R_VERPOL", "R Gate Verpolschutz (Wert offen)"); rg[1] += q1["G"]; rg[2] += GND
dz = mk(DZ3, "D_VERPOL", "Z-Diode Gate-Schutz generisch"); dz["A"] += q1["G"]; dz["K"] += VBAT
tvs = mk(DTVS, "D_TVS", "TVS ISO 7637-2 generisch"); tvs["A"] += GND; tvs["K"] += VBAT
l1 = mk(L, "L_VERSORGUNG", "Drossel Eingangsfilter (Wert offen)"); l1[1] += VBAT; l1[2] += VBATF
for i in range(2): c = mk(C12, f"C_VBAT{i}", "C Pufferung (Wert offen)"); c[1] += VBATF; c[2] += GND
c = mk(CPe, "C_VBAT_ELKO", "C Elko Pufferung (Wert offen)"); c[1] += VBATF; c[2] += GND
c = mk(C, "C_VBAT_HF", "C Entkopplung (Wert offen)"); c[1] += VBATF; c[2] += GND
sbc = mk(SBC, "U_SBC", "Systembasis-IC generisch mit Watchdog, ASIL D")
sbc["VS1"] += VBATF; sbc["VS2"] += VBATF; sbc["GND1"] += GND; sbc["GND2"] += GND; sbc["V1"] += V33; sbc["V2"] += V5
RST = Net("NRST"); WDI = Net("WDI"); INTN = Net("INTN"); sbc["RSTN"] += RST; sbc["WDI"] += WDI; sbc["INTN"] += INTN; sbc["EN"] += VBATF
r = mk(R, "R_KL15", "R Weckeingang KL15 (Wert offen)"); r[1] += KL15; r[2] += sbc["WAKE"]
for k, n in enumerate((V33, V5)): c = mk(C8, f"C_SBC_OUT{k}", "C Ausgang SBC (Wert offen)"); c[1] += n; c[2] += GND
c = mk(C, "C_SBC_VS", "C Entkopplung (Wert offen)"); c[1] += VBATF; c[2] += GND
# ---- Rechner
mcu = mk(MCU, "U_MCU", "Mikrocontroller generisch ASIL D Lockstep LQFP-144")
for i in range(1, 11):
    mcu[f"VDD{i}"] += V33; mcu[f"VSS{i}"] += GND
    c = mk(C, f"C_MCU{i}", "C Entkopplung (Wert offen)"); c[1] += V33; c[2] += GND
mcu["VDDA"] += V33; mcu["VSSA"] += GND; mcu["VREF"] += V33
for i in range(3): c = mk(C, f"C_MCUA{i}", "C Entkopplung analog (Wert offen)"); c[1] += V33; c[2] += GND
for i in range(2): c = mk(C8, f"C_MCUB{i}", "C Puffer Rechner (Wert offen)"); c[1] += V33; c[2] += GND
mcu["NRST"] += RST; mcu["WDI"] += WDI; mcu["INTN"] += INTN
cr = mk(C, "C_RESET", "C Reset (Wert offen)"); cr[1] += RST; cr[2] += GND
xt = mk(XT, "Y_MCU", "Quarz Rechner (Wert offen)"); X1, X2 = Net("XTAL1"), Net("XTAL2"); xt["X1"] += X1; xt["X2"] += X2; xt["G1"] += GND; xt["G2"] += GND; mcu["XTAL1"] += X1; mcu["XTAL2"] += X2
for k, n in enumerate((X1, X2)): c = mk(C, f"C_XTAL{k}", "C Quarz (Wert offen)"); c[1] += n; c[2] += GND
dbg = mk(JDBG, "J_DEBUG", "Debug-Stecker SWD"); dbg["VREF"] += V33; dbg["SWDIO"] += mcu["SWDIO"]; dbg["SWCLK"] += mcu["SWCLK"]; dbg["SWO"] += mcu["SWO"]; dbg["NRST"] += RST
for k in ("GND", "GND2", "GND3"): dbg[k] += GND
for i in range(3):
    d = mk(LED, f"D_LED{i+1}", "LED Status"); rl = mk(R, f"R_LED{i+1}", "R LED (Wert offen)"); n = Net(f"LED{i+1}")
    mcu[f"LED{i+1}"] += n; rl[1] += n; rl[2] += d["A"]; d["K"] += GND
ntc = mk(R, "R_NTC", "NTC Platinentemperatur (extern bestückt, Wert offen)"); rn = mk(R, "R_NTC_PU", "R Pull-up NTC (Wert offen)"); nn = Net("NTC_ADC")
ntc[1] += nn; ntc[2] += GND; rn[1] += V33; rn[2] += nn; mcu["NTC_ADC"] += nn
# ---- Bus: 2 x CAN-FD, Gleichtaktdrossel, Terminierung, ESD
for b, (nm, tx, rx) in enumerate((("1", "CAN1_TX", "CAN1_RX"), ("2", "CAN2_TX", "CAN2_RX"))):
    u = mk(CAN, f"U_CAN{nm}", f"CAN-FD-Transceiver {'Fahrzeug' if b == 0 else 'Laden'}")
    cl, ch = Net(f"CANL{nm}"), Net(f"CANH{nm}"); cl2, ch2 = Net(f"CANL{nm}_BUS"), Net(f"CANH{nm}_BUS"); mid = Net(f"CAN{nm}_MITTE")
    t, rr = Net(tx), Net(rx); mcu[tx] += t; u["TXD"] += t; mcu[rx] += rr; u["RXD"] += rr
    u["GND"] += GND; u["VCC"] += V5; u["VIO"] += V33; u["CANL"] += cl; u["CANH"] += ch
    rstb = mk(R, f"R_STB{nm}", "R Standby (Wert offen)"); rstb[1] += u["STB"]; rstb[2] += GND
    cm = mk(CMC, f"L_CAN{nm}", "Gleichtaktdrossel CAN"); cm["A1"] += ch; cm["B1"] += ch2; cm["A2"] += cl; cm["B2"] += cl2
    for k, (a, z) in enumerate(((ch2, mid), (mid, cl2))): rt = mk(R, f"R_TERM{nm}_{k}", "R Terminierung geteilt (Wert offen)"); rt[1] += a; rt[2] += z
    ct = mk(C, f"C_TERM{nm}", "C Terminierung (Wert offen)"); ct[1] += mid; ct[2] += GND
    for k, n in enumerate((ch2, cl2)): e = mk(DESD, f"D_ESD{nm}_{k}", "ESD-Diode CAN"); e["A"] += GND; e["K"] += n
    for k, n in enumerate((V5, V33)): c = mk(C, f"C_CAN{nm}_{k}", "C Entkopplung (Wert offen)"); c[1] += n; c[2] += GND
    jc = mk(J4, f"J_CAN{nm}", f"Stecker CAN {'Fahrzeug' if b == 0 else 'Laden'} (CANH, CANL, GND)"); jc[1] += ch2; jc[2] += cl2; jc[3] += GND
# ---- Schützansteuerung BT-715: 3 Kanäle, High-Side + Low-Side, Zener-Löschung, Hardware-UND mit Sekundärpfad
SEK_OK = Net("SEK_OK")
ands = [mk(AND, f"U_AND{i+1}", "UND-Gatter 4fach (Hardware-UND Sekundärpfad, FSR-06)") for i in range(2)]
for ia, a in enumerate(ands):
    a["GND"] += GND; a["VCC"] += V33
    c = mk(C, f"C_AND{ia+1}", "C Entkopplung (Wert offen)"); c[1] += V33; c[2] += GND
gate = 0
for kc, ch_ in enumerate(("P", "M", "V")):
    n_hs_en, n_ls_en = Net(f"{ch_}_HS_EN"), Net(f"{ch_}_LS_EN"); mcu[f"{ch_}_HS_EN"] += n_hs_en; mcu[f"{ch_}_LS_EN"] += n_ls_en
    g_hs, g_ls = Net(f"{ch_}_HS_IN"), Net(f"{ch_}_LS_G")   # Ausgänge der UND-Gatter
    a_hs = ands[(2 * kc) // 4]; k_hs = (2 * kc) % 4 + 1; a_ls = ands[(2 * kc + 1) // 4]; k_ls = (2 * kc + 1) % 4 + 1
    a_hs[f"A{k_hs}"] += n_hs_en; a_hs[f"B{k_hs}"] += SEK_OK; a_hs[f"Y{k_hs}"] += g_hs
    a_ls[f"A{k_ls}"] += n_ls_en; a_ls[f"B{k_ls}"] += SEK_OK; a_ls[f"Y{k_ls}"] += g_ls
    hs = mk(HS, f"U_HS_{ch_}", f"High-Side-Schalter generisch, Schütz {ch_}"); cp, cn = Net(f"{ch_}_SPULE_P"), Net(f"{ch_}_SPULE_N"); diag = Net(f"{ch_}_DIAG"); mcu[f"{ch_}_DIAG"] += diag
    hs["IN"] += g_hs; hs["GND"] += GND; hs["DIAG"] += diag; hs["OUT"] += cp; hs["VS"] += VBATF
    rpd = mk(R, f"R_HS_PD_{ch_}", "R Pull-down Eingang (Wert offen)"); rpd[1] += g_hs; rpd[2] += GND
    q = mk(QN, f"Q_LS_{ch_}", f"NMOS Low-Side, Schütz {ch_}"); rgq = mk(R, f"R_LS_G_{ch_}", "R Gate (Wert offen)"); rpq = mk(R, f"R_LS_PD_{ch_}", "R Gate-Pull-down (Wert offen)"); gq = Net(f"{ch_}_LS_GATE")
    rgq[1] += g_ls; rgq[2] += gq; q["G"] += gq; rpq[1] += gq; rpq[2] += GND; q["D"] += cn; sn = Net(f"{ch_}_SENSE"); q["S"] += sn
    rs = mk(RS, f"R_SENSE_{ch_}", "R Messwiderstand Spulenstrom (Wert offen)"); rs[1] += sn; rs[2] += GND
    ri = mk(R, f"R_I_{ch_}", "R Filter Strommessung (Wert offen)"); ci = mk(C, f"C_I_{ch_}", "C Filter Strommessung (Wert offen)"); an = Net(f"{ch_}_I")
    ri[1] += sn; ri[2] += an; ci[1] += an; ci[2] += GND; mcu[f"{ch_}_I"] += an
    zn = Net(f"{ch_}_ZENER")   # Zener-Löschung: Spulenende N -> Diode -> Z-Diode (in Sperrrichtung) -> VBAT_F
    db = mk(DBLK, f"D_FREI_{ch_}", "Diode Freilauf in Reihe zur Z-Diode"); db["A"] += cn; db["K"] += zn
    zl = mk(DZL, f"D_ZENER_{ch_}", "Z-Diode Löschung generisch"); zl["K"] += zn; zl["A"] += VBATF
    js = mk(J2, f"J_SPULE_{ch_}", f"Stecker Spule Schütz {ch_} (BT-715)"); js[1] += cp; js[2] += cn
# ---- HV-Seite: Shunt-ADC (BT-340), Sekundärpfad, Daisy-Chain-Master
SPS, SNS = Net("SHUNT_P"), Net("SHUNT_N"); jsh = mk(JS4, "J_SHUNT", "Stecker Shunt (BT-340, HV-Seite): Shunt+, Shunt-, HV_VDD, HV_GND", "HV"); jsh[1] += SPS; jsh[2] += SNS; jsh[3] += HVDD; jsh[4] += HGND
ip, im = Net("ADC_INP"), Net("ADC_INN")
for k, (a, z) in enumerate(((SPS, ip), (SNS, im))): rr = mk(R, f"R_SHF{k}", "R Eingangsfilter Shunt (Wert offen)", "HV"); rr[1] += a; rr[2] += z
cd = mk(C, "C_SHF_D", "C Differenzfilter Shunt (Wert offen)", "HV"); cd[1] += ip; cd[2] += im
for k, n in enumerate((ip, im)): c = mk(C, f"C_SHF{k}", "C Filter nach HV_GND (Wert offen)", "HV"); c[1] += n; c[2] += HGND
adc = mk(ADC, "U_ADC", "Shunt-ADC generisch (Sigma-Delta, HV-Seite)", "HV"); adc["INP"] += ip; adc["INN"] += im; adc["VDD"] += HVDD; adc["GND"] += HGND
hclk, hdat = Net("HV_CLK"), Net("HV_DAT"); adc["MCLK"] += hclk; adc["MDAT"] += hdat
for k in range(2): c = mk(C, f"C_ADC{k}", "C Entkopplung HV (Wert offen)", "HV"); c[1] += HVDD; c[2] += HGND
iso1 = mk(ISO, "U_ISO_SHUNT", "Shunt-ADC-Isolator: digitaler Isolator, verstärkt (HV/NV)", "BR")
iso1["VDD1"] += HVDD; iso1["GND1"] += HGND; iso1["IN_A"] += hclk; iso1["IN_B"] += hdat; iso1["VDD2"] += V33; iso1["GND2"] += GND
shc, shd = Net("SH_CLK"), Net("SH_DAT"); iso1["OUT_A"] += shc; iso1["OUT_B"] += shd; mcu["SH_CLK"] += shc; mcu["SH_DAT"] += shd
c = mk(C, "C_ISO1_HV", "C Entkopplung HV (Wert offen)", "HV"); c[1] += HVDD; c[2] += HGND
c = mk(C, "C_ISO1_NV", "C Entkopplung NV (Wert offen)"); c[1] += V33; c[2] += GND
# Sekundärpfad FSR-06: Leitung der CMU (HV-Seite) -> verstärkt isolierter Isolator -> Hardware-UND
jse = mk(J3, "J_SEKUNDAER", "Stecker Sekundärpfad der CMUs (ABSCHALT, HV_GND, HV_VDD)", "HV"); SEK_HV = Net("SEK_IN_HV"); jse[1] += SEK_HV; jse[2] += HGND; jse[3] += HVDD
iso2 = mk(ISO, "U_ISO_SEK", "Isolator Sekundärpfad: digitaler Isolator, verstärkt (HV/NV)", "BR")
iso2["VDD1"] += HVDD; iso2["GND1"] += HGND; iso2["IN_A"] += SEK_HV; iso2["VDD2"] += V33; iso2["GND2"] += GND; iso2["OUT_A"] += SEK_OK
sst = Net("SEK_STATUS"); iso2["OUT_B"] += sst; mcu["SEK_STATUS"] += sst; mcu["SEK_OK"] += SEK_OK
rsk = mk(R, "R_SEK_HV", "R Eingang Sekundärpfad HV (Wert offen)", "HV"); rsk[1] += SEK_HV; rsk[2] += HGND
c = mk(C, "C_ISO2_HV", "C Entkopplung HV (Wert offen)", "HV"); c[1] += HVDD; c[2] += HGND
c = mk(C, "C_ISO2_NV", "C Entkopplung NV (Wert offen)"); c[1] += V33; c[2] += GND
rsn = mk(R, "R_SEK_NV", "R Pull-down SEK_OK (Wert offen)"); rsn[1] += SEK_OK; rsn[2] += GND
# Daisy-Chain-Master: Master-IC (NV), 2 Übertrager mit verstärkter Isolation (Brücke), je Stecker + TVS (HV)
dm = mk(DM, "U_DM", "Daisy-Chain-Master generisch (BT-322-Gegenstück)"); dm["VDD"] += V33; dm["GND"] += GND
for nme, pn in (("SCK", "DM_SCK"), ("MOSI", "DM_MOSI"), ("MISO", "DM_MISO"), ("CS", "DM_CS")): n = Net(pn); dm[nme] += n; mcu[pn] += n
c = mk(C, "C_DM", "C Entkopplung (Wert offen)"); c[1] += V33; c[2] += GND
for i, (ta, tb) in enumerate((("TXA", "TXB"), ("RXA", "RXB"))):
    x = mk(TRF, f"T_DAISY{i+1}", f"Übertrager verstärkte Isolation zur ersten CMU ({'Senden' if i == 0 else 'Empfang'})", "BR")
    n1, n2 = Net(f"DM_{ta}"), Net(f"DM_{tb}"); dm[ta] += n1; dm[tb] += n2; x["P1"] += n1; x["P2"] += n2
    h1, h2 = Net(f"DC{i+1}_A"), Net(f"DC{i+1}_B"); x["S1"] += h1; x["S2"] += h2
    jd = mk(JD2, f"J_DAISY{i+1}", f"Daisy-Chain-Stecker {'Ausgang' if i == 0 else 'Eingang'} zur ersten CMU", "HV"); jd["A"] += h1; jd["B"] += h2
    tv = mk(DTV2, f"D_TVS_DAISY{i+1}", "TVS Daisy-Chain (analog E3 N2)", "HV"); tv["A"] += h1; tv["K"] += h2
    rt = mk(R, f"R_DC{i+1}", "R Abschluss Daisy-Chain (Wert offen)", "HV"); rt[1] += h1; rt[2] += h2
buf = io.StringIO()
with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf): ERC()
(H / "bms_erc.txt").write_text(buf.getvalue())
generate_netlist(file_=str(H / "bms.net"), tool=KICAD9)
dc = builtins.default_circuit
tag = {id(p): (t, s) for p, t, s in teile_tags}
teile = []
for p in dc.parts:
    t, s = tag[id(p)]
    teile.append(dict(ref=p.ref, tag=t, name=p.name, value=str(p.value), footprint=str(p.footprint), seite=s, pins={str(pi.num): (pi.net.name if pi.net else None) for pi in p.pins}, pinnamen={str(pi.num): pi.name for pi in p.pins}))
json.dump(dict(herkunft=herk, teile=teile), open(H / "bms_teile.json", "w"), indent=1, ensure_ascii=False)
with open(H / "bms_bom.csv", "w", newline="") as f:
    w = csv.writer(f, delimiter=";"); w.writerow(["Ref", "Tag", "Wert", "Footprint", "Bauteilklasse", "Seite"])
    for t in teile: w.writerow([t["ref"], t["tag"], t["value"], t["footprint"], t["name"], t["seite"]])
print("Teile:", len(teile), "ERC-ERROR:", buf.getvalue().count("ERC ERROR"), "ERC-WARNING:", buf.getvalue().count("ERC WARNING"))
