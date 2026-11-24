| Dok.-Nr. | BAT-KR-F1 | Version | 0.1 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Gewichte der Kriterien: Paarvergleich (Trennen gegen Verfügbarkeit (SG-01/03 gegen SG-05)) | Ersteller | Claude Sonnet (KI), im Auftrag von Opus | Prüfer | Autor |

> **Ausgefüllt vom Autor 2026-11-24 im Chat (Ziffern in VORGABE_OPUS.md), übertragen von Sonnet. Vermerk: Autor im Chat, übertragen.** Die Summen stehen in `gewichte.json`.
>
> **KI-generiert (Claude Sonnet, 2026-11-24).** Die Gewichte setzt der Autor (Abwägung). **Bis zu seiner Antwort rechnet das Skript mit gleichen Gewichten. Das Ergebnis ist deshalb vorläufig.**

## So füllen Sie aus
Je Zeile ein Kriterienpaar. Tragen Sie ein: **2**, wenn das Kriterium links wichtiger ist, **1**, wenn beide gleich wichtig sind, **0**, wenn das Kriterium rechts wichtiger ist. Die Summe je Kriterium (0 bis 12) wird sein Gewicht. Danach `KR2/gewichte.json` im Format `{"gewichte": {"Kriterium": Zahl, ...}, "von": "Autor"}` ablegen.

| Nr | Kriterium links | Kriterium rechts | Eintrag (2 / 1 / 0) |
|---|---|---|---|
| 1 | Sicherheit | Verfügbarkeit | 2 |
| 2 | Sicherheit | Kosten | 2 |
| 3 | Sicherheit | Nachweisaufwand | 2 |
| 4 | Sicherheit | Reifegrad | 2 |
| 5 | Verfügbarkeit | Kosten | 2 |
| 6 | Verfügbarkeit | Nachweisaufwand | 2 |
| 7 | Verfügbarkeit | Reifegrad | 2 |
| 8 | Kosten | Nachweisaufwand | 1 |
| 9 | Kosten | Reifegrad | 0 |
| 10 | Nachweisaufwand | Reifegrad | 1 |

Kriterien (5), Paare: 10.

---
*KI-generiert (Claude Sonnet, 2026-11-24). Status Entwurf. Freigabe nur durch den Autor.*
