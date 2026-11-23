#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-23), Entwurf. Abfragen auf pm/graph/graph.json nach pm/graph/SCHEMA.md.
    python3 pm/graph/frage.py folgen <ID>        was stromabwärts neu zu rechnen / zu prüfen ist
    python3 pm/graph/frage.py luecken            Lücken im Graphen
    python3 pm/graph/frage.py herkunft <ID>      stromaufwärts bis Quelle, Norm, Annahme, Vorgabe
    python3 pm/graph/frage.py norm <Regelwerk>   betroffene Anforderungen, Bauteile, Rechnungen
Option --json: Ausgabe als JSON. Kanten vom Typ erwaehnt sind schwach und stehen getrennt."""
import json, sys, re
from pathlib import Path
from collections import defaultdict, deque

R = Path(__file__).resolve().parents[2]
D = json.loads((R / "pm/graph/graph.json").read_text())
N = {n["id"]: n for n in D["nodes"]}
OUT, IN = defaultdict(list), defaultdict(list)
for e in D["edges"]:
    OUT[e["source"]].append((e["target"], e["typ"])); IN[e["target"]].append((e["source"], e["typ"]))


def pruefe_id(i):
    if i in N: return i
    c = [k for k in N if k.lower() == i.lower() or k.endswith("." + i)]
    if len(c) == 1: return c[0]
    sys.exit(f"ID {i} nicht im Graphen" + (f"; meinst du: {', '.join(c[:8])}" if c else ""))


def nachfolger(x):
    """(Ziel, Kante, Richtung) stromabwärts; erwaehnt wird nicht verfolgt."""
    for y, t in IN[x]:
        if t in ("verwendet", "legt_fest" if False else "verwendet"): yield y, "verwendet (rückwärts)"
        if t == "verifiziert_durch": yield y, "verifiziert_durch (rückwärts)"
        if t == "realisiert": yield y, "realisiert (rückwärts)"
        if t == "teil_von": yield y, "teil_von (rückwärts)"
    for y, t in OUT[x]:
        if t in ("erzeugt", "legt_fest", "hat_merkmal", "eingang_cad"): yield y, t
    for y, t in IN[x]:
        if t == "ersetzt": pass


def folgen(i):
    i = pruefe_id(i); seen = {i: None}; q = deque([i])
    while q:
        x = q.popleft()
        for y, t in nachfolger(x):
            if y not in seen: seen[y] = (x, t); q.append(y)
    schwach = sorted({y for x in seen for y, t in IN[x] if t == "erwaehnt" and N[y]["typ"] in ("Dokument",) and N[x]["typ"] == "Ergebnis"} - set(seen))
    def pfad(x):
        p = []
        while seen[x]: p.append(f"{seen[x][0]} --{seen[x][1]}--> {x}"); x = seen[x][0]
        return p[::-1]
    gr = lambda typ: sorted(k for k in seen if N[k]["typ"] == typ)
    ergs = [k for k in gr("Ergebnis")]
    res = dict(start=i, rechnungen=[k for k in gr("Rechnung") if k != i], anforderungen=gr("Anforderung"),
               bilder=[k for k in ergs if k.lower().endswith(".png")], ergebnisdateien=[k for k in ergs if not k.lower().endswith(".png")],
               merkmale=[k for k in gr("Merkmal") if k != i], stueckliste=gr("Stuecklistenposition"),
               dokumente_schwach=[d for d in schwach], pfade={k: pfad(k) for k in gr("Rechnung") if k != i})
    res["bausteine_schwach"] = [d for d in schwach if "bausteine/" in d]
    return res


def md_folgen(r):
    z = [f"# folgen {r['start']}", "", f"Typ: {N[r['start']]['typ']}. Stromabwärts über verwendet, erzeugt, verifiziert_durch, realisiert, teil_von (Schema Abfrage 1, mit eingang_cad).", "",
         f"## Neu zu rechnende Rechnungen ({len(r['rechnungen'])})"]
    for k in r["rechnungen"]: z.append(f"- `{k}`  (Weg: {r['pfade'][k][0] if len(r['pfade'][k]) == 1 else ' ; '.join(r['pfade'][k][:1] + ['…'] + r['pfade'][k][-1:])})")
    z += ["", f"## Betroffene Anforderungen ({len(r['anforderungen'])})"] + [f"- {k}: {N[k]['name']} ({N[k]['status']})" for k in r["anforderungen"]]
    z += ["", f"## Betroffene Bilder ({len(r['bilder'])})"] + [f"- `{k}`" for k in r["bilder"][:40]] + ([f"- … und {len(r['bilder'])-40} weitere"] if len(r["bilder"]) > 40 else [])
    z += ["", f"## Betroffene Ergebnisdateien ({len(r['ergebnisdateien'])})"] + [f"- `{k}`" for k in r["ergebnisdateien"][:40]] + ([f"- … und {len(r['ergebnisdateien'])-40} weitere"] if len(r["ergebnisdateien"]) > 40 else [])
    z += ["", f"## Weitere Merkmale / Stücklistenpositionen ({len(r['merkmale'])} / {len(r['stueckliste'])})"] + [f"- {k}" for k in r["merkmale"][:30]] + [f"- Pos {k}" for k in r["stueckliste"][:30]]
    z += ["", f"## Schwach (nur Textvorkommen eines Ergebnispfads, kein Beleg): Dokumente ({len(r['dokumente_schwach'])}), davon Folienbausteine ({len(r['bausteine_schwach'])})"]
    z += [f"- `{k}`" for k in r["dokumente_schwach"][:40]]
    return "\n".join(z)


def luecken():
    L = {}
    L["anforderung_ohne_verifiziert_durch"] = sorted(k for k, n in N.items() if n["typ"] == "Anforderung" and not any(t == "verifiziert_durch" for _, t in OUT[k]))
    L["rechnung_ohne_gehoert_zu"] = sorted(k for k, n in N.items() if n["typ"] == "Rechnung" and not any(t == "gehoert_zu" for _, t in OUT[k]))
    L["rechnung_ohne_gehoert_zu_hinweis_erwaehnt"] = {k: sorted(y for y, t in OUT[k] if t == "erwaehnt" and y.startswith("REQ-")) for k in L["rechnung_ohne_gehoert_zu"]}
    L["rechnung_ohne_verwendet"] = sorted(k for k, n in N.items() if n["typ"] == "Rechnung" and not any(t == "verwendet" for _, t in OUT[k]))
    L["entscheidung_ohne_belegt_durch"] = sorted(k for k, n in N.items() if n["typ"] == "Entscheidung" and not any(t == "belegt_durch" for _, t in OUT[k]))
    mo = sorted(k for k, n in N.items() if n["typ"] == "Merkmal" and not any(t == "legt_fest" for _, t in IN[k]))
    L["merkmal_ohne_legt_fest_von_rechnung_verwendet"] = [k for k in mo if any(t == "verwendet" for _, t in IN[k])]
    L["merkmal_ohne_legt_fest_mit_wert"] = [k for k in mo if json.loads(json.dumps(N[k])).get("wert") not in (None, "null") or N[k].get("wert_LFP") or N[k].get("wert_NMC")]
    L["merkmal_ohne_legt_fest_gesamt"] = mo
    k_ = []
    for a, n in N.items():
        if n["typ"] == "Anforderung" and str(n.get("status", "")).startswith("verfehlt"):
            for y, t in OUT[a]:
                if t == "kriterium_aus" and N[y]["typ"] == "Annahme": k_.append((a, y))
    L["verfehlt_mit_annahme_kriterium"] = [{"anforderung": a, "annahme": y} for a, y in k_]
    L["unaufgeloest"] = D["unaufgeloest"]
    return L


def md_luecken(L):
    z = ["# luecken", ""]
    def sek(t, items, fmt=lambda x: f"- {x}", n=60):
        z.append(f"## {t} ({len(items)})"); z.extend(fmt(x) for x in items[:n])
        if len(items) > n: z.append(f"- … und {len(items)-n} weitere (siehe --json)")
        z.append("")
    sek("Anforderung ohne verifiziert_durch", L["anforderung_ohne_verifiziert_durch"], lambda k: f"- {k}: {N[k]['name']} ({N[k]['status']})")
    sek("Rechnung ohne gehoert_zu (keine ERWARTUNG mit Abschnitt „Anforderung“; Hinweis: erwähnte REQ)", L["rechnung_ohne_gehoert_zu"], lambda k: f"- `{k}`  erwähnt: {', '.join(L['rechnung_ohne_gehoert_zu_hinweis_erwaehnt'][k]) or '–'}")
    sek("Rechnung ohne verwendet-Kante (eingaben.json fehlt oder ohne Präfixformat; Zusatzprüfung, nicht im Schema)", L["rechnung_ohne_verwendet"], lambda k: f"- `{k}`")
    sek("Entscheidung ohne belegt_durch", L["entscheidung_ohne_belegt_durch"], lambda k: f"- {k}: {N[k]['name']} ({N[k]['status']})")
    sek("Merkmal ohne legt_fest, das eine Rechnung verwendet (stärkste Lücke: Rechnung nutzt Wert ohne Akte)", L["merkmal_ohne_legt_fest_von_rechnung_verwendet"])
    sek("Merkmal ohne legt_fest, aber mit Wert in parameter*.json", L["merkmal_ohne_legt_fest_mit_wert"])
    z.append(f"## Merkmal ohne legt_fest gesamt: {len(L['merkmal_ohne_legt_fest_gesamt'])} von {sum(1 for n in N.values() if n['typ'] == 'Merkmal')}\n")
    sek("Anforderung „verfehlt“, deren Kriterium eine Annahme ist", L["verfehlt_mit_annahme_kriterium"], lambda x: f"- {x['anforderung']} → {x['annahme']} ({N[x['annahme']].get('name', '')})")
    sek("Unaufgelöste Kanten (Ziel nicht vorhanden)", L["unaufgeloest"], lambda x: f"- {x['kante']}: {x['von']} → {x['nach']}")
    return "\n".join(z)


def herkunft(i):
    i = pruefe_id(i); seen = {i: None}; q = deque([i]); ende = {"Quelle", "Norm", "Annahme", "Vorgabe"}
    while q:
        x = q.popleft()
        if N[x]["typ"] in ende and x != i: continue
        nxt = []
        for y, t in OUT[x]:
            if t in ("kriterium_aus", "belegt_durch", "verwendet", "verifiziert_durch", "ersetzt", "erfuellt_beitrag" if False else "kriterium_aus"): nxt.append((y, t))
        for y, t in IN[x]:
            if t in ("legt_fest", "erzeugt"): nxt.append((y, t + " (rückwärts)"))
        for y, t in nxt:
            if y not in seen: seen[y] = (x, t); q.append(y)
    zeilen = []
    for k in seen:
        if seen[k]: zeilen.append((k, seen[k][0], seen[k][1]))
    wurzeln = sorted(k for k in seen if N[k]["typ"] in ende)
    return dict(start=i, wurzeln=[{"id": k, "typ": N[k]["typ"]} for k in wurzeln], kanten=[dict(von=a, nach=b, kante=c) for b, a, c in zeilen])


def md_herkunft(r):
    z = [f"# herkunft {r['start']}", "", f"Endpunkte (Quelle, Norm, Annahme, Vorgabe): {len(r['wurzeln'])}", ""]
    for w in r["wurzeln"]: z.append(f"- {w['typ']}: {w['id']}")
    z += ["", "## Kanten (von → nach, stromaufwärts)"] + [f"- {k['von']} --{k['kante']}--> {k['nach']}" for k in r["kanten"][:120]]
    return "\n".join(z)


def norm(s):
    c = [k for k, n in N.items() if n["typ"] == "Norm" and s.lower() in k.lower()]
    if not c: sys.exit(f"Kein Regelwerk mit „{s}“ in docs/07 (Normknoten: {', '.join(k for k, n in N.items() if n['typ'] == 'Norm')[:300]})")
    quellen = sorted({w for k in c for w in json.loads(N[k]["recherche"])}) if all(isinstance(N[k].get("recherche"), str) for k in c) else []
    direkt = sorted({a for k in c for a, t in IN[k] if t == "kriterium_aus"} | {a for w in quellen if w in N for a, t in IN[w] if t == "kriterium_aus"})
    bt = sorted(b for b, n in N.items() if n["typ"] == "Bauteil" and set(direkt) & set(json.loads(n.get("anforderungen", "[]"))))
    ents = sorted({e for a in direkt for e, t in IN[a] if t == "erfuellt_beitrag"})
    rech = sorted({r for a in direkt for r, t in IN[a] if t == "gehoert_zu"})
    rech_schwach = sorted({r for a in direkt for r, t in IN[a] if t == "erwaehnt" and N[r]["typ"] == "Rechnung"})
    return dict(regelwerke=c, quellen=quellen, anforderungen=direkt, bauteile=bt, entscheidungen=ents, rechnungen=rech, rechnungen_schwach=rech_schwach)


def md_norm(r):
    z = [f"# norm", "", "Regelwerke: " + "; ".join(r["regelwerke"]), "Recherche (docs/07): " + ", ".join(r["quellen"]), ""]
    for t, k in (("Anforderungen (kriterium_aus direkt oder über Quelle Wxx)", "anforderungen"), ("Bauteile (Feld anforderungen in struktur.json)", "bauteile"), ("Entscheidungen (erfuellt_beitrag)", "entscheidungen"), ("Rechnungen (gehoert_zu)", "rechnungen"), ("Rechnungen schwach (Text erwähnt die REQ)", "rechnungen_schwach")):
        z += [f"## {t} ({len(r[k])})"] + [f"- {x}" for x in r[k]] + [""]
    return "\n".join(z)


if __name__ == "__main__":
    a = sys.argv[1:]; j = "--json" in a
    a = [x for x in a if x != "--json"]
    if not a: print(__doc__); sys.exit(0)
    cmd = a[0]
    if cmd == "folgen" and len(a) > 1: r = folgen(a[1]); md = md_folgen
    elif cmd == "luecken": r = luecken(); md = md_luecken
    elif cmd == "herkunft" and len(a) > 1: r = herkunft(a[1]); md = md_herkunft
    elif cmd == "norm" and len(a) > 1: r = norm(" ".join(a[1:])); md = md_norm
    else: print(__doc__); sys.exit(1)
    print(json.dumps(r, ensure_ascii=False, indent=1) if j else md(r))
