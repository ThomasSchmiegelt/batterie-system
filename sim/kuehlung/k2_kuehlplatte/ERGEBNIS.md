| Dok.-Nr. | ERG-K2 | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Ergebnis K2: Kühlplatten, 1D-Hydraulik und Wärmeübergang | Ersteller | Claude Sonnet (KI) | Prüfer | Opus (offen) |

> **KI-generiert** (Claude Sonnet, 2026-11-17), Entwurf, nicht von Opus geprüft. Quelle aller Zahlen: sim/kuehlung/k2_kuehlplatte/ergebnis.json (Skript kuehlplatte.py, Eingaben eingaben.json).

## 1 Eingaben
| Fall | Wärme je Zelle | Zellen | Wärme Pack | je Platte (hälftig) | Quelle |
|---|---|---|---|---|---|
| LFP_P0 | 55.01 W | 250 | 13.75 kW | 6.88 kW | sim/kuehlung/k1_schnellladen/ergebnis.json faelle.LFP_P0.E_quelle_exakt_J / 1200 s |
| NMC_P4 | 6.81 W | 868 | 5.91 kW | 2.96 kW | sim/kuehlung/k1_schnellladen/ergebnis.json faelle.NMC_P4.E_quelle_exakt_J / 1800 s |
| NMC_P3 | 9.81 W | 868 | 8.52 kW | 4.26 kW | sim/kuehlung/k1_schnellladen/ergebnis.json faelle.NMC_P3.E_quelle_exakt_J / 1500 s |

Platte LFP: 1970 x 1370 mm, 2 Stück (cad/pack/entwurf/parameter_LFP.json, ergebnis_LFP.json). 
Platte NMC: 1890 x 1370 mm, 2 Stück (cad/pack/entwurf/parameter_NMC.json, ergebnis_NMC.json). 
Kühlmittel: ρ 1070, c 3300, μ 3 mPa·s, k 0.4 W/(m·K) (NEU, Annahme Sonnet, nicht in ERWARTUNG.md), Pr 24.8. Kanal 5 mm hoch, Stege 3 mm, Zuschlag 30 % (AUFTRAG).

## 2 Ergebnis (Kanal 20 mm, beste Breite für h; Führung quer; alle Zeilen in ergebnis.json)
| Fall | ΔT | Durchfluss Pack | Kanäle je Platte | Re | h [W/(m²K)] | Δp [bar] | hydr. Leistung [W] |
|---|---|---|---|---|---|---|---|
| LFP_P0 | 5 K | 46.7 L/min | 85 | 131 | 316 | 0.0014 | 0.11 |
| LFP_P0 | 8 K | 29.2 L/min | 85 | 82 | 299 | 0.0009 | 0.04 |
| LFP_P0 | 10 K | 23.4 L/min | 85 | 65 | 293 | 0.0007 | 0.03 |
| NMC_P4 | 5 K | 20.1 L/min | 82 | 58 | 291 | 0.0006 | 0.02 |
| NMC_P4 | 8 K | 12.6 L/min | 82 | 36 | 282 | 0.0004 | 0.01 |
| NMC_P4 | 10 K | 10.0 L/min | 82 | 29 | 279 | 0.0003 | 0.01 |
| NMC_P3 | 5 K | 28.9 L/min | 82 | 84 | 300 | 0.0009 | 0.04 |
| NMC_P3 | 8 K | 18.1 L/min | 82 | 52 | 289 | 0.0006 | 0.02 |
| NMC_P3 | 10 K | 14.5 L/min | 82 | 42 | 285 | 0.0004 | 0.01 |

## 3 Abgleich mit ERWARTUNG.md
| Erwartung | Rechnung | Ergebnis |
|---|---|---|
| Durchfluss 5 K: LFP ≈ 47, NMC ≈ 20 L/min | LFP 46.7, NMC (P4) 20.1 L/min | getroffen |
| LFP_P0: Δp 0,1-0,4 bar (LFP) / < 0,1 bar (NMC) | Δp 0.0007 bis 0.0040 bar | LFP: weit darunter (Erwartung verfehlt, günstig) |
| LFP_P0: Re 500-2000, h 500-1000 | Re 61 bis 188, h 273 bis 316 W/(m²K) | **Erwartung verfehlt**; h im Verfehlt-Bereich (um 300) |
| NMC_P4: Δp 0,1-0,4 bar (LFP) / < 0,1 bar (NMC) | Δp 0.0003 bis 0.0016 bar | NMC: erfüllt (weit darunter) |
| NMC_P4: Re 500-2000, h 500-1000 | Re 27 bis 81, h 260 bis 291 W/(m²K) | **Erwartung verfehlt**; h im Verfehlt-Bereich (unter 300) |

