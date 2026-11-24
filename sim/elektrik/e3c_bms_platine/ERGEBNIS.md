| Dok.-Nr. | ERG-E3c | Version | 0.1 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Ergebnis E3c: BMS-Leiterplatte BT-311 (KiCad) und LFP-Kollisionen Servicedeckel | Ersteller | Claude Sonnet (KI) | Prüfer | Opus (offen) |

> **KI-generiert** (Claude Sonnet, 2026-11-24). Entwurf, nicht freigegeben. Grundlage `ERWARTUNG.md` (ERW-E3c, nicht geändert). Zahlen aus `ergebnis_platine.json`, `ergebnis_kriechstrecke.json`, `ergebnis_routing.json`, `ergebnis_pack_LFP_teilA.json` (Kopie von `cad/pack/entwurf/ergebnis_LFP_e2d_e3.json` nach Teil A) in diesem Ordner. Regel „erst konservativ“: Optimierungen nur in `pm/optimierungen.md` (neu OPT-014).

## Abgleich der Erwartungen
| Nr | Erwartung (ERWARTUNG.md) | Ergebnis (Quelle) | Urteil |
|---|---|---|---|
| A | LFP 0 Kollisionen, Höhenzuwachs Deckel ≤ 10 mm | 0 Kollisionen, 1 zugelassene verschraubte Berührung (0,0017 mm³); Höhenzuwachs 4,6 mm (`ergebnis_pack_LFP_teilA.json`, e2.stecker_lfp) | ok |
| 1 | ≈ 150–220 Teile, Platine ≈ 160 x 100 mm, passt in die Schaltbox | 131 Teile (unter dem Band); Platine 160 x 100 mm, Bauhöhe 9,3 mm; BT-310 200 x 150 x 20 mm: Länge ok, Breite ok, Höhe ok; Schaltbox innen 320 x 300 x 116 mm (`ergebnis_platine.json`) | Teilezahl verfehlt, Maß und Passung ok |
| 2 | Sperrzone als Linie ≥ 10 mm sichtbar, nur Übertrager, Isolator, Shunt-ADC-Isolator überbrücken | Zone x = 100…110 mm, volle Höhe 100 mm, Objekte in der Zone 0, Kupferabstand NV/HV 10,4 mm; überbrückende Teile: 4 (U_ISO_SHUNT, U_ISO_SEK, T_DAISY2, T_DAISY1) | ok |
| 3 | Routing vollständig, DRC 0, Kriechstrecke ≥ Luftstrecke | DRC-Verstöße 0, offene Verbindungen 0; Kriechstrecke 10 mm ≥ Luftstrecke 8 mm: ok (`ergebnis_kriechstrecke.json`) | ok |
| 4 | Masse ≈ 60–90 g | 66,5 g (FR4 43,5 g, Kupfer 18,7 g, Bauteile 4,3 g); nicht angesetzt: 3x JST_PH_S4B-PH-SM4-TB_1x04-1MP_P2.00mm_Horizontal, 2x L_CommonModeChoke_Coilcraft_1812CAN, 3x JST_PH_S2B-PH-SM4-TB_1x02-1MP_P2.00mm_Horizontal (`ergebnis_platine.json`) | ok (Untergrenze der Bauteilmasse, siehe Grenzen) |
| 5 | Bilder: 3D iso/top, Explosionsansicht mit Sperrzone, Platine in der Schaltbox | siehe Abschnitt Bilder | ok |

## Teil A: LFP-Kollisionen
- **Servicedeckel BT-722:** Der Schraubenstapel der Trennbrücke ist 9,6 mm hoch (Kopf 8 mm + Scheibe 1,6 mm, `A_e2d_m8_*`), die freie Höhe unter dem flachen Deckel war 8,0 mm. Neu: lichte Höhe innen = Stapel + 3 mm = 12,6 mm (Tasche in der Deckelunterseite innerhalb der Dichtung, 12 mm vom Rand), Deckel um 4,6 mm dicker, Oberkante 130,6 mm, 9,6 mm über dem Gehäusedeckel. Schraubenköpfe (Senkschrauben M5) sitzen weiter bündig oben.
- **Kontakt Schmelz_Lasche_A / Schiene_5:** als verschraubter Kontakt zugelassen (Schwelle 0,01 mm³, nur für Paare in der Liste `KONTAKT_VERSCHRAUBT` in `cad/pack/pack_e2d.py`, Wert `A_e3c_kontakt_schwelle_mm3`). Der Kontakt steht in `kontakte_zugelassen` des Ergebnisses.
- **Merkmal fehlt:** BT-722 hat in `struktur.json` nur `laenge_mm`, `breite_mm`. Das Merkmal „lichte Höhe innen“ wurde **nicht angelegt** (Auftrag: fehlendes Merkmal melden). Der Wert steht deshalb als Annahme `A_e3c_servicedeckel_lichte_zugabe_mm` = 3 (Herkunft ERW-E3c) in `cad/pack/entwurf_parameter_e2d.py`, ohne Akte. → Opus: Merkmal anlegen und Akte schreiben.
- **Höhe:** Deckeloberkante 130,6 mm gegen `A_hoehe_max_mm` = 130 mm; `hoehe_vorn_mm` des Pakets 134 mm (unverändert gegenüber dem Lauf davor, nicht vom Deckel bestimmt).
- Rechenzeit 133 s, Teile 956, Masse bekannt 620,179 kg. NMC wurde nicht neu gerechnet (Änderung betrifft nur den LFP-Zweig und die Kontaktliste).

