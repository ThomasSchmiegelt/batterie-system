# KI-generiert (Claude Sonnet, 2026-11-25), Entwurf. Konfiguration des Wächters (rechnen/kolibri_waechter.py) für W1: CMU-Routing (Freerouting) mit Befestigungsbohrungen.
# Verfahren wie E3 (sim/elektrik/e3_platine): DSN-Export, Freerouting-Jar $FREEROUTING, SES-Import, DRC mit den E3-Regeln (drc_LFP.kicad_dru, ENT-168/ENT-183), unverändert.
import os, re, json, time, shutil, subprocess, pathlib, datetime, sys
H = pathlib.Path("/home/cae/hermes/batterie"); SIM = H / "sim/elektrik/w1_kolibri_waechter"; W = pathlib.Path("/home/cae/cae_projekte/batterie/w1")
sys.path.insert(0, str(SIM)); import strip_pcb
ORDNER = W / "waechter"; LOGORDNER = SIM
KP = str(H / "werkzeuge/kicad-python.sh"); KC = str(H / "werkzeuge/kicad-cli.sh"); FR = os.environ.get("FREEROUTING", "/home/cae/.local/opt/freerouting/freerouting.sh")
VAR = ("B4", "B4v", "B3", "B2K")
def _in(menge): return lambda v: (v in menge, f"Wert nicht in {menge}")
def _passes(v): return (isinstance(v, int) and not isinstance(v, bool) and 20 <= v <= 200, "max_passes nur 20 bis 200")
ERLAUBT = {   # Erlaubtliste ERWARTUNG.md; für "Schwelle" ist kein Wertebereich festgelegt -> verworfen (offene Frage an Opus)
    "bohrungsvariante": _in(VAR), "max_passes": _passes, "optimierung": _in(("an", "aus")),
    "optimierung_schwelle": lambda v: (False, "Wertebereich der Schwelle nicht festgelegt (offene Frage an Opus)"),
    "reihenfolge": _in(("standard", "t_zuerst")), "fanout": _in(("ja", "nein")),
}
START = dict(bohrungsvariante="B4", max_passes=20, optimierung="an", reihenfolge="standard", fanout="nein")

def _run(cmd, **kw): return subprocess.run(cmd, capture_output=True, text=True, **kw)

def vorbereiten(p, ld):
    ld.mkdir(parents=True, exist_ok=True)
    shutil.copy(W / "start/route_LFP.kicad_pro", ld / "cmu_LFP.kicad_pro")
    strip_pcb.strip(str(W / "start/start_LFP.kicad_pcb"), str(ld / "s.kicad_pcb"))
    r = _run(["nice", "-n", "10", KP, str(SIM / "w1_platine.py"), "bereit", str(ld / "s.kicad_pcb"), str(ld / "cmu_LFP.kicad_pcb"), p["bohrungsvariante"]])
    if not (ld / "cmu_LFP.dsn").exists(): raise RuntimeError("DSN-Export fehlgeschlagen: " + (r.stdout + r.stderr)[-300:])
    notiz = []
    if p["reihenfolge"] == "t_zuerst":   # Netze T* (Spannungsmessleitungen der AFE-Eingänge) im DSN-Netzblock zuerst; Wirkung auf Freerouting ungeprüft
        t = (ld / "cmu_LFP.dsn").read_text(); i = t.index("  (network"); j = t.index("\n  )\n", i)   # Ende des network-Blocks (Klammer auf Einrückung 2)
        kopf, rumpf = t[:i], t[i:j]
        teile = re.split(r"(?=\n    \(net )", rumpf); vor, netze = teile[0], teile[1:]
        netze.sort(key=lambda x: 0 if re.match(r"\n    \(net T\d+\b", x) else 1)
        (ld / "cmu_LFP.dsn").write_text(kopf + vor + "".join(netze) + t[j:]); notiz.append("DSN: T-Netze zuerst")
    if p["fanout"] == "ja": notiz.append("fanout=ja: kein Schalter in der Freerouting-CLI, nicht umgesetzt")
    (ld / "notiz.txt").write_text("\n".join(notiz))

def starten(p, ld):
    cmd = ["nice", "-n", "10", FR, "-de", "cmu_LFP.dsn", "-do", "cmu_LFP.ses", "-mp", str(p["max_passes"]), "-mt", "5", "-l", "en"]
    cmd.append("--router.optimizer.enabled=" + ("true" if p["optimierung"] == "an" else "false"))   # Wirkung nicht bestätigt, Lauflog prüfen
    return subprocess.Popen(cmd, cwd=str(ld), stdout=open(ld / "fr.log", "w"), stderr=subprocess.STDOUT, start_new_session=True)

