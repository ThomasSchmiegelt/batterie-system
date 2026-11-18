| Dok.-Nr. | ERG-C2 | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Ergebnis C2: Parametersätze Blade-LFP und 4680 kalibriert, Schnellladen neu | Ersteller | Claude Sonnet (KI), Auftrag Opus | Prüfer | – (Opus offen) |

> **KI-generiert.** Entwurf, nicht freigegeben. Stand 2026-11-17. Zahlen aus `ergebnis_blade.json`, `ergebnis_dcir.json`, `ergebnis_schnellladen_lfp.json`, `ergebnis_schnellladen_n4680.json`, `kalibrierung_pulse.csv`, `blade_pulse.csv` (alle in diesem Ordner). PyBaMM 26.10, SPMe, CPU, nice. Rohdaten nur gelesen. Zwischendaten: `/home/cae/cae_projekte/batterie/c2/`. Herkunft Parameter: `eingaben.json`. Erwartung: `ERWARTUNG.md` (Opus, unverändert).

## Rohdaten Test#5 (Struktur)
`quellen/blade_datensatz/daten/5_Test_5.zip` enthält 10 Dateien (Arbin): CSV (HPPC/Kapazität 22. und 26.2.2024, SOP 27.2.2024 ≈ 25 °C) und xlsx (SOP 0 °C, −10 °C, 40 °C; Blatt `Channel-1_1`). Spalten u. a. Test_Time, Current, Voltage, SOC, Charge/Discharge_Capacity, Aux_Temperature (Thermoelement an der Zelle). Ablauf: Laden 0,5C auf 3,65 V, Ruhe, Entladen 1C (135 A) in SOC-Stufen, dazwischen 10-s-Entladepuls −475 A (3,5C) und Ladepuls +270 A; derselbe Ablauf mehrfach wiederholt. Abtastung im Puls grob (ca. 12 Punkte in 9 s). Zellentemperatur real ≈ −7, 3, 28, 41 °C (nicht −10/0/25/40). 1C-Kapazität Rohdaten: 135 A × 3520 s (Feb-26-Datei, Schritt 21) ≈ 132 Ah.

## Abgleich mit ERWARTUNG.md
| Nr. | Erwartung | Ergebnis (Fundstelle) | Urteil |
|---|---|---|---|
| 1a | Blade-DCIR 25 °C, 50 % ≈ 0,8–1,2 mΩ (W20 ≈ 1,0) | Messung 0,877 mΩ bei Zelle 28,3 °C; Modell 0,827 (`ergebnis_blade.json` R10_50pct.p25) | erfüllt |
| 1b | bei −10 °C 2–4-fach | Messung 1,712 mΩ bei −6,9 °C (1,95-fach zu 25 °C); Modell 1,299 | Messung am unteren Rand/knapp darunter, Modell unterschätzt |
| 1c | RMS Spannung ≤ 15 mV nach Kalibrierung | Kalibriersatz 25 °C, 15–90 % SOC: 15,3 mV (`rms_b_nachher_mV`, vorher 392 mV). Temperaturreihe (−7/3/41 °C): 157,8 mV (`rms_c_nachher_mV`, vorher 254 mV) | 25 °C: Grenze knapp verfehlt (15,3 > 15, < 30). **Temperatur: verfehlt (> 30 mV)** |
| 2 | LFP 92,4 Ah: DCIR ≈ 1,2–1,75 mΩ | 1,218 mΩ (`ergebnis_dcir.json` lfp92_25), −10 °C: 2,115 mΩ | im Band (am unteren Rand) |
| 2 | Wärme 2,1C ≈ 45–65 W (K1: 55 W) | CC-Phase nur 2,79 min bis 3,65 V: 64,5 W (`ergebnis_schnellladen_lfp.json` LFP.waerme_mittel_CC_W). 80 % nicht erreicht (Q 9,0 Ah bei CC-Ende; nach 62,8 min CV 25,9 Ah, Ziel 64,7 Ah) | **verfehlt / nicht belastbar**: Modell am SOC-Ende unbrauchbar (fDp an Fitgrenze) |
| 3 | 4680 DCIR 5,4–7 mΩ (W24) | 6,40 mΩ 25 °C, 7,93 mΩ 10 °C, 5,13 mΩ 40 °C (`ergebnis_dcir.json` n4680_*) | im Band, daher **keine Kalibrierung**; W20 Abb. 8 liegt nicht als Zahl vor (siehe offen) |
| 3 | 4680 10→80 % in 30 min bei Startstrom ≈ 1,7–2,0C | 1,5C: 29,68 min; 1,3C: 32,97 min; 1,7C: 26,55; 1,8C: 25,79; 1,9C: 24,96 min (`ergebnis_schnellladen_n4680.json`). ≥ 2,0C Solverabbruch, nicht ausgewertet | 30 min schon ab 1,5C (unter Erwartung 1,7–2,0C) |
| 3 | 4680 Wärme ≈ 8–12 W (K1b 6,7 W) | 1,5C: gesamt 7,37 W, I·|ΔU| 11,49 W; 1,8C: 9,74 / 15,10 W | gesamt knapp unter, I·ΔU im Band |
| 3 | Plating-Grenze könnte 30 min verhindern | Anodenpotential min. −0,031 V (1C) … −0,088 V (1,9C): in **allen** gültigen Läufen < 0 V (`phi_an_min_V`) | Grenze bei Chen2020/4,3 V schon bei 1C verletzt |
| Verfehlt | RMS > 30 mV | Temperaturstufe c: 157,8 mV | **eingetreten** (Rückgabe an Opus) |

