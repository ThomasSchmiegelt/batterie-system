# Im KiCad-Flatpak: thermovias.py <V> <Anzahl je Paar>. Nachtrag 6: Vias im eigenen Netz der Widerstandspads (je Pad N/4 Vias längs des Pads, 0,6/0,3 mm),
# je Netz und Paar eine B.Cu-Kupferfläche unter den Pads dieses Netzes (Abstand zwischen den Flächen und zu fremdem Kupfer >= 0,2 mm). KI-generiert (Claude Sonnet, 2026-11-24), ENT-187.
import sys, math, json, pcbnew
V, N = sys.argv[1], int(sys.argv[2]); F = f"/home/cae/cae_projekte/batterie/e3/cmu_{V}.kicad_pcb"
b = pcbnew.LoadBoard(F); mm = pcbnew.FromMM

# Engstelle: zwei Innenlagen-Leiterbahnen (beide horizontal) lassen unter der Padreihe weniger als 0,6 + 2*0,2 mm Platz (Lücke 0,9945 mm statt 1,0 mm).
# Beide werden um je <= 11 µm auseinandergeschoben (Endpunkte bleiben im Kupfer der Anschlüsse), keine Annahme, DRC prüft.
segs = [t for t in b.Tracks() if t.Type() != pcbnew.PCB_VIA_T and t.GetLayer() in (pcbnew.In1_Cu, pcbnew.In2_Cu) and t.GetStart().y == t.GetEnd().y]
nudged = []
for f in b.GetFootprints():
    if "R_2512" not in str(f.GetFPID().GetLibItemName()): continue
    for p in f.Pads():
        py_ = p.GetPosition().y / 1e6; px_ = p.GetPosition().x / 1e6
        near = sorted([t for t in segs if abs(t.GetStart().y / 1e6 - py_) < 1.5 and min(t.GetStart().x, t.GetEnd().x) / 1e6 < px_ < max(t.GetStart().x, t.GetEnd().x) / 1e6], key=lambda t: t.GetStart().y)
        for lo, hi in zip(near, near[1:]):
            gap = (hi.GetStart().y - lo.GetStart().y) / 1e6 - lo.GetWidth() / 2e6 - hi.GetWidth() / 2e6
            if lo.GetLayer() == hi.GetLayer() and 0.9 < gap < 1.0 and lo.GetNetname() != hi.GetNetname() and lo.m_Uuid.AsString() not in nudged:
                d = int((1.0 + 0.016 - gap) / 2 * 1e6) + 1
                for t, sg in ((lo, -1), (hi, 1)):
                    t.SetStart(pcbnew.VECTOR2I(t.GetStart().x, t.GetStart().y + sg * d)); t.SetEnd(pcbnew.VECTOR2I(t.GetEnd().x, t.GetEnd().y + sg * d)); nudged.append(t.m_Uuid.AsString())
                print("Engstelle gelöst", lo.GetNetname(), hi.GetNetname(), "Lücke vorher", round(gap, 4), "Verschiebung je", d, "nm")
items = []   # (typ, netname, geom)
for t in b.Tracks():
    if t.Type() == pcbnew.PCB_VIA_T: items.append(("via", t.GetNetname(), (t.GetPosition().x / 1e6, t.GetPosition().y / 1e6, t.GetWidth(pcbnew.F_Cu) / 2e6)))
    else: items.append(("seg", t.GetNetname(), (t.GetStart().x / 1e6, t.GetStart().y / 1e6, t.GetEnd().x / 1e6, t.GetEnd().y / 1e6, t.GetWidth() / 2e6)))
pads = []
for f in b.GetFootprints():
    for p in f.Pads(): pads.append((f.GetReference(), p.GetNumber(), p.GetNetname(), p.GetPosition().x / 1e6, p.GetPosition().y / 1e6, p.GetBoundingBox().GetWidth() / 2e6, p.GetBoundingBox().GetHeight() / 2e6))
def dseg(px, py, s):
    x1, y1, x2, y2, w = s; dx, dy = x2 - x1, y2 - y1; L = dx * dx + dy * dy
    u = 0 if L == 0 else max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / L)); return math.hypot(px - x1 - u * dx, py - y1 - u * dy) - w
RV = 0.3   # Via-Radius, 0,225 nur als Ausnahme (Opus, Frage 9)
def frei(x, y, net, placed):
    for typ, n, g in items:
        if typ == "via" and math.hypot(x - g[0], y - g[1]) < 0.7: return False
        if n == net: continue
        if typ == "seg" and dseg(x, y, g) < RV + 0.2 - 3e-6: return False
        if typ == "via" and math.hypot(x - g[0], y - g[1]) - g[2] < RV + 0.2 - 3e-6: return False
    for ref, num, n, px, py, sx, sy in pads:
        if n == net: continue
        if abs(x - px) < sx + RV + 0.2 and abs(y - py) < sy + RV + 0.2: return False
    return all(math.hypot(x - a, y - c) >= 0.8 or nn == net and False for a, c, nn, _d in placed) if False else all(math.hypot(x - a, y - c) >= 0.7 for a, c, nn, _d in placed)
