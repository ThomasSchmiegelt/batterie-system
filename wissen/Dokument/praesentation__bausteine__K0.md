---
typ: dokument
datei: "praesentation/bausteine/K0.md"
tags: ["dokument", "kopie"]
---
# K0

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

- Kopie von `praesentation/bausteine/K0.md` (Quelle im Repo, hier nur Lesekopie)

## Inhalt

> **KI-generiert** (Claude Sonnet, 2026-11-17), Entwurf. Folienbaustein Vorgang K0 (Wärmesimulation Zelle).

# Zelltemperatur beim Schnellladen
**Kernaussage: Beim Schnellladen 10→80 % in 20 min bleibt die LFP-Zelle mit Bodenkühlung unter 45 °C (43.1 °C), die 4680-Zelle nicht (53.6 °C); die Spreizung 5 K halten beide nicht ein (LFP 10.6 K, NMC 16.0 K) (Opus).**

**Bild:** sim/kuehlung/k0_zelle/verlauf_L2.png (Vorgabe 45 °C und 5 K beschriftet, REQ-P09); gerendert sim/kuehlung/k0_zelle/bilder/render_LFP_K1_L2_t1200s.png und render_NMC_K1_L2_t1200s.png, Video bilder/verlauf_*.mp4

**Zahlen** (Quelle sim/kuehlung/k0_zelle/ergebnis.json):
- L1 (1C): LFP T_max 30.1 °C, ΔT 3.0 K; NMC 33.5 °C, 4.8 K
- L2: LFP 43.1 °C / 10.6 K; NMC K1 53.6 °C / 16.0 K; NMC K2 (nur Vergleich) 49.9 °C / 18.1 K
- Annahmen: Innenwiderstand, h = 500 W/(m²K), 25 °C Kühlmittel; Entwurf, noch nicht von Opus geprüft

*KI-generiert, Entwurf.*

