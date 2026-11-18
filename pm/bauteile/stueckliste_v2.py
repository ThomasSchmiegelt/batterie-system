"""stueckliste_v2.py -- Stückliste auf Konstruktionsstand je Variante (Auftrag SL2, AUFTRAG_STUECKLISTE_V2.md).

KI-generiert (Claude Sonnet, 2026-11-18), Entwurf.
    python3 pm/bauteile/stueckliste_v2.py --variante LFP|NMC     (stueckliste.py --variante V ruft dieses Skript)
Eingaben: struktur.json, parameter_<V>.json, cad/pack/entwurf/ergebnis_<V>_e2.json (Mengen, Massen, E2-Annahmen),
          cad/pack/entwurf/ergebnis_<V>.json und ergebnis.json (Vergleich pack_massen.py), sim/elektrik/e1_querschnitte/ergebnis.json (Vergleich).
Ausgabe:  pm/bauteile/stueckliste_<V>.json, docs/13_stueckliste_<V>.md, docs/bilder/stueckliste_massen_<V>.png
Keine Preise, keine neuen Annahmen: Position ohne CAD-Menge bekommt "offen". Kostenspalten bleiben leer.
"""
import json, sys
from pathlib import Path
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
V = sys.argv[sys.argv.index("--variante") + 1]
D = ROOT / "cad/pack/entwurf"
E2P = f"cad/pack/entwurf/ergebnis_{V}_e2d.json"   # Detailstand e2d (2026-11-18, Auftrag BERICHT_03 Vorher); Rückfall e2
if not (ROOT / E2P).exists(): E2P = f"cad/pack/entwurf/ergebnis_{V}_e2.json"
E2 = json.loads((ROOT / E2P).read_text()); G = E2["gruppen"]; A = E2["annahmen"]
P = json.loads((ROOT / f"pm/bauteile/parameter_{V}.json").read_text())["parameter"]
BT = {x["id"]: x for x in json.loads((ROOT / "pm/bauteile/struktur.json").read_text())["bauteile"]}
V1 = json.loads((D / f"ergebnis_{V}.json").read_text())
PM = json.loads((D / "ergebnis.json").read_text())
E1 = json.loads((ROOT / "sim/elektrik/e1_querschnitte/ergebnis.json").read_text())["arten"]
am = lambda k: A[k]["wert"]

# (Pos, BT, Benennung, art, werkstoff, CAD-Gruppe | None, Menge-Überschreibung, Masse-gesamt-Überschreibung, Quelle-Zusatz)
CADQ = E2P
Z = []   # Zeilen
def add(pos, bt, ben, art, wst, gruppe=None, menge=None, masse=None, quelle=None, bem=""):
    Z.append(dict(pos=pos, bt=bt, benennung=ben, art=art, werkstoff=wst, gruppe=gruppe, menge=menge, masse=masse, quelle=quelle, bemerkung=bem))
g = lambda n: G.get(n)
add("100.1", "BT-100", f"Zelle ({P['BT-100']['format']['wert'].strip(chr(34))}, {V})", "K", "Zelle (Masse aus Akte, Hüllkörper)", "Zellen")
add("200.3", "BT-230", "Wärmeleitmaterial / Pad Zelle-Kühlplatte", "K", "Pad", "Pad")
if V == "NMC":
    add("200.5", "BT-250", "Zellhalter / Zellträger", "K", "offen (Werkstoff/Dichte fehlt)", "Zelltraeger")
add("500.1", "BT-510", "Gehäusewanne (im CAD: Boden)", "E", "Al", "Boden")
add("500.2", "BT-520", "Deckel (Dichtung nicht im CAD)", "E", "Al", "Deckel")
add("500.3", "BT-530", "Querträger", "E", "Al", "Quertraeger")
add("500.4", "BT-540", "Seitenrahmen / Crashprofil", "E", "Al (Vollprofil, Obergrenze)", "Seitenrahmen")
add("500.5", "BT-550", "Unterfahrschutz", "E", "Al", "Unterfahrschutz")
add("600.1", "BT-610", "Kühlplatte", "E", "Al (Vollmaterial, Obergrenze)", "Kuehlplatte")
if V == "LFP":
    add("400.2", "BT-420", "Zellverbinder = Reihenverbinder (p = 1)", "E", "Al", "Zellverbinder")
