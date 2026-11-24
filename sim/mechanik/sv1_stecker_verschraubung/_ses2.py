import pcbnew
D="/home/cae/cae_projekte/batterie/e3/route"
b=pcbnew.LoadBoard(f"{D}/alt_vor_sv1/cmu_LFP.kicad_pcb")
print("ALT", pcbnew.ImportSpecctraSES(b,f"{D}/alt_vor_sv1/cmu_LFP.ses"))
