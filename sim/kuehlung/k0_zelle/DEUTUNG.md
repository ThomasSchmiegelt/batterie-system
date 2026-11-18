| Dok.-Nr. | DEU-K0 | Version | 1.0 | Status | geprüft (KI) |
|---|---|---|---|---|---|
| Titel | Deutung K0: Wärme der Einzelzelle | Ersteller | Claude Opus (KI) | Prüfer | – (Mensch offen) |

> **KI-generiert** (Opus, 2026-11-17). Grundlage ergebnis.json, ERGEBNIS.md, Bilder verlauf_L2, render_*_t1200s angesehen. Gegenrechnung Opus (Skript): Filmwiderstand Kühlrand Q/(h·A).

## Prüfung
- Energiebilanz < 0,001 % stationär, Netzstudie 0,017 K: Rechnung numerisch sauber.
- **Verfehlte Erwartung NMC (33,5 statt ≈ 31 °C; L2 53,6 statt 45–50 °C) ist ein Fehler der Erwartung, nicht der Rechnung:** Opus hat den Temperatursprung am Kühlrand vergessen. Der 4680-Boden ist nur 16,6 cm² groß: 3,5 W / (500 · 0,00166) = 4,2 K bei 1C, 18 K bei 2,1C. Mit Film: 25 + 4,2 + 4,8 = 34 °C (Rechnung 33,5). LFP-Boden 95 cm², Film 2,6 K → 30,6 °C (Rechnung 30,1).
- K2 (Mantelband 25 %) kühler als K1: Kühlfläche 29 cm² statt 17 cm², Film kleiner; ΔT größer (18,1 K, radial schlecht leitend). Plausibel.
- LFP nach 20 min 82 % stationär: Leitzeit über 90 mm Höhe L²/a ≈ 0,0081 / 8,3·10⁻⁶ ≈ 1000 s – plausibel.
## Aussage
1. **1C:** beide Varianten in der Vorgabe (45 °C, 5 K).
2. **Schnellladen 20 min:** LFP hält 45 °C (43,1), NMC-4680 mit Bodenkühlung nicht (53,6 °C ab Minute 10,7). Die **Spreizung 5 K verfehlen beide** (LFP 10,6 K, NMC 16 K) – mit Kühlung nur von unten ist die Vorgabe beim Schnellladen nicht erreichbar.
3. Engpass 4680: kleine Bodenfläche (Film 18 K) – nicht die Leitung im Wickel. Engpass LFP: Weg 90 mm in der Höhe.
4. Stärkster Hebel laut Tornado: Innenwiderstand (Faktor 2 Band, grob aus W20 Abb. 8 abgelesen) → C1–C3-Zellmodell mit Blade-Pulsdatensatz schärft das.
## Fragen an den Autor (Vorschlag Opus, nicht entschieden)
- Spreizung 5 K beim Schnellladen: (a) Ladeleistung begrenzen, (b) Vorgabe 5 K nur für 1C, beim Schnellladen z. B. 10 K, (c) zweiseitige Kühlung. Für NMC zusätzlich: Boden-Wärmeleitung verbessern (Tab-Scheibe flächig angebunden, h höher) oder Mantelkühlung.
- Vorkonditionierung (Start 25 °C ist Annahme; im Winter kälter, im Sommer wärmer).
