---
typ: anforderung
tags: ["anforderung"]
---
# REQ-D11

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

Jede Entscheidung als Akte an Bauteil und Merkmal gebunden; CAD-Maße nur aus diesen Akten

Lastenheft: [[docs/01_lastenheft]]

## Vorgänge
- [[wissen/Vorgang/R5|R5]] – Werkzeugwahl festlegen (ENT): Zellmodell, Packmodell, Schaltung
- [[wissen/Vorgang/G1|G1]] – Zellmaße als ENT-Akten (aus W03/W08/P01, sonst Annahme)
- [[wissen/Vorgang/G2|G2]] – Parametrische Zelle FreeCAD (liest parameter.json)
- [[wissen/Vorgang/G4|G4]] – Pack: Zellanordnung, Querträger, Kühlplatte, Deckel
- [[wissen/Vorgang/SL2|SL2]] – Stückliste fortschreiben nach Auslegung (Mengen, Kauf/Eigen, Werkstoffe, Bezugsquellen)
