| Dok.-Nr. | BAT-KR-E1 | Version | 0.1 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Ergebnis KR1: Kreativwerkzeug und Pilot Zellausgleich NMC | Ersteller | Claude Sonnet (KI), im Auftrag von Opus | Prüfer | Opus (Rohdaten, Stichprobe Paarurteile), offen |

> **KI-generiert (Claude Sonnet, 2026-11-24).** Urteile und Ideen stammen von PI (qwen-gross, lokal, ohne Werkzeuge): Einschätzungen, keine Rechnungen. **Gewichte vorläufig gleich**, der Autor hat `gewichte_formular.md` noch nicht ausgefüllt. Auftrag: `pm/kreativ/AUFTRAG_KR1.md`, Methode: `pm/kreativ/METHODE.md` (unverändert).

## Was getan wurde
- Werkzeug `pm/kreativ/kreativ.py` (Befehle triz, kasten, konzepte, kopfstand, formular, paare, rang; Bedienung im Kopf der Datei).
- TRIZ-Daten `pm/kreativ/triz_daten.json`: 39 Parameter und 40 Prinzipien mit eigenen deutschen Kurznamen, Matrix mit 1248 belegten Zellen (`herkunft.zellen`). Quelle und Lizenz in `docs/10`: Quelle 1 MIT, Quelle 2 ungeklärt, nur privat.
- Gegenprüfung der Matrix (`triz_daten.json`, Feld `gegenpruefung`): 8 Zellen verglichen (1-3, 14-9, 25-17, 25-22, 39-17, 39-22, 39-19, 22-17), alle gleich. Vollvergleich: 15 von 1248 Zellen weichen ab. Das sind laut `DATA_SOURCES.md` der Quelle 1 genau die dort korrigierten Tippfehler der englischen Abschrift. **Einschränkung:** Quelle 2 gehört zu derselben Abschriftenfamilie, es sind keine zwei vollständig unabhängigen Ursprünge.
- Pilot in `pm/kreativ/KR1/`: `problem.json` (Fakten F1 bis F10 mit Fundstelle), `triz.json`, `kasten.json`, `ausschluesse.json`, `konzepte.json`, `kopfstand.json`, `gewichte_formular.md`, `paare.json`, `rang.json`, `rang.png`, Rohantworten in `roh/` (61 Dateien), `lauf.sh`.
- Lauf: Scope `hermes-batterie-kr1`, 09:22 bis 09:54 Uhr (32 min PI, GPU vor jedem Aufruf geprüft, kein fremder Prozess). Alle Aufrufe gaben im ersten Versuch gültiges JSON, außer einem (Neuversuch `_v2`, siehe `roh/`).

## Abweichungen vom Auftrag (zur Prüfung durch Opus)
1. **Paarurteile je geordnetem Paar, alle sieben Kriterien in einer Antwort** (20 PI-Aufrufe statt 140). Jedes Urteil hat Gewinner, Begründung, Zahl mit Fakt-ID. Grund: Zeitrahmen 150 min.
2. **Zahlenprüfung:** Das Skript prüft Fakt-ID und jede Zahl gegen den Fakttext. Nach der Prüfung bleiben 5 von 140 Urteilen mit falscher Fundstelle (`rang.json`, `zahlverstoesse`). Sie sind markiert, nicht entfernt.
3. **Kasten nicht gekürzt** (Opus kürzt): je Zeile 5 Ausprägungen, Reihenfolge PI. Einige sind fachlich schwach (z. B. T3.4 „Temperaturgepumpt“, T2.5 „Ultraschall-Konvektion“).
4. **Ausschlüsse** sind Vorschlag Sonnet (20 Paare, `ausschluesse.json`), Opus prüft.
5. **Zusatz zur Empfindlichkeit:** neben „±1 Stufe“ (Methode) auch jedes Gewicht auf 0 und 12 (Grenzen des Paarvergleichs 0 bis 12), um die Erwartung 3 prüfbar zu machen. Fehlerbalken im Bild nur aus ±1.
6. Die Auswahl der Konzepte ergab 5 (Untergrenze), alle mit dem größten Abstand (Hamming 6 von 6, `konzepte.json`, `min_hamming`): Das Verfahren (eine Richtung je Ausprägung der Zeile „Prinzip“) wählt Kombinationen, die in jeder Zeile anders sind. Mischformen wie „passiv mit Wärmepfad“ kommen so nicht vor.