else:
    add("400.1", "BT-410", "Zellabgriff", "E", "Al", "Zellabgriff")
    add("400.2", "BT-420", "Gruppenverbinder (je 4 Zellen)", "E", "Al (Annahme, Cu offen)", "Gruppenverbinder")
    add("400.2b", "BT-420", "Gruppenbrücke (Reihenbrücke)", "E", "Al (Annahme, Cu offen)", "Gruppenbruecke")
add("400.3", "BT-430", "HV-Leitung im Pack", "K", "Cu (Leiter, Isolierung ohne Wert)", "E2_HV_Leitung")
add("300.2", "BT-320", "Zellüberwachung CMU (Platine)", "K", "E2 Teil (Masse ERW-E2 N1)", "E2_CMU", bem="Zuordnung nach Name BT-320, Opus bestätigen")
add("300.6", "BT-360", "Flexleiterplatte FPC Zelle -> CMU", "K", "FPC (Masse ERW-E2 N1)", "E2_FPC", bem="Zuordnung nach Name (300.6 nennt Flexleiterplatte), Opus bestätigen")
add("700.1", "BT-710", "Schaltbox (Gehäuse)", "E", "Al", "E2_Schaltbox")
if "E2_Schaltbox_Deckel" in G: add("700.1b", "BT-710", "Schaltbox-Deckel (e2d)", "E", "Al", "E2_Schaltbox_Deckel")
# Schaltbox-Inhalt und Stecker aus E2-Annahmen (Einzelmassen), Summe wird gegen die CAD-Gruppe geprüft
INH = [("300.1", "BT-310", "BMS-Platine", 1, am("A_e2_bms_masse_kg"), "K"),
       ("300.4", "BT-340", "Shunt (Strommessung)", 1, am("A_e2_shunt_masse_kg"), "K"),
       ("700.2", "BT-711", "Hauptschütz", 2, 2 * am("A_e2_schuetz_masse_kg"), "K"),
       ("700.3", "BT-712", "Vorladeschütz und Vorladewiderstand (Widerstandsmasse 0 gesetzt)", 2, am("A_e2_vorlade_masse_kg"), "K"),
       ("700.4", "BT-713", "Pyrosicherung und Schmelzsicherung", 2, am("A_e2_pyro_masse_kg") + am("A_e2_schmelz_masse_kg"), "K")]
STE = [("700.6", "BT-730", "HV-Steckverbinder 250 A und 40 A", 2, am("A_e2_hv250_masse_kg") + am("A_e2_hv40_masse_kg"), "K"),
       ("700.7", "BT-740", "NV-Steckverbinder 26-polig", 1, am("A_e2_nv_masse_kg"), "K"),
       ("700.10", "BT-770", "Gas- und Drucksensor", 1, am("A_e2_gas_masse_kg"), "K")]
if V == "NMC": STE.append(("700.5", "BT-720", "Service-Trennstecker", 1, am("A_e2_trennstecker_masse_kg"), "K"))
for pos, bt, ben, n, m, art in INH:
    add(pos, bt, ben, art, "E2 Teil (Masse ERW-E2 N1)", None, n, m, f"{E2P} annahmen A_e2_*; Summe geprüft gegen Gruppe E2_Schaltbox_Inhalt")
for pos, bt, ben, n, m, art in STE:
    add(pos, bt, ben, art, "E2 Teil (Masse ERW-E2 N1)", None, n, m, f"{E2P} annahmen A_e2_*; Summe geprüft gegen Gruppe E2_Stecker_Sensor")

# Prüfung: Einzelmassen gegen Gruppenmassen
chk_inh = sum(r["masse"] for r in Z if r["quelle"] and "Inhalt" in r["quelle"]); chk_ste = sum(r["masse"] for r in Z if r["quelle"] and "Stecker_Sensor" in r["quelle"])
assert abs(chk_inh - G["E2_Schaltbox_Inhalt"]["masse_kg"]) < 1e-6, (chk_inh, G["E2_Schaltbox_Inhalt"]); assert abs(chk_ste - G["E2_Stecker_Sensor"]["masse_kg"]) < 1e-6, (chk_ste, G["E2_Stecker_Sensor"])
E2D = E2P.endswith("_e2d.json")   # e2d zählt Einzelteile (Schrauben, Stifte), die Positionsmengen zählen Bauteile: Zählprüfung nur bei e2
assert E2D or sum(r["menge"] for r in Z if r["quelle"] and "Inhalt" in r["quelle"]) == G["E2_Schaltbox_Inhalt"]["anzahl"]
assert E2D or sum(r["menge"] for r in Z if r["quelle"] and "Stecker_Sensor" in r["quelle"]) == G["E2_Stecker_Sensor"]["anzahl"]

