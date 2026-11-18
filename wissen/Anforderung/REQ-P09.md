---
typ: anforderung
tags: ["anforderung"]
---
# REQ-P09

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

max. Zelltemperatur und Spreizung

Lastenheft: [[docs/01_lastenheft]]

## Vorgänge
- [[wissen/Vorgang/V1|V1]] – Lastenheft-Werte REQ-P01..P08 vorschlagen (Fahrzeug, kWh, Spannung, Leistung, Laden, Chemie, Bauraum, Temperatur)
- [[wissen/Vorgang/V2|V2]] – Freigabe Lastenheft durch Autor
- [[wissen/Vorgang/K0|K0]] – Kühlart Luft gegen Wasser (1D-Wärmebilanz Schnellladen, W16), Entscheidung ENT
- [[wissen/Vorgang/K1|K1]] – ERWARTUNG Kühlung Schnellladen (max. Zelltemperatur, Spreizung)
- [[wissen/Vorgang/K2|K2]] – Kanalverteilung 1D (Verteiler, Druckverlust)
- [[wissen/Vorgang/K3|K3]] – Elmer: Zelle -> Paste -> Platte, Schnellladefall
- [[wissen/Vorgang/K4|K4]] – FluidX3D: Strömung Kühlplatte bzw. Luftkanal (Gegenprüfung 1D)
- [[wissen/Vorgang/K5|K5]] – Deutung Kühlung, Abgleich Erwartung, Änderungsvorschlag
- [[wissen/Vorgang/U4|U4]] – Optimierung Kühlplatte/Ladeprofil mit Ersatzmodell, Bestwerte mit Elmer bestätigen
