| Dok.-Nr. | ERG-E2 | Version | 0.4 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Ergebnis E2 (Rechnung, Akten, CAD Schaltbox hinten, CMU, FPC, HV intern, Bilder) | Ersteller | Claude Sonnet (KI) | Prüfer | Opus (offen) |

> KI-generiert (Claude Sonnet, 2026-11-18). Entwurf. Die Abschnitte „Version 0.2“ (Fall b vorn, ENT-109) und „Version 0.3“ sind überholt; maßgebend ist „Version 0.4“ am Ende. Zahlen aus `ergebnis.json` (dieser Ordner), erzeugt von `elektronik.py` aus `eingaben.json`.

## Abgleich mit ERWARTUNG.md
| Punkt | Erwartung | LFP | NMC | Urteil |
|---|---|---|---|---|
| 1 Spannungsabgriffe | 251 / 218 | 251 | 218 | ok |
| 1 Messleitungslänge 25–40 m | 25–40 m | 11.8 m (davon 8.0 m mit Platz im Seitenspalt) | 30.7 m | NMC im Band; LFP **unter dem Band** und nur teilweise platzierbar (v0.3) |
| 2 Ausgleich 1,85 Ah | ≈ 12 h | 12.32 h (150 mA) | 14.22 h (130 mA, ENT-146) | ok (< 24 h), `ergebnis.json` |
| 2 Wärme je CMU ≤ 10 W (18 Kanäle, Höchstspannung) | ≤ 10 W | 9.85 W | 9.83 W (130 mA) | ok beide (v0.3, vorher NMC 11,34 W) |
| 3 Vorladung | ≈ 8 A, 320 J, ≤ 300 ms | 8,0 A, 320 J, t95 = 300 ms | gleich | ok |
| 4 Heizung 5 kW, 25 K | LFP 40 min, NMC 30–35 min | 11,56 MJ, 38,5 min | 7,70 MJ, 25,7 min | LFP ok; **NMC verfehlt** (unter Band): Zellmasse 308 kg (868 × 0,355 kg) statt der in der Erwartung angenommenen Größenordnung |
| 6 HV intern (Erwartung 3–5 m, ≤ 15 W; Nachtrag 1: 12,95 / 9,49 W je m) | ≤ 15 W | 38,8–64,7 W bei 3–5 m (12,95 W je m Leiter) | 28,5–47,5 W bei 3–5 m (9,49 W je m, 139 A) | **v0.3:** LFP nicht gebaut; NMC gebaut 1.19 m, 11.3 W (Fußnote unten). Erwartung 3–5 m / 15 W durch Opus-Nachtrag 1 überholt |

Punkt 2 ergänzt (Höchstspannung nach Opus-Antwort 5, `ergebnis.json` Felder `cmu_W_alle_kanaele_umax`, Eingabe `eingaben.json` `u_max_V`): LFP 18 × 0,15 A × 3,65 V = 9,855 W (≤ 10 W, ok); NMC 18 × 0,15 A × 4,2 V = 11,34 W (**> 10 W, Erwartung verfehlt**; bei Nennspannung 9,95 W).

## Version 0.2 (2026-11-18, Auftrag „Fortsetzung“)
**1. Akten:** ENT-110 bis ENT-143 (34 Akten, Status „vorgeschlagen“, wer „Opus (Annahme ERW-E2)“, belege B-BAT-024). `pm.py pruefe`: 143 Entscheidungen, 0 Fehler; `pm.py register` gelaufen. Zuordnung: BT-300 (110), BT-320 (111–115), BT-330 (116–117), BT-340 (118–119), BT-350 (120), BT-360 (121–122), BT-711 (123–124), BT-712 (125–126), BT-713 (127–129), BT-720 (130–131), BT-730 (132–133), BT-740 (134), BT-760 (135–136), BT-770 (137), BT-310 (138–141), BT-430 Biegeradius (142 LFP 70 mm, 143 NMC 60 mm).
**Fehlende Merkmale in `struktur.json` (Wert aus ERW-E2, deshalb keine Akte):**
- BT-350: zweiter Ansprechwert Fehler 80 kΩ (nur `ansprechwert_kOhm`, dort Warnung 400 kΩ eingetragen)
- BT-712: C_ZK 1000 µF
- BT-713: nur Maße/Masse der Sicherungen; BT-711 Maße und Masse; Vorladeschütz und -widerstand (BT-712 Maße)
- BT-320: Maße CMU-Platine 120 × 60 × 10 mm, Masse; BT-360: Dicke 0,3 mm, Halter 3 mm, Masse je m
- BT-430: Außendurchmesser 14/12 mm; BT-720, BT-730, BT-740, BT-770: Maße und Masse
- BT-730: zweiter Stecker 40 A (Nebenverbraucher); BT-720: Lage/Maße (nur `nennstrom_A`, `einbauort`)
- BT-710: Maße Schaltbox ohne Merkmalwert (aus Inhalt gerechnet); BT-710/310 Halter für den Höhenzuwachs
Alle diese Maße stehen als `A_e2_*` in `cad/pack/entwurf_parameter.py` (Herkunft „ERW-E2 N1“). Neue Annahme als Platzhalter: `A_e2_box_teilabstand_mm` = 10 mm (Abstand der Teile in der Schaltbox, nicht in ERW-E2 gesetzt).

