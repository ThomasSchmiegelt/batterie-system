| Dok.-Nr. | ERG-E1 | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Ergebnis E1 Ströme, Querschnitte, Verluste | Ersteller | Claude Sonnet (KI) | Prüfer | Opus (Stichprobe) |

> **KI-generiert.** Claude Sonnet, 2026-11-17, Auftrag E1. Entwurf, nicht freigegeben. Alle Zahlen aus `sim/elektrik/e1_querschnitte/ergebnis.json` (aus `eingaben.json` durch `querschnitte.py`, Sekunden, CPU). Modell: Strom aus Last, Querschnitt aus Stromdichte (Al ≤ 3, Cu ≤ 5 A/mm²) und stationärer Erwärmung über Pad zur Kühlplatte.

## Abgleich ERWARTUNG.md
1. Maßgeblicher Strom LFP 194 A Laden / ≈ 240 A Spitze Entladeschluss: Ist 193,99 A und 240,0 A: ERFÜLLT.
2. LFP Reihenverbinder Al 70–100 mm², 249 Stück: Ist 75 mm² (15×5, J 2,59 A/mm²), 249 Stück: ERFÜLLT.
3a. NMC Gruppenverbinder Al 50–80 mm²: Ist 45 mm² (15×3, J 2,88 A/mm², Dauer 129,5 A): VERFEHLT knapp (7 mm² unter Band, 10 % unter Untergrenze; innerhalb der Toleranz 50 %). Grund: Wahl nach oberer Stromdichtegrenze 3 A/mm² (Mindestquerschnitt 43,2 mm²).
3b. NMC Zellabgriff 10–20 mm²: Ist 12 mm² (12×1), Zellstrom 32,4 A Laden, 57,6 A Spitze: ERFÜLLT.
4. HV-Hauptleitung Cu 35–50 mm²: Ist LFP 50 mm² (J 3,88), NMC 35 mm² (J 3,70): ERFÜLLT (LFP am oberen Bandrand).
5. Verluste bei Dauerstrom < 100 W: Ist LFP 105,2 W (Verbinder 52,8 + HV 52,4), NMC 385,4 W nach Nachtrag Methode (Gruppe 254,9 + Zellabgriff 98,3 + HV 32,1; vorher 566,3 W): LFP knapp VERFEHLT (5 %), NMC VERFEHLT (> 300 W, Verfehlt-Bedingung der Erwartung).
Spannungsabfall (Grenze 0,5 %, Annahme): LFP 0,27+0,27 = 0,54 V = 0,068 %, ERFÜLLT; NMC 3,54 V = 0,442 %, ERFÜLLT (vorher 0,547 %).
Erwärmung gegen Kühlplatte (Grenze 30 K, Pad 1 mm, λ 3 W/mK): LFP 0,31 K, NMC Gruppe 0,23 K, Zellabgriff 0,07 K; mit λ 1 W/mK höchstens ≈ 0,9 K: nie maßgeblich, die Stromdichte entscheidet. Adiabatischer Anstieg Spitze 10 s höchstens 3,0 K (Gruppenverbinder).

## Tabelle (Quelle ergebnis.json, arten[…])
| Art | Stück | Maß / Querschnitt | J A/mm² | Verlust Dauer W | Verlust Spitze W | Masse kg |
|---|---|---|---|---|---|---|
| LFP Zell-/Reihenverbinder | 249 | Al 15×5 = 75 mm², L 15 mm | 2,59 | 52,8 | 80,9 | 0,76 |
| LFP HV-Leitung | 2 | Cu 50 mm², L 2024 mm | 3,88 | 52,4 | 80,2 | 1,81 |
| NMC Gruppenverbinder (217 Sammelstrecken L 192 + 216 Brücken L 48) | 216 | Al 15×3 = 45 mm² | 2,88 | 254,9 | 807,0 | 6,32 |
| NMC Zellabgriff | 1736 | Al 12×1 = 12 mm², L 23 mm | 2,70 | 98,3 | 311,3 | 1,29 |
| NMC HV-Leitung | 2 | Cu 35 mm², L 1950 mm | 3,70 | 32,1 | 101,8 | 1,22 |
Summen: LFP 2,57 kg (Al 0,76, Cu 1,81), NMC 8,84 kg (Al 7,62, Cu 1,22); Verlust 0,070 % (LFP) und 0,257 % (NMC) von 150 kW.

## Annahmen (neu durch diesen Lauf, alle in eingaben.json mit Herkunft)
Pad λ = 3 W/mK (Band 1–5; in den Akten nicht belegt, ENT-095), ρ Al 2,82e-8 / Cu 1,72e-8 Ωm bei 20 °C, Cu-Dichte 8960 und c-Werte (Lehrbuch), Normstufen Breite 10–50 mm, Dicke 1–5 mm, HV 10–95 mm² (handelsüblich, keine Norm zitiert), Zellabgriff-Länge 23 mm, Gruppenverbinder-Länge 192 mm (voller Strom über ganze Länge, konservativ), HV-Länge je Pol = Gehäuselänge M0, Zellabgriffe 1736 (2 je Zelle), Wahlregel kleinste Fläche, bei Gleichheit kleinste Breite.

## Offen / Rückfragen an Opus
- NMC-Verlust 385 W > 300 W bleibt auch nach Nachtrag Methode; größter Posten Gruppenverbinder 254,9 W (Sammel 146,0 + Brücke 109,0), Entscheidung über größeren Querschnitt bei Opus.
- Stückliste war 220/10 Stück; jetzt aus s und p abgeleitet (siehe Nachtrag Stückliste).
- Zellverbinder-Kontaktwiderstand (Laserschweißung ENT-094), HV-Leitungserwärmung und Isolation, Pad-λ nicht modelliert/belegt.
- Annahme Verfehlt-Grenzen verletzt: Entscheidung ob Gruppenverbinder auf 60–80 mm² erhöht werden soll liegt bei Opus.

## Nachtrag Methode (Annahme Opus, 2026-11-17)
Gruppenverbinder NMC: Der Strom wächst entlang der Sammelstrecke gleichmäßig von 0 auf I (4 Zellabgriffe), Verlust dort I²R/3 (217 Stück, L 192 mm); nur die Reihenbrücke zur Nachbargruppe (216 Stück, L 48 mm = 1 Zellteilung M0) führt vollen Strom. Querschnitt unverändert nach Stromdichte am Gruppenende (45 mm²). Spannungsabfall Sammelstrecke I·R/2 (linearer Stromanstieg, Sonnet-Folgerung aus derselben Annahme). Werte (ergebnis.json, arten[NMC Gruppenverbinder]): Verlust 254,9 W (Sammel 146,0, Brücke 109,0; vorher 435,8 W), Spitze 807,0 W, Abfall 2,53 V, Masse 6,32 kg. NMC-Summe 385,4 W, 0,442 %.

## Nachtrag Stückliste (Opus 2026-11-17)
`pm/bauteile/stueckliste.py`: 400.1 = 2·n bei p > 1, sonst 0; 400.2 = s − 1. Läufe ohne Variante (220 s, p 1: 0 und 219), LFP (0 und 249), NMC (1736 und 216); docs/13_stueckliste*.md neu erzeugt. Stückliste LFP zählt 249 unter 400.2 (BT-420), 400.1 entfällt bei p = 1.

*KI-generiert (Claude Sonnet), Entwurf.*
