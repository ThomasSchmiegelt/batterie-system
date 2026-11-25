#!/usr/bin/env python3
# KI-generiert (Claude Sonnet, 2026-11-25), Entwurf. W1 (ERW-W1, sim/elektrik/w1_kolibri_waechter/ERWARTUNG.md).
# Allgemeiner Wächter: startet eine Rechnung als Unterprozess, liest alle POLL_S s die Messgrößen, fragt Kolibri (PI, ohne Werkzeuge) nach einer
# Aktion als JSON und führt NUR aus, was die Grenzen der Konfiguration erlauben. Die Rechnung selbst steckt in einem Konfigurationsmodul
# (z. B. rechnen/kolibri_waechter_cmu.py), das die Funktionen vorbereiten/starten/messen/nach_lauf/bericht und die Tabelle ERLAUBT liefert.
#
# Aufruf:  python3 rechnen/kolibri_waechter.py kolibri_waechter_cmu [--probe]
# Feste Grenzen (nicht von Kolibri änderbar, ERWARTUNG.md):
#   - Parameter nur aus cfg.ERLAUBT (Name, Wertebereich); alles andere wird verworfen und protokolliert
#   - höchstens MAX_NEUSTARTS Neustarts, höchstens MAX_MIN Minuten Gesamtzeit, nur CPU (nice)
#   - Regeln (DRC, Kriechstrecken) werden nie gelockert: es gibt keinen Parameter dafür; Versuche werden als lockerung_versuch markiert
# Abbruch an OPUS: Neustartlimit erreicht ohne Erfolg; Kolibri liefert > 3 Mal in Folge kein gültiges JSON; "aufgeben".
import sys, os, re, json, time, signal, subprocess, importlib, datetime, pathlib, shlex

POLL_S = 30
MAX_NEUSTARTS = 6
MAX_MIN = 90
MAX_UNGUELTIG = 3
PI = os.path.expanduser("~/.npm-global/bin/pi")
MONITORING = "/home/cae/hermes/batterie/forschung/modelltest/monitoring.csv"
LOCKERUNG = re.compile(r"abstand|clearance|kriech|drc|regel|breite|width|via|min_|toleranz|rule", re.I)

def jetzt(): return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def key():
    for z in reversed(open(os.path.expanduser("~/.bashrc")).read().splitlines()):
        m = re.match(r'export FRANCONIA_API_KEY=["\']?([^"\']+)["\']?', z)
        if m: return m.group(1)
    raise SystemExit("FRANCONIA_API_KEY nicht gefunden")

def kolibri(bericht):
    """Ein Aufruf von Kolibri 1. Rückgabe (text, usage, dauer_s). Befehl wie im Auftrag vorgegeben."""
    t0 = time.time()
    cmd = [PI, "--provider", "franconia", "--model", "Kolibri 1", "--api-key", key(), "--no-tools", "--no-extensions", "--no-skills",
           "--no-session", "--no-context-files", "--mode", "json", "-p", bericht]
    try:
        r = subprocess.run(cmd, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=180)
    except subprocess.TimeoutExpired:
        return "", {}, time.time() - t0
    text, usage = "", {}
    for z in r.stdout.splitlines():
        try: e = json.loads(z)
        except Exception: continue
        if e.get("type") == "message_end" and e.get("message", {}).get("role") == "assistant":
            text = "".join(c.get("text", "") for c in e["message"].get("content", []) if c.get("type") == "text")
            usage = e["message"].get("usage", {})
    return text, usage, time.time() - t0

def json_aus(text):
    t = text.strip()
    m = re.search(r"\{.*\}", t, re.S)
    if not m: return None
    try: d = json.loads(m.group(0))
    except Exception: return None
    return d if isinstance(d, dict) and d.get("aktion") in ("weiter", "neustart", "fertig", "aufgeben") else None

def pruefe_parameter(vorschlag, erlaubt, aktuell):
    """Gibt (angenommen, verworfen) zurück. erlaubt[name] = Funktion(wert) -> (ok, grund)."""
    ang, verw = {}, []
    if not isinstance(vorschlag, dict): return ang, [dict(key="parameter", grund="kein Objekt")]
    for k, v in vorschlag.items():
        if k not in erlaubt:
            verw.append(dict(key=k, wert=v, grund="nicht in der Erlaubtliste", lockerung_versuch=bool(LOCKERUNG.search(k))))
            continue
        ok, grund = erlaubt[k](v)
        if not ok: verw.append(dict(key=k, wert=v, grund=grund)); continue
        ang[k] = v
    return ang, verw

