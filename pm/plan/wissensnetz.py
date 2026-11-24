"""geändert 2026-11-23 Sonnet (Auftrag AUFTRAG_OBSIDIAN_2: Anforderungen aus pm/anforderungen.json mit VER-Bewertung, Dokumente, Bericht, Bausteine, Steckbriefe, alle Recherchethemen im JSON); geändert 2026-11-16 Sonnet (Feld variante der Akten, AUFTRAG_VARIANTEN).
wissensnetz.py -- Netzplan als Rückgrat für Wissensmanagement und Projektdokumentation.

KI-generiert (Claude Opus, 2026-11-12). Anstoß des Autors: „vielleicht kann man über den Netzplan auch das
Wissensmanagement und die Projektdoku machen und sie entsprechend verknüpfen“.

Jeder Vorgang (aus plan_batterie.py) bekommt Verknüpfungen:
  req     Anforderungen (docs/01_lastenheft.md)        bt      Bauteile (pm/bauteile/struktur.json)
  wissen  Recherchethemen W/T/P (forschung/ergebnis)    doc     Projektdokumente (docs/)
  aus     Ergebnisdateien (Glob) -> bestimmen den Status automatisch; sammel=True: Status aus den Recherchethemen
Aufgelöst werden zusätzlich: Befunde (BEFUNDE.md, über Vorgang-ID in [..] oder genannte Themen), Entscheidungsakten
(pm/entscheidungen, über Bauteil), Ereignisse im Buchprotokoll (über Dateinamen/IDs, nur Zählung, Buch bleibt getrennt).

    python3 pm/plan/wissensnetz.py
Ausgabe: pm/plan/wissensnetz.json (für Ansicht und PI), danach wissensnetz.html und Obsidian-Notizen wissen/, docs/03_anforderungsverfolgung.md (erzeugt),
         pm/plan/plan_batterie.json (Notizen mit Verknüpfungen, für den Planer des AI_Framework)
Status: fertig = alle `aus` vorhanden, teilweise = einige, offen = keine; ohne `aus`: „ohne Nachweis“.
"""
import glob, json, re, sys
from pathlib import Path

HIER = Path(__file__).resolve().parent; ROOT = HIER.parents[1]
sys.path.insert(0, str(HIER)); import plan_batterie as PB

