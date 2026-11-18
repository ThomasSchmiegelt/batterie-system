| Dok.-Nr. | BAT-DOC-03 | Version | 0.2 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Anforderungsverfolgung (erzeugt aus dem Netzplan) | Ersteller | Claude Opus (KI), pm/plan/wissensnetz.py | Prüfer | – (Mensch offen) |

> **KI-generiert.** Nicht von Hand bearbeiten: `python3 pm/plan/wissensnetz.py` schreibt diese Datei neu. Entwurf, nicht freigegeben.

| REQ | Anforderung | Vorgänge | Nachweise (Ergebnis, Befund) | Status |
|---|---|---|---|---|
| REQ-P01 | Anwendung / Fahrzeugklasse | V1, V2 | B-BAT-004, B-BAT-006, B-BAT-007, B-BAT-008, B-BAT-009, B-BAT-010, B-BAT-011, B-BAT-013, pm/startwerte.json | in Arbeit |
| REQ-P02 | nutzbarer Energieinhalt | V1, V2, G3 | B-BAT-004, B-BAT-006, B-BAT-007, B-BAT-008, B-BAT-009, B-BAT-010, B-BAT-011, B-BAT-013, pm/startwerte.json | in Arbeit |
| REQ-P03 | Systemspannung (Nenn, min, max) | V1, V2, G3, E4 | B-BAT-002, B-BAT-004, B-BAT-006, B-BAT-007, B-BAT-008, B-BAT-009, B-BAT-010, B-BAT-011, B-BAT-013, pm/startwerte.json | in Arbeit |
| REQ-P04 | Dauer- und Spitzenleistung Entladen | V1, V2, C3, E1 | B-BAT-003, B-BAT-004, B-BAT-006, B-BAT-007, B-BAT-008, B-BAT-009, B-BAT-010, B-BAT-011, B-BAT-013, pm/startwerte.json | in Arbeit |
| REQ-P05 | Schnellladen 10 → 80 % | V1, V2, C3 | B-BAT-004, B-BAT-006, B-BAT-007, B-BAT-008, B-BAT-009, B-BAT-010, B-BAT-011, B-BAT-013, pm/startwerte.json | in Arbeit |
| REQ-P06 | Zellchemie | V1, V2, C2, C5 | B-BAT-001, B-BAT-004, B-BAT-005, B-BAT-006, B-BAT-007, B-BAT-008, B-BAT-009, B-BAT-010, B-BAT-011, B-BAT-013, pm/startwerte.json | in Arbeit |
| REQ-P07 | Bauraum (L × B × H) und Masse | V1, V2, G4 | B-BAT-003, B-BAT-004, B-BAT-006, B-BAT-007, B-BAT-008, B-BAT-009, B-BAT-010, B-BAT-011, B-BAT-012, B-BAT-013, B-BAT-020, pm/startwerte.json | in Arbeit |
| REQ-P08 | Umgebungstemperatur Betrieb und Laden | V1, V2 | B-BAT-004, B-BAT-006, B-BAT-007, B-BAT-008, B-BAT-009, B-BAT-010, B-BAT-011, B-BAT-013, pm/startwerte.json | in Arbeit |
| REQ-P09 | max. Zelltemperatur und Spreizung | V1, V2, K0, K1, K2, K3, K4, K5, U4 | B-BAT-004, B-BAT-006, B-BAT-007, B-BAT-008, B-BAT-009, B-BAT-010, B-BAT-011, B-BAT-013, B-BAT-017, B-BAT-018, B-BAT-019, B-BAT-020, B-BAT-021, pm/startwerte.json | in Arbeit |
| REQ-P10 | Lebensdauer (Zyklen, Jahre, Restkapazität) | V1, V2, C5 | B-BAT-004, B-BAT-005, B-BAT-006, B-BAT-007, B-BAT-008, B-BAT-009, B-BAT-010, B-BAT-011, B-BAT-013, pm/startwerte.json | in Arbeit |
| REQ-P11 | Sicherheit: keine Ausbreitung des thermischen Durchgehens bzw. Warnzei | E2, X1, F1 | B-BAT-002, B-BAT-004 | offen |
| REQ-P12 | Kühlmittel und Anschlüsse | K0 | B-BAT-004, B-BAT-017, B-BAT-018 | offen |
| REQ-P13 | Schutzart, Isolation, Berührschutz | G5, E2, L1, E4 | B-BAT-002, B-BAT-004 | offen |
| REQ-P14 | Mechanik: Stoß, Schwingung, Crash | M1, X1, X2 | B-BAT-002, B-BAT-019, sim/mechanik/* | in Arbeit |
| REQ-P15 | Messung und BMS: Zellspannung, Temperatur, Isolationswächter | E3 | B-BAT-002, B-BAT-004, B-BAT-013 | offen |
| REQ-D01 | Jede Zahl ist rückverfolgbar (Rechnung mit Datei oder Quelle mit wörtl | R1, R2, R4, SL1, C4, U3, SL2, B5 | B-BAT-001, B-BAT-002, B-BAT-003, B-BAT-004, B-BAT-005, B-BAT-007, B-BAT-008, B-BAT-009, docs/13_stueckliste.md, forschung/WERKZEUGE.md, forschung/WISSEN.md, pm/bauteile/stueckliste.json | in Arbeit |
| REQ-D02 | Jedes Dokument hat einen Kopf nach BAT-DOC-00 und ist als KI-generiert | B1 | B-BAT-017, bericht/*.pdf | erfüllt? (Mensch prüft) |
| REQ-D03 | Jede Anforderung hat einen Nachweis in BAT-DOC-03 | F1 | – | offen |
| REQ-D04 | KI-Einsatz protokolliert: Modell, Aufgabe, Prüfung | B1 | B-BAT-017, bericht/*.pdf | erfüllt? (Mensch prüft) |
| REQ-D05 | Freigabe nur durch den Menschen | V2, B4 | – | offen |
| REQ-D06 | Erwartung vor jeder Rechnung, Vergleich danach | C1, C4, K1, K5, U1 | B-BAT-004, B-BAT-005, B-BAT-015, B-BAT-019, B-BAT-020, B-BAT-022 | offen |
| REQ-D07 | Fremde Inhalte und Geheimnisse nicht im Repo, Lizenzen erfasst | R1, R2 | B-BAT-001, B-BAT-002, B-BAT-003, B-BAT-004, B-BAT-005, B-BAT-008, B-BAT-009, forschung/WERKZEUGE.md, forschung/WISSEN.md | erfüllt? (Mensch prüft) |
| REQ-D08 | Patentrecherche ohne rechtliche Bewertung; Freedom to Operate nur durc | R3 | B-BAT-003, B-BAT-004, B-BAT-007, B-BAT-013, B-BAT-017, B-BAT-019, B-BAT-020, B-BAT-022, forschung/PATENTE.md | erfüllt? (Mensch prüft) |
| REQ-D09 | Rechnungen reproduzierbar: Skript, Eingaben, Softwarestand (requiremen | S0, U2 | README.md, SOFTWARE.md, requirements.txt | in Arbeit |
| REQ-D11 | Jede Entscheidung als Akte an Bauteil und Merkmal gebunden; CAD-Maße n | R5, G1, G2, G4, SL2 | B-BAT-002, B-BAT-003, B-BAT-004, B-BAT-007, B-BAT-008, B-BAT-009, B-BAT-010, B-BAT-012, B-BAT-013, B-BAT-014, B-BAT-015, B-BAT-016, B-BAT-020 | offen |
| REQ-D12 | Bauteilgespräch: jedes Bauteil begründet seine Form mit Aktenverweisen | B2 | pm/gespraeche/*.md | erfüllt? (Mensch prüft) |
| REQ-D13 | Projektdokumentation als Abschlussvideo (Zelle → … → System) | B3 | – | offen |
| REQ-D14 | Unternehmenspräsentation am Projektende, erzeugt aus den Projektdaten; | B0, B5 | – | offen |
| REQ-D10 | Aufwand messbar: Laufzeiten und Agentenaufrufe je Arbeitspaket | U2 | – | offen |

---
*KI-generiert. Erzeugt aus pm/plan/wissensnetz.json. Prüffehler: 0.*