# Gruppen ohne BT (nicht anlegen, auflisten)
OHNE_BT = {"Verguss": "Verguss (Zellfeld NMC)", "E2_Lasche": "Plus-/Minus-Lasche (Stromschiene)", "E2_Trennbruecke": "Service-Trennbrücke (Cu) mit Schrauben", "E2_Servicedeckel": "Servicedeckel",
           "E2_FPC_Halter": "FPC-Halter (Masse offen, 0 gesetzt)",
           # neu im Detailstand e2d: Stromschiene mit Masse, übrige Masse offen (0 gesetzt)
           "E2_Stromschiene": "Stromschienen Cu der Schaltbox (e2d)"}
# e2d-Einzelteile ohne Masse (0 gesetzt): nur aufgelistet, nicht als Kostenposition gezählt
DETAIL = {"E2_Schraube": "Schrauben (e2d, Masse offen)", "E2_Kabelschuh": "Kabelschuhe (e2d, Masse offen)",
           "E2_Clip": "Kabelclips (e2d, Masse offen)", "E2_Schrumpfschlauch": "Schrumpfschlauch (e2d, Masse offen)", "E2_Dichtung": "Dichtungen (e2d, Masse offen)",
           "E2_Trennbrueckenschraube": "Trennbrückenschrauben (e2d, Masse offen)", "E2_FPC_Detail": "FPC-Details Tabs/NTC/Stecker (e2d, Masse offen)",
           "E2_Daisy": "Daisy-Chain-Kabel (e2d, Masse offen)", "E2_Beruehrschutz": "Berührschutz (e2d, Masse offen)"}
detail = [dict(gruppe=k, benennung=n, anzahl=G[k]["anzahl"], masse_kg=G[k]["masse_kg"], quelle=E2P) for k, n in DETAIL.items() if k in G]
fehlend = [dict(gruppe=k, benennung=n, anzahl=G[k]["anzahl"], masse_kg=G[k]["masse_kg"], quelle=E2P) for k, n in OHNE_BT.items() if k in G]
fehlend.append(dict(gruppe="(nicht im CAD)", benennung="Dichtungen (Deckel, Schaltbox, Servicedeckel)", anzahl=None, masse_kg=None, quelle="Auftrag, kein CAD-Teil"))
abgedeckt = {r["gruppe"] for r in Z if r["gruppe"]} | {"E2_Schaltbox_Inhalt", "E2_Stecker_Sensor"} | set(OHNE_BT) | set(DETAIL)
nicht_zugeordnet = [k for k in G if k not in abgedeckt]
assert not nicht_zugeordnet, nicht_zugeordnet

# Positionen füllen
def baugruppe(bt):
    while BT[bt].get("eltern") and BT[bt]["eltern"] != "BT-000": bt = BT[bt]["eltern"]
    return bt
for r in Z:
    if r["gruppe"]:
        x = G[r["gruppe"]]; r["menge"] = x["anzahl"]; r["masse"] = x["masse_kg"]; r["quelle"] = f"{E2P} gruppen.{r['gruppe']}"
        if r["werkstoff"] is None: r["werkstoff"] = x["werkstoff"]
    r["menge_" + V] = r["menge"]
    r["masse_je_kg"] = round(r["masse"] / r["menge"], 6) if r["menge"] and r["masse"] is not None else "offen"
    r["masse_ges_kg"] = round(r["masse"], 4) if r["masse"] is not None else "offen"
    r["kosten_je_eur"] = None; r["kosten_ges_eur"] = None
    r["baugruppe"] = baugruppe(r["bt"]); r["bt_name"] = BT[r["bt"]]["name"]
    for k in ("gruppe", "masse", "menge"): r.pop(k)
    assert r["bt"] in BT
# Zellmasse je Stück: Akte BT-100 masse_g
zel = next(r for r in Z if r["pos"] == "100.1"); zel["quelle"] += f"; Zellmasse parameter_{V}.json BT-100 masse_g = {P['BT-100']['masse_g']['wert']}"

