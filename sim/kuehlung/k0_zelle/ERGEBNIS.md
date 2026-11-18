| Dok.-Nr. | ERG-K0 | Version | 0.1 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Ergebnis K0: Wärmesimulation einer Zelle je Variante (Elmer) | Ersteller | Claude Sonnet (KI), Auftrag Opus | Prüfer | – (Opus offen) |

> **KI-generiert.** Entwurf, nicht vom Menschen freigegeben. Stand 2026-11-17. Quelle aller Zahlen: `sim/kuehlung/k0_zelle/ergebnis.json` (erzeugt von `auswertung.py` aus `elmer/fall_*/`).


## Was getan wurde
Elmer-Wärmeleitung (HeatSolver) mit einem homogenisierten, orthotropen Kern, Gehäuse als eigene Schicht, Luft im NMC-Kernloch und in den LFP-Endzonen, Wärmequelle Q = I²·R gleichmäßig im Kern. Netz mit gmsh (nur Hexaeder), je Fall Netzstudie auf zwei Stufen. Alle Eingaben aus `eingaben.json` und `cad/zelle/entwurf/parameter_<V>_entwurf.json`. Grenzen **T_max ≤ 45 °C und ΔT ≤ 5 K sind Vorgabe (REQ-P09, Autor 2026-11-17)**. K1 (Boden gekühlt, ENT-081) ist Hauptfall, K2 nur Vergleich. Rechnung CPU, ein Kern.

## Hauptergebnisse (ΔT = Kern max − Kern min; T_max über die ganze Zelle)
| Fall | Wärme (W) | T_max (°C) | T_min Kern (°C) | ΔT Kern (K) | T_max ≤ 45 | ΔT ≤ 5 | Bilanz (Quelle − Kühlrand) |
|---|---|---|---|---|---|---|---|
| LFP_K1_L1 | 12.47 | 30.1 | 27.0 | 3.0 | ja | ja | -0.000 % |
| LFP_K1_L2 | 55.01 | 43.1 | 32.5 | 10.6 | ja | nein | -0.008 % (Energie) |
| NMC_K1_L1 | 3.48 | 33.5 | 28.7 | 4.8 | ja | ja | -0.000 % |
| NMC_K1_L2 | 15.33 | 53.6 | 37.6 | 16.0 | nein | nein | -0.008 % (Energie) |
| NMC_K2_L1 | 3.48 | 31.8 | 26.8 | 5.0 | ja | ja | -0.000 % |
| NMC_K2_L2 | 15.33 | 49.9 | 31.8 | 18.1 | nein | nein | +0.011 % (Energie) |

Bei L2 (transient, 1200 s) stehen T_max und ΔT zum Endzeitpunkt t = 1200 s; die Zelle ist dort nicht stationär (Kühlrandleistung am Ende: LFP 45.3 von 55.0 W, NMC K1 11.9 von 15.3 W, NMC K2 12.9 von 15.3 W).

Zeitpunkte (L2, Quelle `ergebnis.json` → `faelle.<Fall>.t_Tmax45_s` bzw. `t_dT5_s`; ΔT nur auf dem Raster t = 30, 70, 110, … s ausgewertet: erster Rasterpunkt mit ΔT ≥ Vorgabe):
| Fall | T_max erreicht 45 °C bei (s) | ΔT erreicht 5 K bei (s) |
|---|---|---|
| LFP_K1_L2 | nie in 1200 s | 430.0 |
| NMC_K1_L2 | 640.0 | 270.0 |
| NMC_K2_L2 | 750.0 | 230.0 |