PASS = re.compile(r"^(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d)\.\d+ INFO .*Auto-routing pass #(\d+) .* in ([\d.]+) seconds with score ([\d.]+) \((\d+) unrouted and (\d+) violations?\)")
def messen(ld, p, t_lauf):
    ps = []; log = ld / "fr.log"; ende = ""
    if log.exists():
        for z in log.read_text(errors="replace").splitlines():
            m = PASS.match(z)
            if m:
                ps.append(dict(nr=int(m[2]), sek=float(m[3]), score=float(m[4]), offen=int(m[5]), verletzungen=int(m[6]),
                               t_abs=datetime.datetime.strptime(m[1], "%Y-%m-%d %H:%M:%S").timestamp()))
            if "Skipping optimization" in z or "Optimization" in z or "finished with state" in z: ende = z[24:200]
    return dict(passes=ps, minuten=round((time.time() - t_lauf) / 60, 1), ende=ende)

def nach_lauf(p, ld):
    if not (ld / "cmu_LFP.ses").exists(): return dict(ses=False)
    r = _run(["nice", "-n", "10", KP, str(SIM / "w1_platine.py"), "ses", str(ld / "cmu_LFP.kicad_pcb"), str(ld / "cmu_LFP.ses"), str(ld / "cmu_LFP_geroutet.kicad_pcb"), p["bohrungsvariante"]])
    imp = "SES True" in r.stdout
    if not (ld / "cmu_LFP_geroutet.kicad_pcb").exists(): return dict(ses=True, import_ok=imp, fehler="Board nicht gespeichert")
    shutil.copy(W / "start/drc_LFP.kicad_pro", ld / "cmu_LFP_geroutet.kicad_pro"); shutil.copy(W / "start/drc_LFP.kicad_dru", ld / "cmu_LFP_geroutet.kicad_dru")
    _run(["nice", "-n", "10", KC, "pcb", "drc", "--severity-all", "--format", "json", "-o", str(ld / "drc.json"), str(ld / "cmu_LFP_geroutet.kicad_pcb")])
    try: d = json.load(open(ld / "drc.json"))
    except Exception: return dict(ses=True, import_ok=imp, fehler="DRC-Datei fehlt")
    typen = {}
    for v in d.get("violations", []): typen[v["type"]] = typen.get(v["type"], 0) + 1
    return dict(ses=True, import_ok=imp, drc_verletzungen=len(d.get("violations", [])), offen=len(d.get("unconnected_items", [])), typen=typen)

def erfolg(e): return bool(e) and e.get("ses") and e.get("import_ok") and e.get("offen") == 0 and e.get("drc_verletzungen") == 0

def kurz(m):
    p = m["passes"]; k = dict(minuten=m["minuten"])
    if p: k.update(pass_=p[-1]["nr"], offen=p[-1]["offen"], verletzungen=p[-1]["verletzungen"])
    if m.get("ergebnis"): k["drc"] = m["ergebnis"]
    return k

def bericht(z):
    m = z["messung"]; verlauf = [(p["nr"], p["offen"]) for p in m["passes"]][-12:]
    gl = [f"Lauf {r['lauf']} {r['parameter']['bohrungsvariante']}: offen letzter Pass {r['passes'][-1]['offen'] if r['passes'] else '-'}" + (f", DRC {r['ergebnis']}" if r.get("ergebnis") else "") for r in z["runs"]]
    return ("Du überwachst Freerouting für eine Platine (120x60 mm, 4 Lagen, 4 Befestigungsbohrungen M3). Ziel: 0 offene Verbindungen und DRC 0.\n"
            f"Lauf {z['lauf']}, Parameter {json.dumps(z['parameter'])}, läuft: {z['laeuft']}, Laufzeit {m['minuten']} min, gesamt {z['gesamt_min']} min (Rest {z['rest_min']}), Neustarts {z['neustarts']} von {z['neustarts_max']}.\n"
            f"Verlauf (Pass, offene Verbindungen): {verlauf}. Ein Pass dauert etwa 2 min.\n"
            + (f"Frühere Läufe: {'; '.join(gl)}.\n" if gl else "") + (f"Ergebnis nach Lauf: {json.dumps(z['ergebnis'])}.\n" if z["ergebnis"] else "")
            + "Du darfst nur diese Parameter setzen: bohrungsvariante (B4 = 4 Ecken, B4v = 4 Ecken je 2 mm nach innen, B3 = 3 Bohrungen, B2K = 2 Bohrungen mit Klemmleiste), max_passes (20 bis 200), optimierung (an/aus), reihenfolge (standard/t_zuerst), fanout (ja/nein; das Fanout macht der Router bereits selbst, der Schalter ist wirkungslos).\n"
            "Antworte NUR mit einem JSON-Objekt, kein anderer Text: {\"aktion\": \"weiter\" | \"neustart\" | \"fertig\" | \"aufgeben\", \"parameter\": {...nur bei neustart...}, \"begruendung\": \"ein Satz\"}")
