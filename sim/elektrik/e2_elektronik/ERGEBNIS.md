| Dok.-Nr. | ERG-E2 | Version | 1.1 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Ergebnis E2 (Rechnung, Akten, CAD Schaltbox hinten, CMU, FPC, HV intern, Bilder) | Ersteller | Claude Sonnet (KI) | Prüfer | Opus (offen; v1.0 Stichprobe 2026-11-18, B-BAT-027) |

> KI-generiert (Claude Sonnet, 2026-11-18). Entwurf. Die Abschnitte „Version 0.2“ (Fall b vorn, ENT-109) und „Version 0.3“ sind überholt; maßgebend ist „Version 1.0 (Fortsetzung 4)“ am Ende; sie ersetzt in v0.4 die Aussagen zu Trennstecker LFP, Laschen, Nut, Al-Verlust. Zahlen aus `ergebnis.json` (dieser Ordner), erzeugt von `elektronik.py` aus `eingaben.json`.

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

## Version 1.0 (2026-11-18, Auftrag „Fortsetzung 4“ mit „Änderung zu Punkt 4“)
Quellen: `cad/pack/entwurf/ergebnis_LFP_e2.json`, `ergebnis_NMC_e2.json` (Block `e2`), `verlust_al.json` (dieser Ordner, erzeugt von `verlust_al.py` aus `e1_querschnitte/eingaben.json`, `ergebnis.json` und den CAD-Ergebnissen). Läufe 2026-11-18 (nice, `systemd-run --user --scope`, nur CPU): `pack.py` PACK_E2=1 LFP 4 s, NMC 172 s, Blender Cycles 24 Samples je Variante ca. 2 min. FCStd: `cad/pack/entwurf/pack_LFP_e2.FCStd`, `cad/pack/entwurf/pack_NMC_e2.FCStd`; STEP und Netze in `/home/cae/cae_projekte/batterie/e2/` (Links in `cad/pack/entwurf/`).

**1. Akten:** ENT-150 (BT-720 `einbauort` = `trennbruecke_servicedeckel_vorn`, nur LFP, vorgeschlagen, ersetzt ENT-131 für LFP). ENT-131 (Reihenmitte, alle Varianten) auf `variante: [NMC]` gesetzt, gleiches Vorgehen wie ENT-122/ENT-149; bitte bestätigen. `pm.py pruefe`: 150 Entscheidungen, 0 Fehler; `register` gelaufen. **Merkmal „bauform“ fehlt für BT-720 in `struktur.json`** (Auftrag nennt „bauform“); nicht angelegt, deshalb unter `einbauort`. Annahmen „ERW-E2 N3“ als `A_e2_*` in `cad/pack/entwurf_parameter.py`: Brücke Cu 25 × 3, Überlappung 25 mm je Seite, **Lücke im Querverbinder 30 mm (Platzhalter, nicht in N3 gesetzt)**, Öffnung 120 (y) × 80 (x), Lasche 25 × 3, Bohrung Ø 8 (Nennmaß M8, Durchgangsloch nicht gesetzt).

