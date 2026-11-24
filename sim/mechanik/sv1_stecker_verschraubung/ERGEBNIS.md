| Dok.-Nr. | ERG-SV1 | Version | 0.1 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Ergebnis SV1: Stecker mit Gegenstück, Steckfreigang, Verschraubungen im Pack-CAD | Ersteller | Claude Sonnet (KI) | Prüfer | Opus (offen) |

> **KI-generiert** (Claude Sonnet, 2026-11-24). Entwurf, nicht freigegeben. Grundlage `ERWARTUNG.md` (ERW-SV1, nicht geändert). Zahlen aus `ergebnis.json` (Auszug aus `cad/pack/entwurf/ergebnis_<V>_e2d_e3c_sv1.json`, Vergleich `ergebnis_<V>_e2d_e3c.json`). Alle zusätzlichen Maße sind Annahmen Sonnet, Herkunft ERW-SV1, in `cad/pack/entwurf/annahmen_sv1.json` (A_sv1_*). Sicherungen der geänderten Dateien: `/tmp/claude-1003/SV1/`.

## Was getan
- `cad/pack/pack_e2d.py` um `PACK_SV1=1` erweitert (setzt `PACK_E3C=1` voraus, Ausgabe `_sv1`): Kabelstecker (transparent) mit Gegenstück (fest), Gruppe `E2_Steckfreigang` mit Kollisionsprüfung gegen feste Teile (Ausnahmen je Stecker: eigene Teile, eigene Leitungen, Servicedeckel bei der Trennbrücke), M3-Schrauben mit Abstandsbolzen je CMU. Lauf: `sim/mechanik/sv1_stecker_verschraubung/pack_sv1.sh LFP NMC` (CPU, LFP ca. 5 min, NMC ca. 9 min).
- Bilder: `cad/pack/render_sv1.py` (Blender CPU), `cad/pack/label_sv1.py`; je Variante Schaltbox und Endzone.
- CMU-Platine: Bohrungen im Skript ergänzt (`sim/elektrik/e3_platine/pcb_bauen.py`, `drc_regeln.py`, `sv1_loecher.py`, `route_sv1.sh`); Routing nicht vollständig, siehe unten.

## Abgleich der Erwartungen
| Nr | Erwartung | Ergebnis (Quelle `ergebnis.json`) | Urteil |
|---|---|---|---|
| 1 | Steckfreigänge außen frei; 1–3 Verletzungen, vor allem Schaltbox | LFP 211 und NMC 215 Verletzungen (Freigang gegen festes Teil, je Paar gezählt), 62 bzw. 60 Freigangkörper. Hauptursachen: Daisy-/FPC-Freigang je CMU gegen Seitenrahmen, Zellen, Kühlplatte/Pad (Quer 10 mm bei 1 mm Wandabstand, Steckrichtung ±y), Handräume Ø 75 der Deckelstecker gegen Nachbarstecker, HV-250-Freigang gegen Deckel und obere Kühlplatte, BMS-Stecker gegen Schaltbox-Wanne (5) | verfehlt (Erwartung unterschritten) |
| 1b | keine harten Kollisionen | LFP 0; NMC 52: Daisy-Gegenstück (Buchse) gegen Zellträger und Verguss des Feldes 0 und 3 | NMC verfehlt |
| 2 | CMU-Bohrungen, DRC 0, 0 offen | **nicht erreicht**: LFP-Routing mit Sperrflächen: 5 offen laut Freerouting; nach SES-Import DRC 1 Verstoß (shorting_items) und 2 offen. Nachlauf mit bestehenden Bahnen verschlechterte (12 offen). Abbruch laut ERW → OPUS. Platinen und STEP in `/home/cae/cae_projekte/batterie/e3/` auf den Stand vor SV1 zurückgesetzt (LFP und NMC DRC 0 und 0 offen, Gerber neu erzeugt). Versuch: `e3/sv1_versuch/` | verfehlt |
| 3 | Masse + 0,3–0,6 kg | LFP + 1,29 kg, NMC + 1,26 kg (Masse bekannt 619,85 → 621,13 bzw. 482,41 → 483,68). Treiber: Annahmemassen der Kabelstecker (A_sv1_masse_kg) | verfehlt |
| 4 | Bilder je Variante: Schaltbox, Endzone; Detail HV-Stecker | 4 Bilder (`sv1_<V>_schaltbox.png`, `sv1_<V>_endzone.png`); Detail HV-Stecker entfällt (Zeit) | teilweise |

