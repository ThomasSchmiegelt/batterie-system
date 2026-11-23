"""KI-generiert, ergänzt Sonnet 2026-11-23 (AUFTRAG_OBSIDIAN_2: Typen Dokument, Bericht, Baustein, Steckbrief, Nachweis; Anforderungen mit VER-Bewertung; alle Recherchethemen), Auftrag Opus (Notizen für alle ENT-Akten und alle Befunde, auch ohne Vorgang); geändert 2026-11-16 Sonnet (Variante in Akten-Notizen, Tag #variante/V, AUFTRAG_VARIANTEN; Bauteilnotizen für alle Bauteile aus struktur.json, AUFTRAG_LFP_UMSTELLUNG).
wissensnetz_obsidian.py -- erzeugt aus pm/plan/wissensnetz.json eine Obsidian-Notizsammlung unter wissen/.

KI-generiert. Vault-Wurzel ist das Projektverzeichnis; erzeugt wird nur wissen/ (plus .obsidian/-Schlüssel, .gitignore-Zeile).
    python3 pm/plan/wissensnetz_obsidian.py
"""
import json, re, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
import os
W = Path(os.environ["OBS_OUT"]) if os.environ.get("OBS_OUT") else ROOT / "wissen"
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

# Anforderungsnotizen: siehe Abschnitt "AUFTRAG_OBSIDIAN_2" weiter unten (nach den Bauteilen)
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

# ergänzt Sonnet 2026-11-23, Auftrag Opus: Notizen für JEDE Akte und JEDEN Befund, auch ohne Vorgang
for f in sorted((ROOT / "pm/entscheidungen").glob("ENT-*.md")):
    if f.name == "VORLAGE.md" or f"Entscheidung/{f.stem}" in notes: continue
    d = {}
    for z in f.read_text().split("---")[1].splitlines():
        if ":" in z and not z.startswith((" ", "#")): a_, b_ = z.split(":", 1); d[a_.strip()] = b_.split("   #")[0].strip()
    bts_ = re.findall(r"BT-\d+", d.get("bauteile", ""))
    bts = "\n".join(f"- [[wissen/Bauteil/{b}|{b}]]" if b in STD else f"- {b}" for b in bts_) or "- –"
    va = [x.strip() for x in d.get("variante", "").strip("[]").split(",") if x.strip()]
    notes[f"Entscheidung/{f.stem}"] = (fm("entscheidung", status=d.get("status", ""), variante=va or "alle", tags=["entscheidung"] + [f"variante/{v_}" for v_ in va])
        + f"# {f.stem} – {d.get('titel', '')}\n\n{KOPF}\n\n- Status: {d.get('status', '')}\n- Variante: {', '.join(va) or 'alle'}\n"
        f"- Akte: [[pm/entscheidungen/{f.stem}]]\n- Merkmal: {d.get('merkmal', '–')} = {d.get('wert', '–')} {d.get('einheit', '')}\n\n## Bauteile\n{bts}\n\n## Vorgänge\n- –\n")
for m_ in re.finditer(r"^## (B-BAT-\d+)\s+(.*)$", (ROOT / "BEFUNDE.md").read_text(), re.M):
    if f"Befund/{m_.group(1)}" in notes: continue
    notes[f"Befund/{m_.group(1)}"] = fm("befund", tags=["befund"]) + f"# {m_.group(1)}\n\n{KOPF}\n\n{m_.group(2)}\n\nQuelle: [[BEFUNDE]]\n\n## Vorgänge\n- –\n"


# ===== ergänzt Sonnet 2026-11-23 (AUFTRAG_OBSIDIAN_2) =====
ENT_IDS = {n.split("/")[1] for n in notes if n.startswith("Entscheidung/")}
BEF_IDS = {n.split("/")[1] for n in notes if n.startswith("Befund/")}
BT_IDS = set(STD)
def idlink(i_):
    """Wikilink auf eine vorhandene Notiz (REQ, ENT, B-BAT, BT, W/T/P), sonst None."""
    for pre, ids in (("Entscheidung", ENT_IDS), ("Befund", BEF_IDS), ("Bauteil", BT_IDS)):
        if i_ in ids: return f"[[wissen/{pre}/{i_}|{i_}]]"
    if i_.startswith("REQ-") and f"Anforderung/{i_}" in notes_req_ids: return f"[[wissen/Anforderung/{i_}|{i_}]]"
    return None
