import pcbnew,sys
D="/home/cae/cae_projekte/batterie/e3/route"
m=sys.argv[1]
b=pcbnew.LoadBoard(f"{D}/cmu_LFP.kicad_pcb")
if 'z' in m:
    for z in list(b.Zones()): b.Remove(z)
if 'h' in m:
    for f in list(b.GetFootprints()):
        if f.GetReference().startswith("H"): b.Remove(f)
print(m, pcbnew.ImportSpecctraSES(b,f"{D}/cmu_LFP.ses"))
