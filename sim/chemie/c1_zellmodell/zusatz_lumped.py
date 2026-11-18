# KI-generiert (Claude Sonnet), Entwurf. Zusatzlauf NMC lumped (Chen2020 hat Thermikparameter, Prada2013 nicht).
import re,sys
s=open("zellmodell.py").read().replace('TH = "isothermal"','TH = "lumped"').replace('for v in ("LFP","NMC"):','for v in ("NMC",):').replace('"ergebnis.json"','"ergebnis_NMC_lumped.json"')
exec(compile(s,"zellmodell_lumped","exec"))
