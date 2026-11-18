| Dok.-Nr. | ERG-K1 | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Ergebnis K1: Schnellladen, Ladeprofile, Kühlvarianten (Elmer, Fortsetzung K0) | Ersteller | Claude Sonnet (KI), Auftrag Opus | Prüfer | – (Opus offen) |

> **KI-generiert.** Entwurf, nicht vom Menschen freigegeben. Stand 2026-11-17. Alle Zahlen aus `sim/kuehlung/k1_schnellladen/ergebnis.json` (erzeugt von `k1_auswertung.py` aus `elmer/fall_*/`). Keine Deutung; Vergleich mit `ERWARTUNG.md` Punkt für Punkt unten. Vorgabe REQ-P09 (Annahme, offen): T_max ≤ 45 °C, Spreizung ≤ 5 K. ΔT = Kernmaximum minus Kernminimum (wie K0 `dT_kern`).

## 1 Abgleich P0 mit K0 L2 (Stoppkriterium > 0,3 K)

| Variante | T_max K1 P0 | T_max K0 L2 | Abw. | ΔT K1 P0 | ΔT K0 L2 | Abw. | Fundstelle K0 |
|---|---|---|---|---|---|---|---|
| LFP | 43.065 °C | 43.065 °C | +0.0000 K | 10.594 K | 10.594 K | +0.0000 K | sim/kuehlung/k0_zelle/ergebnis.json faelle.LFP_K1_L2 |
| NMC | 53.409 °C | 53.615 °C | -0.2059 K | 15.694 K | 16.042 K | -0.3478 K | sim/kuehlung/k0_zelle/ergebnis.json faelle.NMC_K1_L2 |

NMC-Netz: nach dem Nachtrag (Abschnitt 7) auf dem aktuellen CAD-Stand (Kernloch r 6,25 mm, V_kern 111 711 mm³). Der erste Lauf (K0-Stand r 7,0 mm) steht in `ergebnis_vor_nachtrag.json` / `ERGEBNIS_vor_nachtrag.md`. Die NMC-Abweichung zu K0 L2 oben ist deshalb Geometrie, nicht Rechenfehler.

## 2 Ergebnistabellen (alle Fälle)

Kühlung Boden h 500 und Start 25 °C, wenn im Fallnamen nichts anderes steht (Kh = h in W/(m²K), K3 = Boden und Oben gekühlt, V15 = Start und Kühlmittel 15 °C). t > Schwelle: linear interpolierte Zeit über der Schwelle. Bilanz: (Kühlrand-Integral + gespeicherte Energie − ∫Q dt) / ∫Q dt.

### LFP

| Fall | I-Profil | Ladezeit | T_max-Spitze (t) | ΔT-Spitze (t) | T_max Ladeende | ΔT Ladeende | ΔT Mittel | t > 45 °C | t > 5 K | ∫Q dt | Q rel. P0 | Bilanz | Laufzeit |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| LFP_P0 | 2.1C 0-1200s | 20 min | 43.1 °C (1200 s) | 10.6 K (1200 s) | 43.1 °C | 10.6 K | 6.4 K | 0 s | 805 s | 66.01 kJ | 1.000 | -0.008 % | 25 s |
| LFP_P1 | 3C 0-360s; 2C 360-810s; 1.38C 810-1200s | 20 min | 44.1 °C (810 s) | 11.3 K (810 s) | 40.4 °C | 9.4 K | 8.8 K | 0 s | 1010 s | 72.20 kJ | 1.094 | +0.598 % | 17 s |
| LFP_P2 | 4.2C 0-30s; 0C 30-60s; 4.2C 60-90s …(Takt 60 s) | 20 min | 61.7 °C (1170 s) | 21.3 K (1180 s) | 60.7 °C | 21.2 K | 13.1 K | 768 s | 1018 s | 132.02 kJ | 2.000 | +0.413 % | 45 s |
| LFP_P3 | 1.68C 0-1500s | 25 min | 37.5 °C (1500 s) | 7.4 K (1500 s) | 37.5 °C | 7.4 K | 4.7 K | 0 s | 801 s | 52.81 kJ | 0.800 | -0.007 % | 22 s |
| LFP_P4 | 1.4C 0-1800s | 30 min | 34.1 °C (1800 s) | 5.4 K (1800 s) | 34.1 °C | 5.4 K | 3.6 K | 0 s | 409 s | 44.01 kJ | 0.667 | -0.005 % | 32 s |
| LFP_P0_Kh1000 | 2.1C 0-1200s | 20 min | 39.7 °C (1200 s) | 10.8 K (1200 s) | 39.7 °C | 10.8 K | 7.1 K | 0 s | 891 s | 66.01 kJ | 1.000 | -0.014 % | 27 s |
| LFP_P0_Kh2000 | 2.1C 0-1200s | 20 min | 37.4 °C (1200 s) | 10.5 K (1200 s) | 37.4 °C | 10.5 K | 7.4 K | 0 s | 936 s | 66.01 kJ | 1.000 | -0.021 % | 26 s |
| LFP_P0_K3 | 2.1C 0-1200s | 20 min | 33.8 °C (1200 s) | 4.6 K (1200 s) | 33.8 °C | 4.6 K | 3.4 K | 0 s | 0 s | 66.01 kJ | 1.000 | -0.016 % | 25 s |
| LFP_P0_V15 | 2.1C 0-1200s | 20 min | 33.1 °C (1200 s) | 10.6 K (1200 s) | 33.1 °C | 10.6 K | 6.4 K | 0 s | 805 s | 66.01 kJ | 1.000 | -0.008 % | 31 s |
| LFP_P1_K3 | 3C 0-360s; 2C 360-810s; 1.38C 810-1200s | 20 min | 37.6 °C (360 s) | 6.3 K (380 s) | 30.4 °C | 3.0 K | 4.4 K | 0 s | 502 s | 72.20 kJ | 1.094 | +0.584 % | 31 s |
| LFP_P0_K3h1000 | 2.1C 0-1200s | 20 min | 30.8 °C (1200 s) | 3.8 K (1200 s) | 30.8 °C | 3.8 K | 3.1 K | 0 s | 0 s | 66.01 kJ | 1.000 | -0.027 % | 30 s |
| LFP_P0_K3_R128 | 2.1C 0-1200s | 20 min | 32.7 °C (1200 s) | 4.0 K (1200 s) | 32.7 °C | 4.0 K | 3.0 K | 0 s | 0 s | 57.83 kJ | 0.876 | -0.016 % | 14 s |

