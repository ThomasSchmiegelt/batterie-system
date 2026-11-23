---
typ: anforderung
gruppe: "REQ-P"
methode: "A"
ebene: "System"
bewertung: "offen"
tags: ["anforderung", "bewertung/offen"]
verifiziert_durch: ["sim/chemie/varianten_lfp_nmc/ergebnis.json::systemspannung_V"]
---
# REQ-P03

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

Systemspannung (Nenn, min, max)

- Wert (Lastenheft): 800 V nominal (ENT-006, Autor 2026-11-16); min/max folgen aus Zellfenster
- Priorität: Muss
- Vom Autor bestätigt: nein

## Verifikation (V-Modell-Matrix)

- Methode: A (A Analyse, S Simulation, I Inspektion, T Test, R Review)
- Ebene: System
- Kriterium: U_nenn zwischen [720, 880] V [Annahme Opus]<br>U_min vorhanden [Annahme Opus]<br>U_max vorhanden [Annahme Opus]
- Ist-Wert: [U_nenn] U_nenn = 800 [sim/chemie/varianten_lfp_nmc/ergebnis.json :: systemspannung_V]; [U_min] kein Nachweis verknüpft; [U_max] kein Nachweis verknüpft
- Bewertung: **offen**
- Matrix: [[Dokument/06_verifikationsplan]] · Lastenheft: [[Dokument/01_lastenheft]] · Verfolgung: [[Dokument/03_anforderungsverfolgung]]

## Nachweisdateien
- [[Nachweis/sim_chemie_varianten_lfp_nmc_ergebnis.json|sim/chemie/varianten_lfp_nmc/ergebnis.json]]

## Vorgänge
- [[Vorgang/V1|V1]] – Lastenheft-Werte REQ-P01..P08 vorschlagen (Fahrzeug, kWh, Spannung, Leistung, Laden, Chemie, Bauraum, Temperatur)
- [[Vorgang/V2|V2]] – Freigabe Lastenheft durch Autor
- [[Vorgang/G3|G3]] – Verschaltung sS/pP aus Spannung und Energie festlegen (ENT)
- [[Vorgang/E4|E4]] – Schaltungsmodell ngspice/Modelica: Vorladung, Kurzschluss

## Bauteile
- [[Bauteil/BT-000|BT-000]]
- [[Bauteil/BT-200|BT-200]]