## Offene Punkte und Fragen an Opus
1. **Fehlende Merkmale** in `struktur.json` (nicht angelegt): BT-321 und BT-311 `befestigung`, `bohrung_d_mm`, `bohrung_abstand_rand_mm`, `bohrung_kupferabstand_mm`; für BT-720, BT-730, BT-740, BT-360, BT-311, BT-711 `steckfreigang_mm` (Steckweg, Länge, Greifraum, quer). Bis dahin A_sv1_*.
2. **CMU-Bohrungen nicht routbar vollständig:** Mitte 2,8 mm vom Rand (kleinster Wert, bei dem R20/R38 noch 2 mm Kupferabstand zur Bohrung haben, ohne Bauteile zu verschieben). Entscheidung nötig: Bauteile R20/R38 verlegen oder Bohrung anders setzen oder Platine vergrößern. Der KiCad-SES-Import scheitert bei Boards mit Bauteilen ohne Pads (NPTH); Abhilfe `sv1_loecher.py`. Im Pack sind die Schrauben dennoch gesetzt, das CMU-STEP im Pack ist das alte ohne Bohrungen.
3. **BMS-Platine (6 Bohrungen) offen:** E3c ERGEBNIS v0.3 lag erst spät vor, die Zeit für Routing und Neuexport reichte nicht. Die BMS-Kabelstecker im Pack folgen der Lage aus `e3c_bms_platine/layout_info.json` (Stand v0.3), Richtung zum nächsten Rand, Annahme.
4. **Abstandsbolzen 6 mm** passen nicht: Die CMU liegt im E3-Modell mit der Rückseite an der Wand. Bolzen sind als Hülse im Rahmen dargestellt (zugelassene Überlappung `SV1 Schraube im Rahmen`). Konflikt mit dem Wärmepad ENT-185 klären.
5. **Vereinfachungen (Integrationsgrenzen):** Gegenstück der Platinenstecker als Quader hinter dem Stecker; die echten Stecker der CMU-Platine (E3) liegen an anderer Stelle als die E2-Quader; Stecker überlappt Flansch/Schraubenköpfe/Platine (als Kontakt „gesteckt“ gezählt, 197 bzw. 184 zugelassene Kontakte); HV 250 A koaxial entlang des Körpers, nicht senkrecht zum Deckel wie in der ERW; Handraumhöhe = Freigangshöhe; Freigang-Freigang-Überlappungen nicht gezählt; Steckfreigang der BMS-Stecker gegen die BMS-Platine ausgenommen.
6. Schütze, Sicherung, Shunt (M5/M8) sind vorhanden und sichtbar, keine Änderung.

## Dateien
`cad/pack/pack_e2d.py`, `cad/pack/entwurf/annahmen_sv1.json`, `cad/pack/render_sv1.py`, `cad/pack/label_sv1.py`, `sim/mechanik/sv1_stecker_verschraubung/{ergebnis.json,lesehilfe.md,pack_sv1.sh,sv1_*_*.png}`, `sim/elektrik/e3_platine/{pcb_bauen.py,drc_regeln.py,sv1_loecher.py,route_sv1.sh}`, `praesentation/bausteine/SV1.md`.

> KI-generiert (Claude Sonnet, 2026-11-24), Entwurf, nicht freigegeben.
