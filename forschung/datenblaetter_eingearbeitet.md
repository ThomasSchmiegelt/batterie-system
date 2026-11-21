| Dok.-Nr. | BAT-DOC-DB2 | Version | 0.1 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Datenblattwerte in der Baukasten-Geometrie (DB2) | Ersteller | Claude Sonnet (KI) | Prüfer | – (Opus offen) |

> **KI-generiert (Claude Sonnet, 2026-11-20).** Entwurf, nicht geprüft, nicht freigegeben. REQ-P13, REQ-P16. Eintrag in `cad/baukasten/annahmen_datenblatt.json` (kern.py liest sie zuletzt). Quellen: `quellen/datenblaetter/`, `forschung/datenblaetter.md`.

| Schlüssel | alter Wert | Datenblattwert | Datei / Seite | im PDF-Text geprüft |
|---|---|---|---|---|
| A_e2d_schuetz_bolzen_abstand_mm | 40 | 25,5 | BT-711_glvac_GLFX250.pdf S. 6 (Zeichnung; GV200: 26,7, gleicher Schlüssel) | nein, aus Zeichnung |
| A_e2_pyro_masse_kg | 0,15 | 0,23 | BT-713_sensata_pyrofuse.pdf S. 1 | ja |
| A_e2d_ntc_mm | 3 × 2 × 1 | 1,6 × 0,8 × 0,8 | BT-330_vishay_NTCS0603E3.pdf S. 2 | ja |
| A_e2d_box_druckausgleich_d_mm | 20 | 7,8 (Einbauloch) | BT-570_gore_auto-batteries-snapfit.pdf S. 2 | ja |
| A_e2_gas_masse_kg | 0,03 | 0,015 (Obergrenze „< 15 g“) | BT-770_amphenol_SGX_TRDU5.pdf S. 3 | ja |
| A_e2_hv40_mm | 50 × 40 × 40 | 45,4 × 40,6 × 49 (Händlerblatt, Ausrichtung angenommen) | BT-730_te_HVA280_header_1-2103124-1.pdf S. 2 | ja |
| A_e2_vorladewiderstand_mm | 60 × 20 × 20 | 49,99 × 28,96 × 21,44 (Buchstabenzuordnung unsicher) | BT-712_vishay_RH050.pdf S. 2 | nein, aus Zeichnung |

Bereits vorher durch Opus gesetzt (nicht erneut): A_e2_schuetz_mm, A_e2_schuetz_masse_kg, A_e2_vorladeschuetz_mm, A_e2_vorlade_masse_kg, A_e2_pyro_mm, A_e2_shunt_mm, A_e2_gas_mm, A_g5_druckausgleich_mm, A_g5_entgasungsventil_mm, A_g5_kuehlmittelfuehler_mm/_masse_kg.

## Nicht übernommen (zurück an Opus)
- Schütz GLFX250 hat Innengewinde-Anschlüsse (Zeichnung S. 6, Gewinde-Tiefe 8,5–11,5), das Modell hat Bolzen Ø8 × 15 (A_e2d_schuetz_bolzen_d/h_mm): kein Datenblattwert für Bolzen, Modellform passt nicht. Fußlaschen: 2 × Ø6 Abstand 70,5, Flanschdicke 6 (Modell 20 × 9 × 2, M5): nicht ersetzt.
- Pyro: Datenblatt verlangt Schiene 23,75 × 4 und M6 (Modell: Cu 25 × 3, Gewinde 8): Widerspruch zur Akte. PDF-Text nennt Masse ±34,85 %, datenblaetter.md ±5 %.
- Shunt IVT-S: Bohrung Ø8,3 (Modell teilt A_e2d_schiene_bohrung_mm 8,5 mit den Schienen), Lochabstand 64: nicht getrennt.
- Kabelschuh Pfisterer (L 51/42, B 22/17): Zuordnung zu A_e2d_kabelschuh_huelse_mm/_lasche_mm unklar, nicht ersetzt. Kein Maß/Datenblatt: HVP 800, MSD, Bender iso165C (nur 600 V), Eaton EKC14-40.

## Prüflauf (LFP, G5_NUR=schaltbox,kaufteile,elektronik,normteile,verbinder, 14 s)
Quelle: `cad/baukasten/ausgabe/pruefung_LFP.txt` (Lauf 2026-11-20 09:5x). Vorher 13 Fehler, nachher 15. Neue Kollisionen: keine (eine alte, Linsenkopf ↔ Kabelschuh_Plus_Box 6,2 mm³, entfällt). Neu sind drei Massenabweichungen gegen die Stückliste, weil die Stückliste noch alte Werte hat: 700.4 Sicherungen CAD 0,330 gegen 0,250 kg, 700.10 Gassensor 0,015 gegen 0,030 kg, 300.3 NTC (−75 %). Gesamtmasse 12,87 → 12,90 kg, Höhe 247 → 245 mm. Teil über 20 % größer: HV40 Höhe 40→49 (+22 %), Vorladewiderstand Breite 20→28,96; Prüfung gegen Innenhöhe 66 mm nicht gesondert gemacht (Pyro 75, Schütz 74,5 sind schon vorher > 66 und liegen offenbar), Opus bitte prüfen.

Zeile docs/08: `| 2026-11-20 | Sonnet | DB2 Datenblattwerte in Geometrie | forschung/datenblaetter_eingearbeitet.md, cad/baukasten/annahmen_datenblatt.json | Opus-Stichprobe offen | Entwurf |`

---
*KI-generiert (Claude Sonnet, 2026-11-20). Status Entwurf. Freigabe nur durch den Autor.*