## 4 Auswahl (kleinster Δp mit h ≥ 500)
**Keine Variante erfüllt h ≥ 500.** Auswahl nach AUFTRAG nicht möglich. Höchstes h je Fall (nur zur Information):

- LFP_P0: 20 mm, laengs, ΔT 5 K: h 316 W/(m²K), Δp 0.0029 bar, 46.7 L/min
- NMC_P4: 20 mm, laengs, ΔT 5 K: h 291 W/(m²K), Δp 0.0012 bar, 20.1 L/min
- NMC_P3: 20 mm, laengs, ΔT 5 K: h 300 W/(m²K), Δp 0.0017 bar, 28.9 L/min

## 5 Deutung (Entwurf, Opus prüft)
- Der Druckverlust ist durch die vielen parallelen Kanäle (59 bis 151 je Platte) vernachlässigbar; Zielband Δp ≤ 0,5 bar wird um mehr als zwei Größenordnungen unterschritten.
- Die Strömung ist stark laminar (Re ≈ 30 bis 190). Dort hängt h nur von Kanalform und Kühlmittel-k ab (Nu ≈ 4-5), nicht vom Durchfluss: Mehr Pumpen hilft nicht.
- h ≈ 260 bis 316 W/(m²K) liegt unter der K0/K1-Annahme 500, bei LFP am Rand und bei NMC im Verfehlt-Bereich unter 300. K1 rechnete mit h 500; mit den hier erreichbaren h wären die K1-Temperaturen höher (K1 Kühlfall h 500 gegen K1 Kh1000 in sim/kuehlung/k1_schnellladen/ergebnis.json). Das ist keine neue Rechnung hier.
- Die Kühlmittelseite wirkt nur über h, die Zelle-Platte-Kette (Pad, Kontakt) ist nicht Teil von K2.

## 6 Offene Fragen an Opus
1. Wärmeleitfähigkeit Kühlmittel k = 0,40 W/(m·K) ist neu (nicht in ERWARTUNG.md). h ist proportional zu k; für h 500 bräuchte es k ≈ 0,63 (rechnerisch aus Verhältnis, ohne Neurechnung).
2. Erwartung Re 500-2000 und h 500-1000 verfehlt. Ursache vermutlich: viele parallele Kanäle (Annahme 3 mm Stege über die ganze Plattenfläche). Für h ≥ 500 müsste Dh kleiner (schmale/flache Kanäle) oder Mikrokanal/Turbulator gewählt werden: Entscheidung Opus (keine Variante im Auftrag).
3. K1/K3 nutzte h 500 als Annahme; soll K1 mit dem hier gerechneten h (ca. 300) wiederholt werden?
4. Nu-Korrelation: Nu_H1 (konstanter Wärmestrom, allseitig beheizt) statt einseitiger Beheizung; Korrelationen aus dem Gedächtnis (Annahme, kein abgerufener Beleg).
5. ΔT-Ziel ≤ 5 K ist nur beim Durchfluss 46,7 L/min (LFP) bzw. 20,1 L/min (NMC P4) erfüllt (ok_dT in ergebnis.json); die Auswahlregel allein ginge nicht darauf ein.
6. Pumpenwirkungsgrad nicht angenommen; nur hydraulische Leistung.
7. Kühlmittelseitige Spreizung als Beitrag zu REQ-P09 (ERWARTUNG Punkt 4): offen beim Autor, hier nicht gerechnet.

## 7 Dateien
kuehlplatte.py, eingaben.json, ergebnis.json, bilder.py, bericht.py, durchfluss_druck.png, platte_LFP.png, platte_NMC.png, k2_lesehilfe.md, praesentation/bausteine/K2.md

---
*KI-generiert (Claude Sonnet, 2026-11-17), Entwurf.*


## 8 Nachtrag (Opus-Auftrag): U_gesamt auf Plattengrundfläche und Zusatzvarianten
Methode (eingaben.json, Abschnitt nachtrag): h_eff = h_Kanal·(w + 2·η·H)/(w + Steg), η Rippenwirkungsgrad Steg (Al k 237, Steg 3 mm, Annahme Opus), in Reihe mit Pad 1 mm (k 3) und Blech 1,5 mm Al. Varianten: Breite 4/6/8/10/15/20 mm, Höhe 3/5 mm, Durchgänge 1/2/4/6, quer/längs, ΔT 5/8/10 K (864 Zeilen in ergebnis_nachtrag.json). k_Kühlmittel 0,40 als Annahme in eingaben.json eingetragen.

