# KI-generiert (Claude Sonnet), Entwurf. Zusatz LFP_kap: Elektrodenflaeche auf Aktenkapazitaet 92,4 Ah skaliert (Faktor aus ergebnis.json), isotherm 25 C.
import json,copy
r=json.load(open("ergebnis.json"))["LFP"]; f=r["kapazitaet_ziel_Ah"]/r["kapazitaet_C20_Ah"]
s=open("zellmodell.py").read()
s=s.replace('H = json.load(open("eingaben.json")); out = {}','H = json.load(open("eingaben.json")); out = {}\nH["LFP_kap"]=copy.deepcopy(H["LFP"]); H["LFP_kap"]["elektrodenbreite_m"]*=%r; H["LFP_kap"]["kapazitaet_ziel_Ah"]=H["LFP"]["kapazitaet_ziel_Ah"]; H["zellvolumen_m3"]["LFP_kap"]=H["zellvolumen_m3"]["LFP"]'%f)
s=s.replace('"Prada2013" if v=="LFP"','"Prada2013" if v.startswith("LFP")').replace('for v in ("LFP","NMC"):','for v in ("LFP_kap",):').replace('"ergebnis.json"','"ergebnis_LFP_kap.json"').replace('import json,','import copy,json,')
s=s.replace('H = json.load','import copy\nH = json.load',1)
open("_kap_tmp.py","w").write(s); print("faktor",f)
exec(compile(s,"zellmodell_kap","exec"))
