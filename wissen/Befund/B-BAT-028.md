---
typ: befund
tags: ["befund"]
---
# B-BAT-028

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

B-BAT-028 (2026-11-18) SL2 Stückliste je Variante: Massen stimmen (±1,3 %), fünf Bauteile fehlten im Baum, vier Zählwidersprüche CAD/E1

Quelle: [[Dokument/BEFUNDE]]

## Vorgänge
- [[Vorgang/SL2|SL2]] – Stückliste fortschreiben nach Auslegung (Mengen, Kauf/Eigen, Werkstoffe, Bezugsquellen)

## Text aus BEFUNDE.md

- `docs/13_stueckliste_<V>.md` v0.2: je 38 Positionen; LFP 619 kg (+1,2 % gegen pack_massen), NMC 471 kg (−0,4 %); NMC über G4-Band 390–430 kg. Kostenspalten leer, Gerüst `pm/kosten/`.
- Baum erweitert (Opus): BT-260 Verguss (NMC), BT-361 FPC-Halter, BT-440 Pol-Anschlusslaschen, BT-721 Trennbrücke, BT-722 Servicedeckel (LFP), BT-720 bauform (ENT-150 umgehängt). CMU → BT-320, FPC → BT-360 bestätigt. Dichtungen bleiben in BT-520/BT-710.
- **Zählwidersprüche, nach E2 v1.1 klären:**
  - LFP-Reihenverbinder: CAD 130, E1 249. Bei 250 Zellen in Reihe sind 249 nötig.
  - NMC-Abgriffe: 868 gegen 1736. Das ist eine Definitionsfrage: je Gruppe 218 Spannungsabgriffe, je Zelle 2 Pole.
  - NMC-Gruppenverbinder: 217 gegen 216. Möglicherweise ist die Endlasche mitgezählt.
  - HV-Leitung: CAD 0,5/0,4 kg, nur Cu, gegen E1 1,8/1,2 kg. Die E1-Werte sind eine Schätzung mit Isolierung. Es gilt CAD plus Isolierung.
- Vorgang: [SL2]
