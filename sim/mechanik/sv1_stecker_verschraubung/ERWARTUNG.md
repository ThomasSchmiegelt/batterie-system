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
