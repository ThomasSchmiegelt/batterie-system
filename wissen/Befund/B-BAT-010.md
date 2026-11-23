---
typ: befund
tags: ["befund"]
---
# B-BAT-010

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

B-BAT-010 (2026-11-16) Zwei Varianten parallel: LFP-Blade und NMC-4680, gleiche Spezifikation

Quelle: [[Dokument/BEFUNDE]]

## Vorgänge
- [[Vorgang/V1|V1]] – Lastenheft-Werte REQ-P01..P08 vorschlagen (Fahrzeug, kWh, Spannung, Leistung, Laden, Chemie, Bauraum, Temperatur)
- [[Vorgang/G1|G1]] – Zellmaße als ENT-Akten (aus W03/W08/P01, sonst Annahme)
- [[Vorgang/G3|G3]] – Verschaltung sS/pP aus Spannung und Energie festlegen (ENT)

## Text aus BEFUNDE.md

- Autor: „kannst du auch zwei varianten paralell bauen? bei mit den selben spezifikationen“; Wahl NMC = Rundzelle 4680.
- Umsetzung (Sonnet, Auftrag pm/AUFTRAG_VARIANTEN.md, Opus geprüft): Akten haben `variante:` (null = alle); pm.py pruefe erlaubt gleiche Merkmale in verschiedenen Varianten; parameter.json (gemeinsam) + parameter_LFP/NMC.json; startwerte.py/stueckliste.py `--variante`. Gemeinsam: ENT-004 Baum, ENT-006 800 V.
- Akten: ENT-005 nur [LFP]; ENT-007…011 [NMC] (NMC811, Rundzelle 4680, 23,125 Ah, 3,7 V, 355 g; W20), entschieden (Mensch, Formatwahl des Autors, Werte gemessen). ENT-012 (vorgeschlagen): Baum mit Feld `varianten`, BT-250 Zellhalter (NMC), BT-100 durchmesser/hoehe, BT-220/240 nur LFP; 50 Einträge.
- Fehler von Sonnet gemeldet und von Opus behoben: stueckliste.py las `_par["BT-000"]` statt `_par["parameter"]["BT-000"]` (Spannung kam still aus startwerte, Wert zufällig gleich).
- Variantenvergleich mit Messwerten (C0b) läuft, Erwartung vorher. Vorgang: [C0] [G1] [G3] [V1]
