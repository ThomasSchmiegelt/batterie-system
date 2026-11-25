| Dok.-Nr. | ERW-SV1 | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Erwartung SV1: Stecker mit Gegenstück, Steckfreigang, Verschraubungen im Pack-CAD | Ersteller | Claude Opus (KI) | Prüfer | – |

> KI-generiert (Opus, 2026-11-24). Vorgabe Autor 2026-11-24: „wenn stecker verbaut sind sollen stecker und gegenstück dargestellt sein. der stecker transparent. es ist wichtig die steckfreigänge sichtbar sind. es sollten auch verschraubungen vorgesehen werden.“ Regel „erst konservativ“. Alle Maße unten sind **Annahmen Opus** (Herkunft „ERW-SV1“), sofern keine Akte genannt ist.

## Anforderung
REQ-P13 (Service, Trennbarkeit), REQ-P14 (Crash, Halt der Teile), REQ-P20 (Vibration ISO 16750-3), REQ-P07 (Bauraum)

## Umfang: alle Stecker im Pack (cad/pack/pack_e2d.py)
| Stecker | heute | Gegenstück | Steckrichtung |
|---|---|---|---|
| HV_Stecker_250A, HV_Stecker_40A, NV_Stecker_26pol | Flansch mit Schrauben, nur Buchse | Kabelstecker mit Abgang 90° | außen, senkrecht zum Deckel |
| Service_Trennstecker (NMC), Trennbrücke M8 (LFP) | Körper | Stecker bzw. Brücke | von oben durch die Deckelöffnung |
| FPC_Stecker (je CMU) | Quader | FPC-Buchse auf der CMU + Stecker am FPC | parallel zur Platine |
| Daisy_Stecker (je CMU, 2) | Quader | Kabelstecker | parallel zur Platine |
| BMS-Stecker (BT-311) | aus dem KiCad-STEP | Kabelstecker | parallel zur Platine |
| Schütz-Spulenstecker | Quader | Kabelstecker | seitlich |

## Darstellung
- **Gegenstück (Buchse, fest)** blickdicht. **Stecker (beweglich) transparent** (Blender α ≈ 0,35, eigene Farbe), gesteckt dargestellt.
- **Steckfreigang** als eigener Körper je Stecker, schraffiert bzw. halbtransparent rot. Er wird **in die Kollisionsprüfung aufgenommen**: Kein festes Teil darf hinein, Kabel und Leitungen sind ausgenommen, wenn sie zum Stecker gehören.
- Maß des Steckfreigangs (Annahme ERW-SV1): in Steckrichtung Steckweg + Steckerlänge + 25 mm Greifraum, quer je 10 mm für Verriegelung und Finger. Für die Stecker auf dem Außendeckel zusätzlich ein Werkzeug- und Handraum Ø 75 mm über dem Stecker (Servicefall).

## Verschraubungen (Annahmen ERW-SV1, konservativ)
| Teil | Verschraubung |
|---|---|
| CMU-Platine (BT-321) | 4 × M3 (ISO 14580, A2) mit Abstandsbolzen 6 mm in den Rahmen, Bohrungen Ø 3,2 in den Ecken, Abstand Kupfer ≥ 2 mm. Die Bohrungen müssen ins KiCad-Layout (DRC erneut 0) |
| BMS-Platine (BT-311) | 6 × M3 mit Abstandsbolzen 8 mm auf den Boden der Schaltbox. Bohrungen nur im NV-Bereich bzw. im HV-Bereich mit Kriechstrecke 10 mm zum NV-Bezug |
| FPC- und Daisy-Stecker | Platinenstecker mit Verriegelung, keine Schraube |
| HV-/NV-Flanschstecker | vorhanden (Akten hv250/hv40/nv_schrauben), prüfen und darstellen |
| Schütze, Sicherung, Shunt | Bodenverschraubung M5 (bzw. M8 an den Stromschienen nach vorhandener Akte), sichtbar |
| Kabelhalter | nicht im Umfang |

Neue Merkmale (z. B. BT-321 `befestigung`, `bohrung_d_mm`; BT-311 dasselbe; BT-7xx `steckfreigang_mm`): nicht selbst anlegen → an OPUS melden, dann die Akten.

## Erwartung
1. Steckfreigänge außen am Deckel frei. **Kritisch** sind (a) der Daisy- bzw. FPC-Stecker der CMU zur Endwand (Bauraum 10 mm, Steckrichtung parallel zur Platine sollte passen) und (b) die BMS-Stecker in der Schaltbox (Turm 89 mm, ENT-144). **Erwartung: 1–3 Verletzungen**, vor allem in der Schaltbox. Jede Verletzung → OPUS mit Maß, nicht selbst verschieben.
2. Bohrungen auf der CMU: Mit den Ecken bei 120 × 60 bleibt das Routing machbar. Die Bohrungen verdrängen schlimmstenfalls 2–4 Vias, DRC wieder 0. Geht es nicht → OPUS (nicht vergrößern).
3. Masse: + ≈ 0,3–0,6 kg je Variante (Schrauben, Bolzen, Gegenstecker).
4. Bilder:
   - je Variante eine Ansicht der Schaltbox und eine Ansicht der Endzone
   - Stecker transparent, Gegenstück fest, Steckfreigänge rot halbtransparent, Schrauben sichtbar
   - Detail eines HV-Steckers außen mit Handraum

## Abbruch → OPUS
Jede Verletzung eines Steckfreigangs; fehlendes Merkmal; Bohrung nicht routbar.

