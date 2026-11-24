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
- [[Bauteil/BT-320|BT-320]]
- [[Bauteil/BT-330|BT-330]]
- [[Bauteil/BT-350|BT-350]]
- [[Entscheidung/ENT-006|ENT-006]]
- [[Entscheidung/ENT-013|ENT-013]]
- [[Entscheidung/ENT-151|ENT-151]]
- [[Entscheidung/ENT-159|ENT-159]]

## Vorgänge, die dieses Dokument nennen
- –

## Inhalt (Kopie aus `docs/19_freigaberunde.md`)

| Dok.-Nr. | BAT-DOC-19 | Version | 0.1 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Freigaberunde (Sammelliste) | Ersteller | Claude Sonnet (KI), pm.py freigabe | Prüfer | – (Mensch offen) |

> **KI-generiert.** Entwurf, nicht vom Menschen freigegeben. Erzeugt am 2026-11-23 von `python3 pm/pm.py freigabe`, nicht von Hand bearbeiten (Antworten in der Spalte „Autor“ gehören in die Quelle: Akte, `pm/anforderungen.json`, `annahmen*.json`). Konzept: `docs/17_workflow_schleife.md` §4.

Zählung: 0 offene Akten, 31 Kriterien ohne Herkunft Autor oder Anforderungen mit Lücke, 22 Annahmen A_* ohne Akte. Akten mit Status „ersetzt“ sind nicht aufgeführt. Als „ohne Akte“ gilt eine Annahme, deren Schlüsselname in keiner `pm/entscheidungen/ENT-*.md` vorkommt.

## 1 Offene Akten (Status nicht „entschieden…“)

| ID | Frage | Vorschlag | Autor: ja/nein/ändern |
|---|---|---|---|

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
| A_boden_mm | Wert 3 mm, Herkunft: M0 eingaben.json hoehenstapel_mm.boden (Annahme) (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_deckel_mm | Wert 2 mm, Herkunft: M0 eingaben.json hoehenstapel_mm.deckel (Annahme) (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_dichte_pad_kg_m3 | Wert 2500 kg/m3, Herkunft: Annahme Opus 2026-11-17 (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_e2_trennstecker_mm | Wert [80, 50, 60] mm, Herkunft: ERW-E2 N1, oben zugänglich (Deckelöffnung) (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_g5_befestigung_huelse_mm | Wert [20, 10.5] mm, Herkunft: Annahme Opus: Stahlhülse Außen-Ø 20, Innen-Ø 10,5 (M10), Hülse ≤ Rahmenbreite 30 − 2 × Wand (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g5_befestigung_n_je_seite | Wert 6 Stück, Herkunft: Annahme Opus: 6 Schraubpunkte je Längsseite (12 gesamt), M10 senkrecht durch den Seitenrahmen, weil die Breite 1430 fest ist (kein Flansch außen) (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g5_befestigung_rand_x_mm | Wert 80 mm, Herkunft: Annahme Opus: erster/letzter Punkt 80 mm von der Stirnseite (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_g5_rahmen_kammern_lage | Wert uebereinander, Herkunft: Opus 2026-11-19: 3 Kammern (A_seitenrahmen_kammern) übereinander, Stege waagerecht leiten Seitenkraft zum Schweller (ENT-151); ersetzt die Lesart 'über die Breite' (annahmen_g5.json) | Wert beibehalten und Akte anlegen | |
| A_gruppenverbinder_NMC_mm | Wert [25, 3] mm, Herkunft: AUFTRAG G4: Querschnitt 25 x 3 (Breite x Dicke) (annahmen.json) | Wert beibehalten und Akte anlegen | |
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
| A_unterfahrschutz_mm | Wert 3 mm, Herkunft: M0 eingaben.json (Annahme) (annahmen.json) | Wert beibehalten und Akte anlegen | |
| A_zellabgriff_NMC_mm | Wert [12, 1] mm, Herkunft: AUFTRAG G4: 12 x 1 (Durchmesser x Dicke, Scheibe auf dem Pluspol) (annahmen.json) | Wert beibehalten und Akte anlegen | |

---
*KI-generiert (Claude Sonnet, 2026-11-23). Status Entwurf. Freigabe nur durch den Autor.*

