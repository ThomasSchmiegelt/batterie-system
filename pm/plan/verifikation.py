#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-23), Entwurf. Auftrag pm/AUFTRAG_WORKFLOW_V.md Punkt 2, erweitert durch pm/AUFTRAG_REQ_SCHAERFEN.md; Konzept docs/17 §1.
V-Modell-Matrix: liest pm/anforderungen.json und die Nachweisdateien, schreibt docs/06_verifikationsplan.md und bericht/verifikation_tabelle.tex.
Keine eigenen Zahlen: Ist-Werte kommen aus den Nachweisdateien (Pfad + JSON-Schluessel), Kriterien aus anforderungen.json.
    python3 pm/plan/verifikation.py [--eingabe PFAD] [--md PFAD] [--tex PFAD]
Bewertung (docs/17 §1): nachgewiesen | rechnerisch erfüllt (nicht validiert) | verfehlt | offen | blockiert.
Tor T0: Fehlt bei einer REQ ein Pflichtfeld (Messgröße, Ort, Lastfall, Methode, Ebene, Kriterium), bricht das Skript mit rc 1 ab und nennt die REQ (keine Bewertung „nicht definiert“).
Kriterium (dict oder Liste): {groesse, variante?, op, wert | wert_aus {datei, schluessel}, einheit, herkunft_kriterium, blockiert?, hinweis?}
  op: <= >= < > == | zwischen (wert [min,max]) | vorhanden (Schlüssel/Datei existiert, nicht leer) | rc0 (Skript endet mit 0)
  herkunft_kriterium: Autor | Startwert (Vorschlag) | Annahme Opus | Norm (zu belegen Wxx)
