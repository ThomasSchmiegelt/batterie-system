| Dok.-Nr. | Auftrag KR1 | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Werkzeug Kreativmethoden + Paarvergleich, Pilot Zellausgleich NMC | Ersteller | Claude Opus (KI) | Prüfer | Opus (Rohdaten, Stichprobe Paarurteile) |

> KI-generiert, Opus → Sonnet, 2026-11-24. Methode und Erwartung: `pm/kreativ/METHODE.md` (nicht ändern). Keine eigenen Annahmen.

## Ziel
Wiederverwendbares Werkzeug `pm/kreativ/kreativ.py` (Unterbefehle je Stufe 2–8) und Pilot `pm/kreativ/KR1/`.

## Schritte
1. **TRIZ-Daten** `pm/kreativ/triz_daten.json`:
   - die 39 Parameter und die 40 Prinzipien (Nummer und eigener deutscher Kurzname, keine fremden Erläuterungstexte)
   - die Widerspruchsmatrix (39 × 39, Prinzipnummern)
   Quelle mit Lizenz in `docs/10`. Hat keine Quelle eine klare Lizenz: als „ungeklärt, nur privat“ vermerken. Die Matrix stichprobenartig an zwei Quellen gegenprüfen (5 Zellen) und das Ergebnis in die Datei schreiben.
2. **PI-Aufruf** wie in `pm/gespraech.sh` (gleiche Flags, `--no-tools --offline`): Funktion `frage_pi(prompt) → text`, Rohantworten nach `KRn/roh/`.
   - **Vor jedem PI-Lauf die GPU prüfen** (`nvidia-smi`). Ist sie durch einen fremden Prozess belegt (FluidX3D, GX): pausieren und an Opus melden.
   - Antworten als JSON anfordern. Ist eine Antwort kein gültiges JSON, höchstens zweimal neu fragen.
3. **Stufen 2–5** wie in der Methode:
   - Konzeptauswahl per Hamming-Abstand, 5–8 Konzepte
   - Ausschlüsse: zuerst nur offensichtliche technische (z. B. „aktiv kapazitiv“ zusammen mit „Wärme nur im Widerstand“). Die Liste markiert Sonnet als Vorschlag, Opus prüft sie.
4. **Stufe 6:** Formular `KR1/gewichte_formular.md` mit der Dreiecksmatrix der Kriterien für den Autor. Bis zur Antwort rechnet das Skript mit **gleichen Gewichten** und kennzeichnet das deutlich als vorläufig.
5. **Stufe 7:** Paarurteile von PI, jedes Paar in beiden Reihenfolgen. Pro Urteil: Gewinner, Begründung in einem Satz und eine verwendete Zahl mit Quelle, falls vorhanden.
   Zahlen nur aus:
   - `sim/elektrik/e2_elektronik/ergebnis.json`
   - `sim/elektrik/e3_platine/ERWARTUNG.md`
   - `forschung/ergebnis/*.md`
6. **Stufe 8:** zirkuläre Triaden, Kendall ζ, Widersprüche zwischen den Reihenfolgen, Rang, Empfindlichkeit (jedes Gewicht ±1). Dazu das Bild `KR1/rang.png`:
   - Balken der Gesamtpunkte
   - Fehlerbalken aus der Empfindlichkeit
   - Markierung der Konzepte, die in einer Variante Platz 1 erreichen
   - Lesehilfe
7. **Bericht:**
   - `KR1/ERGEBNIS.md`: Kasten, Konzepte, Kopfstand-Risiken, Rang, Abgleich mit der Erwartung aus der Methode, Vorschlag für die Alternativen-Tabelle der Akte ENT-146
   - Folienbaustein `praesentation/bausteine/KR1.md`
   - Zeile in `docs/08_ki_einsatz_protokoll.md`
   - kurze Bedienungsanleitung im Kopf von `kreativ.py`

≤ 150 min. Rückgabe ≤ 5 Zeilen. Abbruch → OPUS: mehr als 3 zirkuläre Triaden nach zwei Nachfragen, Erwartung verfehlt, fehlende Zahl, GPU belegt, Lizenzfrage.