def anhaengen(pfad, zeile):
    with open(pfad, "a") as f: f.write(zeile + "\n")

def beenden(proc):
    if proc and proc.poll() is None:
        try: os.killpg(proc.pid, signal.SIGTERM)
        except Exception: pass
        for _ in range(20):
            if proc.poll() is not None: break
            time.sleep(0.5)
        if proc.poll() is None:
            try: os.killpg(proc.pid, signal.SIGKILL)
            except Exception: pass

def main():
    cfg = importlib.import_module(sys.argv[1])
    ordner = pathlib.Path(cfg.ORDNER); ordner.mkdir(parents=True, exist_ok=True)
    lo = pathlib.Path(getattr(cfg, "LOGORDNER", cfg.ORDNER)); lo.mkdir(parents=True, exist_ok=True)
    LOG = lo / "waechter_log.jsonl"; VERLAUF = lo / "verlauf.csv"; STATUS = lo / "status.json"
    t_start = time.time(); params = dict(cfg.START); runs = []; neustarts = 0; ungueltig = 0; status = "laeuft"; abbruch = ""
    if not VERLAUF.exists(): VERLAUF.write_text("t_s;lauf;pass;offen;verletzungen;variante\n")
    def log(d): d["zeit"] = jetzt(); anhaengen(LOG, json.dumps(d, ensure_ascii=False))
    log(dict(ereignis="start", grenzen=dict(max_neustarts=MAX_NEUSTARTS, max_min=MAX_MIN, poll_s=POLL_S), start=params, erlaubt=list(cfg.ERLAUBT)))
    lauf = 0; proc = None
    while status == "laeuft":
        lauf += 1; ld = ordner / f"lauf_{lauf:02d}"; t_lauf = time.time()
        log(dict(ereignis="lauf_start", lauf=lauf, parameter=params))
        try:
            cfg.vorbereiten(params, ld); proc = cfg.starten(params, ld)
        except Exception as e:
            log(dict(ereignis="fehler_vorbereitung", lauf=lauf, fehler=repr(e))); status = "abbruch"; abbruch = f"Vorbereitung gescheitert: {e!r}"; break
        gesehen = None; passes_vor = 0; ergebnis = None; entschieden_neustart = False; ende_fragen = 0
        while True:
            time.sleep(POLL_S if "--probe" not in sys.argv else 5)
            laeuft = proc.poll() is None; m = cfg.messen(ld, params, t_lauf)
            for p in m["passes"][passes_vor:]:
                anhaengen(VERLAUF, f"{p['t_abs'] - t_start:.0f};{lauf};{p['nr']};{p['offen']};{p['verletzungen']};{params.get('bohrungsvariante','')}")
            passes_vor = len(m["passes"])
            gesamt_min = (time.time() - t_start) / 60
            if gesamt_min > MAX_MIN:
                beenden(proc); log(dict(ereignis="zeitlimit", lauf=lauf, minuten=round(gesamt_min, 1))); status = "zeitlimit"; abbruch = f"{MAX_MIN} min Gesamtzeit erreicht"; break
            if not laeuft and ergebnis is None:
                ergebnis = cfg.nach_lauf(params, ld); m["ergebnis"] = ergebnis
                log(dict(ereignis="lauf_ende", lauf=lauf, ergebnis=ergebnis, messung=cfg.kurz(m)))
                if cfg.erfolg(ergebnis):
                    status = "erfolg"; runs.append(dict(lauf=lauf, parameter=dict(params), ergebnis=ergebnis, passes=m["passes"])); break
            sig = (len(m["passes"]), laeuft)
            if sig == gesehen or (not m["passes"] and laeuft): continue
            gesehen = sig
            bericht = cfg.bericht(dict(lauf=lauf, parameter=params, messung=m, laeuft=laeuft, ergebnis=ergebnis, gesamt_min=round(gesamt_min, 1),
                                       rest_min=round(MAX_MIN - gesamt_min, 1), neustarts=neustarts, neustarts_max=MAX_NEUSTARTS, runs=runs))
            text, usage, dauer = kolibri(bericht); d = json_aus(text)
            e = dict(ereignis="kolibri", lauf=lauf, zustand=cfg.kurz(m), laeuft=laeuft, antwort=text.strip()[:700], dauer_s=round(dauer, 1),
                     tokens=dict(eingabe=usage.get("input"), ausgabe=usage.get("output"), summe=usage.get("totalTokens")), json_ok=d is not None, t_s=round(time.time() - t_start))
            anhaengen(MONITORING, f"{jetzt()};kolibri;waechter_routing;{dauer:.0f};{len(text)};{1 if d else 0};{0 if d else 1};{1 if not text else 0}")
            if d is None:
                ungueltig += 1; e.update(entscheidung="verworfen: kein gültiges JSON", folge_ungueltig=ungueltig); log(e)
                if ungueltig > MAX_UNGUELTIG:
                    beenden(proc); status = "abbruch"; abbruch = f"Kolibri lieferte {ungueltig} Mal in Folge kein gültiges JSON"; break
                continue
            ungueltig = 0; a = d["aktion"]; ang, verw = pruefe_parameter(d.get("parameter"), cfg.ERLAUBT, params)
            e.update(aktion=a, vorschlag=d.get("parameter"), angenommen=ang, verworfen=verw, begruendung=str(d.get("begruendung", ""))[:300])
            if a == "weiter":
                e["entscheidung"] = "angenommen: weiter" if laeuft else "verworfen: Lauf ist beendet, weiter nicht möglich"
                log(e)
                if not laeuft: pass
            elif a == "neustart":
                neu = dict(params); neu.update(ang)
                if not ang: e["entscheidung"] = "verworfen: neustart ohne gültigen Parameter"; log(e)
                elif neu == params: e["entscheidung"] = "verworfen: Parameter unverändert (Neustart wirkungslos)"; log(e)
                elif neustarts >= MAX_NEUSTARTS:
                    e["entscheidung"] = f"verworfen: {MAX_NEUSTARTS} Neustarts verbraucht"; log(e); beenden(proc); status = "abbruch"; abbruch = "Neustartlimit erreicht ohne Erfolg"; break
                else:
                    e["entscheidung"] = "angenommen: neustart"; log(e); beenden(proc)
                    runs.append(dict(lauf=lauf, parameter=dict(params), ergebnis=ergebnis, passes=m["passes"], beendet="neustart durch Kolibri"))
                    params = neu; neustarts += 1; entschieden_neustart = True; break
            elif a == "fertig":
                if not laeuft and ergebnis is not None and cfg.erfolg(ergebnis):
                    e["entscheidung"] = "angenommen: fertig"; log(e); status = "erfolg"; break
                if not laeuft:
                    e["entscheidung"] = "angenommen: fertig (ohne Erfolgskriterium, Lauf beendet)"; log(e); status = "fertig_ohne_erfolg"; break
                e["entscheidung"] = "verworfen: fertig, solange der Lauf läuft und Erfolgskriterium nicht erfüllt"; log(e)
            elif a == "aufgeben":
                e["entscheidung"] = "angenommen: aufgeben"; log(e); beenden(proc); status = "abbruch"; abbruch = "Kolibri gibt auf"; break
            if not laeuft and not entschieden_neustart and status == "laeuft":
                ende_fragen += 1; gesehen = None   # Lauf beendet, kein gültiger Neustart: erneut fragen, höchstens 3 Mal
                if ende_fragen >= 3:
                    status = "abbruch"; abbruch = "Lauf beendet ohne Erfolg, Kolibri liefert keinen gültigen Neustart (3 Anfragen)"; break
        if status != "laeuft":
            if proc and proc.poll() is None: beenden(proc)
            if not runs or runs[-1]["lauf"] != lauf: runs.append(dict(lauf=lauf, parameter=dict(params), ergebnis=ergebnis, passes=m["passes"], beendet=status))
            break
    ende = dict(status=status, abbruch=abbruch, laeufe=lauf, neustarts=neustarts, minuten=round((time.time() - t_start) / 60, 1), parameter_final=params, runs=runs)
    STATUS.write_text(json.dumps(ende, ensure_ascii=False, indent=1)); log(dict(ereignis="ende", **{k: v for k, v in ende.items() if k != "runs"}))
    print(json.dumps({k: v for k, v in ende.items() if k != "runs"}, ensure_ascii=False))

if __name__ == "__main__": main()