def idliste(ids): return "\n".join(f"- {idlink(i_)}" for i_ in ids if idlink(i_)) or "- –"

ANF = {a["id"]: a for a in D.get("anforderungen", [])}
for r_, v_ in req.items():   # Anforderung nur aus Vorgängen, falls anforderungen.json fehlt
    ANF.setdefault(r_, dict(id=r_, text=v_["text"], bewertung="nicht definiert", methode="–", ebene="–", kriterium="–", ist="–", luecken=[], nachweis=[], wert="", prioritaet="", gruppe="", bestaetigt_autor=False))
notes_req_ids = set(f"Anforderung/{i_}" for i_ in ANF)
notes_req_ids = {x.split("/")[1] for x in notes_req_ids}; notes_req_ids = {f"Anforderung/{x}" for x in notes_req_ids}
def bew_tag(b): return "bewertung/" + re.sub(r"[^\w]+", "_", b).strip("_")
nachw = {}   # Nachweisdatei -> [REQ]
for r_, a in ANF.items():
    for n_ in a["nachweis"]: nachw.setdefault(n_, []).append(r_)
def nlink(n_): return f"[[wissen/Nachweis/{safe(n_)}|{n_}]]"
for r_, a in ANF.items():
    vs_ = req.get(r_, dict(v=[]))["v"]
    nl = "\n".join(f"- {nlink(n_)}" for n_ in a["nachweis"]) or "- kein Nachweis verknüpft"
    nl += "".join(f"\n- Prüfskript: `{c_}`" for c_ in a.get("skripte", []))
    notes[f"Anforderung/{r_}"] = (fm("anforderung", gruppe=a["gruppe"], methode=a["methode"], ebene=a["ebene"], bewertung=a["bewertung"], tags=["anforderung", bew_tag(a.get("stufe", a["bewertung"]))])
        + f"# {r_}\n\n{KOPF}\n\n{a['text']}\n\n- Wert (Lastenheft): {a['wert'] or '–'}\n- Priorität: {a['prioritaet'] or '–'}\n- Vom Autor bestätigt: {'ja' if a['bestaetigt_autor'] else 'nein'}\n\n"
        f"## Verifikation (V-Modell-Matrix)\n\n- Methode: {a['methode']} (A Analyse, S Simulation, I Inspektion, T Test, R Review)\n- Ebene: {a['ebene']}\n- Kriterium: {a['kriterium']}\n"
        f"- Ist-Wert: {a['ist']}\n- Bewertung: **{a['bewertung']}**" + (f" (fehlt: {', '.join(a['luecken'])})" if a['luecken'] else "") + "\n"
        f"- Matrix: [[docs/06_verifikationsplan]] · Lastenheft: [[docs/01_lastenheft]] · Verfolgung: [[docs/03_anforderungsverfolgung]]\n\n## Nachweisdateien\n{nl}\n\n## Vorgänge\n{vliste(vs_)}\n"
        + ("\n## Bauteile\n" + "\n".join(f"- [[wissen/Bauteil/{b_['id']}|{b_['id']}]]" for b_ in ST if r_ in b_.get("anforderungen", [])) + "\n" if any(r_ in b_.get("anforderungen", []) for b_ in ST) else ""))
for n_, rs in nachw.items():
    notes[f"Nachweis/{safe(n_)}"] = (fm("nachweis", datei=n_, vorhanden=ex(n_), tags=["nachweis"]) + f"# Nachweis {n_}\n\n{KOPF}\n\n- Datei: " + (f"[[{n_[:-3]}]]" if n_.endswith(".md") and ex(n_) else f"`{n_}`")
        + f" ({'vorhanden' if ex(n_) else 'fehlt'})\n\n## Anforderungen, die diese Datei belegt\n" + "\n".join(f"- [[wissen/Anforderung/{r_}|{r_}]] – Bewertung: {ANF[r_]['bewertung']}" for r_ in rs) + "\n")

# Dokumente
DOKS = [d_ for d_ in D.get("dokumente", [])]
def dok_ids(path):
    t = (ROOT / path).read_text()
    return sorted(set(re.findall(r"REQ-[A-Z]\d+|ENT-\d+|B-BAT-\d+|BT-\d{3}\b", t)))
