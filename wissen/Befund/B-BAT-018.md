---
typ: befund
tags: ["befund"]
---
# B-BAT-018

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

B-BAT-018 (2026-11-17) K0 Wärme Einzelzelle: Schnellladen verfehlt 5 K bei beiden, 45 °C bei NMC

Quelle: [[Dokument/BEFUNDE]]

## Vorgänge
- [[Vorgang/K0|K0]] – Kühlart Luft gegen Wasser (1D-Wärmebilanz Schnellladen, W16), Entscheidung ENT

## Text aus BEFUNDE.md

- Elmer, CPU, Bilanz < 0,001 %, Netz 0,017 K. 1C: LFP 30,1 °C/3,0 K, NMC 33,5 °C/4,8 K (Vorgabe erfüllt). 2,1C 20 min: LFP 43,1 °C/10,6 K, NMC Boden 53,6 °C/16,0 K, NMC Mantel 49,9 °C/18,1 K.
- Verfehlte Erwartung NMC: Opus-Fehler (Filmwiderstand am 16,6-cm²-Boden vergessen, 18 K bei 2,1C). DEUTUNG.md.
- pvbatch ohne Python-Modul → Blender-Workbench-Render und 3 MP4. VTU (595 MB) nach /home/cae/cae_projekte/batterie/k0_zelle/elmer verschoben (Link).
- Offen beim Autor: Umgang mit 5 K beim Schnellladen; Gehäuse-c/Dichte fehlt in eingaben.json (ganze Masse im Kern). Bericht: 683/644-kg-Zielband zwischen empfindlichkeit.png und kriterien.png uneinheitlich (verschiedene Bezugsfälle). Vorgang: [K0]
