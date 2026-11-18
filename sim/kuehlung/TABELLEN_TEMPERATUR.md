| Dok.-Nr. | TAB-K | Version | 1.0 | Status | geprüft (KI) |
|---|---|---|---|---|---|
| Titel | Sammeltabellen Temperaturberechnung K0, K1, K1b, K1c (Einzelzelle, Elmer) | Ersteller | Claude Opus (KI) | Prüfer | – (Mensch offen) |

> KI-generiert, 2026-11-17, auf Wunsch des Autors („merke dir auch die tabellen der temperaturberechnung“). Zahlen aus `k0_zelle/ergebnis.json`, `k1_schnellladen/ergebnis.json` (von Opus stichprobenartig geprüft). Vorgabe REQ-P09: T_max ≤ 45 °C, Spreizung in der Zelle ≤ 5 K. **NMC-Zeilen K0/K1 (außer Tab-Scheibe/K1b) stammen vom alten Netz (Kern r 7,0 mm); Neulauf mit r 6,25 mm weicht ≤ 0,3 K ab (z. B. P0 53,4/15,7) – maßgeblich ist `k1_schnellladen/ergebnis.json`.** Annahmen: Kühlmittel 25 °C, h 500 W/(m²K), R LFP 1,46 mΩ, R NMC 6,5 mΩ.

## K0 – Grundfälle (Kühlplatte unten)
| Fall | LFP T_max / ΔT | NMC T_max / ΔT |
|---|---|---|
| L1 1C stationär | 30,1 °C / 3,0 K | 33,5 °C / 4,8 K |
| L2 Schnellladen 2,1C, 20 min | 43,1 / 10,6 | 53,6 / 16,0 |
| L2, NMC Kühlband Mantel (K2) | – | 49,9 / 18,1 |

## K1 – Schnellladen: Profile und Kühlung (Spitzenwerte)
| Fall | LFP | NMC |
|---|---|---|
| P0 konstant 20 min | 43,1 / 10,6 | 53,6 / 16,0 |
| P1 Stufen 3C/2C/1,4C | 44,1 / 11,3 | 55,1 / 17,0 |
| P2 Puls bzw. Zellen im Wechsel | 61,7 / 21,3 | 82,9 / 32,3 |
| P3 konstant 25 min | 37,5 / 7,4 | 45,0 / 11,3 |
| P4 konstant 30 min | 34,1 / 5,4 | 39,7 / 8,3 |
| P0 + h 1000 | 39,7 / 10,8 | 49,3 / 17,7 |
| P0 + h 2000 | 37,4 / 10,5 | 46,3 / 18,1 |
| P0 + Vorkühlung 15 °C | 33,1 / 10,6 | 43,6 / 16,0 |
| **P0 + Kühlplatte oben und unten (K3)** | **33,8 / 4,6 ✓** | 38,9 / 5,8 (mit Tab-Scheibe) |
| P0 + K3 + h 1000 | 30,8 / 3,8 ✓ | 34,6 / 5,7 |
| P3 + K3 | – | 34,0 / 3,8 ✓ (Deckel direkt gekühlt) |

## K1b – NMC oben über Verbinder + Isolierpad (h_eff ≈ 214)
| Fall | NMC |
|---|---|
| P0 20 min | 42,8 / 8,1 |
| P3 25 min | 36,9 / 5,5 (36,86 / 5,47) |
| **P4 30 min** | **33,3 / 3,8 ✓** |
| P3, Bedeckung 0,3 / 0,7 | 38,6 / 6,6 · 35,6 / 4,7 ✓ |
| P3, Pad k 1 / 6 W/mK | 37,7 / 6,0 · 36,5 / 5,2 |

## K1c – Wärme aus C2 statt I²R-Schätzung (Zahlen aus `k1_schnellladen/ergebnis.json`, Abschnitt 9 in ERGEBNIS.md)
| Fall | T_max / ΔT (Spitze) |
|---|---|
| LFP P0 + K3, R 1,28 mΩ (C2/Test#5; vorher R 1,46: 33,8 / 4,6) | 32.7 / 4.0 |
| NMC K3b, C2-Q(t) 1,5C, Modell gesamt (mittel 7,4 W, 28,7 min) | 34.0 / 4.2 |
| NMC K3b, C2-Q(t) 1,5C, I·ΔU (skalierte Form, mittel 11,5 W) | 39.1 / 6.5 |
Hinweis: CSV-Verlauf endet bei 1720,8 s (80 % bei 1780,8 s); I·ΔU-Verlauf = skalierte Form (Annahme).

## Folge (Autor-Entscheidungen)
Kühlplatte oben und unten (ENT-088); Schnellladen LFP 20 min, NMC 30 min (REQ-P05). Stufen-/Pulsladen thermisch ohne Nutzen; h und Vorkühlung senken nur T_max.