Nachweis [{datei, schluessel (punktgetrennt, Filter Liste[feld=wert]), groesse, variante?}] oder {typ: datei, datei, groesse} oder {typ: skript, befehl, groesse}."""
import json, re, subprocess, sys, datetime, operator
from pathlib import Path
R = Path(__file__).resolve().parents[2]; ND = "nicht definiert"
OPS = {"<=": operator.le, ">=": operator.ge, "<": operator.lt, ">": operator.gt, "==": operator.eq}
STUFEN = ["nachgewiesen", "rechnerisch erfüllt (nicht validiert)", "verfehlt", "offen", "blockiert"]
ZUSATZ = " (Kriterium Annahme, Autor offen)"
PFLICHT = ("messgroesse", "ort", "lastfall", "methode", "ebene")

def pfad(d, schl):
    for k in schl.split("."):
        m = re.fullmatch(r"(.+)\[(\w+)=(.+)\]", k)
        if m:
            d = d[m.group(1)] if isinstance(d, dict) else None
            if not isinstance(d, list): raise KeyError(k)
            tr = [x for x in d if isinstance(x, dict) and str(x.get(m.group(2))) == m.group(3)]
            if not tr: raise KeyError(k)
            d = tr[0]
        elif isinstance(d, dict) and k in d: d = d[k]
        elif isinstance(d, list) and k.isdigit() and int(k) < len(d): d = d[int(k)]
        else: raise KeyError(k)
    return d

def holen(n):
    """(Wert, Fehler). typ datei: Wert True, wenn vorhanden; typ skript: Rückgabecode."""
    t = n.get("typ", "json")
    if t == "datei":
        return (True, None) if (R / n["datei"]).exists() else (None, f"Datei fehlt: {n['datei']}")
    if t == "skript":
        rc = subprocess.run(n["befehl"], shell=True, cwd=R, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode
        return rc, None
    return holen_json(n["datei"], n["schluessel"])

def holen_json(datei, schl):
    p = R / datei
    if not p.exists(): return None, f"Datei fehlt: {datei}"
    try: d = json.loads(p.read_text())
    except Exception as e: return None, f"JSON-Fehler {datei}: {e}"
    try: return pfad(d, schl), None
    except KeyError: return None, f"Schlüssel fehlt: {datei} :: {schl}"

def kriterien(r):
    k = r.get("kriterium")
    return [k] if isinstance(k, dict) else (k if isinstance(k, list) else [])

def sollwert(k):
    if "wert_aus" in k:
        w, f = holen_json(k["wert_aus"]["datei"], k["wert_aus"]["schluessel"])
        if f: raise ValueError(f)
        return w
    return k.get("wert")

def ktext(k):
    try: w = sollwert(k)
    except ValueError as e: w = f"({e})"
    zus = f" [{k['herkunft_kriterium']}]" if k.get("herkunft_kriterium") else ""
    v = f" {k['variante']}" if k.get("variante") else ""
    return f"{k['groesse']}{v} {k['op']} {w if k['op'] not in ('vorhanden', 'rc0') else ''} {k.get('einheit', '')}".replace("  ", " ").strip() + zus

def fmt(x): return f"{x:.4g}" if isinstance(x, float) else str(x)

def leer(v): return v is None or v == "" or v == [] or v == {}

def pruefe_k(r, k):
    """Gibt (status, ist_zeilen) für ein Kriterium zurück: erfuellt | verfehlt | offen | blockiert."""
    passend = [n for n in r.get("nachweis", []) if n.get("groesse") == k["groesse"] and (not k.get("variante") or n.get("variante") == k["variante"] or not n.get("variante"))]
    if k.get("blockiert") and not passend: return "blockiert", [f"blockiert: {k['blockiert']}"]
    if not passend: return "offen", ["kein Nachweis verknüpft"]
    ist, urteile = [], []
    for n in passend:
        v, fehler = holen(n)
        if fehler: ist.append(f"({fehler})"); urteile.append(None); continue
        try: soll = sollwert(k)
        except ValueError as e: ist.append(f"(Sollwert: {e})"); urteile.append(None); continue
        if k["op"] == "vorhanden": ok = not leer(v)
        elif k["op"] == "rc0": ok = (v == 0)
        elif k["op"] == "zwischen": ok = isinstance(v, (int, float)) and soll[0] <= v <= soll[1]
        elif isinstance(v, (int, float)) and not isinstance(v, bool): ok = OPS[k["op"]](v, soll)
        else: ok = (str(v) == str(soll)) if k["op"] == "==" else None
        urteile.append(ok)
        quelle = n.get("datei") or n.get("befehl", "")
        if n.get("schluessel"): quelle += f" :: {n['schluessel']}"
        wert = "vorhanden" if (k["op"] == "vorhanden" and ok) else ("rc " + str(v) if k["op"] == "rc0" else fmt(v))
        ist.append(f"{(n['variante'] + ' ') if n.get('variante') else ''}{n['groesse']} = {wert} [{quelle}]")
    if False in urteile: return "verfehlt", ist
    if None in urteile: return "offen", ist
    return "erfuellt", ist

def luecken(r):
    f = [x for x in PFLICHT if r.get(x) in (None, "", ND)]
    if not kriterien(r): f.append("kriterium")
    return f

def bewerte(r):
    """(Bewertung, Ist-Text, Kriterium-Text, alle_autor)"""
    kr = kriterien(r)
    kt = "<br>".join(ktext(k) for k in kr) if kr else ND
    if r.get("gruppe") == "REQ-G": kt = ktext(kr[0]) + f" ({r.get('status_lastenheft', '')})"
    res = [pruefe_k(r, k) for k in kr]
    ist = "<br>".join(f"{('[' + k['groesse'] + (' ' + k['variante'] if k.get('variante') else '') + '] ') if len(kr) > 1 else ''}" + "; ".join(i) for k, (s, i) in zip(kr, res))
    st = [s for s, _ in res]
    if "verfehlt" in st: b = "verfehlt"
    elif "blockiert" in st: b = "blockiert"
    elif "offen" in st: b = "offen"
    else: b = "rechnerisch erfüllt (nicht validiert)" if r.get("methode") == "S" else "nachgewiesen"
    ausgewertet = [k for k, (s, i) in zip(kr, res) if s in ("erfuellt", "verfehlt")]
    if b in ("verfehlt", "nachgewiesen", "rechnerisch erfüllt (nicht validiert)") and any(k.get("herkunft_kriterium") != "Autor" for k in ausgewertet): b += ZUSATZ
    return b, ist, kt, all(k.get("herkunft_kriterium") == "Autor" for k in kr)

def tex(s):
    for a, b in (("\\", "\\textbackslash{}"), ("&", "\\&"), ("%", "\\%"), ("_", "\\_"), ("#", "\\#"), ("$", "\\$"), ("{", "\\{"), ("}", "\\}"), ("<br>", "\\newline "), ("≤", "$\\leq$"), ("≥", "$\\geq$"), ("Δ", "$\\Delta$"), ("Ω", "$\\Omega$")): s = s.replace(a, b)
    return s

def stufe(b): return b.replace(ZUSATZ, "")

def main(a):
    def opt(n, d):
        return a[a.index(n) + 1] if n in a else d
    ein = Path(opt("--eingabe", R / "pm/anforderungen.json")); md = Path(opt("--md", R / "docs/06_verifikationsplan.md")); tx = Path(opt("--tex", R / "bericht/verifikation_tabelle.tex"))
    reqs = json.loads(ein.read_text())["anforderungen"]
    fehl = [(r["id"], luecken(r)) for r in reqs if luecken(r)]
    if fehl:
        print("TOR T0 ZU: Pflichtfelder fehlen (keine Bewertung möglich):")
        for i, f in fehl: print(f"  {i}: {', '.join(f)}")
        sys.exit(1)
    zeilen, zaehl, zaehl_a = [], {s: 0 for s in STUFEN}, {s: 0 for s in STUFEN}
    for r in reqs:
        b, ist, kt, alle_autor = bewerte(r); zaehl[stufe(b)] += 1
        if alle_autor: zaehl_a[stufe(b)] += 1
        zeilen.append((r["id"], r["ebene"], r["methode"], kt, ist, b))
    heute = datetime.date.today().isoformat()
    M = ["| Dok.-Nr. | BAT-DOC-06 | Version | 0.3 | Status | Entwurf |", "|---|---|---|---|---|---|",
         "| Titel | Verifikationsplan (V-Modell-Matrix) | Ersteller | Claude Sonnet (KI), pm/plan/verifikation.py | Prüfer | – (Opus, Mensch offen) |", "",
         "> **KI-generiert.** Entwurf, nicht vom Menschen freigegeben. Testprojekt „KI im Engineering“, kein Produkt. Erzeugt am " + heute + ", nicht von Hand bearbeiten.", "",
         f"Quellen: `{ein.relative_to(R) if ein.is_relative_to(R) else ein}` (Anforderungen, Kriterien, Nachweisverweise) und die dort genannten Ergebnisdateien. Bewertungsstufen: `docs/17_workflow_schleife.md` §1. Bei Methode S ist die höchste Stufe „rechnerisch erfüllt (nicht validiert)“. Jedes Kriterium trägt seine Herkunft in eckigen Klammern; hängt eine Bewertung an einem Kriterium ohne Herkunft „Autor“, steht „(Kriterium Annahme, Autor offen)“ dahinter. Kriterien mit Herkunft Annahme Opus, Startwert oder Norm sind Vorschläge und stehen in `docs/19_freigaberunde.md`.", "",
         "| REQ | Ebene | Methode | Kriterium | Ist-Wert mit Quelle | Bewertung |", "|---|---|---|---|---|---|"]
    for z in zeilen: M.append("| " + " | ".join(z[:6]) + " |")
    M += ["", "## Zählung je Bewertung", "", "| Bewertung | Anzahl |", "|---|---|"] + [f"| {s} | {zaehl[s]} |" for s in STUFEN] + [f"| **gesamt** | {len(reqs)} |", "",
          "## Zählung davon mit vom Autor bestätigtem Kriterium", "", "Gezählt werden Anforderungen, bei denen jedes Kriterium die Herkunft „Autor“ hat.", "", "| Bewertung | Anzahl |", "|---|---|"] + [f"| {s} | {zaehl_a[s]} |" for s in STUFEN] + [f"| **gesamt** | {sum(zaehl_a.values())} |", "",
          "## Anhang: früherer Stand v0.1 (Opus, 2026-11-11, unverändert übernommen)", "",
          "| Nr | REQ | Methode | Werkzeug | Erwartung vorher in | Abnahmekriterium |", "|---|---|---|---|---|---|",
          "| VER-001 | – | PyBaMM-Modell gegen veröffentlichte Messkurve des Parametersatzes | PyBaMM | sim/chemie/ERWARTUNG.md | Abweichung festlegen (Annahme) |",
          "| VER-002 | REQ-P09 | Zelltemperatur beim Auslegungsfall | Elmer | sim/kuehlung/ERWARTUNG.md | Grenze aus REQ-P09 |",
          "| VER-003 | REQ-D01 | Zitate in Rechercheergebnissen | pruefe.py | – | 0 Fehler |", "",
          "---", "*KI-generiert (Claude Sonnet, 2026-11-23). Status Entwurf. Freigabe nur durch den Autor.*"]
    md.write_text("\n".join(M) + "\n")
    T = ["% KI-generiert (Claude Sonnet, 2026-11-23), Entwurf. Erzeugt von pm/plan/verifikation.py, nicht von Hand bearbeiten.",
         "\\begin{longtable}{p{1.7cm}p{1.6cm}p{1.2cm}p{3.2cm}p{4.8cm}p{2.6cm}}",
         "\\toprule \\textbf{REQ} & \\textbf{Ebene} & \\textbf{Meth.} & \\textbf{Kriterium} & \\textbf{Ist-Wert (Quelle)} & \\textbf{Bewertung}\\\\\\midrule\\endfirsthead",
         "\\toprule \\textbf{REQ} & \\textbf{Ebene} & \\textbf{Meth.} & \\textbf{Kriterium} & \\textbf{Ist-Wert (Quelle)} & \\textbf{Bewertung}\\\\\\midrule\\endhead\\bottomrule\\endlastfoot"]
    for z in zeilen: T.append(" & ".join(tex(str(x)) for x in z[:5]) + " & \\textbf{" + tex(z[5]) + "}\\\\")
    T += ["\\end{longtable}", "% Zählung: " + ", ".join(f"{s} {zaehl[s]}" for s in STUFEN) + " | davon Autor-Kriterium: " + ", ".join(f"{s} {zaehl_a[s]}" for s in STUFEN)]
    tx.write_text("\n".join(T) + "\n")
    print("Zählung:", ", ".join(f"{s} {n}" for s, n in zaehl.items()), f"(gesamt {len(reqs)})")
    print("davon Autor-Kriterium:", ", ".join(f"{s} {n}" for s, n in zaehl_a.items()), f"(gesamt {sum(zaehl_a.values())})"); print("Lücken T0: 0")
if __name__ == "__main__": main(sys.argv[1:])