### NMC

| Fall | I-Profil | Ladezeit | T_max-Spitze (t) | ΔT-Spitze (t) | T_max Ladeende | ΔT Ladeende | ΔT Mittel | t > 45 °C | t > 5 K | ∫Q dt | Q rel. P0 | Bilanz | Laufzeit |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| NMC_P0 | 2.1C 0-1200s | 20 min | 53.4 °C (1200 s) | 15.7 K (1200 s) | 53.4 °C | 15.7 K | 9.3 K | 556 s | 931 s | 18.39 kJ | 1.000 | -0.008 % | 204 s |
| NMC_P1 | 3C 0-360s; 2C 360-810s; 1.38C 810-1200s | 20 min | 54.9 °C (810 s) | 16.6 K (810 s) | 49.8 °C | 14.1 K | 12.9 K | 938 s | 1059 s | 20.12 kJ | 1.094 | +0.599 % | 196 s |
| NMC_P2 | 4.2C 0-30s; 0C 30-60s; 4.2C 60-90s …(Takt 60 s) | 20 min | 82.5 °C (1170 s) | 31.6 K (1180 s) | 81.2 °C | 31.4 K | 19.1 K | 946 s | 1069 s | 36.79 kJ | 2.000 | +0.413 % | 373 s |
| NMC_P3 | 1.68C 0-1500s | 25 min | 44.9 °C (1500 s) | 11.0 K (1500 s) | 44.9 °C | 11.0 K | 6.9 K | 0 s | 1070 s | 14.72 kJ | 0.800 | -0.006 % | 245 s |
| NMC_P4 | 1.4C 0-1800s | 30 min | 39.6 °C (1800 s) | 8.1 K (1800 s) | 39.6 °C | 8.1 K | 5.3 K | 0 s | 1118 s | 12.26 kJ | 0.667 | -0.005 % | 278 s |
| NMC_P0_Kh1000 | 2.1C 0-1200s | 20 min | 49.0 °C (1200 s) | 17.3 K (1200 s) | 49.0 °C | 17.3 K | 11.1 K | 434 s | 999 s | 18.39 kJ | 1.000 | -0.012 % | 185 s |
| NMC_P0_Kh2000 | 2.1C 0-1200s | 20 min | 46.0 °C (1200 s) | 17.8 K (1200 s) | 46.0 °C | 17.8 K | 12.0 K | 209 s | 1033 s | 18.39 kJ | 1.000 | -0.018 % | 186 s |
| NMC_P0_K3 | 2.1C 0-1200s | 20 min | 38.9 °C (1200 s) | 5.8 K (1200 s) | 38.9 °C | 5.8 K | 4.3 K | 0 s | 586 s | 18.39 kJ | 1.000 | -0.014 % | 194 s |
| NMC_P0_V15 | 2.1C 0-1200s | 20 min | 43.4 °C (1200 s) | 15.7 K (1200 s) | 43.4 °C | 15.7 K | 9.3 K | 0 s | 931 s | 18.39 kJ | 1.000 | -0.008 % | 196 s |
| NMC_P1_K3 | 3C 0-360s; 2C 360-810s; 1.38C 810-1200s | 20 min | 44.3 °C (360 s) | 8.0 K (380 s) | 33.8 °C | 3.7 K | 5.5 K | 0 s | 762 s | 20.12 kJ | 1.094 | +0.587 % | 175 s |
| NMC_P0_K3h1000 | 2.1C 0-1200s | 20 min | 34.6 °C (1200 s) | 5.7 K (1200 s) | 34.6 °C | 5.7 K | 4.7 K | 0 s | 751 s | 18.39 kJ | 1.000 | -0.023 % | 168 s |
| NMC_P3_Kh2000 | 1.68C 0-1500s | 25 min | 39.0 °C (1500 s) | 11.9 K (1500 s) | 39.0 °C | 11.9 K | 8.5 K | 0 s | 1230 s | 14.72 kJ | 0.800 | -0.015 % | 183 s |
| NMC_P3_K3 | 1.68C 0-1500s | 25 min | 34.0 °C (1500 s) | 3.8 K (1500 s) | 34.0 °C | 3.8 K | 3.0 K | 0 s | 0 s | 14.72 kJ | 0.800 | -0.011 % | 181 s |
| NMC_P0_K3b | 2.1C 0-1200s | 20 min | 42.8 °C (1200 s) | 8.1 K (1200 s) | 42.8 °C | 8.1 K | 5.6 K | 0 s | 802 s | 18.39 kJ | 1.000 | -0.011 % | 73 s |
| NMC_P3_K3b | 1.68C 0-1500s | 25 min | 36.8 °C (1500 s) | 5.4 K (1500 s) | 36.8 °C | 5.4 K | 3.9 K | 0 s | 490 s | 14.72 kJ | 0.800 | -0.009 % | 90 s |
| NMC_P4_K3b | 1.4C 0-1800s | 30 min | 33.3 °C (1800 s) | 3.8 K (1800 s) | 33.3 °C | 3.8 K | 2.9 K | 0 s | 0 s | 12.26 kJ | 0.667 | -0.007 % | 109 s |
| NMC_P3_K3b_phi03 | 1.68C 0-1500s | 25 min | 38.6 °C (1500 s) | 6.6 K (1500 s) | 38.6 °C | 6.6 K | 4.6 K | 0 s | 817 s | 14.72 kJ | 0.800 | -0.008 % | 92 s |
| NMC_P3_K3b_phi07 | 1.68C 0-1500s | 25 min | 35.6 °C (1500 s) | 4.7 K (1500 s) | 35.6 °C | 4.7 K | 3.5 K | 0 s | 0 s | 14.72 kJ | 0.800 | -0.010 % | 88 s |
| NMC_P3_K3b_kpad1 | 1.68C 0-1500s | 25 min | 37.7 °C (1500 s) | 6.0 K (1500 s) | 37.7 °C | 6.0 K | 4.3 K | 0 s | 706 s | 14.72 kJ | 0.800 | -0.008 % | 88 s |
| NMC_P3_K3b_kpad6 | 1.68C 0-1500s | 25 min | 36.5 °C (1500 s) | 5.2 K (1500 s) | 36.5 °C | 5.2 K | 3.8 K | 0 s | 373 s | 14.72 kJ | 0.800 | -0.009 % | 88 s |
| NMC_C2gesamt_K3b | 1.5C 0-300s; 1.5C 300-600s; 1.5C 600-900s …(Takt 60 s) | 29 min | 34.0 °C (1321 s) | 4.2 K (1331 s) | 32.9 °C | 3.7 K | 3.2 K | 0 s | 0 s | 12.50 kJ | nan | +0.077 % | 98 s |
| NMC_C2idu_K3b | 1.5C 0-300s; 1.5C 300-600s; 1.5C 600-900s …(Takt 60 s) | 29 min | 39.1 °C (1321 s) | 6.5 K (1331 s) | 37.4 °C | 5.8 K | 4.9 K | 0 s | 1124 s | 19.50 kJ | nan | +0.077 % | 99 s |

