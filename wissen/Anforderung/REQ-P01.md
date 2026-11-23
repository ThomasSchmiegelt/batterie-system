---
typ: anforderung
gruppe: "REQ-P"
methode: "R"
ebene: "System"
bewertung: "nachgewiesen"
tags: ["anforderung", "bewertung/nachgewiesen"]
kriterium_aus: ["Autor"]
verifiziert_durch: ["sim/chemie/varianten_lfp_nmc/ergebnis.json::varianten.LFP.faelle.A.hauptwert.gesamtmasse_kg", "sim/chemie/varianten_lfp_nmc/ergebnis.json::varianten.NMC.faelle.A.hauptwert.gesamtmasse_kg"]
---
# REQ-P01

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

Anwendung / Fahrzeugklasse

- Wert (Lastenheft): Pkw, Fahrzeugmasse etwa 1500 kg, Anhaltswert (Autor 2026-11-16); Auslegung rechnet Fall A (mit Batterie) und Fall B (ohne Batterie) als Spanne
- Priorität: Muss
- Vom Autor bestätigt: ja

## Verifikation (V-Modell-Matrix)

- Methode: R (A Analyse, S Simulation, I Inspektion, T Test, R Review)
- Ebene: System
- Kriterium: m_fahrzeug == 1500 kg [Autor]
- Ist-Wert: LFP m_fahrzeug = 1500 [sim/chemie/varianten_lfp_nmc/ergebnis.json :: varianten.LFP.faelle.A.hauptwert.gesamtmasse_kg]; NMC m_fahrzeug = 1500 [sim/chemie/varianten_lfp_nmc/ergebnis.json :: varianten.NMC.faelle.A.hauptwert.gesamtmasse_kg]
- Bewertung: **nachgewiesen**
- Matrix: [[Dokument/06_verifikationsplan]] · Lastenheft: [[Dokument/01_lastenheft]] · Verfolgung: [[Dokument/03_anforderungsverfolgung]]

## Nachweisdateien
- [[Nachweis/sim_chemie_varianten_lfp_nmc_ergebnis.json|sim/chemie/varianten_lfp_nmc/ergebnis.json]]

## Vorgänge
- [[Vorgang/V1|V1]] – Lastenheft-Werte REQ-P01..P08 vorschlagen (Fahrzeug, kWh, Spannung, Leistung, Laden, Chemie, Bauraum, Temperatur)
- [[Vorgang/V2|V2]] – Freigabe Lastenheft durch Autor

## Bauteile
- [[Bauteil/BT-000|BT-000]]
