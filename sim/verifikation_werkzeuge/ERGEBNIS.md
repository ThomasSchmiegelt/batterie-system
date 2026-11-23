# ERGEBNIS QN1: Werkzeug-Testfälle V1–V5

| Dokument | BAT-QN1-ERG, Version 0.1, Status Entwurf, Ersteller Claude Sonnet 5.5 (Auftrag Opus 2026-11-23), Prüfer Opus (offen), Stand 2026-11-23 |
|---|---|

> **KI-generiert (Claude Sonnet), Entwurf, nicht freigegeben.** Gehört zu BAT-DOC-22 (AP QN1), Erwartung: `ERWARTUNG.md` in diesem Ordner. Keine Deutung, nur Vergleich mit der Erwartung (Deutung: Opus, QN8).

Neu rechnen (alle Fälle, ca. 2 min ohne GPU-Wartezeit): `bash sim/verifikation_werkzeuge/lauf.sh` (Exitcode 0 alle bestanden, 1 ein Fall verfehlt, 2 Rechenfehler). Zusammenfassung `ergebnis.json`, je Fall `ergebnis_V<n>.json`, Eingaben `eingaben.json` (Präfixformat, Testwerkstoffe `annahme:`). Lauf vom 2026-11-23 16:49 bis 16:56 (V2 wartete auf die GPU bis 16:55).

## Ergebnis auf einen Blick (ergebnis.json)
| Fall | Werkzeug | Abweichung fein | Ordnung beobachtet | Toleranz | bestanden |
|---|---|---|---|---|---|
| V1 | Elmer | -0,23 % (T_max), Wärmestrom +0,000 % | 2,00 / 2,00 | < 1 % | ja |
| V2 | FluidX3D | +0,068 % (h = 32, u_mittel), Massenerhalt +0,00043 % | 2,07 / 2,44 (8→16→32) | < 2 % ab h = 20 | ja |
| V3 | OpenRadioss | -0,484 % (Durchbiegung), Energiebilanz 0,000014 % | – | < 3 %, < 1 % | ja |
| V4 | PyBaMM | LFP Ladung -47,37 %, NMC +0,26 %; SPM-DFN max. 4,01 mV | – | ±2 %, < 10 mV | **NEIN (LFP-Ladung)** |
| V5 | Verteiler-1D | +0,060 % (gegen exakte Reihe), gegen Shah-London 0,000 % | – | < 1 % | ja |

Das Bild `qn1_sammelbild.png` zeigt alle Fälle (grün bestanden, rot verfehlt, Zielband als schwarze Linie).

## V1 Elmer (ergebnis_V1.json, v1_elmer.py, v1_konvergenz.png)
Platte L = 20 mm, q = 1·10⁶ W/m³, k = 10 W/(m K), beide Wände 0 °C, analytisch T_max = 5,0 K. Strukturiertes Q4-Netz, Streifen seitlich adiabat. Ungerade Elementzahl, weil bei gerader Zahl ein Knoten in der Mitte liegt und der Knotenwert exakt wird (Zusatzreihe 4/10/20 Elemente in `reihe_gerade_zusatz`: Abweichung ≈ 0).
| Elemente | h [mm] | T_max [K] | Abweichung [%] | Wärmestrom Wand [%] |
|---|---|---|---|---|
| 5 | 4,000 | 4,8000 | -4,000 | +0,000 |
| 11 | 1,818 | 4,9587 | -0,826 | +0,000 |
| 21 | 0,952 | 4,9887 | -0,227 | +0,000 |

