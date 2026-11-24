| Dok.-Nr. | BAT-KR-V2 | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | KR2: Trennen gegen Verfügbarkeit (SG-01/03 gegen SG-05), Vorgabe Opus | Ersteller | Claude Opus (KI) | Prüfer | – |

> KI-generiert (Claude Opus, 2026-11-24). Methode: `pm/kreativ/METHODE.md` (mit den Korrekturen aus KR1). Regel „erst konservativ“.

## Problem
Die HARA (`docs/24`) verlangt zweierlei: Bei Überladung bzw. Übertemperatur trennen (SG-01 ASIL D, SG-03 ASIL C, FTTI 1 s), aber während der Fahrt nicht unerwartet trennen (SG-05 ASIL B). TRIZ: verbessern „Zuverlässigkeit/Sicherheit“, verschlechtern „Verfügbarkeit/Anpassungsfähigkeit“.
**Nicht im Umfang:** Kurzschluss (SG-04). Dort trennt immer die Sicherung bzw. das Schütz sofort, eine Vorwarnung ist unmöglich.

## Festforderung (Stufe 5b)
Die **erste sichere Reaktion** (Leistung begrenzen oder trennen) erfolgt innerhalb der FTTI von 1 s (SG-01/03). Eine Vorwarnung **vor dem vollständigen Trennen** ist nur zulässig, wenn innerhalb von 1 s gedrosselt wird.

## Kasten
| Zeile | Ausprägungen |
|---|---|
| T1 Stufen | 1 eine Schwelle → trennen · 2 Warnung → trennen · 3 drosseln → warnen → trennen |
| T2 Plausibilisierung | 1 einkanalig (1oo1) · 2 zweikanalig, einer genügt (1oo2) · 3 Mehrheit (2oo3) |
| T3 Reaktionsweg | 1 nur Software BMS · 2 Software + unabhängiger Hardwarepfad (Sekundärschutz, FSR-06) |
| T4 Ausmaß | 1 sofort ganzes Pack · 2 abgestuft: Laden sperren bzw. Leistung 0 per CAN, dann Schütze |
| T5 Vorwarnung an Fahrer | 1 keine · 2 ≥ 2 s (FSR-07) · 3 ≥ 10 s Notlauf mit gedrosselter Leistung |

| Konzept | Leitidee | T1 | T2 | T3 | T4 | T5 |
|---|---|---|---|---|---|---|
| K1 | Ist (HARA-FSR): gestuft, 1oo2, Hardwarepfad | 3 | 2 | 2 | 2 | 2 |
| K2 | einfach hart: sofort trennen | 1 | 1 | 1 | 1 | 1 |
| K3 | verfügbarkeitsorientiert: Mehrheit, Notlauf | 3 | 3 | 2 | 2 | 3 |
| K4 | sicherheitsmaximal: 1oo2, Hardwarepfad, ganzes Pack | 2 | 2 | 2 | 1 | 2 |
| K5 | Mehrheit ohne Hardwarepfad | 3 | 3 | 1 | 2 | 2 |

## Kriterien und Definitionen (für den Prompt)
- **Sicherheit:** Wie sicher werden Überladung und Übertemperatur beherrscht (Abdeckung, Unabhängigkeit, ASIL D für SG-01)?
- **Verfügbarkeit:** Wie selten trennt das System während der Fahrt unerwartet (Fehlauslösung, Vorwarnung, Notlauf)?
- **Kosten:** Bauteile und Kanäle.
- **Nachweisaufwand:** Aufwand für FMEDA, Software-ASIL, Unabhängigkeitsnachweis.
- **Reifegrad:** Verbreitung des Prinzips in Serien-BMS (nicht der Projektstand).

## Gewichte des Autors (2026-11-24, im Chat, 10 Paare)
Ziffern 1–10 (Reihenfolge Sicherheit, Verfügbarkeit, Kosten, Nachweisaufwand, Reifegrad, Dreiecksmatrix zeilenweise): `2 2 2 2 2 2 2 1 0 1`. Punkte: Sicherheit 8, Verfügbarkeit 6, Reifegrad 3, Nachweisaufwand 2, Kosten 1 (Summe 20).

## Erwartung Opus (vorher)
- Alle Konzepte erfüllen die Festforderung, auch K3, weil gedrosselt wird.
- K2 verliert bei der Verfügbarkeit deutlich (jede Fehlmessung → Liegenbleiben). Bei der Sicherheit gewinnt es kaum gegen K1/K4, denn ihm fehlt der Hardwarepfad.
- **K1 vorn**, K4 knapp dahinter (höhere Sicherheit, weniger Verfügbarkeit). K3 gewinnt bei der Verfügbarkeit, verliert bei Kosten und Nachweisaufwand (dritter Kanal). K5 verliert bei der Sicherheit, weil der Hardwarepfad fehlt.
- Das Ergebnis ist robust, weil Sicherheit und Verfügbarkeit zusammen 70 % wiegen.