## 3 Wärmeintegral gegen Tabelle (Prüfung ±2 %)

| Fall | ∫Q dt (Schrittsumme) | ∫Q dt exakt aus Stufen | Q rel. P0 | Tabelle ERWARTUNG | Abw. | Prüfung |
|---|---|---|---|---|---|---|
| LFP_P0 | 66012.4 J | 66012.4 J | 1.0000 | 1.0 | +0.00 % | ≤ 2 % erfüllt |
| LFP_P1 | 72195.7 J | 72195.7 J | 1.0937 | 1.09 | +0.34 % | ≤ 2 % erfüllt |
| LFP_P2 | 132024.8 J | 132024.8 J | 2.0000 | 2.0 | +0.00 % | ≤ 2 % erfüllt |
| LFP_P3 | 52809.9 J | 52809.9 J | 0.8000 | 0.8 | -0.00 % | ≤ 2 % erfüllt |
| LFP_P4 | 44008.3 J | 44008.3 J | 0.6667 | 0.6667 | -0.00 % | ≤ 2 % erfüllt |
| NMC_P0 | 18394.9 J | 18394.9 J | 1.0000 | 1.0 | +0.00 % | ≤ 2 % erfüllt |
| NMC_P1 | 20117.9 J | 20117.9 J | 1.0937 | 1.09 | +0.34 % | ≤ 2 % erfüllt |
| NMC_P2 | 36789.7 J | 36789.7 J | 2.0000 | 2.0 | +0.00 % | ≤ 2 % erfüllt |
| NMC_P3 | 14715.9 J | 14715.9 J | 0.8000 | 0.8 | -0.00 % | ≤ 2 % erfüllt |
| NMC_P4 | 12263.2 J | 12263.2 J | 0.6667 | 0.6667 | -0.00 % | ≤ 2 % erfüllt |

