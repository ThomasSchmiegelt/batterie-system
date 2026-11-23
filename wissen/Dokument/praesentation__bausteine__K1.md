---
typ: dokument
datei: "praesentation/bausteine/K1.md"
tags: ["dokument", "kopie"]
---
# K1

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

- Kopie von `praesentation/bausteine/K1.md` (Quelle im Repo, hier nur Lesekopie)

## Inhalt

> **KI-generiert** (Claude Sonnet, 2026-11-17), Entwurf. Folienbaustein Vorgang K1 (Schnellladen: Ladeprofile, Kühlung, Begrenzung), mit Nachtrag.

# Schnellladen in den Griff bekommen
**Kernaussage: Die LFP-Zelle hält mit beidseitiger Kühlung (K3) beide Vorgaben ein (33.8 °C / 4.6 K); die 4680-Zelle (NMC) schafft das erst mit beidseitiger Kühlung über die Tab-Scheibe und begrenztem Strom (P3 + K3: 34.0 °C / 3.8 K), bei 2,1C bleibt sie bei 38.9 °C / 5.8 K knapp über der Spreizungsvorgabe (Opus).**

**Bild:** sim/kuehlung/k1_schnellladen/landkarte.png (alle Fälle gegen die Vorgaben, Ampel; Zielband 45 °C / 5 K beschriftet), Verläufe sim/kuehlung/k1_schnellladen/verlauf_kuehlung_NMC.png (Zielband grün); gerendert sim/kuehlung/k1_schnellladen/bilder/render_NMC_P3_K3_ende.png

**Zahlen** (Quelle sim/kuehlung/k1_schnellladen/ergebnis.json, Spitzenwerte T_max / ΔT Kern):
- P0 konstant 2,1C, 20 min: LFP 43.1 °C / 10.6 K; NMC 53.4 °C / 15.7 K
- P1 Stufen: LFP 44.1 °C / 11.3 K; NMC 54.9 °C / 16.6 K; P2 Puls/Wechsel (4,2C, 50 %): LFP 61.7 °C / 21.3 K; NMC 82.5 °C / 31.6 K
- P3 1,68C, 25 min: LFP 37.5 °C / 7.4 K; NMC 44.9 °C / 11.0 K. P4 1,4C, 30 min: LFP 34.1 °C / 5.4 K; NMC 39.6 °C / 8.1 K
- Kühlung bei P0: h 1000 LFP 39.7 °C / 10.8 K, NMC 49.0 °C / 17.3 K; K3 LFP 33.8 °C / 4.6 K, NMC 38.9 °C / 5.8 K; K3 + h 1000 NMC 34.6 °C / 5.7 K; Vorkühlung 15 °C: LFP 33.1 °C / 10.6 K, NMC 43.4 °C / 15.7 K
- K1b (NMC, oben über Verbinder/Pad statt Plattenkontakt, h_eff 214 W/(m²K), Annahme Opus): P0 42.8 °C / 8.1 K; P3 36.8 °C / 5.4 K (ΔT-Vorgabe knapp verfehlt; mit Bedeckung 0,7: 35.6 °C / 4.7 K erfüllt); P4 33.3 °C / 3.8 K erfüllt (Quelle sim/kuehlung/k1_schnellladen/ergebnis.json, Abschnitt 8 in ERGEBNIS.md)
- Annahmen: Profile, Kühlfälle, h-Werte, Innenwiderstand, Q = I²R gleichmäßig im Kern; Tab-Scheibe 0,3 mm Al + Kontaktschicht (Umsetzung als Ersatzleitfähigkeit, Annahme); Vorgaben 45 °C / 5 K (REQ-P09 offen); Entwurf, noch nicht von Opus geprüft

*KI-generiert, Entwurf.*

