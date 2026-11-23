# Kontext für das Bauteilgespräch: BT-300 Regelung (BMS)

KI-generiert von pm.py aus Projektdateien (nur eigene Dokumente).

## Ich bin
Regelung (BMS) (BT-300). Aufgabe: misst, schützt, gleicht aus, schaltet. Teil von: BT-000. Meine Teile: BT-310 BMS-Hauptsteuergerät, BT-320 Zellüberwachung, BT-330 Temperaturfühler Zelle, BT-340 Strommessung, BT-350 Isolationswächter, BT-360 Messleitungen.

## Meine Merkmale (Wert und entscheidende Akte)
- architektur: noch nicht entschieden  (–)

## Anforderungen an mich (Lastenheft)
| REQ-P11 | Sicherheit: keine Ausbreitung des thermischen Durchgehens bzw. Warnzeit nach Norm | nach Norm (BAT-DOC-07) | Norm | Muss | offen |
| REQ-P15 | Messung und BMS: Zellspannung, Temperatur, Isolationswächter | Umfang offen | Autor | Muss | offen |

## Entscheidungen, die mich betreffen (vollständig)
### ENT-110 Zentrales BMS mit Zellüberwachung (CMU) in isolierter Daisy-Chain (2026-11-18, vorgeschlagen, Opus (Annahme ERW-E2); Variante: alle)
Merkmal: architektur = zentral_BMS_CMU_Daisy-Chain ; Anforderungen: REQ-P15; Belege: B-BAT-024
## Frage
Auslegungswert architektur von BT-300 für E2 (Elektronik, Kabel).
## Alternativen
Keine geprüft; Annahme Opus (ERW-E2 Annahmen-Tabelle bzw. Nachtrag 1), Lehrbuch-/Gedächtniswissen, kein Beleg aus Recherche W27.
## Entscheidung und Begründung
Zentrales BMS mit Zellüberwachung (CMU) in isolierter Daisy-Chain. Herkunft: sim/elektrik/e2_elektronik/ERWARTUNG.md (ERW-E2). Status vorgeschlagen, Freigabe nur durch den Mensch.
## Folgen
Eingabe für cad/pack/pack.py (E2) und sim/elektrik/e2_elektronik/elektronik.py.

---
*KI-generiert (Claude Sonnet, 2026-11-18), im Auftrag von Opus.*

## Befund B-BAT-024
B-BAT-024 (2026-11-18) E2 Elektronik Teil 1: Abgriffe, Ausgleich, Vorladung ok; HV-Verlust 13 W/m akzeptiert; Schaltbox Fall b
- Teil 1 (`sim/elektrik/e2_elektronik/ERGEBNIS.md`): 251/218 Abgriffe, Ausgleich 12,3 h, Vorladung 8 A/320 J/300 ms. Opus-Fehler in der Erwartung: ≤ 15 W bei 3–5 m HV-Leitung war mit 50 mm² nicht möglich (≈ 13 W/m, nur beim Schnellladen). NMC-Heizung 26 min unter dem Band, weil die Zellmasse kleiner ist (308 kg).
- CMU-Wärme NMC 9,95 W bei Nennspannung, bei Ladeschluss über 10 W → Rechnung mit Zellhöchstspannung nachholen.
- Autor: Schaltbox auf dem Deckel vorne (ENT-109). Antworten auf Sonnets Fragen 1–3 im Nachtrag 1 der ERWARTUNG; 4: 139 A (1,5C) gilt; 5: Höchstspannung LFP 3,65 V, NMC 4,2 V (Annahme). Vorgang: [E2]

## B-BAT-023 (2026-11-17) C2 Kalibrierung: Blade-Widerstand gemessen 0,877 mΩ; 4680 schafft 30 min bei 1,5C, Plating-Risiko im Modell
- Blade 25 °C, 15–90 % SOC: RMS 15,3 mV, R10 Modell 0,827 / Messung 0,877 mΩ (Test#5). Temperaturfit verfehlt (158 mV), OCV des Literatursatzes 143 mV daneben → **DFN für LFP nicht belastbar; Opus: für Wärme den gemessenen Widerstand nutzen** (unsere Zelle 1,28 mΩ → 48 W statt 55 W bei 2,1C; K1 war konservativ).
- 4680 (Chen2020-Material, W20-Geometrie, DCIR 6,4 mΩ im Band): 10→80 % in 29,7 min bei 1,5C CC-CV → REQ-P05 erfüllbar. Wärme 7,4 W (Modell) bzw. 11,5 W (I·ΔU) gegen K1b-Annahme 6,7 W → K1c: LFP 32,7 °C / 4,0 K ✓; 4680 mit Modellwärme 34,0 / 4,15 ✓, mit I·ΔU 39,1 / 6,5 ✗ (5 K). Opus: Differenz de