Größte Abweichung: 0.34 %. (Tabellenwerte in `eingaben.json` aus ERWARTUNG; P1 letzte Stufe 1,3846C = 0,15/(390/3600), Tabelle 1,385C.)

## 4 Abgleich mit ERWARTUNG.md, Punkt für Punkt

Bereichsangaben (a–b) werden mit erfüllt/verfehlt bewertet; Angaben mit „≈“ nur als Abweichung (keine Toleranz in ERWARTUNG festgelegt). Deutung bleibt bei Opus.

### Profile

| Punkt | Erwartung (ERWARTUNG.md) | Ergebnis | Bewertung |
|---|---|---|---|
| LFP P0 | 43.1 °C / 10.6 K | 43.1 °C / 10.6 K | ≈: Abw. -0.0 K / -0.0 K |
| NMC P0 | 53.6 °C / 16.0 K | 53.4 °C / 15.7 K | ≈: Abw. -0.2 K / -0.3 K |
| LFP P1 | Spitze ΔT ≈ 10–12 K (während 3C), Ende ≈ 5–7 K; T_max ± 2 K zu P0 | Spitze 11.3 K bei 810 s; Ende 9.4 K; T_max-Ende 40.4 (P0 43.1, Diff -2.7 K), Spitze 44.1 | Spitze ΔT 10–12: erfüllt; Ende 5–7: verfehlt; T_max ±2 K: verfehlt |
| NMC P1 | ähnlich, Spitze ΔT ≈ 15–18 K | Spitze 16.6 K bei 810 s; Ende 14.1 K; T_max-Ende 49.8 (P0 53.4) | Spitze ΔT 15–18: erfüllt |
| LFP P2 | T_max ≈ 55–60 °C, ΔT schwankt um ≈ 20 K | T_max-Spitze 61.7 °C (Ende 60.7); ΔT Spitze 21.3 K, Mittel 13.1 K, Min in 2. Hälfte 14.2 K | T_max 55–60: verfehlt; ΔT-Mittel ≈ 20: Abw. -6.9 K |
| NMC P2 | T_max ≈ 75–85 °C, schlechter als P0 | T_max-Spitze 82.5 °C (Ende 81.2); ΔT Spitze 31.6 K, Mittel 19.1 K, Min in 2. Hälfte 20.8 K | T_max 75–85: erfüllt; schlechter als P0 (P0 53.4 °C): erfüllt |
| LFP P3 | ≈ 40 °C / ≈ 7–8 K | 37.5 °C / 7.4 K (Spitze ΔT 7.4 K) | T_max Abw. -2.5 K; ΔT 7–8: erfüllt |
| NMC P3 | ≈ 47–50 °C / ≈ 11–13 K | 44.9 °C / 11.0 K (Spitze ΔT 11.0 K) | T_max 47–50: verfehlt; ΔT 11–13: erfüllt |
| LFP P4 | ≈ 37 °C / ≈ 5–6 K | 34.1 °C / 5.4 K (Spitze ΔT 5.4 K) | T_max Abw. -2.9 K; ΔT 5–6: erfüllt |
| NMC P4 | ≈ 42–44 °C / ≈ 8–9 K | 39.6 °C / 8.1 K (Spitze ΔT 8.1 K) | T_max 42–44: verfehlt; ΔT 8–9: erfüllt |

Nicht gerechnet in K1 (nicht Teil des Auftrags): „Stationär nötig für 5 K: LFP ≤ 1,29C, NMC ≤ 1,02C“.

### Kühlung (Profil P0, Differenz zu P0 derselben Variante)

| Punkt | Erwartung | Ergebnis | Bewertung |
|---|---|---|---|
| LFP Kh1000 | T_max −3…−5 K, ΔT unverändert | T_max 39.7 °C (-3.4 K), ΔT 10.8 K (+0.20 K) | T_max-Änderung -5…-3: erfüllt; ΔT-Änderung +0.20 K |
| LFP Kh2000 | T_max −5…−8 K, ΔT unverändert | T_max 37.4 °C (-5.7 K), ΔT 10.5 K (-0.07 K) | T_max-Änderung -8…-5: erfüllt; ΔT-Änderung -0.07 K |
| LFP K3 | ΔT ≈ ÷4 → ≈ 3 K ✓, T_max ≈ 35 °C ✓ | T_max 33.8 °C, ΔT 4.6 K | ΔT-Verhältnis K3/P0 = 0.433; verfehlt-Kriterium „ΔT sinkt um weniger als die Hälfte“: nicht eingetreten; ΔT ≈ 3: Abw. +1.6 K; T_max ≈ 35: Abw. -1.2 K |
| LFP V15 | T_max −10 K, ΔT unverändert | T_max 33.1 °C (-10.00 K), ΔT 10.6 K (+0.000 K) | T_max −10: erfüllt; ΔT-Änderung +0.000 K |
| NMC Kh1000 | T_max −8…−10 K, ΔT unverändert | T_max 49.0 °C (-4.4 K), ΔT 17.3 K (+1.63 K) | T_max-Änderung -10…-8: verfehlt; ΔT-Änderung +1.63 K |
| NMC Kh2000 | T_max ≈ 41–44 °C ✓, ΔT ≈ 16 K ✗ | T_max 46.0 °C (-7.4 K), ΔT 17.8 K (+2.08 K) | T_max 41–44: verfehlt; ΔT ≈ 16: Abw. +1.8 K; ΔT-Änderung +2.08 K |
| NMC K3 | ΔT ≈ 4–5 K (knapp), T_max ≈ 38–40 °C ✓ | T_max 38.9 °C, ΔT 5.8 K | ΔT-Verhältnis K3/P0 = 0.368; ΔT 4–5: verfehlt; T_max 38–40: erfüllt |
| NMC V15 | T_max −10 K, ΔT unverändert | T_max 43.4 °C (-10.00 K), ΔT 15.7 K (-0.000 K) | T_max −10: erfüllt; ΔT-Änderung -0.000 K |

