"""stueckliste.py -- Grobe Stückliste (Baugruppen und Hauptkomponenten, keine Normteile) aus Bauteilbaum und Startwerten.

KI-generiert (Claude Opus, 2026-11-12; geändert 2026-11-16 Sonnet, --variante V nach AUFTRAG_VARIANTEN). Vorgabe des Autors: „Du kannst aber auch schon eine Art Stückliste schreiben,
damit wir wissen, was wir brauchen, das muss natürlich nicht auf eine Schraube runtergebrochen werden.“

    python3 pm/bauteile/stueckliste.py [--variante V]
Eingaben: pm/startwerte.json (Startsatz, Vorschlag), pm/bauteile/struktur.json (BT-Nummern)
Ausgabe:  pm/bauteile/stueckliste.json, docs/13_stueckliste.md
Mit --variante V: Eingaben pm/startwerte_V.json und pm/bauteile/parameter_V.json, Ausgabe stueckliste_V.json, docs/13_stueckliste_V.md.
Mengen mit Formel hängen am Startsatz und an ANNAHMEN (A_*), bis Recherche und Auslegung sie ersetzen.
Art: K = Kaufteil, E = Eigenteil (Konstruktion im Projekt), S = Schnittstelle zum Fahrzeug (nicht im Pack, nur Anforderung).
"""
import json, math, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if "--variante" in sys.argv and "--alt" not in sys.argv:   # SL2 (2026-11-18): Konstruktionsstand statt Startwert-Entwurf; alter Entwurf mit --alt
    import subprocess; raise SystemExit(subprocess.call([sys.executable, str(Path(__file__).with_name("stueckliste_v2.py")), "--variante", sys.argv[sys.argv.index("--variante") + 1]]))
VAR = None
if "--variante" in sys.argv:
    VAR = sys.argv[sys.argv.index("--variante") + 1]
    if VAR not in json.loads((ROOT / "pm/varianten.json").read_text()): raise SystemExit(f"Unbekannte Variante {VAR}")
SFX = f"_{VAR}" if VAR else ""
S = json.loads((ROOT / f"pm/startwerte{SFX}.json").read_text()); ab = S["abgeleitet"]
_par = json.loads((ROOT / f"pm/bauteile/parameter{SFX}.json").read_text())
_p100 = _par["parameter"]["BT-100"]
CHEM = (_p100.get("chemie", {}).get("wert") or ab["chemie"]).split()[0] if VAR else ab["chemie"].split()[0]   # Variante: Chemie aus entschiedener Akte (startwerte_V nennt noch LFP)
_fmt = _p100["format"]["wert"]
FORMAT = "Format entschieden: " + str(_fmt) if _fmt else "Zellformat offen"

# Annahmen (Schätzwerte Opus) -- prüfen durch Recherche/Auslegung
A_U_ZELLE = {"LFP": 3.2, "NMC": 3.65}       # Nennspannung je Zelle [V]       prüft: W01, W10
A_AH_ZELLE = {"LFP": 140, "NMC": 100}       # Kapazität einer langen prismatischen Zelle [Ah]   prüft: W03, W08, P01
A_KANAELE_JE_UEBERWACHUNG = 16              # Zellspannungen je Überwachungsbaustein          prüft: W05, W14, T06
A_ZELLEN_JE_TEMPFUEHLER = 4                 # Temperaturfühler: einer je 4 Zellen              prüft: W05
A_ZELLEN_JE_REIHE = 24                      # Zellen je Reihe zwischen zwei Querträgern (CTP)  prüft: W03, P02

try:
    _u = _par["parameter"]["BT-000"]["nennspannung_V"]["wert"]       # ENT-006, falls entschieden
except (KeyError, TypeError):
    _u = None
