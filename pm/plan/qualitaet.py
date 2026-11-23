#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-23), Entwurf. Erzeugt Abschnitt 4 von docs/22_qualitaetsnachweis.md.
Tabelle Q1-Q10 x Kategorien W,L,V,E,U,R,D (Stufe 0-4). Nur aus Dateien abgeleitet; sonst "? (Opus)", nichts geschätzt.
Regeln (Auftrag Opus 2026-11-23):
 W  sim/verifikation_werkzeuge/ergebnis.json faelle.V1..V5 (siehe kat_W), Q7-Q10 '-'
 L  ERGEBNIS.md der Rechnung: "Bilanz|Energiefehler" -> 1, sonst 0; Netz-/Zeitschrittstudie erwähnt -> ? (Opus); ohne ERGEBNIS.md -> ? (Opus)
 V  sim/vergleich_produkte/ergebnis.json (kategorie_V.Qn) für Q7, Q8, sonst 0
 E  graph herkunft <ID> --json: Wurzeln vorhanden (aufgelöst) -> mindestens 1; Quellen vorhanden -> ? (Opus) (2 nur mit Zitat der Haupteingaben); keine Wurzel -> ? (Opus)
 Opus-Stufen: pm/plan/qualitaet_opus.json ersetzt ? (Opus), in der Tabelle mit (Opus) gekennzeichnet
 U  ERGEBNIS.md erwähnt Empfindlichkeit/Unsicherheit -> ? (Opus), sonst 0
 R  ERGEBNIS.md erwähnt Gegenprüfung/zweite Methode -> ? (Opus), erwähnt Varianten -> 1, sonst 0; ohne ERGEBNIS.md -> ? (Opus)
 D  docs/08 Zeilen zum Stichwort: Opus-Prüfung mit "ok" -> 1; zusätzlich PI/lokales Modell -> 2; keine -> 0 (Mensch nicht ableitbar)
