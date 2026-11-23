---
typ: anforderung
gruppe: "REQ-P"
methode: "A"
ebene: "System"
bewertung: "nachgewiesen (Kriterium Annahme, Autor offen)"
tags: ["anforderung", "bewertung/nachgewiesen"]
kriterium_aus: ["startwert:abgeleitet.kWh_brutto"]
verifiziert_durch: ["pm/bauteile/stueckliste_LFP.json::summen.energie_kWh", "pm/bauteile/stueckliste_NMC.json::summen.energie_kWh"]
---
# REQ-P02

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

nutzbarer Energieinhalt

- Wert (Lastenheft): aus Reichweite 400 km (Vorgabe Autor 2026-11-16) × Verbrauch (Annahme), Vergleich sim/chemie/vergleich_lfp_nmc
- Priorität: Muss
- Vom Autor bestätigt: nein

## Verifikation (V-Modell-Matrix)

- Methode: A (A Analyse, S Simulation, I Inspektion, T Test, R Review)
- Ebene: System
- Kriterium: E_brutto LFP >= 73.9 kWh [Startwert (Vorschlag)]<br>E_brutto NMC >= 73.9 kWh [Startwert (Vorschlag)]
- Ist-Wert: [E_brutto LFP] LFP E_brutto = 73.92 [pm/bauteile/stueckliste_LFP.json :: summen.energie_kWh]; [E_brutto NMC] NMC E_brutto = 74.27 [pm/bauteile/stueckliste_NMC.json :: summen.energie_kWh]
- Bewertung: **nachgewiesen (Kriterium Annahme, Autor offen)**
- Matrix: [[Dokument/06_verifikationsplan]] · Lastenheft: [[Dokument/01_lastenheft]] · Verfolgung: [[Dokument/03_anforderungsverfolgung]]

## Nachweisdateien
- [[Nachweis/pm_bauteile_stueckliste_LFP.json|pm/bauteile/stueckliste_LFP.json]]
- [[Nachweis/pm_bauteile_stueckliste_NMC.json|pm/bauteile/stueckliste_NMC.json]]

## Vorgänge
- [[Vorgang/V1|V1]] – Lastenheft-Werte REQ-P01..P08 vorschlagen (Fahrzeug, kWh, Spannung, Leistung, Laden, Chemie, Bauraum, Temperatur)
- [[Vorgang/V2|V2]] – Freigabe Lastenheft durch Autor
- [[Vorgang/G3|G3]] – Verschaltung sS/pP aus Spannung und Energie festlegen (ENT)

## Bauteile
- [[Bauteil/BT-000|BT-000]]
- [[Bauteil/BT-200|BT-200]]
- [[Bauteil/BT-210|BT-210]]
