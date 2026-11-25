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
| 2026-11-25 | Recherche W51/W48/W35 (modelltest.sh) | 35–59 s je Thema (qwen lokal ≈ 140 s), ≈ 155 Token/s, ≈ 90 % der Ausgabe Reasoning. Zitate 4/2/7 bestätigt, **0 falsch** (qwen 9/11/9, 1 falsch). URL ohne Klammern → Formatvorgabe verfehlt, Rohprüfung zeigte 0 | Zitattreue sehr gut, Formattreue schwach, belegt weniger Werte als qwen. Skript normalisiert jetzt und zählt roh getrennt |
| 2026-11-25 | Buch 14c-Fortsetzung (Sonnet steuert) | 11 202 Zeichen in 7 Abschnitten. Zahlen 99/101 → nach 1 Wiederholung 103/103 mit Fundstelle. **8 von 18 Aufrufen leer** (105–126 s), deshalb Abschnitte geteilt und Kontext verkleinert | Zahlentreue sehr gut. **Stil unbrauchbar als Buchtext:** Aneinanderreihung von Kurzsätzen mit Klammer nach fast jedem Satz, teils sinnentstellt („Sonnet rechnete in 2 min“). Zuschreibungsfehler: „Der Autor legte 16 Akten an“ (die KI legte sie an). Eignung: Faktengerüst, kein Fließtext |
| 2026-11-25 | Video-Storyboard | Lauf 1 leer, Lauf 3 (nach Nachtrag) 109 s, alle 6 Szenen. 4 Fehler gestrichen: „SPFM 99,00 %“ (Ziel statt Ergebnis), „Teile 244“ (Summe nicht in den Daten) | Struktur gut, Zahlen müssen geprüft werden, verwechselt Ziel und Ergebnis |
| 2026-11-25 | Wächter W1 (CMU-Routing) | 13 Entscheidungen, JSON 13/13 gültig, Erlaubtliste 13/13 eingehalten, 8–42 s und 1 739–6 157 Token je Aufruf. 7 Neustarts, Ziel nicht erreicht. B4v zweimal nach 1–2 Pässen abgebrochen, B3/B2K nie versucht | Formal zuverlässig, inhaltlich ungeduldig (bricht vor dem Trend ab). Empfehlung: Mindestlaufzeit vor dem Neustart fest im Wächter |

**Neutraler Bericht:** `bericht/Bericht_Modelltest_Kolibri-1.md` (+ PDF), ohne Personen- und Projektdaten (Vorgabe Autor 2026-11-25).
| 2026-11-25 | Buch 14c, Versuch 2 mit Stilvorgabe (Haiku steuert) | 10 432 Zeichen, 7 Abschnitte, 37–75 s je Aufruf, **0 leer** (kleinere Eingaben). Absatzprüfung Opus: 60/60 Zahlen in den genannten MB2-Zeilen (der Satzprüfer meldete 38 „ohne Klammer“, weil er Absatz-Fundstellen nicht liest) | **Deutlich besser lesbar**, zusammenhängende Absätze. Fehler: (1) erfundene Personenangabe „ohne Ingenieursabschluss“ (steht nirgends), (2) Perspektive springt zwischen „der Autor“ und „ich“, (3) Zahlen als Wort („acht“, „sieben“) entgehen der Prüfung. Eignung: Rohfassung zum Überarbeiten |
| 2026-11-25 | Vergleich: Qwen 3.8 27B über Franconia, Recherche W51/W48/W35 (gleiche Pakete, gleiches Prüfskript) | 302–395 s je Thema (Kolibri 35–59 s, Qwen 3.5 lokal ≈ 140 s); **38 Zitate, 1 falsch** (Kolibri 13/0, Qwen 3.5 lokal 29/1); Format ohne Nachbearbeitung erkannt | Qwen 3.8 liefert fast 3× so viele belegte Werte wie Kolibri bei gleicher Fehlerquote, ist aber 6–8× langsamer. Für Recherche Qwen 3.8, für schnelle Extraktion Kolibri |
