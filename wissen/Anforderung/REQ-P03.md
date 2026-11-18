---
typ: anforderung
tags: ["anforderung"]
---
# REQ-P03

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

Systemspannung (Nenn, min, max)

Lastenheft: [[docs/01_lastenheft]]

## Vorgänge
- [[wissen/Vorgang/V1|V1]] – Lastenheft-Werte REQ-P01..P08 vorschlagen (Fahrzeug, kWh, Spannung, Leistung, Laden, Chemie, Bauraum, Temperatur)
- [[wissen/Vorgang/V2|V2]] – Freigabe Lastenheft durch Autor
- [[wissen/Vorgang/G3|G3]] – Verschaltung sS/pP aus Spannung und Energie festlegen (ENT)
- [[wissen/Vorgang/E4|E4]] – Schaltungsmodell ngspice/Modelica: Vorladung, Kurzschluss
