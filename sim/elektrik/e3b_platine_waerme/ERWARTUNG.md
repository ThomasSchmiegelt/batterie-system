| Dok.-Nr. | ERW-E3b | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Erwartung E3b: Temperatur der CMU-Platine mit Wärmeleitpad (ENT-184), Elmer | Ersteller | Claude Opus (KI) | Prüfer | – |

> KI-generiert (Opus, 2026-11-24), vor der Rechnung. Anlass: B-BAT-051 (ohne Wärmepfad 112–184 °C), Entscheidung ENT-184 (Autor, KR1 K2). Anforderungen: REQ-P15, REQ-P20 (Bauteiltemperatur), REQ-P09 (Zellen ≤ 45 °C). Alle Werte unten sind **Annahmen Opus** (Herkunft „ERW-E3b“), sofern nicht als Akte oder Ergebnis genannt.


## Anforderung
REQ-P20, REQ-P15, REQ-P09

## Lage (aus dem CAD, prüfen!)
Die CMU steht **hochkant in den Endzonen, an den Rahmen gelehnt** (`cad/pack/pack_e2d.py`, Z. 207 ff.). Das Pad sitzt deshalb zwischen der CMU-Rückseite und dem **Seitenrahmen bzw. der Gehäusewand** (Al), nicht direkt auf der Kühlplatte. Ist die Wand nicht thermisch an die Kühlplatte angebunden → als offene Frage melden.

## Annahmen Opus (ERW-E3b)
| Größe | Wert | Begründung |
|---|---|---|
| Verlust je CMU | LFP 9,99 W, NMC 9,64 W (E3 SPICE) | ungünstigster Fall U_max, alle 18 Kanäle gleichzeitig |
| Lage der Wärmequellen | 36 Widerstände 2512 und 18 FETs nach Layout E3 (`layout_<V>_info.json`) | |
| Leiterplatte | FR4 1,6 mm, λ 0,3 (quer) / 0,8 W/mK (längs), 4 × Cu (70/35/35/70 µm), λ_Cu 390 W/mK | Schichten als homogenisierte Ersatz-λ oder Schalen |
| Thermische Vias | unter jedem Widerstandspaar 8 Vias Ø 0,3 mm (Annahme, ins Layout übernehmen) | Durchgang zur Rückseite |
| Pad | 1,0 mm, λ = 3 W/mK, ganzflächig 120 × 60 mm | marktübliche Klasse |
| Rand Wand | T = 45 °C (Zellgrenze REQ-P09, ungünstig: Wand so warm wie die wärmste Zelle) | |
| Vorderseite | h = 5 W/m²K Konvektion + Strahlung ε 0,9 gegen 45 °C | konservativ |
| Grenzwert | Bauteil ≤ 105 °C (Annahme, wie E3); FR4-Tg nicht relevant | |

## Erwartung
1. **Mit Pad:**
   - Pad: R ≈ 0,001 / (3 × 0,0072) ≈ 0,05 K/W → ≈ 0,5 K
   - Leiterplatte quer mit Vias: ≈ 0,3–1 K/W → 3–10 K
   - örtliche Spitze am Widerstand: 10–25 K
   - **T_max ≈ 60–80 °C**, Grenze 105 °C mit ≥ 25 K Reserve eingehalten
2. **Ohne Vias (nur FR4 quer):** R ≈ 0,0016 / (0,3 × 0,0072) ≈ 0,74 K/W, das ergibt flächig +7 K. Örtlich unter den Widerständen ist es viel mehr, **T_max ≈ 80–100 °C**. Die Vias sind also nötig, aber kein Muss für die Grenze.
3. **Ohne Pad (Prüffall, Abgleich mit E3):** ≈ 100–130 °C. Das muss im Band der Abschätzung von E3 mit Strahlung liegen (B-BAT-051). Liegt es außerhalb: Modellfehler suchen, nicht weiterrechnen.
4. **Wärmestrom in die Wand** ≈ 90 % von P. Die Zellen in der Endzone erwärmt das um < 1 K (bei 14 CMU ≈ 140 W über die Wand verteilt). Grob abschätzen, nicht rechnen.
5. Netzunabhängigkeit: zwei Netze, Unterschied von T_max < 2 K.

## Abbruch → OPUS
Erwartung 3 verfehlt (Modell stimmt nicht); T_max mit Pad > 105 °C; CMU ohne Kontakt zu einer gekühlten Wand; fehlendes Maß; jede neue Annahme.

## Nachtrag 1 (Opus, 2026-11-24, nach der Rechnung; Rohdaten `ergebnis.json` geprüft, Energiebilanz 9,75 + 0,24 W ≈ 9,99 W)
- **Erwartung 1 und 2 nach unten verfehlt.** Ursache: Das Modell setzt vier vollflächige Cu-Lagen an (λ_xy 51,9 W/mK). Das ist günstiger als meine Abschätzung. Maßgebend nach der Regel „erst konservativ“ ist der Fall **Cu ohne Querleitung**: (a) 52,6 / 52,4 °C, (b) 93,9 / 92,5 °C. Damit liegt (b) im Band. Das Modell ist nicht falsch, meine Bänder waren zu vorsichtig.
- **Entscheidung:** Pad 1,0 mm, λ 3 W/mK, 8 Vias je Widerstandspaar (ENT-185…187, Opus delegiert). Vias weglassen bleibt OPT-003 (nur 11 K Reserve).
- Die Wand mit 45 °C ist konservativ (Al-Rahmen mit Kontakt zu den Kühlplatten). Die Zellerwärmung < 1 K bleibt ungeprüft (Schleife 2).
