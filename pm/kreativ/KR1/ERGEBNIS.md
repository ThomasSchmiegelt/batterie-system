| Dok.-Nr. | BAT-KR-E1 | Version | 0.3 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Ergebnis KR1 Lauf 3: Zellausgleich NMC (Festforderung, Kriteriendefinitionen) | Ersteller | Claude Sonnet (KI), im Auftrag von Opus | Prüfer | Opus (Rohdaten, Stichprobe Paarurteile), offen |

> **KI-generiert (Claude Sonnet, 2026-11-24).** Urteile stammen von PI (qwen-gross, lokal, ohne Werkzeuge): Einschätzungen, keine Rechnungen. Gewichte: Autor, 2026-11-24. Grundlage: `PRUEFUNG_OPUS.md` (Prüfung Lauf 2, Vorgabe Lauf 3), `pm/kreativ/METHODE.md` (unverändert). Lauf 1 in `KR1/lauf1/`, Lauf 2 in `KR1/lauf2/`, unverändert.

## Was getan wurde
- `kreativ.py`: Festforderungen (`ausschluss_fest.json`, Konzepte scheiden vor dem Paarvergleich aus) und Kriteriendefinitionen im Prompt (`problem.json`, `kriteriendefinitionen`). Neu urteilen nur die Kriterien in `neu_urteilen`, die übrigen kommen aus `lauf2/paare.json` (im Paarurteil mit `uebernommen: true` markiert).
- **Ausgeschieden vor dem Vergleich** (Festforderung Platinentemperatur ≤ 105 °C bei 45 °C Umgebung, B-BAT-051):
  - K1 (Ist-Entwurf): Platine 111,9 °C bei h = 10 W/m²K (`sim/elektrik/e3_platine/ergebnis_waerme.json`, NMC, `T_h10_C`).
  - K3 (getaktet in Ruhe): bei 260 mA und 50 % Takt doppelte mittlere Verlustleistung, Spitze etwa 39 W je CMU (Rechnung Opus, `PRUEFUNG_OPUS.md` Punkt 1).
- Neu geurteilt: **Reifegrad** und **Fehlermöglichkeiten** über K2, K4, K5, K6 (6 Paare × 2 Reihenfolgen = 12 Aufrufe) mit den Definitionen aus der Vorgabe (Reife: Verbreitung in Serien-BMS von Pkw, nicht Projektstand; Fehler: neue Fehlerarten mit Bezug FSR-01/02/06, Temperatur ausgeschlossen). Nachfragen: 1 Fall in Runde 1, 1 Fall in Runde 2 (K5/K6 bei Fehlern).
- Übernommen aus Lauf 2: Ausgleichszeit, Wärme, Kosten, Bauraum, Wirkungsgrad (für K2, K4, K5, K6).
- Lauf: Scope `hermes-batterie-kr1c`, 10:44 bis 10:49 Uhr, GPU vor jedem Aufruf geprüft (nur ollama).
- Hinweis: Nur 4 Konzepte bleiben im Vergleich (Methode nennt 5 bis 8 für die Auswahl; die Festforderung unterschreitet das).

## Rang (`rang.json`, `rang.png`)
| Platz | Konzept | Punkte Gewichte Autor | Spanne ±1 | Punkte gleiche Gewichte |
|---|---|---|---|---|
| 1 | K6 aktiv kapazitiv | 0,563 | 0,555 bis 0,572 | 0,524 (Platz 2 gleichauf mit K4) |
| 2 | K2 Ist mit Wärmepfad | 0,544 | 0,531 bis 0,557 | 0,560 (Platz 1) |
| 3 | K4 Wärme auf Kühlplatte | 0,472 | 0,459 bis 0,484 | 0,524 |
| 4 | K5 aktiv induktiv | 0,421 | 0,411 bis 0,430 | 0,393 |

- **K6 und K2 liegen 0,019 auseinander, die ±1-Spannen überlappen.** Mit gleichen Gewichten führt K2. Bei ±1 ist Platz 1 K2 oder K6, in den Grenzvarianten (Gewicht 0 oder 12) zusätzlich K4 (Bauraum 12). Platz 1 ist nicht belastbar.
- Punkte je Kriterium (`punkte_je_kriterium`): K2 Kosten 1,00, Reife 1,00, Fehler 0,92, Wärme 0,00, Zeit 0,17, Wirkungsgrad 0,17; K6 Wärme 0,92, Zeit 0,83, Wirkungsgrad 0,92, Kosten 0,25, Reife 0,25, Fehler 0,25; K4 Bauraum 1,00; K5 Zeit 0,83, Kosten 0,08, Reife 0,08, Fehler 0,17.