## V2 FluidX3D (ergebnis_V2.json, v2_fluidx3d.py, v2_aufloesung.png)
Spalt, periodisch in x und z, Volumenkraft, Wand TYPE_S, Binärdatei `k3_gesamt/fluidx3d/bin/FluidX3D` (SRT, D3Q19, FP32, wie K3), ν = 0,0106667 (τ = 0,532, wie K3) und Zusatzreihe ν = 0,1 (τ = 0,8). Analytisch u_mittel = G h²/(12 ν), u_max = G h²/(8 ν) (Zellmitten-Profil). Je Lauf 1–3 s.
**Auflösungsreihe (Abweichung gegen analytisch, %)**
| h [Zellen] | u_mittel (τ 0,532) | u_max (τ 0,532) | Profil L2 | u_mittel (τ 0,8) | u_max (τ 0,8) |
|---|---|---|---|---|---|
| 4 | -6,198 | -12,465 | 8,496 | -1,750 | -9,500 |
| 5 | -3,966 | -3,977 | 5,442 | -1,120 | -2,080 |
| 8 | -1,549 | -3,116 | 2,127 | -0,438 | -2,376 |
| 16 | -0,369 | -0,760 | 0,515 | -0,111 | -0,595 |
| 32 | -0,068 | -0,163 | 0,108 | -0,034 | -0,155 |

Ordnung u_mittel zwischen Stufen (τ 0,532): 2,00, 2,00, 2,07, 2,44 (4→5, 5→8, 8→16, 16→32; Schrittweite 1/h); τ 0,8: 2,00, 2,00, 1,98, 1,72. Massenerhalt (mittlere Dichte): größte Abweichung 0,00043 %.

## V3 OpenRadioss (ergebnis_V3.json, v3_radioss.py, v3_kragbalken.png)
Kragbalken L = 200 mm, Querschnitt 10 × 10 mm, E = 210 GPa, ν = 0,3, F = 0,01 kN am Ende (cos-Rampe 60 ms, dann Halten bis 100 ms), Brick Isolid 24, 40 × 4 × 4 Elemente, 280372 Zyklen, Laufzeit ca. 1 min. δ analytisch 0,15238 mm, Werkzeug 0,15164 mm (Mittel Endknoten, letzte 10 ms; Restschwingung 0,000076 mm), Abweichung -0,484 %. Energiebilanz (äußere Arbeit minus Summe der Energien, aus der TH-Datei): größter Betrag 0,000014 % der Endarbeit. Äußere Arbeit 0,0007585 J gegen ½·F·δ (δ des Werkzeugs) 0,0007582 J, Abweichung +0,032 % (nur Gegenprobe).

## V4 PyBaMM (ergebnis_V4.json, v4_pybamm.py, v4_pybamm.png, v4_kurven.png)
Parametersätze und Zellfläche wie C1 (`sim/chemie/c1_zellmodell/eingaben.json`, Prada2013 / Chen2020), Entladung C/20 bis Abschaltspannung, Ladung = ∫I dt, Projektmodell SPMe isotherm. Nennkapazität = „Nominal cell capacity“ des Satzes (Zielkapazität der Akte).
| Satz | Nennkapazität [Ah] | Ladung SPMe [Ah] | Abweichung [%] | SPM–DFN max. [mV] | Ladung ±2 % / SPM–DFN < 10 mV |
|---|---|---|---|---|---|
| LFP | 92,4 | 48,630 | -47,37 | 0,64 | NEIN / ja |
| NMC | 23,1 | 23,185 | +0,26 | 4,01 | ja / ja |

LFP verfehlt die Toleranz (Ladung 48,63 Ah gegen 92,4 Ah). Der Wert stimmt mit C1 überein (`sim/chemie/c1_zellmodell/ergebnis.json` LFP kapazitaet_C20_Ah, abw_prozent −47,37 %; dort schon dokumentiert in ERGEBNIS.md C1). Das Modell wurde nicht angepasst. Zusatz (nicht in der Wertung): LFP mit auf die Zielkapazität skalierter Elektrodenbreite (Faktor 1,9001) liefert 93,08 Ah (+0,73 %), gleich C1 `ergebnis_LFP_kap.json` (93,08 Ah).