**2. Änderung Punkt 4, LFP-Trennbrücke:** Querverbinder vorn mit 30-mm-Lücke, Cu-Brücke 25 × 3 × 80 mm (25 mm auf jeder Seite überlappend), 2 Schrauben M8 (Ø 8, Masse offen = 0), Öffnung 120 × 80 mm durch Pad, obere Kühlplatte und Deckel, darüber ein flacher Servicedeckel (Al, Dicke wie Deckel 2 mm, bündig). HV-Interlock-Kontakt nicht modelliert. Die zwei Mittelleitungen und der Stecker entfallen.
| Größe | LFP | Fundstelle |
|---|---|---|
| Höhenzuwachs über dem Deckel vorn | 0 mm | `e2.stecker_lfp.ueber_deckel_mm` |
| Packhöhe vorn (Deckeloberkante, Servicedeckel bündig) | 121 mm (Soll ≤ 130 mm: **erfüllt**) | `hoehe_stapel_mm` 121; höchstes Teil vorn `e2.hoehe_vorn_mm` 121 |
| Packhöhe mit Turm hinten | 210 mm (ENT-144) | `hoehe_mm` |
| HV intern | 1.164 m (Plus 572 + Minus 572 + 20 mm), Verlust 15.07 W | `e2.hv_laenge_gesamt_m`, `e2.hv_verlust_W` (Erwartung 6–20 W: ok) |
| Elektronikmasse mit HV-Leitern | 6.34 kg (Band 7–12 kg: 0,7 kg darunter); davon HV-Cu 0.521 kg | `e2.masse_elektronik_gesamt_kg`, `e2.masse_hv_leiter_cu_kg` |
| Kollisionen | **0** bei 1050 Paaren | `anzahl_kollisionen` |
Nicht belegt: ob 120 × 80 mm für das Werkzeug reicht und ob die Öffnung in der Kühlplatte (Fläche siehe 4.) thermisch zulässig ist; Dichtung des Servicedeckels nicht modelliert.

**3. Anschlusslaschen (Punkt 1):** Al 25 × 3 (Querschnitt wie Verbinder, 75 mm²), Bohrung Ø 8.
- **NMC:** Platte 25 × 25 × 3 mm auf dem Gruppenverbinder im Zellmittelpunkt (Überlappung 25 mm erfüllt), 4 Stück (Plus, Minus, 2 × Mitte); Leitung beginnt auf der Lasche (3 mm kürzer). Aussparungen: Pad und obere Kühlplatte (Pad_oben 132.0 cm³ gesamt, Kühlplatte 7.7 cm³). FPC-Spur musste verschoben werden (Abstand zur Lasche 22,5 mm statt 17 mm), Kollision FPC_06 mit Lasche vorher 20,6 mm³, jetzt 0; FPC 30.77 m (vorher 30.73 m).
- **LFP:** Der Seitenspalt lässt nur 1 mm neben dem Zellverbinder frei (Rahmen 30 mm, Verbinder 3 mm dick, Zellen ab 34 mm). **Die geforderte Überlappung von 25 mm auf dem Zellverbinder ist dort nicht darstellbar.** Gebaut: Steg 25 (y) × 3 (x) am Ende des hintersten Zellverbinders (Stumpfstoß, wie angeschweißt), Flansch 25 × 15 × 3 mm über der FPC-Ebene mit Bohrung Ø 8 unter dem Leitungsfuß, Pfad je Lasche 65.5 mm. Beginn y hinter dem FPC-Stapel (3 mm). Bohrungsrand zum Flanschrand nur ≈ 0,8 mm (Leitung liegt bei y = 38 mm, Flansch beginnt bei 33,2 mm). → OPUS: Lage der Leitung oder Stumpfstoß-Konzept.

**4. Nut LFP für K2 (Punkt 3):** Nut 2 mm tief in der oberen Kühlplatte (Querverbinder 3 mm, Pad 1 mm), Breite 25 mm, `e2.stecker_lfp.nut`: Nutfläche ohne Öffnung 31 200 mm² = **1.14 %** der oberen Kühlfläche (2 726 300 mm² = (2050 − 60) × (1430 − 60), Innenfläche). Dazu die Serviceöffnung 9 600 mm² = 0.35 %, Nut plus Öffnung 1.50 %. Volumen Aussparung Kühlplatte oben 142.5 cm³ (`aussparungen_mm3`).

