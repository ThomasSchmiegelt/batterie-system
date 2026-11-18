"""KI-generiert, geändert 2026-11-16 Sonnet (Variante in Akten-Notizen, Tag #variante/V, AUFTRAG_VARIANTEN; Bauteilnotizen für alle Bauteile aus struktur.json, AUFTRAG_LFP_UMSTELLUNG).
wissensnetz_obsidian.py -- erzeugt aus pm/plan/wissensnetz.json eine Obsidian-Notizsammlung unter wissen/.

KI-generiert. Vault-Wurzel ist das Projektverzeichnis; erzeugt wird nur wissen/ (plus .obsidian/-Schlüssel, .gitignore-Zeile).
    python3 pm/plan/wissensnetz_obsidian.py
"""
import json, re, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
W = ROOT / "wissen"
KOPF = "> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten"
D = json.loads((ROOT / "pm/plan/wissensnetz.json").read_text())
K = {k["id"]: k for k in D["knoten"]}
notes = {}   # relpfad (ohne .md) -> text


def safe(s): return re.sub(r"[^\w.\-]+", "_", s).strip("_")
def vl(i, esc=False): return f"[[wissen/Vorgang/{i}{chr(92) if esc else ''}|{i}]]"
def st_tag(s): return "status/" + s.replace(" ", "")
def ex(rel): return (ROOT / rel).exists()


def docl(p):
    """Dokument als Wikilink (nur .md vorhanden), sonst Code."""
    if p.endswith(".md") and ex(p): return f"[[{p[:-3]}]]"
    return f"`{p}`"


def fm(typ, **kw):
    z = ["---", f"typ: {typ}"]
    for k, v in kw.items():
        if isinstance(v, list): z.append(f"{k}: [" + ", ".join(json.dumps(x, ensure_ascii=False) for x in v) + "]")
        elif isinstance(v, bool): z.append(f"{k}: {str(v).lower()}")
        elif isinstance(v, (int, float)): z.append(f"{k}: {v}")
        else: z.append(f"{k}: {json.dumps(v, ensure_ascii=False)}")
    return "\n".join(z + ["---", ""])


def vliste(ids): return "\n".join(f"- {vl(i)} – {K[i]['name']}" for i in ids) or "- –"


# Rückverweise sammeln
req, bt, wis, sw, bef, ent = {}, {}, {}, {}, {}, {}
for k in D["knoten"]:
    i = k["id"]
    for r in k["req"]: req.setdefault(r["id"], dict(text=r["text"], v=[]))["v"].append(i)
    for b in k["bt"]: bt.setdefault(b["id"], dict(name=b["name"], v=[], e={}))["v"].append(i)
    for w in k["wissen"]: wis.setdefault(w["id"], dict(w=w, v=[]))["v"].append(i)
    for s in k["software"]: sw.setdefault(s["name"], dict(status=s["status"], v=[]))["v"].append(i)
    for b in k["befunde"]: bef.setdefault(b["id"], dict(titel=b["titel"], v=[]))["v"].append(i)
    for e in k["entscheidungen"]: ent.setdefault(e["id"], dict(e=e, v=[]))["v"].append(i)
    for e in k["entscheidungen"]:
        for b in k["bt"]: bt[b["id"]]["e"][e["id"]] = e

