| Dok.-Nr. | BAT-DOC-06 | Version | 0.3 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Verifikationsplan (V-Modell-Matrix) | Ersteller | Claude Sonnet (KI), pm/plan/verifikation.py | Prüfer | – (Opus, Mensch offen) |

> **KI-generiert.** Entwurf, nicht vom Menschen freigegeben. Testprojekt „KI im Engineering“, kein Produkt. Erzeugt am 2026-11-23, nicht von Hand bearbeiten.

Quellen: `pm/anforderungen.json` (Anforderungen, Kriterien, Nachweisverweise) und die dort genannten Ergebnisdateien. Bewertungsstufen: `docs/17_workflow_schleife.md` §1. Bei Methode S ist die höchste Stufe „rechnerisch erfüllt (nicht validiert)“. Jedes Kriterium trägt seine Herkunft in eckigen Klammern; hängt eine Bewertung an einem Kriterium ohne Herkunft „Autor“, steht „(Kriterium Annahme, Autor offen)“ dahinter. Kriterien mit Herkunft Annahme Opus, Startwert oder Norm sind Vorschläge und stehen in `docs/19_freigaberunde.md`.

| REQ | Ebene | Methode | Kriterium | Ist-Wert mit Quelle | Bewertung |
|---|---|---|---|---|---|
| REQ-P01 | System | R | m_fahrzeug == 1500 kg [Autor] | LFP m_fahrzeug = 1500 [sim/chemie/varianten_lfp_nmc/ergebnis.json :: varianten.LFP.faelle.A.hauptwert.gesamtmasse_kg]; NMC m_fahrzeug = 1500 [sim/chemie/varianten_lfp_nmc/ergebnis.json :: varianten.NMC.faelle.A.hauptwert.gesamtmasse_kg] | nachgewiesen |
| REQ-P02 | System | A | E_brutto LFP >= 73.9 kWh [Startwert (Vorschlag)]<br>E_brutto NMC >= 73.9 kWh [Startwert (Vorschlag)] | [E_brutto LFP] LFP E_brutto = 73.92 [pm/bauteile/stueckliste_LFP.json :: summen.energie_kWh]<br>[E_brutto NMC] NMC E_brutto = 74.27 [pm/bauteile/stueckliste_NMC.json :: summen.energie_kWh] | nachgewiesen (Kriterium Annahme, Autor offen) |
| REQ-P03 | System | A | U_nenn zwischen [720, 880] V [Autor (Freigaberunde 2026-11-23)]<br>U_min vorhanden [Autor (Freigaberunde 2026-11-23)]<br>U_max vorhanden [Autor (Freigaberunde 2026-11-23)] | [U_nenn] U_nenn = 800 [sim/chemie/varianten_lfp_nmc/ergebnis.json :: systemspannung_V]<br>[U_min] kein Nachweis verknüpft<br>[U_max] kein Nachweis verknüpft | offen |
| REQ-P04 | System | S | P_spitze >= 150 kW [Autor (Freigaberunde 2026-11-23)]<br>P_dauer >= 60 kW [Autor (Freigaberunde 2026-11-23)] | [P_spitze] kein Nachweis verknüpft<br>[P_dauer] kein Nachweis verknüpft | offen |
| REQ-P05 | System | S | t_10_80 LFP <= 20 min [Autor]<br>t_10_80 NMC <= 30 min [Autor] | [t_10_80 LFP] blockiert: LFP ohne gemessenen Zellparametersatz nicht nachweisbar (bericht/bericht.tex, REQ-P05; sim/chemie/c2_kalibrierung/ERGEBNIS.md)<br>[t_10_80 NMC] NMC t_10_80 = 29.68 [sim/chemie/c2_kalibrierung/ergebnis_schnellladen_n4680.json :: N4680.2.zeit_10_80_min] | blockiert |
| REQ-P06 | System | I | CAD_Pack LFP vorhanden [Autor]<br>CAD_Pack NMC vorhanden [Autor] | [CAD_Pack LFP] LFP CAD_Pack = vorhanden [cad/baukasten/ausgabe/ergebnis_LFP.json :: teile]<br>[CAD_Pack NMC] NMC CAD_Pack = vorhanden [cad/baukasten/ausgabe/ergebnis_NMC.json :: teile] | nachgewiesen |
| REQ-P07 | System | I | B <= 1430 mm [Autor (Freigaberunde 2026-11-23)]<br>L <= 2400 mm [Autor (Freigaberunde 2026-11-23)]<br>H <= 130 mm [Autor (Freigaberunde 2026-11-23)]<br>H_dom <= 250 mm [Autor (Freigaberunde 2026-11-23)]<br>Masse LFP <= 528 kg [Autor (Freigaberunde 2026-11-23)]<br>Masse NMC <= 370 kg [Autor (Freigaberunde 2026-11-23)] | [B] LFP B = 1430 [cad/baukasten/ausgabe/ergebnis_LFP.json :: breite_mm]; NMC B = 1430 [cad/baukasten/ausgabe/ergebnis_NMC.json :: breite_mm]<br>[L] LFP L = 2373 [cad/baukasten/ausgabe/ergebnis_LFP.json :: laenge_mm]; NMC L = 2273 [cad/baukasten/ausgabe/ergebnis_NMC.json :: laenge_mm]<br>[H] LFP H = 117 [cad/baukasten/ausgabe/ergebnis_LFP.json :: ctx.z_deckel_o]; NMC H = 111 [cad/baukasten/ausgabe/ergebnis_NMC.json :: ctx.z_deckel_o]<br>[H_dom] LFP H_dom = 244.8 [cad/baukasten/ausgabe/ergebnis_LFP.json :: hoehe_max_mm]; NMC H_dom = 227.8 [cad/baukasten/ausgabe/ergebnis_NMC.json :: hoehe_max_mm]<br>[Masse LFP] LFP Masse = 626.8 [pm/bauteile/stueckliste_LFP.json :: summen.masse_stueckliste_kg]<br>[Masse NMC] NMC Masse = 486.4 [pm/bauteile/stueckliste_NMC.json :: summen.masse_stueckliste_kg] | verfehlt (Kriterium Annahme, Autor offen) |
| REQ-P08 | System | S | T_betrieb zwischen [-20, 45] °C [Autor (Freigaberunde 2026-11-23)]<br>T_laden zwischen [0, 45] °C [Autor (Freigaberunde 2026-11-23)] | [T_betrieb] kein Nachweis verknüpft<br>[T_laden] kein Nachweis verknüpft | offen |
| REQ-P09 | Subsystem | S | T_max <= 45 °C [Autor (Freigaberunde 2026-11-23)]<br>Spreizung <= 5 K [Autor (Freigaberunde 2026-11-23)] | [T_max] LFP T_max = 35.57 [sim/kuehlung/k3_gesamt/elmer_LFP_P0_V4p/ergebnis.json :: T_max_Zellblock_C]; NMC T_max = 30.6 [sim/kuehlung/k3_gesamt/elmer_NMC_P4_V4p/ergebnis.json :: T_max_Zellblock_C]<br>[Spreizung] LFP Spreizung = 9.573 [sim/kuehlung/k3_gesamt/elmer_LFP_P0_V4p/ergebnis.json :: dT_Zellblock_K]; NMC Spreizung = 2.574 [sim/kuehlung/k3_gesamt/elmer_NMC_P4_V4p/ergebnis.json :: dT_Zellblock_K] | verfehlt (Kriterium Annahme, Autor offen) |
| REQ-P10 | System | S | SOH >= 70 % [Autor (Freigaberunde 2026-11-23)] | kein Nachweis verknüpft | offen |
| REQ-P11 | System | T | t_warnung >= 5 min [Norm (W35d belegt: UN R100 42024X1955, Warnung 5 min vor gefährlicher Situation im Fahrgastraum)] | kein Nachweis verknüpft | offen |
| REQ-P12 | Subsystem | S | Kuehlmittel vorhanden [Autor (Freigaberunde 2026-11-23)]<br>dp_Platte <= 0.5 bar [Autor (Freigaberunde 2026-11-23)]<br>Verteilung_abw <= 10 % [Autor (Freigaberunde 2026-11-23)] | [Kuehlmittel] LFP Kuehlmittel = vorhanden [pm/bauteile/stueckliste_LFP.json :: positionen[bt=BT-650].werkstoff]<br>[dp_Platte] dp_Platte = 0.1709 [sim/kuehlung/k5_parallel/ergebnis_verteiler.json :: gruppen.faelle.k2_d25_x3.dp_bar]<br>[Verteilung_abw] Verteilung_abw = 2.05 [sim/kuehlung/k5_parallel/ergebnis_verteiler.json :: gruppen.faelle.k2_d25_x3.max_abw_pct] | rechnerisch erfüllt (nicht validiert) (Kriterium Annahme, Autor offen) |
| REQ-P13 | System | T | R_iso >= 100 Ω/V [Autor (Freigaberunde 2026-11-23)]<br>Schutzart == IP67 [Autor (Freigaberunde 2026-11-23)] | [R_iso] kein Nachweis verknüpft<br>[Schutzart] kein Nachweis verknüpft | offen |
| REQ-P14 | System | S | dy_a <= 0.5 mm [Autor (Freigaberunde 2026-11-23)]<br>dy_b <= 0.5 mm [Autor (Freigaberunde 2026-11-23)] | [dy_a] LFP dy_a = 6.732 [sim/mechanik/x3_crash_g5/ergebnis.json :: LFP_a.zellblock_vorderseite_dy_max_mm]; NMC dy_a = 8.279 [sim/mechanik/x3_crash_g5/ergebnis.json :: NMC_a.zellblock_vorderseite_dy_max_mm]<br>[dy_b] LFP dy_b = 0.0188 [sim/mechanik/x3_crash_g5/ergebnis.json :: LFP_b.zellblock_vorderseite_dy_max_mm]; NMC dy_b = 2.591 [sim/mechanik/x3_crash_g5/ergebnis.json :: NMC_b.zellblock_vorderseite_dy_max_mm] | verfehlt (Kriterium Annahme, Autor offen) |
| REQ-P15 | Subsystem | I | CMU vorhanden [Autor (Freigaberunde 2026-11-23)]<br>Temperaturfuehler vorhanden [Autor (Freigaberunde 2026-11-23)]<br>Isolationswaechter vorhanden [Autor (Freigaberunde 2026-11-23)] | [CMU] LFP CMU = vorhanden [pm/bauteile/stueckliste_LFP.json :: positionen[bt=BT-320].pos]; NMC CMU = vorhanden [pm/bauteile/stueckliste_NMC.json :: positionen[bt=BT-320].pos]<br>[Temperaturfuehler] LFP Temperaturfuehler = vorhanden [pm/bauteile/stueckliste_LFP.json :: positionen[bt=BT-330].pos]; NMC Temperaturfuehler = vorhanden [pm/bauteile/stueckliste_NMC.json :: positionen[bt=BT-330].pos]<br>[Isolationswaechter] LFP Isolationswaechter = vorhanden [pm/bauteile/stueckliste_LFP.json :: positionen[bt=BT-350].pos]; NMC Isolationswaechter = vorhanden [pm/bauteile/stueckliste_NMC.json :: positionen[bt=BT-350].pos] | nachgewiesen (Kriterium Annahme, Autor offen) |
| REQ-P16 | System | A | Kosten_Summe LFP vorhanden [Autor]<br>Kosten_Summe NMC vorhanden [Autor]<br>Anteil_Schaetzung LFP vorhanden [Autor]<br>Anteil_Schaetzung NMC vorhanden [Autor] | [Kosten_Summe LFP] LFP Kosten_Summe = vorhanden [pm/kosten/ergebnis_LFP.json :: summe_eur_pack]<br>[Kosten_Summe NMC] NMC Kosten_Summe = vorhanden [pm/kosten/ergebnis_NMC.json :: summe_eur_pack]<br>[Anteil_Schaetzung LFP] LFP Anteil_Schaetzung = vorhanden [pm/kosten/ergebnis_LFP.json :: anteil_schaetzung_an_summe_pct]<br>[Anteil_Schaetzung NMC] NMC Anteil_Schaetzung = vorhanden [pm/kosten/ergebnis_NMC.json :: anteil_schaetzung_an_summe_pct] | nachgewiesen |
| REQ-D01 | Prozess | R | Pruefskript rc0 [Autor] | Pruefskript = rc 0 [python3 pm/pm.py pruefe] | nachgewiesen |
| REQ-D02 | Prozess | R | Nachweisdatei vorhanden [Autor] | kein Nachweis verknüpft | offen |
| REQ-D03 | Prozess | R | Nachweisdatei vorhanden [Autor] | Nachweisdatei = vorhanden [docs/03_anforderungsverfolgung.md] | nachgewiesen |
| REQ-D04 | Prozess | R | Nachweisdatei vorhanden [Autor] | Nachweisdatei = vorhanden [docs/08_ki_einsatz_protokoll.md] | nachgewiesen |
| REQ-D05 | Prozess | R | Nachweisdatei vorhanden [Autor] | Nachweisdatei = vorhanden [docs/00_dokumentenlenkung.md] | nachgewiesen |
| REQ-D06 | Prozess | R | Nachweisdatei vorhanden [Autor] | kein Nachweis verknüpft | offen |
| REQ-D07 | Prozess | R | Nachweisdatei vorhanden [Autor] | Nachweisdatei = vorhanden [.gitignore]; Nachweisdatei = vorhanden [docs/10_lizenzen_und_quellen.md] | nachgewiesen |
| REQ-D08 | Prozess | R | Nachweisdatei vorhanden [Autor] | Nachweisdatei = vorhanden [forschung/AUFTRAG_PATENTE.md] | nachgewiesen |
| REQ-D09 | Prozess | R | Nachweisdatei vorhanden [Autor] | Nachweisdatei = vorhanden [SOFTWARE.md] | nachgewiesen |
| REQ-D11 | Prozess | R | Pruefskript rc0 [Autor] | Pruefskript = rc 0 [python3 pm/pm.py pruefe] | nachgewiesen |
| REQ-D12 | Prozess | R | Nachweisdatei vorhanden [Autor] | Nachweisdatei = vorhanden [pm/gespraech.sh] | nachgewiesen |
| REQ-D13 | Prozess | R | Nachweisdatei vorhanden [Autor] | Nachweisdatei = vorhanden [video/abschluss.mp4] | nachgewiesen |
| REQ-D14 | Prozess | R | Nachweisdatei vorhanden [Autor] | Nachweisdatei = vorhanden [praesentation/unternehmenspraesentation.pptx] | nachgewiesen |
| REQ-D10 | Prozess | R | Nachweisdatei vorhanden [Autor] | Nachweisdatei = vorhanden [docs/08_ki_einsatz_protokoll.md] | nachgewiesen |
| REQ-G01 | System | R | Anwendbarkeit_belegt vorhanden [Norm (W37c.nachtrag belegt: VO 2023/1230 Art. 2 Abs. 2 g)] (nicht anwendbar (zu belegen, W37)) | Anwendbarkeit_belegt = vorhanden [forschung/ergebnis/W37c.nachtrag.md] | nachgewiesen (Kriterium Annahme, Autor offen) |
| REQ-G02 | System | R | Batteriepass_Datensatz vorhanden [Autor (Freigaberunde 2026-11-23)] (festgelegt) | kein Nachweis verknüpft | offen |

