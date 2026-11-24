# KI-generiert (Claude Sonnet, 2026-11-24). Zeigt DRC-Verstöße mit Bauteil-Tag. Aufruf: python3 drc_zeigen.py <drc.json> [Typ ...]
import json, sys, re, collections
T = {t["ref"]: t["tag"] for t in json.load(open("/home/cae/hermes/batterie/sim/elektrik/e3c_bms_platine/bms_teile.json"))["teile"]}
d = json.load(open(sys.argv[1])); skip = set(sys.argv[2:])
print(collections.Counter(x["type"] for x in d["violations"]), "offen:", len(d["unconnected_items"]))
for x in d["violations"]:
    if x["type"] in ("silk_over_copper", "silk_overlap", "lib_footprint_issues"): continue
    if skip and x["type"] not in skip: continue
    its = []
    for i in x["items"]:
        m = re.search(r"Footprint (\w+)|of (\w+)|(\w+)\]", i["description"]); r = re.search(r"\b([A-Z]+\d+)\b", i["description"])
        its.append((T.get(r.group(1), r.group(1)) if r else "?", i["description"][:50], round(i["pos"]["x"], 1), round(i["pos"]["y"], 1)))
    print(x["type"], x["description"][:70], its)
