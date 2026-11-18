| Dok.-Nr. | DEU-C0b | Version | 1.0 | Status | geprüft (KI) |
|---|---|---|---|---|---|
| Titel | Deutung Variantenvergleich LFP-Blade gegen NMC-4680 mit Messwerten (800 V, 400 km, 1500 kg) | Ersteller | Claude Opus (KI) | Prüfer | – (Mensch offen) |

> **KI-generiert.** Grundlage `ergebnis.json` (Sonnet, `varianten.py`). Opus hat Fall A und B beider Varianten mit eigenem Skript nachgerechnet: gleich. Erwartung (ERWARTUNG.md) Punkte 1–6 erfüllt, Punkt 1 NMC Fall B knapp darüber (86,6 statt 84–86 kWh).

## Kernaussage
Mit gemessenen Zellwerten ist die NMC-4680-Variante bei gleicher Spezifikation **rund ein Drittel leichter** (Fall A 411 gegen 616 kg) und passt in den Bauraum. Die LFP-Blade-Variante passt in Fall A nur knapp und in Fall B nicht. LFP bleibt vorn bei Zyklen und Sicherheit.

## Deutung
| Kriterium | LFP-Blade | NMC-4680 | Wertung |
|---|---|---|---|
| Packmasse A (Zelle gemessen) | 616 kg (160 Wh/kg); 469 kg mit Herstellerwert Gen 2 (210) | 411 kg | NMC klar leichter. Selbst LFP Gen 2 ist 14 % schwerer. |
| Anteil an 1500 kg (Grenze 30 %, Annahme) | 41 % | 27 % | LFP sprengt die Grenze in A. |
| Fall B (1500 kg ohne Batterie) | 93,0 kWh, 775 kg (160 Wh/kg) | 86,6 kWh Bedarf, 5p → 92,8 kWh, 514 kg | Masse treibt Verbrauch: LFP braucht 7 % mehr Energie. |
| Bauraum | A: 213,7 nötig / 213,2 verfügbar (−0,3 %), B: nicht (269 nötig bei 160 Wh/kg; ERGEBNIS nennt 259,9 bei Bandmitte 185) | erfüllt (257–386) | LFP hängt an der Volumennutzung 60 % (Sekundärquelle W19). |
| Zellen | 250 (92 Ah, Sonderzelle ~660 mm) | 868 (Kaufzelle) | 4680: 3,5-mal mehr Zellen, Schweißstellen und Zellhalter; BMS misst trotzdem nur 217 Reihen. |
| Zyklen | erfüllt | unsicher (keine 4680-Quelle) | für LFP |
| Wärme | W20: 4680 erzeugt je Volumen mehr Wärme bei 1 C (Faktor bei Textumwandlung verloren) | | Kühlung NMC aufwendiger (K-Vorgänge). |
| Sicherheit | Nageltest Blade (W03) | NMC811, O₂-Freisetzung (W10) | für LFP |

## Annahmen, die das Ergebnis tragen
1. Zellanteil am Pack k = 0,75 für **beide** Varianten. Rundzellen-Packs haben eher mehr Strukturmasse (Halter, Kühlbänder). Ein NMC-k von 0,65 ergäbe 474 kg, immer noch leichter als LFP.
2. Volumennutzung LFP 60 % aus einer schwachen Sekundärquelle (W19). Ein Prozentpunkt entscheidet in Fall A über „passt / passt nicht“.
3. Zellen je Reihe (24) und Temperaturfühler in der NMC-Stückliste stammen aus der LFP-Annahme; für Rundzellen offen (G4).

## Folge
Beide Varianten weiterbauen, wie vom Autor gewünscht. Die Rechnung macht die Varianten **nicht gleichwertig**: Ist 1500 kg die Gesamtmasse (Fall A), erfüllt nur NMC-4680 Masse und Bauraum. LFP-Blade ist die robuste, langlebige Variante, die mehr Bauraum oder ein leichteres Restfahrzeug braucht. Für das Bild: Balken LFP auf den Messwert 160 Wh/kg stellen (zeigt heute Bandmitte 185), Auftrag folgt.

---
*KI-generiert (Claude Opus, 2026-11-16). Status geprüft (KI), nicht freigegeben.*
