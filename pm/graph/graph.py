#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-23), Entwurf. Auftrag pm/graph/AUFTRAG_GRAPH.md, Schema pm/graph/SCHEMA.md.
Baut den Wissensgraphen aus strukturierten Feldern -> pm/graph/graph.json (node-link) und graph.graphml.
Erzeugte Datei, nicht von Hand bearbeiten.   python3 pm/graph/graph.py
Kanten nur aus Feldern; Textvorkommen = Kante "erwaehnt" (schwach, nie Beleg)."""
import json, re, sys, glob
from pathlib import Path
import networkx as nx

R = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(R / "pm/plan"))
RE_ID = re.compile(r"\bREQ-[A-Z]\d+\b|\bENT-\d+\b|\bB-BAT-\d+\b|\bBT-\d{3}\b|\b[WPT]\d{2}\b")
NODES, EDGES, UNRES = {}, [], []


def rd(p): return (R / p).read_text(errors="replace")
def js(p): return json.loads(rd(p))
def node(i, typ, **kw):
    n = NODES.setdefault(i, {"typ": typ}); n.update({k: v for k, v in kw.items() if v is not None}); return i
def edge(u, v, typ, quelle, **kw): EDGES.append((u, v, typ, quelle, kw))
def ex(p): return (R / p).exists()


# ---- Bauteile, Merkmale, Parameter
ST = js("pm/bauteile/struktur.json")["bauteile"]
PAR = {v: js(f"pm/bauteile/parameter{s}.json")["parameter"] for v, s in (("alle", ""), ("LFP", "_LFP"), ("NMC", "_NMC"))}
for b in ST:
    node(b["id"], "Bauteil", name=b["name"], art=b.get("art"), anforderungen=b.get("anforderungen", []), pfad="pm/bauteile/struktur.json")
for b in ST:
    if b.get("eltern"): edge(b["id"], b["eltern"], "teil_von", "struktur.json eltern")
    for m in b.get("merkmale", {}):
        mid = f"{b['id']}.{m}"; w = {v: PAR[v].get(b["id"], {}).get(m, {}).get("wert") for v in PAR}
        node(mid, "Merkmal", wert=w["alle"], wert_LFP=w["LFP"], wert_NMC=w["NMC"], entscheidung=PAR["alle"].get(b["id"], {}).get(m, {}).get("entscheidung"))
        edge(b["id"], mid, "hat_merkmal", "struktur.json merkmale")
node("LFP", "Variante"); node("NMC", "Variante")

# ---- Anforderungen
import verifikation as V
ANF = js("pm/anforderungen.json")["anforderungen"]
HERK_UNRES = []
for r in ANF:
    try: bew = V.bewerte(r)[0]
    except Exception as e: bew = f"nicht bewertbar ({e})"
    node(r["id"], "Anforderung", name=r["text"], status=bew, methode=r.get("methode"), ebene=r.get("ebene"), pfad="pm/anforderungen.json")
    kr = r.get("kriterium") or []; kr = [kr] if isinstance(kr, dict) else kr
    for k in kr:
        h = k.get("herkunft_kriterium", "")
        if h == "Autor":
            node("Autor", "Vorgabe", name="Vorgabe des Autors"); edge(r["id"], "Autor", "kriterium_aus", "herkunft_kriterium", groesse=k.get("groesse"))
        elif h.startswith("Annahme"):
            a = node(f"annahme_opus:{r['id']}.{k.get('groesse')}", "Annahme", name=f"Kriterium {k.get('groesse')} {k.get('op')} {k.get('wert')} (Annahme Opus)")
            edge(r["id"], a, "kriterium_aus", "herkunft_kriterium", groesse=k.get("groesse"))
        elif h.startswith("Startwert"):
            sk = (k.get("wert_aus") or {}).get("schluessel", k.get("groesse"))
            a = node(f"startwert:{sk}", "Annahme", name="Startwert (Vorschlag)", pfad="pm/startwerte.json")
            edge(r["id"], a, "kriterium_aus", "herkunft_kriterium", groesse=k.get("groesse"))
        elif h.startswith("Norm"):
            ws = re.findall(r"\bW\d+\b", h)
            if not ws: UNRES.append((r["id"], "Norm ohne Wxx: " + h, "kriterium_aus"))
            for w in ws: edge(r["id"], w, "kriterium_aus", "herkunft_kriterium", groesse=k.get("groesse"))
        else: UNRES.append((r["id"], "Herkunft unbekannt: " + h, "kriterium_aus"))
    for n in r.get("nachweis", []):
        d = n.get("datei") or n.get("befehl")
        if not d: continue
        eid = node(f"{d}::{n['schluessel']}" if n.get("schluessel") else d, "Ergebnis", datei=n.get("datei"), pfad=n.get("datei"))
        edge(r["id"], eid, "verifiziert_durch", "anforderungen.json nachweis", groesse=n.get("groesse"), variante=n.get("variante"))

# ---- Annahmen
for f in sorted(glob.glob(str(R / "cad/baukasten/annahmen*.json"))):
    for k, v in json.loads(Path(f).read_text()).items():
        if k.startswith("_"): continue
        node(k, "Annahme", wert=v.get("wert") if isinstance(v, dict) else v, pfad=str(Path(f).relative_to(R)))
for f in sorted(glob.glob(str(R / "pm/startwerte*.json"))):
    for k in (json.loads(Path(f).read_text()).get("annahmen") or {}):
        node(f"startwert:annahmen.{k}", "Annahme", pfad=str(Path(f).relative_to(R)))

# ---- Entscheidungen
def kopf(t):
    d = {}
    for z in t.split("---")[1].splitlines():
        if ":" in z and not z.startswith((" ", "#")):
            a, b = z.split(":", 1); d[a.strip()] = re.sub(r"\s+#.*$", "", b).strip()
    return d
def liste(s):
    s = (s or "").strip()
    if s in ("", "null", "-", "~"): return []
    return [x.strip() for x in s.strip("[]").split(",") if x.strip()]

ENT_TEXT = {}
for f in sorted((R / "pm/entscheidungen").glob("ENT-*.md")):
    t = f.read_text(); d = kopf(t); i = f.stem; ENT_TEXT[i] = t
    node(i, "Entscheidung", name=d.get("titel"), status=d.get("status"), datum=d.get("datum"), variante=liste(d.get("variante")) or "alle", pfad=f"pm/entscheidungen/{f.name}")
    mk = d.get("merkmal", "-")
    if mk not in ("-", "", "null"):
        for bt in liste(d.get("bauteile")): edge(i, f"{bt}.{mk}", "legt_fest", "ENT bauteile+merkmal", wert=d.get("wert"))
    for r in liste(d.get("anforderungen")): edge(i, r, "erfuellt_beitrag", "ENT anforderungen")
    for b in liste(d.get("belege")): edge(i, b, "belegt_durch", "ENT belege")
    if d.get("ersetzt") not in (None, "", "null"): edge(i, d["ersetzt"], "ersetzt", "ENT ersetzt")
    for v in liste(d.get("variante")): edge(i, v, "gilt_fuer", "ENT variante")

# ---- Befunde
BEF_TEXT = {}
parts = re.split(r"^## (?=B-BAT-\d+)", rd("BEFUNDE.md"), flags=re.M)[1:]
for p in parts:
    m = re.match(r"(B-BAT-\d+)[ \t]+([^\n]*)", p)   # Überschrift: ID, Titel, Datum (vor oder im Titel)
    if m:
        dm = re.search(r"\d{4}-\d\d-\d\d", m.group(2))
        node(m.group(1), "Befund", name=m.group(2), datum=dm.group(0) if dm else None, pfad="BEFUNDE.md"); BEF_TEXT[m.group(1)] = p

# ---- Quellen
for f in sorted((R / "forschung/ergebnis").glob("*.pruefung.txt")):
    i = f.name.split(".")[0]
    if re.fullmatch(r"[WPT]\d+", i):
        z = [x for x in f.read_text().splitlines() if "bestaetigt" in x]
        node(i, "Quelle", status=z[-1].strip() if z else None, pfad=f"forschung/ergebnis/{i}.md")

# ---- Normen (docs/07 Tabelle 1)
for z in rd("docs/07_normen_und_vorschriften.md").splitlines():
    c = [x.strip() for x in z.strip().strip("|").split("|")]
    if z.startswith("|") and len(c) == 5 and c[0] not in ("Regelwerk",) and not c[0].startswith("-"):
        node(c[0], "Norm", name=c[1], anwendbar=c[2], recherche=re.findall(r"\bW\d+\b", c[4]), pfad="docs/07_normen_und_vorschriften.md")

# ---- Stückliste
for v, fn in (("alle", "stueckliste.json"), ("LFP", "stueckliste_LFP.json"), ("NMC", "stueckliste_NMC.json")):
    for p in js(f"pm/bauteile/{fn}").get("positionen", []):
        pid = node(f"{v}:{p['pos']}", "Stuecklistenposition", name=p.get("benennung"), variante=v, bt=p.get("bt"), pfad=f"pm/bauteile/{fn}")
        edge(pid, p.get("bt"), "realisiert", f"{fn} bt")

# ---- Rechnungen
ERG_PAT = ("ergebnis*.json", "ERGEBNIS*.md", "*.png")
RECH = {}
for f in sorted(R.glob("sim/**/ERWARTUNG.md")):
    ordner = f.parent; rel = str(ordner.relative_to(R)); RECH[rel] = ordner
    node(rel, "Rechnung", name=ordner.name, pfad=rel)
    t = f.read_text()
    m = re.search(r"^## Anforderung[^\n]*\n(.*?)(?=^## |\Z)", t, re.M | re.S)
    if m:
        for r_ in set(re.findall(r"REQ-[A-Z]\d+", m.group(1))): edge(rel, r_, "gehoert_zu", "ERWARTUNG ## Anforderung")
    for pat in ERG_PAT:
        for g in sorted(ordner.rglob(pat)):
            if g.is_file(): edge(rel, node(str(g.relative_to(R)), "Ergebnis", datei=str(g.relative_to(R)), pfad=str(g.relative_to(R))), "erzeugt", "Ergebnisdatei im Ordner")
    n_ref = 0
    for ein in (ordner / "eingaben.json", ordner / "eingaben_graph.json"):   # eingaben_graph.json: Nachtrag Sonnet 2026-11-23 (alte eingaben.json blieb unverändert)
        if not ein.exists(): continue
        try: E = json.loads(ein.read_text())
        except Exception: E = {}
        var = E.get("_variante", "LFP") if isinstance(E, dict) else "LFP"
        def walk(o):
            if isinstance(o, dict):
                if isinstance(o.get("quelle"), str): yield o
                for x in o.values(): yield from walk(x)
            elif isinstance(o, list):
                for x in o: yield from walk(x)
        for o in walk(E):
            art, _, rest = o["quelle"].partition(":")
            if art == "parameter":
                bt = o.get("bt"); c = [f"{b['id']}.{rest}" for b in ST if rest in b.get("merkmale", {}) and (bt is None or b["id"] == bt)]
                if len(c) == 1: edge(rel, c[0], "verwendet", "eingaben.json parameter:")
                else: UNRES.append((rel, f"parameter:{rest} bt={bt} ({len(c)} Treffer)", "verwendet"))
            elif art == "annahme": edge(rel, rest, "verwendet", "eingaben.json annahme:")
            elif art == "ergebnis":
                fpath, _, key = rest.partition("#"); edge(rel, node(f"{fpath}::{key}" if key else fpath, "Ergebnis", datei=fpath, pfad=fpath), "verwendet", "eingaben.json ergebnis:")
            elif art == "cad":
                fpath = f"cad/baukasten/ausgabe/ergebnis_{var}.json"; edge(rel, node(f"{fpath}::{rest}", "Ergebnis", datei=fpath, pfad=fpath), "verwendet", "eingaben.json cad:")
            elif art == "stueckliste": edge(rel, f"{var}:{rest}", "verwendet", "eingaben.json stueckliste:")
            else: continue
            n_ref += 1
    NODES[rel]["eingaben_praefix"] = n_ref
# ---- CAD-Lauf (Schema Nachtrag 1): jedes Merkmal -> CAD-Lauf (eingang_cad), CAD-Lauf -> jedes Ergebnis cad:<schluessel> (erzeugt)
for v in ("LFP", "NMC"):
    fp = f"cad/baukasten/ausgabe/ergebnis_{v}.json"; cl = node(f"cad:{v}", "CAD-Lauf", name=f"CAD-Lauf {v}", variante=v, pfad=fp)
    for i_, n_ in list(NODES.items()):
        if n_["typ"] == "Merkmal": edge(i_, cl, "eingang_cad", "Schema Nachtrag 1: CAD liest alle Merkmale")
    if ex(fp):
        for k_ in js(fp): edge(cl, node(f"{fp}::{k_}", "Ergebnis", datei=fp, pfad=fp), "erzeugt", "Schema Nachtrag 1: ergebnis_<var>.json")
# Ergebnis mit Schlüssel liegt in einem Rechenordner: erzeugt (Ordner enthält die Datei)
for i, n in list(NODES.items()):
    if n["typ"] == "Ergebnis" and n.get("datei") and "::" in i:
        for rel in RECH:
            if n["datei"].startswith(rel + "/"): edge(rel, i, "erzeugt", "Ergebnisdatei im Ordner")

# ---- Dokumente und Textvorkommen (erwaehnt)
DOK = sorted(glob.glob(str(R / "docs/*.md"))) + [str(R / p) for p in ("bericht/bericht.tex", "praesentation/STORYBOARD.md", "video/STORYBOARD.md", "BEFUNDE.md", "PLAN.md", "ERINNERUNGEN.md") if ex(p)] + sorted(glob.glob(str(R / "praesentation/bausteine/*.md")))
DOKP = []
for f in DOK:
    rel = str(Path(f).relative_to(R)); DOKP.append(rel)
    typ_ = "bausteine" if "bausteine/" in rel else "docs"
    node(rel, "Dokument", name=Path(rel).stem, pfad=rel, art=typ_)
def mentions(src, text, skip=()):
    for x in sorted(set(RE_ID.findall(text))):
        if x != src and x not in skip: edge(src, x, "erwaehnt", "Textvorkommen")
for rel in DOKP:
    if rel == "BEFUNDE.md": continue    # Befunde einzeln unten
    t = rd(rel); mentions(rel, t)
    for en, enode in list(NODES.items()):   # Pfade von Ergebnisdateien
        if enode["typ"] == "Ergebnis" and "::" not in en and en in t: edge(rel, en, "erwaehnt", "Textvorkommen Pfad")
for i, t in ENT_TEXT.items(): mentions(i, t.split("---", 2)[2] if t.count("---") >= 2 else t)
for i, t in BEF_TEXT.items(): mentions(i, t)
for rel, o in RECH.items():
    for fn in ("ERWARTUNG.md", "ERGEBNIS.md"):
        if (o / fn).exists(): mentions(rel, (o / fn).read_text())

# ---- Auflösung
G = nx.MultiDiGraph()
for i, n in NODES.items(): G.add_node(i, **{k: (json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v) for k, v in n.items()})
seen = set()
for u, v, t, q, kw in EDGES:
    if v is None or u not in NODES or v not in NODES:
        if t != "erwaehnt": UNRES.append((u, v, t))
        continue
    if (u, v, t) in seen: continue
    seen.add((u, v, t)); G.add_edge(u, v, key=t, typ=t, quelle=q, **{k: x for k, x in kw.items() if x is not None})
data = nx.node_link_data(G, edges="edges")
data["unaufgeloest"] = [{"von": a, "nach": b, "kante": c} for a, b, c in UNRES]
data["hinweis"] = "KI-generiert (Claude Sonnet, 2026-11-23). Erzeugt von pm/graph/graph.py nach pm/graph/SCHEMA.md, nicht von Hand bearbeiten."
(R / "pm/graph/graph.json").write_text(json.dumps(data, ensure_ascii=False, indent=1))
nx.write_graphml(G, str(R / "pm/graph/graph.graphml"))

from collections import Counter
print("Knoten", G.number_of_nodes(), dict(Counter(d["typ"] for _, d in G.nodes(data=True))))
print("Kanten", G.number_of_edges(), dict(Counter(k for _, _, k in G.edges(keys=True))))
print("Unaufgeloest:", len(UNRES))
for a, b, c in UNRES: print(f"  {c}: {a} -> {b}")