# id: dict(req, bt, wissen, doc, aus)   -- leere Felder weglassen
V = {
    "S0": dict(doc=["README.md", "CLAUDE.md", "AGENTS.md", "SOFTWARE.md"], aus=["README.md", "SOFTWARE.md", "requirements.txt"], req=["REQ-D09"]),
    "R1": dict(sammel=True, wissen=[f"W{i:02d}" for i in range(1, 18)], aus=["forschung/WISSEN.md"], req=["REQ-D01", "REQ-D07"]),
    "R2": dict(sammel=True, wissen=[f"T{i:02d}" for i in range(1, 10)], aus=["forschung/WERKZEUGE.md"], req=["REQ-D01", "REQ-D07"]),
    "R3": dict(sammel=True, wissen=[f"P{i:02d}" for i in range(1, 11)], aus=["forschung/PATENTE.md"], req=["REQ-D08"]),
    "R4": dict(doc=["BEFUNDE.md"], req=["REQ-D01"]),   # Lesung durch Opus: kein Dateinachweis, Befunde verknüpft
    "R5": dict(doc=["docs/04_entscheidungen.md"], wissen=["T01", "T02", "T04", "T05"], req=["REQ-D11"]),
    "W1": dict(doc=["docs/konzept_werkzeuge_kuehlung_kabel_crash.md"], aus=["werkzeuge/pre/*"]),
    "W2": dict(doc=["docs/konzept_werkzeuge_kuehlung_kabel_crash.md"], aus=["werkzeuge/post/*"]),
    "V1": dict(bt=["BT-000"], req=[f"REQ-P{i:02d}" for i in range(1, 11)], doc=["docs/startparameter.md", "docs/01_lastenheft.md", "docs/13_stueckliste.md"], aus=["pm/startwerte.json"]),
    "SL1": dict(doc=["docs/13_stueckliste.md"], bt=["BT-000"], req=["REQ-D01"], aus=["pm/bauteile/stueckliste.json", "docs/13_stueckliste.md"]),
    "SL2": dict(doc=["docs/13_stueckliste.md"], bt=["BT-000"], req=["REQ-D01", "REQ-D11"]),
    "V2": dict(bt=["BT-000"], req=["REQ-D05"] + [f"REQ-P{i:02d}" for i in range(1, 11)], doc=["docs/01_lastenheft.md"]),
    "C1": dict(req=["REQ-D06"], bt=["BT-100"], aus=["sim/chemie/ERWARTUNG.md"]),
    "C2": dict(req=["REQ-P06"], bt=["BT-100"], wissen=["W01", "W09", "T01"], aus=["sim/chemie/zelle_lang*"]),
    "C3": dict(req=["REQ-P04", "REQ-P05"], bt=["BT-100"], aus=["sim/chemie/ratentest*"]),
    "C4": dict(req=["REQ-D06", "REQ-D01"], bt=["BT-100"], aus=["sim/chemie/ERGEBNIS.md"]),
    "C5": dict(req=["REQ-P10", "REQ-P06"], bt=["BT-100"], wissen=["W02", "W07", "W10"], aus=["sim/chemie/alterung*"]),
    "G1": dict(req=["REQ-D11"], bt=["BT-100"], wissen=["W03", "W08", "P01"], doc=["pm/bauteile/parameter.json"]),
    "G2": dict(req=["REQ-D11"], bt=["BT-100"], aus=["cad/zelle/*.FCStd"]),
    "G3": dict(req=["REQ-P02", "REQ-P03"], bt=["BT-200"], wissen=["W12"]),
    "G4": dict(doc=["docs/13_stueckliste.md"], req=["REQ-P07", "REQ-D11"], bt=["BT-200", "BT-500"], wissen=["W15", "P02"], aus=["cad/pack/*.FCStd"]),
    "G5": dict(req=["REQ-P13"], bt=["BT-200", "BT-500"], aus=["cad/pack/bauregeln*"]),
    "K0": dict(req=["REQ-P09", "REQ-P12"], bt=["BT-600"], wissen=["W16"], doc=["docs/konzept_werkzeuge_kuehlung_kabel_crash.md"], aus=["sim/kuehlung/kuehlart*"]),
    "E1": dict(req=["REQ-P04"], bt=["BT-400"], wissen=["W13", "P06"], aus=["sim/elektrik/verbinder*"]),
    "E2": dict(req=["REQ-P13", "REQ-P11"], bt=["BT-400", "BT-700"], wissen=["W13"], aus=["sim/elektrik/schutz*"]),
    "L1": dict(req=["REQ-P13"], bt=["BT-400"], wissen=["T09"], doc=["docs/konzept_werkzeuge_kuehlung_kabel_crash.md"], aus=["cad/pack/kabel*"]),
    "E3": dict(req=["REQ-P15", "REQ-P17", "REQ-P19", "REQ-P20"], bt=["BT-300", "BT-320", "BT-321"], wissen=["W05", "W14", "T06", "P07"], doc=["sim/elektrik/e3_platine/ERWARTUNG.md"], aus=["sim/elektrik/e3_platine/ERGEBNIS.md"]),
    "E3b": dict(req=["REQ-P20", "REQ-P15"], bt=["BT-321"], doc=["sim/elektrik/e3b_platine_waerme/ERWARTUNG.md"], aus=["sim/elektrik/e3b_platine_waerme/ERGEBNIS.md"]),
    "S1": dict(req=["REQ-P18", "REQ-P21", "REQ-P11"], bt=["BT-300", "BT-700"], wissen=["W35d", "W47", "W48"], doc=["docs/24_gefahrenanalyse_hara.md"], aus=["docs/24_gefahrenanalyse_hara.md"]),
    "KR1": dict(req=["REQ-D15"], bt=["BT-321"], doc=["pm/kreativ/METHODE.md", "docs/25_loesungen_aus_kreativmethoden.md"], aus=["pm/kreativ/KR1/ERGEBNIS.md"]),
    "E4": dict(req=["REQ-P03", "REQ-P13"], bt=["BT-300", "BT-400", "BT-712"], wissen=["T04", "T05"], aus=["sim/elektrik/e3_platine/ergebnis_vorladung.json"]),
    "K1": dict(req=["REQ-D06", "REQ-P09"], bt=["BT-600"], aus=["sim/kuehlung/ERWARTUNG.md"]),
    "K2": dict(req=["REQ-P09"], bt=["BT-600"], wissen=["P03"], aus=["sim/kuehlung/verteilung*"]),
    "K3": dict(req=["REQ-P09"], bt=["BT-600"], aus=["sim/kuehlung/elmer*"]),
    "K4": dict(req=["REQ-P09"], bt=["BT-600"], aus=["sim/kuehlung/fluidx3d*"]),
    "K5": dict(req=["REQ-P09", "REQ-D06"], bt=["BT-600"], aus=["sim/kuehlung/ERGEBNIS.md"]),
    "U1": dict(req=["REQ-D06"], wissen=["T07"], doc=["docs/ersatzmodell_einsatz.md"], aus=["sim/ersatzmodell/ERWARTUNG.md"]),
    "U2": dict(req=["REQ-D09", "REQ-D10"], aus=["sim/ersatzmodell/doe*"]),
    "U3": dict(req=["REQ-D01"], aus=["sim/ersatzmodell/gp*"]),
    "U4": dict(req=["REQ-P09"], bt=["BT-600"], aus=["sim/ersatzmodell/ERGEBNIS.md"]),
    "M1": dict(req=["REQ-P14"], bt=["BT-200", "BT-500"], aus=["sim/mechanik/*"]),
    "X1": dict(req=["REQ-P14", "REQ-P11"], bt=["BT-500"], wissen=["W17", "T08"], aus=["sim/crash/quasistatisch*"]),
    "X2": dict(req=["REQ-P14"], bt=["BT-500"], wissen=["T08"], aus=["sim/crash/dynamisch*"]),
    "F1": dict(req=["REQ-P11", "REQ-D03"], doc=["docs/05_risiken_fmea.md", "docs/06_verifikationsplan.md"]),
    "B1": dict(req=["REQ-D02", "REQ-D04"], doc=["docs/prozess.md", "LESSONS_LEARNED.md", "docs/08_ki_einsatz_protokoll.md"], aus=["bericht/*.pdf"]),
    "B2": dict(req=["REQ-D12"], doc=["pm/gespraech.sh"], aus=["pm/gespraeche/*.md"]),
    "B3": dict(req=["REQ-D13"], doc=["video/STORYBOARD.md"], aus=["video/*.mp4"]),
    "B0": dict(req=["REQ-D14"], doc=["praesentation/STORYBOARD.md"]),
    "B5": dict(req=["REQ-D14", "REQ-D01"], doc=["praesentation/STORYBOARD.md"], aus=["praesentation/*.pptx"]),
    "B4": dict(req=["REQ-D05"]),
}