## Offen / Auffälligkeiten (an Opus)
1. **Stufe (a) OCV:** Prada2013-OCV weicht von Test#5-Ruhespannung um 143 mV RMS ab (`ocv_rms_mV_vorher`), affine SOC-Abbildung nur auf 102 mV, Fit an Grenze a = 0,2 → nicht verwendet (SOC = Messung). Ruhespannung 3,29 V (50 %) gegen Modell 3,27 V; Modell-OCV bei 100 % 3,60 V gegen Messung 3,43–3,52 V. Ein anderer LFP-Materialsatz wäre nötig (Entscheidung Opus).
2. **Stufe (b):** Fit nur auf 15–90 % SOC (Pulse bei 5–10 % und 95 % brachen das unkalibrierte Modell ab: Spannung < 2,6 V). Parameter an Fitgrenzen: fjp = 100, fDp = 0,001, Rc = 0,70 mΩ (`b_parameter`). Fitgrenzen sind meine Wahl (Annahme A2), ohne Beleg. Der Parametersatz ist damit **nicht eindeutig** und außerhalb 15–90 % SOC nicht gültig.
3. **Stufe (c):** Temperaturreihe verfehlt. Modell bleibt bei −7 °C und 3 °C mit R10 1,30 / 1,01 mΩ weit unter Messung 1,71 / 1,30 mΩ; RMS 152 / 122 mV im Kalibriersatz. Ursache vermutlich: Temperaturabhängigkeit sitzt im Kontaktwiderstand/Elektrolyt, nicht in D (Ea_D blieb bei Startwert). Ea-Werte (`c_Ea_kJ_mol`: k 46,3; Dp 10,0; Dn 18,4; Rc 1,1 kJ/mol) sind nicht belastbar (Fit nicht konvergiert). Eigene Erweiterung Ea_Rc (A4).
4. **1C-Kapazität:** Modell 114 Ah (1C bis 2,6 V) gegen Rohdaten ≈ 132 Ah; C/20 auf 135 Ah skaliert (`kapazitaet_C20_Ah` 135,0). Prada-Schichten (Kathode 80 µm) liefern 1,2 mAh/cm² gegen 3,39 mAh/cm² Teardown (W28, usablewatts, bestanden) – Elektrodenfläche daher rechnerisch viel zu groß (Breite 129 m); nur Skalierung, keine Geometrie aus Akten.
5. **LFP-Schnellladen:** Ergebnis wegen Punkt 2 nicht belastbar; K1 für LFP daher nicht aus diesem Modell neu bestimmen.
6. **4680:** Parameter Chen2020 unkalibriert (DCIR im Band). Läufe ≥ 2,0C: Solver-Abbruch beim CV-Schritt (2,0C) bzw. unplausibel (2,3C: 54,6 °C, CV ab 52 s), Spalte `solver_ok`. Wärme gesamt (PyBaMM) und I·ΔU unterscheiden sich um 56 % (wie C1). Lumped-Kühlung: K0/K1-Annahme (Boden 1,66e-3 m², h 500 W/m²K).
7. **W28:** 11 Zeilen (BYD-4680-Zitate iopscience, Z11–Z21) nicht verwendet; verwendet nur 3,39 mAh/cm² und 82 µm als Vergleich (nicht eingesetzt). Elektrolytkonzentration, Separatordicke: „nicht gefunden“, daher Prada-/Chen-Werte als Annahme.
8. **W20 Abb. 8 (DCIR)** nicht als Zahl in W20.md; Kalibrierziel 4680 daher nur W24 (5,4–7 mΩ).
9. **xlsx lesen:** `openpyxl` 3.1.5 ins venv installiert (nicht in requirements.txt eingetragen).
10. Erste Läufe mit falschem Modell (Kontaktwiderstand ohne Option wirkungslos, SOC-Abbildung geclippt) wurden verworfen; Vorlauf-Stände: `ergebnis_blade_lauf1.json`, `kalibrierung_pulse_lauf1.csv`.

## Dateien
`daten_blade.py`, `xlsx_zu_csv.py`, `parameter_blade.py`, `kern.py`, `kalibrieren.py` (`--c`: Stufen a,b aus Vorlauf), `dcir.py`, `schnellladen.py` (`lfp` | `n4680`), `bilder.py`, `eingaben.json`, `blade_pulse.csv`, `kalibrierung_pulse.csv`, `schnellladen_Q_t.csv`, `ergebnis_*.json`, Bilder `blade_widerstand.png`, `kalibrierung_blade.png`, `dcir_vergleich.png`, `schnellladen_4680.png`, `waerme_vergleich.png`, `lesehilfe.md`, Baustein `praesentation/bausteine/C2.md`. Logs `kal.log`, `n4680.log`, `daten.log`.

*KI-generiert, Entwurf.*
