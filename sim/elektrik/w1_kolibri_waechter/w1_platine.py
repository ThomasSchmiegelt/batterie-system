# Im KiCad-Flatpak (werkzeuge/kicad-python.sh). KI-generiert (Claude Sonnet, 2026-11-25), Entwurf. W1 (ERW-W1).
# Aufrufe:
#   w1_platine.py bereit <start.kicad_pcb> <ziel.kicad_pcb> <variante>   Bohrungen und alte Sperrflächen entfernen, Sperrflächen der Variante setzen (ohne Bohrungen, sonst scheitert der SES-Import, siehe SV1 sv1_loecher.py), DSN exportieren
#   w1_platine.py ses <ziel.kicad_pcb> <datei.ses> <geroutet.kicad_pcb> <variante>   SES importieren, Bohrungen der Variante wieder setzen, speichern
# Maße der Bohrung wie pcb_bauen.py (SV1): Durchmesser 3,2 mm, Kupferabstand 2,0 mm, Randabstand 2,8 mm (Mitte), Platine 120 x 60.
# Die Hilfsskripte ecken.py / edit_pcb.py aus SV1 lagen nicht mehr unter /tmp/claude-1003/SV1/. Die Lage der Variantenbohrungen unten ist eine ANNAHME von W1 (siehe ERGEBNIS.md), sie folgt der Beschreibung in ERWARTUNG.md.
import sys, math, pcbnew
mm = pcbnew.FromMM
L, B, BD, RA, KA = 120.0, 60.0, 3.2, 2.8, 2.0
VERSATZ_INNEN = 2.0   # B4v: je 2 mm nach innen (ERWARTUNG.md)

def lagen(v):
    if v == "B4":  return [(RA, RA), (L - RA, RA), (RA, B - RA), (L - RA, B - RA)]
    if v == "B4v": r = RA + VERSATZ_INNEN; return [(r, r), (L - r, r), (r, B - r), (L - r, B - r)]
    if v == "B3":  return [(RA, RA), (RA, B - RA), (L - RA, B / 2)]   # 2 Ecken links + Mitte der gegenüberliegenden (rechten) Kante
    if v == "B2K": return [(RA, RA), (L - RA, B - RA)]                # 2 Bohrungen diagonal; die Klemmleiste im Rahmen ist Annahme, nicht modelliert
    raise SystemExit("Variante unbekannt " + v)

def sperre(b, hx, hy):
    z = pcbnew.ZONE(b); z.SetIsRuleArea(True); z.SetDoNotAllowTracks(True); z.SetDoNotAllowVias(True); z.SetDoNotAllowZoneFills(True)
    z.SetLayerSet(pcbnew.LSET.AllCuMask()); o = z.Outline(); o.NewOutline()
    for i in range(24): o.Append(mm(hx + (BD / 2 + KA) * math.cos(2 * math.pi * i / 24)), mm(hy + (BD / 2 + KA) * math.sin(2 * math.pi * i / 24)))
    h = o.NewHole(0)
    for i in range(24): o.Append(mm(hx + (BD / 2 + 0.1) * math.cos(2 * math.pi * i / 24)), mm(hy + (BD / 2 + 0.1) * math.sin(2 * math.pi * i / 24)), 0, h)
    b.Add(z)

def bohrung(b, k, hx, hy):
    fp = pcbnew.FOOTPRINT(b); fp.SetReference(f"MH{k}"); fp.SetValue("M3_Bohrung_3.2"); fp.Reference().SetVisible(False); fp.Value().SetVisible(False)
    pd = pcbnew.PAD(fp); pd.SetAttribute(pcbnew.PAD_ATTRIB_NPTH); pd.SetShape(pcbnew.PAD_SHAPE_CIRCLE); pd.SetSize(pcbnew.VECTOR2I(mm(BD), mm(BD))); pd.SetDrillSize(pcbnew.VECTOR2I(mm(BD), mm(BD)))
    pd.SetLayerSet(pcbnew.LSET.AllCuMask()); pd.SetNumber(""); fp.Add(pd); fp.SetPosition(pcbnew.VECTOR2I(mm(hx), mm(hy))); b.Add(fp)

# Entfernen von MH-Bohrungen und Sperrflächen macht der Wächter vorher per Textbearbeitung (kolibri_waechter_cmu.strip_pcb): b.Remove() stürzt in diesem KiCad-swig beim anschließenden Speichern ab (Segfault 139, 2026-11-25).

m = sys.argv[1]
if m == "bereit":
    src, dst, v = sys.argv[2:5]
    b = pcbnew.LoadBoard(src)
    for (hx, hy) in lagen(v): sperre(b, hx, hy)
    pcbnew.SaveBoard(dst, b); b = pcbnew.LoadBoard(dst)
    print("DSN", pcbnew.ExportSpecctraDSN(b, dst.replace(".kicad_pcb", ".dsn")), "Sperrflaechen", len(lagen(v)))
elif m == "ses":
    pcb, ses, out, v = sys.argv[2:6]
    b = pcbnew.LoadBoard(pcb); ok = pcbnew.ImportSpecctraSES(b, ses); print("SES", ok)
    for k, (hx, hy) in enumerate(lagen(v), 1): bohrung(b, k, hx, hy)
    pcbnew.SaveBoard(out, b); print("Bohrungen", len(lagen(v)))
