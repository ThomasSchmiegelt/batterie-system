| Dok.-Nr. | Auftrag VAR | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Zwei Varianten parallel (LFP, NMC) mit gleicher Spezifikation: Variantenfeld in Akten, Parameter und Stückliste je Variante | Ersteller | Claude Opus (KI) | Prüfer | Opus (Rohdaten) |

> **KI-generiert.** Auftrag von Opus an Sonnet (`sonnet-umsetzer`), 2026-11-16. Anlass: Autor: „kannst du auch zwei varianten paralell bauen? bei mit den selben spezifikationen“. Gleiche Spezifikation = gleiche Vorgaben (1500 kg Anhaltswert, 400 km, 800 V, Bauraum, Lastenheft). Verschieden ist nur, was aus der Chemie folgt.

## Vorgabe Opus (Methode, nicht ändern)
1. Neue Datei `pm/varianten.json`: `{"LFP": {"titel": "LFP Blade (prismatisch, Cell-to-Pack)"}, "NMC": {"titel": "NMC (Zellformat offen)"}}`.
2. **Akten:** neues optionales YAML-Feld `variante:` (Liste, z. B. `[LFP]`). Fehlt es, gilt die Akte für alle Varianten. `VORLAGE.md` bekommt die Zeile `variante: null   # null = alle Varianten, sonst [LFP] oder [NMC]`. `pm.py neu` nimmt optional `--variante LFP`.
3. **`pm.py pruefe`:** Doppelte gültige Entscheidung zum selben Bauteil+Merkmal ist nur dann ein Fehler, wenn sich die Varianten überschneiden. Unbekannte Variante (nicht in varianten.json) ist ein Fehler.
4. **`pm.py parameter`:** schreibt `pm/bauteile/parameter.json` (nur gemeinsame Akten, wie bisher) **und** je Variante `pm/bauteile/parameter_<V>.json` (gemeinsam + variantenbezogen; variantenbezogen gewinnt nur, wo kein gemeinsamer Wert besteht, sonst Fehler aus 3). `pm.py register` zeigt eine Spalte „Variante“. `pm.py kontext BT-xxx [--variante V]`.
5. **ENT-005 nicht löschen.** Opus stellt die Akte selbst um (nicht Sonnet).
6. **`pm/startwerte.py` und `pm/bauteile/stueckliste.py`:** Parameter `--variante V`. Chemie dann aus `parameter_<V>.json`. Ausgaben je Variante: `pm/startwerte_<V>.json`, `docs/startparameter_<V>.md`, `pm/bauteile/stueckliste_<V>.json`, `docs/13_stueckliste_<V>.md`. Ohne `--variante` verhalten sich beide Skripte wie heute. Zellzahl: s = ceil(U_sys/U_zelle); Ah je Zelle = E/(s·U_zelle) bei p = 1, solange kein Zellformat entschieden ist (gleiche Regel wie jetzt).
7. `pm/plan/wissensnetz.py` / Obsidian: Akten mit Variante zeigen die Variante (Feld in der Notiz, Tag `#variante/LFP`). Keine Doppelstruktur des Baums.

## Eingang
`pm/pm.py`, `pm/entscheidungen/*.md` (nur lesen), `pm/startwerte.py`, `pm/bauteile/stueckliste.py`, `pm/plan/wissensnetz*.py`.

## Ausgabe
Geänderte Skripte (Kopf „geändert 2026-11-16 Sonnet“), `pm/varianten.json`, VORLAGE-Zeile. Test: eine Wegwerf-Akte im Scratchpad oder `pm/entscheidungen/_test/` mit `variante: [NMC]` und gleichem Merkmal wie ENT-005 → pruefe 0 Fehler; zweite mit `[LFP]` → Fehler erkannt; Testakten danach löschen. Kurzbericht `pm/AUFTRAG_VARIANTEN_ergebnis.txt` (≤ 12 Zeilen).

## Abbruch und Rückgabe
- Fertig, wenn `pm.py pruefe|register|parameter`, beide Skripte mit und ohne `--variante` und `wissensnetz.py` fehlerfrei laufen. Abbruch nach 30 min.
- Nicht ändern: ENT-Akten, struktur.json, Annahmewerte, forschung/, sim/.
- **→ OPUS**: Wenn die Stückliste eine Chemie oder Zellwerte braucht, die nicht entschieden sind (NMC-Zelle offen), Platzhalter „offen“ ausgeben, keine eigenen Zahlen.
