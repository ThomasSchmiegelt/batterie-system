"""doku.py -- erzeugt docs/18_kosten.md, praesentation/bausteine/KO1.md und KO2.md aus ergebnis_<V>.json (KI-generiert, Claude Sonnet, 2026-11-18, KO2 2026-11-19, Entwurf)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]; R = ROOT / "pm/kosten"
D = {v: json.loads((R / f"ergebnis_{v}.json").read_text()) for v in ("LFP", "NMC")}; EIN = json.loads((R / "eingaben.json").read_text())
N = {"BT-200": "Zellverbund", "BT-300": "BMS/Sensorik", "BT-400": "Verbinder/Leitung", "BT-500": "Gehäuse/Struktur", "BT-600": "Kühlung", "BT-700": "Schaltbox/Stecker"}
f = lambda x, n=0: f"{x:,.{n}f}".replace(",", "X").replace(".", ",").replace("X", ".")
pr = {v: D[v]["pruefung_erwartung"] for v in D}; k2 = {v: D[v]["pruefung_ko2"] for v in D}
def jn(b): return "im Band" if b else "VERFEHLT (ausserhalb ±8 %)"
L = ["| Dok.-Nr. | BAT-DOC-18 | Version | 0.3 | Status | Entwurf |", "|---|---|---|---|---|---|", "| Titel | Kostenbewertung je Variante (REQ-P16, Vorgänge KO1, KO2) | Ersteller | Claude Sonnet (KI), Auftrag Opus | Prüfer | Opus (offen) |", "",
"> **KI-generiert** (Claude Sonnet, 2026-11-19), Entwurf. Alle Preise sind **Annahmen** (ERW-KO1/KO2, Opus) oder aus Distributorpreisen abgeleitet. Belegt ist nur der Marktpreis W29.", "",
"## Ergebnis in einem Satz",
f"Nach KO2 (Stückliste SL3.1, Blech-Kühlplatte mit echter Masse, Kühlkreis BT-661…665, Normteile, Serienfaktor f_serie {f(EIN['f_serie']['wert'],2)}) ergibt die **Teilsumme** (offene Positionen fehlen, also **untere Schranke**) für LFP {f(D['LFP']['summe_eur_pack'])} € je Pack ({f(D['LFP']['summe_eur_je_kWh'],1)} €/kWh, {jn(k2['LFP']['summe_im_band'])}) und für NMC {f(D['NMC']['summe_eur_pack'])} € ({f(D['NMC']['summe_eur_je_kWh'],1)} €/kWh, {jn(k2['NMC']['summe_im_band'])}).", "",
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
"## Abgleich mit der Erwartung KO2 (`pm/kosten/ERWARTUNG.md`, Nachtrag 2)", "| Erwartung (ERW-KO2) | LFP | NMC |", "|---|---|---|",
"| Pack (Erwartung; Band ±8 %) | " + " | ".join(f"{f(k2[v]['erwartung_pack_eur'])} € (Band {f(k2[v]['band_pack_eur'][0])}–{f(k2[v]['band_pack_eur'][1])}): {f(D[v]['summe_eur_pack'])} € ({f(k2[v]['abweichung_pack_pct'],1)} %), {jn(k2[v]['summe_im_band'])}" for v in D) + " |",
"| €/kWh (Erwartung; Band ±8 %) | " + " | ".join(f"{f(k2[v]['erwartung_eur_kwh'])} (Band {f(k2[v]['band_eur_kwh'][0],1)}–{f(k2[v]['band_eur_kwh'][1],1)}): {f(D[v]['summe_eur_je_kWh'],1)} ({f(k2[v]['abweichung_eur_kwh_pct'],1)} %)" for v in D) + " |",
"| Anteil verifiziert/abgeleitet < 1 % | " + " | ".join(f"{f(k2[v]['anteil_verifiziert_abgeleitet_pct'],2)} %: " + ("erfüllt" if k2[v]['anteil_verifiziert_abgeleitet_unter_grenze'] else "VERFEHLT") for v in D) + " |",
"| Position ohne Menge/Masse als „offen“ ausgewiesen | " + " | ".join(("erfüllt (alle offenen mit Grund)" if not k2[v]['offene_ohne_grund'] else "VERFEHLT " + ", ".join(k2[v]['offene_ohne_grund'])) for v in D) + " |", "",
"Frühere Prüfungen (ERW-KO1/Nachtrag 1, Zielband KO1 LFP 5 500–7 000 € / NMC 7 000–9 000 €): " + "; ".join(f"{v} Pack {'im Band' if pr[v]['summe_im_band'] else 'AUSSERHALB'}, Zellanteil {f(pr[v]['zellanteil_pct'],1)} % ({'im Band 65–80 %' if pr[v]['zellanteil_im_band'] else ('VERFEHLT (< 60 % oder > 85 %)' if pr[v]['zellanteil_verfehlt_schwelle'] else 'unter 65 %, Schwelle 60 % nicht unterschritten')}), größte Nicht-Zell-Position {pr[v]['groesste_nichtzellpositionen_pct'][0]['bt']} {f(pr[v]['groesste_nichtzellpositionen_pct'][0]['pct'],1)} %" for v in D) + ".", "",
"Deutung bleibt bei Opus. Die Teilsumme ist eine untere Schranke (offene Positionen fehlen).", "",
"## Status der Preise (3 Stufen)",
"Stufen: „verifiziert (Wxx/Datenblatt)“, „abgeleitet aus Distributorpreis“, „Schätzung (Annahme Opus)“. Quelle `pm/kosten/eingaben.json` und `ergebnis_<V>.json` (`eur_je_stufe`).", "",
"| Stufe | LFP € | LFP Anteil | NMC € | NMC Anteil |", "|---|---|---|---|---|"] + [
 f"| {s} | {f(D['LFP']['eur_je_stufe'][s],2)} | {f(D['LFP']['anteil_je_stufe_pct'][s],2)} % | {f(D['NMC']['eur_je_stufe'][s],2)} | {f(D['NMC']['anteil_je_stufe_pct'][s],2)} % |" for s in ("verifiziert", "abgeleitet", "Schätzung")] + ["",
 f"Abgeleitet sind: Schmelzsicherung Eaton EKC14-40 ({f(EIN['distributorpreise']['BT-713_Schmelzsicherung']['preis_menge1_eur'],2)} € Menge 1 × f_serie {f(EIN['f_serie']['wert'],2)} = {f(EIN['eur_je']['BT-713']['teile'][1]['wert'],2)} €, Teil des BT-713-Satzes) und NTC Vishay NTCS0603E3 ({f(EIN['distributorpreise']['BT-330_NTC']['preis_menge1_eur'],2)} € × f_serie = {f(EIN['eur_je']['BT-330']['wert'],2)} €). f_serie ist selbst eine Schätzung (Annahme Opus). Arcol HS50 wird nicht verwendet (gehört nicht zum gewählten Vishay RH050). Der Marktpreis W29 ist ein Beleg zum Vergleich, keine Position; **verifiziert** ist keine Position.", "",
 "**Zielwert für REQ-P16:** keiner, bleibt offen (Autor). Das Zielband in den Bildern ist eine Erwartung (Schätzung), kein Zielwert.", "",
 "## Preise je Eintrag", "| Schlüssel | Preis | Einheit | Status | wert_ko1 | LFP € / Pack | NMC € / Pack |", "|---|---|---|---|---|---|---|"] + [
 f"| {k} | " + ("entfällt" if p['wert'] is None else (f(p['wert'],2) if not isinstance(p['wert'],dict) else 'LFP '+str(p['wert']['LFP'])+' / NMC '+str(p['wert']['NMC']))) + f" | {p['einheit']} | {p['status']} | " + (str(p['wert_ko1']) if 'wert_ko1' in p and not isinstance(p['wert_ko1'], dict) else ('LFP '+str(p['wert_ko1']['LFP'])+' / NMC '+str(p['wert_ko1']['NMC']) if 'wert_ko1' in p else '–')) + " | " + " | ".join((lambda es: f(sum(es),2) if es and all(e is not None for e in es) else "offen")([r['eur_ges'] for r in D[v]['positionen'] if r['preis_schluessel']==k]) if any(r['preis_schluessel']==k for r in D[v]['positionen']) else "–" for v in D) + " |"
 for k, p in EIN["eur_je"].items()] + ["| Beleg Packpreis | 97 USD/kWh = " + f(EIN['beleg_packpreis']['eur_je_kWh_berechnet'],1) + " €/kWh | €/kWh | " + EIN['beleg_packpreis']['status'] + " | – | – | – |", "| Fertigung | 10 % Nicht-Zell + 50 €/Pack | – | " + EIN['fertigung']['status'] + " | – | " + " | ".join(f(D[v]['fertigung']['eur_pack']) for v in D) + " |", "",
 "## Offene Positionen (untere Schranke, nicht als 0 gezählt)"]
for v in D:
    o = [r for r in D[v]["positionen"] if r["status"] == "offen"]
    L += ["", f"**{v} ({len(o)}):** " + "; ".join(f"{r['pos']} {r['bt'] or 'Dichtungen'} {r['benennung'][:35]} ({r['grund_offen']})" for r in o)]
L += ["", "Entfallen (0 €, nicht offen): BT-240 Verspannung, BT-660 (ersetzt durch BT-661…665); BT-720 LFP ersetzt durch BT-721/722 (Positionszuordnung `pos_zu_preis`).", "",
"## Annahmen und Auslegungen",
"1. Fertigung: 10 % auf die Nicht-Zell-Summe + 50 € je Pack (Nachtrag 1).", f"2. BT-610 Kühlplatte: 12 €/kg × Blechmasse aus K2b (Blech 1/4/1, ENT-152…156); der Faktor 0,6 entfällt (ERW-KO2 Punkt 4). Bis G5.7 steht die K2b-Masse in der Stückliste.",
"3. Längen aus `cad/pack/entwurf/ergebnis_<V>_e2d.json`: BT-360 FPC = Masse / `A_e2_fpc_masse_kg_m`; BT-430 HV-Leitung = `e2.hv_laenge_gesamt_m`. Die Länge gilt nur für die Position 300.6 bzw. 400.3; die Positionen 360.3 und 360.4 (FPC-Detail, Daisy-Chain) erhalten keinen Längenpreis und sind offen (in KO1 wurde die FPC-Länge dreifach gezählt, siehe Hinweis in `eingaben.json laengen_aus_cad`).",
f"4. BT-721/722 zusammen 15 €, BT-713 als Satz ({f(EIN['eur_je']['BT-713']['wert'],2)} €), BT-730 als Satz (80 €). BT-712 25 €/Stück bei Menge 2 (Auslegung). BT-210 ist eine Anordnung ohne Masse und bleibt offen.", "5. Kühlmittelvolumen BT-650 offen; Masse BT-620 offen bis G5-CAD.",
"6. Massen BT-510…550, 620, 630 und Schläuche 660.4 sind bis zur Gesamtmontage (G5.7) die Obergrenzen aus e2d bzw. offen; nach `stueckliste_v3.py --aus-cad` ersetzt die CAD-Masse sie.", "",
"## Bilder (Zielband beschriftet, Lesehilfe im Bild)", "- `pm/kosten/kosten_LFP.png`, `kosten_NMC.png`, `kosten_vergleich.png`: gestapelter Balken €/kWh je Baugruppe, Zielband ERW-KO2 ±8 % (schwarzer Rahmen), Beleg 89,2 €/kWh (rot).", "",
"## Dateien und Neulauf", "`pm/kosten/eingaben.json`, `preisregeln.py`, `kosten.py`, `bilder.py`, `doku.py`, `ergebnis_LFP.json`, `ergebnis_NMC.json`, `praesentation/bausteine/KO1.md`, `KO2.md`.",
"Neulauf nach der Gesamtmontage: `python3 pm/bauteile/stueckliste_v3.py --aus-cad && python3 pm/kosten/kosten.py && python3 pm/kosten/bilder.py && python3 pm/kosten/doku.py`.", "",
"*KI-generiert, Entwurf. Nicht freigegeben. BAT-DOC-18.*"]
(ROOT / "docs/18_kosten.md").write_text("\n".join(L) + "\n")
B = ["> **KI-generiert** (Claude Sonnet, 2026-11-19), Entwurf. Folienbaustein Vorgang KO2 (ersetzt KO1).", "", "# Kosten LFP gegen NMC nach Stückliste SL3.1 (Annahmen, untere Schranke)",
f"**Kernaussage: Mit Annahmenpreisen liegt das Pack bei {f(D['LFP']['summe_eur_je_kWh'],1)} €/kWh (LFP) und {f(D['NMC']['summe_eur_je_kWh'],1)} €/kWh (NMC); die Zelle bleibt der größte Posten, weniger als {f(max(k2[v]['anteil_verifiziert_abgeleitet_pct'] for v in D),1)} % der Summe sind belegt oder abgeleitet.**", "",
"**Bild:** pm/kosten/kosten_vergleich.png (Zielband ERW-KO2 ±8 % beschriftet, Beleg W29 89,2 €/kWh)", "", "**Zahlen** (Quelle pm/kosten/ergebnis_LFP.json, ergebnis_NMC.json):",
f"- Teilsumme Pack: LFP {f(D['LFP']['summe_eur_pack'])} € ({jn(k2['LFP']['summe_im_band'])}), NMC {f(D['NMC']['summe_eur_pack'])} € ({jn(k2['NMC']['summe_im_band'])})", f"- Zellanteil: LFP {f(pr['LFP']['zellanteil_pct'],1)} %, NMC {f(pr['NMC']['zellanteil_pct'],1)} %",
f"- Offene Positionen: LFP {D['LFP']['positionen_offen_gesamt']}, NMC {D['NMC']['positionen_offen_gesamt']}",
f"- Status der Summe: verifiziert {f(D['LFP']['anteil_verifiziert_an_summe_pct'],2)} / {f(D['NMC']['anteil_verifiziert_an_summe_pct'],2)} %, abgeleitet {f(D['LFP']['anteil_abgeleitet_an_summe_pct'],2)} / {f(D['NMC']['anteil_abgeleitet_an_summe_pct'],2)} %, Schätzung {f(D['LFP']['anteil_schaetzung_an_summe_pct'],1)} / {f(D['NMC']['anteil_schaetzung_an_summe_pct'],1)} % (LFP / NMC)",
"- Beleg: 97 USD/kWh BEV-Pack 2024 (forschung/ergebnis/W29.md), Status: verifiziert (W29, Zitat geprüft)", "- Zielwert REQ-P16: keiner, offen (Autor)", "", "*KI-generiert, Entwurf.*"]
(ROOT / "praesentation/bausteine/KO2.md").write_text("\n".join(B) + "\n")
