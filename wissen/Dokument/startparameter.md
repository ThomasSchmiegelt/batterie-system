---
typ: dokument
nr: ""
version: ""
status: ""
tags: ["dokument"]
---
# startparameter – Startparameter Batteriesystem

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

- Datei: `docs/startparameter`
- Version: –
- Status: –
- Typ: Projektdokument (Dokumentenlenkung [[Dokument/00_dokumentenlenkung]])

## Genannte Anforderungen (Textvorkommen)
- [[Anforderung/REQ-P01|REQ-P01]]
- [[Anforderung/REQ-P02|REQ-P02]]
- [[Anforderung/REQ-P03|REQ-P03]]
- [[Anforderung/REQ-P04|REQ-P04]]
- [[Anforderung/REQ-P05|REQ-P05]]
- [[Anforderung/REQ-P06|REQ-P06]]
- [[Anforderung/REQ-P07|REQ-P07]]
- [[Anforderung/REQ-P08|REQ-P08]]
- [[Anforderung/REQ-P09|REQ-P09]]
- [[Anforderung/REQ-P10|REQ-P10]]

## Genannte Entscheidungen, Befunde, Bauteile (Textvorkommen)
- [[Entscheidung/ENT-013|ENT-013]]
- [[Entscheidung/ENT-030|ENT-030]]

## Vorgänge, die dieses Dokument nennen
- [[Vorgang/V1|V1]] – Lastenheft-Werte REQ-P01..P08 vorschlagen (Fahrzeug, kWh, Spannung, Leistung, Laden, Chemie, Bauraum, Temperatur)

## Inhalt (Kopie aus `docs/startparameter.md`)

# Startparameter Batteriesystem

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
| REQ-P06 | Zellchemie | NMC | nötig 204 Wh/L im Bauraum 363 L; Pack LFP 180, NMC 330 Wh/L; Regel: LFP, wenn sie passt (günstiger, sicherer) |
| REQ-P07 | Bauraum / Masse | 1.95 × 1.43 × 0.13 m, ca. 370 kg | Fahrzeugklasse; L aus ENT-013; B aus ENT-030; Masse = 74 kWh / 200 Wh/kg |
| REQ-P08 | Umgebungstemperatur | -20 … +40 °C | Einsatzgebiet Mitteleuropa |
| REQ-P10 | Lebensdauer | ≥ 1000 Vollzyklen bis 80 % Restkapazität | 200000 km / 400 km × 2.0 |

## Warnungen

- LFP passt nicht in den Bauraum (nötig 204 > 180 Wh/L)

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

