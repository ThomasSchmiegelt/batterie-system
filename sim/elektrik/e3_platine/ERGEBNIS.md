| Dok.-Nr. | ERG-E3 | Version | 0.5 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Ergebnis E3: CMU-Leiterplatte (KiCad), Ausgleich und Vorladung (SPICE), Platine im Pack | Ersteller | Claude Sonnet (KI) | Prüfer | Opus (offen) |

> **KI-generiert** (Claude Sonnet, 2026-11-24). Entwurf, nicht freigegeben. Grundlage `ERWARTUNG.md` mit Nachtrag 1. Zahlen aus `ergebnis_ausgleich.json`, `ergebnis_vorladung.json`, `ergebnis_platine.json`, `ergebnis_waerme.json` (dieser Ordner), `cad/pack/entwurf/ergebnis_<V>_e2d_e3.json`. v0.5 ersetzt v0.4: Nachtrag 6 (Thermovias im eigenen Netz mit B.Cu-Kupferflächen, Masse aus Layout, Explosionsansicht und Einbauort). v0.4 ersetzte v0.3: Nachträge 4 und 5 (ENT-168 = 0,2 mm), Platine vollständig geroutet. Grundlage ab v0.3 auch Nachträge 2 und 3 der Erwartung.

## Werkzeuge
KiCad 10.0.8 (Flatpak, Nutzerinstallation; Auftrag nannte KiCad 9, Version weicht ab), ngspice 42, SKiDL 3.0.0, spicelib 1.6.4. Freerouting 2.5.0 (GPL-3, Jar mit JRE 25, `$FREEROUTING`) routet vollständig (Abschnitt Routing).  Akten ENT-163…ENT-183 (vorgeschlagen, Annahmen ERW-E3). Annahmen ERW-E3 N2 (Auftrag E3 Routing, als A_* in `cmu_skidl.py`): 4 AFE-Versorgungspins mit je 100 nF, 1 TVS je Daisy-Chain-Stecker (Eingang, Ausgang; Typ generisch), Daisy-Stecker (Nachtrag 3): 2-polig, nur 2 Datenleitungen, JST-SH-Footprint 1,0 mm liegend (generisch), GND/VCC entfernt.

## Abgleich der Erwartungen (mit Nachtrag 1)
| Nr | Erwartung | Ergebnis | Urteil |
|---|---|---|---|
| 1 | Ausgleichsstrom nach U; Verlängerung ≈ 10–15 % bei U_nenn | LFP 152,0 mA bei 3.65 V, 133,3 mA bei 3.2 V, Verlängerung bei U_nenn 14,1 %; NMC 127,4 / 112,3 mA, 13,5 % | ok |
| 2 | Kanal 0,53–0,57 W, Widerstand ≈ 0,28 W, FET ≤ 0,02 W, CMU ≈ 9,8 W ±3 % zu E2 | LFP 0,555 W, 0,272 W je R, FET 0,012 W, CMU 9,99 W (1,4 % zu E2); NMC (32,45 Ω) 0,535 W, 0,264 W je R, FET 0,008 W, CMU 9,64 W (-2,0 % zu E2; Nachtrag: ≈ 9,6 W) | LFP ok, NMC ok (Abweichung zu E2 innerhalb ±3 %) |
| 3 | 60–100 K Übertemperatur, über 105 °C bei 45 °C | 1387 W/m²; ΔT 69 K (h = 10) bis 139 K (h = 5), also 114–184 °C (NMC 67–134 K) | Urteil „verfehlt (über 105 °C)“ bestätigt; der obere Wert liegt über dem erwarteten Band, Rechnung ΔT = P/(h·2·A). E3b (Elmer) nötig |
| 4 | 9,1 A, 416 J, t_95 300 ms bei 912 V | 9,12 A, 415,8 J, 299,6 ms; Puls ≤ 450 J: ja | ok |
| 5 | ≈ 130–170 Teile je CMU | 108 Teile (v0.1: 106; plus 2 TVS) (FPC_24 1, AFE_generisch_18K 1, R 55, C 22, NMOS_generisch 18, NTC_Eingang 4, Uebertrager_generisch 2, Daisy_Stecker 2, TVS_generisch 2, Sekundaerschutz_generisch 1) | **verfehlt** (zu wenig; 18 × (2 R + FET) + 37 Filter + Rest, auch mit N2) |
| 6 | Layout passt 120 × 60 mm, 4 Lagen, DRC und ERC 0 Fehler | passt; DRC LFP 0, NMC 0 Verstöße, aber 0 unverbundene Elemente (nicht geroutet); SKiDL-ERC 0 Fehler; `kicad-cli sch erc` nicht möglich (kein .kicad_sch) | ok: geroutet, Netzklassen 0,2 / 2,5 mm gehalten (DRC aus `.kicad_dru`) |
| 7 | STEP im Pack ohne Kollision, Masse ≤ 80 g | Platine 120 × 60 × 4,56 mm (Platz 10 mm); Kollisionen mit CMU: LFP 0, NMC 0 ; Kollisionen gesamt LFP 3 (vorher 3), NMC 0 (vorher 0). Masse (ERWARTUNG Nachtrag 6, `ergebnis_platine.json`): LFP Platine ohne Pad 27,2 g, mit Pad 48,9 g; NMC 27,2 g, mit Pad 48,9 g. Pack rechnet jetzt mit diesen Massen (je CMU, statt 0,08 kg): Gesamtmasse LFP 620,57 → 620,13 kg, NMC 483,15 → 482,75 kg | Kollision: siehe Zahlen; Masse ≤ 80 g (Platine, auch mit Pad 48,9 g): ok |

