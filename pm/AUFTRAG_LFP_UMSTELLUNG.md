| Dok.-Nr. | Auftrag V1-LFP | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Startwerte und Stückliste auf LFP (ENT-005), Obsidian-Notizen für alle Bauteile | Ersteller | Claude Opus (KI) | Prüfer | Opus (Rohdaten) |

> **KI-generiert.** Auftrag von Opus an Sonnet (`sonnet-umsetzer`), 2026-11-16. Anlass: Der Autor hat ENT-004 (Bauteilbaum) und ENT-005 (BT-100 chemie = LFP) am 2026-11-16 freigegeben. REQ-P01 ist jetzt ein Anhaltswert (1500 kg, Fall A und B als Spanne).

## Ziel
1. **`pm/startwerte.py`:** Gibt es in `pm/bauteile/parameter.json` einen entschiedenen Wert für `BT-100` / `chemie`, gilt er vor der Bauraumregel (Zeile ~83–87). Die Regel wird weiter gerechnet und ausgegeben, aber nur als Prüfung: Text in REQ-P06 „LFP (ENT-005, entschieden); Bauraumregel: …“. Passt LFP nach der Regel nicht, kommt eine Warnung „Bauraum offen: Annahme wh_l_pack LFP 180 Wh/L unbelegt (B-BAT-004/006)“, aber **keine** Umstellung auf NMC. Die Annahmen in `TAB_*` nicht ändern.
2. Lauf: `python3 pm/startwerte.py "Kompaktwagen, 400 km Reichweite, in 20 min auf 80 %, Mitteleuropa"`, dann `python3 pm/bauteile/stueckliste.py`. Die Stückliste rechnet danach mit LFP (3,2 V, Annahme 140 Ah).
3. **Obsidian:** `pm/plan/wissensnetz_obsidian.py` (bzw. der Teil von `wissensnetz.py`, der `wissen/` schreibt) erzeugt eine Notiz je Bauteil aus `struktur.json` (alle 46, nicht nur 8 Gruppen), mit Eltern-/Kind-Links, Merkmalen und verlinkten ENT-Akten. Danach `python3 pm/plan/wissensnetz.py && python3 pm/plan/wissensnetz_ansicht.py`.
4. **Kosmetik:** In `sim/chemie/vergleich_lfp_nmc/packmasse.png` überdeckt die Beschriftung „Grenze 450“ in Fall A die Balken. Beschriftung verschieben (in `vergleich.py`), neu laufen lassen, Zahlen in `ergebnis.json` dürfen sich nicht ändern (vorher/nachher vergleichen).

## Eingang
`pm/startwerte.py`, `pm/bauteile/stueckliste.py`, `pm/bauteile/parameter.json`, `pm/bauteile/struktur.json`, `pm/entscheidungen/ENT-00*.md`, `pm/plan/*.py`, `sim/chemie/vergleich_lfp_nmc/vergleich.py`.

## Ausgabe
Geänderte Skripte (Kopf „KI-generiert, geändert 2026-11-16 Sonnet“), neu erzeugt: `pm/startwerte.json`, `docs/startparameter.md`, `docs/13_stueckliste.md`, `wissen/`, `docs/03`, `packmasse.png`. Kurzbericht `pm/AUFTRAG_LFP_UMSTELLUNG_ergebnis.txt` (≤ 15 Zeilen): Chemie in startwerte.json, Energie brutto aus startwerte und aus Stückliste (beide Zahlen nennen, Widerspruch nicht selbst lösen), Zellen s×p, Anzahl Bauteilnotizen, Warnungen, `python3 pm/pm.py pruefe`-Ergebnis.

## Abbruch und Rückgabe
- Fertig, wenn alle Skripte fehlerfrei laufen und `pm.py pruefe` 0 Fehler meldet. Abbruch nach 30 min.
- Nicht ändern: `ENT-*.md`, `struktur.json`, Annahmewerte, `eingaben.json`. Keine eigenen neuen Zahlen.
- **→ OPUS**: Wenn die Stückliste mit LFP eine Energie weit weg von 73,9 kWh ergibt (> 10 %), wenn ein Skript eine Annahme braucht, die es nicht gibt, oder wenn sich `ergebnis.json` ändert.