# Alte Positionen ohne CAD-Menge: offen (keine Schätzung)
alt = json.loads((ROOT / "pm/bauteile/stueckliste.json").read_text())["positionen"]
besetzt = {r["pos"] for r in Z}
bt_besetzt = {r["bt"] for r in Z}
entf = [p for p in alt if V and BT[p["teil"]].get("varianten") and V not in BT[p["teil"]]["varianten"]]
entf_pos = {p["pos"] for p in entf}
offen_zeilen = []
for p in alt:
    if p["pos"] in besetzt or p["pos"] in entf_pos or p["teil"] in bt_besetzt: continue
    r = dict(pos=p["pos"], bt=p["teil"], benennung=p["benennung"], art=p["art"], werkstoff="offen", bemerkung="nicht im CAD, keine Akte mit Menge: offen", quelle="pm/bauteile/stueckliste.json (nur Benennung)",
             masse_je_kg="offen", masse_ges_kg="offen", kosten_je_eur=None, kosten_ges_eur=None, baugruppe=baugruppe(p["teil"]), bt_name=BT[p["teil"]]["name"]); r["menge_" + V] = "offen"; offen_zeilen.append(r)
Z += offen_zeilen
Z.sort(key=lambda r: (r["baugruppe"], r["bt"], r["pos"]))

# Summen
m_sum = sum(r["masse_ges_kg"] for r in Z if r["masse_ges_kg"] != "offen")
m_v1 = V1["masse_bekannt_kg"]; m_pm = PM["masse_kg"][V]
m_ohne_e2 = sum(r["masse_ges_kg"] for r in Z if r["masse_ges_kg"] != "offen" and not (r["quelle"] and ("E2_" in r["quelle"] or "A_e2" in r["quelle"])) )
abw = 100 * (m_sum / m_pm - 1); abw_e2cad = 100 * (m_sum / E2["masse_bekannt_kg"] - 1)
zellen_soll = {"LFP": 250, "NMC": 868}[V]; zellen = zel["menge_" + V]
n = zellen; energie = n * P["BT-100"]["nennspannung_V"]["wert"] * P["BT-100"]["kapazitaet_Ah"]["wert"] / 1000
# Widersprüche Akte/CAD (E1)
wid = []
if V == "LFP":
    r = next(r for r in Z if r["pos"] == "400.2"); wid.append(f"Zell-/Reihenverbinder: CAD {r['menge_LFP']} Stück, E1 {E1['LFP Zell-/Reihenverbinder (BT-410/420)']['stueck']} (s-1); CAD: innen stoßen Zellen an ({E2P}), Quelle E1 sim/elektrik/e1_querschnitte/ergebnis.json")
    r = next(r for r in Z if r["pos"] == "400.3"); wid.append(f"HV-Leitung: CAD {r['masse_ges_kg']} kg ({r['menge_LFP']} Stück), E1 {E1['LFP HV-Hauptleitung (BT-430)']['masse_gesamt_kg']:.2f} kg (2 x {E1['LFP HV-Hauptleitung (BT-430)']['laenge_mm']} mm)")
else:
    r = next(r for r in Z if r["pos"] == "400.1"); wid.append(f"Zellabgriff: CAD {r['menge_NMC']} Stück, E1 {E1['NMC Zellabgriff (BT-410)']['stueck']} (2 je Zelle)")
    r = next(r for r in Z if r["pos"] == "400.2"); wid.append(f"Gruppenverbinder: CAD {r['menge_NMC']} Stück ({r['masse_ges_kg']} kg), E1 {E1['NMC Gruppenverbinder (BT-420)']['stueck']} Stück ({E1['NMC Gruppenverbinder (BT-420)']['masse_gesamt_kg']:.2f} kg)")
    r = next(r for r in Z if r["pos"] == "400.3"); wid.append(f"HV-Leitung: CAD {r['masse_ges_kg']} kg ({r['menge_NMC']} Stück), E1 {E1['NMC HV-Hauptleitung (BT-430)']['masse_gesamt_kg']:.2f} kg (2 x {E1['NMC HV-Hauptleitung (BT-430)']['laenge_mm']} mm)")

# je Baugruppe
bg = {}
for r in Z:
    if r["masse_ges_kg"] != "offen": bg[r["baugruppe"]] = bg.get(r["baugruppe"], 0) + r["masse_ges_kg"]
