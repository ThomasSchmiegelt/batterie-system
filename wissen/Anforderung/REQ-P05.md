---
typ: anforderung
gruppe: "REQ-P"
methode: "S"
ebene: "System"
bewertung: "blockiert"
tags: ["anforderung", "bewertung/blockiert"]
kriterium_aus: ["Autor"]
verifiziert_durch: ["sim/chemie/c2_kalibrierung/ergebnis_schnellladen_n4680.json::N4680.2.zeit_10_80_min"]
---
# REQ-P05

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

Schnellladen 10 → 80 %

- Wert (Lastenheft): LFP 20 min, NMC-4680 30 min (Autor 2026-11-17 „30 minuten“, nach K1b; Variantenunterschied)
- Priorität: Muss
- Vom Autor bestätigt: ja

## Verifikation (V-Modell-Matrix)

- Methode: S (A Analyse, S Simulation, I Inspektion, T Test, R Review)
- Ebene: System
- Kriterium: t_10_80 LFP <= 20 min [Autor]<br>t_10_80 NMC <= 30 min [Autor]
- Ist-Wert: [t_10_80 LFP] blockiert: LFP ohne gemessenen Zellparametersatz nicht nachweisbar (bericht/bericht.tex, REQ-P05; sim/chemie/c2_kalibrierung/ERGEBNIS.md); [t_10_80 NMC] NMC t_10_80 = 29.68 [sim/chemie/c2_kalibrierung/ergebnis_schnellladen_n4680.json :: N4680.2.zeit_10_80_min]
- Bewertung: **blockiert**
- Matrix: [[Dokument/06_verifikationsplan]] · Lastenheft: [[Dokument/01_lastenheft]] · Verfolgung: [[Dokument/03_anforderungsverfolgung]]

## Nachweisdateien
- [[Nachweis/sim_chemie_c2_kalibrierung_ergebnis_schnellladen_n4680.json|sim/chemie/c2_kalibrierung/ergebnis_schnellladen_n4680.json]]

## Vorgänge
- [[Vorgang/V1|V1]] – Lastenheft-Werte REQ-P01..P08 vorschlagen (Fahrzeug, kWh, Spannung, Leistung, Laden, Chemie, Bauraum, Temperatur)
- [[Vorgang/V2|V2]] – Freigabe Lastenheft durch Autor
- [[Vorgang/C3|C3]] – Ratentest 0,5C/1C/2C, Wärmeleistung, R_i über SOC und T

## Bauteile
- [[Bauteil/BT-600|BT-600]]
- [[Bauteil/BT-660|BT-660]]
- [[Bauteil/BT-661|BT-661]]
- [[Bauteil/BT-662|BT-662]]
- [[Bauteil/BT-663|BT-663]]
- [[Bauteil/BT-664|BT-664]]
- [[Bauteil/BT-665|BT-665]]
- [[Bauteil/BT-711|BT-711]]
- [[Bauteil/BT-730|BT-730]]