# Vorgänge
for k in D["knoten"]:
    i = k["id"]
    t = fm("vorgang", status=k["status"], kritisch=k["kritisch"], dauer_AT=k["dauer"], es=k["es"], ef=k["ef"], puffer=k["puffer"],
           ressourcen=k["ressourcen"], tags=["vorgang", st_tag(k["status"])])
    t += f"# {i} – {k['name']}\n\n{KOPF}\n\n"
    t += f"- Status: {k['status']}{' (kritischer Pfad)' if k['kritisch'] else ''}; Dauer {k['dauer']} AT; ES {k['es']}, EF {k['ef']}, Puffer {k['puffer']}\n"
    t += f"- Ressourcen: {', '.join(k['ressourcen']) or '–'}\n- Notiz: {k['notiz'] or '–'}\n"
    t += f"- Vorgänger: {', '.join(vl(x) for x in k['vorgaenger']) or '–'}\n- Nachfolger: {', '.join(vl(x) for x in k['nachfolger']) or '–'}\n\n"
    t += "## Anforderungen\n" + ("\n".join(f"- [[wissen/Anforderung/{r['id']}|{r['id']}]] – {r['text']}" for r in k["req"]) or "- –") + "\n\n"
    t += "## Bauteile\n" + ("\n".join(f"- [[wissen/Bauteil/{b['id']}|{b['id']}]] – {b['name']}" for b in k["bt"]) or "- –") + "\n\n"
    t += "## Recherche\n" + ("\n".join(f"- [[wissen/Recherche/{w['id']}|{w['id']}]] – {w['status']}" for w in k["wissen"]) or "- –") + "\n\n"
    t += "## Stückliste\n" + ("\n".join(f"- [[wissen/Teil/{x['pos']}|{x['pos']}]] – {x['benennung']} ({x['menge']}×, {x['art']})" for x in k["teile"]) or "- –") + "\n\n"
    t += "## Software\n" + ("\n".join(f"- [[wissen/Software/{safe(s['name'])}|{s['name']}]] – {s['status']}" for s in k["software"]) or "- –") + "\n\n"
    t += "## Dokumente\n" + ("\n".join(f"- {docl(d)}" for d in k["doc"]) or "- –") + "\n\n"
    t += "## Ergebnisse\n" + ("\n".join(f"- {'✓' if a['vorhanden'] else '✗'} `{a['glob']}`" for a in k["aus"]) or "- ohne Nachweisdatei") + "\n\n"
    t += "## Befunde\n" + ("\n".join(f"- [[wissen/Befund/{b['id']}|{b['id']}]] – {b['titel']}" for b in k["befunde"]) or "- –") + "\n\n"
    t += "## Entscheidungen\n" + ("\n".join(f"- [[wissen/Entscheidung/{e['id']}|{e['id']}]] – {e['titel']} ({e['status']})" for e in k["entscheidungen"]) or "- –") + "\n\n"
    t += f"---\n*{KOPF[2:]}*\n"
    notes[f"Vorgang/{i}"] = t

SL = D["stueckliste"]
for x in SL:
    ws = [w.strip() for w in (x.get("recherche") or "").split(",") if w.strip()]
    vs = [v.strip() for v in (x.get("vorgang") or "").split(",") if v.strip()]
    rl = "\n".join(f"- [[wissen/Recherche/{w}|{w}]]" if w in wis else f"- {w} (ohne Notiz)" for w in ws) or "- –"
    bl = f"[[wissen/Bauteil/{x['bt']}|{x['bt']}]]" if x["bt"] in bt else x["bt"]
    notes[f"Teil/{x['pos']}"] = (fm("teil", art=x["art"], menge=x["menge"], bt=x["bt"], tags=["teil", "art/" + x["art"]])
        + f"# {x['pos']} – {x['benennung']}\n\n{KOPF}\n\n- Art: {x['art']} (K Kaufteil, E Eigenteil, S Schnittstelle zum Fahrzeug)\n- Menge: {x['menge']}\n- Bauteil: {bl}\n"
        f"- Herleitung: {x.get('formel') or '–'}\n- Bemerkung: {x.get('bemerkung') or '–'}\n\n## Recherche\n{rl}\n\n"
        f"## Auslegende Vorgänge\n" + ("\n".join(f"- {vl(i)} – {K[i]['name']}" if i in K else f"- {i}" for i in vs) or "- –") + "\n\nQuelle: [[docs/13_stueckliste]]\n")

for r, v in req.items():
    notes[f"Anforderung/{r}"] = (fm("anforderung", tags=["anforderung"]) + f"# {r}\n\n{KOPF}\n\n{v['text']}\n\n"
        f"Lastenheft: [[docs/01_lastenheft]]\n\n## Vorgänge\n{vliste(v['v'])}\n")
# Bauteile: alle aus struktur.json (Eltern-/Kind-Links, Merkmale, ENT-Akten), Vorgänge aus dem Wissensnetz
ST = json.loads((ROOT / "pm/bauteile/struktur.json").read_text())["bauteile"]
STD = {b["id"]: b for b in ST}
PAR = json.loads((ROOT / "pm/bauteile/parameter.json").read_text())["parameter"]
kinder = {}
for b in ST: kinder.setdefault(b["eltern"], []).append(b["id"])
ent_bt = {}   # BT -> [(ENT, Titel, Status, Merkmal, Wert)]
for f in sorted((ROOT / "pm/entscheidungen").glob("ENT-*.md")):
    if f.name == "VORLAGE.md": continue
    kopf = f.read_text().split("---")[1]; d = {}
    for z in kopf.splitlines():
        if ":" in z: a_, b_ = z.split(":", 1); d[a_.strip()] = b_.strip()
    for b_ in re.findall(r"BT-\d+", d.get("bauteile", "")):
        ent_bt.setdefault(b_, []).append((f.stem, d.get("titel", ""), d.get("status", ""), d.get("merkmal", ""), d.get("wert", ""), d.get("variante", "")))
