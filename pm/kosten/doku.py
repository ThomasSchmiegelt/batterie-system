"""doku.py -- erzeugt docs/18_kosten.md und praesentation/bausteine/KO1.md aus ergebnis_<V>.json (KI-generiert, Claude Sonnet, 2026-11-18, Entwurf)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]; R = ROOT / "pm/kosten"
D = {v: json.loads((R / f"ergebnis_{v}.json").read_text()) for v in ("LFP", "NMC")}; EIN = json.loads((R / "eingaben.json").read_text())
N = {"BT-200": "Zellverbund", "BT-300": "BMS/Sensorik", "BT-400": "Verbinder/Leitung", "BT-500": "Gehäuse/Struktur", "BT-600": "Kühlung", "BT-700": "Schaltbox/Stecker"}
f = lambda x, n=0: f"{x:,.{n}f}".replace(",", "X").replace(".", ",").replace("X", ".")
pr = {v: D[v]["pruefung_erwartung"] for v in D}; zb = EIN["zielband"]
def band(v, k, x, einh): lo, hi = zb[v][k]; return f"{f(x, 1 if k=='eur_kwh' else 0)} {einh}: " + ("im Band" if lo <= x <= hi else "AUSSERHALB")
L = ["| Dok.-Nr. | BAT-DOC-18 | Version | 0.2 | Status | Entwurf |", "|---|---|---|---|---|---|", "| Titel | Kostenbewertung je Variante (REQ-P16, Vorgang KO1) | Ersteller | Claude Sonnet (KI), Auftrag Opus | Prüfer | Opus (offen) |", "",
"> **KI-generiert** (Claude Sonnet, 2026-11-18), Entwurf. Alle Preise sind **Annahmen** (ERW-KO1 inkl. Nachtrag 1, Opus). Belegt ist nur der Marktpreis W29.", "",
"## Ergebnis in einem Satz",
f"Nach Nachtrag 1 (Fertigung nur auf Nicht-Zell-Summe, Kühlplatte × 0,6, Längen BT-360/430 aus dem CAD) ergibt die **Teilsumme** (offene Positionen fehlen, also **untere Schranke**) für LFP {f(D['LFP']['summe_eur_pack'])} € je Pack ({f(D['LFP']['summe_eur_je_kWh'],1)} €/kWh) und für NMC {f(D['NMC']['summe_eur_pack'])} € ({f(D['NMC']['summe_eur_je_kWh'],1)} €/kWh).", "",
"## Zahlen (Quelle: `pm/kosten/ergebnis_LFP.json`, `pm/kosten/ergebnis_NMC.json`)", "| | LFP | NMC |", "|---|---|---|",
f"| Energie (kWh) | {f(D['LFP']['energie_kWh'],2)} | {f(D['NMC']['energie_kWh'],2)} |", f"| Teilsumme Pack (€) | {f(D['LFP']['summe_eur_pack'])} | {f(D['NMC']['summe_eur_pack'])} |",
f"| €/kWh | {f(D['LFP']['summe_eur_je_kWh'],1)} | {f(D['NMC']['summe_eur_je_kWh'],1)} |",
f"| Zellkosten (€) / Zellanteil | {f(D['LFP']['zellkosten_eur'])} / {f(pr['LFP']['zellanteil_pct'],1)} % | {f(D['NMC']['zellkosten_eur'])} / {f(pr['NMC']['zellanteil_pct'],1)} % |"]
for k, n in N.items(): L.append(f"| {k} {n} (€ / Anteil) | " + " | ".join(f"{f(D[v]['je_baugruppe'][k]['eur_pack'])} / {f(D[v]['je_baugruppe'][k]['anteil_an_teilsumme_pct'],1)} %" for v in D) + " |")
L += ["| Fertigung (€ / Anteil) | " + " | ".join(f"{f(D[v]['fertigung']['eur_pack'])} / {f(D[v]['fertigung']['anteil_an_teilsumme_pct'],1)} %" for v in D) + " |",
"| Offene Positionen | " + " | ".join(str(D[v]["positionen_offen_gesamt"]) for v in D) + " |",
"| Zellpreis -20 % / +20 % → Pack | " + " | ".join(f"{f(D[v]['empfindlichkeit']['zellpreis_x0.8']['aenderung_pct'],1)} % / +{f(D[v]['empfindlichkeit']['zellpreis_x1.2']['aenderung_pct'],1)} %" for v in D) + " |",
f"| Abstand zum Beleg {f(EIN['beleg_packpreis']['eur_je_kWh_berechnet'],1)} €/kWh | " + " | ".join(f"{f(pr[v]['abstand_beleg_eur_kwh'],1)} €/kWh" for v in D) + " |", "",
"Beleg: 97 USD/kWh BEV-Packpreis 2024 (BNEF, `forschung/ergebnis/W29.md`), Kurs 0,92 (Annahme). Der Beleg ist ein **Preis**, hier gerechnet sind **Herstellkosten** ohne Gemeinkosten und Marge; Vergleich nur als Größenordnung.", "",
"## Abgleich mit der Erwartung (`pm/kosten/ERWARTUNG.md`, Nachtrag 1)", "| Erwartung | LFP | NMC |", "|---|---|---|",
"| Pack LFP 5 500–7 000 € / NMC 7 000–9 000 € | " + " | ".join(band(v, "pack_eur", D[v]["summe_eur_pack"], "€") for v in D) + " |",
"| €/kWh LFP 75–95 / NMC 95–120 | " + " | ".join(band(v, "eur_kwh", D[v]["summe_eur_je_kWh"], "€/kWh") for v in D) + " |",
"| Nachtrag 1: LFP ≈ 5 800 € / 79 €/kWh / 63 %, NMC ≈ 7 900 € / 106 €/kWh / 70 % | " + f"{f(D['LFP']['summe_eur_pack'])} € / {f(D['LFP']['summe_eur_je_kWh'],1)} / {f(pr['LFP']['zellanteil_pct'],1)} % | {f(D['NMC']['summe_eur_pack'])} € / {f(D['NMC']['summe_eur_je_kWh'],1)} / {f(pr['NMC']['zellanteil_pct'],1)} % |",
"| Zellanteil 65–80 % (Verfehlt < 60 % oder > 85 %) | " + " | ".join(f"{f(pr[v]['zellanteil_pct'],1)} %: " + ("im Band" if pr[v]['zellanteil_im_band'] else ("VERFEHLT" if pr[v]['zellanteil_verfehlt_schwelle'] else "unter dem Band 65 %, Verfehlt-Schwelle nicht erreicht")) for v in D) + " |",
"| keine Nicht-Zell-Position > 10 % | " + " | ".join(f"größte BT-610 {f(pr[v]['groesste_nichtzellpositionen_pct'][0]['pct'],1)} %: " + ("erfüllt" if not pr[v]['nichtzellposition_ueber_10pct'] else "VERFEHLT") for v in D) + " |",
"| Zellpreis ±20 % → Pack ±13–16 % | " + " | ".join(f"±{f(abs(D[v]['empfindlichkeit']['zellpreis_x0.8']['aenderung_pct']),1)} %" for v in D) + " |", "",
"Gründe für Abweichungen nach unten bei Zellanteil/Pack: Teilsumme ohne offene Positionen (untere Schranke); deshalb liegt der Zellanteil real eher darunter, der Packpreis darüber. Deutung bleibt bei Opus.", "",
"## Preise je Position mit Status", "Status: nur der BNEF-Packpreis (W29) ist „verifiziert (W29, Zitat geprüft)“; alle Positionspreise sind „Schätzung (Annahme Opus, ERW-KO1)“. Quelle `pm/kosten/eingaben.json` (Spalte status) und `ergebnis_<V>.json`.", "",
"| BT | Preis | Einheit | Status | LFP € / Pack | NMC € / Pack |", "|---|---|---|---|---|---|"] + [
 f"| {bt} | {f(p['wert'],2) if not isinstance(p['wert'],dict) else 'LFP '+str(p['wert']['LFP'])+' / NMC '+str(p['wert']['NMC'])} | {p['einheit']} | {p['status']} | " + " | ".join((lambda es: f(sum(es),0) if es and all(e is not None for e in es) else "offen")([r['eur_ges'] for r in D[v]['positionen'] if r['bt']==bt]) if any(r['bt']==bt for r in D[v]['positionen']) else "–" for v in D) + " |"
 for bt, p in EIN["eur_je"].items()] + ["| Beleg Packpreis | 97 USD/kWh = " + f(EIN['beleg_packpreis']['eur_je_kWh_berechnet'],1) + " €/kWh | €/kWh | " + EIN['beleg_packpreis']['status'] + " | – | – |", "| Fertigung | 10 % Nicht-Zell + 50 €/Pack | – | " + EIN['fertigung']['status'] + " | " + " | ".join(f(D[v]['fertigung']['eur_pack']) for v in D) + " |", "",
 f"**Anteil an Schätzungen:** {f(D['LFP']['anteil_schaetzung_an_summe_pct'],1)} % der Summe (LFP) und {f(D['NMC']['anteil_schaetzung_an_summe_pct'],1)} % (NMC) beruhen auf Schätzungen (Annahme Opus, ERW-KO1); verifiziert ist keine Position, nur der Marktpreis-Beleg zum Vergleich.", "",
 "**Zielwert für REQ-P16:** keiner, bleibt offen (Autor). Das Zielband in den Bildern ist eine Erwartung (Schätzung), kein Zielwert.", "",
 "## Offene Positionen (untere Schranke, nicht als 0 gezählt; kein Abbruch nach Nachtrag 1)"]
for v in D:
    o = [r for r in D[v]["positionen"] if r["status"] == "offen"]
    L += ["", f"**{v} ({len(o)}):** " + "; ".join(f"{r['bt'] or 'Dichtungen'} {r['benennung'][:35]} ({r['grund_offen']})" for r in o)]
L += ["", "Hinweise: BT-760 Heizung und BT-660 Schnittstelle Preis 0 (Fahrzeug), nicht offen. BT-720 LFP ersetzt durch BT-721/722.", "",
"## Annahmen und Auslegungen",
"1. Fertigung: 10 % auf die Nicht-Zell-Summe + 50 € je Pack (Nachtrag 1).", "2. BT-610 Kühlplatte: Masse × 0,6 bis K2 eine Hohlmasse liefert (Nachtrag 1).",
"3. Längen aus `cad/pack/entwurf/ergebnis_<V>_e2d.json`: BT-360 FPC = Masse / `A_e2_fpc_masse_kg_m` (0,05 kg/m); BT-430 HV-Leitung = `e2.hv_laenge_gesamt_m` direkt (Stand Bericht 0.3, vorher aus dem Volumen).",
"4. BT-721/722 zusammen 15 €, BT-713 (55 €) und BT-730 (80 €) als Satz (von Opus bestätigt). BT-712 25 €/Stück bei Menge 2 (Auslegung). BT-210/240 mit Al 6 €/kg, Masse offen, ohne Wirkung.", "5. Kühlmittelvolumen BT-650 offen bis K2.", "",
"## Bilder (Zielband beschriftet, Lesehilfe im Bild)", "- `pm/kosten/kosten_LFP.png`, `kosten_NMC.png`, `kosten_vergleich.png`: gestapelter Balken €/kWh je Baugruppe, Zielband (schwarzer Rahmen), Beleg 89,2 €/kWh (rot).", "",
"## Dateien", "`pm/kosten/eingaben.json`, `kosten.py`, `bilder.py`, `doku.py`, `ergebnis_LFP.json`, `ergebnis_NMC.json`, `praesentation/bausteine/KO1.md`. Aufruf: `python3 pm/kosten/kosten.py && python3 pm/kosten/bilder.py && python3 pm/kosten/doku.py`.", "",
"*KI-generiert, Entwurf. Nicht freigegeben. BAT-DOC-18.*"]
(ROOT / "docs/18_kosten.md").write_text("\n".join(L) + "\n")
B = ["> **KI-generiert** (Claude Sonnet, 2026-11-18), Entwurf. Folienbaustein Vorgang KO1.", "", "# Kostenbewertung LFP gegen NMC (Annahmen, untere Schranke)",
f"**Kernaussage: Mit Annahmenpreisen liegt das Pack bei {f(D['LFP']['summe_eur_je_kWh'],1)} €/kWh (LFP) und {f(D['NMC']['summe_eur_je_kWh'],1)} €/kWh (NMC); die Zelle ist der größte Posten, offene Positionen machen die Werte zu Untergrenzen.**", "",
"**Bild:** pm/kosten/kosten_vergleich.png (Zielband ERW-KO1 beschriftet, Beleg W29 89,2 €/kWh)", "", "**Zahlen** (Quelle pm/kosten/ergebnis_LFP.json, ergebnis_NMC.json):",
f"- Teilsumme Pack: LFP {f(D['LFP']['summe_eur_pack'])} €, NMC {f(D['NMC']['summe_eur_pack'])} €", f"- Zellanteil: LFP {f(pr['LFP']['zellanteil_pct'],1)} %, NMC {f(pr['NMC']['zellanteil_pct'],1)} %",
f"- Offene Positionen: LFP {D['LFP']['positionen_offen_gesamt']}, NMC {D['NMC']['positionen_offen_gesamt']}", "- Beleg: 97 USD/kWh BEV-Pack 2024 (forschung/ergebnis/W29.md), Status: verifiziert (W29, Zitat geprüft)", "- Alle übrigen Preise: Status Schätzung (Annahme Opus, ERW-KO1); Anteil an der Summe LFP " + f(D["LFP"]["anteil_schaetzung_an_summe_pct"],1) + " %, NMC " + f(D["NMC"]["anteil_schaetzung_an_summe_pct"],1) + " %", "- Zielwert REQ-P16: keiner, offen (Autor)", "", "*KI-generiert, Entwurf.*"]
(ROOT / "praesentation/bausteine/KO1.md").write_text("\n".join(B) + "\n")
