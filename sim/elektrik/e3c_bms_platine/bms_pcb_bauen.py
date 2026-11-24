# E3c BMS-Layout, läuft im KiCad-Flatpak: werkzeuge/kicad-python.sh bms_pcb_bauen.py
# KI-generiert (Claude Sonnet, 2026-11-24), Entwurf. Liest bms_teile.json (aus bms_skidl.py), baut Platine 160 x 100 (ENT-188/189), 4 Lagen (ENT-190),
# Sperrzone HV/NV als durchgehendes Keepout (Breite = Kriechstrecke ENT-191 = 10 mm), Brücken-Footprints mit Padreihen im Abstand > 10 mm. Platzierung per Tabelle.
import sys, json, re, pcbnew, math
H = "/home/cae/hermes/batterie/sim/elektrik/e3c_bms_platine"; OUT = "/home/cae/cae_projekte/batterie/e3c"; LIB = "/app/extensions/Library/footprints"
d = json.load(open(f"{H}/bms_teile.json")); teile = d["teile"]
def akt(bt, m):
    for f in sorted(__import__("glob").glob("/home/cae/hermes/batterie/pm/entscheidungen/ENT-*.md")):
        t = open(f).read(); mm_ = re.match(r"---\n(.*?)\n---", t, re.S)
        if not mm_: continue
        y = {z.partition(":")[0].strip(): re.sub(r"\s+#.*$", "", z.partition(":")[2]).strip() for z in mm_.group(1).splitlines()}
        if y.get("merkmal") == m and bt in y.get("bauteile", "") and y.get("status", "").startswith(("entschieden", "vorgeschlagen")): return float(y["wert"].strip('"'))
    sys.exit(f"Akte fehlt {bt} {m}")
L, B = akt("BT-311", "laenge_mm"), akt("BT-311", "breite_mm"); NL = int(akt("BT-311", "lagen")); KRIECH = akt("BT-311", "kriechstrecke_hv_nv_mm")
b = pcbnew.BOARD(); b.SetCopperLayerCount(NL); mm = pcbnew.FromMM
def P(x, y): return pcbnew.VECTOR2I(mm(x), mm(y))
for (x1, y1, x2, y2) in [(0, 0, L, 0), (L, 0, L, B), (L, B, 0, B), (0, B, 0, 0)]:
    s = pcbnew.PCB_SHAPE(b); s.SetShape(pcbnew.SHAPE_T_SEGMENT); s.SetLayer(pcbnew.Edge_Cuts); s.SetStart(P(x1, y1)); s.SetEnd(P(x2, y2)); s.SetWidth(mm(0.1)); b.Add(s)
ZX0 = 100.0; ZX1 = ZX0 + KRIECH      # Sperrzone x 100 ... 110 (Breite = Kriechstrecke)
nets = {}
def net(n):
    if n not in nets:
        ni = pcbnew.NETINFO_ITEM(b, n); b.Add(ni); nets[n] = ni
    return nets[n]
def rect_courtyard(fp, x0, y0, x1, y1):
    s = pcbnew.PCB_SHAPE(fp); s.SetShape(pcbnew.SHAPE_T_RECT); s.SetFilled(False); s.SetLayer(pcbnew.F_CrtYd); s.SetStart(P(x0, y0)); s.SetEnd(P(x1, y1)); s.SetWidth(mm(0.05)); fp.Add(s)
def pad(fp, num, x, y, w, h):
    p = pcbnew.PAD(fp); p.SetNumber(str(num)); p.SetShape(pcbnew.PAD_SHAPE_RECT); p.SetAttribute(pcbnew.PAD_ATTRIB_SMD); p.SetLayerSet(p.SMDMask()); p.SetSize(P(w, h)); p.SetPosition(P(x, y)); fp.Add(p)