**Konsistenz** (`rang.json`, `konsistenz`, `position`):
- Zirkuläre Triaden: **0** (Lauf 2: 3). Kendall ζ 1,0 in allen Kriterien. Ziel erreicht.
- Widersprüche zwischen den Reihenfolgen: 1 von 42 Paar/Kriterium-Fällen (K5/K6 bei Fehlern, nach zwei Nachfragen).
- Positionsneigung: erste Nennung gewinnt 36, zweite 36, gleich 12 von 84. Keine Neigung.
- Zahlenprüfung: 0 Verstöße (`zahlverstoesse` leer).

## Abgleich gegen die Prüfung Lauf 2 (PRUEFUNG_OPUS.md)
| Befund Lauf 2 | Lauf 3 |
|---|---|
| 3: Fehlermöglichkeiten zählten die 105 °C doppelt, daher 3 Zirkel | **Behoben.** Mit der Definition (Temperatur ausgeschlossen) 0 Zirkel. Durchsicht der 12 Fehler-Begründungen: keine nennt die Temperaturgrenze oder 105 °C; drei (K2|K4, K4|K2, K6|K4) erwähnen „Temperatursensor“ bzw. „thermisches Pad“ als Bauteil, das ist zulässig (Fehlerart eines Bauteils). |
| 2: Reifegrad als Projektstand gelesen | **Behoben im Sinn der Definition.** Begründungen nennen die Verbreitung in Serien-BMS: Passiv am verbreitetsten (K2 1,00, K4 0,67), aktiv selten. **Aber:** PI urteilt widersprüchlich über aktiv kapazitiv: bei K5|K6 „Standard in Pkw-BMS (z. B. Infineon, TI)“, bei K6|K2 „nur Nischen-Toplevel-Designs“. Das ist Wissen ohne Beleg und ohne Zahl, die Reife von K5 und K6 ist nicht belegt. Eine Begründung enthält chinesische Zeichen („少数“). |
| 4: K1 hätte nicht bewertet werden dürfen | **Umgesetzt.** K1 und K3 scheiden vor dem Vergleich aus (`ausschluss_fest.json`). |
| 6: K2 vorn, bleibt bei ±1 vorn; K6 knapp dahinter | **Teilweise geändert.** Mit den Gewichten des Autors führt jetzt K6 (0,563) vor K2 (0,544), der Abstand liegt in der ±1-Spanne. Mit gleichen Gewichten führt K2. Die Spitze ist ein Gleichstand. |

## Vorschlag Alternativen-Tabelle ENT-146 (nur Vorschlag, Akte nicht geändert)
| Alternative | Urteil (PI, Gewichte Autor) |
|---|---|
| K1 Ist-Entwurf (passiv, Konvektion) | ausgeschieden: Festforderung 105 °C verfehlt (111,9 °C, `ergebnis_waerme.json`) |
| K3 getaktet in Ruhe, 260 mA | ausgeschieden: Verlustleistung verdoppelt, Festforderung verfehlt |
| K6 aktiv kapazitiv | Platz 1, 0,56. Beste Wärme, Zeit, Wirkungsgrad; Kosten, Reife, Fehler schwach (je 0,25) |
| K2 passiv mit Wärmeleitpad | Platz 2, 0,54 (mit gleichen Gewichten Platz 1). Billig, reif, wenig Fehlerarten; Wärme (0,00) und Zeit (0,17) schwach, Wärme erst durch das Pad erfüllt (kein PI-Maß, Elmer E3b offen) |
| K4 Wärme ausgelagert | Platz 3, 0,47 |
| K5 aktiv induktiv | Platz 4, 0,42 |
Spitze K6/K2 ist knapp; die Abwägung hängt am Gewicht von Wirkungsgrad, Reife und Kosten. Opus entscheidet nach der Stichprobe.

## Offen für Opus
1. Stichprobe, besonders Reifegrad aktiv kapazitiv gegen induktiv (widersprüchlich) und die Wärme für K2 (0,00 gegen K6: ob das Wärmeleitpad im Urteil berücksichtigt wird, ist aus `punkte_je_kriterium` nicht ablesbar, Lauf-2-Urteile unverändert übernommen).
2. Eine belegte Quelle für die Reife der aktiven Ausgleichsprinzipien (Recherchebeauftragung); bis dahin ist Reife kapazitiv/induktiv Wissen der KI ohne Beleg.
3. Ob 4 Konzepte reichen oder ein weiteres Konzept (z. B. K2 mit größerer Platine) aufgenommen wird.
4. Lizenz der TRIZ-Matrix (zweite Quelle ungeklärt, nur privat).

---
*KI-generiert (Claude Sonnet, 2026-11-24). Status Entwurf. Freigabe nur durch den Autor.*
