---
typ: dokument
nr: "BAT-DOC-19"
version: "0.1"
status: "Entwurf"
tags: ["dokument"]
---
# BAT-DOC-19 – Freigaberunde (Sammelliste)

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

- Datei: `docs/19_freigaberunde`
- Version: 0.1
- Status: Entwurf
- Typ: Projektdokument (Dokumentenlenkung [[Dokument/00_dokumentenlenkung]])

## Genannte Anforderungen (Textvorkommen)
- [[Anforderung/REQ-G01|REQ-G01]]
- [[Anforderung/REQ-G02|REQ-G02]]
- [[Anforderung/REQ-P02|REQ-P02]]
- [[Anforderung/REQ-P03|REQ-P03]]
- [[Anforderung/REQ-P04|REQ-P04]]
- [[Anforderung/REQ-P07|REQ-P07]]
- [[Anforderung/REQ-P08|REQ-P08]]
- [[Anforderung/REQ-P09|REQ-P09]]
- [[Anforderung/REQ-P10|REQ-P10]]
- [[Anforderung/REQ-P11|REQ-P11]]
- [[Anforderung/REQ-P12|REQ-P12]]
- [[Anforderung/REQ-P13|REQ-P13]]
- [[Anforderung/REQ-P14|REQ-P14]]
- [[Anforderung/REQ-P15|REQ-P15]]

## Genannte Entscheidungen, Befunde, Bauteile (Textvorkommen)
- [[Bauteil/BT-000|BT-000]]
- [[Bauteil/BT-132|BT-132]]
- [[Bauteil/BT-140|BT-140]]
- [[Bauteil/BT-310|BT-310]]
- [[Bauteil/BT-320|BT-320]]
- [[Bauteil/BT-330|BT-330]]
- [[Bauteil/BT-350|BT-350]]
- [[Bauteil/BT-610|BT-610]]
- [[Bauteil/BT-710|BT-710]]
- [[Bauteil/BT-712|BT-712]]
- [[Entscheidung/ENT-006|ENT-006]]
- [[Entscheidung/ENT-013|ENT-013]]
- [[Entscheidung/ENT-104|ENT-104]]
- [[Entscheidung/ENT-105|ENT-105]]
- [[Entscheidung/ENT-106|ENT-106]]
- [[Entscheidung/ENT-109|ENT-109]]
- [[Entscheidung/ENT-144|ENT-144]]
- [[Entscheidung/ENT-147|ENT-147]]
- [[Entscheidung/ENT-151|ENT-151]]
- [[Entscheidung/ENT-152|ENT-152]]
- [[Entscheidung/ENT-153|ENT-153]]
- [[Entscheidung/ENT-154|ENT-154]]
- [[Entscheidung/ENT-155|ENT-155]]
- [[Entscheidung/ENT-158|ENT-158]]
- [[Entscheidung/ENT-159|ENT-159]]

## Vorgänge, die dieses Dokument nennen
- –

## Inhalt (Kopie aus `docs/19_freigaberunde.md`)

| Dok.-Nr. | BAT-DOC-19 | Version | 0.1 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Freigaberunde (Sammelliste) | Ersteller | Claude Sonnet (KI), pm.py freigabe | Prüfer | – (Mensch offen) |

> **KI-generiert.** Entwurf, nicht vom Menschen freigegeben. Erzeugt am 2026-11-23 von `python3 pm/pm.py freigabe`, nicht von Hand bearbeiten (Antworten in der Spalte „Autor“ gehören in die Quelle: Akte, `pm/anforderungen.json`, `annahmen*.json`). Konzept: `docs/17_workflow_schleife.md` §4.

Zählung: 5 offene Akten, 31 Kriterien ohne Herkunft Autor oder Anforderungen mit Lücke, 215 Annahmen A_* ohne Akte. Akten mit Status „ersetzt“ sind nicht aufgeführt. Als „ohne Akte“ gilt eine Annahme, deren Schlüsselname in keiner `pm/entscheidungen/ENT-*.md` vorkommt.

## 1 Offene Akten (Status nicht „entschieden…“)

| ID | Frage | Vorschlag | Autor: ja/nein/ändern |
|---|---|---|---|
| ENT-104 | Kühlplatte: Kanalbreite 4 mm (BT BT-610, Status ersetzt durch ENT-153) | Wert 4.0 mm laut Akte | |
| ENT-105 | Kühlplatte: Kanalhöhe 5 mm (BT BT-610, Status ersetzt durch ENT-154) | Wert 5.0 mm laut Akte | |
| ENT-106 | Kühlplatte: Werkstoff Al, gelötete Platte mit parallelen Kanälen quer (BT BT-610, Status ersetzt durch ENT-155) | Wert "Al, gelötet, parallele Kanäle quer, 1 Durchgang" laut Akte | |
| ENT-109 | Schaltbox auf dem Deckel vorne (Fall b), beide Varianten (BT BT-710, Status ersetzt durch ENT-144) | Wert deckel_vorne laut Akte | |
| ENT-147 | Bauraumlänge LFP 2050 mm (CMU hochkant in beiden Endzonen, je +10 mm) (BT BT-000, Status vorgeschlagen) | Wert 2050.0 mm laut Akte | |

## 2 Kriterien ohne Herkunft „Autor“ (je Kriterium eine Zeile) und Anforderungen mit fehlendem Pflichtfeld