**2. CAD Fall b** (`cad/pack/pack.py`, Schalter `PACK_E2=1`, Ausgabe `cad/pack/entwurf/ergebnis_<V>_e2.json`, `pack_<V>_e2.FCStd`; G4-Dateien unverändert). Gebaut: Schaltbox Al 2 mm mit BMS-Platine, Shunt, 2 Hauptschütze, Vorladeschütz + Widerstand, Pyro- und Schmelzsicherung; daneben auf dem Deckel HV-Stecker 250 A und 40 A, NV-Stecker, Gas-/Drucksensor. Vorne = x klein (nur Benennung), Box mittig in y, Fuß bei x = 30 mm.
| Größe | LFP | NMC | Fundstelle |
|---|---|---|---|
| Schaltbox L × B × H | 320 × 290 × 89 mm | 320 × 290 × 89 mm | `ergebnis_<V>_e2.json` e2.schaltbox_* |
| Höhenzuwachs Fall b (ohne Halter) | 89 mm | 89 mm | e2.hoehenzuwachs_gesamt_mm |
| Packhöhe gesamt | 210 mm (Stapel 121) | 204 mm (Stapel 115) | hoehe_mm, e2.hoehe_stapel_vor_e2_mm |
| Kollisionen | 0 bei 393 Paaren | 0 bei 5387 Paaren | anzahl_kollisionen, kollisionspaare_geprueft |
| Masse E2 gebaute Teile | 3,99 kg | 3,99 kg | gruppen E2_* (Box 1,56 + Inhalt 1,80 + Stecker/Sensor 0,63) |
| Masse Pack mit E2-Teilen | 615,9 kg | 477,3 kg | masse_bekannt_kg (G4 ohne E2: 611,9 / 473,4) |
| CMU-Masse (nicht gesetzt) | 1,12 kg (14) | 1,04 kg (13) | e2.cmu_masse_kg |
**Nicht gebaut (Abbruch nach Auftrag, Fragen an Opus):**
1. **HV-Leitungen intern / Service-Trennstecker:** `pack.py` legt keine Reihenfolge der Zellen in Reihe fest (nur Hüllkörper und Verbinder ohne Polarität). Mit der einfachsten Führung (je ein Strang pro Zellreihe, LFP: zwei Reihen, NMC: Gruppen-Reihen in Längsrichtung) liegen die beiden Kettenenden an einem Packende und die Kettenmitte am anderen. Dann muss eine Leitung längs durch das Pack (Länge ≈ Gehäuselänge 2030 / 1950 mm, `ergebnis_<V>_e2.json` gehaeuse_L_mm). Freier Querschnitt längs: LFP Spalt Zellende–Seitenrahmen 4 mm, davon 3 mm Zellverbinder (1 mm frei; Leitung Ø 14 mm) bzw. mit Halter ≥ 3,3 mm nur außerhalb des Verbinderbandes; NMC: Verbinderebene 0 mm frei (Abgriff und Gruppenverbinder bis zum Pad). Eine längs geführte HV-Leitung passt also nicht. Eine vierstrangige Führung (Anfang, Mitte und Ende am selben Packende) würde das vermeiden, ist aber eine Verschaltungsentscheidung (G3). → OPUS.
2. **CMU-Platinen in den Endzonen (120 × 60 × 10 mm):** Freier Abstand Rahmeninnenkante bis erste Zelle vorn: LFP 3,0 mm (`e2.freier_spalt_endzone_vorn_mm`), NMC 41,6 mm (derselbe Wert; Zellträger und Verguss belegen dort bis halbe Zellhöhe). Die kleinste Plattenkante 60 mm passt in keinem Fall flach. → OPUS (Lage ändern, z. B. CMU auf dem Deckel neben der Schaltbox, oder Endzone vergrößern).
3. **FPC-Messleitungen:** nicht gebaut, weil sie ohne CMU-Lage kein Ziel haben. Messleitungslänge (Punkt 1) und FPC-Masse offen.
4. **Höhe:** Packhöhe mit Schaltbox 210 / 204 mm gegenüber `A_hoehe_max_mm` = 130 mm (M0, Annahme, `cad/pack/entwurf/ergebnis_<V>_e2.json` e2.hoehe_max_A_mm). Der Höhenzuwachs 89 mm liegt unter der Abbruchgrenze 120 mm; ob 130 mm für die Packhöhe oder den Stapel gilt, ist offen. → OPUS.