DOK_STEM = {}
for d_ in DOKS:
    nm = d_["nr"] or d_["stem"]; key = safe(d_["stem"]); DOK_STEM[d_["datei"]] = key
    ids_ = dok_ids(d_["datei"])
    reqs_ = [i_ for i_ in ids_ if i_.startswith("REQ-") and idlink(i_)]
    sonst = [i_ for i_ in ids_ if not i_.startswith("REQ-") and idlink(i_)]
    vs_ = [k["id"] for k in D["knoten"] if d_["datei"] in k["doc"]]
    notes[f"Dokument/{key}"] = (fm("dokument", nr=d_["nr"], version=d_["version"], status=d_["status"], tags=["dokument"] + (["auftrag"] if d_["auftrag"] else []))
        + f"# {d_['nr'] or d_['stem']} – {d_['titel']}\n\n{KOPF}\n\n- Datei: [[{d_['datei'][:-3]}]]\n- Version: {d_['version'] or '–'}\n- Status: {d_['status'] or '–'}\n"
        f"- Typ: {'Auftrag an einen Agenten' if d_['auftrag'] else 'Projektdokument (Dokumentenlenkung [[docs/00_dokumentenlenkung]])'}\n\n"
        f"## Genannte Anforderungen (Textvorkommen)\n" + (("\n".join(f"- {idlink(i_)}" for i_ in reqs_[:60]) + (f"\n- … und {len(reqs_)-60} weitere" if len(reqs_) > 60 else "")) or "- –") + "\n\n"
        f"## Genannte Entscheidungen, Befunde, Bauteile (Textvorkommen)\n" + (("\n".join(f"- {idlink(i_)}" for i_ in sonst[:60]) + (f"\n- … und {len(sonst)-60} weitere" if len(sonst) > 60 else "")) or "- –") + "\n\n"
        f"## Vorgänge, die dieses Dokument nennen\n{vliste(vs_)}\n")

# Bericht
B_ = D.get("bericht") or {}
if B_:
    kap = "\n".join(f"{'  ' if k_['ebene'] == 'subsection' else ''}- {k_['nr'] + ' ' if k_['nr'] else ''}{k_['titel']} (S. {k_['seite']})" for k_ in B_["kapitel"])
    bi = [i_ for i_ in B_["ids"] if idlink(i_)]
    notes["Bericht/Abschlussbericht"] = (fm("bericht", version=B_["version"], tags=["bericht"]) + f"# Abschlussbericht BAT-DOC-17, Version {B_['version']}\n\n{KOPF}\n\n"
        f"- PDF: `{B_['pdf']}`; Quelle: `{B_['tex']}`\n- Status: geprüft (KI), nicht freigegeben (Kopf des Berichts)\n- Kapitelliste aus `bericht/bericht.toc`\n\n## Kapitel\n{kap}\n\n"
        f"## Im Bericht genannte Anforderungen, Entscheidungen, Befunde, Bauteile (Textvorkommen in bericht.tex)\n" + "\n".join(f"- {idlink(i_)}" for i_ in bi) + "\n\n"
        f"## Verifikation\n- [[docs/06_verifikationsplan]] (REQ-Übersicht im Bericht, Kapitel 2)\n")

# Folienbausteine
BS = D.get("bausteine", [])
for b_ in BS:
    vid = next((k["id"] for k in D["knoten"] if k["id"].upper() == b_["stem"].split("_")[0].upper()), None)
    ql = "\n".join(f"- `{q_}`" for q_ in b_["quellen"]) or "- –"
    notes[f"Baustein/{safe(b_['stem'])}"] = (fm("baustein", vorgang=vid or "", tags=["baustein"]) + f"# Folienbaustein {b_['stem']}\n\n{KOPF}\n\n- Datei: [[{b_['datei'][:-3]}]]\n- Titel: {b_['titel']}\n"
        f"- Vorgang: {vl(vid) if vid else 'kein gleichnamiger Vorgang im Netzplan'}\n- Folienplan: [[praesentation/STORYBOARD]]\n\n## Genannte Anforderungen, Entscheidungen, Befunde, Bauteile\n{idliste(b_['ids'])}\n\n## Quelldateien der Zahlen (Auszug)\n{ql}\n")

