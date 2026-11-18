"""plan_batterie.py -- Projektplan Batteriesystem als Netzplan (CPM) für den Planer des AI_Framework.

KI-generiert (Claude Opus, 2026-11-12). Dauern in Arbeitstagen sind ANNAHMEN (Schätzung Opus), keine Erfahrungswerte.
Grundlage: PLAN.md (Stufen 0-7, PM) und CLAUDE.md (Arbeitsteilung Opus/Sonnet/Haiku/PI/Maschine/Mensch).

    python3 pm/plan/plan_batterie.py
Ausgabe: pm/plan/plan_batterie.json (Planer-Format), pm/plan/plan_batterie.csv, pm/plan/kritischer_pfad.txt
Laden im AI_Framework: Datei nach ai_framework/data/plans/ kopieren, im Tab Planer über „— Plan laden —“ wählen.
"""
import csv, json, time
from pathlib import Path

HIER = Path(__file__).resolve().parent

# Ressourcen (kind: human | software | hardware). Sätze 0: Hobbyprojekt, Kosten werden nicht geplant.
RES = {"Mensch": "human", "Opus": "software", "Sonnet": "software", "Haiku": "software", "PI": "software",
       "Maschine": "hardware"}

# id, Name, Dauer [AT], Vorgänger, Ressourcen, Notiz (Stufe PLAN.md)
A = [
    ("S0", "Projektstart: Grundgerüst, Regeln, Software", 0, [], ["Opus"], "erledigt 2026-11-11"),
    # Stufe 1 Recherche
    ("R1", "Wissensaufbau W01-W15 (Chemie, Zelltypen, Spannung, Kabel, Steuerung, Struktur)", 2, ["S0"], ["PI", "Maschine"], "Stufe 1, läuft seit 2026-11-12"),
    ("R2", "Werkzeuge T01-T07 (Open Source Zellchemie, Elektroauslegung, Ersatzmodelle)", 1, ["R1"], ["PI", "Maschine"], "Stufe 1"),
    ("R3", "Patente P01-P10", 1, ["R2"], ["PI", "Maschine"], "Stufe 1"),
    ("R4", "Recherche prüfen: Zitate, Aussagen, Widersprüche -> BEFUNDE", 1, ["R3"], ["Opus", "Haiku"], "Regel 2 CLAUDE.md"),
    ("R5", "Werkzeugwahl festlegen (ENT): Zellmodell, Packmodell, Schaltung", 1, ["R4"], ["Opus", "Mensch"], "Entscheidungsakte"),
    ("W1", "Preprocessing mit Sketch-to-Prompt: Ein-/Auslass, Lager, Lasten, Kabelwege auf das STL zeichnen", 2, ["R5"], ["Opus", "Mensch"], "Werkzeug, Nutzerwunsch 2026-11-12"),
    ("W2", "Postprocessing: Schnittebenen aus Skizzenlinie + Blickrichtung, Feldwerte (Strömung, Spannung) je Schnitt", 2, ["W1"], ["Sonnet"], "Werkzeug, für K/X/M"),
    # Stufe 0 Vorgaben
    ("V1", "Lastenheft-Werte REQ-P01..P08 vorschlagen (Fahrzeug, kWh, Spannung, Leistung, Laden, Chemie, Bauraum, Temperatur)", 1, ["R4"], ["Opus"], "Stufe 0"),
    ("SL1", "Grobe Stückliste aus Startsatz (Baugruppen, Mengen mit Herleitung)", 0.5, ["V1"], ["Opus"], "erledigt 2026-11-12 (Vorschlags-Startsatz)"),
    ("V2", "Freigabe Lastenheft durch Autor", 2, ["V1"], ["Mensch"], "nur Mensch gibt frei"),
    # Stufe 2 Chemie und Zelle
    ("C1", "ERWARTUNG Zellmodell (Entladekurve, Wärme, Innenwiderstand)", 0.5, ["V2", "R5"], ["Opus"], "Stufe 2"),
    ("C2", "Zellmodell LFP (PyBaMM Prada2013) auf langes Format skalieren", 2, ["C1"], ["Sonnet", "Maschine"], "Stufe 2"),
    ("C3", "Ratentest 0,5C/1C/2C, Wärmeleistung, R_i über SOC und T", 1, ["C2"], ["Sonnet", "Maschine"], "Stufe 2"),
    ("C4", "Validierung gegen veröffentlichte Messkurven, Abgleich Erwartung", 1, ["C3"], ["Opus"], "Stufe 2"),
    ("C5", "Alterung (Zyklen, Kalender) und Vergleich NMC / Natrium-Ionen", 2, ["C4"], ["Sonnet", "Maschine"], "Stufe 2"),
    # Stufe 3 Geometrie und Zusammenbau
    ("G1", "Zellmaße als ENT-Akten (aus W03/W08/P01, sonst Annahme)", 0.5, ["V2", "R4"], ["Opus", "Mensch"], "Stufe 3, PM"),
    ("G2", "Parametrische Zelle FreeCAD (liest parameter.json)", 2, ["G1"], ["Sonnet"], "Stufe 3"),
    ("G3", "Verschaltung sS/pP aus Spannung und Energie festlegen (ENT)", 1, ["V2", "C3"], ["Opus", "Mensch"], "Stufe 4, bestimmt Zellzahl"),
    ("G4", "Pack: Zellanordnung, Querträger, Kühlplatte, Deckel", 3, ["G2", "G3"], ["Sonnet", "Maschine"], "Stufe 3"),
    ("G5", "Bauregeln + Prüfskript (Abstände, Isolation, Montagefolge)", 1, ["G4"], ["Opus", "Sonnet"], "Stufe 3"),
    ("K0", "Kühlart Luft gegen Wasser (1D-Wärmebilanz Schnellladen, W16), Entscheidung ENT", 1, ["C3", "G3", "R4"], ["Opus", "Sonnet", "Mensch"], "Nutzerwunsch 2026-11-12"),
    # Stufe 4 Elektrik
    ("E1", "Zellverbinder/Kabel: Querschnitt, Verluste, Erwärmung (Zielband als Annahme)", 2, ["G3", "G4"], ["Sonnet", "Maschine"], "Stufe 4"),
    ("E2", "Schutzkonzept: Sicherung, Schütze, Vorladung, Isolationswächter", 2, ["G3"], ["Opus", "Sonnet"], "Stufe 4"),
    ("L1", "Kabelverlegung: Weg skizzieren (Sketch-to-Prompt), Prüfskript Biegeradius/Abstand HV-NV/Kühlleitung, FreeCAD-Sweep", 3, ["E2", "G4", "W1"], ["Opus", "Sonnet"], "Nutzerwunsch 2026-11-12, Vorbild spulen_montage.py"),
    ("E3", "Steuerung/BMS: Messkonzept, Ladezustand, Ausgleich (Konzept, offene Software aus T06)", 2, ["E2", "C4"], ["Opus", "Sonnet"], "Stufe 4"),
    ("E4", "Schaltungsmodell ngspice/Modelica: Vorladung, Kurzschluss", 2, ["E2", "R5"], ["Sonnet", "Maschine"], "Stufe 4"),
    # Stufe 5 Kühlung
    ("K1", "ERWARTUNG Kühlung Schnellladen (max. Zelltemperatur, Spreizung)", 0.5, ["C3", "G4", "K0", "W2"], ["Opus"], "Stufe 5"),
    ("K2", "Kanalverteilung 1D (Verteiler, Druckverlust)", 1, ["K1"], ["Sonnet", "Maschine"], "Stufe 5"),
    ("K3", "Elmer: Zelle -> Paste -> Platte, Schnellladefall", 3, ["K2"], ["Sonnet", "Maschine"], "Stufe 5"),
    ("K4", "FluidX3D: Strömung Kühlplatte bzw. Luftkanal (Gegenprüfung 1D)", 2, ["K2"], ["Maschine"], "Stufe 5, GPU nicht zugleich mit PI"),
    ("K5", "Deutung Kühlung, Abgleich Erwartung, Änderungsvorschlag", 1, ["K3", "K4"], ["Opus"], "Stufe 5"),
    # Ersatzmodell (Surrogat)
    ("U1", "ERWARTUNG Ersatzmodell: Zielgröße, Gültigkeitsbereich, Mindestgüte (z. B. Rangkorrelation)", 0.5, ["K5", "R2"], ["Opus"], "Lehre Fusion: Proxy 0,59 reichte nicht"),
    ("U2", "Versuchsplan (Latin Hypercube): Durchfluss, Eintritt, C-Rate, Plattenmaß -> Elmer-Läufe", 3, ["U1"], ["Sonnet", "Maschine"], "losgelöst, pausierbar"),
    ("U3", "Ersatzmodell anpassen (Gauß-Prozess), Kreuzvalidierung gegen zurückgehaltene Läufe", 1, ["U2"], ["Sonnet"], ""),
    ("U4", "Optimierung Kühlplatte/Ladeprofil mit Ersatzmodell, Bestwerte mit Elmer bestätigen", 2, ["U3"], ["Opus", "Maschine"], "Ersatzmodell nur sortiert, Elmer entscheidet"),
    # Stufe 6 Mechanik
    ("M1", "Mechanik: Zellverspannung, Eigenfrequenzen, Lagerung", 3, ["G5"], ["Sonnet", "Maschine"], "Stufe 6, optional"),
    ("X1", "Seitencrash Pfahl, quasistatisch: Eindringung in Gehäuse/Querträger (CalculiX, plastisch, Kontakt)", 3, ["G5", "W2", "R4"], ["Sonnet", "Maschine"], "Nutzerwunsch 2026-11-12"),
    ("X2", "Seitencrash dynamisch (OpenRadioss, Installation nur nach Freigabe)", 4, ["X1"], ["Opus", "Maschine", "Mensch"], "optional"),
    # Querschnitt
    ("SL2", "Stückliste fortschreiben nach Auslegung (Mengen, Kauf/Eigen, Werkstoffe, Bezugsquellen)", 1, ["SL1", "G5", "E2", "E3", "K5", "L1", "X1"], ["Sonnet", "Opus"], "lebendes Dokument BAT-DOC-13"),
    ("F1", "FMEA und Verifikationsplan nachziehen", 1, ["E1", "E3", "K5", "M1", "L1", "X2"], ["Opus", "Haiku"], "BAT-DOC-05/06"),
    ("B1", "Bericht DE/EN je Kapitel, Prozessdoku, Lessons Learned", 4, ["C5", "E4", "U4", "F1", "SL2"], ["Sonnet", "Opus"], "Stufe 7"),
    ("B2", "Bauteilgespräch testen (pm/gespraech.sh für alle BT)", 1, ["B1"], ["PI", "Opus"], "Stufe 7"),
    ("B3", "Abschlussvideo (Storyboard -> Blender -> ffmpeg)", 3, ["B1", "G5"], ["Sonnet", "Maschine"], "Stufe 7"),
    ("B0", "Präsentation: Zielgruppe, Ziel, Firmenvorlage, Sprache festlegen", 0.5, ["V1"], ["Mensch"], "BAT-DOC-14, nur Mensch"),
    ("B5", "Unternehmenspräsentation aus Folienbausteinen erzeugen (pptx + PDF, DE/EN), Zahlen gegen Quellen prüfen", 2, ["B0", "B1", "SL2", "F1", "R3"], ["Sonnet", "Opus"], "Stufe 7, REQ-D14"),
    ("B4", "Freigabe und Veröffentlichung durch Autor", 1, ["B2", "B3", "B5"], ["Mensch"], "nur Mensch"),
]


