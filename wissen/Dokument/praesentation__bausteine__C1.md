---
typ: dokument
datei: "praesentation/bausteine/C1.md"
tags: ["dokument", "kopie"]
---
# C1

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

- Kopie von `praesentation/bausteine/C1.md` (Quelle im Repo, hier nur Lesekopie)

## Inhalt

> **KI-generiert** (Claude Sonnet, 2026-11-17), Entwurf. Folienbaustein Vorgang C1 (Zellmodell PyBaMM).

# Elektrochemie bestätigt die Wärmeannahme nur für NMC
**Kernaussage: Das PyBaMM-Modell bestätigt die I²R-Wärme der NMC-Zelle (Mittel 6,9 W gegen 6,7 W Annahme), für die LFP-Zelle liegt sie mit 32,8 W unter dem Band (Annahme 55 W); die NMC-Zelle erreicht 80 % erst nach 36 min statt 20 min.**

**Bild:** sim/chemie/c1_zellmodell/waerme_NMC.png und waerme_LFP.png (Zielband Faktor 1,5 beschriftet), dcir.png, ladekurve.png

**Zahlen** (Quelle sim/chemie/c1_zellmodell/ergebnis_zahlen.json):
- Kapazität: LFP 93,08 Ah (Fläche auf 92,4 Ah skaliert; mit Akten-Fläche 48,63 Ah), NMC 23,19 Ah
- Wärme Schnellladen: NMC 6,92 W (bis CV), LFP 32,8 W (nur I·ΔU)
- DCIR 25 °C: LFP 0,76 mΩ, NMC 6,40 mΩ
- Annahmen: Parametersätze Prada2013/Chen2020, Fläche beidseitig, LFP isotherm; Entwurf, nicht von Opus geprüft

*KI-generiert, Entwurf.*

