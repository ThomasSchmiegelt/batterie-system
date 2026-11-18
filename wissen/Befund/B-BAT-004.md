---
typ: befund
tags: ["befund"]
---
# B-BAT-004

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

B-BAT-004 (2026-11-16) Analyse: Was fehlt für die komplette Batterie (Struktur gegen Information)

Quelle: [[BEFUNDE]]

## Vorgänge
- [[wissen/Vorgang/R1|R1]] – Wissensaufbau W01-W15 (Chemie, Zelltypen, Spannung, Kabel, Steuerung, Struktur)
- [[wissen/Vorgang/R2|R2]] – Werkzeuge T01-T07 (Open Source Zellchemie, Elektroauslegung, Ersatzmodelle)
- [[wissen/Vorgang/R3|R3]] – Patente P01-P10
- [[wissen/Vorgang/R4|R4]] – Recherche prüfen: Zitate, Aussagen, Widersprüche -> BEFUNDE
- [[wissen/Vorgang/R5|R5]] – Werkzeugwahl festlegen (ENT): Zellmodell, Packmodell, Schaltung
- [[wissen/Vorgang/V1|V1]] – Lastenheft-Werte REQ-P01..P08 vorschlagen (Fahrzeug, kWh, Spannung, Leistung, Laden, Chemie, Bauraum, Temperatur)
- [[wissen/Vorgang/SL1|SL1]] – Grobe Stückliste aus Startsatz (Baugruppen, Mengen mit Herleitung)
- [[wissen/Vorgang/C2|C2]] – Zellmodell LFP (PyBaMM Prada2013) auf langes Format skalieren
- [[wissen/Vorgang/C5|C5]] – Alterung (Zyklen, Kalender) und Vergleich NMC / Natrium-Ionen
- [[wissen/Vorgang/G1|G1]] – Zellmaße als ENT-Akten (aus W03/W08/P01, sonst Annahme)
- [[wissen/Vorgang/G4|G4]] – Pack: Zellanordnung, Querträger, Kühlplatte, Deckel
- [[wissen/Vorgang/K0|K0]] – Kühlart Luft gegen Wasser (1D-Wärmebilanz Schnellladen, W16), Entscheidung ENT
- [[wissen/Vorgang/E1|E1]] – Zellverbinder/Kabel: Querschnitt, Verluste, Erwärmung (Zielband als Annahme)
- [[wissen/Vorgang/E2|E2]] – Schutzkonzept: Sicherung, Schütze, Vorladung, Isolationswächter
- [[wissen/Vorgang/E3|E3]] – Steuerung/BMS: Messkonzept, Ladezustand, Ausgleich (Konzept, offene Software aus T06)
- [[wissen/Vorgang/E4|E4]] – Schaltungsmodell ngspice/Modelica: Vorladung, Kurzschluss
- [[wissen/Vorgang/U1|U1]] – ERWARTUNG Ersatzmodell: Zielgröße, Gültigkeitsbereich, Mindestgüte (z. B. Rangkorrelation)