def cpm(a):
    d = {t[0]: t for t in a}; es, ef = {}, {}
    for i, n, dur, vor, *_ in a:                       # Liste ist topologisch sortiert
        es[i] = max((ef[v] for v in vor), default=0); ef[i] = es[i] + dur
    ende = max(ef.values()); nach = {i: [t[0] for t in a if i in t[3]] for i in d}
    lf, ls = {}, {}
    for i, n, dur, *_ in reversed(a):
        lf[i] = min((ls[s] for s in nach[i]), default=ende); ls[i] = lf[i] - dur
    return es, ef, ls, lf, nach, ende


def main():
    ids = [t[0] for t in A]
    for t in A:
        assert all(v in ids[:ids.index(t[0])] for v in t[3]), f"Vorgänger fehlt/Reihenfolge: {t[0]}"
    es, ef, ls, lf, nach, ende = cpm(A)
    tasks = [{"id": i, "name": n, "duration": dur, "predecessors": vor, "successors": nach[i],
              "resources": ", ".join(r), "resource_list": [{"kind": RES[x], "name": x, "qty": 1, "rate": 0} for x in r],
              "notes": notiz, "is_start": not vor, "is_end": not nach[i]} for i, n, dur, vor, r, notiz in A]
    plan = {"id": "batterie0001", "name": "Batteriesystem (KI-generiert)", "created_at": time.time(), "updated_at": time.time(),
            "tasks": tasks, "description": "KI-generiert (Claude Opus, 2026-11-12). Batteriesystem für ein E-Fahrzeug: Recherche, "
            "Zellchemie (PyBaMM), Zelle und Pack (FreeCAD), Elektrik, Kühlung (Elmer/FluidX3D), Ersatzmodell, Bericht, Video. "
            "Dauern in Arbeitstagen sind Annahmen. Quelle: hermes/batterie/PLAN.md.",
            "system_prompt": "", "resource_catalog": [{"kind": k, "name": n, "rate": 0} for n, k in RES.items()],
            "resource_mode": "catalog", "start_date": "2026-11-12", "workdays": True, "project_id": ""}
    (HIER / "plan_batterie.json").write_text(json.dumps(plan, ensure_ascii=False, indent=2))
    with open(HIER / "plan_batterie.csv", "w", newline="") as f:
        w = csv.writer(f, delimiter=";"); w.writerow(["ID", "Name", "Dauer_AT", "Vorgaenger", "Ressourcen", "ES", "EF", "Puffer", "Notiz"])
        for i, n, dur, vor, r, notiz in A:
            w.writerow([i, n, dur, ",".join(vor), ",".join(r), es[i], ef[i], round(lf[i] - ef[i], 2), notiz])
    krit = [i for i in ids if abs(lf[i] - ef[i]) < 1e-9]
    last = {}
    for i, n, dur, vor, r, _ in A:
        for x in r: last[x] = last.get(x, 0) + dur
    txt = (f"KI-generiert. Projektdauer {ende:g} Arbeitstage (Annahme), Start 2026-11-12.\n"
           f"Kritischer Pfad: {' -> '.join(krit)}\n"
           f"Belegung (Summe Vorgangsdauern je Ressource, parallel möglich): {last}\n")
    (HIER / "kritischer_pfad.txt").write_text(txt); print(txt)


if __name__ == "__main__":
    main()