| ID | Frage | Vorschlag | Autor: ja/nein/ändern |
|---|---|---|---|
| REQ-P02 / E_brutto-LFP | nutzbarer Energieinhalt: Kriterium E_brutto LFP >= Startwert aus pm/startwerte_LFP.json :: abgeleitet.kWh_brutto kWh, Herkunft Startwert (Vorschlag) | Kriterium so übernehmen | |
| REQ-P02 / E_brutto-NMC | nutzbarer Energieinhalt: Kriterium E_brutto NMC >= Startwert aus pm/startwerte_NMC.json :: abgeleitet.kWh_brutto kWh, Herkunft Startwert (Vorschlag) | Kriterium so übernehmen | |
| REQ-P03 / U_nenn | Systemspannung (Nenn, min, max): Kriterium U_nenn zwischen [720, 880] V, Herkunft Autor (Freigaberunde 2026-11-23) (Autor: 800 V nominal (ENT-006); Band ±10 % ist Annahme Opus) | Kriterium so übernehmen | |
| REQ-P03 / U_min | Systemspannung (Nenn, min, max): Kriterium U_min vorhanden, Herkunft Autor (Freigaberunde 2026-11-23) | Kriterium so übernehmen | |
| REQ-P03 / U_max | Systemspannung (Nenn, min, max): Kriterium U_max vorhanden, Herkunft Autor (Freigaberunde 2026-11-23) | Kriterium so übernehmen | |
| REQ-P04 / P_spitze | Dauer- und Spitzenleistung Entladen: Kriterium P_spitze >= Startwert aus pm/startwerte.json :: fahrzeug_tabelle.p_spitze kW, Herkunft Autor (Freigaberunde 2026-11-23) (10 s) | Kriterium so übernehmen | |
| REQ-P04 / P_dauer | Dauer- und Spitzenleistung Entladen: Kriterium P_dauer >= 60 kW, Herkunft Autor (Freigaberunde 2026-11-23) (Annahme Opus; startwerte.json nennt dauer_zu_spitze 0,4 (Annahme)) | Kriterium so übernehmen | |
| REQ-P07 / B | Bauraum (L × B × H) und Masse: Kriterium B <= 1430 mm, Herkunft Autor (Freigaberunde 2026-11-23) | Kriterium so übernehmen | |
| REQ-P07 / L | Bauraum (L × B × H) und Masse: Kriterium L <= 2400 mm, Herkunft Autor (Freigaberunde 2026-11-23) (Freigaberunde 2026-11-23 Runde 1: L ≤ 2400 mm (Radstand Kompaktwagen etwa 2,6–2,7 m, Annahme); ersetzt 1950 (ENT-013)) | Kriterium so übernehmen | |
| REQ-P07 / H | Bauraum (L × B × H) und Masse: Kriterium H <= 130 mm, Herkunft Autor (Freigaberunde 2026-11-23) (H ≤ 130 mm im Zellbereich (Runde 1)) | Kriterium so übernehmen | |
| REQ-P07 / H_dom | Bauraum (L × B × H) und Masse: Kriterium H_dom <= 250 mm, Herkunft Autor (Freigaberunde 2026-11-23) (Dom Schaltbox bis 250 mm (Runde 1)) | Kriterium so übernehmen | |
| REQ-P07 / Masse-LFP | Bauraum (L × B × H) und Masse: Kriterium Masse LFP <= Startwert aus pm/startwerte_LFP.json :: abgeleitet.masse_kg kg, Herkunft Autor (Freigaberunde 2026-11-23) (Startwerte als Ziel (Runde 1): LFP ≤ 528 kg, NMC ≤ 370 kg; beide aktuell verfehlt, Leichtbauziel Schleife 2) | Kriterium so übernehmen | |
| REQ-P07 / Masse-NMC | Bauraum (L × B × H) und Masse: Kriterium Masse NMC <= Startwert aus pm/startwerte_NMC.json :: abgeleitet.masse_kg kg, Herkunft Autor (Freigaberunde 2026-11-23) (Startwerte als Ziel (Runde 1): LFP ≤ 528 kg, NMC ≤ 370 kg; beide aktuell verfehlt, Leichtbauziel Schleife 2) | Kriterium so übernehmen | |
| REQ-P08 / T_betrieb | Umgebungstemperatur Betrieb und Laden: Kriterium T_betrieb zwischen [-20, 45] °C, Herkunft Autor (Freigaberunde 2026-11-23) | Kriterium so übernehmen | |
| REQ-P08 / T_laden | Umgebungstemperatur Betrieb und Laden: Kriterium T_laden zwischen [0, 45] °C, Herkunft Autor (Freigaberunde 2026-11-23) | Kriterium so übernehmen | |
| REQ-P09 / T_max | max. Zelltemperatur und Spreizung zwischen den Zellen: Kriterium T_max <= 45 °C, Herkunft Autor (Freigaberunde 2026-11-23) | Kriterium so übernehmen | |
| REQ-P09 / Spreizung | max. Zelltemperatur und Spreizung zwischen den Zellen: Kriterium Spreizung <= 5 K, Herkunft Autor (Freigaberunde 2026-11-23) | Kriterium so übernehmen | |
| REQ-P10 / SOH | Lebensdauer (Zyklen, Jahre, Restkapazität): Kriterium SOH >= 70 %, Herkunft Autor (Freigaberunde 2026-11-23) (Laufleistung: Startwert (Vorschlag); 70 %: Annahme Opus) | Kriterium so übernehmen | |
| REQ-P11 / t_warnung | Sicherheit: keine Ausbreitung des thermischen Durchgehens bzw. Warnzeit nach Norm: Kriterium t_warnung >= 5 min, Herkunft Norm (W35d belegt: UN R100 42024X1955, Warnung 5 min vor gefährlicher Situation im Fahrgastraum) (FMVSS 305a (W40b) misst anders: Warnung innerhalb 3 min nach Beginn des Ereignisses; beide ausweisen) | Kriterium so übernehmen | |
| REQ-P12 / Kuehlmittel | Kühlmittel und Anschlüsse: Kriterium Kuehlmittel vorhanden, Herkunft Autor (Freigaberunde 2026-11-23) | Kriterium so übernehmen | |
| REQ-P12 / dp_Platte | Kühlmittel und Anschlüsse: Kriterium dp_Platte <= 0.5 bar, Herkunft Autor (Freigaberunde 2026-11-23) | Kriterium so übernehmen | |
| REQ-P12 / Verteilung_abw | Kühlmittel und Anschlüsse: Kriterium Verteilung_abw <= 10 %, Herkunft Autor (Freigaberunde 2026-11-23) (±10 % aus ENT-159 (entschieden, Mensch)) | Kriterium so übernehmen | |
| REQ-P13 / R_iso | Schutzart, Isolation, Berührschutz: Kriterium R_iso >= 100 Ω/V, Herkunft Autor (Freigaberunde 2026-11-23) (DC) | Kriterium so übernehmen | |
| REQ-P13 / Schutzart | Schutzart, Isolation, Berührschutz: Kriterium Schutzart == IP67, Herkunft Autor (Freigaberunde 2026-11-23) | Kriterium so übernehmen | |
| REQ-P14 / dy_a | Mechanik: Stoß, Schwingung, Crash: Kriterium dy_a <= 0.5 mm, Herkunft Autor (Freigaberunde 2026-11-23) (Kontaktspalt KONTAKT_B der Auswertung; Lastfälle zu belegen W35/W36) | Kriterium so übernehmen | |
| REQ-P14 / dy_b | Mechanik: Stoß, Schwingung, Crash: Kriterium dy_b <= 0.5 mm, Herkunft Autor (Freigaberunde 2026-11-23) (Kriterium Zellverschiebung ist Annahme Opus; R100 prüft nach Quetschung auf Feuer, Explosion, Elektrolytaustritt, Isolation (strengere Annahme)) | Kriterium so übernehmen | |
| REQ-P15 / CMU | Messung und BMS: Zellspannung, Temperatur, Isolationswächter: Kriterium CMU vorhanden, Herkunft Autor (Freigaberunde 2026-11-23) (Zellspannung je Reihe (BT-320)) | Kriterium so übernehmen | |
| REQ-P15 / Temperaturfuehler | Messung und BMS: Zellspannung, Temperatur, Isolationswächter: Kriterium Temperaturfuehler vorhanden, Herkunft Autor (Freigaberunde 2026-11-23) (BT-330) | Kriterium so übernehmen | |
| REQ-P15 / Isolationswaechter | Messung und BMS: Zellspannung, Temperatur, Isolationswächter: Kriterium Isolationswaechter vorhanden, Herkunft Autor (Freigaberunde 2026-11-23) (BT-350) | Kriterium so übernehmen | |
| REQ-G01 / Anwendbarkeit_belegt | Maschinenrichtlinie (EU 2023/1230): Kriterium Anwendbarkeit_belegt vorhanden, Herkunft Norm (W37c.nachtrag belegt: VO 2023/1230 Art. 2 Abs. 2 g) („nicht anwendbar“ belegt: W37 liegt als Rechercheergebnis vor, Aussage muss Opus prüfen und Nachweis dann verknüpfen) | Kriterium so übernehmen | |
| REQ-G02 / Batteriepass_Datensatz | Kennzeichnung, CO₂-Fußabdruck und Batteriepass nach VO (EU) 2023/1542: Kriterium Batteriepass_Datensatz vorhanden, Herkunft Autor (Freigaberunde 2026-11-23) | Kriterium so übernehmen | |

## 3 Annahmen A_* ohne Akte