def bl(i_): return f"[[wissen/Bauteil/{i_}|{i_}]] – {STD[i_]['name']}" if i_ in STD else i_
for b in ST:
    i_ = b["id"]; v = bt.get(i_, dict(v=[]))
    mk = "\n".join(f"- {m}: " + (f"**{PAR[i_][m]['wert']}** ({PAR[i_][m]['entscheidung']})" if PAR.get(i_, {}).get(m, {}).get("wert") is not None else "offen") for m in b.get("merkmale", {})) or "- –"
    es_ = "\n".join(f"- [[wissen/Entscheidung/{e[0]}|{e[0]}]] – {e[1]} ({e[2]}; {e[3]} = {e[4]}; Variante {e[5].strip('[]') or 'alle'})" for e in ent_bt.get(i_, [])) or "- –"
    sl_ = "\n".join(f"- [[wissen/Teil/{x['pos']}|{x['pos']}]] – {x['benennung']} ({x['menge']}×, {x['art']})" for x in SL if x["bt"] == i_) or "- –"
    rq = ", ".join(f"[[wissen/Anforderung/{r}|{r}]]" if r in req else r for r in b.get("anforderungen", [])) or "–"
    el = bl(b["eltern"]) if b["eltern"] else "– (Wurzel)"
    kl = "\n".join(f"- {bl(k_)}" for k_ in kinder.get(i_, [])) or "- –"
    notes[f"Bauteil/{i_}"] = (fm("bauteil", art=b.get("art", ""), tags=["bauteil"]) + f"# {i_} – {b['name']}\n\n{KOPF}\n\n"
        f"- Rolle: {b.get('rolle', '–')}\n- Art: {b.get('art') or '–'}\n- Anforderungen: {rq}\n- Eltern: {el}\n\n## Kinder\n{kl}\n\n"
        f"## Merkmale (offen = noch keine entschiedene Akte)\n{mk}\n\n## Entscheidungen\n{es_}\n\n## Stückliste\n{sl_}\n\n## Vorgänge\n{vliste(v['v'])}\n")
for w, v in wis.items():
    x = v["w"]; z = f"- Prüfung: {x.get('pruefung', '–')}\n"
    z += f"- Ergebnis: [[{x['datei'][:-3]}]]\n" if x.get("datei") and ex(x["datei"]) else (f"- Ergebnis: `forschung/ergebnis/{w}.md` (noch nicht vorhanden)\n")
    notes[f"Recherche/{w}"] = (fm("recherche", status=x["status"], tags=["recherche", st_tag(x["status"])])
        + f"# {w}\n\n{KOPF}\n\n- Status: {x['status']}\n{z}\n## Vorgänge\n{vliste(v['v'])}\n")
for s, v in sw.items():
    notes[f"Software/{safe(s)}"] = (fm("software", status=v["status"], tags=["software"]) + f"# {s}\n\n{KOPF}\n\n- Status: {v['status']}\n- Übersicht: [[SOFTWARE]]\n\n## Vorgänge\n{vliste(v['v'])}\n")
for b, v in bef.items():
    notes[f"Befund/{b}"] = fm("befund", tags=["befund"]) + f"# {b}\n\n{KOPF}\n\n{v['titel']}\n\nQuelle: [[BEFUNDE]]\n\n## Vorgänge\n{vliste(v['v'])}\n"
for e, v in ent.items():
    x = v["e"]; bts = "\n".join(f"- [[wissen/Bauteil/{b}|{b}]]" for b in x["bt"] if b in bt) or "- –"
    akte = f"[[{x['datei'][:-3]}]]" if ex(x["datei"]) else f"`{x['datei']}`"
    va = x.get("variante") or []
    notes[f"Entscheidung/{e}"] = (fm("entscheidung", status=x["status"], variante=va or "alle", tags=["entscheidung"] + [f"variante/{v_}" for v_ in va]) + f"# {e} – {x['titel']}\n\n{KOPF}\n\n"
        f"- Status: {x['status']}\n- Variante: {', '.join(va) or 'alle'}\n- Akte: {akte}\n\n## Bauteile\n{bts}\n\n## Vorgänge\n{vliste(v['v'])}\n")

