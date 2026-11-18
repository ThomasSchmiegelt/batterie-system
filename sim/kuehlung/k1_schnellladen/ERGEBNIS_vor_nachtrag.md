| Dok.-Nr. | ERG-K1 | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Ergebnis K1: Schnellladen, Ladeprofile, Kühlvarianten (Elmer, Fortsetzung K0) | Ersteller | Claude Sonnet (KI), Auftrag Opus | Prüfer | – (Opus offen) |

> **KI-generiert.** Entwurf, nicht vom Menschen freigegeben. Stand 2026-11-17. Alle Zahlen aus `sim/kuehlung/k1_schnellladen/ergebnis.json` (erzeugt von `k1_auswertung.py` aus `elmer/fall_*/`). Keine Deutung; Vergleich mit `ERWARTUNG.md` Punkt für Punkt unten. Vorgabe REQ-P09 (Annahme, offen): T_max ≤ 45 °C, Spreizung ≤ 5 K. ΔT = Kernmaximum minus Kernminimum (wie K0 `dT_kern`).

## 1 Abgleich P0 mit K0 L2 (Stoppkriterium > 0,3 K)

| Variante | T_max K1 P0 | T_max K0 L2 | Abw. | ΔT K1 P0 | ΔT K0 L2 | Abw. | Fundstelle K0 |
|---|---|---|---|---|---|---|---|
| LFP | 43.065 °C | 43.065 °C | +0.0000 K | 10.594 K | 10.594 K | +0.0000 K | sim/kuehlung/k0_zelle/ergebnis.json faelle.LFP_K1_L2 |
| NMC | 53.615 °C | 53.615 °C | +0.0000 K | 16.042 K | 16.042 K | +0.0000 K | sim/kuehlung/k0_zelle/ergebnis.json faelle.NMC_K1_L2 |

Hinweis zum Netz: Das K0-Netz NMC wurde mit dem damaligen CAD-Stand erzeugt (Kernloch r 7,0 mm, Kern z 1…76 mm). Das aktuelle `cad/zelle/entwurf/parameter_NMC_entwurf.json` / `detail/ergebnis_detail_NMC.json` (geändert 12:10/12:16, nach dem K0-Netz 11:58) liefert r_loch 6,25 mm und V_kern 111 711 mm³ statt 109 357 mm³. K1 friert die Geometrie wie im K0-Netz ein (`k1_geometrie.py`, liest `../k0_zelle/elmer/netz_NMC_f1/netzinfo.json`), damit der Abgleich gilt. **Offene Frage an Opus:** K0-NMC-Ergebnisse mit dem aktuellen CAD-Stand neu rechnen?

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

### NMC