## Konzepte (`konzepte.json`)
| Nr | Konzept (Prinzip / Ort / Zeit / Schalter / Wärmeabfuhr / Steuerung) |
|---|---|
| K1 | Passiv Widerstand / Widerstände auf CMU / kontinuierlich / MOSFET + 34 Ω / freie Konvektion / Spannungsschwelle, 130 mA (entspricht Ausgangsentwurf E2/E3) |
| K2 | Gepulster Hochstrom / externer Flüssigkeitskreislauf / einmalig im Aufwachfenster / PWM-Schalter / Flüssigkeitskreis / temperaturabhängiger Strom |
| K3 | Transformergekoppelt aktiv / induktives Koppelelement / kurz parallel im Hochstromfenster / HF-Schalter / gepulster Betrieb / periodisches Aufwachen, Batch |
| K4 | Vorgleich in Aufwachphase / doppelte Platinenfläche / nur bei kühlem Zustand / zellenweiser Schalter / Wärmeleitpad zur Kühlplatte / Einmal-Durchlauf 18 Kanäle |
| K5 | Paralleler Gleichstromausgleich / Kühlplatte mit Ultraschall / Vorgleich vor Betrieb / Sequenzschalter / Transformatorkopplung / parallele Auslösung |

Zulässig 7032 von 15625 Kombinationen (`konzepte.json`).

## Kopfstand-Risiken (`kopfstand.json`, Kandidaten für docs/05, ungeprüft)
- K1: thermisches Versagen der Platine (60 bis 100 K, F5), Stromerhöhung sprengt das Wärmebudget, schwächste Zelle begrenzt die Kapazität.
- K2: Kühlkreisausfall, Schalteralterung, Aufwachfenster zu kurz.
- K3: thermisches Kippen des Koppelelements, HF-Schalterausfall, Zeitverkürzung verletzt Wärmebudget.
- K4: Taktungslogik-Deadlock, falsche dQ-Vorberechnung, Padausfall unter mechanischer Last.
- K5: Wärmespitze bei paralleler Auslösung, Verlust im Zellinnenwiderstand statt in der Kopplung, Antrieb Dauerbetrieb.

## Rang (`rang.json`, Bild `rang.png`)
Gewichte: vorläufig gleich (`gewichte_quelle`). Gesamtpunkte 0 bis 1:
| Platz | Konzept | Punkte | Spanne ±1 |
|---|---|---|---|
| 1 | K4 | 0,589 | 0,581 bis 0,597 |
| 2 | K3 | 0,554 | 0,544 bis 0,564 |
| 3 | K1 | 0,518 | 0,506 bis 0,530 |
| 4 | K2 | 0,438 | 0,433 bis 0,442 |
| 5 | K5 | 0,402 | 0,390 bis 0,413 |

**Konsistenz** (`rang.json`, `konsistenz`, `position`):
- Zirkuläre Triaden nach zwei Nachfragerunden: **2** (beide im Kriterium Fehlermöglichkeiten: K1>K3>K2>K1 und K1>K5>K2>K1). Ziel 0 verfehlt, Abbruchgrenze (mehr als 3) nicht erreicht.
- Kendall ζ je Kriterium: 1,0 außer Fehlermöglichkeiten mit 0,6.
- Widersprüche zwischen den Reihenfolgen: 8 von 70 Paar/Kriterium-Fällen nach den Nachfragen (14 Fälle in Runde 1, 10 in Runde 2, `nachfragen`).
- Positionsneigung: erste Nennung gewinnt 68, zweite 59, gleich 13 von 140 Urteilen. Leichte Neigung zur ersten Stelle.
- Empfindlichkeit ±1: Platz 1 bleibt K4. Mit den Zusatzgrenzwerten erreichen K1 (Wärme Gewicht 0 oder Bauraum Gewicht 12) und K3 (Zeit 12, Kosten 0, Fehlermöglichkeiten 0, Wirkungsgrad 12, Reifegrad 0, Wärme 12) Platz 1.