# Software je Vorgang (Nutzer 2026-11-12: „auch Software kann da rein“). Status: in SOFTWARE.md geführt oder „nicht installiert“.
SW = {
    "R1": ["PI", "web-recherche"], "R2": ["PI", "web-recherche"], "R3": ["PI", "patent-recherche"], "B2": ["PI"],
    "W1": ["Sketch-to-Prompt"], "W2": ["Sketch-to-Prompt", "ParaView", "pyvista"], "L1": ["Sketch-to-Prompt", "FreeCAD"],
    "C2": ["PyBaMM"], "C3": ["PyBaMM"], "C4": ["PyBaMM"], "C5": ["PyBaMM"],
    "G2": ["FreeCAD"], "G4": ["FreeCAD", "gmsh"], "G5": ["FreeCAD"],
    "K0": ["numpy"], "K2": ["numpy", "scipy"], "K3": ["ElmerFEM", "gmsh"], "K4": ["FluidX3D"],
    "U2": ["ElmerFEM"], "U3": ["scikit-learn"], "U4": ["scikit-learn", "ElmerFEM"],
    "E1": ["numpy"], "E4": ["ngspice", "OpenModelica"], "E3": ["foxBMS"],
    "M1": ["ElmerFEM"], "X1": ["CalculiX", "gmsh"], "X2": ["OpenRadioss"],
    "B1": ["pdflatex"], "B3": ["Blender", "FreeCAD"], "B5": ["python-pptx", "LibreOffice"],
}
VORHANDEN_AUSSERHALB = {"Sketch-to-Prompt": "~/sketch-to-prompt", "CalculiX": "~/.local/bin/ccx"}