## Kriechstrecken und Netzklassen
`drc_regeln.py` schreibt `.kicad_pro`/`.kicad_dru`: 0,2 mm (ENT-168, Nachtrag 5) innerhalb, 2,5 mm (ENT-183) zwischen Daisy-Chain-Netzen und allen anderen. Abstand zwischen Pads desselben Bauteils (Gehäuseraster, z. B. 0,5-mm-AFE) ist mit 0,15 mm ausgenommen: **Methodenwahl, keine Normaussage**.

## Dateien
`cmu_skidl.py` (Netzliste `cmu_<V>.net`, `cmu_<V>_bom.csv`, `cmu_<V>_erc.txt`), `pcb_bauen.py`, `drc_regeln.py`, `drc_auswerten.py`, `spice_*.py`, `platine_<V>.png`. Groß (nicht im Repo): `/home/cae/cae_projekte/batterie/e3/` (kicad_pcb, Gerber, STEP, DRC-Berichte, Renderbilder). Pack: `cad/pack/pack_e2d.py` mit Schalter `PACK_E3=1` (Ausgabe `_e2d_e3`), STEP `/home/cae/cae_projekte/batterie/e2/pack_<V>_e2d_e3.step`.

## Routing
Ablauf: `pcb_bauen.py` (Platzierung, Daisy-Leitungen von Hand) → DSN (`route_dsn.py`, Default 0,2 mm, Daisy-Klasse 2,5 mm, Ausgleich D-Netze 0,3 mm, Via 0,6/0,3) → `$FREEROUTING -mp 10` → SES-Import → `via_aufraeumen.py` → `kicad-cli pcb drc` mit `.kicad_dru`. Zahlen aus `ergebnis_platine.json` und `ergebnis_routing.json`.
- **Endstand:** LFP 0 Verstöße, 0 offene Verbindungen; NMC 0 Verstöße, 0 offen. Leiterbahnsegmente LFP 1070, NMC 1093.
- **Weg dahin (Methode):** Mit 0,6 mm als globalem Abstand (Fehler Opus, Nachtrag 5) blieben 74–82 Verbindungen offen (frühere Läufe). Mit 0,2 mm blieben nur die Daisy-Netze offen, weil Freerouting Daisy-Pads (Raster 1 mm) gegeneinander mit 2,5 mm Abstand bewertet; Freerouting kennt hier keine Klasse-gegen-Klasse-Ausnahme. Deshalb sind die 8 Verbindungen der Daisy-Strecke (2 Übertrager, 2 Stecker, 2 TVS) **von Hand vorverlegt** (F.Cu, 0,2 mm, Korridor zwischen Filterreihen), der Router hält 2,5 mm dazu ein.
- **Abweichungen von den Vorgaben:** (1) Klasse Ausgleich 0,3 mm nur für die D-Netze (Widerstand-FET), nicht für die T-Netze: 0,3 mm kommt nicht aus dem 0,5-mm-FPC-Pinfeld (mit T-Netzen in der Klasse blieb 1 Verbindung offen). (2) 3 Bahnen mit 0,12 mm aus dem Router (NMC) auf 0,15 mm verbreitert (Mindestbreite aus `.kicad_pro`, meine Einstellung); 6 hängende Vias (LFP) entfernt. (3) Ungenutzte Pads des generischen Übertragers und des Daisy-Steckers (MP) entfernt, damit Freerouting sie nicht als Verstoß meldet. (4) Der Teil der Bahnen unter 0,2 mm (Signal) sind keine Absicht, siehe (2).
- **Thermovias (ENT-187, Nachtrag 6, `thermovias.py`; parameter.json BT-321.vias_je_widerstandspaar = 8):** Neu gesetzt: Die Vias 0,6/0,3 mm sitzen **im eigenen Netz** der Widerstandspads (je Pad 2 Vias in der Padfläche), und auf B.Cu liegt **je Widerstandsnetz eine Kupferfläche** (Rechteck um die Pads, Abstand zu fremdem Kupfer ≥ 0,2 mm, vom Füller gesetzt). Gesetzt: LFP 144 von 144 (36 Flächen), NMC 144 von 144 (36 Flächen); Quelle `thermovias_<V>.json`. DRC danach LFP 0 / NMC 0 Verstöße, 0 / 0 offen. **Ausnahme (Opus, Frage 9):** Unter den NMC-Pads R22, R23 (Bahnen S0/G1 um je 10,75 µm auseinandergeschoben), R24, R26, R27 reichte der Platz zwischen Innenlagenbahnen und F.Cu-Bahn nicht für Via 0,6/0,3 mm mit 0,2 mm Abstand. Dort sitzen 1 Via(s) mit **0,45/0,2 mm** (Abstand weiter 0,2 mm, teils mit Rand ins Pad ragend, Überlappung ≥ 0,05 mm). Dafür sind in `cmu_NMC.kicad_pro` Mindest-Via 0,4 mm und Mindestbohrung 0,2 mm gesetzt (nur NMC). Die 8 Vias je Paar (ENT-187) bleiben, das Netz T4 hat nun auch seine B.Cu-Fläche.
- Kriechstrecke ≥ Luftstrecke (`ergebnis_kriechstrecke.json`): innerhalb 0.2 mm gegen 0.2 mm: ok; Trennstelle 2.5 mm gegen 2.5 mm: ok. Die Luftstrecke ist hier gleich dem DRC-Abstand gesetzt (kein Wert für die Stoßspannung vorhanden), Auslegungshöhe 3000 m ist eine offene Frage an den Autor.

