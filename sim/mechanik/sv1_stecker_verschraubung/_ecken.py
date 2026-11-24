import pcbnew, math
b = pcbnew.LoadBoard("/home/cae/cae_projekte/batterie/e3/cmu_LFP_ungeroutet.kicad_pcb")
L,B=120,60
for ins in (2.8,3.0,3.2,3.5,4.0):
  out=[]
  for (cx,cy) in ((ins,ins),(ins,B-ins)):
    m=9e9
    for f in b.GetFootprints():
      for p in f.Pads():
        bb=p.GetBoundingBox(); x0,x1,y0,y1=bb.GetLeft()/1e6,bb.GetRight()/1e6,bb.GetTop()/1e6,bb.GetBottom()/1e6
        dx=max(x0-cx,0,cx-x1); dy=max(y0-cy,0,cy-y1); d=math.hypot(dx,dy)
        if d<m: m=d; r=f.GetReference()
    out.append((round(m,2),r))
  print(ins,out)