Modellfakt zu NMC K3 (Nachtrag): Zwischen Wickel (z 76 mm) und Deckel (z 79,6 mm) liegt bei K3/K3h1000 die Tab-Scheibe statt Luft (Abschnitt 7); bei allen anderen NMC-Fällen bleibt Luft (k = 0,026). Bei LFP liegt der Kern mit Gehäusewand (0,3 mm Al) direkt an Boden und Oben.


### Kombinationen

| Fall | Erwartung | Ergebnis (Ladeende; Spitzen) | Vorgaben T_max ≤ 45 °C / ΔT ≤ 5 K (Spitzenwerte) |
|---|---|---|---|
| LFP_P0_K3 | siehe oben (K3 allein) | T_max 33.8 °C (Spitze 33.8), ΔT 4.6 K (Spitze 4.6) | T_max erfüllt; ΔT erfüllt |
| LFP_P1_K3 | LFP K3 erfüllt beides bei 20 min | T_max 30.4 °C (Spitze 37.6), ΔT 3.0 K (Spitze 6.3) | T_max erfüllt; ΔT verfehlt |
| LFP_P0_K3h1000 | LFP K3 erfüllt beides bei 20 min | T_max 30.8 °C (Spitze 30.8), ΔT 3.8 K (Spitze 3.8) | T_max erfüllt; ΔT erfüllt |
| NMC_P0_K3 | siehe oben (K3 allein) | T_max 38.9 °C (Spitze 38.9), ΔT 5.8 K (Spitze 5.8) | T_max erfüllt; ΔT verfehlt |
| NMC_P1_K3 | NMC braucht K3 + h ≥ 1000 oder K3 + P3 | T_max 33.8 °C (Spitze 44.3), ΔT 3.7 K (Spitze 8.0) | T_max erfüllt; ΔT verfehlt |
| NMC_P0_K3h1000 | NMC braucht K3 + h ≥ 1000 oder K3 + P3 | T_max 34.6 °C (Spitze 34.6), ΔT 5.7 K (Spitze 5.7) | T_max erfüllt; ΔT verfehlt |
| NMC_P3_K3 | NMC K3 + P3 (Erwartung: reicht) | T_max 34.0 °C (Spitze 34.0), ΔT 3.8 K (Spitze 3.8) | T_max erfüllt; ΔT erfüllt |
| NMC_P3_Kh2000 | (Kombination aus ERWARTUNG; Einzelwert nicht angegeben) | T_max 39.0 °C (Spitze 39.0), ΔT 11.9 K (Spitze 11.9) | T_max erfüllt; ΔT verfehlt |

### Als „Verfehlt“ in ERWARTUNG definiert

- Wärmeintegral > 2 % von Tabelle: größte Abweichung 0.34 % → nicht eingetreten.
- P0 weicht > 0,3 K von K0 L2 ab (LFP): Abw. T +0.0000 K, ΔT +0.0000 K → nicht eingetreten.
- P0 weicht > 0,3 K von K0 L2 ab (NMC): Abw. T -0.2059 K, ΔT -0.3478 K → EINGETRETEN.
- K3 senkt ΔT bei LFP um weniger als die Hälfte: ΔT 10.6 → 4.6 K (−57 %) → nicht eingetreten.

## 7 Nachtrag (Auftrag Opus): NMC-Netz aktuell, NMC K3 mit Tab-Scheibe

- Änderung 1: NMC-Netz auf aktuelles CAD (Kernloch r 6,25 mm statt 7,0 mm), alle 13 NMC-Fälle neu gerechnet; LFP unverändert.
- Neuer Abgleich NMC P0 (K1, neues Netz) gegen K0 L2 (altes Netz, `sim/kuehlung/k0_zelle/ergebnis.json faelle.NMC_K1_L2`): T_max 53.409 gegen 53.615 °C (-0.206 K), ΔT 15.694 gegen 16.042 K (-0.348 K). Die 0,3-K-Grenze gilt für gleiches Netz (Abgleich vorher: 0,0000 K); hier ist die Abweichung die Wirkung der Geometrieänderung.
- Änderung 2: NMC K3/K3h1000: Raum Wickel–Deckel (Höhe g = 3.6 mm) statt Luft als Tab-Scheibe. Annahme Opus: 0.3 mm Al flächig (k 237) plus Kontaktschicht 0.1 mm, k 1 W/(m K). Unten liegt im Modell keine Luft (Raum Becherboden–Wickel ist Kernmaterial), dort daher keine Scheibe. Umsetzung (Annahme des Umsetzers, bitte prüfen): in der Ebene k_xy = 19.77, senkrecht k_z = 31.37 W/(m K) (Scheibe überbrückt den Raum als Leiter, Kontaktschicht in Reihe).

