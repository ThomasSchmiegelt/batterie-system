| Dok.-Nr. | BAT-DOC-26 | Version | 0.1 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Modelltest Kolibri 1 (Aleph Alpha) im Projektablauf: Einsatz, Messwerte, Bewertung | Ersteller | Claude Opus (KI) | Prüfer | – (Autor offen) |

> KI-generiert (Claude Opus, 2026-11-25). Auftrag Autor 2026-11-25: „ich möchte in unserem ablauf dieses Modell testen … es soll exzessiv genutzt und gemonitort werden, was es so kann, also im technischen, und es soll das Buch schreiben“; „was kolibri macht soll dokumentiert werden.“

## 1 Modell und Zugang
| Punkt | Stand |
|---|---|
| Modell | Kolibri 1, Aleph Alpha (Heidelberg), MoE 78B gesamt / 3,5B aktiv, Reasoning, DE/EN (Angabe Autor) |
| Zugang | Franconia, `https://api.franconia.ai/v1` (OpenAI-kompatibel), Modell-ID `Kolibri 1`. Der Server meldet `kolibri-1-fp8` |
| Einbindung | PI-Anbieter `franconia` in `~/.pi/agent/models.json` (`compat.supportsDeveloperRole: false`), Schlüssel aus `FRANCONIA_API_KEY` per `--api-key` |
| Lokal | nicht möglich (RTX 3090 24 GB, Modell FP8 ≈ 78 GB, Platte 22 GB frei) |
| Einrichtungsfehler | (1) PI liest die Umgebungsvariable nicht → `--api-key`. (2) Rolle `developer` abgelehnt (HTTP 422) → compat. (3) Opus rief PI ohne `< /dev/null` auf, PI wartete auf stdin, das sah aus wie ein Hänger |

## 2 Wo Kolibri eingesetzt wird
| Prozess | Aufgabe | Werkzeug | Prüfung |
|---|---|---|---|
| Recherche (technisch) | Pakete W51, W48, W35 neu, Vergleich mit qwen-gross | `forschung/modelltest.sh` → `forschung/modelltest/kolibri/` | `pruefe.py` (Zitate wörtlich), Opus liest Aussagen |
| Buch | Batteriekapitel fortschreiben aus Material MAT-batterie-nov2 | Auftrag Buch B-K1 | Fundstellen gegen MAT, Opus Stichprobe |
| geplant | Bauteilgespräch (`pm/gespraech.sh`), Kopfstand/Paarurteile in KR-Sitzungen, Zweitmeinung zu Berichten | PI-Schalter | wie bisher |

## 3 Monitoring
Jeder Lauf: eine Zeile in `forschung/modelltest/monitoring.csv` (Datum, Modell, Thema, Dauer, Zeichen, Belege ok/Fehler, Abbruch). Jede Verteilung zusätzlich in `docs/08`, mit „PI (Kolibri)“.

## 4 Beobachtungen (laufend, neueste unten)
| Datum | Test | Ergebnis | Bewertung Opus |
|---|---|---|---|
| 2026-11-25 | Fachfrage Vorladung 912 V / 1 mF (curl) | 416 J richtig. Begründung „Überspannung“ falsch, richtig ist Einschaltstrom. 0 Reasoning-Token, < 1 s | Rechnung gut, Begründung unscharf |
| 2026-11-25 | dieselbe Frage über PI | Begründung richtig (Einschaltstrom begrenzen), 1 s | gut |