**3. Bilder:** `schaltbild_LFP.png`, `schaltbild_NMC.png` (matplotlib, `schaltbild.py`; Werte aus `parameter_<V>.json`), angesehen, Beschriftung lesbar. **Renders und `kabelplan_<V>.png` nicht erstellt** (CMU, FPC und HV-Leitungen offen, ein Render ohne sie wäre irreführend). Lesehilfe `lesehilfe.md` (nur Schaltbilder). Baustein `praesentation/bausteine/E2.md` (Entwurf).
**Kabelplan (von/nach/Länge/Querschnitt):** nicht lesbar, weil die Längen von den offenen Punkten 1 und 2 abhängen. Querschnitte aus Akten: LFP 50 mm², NMC 35 mm² (ENT-100/101), Biegeradius 70/60 mm (ENT-142/143).
**Punkte 6 und 7 der Erwartung (HV-Verlust, Elektronikmasse gesamt):** offen aus demselben Grund. Gebaute Teile 3,99 kg plus CMU 1,12/1,04 kg = 5,1/5,0 kg (ohne FPC, Leitungen, Service-Trennstecker; unter dem Band 12–18 kg).

## Offene Fragen an Opus
1. HV längs durch das Pack (Punkt 1 oben) und Verschaltungsfolge (G3).
2. CMU-Lage (Punkt 2 oben).
3. Gesamthöhe 210/204 mm gegen 130 mm (Punkt 4 oben); Halter der Schaltbox (Höhe fehlt).
4. Platzhalter `A_e2_box_teilabstand_mm` = 10 mm bestätigen oder ersetzen.
5. NMC CMU-Wärme 11,34 W > 10 W bei 4,2 V: Erwartung verfehlt, Deutung durch Opus.
6. Fehlende Merkmale (Liste oben) in `struktur.json` aufnehmen.
7. Lage des Service-Trennstecker-Mittelpunktes und des Gas-/Drucksensors im Pack (hier nur auf dem Deckel neben der Schaltbox, Sensor nicht in der Packmitte).

Dateien: `cad/pack/entwurf/ergebnis_LFP_e2.json`, `ergebnis_NMC_e2.json`; große Dateien (STEP, Netze NMC) in `/home/cae/cae_projekte/batterie/e2/` (Links in `cad/pack/entwurf/`); FCStd in `cad/pack/entwurf/`.


## Version 0.3 (2026-11-18, Auftrag „Fortsetzung 2“: Schaltbox hinten, Mäander, CMU, FPC, HV intern)
Quellen: `cad/pack/entwurf/ergebnis_LFP_e2.json`, `ergebnis_NMC_e2.json` (Block `e2`), `sim/elektrik/e2_elektronik/ergebnis.json`. Läufe: `pack.py` mit `PACK_E2=1` (LFP 3 s, NMC 140 s, nice, `systemd-run --user --scope`), Renders Blender Cycles CPU 24 Samples. Große Dateien (Netze, STEP, Renderrohbilder): `/home/cae/cae_projekte/batterie/e2/` (Links `cad/pack/entwurf/*.step`, `netz_*_e2*.json`).

**1. Akten** (vorgeschlagen, `pm.py pruefe`: 147 Entscheidungen, 0 Fehler; `register` gelaufen):
- **ENT-145** BT-200 verschaltung = maeander, nur NMC. **LFP: nicht machbar** (siehe 2).
- **ENT-146** BT-320 ausgleichsstrom_mA = 130, NMC. ENT-115 auf variante [LFP] gesetzt.
- **ENT-147** BT-000 bauraum_laenge_mm = 2050, LFP, ersetzt ENT-102 (vom Autor entschieden, bleibt Status Entwurf bis Freigabe). NMC bleibt ENT-103 (1950).
- Hinweis: ENT-138 (BT-310 einbauort „deckel_vorne“, vorgeschlagen) widerspricht ENT-144 (BMS in der Box, Box hinten). Nicht geändert, weil nicht beauftragt. → Opus.

