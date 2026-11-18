#!/usr/bin/env python3
"""geändert 2026-11-16 Sonnet (Varianten LFP/NMC, AUFTRAG_VARIANTEN).
pm.py -- Projektmanagement Batteriesystem: Entscheidungen, Bauteilbaum, Parameter für das CAD, Kontext fürs Bauteilgespräch.

KI-generiert (Claude Opus, 2026-11-11). Nur Python-Standardbibliothek.

    python3 pm/pm.py pruefe            Verweise prüfen (BT, REQ, B-BAT, Merkmal, doppelte gültige Entscheidungen)
    python3 pm/pm.py register          docs/04_entscheidungen.md aus pm/entscheidungen/ENT-*.md erzeugen
    python3 pm/pm.py parameter         pm/bauteile/parameter.json (gemeinsame Akten) und je Variante parameter_<V>.json (gemeinsam + variantenbezogen)
    python3 pm/pm.py kontext BT-100 [--variante V]   pm/gespraeche/kontext_BT-100[_V].md: alles, was das Bauteil über sich wissen darf
    python3 pm/pm.py neu "Titel" BT-100 merkmal [--variante LFP]   nächste freie ENT-Nummer aus der Vorlage anlegen

Varianten: pm/varianten.json. YAML-Feld `variante: [LFP]` in einer Akte; fehlt es (null), gilt die Akte für alle Varianten.

Grundsatz: Ein Maß im CAD hat genau eine Herkunft, eine Entscheidung. Das Bauteil kann deshalb jede Form begründen.
"""
import json, re, sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]; PM = R / "pm"; E = PM / "entscheidungen"
STRUKTUR = PM / "bauteile" / "struktur.json"
VARIANTEN = PM / "varianten.json"


def varianten():
    return json.loads(VARIANTEN.read_text()) if VARIANTEN.exists() else {}


def vset(e):
    """Varianten, für die eine Akte gilt (variante null = alle)."""
    v = e.get("variante")
    if isinstance(v, str): v = [v]
    return set(v) if v else set(varianten())


def lies(f):
    t = f.read_text(); m = re.match(r"---\n(.*?)\n---\n(.*)", t, re.S)
    kopf = {}
    for z in m.group(1).splitlines():
        z = z.split("  #")[0].rstrip()
        if ":" not in z: continue
        k, v = z.split(":", 1); v = v.strip()
        if v.startswith("["): v = [x.strip() for x in v.strip("[]").split(",") if x.strip()]
        elif v in ("null", ""): v = None
        else:
            try: v = float(v) if re.fullmatch(r"-?\d+(\.\d+)?", v) else v
            except ValueError: pass
        kopf[k.strip()] = v
    kopf["_text"] = m.group(2); kopf["_datei"] = f.relative_to(R).as_posix()
    return kopf


def alle():
    return [lies(f) for f in sorted(E.glob("ENT-[0-9]*.md"))]


def struktur():
    return {b["id"]: b for b in json.loads(STRUKTUR.read_text())["bauteile"]}


def gueltig(e):
    return str(e.get("status", "")).startswith("entschieden")


def pruefe():
    bt = struktur(); lh = (R / "docs" / "01_lastenheft.md").read_text(); bef = (R / "BEFUNDE.md").read_text()
    ids = [e["id"] for e in alle()]; fehler = 0; belegt = {}; bekannt = set(varianten())
    for e in alle():
        for v in ([e["variante"]] if isinstance(e.get("variante"), str) else e.get("variante") or []):
            if v not in bekannt: print(f"{e['id']}: unbekannte Variante {v} (nicht in pm/varianten.json)"); fehler += 1
        for b in e.get("bauteile") or []:
            if b not in bt: print(f"{e['id']}: Bauteil {b} fehlt in struktur.json"); fehler += 1
            elif e.get("merkmal") not in (None, "-") and e["merkmal"] not in bt[b]["merkmale"]:
                print(f"{e['id']}: Merkmal {e['merkmal']} fehlt bei {b}"); fehler += 1
            if gueltig(e) and e.get("merkmal") not in (None, "-"):
                belegt.setdefault((b, e["merkmal"]), []).append(e)
        for r in e.get("anforderungen") or []:
            if f"| {r} |" not in lh: print(f"{e['id']}: Anforderung {r} fehlt im Lastenheft"); fehler += 1
        for b in e.get("belege") or []:
            if b.startswith("B-BAT") and b not in bef: print(f"{e['id']}: Befund {b} fehlt in BEFUNDE.md"); fehler += 1
        if e.get("ersetzt") and e["ersetzt"] not in ids: print(f"{e['id']}: ersetzt unbekannte {e['ersetzt']}"); fehler += 1
        if ids.count(e["id"]) > 1: print(f"{e['id']}: Nummer doppelt"); fehler += 1
    ersetzte = {e.get("ersetzt") for e in alle()}
    for k, v in belegt.items():
        v = [x for x in v if x["id"] not in ersetzte]
        for i in range(len(v)):
            for j in range(i + 1, len(v)):
                ue = vset(v[i]) & vset(v[j])
                if ue: print(f"{k}: mehrere gültige Entscheidungen {v[i]['id']}, {v[j]['id']} (Varianten überschneiden sich: {sorted(ue)})"); fehler += 1
    print(f"{len(ids)} Entscheidungen, {fehler} Fehler"); return fehler


