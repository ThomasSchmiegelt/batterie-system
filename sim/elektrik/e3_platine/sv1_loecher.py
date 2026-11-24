# Im KiCad-Flatpak: sv1_loecher.py <V> entfernt|setzen <datei>. KI-generiert (Claude Sonnet, 2026-11-24), Entwurf. SV1: NPTH-Bohrungen MH1..MH4 (Ø 3,2) aus einer Platine nehmen bzw. wieder setzen.
# Grund: Der Specctra-SES-Import von KiCad scheitert (Rückgabe False), wenn das Board Bauteile ohne Pads (NPTH) enthält. Routing und Import laufen daher ohne die Bohrungen, danach werden sie wieder gesetzt. Werte wie pcb_bauen.py.
import sys, pcbnew
V, m, F = sys.argv[1], sys.argv[2], sys.argv[3]; b = pcbnew.LoadBoard(F); mm = pcbnew.FromMM
L, B, BD, RA = 120.0, 60.0, 3.2, 2.8
if m == "entfernt":
    for f in list(b.GetFootprints()):
        if f.GetReference().startswith("MH"): b.Remove(f)
else:
    for k_, (hx, hy) in enumerate(((RA, RA), (L - RA, RA), (RA, B - RA), (L - RA, B - RA))):
        fp = pcbnew.FOOTPRINT(b); fp.SetReference(f"MH{k_ + 1}"); fp.SetValue("M3_Bohrung_3.2"); fp.Reference().SetVisible(False); fp.Value().SetVisible(False)
        pd = pcbnew.PAD(fp); pd.SetAttribute(pcbnew.PAD_ATTRIB_NPTH); pd.SetShape(pcbnew.PAD_SHAPE_CIRCLE); pd.SetSize(pcbnew.VECTOR2I(mm(BD), mm(BD))); pd.SetDrillSize(pcbnew.VECTOR2I(mm(BD), mm(BD)))
        pd.SetLayerSet(pcbnew.LSET.AllCuMask()); pd.SetNumber(""); fp.Add(pd); fp.SetPosition(pcbnew.VECTOR2I(mm(hx), mm(hy))); b.Add(fp)
pcbnew.SaveBoard(F, b); print(m, len(b.GetFootprints()))