**5. Verlust der Al-Verbinder (Punkt 2, Dauerstrom, ρ_Al 2,82e-8 Ωm aus `e1_querschnitte/eingaben.json`; `verlust_al.json`):**
| | Erwartung | Rechnung | Abweichung | Urteil |
|---|---|---|---|---|
| LFP Zellverbinder 248 × L 15 mm, 75 mm², 194 A | – | 52.6 W | – | – |
| LFP Querverbinder Mitte 1338 mm, 75 mm² | – | 18.9 W | – | – |
| LFP Laschen 2 × 65,5 mm | – | 1.94 W | – | – |
| **LFP Summe Dauer** (Spitze 240 A: 112.5 W) | ≤ 50 W | **73.5 W** | **+47 %** | **verfehlt, > 30 % → OPUS** |
| NMC mit E1-Querschnitt 45 mm² (Gruppen 362.7 W + Zellabgriff 98.3 W) | ≈ 385 W | **461.1 W** (Spitze 1459.6 W) | +19.8 % gegen 385; +30.5 % gegen E1-Al-Summe 353.3 W | Grenzfall (> 30 % gegen E1-Al), → OPUS |
| NMC mit CAD-Querschnitt 25 × 3 = 75 mm² (Gruppen 217.6 W + Zellabgriff 98.3 W) | ≈ 385 W | 316.0 W (Spitze 1000.3 W) | −17.9 % | im Band |
- LFP: der Querverbinder (1338 mm) ist der Posten, den E1 nicht kannte (E1: 249 Verbinder à 15 mm, 52.8 W).
- NMC: Gruppenverbinder im Mäander länger als bei E1 (Sammelstrecke im Mittel 209.7 mm statt 192 mm, Brücken im Mittel 89.6 mm statt 48 mm, größte 190.5 mm, 217 Gruppen, 216 Brücken); Methode wie E1 (Sammelstrecke I²R/3, Brücke voller Strom, Zugabe 48 mm wie in E1). Laschen NMC 0.32 W.
- **Widerspruch, den ich nicht entscheide:** E1 hat 15 × 3 = 45 mm² gewählt, das CAD (G4) zeichnet 25 × 3 = 75 mm². Beide Ergebnisse stehen oben. Die „≈ 385 W“ der Erwartung ist die E1-Summe aus Gruppen, Zellabgriff **und HV-Cu** (385.4 W, `e1_querschnitte/ergebnis.json` NMC_summe.verlust_W), nicht nur Al (353.3 W). Zellabgriff (98.3 W) aus E1 unverändert (Geometrie gleich).
- Kontaktwiderstände der Schweißungen und Schrauben nicht modelliert.

**6. Bilder** (alle angesehen, Höhengrenze 130 mm und Packhöhe im Schnitt beschriftet, Lesehilfe `lesehilfe.md`): `e2_<V>_gesamt|draufsicht|schnitt|detail.png`, neu `e2_LFP_bruecke.png` (Trennbrücke vorn, Servicedeckel ausgeblendet), `kabelplan_<V>.png`, `schaltbild_<V>.png` (v1.0). Das Bild `e2_LFP_bruecke.png` zeigt die Brücke ohne Zielband (Maßbild); das Zielband „≤ 130 mm vorn“ steht im Schnitt `e2_LFP_schnitt.png`.

**Offen (v1.0)**
1. LFP-Al-Verlust 73.5 W gegen ≤ 50 W (+47 %); NMC je nach Querschnittsbasis 461 W oder 316 W. Entscheidung Opus (Querschnitt NMC E1 oder G4; LFP Querverbinder breiter/dicker?).
2. Merkmal „bauform“ in BT-720 fehlt; ENT-150 unter `einbauort`; ENT-131 auf [NMC] geändert, zu bestätigen.
3. Lücke 30 mm, Öffnung 120 × 80 mm, Schrauben-Masse, Interlock, Dichtung: Platzhalter.
4. LFP-Lasche: Überlappung 25 mm im Seitenspalt nicht darstellbar (Stumpfstoß); Bohrungsrand 0,8 mm.
5. Elektronikmasse LFP 6.34 kg, 0,7 kg unter dem Band; NMC 7.15 kg (ok).
6. Aus v0.4 weiter offen: ENT-138 gegen ENT-144; ENT-147; Halter-Masse; NMC-Hälften 413/387 V.

