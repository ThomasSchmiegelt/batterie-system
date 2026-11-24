# Im KiCad-Flatpak: ergebnis_aktualisieren.py <V>... KI-generiert (Claude Sonnet, 2026-11-24), Entwurf.
# Schreibt Teile, Bahnen, Vias, DRC, Länge in ergebnis_platine.json[V] aus cmu_<V>.kicad_pcb, cmu_<V>_drc.json, cmu_<V>_teile.json.
import sys, json, pcbnew, os
H = "/home/cae/hermes/batterie/sim/elektrik/e3_platine"; O = "/home/cae/cae_projekte/batterie/e3"
P = json.load(open(f"{H}/ergebnis_platine.json"))
for V in sys.argv[1:]:
    b = pcbnew.LoadBoard(f"{O}/cmu_{V}.kicad_pcb"); d = json.load(open(f"{O}/cmu_{V}_drc.json")); t = json.load(open(f"{H}/cmu_{V}_teile.json"))
    tr = [x for x in b.GetTracks()]; vias = [x for x in tr if x.GetClass() == "PCB_VIA"]; bahn = [x for x in tr if x.GetClass() == "PCB_TRACK"]
    bb = b.GetBoardEdgesBoundingBox(); L = round(bb.GetWidth() / 1e6 - 0.1, 1); Bm = round(bb.GetHeight() / 1e6 - 0.1, 1)
    kl = {}
    for x in t["teile"]: kl[x["name"]] = kl.get(x["name"], 0) + 1
    P[V].update(laenge_mm=L, breite_mm=Bm, teile=len(t["teile"]), leiterbahnen=len(bahn), vias=len(vias), drc_verstoesse=len(d["violations"]), drc_unverbunden=len(d["unconnected_items"]),
                drc_typen=sorted({x["type"] for x in d["violations"]}), teile_je_klasse=kl)
    print(V, L, Bm, len(t["teile"]), len(bahn), len(vias), len(d["violations"]), len(d["unconnected_items"]))
json.dump(P, open(f"{H}/ergebnis_platine.json", "w"), indent=1, ensure_ascii=False)
