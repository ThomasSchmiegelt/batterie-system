| Dok.-Nr. | Auftrag K0-R | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Temperaturbilder K0 hochwertig neu rendern (Blender Cycles, CPU) | Ersteller | Claude Opus (KI) | Prüfer | Opus (jedes Bild ansehen) |

> **KI-generiert.** Auftrag von Opus an Sonnet (`sonnet-umsetzer`), 2026-11-17. Autor: „mach die renderings neu“. Mangel der ersten Fassung (Opus): Workbench flach ohne Schattierung, LFP als schräger Streifen kaum lesbar, NMC ohne Gehäuse-Bezug.

## Ziel
`render_cycles.py` (Blender 4.0.2 `$BLENDER -b -P`, Cycles **CPU**, keine GPU, `nice -n 10`; ohne OpenImageDenoise → genug Samples, z. B. 128, oder Blender-eigener NLM-Denoiser falls vorhanden): wiederverwendbar mit Argumenten (VTU-Pfad, Variante, Schnitt, Zeit, Ausgabe), damit K1 es nutzen kann. Knotentemperaturen aus den Elmer-VTU (`elmer/` Link nach cae_projekte) als Vertex-Farbe, Farbkarte und Skala wie bisher (einheitlich 25–55 °C, 45 °C markiert).
- **Optik wie die Zellrender** in `cad/zelle/render_blender.py` / `render_detail.py` (Licht, Hintergrund, Kamera-Stil übernehmen): Emission+Diffus-Mischung, damit Farben ablesbar bleiben (Farbe darf durch Licht nicht verfälscht werden – Farbskala muss stimmen, Prüfung: Pixelfarbe an einer Stelle bekannter Temperatur gegen Skala).
- **LFP:** Zelle in **echter Proportion** (keine Überhöhung im Hauptbild), Blick schräg von vorn-oben auf die große Seitenfläche, halbe Dicke weggeschnitten, Kühlplatte unten als graue Platte angedeutet (Annahme-Darstellung), zusätzlich Ausschnitt-Lupe der Schnittfläche. Pole oben.
- **NMC:** Viertelschnitt, Kamera leicht von oben, Becher als dünne halbtransparente Hülle oder Schnittkante, Kühlplatte unten angedeutet; K2 mit Kühlband am Mantel angedeutet.
- Je Fall (LFP K1 L2, NMC K1 L2, NMC K2 L2) t = 0, 300, 600, 900, 1200 s und MP4 (≥ 41 Frames; bei Rechenzeit Frames mit geringeren Samples). Bilder `bilder/cycles_<Fall>_t<s>.png`, Filme `bilder/cycles_<Fall>.mp4`; zusätzlich eine Bildtafel `bilder/tafel_L2.png` (3 Zeilen Fälle × 5 Zeitpunkte, gemeinsame Skala).
- Beschriftung über matplotlib (wie bisher): Titel, Zeit, T_max, Vorgabe REQ-P09, „Annahmen: Kühlmittel 25 °C, h 500“, KI-generiert.
- Lesehilfe `bilder/render_lesehilfe.md` ergänzen. Alte Workbench-Bilder behalten (nicht löschen), in docs/16 aber nur die neuen zeigen (`bilder.py`: render_* ausblenden oder als „Vorstufe“ markieren). Bericht nicht anfassen.
## Abbruch und Rückgabe
Gesamt ≤ 60 min, ein Bild ≤ 3 min. Parallel läuft K1 (Elmer, CPU) unter sim/kuehlung/k1_schnellladen – nicht anfassen. Jedes neue Bild selbst ansehen. Rückgabe ≤ 8 Zeilen, Farbprüfung nennen.