## Nachtrag 1 (Opus, 2026-11-24 19:50, Stand bei Frist 20:30)
- Teilergebnis: Gegenstücke, Freigänge und Schrauben sind im Pack modelliert, 4 Bilder.
- **211/215 Freigangsverletzungen sind nicht glaubhaft als echte Verletzungen.** Vermutlich prüft das Skript die Freigänge auch gegen das eigene Kabel, den eigenen Stecker oder Nachbarzellen. Die 52 harten Kollisionen bei NMC (Daisy-Gegenstück gegen Zellträger/Verguss) sind dagegen echt. Beides prüft Opus in der nächsten Sitzung an ergebnis.json (Liste der Paare), dann folgen die Ausnahmen bzw. die Lage der Daisy-Stecker.
- CMU-Bohrungen: Das Routing ist bei 120 × 60 mit 4 Bohrungen gescheitert, der Stand ist zurückgesetzt. Nächster Versuch: Bohrungen nur an 2 Ecken + Klemmung im Rahmen, oder 3 Bohrungen. Entscheidung Opus offen.
- Fehlende Merkmale (befestigung, bohrung_*, steckfreigang_mm) → in der nächsten Sitzung anlegen.

## Nachtrag 2 (Opus, 2026-11-25, nach W1)
Reihenfolge, erst konservativ:
1. **CMU-Bohrungen:** Variante **B3** (2 Ecken + 1 Bohrung mittig an der gegenüberliegenden Langseite) direkt rechnen, ohne Wächter, mit 200 Passes. Daisy-Regel 2,5 mm (ENT-183) bleibt. Gelingt B3 nicht, **B4v** mit 200 Passes. Abnahme DRC 0, 0 offen, 144 Thermovias, danach NMC per Übertragung. Die Lagen der Bohrungen aus `sim/elektrik/w1_kolibri_waechter/ERGEBNIS.md` übernehmen, als Annahme ERW-SV1 N2.
2. Abweichung Router-Log (3 unrouted) gegen KiCad-DRC (0 unverbunden) klären. Maßgebend ist der KiCad-DRC.
3. **Freigangslogik prüfen:** Die 211/215 Verletzungen nach Paaren gruppieren. Eigene Teile (Kabel, Gegenstück, Platine desselben Steckers) gehören in die Ausnahmen. Echte Verletzungen an OPUS mit Maß melden.
4. **NMC-Daisy:** Die 52 Kollisionen (Gegenstück gegen Zellträger/Verguss) prüfen. Vorschlag zur Lage melden, nicht selbst ändern.
5. Neue Merkmale: BT-321/BT-311 `befestigung`, `bohrung_d_mm`, `bohrung_anzahl`, BT-7xx `steckfreigang_mm` werden von Opus angelegt (siehe struktur.json), dann die Akten vorgeschlagen.

## Nachtrag 3 (Opus, 2026-11-25, Entscheidungen nach ERGEBNIS v0.2)
1. **Bohrungen CMU: B4 an den Ecken (2,8|2,8), 4 × M3.** `frei_pruefung.txt` zeigt an allen 4 Ecken ≥ 2,0 mm Abstand Kupfer–Bohrung. Das Scheitern in SV1 und W1 lag an der fehlenden Daisy-Netzklasse (Platine ohne Projektdatei geladen), nicht an den Bohrungen. Rechnen mit `sv1b/lauf2.sh B4` **mit Projektdatei**. Abnahme DRC 0, 0 offen, 144 Thermovias. Danach Akten BT-321 befestigung (4 × M3, Bolzen 6 mm), bohrung_d_mm 3,2, bohrung_anzahl 4.
2. **Steckfreigang der Platinenstecker in der CMU (FPC, Daisy): Regel ändern.** Die CMU wird **vor dem Einbau gesteckt** (Montagefolge: Stecker auf die Platine, dann die Platine in die Endzone). Freigang in Steckrichtung = Steckweg + 5 mm, quer 2 mm, geprüft im Einbauzustand. Außenstecker bleiben wie gehabt (+25 mm, Handraum Ø 75). Annahme Opus, ERW-SV1 N3. Die 162/169 Verletzungen danach neu zählen.
3. **NMC-Daisy-Buchsen: Variante a)**, Aussparung im Zellträger und Verguss je Buchse (wie bei der CMU). Konservativ: keine Verlagerung der Stecker.
4. ENT-207 (BMS Ø 3,2): bestätigt.

## Nachtrag 4 (Opus, 2026-11-25)
- Die Via-Ausnahme 0,45/0,2 gilt für LFP und NMC (wie E3 Frage 9). ENT-209 bis 211 entschieden.
- Rest-Freigänge: CMU um 1,5 mm vom Seitenrahmen weg (falls kollisionsfrei, Annahme N4), NMC-Aussparung um den Daisy-Freigang erweitert. Ziel 0 Freigangsverletzungen und 0 Kollisionen.

## Nachtrag 5 (Opus, 2026-11-25)
- Opus prüft Rohdaten: DRC LFP/NMC 0/0 und 0 offen (e3/cmu_*_drc.json). Kollisionen 0/0 (ergebnis_v04.json). Die Abgabe-STEPs sind verschieden (md5), gleiche Größe ist plausibel bei gleichen Gehäusen.
- Der Wandabstand der CMU beträgt 1,0 mm in x statt 1,5 mm in y. Bestätigt als Annahme N4, weil 1,5 mm Kollisionen erzeugt.
- Offen sind 29/26 Freigangsverletzungen an BMS-, Außen- und Schütz-Spulensteckern. Sie werden je Stecker mit Eindringtiefe und Gegenkörper ausgewertet, dann entscheidet Opus über Regel oder Lage. Veraltete Bilder E3 (r3d, explosion, platine_*.png) werden mit Bohrungen neu erzeugt.