**2. Verschaltung machbar?**
| | LFP | NMC |
|---|---|---|
| Ergebnis | **nein** | **ja** |
| Grund | 250s1p in nur 2 Reihen zu je 125 Zellen. Plus, Mitte und Minus hinten brauchen 4 Durchläufe (hin und zurück je Hälfte), die Reihen ergeben 2. Mit 2 Durchläufen liegt die Mitte (Zelle 125) vorn bei x = 50 mm; die Leitung dorthin wäre ≈ 1990 mm lang (nicht gebaut, Querschnitt frei nur ≈ 1 mm, siehe v0.2). Nicht untersucht: Überspringen jeder zweiten Zelle (Verbinder über Nachbarzelle) | 28 Spalten × 31 Reihen. 4 Bänder zu 7 Spalten, je Band ein Spaltenzug (Zickzack entlang x). Gruppen je Band [56, 56, 56, 49]; Plus, Mitte (2 Anschlüsse nebeneinander, y 677 / 725) und Minus alle in der letzten Reihe hinten (`alle_anschluesse_hinten` = true) |
| Nebenwirkung | – | Hälfte A 112 / B 105 Gruppen (nicht 108,5): ≈ 413 V / 387 V Nennspannung bei 800 V. Zellschritt normal 48 mm, 84 Schritte länger (Querträger, fehlende Reihe), größter 231 mm. G4-Gruppenverbinder (4 Zellen quer) stimmen mit dieser Folge nicht überein, Verbinder nicht umgebaut |

**3. CAD** (`pack.py` PACK_E2=1; Box hinten bündig mit Rahmeninnenkante, Trennstecker über den Mittenanschlüssen, Box daneben (+y); Stecker/Sensor vor der Box auf dem Deckel; CMU 10 mm dick (x) × 120 (y) × 60 (z) an den Rahmen gelehnt):
| Größe | LFP | NMC | Fundstelle |
|---|---|---|---|
| Gehäuselänge | 2050 mm | 1950 mm | gehaeuse_L_mm |
| Packhöhe mit Turm (Stapel + 89) | 210 mm (121 + 89) | 204 mm (115 + 89) | hoehe_mm; Grenze M0 130 mm Annahme, Turm erlaubt bis 210 (ENT-144) |
| Freier Abstand Endzone vorn / hinten | 13.0 / 16.0 mm | 41.6 / 71.4 mm | e2.freier_abstand_endzone_* (CMU 10 mm passt) |
| CMU vorn / hinten | 7 / 7 | 11 / 2 | e2.cmu_seite (Endzone = die mit kleinerem fernsten Abstand, Kapazität 11 je Endzone) |
| Messleitung FPC gesamt | 11.77 m (14 Stücke, 6 ohne Platz) | 30.73 m (13 Stücke, 0 ohne Platz) | e2.fpc_laenge_gesamt_m |
| HV intern | nicht gebaut | 1.194 m = Plus 744 + Minus 408 + Mitte 2 × 11 + 20 mm Box → HV-Stecker | e2.hv, e2.hv_laenge_gesamt_m |
| HV-Verlust bei Ladestrom | – (LFP: ≈ +26 W allein für eine Längsleitung, nur Rechnung) | 11.34 W (9.49 W/m × 1.194 m, 139 A) | e2.hv_verlust_W; W/m aus `ergebnis.json` hv_W_je_m_Leiter_laden |
| Elektronikmasse (Box, Inhalt, Stecker, CMU, FPC; ohne HV-Leitungen) | 5.70 kg | 6.77 kg | e2.masse_elektronik_ohne_hv_leitungen_kg. HV-Leitungsmasse offen (Dichte Cu/Isolierung fehlt in den Akten) |
| Masse Pack mit E2-Teilen | 618.8 kg | 479.6 kg | masse_bekannt_kg (G4 ohne E2: 611,9 / 473,4) |
| **Kollisionen** | **9** bei 812 Paaren | **0** bei 6677 Paaren | anzahl_kollisionen |
LFP-Kollisionen: alle 9 sind FPC (20 mm breit, Spur oben/unten im Seitenspalt) gegen Querträger_1…3 (je 171,6 mm³ = 2 mm Überlappung: Spur 25…45 mm über Zellmitte gegen Querträger-Oberkante 27 mm, über dem Querträger sind nur 18 mm frei). Zusätzlich passen nur 2 Spuren je Seitenspalt: von 14 FPC-Stücken sind 8 gebaut, 6 nicht (nicht gebaut, Länge gezählt). Eine 20-mm-FPC (ENT-122) mit Halter 3 mm (`A_e2_fpc_halter_mm`, Halter zusätzlich zur Dicke 0,3 mm) passt im LFP-Seitenspalt (4 mm) nur außerhalb des Verbinderbandes (Zellmitte ± 12,5 mm) und des Querträgerbandes (± 27 mm), und nur in 2 Spuren. In der LFP-Endzone (frei 13,0 mm vorn, 16,0 mm hinten bei 2050 mm) steht die CMU (10 mm), die FPC-Querstücke (0,3 mm) liegen im Rest.
NMC: FPC liegt 0,3 mm dick auf der Verbinderebene (über Gruppenverbindern, unter dem Pad). Das Pad oben ist um die FPC ausgespart (Aussparung `Pad_oben` 130 cm³); Verguss um die CMU ausgespart (`Verguss_f0` 396 cm³, `Verguss_f3` 72 cm³: Verguss im Modell ist ein Vollblock in der Endzone). HV-Leitungen führen durch Pad, Kühlplatte oben und Deckel (Durchführungen: Kühlplatte 3.6 cm³, Deckel 0.9 cm³). Biegeradius 60 mm (ENT-143) eingehalten (Bogen R = 60 mm, Leitungsachse ≥ 10 mm über dem Trennstecker, Abstand = Platzhalter `A_e2_box_teilabstand_mm`).
Stichleitungen von der FPC zu den Abgriffen sind in NMC nur gerechnet (Länge in `e2.fpc[].davon_stichleitungen_mm`), nicht gezeichnet; LFP-Abgriffe an den inneren Zellenden (zwischen Reihe 0 und 1) sind nicht modelliert.