res = sorted([f for f in b.GetFootprints() if "R_2512" in str(f.GetFPID().GetLibItemName())], key=lambda f: (f.GetPosition().x, f.GetPosition().y))
n_pad = N // 4; placed = []; fehl = 0; netpads = {}   # (Paar-Id, Netz) -> Pads
for f in res:
    for p in f.Pads():
        net = p.GetNetname(); px, py = p.GetPosition().x / 1e6, p.GetPosition().y / 1e6; sx, sy = p.GetBoundingBox().GetWidth() / 2e6, p.GetBoundingBox().GetHeight() / 2e6
        key = net; netpads.setdefault(key, []).append((px, py, sx, sy))
        # Kandidaten längs der langen Padachse
        long_y = sy >= sx; cs = sorted(((dx, dy) for dx in ([i * 0.01 for i in range(-90, 91)] if long_y else [i * 0.1 for i in range(-16, 17)]) for dy in ([i * 0.1 for i in range(-16, 17)] if long_y else [i * 0.01 for i in range(-90, 91)])), key=lambda q: abs(q[0]) + abs(q[1]))
        k = 0
        for RV_, dv in ((0.3, 0.6), (0.225, 0.45)):
          RV = RV_
          for dx, dy in cs:
            if k >= n_pad: break
            x, y = px + dx, py + dy
            if abs(dx) > sx - RV + 1e-9 and not long_y or abs(dy) > sy - RV + 1e-9 and long_y:
                if not (dv < 0.5 and (abs(dy) <= sy + 0.17 and not long_y or abs(dx) <= sx + 0.17 and long_y) and abs(dx) <= sx - RV + 1e-9): continue   # kleine Via darf mit Rand ins Pad ragen (Überlappung >= 0,05 mm)   # Via-Mitte so, dass der Via-Rand im Pad bleibt
            if not frei(x, y, net, placed): continue
            placed.append((x, y, net, dv)); k += 1
        fehl += n_pad - k
        if k < n_pad: print('Fehlt', f.GetReference(), p.GetNumber(), net, k, 'pad', round(px,2), round(py,2), round(sx,2), round(sy,2))
for (x, y, net, dv) in placed:
    v = pcbnew.PCB_VIA(b); v.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y))); v.SetWidth(mm(dv)); v.SetDrill(mm(0.3 if dv > 0.5 else 0.2)); v.SetViaType(pcbnew.VIATYPE_THROUGH); v.SetNet(b.FindNet(net)); b.Add(v)
# B.Cu-Flächen: je Netz ein Rechteck um die Pads und Vias dieses Netzes (je Widerstandspaar = Netz, da Paar parallel an T_k bzw. D_k)
zn = 0
for net, ps in netpads.items():
    if not any(n == net for _, _, n, _d in placed): print('Keine Fläche (kein Via möglich):', net); continue
    xs = [p[0] - p[2] for p in ps] + [p[0] + p[2] for p in ps]; ys = [p[1] - p[3] for p in ps] + [p[1] + p[3] for p in ps]
    x0, x1, y0, y1 = min(xs) - 0.2, max(xs) + 0.2, min(ys) - 0.2, max(ys) + 0.2
    z = pcbnew.ZONE(b); ls_ = pcbnew.LSET(); ls_.AddLayer(pcbnew.B_Cu); z.SetLayerSet(ls_); z.SetNet(b.FindNet(net)); z.SetLocalClearance(mm(0.2)); z.SetMinThickness(mm(0.15)); z.SetPadConnection(pcbnew.ZONE_CONNECTION_FULL); z.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_ALWAYS)
    o = z.Outline(); o.NewOutline()
    for (a, c) in ((x0, y0), (x1, y0), (x1, y1), (x0, y1)): o.Append(mm(a), mm(c))
    b.Add(z); zn += 1
pcbnew.ZONE_FILLER(b).Fill(b.Zones())
pcbnew.SaveBoard(F, b)
json.dump(dict(vias_klein_0_45=sum(1 for q in placed if q[3] < 0.5), widerstaende=len(res), vias_gesetzt=len(placed), vias_soll=len(res) * n_pad * 2 // 2 * 2 // 1 // 1 if False else len(res) * N // 2, fehlend=len(res) * N // 2 - len(placed), flaechen_bcu=zn), open(f"/home/cae/hermes/batterie/sim/elektrik/e3_platine/thermovias_{V}.json", "w"))
print("Vias", len(placed), "von", len(res) * N // 2, "Flächen", zn)