# Steckbriefe
for c_ in D.get("steckbriefe", []):
    notes[f"Steckbrief/{safe(c_['stem'])}"] = (fm("steckbrief", bt=c_["bt"], tags=["steckbrief"]) + f"# {c_['titel']}\n\n{KOPF}\n\n- Datei: [[{c_['datei'][:-3]}]]\n- Bauteil: " + (f"[[wissen/Bauteil/{c_['bt']}|{c_['bt']}]]" if c_["bt"] in STD else c_["bt"])
        + f"\n- Workflow: [[docs/17_workflow_schleife]] (Tor T1)\n\n## Genannte Anforderungen, Entscheidungen, Befunde\n{idliste(c_['ids'])}\n")

# Recherchethemen, auch ohne Vorgang (z. B. Regelwerke W35 bis W42)
for w_ in D.get("recherche_alle", []):
    k_ = f"Recherche/{w_['id']}"
    if k_ in notes: continue
    z = f"- Prüfung: {w_.get('pruefung', '–')}\n"
    z += f"- Ergebnis: [[{w_['datei'][:-3]}]]\n" if w_.get("datei") and ex(w_["datei"]) else f"- Ergebnis: `forschung/ergebnis/{w_['id']}.md` (noch nicht vorhanden)\n"
    notes[k_] = (fm("recherche", status=w_["status"], tags=["recherche", st_tag(w_["status"]), "ohne_vorgang"]) + f"# {w_['id']}\n\n{KOPF}\n\n- Thema: {w_.get('thema') or '–'}\n- Status: {w_['status']}\n{z}"
        f"- Einordnung: Regelwerke und Normen, siehe [[docs/07_normen_und_vorschriften]]\n\n## Vorgänge\n- – (kein Vorgang im Netzplan)\n")

# Start
ks = D["knoten"]; zs = {}
for k in ks: zs[k["status"]] = zs.get(k["status"], 0) + 1
s = fm("start", tags=["start"]) + f"# Wissensnetz Batterieprojekt\n\n{KOPF}\n\n"
s += f"Projektdauer (kritischer Pfad): {D['projektdauer_AT']} AT (Annahmen). Vorgänge: {len(ks)}; " + ", ".join(f"{a}: {b}" for a, b in zs.items()) + ".\n\n"
s += "Weiter: [[PLAN]] · [[BEFUNDE]] · [[docs/03_anforderungsverfolgung]] · [[docs/13_stueckliste]] · [Netzplan-Ansicht](pm/plan/wissensnetz.html)\n\n"
za = {}
for x in SL: za[x["art"]] = za.get(x["art"], 0) + 1
s += "## Einstiege\n\n- Bericht: [[wissen/Bericht/Abschlussbericht]] (Version " + (D.get("bericht") or {}).get("version", "?") + ")\n- V-Modell-Matrix: [[docs/06_verifikationsplan]] (Bewertung je Anforderung in den Anforderungsnotizen, Tag `bewertung/...`)\n- Workflow: [[docs/17_workflow_schleife]] · Freigaberunde: [[docs/19_freigaberunde]]\n- Normen und Regelwerke: [[docs/07_normen_und_vorschriften]]\n- Präsentation: [[praesentation/STORYBOARD]] (" + str(len(BS)) + " Folienbausteine, Ordner wissen/Baustein)\n- Steckbriefe: " + (", ".join(f"[[wissen/Steckbrief/{safe(c_['stem'])}|{c_['stem']}]]" for c_ in D.get("steckbriefe", [])) or "–") + "\n- Dokumente: Ordner wissen/Dokument (" + str(len(DOKS)) + " Notizen)\n\n"
bz = {}
for a_ in ANF.values(): bz[a_.get("stufe", a_["bewertung"])] = bz.get(a_.get("stufe", a_["bewertung"]), 0) + 1
s += "## Verifikation der Anforderungen\n\n| Bewertung | Anzahl |\n|---|---|\n" + "".join(f"| {b_} | {n_} |\n" for b_, n_ in bz.items()) + f"| gesamt | {len(ANF)} |\n\n"
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
for w_ in sorted(D.get("recherche_alle", []), key=lambda x: x["id"]):
    s += f"| [[wissen/Recherche/{w_['id']}\\|{w_['id']}]] | {w_['status']} | {w_.get('pruefung', '–')} |\n"
