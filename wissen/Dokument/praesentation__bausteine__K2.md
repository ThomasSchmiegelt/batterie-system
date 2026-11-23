---
typ: dokument
datei: "praesentation/bausteine/K2.md"
tags: ["dokument", "kopie"]
---
# K2

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

- Kopie von `praesentation/bausteine/K2.md` (Quelle im Repo, hier nur Lesekopie)

## Inhalt

> **KI-generiert** (Claude Sonnet, 2026-11-17), Entwurf. Folienbaustein Vorgang K2 (Kühlplatten: Hydraulik und Wärmeübergang).

# Kühlplatte: Druck kein Problem, Wärmeübergang ist die Grenze
**Kernaussage: Die Platten brauchen kaum Pumpendruck (LFP höchstens 0.004 bar, NMC höchstens 0.002 bar bei ≤ 0,5 bar Ziel), aber die laminare Strömung in den 5-mm-Kanälen liefert nur h ≈ 291 bis 316 W/(m²K) statt der angenommenen 500 (Entwurf, Opus prüft).**

**Bild:** sim/kuehlung/k2_kuehlplatte/durchfluss_druck.png (Zielband dp ≤ 0,5 bar und h ≥ 500 beschriftet), platte_LFP.png, platte_NMC.png

**Zahlen** (Quelle sim/kuehlung/k2_kuehlplatte/ergebnis.json):
- Durchfluss bei ΔT 5 K: LFP 46.7 L/min, NMC (P4) 20.1 L/min
- Re 61 bis 188 (LFP), 27 bis 81 (NMC P4): laminar
- Beste Variante nach h: LFP 20 mm laengs, h 316; NMC 20 mm laengs, h 291; keine erreicht h ≥ 500
- Annahmen: Kühlmittel-k 0,40 (neu, Sonnet), Zuschlag 30 %, gleichmäßige Verteilung, Lehrbuchkorrelationen; Entwurf, noch nicht von Opus geprüft

- Nachtrag (U auf Grundfläche, Quelle sim/kuehlung/k2_kuehlplatte/ergebnis_nachtrag.json): Auswahl LFP 4 x 5 mm, U 595, 0.42 W; NMC P4 U 565, 0.08 W (Bild nachtrag_U_leistung.png, Zielband U ≥ 500)

*KI-generiert, Entwurf.*

