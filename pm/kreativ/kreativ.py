#!/usr/bin/env python3
"""kreativ.py: Kreativmethoden (TRIZ, Morphologischer Kasten, Kopfstand) mit Paarvergleich. KI-generiert (Claude Sonnet, Auftrag Opus, 2026-11-24). Status Entwurf.
Methode: pm/kreativ/METHODE.md (BAT-KR-00). Eine Sitzung = ein Ordner pm/kreativ/KRn/.

BEDIENUNG (im Projektordner, `source umgebung.sh`):
  python3 pm/kreativ/kreativ.py <befehl> KRn
  Eingaben von Hand (Opus/Autor): KRn/problem.json (Widerspruch, Parameternummern, Teilfunktionen, Kriterien, fakten F1..),
                                  KRn/ausschluesse.json (Stufe 4), KRn/gewichte.json (Stufe 6, vom Autor)
  Befehle (Stufe):
    triz      (2) Matrix -> Prinzipien, PI liefert Ideen        -> triz.json
    kasten    (3) PI füllt den Kasten, oder kasten_vorgabe.json (Opus) wird übernommen -> kasten.json
    konzepte  (4) Auswahl 5-8 Konzepte (Hamming) oder, wenn konzepte_vorgabe.json da ist, nur Prüfung (Ausschlüsse, Hamming >= 2) -> konzepte.json
    kopfstand (5) PI: wie scheitert das Konzept?               -> kopfstand.json
    formular  (6) Dreiecksmatrix für den Autor                 -> gewichte_formular.md (und vorläufig gleiche Gewichte)
    paare     (7) PI-Paarurteile, beide Reihenfolgen, setzt fort-> paare.json (Nachfragen nur bei Zirkeln/Widersprüchen, max. 2)
    rang      (8) Konsistenz, Rang, Empfindlichkeit, Bild      -> rang.json, rang.png
  PI-Aufrufe: nur bei freier GPU (fremder Rechenprozess -> Abbruch), Rohantworten in KRn/roh/. Ungültiges JSON: höchstens 2 Neuversuche.
  Zahlen im Paarurteil nur aus den fakten (ID F..); das Skript prüft ID und Zahl und markiert Verstöße.
  Lange Läufe losgelöst: systemd-run --user --scope --unit=hermes-batterie-kr1 setsid python3 pm/kreativ/kreativ.py paare KR1
"""
import sys, os, json, re, subprocess, itertools, time, datetime

HIER = os.path.dirname(os.path.abspath(__file__))
PI = os.path.expanduser("~/.npm-global/bin/pi")
MODELL = os.environ.get("MODELL", "qwen-gross:latest")
SYS = ("Du bist ein sachlicher Entwicklungsingenieur für Batteriesysteme. Antworte ausschließlich mit gültigem JSON, "
       "ohne Text davor oder danach, ohne Markdown. Erfinde keine Zahlen: Zahlen darfst du nur aus den angegebenen FAKTEN "
       "(mit ihrer ID) verwenden; gibt es keine passende Zahl, nimm null. Deutsch, kurze Sätze.")


class Abbruch(Exception):
    pass