## Bilder
`platine_<V>.png` (Ober-/Unterseite mit Zielband), `platine_<V>_3d_iso|top|bottom|nah.png` (KiCad-3D, Leiterbahnen und Vias sichtbar, neu mit den Thermovias), **`platine_<V>_explosion.png`** (Blender-Explosionsansicht: Bauteile · F.Cu · Substrat · In1 · In2 · B.Cu · Wärmeleitpad ENT-185 · Al-Rahmenausschnitt, Vias als Stäbe, Thermovias orange; .blend in `/home/cae/cae_projekte/batterie/e3/explosion_<V>.blend`), **`platine_<V>_einbau.png`** (CMU am Einbauort in der Endzone, Rest grau durchsichtig, Zellen und Deckel ausgeblendet), `schaltbild_cmu.png`, `spice_ausgleich_vorladung.png`. Lesehilfe: `lesehilfe.md`.

## Grenzen und offene Fragen (an Opus)
1. Handvorverlegung der Daisy-Strecke und Verbreiterung der 3 Bahnen (siehe Routing) sind meine Methodenwahl; bitte bestätigen.
2. Schaltplan nur als Netzliste/BOM, kein Zeichnungs-PDF; `kicad-cli sch erc` entfällt. Blockbild siehe `schaltbild_cmu.png`. Sekundärschutz als generisches Teil nur mit Pins oben und unten (Schwelle je Zelle nicht abgebildet).
3. Teilezahl 108 liegt unter der Erwartung 130–170: Quelle der 130–170 klären.
4. Masse: Innenlagen-Kupferdicke steht nicht in der Erwartung; ich habe 70 µm wie außen gesetzt (Annahme, ändert die Platine um 0,44 g). SOIC-8 (U2, 1 Stück) und D_SOD-323 (2 Stück) haben keinen Massewert im Nachtrag 6 und sind mit 0 angesetzt (`nicht_angesetzt` in `ergebnis_platine.json`). Kupferanteil aus Bahn-, Pad-, Via- und Flächenfläche ohne Abzug von Überlappungen (obere Schranke). Pad: Fläche = Platine 120 × 60 mm, 1,0 mm, 3 g/cm³ = 21,6 g (Nachtrag 6: ≈ 22 g). Stecker: STEP-Volumen der KiCad-Bibliothek × 1,4 g/cm³ (Hirose 164,2 mm³, JST 31,6 mm³, `vol.py` in `/home/cae/cae_projekte/batterie/e3/modelle/`).
5. Platzhalter N2 (siehe oben) und NTC als externe 2-polige Anschlüsse sind Annahmen. GND/VCC am Daisy-Stecker ist laut Nachtrag 3 entfernt.
6. FET-Modell U_GS = 5 V, VTO = 1,5 V: Modellwahl (von Opus übernommen). Platinen-STEP: Bauteilmodelle ersetzt (`--subst-models`), nur Hüllformen.
7. Platinenhöhe nach Nachtrag 3: 4.56 mm (Platz 10 mm).
8. Der Pack-Lauf LFP zeigt 3 Kollisionen schon vor E3 (Trennbrücke/Servicedeckel, Schmelzlasche); unverändert.
9. NMC: alle 144 Thermovias gesetzt, davon 1 als kleinere Via 0,45/0,2 mm (Ausnahme laut Opus, siehe Thermovias oben).

*KI-generiert (Claude Sonnet, 2026-11-24). Status Entwurf.*