## Eingänge der Rechnung (aus `elmer/fall_*/meta.json`)
| Fall | C-Rate | Strom (A) | R (mΩ) | Wärme Q (W) | Q/V Kern (W/m³) | Kernleitfähigkeit (W/(m·K)) | h (W/(m²·K)) | Kühlfläche (mm²) | Knoten |
|---|---|---|---|---|---|---|---|---|---|
| LFP_K1_L1 | 1.00 | 92.4 | 1.461 | 12.47 | 16917 | x=Laenge 21.04, y=Hoehe(Boden y=0) 19.82, z=Dicke 4.11 | 500 | 9534 | 5859 |
| LFP_K1_L2 | 2.10 | 194.0 | 1.461 | 55.01 | 74606 | x=Laenge 21.04, y=Hoehe(Boden y=0) 19.82, z=Dicke 4.11 | 500 | 9534 | 5859 |
| NMC_K1_L1 | 1.00 | 23.1 | 6.500 | 3.48 | 31786 | axial 20.33, tangential 20.33, radial 1.199 | 500 | 1657 | 17738 |
| NMC_K1_L2 | 2.10 | 48.6 | 6.500 | 15.33 | 140174 | axial 20.33, tangential 20.33, radial 1.199 | 500 | 1657 | 17738 |
| NMC_K2_L1 | 1.00 | 23.1 | 6.500 | 3.48 | 31786 | axial 20.33, tangential 20.33, radial 1.199 | 500 | 2888 | 17738 |
| NMC_K2_L2 | 2.10 | 48.6 | 6.500 | 15.33 | 140174 | axial 20.33, tangential 20.33, radial 1.199 | 500 | 2888 | 17738 |

Vergleich Leitfähigkeit LFP (L1/L2, K1): Hauptfall W18 gegen Schichtmischung
| Fall | T_max (°C) | ΔT Kern (K) |
|---|---|---|
| LFP_K1_L1 | 30.1 | 3.0 |
| LFP_K1_L1_mischung | 29.6 | 2.5 |
| LFP_K1_L2 | 43.1 | 10.6 |
| LFP_K1_L2_mischung | 42.0 | 9.1 |

## Netzstudie (L1, Feinheit 1 gegen 2, doppelte Elementzahl je Richtung)
| Fall | T_max f1 (°C) | T_max f2 (°C) | Differenz (K) | ΔT f1 (K) | ΔT f2 (K) | Knoten f1 / f2 |
|---|---|---|---|---|---|---|
| LFP_K1 | 30.073 | 30.075 | +0.001 | 3.04 | 3.06 | 5859 / 33099 |
| NMC_K1 | 33.472 | 33.454 | -0.017 | 4.81 | 4.81 | 17738 / 121830 |
| NMC_K2 | 31.797 | 31.810 | +0.012 | 4.96 | 4.97 | 17738 / 121830 |

Kriterium aus dem Auftrag: Änderung von T_max < 0,5 K. Die Stufe 2 der NMC-Fälle lief mit iterativem Löser (BiCGStab/ILU2), weil der direkte Löser (Umfpack) bei 122 000 Knoten den Speicher überschritt.

## Empfindlichkeit L1 (K1, ΔT Kern, jeweils ein Parameter; Bänder aus `eingaben.json`)
| Variante | Parameter | ΔT Grenze 1 (K) | ΔT Grenze 2 (K) |
|---|---|---|---|
Spalte „Grenze 1“ = Parametergrenze mit erwartet kleinerem ΔT (R tief, h hoch, Stoffbänder hoch); „Grenze 2“ = die andere Grenze; LFP-Leitfähigkeit: Grenze 1 = Hauptfall W18, Grenze 2 = Schichtmischung.

| LFP | Leitfähigkeit: Schichtmischung statt W18 | 3.04 | 2.53 |
| LFP | Wärmeübergang h (200…1000) | 2.72 | 3.61 |
| LFP | Innenwiderstand R | 2.13 | 4.56 |
| NMC | Bodenspalt Luft (Modellvariante) | 4.81 | 9.06 |
| NMC | Leitfähigkeit (Stoffbänder) | 4.69 | 4.96 |
| NMC | Wärmeübergang h (200…1000) | 4.65 | 4.97 |
| NMC | Innenwiderstand R | 3.70 | 8.14 |

Zusatzfall NMC mit Luftspalt unter dem Kern (0,6 mm Luft zwischen Becherboden und Kern, Modellvariante, keine Messung): L1 T_max 42.4 °C, ΔT 9.1 K; L2 T_max 62.2 °C, ΔT 19.1 K (`NMC_K1_L1_spalt`, `NMC_K1_L2_spalt`).