# Start
ks = D["knoten"]; zs = {}
for k in ks: zs[k["status"]] = zs.get(k["status"], 0) + 1
s = fm("start", tags=["start"]) + f"# Wissensnetz Batterieprojekt\n\n{KOPF}\n\n"
s += f"Projektdauer (kritischer Pfad): {D['projektdauer_AT']} AT (Annahmen). Vorgänge: {len(ks)}; " + ", ".join(f"{a}: {b}" for a, b in zs.items()) + ".\n\n"
s += "Weiter: [[PLAN]] · [[BEFUNDE]] · [[docs/03_anforderungsverfolgung]] · [[docs/13_stueckliste]] · [Netzplan-Ansicht](pm/plan/wissensnetz.html)\n\n"
za = {}
for x in SL: za[x["art"]] = za.get(x["art"], 0) + 1
s += "## Stückliste nach Art\n\n| Art | Bedeutung | Positionen |\n|---|---|---|\n"
for a_, bd in (("K", "Kaufteil"), ("E", "Eigenteil"), ("S", "Schnittstelle zum Fahrzeug")): s += f"| {a_} | {bd} | {za.get(a_, 0)} |\n"
s += f"| | gesamt | {len(SL)} |\n\n"
s += "## Kritischer Pfad\n" + " → ".join(vl(k["id"]) for k in ks if k["kritisch"]) + "\n\n"
s += "## Offene Vorgänge\n\n| Vorgang | Name | Status | Dauer AT | Puffer |\n|---|---|---|---|---|\n"
for k in ks:
    if k["status"] in ("offen", "teilweise"): s += f"| {vl(k['id'], True)} | {k['name'].replace('|', '/')} | {k['status']} | {k['dauer']} | {k['puffer']} |\n"
s += "\n## Nicht installierte Software\n\n| Software | Status | Vorgänge |\n|---|---|---|\n"
for n, v in sw.items():
    if "nicht installiert" in v["status"]:
        s += f"| [[wissen/Software/{safe(n)}\\|{n}]] | {v['status']} | {', '.join(vl(i, True) for i in v['v'])} |\n"
s += "\n## Recherche-Stand\n\n| Thema | Status | Prüfung |\n|---|---|---|\n"
for w, v in sorted(wis.items()):
    s += f"| [[wissen/Recherche/{w}\\|{w}]] | {v['w']['status']} | {v['w'].get('pruefung', '–')} |\n"
s += f"\n---\n*{KOPF[2:]}*\n"
notes["Start"] = s

# schreiben
if W.exists():
    if not (W / ".erzeugt").exists(): raise SystemExit("wissen/ existiert ohne Markerdatei .erzeugt – abgebrochen")
    shutil.rmtree(W)
for rel, t in notes.items():
    p = W / f"{rel}.md"; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(t)
(W / ".erzeugt").write_text("Von pm/plan/wissensnetz_obsidian.py erzeugt; Ordner wird beim Lauf geleert.\n")

# .obsidian
OB = ROOT / ".obsidian"
if not OB.exists(): OB.mkdir()
def merge(name, upd):
    f = OB / name; d = json.loads(f.read_text()) if f.exists() else {}
    d.update(upd); f.write_text(json.dumps(d, ensure_ascii=False, indent=2))
merge("app.json", {"userIgnoreFilters": [".venv/", "forschung/recherche_ablage/", "forschung/pakete/", "forschung/patent_ablage/", "quellen/", "node_modules/"]})
farben = {"wissen/Vorgang": 0xE74C3C, "wissen/Anforderung": 0x3498DB, "wissen/Bauteil": 0xF39C12, "wissen/Recherche": 0x2ECC71,
          "wissen/Software": 0x9B59B6, "wissen/Befund": 0xE67E22, "wissen/Entscheidung": 0x1ABC9C, "wissen/Teil": 0xF1C40F, "docs": 0x95A5A6}
merge("graph.json", {"colorGroups": [{"query": f"path:{p}", "color": {"a": 1, "rgb": c}} for p, c in farben.items()]})
gi = ROOT / ".gitignore"; g = gi.read_text()
if ".obsidian/workspace*.json" not in g: gi.write_text(g + ("" if g.endswith("\n") else "\n") + ".obsidian/workspace*.json\n")

# Linkprüfung
fehl = []; n = 0
for p in W.rglob("*.md"):
    for m in re.finditer(r"\[\[([^\]]+)\]\]", p.read_text()):
        n += 1; z = m.group(1).replace("\\|", "|").split("|")[0].split("#")[0]
        if not (ROOT / (z + ".md")).exists(): fehl.append(f"{p.relative_to(ROOT)}: [[{z}]]")
zaehl = {}
for rel in notes: zaehl[rel.split("/")[0]] = zaehl.get(rel.split("/")[0], 0) + 1
print("Notizen:", zaehl, "gesamt", len(notes))
print(f"Links geprüft: {n}; fehlende Ziele: {len(fehl)}"); [print("  ", f) for f in fehl]