| Fall | Regel | Breite x Höhe | Durchg. | Führung | ΔT | Pack L/min | Re | h_Kanal | η | h_eff | U_gesamt | Δp bar | P_hyd W |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| LFP_P0 | alle_dT | 4 x 5 mm | 1 | quer | 10 K | 23.4 | 55 | 354 | 0.992 | 704 | 568 | 0.0027 | 0.11 |
| LFP_P0 | dT_max_5K | 4 x 5 mm | 1 | quer | 5 K | 46.7 | 110 | 375 | 0.991 | 746 | 595 | 0.0054 | 0.42 |
| LFP_P0 | bestes_U | 4 x 5 mm | 6 | quer | 5 K | 46.7 | 671 | 376 | 0.991 | 747 | 596 | 0.1976 | 15.39 |
| NMC_P4 | alle_dT | 4 x 5 mm | 1 | quer | 10 K | 10.0 | 25 | 341 | 0.992 | 678 | 551 | 0.0012 | 0.02 |
| NMC_P4 | dT_max_5K | 4 x 5 mm | 1 | quer | 5 K | 20.1 | 49 | 352 | 0.992 | 699 | 565 | 0.0024 | 0.08 |
| NMC_P4 | bestes_U | 4 x 5 mm | 4 | laengs | 5 K | 20.1 | 277 | 352 | 0.992 | 700 | 565 | 0.0749 | 2.51 |
| NMC_P3 | alle_dT | 4 x 5 mm | 1 | quer | 10 K | 14.5 | 35 | 346 | 0.992 | 688 | 557 | 0.0017 | 0.04 |
| NMC_P3 | dT_max_5K | 4 x 5 mm | 1 | quer | 5 K | 28.9 | 71 | 360 | 0.992 | 716 | 576 | 0.0035 | 0.17 |
| NMC_P3 | bestes_U | 4 x 5 mm | 4 | laengs | 5 K | 28.9 | 398 | 361 | 0.992 | 717 | 577 | 0.1079 | 5.20 |

Vergleich Basis (20 x 5 mm, quer, ΔT 5 K, LFP_P0): h_Kanal 316, h_eff 411, U_gesamt 361 W/(m²K) (ergebnis_nachtrag.json). Auswahl-Regel U ≥ 500 und Δp ≤ 0,5 bar, kleinste Pumpenleistung: siehe Zeilen "alle_dT" (ΔT frei) und "dT_max_5K".

Befunde (Entwurf, Opus prüft): Die Stegfläche hebt h auf der Grundfläche etwa auf das Doppelte (η ≈ 0,99). Mit schmalen Kanälen (4 mm, 5 mm hoch) liegt U_gesamt über 500; die Obergrenze setzt das Pad (1 mm/k 3 → 3000 W/(m²K) allein). Mäander (mehr Durchgänge) bringt kein nennenswert höheres U, nur mehr Δp und Pumpenleistung; die Umlenkverluste sind darin nur über den 30-%-Zuschlag erfasst (bei 4-6 Durchgängen vermutlich zu klein, Annahme). Der Re-Anstieg bei Mäander ist reine Kanalverlängerung bei weniger parallelen Kanälen. Offene Frage: Kontaktwiderstand Zelle-Pad und Pad-Blech nicht enthalten; ΔT-Wahl (Opus/Autor); Auswahl 4 mm-Kanäle fertigungstechnisch (Stege 3 mm, 281 Kanäle je Platte) bewerten.

Bild: nachtrag_U_leistung.png (Zielband U ≥ 500 beschriftet). Lesehilfe in k2_lesehilfe.md.


## 9 K2b: Blech 1/4/1 mm mit Mäander (ENT-152, Entwurf, Opus prüft)
Methode: kuehlplatte.k2b(), Eingaben eingaben.json (k2b), Ergebnis ergebnis_k2b.json (96 Varianten). Durchfluss fest 23 bzw. 20 L/min je Pack (ENT-107/108), daraus ΔT Kühlmittel: LFP_P0 10.2 K, NMC_P4 5.0 K (nicht frei gewählt). Umlenkung ζ 1,5 je Umlenkung (n−1), Annahme Opus. Kein Kontaktwiderstand.