s += f"\n---\n*{KOPF[2:]}*\n"
notes["Start"] = s


# ===== ergänzt Sonnet 2026-11-23 (AUFTRAG_GRAPH Punkt 4 und Folgeauftrag Opus: eigenständiger Tresor) =====
import subprocess, sys
from PIL import Image
BILD_MAX, BILD_DIR = 1200, "_bilder"
BILD_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp"}

# --- 1. typisierte Kanten als Eigenschaften (YAML-Frontmatter) aus pm/graph/graph.json
try: subprocess.run([sys.executable, str(ROOT / "pm/graph/graph.py")], check=True, capture_output=True, timeout=300)
except Exception as e_: print("Warnung: graph.py nicht gelaufen, vorhandenes graph.json wird verwendet:", repr(e_)[:100])
GJ = None
if (ROOT / "pm/graph/graph.json").exists(): GJ = json.loads((ROOT / "pm/graph/graph.json").read_text())
KANTEN_AUS = {}
if GJ:
    for e_ in GJ["edges"]:
        if e_["typ"] != "erwaehnt": KANTEN_AUS.setdefault(e_["source"], {}).setdefault(e_["typ"], []).append(e_["target"])
def knoten_zu_notiz(i_, typ):
    k_ = {"Anforderung": f"Anforderung/{i_}", "Bauteil": f"Bauteil/{i_}", "Entscheidung": f"Entscheidung/{i_}", "Befund": f"Befund/{i_}", "Quelle": f"Recherche/{i_}"}.get(typ)
    if typ == "Dokument" and i_.startswith("docs/") and i_.endswith(".md"): k_ = f"Dokument/{safe(Path(i_).stem)}"
    return k_ if k_ in notes else None
def notiz_zu_knoten(key):
    t_, _, n_ = key.partition("/")
    if t_ in ("Anforderung", "Bauteil", "Entscheidung", "Befund"): return n_
    if t_ == "Recherche": return n_
    if t_ == "Teil": return f"alle:{n_}"
    if t_ == "Dokument":
        for d_ in D.get("dokumente", []):
            if safe(d_["stem"]) == n_: return d_["datei"]
    return None
if GJ:
    GN = {n_["id"]: n_ for n_ in GJ["nodes"]}; nk = 0
    for key, t_ in list(notes.items()):
        gid = notiz_zu_knoten(key)
        if gid not in KANTEN_AUS: continue
        zeilen = []
        for typ, ziele in sorted(KANTEN_AUS[gid].items()):
            vals = []
            for z_ in sorted(set(ziele)):
                nz = knoten_zu_notiz(z_, GN[z_]["typ"]) if z_ in GN else None
                vals.append(f"[[{nz}|{z_}]]" if nz and nz != key else z_)
            zeilen.append(f"{typ}: [" + ", ".join(json.dumps(v, ensure_ascii=False) for v in vals) + "]"); nk += len(vals)
        m_ = re.match(r"---\n(.*?)\n---\n", t_, re.S)
        if m_: notes[key] = "---\n" + m_.group(1) + "\n" + "\n".join(zeilen) + "\n---\n" + t_[m_.end():]
    print("typisierte Kanten als Eigenschaften:", nk)

# --- 2. Ziele außerhalb von wissen/ als Notizen in den Tresor holen, Links umschreiben, Bilder verkleinert kopieren
IMG = {}   # Zielname -> Quellpfad
bodies = {}   # Notizschlüssel -> (Quelldatei, Titel)
WL = re.compile(r"(!?)\[\[([^\]]+)\]\]")
def img_kopie(src):
    """Bild verkleinert nach wissen/_bilder, Rückgabe Dateiname oder None."""
    if not src.exists() or src.suffix.lower() not in BILD_EXT: return None
    rel = str(src.relative_to(ROOT)) if src.is_relative_to(ROOT) else src.name
    base = re.sub(r"[^\w.\-]+", "_", rel.rsplit(".", 1)[0].replace("/", "__"))
    for ext_ in (".png", ".jpg"):
        if (W / BILD_DIR / (base + ext_)).exists() and (W / BILD_DIR / (base + ext_)).stat().st_mtime >= src.stat().st_mtime: return base + ext_
    (W / BILD_DIR).mkdir(parents=True, exist_ok=True)
    im = Image.open(src); im.load()
    if max(im.size) > BILD_MAX: im.thumbnail((BILD_MAX, BILD_MAX), Image.LANCZOS)
    out = W / BILD_DIR / (base + ".png"); im.convert("RGBA" if im.mode in ("RGBA", "LA", "P") else "RGB").save(out, optimize=True)
    if out.stat().st_size > 250_000:
        out.unlink(); out = W / BILD_DIR / (base + ".jpg")
        bg = Image.new("RGB", im.size, "white"); i2 = im.convert("RGBA"); bg.paste(i2, mask=i2.split()[3]); bg.save(out, quality=85, optimize=True)
    return out.name