out = dict(hinweis="KI-generiert (Claude Sonnet, 2026-11-18), Entwurf. Stückliste auf Konstruktionsstand (CAD e2d, Vorher-Lauf Bericht 0.3), Kostenspalten leer.", variante=V, version="0.2",
           quellen=[E2P, f"cad/pack/entwurf/ergebnis_{V}.json", "cad/pack/entwurf/ergebnis.json", f"pm/bauteile/parameter_{V}.json", "sim/elektrik/e1_querschnitte/ergebnis.json", "pm/bauteile/struktur.json"],
           summen=dict(masse_stueckliste_kg=round(m_sum, 3), masse_pack_massen_kg=m_pm, quelle_pack_massen="cad/pack/entwurf/ergebnis.json masse_kg." + V, abweichung_prozent=round(abw, 2),
                       masse_cad_e2_json_kg=E2["masse_bekannt_kg"], abweichung_gegen_e2_json_prozent=round(abw_e2cad, 4), masse_ohne_e2_teile_kg=round(m_ohne_e2, 3),
                       zellen=zellen, zellen_soll=zellen_soll, energie_kWh=round(energie, 2), energie_quelle=f"pm/bauteile/parameter_{V}.json BT-100 nennspannung_V x kapazitaet_Ah x Zellen",
                       masse_je_baugruppe_kg={k: round(v, 3) for k, v in sorted(bg.items())}),
           fehlende_bt=fehlend, detailteile_masse_offen_e2d=detail, widersprueche_akte_cad=wid, entfaellt=[f"{p['pos']} {p['benennung']}" for p in entf], positionen=Z)
