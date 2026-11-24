| Dok.-Nr. | BAT-KR-00 | Version | 0.1 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Kreativmethoden mit nachgeschaltetem Paarvergleich (Werkzeug `pm/kreativ/`) | Ersteller | Claude Opus (KI) | Prüfer | – (Autor offen) |

> KI-generiert (Claude Opus, 2026-11-24). Auftrag Autor 2026-11-24: Kreativtechniken integrieren, „vielleicht kann man hinter die kreativtechnik eine paarbewertung schalten“. Anforderung REQ-D15 (Vorschlag).

## Zweck
Wer eine Akte mit einer echten Abwägung schreibt, soll ihre Alternativen systematisch suchen und nicht aus dem Gedächtnis aufzählen. Dann soll er sie nachvollziehbar bewerten. Das Werkzeug liefert die Spalte „Alternativen“ der Akte und eine Folie.

## Ablauf (eine Sitzung = ein Ordner `pm/kreativ/KRn/`)
| Stufe | Methode | wer | Ausgabe |
|---|---|---|---|
| 1 Problem | Aufgabe als Widerspruch formulieren: „verbessere X, ohne Y zu verschlechtern“. Bezug zu BT, Merkmal, REQ, Akte. | Opus | `problem.md` |
| 2 TRIZ | Den Widerspruch auf die 39 technischen Parameter abbilden. Die Widerspruchsmatrix liefert die Prinzipien (Nummern). Für jedes Prinzip 2–3 Ideen. | Matrix: Skript. Ideen: PI | `triz.json` |
| 3 Morphologischer Kasten | Teilfunktionen als Zeilen, Ausprägungen als Spalten. Quellen der Ausprägungen: Stand der Technik (Recherche W-Nr.), TRIZ-Ideen aus Stufe 2, PI. | Skript + PI, Opus kürzt | `kasten.json` |
| 4 Verträglichkeit und Konzepte | Paare von Ausprägungen, die sich ausschließen, als Liste. Opus legt 5–8 Konzepte mit je einer **Leitidee** fest, darunter immer der Ist-Entwurf als Referenz. Das Skript prüft nur, ob sie zulässig sind (Ausschlüsse) und verschieden genug (Hamming ≥ 1; Varianten einer Leitidee sind erlaubt). **Korrektur nach KR1 Lauf 1:** Die automatische Auswahl über den größten Hamming-Abstand erzeugte widersprüchliche Konzepte (PRUEFUNG_OPUS.md). | Opus | `konzepte.json` |
| 5 Kopfstand | Je Konzept: „Wie bringe ich es zum Versagen?“ Die Antworten werden Risiken (Kandidaten für `docs/05`). | PI | `kopfstand.json` |
| 5b Festforderungen | Konzepte, die einen Muss-Grenzwert (REQ, Befund) verfehlen, scheiden **vor** dem Paarvergleich aus (Korrektur nach KR1 Lauf 2). | Opus | `ausschluss_fest.json` |
| 6 Paarvergleich Kriterien | Jedes Kriterium gegen jedes: wichtiger 2, gleich 1, unwichtiger 0. Ergibt die Gewichte. | **Autor** (Abwägung, CLAUDE.md), Formular `gewichte_formular.md` | `gewichte.json` |
| 7 Paarvergleich Konzepte | Jedes Kriterium mit schriftlicher Definition im Prompt, ohne Überschneidung, damit nichts doppelt zählt (Korrektur nach Lauf 2). Je Kriterium jedes Konzept gegen jedes, mit einem Satz Begründung. Jedes Paar wird **in beiden Reihenfolgen** gefragt, damit eine Vorliebe für die erste oder zweite Stelle auffällt. | PI urteilt, Opus prüft | `paare.json` |
| 8 Konsistenz und Rang | Zirkuläre Triaden zählen (A > B > C > A), Kendall-Konsistenz ζ, Widersprüche zwischen den beiden Reihenfolgen. Zielwert: 0 Zirkel nach Bereinigung. Rang = Σ Gewicht × Punkte. Empfindlichkeit: jedes Gewicht ±1 Stufe, bleibt der Erste der Erste? | Skript | `rang.json`, Bild |
| 9 Übergabe | Ergebnis als Zeile in `docs/25_loesungen_aus_kreativmethoden.md` (Teil A, mit Zuschreibung). Die drei besten Konzepte gehen mit Begründung in die Akte (Alternativen-Tabelle). Was eine Rechnung braucht, wird zur ERWARTUNG eines Rechenauftrags. | Opus | Akte, `ERGEBNIS.md`, Folienbaustein |

**Warum diese Kette?**
- Ein KI-Modell erzeugt Ideen billig, aber unsauber. TRIZ und der Kasten erzwingen, dass der Lösungsraum vollständig abgedeckt wird.
- Der Paarvergleich zerlegt das Urteil in kleine, prüfbare Schritte.
- Die Konsistenzprüfung fängt widersprüchliche Urteile des Modells, die eine Punktbewertung (Nutzwertanalyse 0–4) verdecken würde.
- Die Gewichte setzt der Mensch, denn dort steckt die eigentliche Abwägung.

## Grenzen
- Die Urteile von PI sind Einschätzungen, keine Rechnungen. Wo eine Zahl entscheidet (Wärme, Zeit), steht die Zahl im Paarurteil, mit Quelle.
- TRIZ-Matrix: eine fremde Datentabelle. Herkunft und Lizenz kommen in `docs/10`. Wenn die Lizenz nicht klar ist, bleibt sie nur im privaten Repo und wird als „ungeklärt“ vermerkt.

## Pilot KR1: Zellausgleich NMC
- **Widerspruch:** Die Ausgleichszeit soll kürzer werden (E2: 14,2 h, und laut ERW-E3 im Mittel noch ≈ 15 % länger). Die Wärme in der CMU darf aber nicht steigen (9,83 W bei 10 W Grenze, ERW-E3 Punkt 3 vermutlich schon zu heiß). TRIZ: verbessern „Zeitverlust“ bzw. „Produktivität“, verschlechtern „Temperatur“ bzw. „Energieverlust“.
- **Teilfunktionen für den Kasten (Vorschlag Opus):**
  - Prinzip des Ausgleichs
  - Ort der Verlustwärme
  - Zeitpunkt des Ausgleichs
  - Schalter
  - Wärmeabfuhr
  - Steuerung (Ziel-SOC, Spannungsschwelle)
- **Kriterien:**
  - Ausgleichszeit
  - Wärme in der CMU
  - Kosten
  - Bauraum
  - Fehlermöglichkeiten (FSR, HARA)
  - Wirkungsgrad
  - Reifegrad
- **Erwartung Opus (vor dem Lauf):**
  - Vorne liegt passiver Ausgleich mit einem Wärmepfad zur Kühlplatte oder Ausgleich nur in Ruhephasen mit höherem Strom.
  - Aktiver Ausgleich (induktiv oder kapazitiv) gewinnt bei Zeit und Wirkungsgrad, verliert bei Kosten, Reifegrad und Fehlermöglichkeiten. Platz 2–4.
  - Die Rangfolge hängt am Gewicht von Kosten gegenüber Zeit. Die Empfindlichkeitsrechnung soll das zeigen.

## Nächste Sitzungen (Vorschlag)
- KR2: Zielkonflikt SG-05 „nicht trennen“ gegen SG-01/03/04 „trennen“ (HARA)
- KR3: Masse gegen Crash (REQ-P07 gegen REQ-P14)
