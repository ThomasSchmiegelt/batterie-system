import pcbnew
b=pcbnew.LoadBoard("/home/cae/cae_projekte/batterie/e3/cmu_LFP.kicad_pcb")
for r in ("T1","T2","J6","J7","D1","D2"):
    f=b.FindFootprintByReference(r)
    print(r,f.GetPosition().x/1e6,f.GetPosition().y/1e6,[(p.GetNumber(),round(p.GetPosition().x/1e6,2),round(p.GetPosition().y/1e6,2),p.GetNetname()) for p in f.Pads()])
