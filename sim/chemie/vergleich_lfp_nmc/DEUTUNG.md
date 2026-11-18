| Dok.-Nr. | DEU-C0 | Version | 1.0 | Status | geprüft (KI) |
|---|---|---|---|---|---|
| Titel | Deutung Chemievergleich LFP gegen NMC (1500 kg, 400 km) | Ersteller | Claude Opus (KI) | Prüfer | – (Mensch offen) |

> **KI-generiert.** Grundlage: `ergebnis.json` (Sonnet, `vergleich.py`). Opus hat alle Kernzahlen mit einem eigenen Skript nur aus `eingaben.json` nachgerechnet, mit gleichem Ergebnis (Energie, Packmasse, Spannen, Anteile, Iterationsschritte, Zellzahl). Erwartung: `ERWARTUNG.md`, Punkte 1–6 erfüllt.

## Kernaussage
Für 400 km braucht das Pack bei beiden Chemien rund 74 kWh brutto (Fall A) und wiegt in der Mitte der Datenlage etwa 500 kg (LFP 499 kg, NMC 464 kg). **Die belegten Daten zeigen keinen klaren Massenvorteil für NMC.** Die Spanne von NMC (316–758 kg) umschließt die von LFP (414–615 kg) ganz. Bei Lebensdauer und Sicherheit liegt LFP vorn, bei Kälte NMC. Offen bleibt der Bauraum.

## Deutung je Kriterium
| Kriterium | LFP | NMC | Wertung |
|---|---|---|---|
| Packmasse Fall A / B (Mitte) | 499 / 599 kg | 464 / 549 kg | NMC 7–8 % leichter, weit innerhalb der Unsicherheit. Kein Entscheidungsgrund. |
| Unsicherheit | schmal (Blade-Zellen belegt 185–210 Wh/kg) | breit (150–275 Wh/kg, Ebene unsicher) | LFP ist besser abgesichert. NMC braucht eine fahrzeugspezifische Quelle. |
| Batterieanteil, Grenze 30 % (Annahme) | A 33,3 %, B 28,5 % | A 30,9 %, B 26,8 % | Fall A: Beide liegen über der Grenze. 400 km bei 1500 kg Gesamtmasse sind knapp, unabhängig von der Chemie. |
| Zyklen (Bedarf 1000) | erfüllt (2500–9000) | unsicher (400–1200, nur Li-Ion allgemein) | spricht für LFP |
| Zellen in Reihe, 800 V | 250 | 220 (217–223) | LFP braucht 14 % mehr Zellverbinder und Messkanäle. Gering. |
| Bauraum (nötig 214 Wh/L in A, 253–256 in B) | offen (keine Blade-Quelle) | Zellband 250–842 (allgemein, Zelle) | nicht entscheidbar. Die Annahme 180 Wh/L in startwerte.py, die bisher NMC erzwang, ist unbelegt. |
| Kälte | Material bei −20 °C: 46,7 statt 141,8 mAh/g (W01). Geely Blade: 90,54 % bei −30 °C (W03) | kein Beleg | Belege auf verschiedenen Ebenen. Für LFP wird die Heizung (BT-760) wichtiger. |
| Sicherheit | Nageltest Blade: Oberfläche 30–60 °C (W03) | Sauerstofffreisetzung ab 300 °C (W10) | spricht für LFP (REQ-P11) |
| Vorbild | BYD Blade ist LFP | – | Projektauftrag |

## Stärkste Annahmen
Fall B, Hub der Packmasse: LFP bewegt sich am stärksten mit dem Zellanteil am Pack (196 kg), NMC mit dem Zellband (434 kg). Der Massenanteil des Verbrauchs bewegt beide nur um 80–100 kg. Um die Unsicherheit zu verkleinern:
1. Blade-Zerlegungsstudie (doi:10.1016/j.xcrp.2025.102453): Masse, Ah, Wh/L der Zelle. Das schließt die Bauraumfrage.
2. NMC-Fahrzeugzellen: eigenes Recherchethema mit Zellebene.
3. Zellanteil am Pack: Packkennwerte aus Recherche oder später aus dem eigenen CAD (G4).

## Vorschlag an den Autor
**LFP im Blade-Format als Hauptvariante, NMC als Vergleichsvariante** im Modell mitführen (Akte ENT-005, vorgeschlagen). Begründung: Masse ohne belegten Unterschied, Zyklen und Sicherheit für LFP, Vorbild. Prüfpunkt: Zeigt die Zerlegungsstudie, dass LFP-Blade die nötigen Wh/L im Bauraum nicht erreicht, wird neu entschieden.
Rückfrage: Sind die 1500 kg mit Batterie gemeint (Fall A) oder ohne (Fall B)? In Fall A liegt die Batterie bei beiden Chemien über einem Drittel bzw. knapp über 30 % der Gesamtmasse.

---
*KI-generiert (Claude Opus, 2026-11-16). Status geprüft (KI), nicht freigegeben.*