## V5 Verteiler-1D (ergebnis_V5.json, v5_verteiler.py, v5_verteiler.png)
Einzelkanal 8 × 4 mm, Länge 1,970 m (Bahnlänge aus `verteiler.py`), Fluid wie K5 (ρ, μ aus `kuehlplatte.py`), Volumenstrom = Faktor × K2b-Durchfluss je Teilkanal. Referenz (a) exakte Reihenlösung des Rechteckkanals, (b) Shah-London f·Re. Geprüft wird `verteiler.dp_kanal` (ruft `kuehlplatte.kanal`).
| Durchfluss-Faktor | Re | Δp exakt [Pa] | Δp Werkzeug [Pa] | Abw. gegen exakt [%] | Abw. gegen Shah-London [%] |
|---|---|---|---|---|---|
| 0.1 | 9,5 | 32,25 | 32,27 | +0,0596 | +0,0000 |
| 0.5 | 47,5 | 161,24 | 161,34 | +0,0596 | +0,0000 |
| 1.0 | 94,9 | 322,49 | 322,68 | +0,0596 | +0,0000 |

## Lesehilfe für die Bilder
- Die **schwarze/grüne Linie** ist die Toleranz aus der ERWARTUNG: liegt der Punkt oder Balken darunter, besteht der Fall.
- **Log-log-Bild (V1, V2):** je feiner das Netz (V1 nach links, V2 nach rechts), desto kleiner der Fehler. Das graue **Steigungsdreieck** zeigt „Ordnung 2“: Verdoppelt man die Feinheit, sinkt der Fehler auf ein Viertel.
- **V2 rechts:** Geschwindigkeitsprofile im Spalt gegen die analytische Parabel; bei h = 4 und 5 sind nur wenige Punkte im Spalt.
- Der orange Streifen in V2 markiert die Auflösung, mit der K3 gerechnet hat (4–5 Zellen, laut ERWARTUNG QN1).

## Offene Fragen und Hinweise an Opus
1. **Ordnungsband:** Die ERWARTUNG nennt „≈ 2“ ohne Toleranz. Ich bewerte die Ordnung nicht, nur die Abweichungs-Toleranzen (Tabelle der ERWARTUNG und Plausibilitätskriterien).
2. **V1 Knotenwert:** Bei gerader Elementzahl ist T_max bei Q4 und konstanter Quelle exakt (Abweichung ≈ 0, Ordnung nicht bestimmbar); die bewertete Reihe hat ungerade Elementzahlen (Auslegung Sonnet). Bitte bestätigen.
3. **V2 Kennzahl:** Bewertet wird u_mittel (gleichwertig Δp bei gegebener Kraft); u_max liegt bei h = 4 bis 8 deutlich höher (siehe Tabelle, ERWARTUNG: „deutlich mehr bei h ≈ 4–5“). Massenerhalt in einem periodischen, geschlossenen Gebiet ist nur über die mittlere Dichte prüfbar (geringe Aussagekraft).
4. **V2 Geometrie:** Plattenspalt (unendlich breit), nicht der Rechteckkanal 8 × 4 mm der K3; die Zahl in B-BAT-038 (+232 %) ist damit nicht reproduziert (Deutung: QN8, Opus).
5. **V4 LFP verfehlt:** Abweichung stammt aus der Zellfläche der Akte (C1 bekannt); nicht angepasst, Meldung an Opus.
6. **V3:** Eine Netzstufe (keine Netzreihe, laut ERWARTUNG nur V1 und V2).
7. **Wächter:** Alle Fälle < 10 min (größter V3 ca. 1 min). Kein Fall musste abgebrochen werden.
8. `pm/masse_abgleich.py sim/verifikation_werkzeuge` listet Massenabweichungen anderer Ordner (nicht dieser Arbeit).

---
KI-generiert (Claude Sonnet), Entwurf, Stand 2026-11-23, BAT-QN1-ERG v0.1. Nicht vom Menschen freigegeben.