## Version 1.1 (2026-11-18, Auftrag „Fortsetzung 5“, Konstruktionsstand E2D)
> **KI-generiert** (Claude Sonnet, 2026-11-18), Entwurf, nicht freigegeben. Alle Zahlen aus `cad/pack/entwurf/ergebnis_<V>_e2d.json` und `sim/elektrik/e2_elektronik/verlust_al_e2d.json`; Maße nur aus ERWARTUNG.md Nachtrag 3 (Block `A_e2d_*` in `cad/pack/entwurf/parameter_<V>_e2d.json`, erzeugt von `cad/pack/entwurf_parameter_e2d.py`). Abgeleitete Maße sind dort mit „abgeleitet (Sonnet)“ gekennzeichnet und unten unter „Offen“ gelistet. Neue Dateien: `cad/pack/pack_e2d.py`, `e2d_geo.py`, `render_e2d.py`, `label_e2d.py`; die Basis (`pack.py`, `entwurf_parameter.py`, `pack_<V>_e2.FCStd`, v1.0 oben) ist unverändert. Rechnung: LFP 26 s, NMC 239 s (FreeCAD), Bilder je Variante ca. 4 bis 6 min (Blender Cycles CPU, 24 Samples, daher sichtbares Rauschen); 20-min-Grenze nicht erreicht.

**1. NMC-Verbinderquerschnitt aus der Akte (Schritt 1).** `pm/bauteile/parameter.json` BT-420: breite_mm 25 (ENT-096), dicke_mm 3 (ENT-097), also 75 mm². Verlust `verlust_al_e2d.json` (ρ_Al 2,82e-8 Ωm, Dauerstrom 129,5 A):
| | v1.0 | v1.1 | Erwartung (N3) | Urteil |
|---|---|---|---|---|
| NMC Al-Summe mit Akte 25 × 3 = 75 mm² (Gruppen + Zellabgriff) | 316,0 W | **316,0 W** (Spitze 1000,3 W) | ≈ 460 W gilt für 15 × 3 | weicht ab, weil Akte 25 × 3 sagt |
| NMC mit E1-Querschnitt 15 × 3 = 45 mm² (zum Vergleich) | 461,1 W | 461,1 W (Spitze 1459,6 W) | ≈ 460 W | trifft |
| LFP Summe Dauer (Akte 25 × 3, 194 A) | 73,5 W | **75,6 W** | ≤ 50 W | verfehlt weiter (+51 %); Laschenpfad jetzt 141,8 mm statt 65,5 mm |
Die Länge der Gruppenverbinder ändert sich durch E2D nicht (gleiche Verschaltung). Ob 15 × 3 thermisch reicht, entscheidet Opus (nicht berechnet).