| Fall | I-Profil | Ladezeit | T_max-Spitze (t) | ΔT-Spitze (t) | T_max Ladeende | ΔT Ladeende | ΔT Mittel | t > 45 °C | t > 5 K | ∫Q dt | Q rel. P0 | Bilanz | Laufzeit |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| NMC_P0 | 2.1C 0-1200s | 20 min | 53.6 °C (1200 s) | 16.0 K (1200 s) | 53.6 °C | 16.0 K | 9.5 K | 560 s | 936 s | 18.39 kJ | 1.000 | -0.008 % | 114 s |
| NMC_P1 | 3C 0-360s; 2C 360-810s; 1.38C 810-1200s | 20 min | 55.1 °C (810 s) | 17.0 K (810 s) | 50.1 °C | 14.4 K | 13.2 K | 938 s | 1061 s | 20.12 kJ | 1.094 | +0.599 % | 151 s |
| NMC_P2 | 4.2C 0-30s; 0C 30-60s; 4.2C 60-90s …(Takt 60 s) | 20 min | 82.9 °C (1170 s) | 32.3 K (1180 s) | 81.6 °C | 32.1 K | 19.5 K | 946 s | 1071 s | 36.79 kJ | 2.000 | +0.413 % | 291 s |
| NMC_P3 | 1.68C 0-1500s | 25 min | 45.0 °C (1500 s) | 11.3 K (1500 s) | 45.0 °C | 11.3 K | 7.0 K | 7 s | 1079 s | 14.72 kJ | 0.800 | -0.006 % | 189 s |
| NMC_P4 | 1.4C 0-1800s | 30 min | 39.7 °C (1800 s) | 8.3 K (1800 s) | 39.7 °C | 8.3 K | 5.4 K | 0 s | 1136 s | 12.26 kJ | 0.667 | -0.005 % | 228 s |
| NMC_P0_Kh1000 | 2.1C 0-1200s | 20 min | 49.3 °C (1200 s) | 17.7 K (1200 s) | 49.3 °C | 17.7 K | 11.3 K | 446 s | 1001 s | 18.39 kJ | 1.000 | -0.012 % | 152 s |
| NMC_P0_Kh2000 | 2.1C 0-1200s | 20 min | 46.3 °C (1200 s) | 18.1 K (1200 s) | 46.3 °C | 18.1 K | 12.2 K | 246 s | 1034 s | 18.39 kJ | 1.000 | -0.018 % | 123 s |
| NMC_P0_K3 | 2.1C 0-1200s | 20 min | 47.9 °C (1200 s) | 12.3 K (1200 s) | 47.9 °C | 12.3 K | 7.9 K | 370 s | 914 s | 18.39 kJ | 1.000 | -0.004 % | 93 s |
| NMC_P0_V15 | 2.1C 0-1200s | 20 min | 43.6 °C (1200 s) | 16.0 K (1200 s) | 43.6 °C | 16.0 K | 9.5 K | 0 s | 936 s | 18.39 kJ | 1.000 | -0.008 % | 92 s |
| NMC_P1_K3 | 3C 0-360s; 2C 360-810s; 1.38C 810-1200s | 20 min | 50.1 °C (460 s) | 13.5 K (530 s) | 43.0 °C | 9.9 K | 10.6 K | 779 s | 1057 s | 20.12 kJ | 1.094 | +0.600 % | 89 s |
| NMC_P0_K3h1000 | 2.1C 0-1200s | 20 min | 44.0 °C (1200 s) | 13.5 K (1200 s) | 44.0 °C | 13.5 K | 9.3 K | 0 s | 990 s | 18.39 kJ | 1.000 | -0.009 % | 100 s |
| NMC_P3_Kh2000 | 1.68C 0-1500s | 25 min | 39.2 °C (1500 s) | 12.1 K (1500 s) | 39.2 °C | 12.1 K | 8.6 K | 0 s | 1232 s | 14.72 kJ | 0.800 | -0.015 % | 137 s |

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
| NMC P0 | 53.6 °C / 16.0 K | 53.6 °C / 16.0 K | ≈: Abw. +0.0 K / +0.0 K |
| LFP P1 | Spitze ΔT ≈ 10–12 K (während 3C), Ende ≈ 5–7 K; T_max ± 2 K zu P0 | Spitze 11.3 K bei 810 s; Ende 9.4 K; T_max-Ende 40.4 (P0 43.1, Diff -2.7 K), Spitze 44.1 | Spitze ΔT 10–12: erfüllt; Ende 5–7: verfehlt; T_max ±2 K: verfehlt |
| NMC P1 | ähnlich, Spitze ΔT ≈ 15–18 K | Spitze 17.0 K bei 810 s; Ende 14.4 K; T_max-Ende 50.1 (P0 53.6) | Spitze ΔT 15–18: erfüllt |
| LFP P2 | T_max ≈ 55–60 °C, ΔT schwankt um ≈ 20 K | T_max-Spitze 61.7 °C (Ende 60.7); ΔT Spitze 21.3 K, Mittel 13.1 K, Min in 2. Hälfte 14.2 K | T_max 55–60: verfehlt; ΔT-Mittel ≈ 20: Abw. -6.9 K |
| NMC P2 | T_max ≈ 75–85 °C, schlechter als P0 | T_max-Spitze 82.9 °C (Ende 81.6); ΔT Spitze 32.3 K, Mittel 19.5 K, Min in 2. Hälfte 21.2 K | T_max 75–85: erfüllt; schlechter als P0 (P0 53.6 °C): erfüllt |
| LFP P3 | ≈ 40 °C / ≈ 7–8 K | 37.5 °C / 7.4 K (Spitze ΔT 7.4 K) | T_max Abw. -2.5 K; ΔT 7–8: erfüllt |
| NMC P3 | ≈ 47–50 °C / ≈ 11–13 K | 45.0 °C / 11.3 K (Spitze ΔT 11.3 K) | T_max 47–50: verfehlt; ΔT 11–13: erfüllt |
| LFP P4 | ≈ 37 °C / ≈ 5–6 K | 34.1 °C / 5.4 K (Spitze ΔT 5.4 K) | T_max Abw. -2.9 K; ΔT 5–6: erfüllt |
| NMC P4 | ≈ 42–44 °C / ≈ 8–9 K | 39.7 °C / 8.3 K (Spitze ΔT 8.3 K) | T_max 42–44: verfehlt; ΔT 8–9: erfüllt |