U_SYS = _u if _u else ab["U_nenn_V"]
U_Z = _p100.get("nennspannung_V", {}).get("wert") or A_U_ZELLE[CHEM]            # entschiedene Zellspannung (ENT-010), sonst Annahme
AH_FEST = _p100.get("kapazitaet_Ah", {}).get("wert")                           # entschiedene Zellkapazität (ENT-009), sonst None
s = math.ceil(U_SYS / U_Z)                                                     # Reihenschaltung
if AH_FEST:                                                                    # Kaufzelle fest: p aus Energie
    AH_ZELLE = AH_FEST; p = math.ceil(ab["kWh_brutto"] * 1000 / (s * U_Z * AH_ZELLE))
else:                                                                          # Zelle wird angepasst (ENT-006: p = 1)
    p = 1; AH_ZELLE = ab["kWh_brutto"] * 1000 / (s * U_Z)                      # abgeleitet aus Energie und Systemspannung [Ah]
n = s * p
e_ist = n * U_Z * AH_ZELLE / 1000
ueberw = math.ceil(s / A_KANAELE_JE_UEBERWACHUNG); temp = math.ceil(n / A_ZELLEN_JE_TEMPFUEHLER)
reihen = math.ceil(n / A_ZELLEN_JE_REIHE)

# Pos, BT, Benennung, Menge, Formel, Art, Auslegung (Vorgang), Recherche, Bemerkung
T = [
    # BT-100 Zelle
    ("100.1", "BT-100", (f"Zelle, {_fmt} ({CHEM})" if _fmt else f"Zelle, lang prismatisch ({CHEM})" if CHEM == "LFP" else f"Zelle ({CHEM}, Zellformat offen; Rechenregel wie LFP-Platzhalter)"), n, f"{s}s × {p}p", "K", "C2, G1", "W01, W03, W08, W10, P01",
     (f"Energie {e_ist:.1f} kWh bei {AH_ZELLE:.1f} Ah fest (ENT-009), p aus Energie; Maße folgen in G1" if AH_FEST else f"Energie {e_ist:.1f} kWh bei {AH_ZELLE:.1f} Ah (Annahme bisher {A_AH_ZELLE[CHEM]} Ah); Ah abgeleitet aus Energie und 800 V (ENT-006); Maße folgen in G1")),
    # BT-200 Zellstack
    ("200.1", "BT-200", "Zellreihe zwischen Querträgern (Cell-to-Pack, ohne Module)", reihen, f"{n} / {A_ZELLEN_JE_REIHE}", "E", "G4", "W03, P02", "Alternative: Module, falls CTP verworfen"),
    ("200.2", "BT-200", "Zwischenlage zwischen Zellen (Wärme- und Brandschutz, Quellausgleich)", n, "1 je Zelle", "K", "G4, M1", "W04, P04", "Werkstoff offen (z. B. Glimmer, Aerogel)"),
    ("200.3", "BT-200", "Wärmeleitmaterial Zelle → Kühlplatte", 1, "1 Lage, Fläche aus G4", "K", "G4, K3", "W16, P03", ""),
    ("200.4", "BT-200", "Verspannung der Zellreihen (Endplatte/Band)", reihen, "1 je Reihe", "E", "M1", "W15", "Quellen der Zellen beim Laden"),
    ("200.5", "BT-250", "Zellhalter (hält und teilt Rundzellen, Abstand für Kühlung und Isolation)", 1, "1 Satz", "K", "G4", "–", "Maße offen, G4; nur NMC (Rundzelle)"),
    # BT-300 Regelung
    ("300.1", "BT-300", "BMS-Hauptsteuergerät", 1, "–", "K", "E3", "W05, W14, T06", "Ladezustand, Alterung, Schutzlogik, Fahrzeug-CAN"),
    ("300.2", "BT-300", "Zellüberwachung (Spannung, Ausgleich)", ueberw, f"{s} / {A_KANAELE_JE_UEBERWACHUNG}", "K", "E3", "W05, W14, P07", "passiver oder aktiver Ausgleich offen"),
    ("300.3", "BT-300", "Temperaturfühler Zelle", temp, f"{n} / {A_ZELLEN_JE_TEMPFUEHLER}", "K", "E3, K3", "W05", ""),
    ("300.4", "BT-300", "Strommessung (Shunt oder Hall)", 1, "–", "K", "E3", "W14", ""),
    ("300.5", "BT-300", "Isolationswächter", 1, "–", "K", "E2", "W13", "REQ-P13"),
    ("300.6", "BT-300", "Messleitungen bzw. Flexleiterplatte Zelle → Überwachung", ueberw, "1 je Überwachungsbaustein", "K", "E3, L1", "P07", ""),
    # BT-400 Verkabelung
    ("400.1", "BT-400", "Zellverbinder (Zellabgriff, Plus und Minus je Zelle)", 2 * n if p > 1 else 0, f"2 · {n} Zellen" if p > 1 else "entfällt bei p = 1 (Reihenverbinder 400.2 sind die Zellverbinder)", "E", "E1", "W13, P06", "Querschnitt aus Strom und Erwärmung (E1); Opus 2026-11-17: Mengen aus s und p"),
    ("400.2", "BT-400", "Reihenverbinder (Reihenbrücke, bei p > 1 Gruppenbrücke)", s - 1, f"s − 1 = {s} − 1", "E", "E1, L1", "W13", "Opus 2026-11-17: aus s abgeleitet (LFP 249, NMC 216)"),
    ("400.3", "BT-400", "HV-Hauptleitung plus/minus im Pack", 2, "–", "K", "E1, L1", "W13, T09", "Verlegung skizzieren (Sketch-to-Prompt)"),
    # BT-500 Struktur
    ("500.1", "BT-500", "Gehäusewanne", 1, "–", "E", "G4, X1", "W15, P10", "Werkstoff offen (Alu-Strangpress/Guss, Stahl)"),
    ("500.2", "BT-500", "Deckel mit Dichtung", 1, "1 Satz", "E", "G4", "W15", "Schutzart REQ-P13"),
    ("500.3", "BT-500", "Querträger", reihen + 1, f"{reihen} Reihen + 1", "E", "G4, X1", "W15, P02", "tragen und trennen Zellreihen"),
    ("500.4", "BT-500", "Seitenrahmen / Crashprofil (Seitencrash)", 2, "links, rechts", "E", "X1, X2", "W17, T08", ""),
    ("500.5", "BT-500", "Unterfahrschutz", 1, "–", "E", "M1", "W15", "Steinschlag, Aufsetzen"),
    ("500.6", "BT-500", "Befestigungspunkte am Fahrzeug", 1, "1 Satz", "E", "M1", "–", "Fest-/Loslager (Lehre Wasserstoff)"),
    ("500.7", "BT-500", "Druckausgleichselement (atmend, wasserdicht)", 1, "–", "K", "G5", "–", ""),
    # BT-600 Kühlung
    ("600.1", "BT-600", "Kühlplatte (Wasser-Glykol)", 1, "1 oder je Reihe, aus K0/K3", "E", "K0, K3, U4", "W16, P03", "Alternative Luftkühlung: Gebläse + Kanäle (Entscheidung K0)"),
    ("600.2", "BT-600", "Verteiler und Sammler", 1, "1 Satz", "E", "K2, K4", "P03", "Gleichverteilung entscheidet (Lehre Wasserstoff); Austritt ≥ Eintritt (Regel des Autors aus Fusion, hier prüfen)"),
    ("600.3", "BT-600", "Kühlmittelanschlüsse Ein/Aus", 2, "–", "K", "K2", "–", ""),
    ("600.4", "BT-600", "Temperaturfühler Kühlmittel", 2, "Ein, Aus", "K", "K3, E3", "–", ""),
    ("600.5", "BT-600", "Kühlmittel Wasser-Glykol", 1, "Füllmenge aus K2", "K", "K2", "W16", "REQ-P12"),
    ("600.6", "BT-600", "Pumpe, Wärmetauscher/Kältemittelkühler", 1, "Fahrzeugseite", "S", "K0", "W16", "nur Schnittstelle: Durchfluss, Eintrittstemperatur"),
    # BT-700 Zusatz (Schaltbox, Schutz, Stecker, Entgasung; Zuordnung nach Bauteilrolle BT-700, ENT-004)
    ("700.1", "BT-700", "Schaltbox (Gehäuse für Schütze, Vorladung, Hauptsicherung)", 1, "–", "E", "E2, G4", "W13", "Trennstelle Stack/Fahrzeug; Einbauort aus G4"),
    ("700.2", "BT-700", "Hauptschütz plus und minus", 2, "–", "K", "E2", "W13", f"{ab['U_nenn_V']} V DC, Strom aus REQ-P04/P05"),
    ("700.3", "BT-700", "Vorladeschütz mit Vorladewiderstand", 1, "1 Satz", "K", "E2, E4", "W13", "Einschaltstrom der Umrichterkondensatoren"),
    ("700.4", "BT-700", "Hauptsicherung (ggf. pyrotechnischer Trenner)", 1, "–", "K", "E2", "W13", "Kurzschlussfall E4"),
    ("700.5", "BT-700", "Service-Trennstecker", 1, "–", "K", "E2", "W13", "Werkstatt: Pack spannungsfrei schalten"),
    ("700.6", "BT-700", "HV-Steckverbinder Pack (Antrieb, Laden)", 2, "–", "K", "E2, L1", "W12, W13", ""),
    ("700.7", "BT-700", "NV-Steckverbinder (12 V, CAN, Sensorik)", 1, "–", "K", "E3", "W14", ""),
    ("700.8", "BT-700", "Entgasungsventil mit Entgasungskanal", 1, "1 Satz", "K", "G5", "W04, P05", "thermisches Durchgehen, REQ-P11"),
    ("700.9", "BT-700", "Heizung (Kälte, −20 °C laut REQ-P08)", 1, "–", "K", "K0, C5", "W01, W16", "oder über Kühlkreis (Fahrzeugseite)"),
    ("700.10", "BT-700", "Gas-/Drucksensor Früherkennung thermisches Ereignis", 1, "–", "K", "E3, F1", "W04", "Warnzeit REQ-P11"),
    ("700.11", "BT-700", "Kennzeichnung (Typschild, HV-Warnung)", 1, "1 Satz", "K", "B4", "–", "Normen BAT-DOC-07"),
]