| ID | Frage (Wert und Herkunft) | Vorschlag | Autor: ja/nein/ändern |
|---|---|---|---|
| A_KUEHLPLATTE_FUELLGRAD | Wert 0.4 -, Herkunft: Annahme Opus 2026-11-17: 2 Bleche je 1,5 mm + Kanalstege, Füllgrad 0,4 (Masse = Volumen x Füllgrad x Al-Dichte) (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_alu_dichte_kg_m3 | Wert 2700 kg/m3, Herkunft: M0 eingaben.json (Annahme) (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_boden_mm | Wert 3 mm, Herkunft: M0 eingaben.json hoehenstapel_mm.boden (Annahme) (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_deckel_mm | Wert 2 mm, Herkunft: M0 eingaben.json hoehenstapel_mm.deckel (Annahme) (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_dichte_pad_kg_m3 | Wert 2500 kg/m3, Herkunft: Annahme Opus 2026-11-17 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_dichte_verguss_kg_m3 | Wert 300 kg/m3, Herkunft: Annahme Opus 2026-11-17 (PU-Schaum) (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_dichte_zelltraeger_kg_m3 | Wert 1200 kg/m3, Herkunft: Annahme Opus 2026-11-17 (PC) (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2_bms_masse_kg | Wert 0.4 kg, Herkunft: ERW-E2 N1 BMS-Platine (Maße aus Akte BT-310) (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2_box_hoehe_max_mm | Wert 90 mm, Herkunft: ERW-E2 N1 H ≤ 90 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2_box_rand_mm | Wert 15 mm, Herkunft: ERW-E2 N1 Rand 15 mm um den Inhalt (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2_box_teilabstand_mm | Wert 10 mm, Herkunft: NEUE ANNAHME (Platzhalter, in ERW-E2 N1 nicht gesetzt; Opus entscheiden): Abstand zwischen den Teilen in der Schaltbox (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2_box_wand_mm | Wert 2 mm, Herkunft: ERW-E2 N1 Schaltbox Al, Wand 2 mm (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2_bruecke_luecke_mm | Wert 30 mm, Herkunft: ERW-E2 N3 (Platzhalter Opus/Sonnet): Lücke im Querverbinder LFP für die Service-Trennbrücke (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2_bruecke_querschnitt_mm | Wert [25, 3] mm, Herkunft: ERW-E2 N3: Cu-Brücke 25 x 3, 2 x M8 (je Seite eine Schraube), HV-Interlock-Kontakt nicht modelliert (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2_bruecke_ueberlappung_mm | Wert 25 mm, Herkunft: ERW-E2 N3: Überlappung Brücke auf Querverbinder je Seite (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2_cmu_masse_kg | Wert 0.08 kg, Herkunft: ERW-E2 N1 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2_cmu_mm | Wert [120, 60, 10] mm, Herkunft: ERW-E2 N1 CMU-Platine (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2_fpc_dicke_mm | Wert 0.3 mm, Herkunft: ERW-E2 N1 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2_fpc_halter_mm | Wert 3.0 mm, Herkunft: ERW-E2 N1 (FPC plus Halter) (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2_fpc_masse_kg_m | Wert 0.05 kg/m, Herkunft: ERW-E2 N1 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2_gas_masse_kg | Wert 0.015 kg, Herkunft: KI-generiert (Claude Sonnet, 2026-11-20), Auftrag DB2. Datenblatt BT-770_amphenol_SGX_TRDU5.pdf S. 3 'Weight < 15 g' (Wert im PDF-Text geprüft: ja). OBERGRENZE, keine Messmasse (annahmen_datenblatt.json) | Wert beibehalten und Akte anlegen | |
| A_e2_gas_mm | Wert [39, 35, 27] mm, Herkunft: Datenblatt (forschung/datenblaetter.md, quellen/datenblaetter/BT-770_amphenol_SGX_TRDU5.pdf S. 3): Amphenol SGX TRDU5 39 × 35 × 27, < 15 g (Opus: im PDF-Text bestätigt) (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_e2_hv250_masse_kg | Wert 0.4 kg, Herkunft: ERW-E2 N1 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2_hv250_mm | Wert [90, 70, 60] mm, Herkunft: ERW-E2 N1 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2_hv40_masse_kg | Wert 0.15 kg, Herkunft: ERW-E2 N1 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2_hv40_mm | Wert [45.4, 40.6, 49] mm, Herkunft: KI-generiert (Claude Sonnet, 2026-11-20), Auftrag DB2. Datenblatt BT-730_te_HVA280_header_1-2103124-1.pdf S. 2 (Händlerblatt: Product Length 45,4, Width 40,6, Connector Height 49; Wert im PDF-Text geprüft: ja; ohne Zeichnung, Ausrichtung L/B/H angenommen, Gehäuse 2-polig) (annahmen_datenblatt.json) | Wert beibehalten und Akte anlegen | |
| A_e2_hv_aussendurchmesser_LFP_mm | Wert 14 mm, Herkunft: ERW-E2 N1 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2_hv_aussendurchmesser_NMC_mm | Wert 12 mm, Herkunft: ERW-E2 N1 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2_lasche_bohrung_mm | Wert 8 mm, Herkunft: ERW-E2 N3: Bohrung M8 (Nennmaß 8, Durchgangsloch nicht gesetzt) (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2_lasche_mm | Wert [25, 3] mm, Herkunft: ERW-E2 N3: Anschlusslasche Querschnitt wie Verbinder 25 x 3, Überlappung 25 mm, Bohrung M8 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2_lasche_ueberlappung_mm | Wert 25 mm, Herkunft: ERW-E2 N3 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2_nv_masse_kg | Wert 0.05 kg, Herkunft: ERW-E2 N1 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2_nv_mm | Wert [50, 30, 40] mm, Herkunft: ERW-E2 N1 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2_pyro_masse_kg | Wert 0.23 kg, Herkunft: KI-generiert (Claude Sonnet, 2026-11-20), Auftrag DB2. Datenblatt BT-713_sensata_pyrofuse.pdf S. 1 'Total weight: 230g' (Wert im PDF-Text geprüft: ja; PDF-Text nennt ±34,85 %, datenblaetter.md nannte ±5 %) (annahmen_datenblatt.json) | Wert beibehalten und Akte anlegen | |
| A_e2_pyro_mm | Wert [90, 44, 75] mm, Herkunft: Datenblatt (forschung/datenblaetter.md, quellen/datenblaetter/BT-713_sensata_pyrofuse.pdf): Sensata PyroFuse STPS500 90 × 44 × 75 (Opus: Zeichnung nur als Bild, Wert nicht textlich geprüft) (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_e2_schmelz_masse_kg | Wert 0.1 kg, Herkunft: ERW-E2 N1 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2_schmelz_mm | Wert [30, 30, 85] mm, Herkunft: ERW-E2 N1 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2_schuetz_masse_kg | Wert 0.4 kg, Herkunft: Datenblatt BT-711_glvac_GLFX250.pdf S. 1: Unit weight approx. 400 g je Schütz (Opus im PDF-Text geprüft; 0,8 kg war die Summe für 2) (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_e2_schuetz_mm | Wert [86, 42.5, 74.5] mm, Herkunft: Datenblatt (forschung/datenblaetter.md, quellen/datenblaetter/BT-711_glvac_GLFX250.pdf S. 6): GLVAC GLFX250, 250 A, 800 V (S. 2); L × B × H, Bolzen oben. Opus-Wahl statt Gigavac GX14 (114,8 × 59,8 × 57,3), weil kleiner und 250 A reichen (E1 LFP Spitze 240 A) (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_e2_serviceoeffnung_mm | Wert [120, 80] mm, Herkunft: ERW-E2 N3: Öffnung 120 (y) x 80 (x) durch Pad, obere Kühlplatte, Deckel; Servicedeckel flach, bündig, Dicke = A_deckel_mm (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2_shunt_masse_kg | Wert 0.1 kg, Herkunft: ERW-E2 N1 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2_shunt_mm | Wert [84, 83.2, 15.2] mm, Herkunft: Datenblatt (forschung/datenblaetter.md, quellen/datenblaetter/BT-340_isabellenhuette_IVT-S.pdf): Isabellenhütte IVT-S 83,2 × 84 × 15,2 (Opus: Zeichnung nur als Bild) (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_e2_trennstecker_masse_kg | Wert 0.2 kg, Herkunft: ERW-E2 N1 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2_trennstecker_mm | Wert [80, 50, 60] mm, Herkunft: ERW-E2 N1, oben zugänglich (Deckelöffnung) (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2_vorlade_masse_kg | Wert 0.41 kg, Herkunft: Datenblatt GV200 S. 3: 0,38 kg (Opus im PDF-Text geprüft) + Vishay RH050 28 g = 0,41 kg zusammen (Schütz + Widerstand) (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_e2_vorladeschuetz_mm | Wert [80.5, 56, 72.6] mm, Herkunft: Datenblatt (forschung/datenblaetter.md, quellen/datenblaetter/BT-712_gigavac_GV200.pdf): Gigavac GV200, Flansch 80,5, Gehäuse Ø 56, Höhe 72,6 (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_e2_vorladewiderstand_mm | Wert [49.99, 28.96, 21.44] mm, Herkunft: KI-generiert (Claude Sonnet, 2026-11-20), Auftrag DB2. Datenblatt BT-712_vishay_RH050.pdf S. 2: Körper C 49,99 (Länge), F 28,96 (Breite), B 21,44 (Höhe) (aus Zeichnung gelesen; Zuordnung der Buchstaben nicht eindeutig; Wert im PDF-Text geprüft: nein) (annahmen_datenblatt.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_beruehrschutz_dicke_mm | Wert 1 mm, Herkunft: ERW-E2 N3 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_bms_abstandsbolzen | Wert [4, 4, 8] -, Herkunft: ERW-E2 N3: 4 Stück M4, Höhe 8 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_bms_abstandsbolzen_aussen_mm | Wert 7 mm, Herkunft: abgeleitet (Sonnet): Außendurchmesser Sechskant SW7 (Gedächtnis-Normmaß, nicht belegt) (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_bms_abstandsbolzen_einzug_mm | Wert 5 mm, Herkunft: abgeleitet (Sonnet): Lage 5 mm von der Platinenkante, Lage nicht in N3 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_bms_platine_dicke_mm | Wert 1.6 mm, Herkunft: ERW-E2 N3 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_bms_stecker_mm | Wert [30, 15, 12] mm, Herkunft: ERW-E2 N3: Stecker 26-polig und 2 x Daisy-Chain 12-polig je 30 x 15 x 12 (Lesart: Maß gilt für alle drei) (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_box_deckel_mm | Wert 2 mm, Herkunft: ERW-E2 N3 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_box_dichtung_mm | Wert [3, 3] mm, Herkunft: ERW-E2 N3 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_box_druckausgleich_d_mm | Wert 7.8 mm, Herkunft: KI-generiert (Claude Sonnet, 2026-11-20), Auftrag DB2. Datenblatt BT-570_gore_auto-batteries-snapfit.pdf S. 2: Einbauloch Ø7,8 ±0,1 (Wert im PDF-Text geprüft: ja); Kopf Ø17 steht in A_g5_druckausgleich_mm (annahmen_datenblatt.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_box_flansch_dicke_mm | Wert 2 mm, Herkunft: abgeleitet (Sonnet): Flanschdicke = Wanddicke A_e2_box_wand_mm 2 mm (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_box_flansch_mm | Wert 12 mm, Herkunft: ERW-E2 N3 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_box_schraube_gewinde_mm | Wert 5 mm, Herkunft: ERW-E2 N3 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_box_schraube_teilung_mm | Wert 60 mm, Herkunft: ERW-E2 N3: M5 alle 60 mm (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_bruecke_mm | Wert [25, 3, 80] mm, Herkunft: ERW-E2 N3 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_bruecke_schrauben | Wert [2, 8] -, Herkunft: ERW-E2 N3: 2 x M8 mit Scheibe (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_clip_abstand_mm | Wert 200 mm, Herkunft: ERW-E2 N3 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_clip_mm | Wert [20, 15, 10] mm, Herkunft: ERW-E2 N3 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_daisy_d_mm | Wert 4 mm, Herkunft: ERW-E2 N3 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_daisy_r_min_mm | Wert 20 mm, Herkunft: ERW-E2 N3 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_daisy_stecker_mm | Wert [15, 8, 8] mm, Herkunft: ERW-E2 N3 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_fenster | Wert letztes Feld (hinten) -, Herkunft: abgeleitet (Sonnet): Zellverbinder-Details (Omega, Schweißnaht, Berührschutz) nur im hintersten Querträger-Feld voll, sonst vereinfacht; Auftrag AUFTRAG.md Fortsetzung 5 erlaubt das bei zu großer Datei (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_fpc_stecker_mm | Wert [25, 8, 6] mm, Herkunft: ERW-E2 N3: 20-polig, an der CMU (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_fpc_tab_mm | Wert [8, 4, 0.2] mm, Herkunft: ERW-E2 N3 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_fusslasche_mm | Wert [20, 9, 2] mm, Herkunft: abgeleitet (Sonnet): Laschenbreite 20, Auskragung 9 (< Teilabstand 10), Dicke 2; Bohrung M5 nicht in N3 bemaßt (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_hv250_flansch_mm | Wert [90, 70, 8] mm, Herkunft: ERW-E2 N3 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_hv250_hebel_mm | Wert [60, 10, 10] mm, Herkunft: ERW-E2 N3 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_hv250_koerper_mm | Wert [50, 60] mm, Herkunft: ERW-E2 N3: Ø 50 x 60, 90 Grad gewinkelt (liegend) (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_hv250_oring_mm | Wert [60, 3] mm, Herkunft: abgeleitet (Sonnet): O-Ring Mittendurchmesser 60, Schnur 3 (Schnur = Dichtungsmaß 3 aus N3) (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_hv250_schrauben | Wert [4, 5] -, Herkunft: ERW-E2 N3: 4 x M5 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_hv40_flansch_mm | Wert [50, 40, 6] mm, Herkunft: ERW-E2 N3 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_hv40_schrauben | Wert [4, 4] -, Herkunft: ERW-E2 N3: 4 x M4 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_hvil_mm | Wert [15, 10, 8] mm, Herkunft: ERW-E2 N3 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_kabel_biegeradius_faktor_D | Wert 5 -, Herkunft: ERW-E2 N3: R >= 5 D (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_kabel_schichten | Wert ['Leiter', 'Isolierung', 'Schirm', 'Mantel'] -, Herkunft: ERW-E2 N3 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_kabel_wand_teilung | Wert 3 -, Herkunft: abgeleitet (Sonnet): Radialwand zwischen Leiter und Außendurchmesser in drei gleiche Teile (Isolierung, Schirm, Mantel); N3 nennt keine Schichtdicken (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_kabelschuh_huelse_mm | Wert 40 mm, Herkunft: ERW-E2 N3 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_kabelschuh_lasche_laenge_mm | Wert 20 mm, Herkunft: abgeleitet (Sonnet): Palme quadratisch 20 x 20 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_kabelschuh_lasche_mm | Wert [20, 4] mm, Herkunft: ERW-E2 N3: Lasche 20 breit x 4 dick (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_lasche_lfp_gewinde_mm | Wert 8 mm, Herkunft: ERW-E2 N3 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_lasche_pyro_schmelz_mm | Wert [25, 3, 25] mm, Herkunft: abgeleitet (Sonnet): Laschen = Querschnitt der Schiene Cu 25 x 3 (LFP) bzw. 20 x 3 (NMC) hat Vorrang; Auskragung 25 ohne Vorgabe (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_lasche_ueberlappung_mm | Wert 25 mm, Herkunft: ERW-E2 N3 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_m4_kopf_mm | Wert [7, 4] mm, Herkunft: abgeleitet (Sonnet): Zylinderkopf M4: Ø 7 x 4 (Gedächtnis-Normmaß ISO 4762, nicht belegt) (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_m5_kopf_mm | Wert [8.5, 5] mm, Herkunft: abgeleitet (Sonnet): Zylinderkopf M5: Ø 8,5 x 5 (Gedächtnis-Normmaß ISO 4762, nicht belegt) (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_m8_kopf_mm | Wert [13, 8] mm, Herkunft: abgeleitet (Sonnet): Zylinderkopf M8: Ø 13 x 8 (Gedächtnis-Normmaß ISO 4762, nicht belegt) (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_m8_scheibe_mm | Wert [16, 1.6] mm, Herkunft: abgeleitet (Sonnet): Scheibe M8: Ø 16 x 1,6 (Gedächtnis-Normmaß ISO 7089, nicht belegt) (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_ntc_je_cmu | Wert 4 -, Herkunft: ERW-E2 N3 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_ntc_mm | Wert [1.6, 0.8, 0.8] mm, Herkunft: KI-generiert (Claude Sonnet, 2026-11-20), Auftrag DB2. Datenblatt BT-330_vishay_NTCS0603E3.pdf S. 2: L 1,6 ±0,15, W 0,8 ±0,15, T 0,8 ±0,15 (Wert im PDF-Text geprüft: ja) (annahmen_datenblatt.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_nv_flansch_mm | Wert [50, 30, 5] mm, Herkunft: ERW-E2 N3 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_nv_schrauben | Wert [2, 4] -, Herkunft: ERW-E2 N3: 2 x M4 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_omega_h_mm | Wert 4 mm, Herkunft: ERW-E2 N3: Dehnbogen (Omega) h 4 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_pyro_lasche_gewinde_mm | Wert 8 mm, Herkunft: ERW-E2 N3 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_schiene_biegeradius_innen_faktor_dicke | Wert 1.0 -, Herkunft: ERW-E2 N3: Biegeradius innen = Dicke (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_schiene_bohrung_mm | Wert 8.5 mm, Herkunft: ERW-E2 N3 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_schiene_cu_LFP_mm | Wert [25, 3] mm, Herkunft: ERW-E2 N3 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_schiene_cu_NMC_mm | Wert [20, 3] mm, Herkunft: ERW-E2 N3 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_schmelz_halter_mm | Wert [40, 40, 95] mm, Herkunft: ERW-E2 N3: Schmelzsicherung im Kunststoffhalter (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_schmelz_wand_mm | Wert 5 mm, Herkunft: abgeleitet (Sonnet): Halterwand = (40 - 30) / 2 aus Halter 40 und Sicherung 30 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_schrumpfschlauch_mm | Wert 0.5 mm, Herkunft: ERW-E2 N3 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_schuetz_bolzen_abstand_mm | Wert 25.5 mm, Herkunft: KI-generiert (Claude Sonnet, 2026-11-20), Auftrag DB2. Datenblatt BT-711_glvac_GLFX250.pdf S. 6 (PDF-Zeichnung, aus Zeichnung: 25,5 ±0,5 Lastanschlüsse; Wert im PDF-Text geprüft: nein). Gilt im Modell auch für Vorladeschütz GV200 (BT-712_gigavac_GV200.pdf S. 3: 26,7, aus Zeichnung), ein gemeinsamer Schlüssel (annahmen_datenblatt.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_schuetz_bolzen_d_mm | Wert 8 mm, Herkunft: ERW-E2 N3 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_schuetz_bolzen_h_mm | Wert 15 mm, Herkunft: ERW-E2 N3 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_schuetz_bolzen_n | Wert 2 -, Herkunft: ERW-E2 N3 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_schuetz_fusslasche_gewinde_mm | Wert 5 mm, Herkunft: ERW-E2 N3 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_schuetz_fusslaschen_n | Wert 2 -, Herkunft: ERW-E2 N3 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_schuetz_spulenstecker_mm | Wert [15, 10, 12] mm, Herkunft: ERW-E2 N3 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_schweiss_abstand_mm | Wert 5 mm, Herkunft: abgeleitet (Sonnet): Abstand der zwei Linien 5 mm (Mitte zu Mitte) (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_schweiss_mm | Wert [10, 1, 0.2, 2] mm, Herkunft: ERW-E2 N3: 2 Linien 10 x 1, Vertiefung 0,2 je Pol (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_servicedeckel_dichtung_mm | Wert [3, 3] mm, Herkunft: ERW-E2 N3 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_servicedeckel_mm | Wert [120, 80, 2] mm, Herkunft: ERW-E2 N3 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_servicedeckel_rand_mm | Wert 12 mm, Herkunft: abgeleitet (Sonnet): Rand des Haupt-Deckels um die Serviceöffnung für Dichtung (3) und Senkschrauben; Öffnung im Deckel = 120 x 80 minus 2 x 12 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_servicedeckel_schrauben | Wert [6, 5] -, Herkunft: ERW-E2 N3: 6 x M5 (Senkkopf bündig, Kopfhöhe = Deckeldicke) (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_shunt_platine_mm | Wert [80, 40, 1.6] mm, Herkunft: ERW-E2 N3 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_shunt_stecker_pol | Wert 4 -, Herkunft: ERW-E2 N3 (Stecker 4-polig, Maße fehlen) (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_shunt_steg_mm | Wert 3 mm, Herkunft: ERW-E2 N3: Manganin-Steg 3 mm zwischen Cu-Enden M8 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_stecker_koerper_einzug_mm | Wert 8 mm, Herkunft: abgeleitet (Sonnet): Körper von HV 40 A / NV: Flanschfläche minus 8 mm je Kante (Platz für Schraubenköpfe); Höhe = Hülle aus N1 minus Flansch (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2d_stecker_schraube_einzug_mm | Wert 5 mm, Herkunft: abgeleitet (Sonnet): Schrauben 5 mm von der Flanschkante (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_g54_beruehrschutz_z_mm | Wert 1.0 mm, Herkunft: Annahme Sonnet G5.4: Berührschutz NMC liegt 1 mm über der Verbinderoberkante (über FPC 0,3, Ni-Tab 0,2 und NTC 1 mm), ohne Omega-Bogen (nicht umgesetzt, Stufe K); schneidet Pad und Kühlplatte aus (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g54_bms_stecker_y_mm | Wert [20, 70, 110] mm, Herkunft: Annahme Sonnet G5.4: Lage der drei BMS-Stecker (26-polig, 2 × Daisy) entlang der Platine ab Rand, wie e2d pack_e2d.py (20/70/110) (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g54_cmu_bauteile_mm | Wert [20, 15, 3] mm, Herkunft: Annahme Sonnet G5.4: zwei Bausteine (ICs) je CMU-Platine 20 (y) × 15 (z) × 3 (x), Bauteilandeutung ohne Quelle; Platinendicke = A_e2d_bms_platine_dicke_mm (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g54_cmu_bohrung_mm | Wert [3.2, 5] mm, Herkunft: Annahme Sonnet G5.4: vier Befestigungsbohrungen je Platine Ø 3,2 (M3), 5 mm vom Rand; Platine an den Rahmen gelehnt (Befestigung nicht belegt) (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g54_hv250_hebel_x_mm | Wert 10 mm, Herkunft: Annahme Sonnet G5.4: Hebel des HV250-Steckers (A_e2d_hv250_hebel_mm) beginnt 10 mm hinter der Vorderfläche (Form nicht belegt), damit die Schienen vor der Vorderfläche frei bleiben (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g54_iso10642_mm | Wert [5, 10, 2.8] mm, Herkunft: Annahme Sonnet G5.4: Senkschraube ISO 10642 M5 als Tripel d, dk, k; Norm, nicht in den Akten (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g54_iso4017_mm | Wert [4, 7, 2.8, 5, 8, 3.5, 6, 10, 4, 8, 13, 5.3] mm, Herkunft: Annahme Sonnet G5.4: Sechskantschraube ISO 4017 Normmaße als Tripel d, Schlüsselweite s, Kopfhöhe k (M4, M5, M6, M8); Norm, nicht in den Akten (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g54_iso7380_mm | Wert [3, 5.7, 1.65, 4, 7.6, 2.2, 5, 9.5, 2.75, 6, 10.5, 3.3, 8, 14, 4.4] mm, Herkunft: Annahme Sonnet G5.4: Flachkopf ISO 7380 Normmaße als Tripel d, dk, k (M3, M4, M5, M6, M8); Norm, nicht in den Akten (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g54_isolationsw_eckradius_mm | Wert 2 mm, Herkunft: Annahme Sonnet G5.4: Eckradius Gehäuse Isolationswächter (Stufe H, Form nicht belegt) (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g54_kabelschuh_box_abstand_mm | Wert 6 mm, Herkunft: Annahme Sonnet G5.4: Kabelschuh-Palme der HV-Leitung sitzt direkt an der Innenseite der Boxwand (Mitte des Schienen-Pads 6 mm hinter der Wandinnenseite: Palme 4 + halbe Schienendicke 1,5 + 0,5), weil der Pyro-Körper nur 13 mm von der Wand beginnt; Hülse 40 mm zur Wand und durch sie hinaus (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g54_kabelschuh_huelse_wand_mm | Wert 1 mm, Herkunft: Annahme Sonnet G5.4: Hülse des Kabelschuhs: Außendurchmesser = Leitungsdurchmesser + 2 × 1 mm (Wand), Form nicht belegt; die Hülse sitzt neben der M8-Schraube mit 1 mm Abstand zum Schraubenkopf (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g54_lasche_lfp_riser_mm | Wert 3 mm, Herkunft: Annahme Sonnet G5.4: Pol-Lasche LFP: Steg 3 mm dick hinter der letzten Zelle (x), Stufe auf Fahnenhöhe nach innen bis hinter den FPC-Stapel (y), Platte 25 × 25 über den Zellen (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g54_mutter_mm | Wert [8, 13, 6.8] mm, Herkunft: Annahme Sonnet G5.4: Sechskantmutter ISO 4032 M8 als Tripel d, s, m; Norm, nicht in den Akten (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g54_nmc_kopfrundung_mm | Wert 2 mm, Herkunft: Annahme Sonnet G5.4: Rundung der oberen Außenkante der 4680-Zelle (Schulter) (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g54_nmc_minus_abgriff_mm | Wert 17 mm, Herkunft: Annahme Sonnet G5.4: NMC Minus-Abgriff: Scheibe Ø12 × 1 auf dem Becherrand, Mittelpunkt 17 mm (= Zellradius 23 − Scheibenradius 6) von der Zellachse, quer zur Verbinderrichtung, Vorzeichen wechselnd mit der Zellnummer (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g54_nmc_nut_mm | Wert [14, 16, 0.5] mm, Herkunft: Annahme Sonnet G5.4: Ringnut um den Pluspol: Innen-Ø 14, Außen-Ø 16, Tiefe 0,5 (Isolierring BT-132); der Pol-Nippel selbst entfällt, weil die Abgriffscheibe (A_zellabgriff_NMC_mm) seine Höhe belegt (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g54_ntc_versatz_mm | Wert 0 mm, Herkunft: Annahme Sonnet G5.4: NTC LFP sitzt an der Zellstirn am Messabgriff; Platzierung wie E2d (Offsets in Zellteilungen), hier nur Y-Lage innerhalb der Lücke Rahmen-Zelle (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g54_pol_lfp_mm | Wert [10, 15, 1] mm, Herkunft: Annahme Sonnet G5.4: Polfahne LFP als flache Lasche an der äußeren Stirnseite: Breite 10 (x, wie ANNAHME_POL_DURCHMESSER_MM in cad/zelle/zelle.py), Höhe 15 (z), Dicke 1 (y); an der inneren Stirnseite (Reihen stoßen bei B/2 aneinander) ist kein Platz (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g54_pol_lfp_versatz_mm | Wert 20 mm, Herkunft: Annahme Sonnet G5.4: Plus-Fahne 20 mm über, Minus-Fahne 20 mm unter der Zellmitte, beide an der äußeren Stirnseite (BT-140: Stirnseite neben Kathodenpol); Verbinder zwischen Nachbarzellen als Z-Streifen (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g54_querverbinder_riser_mm | Wert [-7.5, 3] mm, Herkunft: Annahme Sonnet G5.4: Querverbinder LFP (Reihenmitte, vorn): Steg 3 mm dick, Vorderkante 7,5 mm vor der Zellvorderkante (x frei zwischen CMU-Bauteilen und FPC-Stegen), Streifen auf Fahnenhöhe längs y, Steg nach oben zu einer Platte 25 breit auf den Zellen (z = Zelloberkante, wie e2d), Trennbrücke darauf (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g54_schiene_pad_abstand_mm | Wert 13.5 mm, Herkunft: Annahme Sonnet G5.4: Stromschiene sitzt als Pad (Fläche Breite × Breite, Dicke der Schiene) mit der Außenseite bündig am Bolzenende (Bolzenlänge 15: Pad-Mitte 13,5, Pad 3 mm), damit waagerechte Schienenstücke (halbe Breite 12,5) 1 mm Abstand zur Gerätefläche haben; Sicherungs- und Shuntlaschen vereinfacht als Bolzen Ø8 × 15 an der Klemmstelle, Muttern nicht modelliert wo kein Platz (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g54_schuetz_fusslasche_mm | Wert [20, 9, 2] mm, Herkunft: Annahme Sonnet G5.4: Fußlasche des Schützes A_e2d_fusslasche_mm 20 × 9 × 2, je Schütz 2 an den kurzen Seiten, Schraube M5 in den Boden der Schaltbox (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g54_tab_dicke_lfp_mm | Wert 0.2 mm, Herkunft: Annahme Sonnet G5.4: FPC-Tab LFP liegt am Zellende zwischen Verbinderebene und Zelle (y-Dicke = A_e2d_fpc_tab_mm[2]) (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g54_zelle_eckradius_mm | Wert 2 mm, Herkunft: Annahme Sonnet G5.4: Kantenradius der Blade-Zellhülle (Hülle gerundet, Stufe F) (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g5_anschluss_mm | Wert [19, 16, 40] mm, Herkunft: Annahme Opus: Anschlussstutzen Außen-Ø 19 (3/4"), Innen-Ø 16, 40 mm über die Rückwand hinaus (Länge darf wachsen, Autor) (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g5_aussen_teile | Wert {'druckausgleich_y_versatz_mm': 150, 'entgasung_y_versatz_mm': -150, 'fuehler_z_ueber_stutzen_mm': 25, 'typschild_x_mm': 300, 'typschild_rand_mm': 70} mm, Herkunft: Annahme Opus 2026-11-19: Druckausgleich und Entgasungsventil an der Rückwand ±150 mm neben der Mitte (frei vom Kühlmodul), Kühlmittelfühler M12 durch die Rückwand in Verteiler/Sammler 25 mm über dem Stutzen, Typschild vorn auf dem Deckel; 2026-11-20: Typschild x 300, 70 mm vom rechten Rahmen (vorher Mitte, traf Servicedeckel) (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g5_befestigung_huelse_mm | Wert [20, 10.5] mm, Herkunft: Annahme Opus: Stahlhülse Außen-Ø 20, Innen-Ø 10,5 (M10), Hülse ≤ Rahmenbreite 30 − 2 × Wand (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g5_befestigung_n_je_seite | Wert 6 Stück, Herkunft: Annahme Opus: 6 Schraubpunkte je Längsseite (12 gesamt), M10 senkrecht durch den Seitenrahmen, weil die Breite 1430 fest ist (kein Flansch außen) (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g5_befestigung_rand_x_mm | Wert 80 mm, Herkunft: Annahme Opus: erster/letzter Punkt 80 mm von der Stirnseite (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g5_behaelter_masse_kg | Wert 0.3 kg, Herkunft: Annahme Opus 2026-11-19, bis Datenblatt (G5.5b):  (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g5_behaelter_mm | Wert [100, 150, 100] mm, Herkunft: Annahme Opus 2026-11-19, bis Datenblatt (G5.5b): kein Datenblatt (Autorliste), ≈ 1 L durchströmt (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g5_blech_mm | Wert 1.0 mm, Herkunft: ENT-152 (Autor: Blech oben und unten 1 mm, 4 mm Wasserraum) (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g5_box_eckradius_mm | Wert 5 mm, Herkunft: Annahme Opus 2026-11-19 (Schaltbox liegend): senkrechte Außenkanten der Wanne (Tiefziehen/Fräsen) (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g5_box_freiraum_oben_mm | Wert 10 mm, Herkunft: Annahme Opus 2026-11-19 (Schaltbox liegend): Luft über dem höchsten liegenden Gerät (Kriechstrecke, Montage) (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g5_chiller_masse_kg | Wert 1.2 kg, Herkunft: Annahme Opus 2026-11-19, bis Datenblatt (G5.5b):  (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g5_chiller_mm | Wert [120, 200, 60] mm, Herkunft: Annahme Opus 2026-11-19, bis Datenblatt (G5.5b): kein Datenblatt (Autorliste) (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g5_deckelschraube_ausweich_mm | Wert 2 mm, Herkunft: Annahme Sonnet, Opus prüft (G5.9; Opus 2026-11-23 freigegeben als Regel): Zuschlag zu halber Blockbreite + Schaftradius beim seitlichen Ausweichen der Rückreihen-Deckelschrauben vor den Plattenlaschen (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g5_deckelschraube_mm | Wert [6.4, 100] mm, Herkunft: Annahme Opus: Deckelschrauben M6 (Bohrung 6,4), Teilung 100 mm auf Rahmenmitte (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g5_druckausgleich_mm | Wert [17, 12.9, 7.8] mm, Herkunft: Datenblatt (forschung/datenblaetter.md, quellen/datenblaetter/BT-570_gore_auto-batteries-snapfit.pdf): Gore PolyVent AVS 70, Kopf Ø 17, Höhe 12,9, Einbauloch Ø 7,8 (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g5_eckradius_platte_mm | Wert 10 mm, Herkunft: Annahme Opus: Ecken Unterfahrschutz, Wanne, Deckel (Blechzuschnitt), ≤ halbe Rahmenbreite (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g5_entgasungsventil_mm | Wert [77, 55, 22.5] mm, Herkunft: Datenblatt (forschung/datenblaetter.md, quellen/datenblaetter/BT-750_vernay_VoltaVent.pdf S. 3): Vernay VoltaVent 77 × 55 × 22,5 (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g5_hv_eingang_abstand_mm | Wert 5 mm, Herkunft: Annahme Opus 2026-11-19 (Schaltbox liegend): HV-Leitung tritt 5 mm über dem Boxboden durch die Seitenwand (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g5_isolationswaechter_mm | Wert [60, 40, 15] mm, Herkunft: Annahme Opus 2026-11-19 (Schaltbox liegend): Isolationswächter als Platine 60 × 40 × 15 bis W34 (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g5_kabelschuh_m8_35_mm | Wert [42, 17] mm, Herkunft: Datenblatt (forschung/datenblaetter.md, quellen/datenblaetter/Pfisterer 300 010 010): 35 mm², M8, L 42, B 17 (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g5_kabelschuh_m8_50_mm | Wert [51, 22, 10, 8.4] mm, Herkunft: Datenblatt (forschung/datenblaetter.md, quellen/datenblaetter/BT-590_pfisterer_300013260.pdf): Pfisterer DIN 46235 M8 50 mm²: L 51, B 22, Hülse Ø 10, Loch 8,4 (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g5_kaeltemittel_stutzen_mm | Wert [12, 25] mm, Herkunft: Annahme Opus 2026-11-19, bis Datenblatt (G5.5b): Kältemittelstutzen Ø 12 × 25 (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g5_kanal_rand_x_mm | Wert 15 mm, Herkunft: Annahme Opus: erster/letzter Querkanal 15 mm vom Plattenende (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g5_kantenradius_profil_mm | Wert 1.5 mm, Herkunft: Annahme Opus: Außenkanten Strangpressprofile (≈ Wand/2) (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g5_kragen_kuehlplatte_mm | Wert 3 mm, Herkunft: Annahme Opus 2026-11-19: gelöteter Kragen (ohne Wasser) um jede Durchführung durch die Kühlplatte (HV-Leitung, Schraubenköpfe, Laschen) (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g5_kuehlmittelfuehler_form_mm | Wert {'gewinde_l': 12, 'sw': 19, 'sechskant_h': 8, 'koerper_d': 12, 'stecker': [20, 14, 14]} mm, Herkunft: Annahme Opus 2026-11-19: Aufteilung der Gesamtlänge 51 mm (Datenblatt) in Gewinde, Sechskant SW19, Körper und Stecker; Stufe F (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g5_kuehlmittelfuehler_masse_kg | Wert 0.017 kg, Herkunft: Datenblatt BT-640_kyocera-avx_94082.pdf S. 3 (17 g, forschung/datenblaetter.md) (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g5_kuehlmittelfuehler_mm | Wert [12, 1.5, 51] mm, Herkunft: Datenblatt (forschung/datenblaetter.md, quellen/datenblaetter/BT-640_kyocera-avx_94082.pdf S. 3): Kyocera AVX 94082, Einschraubgewinde M12 × 1,5 (im PDF-Text bestätigt), Länge 51, 17 g (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g5_kuehlmodul_abstand_mm | Wert 60 mm, Herkunft: Annahme Opus 2026-11-19, bis Datenblatt (G5.5b): Abstand Stutzenende → Geräte (Schlauchbogen) (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g5_kuehlmodul_teilabstand_mm | Wert 60 mm, Herkunft: Annahme Opus 2026-11-19, bis Datenblatt (G5.5b): Abstand der Geräte im Kühlmodul (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g5_kuehlplatte_blech_mm | Wert 1.5 mm, Herkunft: K2 Nachtrag (Blech 1,5 mm Al) (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g5_maeander | Wert {'bahnen': 8, 'teilkanal_mm': 8, 'fuehrung': 'laengs'}, Herkunft: ENT-153…156 (K2b, Opus-Auswahl): 8 Bahnen längs, Teilkanal 8 mm (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g5_ntc_zelle_mm | Wert [1.6, 0.8, 0.8] mm, Herkunft: Datenblatt (forschung/datenblaetter.md, quellen/datenblaetter/Vishay NTCS0603E3): 1,6 × 0,8 × 0,8 (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g5_pumpe_masse_kg | Wert 1.0 kg, Herkunft: Annahme Opus 2026-11-19, bis Datenblatt (G5.5b):  (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g5_pumpe_mm | Wert [80, 150] mm, Herkunft: Annahme Opus 2026-11-19, bis Datenblatt (G5.5b): Pierburg CWA100-3 gewählt (25 L/min bei 1 bar, Datenblatt S. 1), Maße fehlen im Datenblatt → Ø 80 × 150 Annahme (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g5_rahmen_kammern_lage | Wert uebereinander, Herkunft: Opus 2026-11-19: 3 Kammern (A_seitenrahmen_kammern) übereinander, Stege waagerecht leiten Seitenkraft zum Schweller (ENT-151); ersetzt die Lesart 'über die Breite' (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g5_sammler_mm | Wert [20, 3] mm, Herkunft: Annahme Opus: Sammelkanal je Längsseite 20 mm breit in der Platte, 3 mm Wand zum Plattenrand (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g5_schienengasse_mm | Wert 40 mm, Herkunft: Annahme Opus 2026-11-19 (Schaltbox liegend): Gasse zwischen Sicherungsreihe und Schützreihe: Bolzen 15 + Mutter + Schiene 25 breit hochkant (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g5_schlauch_biegeradius_mm | Wert 60 mm, Herkunft: Annahme Opus 2026-11-19: ≈ 2,2 × Außen-Ø (Händlerangaben Gates/ContiTech ohne Datenblatt, Autorliste) (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g5_schlauch_mm | Wert [27, 19] mm, Herkunft: Annahme Opus 2026-11-19, bis Datenblatt (G5.5b): EPDM außen 27, innen 19 (Stutzen 19) (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g5_trennsteg_mm | Wert 6 mm, Herkunft: Annahme Sonnet, Opus prüft (G5.9, ENT-158/159): Trennsteg zwischen den zwei Mäandern = 2 × A_g5_kanal_steg_mm (3 mm) (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g5_typschild_mm | Wert [100, 60, 0.3] mm, Herkunft: Annahme Opus 2026-11-19: Typschild Al-Folie 100 × 60 × 0,3 mm, geklebt (ECE R100 Kennzeichnung) (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g5_umlenk_mm | Wert 30 mm, Herkunft: Annahme Opus: Länge der Umlenkkammer am Bahnende (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g5_ventil_masse_kg | Wert 0.4 kg, Herkunft: Annahme Opus 2026-11-19, bis Datenblatt (G5.5b):  (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g5_ventil_mm | Wert [60, 80, 60] mm, Herkunft: Annahme Opus 2026-11-19, bis Datenblatt (G5.5b): Pierburg 3/2-Wege-Ventil (Broschüre F0001 ohne Maße) (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g5_verteiler_mm | Wert [40, 30] mm, Herkunft: Annahme Opus: Verteiler-/Sammlerblock 40 (x) × 30 (y), verbindet obere und untere Platte senkrecht, in der hinteren Endzone (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g5_verteilerrohr_abstand_mm | Wert 10 mm, Herkunft: Annahme Sonnet, Opus prüft (G5.9, ENT-158/159): Lücke Blockrückseite bis Rohraußenseite, überbrückt vom Nippel Ø19/16 (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g5_verteilerrohr_spalt_mm | Wert 2 mm, Herkunft: Annahme Sonnet, Opus prüft (G5.9, ENT-158/159): Spalt zwischen Verteilerrohr (oben) und Sammelrohr (unten) (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g5_verteilerrohr_wand_mm | Wert 1.5 mm, Herkunft: Annahme Sonnet, Opus prüft (G5.9, ENT-158/159): Wand Al-Rohr wie Anschlussstutzen (A_g5_anschluss_mm: (19−16)/2); Innen-Ø 25 aus ENT-159 (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g5_vorladewiderstand_typ | Wert Vishay RH050, Herkunft: Datenblatt (forschung/datenblaetter.md, quellen/datenblaetter/BT-712, S. 2, 28 g; Maßbuchstaben nicht geprüft → Maße A_e2_vorladewiderstand_mm bleiben bis zur Prüfung (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_gruppenverbinder_NMC_mm | Wert [25, 3] mm, Herkunft: AUFTRAG G4: Querschnitt 25 x 3 (Breite x Dicke) (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_hoehe_max_mm | Wert 130 mm, Herkunft: M0 eingaben.json (Annahme) (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_kuehlplatte_mm | Wert 8 mm, Herkunft: M0 eingaben.json (Annahme); Vollmaterial, real hohl (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_luft_mm | Wert 5 mm, Herkunft: M0 eingaben.json (Annahme) (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_pad_mm | Wert 1 mm, Herkunft: M0 eingaben.json waermeleitschicht_je (Annahme) (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_quertraeger_anzahl | Wert 3 -, Herkunft: M0 eingaben.json (Annahme Opus) (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_quertraeger_breite_mm | Wert 26 mm, Herkunft: M0 eingaben.json (W22, US9045030) (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_quertraeger_hoehe_mm | Wert 54 mm, Herkunft: M0 eingaben.json (W22, US9045030) (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_quertraeger_spiel_mm | Wert 2 mm, Herkunft: M0 eingaben.json (Annahme) (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_quertraeger_wand_mm | Wert 2.5 mm, Herkunft: M0 eingaben.json (Annahme, Mitte 2-3 mm) (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_rand_mm | Wert 30 mm, Herkunft: M0 eingaben.json rand_mm (Annahme) (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_seitenrahmen_kammern | Wert 3 -, Herkunft: Annahme Opus 2026-11-17: 3 Kammern über die Rahmenbreite (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_seitenrahmen_wand_mm | Wert 2.5 mm, Herkunft: Annahme Opus 2026-11-17: Mehrkammerprofil, Wand 2,5 mm (W22-Wandbereich) (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_traeger_dicke_NMC_mm | Wert 2.5 mm, Herkunft: NEUE ANNAHME (Platzhalter, in M0 nicht gesetzt; Opus entscheiden) (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_unterfahrschutz_mm | Wert 3 mm, Herkunft: M0 eingaben.json (Annahme) (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_vergusshoehe_anteil_NMC | Wert 0.5 -, Herkunft: AUFTRAG G4: Verguss bis halbe Zellhöhe (Annahme) (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_zellabgriff_NMC_mm | Wert [12, 1] mm, Herkunft: AUFTRAG G4: 12 x 1 (Durchmesser x Dicke, Scheibe auf dem Pluspol) (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_zellverbinder_LFP_mm | Wert [25, 3] mm, Herkunft: AUFTRAG G4: Querschnitt 25 x 3 (Breite x Dicke) (annahmen.json) | Wert beibehalten und Akte anlegen | |

---
*KI-generiert (Claude Sonnet, 2026-11-23). Status Entwurf. Freigabe nur durch den Autor.*

