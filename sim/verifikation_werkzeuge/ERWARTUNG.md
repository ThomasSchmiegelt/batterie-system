# ERWARTUNG QN1: Werkzeug-Testfälle mit bekannter Lösung

KI-generiert (Claude Opus, 2026-11-23). Gehört zu BAT-DOC-22, Kategorie W.

## Anforderung
REQ-D01, REQ-D09. Mittelbar alle S-Anforderungen (P05, P09, P12, P14).

## Steckbrief
Kein Bauteil. Testgeometrien sind einfache Körper mit analytischer Lösung. Werkstoffwerte frei wählbar: Sie gehen nicht in das Produkt ein und müssen nur in Rechnung und Formel gleich sein.

## Vorrechnung
Die analytischen Lösungen selbst sind die Vorrechnung (siehe Erwartung).

## Erwartung
| Fall | Werkzeug | Aufbau | Lösung | erwartete Abweichung (feines Netz) | erwartete Ordnung |
|---|---|---|---|---|---|
| V1 | Elmer (Wärme, stationär) | Platte, Dicke L, Wärmequelle q, beide Seiten T_w | T_max − T_w = q L²/(8 k) (beidseitig gekühlt) | < 1 % | ≈ 2 (lineare Elemente) |
| V2 | FluidX3D (LBM) | Spalt zwischen zwei Platten, Abstand h, Druckgradient bzw. Volumenkraft | Parabelprofil, u_max = G h²/(8 μ); Δp = 12 μ L ū / h² | < 2 % bei h ≥ 20 Zellen; deutlich mehr bei h ≈ 4–5 Zellen | ≈ 2 |
| V3 | OpenRadioss | Kragbalken, quasistatisch, linear-elastisch, Endkraft F | δ = F L³/(3 E I) | < 3 %, Energiefehler < 1 % | – |
| V4 | PyBaMM | Konstantstromentladung, Parametersatz des Projekts | entnommene Ladung = I·t bis Abschaltspannung ≈ Nennkapazität des Satzes; SPM gegen DFN bei C/20: Spannungsunterschied | Ladung ±2 %; SPM/DFN < 10 mV | – |
| V5 | Verteiler-1D (k5 verteiler.py) | ein gerader Kanal ohne Abzweig | Hagen-Poiseuille bzw. Shah-London für das Rechteck | < 1 % | – |

**Wichtigste Erwartung:** In V2 hängt die Abweichung stark von der Auflösung ab. Löste K3 die Kanäle (4 × 5 mm) nur mit wenigen Zellen auf, kann V2 die +232 % gegenüber der Korrelation (B-BAT-038, K3) erklären. Rechne V2 deshalb bei h = 4, 5, 8, 16 und 32 Zellen und trage die Abweichung über der Auflösung auf.

## Plausibilitätskriterien
Massenerhalt in V2 < 0,5 %. Energiebilanz in V3 < 1 %. In V1 liegt der Wärmestrom durch die Wände bei q·L (±0,5 %).

## Abbruchkriterien (Wächter)
Jeder Fall dauert unter 10 min. Sonst Abbruch und Meldung, die Netzgröße wird nicht still verkleinert. FluidX3D nur nach `rechnen/gpu_warten.sh`.

## Informationsgewinn der Varianten
Netzreihe mit 3 Stufen in V1 und V2 (Ordnung bestimmen), Auflösungsreihe in V2 (Erklärung von K3). Weitere Varianten nicht.

## Zielband Bild
Je Fall: Abweichung über der Netzfeinheit (log-log) mit Zielband (Toleranz oben) und Steigungsdreieck der Ordnung 2. Ein Sammelbild zeigt alle Fälle, grün bestanden, rot verfehlt.

## Prüfung
KI-generiert (Claude Sonnet, 2026-11-23), Entwurf. Vergleich mit der Erwartung, keine Deutung (Zahlen aus `ergebnis.json` und `ergebnis_V<n>.json`).

| Fall | erwartete Abweichung | gefunden | erwartete Ordnung | gefunden | Erwartung erfüllt |
|---|---|---|---|---|---|
| V1 | < 1 % | -0,23 %, Wärmestrom +0,000 % (Soll ±0,5 %) | ≈ 2 | 2,00 | ja |
| V2 | < 2 % bei h ≥ 20; deutlich mehr bei h ≈ 4–5 | h = 32: +0,068 %; h = 4: -6,20 %, h = 5: -3,97 % (u_max: -12,5 % bzw. -4,0 %) | ≈ 2 | 2,07 / 2,44 | ja (Massenerhalt 0,00043 % < 0,5 %) |
| V3 | < 3 %, Energiefehler < 1 % | -0,484 %, Energiefehler 0,000014 % | – | – | ja |
| V4 | Ladung ±2 %, SPM/DFN < 10 mV | LFP -47,37 % (verfehlt), NMC +0,26 %; SPM–DFN LFP 0,64 mV, NMC 4,01 mV | – | – | **teilweise: LFP-Ladung verfehlt** |
| V5 | < 1 % | +0,060 % | – | – | ja |

**Erwartung „wichtigste“ (V2-Auflösung):** Die Abweichung hängt von der Auflösung ab: von -0,07 % (h = 32) auf -6,20 % (h = 4). Sie erreicht bei h = 4–5 nicht die +232 % aus B-BAT-038 (anderes Gebiet: Plattenspalt statt Rechteckkanal 8 × 4 mm, siehe ERGEBNIS.md Punkt 4). Verfehlter Fall V4 LFP: Modell nicht angepasst, an Opus gemeldet.
Bilder angesehen (Read): `v1_konvergenz.png`, `v2_aufloesung.png`, `v3_kragbalken.png`, `v4_pybamm.png`, `qn1_sammelbild.png`; Zielband und Zahlen plausibel.

### Prüfung Opus (2026-11-23)
Erwartung: teilweise
Gefunden von: Tor QN1 (Sonnet), Deutung Opus
Getroffen: V1, V2, V3, V5 und V4-NMC innerhalb der Toleranz, Ordnung etwa 2 wie erwartet. Verfehlt: V4-LFP (−47 % Ladung, B-BAT-049). Die wichtigste Erwartung, dass grobe Auflösung die K3-Abweichung erklärt, ist **verfehlt**: Die Auflösung verursacht −4 bis −6 % (Unterschätzung), nicht +232 %. Die Ursache liegt im Modellvergleich (B-BAT-049).
