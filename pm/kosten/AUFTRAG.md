| Dok.-Nr. | Auftrag KO1 | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Kostenbewertung je Variante | Ersteller | Claude Opus (KI) | Prüfer | Opus (Stichprobe) |

> KI-generiert, Opus → Sonnet, 2026-11-18.

1. `pm/kosten/eingaben.json`: Werte aus der Tabelle in `ERWARTUNG.md` eintragen. Je Feld `wert`, `einheit` (€/Stück, €/kg, €/m, €/kWh, €/L) und `herkunft` („ERW-KO1 Annahme“, Packpreis „W29“). Die neuen BT-260, 361, 440, 721, 722 ergänzen. Keine eigenen Werte.
2. `kosten.py`:
   - €/kg mal Masse, €/m mal Länge, €/kWh mal Energie (LFP 73,92, NMC 74,27 kWh), dazu Fertigung.
   - Positionen ohne Masse oder Menge als „offen“ zählen und ausweisen, nicht als 0.
   - Ausgabe `ergebnis_<V>.json`: Summe, €/kWh, Anteil je Baugruppe BT-100/200/300/400/500/600/700 und Fertigung.
   - Empfindlichkeit: Zellpreis ±20 %.
3. Bilder `pm/kosten/kosten_<V>.png` und Vergleich `kosten_vergleich.png`:
   - gestapelter Balken je Variante nach Baugruppen
   - Linie für den Beleg 97 USD/kWh ≈ 89 €/kWh
   - Zielband aus der Erwartung
   - Lesehilfe
4. `docs/18_kosten.md` (Dokumentkopf, Status Entwurf, Abgleich mit der Erwartung, Annahmen deutlich gekennzeichnet). Folienbaustein `praesentation/bausteine/KO1.md`.
Abbruch → OPUS: Verfehlt-Fall der Erwartung, mehr als 5 offene Positionen je Variante. Rückgabe höchstens 5 Zeilen.
