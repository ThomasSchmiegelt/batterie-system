# Startparameter Batteriesystem – Variante LFP

> **KI-generiert** (Claude Opus, pm/startwerte.py). Status: Vorschlag, nicht freigegeben. Alle Faktoren sind **Annahmen**, bis die Recherche (W01–W15) sie bestätigt.

## Startsatz (das Einzige, was der Mensch vorgibt)

> „Kompaktwagen, 400 km Reichweite, in 20 min auf 80 %, Mitteleuropa“

| Angabe | Wert | Herkunft |
|---|---|---|
| fahrzeug | Kompakt | Startsatz |
| reichweite_km | 400 | Startsatz |
| laden_min | 20 | Startsatz |
| klima | Mitteleuropa | Startsatz |

## Hergeleitete Lastenheft-Werte

| REQ | Größe | Wert | Rechenweg |
|---|---|---|---|
| REQ-P01 | Fahrzeug | Kompakt | Startsatz |
| REQ-P02 | Energie nutzbar / brutto | 68 / 74 kWh | 400 km × 17 kWh/100 km; brutto = netto / (1 − 0.08) |
| REQ-P05 | Schnellladen | 10→80 % in 20 min: Mittel 143 kW, Spitze 186 kW | 0.7 × 68 kWh / 0.33 h; Spitze × 1.3 |
| REQ-P03 | Systemspannung | 800 V (nominal) | max(Ladespitze 186, Antrieb 150) kW > 150 kW |
| REQ-P04 | Leistung Entladen | Spitze 150 kW, Dauer 60 kW | Fahrzeugklasse; Dauer = 0.4 × Spitze |
| REQ-P06 | Zellchemie | LFP | LFP (ENT-005, entschieden); Bauraumregel: nötig 204 Wh/L im Bauraum 363 L; Pack LFP 180, NMC 330 Wh/L; Regel ergäbe NMC |
| REQ-P07 | Bauraum / Masse | 1.95 × 1.43 × 0.13 m, ca. 528 kg | Fahrzeugklasse; L aus ENT-013; B aus ENT-030; Masse = 74 kWh / 140 Wh/kg |
| REQ-P08 | Umgebungstemperatur | -20 … +40 °C | Einsatzgebiet Mitteleuropa |
| REQ-P10 | Lebensdauer | ≥ 1000 Vollzyklen bis 80 % Restkapazität | 200000 km / 400 km × 2.0 |

## Warnungen

- Bauraum offen: Annahme wh_l_pack LFP 180 Wh/L unbelegt (B-BAT-004/006); nötig 204 Wh/L

## Annahmen (zu prüfen durch die Recherche)

- `reserve` = 0.08
- `ladefenster` = 0.7
- `spitze_zu_mittel` = 1.3
- `grenze_400V_kW` = 150
- `dauer_zu_spitze` = 0.4
- `km_leben` = 200000
- `sicherheit_zyklen` = 2.0
- `rest_soh` = 0.8
- `wh_l_pack` = {'LFP': 180, 'NMC': 330}
- `wh_kg_pack` = {'LFP': 140, 'NMC': 200}
- `c_laden_max` = {'LFP': 3.0, 'NMC': 3.0}

Nicht im Startsatz, weil nach Norm oder aus Rechnung: REQ-P09 (Zelltemperatur, Recherche), P11/P13/P14 (Normen), P12 (Kühlmittel, Vorschlag Wasser-Glykol), P15 (BMS-Umfang folgt aus Spannung und Zellzahl).