(ROOT / f"pm/bauteile/stueckliste_{V}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))

# Dokument
f3 = lambda x: f"{x:.3f}".replace(".", ",") if isinstance(x, (int, float)) else x
md = [f"| Dok.-Nr. | BAT-DOC-13 | Version | 0.2 | Status | Entwurf |\n|---|---|---|---|---|---|\n| Titel | Stückliste Konstruktionsstand – Variante {V} | Ersteller | Claude Sonnet (KI), pm/bauteile/stueckliste_v2.py | Prüfer | Opus (Stichprobe), Mensch offen |\n\n"
      f"> **KI-generiert.** Nicht von Hand bearbeiten, `python3 pm/bauteile/stueckliste_v2.py --variante {V}` schreibt die Datei neu. Entwurf, nicht freigegeben. Mengen und Massen aus dem CAD (Stand e2d (Detailstand), neu erzeugt 2026-11-18), Quelle `{E2P}`.\n"
      "> **Kosten:** Spalten leer, werden von der Kostenrechnung gefüllt (`pm/kosten/`). Keine Preise in diesem Dokument.\n\n"
      f"**Zellen:** {zellen} (Soll {zellen_soll}), Energie {energie:.2f} kWh (Rechnung aus Akte BT-100). **Masse Stückliste:** {m_sum:.2f} kg; `pack_massen.py` (`cad/pack/entwurf/ergebnis.json`): {m_pm:.2f} kg; Abweichung {abw:+.2f} %"
      + (" (**> 2 %, an Opus**)" if abs(abw) > 2 else " (≤ 2 %)") + f". Gegen die CAD-Summe E2 (`{E2P}`): {abw_e2cad:+.4f} %. Der Unterschied zu `pack_massen.py` kommt aus den E2-Teilen und der längeren Wanne (Stand E2 gegen G4); ohne E2-Teile {m_ohne_e2:.2f} kg.\n\n"
      "Art: K Kaufteil, E Eigenteil. „offen“: keine CAD-Menge und keine Akte, nichts geschätzt.\n"]
bgn = None
for r in Z:
    if r["baugruppe"] != bgn:
        bgn = r["baugruppe"]; md.append(f"\n## {bgn} {BT[bgn]['name']}\n\n| Pos. | BT | Benennung | Menge {V} | Masse je [kg] | Masse ges. [kg] | Art | Werkstoff | Kosten je [€] | Kosten ges. [€] | Quelle | Bemerkung |\n|---|---|---|---|---|---|---|---|---|---|---|---|\n")
    md.append(f"| {r['pos']} | {r['bt']} {r['bt_name']} | {r['benennung']} | {r['menge_' + V]} | {f3(r['masse_je_kg'])} | {f3(r['masse_ges_kg'])} | {r['art']} | {r['werkstoff']} | | | {r['quelle']} | {r['bemerkung']} |\n")
md.append("\n## Fehlende Bauteile in struktur.json (Opus erweitert)\n\nIm CAD gebaut, aber ohne eigenes BT mit Merkmalen. Nicht angelegt, nur aufgelistet.\n\n| CAD-Gruppe | Benennung | Anzahl | Masse [kg] | Quelle |\n|---|---|---|---|---|\n")
for x in fehlend: md.append(f"| {x['gruppe']} | {x['benennung']} | {x['anzahl'] if x['anzahl'] is not None else '–'} | {f3(x['masse_kg']) if x['masse_kg'] is not None else '–'} | {x['quelle']} |\n")
md.append("\nDiese Massen sind in der Summe oben **nicht** enthalten (keine Position).\n")
if detail:
    md.append("\n## Detailteile aus e2d ohne Masse (nicht in Summe, nicht als Kostenposition gezählt)\n\n| CAD-Gruppe | Benennung | Anzahl | Masse [kg] | Quelle |\n|---|---|---|---|---|\n" + "".join(f"| {x['gruppe']} | {x['benennung']} | {x['anzahl']} | {f3(x['masse_kg'])} (offen, 0 gesetzt) | {x['quelle']} |\n" for x in detail))
md.append("\n## Widersprüche Akte/E1 gegen CAD (an Opus)\n\n" + "".join(f"- {w}\n" for w in wid))
md.append("\n## Masse je Baugruppe\n\n| Baugruppe | Masse [kg] |\n|---|---|\n" + "".join(f"| {k} {BT[k]['name']} | {f3(v)} |\n" for k, v in sorted(bg.items())))
md.append(f"\n![Masse je Baugruppe](bilder/stueckliste_massen_{V}.png)\n\n**Lesehilfe.** Links: Masse jeder Baugruppe des Packs in kg (logarithmische Achse, weil die Zellen alles andere weit übertreffen). Rechts: die Gesamtmasse der Stückliste gegen das grün schraffierte Zielband aus der G4-Erwartung (`cad/pack/pack_massen.py`, Band LFP 560–620 kg, NMC 390–430 kg) und die schwarze Linie `pack_massen.py`. Liegt der Balken im Band, passt die Stückliste zur Erwartung; liegt er darüber, sind es vor allem die Annahmen zu Kühlplatten, Rahmen und Verguss.\n")
md.append(f"\n---\n*KI-generiert (Claude Sonnet, 2026-11-18), Entwurf, nicht freigegeben. {len(Z)} Positionen. Dokument BAT-DOC-13, Version 0.2.*\n")
(ROOT / f"docs/13_stueckliste_{V}.md").write_text("".join(md))

# Bild
BAND = {"LFP": (560, 620), "NMC": (390, 430)}[V]
fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 5.5), gridspec_kw=dict(width_ratios=[2.2, 1]))
ks = sorted(bg); a1.barh([f"{k} {BT[k]['name']}" for k in ks], [bg[k] for k in ks], color="#1f77b4"); a1.set_xscale("log"); a1.invert_yaxis(); a1.set_xlabel("Masse [kg], logarithmisch")
for i, k in enumerate(ks): a1.text(bg[k] * 1.05, i, f"{bg[k]:.1f} kg", va="center", fontsize=8)
a1.set_xlim(0.1, 2000); a1.set_title(f"Masse je Baugruppe, Variante {V}")
a2.bar(0, m_sum, 0.5, color="#1f77b4"); a2.add_patch(plt.Rectangle((-0.38, BAND[0]), 0.76, BAND[1] - BAND[0], fill=False, ec="green", lw=2.5, hatch="//", label=f"Zielband {BAND[0]}–{BAND[1]} kg"))
a2.plot([-0.38, 0.38], [m_pm] * 2, "k--", label=f"pack_massen.py {m_pm:.0f} kg"); a2.text(0, m_sum + 8, f"Stückliste {m_sum:.0f} kg", ha="center", fontweight="bold")
a2.set_xticks([]); a2.set_ylim(0, 900 if V == "LFP" else 700); a2.set_ylabel("Masse [kg]"); a2.set_title(f"Gesamt ({zellen} Zellen)"); a2.legend(loc="upper right", fontsize=8)
fig.text(.01, .01, f"KI-generiert (Claude Sonnet), Entwurf, nicht freigegeben. Quelle: pm/bauteile/stueckliste_{V}.json, {E2P}, cad/pack/entwurf/ergebnis.json. Band: cad/pack/pack_massen.py. Lesehilfe: docs/13_stueckliste_{V}.md", fontsize=7)
fig.tight_layout(rect=(0, .03, 1, 1)); fig.savefig(ROOT / f"docs/bilder/stueckliste_massen_{V}.png", dpi=110); plt.close(fig)
print(V, len(Z), "Positionen", f"{m_sum:.2f} kg vs {m_pm:.2f} ({abw:+.2f} %)", "Zellen", zellen)