def sw_status(name):
    t = "\n".join(l for l in (ROOT / "SOFTWARE.md").read_text().splitlines() if l.startswith("|"))   # nur Tabellenzeilen
    if name in t: return dict(name=name, status="im Projekt (SOFTWARE.md)")
    if name in VORHANDEN_AUSSERHALB: return dict(name=name, status=f"vorhanden, nicht in SOFTWARE.md ({VORHANDEN_AUSSERHALB[name]})")
    return dict(name=name, status="nicht installiert / nicht geprüft")


def lese_req():
    f = ROOT / "pm/anforderungen.json"
    if f.exists():
        return {r["id"]: r["text"].strip() for r in json.loads(f.read_text())["anforderungen"]}
    t = (ROOT / "docs/01_lastenheft.md").read_text()
    return {m.group(1): m.group(2).strip() for m in re.finditer(r"^\| (REQ-[PD]\d+) \| ([^|]+)", t, re.M)}


def lese_befunde():
    t = (ROOT / "BEFUNDE.md").read_text(); out = []
    for blk in re.split(r"\n(?=## B-BAT-)", t)[1:]:
        kopf = blk.splitlines()[0][3:]; out.append(dict(id=kopf.split()[0], titel=kopf, text=blk))
    return out


def lese_ent():
    out = []
    for f in sorted((ROOT / "pm/entscheidungen").glob("ENT-*.md")):
        t = f.read_text(); bt = sorted(set(re.findall(r"BT-\d{3}", t)))
        st = re.search(r"[Ss]tatus[^\n]*?(vorgeschlagen|freigegeben|verworfen|entwurf)", t, re.I)
        tit = next((l.lstrip("# ").strip() for l in t.splitlines() if l.startswith("#")), f.stem)
        mv = re.search(r"^variante:\s*\[([^\]]*)\]", t, re.M)
        var = [x.strip() for x in mv.group(1).split(",") if x.strip()] if mv else []
        out.append(dict(id=f.stem, titel=tit, bt=bt, variante=var, status=st.group(1).lower() if st else "?", datei=str(f.relative_to(ROOT))))
    return out


def wissen_status(nr):
    e = ROOT / "forschung/ergebnis" / f"{nr}.md"; p = e.with_suffix(".pruefung.txt")
    if not e.exists(): return dict(id=nr, status="offen")
    z = p.read_text().strip().splitlines()[-1] if p.exists() else "ungeprüft"
    return dict(id=nr, status="fertig", pruefung=z, datei=str(e.relative_to(ROOT)))


