# KI-generiert (Claude Sonnet 5.5, 2026-11-25), Entwurf. Auftrag Opus (Vorgabe Autor: „mir geht es in erster Linie um den agentischen Ablauf“).
# Erzeugt video/elektronik/agenten.json aus docs/08_ki_einsatz_protokoll.md: je Szenenabschnitt die Zeilennummern des Protokolls, daraus die aktiven Agenten (Regel unten) und die Zählung der Verteilungen je Agent.
# Regel (nichts erfinden): Agent aktiv, wenn er in Spalte 2 (Agent/Modell) der zitierten Zeile steht; Opus zusätzlich, wenn Spalte 5 (Geprüft von) mit „Opus“ beginnt oder Spalte 3 „Auftrag Opus“ bzw. „ERW-“ (Erwartung) nennt; „Prüfung Opus offen“ zählt nicht; Kolibri zusätzlich, wenn Spalte 3 „Kolibri“ nennt (Storyboard); Autor, wenn Spalte 3 „Freigaberunde“ oder „Status Autor“ nennt.
# Fehlt die Zeile, bleibt die Marke aus. PI/qwen = PI-Zeilen ohne Kolibri.
import re, json
R = "/home/cae/hermes/batterie"; L = open(f"{R}/docs/08_ki_einsatz_protokoll.md", encoding="utf-8").read().split("\n")
def spalten(n): return [c.strip() for c in L[n - 1].strip().strip("|").split("|")]
def erkenne(n):
    c = spalten(n); a2, a3, a5 = c[1], c[2], c[4] if len(c) > 4 else ""; s = set()
    if "Opus" in a2 or a5.startswith("Opus") or "Auftrag Opus" in a3 or "ERW-" in a3: s.add("Opus")   # Auftrag/Erwartung von Opus (AGENTS.md: ERWARTUNG von Opus)
    if "Sonnet" in a2: s.add("Sonnet")
    if "Haiku" in a2: s.add("Haiku")
    if "Kolibri" in a2 or "Kolibri" in a3: s.add("Kolibri")
    if re.search(r"\bPI\b", a2) and "Kolibri" not in a2: s.add("PI/qwen")
    if "Freigaberunde" in a3 or "Status Autor" in a3: s.add("Autor")
    return s
SEG = [  # (von s, bis s, Szene, Zeilen, Kurzangabe aus den Zeilen)
 (0, 25, "Anforderungen und Normen", [144, 151, 145, 153, 92, 169, 193], "Opus: Kriterien · Sonnet: anforderungen.json, Regelwerke · PI: W30 · Autor: Freigaberunde · Kolibri: Tafeltexte"),
 (25, 50, "Zelle", [76, 193], "Sonnet: C1 PyBaMM-Zellmodell · Opus: Prüfung gegen W20/W24 · Kolibri: Storyboard"),
 (50, 62, "Pack", [69, 70, 71, 135, 193], "Sonnet: G4 Pack-CAD, G5.9 · Opus: Prüfung Schnitt, Masse · Kolibri: Storyboard"),
 (62, 70, "Kühlung", [118, 119, 120, 121, 123, 193], "Sonnet: K3/K4 FluidX3D, Film · Opus: Prüfung K4 · Kolibri: Storyboard"),
 (70, 80, "Crash", [91, 117, 122, 123, 193], "Sonnet: X3 Crash (CalculiX/Radioss) · Opus: Fehlersuche LFP_a · Kolibri: Storyboard"),
 (80, 95, "CMU-Platine", [176, 183, 184, 189, 195, 193], "Opus: Auftrag, Erwartung · Sonnet: KiCad-Routing · Kolibri: Wächter, Storyboard · Prüfung offen"),
 (95, 110, "BMS-Platine", [186, 188, 191, 193], "Opus: Erwartung ERW-E3c · Sonnet: BMS-Platine, SPICE · Kolibri: Storyboard · Prüfung offen"),
 (110, 125, "Rechnungen", [176, 191, 182, 185, 193], "Opus: Erwartung · Sonnet: SPICE, Elmer, FMEDA · Kolibri: Storyboard · Prüfung offen"),
 (125, 140, "Nachverfolgung", [157, 158, 159, 21, 193], "Sonnet: Wissensgraph · Opus: Prüfung, Schema · Kolibri: Storyboard"),
 (140, 165, "Batterie fertig, Graph", [157, 159, 173, 174, 196, 193], "Sonnet: Graph, Video · Opus: Prüfung Video 2 · Kolibri: Storyboard"),
]
out = []
for a, b, name, zl, kurz in SEG:
    ag = set()
    for n in zl: ag |= erkenne(n)
    for m in re.findall(r"(Opus|Sonnet|Haiku|PI|Kolibri|Autor)\b", kurz):   # jede in der Kurzangabe genannte Marke muss durch eine Zeile gedeckt sein
        mm = {"PI": "PI/qwen"}.get(m, m)
        assert mm in ag, f"{name}: {mm} nicht durch Zeilen {zl} gedeckt"
    out.append(dict(von=a, bis=b, szene=name, zeilen=zl, agenten=sorted(ag), kurz=kurz, zeilen_agenten={str(n): sorted(erkenne(n)) for n in zl}))
# Zählung der Verteilungen je Agent (Zeilen ab Tabellenbeginn, Spalte 2)
z = {k: 0 for k in ("Opus", "Sonnet", "Haiku", "PI/qwen", "Kolibri")}; n_zeilen = 0
for i, l in enumerate(L, 1):
    if not re.match(r"\| 20\d\d-", l): continue
    n_zeilen += 1; a2 = spalten(i)[1]
    if "Opus" in a2: z["Opus"] += 1
    if "Sonnet" in a2: z["Sonnet"] += 1
    if "Haiku" in a2: z["Haiku"] += 1
    if "Kolibri" in a2: z["Kolibri"] += 1
    if re.search(r"\bPI\b", a2) and "Kolibri" not in a2: z["PI/qwen"] += 1
json.dump(dict(quelle="docs/08_ki_einsatz_protokoll.md", regel=__doc__ if False else "Agent in Spalte 2; Opus auch Spalte 5 Beginn Opus; Kolibri auch Spalte 3; Autor Spalte 3 Freigaberunde; Zählung: Zeilen mit Datum, Agent in Spalte 2 (eine Zeile zählt für jeden genannten Agenten)", zeilen_gesamt=n_zeilen, zaehlung=z, abschnitte=out),
          open(f"{R}/video/elektronik/agenten.json", "w"), ensure_ascii=False, indent=1)
for o in out: print(o["von"], o["szene"], o["agenten"])
print(n_zeilen, z)