def ext_ziel(t):
    """Zielpfad (relativ zum Repo, ohne .md) -> Notizschlüssel im Tresor oder None, wenn Datei fehlt."""
    f = ROOT / (t + ".md")
    if not f.is_file():
        f = ROOT / t
        if not f.is_file() or f.suffix.lower() in BILD_EXT: return None
    stem = f.stem; rel = str(f.relative_to(ROOT))
    if rel.startswith("pm/entscheidungen/ENT-") and f"Entscheidung/{stem}" in notes: k_ = f"Entscheidung/{stem}"
    elif rel.startswith("forschung/ergebnis/") and f"Recherche/{stem}" in notes: k_ = f"Recherche/{stem}"
    elif rel.startswith("docs/") and f"Dokument/{safe(stem)}" in notes: k_ = f"Dokument/{safe(stem)}"
    else: k_ = f"Dokument/{safe(rel.rsplit('.', 1)[0].replace('/', '__'))}"
    bodies.setdefault(k_, f)
    return k_
tot, fehlende_ziele = set(), []
def umschreiben(text, key, quelle_dir=None):
    def wl(m):
        pre, inner = m.group(1), m.group(2)
        mm = re.match(r"(.*?)(\\?\|.*)?$", inner, re.S); tgt, alias = mm.group(1), mm.group(2) or ""
        tgt, _, anker = tgt.partition("#")
        if pre == "!" or Path(tgt).suffix.lower() in BILD_EXT: return m.group(0)
        if tgt.startswith("wissen/"): neu = tgt[7:]
        elif tgt in notes: neu = tgt
        else:
            neu = ext_ziel(tgt)
            if neu is None: fehlende_ziele.append((key, tgt)); return f"`{tgt}`"
        if neu == key: return f"`{tgt}`" if not alias else alias.lstrip("\\|")
        return f"[[{neu}{'#' + anker if anker else ''}{alias}]]"
    text = WL.sub(wl, text)
    def bild(m):
        alt, p = m.group(1), m.group(2)
        if re.match(r"(https?:|data:)", p): return m.group(0)
        src = ((quelle_dir or ROOT) / p.split("#")[0].split("?")[0]).resolve()
        n_ = img_kopie(src)
        return f"![[{BILD_DIR}/{n_}]]" if n_ else f"`{alt or p} (Bild nur im Repo: {p})`"
    text = re.sub(r"!\[([^\]]*)\]\(([^)\s]+)\)", bild, text)
    text = re.sub(r"(?<!!)\[([^\]]+)\]\((?!https?:|mailto:|#)([^)]+)\)", lambda m: f"{m.group(1)} (`{m.group(2)}`, im Repo)", text)
    return text
def koerper(f):
    t = f.read_text(errors="replace")
    if t.startswith("---\n"):
        m = re.match(r"---\n.*?\n---\n", t, re.S)
        if m: t = t[m.end():]
    return t
for key in list(notes): notes[key] = umschreiben(notes[key], key)
fertig = set()
while True:
    neu_ = [k for k in bodies if k not in fertig]
    if not neu_: break
    for k_ in neu_:
        fertig.add(k_); f = bodies[k_]; rel = str(f.relative_to(ROOT))
        inh = umschreiben(koerper(f), k_, f.parent)
        if k_ in notes:
            notes[k_] = notes[k_].rstrip("\n") + f"\n\n## Inhalt (Kopie aus `{rel}`)\n\n{inh}\n"
        else:
            notes[k_] = (fm("dokument", datei=rel, tags=["dokument", "kopie"]) + f"# {f.stem}\n\n{KOPF}\n\n- Kopie von `{rel}` (Quelle im Repo, hier nur Lesekopie)\n\n## Inhalt\n\n{inh}\n")