**2. Gebaut (Schritte 2 bis 5).** Schaltbox: Wanne 2 mm mit Flansch 12 mm, Dichtung 3 × 3, Deckel 2 mm, M5 alle 60 mm, Druckausgleich Ø 20; Geräte mit Bolzen M8 (Schütze 2 × Ø 8 × 15, Abstand 40), Fußlaschen, Spulenstecker, BMS-Abstandsbolzen M4, Stecker 26 pol/2 × Daisy, Shunt mit Platine; 6 Stromschienen (Cu 25 × 3 LFP, 20 × 3 NMC, R innen = Dicke, Schrumpfschlauch 0,5) mit Bohrungen 8,5; HV-Stecker 250 A (Flansch 90 × 70 × 8, 4 × M5, Hebel, O-Ring), 40 A, NV; Kabel 4 Schichten (Leiter, Isolierung, Schirm, Mantel), Kabelschuhe (Hülse 40, Palme 20 × 4), Clips alle 200 mm; FPC-Ni-Tab 8 × 4 × 0,2, NTC 3 × 2 × 1 (4 je CMU), FPC-Stecker 25 × 8 × 6, Daisy-Chain (Stecker, Leitung Ø 4). LFP zusätzlich: Anschlusslasche als abgekantetes Band, Trennbrücke 25 × 3 × 80 mit 2 × M8 und Scheibe, HVIL, Servicedeckel 120 × 80 × 2 auf Dichtung mit 6 × M5 Senkkopf, Schweißlinien. NMC zusätzlich: Berührschutz 1 mm über dem Omega-Scheitel.
| Größe | LFP | NMC | Fundstelle |
|---|---|---|---|
| Teile (v1.0 → v1.1) | 442 → 956 (2,2 ×) | 2236 → 2701 (1,2 ×) | `ergebnis_<V>_e2[d].json` teile (Erwartung N3: 3 bis 5 ×, **nicht erreicht**, weil NMC schon viele Teile hatte) |
| Kollisionen nach Schritt 5 | **3** (Schmelz_Lasche_A/Schiene_5 0,0017 mm³ = Berührung; 2 × Trennbrücke-M8-Kopf/Servicedeckel je 212,4 mm³) | **0** | `anzahl_kollisionen`, `kollisionen` |
| Elektronikmasse gesamt (v1.0 → v1.1, Zuwachs) | 6,342 → 7,351 kg (+1,01) | 7,150 → 7,941 kg (+0,79) | `e2.masse_elektronik_gesamt_kg`; Erwartung +1…3 kg: LFP am unteren Rand, **NMC darunter**. Masse offener Teile (Kabelschuh, Schrauben, Dichtung) mit 0 gesetzt |
| Packmasse bekannt | 620,6 kg | 483,2 kg | `masse_bekannt_kg` |
| Schaltbox Wanne L × B × H bis Deckel | 320 × 300 × 123 mm | 320 × 300 × 117 mm | `e2.schaltbox_*` |
| Innenhöhe Schaltbox (Cap N1 90 mm) | 116 mm, **über** | 110 mm, **über** | `e2.schaltbox_innenhoehe_mm`, `schaltbox_hoehe_max_N1_mm` |
| Packhöhe vorn (Grenze 130 mm) | **134 mm, über** (Ursache: M8-Kopf der Trennbrücke) | 128 mm, ok | `e2.hoehe_vorn_mm` |
| HV intern Länge, Verlust | 1,08 m, 13,98 W | 1,088 m, 10,34 W | `e2.hv_laenge_gesamt_m`, `hv_verlust_W` |
| Stromschienen (Länge Mittellinie) | 155 / 385 / 75 / 175 / 74 / 75 mm | 149 / 380 / 70 / 144 / 69 / 60 mm | `e2.schienen` |
| Details (Tab / NTC / FPC-Stecker / Daisy-Stecker) | 251 / 56 / 14 / 28 | 218 / 50 / 13 / 26 | `e2.details` |

**3. Kollisionsprüfung je Schritt.** Verlauf LFP 95 → 9 → 7 → 3 Kollisionen (Korrekturen: Schraubenstapel, Fußlaschen, Schienen mit Biegung, Lasche eine Dicke höher, NTC aus den Querträgern verschoben, Kabelhöhe über dem höchsten Gerät). NMC: 354 → 0. Eingebaute Aussparungen (Volumen gemeldet, `e2.aussparungen_mm3`): Pad/Kühlplatte/Deckel um Kabel, Tabs, NTC; Verguss/Zellträger um Daisy-Stecker und -Leitung (NMC: Daisy-Leitung schneidet 11 Mal durch den Verguss, größter Posten 18 275,7 mm³ im ersten Lauf, **Lage offen**); FPC an 3 Gruppenverbindern ausgespart. Zwei NTC (NMC `NTC_00_000`, `NTC_12_217`) liegen unter den Anschlusslaschen und entfallen im Modell (`e2.teile_entfallen_durch_aussparung`).