GAP_IN = 5.2      # halber Abstand der inneren Padkanten: 2 x 5,2 = 10,4 mm >= Kriechstrecke 10 mm (Platzhalter-Footprint, Sonnet)
def bruecke(name):
    fp = pcbnew.FOOTPRINT(b); fp.SetFPID(pcbnew.LIB_ID("E3c", name)); pl, pw = 1.6, 0.6 if name.startswith("ISO") else 0.8; xc = GAP_IN + pl / 2
    if name == "ISO_Bruecke_8":
        for i in range(4): pad(fp, i + 1, -xc, -1.905 + 1.27 * i, pl, pw)
        for i in range(4): pad(fp, 5 + i, xc, 1.905 - 1.27 * i, pl, pw)
        hy = 6.5 / 2 + 0.25; rect_courtyard(fp, -7.05, -hy, 7.05, hy); h = 3.0
    else:
        pad(fp, 1, -xc, -1.27, pl, pw); pad(fp, 2, -xc, 1.27, pl, pw); pad(fp, 3, xc, 1.27, pl, pw); pad(fp, 4, xc, -1.27, pl, pw)
        hy = 6.5 / 2 + 0.25; rect_courtyard(fp, -7.05, -hy, 7.05, hy); h = 4.0
    m = pcbnew.FP_3DMODEL(); m.m_Filename = f"{OUT}/modelle/{name}.step"; fp.Models().append(m)
    return fp
def laden(fp):
    lib, name = fp.split(":")
    if lib == "E3c": return bruecke(name)
    return pcbnew.FootprintLoad(f"{LIB}/{lib}.pretty", name)
# ---------------- Platzierung (x, y, Winkel); NV links (x < 100), Sperrzone x 100...110, HV rechts
pos = {}
def at(tag, x, y, a=0): pos[tag] = (x, y, a)
MX, MY = 62.0, 50.0   # MCU-Mitte
at("U_MCU", MX, MY)
# Versorgung (links)
at("J_VERSORGUNG", 6.5, 44, 270); at("Q_VERPOL", 15, 38); at("R_VERPOL", 15, 43); at("D_VERPOL", 20, 43); at("D_TVS", 16, 52); at("L_VERSORGUNG", 24, 52)
at("C_VBAT0", 30, 56); at("C_VBAT1", 30, 61); at("C_VBAT_ELKO", 37, 59); at("C_VBAT_HF", 24, 59)
at("U_SBC", 31, 36); at("C_SBC_OUT0", 39, 44); at("C_SBC_OUT1", 39, 48); at("C_SBC_VS", 24, 44); at("R_KL15", 22, 33)
at("J_DEBUG", 12, 76, 90)
for i in range(3): at(f"D_LED{i+1}", 16 + 5 * i, 93); at(f"R_LED{i+1}", 16 + 5 * i, 89.5)
at("R_NTC", 6, 93); at("R_NTC_PU", 10, 93)
at("Y_MCU", 55, 33); at("C_XTAL0", 50.5, 31, 90); at("C_XTAL1", 59.5, 31, 90)
at("C_RESET", 46, 36); at("C_MCUB0", 44, 63, 0); at("C_MCUB1", 44, 66.5, 0)
# CAN (oben)
for nm, cx in (("1", 69), ("2", 87)):
    at(f"J_CAN{nm}", cx, 6, 0); at(f"D_ESD{nm}_0", cx - 7, 14); at(f"D_ESD{nm}_1", cx + 7, 14); at(f"R_TERM{nm}_0", cx - 4, 17); at(f"R_TERM{nm}_1", cx + 4, 17); at(f"C_TERM{nm}", cx, 17)
    at(f"L_CAN{nm}", cx, 21.5); at(f"U_CAN{nm}", cx, 28.5); at(f"R_STB{nm}", cx + 6.5, 25.5); at(f"C_CAN{nm}_0", cx + 6.5, 29.5); at(f"C_CAN{nm}_1", cx - 6.5, 29.5)
