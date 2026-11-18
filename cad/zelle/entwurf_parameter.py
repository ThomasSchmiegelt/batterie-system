#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. Auftrag G2.
Wie `pm.py parameter`, nimmt aber auch Akten mit Status "vorgeschlagen". Schreibt cad/zelle/entwurf/parameter_<V>_entwurf.json.
Ändert keine Datei in pm/. Kopf: ENTWURF, nicht freigegeben."""
import sys, json
from pathlib import Path
R = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(R / "pm"))
import pm as P

def ok(e):
    s = str(e.get("status", ""))
    return (s.startswith("entschieden") or s.startswith("vorgeschlagen")) and e.get("merkmal") not in (None, "-")

def main():
    bt = P.struktur(); ers = {e.get("ersetzt") for e in P.alle()}; V = P.varianten()
    akten = [e for e in P.alle() if ok(e) and e["id"] not in ers]
    out_dir = R / "cad" / "zelle" / "entwurf"; out_dir.mkdir(parents=True, exist_ok=True)
    for v in V:
        out = {b: {m: {"wert": None, "entscheidung": None} for m in d["merkmale"]} for b, d in bt.items()}
        # gemeinsame Akten zuerst, dann variantenbezogene
        for gruppe in (False, True):
            for e in akten:
                if bool(e.get("variante")) != gruppe: continue
                if gruppe and v not in P.vset(e): continue
                for b in e.get("bauteile") or []:
                    d = {"wert": e.get("wert"), "einheit": e.get("einheit"), "entscheidung": e["id"], "status": e.get("status")}
                    if gruppe: d["variante"] = v
                    out[b][e["merkmal"]] = d
        f = out_dir / f"parameter_{v}_entwurf.json"
        f.write_text(json.dumps({"hinweis": "ENTWURF, nicht freigegeben. KI-generiert, erzeugt von cad/zelle/entwurf_parameter.py aus Akten mit Status entschieden und vorgeschlagen.", "parameter": out}, indent=1, ensure_ascii=False))
        print(f.relative_to(R))
main()