**LFP_P0** (Kriterium U ≥ 500, kleinstes Δp; 20 von 48 Varianten erreichen U ≥ 500)

| Rang | Führung | n | w mm | Teilkanäle m | Re | h_Kanal | h_eff | U | Δp bar | P_hyd W | Masse 2 Platten kg |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | quer | 4 | 6 | 54 | 253 | 409 | 634 | 522 | 0.032 | 1.21 | 49.1 |
| 2 | quer | 6 | 10 | 25 | 391 | 442 | 610 | 506 | 0.049 | 1.87 | 43.1 |
| 3 | quer | 6 | 8 | 29 | 393 | 440 | 638 | 525 | 0.057 | 2.20 | 46.3 |
| 4 | laengs | 4 | 6 | 38 | 360 | 408 | 633 | 521 | 0.065 | 2.47 | 48.6 |
| 5 | quer | 8 | 40 | 5 | 621 | 544 | 607 | 504 | 0.066 | 2.54 | 40.1 |

**NMC_P4** (Kriterium U ≥ 500, kleinstes Δp; 16 von 48 Varianten erreichen U ≥ 500)

| Rang | Führung | n | w mm | Teilkanäle m | Re | h_Kanal | h_eff | U | Δp bar | P_hyd W | Masse 2 Platten kg |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | quer | 4 | 6 | 52 | 229 | 401 | 622 | 514 | 0.028 | 0.95 | 47.0 |
| 2 | quer | 6 | 8 | 28 | 354 | 430 | 623 | 515 | 0.052 | 1.72 | 44.1 |
| 3 | laengs | 4 | 6 | 38 | 313 | 401 | 621 | 514 | 0.054 | 1.79 | 46.7 |
| 4 | quer | 6 | 6 | 35 | 340 | 435 | 674 | 549 | 0.064 | 2.14 | 46.6 |
| 5 | quer | 8 | 15 | 13 | 481 | 477 | 608 | 505 | 0.066 | 2.20 | 37.7 |

Abgleich mit der Erwartung (Quelle ergebnis_k2b.json):
1. U ≥ 500 nur mit w ≤ ≈ 10 mm; w ≥ 40 bei U ≈ 350–420: **teilweise verfehlt.** w = 40 liegt bei U 405–518 (n = 4 längs LFP: 449), also über 420; einzelne breite Varianten (quer, n = 6–8) erreichen sogar U ≥ 500 (z. B. LFP n 8, w 40, quer: 504). Grund: kürzere Bahn bzw. weniger Teilkanäle erhöhen Re und Einlaufeffekt; Nu ≈ 5,4-Annahme gilt nur voll entwickelt.
2. Δp wächst mit n wie n² (LFP w 8 längs: n 2/4/6/8 = 0,013/0,051/0,120/0,215 bar). Δp n = 4: 0.051 bar, im Band 0,05–0,2 **erfüllt**; n = 8: 0.215 bar, Erwartung 0,4–1 **verfehlt** (kleiner).
3. Auswahl n = 4, w = 8, längs, LFP: U 487 (Erwartung ≈ 550) **verfehlt**, U < 500; Δp 0.051 < 0,3 bar und P_hyd 1.9 W < 15 W **erfüllt**. Die beste Variante nach Tabelle ist n = 4, w = 6, quer, (LFP U 522, Δp 0,032 bar).
4. Masse beider Platten ≈ 45 kg: **erfüllt** (alle Varianten 31.8–49.1 kg, Grenze 55 kg nicht überschritten).
Verfehlt-Kriterium (keine Variante U ≥ 500 bei Δp ≤ 0,5 bar): **nicht eingetreten** (LFP max U 594, NMC max U 581). Die Marge ist klein (U 505–525 knapp über 500, ΔU durch Kontaktwiderstände nicht abgedeckt).
Vorschlag (keine Entscheidung): n = 4, w = 6 mm, Bahnen quer (kürzeste Weglänge je Bahn, kleinstes Δp mit U ≥ 500 bei beiden Packs). Bei w = 8 längs, Erwartungsfall, U < 500. Rückfrage an Opus: Erwartungspunkt 3 verfehlt (U), Auswahl neu zu bewerten.

Bild: k2b_U_dp.png (Zielband beschriftet). Lesehilfe in k2_lesehilfe.md.

---
*KI-generiert (Claude Sonnet, 2026-11-19), Entwurf.*