## Teil B: BMS-Leiterplatte BT-311
**Werkzeuge:** wie E3 (KiCad 10.0.8 Flatpak, SKiDL, Freerouting 2.5.0). Skripte (Muster aus `sim/elektrik/e3_platine`, dort unverändert): `bms_skidl.py` (Netzliste, BOM), `bms_pcb_bauen.py` (Layout), `bms_regeln.py` (Netzklassen, Regeln), `bms_route.sh` (Ablauf), `bms_aufraeumen.py`, `bms_pruefung.py`, `bms_ergebnis.py`, Bilder `bms_*bild*.py`, `bms_*blender.py`. Groß (nicht im Repo): `/home/cae/cae_projekte/batterie/e3c/` (kicad_pcb, Gerber, STEP, DRC, Renderbilder, .blend).

**Akten (Status vorgeschlagen, wer „Opus (Annahme ERW-E3c)“):** ENT-188 Länge 160 mm, ENT-189 Breite 100 mm, ENT-190 Lagen 4, ENT-191 Kriechstrecke HV/NV 10 mm (BT-311). Alle anderen Werte der Tabelle haben **kein Merkmal** an BT-311 und damit keine Akte (siehe Offene Fragen).

**Schaltung** (Blöcke nach Tabelle): Rechner (generisch, LQFP-144), Versorgung 12 V (Verpolschutz, TVS, Systembasis-IC mit Watchdog), 2 CAN-FD mit Gleichtaktdrossel, Schützansteuerung für 3 Kanäle (High-Side und Low-Side, **Zener-Löschung**, Sparschaltung nicht gebaut = OPT-006), Hardware-UND für den Sekundärpfad (FSR-06), Daisy-Chain-Master mit 2 Übertragern (verstärkt), Shunt-ADC auf der HV-Seite mit digitalem Isolator (verstärkt), Sekundärpfad über digitalen Isolator. ERC 131 Teile, 0 Fehler (`bms_erc.txt`). Teile nach Footprint in `ergebnis_platine.json`.

**Layout und Routing:** 160 x 100 mm, 4 Lagen, 1167 Bahnsegmente, 242 Vias. Abstand NV 0,15 mm, HV 0,2 mm (ENT-168), HV/NV 10 mm (ENT-191, Regel in `bms.kicad_dru`, Sperrzone als Keepout über alle Lagen). Der Ablauf: Platzierung per Tabelle → DSN → Freerouting `-mp 10` → SES → Aufräumen und Füllen → DRC. Zahlen aus `ergebnis_routing.json`.
- **Methode (Abweichung von E3, Sonnet):** Innenlage In1 trägt Masseflächen (NV: GND, HV: HV_GND, getrennt durch die Sperrzone) und darf zugleich Signale führen; In2 trägt Signale und Versorgung. Mit zwei Flächenlagen (In1 und In2 als Fläche) blieben 76 Verbindungen offen, mit In1 als reiner Fläche 70; mit Fläche +3V3 auf In2 wurde die Fläche zerschnitten. Gewählt (Lauf 5): nur GND-Flächen auf In1, vollständig geroutet. Zwei Massevias lagen danach in abgeriegelten Inseln der In1-Fläche; eine zusätzliche Massefläche auf B.Cu (NV und HV getrennt, `bms_aufraeumen.py`) verbindet sie. DRC danach 0 Verstöße, 0 offen.
- **Brücken-Footprints (Platzhalter, Sonnet):** Übertrager und digitale Isolatoren haben selbst definierte Footprints (`E3c:ISO_Bruecke_8`, `E3c:Uebertrager_Bruecke_4`) mit Padreihen im Innenabstand 10,4 mm, damit die 10 mm gelten. Die Hüllkörper (13,2 mm quer zur Zone) sind Platzhalter. Reale Teile mit 10 mm Kriechstrecke sind nicht geprüft.