Nicht gerechnet in K1 (nicht Teil des Auftrags): „Stationär nötig für 5 K: LFP ≤ 1,29C, NMC ≤ 1,02C“.

### Kühlung (Profil P0, Differenz zu P0 derselben Variante)

| Punkt | Erwartung | Ergebnis | Bewertung |
|---|---|---|---|
| LFP Kh1000 | T_max −3…−5 K, ΔT unverändert | T_max 39.7 °C (-3.4 K), ΔT 10.8 K (+0.20 K) | T_max-Änderung -5…-3: erfüllt; ΔT-Änderung +0.20 K |
| LFP Kh2000 | T_max −5…−8 K, ΔT unverändert | T_max 37.4 °C (-5.7 K), ΔT 10.5 K (-0.07 K) | T_max-Änderung -8…-5: erfüllt; ΔT-Änderung -0.07 K |
| LFP K3 | ΔT ≈ ÷4 → ≈ 3 K ✓, T_max ≈ 35 °C ✓ | T_max 33.8 °C, ΔT 4.6 K | ΔT-Verhältnis K3/P0 = 0.433; verfehlt-Kriterium „ΔT sinkt um weniger als die Hälfte“: nicht eingetreten; ΔT ≈ 3: Abw. +1.6 K; T_max ≈ 35: Abw. -1.2 K |
| LFP V15 | T_max −10 K, ΔT unverändert | T_max 33.1 °C (-10.00 K), ΔT 10.6 K (+0.000 K) | T_max −10: erfüllt; ΔT-Änderung +0.000 K |
| NMC Kh1000 | T_max −8…−10 K, ΔT unverändert | T_max 49.3 °C (-4.4 K), ΔT 17.7 K (+1.61 K) | T_max-Änderung -10…-8: verfehlt; ΔT-Änderung +1.61 K |
| NMC Kh2000 | T_max ≈ 41–44 °C ✓, ΔT ≈ 16 K ✗ | T_max 46.3 °C (-7.3 K), ΔT 18.1 K (+2.04 K) | T_max 41–44: verfehlt; ΔT ≈ 16: Abw. +2.1 K; ΔT-Änderung +2.04 K |
| NMC K3 | ΔT ≈ 4–5 K (knapp), T_max ≈ 38–40 °C ✓ | T_max 47.9 °C, ΔT 12.3 K | ΔT-Verhältnis K3/P0 = 0.765; ΔT 4–5: verfehlt; T_max 38–40: verfehlt |
| NMC V15 | T_max −10 K, ΔT unverändert | T_max 43.6 °C (-10.00 K), ΔT 16.0 K (+0.000 K) | T_max −10: erfüllt; ΔT-Änderung +0.000 K |

Modellfakt zu NMC K3 (aus `k1_geometrie.py`, keine Deutung): Der Kern (z 1…76 mm) ist vom Deckel durch eine Luftschicht (k = 0,026 W/(m K), z 76…79,6 mm) getrennt; die Wärme gelangt nur über diese Schicht und die Gehäusewand zum gekühlten Deckel. Bei LFP liegt der Kern dagegen mit Gehäusewand (0,3 mm Al) direkt an Boden und Oben.


