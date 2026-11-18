| Dok.-Nr. | ERW-C1 | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Erwartung C1: Zellmodell PyBaMM (DFN/SPMe + thermisch lumped) beider Zellen, Wärme beim Schnellladen | Ersteller | Claude Opus (KI) | Prüfer | – |

> KI-generiert, vor der Rechnung. Ziel: die I²R-Wärme aus K0/K1 (R konstant, grob aus W20 Abb. 8) gegen ein elektrochemisches Modell prüfen. Parametersätze PyBaMM: LFP `Prada2013`, NMC811 `Chen2020` (LG M50, 21700) – **Annahme**: auf unsere Zellkapazität (92,4 bzw. 23,1 Ah) über Elektrodenfläche skaliert (Fläche aus Akten ENT-032…045 bzw. ENT-057…070).
## Erwartung
1. Kapazität nach Skalierung ± 10 % der Akten (LFP 92,4 Ah, NMC 23,1 Ah).
2. Wärme beim Schnellladen (LFP 2,1C, NMC 1,4C, 25 °C): mittlere Wärme LFP ≈ 40–70 W (I²R-Annahme 55 W), NMC ≈ 5–9 W (6,7 W). Reversibler Anteil ± 10–20 %.
3. Gleichstromwiderstand (10 s Puls, 50 % SOC, 25 °C): LFP ≈ 1–2 mΩ, NMC ≈ 5–8 mΩ (W24: 5,4–7).
4. Endspannung beim Laden erreicht bei NMC 1,4C die Ladeschlussspannung 4,2 V vor 80 % → CC-CV, Ladezeit länger (Prüfgröße).
## Verfehlt
Kapazität > 10 % daneben; Wärme außerhalb Faktor 1,5 der I²R-Annahme (dann K1 neu mit Modellwärme).