def register():
    z = ["| Dok.-Nr. | BAT-DOC-04 | Version | automatisch | Status | Entwurf |", "|---|---|---|---|---|---|",
         "| Titel | Entscheidungen (erzeugt von pm/pm.py register aus pm/entscheidungen/) | Ersteller | pm.py | Prüfer | – |", "",
         "> **KI-generiert.** Nicht von Hand ändern; Quelle sind die Einzelakten ENT-*.md.", "",
         "| Nr | Datum | Entscheidung | Variante | Bauteile | Merkmal = Wert | Anforderungen | Belege | Wer | Status |", "|---|---|---|---|---|---|---|---|---|---|"]
    for e in alle():
        w = "-" if e.get("merkmal") in (None, "-") else f"{e['merkmal']} = {e.get('wert')} {e.get('einheit') or ''}".strip()
        z.append(f"| [{e['id']}](../{e['_datei']}) | {e['datum']} | {e['titel']} | {', '.join(e.get('variante') or []) or 'alle'} | {', '.join(e.get('bauteile') or [])} | {w} | "
                 f"{', '.join(e.get('anforderungen') or [])} | {', '.join(e.get('belege') or []) or '–'} | {e.get('wer')} | {e.get('status')} |")
    z += ["", "---", "*KI-generiert (pm.py). Status „entschieden“ setzt nur der Autor.*"]
    (R / "docs" / "04_entscheidungen.md").write_text("\n".join(z) + "\n"); print("docs/04_entscheidungen.md geschrieben")


def parameter():
    bt = struktur(); ersetzte = {e.get("ersetzt") for e in alle()}; V = varianten(); fehler = 0
    gueltige = [e for e in alle() if gueltig(e) and e["id"] not in ersetzte and e.get("merkmal") not in (None, "-")]

    def leer():
        return {b["id"]: {m: {"wert": None, "entscheidung": None} for m in b["merkmale"]} for b in bt.values()}

    def setze(out, e):
        for b in e.get("bauteile") or []:
            out[b][e["merkmal"]] = {"wert": e.get("wert"), "einheit": e.get("einheit"), "entscheidung": e["id"]}

    def schreibe(datei, out, hinweis):
        offen = sum(v["wert"] is None for d in out.values() for v in d.values())
        (PM / "bauteile" / datei).write_text(json.dumps({"hinweis": hinweis, "parameter": out}, indent=1, ensure_ascii=False))
        print(f"pm/bauteile/{datei}: {offen} Merkmale noch ohne Entscheidung")

    gem = leer()
    for e in gueltige:
        if not e.get("variante"): setze(gem, e)
    schreibe("parameter.json", gem, "KI-generiert, erzeugt von pm.py parameter. Einzige Maßquelle fürs CAD.")
    for v in V:
        out = leer()
        for e in gueltige:
            if e.get("variante"): continue
            setze(out, e)
        for e in gueltige:
            if not e.get("variante") or v not in vset(e): continue
            for b in e.get("bauteile") or []:
                if out[b][e["merkmal"]]["wert"] is not None:
                    print(f"FEHLER: {b}/{e['merkmal']} hat gemeinsamen Wert ({out[b][e['merkmal']]['entscheidung']}) und Variante {v} ({e['id']})"); fehler += 1; continue
                out[b][e["merkmal"]] = {"wert": e.get("wert"), "einheit": e.get("einheit"), "entscheidung": e["id"], "variante": v}
        schreibe(f"parameter_{v}.json", out, f"KI-generiert, erzeugt von pm.py parameter. Maßquelle Variante {v}: gemeinsame Akten plus Akten mit variante {v}.")
    if fehler: sys.exit(1)


