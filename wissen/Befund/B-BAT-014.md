---
typ: befund
tags: ["befund"]
---
# B-BAT-014

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

B-BAT-014 (2026-11-17) G1: Zellmaße je Variante als Akten (ENT-014…029, vorgeschlagen)

Quelle: [[Dokument/BEFUNDE]]

## Vorgänge
- [[Vorgang/G1|G1]] – Zellmaße als ENT-Akten (aus W03/W08/P01, sonst Annahme)
- [[Vorgang/G2|G2]] – Parametrische Zelle FreeCAD (liest parameter.json)

## Text aus BEFUNDE.md

- Autor: „ja mach“ (Zellmaße als Akten vorschlagen).
- LFP [LFP]: Blade-Querschnitt verkürzt, 660 × 90 × 14 mm, 92,4 Ah, 3,2 V, ~1850 g (Annahme: Masse ∝ Ah), Z-gefalteter Einzelstapel mit 38 Kathodenlagen, Gehäuse Aluminium (PET-isoliert), Wand 0,3 mm. Länge ∝ Ah ist **Annahme** (Polzonen vernachlässigt).
- NMC [NMC]: 4680 Ø 46 × 80 mm, Wickel (tabless), Stahl vernickelt (Quelle: „presumably“), Wand 0,4 mm.
- Belege W20 (Zerlegung, Tabelle 1 und Fließtext, von Opus am Rohtext gelesen), G1-Rechnung. pm.py pruefe: 29 Akten, 0 Fehler.
- G2-Entwurf fertig (cad/zelle/, FreeCAD 1.1.4 headless): LFP 0,8316 L, 355,6 Wh/L; 4680 0,1330 L, 643,6 Wh/L (Opus nachgerechnet, = W20). Parametertest Länge 700 mm ohne Codeänderung. Bilder angesehen: plausibel; Polmaße Annahme (LFP Ø 10 mm auf 14 mm Stirnfläche, eng; W20 nennt Gewindepole seitlich → Polform später prüfen). Innenaufbau nicht modelliert. Standardlauf bricht ohne freigegebene Akten mit FEHLT ab (gewollt). Vorgang: [G1] [G2]
