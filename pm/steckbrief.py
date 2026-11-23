#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-23), Entwurf. Auftrag pm/AUFTRAG_WORKFLOW_V.md Punkt 4, docs/17 Tor T1 (L1).
Schreibt pm/steckbriefe/BT-xxx_<LFP|NMC>.md aus parameter_<V>.json, cad/baukasten/ausgabe/ergebnis_<V>.json,
pm/bauteile/stueckliste_<V>.json und struktur.json. Keine eigenen Werte; fehlt etwas, steht „nicht definiert“.
Aufruf: python3 pm/steckbrief.py BT-xxx [LFP|NMC]   (Vorgabe LFP)"""
import json, re, sys, datetime
from pathlib import Path
R = Path(__file__).resolve().parents[1]; ND = "nicht definiert"
def lade(p):
    f = R / p
    return json.loads(f.read_text()) if f.exists() else None

def main(bt, var):
    st = {b["id"]: b for b in lade("pm/bauteile/struktur.json")["bauteile"]}
    if bt not in st: sys.exit(f"{bt} nicht in pm/bauteile/struktur.json")
    b = st[bt]
    if b.get("varianten") and var not in b["varianten"]: print(f"Hinweis: {bt} gilt laut struktur.json nur für {b['varianten']}")
    par = (lade(f"pm/bauteile/parameter_{var}.json") or {}).get("parameter", {}).get(bt, {})
    cad = lade(f"cad/baukasten/ausgabe/ergebnis_{var}.json") or {}
    sl = lade(f"pm/bauteile/stueckliste_{var}.json") or {}
    kinder = [k for k in st.values() if k.get("eltern") == bt]
    ents = sorted({a for p in sl.get("positionen", []) if p["bt"] == bt for a in p.get("akten", [])})
    M = [f"| Dok.-Nr. | STB-{bt}-{var} | Version | 0.1 | Status | Entwurf |", "|---|---|---|---|---|---|",
         f"| Titel | Steckbrief {bt} {b['name']} ({var}) | Ersteller | Claude Sonnet (KI), pm/steckbrief.py | Prüfer | – (Opus, Mensch offen) |", "",
         f"> **KI-generiert.** Entwurf, nicht vom Menschen freigegeben. Erzeugt am {datetime.date.today().isoformat()}, nicht von Hand bearbeiten. Tor T1 nach docs/17.", "",
         f"## Stellung im Baum", f"- Bauteil: {bt} {b['name']}; Art: {b.get('art', ND)}; Rolle: {b.get('rolle', ND)}",
         f"- Elternbauteil: {b['eltern'] + ' ' + st[b['eltern']]['name'] if b.get('eltern') else 'keines (Wurzel)'}",
         f"- Kindbauteile: {', '.join(k['id'] + ' ' + k['name'] for k in kinder) or 'keine'}",
         f"- Anforderungen (struktur.json): {', '.join(b.get('anforderungen', [])) or ND}",
         f"- Varianten: {', '.join(b['varianten']) if b.get('varianten') else 'alle'}", "",
         f"## Merkmale aus pm/bauteile/parameter_{var}.json", "| Merkmal | Wert | Einheit | Akte |", "|---|---|---|---|"]
    for m in b.get("merkmale", {}):
        e = par.get(m, {}); w = e.get("wert")
        M.append(f"| {m} | {ND if w is None else str(w).strip(chr(34))} | {e.get('einheit') or ''} | {e.get('entscheidung') or ''} |")
    M += ["", f"## Anzahlen und Massen (Stückliste {sl.get('version', '?')}, CAD-Ausgabe)", "| Pos | Benennung | Menge Soll | Menge CAD | Masse Stückliste [kg] | Masse CAD [kg] | Stufe |", "|---|---|---|---|---|---|---|"]
    cp = {p["pos"]: p for p in cad.get("positionen", [])}; summe = 0; n = 0
    for p in sl.get("positionen", []):
        if p["bt"] != bt: continue
        c = cp.get(p["pos"], {}); n += 1
        if isinstance(p.get("masse_ges_kg"), (int, float)): summe += p["masse_ges_kg"]
        M.append(f"| {p['pos']} | {p['benennung']} | {p.get('menge_' + var, ND)} | {c.get('ist', ND)} | {p.get('masse_ges_kg', ND)} | {c.get('masse_cad_kg', ND)} | {c.get('stufe', p.get('geometrie', {}).get('detailstufe', ND))} |")
    if not n: M.append(f"| – | keine Stückliste-Position für {bt} in stueckliste_{var}.json | | | | | |")
    else: M.append(f"| | **Summe Stückliste** | | | **{summe:.5g}** | | |")
    M += ["", "## Querschnitte, Werkstoffe, Hinweise aus der Stückliste"]
    z = 0
    for p in sl.get("positionen", []):
        if p["bt"] != bt: continue
        M.append(f"- {p['pos']}: Werkstoff {p.get('werkstoff') or ND}; Herkunft Masse: {p.get('masse_quelle', ND)}")
        for f in ("bemerkung", "hinweis_opus"):
            if p.get(f): M.append(f"  - {f}: {p[f]}"); z += 1
    if not n: M.append(f"- {ND}")
    M += ["", "## Akten (aus der Stückliste)", ", ".join(ents) or ND, "",
          "## Quellen", f"`pm/bauteile/struktur.json`, `pm/bauteile/parameter_{var}.json`, `pm/bauteile/stueckliste_{var}.json`, `cad/baukasten/ausgabe/ergebnis_{var}.json` (CAD-Stand: Stückliste {cad.get('stueckliste_version', ND)}, {cad.get('teile', ND)} Teile)", "",
          "---", "*KI-generiert (Claude Sonnet, 2026-11-23). Status Entwurf. Freigabe nur durch den Autor.*"]
    o = R / "pm/steckbriefe" / f"{bt}_{var}.md"; o.parent.mkdir(exist_ok=True); o.write_text("\n".join(M) + "\n"); print(o.relative_to(R))

if __name__ == "__main__":
    if len(sys.argv) < 2: sys.exit(__doc__)
    v = sys.argv[2] if len(sys.argv) > 2 else "LFP"
    if v not in ("LFP", "NMC"): sys.exit("Variante LFP oder NMC")
    main(sys.argv[1], v)