def main():
    bt_liste = json.loads((ROOT / "pm/bauteile/struktur.json").read_text())["bauteile"]
    teil = {pos: x["id"] for x in bt_liste for pos in (x.get("stueckliste") or [])}
    # Positionen von Bauteilen mit Feld "varianten" entfallen in Varianten, die nicht darin stehen
    entfaellt = {pos for x in bt_liste if VAR and x.get("varianten") and VAR not in x["varianten"] for pos in ([*(x.get("stueckliste") or [])])}
    gestrichen = sorted(entfaellt); NAME = {x[0]: x[2] for x in T}
    items = [dict(pos=a, bt=b, teil=teil.get(a, "FEHLT"), benennung=c, menge=d, formel=e, art=f, vorgang=g, recherche=h, bemerkung=i) for a, b, c, d, e, f, g, h, i in T if a not in entfaellt]
    fehlt = [x["pos"] for x in items if x["teil"] == "FEHLT"] + sorted(set(teil) - {x["pos"] for x in items} - entfaellt)
    if fehlt: raise SystemExit(f"Stückliste und struktur.json passen nicht zusammen: {fehlt}")
    out = dict(hinweis="KI-generiert. Grobe Stückliste, Mengen aus Startsatz (Vorschlag) und Annahmen.", startsatz=S["satz"],
               entfaellt=[f"{pos} {NAME.get(pos, '')}" for pos in gestrichen],
               ableitung=dict(variante=VAR, chemie=CHEM, zellformat=FORMAT, reihe_s=s, parallel_p=p, ah_zelle=round(AH_ZELLE, 3), u_zelle_V=U_Z, zellen=n, energie_kWh=round(e_ist, 1),
                              ueberwachungsbausteine=ueberw, temperaturfuehler=temp, zellreihen=reihen),
               annahmen=dict(U_zelle=A_U_ZELLE, Ah_zelle=A_AH_ZELLE, kanaele_je_ueberwachung=A_KANAELE_JE_UEBERWACHUNG,
                             zellen_je_tempfuehler=A_ZELLEN_JE_TEMPFUEHLER, zellen_je_reihe=A_ZELLEN_JE_REIHE), positionen=items)
    (ROOT / f"pm/bauteile/stueckliste{SFX}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
    md = ["| Dok.-Nr. | BAT-DOC-13 | Version | 0.1 | Status | Entwurf |\n|---|---|---|---|---|---|\n"
          f"| Titel | Grobe Stückliste{' – Variante ' + VAR if VAR else ''} | Ersteller | Claude Opus (KI), pm/bauteile/stueckliste.py | Prüfer | – (Mensch offen) |\n\n"
          f"> **Variante: {VAR or '(ohne Variantenangabe)'}; {FORMAT}.**\n"
          + (f"> **Entfällt bei {VAR}:** " + "; ".join(f"{pos} {NAME.get(pos, '')}" for pos in gestrichen) + ".\n" if gestrichen else "")
          + "> **KI-generiert.** Nicht von Hand bearbeiten, das Skript schreibt die Datei neu. Baugruppen und Hauptkomponenten, keine Normteile.\n"
          "> Mengen hängen am **Startsatz (Vorschlag, nicht freigegeben)** und an **Annahmen**; sie ändern sich mit Lastenheft und Auslegung.\n\n"
          f"Startsatz: „{S['satz']}“ → {CHEM}, {ab['U_nenn_V']} V, {ab['kWh_brutto']} kWh brutto.\n\n"
          f"**Zellverschaltung:** {s}s × {p}p = **{n} Zellen**, {e_ist:.1f} kWh "
          + (f"({U_Z} V, {AH_ZELLE:.3f} Ah je Zelle fest (ENT-009/010), p = ceil(E·1000/(s·U·Ah)) bei {U_SYS:.0f} V).\n\n" if AH_FEST else f"({U_Z} V Annahme; {AH_ZELLE:.1f} Ah je Zelle abgeleitet aus Energie und {U_SYS:.0f} V, ENT-006; Annahme bisher {A_AH_ZELLE[CHEM]} Ah).\n\n")
          + "Art: K = Kaufteil, E = Eigenteil (wird im Projekt konstruiert), S = Schnittstelle zum Fahrzeug (nur Anforderung).\n"]
    gruppe = None
    namen = {x["id"]: x["name"] for x in json.loads((ROOT / "pm/bauteile/struktur.json").read_text())["bauteile"]}
    for it in items:
        if it["bt"] != gruppe:
            gruppe = it["bt"]
            md.append(f"\n## {gruppe} {namen.get(gruppe, '')}\n\n| Pos. | Bauteil | Benennung | Menge | Herleitung | Art | Auslegung (Vorgang) | Recherche | Bemerkung |\n|---|---|---|---|---|---|---|---|---|\n")
        md.append(f"| {it['pos']} | {it['teil']} | {it['benennung']} | {it['menge']} | {it['formel']} | {it['art']} | {it['vorgang']} | {it['recherche']} | {it['bemerkung']} |\n")
    md.append("\n## Annahmen\n\n" + "".join(f"- `{k}` = {v}\n" for k, v in out["annahmen"].items()))
    md.append(f"\n---\n*KI-generiert. {len(items)} Positionen. Vorgänge siehe pm/plan/wissensnetz.html.*\n")
    (ROOT / f"docs/13_stueckliste{SFX}.md").write_text("".join(md))
    print(json.dumps(out["ableitung"], ensure_ascii=False), f"{len(items)} Positionen")


if __name__ == "__main__":
    main()