### Kombinationen

| Fall | Erwartung | Ergebnis (Ladeende; Spitzen) | Vorgaben T_max ≤ 45 °C / ΔT ≤ 5 K (Spitzenwerte) |
|---|---|---|---|
| LFP_P0_K3 | siehe oben (K3 allein) | T_max 33.8 °C (Spitze 33.8), ΔT 4.6 K (Spitze 4.6) | T_max erfüllt; ΔT erfüllt |
| LFP_P1_K3 | LFP K3 erfüllt beides bei 20 min | T_max 30.4 °C (Spitze 37.6), ΔT 3.0 K (Spitze 6.3) | T_max erfüllt; ΔT verfehlt |
| LFP_P0_K3h1000 | LFP K3 erfüllt beides bei 20 min | T_max 30.8 °C (Spitze 30.8), ΔT 3.8 K (Spitze 3.8) | T_max erfüllt; ΔT erfüllt |
| NMC_P0_K3 | siehe oben (K3 allein) | T_max 47.9 °C (Spitze 47.9), ΔT 12.3 K (Spitze 12.3) | T_max verfehlt; ΔT verfehlt |
| NMC_P1_K3 | NMC braucht K3 + h ≥ 1000 oder K3 + P3 | T_max 43.0 °C (Spitze 50.1), ΔT 9.9 K (Spitze 13.5) | T_max verfehlt; ΔT verfehlt |
| NMC_P0_K3h1000 | NMC braucht K3 + h ≥ 1000 oder K3 + P3 | T_max 44.0 °C (Spitze 44.0), ΔT 13.5 K (Spitze 13.5) | T_max erfüllt; ΔT verfehlt |
| NMC_P3_Kh2000 | (Kombination aus ERWARTUNG; Einzelwert nicht angegeben) | T_max 39.2 °C (Spitze 39.2), ΔT 12.1 K (Spitze 12.1) | T_max erfüllt; ΔT verfehlt |

### Als „Verfehlt“ in ERWARTUNG definiert

- Wärmeintegral > 2 % von Tabelle: größte Abweichung 0.34 % → nicht eingetreten.
- P0 weicht > 0,3 K von K0 L2 ab (LFP): Abw. T +0.0000 K, ΔT +0.0000 K → nicht eingetreten.
- P0 weicht > 0,3 K von K0 L2 ab (NMC): Abw. T +0.0000 K, ΔT +0.0000 K → nicht eingetreten.
- K3 senkt ΔT bei LFP um weniger als die Hälfte: ΔT 10.6 → 4.6 K (−57 %) → nicht eingetreten.

## 5 Laufzeiten

Summe Einzelläufe (Elmer + Nachlauf) 34.5 min CPU, 4 Läufe parallel (nice 10, 1 Kern je Lauf); P0-Gate separat. Je Fall: Tabelle in Abschnitt 2, Spalte Laufzeit.

## 6 Bilder

`profile.png`, `verlauf_profile_LFP.png`, `verlauf_profile_NMC.png`, `verlauf_kuehlung_LFP.png`, `verlauf_kuehlung_NMC.png`, `landkarte.png` (Lesehilfe `k1_lesehilfe.md`); Render (Blender Cycles CPU, Endzustand): `bilder/render_LFP_P0_K3h1000_ende.png` (Fall mit niedrigster T_max unter den beide-erfüllenden LFP-Fällen), `bilder/render_NMC_P4_ende.png` (kein NMC-Fall erfüllt beide; bester = T_max ≤ 45 °C mit kleinster ΔT-Spitze); Lesehilfe `bilder/render_lesehilfe.md`. Die obere Kühlplatte (K3) ist im Render nicht gezeichnet; LFP-Render wirkt dunkel wegen der festen Skala 25–55 °C.

---
*KI-generiert (Claude Sonnet), Entwurf, nicht vom Menschen freigegeben. Erzeugt von k1_bericht.py.*