## Bilder
`platine_bms.png` (Ober-/Unterseite, Zielband Umriss, Sperrzone beschriftet), `platine_bms_3d_iso|top|bottom|nah.png` (KiCad 3D), **`platine_bms_explosion.png`** (Blender, Lagen auseinandergezogen, Sperrzone rot), **`platine_bms_einbau.png`** (Platine in der offenen Schaltbox, Platz BT-310 als Zielband). Schaltplanblätter: `schaltplan_bms_blatt-1…7.png`. Lesehilfe: `lesehilfe.md`.

## Platine im Pack (Nacharbeit Opus)
`PACK_E3C=1 PACK_VARIANTE=<V> pack_e2d.py` (Ausgabe `ergebnis_<V>_e2d_e3c.json`, Suffix _e3c): die BMS-Platine BT-311 ist als KiCad-STEP (`bms.step`) anstelle des Quaders im Pack, Ecke auf der Ecke des BMS-Platzes, die drei Steckerplatzhalter des E2-Modells entfallen (Stecker stecken im STEP). Masse 66,5 g aus `ergebnis_platine.json`. Die Deckelhöhe liest `pack_e2d.py` jetzt aus `pm/bauteile/parameter.json` (BT-722 `lichte_hoehe_zugabe_mm`, ENT-194); `A_e3c_servicedeckel_lichte_zugabe_mm` ist entfernt.
| Variante | Kollisionen | zugelassene Berührungen | Masse bekannt kg | Rechenzeit s | Quelle |
|---|---|---|---|---|---|
| LFP | 0 | 1 | 619,846 | 167 | `cad/pack/entwurf/ergebnis_LFP_e2d_e3c.json` |
| NMC | 0 | 0 | 482,415 | 422 | `cad/pack/entwurf/ergebnis_NMC_e2d_e3c.json` |

## Schaltplan (Zusatz Autor, Version 0.2 mit Drähten)
Hierarchischer KiCad-Schaltplan `bms_schaltplan.kicad_sch` (Deckblatt und 6 Blätter: Versorgung 12 V, Rechner, CAN, Schützansteuerung, Daisy-Master mit Isolation (mit Sekundärpfad), Strommessung HV-Seite), erzeugt von `bms_schaltplan.py` (Aufruf `schaltplan_bauen.sh`) aus `bms_teile.json` (dieselbe Quelle wie das Layout). Dateien: `schaltplan_quelle/` (Kopie von `/home/cae/cae_projekte/batterie/e3c/schaltplan/`), PDF `schaltplan_bms.pdf`, PNG je Blatt `schaltplan_bms_blatt-N.png`.
- **Darstellung:** Spalten von links nach rechts = Signalfluss, Passive stehen am beschalteten Bauteil, Netze innerhalb eines Blattes sind mit Drähten gezeichnet. Schützansteuerung je Kanal eine Zeile: UND-Gatter, High-Side-Schalter, Spulenstecker, Low-Side-FET, Shunt, mit Freilauf- und Zener-Löschpfad am Spulenstecker. Netznamen nur für Versorgung/GND (globale Labels) und zwischen den Blättern (hierarchische Labels, Blattpins und Drähte auf dem Deckblatt). Blätter Rechner, CAN, Schützansteuerung auf A2, übrige A3, damit kein Teil im Schriftfeld steht.
- **HV/NV-Trennung:** auf den Blättern Daisy und Strommessung als Rahmen NV | Trennung | HV mit dem Vermerk „verstärkte Isolation 10/8 mm“; auf dem Deckblatt die beiden Blattsymbole rot umrandet. Jedes Teil trägt Referenz, Wert, Tag und Akte (ENT-188…197, ERW-E3c; Akte sichtbar bei Kästen, bei Passiven als verborgenes Feld).
- ERC: 0 Verstöße. `lib_symbol_issues` und `footprint_link_issues` sind in `bms_schaltplan.kicad_pro` auf „ignorieren“ gesetzt (Symbole eingebettet, keine Bibliothekstabellen im Projekt; Footprints prüft das Layout).
- Netzliste: 98 Netze, 131 Teile; Abweichungen Schaltplan gegen Quelle 0, gegen Layout (`bms.kicad_pcb`, Pads je Netz) 0 (`ergebnis_schaltplan.json`, `bms_schaltplan_pruefung.py`). Unbenannte Netze verglichen als Zerlegung der Pins.
- Grenzen: Symbole sind generische Kästen mit den Pins der SKiDL-Teile (keine Normsymbole); Lage der Teile nach Spaltenraster; einzelne lange Drähte (UND-Gatter zu Kanal M, Schleifen unter Dioden) sind zweckmäßig, nicht schön. Netz VBAT ist auf dem Versorgungsblatt verdrahtet; Nicht verdrahtete blattinterne Netze: siehe `schaltplan_zuordnung.json` (Feld nicht_verdrahtet).