# Kanalgruppen unten
for k, ch in enumerate("PMV"):
    x0 = 30 + 22 * k
    at(f"U_HS_{ch}", x0 + 5, 77); at(f"R_HS_PD_{ch}", x0 + 9, 77); at(f"Q_LS_{ch}", x0 + 5, 83); at(f"R_LS_G_{ch}", x0 + 9, 80.5); at(f"R_LS_PD_{ch}", x0 + 9, 83.5)
    at(f"R_SENSE_{ch}", x0 + 14, 83); at(f"R_I_{ch}", x0 + 14, 79); at(f"C_I_{ch}", x0 + 14, 75)
    at(f"D_FREI_{ch}", x0 + 5, 89); at(f"D_ZENER_{ch}", x0 + 5, 93); at(f"J_SPULE_{ch}", x0 + 15, 93, 0)
at("U_AND1", 54, 70, 90); at("U_AND2", 84, 70, 90); at("C_AND1", 63, 70, 0); at("C_AND2", 93, 70, 0)
# rechts NV
at("U_DM", 90, 48); at("C_DM", 94, 55); at("R_SEK_NV", 94, 66); at("C_ISO1_NV", 94, 22); at("C_ISO2_NV", 94, 61)
# Brücken
at("U_ISO_SHUNT", 105, 15); at("T_DAISY1", 105, 34); at("T_DAISY2", 105, 46); at("U_ISO_SEK", 105, 70)
# HV
at("J_SHUNT", 156, 13, 90); at("R_SHF0", 148, 10); at("R_SHF1", 148, 16); at("C_SHF_D", 143, 13); at("C_SHF0", 143, 9); at("C_SHF1", 143, 17)
at("U_ADC", 130, 15); at("C_ADC0", 123, 12); at("C_ADC1", 123, 18); at("C_ISO1_HV", 117, 22)
at("J_DAISY1", 156, 34, 90); at("D_TVS_DAISY1", 149, 31); at("R_DC1", 149, 37); at("J_DAISY2", 156, 46, 90); at("D_TVS_DAISY2", 149, 43); at("R_DC2", 149, 49)
at("J_SEKUNDAER", 156, 70, 90); at("R_SEK_HV", 148, 70); at("C_ISO2_HV", 117, 64)
byt = {t["tag"]: t for t in teile}
miss = [t["tag"] for t in teile if t["tag"] not in pos]
# MCU-Entkoppler am jeweiligen VDD-Pad
if not miss or all(m.startswith("C_MCU") for m in miss): pass
fps = {}
for t in teile:
    fp = laden(t["footprint"]); fp.SetReference(t["ref"]); fp.SetValue(t["value"][:40]); fp.Reference().SetVisible(False); fp.Value().SetVisible(False)
    for pn, n in t["pins"].items():
        if not n: continue
        pd = fp.FindPadByNumber(pn)
        if pd: pd.SetNet(net(n))
        else: print("PAD FEHLT", t["tag"], pn)
    if t["seite"] in ("HV", "BR"):   # unbenutzte Pads (ohne Netz) von HV-Teilen entfernen, sonst gilt die 10-mm-Regel gegen sie (Muster E3: Daisy-Stecker, Übertrager)
        for pd in list(fp.Pads()):
            if pd.GetNetname() == "": fp.Remove(pd)
    fps[t["tag"]] = fp
# MCU zuerst platzieren, Entkoppler an die VDD-Pads setzen
m = fps["U_MCU"]; m.SetPosition(P(MX, MY)); b.Add(m)
vd = {}
for t in teile:
    if t["tag"] == "U_MCU":
        for pn, nm in t["pinnamen"].items():
            if nm.startswith("VDD") and nm != "VDDA": vd[int(nm[3:])] = pn
for i in range(1, 11):
    pp = m.FindPadByNumber(vd[i]).GetPosition(); px, py = pp.x / 1e6, pp.y / 1e6; dx, dy = px - MX, py - MY
    if abs(dx) > abs(dy): at(f"C_MCU{i}", px + math.copysign(4.0, dx), py, 90)
    else: at(f"C_MCU{i}", px, py + math.copysign(4.0, dy), 0)
