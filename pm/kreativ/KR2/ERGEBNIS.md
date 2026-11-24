| Dok.-Nr. | BAT-KR-E2 | Version | 0.1 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Ergebnis KR2: Trennen gegen Verfügbarkeit (SG-01/03 gegen SG-05) | Ersteller | Claude Sonnet (KI), im Auftrag von Opus | Prüfer | Opus (Rohdaten, Stichprobe Paarurteile), offen |

> **KI-generiert (Claude Sonnet, 2026-11-24).** Urteile stammen von PI (qwen-gross, lokal, ohne Werkzeuge): Einschätzungen, keine Rechnungen. Gewichte: Autor, 2026-11-24 im Chat, übertragen. Grundlage: `VORGABE_OPUS.md` (Kasten, Konzepte, Festforderung, Kriteriendefinitionen, Erwartung), `pm/kreativ/METHODE.md` (unverändert).

## Was getan wurde
- Eingaben aus der Vorgabe unverändert: `kasten_vorgabe.json`, `konzepte_vorgabe.json`, `problem.json` (Fakten F1 bis F5 nur aus `docs/24_gefahrenanalyse_hara.md` und `sim/elektrik/e3d_fmeda/ergebnis.json`), Kriteriendefinitionen im Prompt.
- TRIZ: verbessern Parameter 27 (Zuverlässigkeit), verschlechtern 35 (Anpassungsfähigkeit); Matrixzelle 27-35 liefert 13 Umkehren, 35 Parameter ändern, 8 Gegengewicht, 24 Vermittler, je 2 bis 3 Ideen von PI (`triz.json`).
- Kasten: 5 Zeilen, Konzepte K1 bis K5, min. Hamming 2, 0 Ausschlussverstöße (`konzepte.json`).
- Festforderung (`ausschluss_fest.json`): nach Vorgabe erfüllen alle 5 Konzepte sie, keines scheidet aus. Siehe Kopfstand: PI hält die 2-s-Warnphase bei K4 und K5 für einen Verstoß gegen FTTI 1 s. Das ist ein Lesefehler gegen die Festforderung (gedrosselt wird innerhalb 1 s), Opus prüft.
- Kopfstand je Konzept, 3 Versagensarten (`kopfstand.json`): K1 Common Cause AFE/Sekundärschutz, Schütz verschweißt, CAN-Ausfall; K2 Falschauslösung, kein Hardwarepfad, Überreaktion; K3 2oo3 mit nur zwei unabhängigen Pfaden, 10 s Notlauf, CAN-Ausfall; K4 Falschauslösung 1oo2, Zeitkonflikt, ganzes Pack; K5 Softwarehänger ohne Hardwarepfad, Zeitkonflikt, Fehlalarm. Ungeprüfte PI-Vorschläge, Kandidaten für `docs/05`. Ein Schlüssel in K2 ist von PI falsch geschrieben („versachen“), Inhalt lesbar.
- Paarurteile: 10 Paare × 2 Reihenfolgen = 20 Aufrufe, je Aufruf alle 5 Kriterien, 2 Nachfragerunden (11 Paar-Fälle). Scope `hermes-batterie-kr2`, 14:27 bis 14:55 Uhr, GPU vor jedem Aufruf geprüft (nur ollama).
- Gewichte (`gewichte.json`, Formular `gewichte_formular.md`, Vermerk „Autor im Chat, übertragen“): Sicherheit 8, Verfügbarkeit 6, Reifegrad 3, Nachweisaufwand 2, Kosten 1 (Summe 20), Ziffern `2 2 2 2 2 2 2 1 0 1`.
- Werkzeug: in `kreativ.py` eine Zeile, der TRIZ-Prompt nimmt den Gegenstand aus `problem.json` (`triz_gegenstand`), Standard unverändert Zellausgleich (KR1 bleibt gleich).

## Rang (`rang.json`, `rang.png`)
| Platz | Konzept | Punkte Gewichte Autor | Spanne ±1 | Punkte gleiche Gewichte |
|---|---|---|---|---|
| 1 | K1 Ist (HARA-FSR) | 0,731 | 0,714 bis 0,750 | 0,637 (Platz 1) |
| 2 | K3 verfügbarkeitsorientiert | 0,609 | 0,580 bis 0,641 | 0,463 (Platz 3) |
| 3 | K4 sicherheitsmaximal | 0,603 | 0,586 bis 0,622 | 0,600 (Platz 2) |
| 4 | K5 Mehrheit ohne Hardwarepfad | 0,425 | 0,408 bis 0,441 | 0,450 |
| 5 | K2 einfach hart | 0,131 | 0,086 bis 0,173 | 0,350 |

- Platz 1 K1 bleibt bei jeder ±1-Variante Platz 1. In den Grenzvarianten (Gewicht 0 oder 12) führen K3 (Sicherheit 0 oder Verfügbarkeit 12) und K4 (Nachweisaufwand 12). K3 und K4 liegen 0,006 auseinander, Platz 2 ist nicht unterscheidbar.
- Punkte je Kriterium (`punkte_je_kriterium`), K1: Sicherheit 0,94, Reife 1,00, Verfügbarkeit 0,50, Kosten 0,38, Nachweis 0,38. K3: Verfügbarkeit 1,00, Kosten 0,00, Nachweis 0,25, Sicherheit 0,50. K4: Sicherheit 0,81, Nachweis 0,75, Verfügbarkeit 0,25. K5: Sicherheit 0,25, Reife 0,12. K2: Kosten 1,00, Nachweis 0,62, Sicherheit 0,00, Verfügbarkeit 0,00.