# Befund-Notizen: Abschnittstext aus BEFUNDE.md
bf = (ROOT / "BEFUNDE.md").read_text()
for mb in re.finditer(r"^## (B-BAT-\d+)[^\n]*\n(.*?)(?=^## |\Z)", bf, re.M | re.S):
    k_ = f"Befund/{mb.group(1)}"
    if k_ in notes: notes[k_] = notes[k_].rstrip("\n") + "\n\n## Text aus BEFUNDE.md\n\n" + umschreiben(mb.group(2).strip(), k_) + "\n"

# --- 3. schreiben (.obsidian und _bilder bleiben erhalten), Tresor-Konfiguration, Prüfung nur innerhalb von wissen/
if W.exists():
    if not (W / ".erzeugt").exists() and {c_.name for c_ in W.iterdir()} - {BILD_DIR, ".obsidian"}: raise SystemExit("wissen/ existiert ohne Markerdatei .erzeugt – abgebrochen")
    for c_ in W.iterdir():
        if c_.name in (".obsidian", BILD_DIR): continue
        shutil.rmtree(c_) if c_.is_dir() else c_.unlink()
for rel, t in notes.items():
    p = W / f"{rel}.md"; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(t)
(W / ".erzeugt").write_text("Von pm/plan/wissensnetz_obsidian.py erzeugt; Ordner wird beim Lauf geleert (außer .obsidian und _bilder). Eigenständiger Obsidian-Tresor.\n")
OB = W / ".obsidian"; OB.mkdir(exist_ok=True)
def merge(name, upd):
    f = OB / name; d = json.loads(f.read_text()) if f.exists() else {}
    d.update(upd); f.write_text(json.dumps(d, ensure_ascii=False, indent=2))
merge("app.json", {"userIgnoreFilters": []})
farben = {"Vorgang": 0xE74C3C, "Anforderung": 0x3498DB, "Bauteil": 0xF39C12, "Recherche": 0x2ECC71, "Software": 0x9B59B6, "Befund": 0xE67E22, "Entscheidung": 0x1ABC9C,
          "Teil": 0xF1C40F, "Dokument": 0x7F8C8D, "Bericht": 0x2C3E50, "Baustein": 0xE91E63, "Steckbrief": 0x8E44AD, "Nachweis": 0x16A085}
merge("graph.json", {"colorGroups": [{"query": f"path:{p}", "color": {"a": 1, "rgb": c}} for p, c in farben.items()]})
gi = ROOT / ".gitignore"; g = gi.read_text()
if "wissen/.obsidian/workspace*.json" not in g: gi.write_text(g + ("" if g.endswith("\n") else "\n") + "wissen/.obsidian/workspace*.json\n")
# Linkprüfung
fehl = []; n = 0; benutzt = set()
for p in W.rglob("*.md"):
    if ".obsidian" in p.parts: continue
    for m in re.finditer(r"(!?)\[\[([^\]]+)\]\]", p.read_text()):
        n += 1; z = m.group(2).replace("\\|", "|").split("|")[0].split("#")[0]
        ziel = W / z if Path(z).suffix.lower() in BILD_EXT else W / (z + ".md")
        if not ziel.exists(): fehl.append(f"{p.relative_to(W)}: [[{z}]]")
        elif m.group(1): benutzt.add(Path(z).name)
bd = W / BILD_DIR
if bd.exists():
    for f in bd.iterdir():
        if f.name not in benutzt: f.unlink()
zaehl = {}
for rel in notes: zaehl[rel.split("/")[0]] = zaehl.get(rel.split("/")[0], 0) + 1
gr = sum(f.stat().st_size for f in W.rglob("*") if f.is_file())
print("Notizen:", zaehl, "gesamt", len(notes))
print(f"Links geprüft: {n}; fehlende Ziele innerhalb wissen/: {len(fehl)}; Bilder {len(benutzt)}; Tresorgröße {gr/1e6:.1f} MB")
for f_ in fehl[:30]: print("  ", f_)
if fehlende_ziele: print("Verweise auf nicht vorhandene Repo-Dateien (als Code gesetzt):", len(fehlende_ziele), sorted(set(t for _, t in fehlende_ziele))[:10])