**4. Kabelplan** (`kabelplan_LFP.png`, `kabelplan_NMC.png`, Skript `kabelplan.py`; Tabelle aus `kabelplan_tabelle.md`):
| Variante | von | nach | Länge mm | Querschnitt / Art |
|---|---|---|---|---|
| LFP | Plus / Mitte / Minus | Schaltbox / Trennstecker | nicht gebaut (Verschaltung nicht machbar) | 50 mm² Cu |
| LFP | CMU 03 Reihe 0 | Zellverbinder-Abgriffe (Reihe 0, Seitenspalt) | 1182 | FPC 20 mm breit |
| LFP | CMU 04 Reihe 0 | Zellverbinder-Abgriffe (Reihe 0, Seitenspalt) | 1003 | FPC 20 mm breit |
| LFP | CMU 05 Reihe 0 | Zellverbinder-Abgriffe (Reihe 0, Seitenspalt), kein Platz | 853 | FPC 20 mm breit |
| LFP | CMU 06 Reihe 0 | Zellverbinder-Abgriffe (Reihe 0, Seitenspalt), kein Platz | 674 | FPC 20 mm breit |
| LFP | CMU 07 Reihe 1 | Zellverbinder-Abgriffe (Reihe 1, Seitenspalt) | 569 | FPC 20 mm breit |
| LFP | CMU 08 Reihe 1 | Zellverbinder-Abgriffe (Reihe 1, Seitenspalt) | 748 | FPC 20 mm breit |
| LFP | CMU 09 Reihe 1 | Zellverbinder-Abgriffe (Reihe 1, Seitenspalt), kein Platz | 898 | FPC 20 mm breit |
| LFP | CMU 10 Reihe 1 | Zellverbinder-Abgriffe (Reihe 1, Seitenspalt) | 1530 | FPC 20 mm breit |
| LFP | CMU 02 Reihe 0 | Zellverbinder-Abgriffe (Reihe 0, Seitenspalt) | 1126 | FPC 20 mm breit |
| LFP | CMU 11 Reihe 1 | Zellverbinder-Abgriffe (Reihe 1, Seitenspalt) | 1111 | FPC 20 mm breit |
| LFP | CMU 01 Reihe 0 | Zellverbinder-Abgriffe (Reihe 0, Seitenspalt) | 736 | FPC 20 mm breit |
| LFP | CMU 12 Reihe 1 | Zellverbinder-Abgriffe (Reihe 1, Seitenspalt), kein Platz | 721 | FPC 20 mm breit |
| LFP | CMU 00 Reihe 0 | Zellverbinder-Abgriffe (Reihe 0, Seitenspalt), kein Platz | 317 | FPC 20 mm breit |
| LFP | CMU 13 Reihe 1 | Zellverbinder-Abgriffe (Reihe 1, Seitenspalt), kein Platz | 302 | FPC 20 mm breit |
| NMC | Plus | Schaltbox | 744 | 35 mm² Cu |
| NMC | Minus | Schaltbox | 408 | 35 mm² Cu |
| NMC | Mitte_A_Ende_Band2 | Trennstecker | 11 | 35 mm² Cu |
| NMC | Mitte_B_Anfang_Band3 | Trennstecker | 11 | 35 mm² Cu |
| NMC | Schaltbox | HV-Stecker 250 A (2 Leitungen) | 20 (gesamt) | 35 mm² Cu |
| NMC | CMU 00 | Zellverbinder-Abgriffe (Verbinderebene unter Pad) | 2512 | FPC 20 mm breit |
| NMC | CMU 01 | Zellverbinder-Abgriffe (Verbinderebene unter Pad) | 2922 | FPC 20 mm breit |
| NMC | CMU 02 | Zellverbinder-Abgriffe (Verbinderebene unter Pad) | 2802 | FPC 20 mm breit |
| NMC | CMU 03 | Zellverbinder-Abgriffe (Verbinderebene unter Pad) | 2598 | FPC 20 mm breit |
| NMC | CMU 04 | Zellverbinder-Abgriffe (Verbinderebene unter Pad) | 2346 | FPC 20 mm breit |
| NMC | CMU 05 | Zellverbinder-Abgriffe (Verbinderebene unter Pad) | 2286 | FPC 20 mm breit |
| NMC | CMU 06 | Zellverbinder-Abgriffe (Verbinderebene unter Pad) | 2430 | FPC 20 mm breit |
| NMC | CMU 07 | Zellverbinder-Abgriffe (Verbinderebene unter Pad) | 2502 | FPC 20 mm breit |
| NMC | CMU 08 | Zellverbinder-Abgriffe (Verbinderebene unter Pad) | 2442 | FPC 20 mm breit |
| NMC | CMU 09 | Zellverbinder-Abgriffe (Verbinderebene unter Pad) | 2574 | FPC 20 mm breit |
| NMC | CMU 10 | Zellverbinder-Abgriffe (Verbinderebene unter Pad) | 2496 | FPC 20 mm breit |
| NMC | CMU 11 | Zellverbinder-Abgriffe (Verbinderebene unter Pad) | 2472 | FPC 20 mm breit |
| NMC | CMU 12 | Zellverbinder-Abgriffe (Verbinderebene unter Pad) | 351 | FPC 20 mm breit |