## Abgleich mit ERWARTUNG.md (Punkt für Punkt, keine Deutung)
1. **Wärme.** Erwartet LFP 1C ≈ 12,5 W, 2,1C ≈ 55 W; 4680 1C ≈ 3,5 W, 2,1C ≈ 15 W; je Volumen etwa doppelt so viel bei 4680. Gerechnet: LFP 12.47 W und 55.01 W; NMC 3.48 W und 15.33 W; Q/V NMC zu LFP = 1.88 (31786 gegen 16917 W/m³). **Erfüllt** (innerhalb ±10 %).
2. **Leitfähigkeit.** Erwartet Mischung LFP Ebene ≈ 28, quer ≈ 1,0; 4680 axial ≈ 21, radial ≈ 1,2. Gerechnet (volumengewichtete Mischregel): LFP Ebene 27.7, quer 1.00; NMC axial/tangential 20.3, radial 1.20 W/(m·K). **Erfüllt.** Hauptfall LFP mit W18 (21,04 / 19,82 / 4,11).
3. **L1.** Erwartet LFP ΔT ≈ 3–4 K, T_max ≈ 30 °C; 4680 ΔT ≈ 4–5 K, T_max ≈ 31 °C. Gerechnet: LFP ΔT Kern 3.04 K (innerhalb 3–4; als Gesamtzelle T_max − T_min 3.68 K), T_max 30.1 °C. NMC ΔT Kern 4.81 K (innerhalb 4–5), T_max 33.5 °C (**+2.5 K gegenüber ≈ 31 °C**). Beide im Ziel (T ≤ 45 °C, ΔT ≤ 5 K).
4. **L2.** Erwartet LFP T_max ≈ 40–45 °C, ΔT ≈ 10–13 K; 4680 Boden T_max ≈ 45–50 °C, ΔT ≈ 15–18 K; ΔT-Vorgabe von beiden verfehlt, 4680 T_max knapp. Gerechnet: LFP T_max 43.1 °C (innerhalb), ΔT 10.6 K (innerhalb); NMC K1 T_max 53.6 °C (**außerhalb 45–50, +3.6 K über dem oberen Wert; Erwartung verfehlt**), ΔT 16.0 K (innerhalb). ΔT-Vorgabe 5 K: von beiden überschritten (Erwartung bestätigt). LFP-Wärmeabfuhr am Ende 82 % der Quelle, also nicht nahezu stationär wie erwartet.
5. **K2.** Erwartet ΔT eher größer als bei Bodenkühlung, 20 K oder mehr. Gerechnet: L1 ΔT 4.96 K (K1: 4.81 K), T_max 31.8 °C (K1: 33.5); L2 ΔT 18.1 K (K1: 16.0), T_max 49.9 °C (K1: 53.6). ΔT bei K2 ist etwas größer als bei K1, der Wert ≥ 20 K **wird nicht erreicht**; T_max ist bei K2 **niedriger** als bei K1.
6. **Stärkste Annahmen.** Empfindlichkeit L1: größte Wirkung auf ΔT durch den Innenwiderstand (LFP 3.0…2.5 K, NMC 4.8…9.1 K), dann h; die Leitfähigkeit wirkt bei NMC wenig. Der Luftspalt unter dem NMC-Kern (Modellvariante) verändert ΔT stärker als die Stoffbänder.
**„Verfehlt“-Kriterien der Erwartung:** Wärme L1 außerhalb ±10 %: nein. LFP L1 ΔT > 8 K oder < 1 K: nein (3.04 K). Energiebilanz stationär > 2 %: nein (größte Abweichung 0.0000 %). Transiente Energiebilanz (Quelle gegen Kühlrand plus gespeichert): größte Abweichung 0.011 % (Elmer-Randlast gegen Trapezregel, nur Plausibilitätsprüfung).

