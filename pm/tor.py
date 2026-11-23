#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-23), Entwurf. Auftrag pm/AUFTRAG_WORKFLOW_V.md Punkt 3, docs/17 Tor T2.
Prüft einen Rechenordner vor dem Start:
  1. ERWARTUNG.md vorhanden, alle Pflichtabschnitte (sim/VORLAGE_ERWARTUNG.md) vorhanden und nicht leer
     (leer = nur Platzhalter in <…>, nur Strich oder Text „offen“/„TODO“); „## Prüfung“ gilt erst nach der Rechnung und darf leer sein,
     die Überschrift muss aber da sein.
  2. Die unter „## Anforderung“ genannte REQ-ID steht in pm/anforderungen.json.
  3. eingaben.json existiert und ist gültiges JSON.
Rückgabe: rc 0 (Tor offen) oder 1 mit Liste der Fehler.   Aufruf: python3 pm/tor.py <ordner>"""
import json, re, sys
from pathlib import Path
R = Path(__file__).resolve().parents[1]
ABSCHNITTE = ["Anforderung", "Steckbrief", "Vorrechnung", "Erwartung", "Plausibilitätskriterien", "Abbruchkriterien (Wächter)", "Informationsgewinn der Varianten", "Zielband Bild", "Prüfung"]
NACH_RECHNUNG = {"Prüfung"}

def leer(t):
    t = re.sub(r"<[^>\n]*>", "", t).strip()
    return len(re.sub(r"[\s\-–—*_|:.]", "", t)) < 3 or t.lower() in ("offen", "todo", "tbd")

def pruefe(ordner):
    fehler = []; o = Path(ordner)
    if not o.is_absolute(): o = (Path.cwd() / o).resolve()
    e = o / "ERWARTUNG.md"
    if not o.is_dir(): return [f"Ordner fehlt: {ordner}"]
    if not e.exists(): fehler.append("ERWARTUNG.md fehlt"); text = ""
    else: text = e.read_text(encoding="utf-8")
    teile = {}
    for m in re.finditer(r"^## +(.+?)\s*\n(.*?)(?=^## |\Z)", text, re.S | re.M):
        teile.setdefault(m.group(1).strip(), m.group(2))
    if text:
        for a in ABSCHNITTE:
            if a not in teile: fehler.append(f"ERWARTUNG.md: Abschnitt „{a}“ fehlt")
            elif a not in NACH_RECHNUNG and leer(teile[a]): fehler.append(f"ERWARTUNG.md: Abschnitt „{a}“ ist leer")
        ids = re.findall(r"REQ-[PDG]\d+", teile.get("Anforderung", ""))
        if "Anforderung" in teile and not leer(teile["Anforderung"]):
            if not ids: fehler.append("Abschnitt „Anforderung“ nennt keine REQ-ID")
            else:
                try: bekannt = {r["id"] for r in json.loads((R / "pm/anforderungen.json").read_text())["anforderungen"]}
                except Exception as ex: bekannt = set(); fehler.append(f"pm/anforderungen.json nicht lesbar: {ex}")
                for i in ids:
                    if i not in bekannt: fehler.append(f"{i} steht nicht in pm/anforderungen.json")
    ei = o / "eingaben.json"
    if not ei.exists(): fehler.append("eingaben.json fehlt")
    else:
        try: json.loads(ei.read_text())
        except Exception as ex: fehler.append(f"eingaben.json kein gültiges JSON: {ex}")
    return fehler

if __name__ == "__main__":
    if len(sys.argv) != 2: sys.exit("Aufruf: python3 pm/tor.py <ordner>")
    f = pruefe(sys.argv[1])
    if f:
        print(f"TOR ZU ({len(f)} Fehler): {sys.argv[1]}"); [print(" -", x) for x in f]; sys.exit(1)
    print(f"TOR OFFEN: {sys.argv[1]}")