| NMC-Fall | vorher (K0-Netz, K3 mit Luft) T_max / ΔT (Spitze) | jetzt (neues Netz, K3 mit Tab) T_max / ΔT (Spitze) | Differenz T_max / ΔT |
|---|---|---|---|
| NMC_C2gesamt_K3b (neu) | – | 34.0 °C / 4.2 K | – |
| NMC_C2idu_K3b (neu) | – | 39.1 °C / 6.5 K | – |
| NMC_P0 | 53.6 °C / 16.0 K | 53.4 °C / 15.7 K | -0.2 K / -0.3 K |
| NMC_P0_K3 | 47.9 °C / 12.3 K | 38.9 °C / 5.8 K | -9.0 K / -6.5 K |
| NMC_P0_K3b (neu) | – | 42.8 °C / 8.1 K | – |
| NMC_P0_K3h1000 | 44.0 °C / 13.5 K | 34.6 °C / 5.7 K | -9.4 K / -7.8 K |
| NMC_P0_Kh1000 | 49.3 °C / 17.7 K | 49.0 °C / 17.3 K | -0.3 K / -0.3 K |
| NMC_P0_Kh2000 | 46.3 °C / 18.1 K | 46.0 °C / 17.8 K | -0.3 K / -0.3 K |
| NMC_P0_V15 | 43.6 °C / 16.0 K | 43.4 °C / 15.7 K | -0.2 K / -0.3 K |
| NMC_P1 | 55.1 °C / 17.0 K | 54.9 °C / 16.6 K | -0.2 K / -0.4 K |
| NMC_P1_K3 | 50.1 °C / 13.5 K | 44.3 °C / 8.0 K | -5.8 K / -5.5 K |
| NMC_P2 | 82.9 °C / 32.3 K | 82.5 °C / 31.6 K | -0.4 K / -0.7 K |
| NMC_P3 | 45.0 °C / 11.3 K | 44.9 °C / 11.0 K | -0.2 K / -0.3 K |
| NMC_P3_K3 (neu) | – | 34.0 °C / 3.8 K | – |
| NMC_P3_K3b (neu) | – | 36.8 °C / 5.4 K | – |
| NMC_P3_K3b_kpad1 (neu) | – | 37.7 °C / 6.0 K | – |
| NMC_P3_K3b_kpad6 (neu) | – | 36.5 °C / 5.2 K | – |
| NMC_P3_K3b_phi03 (neu) | – | 38.6 °C / 6.6 K | – |
| NMC_P3_K3b_phi07 (neu) | – | 35.6 °C / 4.7 K | – |
| NMC_P3_Kh2000 | 39.2 °C / 12.1 K | 39.0 °C / 11.9 K | -0.2 K / -0.2 K |
| NMC_P4 | 39.7 °C / 8.3 K | 39.6 °C / 8.1 K | -0.1 K / -0.2 K |
| NMC_P4_K3b (neu) | – | 33.3 °C / 3.8 K | – |

Vorgaben (Spitzenwerte T_max ≤ 45 °C, ΔT ≤ 5 K) für die K3-Fälle: NMC_P0_K3: T_max erfüllt, ΔT verfehlt; NMC_P0_K3h1000: T_max erfüllt, ΔT verfehlt; NMC_P3_K3: T_max erfüllt, ΔT erfüllt; NMC_P1_K3: T_max erfüllt, ΔT verfehlt.

Hinweis: Die Bewertungen in Abschnitt 4 gelten für die neuen Zahlen. Bilder und Landkarte sind aktualisiert.

## 5 Laufzeiten

Summe Einzelläufe (Elmer + Nachlauf) 65.2 min CPU, 4 Läufe parallel (nice 10, 1 Kern je Lauf); P0-Gate separat. Je Fall: Tabelle in Abschnitt 2, Spalte Laufzeit.

## 6 Bilder

`profile.png`, `verlauf_profile_LFP.png`, `verlauf_profile_NMC.png`, `verlauf_kuehlung_LFP.png`, `verlauf_kuehlung_NMC.png`, `landkarte.png` (Lesehilfe `k1_lesehilfe.md`); Render (Blender Cycles CPU, Endzustand): `bilder/render_LFP_P0_K3h1000_ende.png` (Fall mit niedrigster T_max unter den beide-erfüllenden LFP-Fällen), `bilder/render_NMC_P4_ende.png` (kein NMC-Fall erfüllt beide; bester = T_max ≤ 45 °C mit kleinster ΔT-Spitze); Lesehilfe `bilder/render_lesehilfe.md`. Die obere Kühlplatte (K3) ist im Render nicht gezeichnet; LFP-Render wirkt dunkel wegen der festen Skala 25–55 °C.

## 8 Nachtrag K1b: 4680 obere Kühlung über Verbinder und Isolierpad (Annahme Opus, ENT-092…095 vorgeschlagen)