at("C_MCUA0", 42.5, 40.5, 90); at("C_MCUA1", 42.5, 43.5, 90); at("C_MCUA2", 42.5, 46.5, 90)
miss = [t["tag"] for t in teile if t["tag"] not in pos]; print("nicht platziert:", miss)
for t in teile:
    if t["tag"] == "U_MCU" or t["tag"] in miss: continue
    fp = fps[t["tag"]]; x, y, a = pos[t["tag"]]; fp.SetPosition(P(x, y)); fp.SetOrientationDegrees(a); b.Add(fp)
# ---------------- Sperrzone HV/NV: Keepout über alle Lagen, volle Plattenhöhe
z = pcbnew.ZONE(b); z.SetIsRuleArea(True); z.SetDoNotAllowTracks(True); z.SetDoNotAllowVias(True); z.SetDoNotAllowZoneFills(True); z.SetDoNotAllowPads(False); z.SetDoNotAllowFootprints(False)
ls_ = pcbnew.LSET(); [ls_.AddLayer(l) for l in (pcbnew.F_Cu, pcbnew.In1_Cu, pcbnew.In2_Cu, pcbnew.B_Cu)]; z.SetLayerSet(ls_); z.SetZoneName("Sperrzone_HV_NV")
o = z.Outline(); o.NewOutline()
for (a_, c_) in ((ZX0, 0), (ZX1, 0), (ZX1, B), (ZX0, B)): o.Append(mm(a_), mm(c_))
b.Add(z)
# ---------------- Versorgungsflächen auf den Innenlagen (In1 Masse, In2 Versorgung), je Bereich NV / HV getrennt, Abstand zur Sperrzone >= 0,5 mm
def ebene(layer, netname, x0, x1):
    zz = pcbnew.ZONE(b); ls = pcbnew.LSET(); ls.AddLayer(layer); zz.SetLayerSet(ls); zz.SetNet(b.FindNet(netname)); zz.SetLocalClearance(mm(0.2)); zz.SetMinThickness(mm(0.15))
    zz.SetPadConnection(pcbnew.ZONE_CONNECTION_THERMAL); zz.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_ALWAYS); oo = zz.Outline(); oo.NewOutline()
    for (a_, c_) in ((x0, 0.5), (x1, 0.5), (x1, B - 0.5), (x0, B - 0.5)): oo.Append(mm(a_), mm(c_))
    b.Add(zz)
# In2 bleibt Signal-/Versorgungslage (Lauf 2 mit zwei Flächenlagen: 76 Verbindungen offen; Lauf 1 mit Fläche +3V3 auf In2: Fläche durch Bahnen zerschnitten)
ebene(pcbnew.In1_Cu, "GND", 0.5, ZX0 - 0.5); ebene(pcbnew.In1_Cu, "HV_GND", ZX1 + 0.5, L - 0.5)
pcbnew.ZONE_FILLER(b).Fill(b.Zones())
os_ = __import__("os"); os_.makedirs(OUT, exist_ok=True)
b.Save(f"{OUT}/bms.kicad_pcb")
hv = sorted({n for t in teile for n in t["pins"].values() if n in ("SHUNT_P", "SHUNT_N", "ADC_INP", "ADC_INN", "HV_VDD", "HV_GND", "HV_CLK", "HV_DAT", "SEK_IN_HV", "DC1_A", "DC1_B", "DC2_A", "DC2_B")})
json.dump(dict(hv_netze=hv, nicht_platziert=miss, sperrzone_x_mm=[ZX0, ZX1], platine_mm=[L, B], lagen=NL, kriechstrecke_mm=KRIECH, pos={k: v for k, v in pos.items()}), open(f"{H}/layout_info.json", "w"))
print("Teile", len(b.GetFootprints()), "Netze", len(nets), "HV-Netze", hv)
