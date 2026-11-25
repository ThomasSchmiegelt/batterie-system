# Storyboard Video Elektronik (BAT-DOC-13c), Entwurf

KI-generiert: Rohtext Kolibri 1 (franconia), geprüft und bereinigt von Claude Sonnet 5.5, 2026-11-25. Status: Entwurf. Rohfassung: `video/elektronik/kol3.md`, Prüfung: `video/elektronik/pruefung_storyboard.txt`. Zahlen nur aus `video/elektronik/daten.json`.
Gesamtdauer 165 s (25 fps, 1280x720). Der Wissensgraph läuft als Hintergrund über den ganzen Film (Szene 2).

## Szene 1 Anforderungen mit Normen (0–25 s)
Bild: Tafel aus daten.json (anforderungen, normen), Graph gedimmt im Hintergrund.
1. Pkw, Fahrzeugmasse etwa 1500 kg [REQ-P01]
2. Systemspannung 720–880 V [REQ-P03]
3. Dauerleistung mindestens 60 kW [REQ-P04]
4. Schnellladen LFP 20 min, NMC 30 min [REQ-P05]
5. Hervorgehoben REQ-P15, P17…P21; Normen IEC 60664-1, ISO 26262, CISPR 25, UN R100, EU 2023/1542 [docs/07_normen_und_vorschriften.md]

## Szene 2 Wissensgraph wächst (0–165 s, Hintergrund)
Bildfolge `/home/cae/cae_projekte/batterie_video/wissen/graph/` (aus `video/graph_zeitraffer.py`), über die Filmdauer gedehnt. Keine eigenen Tafeln.

## Szene 3 Zelle (25–50 s)
Bild: sim/chemie/c1_zellmodell/ladekurve.png, dcir.png, waerme_LFP.png
1. Zelle LFP prismatisch Blade [REQ-P06]
2. Ladekurve, DCIR, Wärme [sim/chemie/c1_zellmodell]
3. Zellspreizung höchstens 5 K [REQ-P09]

## Szene 4 Pack baut sich auf (50–80 s)
Bild: cad/pack/entwurf/pack_LFP_schnitt.png, pack_LFP_explosion.png, pack_LFP_gesamt.png
Bild-in-Bild: sim/kuehlung/k3_gesamt/k3_vergleich.png (Kühlung), sim/mechanik/x3_crash_g5/energie_LFP_a.png (Crash)
1. Pack baut sich auf [REQ-P07]
2. Kühlung K3, K4 Vergleich [REQ-P12]
3. Crash Pfahl 5 kJ [REQ-P14]
4. Packmasse 619,85 kg [cad/pack/entwurf/ergebnis_LFP_e2d_e3c.json #masse_bekannt_kg]

## Szene 5 Steuergeräte entstehen (80–140 s)
5a CMU-Platine (80–95 s): platine_LFP_3d_top.png, platine_LFP_explosion.png, platine_LFP_3d_nah.png, schaltplan_LFP_kanal.png (sim/elektrik/e3_platine)
1. CMU-Leiterplatte, 4 Lagen, 110 Teile, DRC 0 [sim/elektrik/e3_platine/ergebnis_platine.json #LFP]
2. Explosion nach Lagen
3. Nahaufnahme Ausgleichskanal
5b BMS-Platine (95–110 s): platine_bms_3d_top.png, platine_bms_explosion.png, schaltplan_bms_blatt-1.png (sim/elektrik/e3c_bms_platine)
1. BMS-Platine, 134 Teile, DRC 0 [sim/elektrik/e3c_bms_platine/ergebnis_platine.json]
2. Rote HV/NV-Sperrzone [REQ-P19]
3. Schaltplanblatt Schütz
5c Rechnungen (110–125 s): spice_ausgleich_vorladung.png, spice_schuetz.png, e3b_temperatur.png, e3d_fmeda.png
1. SPICE Vorladung, U_V 912 V [sim/elektrik/e3_platine/ergebnis_vorladung.json #U_V]
2. Schütz Zener, Spannung 37,11 V [sim/elektrik/e3c_bms_platine/ergebnis_schuetz.json #zener_anzug.v_n_max_V]
3. Elmer-Wärme E3b [sim/elektrik/e3b_platine_waerme/e3b_temperatur.png]
4. FMEDA CMU LFP SG-01: SPFM 99,93 %, LFM 96,72 % (Ziel ASIL D: 99 %, 90 %) [sim/elektrik/e3d_fmeda/ergebnis.json #cmu.LFP.SG-01, #ziel.SG-01]
5d Nachverfolgung und Sicherheitsziele (125–140 s): Graph mit hervorgehobenen Ketten
1. REQ-P18 Funktionale Sicherheit nach ISO 26262 → ENT-192 (vorgeschlagen) → BT-323 Ausgleichskreis → Nachweis E3d, B-BAT-055 [daten.json ketten]
2. REQ-P19 → ENT-195 (entschieden) → BT-311 BMS-Leiterplatte [daten.json ketten]
3. REQ-P15 → ENT-184 (entschieden, Mensch) → BT-321 CMU-Leiterplatte [daten.json ketten]
4. Sicherheitsziele SG-01…SG-08, ASIL D, C, B [docs/24_gefahrenanalyse_hara.md]

## Szene 6 Batterie fertig, verschwindet (140–165 s)
Bild: cad/pack/entwurf/pack_LFP_gesamt.png, wird durchsichtig, nur der Graph bleibt.
1. Packmasse LFP 619,85 kg [cad/pack/entwurf/ergebnis_LFP_e2d_e3c.json]
2. CMU 110 Teile, BMS 134 Teile, DRC 0 [ergebnis_platine.json beider Platinen]
3. FMEDA SG-01 SPFM 99,93 % [sim/elektrik/e3d_fmeda/ergebnis.json]
4. Unten: Thomas Schmiegelt; Abspann: KI-generiert, Autor ist Konstrukteur