## Grenzen und offene Fragen (an Opus)
1. **Erledigt durch Opus:** Merkmal BT-722 (ENT-194) und BT-311 Luftstrecke, Abstand NV, Schützkanäle (ENT-195…197). Das Pack liest ENT-194 aus `parameter.json`; `bms_regeln.py` und `bms_skidl.py` haben die Werte noch als Konstanten (noch nicht auf `parameter.json` umgestellt, Wert gleich). Abstand HV 0,2 mm gehört zu ENT-168 an BT-321.
3. **Passiv-Werte offen:** Kein Widerstands-/Kondensatorwert steht in der Erwartung; die BOM trägt „Wert offen“. Footprintgrößen (0603, 0805, 1206, SMA, SMB u. a.) sind Platzhalter von Sonnet.
4. **Strom der Schützpfade:** `haltestrom_A` (BT-715) ist nicht festgelegt. Die Leistungsnetze (VBAT, Spulen, Zener) haben als Platzhalter 0,4 mm Bahnbreite (M_SPULE_N, M_SPULE_P, M_ZENER …); Stromtragfähigkeit nicht nachgewiesen.
5. **HV-Hilfsversorgung:** Die HV-Seite (Shunt-ADC, Isolatoren) braucht eine Versorgung (`HV_VDD`, `HV_GND`). Die Erwartung nennt keine; sie kommt hier über die Stecker J_SHUNT und J_SEKUNDAER von außen. Quelle und Isolation offen.
6. **Lesart der Tabelle:** „Isolator“ = digitaler Isolator für den Sekundärpfad (U_ISO_SEK), „Shunt-ADC-Isolator“ = digitaler Isolator für die Daten des Shunt-ADC (U_ISO_SHUNT). Bitte bestätigen.
7. **Teilezahl 131 unter 150–220:** Entkopplung, TVS, ESD und Terminierung sind enthalten; mehr Teile hätte nur Füllung bedeutet, deshalb nicht erhöht.
8. **Masse:** Dichten und Bauteilmassen R_0603, C_0603, SOT-23 aus ERWARTUNG e3_platine Nachtrag 6 (Annahme Opus). Alle übrigen Bauteile = STEP-Volumen x 1,4 g/cm³ (dort nur für Stecker; hier ausgedehnt, Sonnet). Kupfer 70 µm auf allen Lagen (wie E3, Annahme), ohne Abzug von Überlappungen (obere Schranke). 3 Footprint-Gruppen ohne 3D-Modell in der Bibliothek (JST PH 4 und 2 polig, Gleichtaktdrossel) sind mit 0 angesetzt, im 3D-Bild und im STEP fehlen sie ebenfalls.
9. **Einbau:** Die Platine ist jetzt im Pack-STEP (Variante `_e3c`), Lage = Ecke des BMS-Platzes (nicht festgelegt, Annahme). Das Einbaubild zeigt dieselbe Lage.
12. **Dateiverlust behoben:** Beim Umbau von `cad/pack/pack_e2d.py` auf E3c wurde die Datei durch einen Skriptfehler kurz geleert. Wiederhergestellt aus `git HEAD` plus den fünf protokollierten Änderungen (E3: 3, Teil A: 2, mit identischen Zeilennummern wie vorher); Kopie des Stands davor liegt nicht vor. Bitte `git diff cad/pack/pack_e2d.py` gegenlesen. Beide Läufe (_e3c) liefen danach fehlerfrei.
10. **Steckrichtung** der Stecker (Eingriff zum Rand) und **Auslegungshöhe 3000 m** sind nicht geprüft; die Luftstrecke 8 mm stammt aus der Erwartung ohne Normbeleg.
11. Routing: Freerouting-Läufe 1–6 (`ergebnis_routing.json`); die ersten Läufe mit Flächen auf In2 sind nicht übernommen.

*KI-generiert (Claude Sonnet, 2026-11-24). Status Entwurf.*
