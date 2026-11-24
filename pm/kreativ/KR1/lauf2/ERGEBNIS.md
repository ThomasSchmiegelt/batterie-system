| Dok.-Nr. | BAT-KR-E1 | Version | 0.2 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Ergebnis KR1 Lauf 2: Zellausgleich NMC (Kasten und Konzepte von Opus, Gewichte vom Autor) | Ersteller | Claude Sonnet (KI), im Auftrag von Opus | Prüfer | Opus (Rohdaten, Stichprobe Paarurteile), offen |

> **KI-generiert (Claude Sonnet, 2026-11-24).** Urteile stammen von PI (qwen-gross, lokal, ohne Werkzeuge): Einschätzungen, keine Rechnungen. Gewichte: Autor, 2026-11-24 im Chat. Grundlage: `PRUEFUNG_OPUS.md`, `pm/kreativ/METHODE.md` (unverändert). Lauf 1 (nur Werkzeugerprobung, keine Grundlage für eine Akte) liegt unverändert in `KR1/lauf1/`.

## Was getan wurde
- `kreativ.py` erweitert: `kasten_vorgabe.json` und `konzepte_vorgabe.json` werden unverändert übernommen. Das Skript prüft nur Ausschlüsse, Anzahl 5 bis 8 und Hamming-Abstand (`konzepte.json`, `pruefung`). Rang-Bild zeigt zusätzlich das Ergebnis mit gleichen Gewichten (Rauten, `rang.json`, `vergleich_gleiche_gewichte`).
- Kasten T1 bis T5 und Konzepte K1 bis K6 wie in PRUEFUNG_OPUS.md. Ausschlüsse (6 Paare, Vorschlag Sonnet) nur als Prüfung, keine Verletzung.
- Gewichte: 21 Einträge im Formular (`gewichte_formular.md`, Kopf „ausgefüllt vom Autor 2026-11-24 im Chat, übertragen von Sonnet“), `gewichte.json`. Die Summen stimmen mit der Opus-Kontrolle überein: Zeit 2, Wärme 7, Kosten 3, Bauraum 2, Fehlermöglichkeiten 8, Wirkungsgrad 11, Reifegrad 9 (Summe 42).
- Kopfstand 6 Konzepte (`kopfstand.json`). Paarurteile: 15 Paare in beiden Reihenfolgen, je Aufruf alle 7 Kriterien (30 Aufrufe, 210 Urteile), Nachfragen in 2 Runden (12 Fälle, `nachfragen`).
- Zahlen im Prompt nur aus `problem.json` Fakten F1 bis F6: E2 (`sim/elektrik/e2_elektronik/ergebnis.json`), E3 (`sim/elektrik/e3_platine/ergebnis_ausgleich.json`, `ergebnis_waerme.json`, `ergebnis_platine.json`, `ergebnis_vorladung.json`) und B-BAT-051 (32,45 Ω gültig).
- Lauf: Scope `hermes-batterie-kr1b`, 10:05 bis 10:41 Uhr, GPU vor jedem Aufruf geprüft (nur ollama).

## Prüfung der Vorgabe (Meldung an Opus)
**Hamming-Prüfung ≥ 2 ist bei zwei Paaren verletzt:** K1–K2 (Abstand 1, nur T5) und K5–K6 (Abstand 1, nur T1). Beide Paare sind so gewollt (Ist mit Wärmepfad, induktiv gegen kapazitiv). Ich habe die Vorgabe nicht geändert, die Meldung steht in `konzepte.json` (`pruefung.hamming_unter_2`). Alle anderen Abstände 2 bis 5.

## Rang mit Gewichten des Autors (`rang.json`, `rang.png`)
| Platz | Konzept (Leitidee) | Punkte Autor | Spanne ±1 | Punkte gleiche Gewichte |
|---|---|---|---|---|
| 1 | K2 Ist mit Wärmepfad | 0,607 | 0,601 bis 0,613 | 0,607 (Platz 2) |
| 2 | K1 Ist-Entwurf | 0,594 | 0,584 bis 0,604 | 0,643 (Platz 1) |
| 3 | K6 aktiv kapazitiv | 0,587 | 0,576 bis 0,599 | 0,536 (Platz 3) |
| 4 | K4 Wärme auf Kühlplatte | 0,454 | 0,445 bis 0,462 | 0,493 (Platz 4) |
| 5 | K5 aktiv induktiv | 0,446 | 0,435 bis 0,457 | 0,414 (Platz 5) |
| 6 | K3 getaktet in Ruhe | 0,312 | 0,305 bis 0,320 | 0,307 (Platz 6) |

Bei ±1 bleibt K2 Platz 1. K1, K2, K6 erreichen in einer Variante Platz 1 (Gewichtsgrenzen 0 oder 12): K6 bei Zeit 12, Wärme 12, Kosten 0, Fehler 0, Reife 0; K1 bei Wärme 0, Kosten 12, Bauraum 12; K2 sonst. Der Abstand K2 zu K1 zu K6 ist klein (0,02), die Reihenfolge der drei ist nicht belastbar.