## Methode und Modellvereinfachungen (bitte von Opus prüfen)
- **Geometrie.** LFP 681 × 90 × 14 mm, Boden = Schmalseite y = 0 (681 × 14 mm), Wand 0,3 mm Aluminium (237), Kern = Innenraum x 32,75…648,25 mm (Elektrodenlänge 615,5 mm, ENT-032), Endzonen je 32,75 mm Luft (0,026; symmetrisch aufgeteilt, Annahme). NMC Ø 46 × 80 mm, Becherwand/Boden/Deckel 0,4 mm Stahl (50), Kern Ringzylinder r 7…22,6 mm, z 0,4…76 mm, Kernloch und Raum oberhalb Luft.
- **NMC-Kern reicht bis auf den Becherboden** (Annahme dieser Auswertung: Tabless-Ableiter in Kontakt mit dem Boden; Parameterdatei nennt Kernbeginn bei z = 1,0 mm, dazwischen wäre sonst 0,6 mm Luft). Die Variante mit Luftspalt ist als Zusatzfall gerechnet (s. o.).
- **Orthotropie LFP:** Länge x = 21,04, Höhe y (Richtung zur Kühlplatte) = 19,82, Dicke z = 4,11 (W18; welche der beiden Ebenenwerte in welche Richtung gehört, ist aus W18 nicht eindeutig: Annahme). **NMC:** Wickel als Zylinderkoordinaten; je Sektor (48 Körper à 7,5°) ein konstanter, um den Mittelwinkel gedrehter 3×3-Tensor (axial = tangential, radial). Probe: Achsensymmetrie bei K1 – Streuung der Mantel-Temperatur am Umfang 0 K.
- **Wärmekapazität (L2):** Dichte und c nur im Kern; Dichte = Zellmasse (ENT-020 bzw. ENT-011) / Kernvolumen, c = 1112 bzw. 1100 J/(kg·K); Gehäuse und Luft ohne Wärmekapazität. Dichte und c des Gehäuses stehen nicht in `eingaben.json` (**offene Frage**).
- **Wärmequelle** Q = I²R gleichmäßig im Kern (Annahme laut Eingaben), R LFP = 1,0 mΩ · 135/92,4 (Regel R ∝ 1/Ah, Annahme), R NMC 6,5 mΩ. Kühlung: Randbedingung Wärmeübergang h = 500 W/(m²K) gegen 25 °C (Annahme); Rest adiabat. L2: BDF 2. Ordnung, Schritt 10 s, 120 Schritte, Start 25 °C; Last 2,1 C = 70 % Ladungsänderung in 1200 s.
- **Löser.** Stationär direkt (Umfpack), transient und NMC-Netzstufe 2 iterativ (BiCGStab, ILU2, Toleranz 1e-12). Bei den ersten beiden Läufen von NMC L2 wurde Umfpack nach ca. 12 Schritten wegen Dauer abgebrochen und neu mit dem iterativen Löser gerechnet; LFP L2 lief zuerst mit Umfpack, dann zur Konsistenz der VTU-Ausgabe (jeder Schritt) mit dem iterativen Löser neu.
- **Dateien:** Netz `elmer/netz_*`, Fälle `elmer/fall_*/{case.sif,scalars.dat,meta.json,solver.log,case_t*.vtu}`; Skripte `geometrie.py`, `rechnen.py`, `auswertung.py`, `bilder_render.py`, `render_blender.py`; Läufe `alle*.sh` (Scope `hermes-batterie-k0*`).

## Bilder (Lesehilfe: `k0_lesehilfe.md`, `bilder/render_lesehilfe.md`)
`temperatur_<LFP|NMC>_<K1|K2>_<L1|L2>.png` (Schnitt, 6 Stück), `temperatur3d_*_L2.png` (3 Stück, matplotlib), `verlauf_L2.png`, `empfindlichkeit_K0.png`; gerendert (Blender Workbench, CPU, da `pvbatch` ohne Python-Modul `paraview` nicht lauffähig ist; ParaView 5.11.2 ist installiert, aber nur die GUI/Binärdateien) in `bilder/render_<Fall>_t<0|300|600|900|1200>s.png` und `bilder/verlauf_<Fall>.mp4` (41 Bilder, 8 B/s, ffmpeg).

## Offene Fragen (→ Opus)
1. Dichte und Wärmekapazität des Gehäuses (Aluminium/Stahl) fehlen in `eingaben.json`; derzeit ohne Kapazität gerechnet.
2. Zuordnung der W18-Werte 21,04 / 19,82 zu Länge/Höhe der LFP-Zelle (hier Länge 21,04, Höhe 19,82).
3. NMC: Kontakt des Wickels zum Becherboden (hier ja) bzw. Luftspalt: Zusatzfall zeigt starken Einfluss.
4. Erwartung Punkt 4 (NMC L2 T_max 45–50 °C) und Punkt 5 (K2 ΔT ≥ 20 K) verfehlt.
5. Endzonen (Pole, Halter, Stromschienen) als reine Luft ist eine grobe Vereinfachung; Wärmeleitung über die Pole nicht berücksichtigt.

---
*KI-generiert (Claude Sonnet), Entwurf, nicht vom Menschen freigegeben.*