def kontext(bid, var=None):
    bt = struktur(); b = bt[bid]; lh = (R / "docs" / "01_lastenheft.md").read_text().splitlines()
    kinder = [x for x in bt.values() if x["eltern"] == bid]; ents = [e for e in alle() if (bid in (e.get("bauteile") or []) or bid == "BT-000") and (not var or var in vset(e))]
    pf = PM / "bauteile" / (f"parameter_{var}.json" if var else "parameter.json")
    par = json.loads(pf.read_text())["parameter"] if pf.exists() else {}
    t = [f"# Kontext für das Bauteilgespräch: {bid} {b['name']}" + (f" (Variante {var})" if var else ""), "", "KI-generiert von pm.py aus Projektdateien (nur eigene Dokumente).", "",
         f"## Ich bin\n{b['name']} ({bid}). Aufgabe: {b['rolle']}. Teil von: {b['eltern'] or '–'}. Meine Teile: {', '.join(k['id']+' '+k['name'] for k in kinder) or '–'}.", "",
         "## Meine Merkmale (Wert und entscheidende Akte)"]
    for m, v in (par.get(bid) or {m: {"wert": None, "entscheidung": None} for m in b["merkmale"]}).items():
        t.append(f"- {m}: {v.get('wert') if v.get('wert') is not None else 'noch nicht entschieden'} {v.get('einheit') or ''} ({v.get('entscheidung') or '–'})")
    t += ["", "## Anforderungen an mich (Lastenheft)"] + [z for z in lh if any(f"| {r} |" in z for r in b["anforderungen"])]
    t += ["", "## Entscheidungen, die mich betreffen (vollständig)"]
    for e in ents:
        t += [f"### {e['id']} {e['titel']} ({e['datum']}, {e.get('status')}, {e.get('wer')}; Variante: {', '.join(e.get('variante') or []) or 'alle'})",
              f"Merkmal: {e.get('merkmal')} = {e.get('wert')} {e.get('einheit') or ''}; Anforderungen: {', '.join(e.get('anforderungen') or [])}; Belege: {', '.join(e.get('belege') or []) or '–'}",
              e["_text"].strip(), ""]
    bef = (R / "BEFUNDE.md").read_text()
    for x in sorted({x for e in ents for x in e.get("belege") or [] if x.startswith("B-BAT")}):
        i = bef.find(x); t += [f"## Befund {x}", bef[i:i + 1500] if i >= 0 else "(fehlt)", ""]
    (PM / "gespraeche").mkdir(exist_ok=True); f = PM / "gespraeche" / (f"kontext_{bid}_{var}.md" if var else f"kontext_{bid}.md"); f.write_text("\n".join(t) + "\n")
    print(f"{f.relative_to(R)} ({len(ents)} Entscheidungen)")


def neu(titel, bid, merkmal, var=None):
    n = max([int(e["id"][4:]) for e in alle()] + [0]) + 1; i = f"ENT-{n:03d}"
    import datetime
    v = (E / "VORLAGE.md").read_text().replace("ENT-NNN", i).replace("JJJJ-MM-TT", datetime.date.today().isoformat()) \
        .replace("titel: kurzer Satz", f"titel: {titel}").replace("bauteile: [BT-100]", f"bauteile: [{bid}]").replace("merkmal: dicke_mm", f"merkmal: {merkmal}")
    if var:
        if var not in varianten(): sys.exit(f"Unbekannte Variante {var} (pm/varianten.json)")
        v = re.sub(r"^variante: null", f"variante: [{var}]", v, flags=re.M)
    (E / f"{i}.md").write_text(v); print(f"pm/entscheidungen/{i}.md angelegt (Status vorgeschlagen)")


def flag(a, name):
    """--name WERT aus der Argumentliste herausnehmen."""
    if name in a:
        i = a.index(name); w = a[i + 1]; del a[i:i + 2]; return w
    return None


if __name__ == "__main__":
    a = sys.argv[1:] or ["hilfe"]; var = flag(a, "--variante")
    {"pruefe": lambda: sys.exit(1 if pruefe() else 0), "register": register, "parameter": parameter,
     "kontext": lambda: kontext(a[1], var), "neu": lambda: neu(a[1], a[2], a[3], var)}.get(a[0], lambda: print(__doc__))()