**Konsistenz** (`rang.json`, `konsistenz`, `position`):
- Zirkuläre Triaden nach zwei Nachfragerunden: **3**, alle im Kriterium Fehlermöglichkeiten (K1>K6>K2>K1, K2>K3>K6>K2, K3>K6>K4>K3). Ziel 0 verfehlt, Grenze (mehr als 3) nicht überschritten. Kendall ζ dort 0,62, sonst 1,0.
- Widersprüche zwischen den Reihenfolgen: 2 von 105 Paar/Kriterium-Fällen (K1/K3 bei Fehlern, K3/K4 bei Reife).
- Positionsneigung: erste Nennung gewinnt 87, zweite 88, gleich 35 von 210. Keine Neigung.
- Zahlenprüfung: 1 von 210 Urteilen mit falscher Fundstelle (K3|K6 Reifegrad, Zahl 14,2 nicht in F5). **Mängel, die das Skript nicht fängt:** PI rechnet gelegentlich selbst (K1|K3 Wärme: „Spitzenleistung ≈ 39 W“, nicht in den Fakten; K3|K1: „doppelt so viel“). Opus soll diese Urteile in der Stichprobe prüfen; K3 steht wegen der Wärme auf 0,00 (`punkte_je_kriterium`).

## Abgleich mit der Erwartung Lauf 2 (PRUEFUNG_OPUS.md)
| Erwartung | Befund |
|---|---|
| Gleiche Gewichte: K2 oder K4 vorn | **Verfehlt.** K1 0,643 vorn, K2 0,607 zweiter, K4 vierter (0,493). |
| K3 verliert bei der Zeit, gewinnt bei Wärme und Kosten | **Teilweise.** Zeit 0,15 (verliert). Wärme 0,00 und Kosten 0,50 (verliert bzw. Mitte): Urteil PI nimmt bei 260 mA und 50 % Takt hohe Spitzenverluste an. |
| K5 und K6 verlieren bei Kosten, Reife, Fehlern | **Weitgehend erfüllt.** Kosten 0,05 und 0,15; Reife je 0,10; Fehler K5 0,05, K6 0,50 (Mitte). |
| K1 landet hinten | **Verfehlt.** K1 Platz 2 (Autor) bzw. 1 (gleich): Kosten 0,95, Bauraum 1,00, Reife 0,95 überwiegen die Wärme (0,20). |
| Kosten hoch gewichtet: K3 vorne | **Verfehlt.** Kosten 12: K1 vorn. K3 führt in keiner Variante. |
| Zeit hoch gewichtet: K5 vorne | **Teilweise.** Zeit 12: K6 vorn, K5 gleichauf bei der Zeit (0,90), aber hinten bei Fehlern. |

**Erwartung insgesamt überwiegend verfehlt.** Das Urteilsmodell hält die Wärmegrenze weniger für ein Ausschlusskriterium als die Erwartung (K1 mit 0,20 bei Wärme bleibt vorne). Das Werkzeug wurde nicht angepasst. Das Ergebnis geht mit dieser Abweichung an Opus.

## Vorschlag Alternativen-Tabelle ENT-146 (nur Vorschlag, Akte nicht geändert)
Basis ist nur die Rangfolge der PI-Urteile mit Gewichten des Autors. Bis Opus die Stichprobe geprüft hat, keine Grundlage für die Akte.
| Alternative | Urteil (PI, Gewichte Autor) |
|---|---|
| K2 Ist mit Wärmepfad (Pad zur Kühlplatte) | Platz 1, 0,61. Löst das Wärmeproblem (B-BAT-051) ohne die Zeit zu ändern (Zeit 0,40, Wärme 0,40) |
| K1 Ist-Entwurf | Platz 2, 0,59. Kosten, Bauraum, Reife am besten, Wärme und Zeit schwach |
| K6 aktiv kapazitiv | Platz 3, 0,59. Beste Zeit, Wärme, Wirkungsgrad, schlechteste Reife und hohe Kosten |
| K4, K5, K3 | Plätze 4 bis 6; K3 (getaktet) hinten wegen der Wärme in der Urteilslogik |

## Offen für Opus
1. Hamming-Verstoß K1–K2 und K5–K6 (Vorgabe bleibt, Prüfregel oder Vorgabe ändern).
2. Stichprobe der Urteile, besonders K3 (Wärme 0,00 mit „≈ 39 W“ vom Modell selbst gerechnet). Eine Neuabfrage mit der Auflage „keine eigene Rechnung“ ist möglich.
3. 3 Zirkel im Kriterium Fehlermöglichkeiten, Erwartung verfehlt: deuten, ob Lauf 2 eine Akte tragen kann.
4. Lizenz der TRIZ-Matrix (zweite Quelle ungeklärt, nur privat). Stufe 2 (TRIZ) wurde in Lauf 2 nicht neu genutzt, `triz.json` stammt aus Lauf 1.

---
*KI-generiert (Claude Sonnet, 2026-11-24). Status Entwurf. Freigabe nur durch den Autor.*