Gesamtstufe = Minimum der bekannten Stufen; "*" = offene Kategorien können sie nur senken.
Aufruf: python3 pm/plan/qualitaet.py   (aus Projektwurzel)"""
import json, re, subprocess, sys
from pathlib import Path
R = Path(__file__).resolve().parents[2]
DOC = R / "docs/22_qualitaetsnachweis.md"
KAT = "WLVEURD"
Q = {  # Nr: (Ergebnis, Rechnungsordner/ERGEBNIS-Quelle, Graph-IDs, Werkzeug, docs/08-Stichworte)
 "Q1-LFP": ("T_max und Spreizung Schnellladen, LFP (V4p)", "sim/kuehlung/k3_gesamt", ["REQ-P09", "sim/kuehlung/k3_gesamt"], "Elmer", ["k3_gesamt", "K3", "K4"]),
 "Q1-NMC": ("T_max und Spreizung Schnellladen, NMC (V4p)", "sim/kuehlung/k3_gesamt", ["REQ-P09", "sim/kuehlung/k3_gesamt"], "Elmer", ["k3_gesamt", "K3", "K4"]),
 "Q2": ("Δp Kühlplatte (K5)", "sim/kuehlung/k5_parallel", ["REQ-P12", "sim/kuehlung/k5_parallel"], "Verteiler-1D", ["k5_parallel", "K5"]),
 "Q3": ("Zellverschiebung Pfahlcrash", "sim/mechanik/x3_crash_g5", ["REQ-P14", "sim/mechanik/x3_crash_g5"], "OpenRadioss", ["x3_crash", "X3"]),
 "Q4": ("Quetschung 100 kN", "sim/mechanik/x3_crash_g5", ["REQ-P14", "sim/mechanik/x3_crash_g5"], "OpenRadioss", ["x3_crash", "X3"]),
 "Q5": ("Verluste Verbinder (E1 G5)", "sim/elektrik/e1_querschnitte", ["REQ-P13", "REQ-P15", "sim/elektrik/e1_querschnitte"], "Python-Netz E1", ["e1_querschnitte", "E1"]),
 "Q6": ("Ladezeit NMC 10→80 %", "sim/chemie/varianten_lfp_nmc", ["REQ-P05", "sim/chemie/varianten_lfp_nmc"], "PyBaMM-NMC", ["varianten_lfp_nmc", "PyBaMM", "C2"]),
 "Q7": ("Packmasse", None, ["REQ-P07"], "-", ["Stückliste", "SL2"]),
 "Q8": ("Energieinhalt", None, ["REQ-P02"], "-", ["Stückliste", "SL2"]),
 "Q9": ("Herstellkosten", "pm/kosten", ["REQ-P16"], "-", ["pm/kosten", "KO1", "KO2"]),
 "Q10": ("Hüllmaß Pack", None, ["REQ-P07"], "-", ["G5.9", "G5"]),
}
UNK = "? (Opus)"
def lies(p):
    f = R / p
    return f.read_text(errors="ignore") if f.is_file() else None
def js(p):
    t = lies(p)
    try: return json.loads(t) if t else None
    except Exception: return None
def herkunft(ids):
    w = {}
    for i in ids:
        try:
            o = subprocess.run([sys.executable, str(R / "pm/graph/frage.py"), "herkunft", i, "--json"], capture_output=True, text=True, cwd=R, timeout=60).stdout
            for x in json.loads(o).get("wurzeln", []): w[x["id"]] = x["typ"]
        except Exception: pass
    return w
def kat_W(werk, wj):
    """QN1-Format: ergebnis.json faelle.V1..V5 {bestanden, ordnung_beobachtet}. Regel Opus 2026-11-23:
    bestanden + Ordnung bestätigt = 3; bestanden ohne Ordnung = 2; verfehlt = 0; kein Testfall = 1; nicht anwendbar = '-' (zählt nicht)."""
    if werk == "-": return "-", "kein Simulationswerkzeug (Stückliste/CAD), W nicht anwendbar"
    if werk == "Python-Netz E1": return 1, "kein Testfall für das E1-Netz (Regel Opus), Stufe 1"
    if wj is None: return 1, "sim/verifikation_werkzeuge/ergebnis.json fehlt: Vorgabe 1"
    fall = {"Elmer": "V1", "FluidX3D": "V2", "OpenRadioss": "V3", "Verteiler-1D": "V5"}.get(werk)
    f = wj.get("faelle", {})
    if werk.startswith("PyBaMM"):
        ch = werk.split("-")[1]; v4 = js("sim/verifikation_werkzeuge/ergebnis_V4.json")
        if not v4: return UNK, "ergebnis_V4.json fehlt"
        sa = v4["saetze"][ch]; ok = sa["bestanden_ladung"] and sa["bestanden_spm_dfn"]
        return (2 if ok else 0), f"sim/verifikation_werkzeuge/ergebnis_V4.json::saetze.{ch} (Ladung {sa['abw_ladung_projektmodell_SPMe_pct']:+.2f} %, bestanden={ok}, keine Ordnung)" + ("" if ok else "; B-BAT-049")
    if fall not in f: return UNK, f"{werk} nicht in sim/verifikation_werkzeuge/ergebnis.json"
    c = f[fall]
    if not c["bestanden"]: return 0, f"ergebnis.json::faelle.{fall} verfehlt"
    return (3 if c.get("ordnung_beobachtet") else 2), f"ergebnis.json::faelle.{fall} bestanden, Ordnung {'bestätigt' if c.get('ordnung_beobachtet') else 'nicht bestimmt'}"
def kat_E(ids):
    w = herkunft(ids); a = sum(t == "Annahme" for t in w.values()); q = sum(t in ("Quelle", "Norm") for t in w.values())
    if a + q == 0: return UNK, f"graph herkunft {'+'.join(ids)}: keine Annahme/Quelle als Wurzel"
    anteil = a / (a + q); s = f"graph herkunft {'+'.join(ids)}: {a} Annahmen, {q} Quellen/Normen ({anteil:.0%} Annahmen), alle bis zur Wurzel aufgelöst (docs/22 §1: Stufe 1 = Annahmen benannt)"
    return (UNK if q else 1), s + (", Zitatprüfung der Quellen nicht automatisch bewertet" if q else "")
def kat_D(keys, t8):
    z = [l for l in t8.splitlines() if l.startswith("|") and any(k.lower() in l.lower() for k in keys)]
    opus = [l for l in z if re.search(r"\bOpus\b", l) and re.search(r"\|\s*ok\b", l.lower())]
    pi = [l for l in opus if re.search(r"\bPI\b|lokales Modell|Zweitmeinung", l)]
    s = f"docs/08: {len(z)} Zeilen zu {keys[0]}, davon {len(opus)} Opus-Prüfung ok, {len(pi)} mit PI"
    return (2 if pi else 1 if opus else 0), s
def main():
    wj = js("sim/verifikation_werkzeuge/ergebnis.json"); vj = js("sim/vergleich_produkte/ergebnis.json")
    t8 = lies("docs/08_ki_einsatz_protokoll.md") or ""
    zeilen, begr = [], []
    for nr, (titel, ordner, ids, werk, keys) in Q.items():
        erg = lies(ordner + "/ERGEBNIS.md") if ordner else None
        r = {}; b = {}
        r["W"], b["W"] = kat_W(werk, wj)
        if erg is None: r["L"], b["L"] = UNK, "keine ERGEBNIS.md der Rechnung"
        elif re.search(r"Netzstudie|Zeitschrittstudie|GCI", erg): r["L"], b["L"] = UNK, f"{ordner}/ERGEBNIS.md erwähnt Netz-/Zeitschrittstudie"
        elif re.search(r"Bilanz|Energiefehler", erg): r["L"], b["L"] = 1, f"{ordner}/ERGEBNIS.md erwähnt Bilanz/Energiefehler"
        else: r["L"], b["L"] = 0, f"{ordner}/ERGEBNIS.md ohne Bilanz"
        vs = (vj or {}).get("kategorie_V", {}).get(nr)
        r["V"], b["V"] = (vs, f"sim/vergleich_produkte/ergebnis.json::kategorie_V.{nr}") if vs is not None else (0, "kein Vergleich" if nr in ("Q7", "Q8") and vj is None else "kein Vergleich mit Produkten oder Versuch")
        if nr in ("Q7", "Q8") and vj is None: b["V"] = "sim/vergleich_produkte/ergebnis.json fehlt (Platzhalter 0)"
        if nr.startswith("Q1"): b["W"] += "; Wärmequelle V4p aus K1 (I²R, R aus K0-Eingaben, Annahme), nicht aus PyBaMM: k3_gesamt/k4_elmer.py Z.82 liest sim/kuehlung/k1_schnellladen/ergebnis.json; nur der Fall LFP_P0_K3_R128 nutzt C2-Widerstand 1,28 mΩ"
        r["E"], b["E"] = kat_E(ids)
        if erg is None: r["U"], b["U"] = UNK, "keine ERGEBNIS.md"
        elif re.search(r"Empfindlichkeit|Unsicherheit|Sensitiv", erg): r["U"], b["U"] = UNK, f"{ordner}/ERGEBNIS.md erwähnt Empfindlichkeit/Unsicherheit"
        else: r["U"], b["U"] = 0, f"{ordner}/ERGEBNIS.md ohne Unsicherheitsangabe"
        if erg is None: r["R"], b["R"] = UNK, "keine ERGEBNIS.md"
        elif re.search(r"Gegenprüfung|zweite Methode|CalculiX", erg): r["R"], b["R"] = UNK, f"{ordner}/ERGEBNIS.md erwähnt Gegenprüfung"
        elif re.search(r"Variante|V[0-4]p?\b", erg): r["R"], b["R"] = 1, f"{ordner}/ERGEBNIS.md nennt Varianten"
        else: r["R"], b["R"] = 0, f"{ordner}/ERGEBNIS.md Einzelfall"
        r["D"], b["D"] = kat_D(keys, t8)
        op = (js("pm/plan/qualitaet_opus.json") or {}).get(nr, {})
        for k, (st, gr) in op.items():
            if r.get(k) != "-": r[k], b[k] = f"{st} (Opus)", f"(Opus, ersetzt Skriptwert {r.get(k)}) {gr}"
        bek = [int(str(v).split()[0]) for v in r.values() if str(v).split()[0].isdigit()]; offen = any(not str(v).split()[0].isdigit() and v != "-" for v in r.values())
        ges = f"{min(bek)}{'*' if offen else ''}" if bek else UNK
        zeilen.append(f"| {nr} {titel} | " + " | ".join(str(r[k]) for k in KAT) + f" | **{ges}** | " + (",".join(k for k in KAT if str(r[k]).split()[0].isdigit() and bek and int(str(r[k]).split()[0]) == min(bek)) or "-") + " |")
        begr.append(f"- **{nr}**: " + "; ".join(f"{k}={r[k]}: {b[k]}" for k in KAT))
    kopf = ["| Ergebnis | W | L | V | E | U | R | D | Gesamt (Min.) | begrenzt durch |", "|---|---|---|---|---|---|---|---|---|---|"]
    txt = ("## 4 Bewertung\n\nErzeugt von `pm/plan/qualitaet.py` (Sonnet) am " + subprocess.run(["date", "+%F %H:%M"], capture_output=True, text=True).stdout.strip() +
           ". Regeln siehe Kopf des Skripts. Stufe 0–4 nach Abschnitt 1, Gesamt = Minimum der bekannten Stufen, `*` = es gibt offene Kategorien (\"? (Opus)\"), die den Wert nur senken können. "
           "W nach Regel Opus (3 bestanden mit Ordnung, 2 ohne Ordnung, 0 verfehlt, 1 kein Testfall, - nicht anwendbar) aus `sim/verifikation_werkzeuge/ergebnis.json` " + ("(vorhanden)" if wj else "(fehlt noch: Platzhalter 1)") + ", V aus `sim/vergleich_produkte/ergebnis.json` " + ("(vorhanden)" if vj else "(fehlt noch: Platzhalter 0)") + ".\n\n"
           + "\n".join(kopf + zeilen) + "\n\n### Begründung mit Quellpfad\n" + "\n".join(begr) + "\n\n")
    d = DOC.read_text()
    i = d.index("## 4 Bewertung"); j = d.index("\n---\n", i) + 1
    DOC.write_text(d[:i] + txt + d[j:])
    print("docs/22 Abschnitt 4 geschrieben")
main()