def lese_anf_voll():
    """Anforderungen aus pm/anforderungen.json mit Bewertung nach pm/plan/verifikation.py (keine eigene Rechnung)."""
    f = ROOT / "pm/anforderungen.json"
    if not f.exists(): return []
    sys.path.insert(0, str(HIER)); import verifikation as VF
    out = []
    for r in json.loads(f.read_text())["anforderungen"]:
        b, ist, kt, alle_autor = VF.bewerte(r); lue = list(VF.luecken(r)) if hasattr(VF, "luecken") else []
        out.append(dict(id=r["id"], gruppe=r.get("gruppe", ""), text=r["text"], wert=r.get("wert", ""), prioritaet=r.get("prioritaet", ""),
                        methode=r.get("methode", "nicht definiert"), ebene=r.get("ebene", "nicht definiert"), bewertung=b, stufe=(VF.stufe(b) if hasattr(VF, "stufe") else b), kriterium=kt,
                        ist=ist.replace("<br>", "; "), luecken=lue, bestaetigt_autor=bool(r.get("bestaetigt_autor")),
                        nachweis=sorted({n["datei"] for n in r.get("nachweis", []) if "datei" in n}),
                        skripte=sorted({n["befehl"] for n in r.get("nachweis", []) if n.get("typ") == "skript"})))
    return out


def lese_dokumente():
    """docs/*.md: Kopf (Dok.-Nr., Version, Status, Titel) aus der Kopftabelle, soweit vorhanden."""
    out = []
    for f in sorted((ROOT / "docs").glob("*.md")):
        t = f.read_text(); kopf = t[:1500]
        def g(label, kopf=kopf):
            m = re.search(rf"\|\s*{label}\s*\|\s*([^|]*?)\s*\|", kopf); return m.group(1).strip() if m else ""
        tit = g("Titel") or next((l.lstrip("# ").strip() for l in t.splitlines() if l.startswith("#")), f.stem)
        m = re.search(r"\|\s*Version\s*\|\s*([^|]*?)\s*\|\s*Status\s*\|\s*([^|]*?)\s*\|", kopf)
        out.append(dict(datei=f"docs/{f.name}", stem=f.stem, nr=g("Dok.-Nr."), titel=tit, version=m.group(1) if m else "", status=m.group(2) if m else "",
                        auftrag=f.name.startswith("AUFTRAG")))
    return out


def lese_bericht():
    f = ROOT / "bericht/bericht.toc"; tex = ROOT / "bericht/bericht.tex"
    if not f.exists(): return {}
    kap = []
    for m in re.finditer(r"\\contentsline \{(section|subsection)\}\{(?:\\numberline \{([^}]*)\})?([^}]*)\}\{(\d+)\}", f.read_text()):
        kap.append(dict(ebene=m.group(1), nr=m.group(2) or "", titel=m.group(3), seite=int(m.group(4))))
    t = tex.read_text() if tex.exists() else ""
    v = re.search(r"BAT-DOC-17, Version (\d+(?:\.\d+)*)", t)
    ids = sorted(set(re.findall(r"REQ-[A-Z]\d+|ENT-\d+|B-BAT-\d+|BT-\d{3}\b", t)))
    return dict(version=v.group(1) if v else "?", pdf="bericht/bericht.pdf", tex="bericht/bericht.tex", kapitel=kap, ids=ids)


def lese_bausteine():
    out = []
    for f in sorted((ROOT / "praesentation/bausteine").glob("*.md")):
        t = f.read_text(); tit = next((l.lstrip("# ").strip() for l in t.splitlines() if l.startswith("# ")), f.stem)
        out.append(dict(datei=f"praesentation/bausteine/{f.name}", stem=f.stem, titel=tit,
                        ids=sorted(set(re.findall(r"REQ-[A-Z]\d+|ENT-\d+|B-BAT-\d+|BT-\d{3}\b", t))),
                        quellen=sorted(set(re.findall(r"(?:sim|cad|pm|docs|bericht)/[\w./\-]+\.(?:json|md|png|csv|tex)", t)))[:12]))
    return out


def lese_steckbriefe():
    out = []
    for f in sorted((ROOT / "pm/steckbriefe").glob("*.md")):
        t = f.read_text(); m = re.match(r"(BT-\d+)", f.stem)
        tit = re.search(r"\| Titel \| ([^|]*?) \|", t)
        out.append(dict(datei=f"pm/steckbriefe/{f.name}", stem=f.stem, bt=m.group(1) if m else "", titel=tit.group(1) if tit else f.stem,
                        ids=sorted(set(re.findall(r"REQ-[A-Z]\d+|ENT-\d+|B-BAT-\d+", t)))))
    return out