**4. Bilder** (alle angesehen; Zielband als Textzeile im Seitenfeld mit Ist-Wert, rot = über Grenze; Lesehilfe `lesehilfe.md`): je Variante `e2d_<V>_boxoffen.png`, `e2d_<V>_stecker.png`, `e2d_<V>_detail.png`, `e2d_<V>_kabel.png`, `e2d_<V>_gesamt.png`, LFP zusätzlich `e2d_LFP_bruecke_offen.png` und `e2d_LFP_bruecke_zu.png` (NMC hat keine Trennbrücke: 5 Bilder). Rohbilder und Netze in `/home/cae/cae_projekte/batterie/e2/`. Rauschen durch 24 Samples; Zellen ausgeblendet; Schaltbox in der Draufsicht bewusst klein gegen das Pack.
CAD: `/home/cae/cae_projekte/batterie/e2/pack_LFP_e2d.FCStd` und `pack_NMC_e2d.FCStd` (je auch `.step`).

**Offen (v1.1), nur Opus/Mensch entscheidet**
1. **NMC 15 × 3 (E1) gegen 25 × 3 (Akte ENT-096/097):** Verlust 461 W gegen 316 W; Erwartung N3 geht von 15 × 3 aus. LFP-Al-Verlust 75,6 W gegen ≤ 50 W.
2. **M8-Schraubenstapel 9,6 mm (`e2.stecker_lfp.schraubenstapel_mm`, Oberkante 125,6 mm) gegen 8 mm unter dem Servicedeckel:** 2 Kollisionen, Packhöhe vorn 134 mm > 130 mm. Nicht geändert (kein eigenes Maß).
3. **Innenhöhe Schaltbox 116/110 mm gegen Cap N1 90 mm:** Schmelzhalter 95 mm hoch, Schienen und Kabelhöhe darüber. Nicht geändert.
4. **LFP-Seitenspalt 1 mm** gegen Omega h = 4, Berührschutz, Lasche mit 25 mm Überlappung: Lasche als Stumpfstoß/abgekantetes Band gebaut.
5. **BT-710 Stromschienen-Querschnitt als Merkmal fehlt** (Schienenmaß nur aus N3); Stecker 4 pol am Shunt ohne Maße (nur Platine); Daisy-Querleitung (LFP 1980 mm, NMC 1880 mm) nicht gezeichnet.
6. **Abgeleitete Maße (Sonnet), zu bestätigen:** Fußlasche 20 × 9 × 2; Laschen Pyro/Schmelz Auskragung 25; Halterwand 5; Schraubenköpfe M4/M5/M8 und Scheibe (Normmaße aus dem Gedächtnis, nicht belegt); BMS-Abstandsbolzen SW 7, Einzug 5; Kabelschichtdicken (Radialwand in 3 gleiche Teile); Servicedeckel-Rand 12; O-Ring Ø 60 × 3; Palmenlänge ≥ Schienenbreite; Freigang 1 mm Kabelhöhe über Gerät; Schienenabstand zur Leitung 40 mm (Lagefaktor); Geräteanordnung in der Box (diagonale 385-mm-Schiene nicht optimiert).
7. **Fensterregel:** Omega, Schweißlinien (LFP) und Berührschutz (NMC) nur im hintersten Feld (`e2.fenster_feld` 3); das war von Beginn an so gebaut, die 20-min-Grenze wurde nicht erreicht. Opus entscheidet, ob alle Felder gewünscht sind.
8. Teilezahl-Erwartung 3 bis 5 × verfehlt (2,2 × / 1,2 ×); NMC-Elektronikmasse +0,79 kg unter +1…3 kg.
9. Die 4-Minuten-Rechnung NMC (Lauf 2) und beide Bildläufe liefen mit `nice` und teils im Vordergrund der Sitzung, nicht alle unter `systemd-run --scope` (Auflage verfehlt bei den ersten FreeCAD-Läufen).

---
*KI-generiert (Claude Sonnet, 2026-11-18), Entwurf, nicht freigegeben.*
