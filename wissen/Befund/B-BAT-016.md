---
typ: befund
tags: ["befund"]
---
# B-BAT-016

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

B-BAT-016 (2026-11-17) Detailmodell Innenaufbau fertig; 4680-Wickel ragte über den Becher (Opus-Fehler im Kern)

Quelle: [[Dokument/BEFUNDE]]

## Vorgänge
- [[Vorgang/G2|G2]] – Parametrische Zelle FreeCAD (liest parameter.json)

## Text aus BEFUNDE.md

- Sonnet (cad/zelle/AUFTRAG_DETAIL.md, 42 min, CPU): FreeCAD-Detailmodelle beider Zellen, 7 Schnitt-/Explosionsbilder, Neulauf G1/C0b mit 1430 mm (LFP A passt, Reserve L 16 / B 8 mm; nötig 203,9 Wh/L; NMC 1260 Plätze).
- LFP-Stapel 12,476 mm in 13,4 mm (Rest 0,92 mm) – wie erwartet. Bild LFP_schnitt angesehen: Schichtfolge, Fahnen, Stromschiene, Halter, O-Ring, Isolationsbeutel erkennbar und beschriftet.
- **Verfehlt:** 4680-Wickel Außenradius 23,75 mm > 22,6 mm. Ursache 1 (Opus): ENT-074 Kern Ø 14 mm nur aus Kathodenfläche abgeleitet; mit allen Bändern (1477 mm²) Kern ≤ 12,75 mm → ENT-074 auf 12,5 mm korrigiert. Ursache 2 (Modell): feste Steigung 0,45 mm auch dort, wo nur noch Anode/Separator liegt → flächentreue Spirale. **Behoben 12:30:** Außenradius 22,565 mm in 22,60 mm (0,035 mm Luft), Kathode 36,7 Windungen. Rest: erste Windung ragt 0,45 mm in den Kern (Band um die Spirallinie zentriert), Startversatz der Bänder Annahme 0.
- Offen: Lesart Fahnenmaße (LFP 27,1/9 und 20,5/7 mm; 4680 2,5/5 und 7,5/2,5 mm), Isolierrand und Klebeband nicht modelliert. Vorgang: [G2]
