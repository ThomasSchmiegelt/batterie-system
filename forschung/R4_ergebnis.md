| Dok.-Nr. | R4-E | Version | 1.0 | Status | geprüft (KI) |
|---|---|---|---|---|---|
| Titel | R4: Recherche geprüft – welche Werte in Entscheidungsakten dürfen | Ersteller | Claude Opus (KI) | Prüfer | – (Mensch offen) |

> **KI-generiert.** Grundlage: Vorprüfung durch Sonnet (`R4_vorpruefung.md`, 27 Themen, 22 FEHLT-Zeilen: 21 Wortlaut abweichend, Wert im Rohtext; 0 nicht im Rohtext; 1 unklar ohne Zahl). Opus-Stichprobe an `pakete/`: W06 Z22, W01 Z15/Z16, W02 Z12 (Befund B-BAT-005). Vorgang R4, REQ-D01.

## Für Akten verwendbar (Beleg geprüft, Bezug klar)
| Größe | Wert | Bezug | Fundstelle | Bauteil/Merkmal |
|---|---|---|---|---|
| Zellmaße Long Blade (Gen. 1) | 960 × 90 × 13,5 mm | BYD, Zelle | W03 Z8–10 | BT-100 laenge_mm / breite_mm / dicke_mm |
| Länge Short Blade | 450–580 mm | BYD 2.0 bzw. Geely | W03 Z11–12 | BT-100 laenge_mm (Alternative) |
| Spez. Energie Blade-Zelle | 190–210 Wh/kg | Long Blade 2.0, Zelle | W03 Z13 | Prüfgröße für BT-100 masse_g |
| Spannungslage LFP | 3,2 V nominal; 3,60–3,65 V Ladeschluss; 2,0–2,8 V Entladeschluss | Chemie | W01 (B-BAT-001 geprüft) | BT-100 nennspannung_V; BT-000 Spannungsfenster |
| Spannungslage NMC | 3,6–3,7 V | Chemie | W10 Z7 | BT-100 nennspannung_V (falls NMC) |
| Lebensende | 80 % Restkapazität | Fahrzeugbatterie | W06 Z16, W15 Z15 (W14: 70–80 %) | REQ-P10 |
| Temperaturfenster Betrieb | +20 bis +30 °C | Thermomanagement allgemein | W16 Z11 | REQ-P09 (Zielband, nicht Grenze) |
| DC-Laden CCS | max. 1000 V, 500 A | Ladestandard | W12 Z13–15 | REQ-P05, BT-730 |
| Seitencrash MDB | 1500 kg, 50 km/h, 90° | Prüfverfahren | W17 | X1/X2 Lastfall |

## Nicht verwenden
| Wert | Grund |
|---|---|
| W06 Z22 „Energiedichte LFP 150–220“ | Im Rohtext NMC-Spalte. LFP-Spalte: 80–150, 210, 90–160, Einheit dort „kWh“ (gemeint wohl Wh/kg), Bezug Zelle oder Pack unklar (B-BAT-005) |
| W01 Z16 „LFP 227–396 Wh/L“ für das Blade-Format | Rechenkommentar im Rohtext: 18650-Rundzelle. Gilt nicht für Blade, beantwortet die 180-Wh/L-Frage nicht |
| W01 Z36 66 %/33 % | von PI gerechnet (richtig 65 %/33 %), ohne Kennzeichnung |
| W13 Z9 „bis 50 mm“ | Quelle sagt „50 mm oder mehr“ |

## Widersprüche: Deutung (Opus)
Die fünf „Widersprüche“ aus der Vorprüfung sind **keine echten Widersprüche**. Sie beziehen sich auf verschiedene Dinge: Zelle oder Pack, Generation (95–172 Wh/kg älter, 180–210 Wh/kg 2024/25), allgemein Li-Ion oder NMC, typische oder maximale Ladeleistung, Ladebereich, Optimum oder Herstellerbereich. Folge: Jeder Wert in einer Akte nennt seinen Bezug (Zelle/Pack, Jahr, Hersteller).

## Lücken für die Auslegung und Weg
| Größe | Weg |
|---|---|
| Kapazität (Ah), Masse, Wh/L der Blade-Zelle | Zerlegungsstudie BYD Blade gegen Tesla 4680, Cell Reports Physical Science 2025, doi:10.1016/j.xcrp.2025.102453 (CC-BY). Automatischer Abruf scheitert (JavaScript). **Autor legt das PDF in `quellen/`**, dann Thema W19 per file://. Davon hängt die Chemiewahl ab (180-Wh/L-Annahme). |
| Wärmeleitfähigkeit und Wärmeentwicklung großer LFP-Prismenzelle | W18 (314-Ah-Zelle, techscience.com, abrufbar), läuft |
| Innenwiderstand, Wärmeleistung über SOC/T | nicht recherchieren, sondern rechnen: PyBaMM (C2/C3) |
| max. Zelltemperatur, Spreizung zwischen Zellen, Kühlmitteltemperatur | keine Quelle. Bis dahin **Annahme** vorschlagen, vom Autor festlegen lassen, oder Normenrecherche (BAT-DOC-07) |
| Zellverbinder-Stromdichte | rechnen (E1: Strom aus REQ-P04/P05, Erwärmung), Zielband als Annahme |
| Patente P02–P10 | weiter gesperrt (B-BAT-003), hinten angestellt (Autor 2026-11-12) |

---
*KI-generiert (Claude Opus, 2026-11-16). Status geprüft (KI), nicht freigegeben.*
