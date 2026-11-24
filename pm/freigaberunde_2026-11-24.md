# Freigaberunde 2026-11-24 (moderiert von Opus, Antworten des Autors als Auswahl)

KI-generiert (Claude Opus). Die Optionen hat Opus vorgeschlagen, die Auswahl traf der Autor. Grundlage: HARA BAT-DOC-24, REQ-P17…P21.

| Punkt | Entscheidung Autor |
|---|---|
| F-S1 Grenze Item | nur Pack; Umrichter, Ladegerät, Ladesäule, Kühlkreis außen sind Schnittstelle |
| F-S2 HE-01 / SG-01 | S3/E4/C3 → **ASIL D**; zwei unabhängige Spannungsmesswege je CMU (BT-325) |
| F-S5/F-S6 Umfang | HARA + Sicherheitsziele + FSR + grobe FMEDA aus KiCad-Stückliste; ohne Sicherheitsnachweis und Software |
| REQ-P17 / REQ-P21 | CISPR 25 Klasse 3; Cybersicherheit nur benennen |

## Runde 2
| Punkt | Entscheidung Autor |
|---|---|
| F-S3 HE-10 / SG-07 | E2, ASIL B |
| F-S4 FTTI | Werte §4 als Annahme übernommen, Prüfung W45 |
| HE-02…HE-12 | alle Einstufungen übernommen |
| REQ-P19, REQ-P20, REQ-D15 | festgelegt; Zahlenwerte bleiben Annahmen bis Beleg W46 |

| REQ-P19 Einsatzhöhe | 3000 m ü. NN (Alpenpässe bis ≈ 2800 m) |
| Zielmarkt | **nur Europa**, China nein (GB 38031/GB/T 31467 nur noch Vergleich in docs/20) |

## Runde 3: Gewichte KR1 (Paarvergleich der Kriterien, 21 Paare im Chat)
Ziffern 1–21: `0 1 1 0 0 0 2 2 1 0 0 1 1 0 0 0 0 0 1 1 2`. Punkte: Wirkungsgrad 11, Reifegrad 9, Fehlermöglichkeiten 8, Wärme in der CMU 7, Kosten 3, Ausgleichszeit 2, Bauraum 2 (Summe 42).

Offen: Normtexte R100/R135/2023/1542 vollständig als PDF nach `quellen/normen/` (nicht im Repo, .gitignore).

## Runde 4: Auswahl KR1
| Punkt | Entscheidung Autor |
|---|---|
| Gewählt Zellausgleich (KR1) | **K2 Wärmeleitpad zur Kühlplatte** (ENT-184, entschieden Autor); K6 als Alternative |

## Runde 5: Gewichte KR2 (10 Paare im Chat)
Ziffern `2 2 2 2 2 2 2 1 0 1` → Sicherheit 8, Verfügbarkeit 6, Reifegrad 3, Nachweisaufwand 2, Kosten 1.