def jl(p, d=None):
    if d is None:
        return json.load(open(p, encoding="utf-8"))
    json.dump(d, open(p + ".tmp", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    os.replace(p + ".tmp", p)


def gpu_frei():
    try:
        o = subprocess.run(["nvidia-smi", "--query-compute-apps=pid,name", "--format=csv,noheader"],
                           capture_output=True, text=True, timeout=30).stdout
    except Exception as e:
        raise Abbruch(f"nvidia-smi nicht lesbar: {e}")
    fremd = [z for z in o.strip().splitlines() if z.strip() and "ollama" not in z.lower()]
    if fremd:
        raise Abbruch("GPU durch fremden Prozess belegt: " + "; ".join(fremd))


def json_aus(text):
    t = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.M).strip()
    for a, b in (("{", "}"), ("[", "]")):
        i, j = t.find(a), t.rfind(b)
        if i >= 0 and j > i:
            try:
                return json.loads(t[i:j + 1])
            except Exception:
                pass
    raise ValueError("kein gültiges JSON")


def frage_pi(prompt, kr, name):
    """Eine PI-Frage (lokal, ohne Werkzeuge). Rückgabe: Rohtext. Rohantwort nach KRn/roh/."""
    gpu_frei()
    os.makedirs(f"{kr}/roh", exist_ok=True)
    r = subprocess.run([PI, "--provider", "ollama", "--model", MODELL, "--no-tools", "--no-extensions", "--no-skills",
                        "--no-prompt-templates", "--no-context-files", "--offline", "--system-prompt", SYS,
                        "--no-session", "-p", prompt], capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=900)
    open(f"{kr}/roh/{name}.txt", "w", encoding="utf-8").write(r.stdout + ("\n[stderr]\n" + r.stderr if r.stderr.strip() else ""))
    return r.stdout


def frage_json(prompt, kr, name, pruefer=None):
    """PI als JSON, höchstens zwei Neuversuche (insgesamt 3). pruefer(obj) darf ValueError werfen."""
    letzt = None
    for k in range(3):
        t = frage_pi(prompt if k == 0 else prompt + "\n\nHinweis: Deine letzte Antwort war kein gültiges JSON im verlangten Format. Antworte NUR mit dem JSON.",
                     kr, f"{name}_v{k + 1}")
        try:
            o = json_aus(t)
            if pruefer:
                pruefer(o)
            return o
        except Exception as e:
            letzt = e
    raise Abbruch(f"{name}: nach 3 Versuchen kein gültiges JSON ({letzt})")


def aktive(kr):
    """Konzepte ohne die per Festforderung ausgeschiedenen (ausschluss_fest.json). Rückgabe (aktiv, ausgeschieden)."""
    kz = jl(f"{kr}/konzepte.json")["konzepte"]
    f = f"{kr}/ausschluss_fest.json"
    if not os.path.exists(f):
        return kz, []
    aus = jl(f)["ausgeschieden"]
    ids = {a["konzept"] for a in aus}
    return [c for c in kz if c["id"] not in ids], aus


def laden(kr):
    return jl(f"{kr}/problem.json"), jl(f"{HIER}/triz_daten.json")


def fakten_text(p):
    return "FAKTEN (nur diese Zahlen sind erlaubt):\n" + "\n".join(f"{k}: {v['text']}  [Quelle: {v['quelle']}]" for k, v in p["fakten"].items())


def kontext(p):
    return (f"AUFGABE: {p['titel']} (Bauteil {p['bezug']['BT']}, Anforderung {p['bezug']['REQ']}).\n"
            f"WIDERSPRUCH: {p['widerspruch']}\n{fakten_text(p)}")


# ---------------- Stufe 2 TRIZ
def cmd_triz(kr):
    p, t = laden(kr)
    zellen, zaehl = [], {}
    for v in p["verbessern"]:
        for w in p["verschlechtern"]:
            pr = t["matrix"].get(f"{v}-{w}", [])
            zellen.append({"verbessern": v, "verbessern_name": t["parameter"][str(v)], "verschlechtern": w,
                           "verschlechtern_name": t["parameter"][str(w)], "prinzipien": pr})
            for i, n in enumerate(pr):
                zaehl.setdefault(n, []).append(i)
    # Rangfolge: Häufigkeit über die Zellen, dann Position in der Zelle
    rang = sorted(zaehl, key=lambda n: (-len(zaehl[n]), sum(zaehl[n]) / len(zaehl[n]), n))
    pl = "\n".join(f"{n}: {t['prinzipien'][str(n)]}" for n in rang)

    def pruef(o):
        if not isinstance(o, dict) or not all(str(n) in o and isinstance(o[str(n)], list) and len(o[str(n)]) >= 2 for n in rang):
            raise ValueError("Prinzip fehlt")
    pr = (kontext(p) + "\n\nTRIZ-Prinzipien aus der Widerspruchsmatrix (Nummer: Name):\n" + pl +
          "\n\nAUFTRAG: Nenne zu JEDEM Prinzip 2 bis 3 konkrete Ideen für " + p.get("triz_gegenstand", "den Zellausgleich (Balancing) einer Batteriezellüberwachung") + ". "
          'Antwort als JSON-Objekt {"<Prinzipnummer>": ["Idee 1","Idee 2"], ...}, Ideen in je einem Satz.')
    ideen = frage_json(pr, kr, "triz", pruef)
    out = {"kopf": "KI-generiert (Claude Sonnet, 2026-11-24). Matrix: pm/kreativ/triz_daten.json; Ideen: PI (nicht geprüft).",
           "zellen": zellen, "rang_prinzipien": [{"nr": n, "name": t["prinzipien"][str(n)], "treffer": len(zaehl[n]),
                                                    "ideen": ideen[str(n)]} for n in rang]}
    jl(f"{kr}/triz.json", out)
    print("triz.json:", len(rang), "Prinzipien")


# ---------------- Stufe 3 Kasten
def cmd_kasten(kr):
    p, t = laden(kr)
    if os.path.exists(f"{kr}/kasten_vorgabe.json"):    # Lauf 2: Kasten von Opus vorgegeben, keine PI-Erzeugung
        v = jl(f"{kr}/kasten_vorgabe.json")
        v["kopf"] = "KI-generiert (Datei). Kasten von Opus vorgegeben (kasten_vorgabe.json), unverändert übernommen."
        jl(f"{kr}/kasten.json", v)
        print("kasten.json aus Vorgabe:", [len(z["optionen"]) for z in v["zeilen"]])
        return
    z = jl(f"{kr}/triz.json")
    tz = "\n".join(f"TRIZ-{x['nr']} {x['name']}: " + " / ".join(x["ideen"]) for x in z["rang_prinzipien"])
    zeilen = []
    for i, tf in enumerate(p["teilfunktionen"], 1):
        pr = (kontext(p) + "\n\nIDEEN AUS TRIZ (Stufe 2):\n" + tz +
              f"\n\nAUFTRAG: Morphologischer Kasten, Teilfunktion „{tf}“. Nenne genau 4 bis 5 voneinander verschiedene Ausprägungen. "
              "Die erste Ausprägung ist der Ausgangsentwurf (passiver Ausgleich mit Widerständen auf der CMU-Platine, E2/E3), falls die Teilfunktion dort festgelegt ist, sonst die einfachste übliche Lösung. "
              "Gib je Ausprägung die Herkunft an: \"TRIZ-<Nr>\" (wenn aus den TRIZ-Ideen), \"Fakt F<n>\" (wenn aus den FAKTEN) oder \"PI-Wissen\". "
              'Antwort als JSON {"optionen":[{"name":"kurz (max 8 Wörter)","quelle":"..."}]}.')

        def pruef(o):
            if not (4 <= len(o["optionen"]) <= 6):
                raise ValueError("Anzahl")
        o = frage_json(pr, kr, f"kasten_T{i}", pruef)
        zeilen.append({"id": f"T{i}", "name": tf, "optionen": [{"id": f"T{i}.{k}", "name": x["name"], "quelle": x.get("quelle", "PI-Wissen")}
                                                                for k, x in enumerate(o["optionen"][:5], 1)]})
    jl(f"{kr}/kasten.json", {"kopf": "KI-generiert (Claude Sonnet, 2026-11-24). PI-Vorschlag, auf 5 Ausprägungen je Zeile gekappt (Reihenfolge PI). Opus prüft und kürzt.",
                              "zeilen": zeilen})
    print("kasten.json:", [len(z["optionen"]) for z in zeilen])


# ---------------- Stufe 4 Konzepte
def hamming(a, b):
    return sum(x != y for x, y in zip(a, b))


def cmd_konzepte_vorgabe(kr):
    """Konzepte von Opus vorgegeben (konzepte_vorgabe.json: Leitidee + Wahl je Zeile). Das Skript prüft nur: Ausschlüsse, Hamming >= 2, Anzahl 5-8."""
    k = jl(f"{kr}/kasten.json")
    vg = jl(f"{kr}/konzepte_vorgabe.json")["konzepte"]
    aus = jl(f"{kr}/ausschluesse.json")["ausschluesse"] if os.path.exists(f"{kr}/ausschluesse.json") else []
    name = {o["id"]: o["name"] for z in k["zeilen"] for o in z["optionen"]}
    konz, fehler = [], []
    for c in vg:
        wahl = c["wahl"]
        for a in aus:
            if a["a"] in wahl and a["b"] in wahl:
                fehler.append(f"{c['id']} verletzt Ausschluss {a['a']} x {a['b']}: {a['grund']}")
        konz.append({"id": c["id"], "richtung": c["leitidee"], "leitidee": c["leitidee"], "wahl": wahl, "namen": [name[x] for x in wahl]})
    ham = {f"{a['id']}-{b['id']}": hamming(a["wahl"], b["wahl"]) for a, b in itertools.combinations(konz, 2)}
    schwach = [x for x, h in ham.items() if h < 2]
    md = min(ham.values()) if ham else 0
    jl(f"{kr}/konzepte.json", {"kopf": "KI-generiert (Datei). Konzepte von Opus vorgegeben (konzepte_vorgabe.json); Skript prüft nur Ausschlüsse und Hamming >= 2.",
                                "ausschluesse": len(aus), "min_hamming": md, "hamming_paare": ham, "konzepte": konz,
                                "pruefung": {"ausschluss_verletzt": fehler, "hamming_unter_2": schwach, "anzahl_5_bis_8": 5 <= len(konz) <= 8}})
    print(f"konzepte.json aus Vorgabe: {len(konz)} Konzepte, min. Hamming {md}, Verstöße {len(fehler)}, Hamming<2 {schwach}")
    if schwach:
        print("WARNUNG: Hamming < 2 (Opus-Vorgabe bleibt unverändert, Meldung an Opus):", schwach)
    if fehler or not 5 <= len(konz) <= 8:
        raise Abbruch("Prüfung der vorgegebenen Konzepte fehlgeschlagen: " + "; ".join(fehler))


def cmd_konzepte(kr):
    if os.path.exists(f"{kr}/konzepte_vorgabe.json"):
        return cmd_konzepte_vorgabe(kr)
    k = jl(f"{kr}/kasten.json")
    aus = jl(f"{kr}/ausschluesse.json")["ausschluesse"]
    zeilen = k["zeilen"]
    ids = [[o["id"] for o in z["optionen"]] for z in zeilen]
    verbot = [(a["a"], a["b"]) for a in aus]
    alle = []
    for c in itertools.product(*ids):
        s = set(c)
        if not any(x in s and y in s for x, y in verbot):
            alle.append(c)
    gesamt = 1
    for l in ids:
        gesamt *= len(l)
    waehl = []
    for d, richt in enumerate(ids[0]):
        kand = [c for c in alle if c[0] == richt]
        if not kand:
            continue
        if not waehl:
            waehl.append(kand[0])
            continue
        waehl.append(max(kand, key=lambda c: (min(hamming(c, w) for w in waehl), sum(hamming(c, w) for w in waehl))))
    name = {o["id"]: o["name"] for z in zeilen for o in z["optionen"]}
    konz = [{"id": f"K{i + 1}", "richtung": name[c[0]], "wahl": list(c), "namen": [name[x] for x in c]} for i, c in enumerate(waehl)]
    md = min([hamming(a, b) for a, b in itertools.combinations(waehl, 2)] or [0])
    jl(f"{kr}/konzepte.json", {"kopf": "KI-generiert (Claude Sonnet, 2026-11-24). Auswahl: eine Richtung je Ausprägung der Zeile T1, jeweils die zulässige Kombination mit größtem kleinsten Hamming-Abstand zu den schon gewählten (Start: erste zulässige Kombination).",
                                "kombinationen_gesamt": gesamt, "kombinationen_zulaessig": len(alle), "ausschluesse": len(verbot),
                                "min_hamming": md, "konzepte": konz})
    print(f"konzepte.json: {len(konz)} Konzepte, zulässig {len(alle)} von {gesamt}, min. Hamming {md}")
    if not 5 <= len(konz) <= 8:
        print("WARNUNG: Zahl der Konzepte außerhalb 5-8")


def konz_text(c, zeilen):
    return (f"Leitidee „{c['leitidee']}“. " if c.get("leitidee") else "") + "; ".join(f"{z['name']}: {n}" for z, n in zip(zeilen, c["namen"]))


# ---------------- Stufe 5 Kopfstand
def cmd_kopfstand(kr):
    p, t = laden(kr)
    kz = jl(f"{kr}/konzepte.json")["konzepte"]
    zeilen = jl(f"{kr}/kasten.json")["zeilen"]
    out = []
    for c in kz:
        pr = (kontext(p) + f"\n\nKONZEPT {c['id']}: {konz_text(c, zeilen)}\n\nAUFTRAG: Kopfstand: Wie bringe ich dieses Konzept zum Versagen? "
              'Nenne 3 Versagensarten mit Ursache und Folge. Antwort als JSON {"risiken":[{"versagen":"...","ursache":"...","folge":"...","schwere":"hoch|mittel|niedrig"}]}. '
              "Keine Zahlen außer aus den FAKTEN.")
        o = frage_json(pr, kr, f"kopf_{c['id']}", lambda o: o["risiken"][2])
        out.append({"konzept": c["id"], "risiken": o["risiken"][:3]})
    jl(f"{kr}/kopfstand.json", {"kopf": "KI-generiert (Claude Sonnet, 2026-11-24). PI-Vorschläge, Kandidaten für docs/05, ungeprüft.", "konzepte": out})
    print("kopfstand.json:", len(out))


# ---------------- Stufe 6 Formular
def cmd_formular(kr):
    p, _ = laden(kr)
    kri = p["kriterien"]
    L = ["| Dok.-Nr. | BAT-KR-F1 | Version | 0.1 | Status | Entwurf |", "|---|---|---|---|---|---|",
         f"| Titel | Gewichte der Kriterien: Paarvergleich ({p['titel']}) | Ersteller | Claude Sonnet (KI), im Auftrag von Opus | Prüfer | Autor |", "",
         "> **KI-generiert (Claude Sonnet, 2026-11-24).** Die Gewichte setzt der Autor (Abwägung). **Bis zu seiner Antwort rechnet das Skript mit gleichen Gewichten. Das Ergebnis ist deshalb vorläufig.**", "",
         "## So füllen Sie aus", "Je Zeile ein Kriterienpaar. Tragen Sie ein: **2**, wenn das Kriterium links wichtiger ist, **1**, wenn beide gleich wichtig sind, **0**, wenn das Kriterium rechts wichtiger ist. "
         "Die Summe je Kriterium (0 bis 12) wird sein Gewicht. Danach `KR1/gewichte.json` im Format `{\"gewichte\": {\"Kriterium\": Zahl, ...}, \"von\": \"Autor\"}` ablegen.", "",
         "| Nr | Kriterium links | Kriterium rechts | Eintrag (2 / 1 / 0) |", "|---|---|---|---|"]
    n = 0
    for a, b in itertools.combinations(kri, 2):
        n += 1
        L.append(f"| {n} | {a} | {b} |  |")
    L += ["", f"Kriterien ({len(kri)}), Paare: {n}.", "", "---", "*KI-generiert (Claude Sonnet, 2026-11-24). Status Entwurf. Freigabe nur durch den Autor.*"]
    open(f"{kr}/gewichte_formular.md", "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("gewichte_formular.md:", n, "Paare")


def gewichte(kr, p):
    f = f"{kr}/gewichte.json"
    if os.path.exists(f):
        g = jl(f)
        return {k: float(g["gewichte"][k]) for k in p["kriterien"]}, "Autor"
    return {k: 6.0 for k in p["kriterien"]}, "vorläufig gleich (6 je Kriterium = Paarvergleichssumme bei Gleichstand, Autor hat noch nicht geantwortet)"


# ---------------- Stufe 7 Paare
def zahlen_ok(z, fakten):
    """Prüft das Feld zahl {wert, quelle}. Quelle: eine oder mehrere Fakten-IDs (F1, F4). Jede Zahl im Feld wert muss im Text einer genannten Fakt stehen. Rückgabe (ok, Hinweis)."""
    if not z or not isinstance(z, dict) or z.get("wert") in (None, ""):
        return True, ""
    ids = re.findall(r"F\d+", str(z.get("quelle", "")))
    if not ids or any(i not in fakten for i in ids):
        return False, f"Quelle {z.get('quelle')} nicht in den Fakten"
    txt = " ".join(fakten[i]["text"] for i in ids).replace(".", ",")
    for num in re.findall(r"\d+(?:[.,]\d+)?", str(z["wert"])):
        if not re.search(r"(?<![\d,])" + re.escape(num.replace(".", ",")) + r"(?![\d])", txt):
            return False, f"Zahl {num} steht nicht in {','.join(ids)}"
    return True, ""


def paar_frage(kr, p, zeilen, kz, ci, cj, krit, nachfrage=""):
    A, B = kz[ci], kz[cj]
    defs = p.get("kriteriendefinitionen", {})
    dtxt = ("\n\nDEFINITIONEN (verbindlich):\n" + "\n".join(f"- {k}: {defs[k]}" for k in krit if k in defs)) if any(k in defs for k in krit) else ""
    pr = (kontext(p) + f"\n\nKONZEPT A ({A['id']}): {konz_text(A, zeilen)}\nKONZEPT B ({B['id']}): {konz_text(B, zeilen)}" + dtxt + "\n\n"
          "AUFTRAG: Vergleiche A und B je Kriterium. Frage je Kriterium: Welches Konzept ist besser? Gewinner \"A\", \"B\" oder \"gleich\". "
          "Begründung in einem Satz. Falls eine FAKTEN-Zahl das Urteil trägt: zahl = {\"wert\":\"...\",\"quelle\":\"F<n>\"}, sonst null. Kriterien:\n"
          + "\n".join(f"- {k}" for k in krit) +
          ('\nAntwort als JSON {"urteile":{"<Kriterium wörtlich>":{"gewinner":"A|B|gleich","grund":"...","zahl":null}}}.') + nachfrage)

    def pruef(o):
        u = o["urteile"]
        for k in krit:
            if u[k]["gewinner"] not in ("A", "B", "gleich") or not u[k].get("grund"):
                raise ValueError("Urteil")
    o = frage_json(pr, kr, f"paar_{A['id']}_{B['id']}_{int(time.time())}", pruef)
    return o["urteile"]


def cmd_paare(kr):
    p, _ = laden(kr)
    kz, _aus = aktive(kr)
    zeilen = jl(f"{kr}/kasten.json")["zeilen"]
    f = f"{kr}/paare.json"
    kri = p["kriterien"]
    neu = p.get("neu_urteilen", kri)    # Lauf 3: nur diese Kriterien neu urteilen, die übrigen aus p["uebernahme"]
    ids = {c["id"] for c in kz}
    if os.path.exists(f):
        d = jl(f)
    else:
        d = {"kopf": "KI-generiert (PI, qwen-gross, ohne Werkzeuge). Urteil je geordnetem Paar (erstes = A), Einschätzung, keine Rechnung. Zahlen aus problem.json fakten.",
             "urteile": {}, "nachfragen": []}
        if p.get("uebernahme"):
            alt = jl(f"{kr}/{p['uebernahme']}")["urteile"]
            for key, v in alt.items():
                x, y = key.split("|")
                if x in ids and y in ids:
                    d["urteile"][key] = {"stand": v["stand"], "runde": 0, "uebernommen": p["uebernahme"],
                                         "kriterien": {k: dict(c, uebernommen=True) for k, c in v["kriterien"].items() if k not in neu}}
            jl(f, d)
    n = len(kz)
    for i, j in itertools.permutations(range(n), 2):
        key = f"{kz[i]['id']}|{kz[j]['id']}"
        e = d["urteile"].setdefault(key, {"stand": "", "runde": 0, "kriterien": {}})
        need = [k for k in kri if k not in e["kriterien"]]
        if not need:
            continue
        u = paar_frage(kr, p, zeilen, kz, i, j, need)
        for k, v in u.items():
            v["zahl_ok"], v["zahl_hinweis"] = zahlen_ok(v.get("zahl"), p["fakten"])
        e["kriterien"].update(u)
        e["stand"] = datetime.datetime.now().isoformat(timespec="seconds")
        jl(f, d)
        print(key, "fertig", need, flush=True)
    kri_n = [k for k in kri if k in neu]
    # Nachfragen bei Widersprüchen und Zirkeln, höchstens zwei Runden
    for runde in (1, 2):
        probleme = finde_probleme(d, kz, kri_n)
        if not probleme["paare"]:
            break
        print(f"Nachfrage-Runde {runde}: {len(probleme['paare'])} Paar/Kriterium-Fälle", flush=True)
        je = {}
        for (a, b, k) in probleme["paare"]:
            je.setdefault((a, b), set()).add(k)
        for (a, b), ks in je.items():
            ks = sorted(ks, key=kri.index)
            for (x, y) in ((a, b), (b, a)):
                i, j = [c["id"] for c in kz].index(x), [c["id"] for c in kz].index(y)
                alt = d["urteile"][f"{x}|{y}"]["kriterien"]
                hinweis = ("\n\nNACHFRAGE: Deine früheren Urteile zu diesem Paar waren widersprüchlich (Reihenfolge oder Dreierkette). Frühere Urteile: " +
                           "; ".join(f"{k}: {alt[k]['gewinner']} ({alt[k]['grund']})" for k in ks) + ". Beurteile nur diese Kriterien neu und wäge die Begründung sorgfältig ab, "
                           "unabhängig davon, welches Konzept zuerst genannt wird.")
                u = paar_frage(kr, p, zeilen, kz, i, j, ks, hinweis)
                for k in ks:
                    v = u[k]
                    v["zahl_ok"], v["zahl_hinweis"] = zahlen_ok(v.get("zahl"), p["fakten"])
                    v["vorher"] = alt[k]["gewinner"]
                    v["runde"] = runde
                    alt[k] = v
            d["nachfragen"].append({"runde": runde, "paar": [a, b], "kriterien": ks})
            jl(f, d)
    jl(f, d)
    print("paare.json fertig")


# ---------------- Stufe 8 Auswertung
def punkt(g):
    return {"A": 1, "B": -1, "gleich": 0}[g]


def ergebnis_paar(d, a, b, k):
    """Aus beiden Reihenfolgen: (Ergebnis +1 a vorne, -1 b vorne, 0 gleich; widerspruch bool; erstes_gewinnt-Zählung)."""
    u1 = punkt(d["urteile"][f"{a}|{b}"]["kriterien"][k]["gewinner"])    # +1 heißt a gewinnt
    u2 = -punkt(d["urteile"][f"{b}|{a}"]["kriterien"][k]["gewinner"])   # in zweiter Reihenfolge ist b = A; +1 heißt a gewinnt
    wid = (u1 * u2 == -1)
    s = u1 + u2
    return (0 if wid else (1 if s > 0 else -1 if s < 0 else 0)), wid, u1, u2


def zirkel(ids, res):
    """Zählt zirkuläre Triaden. res(a,b) = +1 a schlägt b."""
    n = 0
    liste = []
    for a, b, c in itertools.combinations(ids, 3):
        for x, y, z in ((a, b, c), (a, c, b)):
            if res(x, y) == 1 and res(y, z) == 1 and res(z, x) == 1:
                n += 1
                liste.append([x, y, z])
    return n, liste


def finde_probleme(d, kz, kri):
    ids = [c["id"] for c in kz]
    paare = set()
    for k in kri:
        res = {}
        for a, b in itertools.combinations(ids, 2):
            r, wid, _, _ = ergebnis_paar(d, a, b, k)
            res[(a, b)], res[(b, a)] = r, -r
            if wid:
                paare.add((a, b, k))
        n, lst = zirkel(ids, lambda x, y: res[(x, y)])
        for t in lst:
            for x, y in ((t[0], t[1]), (t[1], t[2]), (t[2], t[0])):
                paare.add((x, y, k) if ids.index(x) < ids.index(y) else (y, x, k))
    return {"paare": sorted(paare)}


def kendall(n, dz):
    nenner = (n ** 3 - n) if n % 2 else (n ** 3 - 4 * n)
    return 1 - 24 * dz / nenner


def cmd_rang(kr):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    p, _ = laden(kr)
    kz, ausg = aktive(kr)
    d = jl(f"{kr}/paare.json")
    kri = p["kriterien"]
    ids = [c["id"] for c in kz]
    n = len(ids)
    w, wquelle = gewichte(kr, p)
    pt = {k: {i: 0.0 for i in ids} for k in kri}
    kons = {}
    erste = {"A": 0, "B": 0, "gleich": 0}
    zahl_ver = []
    for k in kri:
        res = {}
        wid, zir = [], 0
        for a, b in itertools.combinations(ids, 2):
            r, wd, u1, u2 = ergebnis_paar(d, a, b, k)
            res[(a, b)], res[(b, a)] = r, -r
            if wd:
                wid.append([a, b])
            for ur in (u1, u2):    # Sicht von a: +1 a gewinnt
                pt[k][a] += (ur + 1) / 2 / (2 * (n - 1))    # Sieg 1, gleich 0,5, Niederlage 0; Mittel über beide Reihenfolgen und alle Gegner
                pt[k][b] += (-ur + 1) / 2 / (2 * (n - 1))
        z, lst = zirkel(ids, lambda x, y: res[(x, y)])
        kons[k] = {"zirkulaere_triaden": z, "triaden": lst, "widersprueche_reihenfolge": wid, "kendall_zeta": kendall(n, z)}
        for key, v in d["urteile"].items():
            erste[v["kriterien"][k]["gewinner"]] += 1
            ok_, hin_ = zahlen_ok(v["kriterien"][k].get("zahl"), p["fakten"])
            if not ok_:
                zahl_ver.append([key, k, hin_])

    def gesamt(wg):
        s = sum(wg.values())
        return {i: sum(wg[k] * pt[k][i] for k in kri) / s for i in ids}
    basis = gesamt(w)
    rang = sorted(ids, key=lambda i: -basis[i])
    gl = gesamt({k: 6.0 for k in kri})
    vergleich = {"gewichte": "gleich (6 je Kriterium)", "gesamt": gl, "rang": sorted(ids, key=lambda i: -gl[i])}
    varianten = []
    for k in kri:
        for dl in (-1, 1):
            wg = dict(w)
            wg[k] = max(0.0, wg[k] + dl)
            varianten.append({"art": "Methode ±1", "kriterium": k, "delta": dl, "gesamt": gesamt(wg)})
    for k in kri:
        for wert in (0.0, 12.0):
            wg = dict(w)
            wg[k] = wert
            varianten.append({"art": "Zusatz Grenzwert", "kriterium": k, "delta": wert, "gesamt": gesamt(wg)})
    for v in varianten:
        v["platz1"] = max(ids, key=lambda i: v["gesamt"][i])
        v["rang"] = sorted(ids, key=lambda i: -v["gesamt"][i])
    mv = [v for v in varianten if v["art"] == "Methode ±1"]
    lo = {i: min(basis[i], *[v["gesamt"][i] for v in mv]) for i in ids}
    hi = {i: max(basis[i], *[v["gesamt"][i] for v in mv]) for i in ids}
    p1_methode = sorted({v["platz1"] for v in mv} | {rang[0]})
    p1_alle = sorted({v["platz1"] for v in varianten} | {rang[0]})
    gz = sum(k["zirkulaere_triaden"] for k in kons.values())
    ww = sum(len(k["widersprueche_reihenfolge"]) for k in kons.values())
    tot = len(d["urteile"]) * len(kri)
    out = {"gewichte": w, "gewichte_quelle": wquelle, "punkte_je_kriterium": pt, "gesamt": basis, "rang": rang,
           "konsistenz": kons, "zirkel_gesamt": gz, "widersprueche_gesamt": ww, "paarkombinationen_je_kriterium": n * (n - 1) // 2 * len(kri),
           "position": {"erster_gewinnt": erste["A"], "zweiter_gewinnt": erste["B"], "gleich": erste["gleich"], "urteile": tot},
           "vergleich_gleiche_gewichte": vergleich, "ausgeschieden_festforderung": ausg, "zahlverstoesse": zahl_ver, "nachfragen": d.get("nachfragen", []),
           "empfindlichkeit": {"von": lo, "bis": hi, "platz1_methode": p1_methode, "platz1_mit_zusatz": p1_alle, "varianten": varianten}}
    jl(f"{kr}/rang.json", out)
    # Bild
    name = {c["id"]: c["id"] + " " + c["richtung"][:46] for c in kz}
    fig, ax = plt.subplots(figsize=(11, 0.7 * n + 2.6))
    y = range(n)
    farben = ["#1f77b4" if i not in p1_alle or i == rang[0] else "#ff7f0e" for i in rang]
    ax.axvspan(0.5, 1.0, color="#2ca02c", alpha=0.10)
    ax.text(0.99, n - 0.45, "Zielband: über 0,5 = besser als der Durchschnitt aller Paare", ha="right", va="bottom", fontsize=8, color="#2ca02c")
    ax.barh(list(y), [basis[i] for i in rang], color=farben, xerr=[[basis[i] - lo[i] for i in rang], [hi[i] - basis[i] for i in rang]], capsize=3)
    ax.scatter([gl[i] for i in rang], list(y), marker="D", color="black", zorder=5, label="Vergleich: gleiche Gewichte")
    ax.legend(loc="lower right", bbox_to_anchor=(1.0, 0.08), fontsize=8)
    for yy, i in zip(y, rang):
        mark = "  ★ Platz 1 in einer Variante" if i in p1_alle else ""
        ax.text(max(hi[i], gl[i]) + 0.02, yy, f"{basis[i]:.2f}{mark}", va="center", fontsize=8)
    ax.set_yticks(list(y))
    ax.set_yticklabels([name[i] for i in rang], fontsize=8)
    ax.invert_yaxis()
    ax.set_xlim(0, 1.15)
    ax.set_xlabel("Gesamtpunkte (0 = überall unterlegen, 1 = überall überlegen)")
    ax.set_title(f"{p['titel']}: Rang der Konzepte, Gewichte {'vorläufig gleich' if wquelle.startswith('vorl') else 'vom Autor (2026-11-24)'}", fontsize=10)
    ausz = ("Ausgeschieden vor dem Vergleich (Festforderung Platine <= 105 °C bei 45 °C): " + ", ".join(a["konzept"] for a in ausg) + ".\n") if ausg else ""
    fig.text(0.01, 0.01, ausz + "Lesehilfe: Balken = gewichtete Gesamtpunkte aus allen Paarvergleichen. Schwarze Rauten = Ergebnis bei gleichen Gewichten (Vergleich).\nSchwarze Striche = Spanne, wenn jedes Gewicht um eine Stufe steigt oder sinkt.\n"
             "★ = Konzept erreicht in mindestens einer Gewichtsvariante Platz 1 (blau: schon im Ausgangsfall Platz 1, orange: nur in einer Variante).\nUrteile stammen von der KI PI (Einschätzung, keine Rechnung). KI-generiert, Entwurf.", fontsize=7, va="bottom")
    fig.tight_layout(rect=(0, 0.1, 1, 1))
    fig.savefig(f"{kr}/rang.png", dpi=130)
    print(f"rang.json, rang.png: Zirkel {gz}, Widersprüche {ww}/{tot}, Rang {rang}, Platz 1 in Varianten {p1_alle}")


BEF = {"triz": cmd_triz, "kasten": cmd_kasten, "konzepte": cmd_konzepte, "kopfstand": cmd_kopfstand,
       "formular": cmd_formular, "paare": cmd_paare, "rang": cmd_rang}

if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] not in BEF:
        print(__doc__)
        sys.exit(1)
    kr = sys.argv[2].rstrip("/")
    if not os.path.isdir(kr):
        kr = os.path.join(HIER, kr)
    try:
        BEF[sys.argv[1]](kr)
    except Abbruch as e:
        print("ABBRUCH -> OPUS:", e)
        sys.exit(2)