def lese_recherche_alle():
    out = []
    for tsv in ("themen_wissen", "themen_werkzeuge", "themen_patente"):
        f = ROOT / "forschung" / f"{tsv}.tsv"
        if not f.exists(): continue
        for z in f.read_text().splitlines():
            if z.strip() and not z.startswith("#"):
                p = z.split("\t"); w = wissen_status(p[0]); w["thema"] = (p[3] if len(p) > 3 else ""); out.append(w)
    return out


def lese_teile():
    f = ROOT / "pm/bauteile/stueckliste.json"
    if not f.exists(): return []
    return json.loads(f.read_text())["positionen"]


def main():
    teile_alle = lese_teile()
    req = lese_req(); bef = lese_befunde(); ent = lese_ent()
    bt_namen = {b["id"]: b["name"] for b in json.loads((ROOT / "pm/bauteile/struktur.json").read_text()).get("bauteile", [])} \
        if (ROOT / "pm/bauteile/struktur.json").exists() else {}
    es, ef, ls, lf, nach, ende = PB.cpm(PB.A)
    knoten, fehler = [], []
    for i, name, dur, vor, res, notiz in PB.A:
        v = V.get(i, {}); aus = v.get("aus", [])
        da = [g for g in aus if glob.glob(str(ROOT / g))]
        status = "ohne Nachweis" if not aus else ("fertig" if len(da) == len(aus) else ("teilweise" if da else "offen"))
        ws = [wissen_status(w) for w in v.get("wissen", [])]
        if v.get("sammel"):                      # Sammelvorgang: Status aus den Themen, nicht aus der Sammeldatei
            n = sum(w["status"] == "fertig" for w in ws)
            status = "fertig" if n == len(ws) else ("teilweise" if n else "offen")
        b = [dict(id=x["id"], titel=x["titel"]) for x in bef if f"[{i}]" in x["text"] or any(re.search(rf"\b{w}\b", x["text"]) for w in v.get("wissen", []))]
        e = [x for x in ent if set(x["bt"]) & set(v.get("bt", []))]
        for r in v.get("req", []):
            if r not in req: fehler.append(f"{i}: unbekannte Anforderung {r}")
        for d in v.get("doc", []):
            if not (ROOT / d).exists(): fehler.append(f"{i}: Dokument fehlt {d}")
        knoten.append(dict(id=i, name=name, dauer=dur, vorgaenger=vor, nachfolger=nach[i], ressourcen=res, notiz=notiz,
                           es=es[i], ef=ef[i], puffer=round(lf[i] - ef[i], 2), kritisch=abs(lf[i] - ef[i]) < 1e-9, status=status,
                           req=[dict(id=r, text=req.get(r, "?")) for r in v.get("req", [])],
                           bt=[dict(id=x, name=bt_namen.get(x, "?")) for x in v.get("bt", [])],
                           wissen=ws, doc=v.get("doc", []), aus=[dict(glob=g, vorhanden=g in da) for g in aus],
                           befunde=b, entscheidungen=e, software=[sw_status(x) for x in SW.get(i, [])],
                           teile=[dict(pos=t['pos'], bt=t['bt'], benennung=t['benennung'], menge=t['menge'], art=t['art']) for t in teile_alle
                                  if i in re.split(r',\s*', t['vorgang']) or (i in ('SL1', 'SL2'))]))
    ohne = [r for r in req if not any(r in [x["id"] for x in k["req"]] for k in knoten)]
    netz = dict(hinweis="KI-generiert (pm/plan/wissensnetz.py). Dauern sind Annahmen.", projektdauer_AT=ende, knoten=knoten, stueckliste=teile_alle,
                anforderungen_ohne_vorgang=ohne, pruef_fehler=fehler,
                anforderungen=lese_anf_voll(), dokumente=lese_dokumente(), bericht=lese_bericht(), bausteine=lese_bausteine(),
                steckbriefe=lese_steckbriefe(), recherche_alle=lese_recherche_alle())
    (HIER / "wissensnetz.json").write_text(json.dumps(netz, ensure_ascii=False, indent=1))

    # Anforderungsverfolgung erzeugen (REQ-D03): REQ -> Vorgänge -> Nachweise
    z = ["| Dok.-Nr. | BAT-DOC-03 | Version | 0.2 | Status | Entwurf |\n|---|---|---|---|---|---|\n"
         "| Titel | Anforderungsverfolgung (erzeugt aus dem Netzplan) | Ersteller | Claude Opus (KI), pm/plan/wissensnetz.py | Prüfer | – (Mensch offen) |\n\n"
         "> **KI-generiert.** Nicht von Hand bearbeiten: `python3 pm/plan/wissensnetz.py` schreibt diese Datei neu. Entwurf, nicht freigegeben.\n\n"
         "| REQ | Anforderung | Vorgänge | Nachweise (Ergebnis, Befund) | Status |\n|---|---|---|---|---|\n"]
    for r, txt in req.items():
        ks = [k for k in knoten if r in [x["id"] for x in k["req"]]]
        nachw = sorted({a["glob"] for k in ks for a in k["aus"] if a["vorhanden"]} | {b["id"] for k in ks for b in k["befunde"]})
        st = "kein Vorgang" if not ks else ("erfüllt? (Mensch prüft)" if ks and all(k["status"] == "fertig" for k in ks) else
                                            ("in Arbeit" if any(k["status"] in ("fertig", "teilweise") for k in ks) else "offen"))
        z.append(f"| {r} | {txt[:70]} | {', '.join(k['id'] for k in ks) or '–'} | {', '.join(nachw) or '–'} | {st} |\n")
    z.append(f"\n---\n*KI-generiert. Erzeugt aus pm/plan/wissensnetz.json. Prüffehler: {len(fehler)}.*\n")
    (ROOT / "docs/03_anforderungsverfolgung.md").write_text("".join(z))

    # Verknüpfungen in die Notizen des Planer-Plans
    plan = json.loads((HIER / "plan_batterie.json").read_text())
    for t, k in zip(plan["tasks"], knoten):
        teile = [k["notiz"], f"Status: {k['status']}"]
        for feld, lab in (("req", "REQ"), ("bt", "Bauteil"), ("wissen", "Wissen"), ("befunde", "Befunde"), ("entscheidungen", "ENT")):
            if k[feld]: teile.append(f"{lab}: " + ", ".join(x["id"] for x in k[feld]))
        if k["teile"] and k["id"] not in ("SL1", "SL2"): teile.append("Stückliste: " + ", ".join(t["pos"] for t in k["teile"]))
        if k["software"]: teile.append("Software: " + ", ".join(x["name"] for x in k["software"]))
        if k["doc"]: teile.append("Doku: " + ", ".join(k["doc"]))
        if k["aus"]: teile.append("Ergebnis: " + ", ".join(a["glob"] + (" ✓" if a["vorhanden"] else "") for a in k["aus"]))
        t["notes"] = " | ".join(x for x in teile if x)
    (HIER / "plan_batterie.json").write_text(json.dumps(plan, ensure_ascii=False, indent=2))
    zs = {s: sum(k["status"] == s for k in knoten) for s in ("fertig", "teilweise", "offen", "ohne Nachweis")}
    import subprocess   # Ansichten aus derselben JSON mit erzeugen (HTML, Obsidian)
    for skript in ("wissensnetz_ansicht.py", "wissensnetz_obsidian.py"):
        if (HIER / skript).exists(): subprocess.run([sys.executable, str(HIER / skript)], check=False, capture_output=True)
    print(f"{len(knoten)} Vorgänge {zs}; Anforderungen ohne Vorgang: {ohne or 'keine'}; Prüffehler: {fehler or 'keine'}")


if __name__ == "__main__":
    main()