Modell: unten Boden h 500 über Becherboden + Tab-Scheibe (wie K3), oben Robin-Rand mit Ersatz-Wärmeübergang h_eff = φ / (1/h + t_pad/k_pad + t_v/k_v), h 500, t_pad 1 mm, Verbinder Al 1,5 mm (k 237). Werte in `eingaben.json` (Herkunft „Annahme Opus“, ERWARTUNG.md Nachtrag K1b). h_eff-Kontrolle: Wert aus `elmer/fall_*/case.sif` (Rand „Kuehlrand_Oben“) gegen Formel.

| Fall | φ | k_pad W/(m K) | h_eff Formel | h_eff in case.sif | Abw. | T_max-Spitze | ΔT-Spitze | T_max Ende | ΔT Ende | Bilanz | Laufzeit |
|---|---|---|---|---|---|---|---|---|---|---|---|
| NMC_P0_K3b | 0.5 | 3 | 213.7 | 213.7 | -0.00 % | 42.8 °C | 8.1 K | 42.8 °C | 8.1 K | -0.011 % | 73 s |
| NMC_P3_K3b | 0.5 | 3 | 213.7 | 213.7 | -0.00 % | 36.8 °C | 5.4 K | 36.8 °C | 5.4 K | -0.009 % | 90 s |
| NMC_P4_K3b | 0.5 | 3 | 213.7 | 213.7 | -0.00 % | 33.3 °C | 3.8 K | 33.3 °C | 3.8 K | -0.007 % | 109 s |
| NMC_P3_K3b_phi03 | 0.3 | 3 | 128.2 | 128.2 | -0.00 % | 38.6 °C | 6.6 K | 38.6 °C | 6.6 K | -0.008 % | 92 s |
| NMC_P3_K3b_phi07 | 0.7 | 3 | 299.2 | 299.2 | +0.00 % | 35.6 °C | 4.7 K | 35.6 °C | 4.7 K | -0.010 % | 88 s |
| NMC_P3_K3b_kpad1 | 0.5 | 1 | 166.3 | 166.3 | +0.00 % | 37.7 °C | 6.0 K | 37.7 °C | 6.0 K | -0.008 % | 88 s |
| NMC_P3_K3b_kpad6 | 0.5 | 6 | 230.1 | 230.1 | +0.00 % | 36.5 °C | 5.2 K | 36.5 °C | 5.2 K | -0.009 % | 88 s |

Größte h_eff-Abweichung Modell/Formel: 0.00 % (Verfehlt-Kriterium > 1 %: nicht eingetreten).

### Abgleich mit ERWARTUNG.md Nachtrag K1b

| Punkt | Erwartung | Ergebnis (Spitze T_max / ΔT) | Bewertung |
|---|---|---|---|
| NMC P0 K3b | 44–46 °C / 8–10 K (zwischen K1 53,6/16,0 und K3 38,9/5,8) | 42.8 °C / 8.1 K | T_max 44–46: verfehlt; ΔT 8–10: erfüllt; Verfehlt-Kriterium (T_max außerhalb 41–49): nicht eingetreten |
| NMC P3 K3b | 38–40 °C / 5,5–7 K → 5 K knapp verfehlt | 36.8 °C / 5.4 K | T_max 38–40: verfehlt; ΔT 5,5–7: verfehlt; ΔT ≤ 5 K: verfehlt |
| NMC P4 K3b | ≈ 35 °C / ≈ 4,5–5 K → knapp erfüllt | 33.3 °C / 3.8 K | T_max Abw. zu 35: -1.7 K; ΔT 4,5–5: verfehlt; ΔT ≤ 5 K: erfüllt |

Empfindlichkeit (Profil P3, Spitzenwerte; Vorgaben T_max ≤ 45 °C, ΔT ≤ 5 K):

| Fall | φ | k_pad | h_eff | T_max | ΔT | T_max-Vorgabe | ΔT-Vorgabe |
|---|---|---|---|---|---|---|---|
| NMC_P3_K3b_phi03 | 0.3 | 3 | 128.2 | 38.6 °C | 6.6 K | erfüllt | verfehlt |
| NMC_P3_K3b | 0.5 | 3 | 213.7 | 36.8 °C | 5.4 K | erfüllt | verfehlt |
| NMC_P3_K3b_phi07 | 0.7 | 3 | 299.2 | 35.6 °C | 4.7 K | erfüllt | erfüllt |
| NMC_P3_K3b_kpad1 | 0.5 | 1 | 166.3 | 37.7 °C | 6.0 K | erfüllt | verfehlt |
| NMC_P3_K3b_kpad6 | 0.5 | 6 | 230.1 | 36.5 °C | 5.2 K | erfüllt | verfehlt |

Vorgaben für alle K3b-Fälle (Spitzenwerte): NMC_P0_K3b: T_max erfüllt, ΔT verfehlt; NMC_P3_K3b: T_max erfüllt, ΔT verfehlt; NMC_P3_K3b_kpad1: T_max erfüllt, ΔT verfehlt; NMC_P3_K3b_kpad6: T_max erfüllt, ΔT verfehlt; NMC_P3_K3b_phi03: T_max erfüllt, ΔT verfehlt; NMC_P3_K3b_phi07: T_max erfüllt, ΔT erfüllt; NMC_P4_K3b: T_max erfüllt, ΔT erfüllt. Bilder: `landkarte.png` und `verlauf_kuehlung_NMC.png` enthalten NMC_P0_K3b bzw. die K3b-Zeilen. Keine Deutung (bei Opus).

