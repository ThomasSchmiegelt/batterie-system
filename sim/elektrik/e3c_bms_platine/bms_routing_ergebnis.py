#!/usr/bin/env python3
"""Fasst die Freerouting-Läufe (fr<N>.log) und das endgültige DRC zusammen -> ergebnis_routing.json. KI-generiert (Claude Sonnet, 2026-11-24)."""
import re, json, pathlib
O = pathlib.Path("/home/cae/cae_projekte/batterie/e3c/route"); H = pathlib.Path(__file__).resolve().parent
beschr = {1: "In1 und In2 als Fläche (GND, +3V3, HV_GND, HV_VDD) und als Signallage", 2: "In1 und In2 nur Fläche (Typ power)", 3: "In1 nur Fläche (GND/HV_GND), In2 Signal ohne Fläche", 4: "In1 Signal und Fläche GND/HV_GND, In2 Signal (Entkopplung 3,2 mm)",
          5: "wie 4, Entkopplung 4,0 mm vom Pad (übernommen)", 6: "wie 3, -mp 40"}
L = {}
for n in range(1, 7):
    f = O / f"fr{n}.log"
    if not f.exists(): continue
    t = f.read_text(errors="ignore"); m = re.findall(r"Auto-routing stage completed: started with (\d+) unrouted nets, completed in ([\d.]+) seconds, final score: ([\d.]+) \((\d+) unrouted and (\d+) violations\)", t)
    if m: a, s, sc, u, v = m[-1]; L[f"lauf{n}"] = dict(beschreibung=beschr[n], start_unverbunden=int(a), offen=int(u), verletzungen=int(v), router_s=float(s), score=float(sc))
d = json.load(open(O / "chk_drc2.json")); L["endstand"] = dict(lauf="lauf5 + B.Cu-Massefläche", drc_verstoesse=len(d["violations"]), drc_unverbunden=len(d["unconnected_items"]))
json.dump(dict(laeufe=L, quelle="/home/cae/cae_projekte/batterie/e3c/route/fr<N>.log, chk_drc2.json"), open(H / "ergebnis_routing.json", "w"), indent=1, ensure_ascii=False); print(json.dumps(L, ensure_ascii=False)[:900])
