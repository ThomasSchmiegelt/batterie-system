| Dok.-Nr. | ERW-C0b | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Erwartung Variantenvergleich LFP-Blade gegen NMC-4680 mit Messwerten (800 V, 400 km, 1500 kg) | Ersteller | Claude Opus (KI) | Prüfer | – (Mensch offen) |

> **KI-generiert.** Festgelegt vor der Rechnung. Eingaben `eingaben.json`; Grundannahmen aus `sim/chemie/vergleich_lfp_nmc/eingaben.json`. Anlass: Zerlegungsstudie W20 (B-BAT-009), Autor: zwei Varianten parallel.

## Erwartung
1. **Energie** wie C0: Fall A 73,9 kWh brutto für beide. Fall B LFP mehr als in C0 (schwereres Pack → etwa 92–95 kWh), NMC weniger (etwa 84–86 kWh).
2. **Zellen:** LFP 250s × 1p, etwa 92 Ah (A). NMC 217s × 4p = 868 Zellen, Energie durch die Stufung etwas über Bedarf (etwa 74 kWh in A); in Fall B 5p möglich.
3. **Masse Fall A:** LFP etwa 615 kg (bei 160 Wh/kg), mit 210 Wh/kg etwa 470 kg. NMC etwa 410 kg. NMC ist klar leichter, das Band schneidet LFP nur am oberen Ende (Gen 2) nicht.
4. **Anteil:** LFP Fall A etwa 40 % (über 30 %), NMC etwa 27 % (unter 30 %).
5. **Bauraum:** LFP Fall A 213 gegen 214 Wh/L nötig → knapp nicht erfüllt oder gerade erfüllt (Rundung); Fall B nicht erfüllt. NMC: 643 × 0,40…0,60 = 257–386 Wh/L → erfüllt in A und B.
6. **Zyklen:** LFP erfüllt, NMC unsicher (keine 4680-Quelle).
7. **Deutung vorab:** Mit Messwerten gewinnt NMC-4680 bei Masse und Bauraum klar; LFP bei Zyklen, Sicherheit, Wärme (W20: 4680 erzeugt je Volumen mehr Wärme, Faktor unklar). Beide Varianten bauen ist sinnvoll.

## Verfehlte Erwartung
- LFP-Packmasse Fall A außerhalb 560–670 kg (bei 160 Wh/kg, k 0,75), NMC außerhalb 370–450 kg.
- NMC-Parallelzahl in Fall A nicht 4.
- Fall B konvergiert nicht in 50 Schritten.

## Nachtrag 2026-11-17: Lauf 2 mit Bauraum 1,95 × 1,4 × 0,13 m (ENT-013), vor der Rechnung
- Massen und Energien unverändert (Bauraum geht nicht in die Masse ein).
- Nötige Pack-Energiedichte: Fall A 208 Wh/L (vorher 214), Fall B LFP 262 (vorher 269), NMC B etwa 244.
- LFP A: 213 verfügbar gegen 208 nötig → **erfüllt** (+2,4 %, knapp über der ±2-%-Schwelle). LFP B nicht erfüllt. NMC erfüllt.
- Verfehlt, wenn sich eine Masse ändert oder LFP A nicht „erfüllt“.

## Nachtrag 2026-11-17: Lauf 3 mit Bauraum 1,95 × 1,43 × 0,13 m (ENT-030), vor der Rechnung
- Volumen 362,5 L; nötig Fall A ≈ 204 Wh/L, LFP B ≈ 257 Wh/L. LFP A erfüllt (+4,6 %), LFP B nicht, NMC erfüllt. Massen unverändert.

## Anforderung (Nachtrag)
REQ-P02, REQ-P06 (Zuordnung Opus 2026-11-23)