## 9 Nachtrag K1c: Wärme aus C2 statt I²R-Schätzung (Annahme Opus, ERWARTUNG.md Nachtrag K1c)

Eingaben: LFP R 1,28 mΩ (Herkunft C2 `ergebnis_blade.json`, Test#5 Blade 10 s, 25 °C, 0,877 mΩ × 135/92,4); NMC Q(t) aus `sim/chemie/c2_kalibrierung/schnellladen_Q_t.csv` (4680, 1,5C, 7 Stützpunkte, linear interpoliert, Laufzeit bis letzter Stützpunkt 1720,8 s; 10→80 % wären 1780,8 s, die letzten 60 s fehlen in der CSV). Fall „I·ΔU“: CSV-Verlauf mit konstantem Faktor skaliert, sodass das Mittel dem I·ΔU-Mittel aus `ergebnis_schnellladen_n4680.json` entspricht (Faktor 1.5600); der Zeitverlauf von I·ΔU ist in C2 nicht gespeichert, die Skalierung ist eine Annahme. Kühlung NMC wie K3b (φ 0,5, k_pad 3).

| Fall | Quelle | ∫Q dt Elmer-Schrittsumme | ∫Q dt CSV (Trapez, ggf. skaliert) | Abw. | T_max-Spitze (t) | ΔT-Spitze | T_max Ende | ΔT Ende | Bilanz | Vorgabe T_max ≤ 45 / ΔT ≤ 5 K | Laufzeit |
|---|---|---|---|---|---|---|---|---|---|---|---|
| LFP_P0_K3_R128 | R 1,28 mOhm: C2 ergebnis_blade.json (Test#5 Blade 10 s 25 C 0,877 mOhm x 135/92,4), Auftrag Opus | 57832.7 J | 57832.7 J | +0.00 % | 32.7 °C (1200 s) | 4.02 K | 32.7 °C | 4.02 K | -0.016 % | T_max erfüllt; ΔT erfüllt | 14 s |
| NMC_C2gesamt_K3b | Q(t) Spalte Q_W schnellladen_Q_t.csv (4680, 1,5C), 'gesamt' (PyBaMM Total heating) | 12497.1 J | 12507.4 J | -0.08 % | 34.0 °C (1321 s) | 4.15 K | 32.9 °C | 3.69 K | +0.077 % | T_max erfüllt; ΔT erfüllt | 98 s |
| NMC_C2idu_K3b | Q(t) wie gesamt, Form skaliert auf I*dU-Mittel 11,49 W (ergebnis_schnellladen_n4680.json); Skalierung = Annahme, Zeitverlauf I*dU nicht gespeichert | 19495.6 J | 19511.7 J | -0.08 % | 39.1 °C (1321 s) | 6.48 K | 37.4 °C | 5.76 K | +0.077 % | T_max erfüllt; ΔT verfehlt | 99 s |

### Abgleich mit ERWARTUNG.md Nachtrag K1c

| Punkt | Erwartung | Ergebnis (Spitze) | Bewertung |
|---|---|---|---|
| LFP P0 K3, R 1,28 mΩ | ≈ 32,8 °C / ≈ 4,0 K (Skalierung ~0,87) | 32.7 °C / 4.02 K (R 1,46: 33.8 / 4.59); Wärme-Verhältnis 0.876 | T_max Abw. zu 32,8: -0.12 K; ΔT Abw. zu 4,0: +0.02 K |
| NMC K3b, Q gesamt (mittel 7,4 W) | ≈ 34–35 °C / 4,2–4,6 K (knapp erfüllt) | 34.0 °C / 4.15 K | T_max 34–35: erfüllt; ΔT 4,2–4,6: verfehlt; ΔT ≤ 5 K: erfüllt |
| NMC K3b, I·ΔU (mittel 11,5 W) | ≈ 38–40 °C / 6–7 K (5 K verfehlt) | 39.1 °C / 6.48 K | T_max 38–40: erfüllt; ΔT 6–7: erfüllt; ΔT ≤ 5 K: verfehlt |

Verfehlt-Kriterium „Wärmeintegral ≠ CSV ± 2 %“: größte Abweichung 0.08 % → nicht eingetreten. Bilder: `landkarte.png` enthält die drei K1c-Zeilen. Offen für Opus: (a) CSV endet bei 1720,8 s, Ladeende 80 % erst bei 1780,8 s; (b) I·ΔU-Verlauf nur als skalierte Form; (c) R 1,28 mΩ gilt bei 25 °C, 50 % SOC, 10 s (Temperaturabhängigkeit nicht berücksichtigt). Keine Deutung (bei Opus).

---
*KI-generiert (Claude Sonnet), Entwurf, nicht vom Menschen freigegeben. Erzeugt von k1_bericht.py.*
