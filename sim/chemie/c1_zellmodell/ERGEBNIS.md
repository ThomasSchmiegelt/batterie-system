| Dok.-Nr. | ERG-C1 | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Ergebnis C1: PyBaMM-Zellmodell LFP und NMC, Wärme und Widerstand | Ersteller | Claude Sonnet (KI), Auftrag Opus | Prüfer | – (Opus offen) |

> **KI-generiert.** Entwurf, nicht freigegeben. Stand 2026-11-17. Alle Zahlen aus `ergebnis_zahlen.json` (erzeugt von `bilder.py` aus `ergebnis.json`, `ergebnis_LFP_kap.json`, `ergebnis_NMC_lumped.json`). Rechnung `zellmodell.py` (SPMe, PyBaMM 26.10), Dauer ca. 15 s je Lauf. Keine Deutung. Herkunft Parametersätze: LFP PyBaMM `Prada2013`, NMC PyBaMM `Chen2020` (beide Literatur).

## Abgleich mit ERWARTUNG.md
| Nr. | Erwartung | Ergebnis (Fundstelle ergebnis_zahlen.json) | Urteil |
|---|---|---|---|
| 1 | Kapazität ± 10 % | LFP mit Akten-Fläche (3,86 m²): 48,63 Ah, −47,4 % (`LFP_Akten`). NMC: 23,19 Ah, +0,26 % (`NMC`). LFP mit auf 92,4 Ah skalierter Fläche (Faktor 1,900): 93,08 Ah, +0,73 % (`LFP_kap`) | LFP verfehlt bei Akten-Fläche; NMC erfüllt |
| 2 | Wärme LFP 40–70 W (I²R 55 W) | `LFP_kap`: Mittel 32,8 W, Spitze 53,1 W (nur irreversibel, I·ΔU, 194 A, 20,15 min). Reversibel: nicht berechenbar (siehe offen) | Mittel unter Faktor-1,5-Band (36,7–82,5 W): verfehlt |
| 2 | Wärme NMC 5–9 W (6,7 W) | `NMC(lumped)`: Mittel bis CV 6,92 W, Spitze 7,48 W, Ganzlauf-Mittel 5,24 W; I·ΔU-Maß 10,6 W (bis CV) | im Band |
| 3 | DCIR LFP 1–2 mΩ, NMC 5–8 mΩ (25 °C) | LFP_kap 0,76 mΩ (10/25/40 °C: 1,10/0,76/0,50); LFP_Akten 1,16; NMC 6,40 (7,93/6,40/5,13) | NMC erfüllt; LFP_kap darunter |
| 4 | NMC erreicht 4,2 V vor 80 %, Ladezeit länger | NMC: 4,2 V nach 21,8 min (CV-Beginn 1309 s), 80 % nach 36,15 min statt 20 min; LFP_kap erreicht 3,6 V nicht (U_max 3,45 V), 20,15 min | erfüllt |

## Offen / Auffälligkeiten (an Opus)
1. Prada2013 enthält keine Thermikparameter (Stromableiterdicke, Dichte, c_p): `lumped` nicht lauffähig. LFP deshalb **isotherm 25 °C**; PyBaMM liefert dort Heizterme = 0. LFP-Wärme daher nur als I·|U−OCV| (Battery open-circuit voltage). Neue Thermik-Annahmen wurden nicht gesetzt. Frage: Thermikwerte für Prada übernehmen (z. B. aus Chen2020, Annahme) oder anderen LFP-Satz?
2. Reversible Wärme ist in beiden Sätzen 0 (NMC lumped, `Q_rev`): kein Entropiekoeffizient im Satz. Erwartungspunkt „reversibler Anteil“ nicht prüfbar.
3. Zwei Wärmemaße bei NMC: PyBaMM-Heizterm (Ohm + Reaktion) 6,92 W, I·ΔU (inkl. Diffusionsüberspannung) 10,6 W bis CV. Welches maßgeblich ist für K1: Opus.
4. Flächen-Annahme: beide Seiten der Elektroden zählen (LFP 38×2×615,5×82,5 mm; NMC 2×3215×72 mm). Mit Akten-Fläche liefert Prada nur 48,6 Ah (Faktor 1,90 zu 92,4 Ah). Der Zusatzlauf `LFP_kap` ist meine Ableitung der ERWARTUNG („auf Zellkapazität skaliert“).
5. Zellvolumen für die Wärme [W]: Elektrodenfläche × Summe der Schichtdicken des Satzes (im Skript berechnet, nicht Gehäusevolumen). Erster Lauf mit Gehäusevolumen gab Ganzlauf-Mittel 5,28 W gegen 5,24 W jetzt (Lauf überschrieben).
6. DCIR-Strom 1C der Aktenkapazität gewählt (Erwartung nennt keinen); Kühlung lumped NMC: Boden 1,66e-3 m², h 500 W/(m²K), 25 °C (K0/K1-Annahmen); T_ende 27,2 °C.
7. Verfehlt-Kriterium der ERWARTUNG (Wärme außerhalb Faktor 1,5) ist für LFP eingetreten: K1 ggf. mit Modellwärme neu (Opus entscheidet).

## Dateien
`eingaben.json`, `zellmodell.py`, `zusatz_lumped.py`, `zusatz_lfp_kap.py`, `bilder.py`, `ergebnis.json`, `ergebnis_LFP_kap.json`, `ergebnis_NMC_lumped.json`, `ergebnis_zahlen.json`, Bilder `waerme_LFP.png`, `waerme_NMC.png`, `dcir.png`, `ladekurve.png`, `lesehilfe.md`, Baustein `praesentation/bausteine/C1.md`. Log: `lauf*.log`.

*KI-generiert, Entwurf.*
