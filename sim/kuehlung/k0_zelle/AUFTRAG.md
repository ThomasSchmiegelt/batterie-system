| Dok.-Nr. | Auftrag K0 | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Wärmesimulation einer Zelle je Variante (Elmer, homogenisierter Kern) | Ersteller | Claude Opus (KI) | Prüfer | Opus (Rohdaten) |

> **KI-generiert.** Auftrag von Opus an Sonnet (`sonnet-umsetzer`), 2026-11-17. Autor: „vielleicht können wir die modelle für eine thermo smulation nutzen?“. Eingaben `eingaben.json`, Erwartung `ERWARTUNG.md` (nicht ändern).

## Ziel
1. `geometrie.py` (gmsh, CLI `/usr/bin/gmsh` oder Python über `.venv/bin/gmsh`): Netz je Variante aus den Maßen in `cad/zelle/entwurf/parameter_<V>_entwurf.json` (keine harte Zahl): Kern (Körper 1), Gehäuse/Endzonen (Körper 2), bei NMC Kernloch (Körper 3, Luft k = 0,026 Annahme). Randflächen benannt (Boden, Mantel, Rest). Netz fein genug, dass Verdoppelung T_max um < 0,5 K ändert (Netzstudie, 2 Stufen).
2. `elmer/` Eingabedateien (ElmerGrid → ElmerSolver, HeatSolver): orthotrope Leitfähigkeit im Kern (LFP: Ebene = Länge/Höhe, quer = Dicke; NMC in Zylinderkoordinaten: axial, radial – als Tensor in kartesischen Koordinaten richtig drehen oder radial/axial über Hauptachsen; Methode dokumentieren). Wärmequelle Q/V im Kern. Fälle: LFP K1 × {L1, L2}, NMC K1 × {L1, L2}, NMC K2 × {L1, L2}. Leitfähigkeit LFP: W18 (Hauptfall) und Schichtmischung (Vergleich). L2 transient 1200 s, Schritt ≤ 10 s.
3. `auswertung.py`: T_max, T_min, ΔT, Energiebilanz (stationär), Verlauf T_max(t) für L2; Empfindlichkeit L1 über die Bänder R, h, Leitfähigkeit (einzeln).
4. Bilder (Regeln: Zielbereich + Lesehilfe): `temperatur_<V>_<Fall>.png` (Temperaturfeld im Schnitt, Farbskala in °C, Zielgrenze 45 °C als Konturlinie), `verlauf_L2.png` (T_max(t) beider Varianten, Ziel 45 °C als Linie, ΔT als zweite Achse mit Ziel 5 K), `empfindlichkeit_K0.png` (Tornado ΔT). Wenn möglich zusätzlich ein 3D-Temperaturbild über ParaView/pvpython (falls installiert, sonst matplotlib). `k0_lesehilfe.md`.
5. `ergebnis.json`, `ERGEBNIS.md` (Kopf, Tabellen, **Abgleich ERWARTUNG Punkt für Punkt**, keine Deutung), `ERGEBNIS_kurz.txt`, `praesentation/bausteine/K0.md` (Kernaussage „(Opus)“). Danach `pm/plan/bilder.py` (Zuordnung k0_zelle → K0).
## Abbruch und Rückgabe
CPU only (GPU geteilt), ein Lauf ≤ 10 min, gesamt ≤ 60 min. Läuft parallel zu einem Blender-Auftrag in cad/zelle/ – diese Dateien nicht anfassen. Nicht ändern: Akten, eingaben.json, ERWARTUNG.md. Rückgabe ≤ 15 Zeilen. **→ OPUS**: verfehlte Erwartung, Energiebilanz > 2 %, fehlende Eingabe.
