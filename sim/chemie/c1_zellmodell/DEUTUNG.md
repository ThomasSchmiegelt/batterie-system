| Dok.-Nr. | DEU-C1 | Version | 1.0 | Status | geprüft (KI) |
|---|---|---|---|---|---|
| Titel | Deutung C1: PyBaMM-Zellmodell | Ersteller | Claude Opus (KI) | Prüfer | – |

> KI-generiert (Opus, 2026-11-17). Grundlage ergebnis_zahlen.json (Rückgabe Sonnet), keine eigene Rechnung.
1. **NMC (Chen2020, LG M50):** Kapazität +0,3 %, DCIR 6,4 mΩ (W24: 5,4–7), Wärme 6,9 W (K1-Annahme 6,7 W) → **K1/K1b für NMC bestätigt**.
2. **NMC-Ladezeit:** Ladeschluss 4,2 V nach 21,8 min, 80 % erst nach 36,2 min (CC-CV). **REQ-P05 (30 min) mit diesem Parametersatz nicht erfüllt.** Einschränkung: Chen2020 ist eine 21700-Zelle, nicht die 4680; W25 nennt für das Model-Y-4680-Pack ≈ 30 min 0→80 %. Erwartung Opus Punkt 4 eingetreten.
3. **LFP (Prada2013, A123 26650):** Beladung des Satzes ist halb so hoch wie in unserer Zelle (Kapazität mit Aktenfläche −47 %); Flächenskalierung ×1,9 halbiert den Widerstand → DCIR 0,76 mΩ gegen W20-Messung (1,0 mΩ bei 135 Ah → 1,46 mΩ bei 92 Ah). Wärme 32,8 W gegen 55 W. **Der generische Satz passt nicht zur Blade; K1 bleibt bei der Messung (konservativ).** Kalibrierung am Blade-Pulsdatensatz (C2) nötig.
4. Reversible Wärme fehlt in beiden Läufen (Prada ohne Thermik) → offen für C2.