**5. Bilder** (alle gesehen, Zielband/Grenze beschriftet, Lesehilfe `lesehilfe.md`): `e2_<V>_gesamt.png`, `e2_<V>_draufsicht.png` (Kabelweg), `e2_<V>_schnitt.png` (Box, Höhengrenze 130 mm gestrichelt und Packhöhe), `e2_<V>_detail.png` (CMU und FPC), `kabelplan_<V>.png`, `schaltbild_<V>.png` (v0.2, noch ohne Mäander-Hinweis). Renderrohbilder in `/home/cae/cae_projekte/batterie/e2/render/`. Baustein `praesentation/bausteine/E2.md`.

## Offene Fragen an Opus (v0.3)
1. LFP-Verschaltung nicht machbar (2 Reihen, 4 Durchläufe nötig): Entscheidung G3 (Überspringen jeder zweiten Zelle mit Verbindern in zwei Ebenen, Mitte vorn mit Längsleitung, anderes Konzept?). Bis dahin LFP ohne HV intern und ohne Trennstecker.
2. LFP-FPC: 20 mm breite FPC passt nicht an den Querträgern vorbei und nur 2 Spuren je Seitenspalt (9 Kollisionen, 6 von 14 Stücken ohne Platz). Schmalere FPC, andere Führung oder Querträger-Aussparung?
3. NMC Mäander: Hälften 112 / 105 Gruppen (413 / 387 V Nennspannung, Erwartung ≤ 400 V je Hälfte nicht eingehalten). G4-Verbinder müssen auf Spaltenzüge umgestellt werden.
4. ENT-138 (BMS-Einbauort vorn) widerspricht ENT-144. ENT-147 ersetzt vom Autor entschiedene ENT-102.
5. Platzhalter `A_e2_box_teilabstand_mm` = 10 mm (Teilabstand in der Box, Leitungsabstand über dem Trennstecker, Abstand Box zu Trennstecker/Steckern) bestätigen oder ersetzen. `A_traeger_dicke_NMC_mm` aus G4 unverändert.
6. Elektronikmasse 5.7 / 6.8 kg liegt weit unter dem Band 12–18 kg der Erwartung (Punkt 7; BMS 0,4 kg, Schütze, CMU 0,08 kg). HV-Leitungsmasse fehlt (Dichte).
7. Verguss im Modell als Vollblock bis halbe Zellhöhe in den Endzonen: CMU verdrängt ihn. Mit Aussparung gerechnet.
8. Schaltbild (v0.2) nennt noch den Trennstecker-Ort offen; bei Entscheidung zu Punkt 1 nachführen.

