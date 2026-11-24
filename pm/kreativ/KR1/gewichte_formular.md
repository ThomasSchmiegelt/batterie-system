| Dok.-Nr. | BAT-KR-F1 | Version | 0.1 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Gewichte der Kriterien: Paarvergleich (Zellausgleich NMC) | Ersteller | Claude Sonnet (KI), im Auftrag von Opus | Prüfer | Autor |

> **Ausgefüllt vom Autor 2026-11-24 im Chat, übertragen von Sonnet.** Die Summen (Gewichte) stehen in `gewichte.json`.
>
> **KI-generiert (Claude Sonnet, 2026-11-24).** Die Gewichte setzt der Autor (Abwägung). Lauf 2 rechnet mit den Gewichten des Autors, gleiche Gewichte nur als Vergleich.

## So füllen Sie aus
Je Zeile ein Kriterienpaar. Tragen Sie ein: **2**, wenn das Kriterium links wichtiger ist, **1**, wenn beide gleich wichtig sind, **0**, wenn das Kriterium rechts wichtiger ist. Die Summe je Kriterium (0 bis 12) wird sein Gewicht. Danach `KR1/gewichte.json` im Format `{"gewichte": {"Kriterium": Zahl, ...}, "von": "Autor"}` ablegen.

| Nr | Kriterium links | Kriterium rechts | Eintrag (2 / 1 / 0) |
|---|---|---|---|
| 1 | Ausgleichszeit | Wärme in der CMU | 0 |
| 2 | Ausgleichszeit | Kosten | 1 |
| 3 | Ausgleichszeit | Bauraum | 1 |
| 4 | Ausgleichszeit | Fehlermöglichkeiten (FSR, HARA) | 0 |
| 5 | Ausgleichszeit | Wirkungsgrad | 0 |
| 6 | Ausgleichszeit | Reifegrad | 0 |
| 7 | Wärme in der CMU | Kosten | 2 |
| 8 | Wärme in der CMU | Bauraum | 2 |
| 9 | Wärme in der CMU | Fehlermöglichkeiten (FSR, HARA) | 1 |
| 10 | Wärme in der CMU | Wirkungsgrad | 0 |
| 11 | Wärme in der CMU | Reifegrad | 0 |
| 12 | Kosten | Bauraum | 1 |
| 13 | Kosten | Fehlermöglichkeiten (FSR, HARA) | 1 |
| 14 | Kosten | Wirkungsgrad | 0 |
| 15 | Kosten | Reifegrad | 0 |
| 16 | Bauraum | Fehlermöglichkeiten (FSR, HARA) | 0 |
| 17 | Bauraum | Wirkungsgrad | 0 |
| 18 | Bauraum | Reifegrad | 0 |
| 19 | Fehlermöglichkeiten (FSR, HARA) | Wirkungsgrad | 1 |
| 20 | Fehlermöglichkeiten (FSR, HARA) | Reifegrad | 1 |
| 21 | Wirkungsgrad | Reifegrad | 2 |

Kriterien (7), Paare: 21.

---
*KI-generiert (Claude Sonnet, 2026-11-24). Status Entwurf. Freigabe nur durch den Autor.*
