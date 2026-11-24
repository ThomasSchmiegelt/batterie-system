---
typ: anforderung
gruppe: "REQ-P"
methode: "S"
ebene: "Subsystem"
bewertung: "verfehlt (Kriterium Annahme, Autor offen)"
tags: ["anforderung", "bewertung/verfehlt"]
verifiziert_durch: ["sim/kuehlung/k3_gesamt/elmer_LFP_P0_V4p/ergebnis.json::T_max_Zellblock_C", "sim/kuehlung/k3_gesamt/elmer_LFP_P0_V4p/ergebnis.json::dT_Zellblock_K", "sim/kuehlung/k3_gesamt/elmer_NMC_P4_V4p/ergebnis.json::T_max_Zellblock_C", "sim/kuehlung/k3_gesamt/elmer_NMC_P4_V4p/ergebnis.json::dT_Zellblock_K"]
---
# REQ-P09

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

max. Zelltemperatur und Spreizung zwischen den Zellen

- Wert (Lastenheft): T_max ≤ 45 °C, Spreizung ΔT ≤ 5 K zwischen den Zellen (Autor, Freigaberunde 2026-11-23; Nachweis neu auswerten, Schleife 2)
- Priorität: Muss
- Vom Autor bestätigt: ja

## Verifikation (V-Modell-Matrix)

- Methode: S (A Analyse, S Simulation, I Inspektion, T Test, R Review)
- Ebene: Subsystem
- Kriterium: T_max <= 45 °C [Autor (Freigaberunde 2026-11-23)]<br>Spreizung <= 5 K [Autor (Freigaberunde 2026-11-23)]
- Ist-Wert: [T_max] LFP T_max = 35.57 [sim/kuehlung/k3_gesamt/elmer_LFP_P0_V4p/ergebnis.json :: T_max_Zellblock_C]; NMC T_max = 30.6 [sim/kuehlung/k3_gesamt/elmer_NMC_P4_V4p/ergebnis.json :: T_max_Zellblock_C]; [Spreizung] LFP Spreizung = 9.573 [sim/kuehlung/k3_gesamt/elmer_LFP_P0_V4p/ergebnis.json :: dT_Zellblock_K]; NMC Spreizung = 2.574 [sim/kuehlung/k3_gesamt/elmer_NMC_P4_V4p/ergebnis.json :: dT_Zellblock_K]
- Bewertung: **verfehlt (Kriterium Annahme, Autor offen)**
- Matrix: [[Dokument/06_verifikationsplan]] · Lastenheft: [[Dokument/01_lastenheft]] · Verfolgung: [[Dokument/03_anforderungsverfolgung]]

## Nachweisdateien
- [[Nachweis/sim_kuehlung_k3_gesamt_elmer_LFP_P0_V4p_ergebnis.json|sim/kuehlung/k3_gesamt/elmer_LFP_P0_V4p/ergebnis.json]]
- [[Nachweis/sim_kuehlung_k3_gesamt_elmer_NMC_P4_V4p_ergebnis.json|sim/kuehlung/k3_gesamt/elmer_NMC_P4_V4p/ergebnis.json]]

## Vorgänge
- [[Vorgang/V1|V1]] – Lastenheft-Werte REQ-P01..P08 vorschlagen (Fahrzeug, kWh, Spannung, Leistung, Laden, Chemie, Bauraum, Temperatur)
- [[Vorgang/V2|V2]] – Freigabe Lastenheft durch Autor
- [[Vorgang/K0|K0]] – Kühlart Luft gegen Wasser (1D-Wärmebilanz Schnellladen, W16), Entscheidung ENT
- [[Vorgang/K1|K1]] – ERWARTUNG Kühlung Schnellladen (max. Zelltemperatur, Spreizung)
- [[Vorgang/K2|K2]] – Kanalverteilung 1D (Verteiler, Druckverlust)
- [[Vorgang/K3|K3]] – Elmer: Zelle -> Paste -> Platte, Schnellladefall
- [[Vorgang/K4|K4]] – FluidX3D: Strömung Kühlplatte bzw. Luftkanal (Gegenprüfung 1D)
- [[Vorgang/K5|K5]] – Deutung Kühlung, Abgleich Erwartung, Änderungsvorschlag
- [[Vorgang/U4|U4]] – Optimierung Kühlplatte/Ladeprofil mit Ersatzmodell, Bestwerte mit Elmer bestätigen

## Bauteile
- [[Bauteil/BT-230|BT-230]]
- [[Bauteil/BT-330|BT-330]]
- [[Bauteil/BT-600|BT-600]]
- [[Bauteil/BT-610|BT-610]]
- [[Bauteil/BT-620|BT-620]]
- [[Bauteil/BT-640|BT-640]]
- [[Bauteil/BT-661|BT-661]]
- [[Bauteil/BT-662|BT-662]]
- [[Bauteil/BT-663|BT-663]]
- [[Bauteil/BT-664|BT-664]]
- [[Bauteil/BT-665|BT-665]]