Fussnote Elektrik: HV-Verlust nur Leitungen im Pack (Zelle → Schaltbox/Trennstecker und 20 mm Schaltbox → HV-Stecker), nicht Verbinder, Schütze, Shunt, Sicherung.


## Version 0.4 (2026-11-18, Auftrag „Fortsetzung 3“, Grundlage ERWARTUNG Nachtrag 2)
Quellen: `cad/pack/entwurf/ergebnis_LFP_e2.json`, `ergebnis_NMC_e2.json` (Block `e2`), `sim/elektrik/e2_elektronik/ergebnis.json`, `eingaben.json`. Läufe 2026-11-18: `pack.py` PACK_E2=1 LFP 4 s, NMC 201 s (nice, `systemd-run --user --scope`, nur CPU), Blender Cycles CPU 24 Samples. Große Dateien (Netze, STEP, Rohbilder): `/home/cae/cae_projekte/batterie/e2/`.

**1. Akten** (Status vorgeschlagen; `pm.py pruefe`: 149 Entscheidungen, 0 Fehler; `register`, `parameter` gelaufen):
- **ENT-148** BT-200 verschaltung = `schleife_2reihen`, nur LFP (Plus und Minus hinten, Mitte und Trennstecker vorn). ENT-145 bleibt auf [NMC].
- **ENT-149** BT-360 breite_mm = 16, nur LFP. Dafür habe ich ENT-122 (FPC 20 mm, vorher für alle) auf `variante: [NMC]` gesetzt, sonst gäbe es zwei gültige Akten für LFP (gleiches Vorgehen wie ENT-115/ENT-146). Das war nicht ausdrücklich beauftragt, bitte bestätigen.
- Ohne Merkmal, daher als A_*/Eingabe: Cu-Dichte 8960 kg/m³ in `eingaben.json` (stoffe.rho_Cu_kg_m3, Herkunft „ERW-E2 N2“); FPC-Stapel 3 mm (4 × 0,3 mm + Halter, `A_e2_fpc_halter_mm`, Halter-Dicke = 3,0 − 4 × 0,3 = 1,8 mm); Teilabstand 10 mm (`A_e2_box_teilabstand_mm`, Opus bestätigt in Nachtrag 2). Merkmale, die in `struktur.json` fehlen: unverändert Liste v0.2.

**2. CAD**
- **LFP (ENT-148, ENT-149):**
  - Plus und Minus: je eine Leitung (Ø 14 mm, 50 mm² Cu, Biegeradius 70 mm) von den hinteren Zellen senkrecht hoch, Bogen, in y zur Schaltbox (je 572 mm). Der Anschluss vom Zellverbinder zur Leitung (Lasche, ca. 32 mm hoch) ist nicht gezeichnet und nicht gezählt.
  - Mitte vorn: Querverbinder Al 25 × 3 mm als zwei Hälften flach auf den vordersten Zellen (Gesamtlänge 1358 mm), zwei Leitungen (je 6 mm) zum Service-Trennstecker in einer Deckelöffnung 80 × 50 mm (Stecker steht auf der oberen Kühlplatte).
  - FPC 16 mm, 4 Lagen je Spur: alle 14 Stücke platziert (vorher 8 von 14).
- **NMC (ENT-145):** Gruppenverbinder nach der Mäander-Folge neu gezeichnet (217 Gruppen, Verbinder-Scheibe und Streifen 25 mm breit, 3 mm dick), 216 Gruppenbrücken zwischen den Gruppen (Wendestellen mit Spaltenwechsel sind Gruppenübergänge, 0 Gruppen mit Spaltenwechsel innerhalb). Aussparung Verguss um die CMU: 396,0 / 72,0 cm³ (f0/f3) gesetzt, Pad 129,9 cm³ (FPC), Kühlplatte 3,6 cm³ und Deckel 0,9 cm³ (HV-Durchführungen).

