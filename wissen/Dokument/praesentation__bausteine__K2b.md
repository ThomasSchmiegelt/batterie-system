---
typ: dokument
datei: "praesentation/bausteine/K2b.md"
tags: ["dokument", "kopie"]
---
# K2b

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

- Kopie von `praesentation/bausteine/K2b.md` (Quelle im Repo, hier nur Lesekopie)

## Inhalt

> **KI-generiert** (Claude Sonnet, 2026-11-19), Entwurf. Folienbaustein Vorgang K2b (Blech-Kühlplatte 1/4/1 mm mit Mäander).

# Dünne Blechplatte mit Mäander erreicht das Wärmeziel knapp
**Kernaussage: Eine Blechplatte 1/4/1 mm mit 4 quer geführten Bahnen aus 6-mm-Teilkanälen erreicht U ≥ 500 W/(m²K) bei nur 0.032 bar (LFP), die Marge ist klein (Entwurf, Opus prüft).**

**Bild:** sim/kuehlung/k2_kuehlplatte/k2b_U_dp.png (Zielband U ≥ 500, Δp ≤ 0,5 bar beschriftet)

**Zahlen** (Quelle sim/kuehlung/k2_kuehlplatte/ergebnis_k2b.json):
- LFP Vorschlag: U 522, Δp 0.032 bar, P_hyd 1.21 W, Masse beider Platten 49.1 kg
- NMC Vorschlag: U 514, Δp 0.028 bar, Masse 47.0 kg
- Erwartungspunkt 3 (n 4, w 8 längs, U ≈ 550) verfehlt: U 487
- Annahmen: ζ 1,5 je Umlenkung, kein Kontaktwiderstand, Lehrbuchkorrelationen

*KI-generiert, Entwurf.*

