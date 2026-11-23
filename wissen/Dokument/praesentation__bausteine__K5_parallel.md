---
typ: dokument
datei: "praesentation/bausteine/K5_parallel.md"
tags: ["dokument", "kopie"]
---
# K5_parallel

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

- Kopie von `praesentation/bausteine/K5_parallel.md` (Quelle im Repo, hier nur Lesekopie)

## Inhalt

# Folienbaustein K5 – gruppierte Parallelführung (KI-generiert, Entwurf)
**Kernaussage:** Zwei parallele Gruppen aus je 4 Bahnen mit außenliegendem Verteilerrohr Ø 25 verteilen auf ±2,0 % gleichmäßig bei 0,17 bar (dreifacher Durchfluss); die LFP-Zellspreizung beim Schnellladen beträgt wie gebaut (V4p) 9,6 K, NMC 2,6 K (Ziel 5 K). 7,6 K gelten nur mit Gegenlauf, nicht im CAD (Verbesserungsvorschlag).
**Bild (Zielband beschriftet):** sim/kuehlung/k5_parallel/verteilung.png (Band ±10 %), dp_durchfluss.png (Linie 0,22 bar), k4_vergleich_V0_V3_V4.png (Band 33–37 °C)
**Zahlen:** siehe Abschnitt „Stand aus Ergebnisdateien“ unten (Quellen ergebnis_verteiler.json und elmer_*_V4p/ergebnis.json). Einzelkanal-Z-Verteiler verworfen (Quelle ergebnis_verteiler.json, status_einzelkanal).

<!-- AUTO-B5 Anfang -->
## Stand aus Ergebnisdateien (Skript praesentation/bausteine_aktualisieren.py, 2026-11-23, KI-generiert, Entwurf)
- Verteilung (Quelle sim/kuehlung/k5_parallel/ergebnis_verteiler.json, gruppen.faelle.k2_d25_x3): max. Abweichung 2,0 %, Δp 0,171 bar; bei einfachem Durchfluss (k2_d25_x1) 0,053 bar; Mäander nachgerechnet (einfacher Durchfluss) 0,215 bar.
- LFP V4p: T_max 35,57 °C, Spreizung 9,57 K (sim/kuehlung/k3_gesamt/elmer_LFP_P0_V4p/ergebnis.json); NMC V4p: 30,60 °C, 2,57 K.
- Maßgeblich ist V4p wie gebaut. 7,6 K (V4, sim/kuehlung/k3_gesamt/elmer_LFP_P0_V4/ergebnis.json) gilt nur mit Gegenlauf, nicht im CAD (Verbesserungsvorschlag). Die Angabe 0,70 bar entfällt (in keiner Ergebnisdatei).
<!-- AUTO-B5 Ende -->