**3. Abgleich mit ERWARTUNG Nachtrag 2**
| Größe | Erwartung | LFP | NMC | Urteil |
|---|---|---|---|---|
| Kollisionen | 0 | **0** bei 1045 Paaren | **0** bei 7491 Paaren | ok beide (`anzahl_kollisionen`) |
| Trennstecker LFP von oben zugänglich | ja | ja, Deckelöffnung 80 × 50, Oberkante 179 mm | – | ok; Stecker ragt 58 mm über den Deckel (`e2.stecker_lfp`), s. Offen 1 |
| HV intern LFP | 0,5–1,5 m | 1.176 m (Plus 572 + Minus 572 + 2 × 6 + 20 mm Box → HV-Stecker) | 1.194 m (unverändert v0.3) | ok |
| HV-Verlust bei Ladestrom | 6–20 W (LFP, 194 A) | 15.22 W (12.947 W/m, `ergebnis.json`) | 11.34 W (9.495 W/m, 139 A) | ok; ohne Zellverbinder und Querverbinder |
| Elektronikmasse mit HV-Leitungen | 7–12 kg | 6.42 kg | 7.13 kg | LFP **0,6 kg unter dem Band**, NMC ok |
| davon HV-Leiter (Cu 8,96 g/cm³, nur Leiter) | – | 0.527 kg | 0.375 kg | `e2.hv_cu_masse_kg` |
| Hälften NMC 413/387 V | Annahme | – | Gruppen 112/105 | unverändert; keine Norm (Nachtrag 2) |
| Messleitung FPC | – | 11.79 m, 14/14 platziert | 30.73 m, 13/13 | NMC im Band 25–40 m, LFP darunter (kurze Zellreihen) |
| Packhöhe mit Turm | – | 210 mm | 204 mm | unverändert, 130-mm-Grenze nur außerhalb Turm |
| Masse Pack mit E2-Teilen | – | 619.8 kg | 482.8 kg | `masse_bekannt_kg` (NMC höher als v0.3 479.6 kg: Verbinder nach Mäander) |
LFP-Elektronikmasse im Detail (`e2.masse_elektronik_*`): ohne HV-Leiter 5.898 kg; Querverbinder Mitte Al 0.275 kg ist Zellverbinder-Gruppe und nicht in der Elektronikmasse.

**4. Schaltbild v0.3, Bilder, Kabelplan:** `schaltbild_LFP.png`, `schaltbild_NMC.png` (Hälften, Trennstecker vorn bzw. hinten, HV-Länge und Verlust aus `ergebnis_<V>_e2.json`, Schaltbox hinten ENT-144); `e2_<V>_gesamt|draufsicht|schnitt|detail.png`, `kabelplan_<V>.png`, `kabelplan_tabelle.md` neu. Alle Bilder angesehen (Zielband/Grenze beschriftet: Höhengrenze 130 mm und Packhöhe im Schnitt, 200-mm-Maßstab). Lesehilfe `lesehilfe.md` v0.3, Baustein `praesentation/bausteine/E2.md` nachgeführt.

**Offen (v0.4)**
1. LFP-Trennstecker (60 mm hoch) steht vorn: Oberkante 179 mm gegen M0-Grenze 130 mm (Annahme); die Box hinten ist durch ENT-144 erlaubt, der Stecker vorn nicht. Entscheidung Opus (Stecker flacher, kleinerer Packbereich vorn?).
2. LFP-Querverbinder 3 mm dick ist dicker als das Pad (1 mm): Nut 2 mm in der oberen Kühlplatte (`aussparungen_mm3.Kuehlplatte_oben` 72.7 cm³). Bestätigen oder anders lösen.
3. Anschlusslaschen (Zellverbinder zu den HV-Leitungen Plus/Minus, NMC und LFP) nicht gezeichnet.
4. Verlust des Querverbinders (Al, 1358 mm, Werkstoffwert ρ_Al fehlt) und der Zellverbinder nicht gerechnet.
5. LFP-Elektronikmasse 6,42 kg: 0,6 kg unter dem Band 7–12 kg; Halter-Masse (0,05 kg/m enthalten?) und Isolierung der Leiter ohne Wert.
6. ENT-138 (BMS vorn) widerspricht ENT-144/ENT-109, ENT-147 (aus v0.3) und ENT-122-Änderung (diese Version) warten auf Bestätigung.
7. NMC-Brücken: Streifenform und 25 mm Breite aus G4 übernommen, Wendebrücken ohne Gruppen-Spaltenwechsel (jede Spalte hat 32 Zellen, Gruppen à 4 teilen sich glatt).

---
*KI-generiert (Claude Sonnet, 2026-11-18), Entwurf, nicht freigegeben.*
