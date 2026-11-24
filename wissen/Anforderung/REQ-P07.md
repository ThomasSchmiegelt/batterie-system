---
typ: anforderung
gruppe: "REQ-P"
methode: "I"
ebene: "System"
bewertung: "verfehlt (Kriterium Annahme, Autor offen)"
tags: ["anforderung", "bewertung/verfehlt"]
verifiziert_durch: ["cad/baukasten/ausgabe/ergebnis_LFP.json::breite_mm", "cad/baukasten/ausgabe/ergebnis_LFP.json::ctx.z_deckel_o", "cad/baukasten/ausgabe/ergebnis_LFP.json::hoehe_max_mm", "cad/baukasten/ausgabe/ergebnis_LFP.json::laenge_mm", "cad/baukasten/ausgabe/ergebnis_NMC.json::breite_mm", "cad/baukasten/ausgabe/ergebnis_NMC.json::ctx.z_deckel_o", "cad/baukasten/ausgabe/ergebnis_NMC.json::hoehe_max_mm", "cad/baukasten/ausgabe/ergebnis_NMC.json::laenge_mm", "pm/bauteile/stueckliste_LFP.json::summen.masse_stueckliste_kg", "pm/bauteile/stueckliste_NMC.json::summen.masse_stueckliste_kg"]
---
# REQ-P07

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

Bauraum (L × B × H) und Masse

- Wert (Lastenheft): L ≤ 2400 mm (Autor, Freigaberunde 2026-11-23); B = 1430 mm (ENT-030, Autor 2026-11-17); H ≤ 130 mm im Zellbereich, Dom Schaltbox ≤ 250 mm; Masse LFP ≤ 528 kg, NMC ≤ 370 kg (Startwerte als Ziel)
- Priorität: Muss
- Vom Autor bestätigt: ja

## Verifikation (V-Modell-Matrix)

- Methode: I (A Analyse, S Simulation, I Inspektion, T Test, R Review)
- Ebene: System
- Kriterium: B <= 1430 mm [Autor (Freigaberunde 2026-11-23)]<br>L <= 2400 mm [Autor (Freigaberunde 2026-11-23)]<br>H <= 130 mm [Autor (Freigaberunde 2026-11-23)]<br>H_dom <= 250 mm [Autor (Freigaberunde 2026-11-23)]<br>Masse LFP <= 528 kg [Autor (Freigaberunde 2026-11-23)]<br>Masse NMC <= 370 kg [Autor (Freigaberunde 2026-11-23)]
- Ist-Wert: [B] LFP B = 1430 [cad/baukasten/ausgabe/ergebnis_LFP.json :: breite_mm]; NMC B = 1430 [cad/baukasten/ausgabe/ergebnis_NMC.json :: breite_mm]; [L] LFP L = 2373 [cad/baukasten/ausgabe/ergebnis_LFP.json :: laenge_mm]; NMC L = 2273 [cad/baukasten/ausgabe/ergebnis_NMC.json :: laenge_mm]; [H] LFP H = 117 [cad/baukasten/ausgabe/ergebnis_LFP.json :: ctx.z_deckel_o]; NMC H = 111 [cad/baukasten/ausgabe/ergebnis_NMC.json :: ctx.z_deckel_o]; [H_dom] LFP H_dom = 244.8 [cad/baukasten/ausgabe/ergebnis_LFP.json :: hoehe_max_mm]; NMC H_dom = 227.8 [cad/baukasten/ausgabe/ergebnis_NMC.json :: hoehe_max_mm]; [Masse LFP] LFP Masse = 626.8 [pm/bauteile/stueckliste_LFP.json :: summen.masse_stueckliste_kg]; [Masse NMC] NMC Masse = 486.4 [pm/bauteile/stueckliste_NMC.json :: summen.masse_stueckliste_kg]
- Bewertung: **verfehlt (Kriterium Annahme, Autor offen)**
- Matrix: [[Dokument/06_verifikationsplan]] · Lastenheft: [[Dokument/01_lastenheft]] · Verfolgung: [[Dokument/03_anforderungsverfolgung]]

## Nachweisdateien
- [[Nachweis/cad_baukasten_ausgabe_ergebnis_LFP.json|cad/baukasten/ausgabe/ergebnis_LFP.json]]
- [[Nachweis/cad_baukasten_ausgabe_ergebnis_NMC.json|cad/baukasten/ausgabe/ergebnis_NMC.json]]
- [[Nachweis/pm_bauteile_stueckliste_LFP.json|pm/bauteile/stueckliste_LFP.json]]
- [[Nachweis/pm_bauteile_stueckliste_NMC.json|pm/bauteile/stueckliste_NMC.json]]

## Vorgänge
- [[Vorgang/V1|V1]] – Lastenheft-Werte REQ-P01..P08 vorschlagen (Fahrzeug, kWh, Spannung, Leistung, Laden, Chemie, Bauraum, Temperatur)
- [[Vorgang/V2|V2]] – Freigabe Lastenheft durch Autor
- [[Vorgang/G4|G4]] – Pack: Zellanordnung, Querträger, Kühlplatte, Deckel

## Bauteile
- [[Bauteil/BT-000|BT-000]]
- [[Bauteil/BT-210|BT-210]]
- [[Bauteil/BT-500|BT-500]]
- [[Bauteil/BT-510|BT-510]]
