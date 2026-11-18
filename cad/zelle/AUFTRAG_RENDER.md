| Dok.-Nr. | Auftrag G2-R | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Zellen in Blender rendern (Entwurf) | Ersteller | Claude Opus (KI) | Prüfer | Opus (Bilder ansehen) |

> **KI-generiert.** Auftrag von Opus an Sonnet (`sonnet-umsetzer`), 2026-11-17. Autor: „kannst du sie vtl. auch in blender rendern“.

## Ziel
1. `cad/zelle/export_mesh.py` (freecadcmd, wie zelle.py per Umgebungsvariable): aus `entwurf/zelle_<V>.FCStd` je Körper (Gehäuse, Pole) eine STL/OBJ in `entwurf/render/` (mm, feine Tessellierung, Rundzelle glatt).
2. `cad/zelle/render_blender.py` (`$BLENDER -b -P …`, Blender 4.0): beide Zellen nebeneinander, **maßstäblich zueinander**, Werkstoff-Anmutung: LFP-Gehäuse Aluminium gebürstet mit blauer PET-Folie (ENT-023), 4680 Stahlbecher vernickelt (ENT-028); Pole Kupfer/Aluminium; neutraler Studio-Hintergrund, 3-Punkt-Licht, leichte Schatten. Kamera isometrisch-schräg. Zusätzlich je Zelle eine Einzelansicht. Maßstabsleiste (z. B. 100-mm-Balken) im Bild. Kleiner Text unten: „Entwurf – Akten vorgeschlagen, KI-generiert“. 
   Render: **Cycles auf CPU** (GPU teilt sich mit ollama; nicht GPU), 1600 × 900, Samples so, dass je Bild ≤ 5 min. Falls Cycles-CPU zu langsam: EEVEE.
3. Ausgaben `cad/zelle/entwurf/render/`: `zellen_vergleich.png`, `zelle_LFP_render.png`, `zelle_NMC_render.png`, `render_lesehilfe.md` (3–5 Sätze je Bild; Maßstab, was Annahme ist: Polmaße, Farben = Anmutung, nicht Messung). `pm/plan/bilder.py` laufen lassen (Zuordnung render → G2).
## Abbruch und Rückgabe
Abbruch nach 30 min. Nicht ändern: Akten, parameter*.json, zelle.py-Maße. Alle Bilder selbst ansehen. Rückgabe ≤ 8 Zeilen.
