"""KI-generiert, geändert 2026-11-16 Sonnet (entschiedene Chemie aus parameter.json hat Vorrang, AUFTRAG_LFP_UMSTELLUNG; --variante V, AUFTRAG_VARIANTEN).
startwerte.py -- Aus EINEM Satz in Alltagssprache die Lastenheft-Werte REQ-P01..P10 herleiten.

KI-generiert (Claude Opus, 2026-11-12). Vorgabe des Autors: „bestimme auch notwendige startparameter:
Ziel -> so wenig wie möglich in natürlicher Sprache“.

Minimaler Startsatz = vier Angaben, die nur der Mensch kennt (alles andere folgt daraus):
  1. Fahrzeug        (Kleinwagen | Kompakt | Mittelklasse | SUV | Transporter)
  2. Reichweite      („… km“, Alltag, nicht Prüfzyklus)
  3. Nachladen       („in … min“ von 10 auf 80 %)
  4. Einsatzgebiet   (Nordeuropa | Mitteleuropa | Südeuropa)
Fehlt eine Angabe, wird der Vorschlag eingesetzt und als solcher gekennzeichnet.

    python3 pm/startwerte.py "Kompaktwagen, 400 km Reichweite, in 20 min auf 80 %, Mitteleuropa"
Ausgabe: pm/startwerte.json, docs/startparameter.md
    python3 pm/startwerte.py --variante NMC "…"   Chemie aus pm/bauteile/parameter_NMC.json (sonst die Variante selbst);
                                                  Ausgabe pm/startwerte_NMC.json, docs/startparameter_NMC.md

ALLE Faktoren in TAB_* sind ANNAHMEN (Schätzwerte Opus) bis zur Bestätigung durch die Recherche (Spalte „prüft“).
Keine Programmlogik versteckt Werte: jede Zahl steht in einer Tabelle oder im Rechenweg.
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VAR = None   # Variante (LFP/NMC) oder None; wird in main() aus --variante gesetzt

# Fahrzeugklasse: Verbrauch Alltag [kWh/100 km], Bauraum Unterboden L x B x H [m], Spitzenleistung Antrieb [kW]
TAB_FZ = {
    "Kleinwagen":   dict(verbrauch=15, L=1.6, B=1.2, H=0.13, p_spitze=90),
    "Kompakt":      dict(verbrauch=17, L=1.9, B=1.4, H=0.13, p_spitze=150),
    "Mittelklasse": dict(verbrauch=18, L=2.1, B=1.5, H=0.13, p_spitze=220),
    "SUV":          dict(verbrauch=21, L=2.2, B=1.6, H=0.15, p_spitze=250),
    "Transporter":  dict(verbrauch=28, L=2.6, B=1.6, H=0.18, p_spitze=150),
}
SYNONYM = {"klein": "Kleinwagen", "kompakt": "Kompakt", "golf": "Kompakt", "mittelklasse": "Mittelklasse", "limousine": "Mittelklasse",
           "suv": "SUV", "gelände": "SUV", "transporter": "Transporter", "lieferwagen": "Transporter", "bus": "Transporter"}
# Einsatzgebiet: Umgebungstemperatur Betrieb [°C]
TAB_KLIMA = {"Nordeuropa": (-30, 35), "Mitteleuropa": (-20, 40), "Südeuropa": (-10, 45)}
# Systemfaktoren
A = dict(
    reserve=0.08,          # Anteil nicht nutzbar (oben/unten gesperrt)          prüft: W06/W14
    ladefenster=0.70,      # 10 -> 80 %                                          Vorgabe Startsatz
    spitze_zu_mittel=1.3,  # Ladeleistung Spitze / Mittel                        prüft: W12
    grenze_400V_kW=150,    # darüber 800 V (Strom ~ 400 A bei 400 V)             prüft: W12 (CCS)
    dauer_zu_spitze=0.4,   # Dauerleistung / Spitzenleistung                     prüft: W06
    km_leben=200000,       # Fahrleistung Lebensdauer                            Annahme
    sicherheit_zyklen=2.0, # Faktor auf rechnerische Vollzyklen                  Annahme
    rest_soh=0.80,         # Restkapazität am Lebensende                         prüft: W14
    wh_l_pack={"LFP": 180, "NMC": 330},   # Pack-Energiedichte Volumen [Wh/L]   prüft: W01/W03/W10 (Zelle x Füllgrad ~0,6)
    wh_kg_pack={"LFP": 140, "NMC": 200},  # Pack-Energiedichte Masse [Wh/kg]    prüft: W01/W10
    c_laden_max={"LFP": 3.0, "NMC": 3.0}, # Ladestrom Spitze in C, Zelle       prüft: W01/W10/P01
)
VORSCHLAG = dict(fahrzeug="Kompakt", reichweite_km=400, laden_min=20, klima="Mitteleuropa")


def lesen(satz):
    s = satz.lower(); g, quelle = {}, {}
    for k, v in SYNONYM.items():
        if k in s: g["fahrzeug"] = v; break
    if m := re.search(r"(\d{2,4})\s*km", s): g["reichweite_km"] = int(m.group(1))
    if m := re.search(r"(\d{1,3})\s*min", s): g["laden_min"] = int(m.group(1))
    for k in TAB_KLIMA:
        if k.lower()[:4] in s or k.lower() in s: g["klima"] = k
    if "deutschland" in s or "alpen" in s: g.setdefault("klima", "Mitteleuropa")
    for k, v in VORSCHLAG.items():
        quelle[k] = "Startsatz" if k in g else "VORSCHLAG (nicht im Satz)"; g.setdefault(k, v)
    return g, quelle


def entschiedene_chemie():
    """Entschiedene Zellchemie aus parameter.json bzw. parameter_<V>.json (BT-100/chemie) -> (Wert, Akte) oder None.
    Mit Variante und ohne Akte: die Variante selbst ist die Chemie (varianten.json), Akte "Variante V"."""
    try:
        f = f"parameter_{VAR}.json" if VAR else "parameter.json"
        e = json.loads((ROOT / "pm" / "bauteile" / f).read_text())["parameter"]["BT-100"]["chemie"]
    except Exception:
        e = {}
    if e.get("wert"): return (e["wert"], e["entscheidung"])
    return (VAR, f"Variante {VAR}") if VAR else None


def entschiedene_laenge():
    """Entschiedene Bauraumlänge BT-000/bauraum_laenge_mm aus parameter.json (mm) -> (m, Akte) oder None (KI, 2026-11-17, ENT-013)."""
    try:
        e = json.loads((ROOT / "pm" / "bauteile" / "parameter.json").read_text())["parameter"]["BT-000"]["bauraum_laenge_mm"]
        if e.get("wert"): return (e["wert"] / 1000, e["entscheidung"])
    except Exception:
        pass
    return None


def entschiedene_breite():
    """Entschiedene Bauraumbreite BT-000/bauraum_breite_mm aus parameter.json (mm) -> (m, Akte) oder None (KI, 2026-11-17, ENT-030; wie die Länge)."""
    try:
        e = json.loads((ROOT / "pm" / "bauteile" / "parameter.json").read_text())["parameter"]["BT-000"]["bauraum_breite_mm"]
        if e.get("wert"): return (e["wert"] / 1000, e["entscheidung"])
    except Exception:
        pass
    return None


def herleiten(g):
    fz = dict(TAB_FZ[g["fahrzeug"]]); r = []   # r: (REQ, Größe, Wert, Rechenweg)
    fz_L = entschiedene_laenge()
    if fz_L: fz["L"] = fz_L[0]
    fz_B = entschiedene_breite()
    if fz_B: fz["B"] = fz_B[0]
    e_netto = g["reichweite_km"] * fz["verbrauch"] / 100
    e_brutto = e_netto / (1 - A["reserve"])
    r.append(("REQ-P01", "Fahrzeug", g["fahrzeug"], "Startsatz"))
    r.append(("REQ-P02", "Energie nutzbar / brutto", f"{e_netto:.0f} / {e_brutto:.0f} kWh",
              f"{g['reichweite_km']} km × {fz['verbrauch']} kWh/100 km; brutto = netto / (1 − {A['reserve']})"))
    p_mittel = A["ladefenster"] * e_netto / (g["laden_min"] / 60); p_lad = A["spitze_zu_mittel"] * p_mittel
    r.append(("REQ-P05", "Schnellladen", f"10→80 % in {g['laden_min']} min: Mittel {p_mittel:.0f} kW, Spitze {p_lad:.0f} kW",
              f"{A['ladefenster']} × {e_netto:.0f} kWh / {g['laden_min']/60:.2f} h; Spitze × {A['spitze_zu_mittel']}"))
    u = 800 if max(p_lad, fz["p_spitze"]) > A["grenze_400V_kW"] else 400
    r.append(("REQ-P03", "Systemspannung", f"{u} V (nominal)", f"max(Ladespitze {p_lad:.0f}, Antrieb {fz['p_spitze']}) kW "
              f"{'>' if u == 800 else '≤'} {A['grenze_400V_kW']} kW"))
    r.append(("REQ-P04", "Leistung Entladen", f"Spitze {fz['p_spitze']} kW, Dauer {A['dauer_zu_spitze']*fz['p_spitze']:.0f} kW",
              f"Fahrzeugklasse; Dauer = {A['dauer_zu_spitze']} × Spitze"))
    vol_l = fz["L"] * fz["B"] * fz["H"] * 1000; noetig = e_brutto * 1000 / vol_l
    passt = {c: A["wh_l_pack"][c] >= noetig for c in A["wh_l_pack"]}
    regel = "LFP" if passt["LFP"] else ("NMC" if passt["NMC"] else "NMC (Bauraum reicht nicht)")
    chem_ent = entschiedene_chemie()
    chem = chem_ent[0] if chem_ent else regel
    c_rate = p_lad / e_brutto
    r.append(("REQ-P06", "Zellchemie", chem, f"nötig {noetig:.0f} Wh/L im Bauraum {vol_l:.0f} L; Pack LFP {A['wh_l_pack']['LFP']}, "
              f"NMC {A['wh_l_pack']['NMC']} Wh/L; Regel: LFP, wenn sie passt (günstiger, sicherer)" if not chem_ent else
              f"{chem} ({chem_ent[1]}, entschieden); Bauraumregel: nötig {noetig:.0f} Wh/L im Bauraum {vol_l:.0f} L; Pack LFP {A['wh_l_pack']['LFP']}, "
              f"NMC {A['wh_l_pack']['NMC']} Wh/L; Regel ergäbe {regel}"))
    c0 = chem.split()[0]; masse = e_brutto * 1000 / A["wh_kg_pack"][c0]
    r.append(("REQ-P07", "Bauraum / Masse", f"{fz['L']} × {fz['B']} × {fz['H']} m, ca. {masse:.0f} kg",
              f"Fahrzeugklasse{'; L aus ' + fz_L[1] if fz_L else ''}{'; B aus ' + fz_B[1] if fz_B else ''}; Masse = {e_brutto:.0f} kWh / {A['wh_kg_pack'][c0]} Wh/kg"))
    t = TAB_KLIMA[g["klima"]]
    r.append(("REQ-P08", "Umgebungstemperatur", f"{t[0]} … +{t[1]} °C", f"Einsatzgebiet {g['klima']}"))
    zyk = A["km_leben"] / g["reichweite_km"] * A["sicherheit_zyklen"]
    r.append(("REQ-P10", "Lebensdauer", f"≥ {zyk:.0f} Vollzyklen bis {A['rest_soh']*100:.0f} % Restkapazität",
              f"{A['km_leben']} km / {g['reichweite_km']} km × {A['sicherheit_zyklen']}"))
    warn = []
    if c_rate > A["c_laden_max"][c0]: warn.append(f"Ladestrom {c_rate:.1f} C über Annahme {A['c_laden_max'][c0]} C für {c0}: Ladezeit oder Zelle prüfen")
    if not passt["LFP"]:
        if chem_ent and chem == "LFP": warn.append(f"Bauraum offen: Annahme wh_l_pack LFP {A['wh_l_pack']['LFP']} Wh/L unbelegt (B-BAT-004/006); nötig {noetig:.0f} Wh/L")
        else: warn.append(f"LFP passt nicht in den Bauraum (nötig {noetig:.0f} > {A['wh_l_pack']['LFP']} Wh/L)")
    if "reicht nicht" in chem: warn.append("Auch NMC passt nicht: Reichweite, Bauraumhöhe oder Fahrzeugklasse ändern")
    abgeleitet = dict(kWh_netto=round(e_netto, 1), kWh_brutto=round(e_brutto, 1), U_nenn_V=u, P_laden_spitze_kW=round(p_lad),
                      C_laden_spitze=round(c_rate, 2), Wh_L_noetig=round(noetig), chemie=chem, masse_kg=round(masse))
    return r, warn, abgeleitet


def main():
    global VAR
    a = sys.argv[1:]
    if "--variante" in a:
        i = a.index("--variante"); VAR = a[i + 1]; del a[i:i + 2]
        if VAR not in json.loads((ROOT / "pm" / "varianten.json").read_text()): raise SystemExit(f"Unbekannte Variante {VAR}")
    sfx = f"_{VAR}" if VAR else ""
    satz = " ".join(a) or "Kompaktwagen, 400 km Reichweite, in 20 min auf 80 %, Mitteleuropa"
    g, quelle = lesen(satz); r, warn, abg = herleiten(g)
    out = dict(variante=VAR, hinweis="KI-generiert. Alle Faktoren Annahmen bis Recherche-Bestätigung.", satz=satz, start=g, herkunft=quelle,
               abgeleitet=abg, warnungen=warn, annahmen={k: v for k, v in A.items()}, fahrzeug_tabelle={**TAB_FZ[g["fahrzeug"]], **({"L": entschiedene_laenge()[0], "L_quelle": entschiedene_laenge()[1]} if entschiedene_laenge() else {})})
    (ROOT / "pm" / f"startwerte{sfx}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
    md = [f"# Startparameter Batteriesystem{' – Variante ' + VAR if VAR else ''}\n\n> **KI-generiert** (Claude Opus, pm/startwerte.py). Status: Vorschlag, nicht freigegeben. "
          f"Alle Faktoren sind **Annahmen**, bis die Recherche (W01–W15) sie bestätigt.\n\n## Startsatz (das Einzige, was der Mensch vorgibt)\n\n> „{satz}“\n\n"
          "| Angabe | Wert | Herkunft |\n|---|---|---|\n"]
    md += [f"| {k} | {g[k]} | {quelle[k]} |\n" for k in VORSCHLAG]
    md.append("\n## Hergeleitete Lastenheft-Werte\n\n| REQ | Größe | Wert | Rechenweg |\n|---|---|---|---|\n")
    md += [f"| {a} | {b} | {c} | {d} |\n" for a, b, c, d in r]
    md.append("\n## Warnungen\n\n" + ("".join(f"- {w}\n" for w in warn) or "- keine\n"))
    md.append("\n## Annahmen (zu prüfen durch die Recherche)\n\n" + "".join(f"- `{k}` = {v}\n" for k, v in A.items()))
    md.append("\nNicht im Startsatz, weil nach Norm oder aus Rechnung: REQ-P09 (Zelltemperatur, Recherche), P11/P13/P14 (Normen), "
              "P12 (Kühlmittel, Vorschlag Wasser-Glykol), P15 (BMS-Umfang folgt aus Spannung und Zellzahl).\n")
    (ROOT / "docs" / f"startparameter{sfx}.md").write_text("".join(md))
    print("".join(md))


if __name__ == "__main__":
    main()
