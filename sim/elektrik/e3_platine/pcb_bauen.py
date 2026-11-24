# E3 Layout, läuft im KiCad-Flatpak: werkzeuge/kicad-python.sh pcb_bauen.py LFP|NMC
# KI-generiert (Claude Sonnet, 2026-11-24), Entwurf. Liest cmu_<V>_teile.json (aus cmu_skidl.py), baut Platine 120 x 60, 4 Lagen.
import sys, json, pcbnew, math
V = sys.argv[1]; H = "/home/cae/hermes/batterie/sim/elektrik/e3_platine"; OUT = "/home/cae/cae_projekte/batterie/e3"
LIB = "/app/extensions/Library/footprints"
d = json.load(open(f"{H}/cmu_{V}_teile.json")); teile = d["teile"]
b = pcbnew.BOARD(); b.SetCopperLayerCount(4)
mm = pcbnew.FromMM
import os
L, B = float(os.environ.get('E3_L', '120')), 60.0; dL = L - 120.0; PL = os.environ.get('E3_PLATZ', 'B')   # PL=A alt (N7), B = N8 gelockert
def P(x, y): return pcbnew.VECTOR2I(mm(x), mm(y))
# Umriss (BT-321 laenge 120 x breite 60 aus ENT-166/167)
for (x1, y1, x2, y2) in [(0, 0, L, 0), (L, 0, L, B), (L, B, 0, B), (0, B, 0, 0)]:
    s = pcbnew.PCB_SHAPE(b); s.SetShape(pcbnew.SHAPE_T_SEGMENT); s.SetLayer(pcbnew.Edge_Cuts); s.SetStart(P(x1, y1)); s.SetEnd(P(x2, y2)); s.SetWidth(mm(0.1)); b.Add(s)
nets = {}
def net(n):
    if n not in nets:
        ni = pcbnew.NETINFO_ITEM(b, n); b.Add(ni); nets[n] = ni
    return nets[n]
PADMAP = {"Uebertrager_generisch": {"1": "1", "2": "2", "3": "15", "4": "16"}}
fps = {}
def laden(fp):
    lib, name = fp.split(":"); return pcbnew.FootprintLoad(f"{LIB}/{lib}.pretty", name)
by = {}
for t in teile: by.setdefault(t["name"], []).append(t)
pos = {}   # ref -> (x, y, winkel)
# Platzierung: 18 Kanalzellen in zwei Reihen (9 je Reihe), Mittelband: FPC, AFE, Sekundärschutz, Übertrager, Daisy, NTC
nb = {}
for t in teile:
    for p, n in t["pins"].items():
        if n: nb.setdefault(n, []).append((t["ref"], t["name"]))
def kanal_von_G(k):   # FET k -> Gate-Netz Gk
    return f"G{k}"
fet = {}
for t in by["Doppel_NMOS_generisch"]:
    k = int([n for n in t["pins"].values() if n and n.startswith("G")][0][1:]); fet[k] = t   # Gate-Netz G<k> (zweites Gate H<k>, Mittelknoten M<k>)
rb_je = {}; rf_je = {}; c_je = {}
for t in by["R"]:
    nn = set(n for n in t["pins"].values() if n)
    if any(n.startswith("D") for n in nn):
        k = int([n for n in nn if n.startswith("D")][0][1:]); rb_je.setdefault(k, []).append(t)
    else:
        k = int([n for n in nn if n.startswith("T")][0][1:]); rf_je[k] = t
for t in by["C"]:
    nn = [n for n in t["pins"].values() if n]
    if nn and nn[0].startswith("S"): c_je[int(nn[0][1:])] = t
    else: pos[t["ref"]] = None
dx = (L - 10.2) / 9; x0 = 1.9
for k in range(1, 19):
    col = (k - 1) % 9; row = 0 if k <= 9 else 1
    cx = x0 + dx * col + 6.0
    if row == 0:
        y_r = 10.0; y_f = 20.0; y_c = 24.0   # Ausgleichswiderstände oben
        for i, r in enumerate(rb_je[k]): pos[r["ref"]] = (cx - 3.0 + 4.0 * i, y_r - 0.0, 90)
        pos[fet[k]["ref"]] = (cx + 5.0, y_r + 3.0, 0)
        pos[rf_je[k]["ref"]] = (cx - 3.0, y_f - 3.0, 90); pos[c_je[k]["ref"]] = (cx + 1.5, y_f - 3.0, 90)
    else:
        y_r = 50.0; y_f = 40.0
        for i, r in enumerate(rb_je[k]): pos[r["ref"]] = (cx - 3.0 + 4.0 * i, y_r, 90)
        pos[fet[k]["ref"]] = (cx + 5.0, y_r - 3.0, 0)
        pos[rf_je[k]["ref"]] = (cx - 3.0, y_f + 3.0, 90); pos[c_je[k]["ref"]] = (cx + 1.5, y_f + 3.0, 90)
