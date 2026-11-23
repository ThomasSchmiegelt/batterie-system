#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-23), Entwurf. Auftrag pm/AUFTRAG_WORKFLOW_V.md Punkt 5, docs/17 §3 (L6).
Vergleicht jede eingaben.json in sim/** mit dem aktuellen Stand und prüft CAD-Masse gegen Stückliste (> 2 % wird gemeldet).
Format eingaben.json:  {"name": {"wert": …, "quelle": "<Quelle>", "bt": "BT-xxx" (optional)}, "_variante": "LFP" (optional, Vorgabe LFP)}
Quellen:  parameter:<merkmal>   pm/bauteile/parameter_<V>.json (mit "bt" eindeutig, sonst muss das Merkmal eindeutig sein)
          cad:<schluessel>      cad/baukasten/ausgabe/ergebnis_<V>.json (oberste Ebene)
          stueckliste:<pos>     pm/bauteile/stueckliste_<V>.json, masse_ges_kg der Position
          annahme:<A_name>      cad/baukasten/annahmen*.json (datenblatt zuletzt)
          ergebnis:<pfad>#<schluessel>   beliebige Ergebnisdatei, Schlüssel punktgetrennt (Listenindex als Zahl)
          text:… oder andere     freie Quelle, nicht automatisch vergleichbar (wird als solche aufgelistet)
Aufruf:  python3 pm/masse_abgleich.py [ordner …]     rc 0 = nichts gefunden, rc 1 = Abweichungen."""
import json, sys
from pathlib import Path
R = Path(__file__).resolve().parents[1]; TOL_REL = 1e-6; TOL_MASSE = 0.02

def lade(p):
    return json.loads((R / p).read_text())

def pfad(d, schl):
    for k in str(schl).split("."):
        if isinstance(d, dict) and k in d: d = d[k]
        elif isinstance(d, list) and k.isdigit() and int(k) < len(d): d = d[int(k)]
        else: raise KeyError(schl)
    return d

def loese(quelle, var, bt):
    art, _, rest = quelle.partition(":")
    if art == "parameter":
        P = lade(f"pm/bauteile/parameter_{var}.json")["parameter"]
        c = {b: m[rest] for b, m in P.items() if rest in m and (bt is None or b == bt)}
        if not c: raise KeyError(f"Merkmal {rest} nicht in parameter_{var}.json")
        if len(c) > 1: raise KeyError(f"Merkmal {rest} mehrdeutig ({', '.join(c)}), „bt“ angeben")
        w = list(c.values())[0]["wert"]; return w
    if art == "cad": return lade(f"cad/baukasten/ausgabe/ergebnis_{var}.json")[rest]
    if art == "stueckliste":
        for p in lade(f"pm/bauteile/stueckliste_{var}.json")["positionen"]:
            if p["pos"] == rest: return p["masse_ges_kg"]
        raise KeyError(f"Position {rest} fehlt in stueckliste_{var}.json")
    if art == "annahme":
        w = None
        for n in ("annahmen.json", "annahmen_g5.json", "annahmen_datenblatt.json"):
            d = lade(f"cad/baukasten/{n}")
            if rest in d: w = d[rest]["wert"]
        if w is None: raise KeyError(f"{rest} nicht in cad/baukasten/annahmen*.json")
        return w
    if art == "ergebnis":
        f, _, s = rest.partition("#"); return pfad(lade(f), s)
    return "__frei__"

def gleich(a, b):
    if isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool):
        return abs(a - b) <= TOL_REL * max(abs(a), abs(b), 1e-12)
    return str(a).strip('"') == str(b).strip('"')

def eingaben_pruefen(f):
    meld = []; frei = 0; alt = 0; n_ok = 0
    d = json.loads(f.read_text()); var = d.get("_variante", "LFP")
    for n, e in d.items():
        if n.startswith("_"): continue
        if not (isinstance(e, dict) and "wert" in e and "quelle" in e): alt += 1; continue
        try: ist = loese(e["quelle"], e.get("variante", var), e.get("bt"))
        except Exception as ex: meld.append(f"  {n}: Quelle nicht auflösbar ({e.get('quelle')}): {ex}"); continue
        if ist == "__frei__": frei += 1; continue
        n_ok += 1
        if not gleich(e["wert"], ist):
            rel = f" ({(ist - e['wert']) / e['wert'] * 100:+.1f} %)" if isinstance(ist, (int, float)) and isinstance(e["wert"], (int, float)) and e["wert"] else ""
            meld.append(f"  {n}: Rechnung {e['wert']} gegen aktuell {ist}{rel}  [{e['quelle']}]")
    return meld, frei, alt, n_ok

def masse_pruefen():
    meld = []
    for v in ("LFP", "NMC"):
        try: c = lade(f"cad/baukasten/ausgabe/ergebnis_{v}.json"); s = lade(f"pm/bauteile/stueckliste_{v}.json")
        except Exception as ex: meld.append(f"{v}: Dateien nicht lesbar: {ex}"); continue
        sl = s["summen"]["masse_stueckliste_kg"]; ab = (c["masse_kg"] - sl) / sl
        if abs(ab) > TOL_MASSE: meld.append(f"{v} Gesamt: CAD {c['masse_kg']} kg gegen Stückliste {sl} kg ({ab*100:+.1f} %)")
        for p in c.get("positionen", []):
            a, b = p.get("masse_cad_kg"), p.get("masse_sl_kg")
            if not isinstance(a, (int, float)) or not isinstance(b, (int, float)) or not b: continue
            if abs(a - b) / b > TOL_MASSE: meld.append(f"{v} Pos {p['pos']} ({p['bt']}, {p['generator']}): CAD {a:.4g} kg gegen Stückliste {b:.4g} kg ({(a-b)/b*100:+.1f} %)")
    return meld

if __name__ == "__main__":
    ordner = [R / a for a in sys.argv[1:]] if sys.argv[1:] else sorted({p.parent for n_ in ("eingaben.json", "eingaben_graph.json") for p in (R / "sim").rglob(n_)})
    rc = 0
    for o in ordner:
      for f in ([o / "eingaben.json", o / "eingaben_graph.json"] if o.is_dir() else [o]):
        if not f.exists(): continue
        m, frei, alt, n_ok = eingaben_pruefen(f); rel = f.relative_to(R).parent / f.name
        zus = f" ({frei} freie Quelle, nicht vergleichbar)" if frei else ""
        if alt: zus += f" [{alt} Einträge im Altformat ohne wert/quelle, nicht prüfbar]"
        print(f"{rel}: {'ABWEICHUNG' if m else ('aktuell' if n_ok else 'nicht prüfbar')}{zus}")
        for z in m: print(z)
        rc |= bool(m)
    print("Masse CAD gegen Stückliste (Schwelle 2 %):")
    mm = masse_pruefen(); [print("  " + z) for z in mm] or None
    if not mm: print("  keine Abweichung über 2 %")
    sys.exit(1 if (rc or mm) else 0)