## Zählung je Bewertung

| Bewertung | Anzahl |
|---|---|
| nachgewiesen | 18 |
| rechnerisch erfüllt (nicht validiert) | 1 |
| verfehlt | 3 |
| offen | 9 |
| blockiert | 1 |
| **gesamt** | 32 |

## Zählung davon mit vom Autor bestätigtem Kriterium

Gezählt werden Anforderungen, bei denen jedes Kriterium die Herkunft „Autor“ hat.

| Bewertung | Anzahl |
|---|---|
| nachgewiesen | 15 |
| rechnerisch erfüllt (nicht validiert) | 0 |
| verfehlt | 0 |
| offen | 2 |
| blockiert | 1 |
| **gesamt** | 18 |

## Anhang: früherer Stand v0.1 (Opus, 2026-11-11, unverändert übernommen)

| Nr | REQ | Methode | Werkzeug | Erwartung vorher in | Abnahmekriterium |
|---|---|---|---|---|---|
| VER-001 | – | PyBaMM-Modell gegen veröffentlichte Messkurve des Parametersatzes | PyBaMM | sim/chemie/ERWARTUNG.md | Abweichung festlegen (Annahme) |
| VER-002 | REQ-P09 | Zelltemperatur beim Auslegungsfall | Elmer | sim/kuehlung/ERWARTUNG.md | Grenze aus REQ-P09 |
| VER-003 | REQ-D01 | Zitate in Rechercheergebnissen | pruefe.py | – | 0 Fehler |

---
*KI-generiert (Claude Sonnet, 2026-11-23). Status Entwurf. Freigabe nur durch den Autor.*
