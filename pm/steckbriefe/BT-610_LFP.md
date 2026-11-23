| Dok.-Nr. | STB-BT-610-LFP | Version | 0.1 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Steckbrief BT-610 Kühlplatte (LFP) | Ersteller | Claude Sonnet (KI), pm/steckbrief.py | Prüfer | – (Opus, Mensch offen) |

> **KI-generiert.** Entwurf, nicht vom Menschen freigegeben. Erzeugt am 2026-11-23, nicht von Hand bearbeiten. Tor T1 nach docs/17.

## Stellung im Baum
- Bauteil: BT-610 Kühlplatte; Art: E; Rolle: nimmt die Wärme der Zellen auf und gibt sie ans Kühlmittel
- Elternbauteil: BT-600 Kühlung
- Kindbauteile: keine
- Anforderungen (struktur.json): REQ-P09, REQ-P12
- Varianten: alle

## Merkmale aus pm/bauteile/parameter_LFP.json
| Merkmal | Wert | Einheit | Akte |
|---|---|---|---|
| anzahl | 2.0 |  | ENT-089 |
| werkstoff | Al-Blech 1 mm, gelötet, Mäander 8 Bahnen längs, Teilkanäle |  | ENT-153 |
| dicke_mm | 6.0 | mm | ENT-152 |
| kanal_anzahl | 8.0 |  | ENT-156 |
| kanal_breite_mm | 8.0 | mm | ENT-155 |
| kanal_hoehe_mm | 4.0 | mm | ENT-154 |
| kanalfuehrung | gruppiert_k2 |  | ENT-158 |
| verteilerrohr_d_mm | 25.0 | mm | ENT-159 |

## Anzahlen und Massen (Stückliste 0.3, CAD-Ausgabe)
| Pos | Benennung | Menge Soll | Menge CAD | Masse Stückliste [kg] | Masse CAD [kg] | Stufe |
|---|---|---|---|---|---|---|
| 600.1 | Kühlplatte (Blech 1/4/1 mm, Mäander 8 Bahnen laengs, Teilkanal 8 mm) | 2 | 2 | 47.4453 | 47.4453 | K |
| | **Summe Stückliste** | | | **47.445** | | |

## Querschnitte, Werkstoffe, Hinweise aus der Stückliste
- 600.1: Werkstoff Al-Blech 1/4/1 mm gelötet (hohl, ENT-152…156); Herkunft Masse: G5-CAD (cad/baukasten/ausgabe/ergebnis_LFP.json)

## Akten (aus der Stückliste)
ENT-089, ENT-090, ENT-104, ENT-105, ENT-106, ENT-152, ENT-153, ENT-154, ENT-155, ENT-156, ENT-158, ENT-159

## Quellen
`pm/bauteile/struktur.json`, `pm/bauteile/parameter_LFP.json`, `pm/bauteile/stueckliste_LFP.json`, `cad/baukasten/ausgabe/ergebnis_LFP.json` (CAD-Stand: Stückliste 0.3, 1347 Teile)

---
*KI-generiert (Claude Sonnet, 2026-11-23). Status Entwurf. Freigabe nur durch den Autor.*
