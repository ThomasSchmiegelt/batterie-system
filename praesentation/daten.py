#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-23), Entwurf. Vorgang B5 (REQ-D14).
Liest alle Zahlen fuer Folien und Folienbausteine aus den Projektdateien. Nichts wird abgetippt.
Jeder Wert kommt als (Wert, Quellpfad) zurueck, damit die Folie die Quelle nennen kann."""
import json, re, os, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def P(*a):
    return os.path.join(ROOT, *a)


def J(rel):
    with open(P(rel), encoding="utf-8") as f:
        return json.load(f)


def T(rel):
    with open(P(rel), encoding="utf-8") as f:
        return f.read()


def tabelle(text, start=0):
    """Markdown-Tabellenzeilen ab 'start' als Listen von Zellen (ohne Trennzeile)."""
    zeilen = []
    for z in text.splitlines()[start:]:
        if z.startswith("|") and not re.match(r"^\|[\s\-|:]+\|$", z):
            zeilen.append([c.strip() for c in z.strip().strip("|").split("|")])
    return zeilen


def f(x, n=1):
    """Zahl deutsch formatieren."""
    if x is None:
        return "–"
    s = f"{x:.{n}f}"
    return s.replace(".", ",")


# ---------- docs/06 ----------
def v_modell():
    txt = T("docs/06_verifikationsplan.md")
    rows = {}
    for r in tabelle(txt):
        if len(r) == 6 and r[0].startswith("REQ-"):
            rows[r[0]] = dict(ebene=r[1], methode=r[2], kriterium=r[3], ist=r[4], bewertung=r[5])
    zaehl = {}
    m = re.search(r"## Zählung je Bewertung(.*?)##", txt, re.S)
    for r in tabelle(m.group(1)):
        if len(r) == 2 and r[0] != "Bewertung":
            zaehl[r[0].replace("*", "")] = int(r[1].replace("*", ""))
    m2 = re.search(r"## Zählung davon mit vom Autor bestätigtem Kriterium(.*?)\n## ", txt, re.S)   # 2026-11-23: zweite Zählung (AUFTRAG_REQ_SCHAERFEN)
    if m2:
        for r in tabelle(m2.group(1)):
            if len(r) == 2 and r[0] != "Bewertung":
                zaehl["autor_" + r[0].replace("*", "")] = int(r[1].replace("*", ""))
    return rows, zaehl, "docs/06_verifikationsplan.md"


# ---------- X3 ----------
X3_PFAD = "sim/mechanik/x3_crash_g5/ergebnis.json"
X3_GUELTIG = ["LFP_a", "LFP_a2", "LFP_b", "NMC_a", "NMC_b"]


def x3():
    d = J(X3_PFAD)
    out = {}
    for k in X3_GUELTIG:
        v = d[k]
        if v.get("status", "").startswith("ungültig") or not v.get("pruef_modell_ok"):
            continue
        out[k] = v
    return out, X3_PFAD


# ---------- K ----------
def kuehlung():
    d = {}
    for v, f_ in [("LFP", "elmer_LFP_P0_V4p"), ("NMC", "elmer_NMC_P4_V4p")]:
        e = J(f"sim/kuehlung/k3_gesamt/{f_}/ergebnis.json")
        d[v] = dict(T=e["T_max_Zellblock_C"], dT=e["dT_Zellblock_K"],
                    quelle=f"sim/kuehlung/k3_gesamt/{f_}/ergebnis.json")
    for v, f_ in [("LFP", "elmer_LFP_P0_V4"), ("NMC", "elmer_NMC_P4_V4")]:
        e = J(f"sim/kuehlung/k3_gesamt/{f_}/ergebnis.json")
        d[v + "_V4"] = dict(T=e["T_max_Zellblock_C"], dT=e["dT_Zellblock_K"],
                            quelle=f"sim/kuehlung/k3_gesamt/{f_}/ergebnis.json")
    k5 = J("sim/kuehlung/k5_parallel/ergebnis_verteiler.json")
    g = k5["gruppen"]["faelle"]
    d["k5"] = dict(abw_x3=g["k2_d25_x3"]["max_abw_pct"], dp_x3=g["k2_d25_x3"]["dp_bar"],
                   dp_x1=g["k2_d25_x1"]["dp_bar"], dp_maeander_x1=k5["dp_maeander_nachgerechnet_bar_x1"],
                   quelle="sim/kuehlung/k5_parallel/ergebnis_verteiler.json")
    return d


# ---------- G5, Kosten, Stueckliste ----------
def pack():
    d = {}
    for v in ("LFP", "NMC"):
        e = J(f"cad/baukasten/ausgabe/ergebnis_{v}.json")
        k = J(f"pm/kosten/ergebnis_{v}.json")
        s = J(f"pm/bauteile/stueckliste_{v}.json")
        d[v] = dict(teile=e["teile"], masse=e["masse_kg"], L=e["laenge_mm"], B=e["breite_mm"],
                    H=e["hoehe_max_mm"], koll=len(e["kollisionen"]) if isinstance(e["kollisionen"], list) else e["kollisionen"],
                    pruefmeldungen=len(e["fehler"]),
                    kosten=k["summe_eur_pack"], kosten_kwh=k["summe_eur_je_kWh"], zelle_eur=k["zellkosten_eur"],
                    offen=k["positionen_offen_gesamt"], voll=k["summe_vollstaendig"],
                    anteil_schaetzung=k["anteil_schaetzung_an_summe_pct"],
                    sl=s["pruefsummen"], summen=s["summen"], positionen=s["positionen"],
                    q_cad=f"cad/baukasten/ausgabe/ergebnis_{v}.json", q_kosten=f"pm/kosten/ergebnis_{v}.json",
                    q_sl=f"pm/bauteile/stueckliste_{v}.json")
    return d


def startwerte():
    return J("pm/startwerte.json"), "pm/startwerte.json"


def anforderungen():
    a = J("pm/anforderungen.json")
    return {r["id"]: r for r in a["anforderungen"]}, "pm/anforderungen.json"


def lastenheft_status():
    """REQ-P: id -> (Anforderung, Wert, Status) aus docs/01."""
    out = {}
    for r in tabelle(T("docs/01_lastenheft.md")):
        if len(r) == 6 and r[0].startswith("REQ-P"):
            out[r[0]] = dict(text=r[1], wert=r[2], status=r[5])
    return out, "docs/01_lastenheft.md"


def elektrik():
    e = J("sim/elektrik/e1_querschnitte/ergebnis_g5.json")
    alt = J("sim/elektrik/e1_querschnitte/ergebnis.json")
    return dict(LFP=e["LFP_summe"], NMC=e["NMC_summe"], verfehlt=e["verfehlt_verlust_ueber_300W"],
                arten=e["arten"], lf=e["lastfaelle"], alt=alt), "sim/elektrik/e1_querschnitte/ergebnis_g5.json"


def zelle():
    b = J("sim/chemie/c2_kalibrierung/ergebnis_blade.json")
    dc = J("sim/chemie/c2_kalibrierung/ergebnis_dcir.json")
    s = J("sim/chemie/c2_kalibrierung/ergebnis_schnellladen_n4680.json")
    sl = {r["C_start"]: r for r in s["N4680"]}
    return dict(r10=b["R10_50pct"], dcir=dc, schnell=sl,
                q=["sim/chemie/c2_kalibrierung/ergebnis_blade.json", "sim/chemie/c2_kalibrierung/ergebnis_dcir.json",
                   "sim/chemie/c2_kalibrierung/ergebnis_schnellladen_n4680.json"])


def risiken():
    txt = T("docs/05_risiken_fmea.md")
    out = []
    for r in tabelle(txt):
        if r[0].startswith("RIS-0") and len(r) == 9:
            out.append(dict(nr=r[0], fehler=r[1], folge=r[2], massnahme=r[4], bew=r[5:8], rpz=r[8]))
        elif r[0] == "R-PLAT" or r[0] == "R-4680W":
            out.append(dict(nr=r[0], fehler=r[2], folge=r[3], massnahme=r[7], bew=r[4:7], rpz="–"))
    return out, "docs/05_risiken_fmea.md"


def patente():
    txt = T("forschung/PATENTE.md")
    nr, inh = [], collections.Counter()
    nicht = 0
    for z in txt.splitlines():
        m = re.match(r"^\| ([A-Z]{2}[0-9A-Z]{6,}) \|(.*)$", z)
        if m and m.group(1) not in nr:
            nr.append(m.group(1))
            c = [x.strip() for x in z.strip().strip("|").split("|")]
            inh[c[2]] += 1
            if "Abruf fehlgeschlagen" in z or "nicht gefunden" in c[4]:
                nicht += 1
    themen = len(re.findall(r"^## P\d+", txt, re.M))
    return dict(n=len(nr), inhaber=inh, ohne_anspruch=nicht, themen=themen), "forschung/PATENTE.md"


def ki_einsatz():
    txt = T("docs/08_ki_einsatz_protokoll.md")
    zeilen = [r for r in tabelle(txt) if re.match(r"^\d{4}-\d\d-\d\d", r[0])]
    c = collections.Counter()
    for r in zeilen:
        a = r[1].lower()
        if "opus" in a and "sonnet" not in a and "haiku" not in a and "pi" not in a.split():
            c["Opus"] += 1
        elif "sonnet" in a:
            c["Sonnet"] += 1
        elif "haiku" in a:
            c["Haiku"] += 1
        elif a.strip() == "pi" or "pi " in a + " ":
            c["PI"] += 1
        else:
            c["sonstige"] += 1
    befunde = set(re.findall(r"B-BAT-\d{3}", T("BEFUNDE.md")))
    return dict(zeilen=len(zeilen), je=c, befunde=len(befunde)), "docs/08_ki_einsatz_protokoll.md, BEFUNDE.md"


def lizenzen():
    txt = T("docs/10_lizenzen_und_quellen.md")
    n = len([r for r in tabelle(txt) if len(r) >= 3 and r[0] not in ("Paket", "Quelle")])
    return n, "docs/10_lizenzen_und_quellen.md"


def software():
    out = []
    for r in tabelle(T("SOFTWARE.md")):
        if len(r) >= 3 and r[0] != "Aufgabe":
            out.append((r[0], r[1], r[2]))
    return out, "SOFTWARE.md"


def x1():
    d = J("sim/mechanik/x1_seitencrash/ergebnis.json")
    y = J("sim/mechanik/x1b_knautschzone/ergebnis_oc.json")["LFP_w20"]
    return d, y, "sim/mechanik/x1_seitencrash/ergebnis.json, sim/mechanik/x1b_knautschzone/ergebnis_oc.json"