pos[rf_je[0]["ref"]] = (3.0, 30.0, 90)
pos[by["AFE_generisch_18K"][0]["ref"]] = (67.0 + dL / 2, 30.0, 0)
for i, t in enumerate(sorted(by["OVP6_generisch"], key=lambda q: q["ref"])): pos[t["ref"]] = ((76.8, 22.5 + 7.5 * i, 0) if PL == "A" else (38.0, 22.0 + 8.0 * i, 0))
for i, t in enumerate(by["Uebertrager_generisch"]): pos[t["ref"]] = (89.0 + dL + 13.5 * i, 29.0, 90)
pos[by["FPC_24"][0]["ref"]] = (24.0, 30.0, 0)
for i, t in enumerate(by["Daisy_Stecker"]): pos[t["ref"]] = (114.6 + dL, 22.0 + 7.0 * i, 90)
for i, t in enumerate(by["NTC_Eingang"]): pos[t["ref"]] = (6.0 + 6.5 * i, 54.5, 0) if False else ((37.0 + 7.5 * (i % 2), 25.5 + 9.0 * (i // 2), 0) if PL == "A" else (47.0 + 7.5 * (i % 2), 25.5 + 9.0 * (i // 2), 0))
ent = [t for t in by["C"] if pos.get(t["ref"], 1) is None]
for i, t in enumerate(by["TVS_generisch"]): pos[t["ref"]] = (118.9 + dL, 22.0 + 7.0 * i, 90)
for i, t in enumerate(ent): pos[t["ref"]] = (78.5 + dL / 2, 23.5 + 4.0 * i, 0)
unplaced = [t["ref"] for t in teile if t["ref"] not in pos or pos[t["ref"]] is None]
for t in teile:
    if t["ref"] in unplaced: continue
    fp = laden(t["footprint"]); fp.SetReference(t["ref"]); fp.SetValue(t["value"][:40]); fp.Reference().SetVisible(False); fp.Value().SetVisible(False)
    x, y, a = pos[t["ref"]]; fp.SetPosition(P(x, y)); fp.SetOrientationDegrees(a)
    pm = PADMAP.get(t["name"], {})
    for pn, n in t["pins"].items():
        if not n: continue
        pad = fp.FindPadByNumber(pm.get(pn, pn))
        if pad: pad.SetNet(net(n))
    if t["name"] in ("Uebertrager_generisch", "Daisy_Stecker"):   # generischer Footprint: nur benutzte Pads (E3 Lauf 3), unbenutzte Pads entfernen
        for pad in list(fp.Pads()):
            if pad.GetNetname() == "": fp.Remove(pad)
    b.Add(fp)

# ---- Daisy-Leitungen (Trennstelle) von Hand vorverlegt, F.Cu, 0,2 mm; Freiraum 2,5 mm zu allem anderen wird per Platzierung und DSN gesichert
def pad_of(ref, num):
    for q in b.FindFootprintByReference(ref).Pads():
        if q.GetNumber() == str(num): return q
def trk(pts, netname):
    for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
        t_ = pcbnew.PCB_TRACK(b); t_.SetStart(P(xa, ya)); t_.SetEnd(P(xb, yb)); t_.SetWidth(mm(0.2)); t_.SetLayer(pcbnew.F_Cu); t_.SetNet(nets[netname]); b.Add(t_)
def pxy(q): return q.GetPosition().x / 1e6, q.GetPosition().y / 1e6
Tn = sorted(t["ref"] for t in by["Uebertrager_generisch"]); Jn = sorted(t["ref"] for t in by["Daisy_Stecker"]); Dn = sorted(t["ref"] for t in by["TVS_generisch"])
for i in range(2):
    p15, p16 = pad_of(Tn[i], 15), pad_of(Tn[i], 16); (x15, y15), (x16, y16) = pxy(p15), pxy(p16)
    jp = {q.GetNetname(): pxy(q) for q in b.FindFootprintByReference(Jn[i]).Pads()}
    dp = {q.GetNetname(): pxy(q) for q in b.FindFootprintByReference(Dn[i]).Pads()}
    n15, n16 = p15.GetNetname(), p16.GetNetname(); xr = jp[n15][0]
    xd = dp[n15][0]
    if i == 0:   # T1: pad16 weiter links -> obere Leitung (y_j), pad15 -> untere
        yo, yu = jp[n16][1], jp[n15][1]
        trk([(x16, y16), (x16, yo), (xr, yo), (xd, yo), (xd, dp[n16][1])], n16)
        trk([(x15, y15), (x15, yu), (xr, yu), (xd, yu), (xd, dp[n15][1])], n15)
    else:        # T2: pad16 (links) -> oben herum, pad15 (rechts) -> geradeaus, dann nach unten
        yo, yu = jp[n16][1], jp[n15][1]
        trk([(x16, y16), (x16, y16 - 1.45), (xr - 2.8, y16 - 1.45), (xr - 2.8, yo), (xr, yo), (xd, yo), (xd, dp[n16][1])], n16)
        trk([(x15, y15), (xr - 4.6, y15), (xr - 4.6, yu), (xr, yu), (xd, yu), (xd, dp[n15][1])], n15)
# Netzklassen/Kriechstrecken: Pro-Datei
daisy = sorted({n for t in by["Daisy_Stecker"] for pn, n in t["pins"].items() if n and t["pinnamen"][pn] in ("A", "B")})
import os
base = f"{OUT}/cmu_{V}"
b.Save(base + ".kicad_pcb")
ausg = sorted({n for t in teile for n in t['pins'].values() if n and (n[0] == 'D') and n[1:].isdigit()})
json.dump(dict(daisy_netze=daisy, ausgleich_netze=ausg, nicht_platziert=unplaced), open(f"{H}/layout_{V}_info.json", "w"))
print("Teile", len(b.GetFootprints()), "nicht platziert", unplaced, "Netze", len(nets), "Daisy", daisy)