## Abgleich mit der Erwartung (METHODE.md, Pilot KR1)
| Erwartung | Befund |
|---|---|
| Vorne: passiver Ausgleich mit Wärmepfad zur Kühlplatte oder Ausgleich in Ruhephasen | **Teilweise erfüllt.** K4 (Vorgleich in der Aufwachphase mit Wärmeleitpad) liegt vorn. Das reine Passiv-mit-Pad-Konzept gibt es nicht, siehe Abweichung 6. |
| Aktiv gewinnt bei Zeit und Wirkungsgrad, verliert bei Kosten, Reife, Fehlern, Platz 2 bis 4 | **Erfüllt.** K3: Zeit 0,88 und Wirkungsgrad 0,88 (beste), Kosten 0,12 und Reife 0,25 (schlechteste), Fehler 0,50, Platz 2. |
| Rang hängt am Gewicht Kosten gegenüber Zeit | **Erfüllt, nicht bei ±1.** Bei Kosten 0 oder Zeit 12 führt K3, bei Kosten 12 führt K4. Bei ±1 bleibt K4 vorn. |

Punkte je Kriterium: `rang.json`, `punkte_je_kriterium`. Referenz K1 (Ist): Ausgleichszeit 0,06 (letzter), Wärme 0,00 (letzter), Kosten, Bauraum, Reife je 1,00.

## Vorschlag Alternativen-Tabelle ENT-146 (Opus entscheidet, Akte nicht geändert)
| Alternative | Urteil (PI, gleiche Gewichte) |
|---|---|
| K1 passiv 130 mA, wie entschieden | Platz 3, 0,52. Billig, reif, kleinster Bauraum. Langsamste (0,06) und heißeste (0,00) Variante |
| K4 Vorgleich in Aufwachphase, Pad, doppelte Fläche | Platz 1, 0,59. Beste Fehlerbilanz (0,94), mittlere Zeit (0,44) |
| K3 transformergekoppelt aktiv | Platz 2, 0,55. Schnellste Zeit und beste Wärme, höchste Kosten (0,12) und geringste Reife (0,25) |
| K2 gepulst mit Flüssigkeitskühlung, K5 parallel mit Ultraschall | Platz 4 und 5, Kopfstand nennt Kühlkreis- und Schalterrisiken |
Wer die Rangfolge nutzt: Gewichte des Autors fehlen, Zahlenbezug nur F1 bis F10 (Spalte „Zahlen“ in `problem.json`).

## Offene Fragen an Opus
1. Gewichte vom Autor (`gewichte_formular.md`), danach `python3 pm/kreativ/kreativ.py rang KR1` neu (ohne PI).
2. Ausschlüsse und Kasten prüfen (Abweichungen 3 und 4). Ein Konzept „passiv + Pad + nur Ruhephase“ fehlt wegen der Auswahlregel.
3. Zwei Zirkel im Kriterium Fehlermöglichkeiten: neu fragen (Opus entscheidet) oder bereinigen. Lizenz Quelle 2 und Rechtslage der Matrix: Frage an den Autor vor einer Veröffentlichung.
4. 5 Urteile mit falscher Fundstelle der Zahl (`zahlverstoesse`).

---
*KI-generiert (Claude Sonnet, 2026-11-24). Status Entwurf. Freigabe nur durch den Autor.*