**Konsistenz** (`rang.json`, `konsistenz`, `position`, `zahlverstoesse`):
- Zirkuläre Triaden: **1** (Nachweisaufwand: K2 > K5 > K4 > K2), nach zwei Nachfragen nicht behoben. Ziel 0 verfehlt. Kendall ζ 1,0 bei Sicherheit, Verfügbarkeit, Kosten, Reife, 0,8 bei Nachweisaufwand.
- Widersprüche zwischen den Reihenfolgen: 4 von 100 Fällen (Kosten K1/K5; Nachweisaufwand K1/K5, K2/K3, K3/K5). Alle in den mittleren Rängen, Platz 1 nicht betroffen.
- Positionsneigung: erste Nennung gewinnt 47, zweite 49, gleich 4 von 100. Keine Neigung.
- Zahlenprüfung: 4 Verstöße von 100 (falsche Fundstelle: 3 × „2“ gegen F4 statt F3, 1 × „10“ gegen F3). Die Zahlen stammen sinngemäß aus den Fakten, die Fundstelle stimmt nicht.
- Eine Begründung enthält ein chinesisches Wort („少见“, K5|K4 Reifegrad).

## Abgleich gegen die Erwartung Opus (`VORGABE_OPUS.md`)
| Erwartung | Befund |
|---|---|
| Alle Konzepte erfüllen die Festforderung | Nach Vorgabe ja. PI sieht bei K4/K5 im Kopfstand einen Zeitkonflikt (Warnphase 2 s gegen FTTI 1 s), das widerspricht der Festforderung. Opus prüft. |
| K2 verliert deutlich bei Verfügbarkeit | **Bestätigt**: 0,00. Bei Sicherheit ebenfalls 0,00 (nicht „kaum Gewinn“, sondern klar letzter). K2 gewinnt nur bei Kosten (1,00). Gesamt 0,131, letzter Platz auch bei gleichen Gewichten (0,350). |
| K1 vorn, K4 knapp dahinter | **Teilweise.** K1 vorn (0,731) bestätigt, robust bei ±1. Platz 2 aber K3 (0,609) vor K4 (0,603), ununterscheidbar (Spannen überlappen). Bei gleichen Gewichten K4 vor K3. |
| K3 gewinnt Verfügbarkeit, verliert Kosten und Nachweisaufwand | **Bestätigt**: Verfügbarkeit 1,00, Kosten 0,00, Nachweis 0,25. |
| K5 verliert bei Sicherheit (fehlender Hardwarepfad) | **Bestätigt**: 0,25 (nur K2 niedriger), Gesamt Platz 4. |
| Ergebnis robust, weil Sicherheit und Verfügbarkeit 70 % wiegen | **Für Platz 1 bestätigt** (nur K1 bei ±1, 0,731 gegen 0,609). Nicht für Platz 2 und 3. Grenzvarianten Sicherheit 0 und Verfügbarkeit 12 setzen K3 nach vorn. Hinweis: Sicherheit 8 plus Verfügbarkeit 6 sind 14 von 20 Punkten, also 70 %. |

## Vorschlag Alternativen-Tabelle der Akte (nur Vorschlag, noch keine Akte)
| Alternative | Urteil (PI, Gewichte Autor) |
|---|---|
| K1 Ist: gestuft (drosseln, warnen, trennen), 1oo2, Hardwarepfad, abgestuft, Vorwarnung ≥ 2 s | gewählt, Platz 1, 0,73. Sicherheit 0,94, Reife 1,00; Verfügbarkeit 0,50, Kosten und Nachweisaufwand je 0,38 |
| K3 mit 2oo3 und Notlauf ≥ 10 s | Platz 2, 0,61. Beste Verfügbarkeit (1,00), teuerste Variante (Kosten 0,00); ein dritter unabhängiger Messweg ist in FSR-01 nicht vorgesehen (PI-Kopfstand) |
| K4 sicherheitsmaximal: ganzes Pack sofort | Platz 3, 0,60. Sicherheit 0,81, Nachweis 0,75, Verfügbarkeit 0,25 |
| K5 Mehrheit ohne Hardwarepfad | Platz 4, 0,43. Sicherheit 0,25, weil der Hardwarepfad (FSR-06) fehlt |
| K2 sofort trennen, eine Schwelle | Platz 5, 0,13. Billig (1,00), aber Sicherheit 0,00 und Verfügbarkeit 0,00 |
Die Entscheidung für K1 stützt sich auf Platz 1 bei jeder ±1-Gewichtsvariante und bei gleichen Gewichten. Opus entscheidet nach der Stichprobe.

## Offen für Opus
1. Zirkel in Nachweisaufwand (1 Triade, ζ 0,8 nach zwei Nachfragen), Ziel 0 nicht erreicht. Ohne weitere Nachfragen gelassen (Auftrag: höchstens zwei).
2. Kopfstand K4/K5 nennt die 2-s-Warnphase als FTTI-Verstoß: Festforderung widerspricht dem. Prüfen, ob die Konzeptbeschreibung im Prompt (Stufe „Warnung → trennen“ in K4) missverständlich ist.
3. Stichprobe Paarurteile, besonders Kosten und Nachweisaufwand K1/K5 und K2/K3 (widersprüchlich).
4. Die Reife (K1 1,00) ist Wissen der KI ohne Beleg; eine belegte Quelle fehlt.
5. Fundstellen der Zahlen in 4 Urteilen (siehe oben) falsch.
6. Eingriff in `kreativ.py`: eine Zeile (`triz_gegenstand`), Rückmeldung an Opus.

---
*KI-generiert (Claude Sonnet, 2026-11-24). Status Entwurf. Freigabe nur durch den Autor.*
