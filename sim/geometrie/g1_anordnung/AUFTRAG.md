| Dok.-Nr. | Auftrag G1-V | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | G1-Vorprüfung Zellanordnung; dazu Bild C0b und Quell-URL im Recherchelauf | Ersteller | Claude Opus (KI) | Prüfer | Opus (Rohdaten) |

> **KI-generiert.** Auftrag von Opus an Sonnet (`sonnet-umsetzer`), 2026-11-17.

## Teil 1: `sim/geometrie/g1_anordnung/anordnung.py`
- Nur `eingaben.json` lesen, keine eigenen Zahlen. Je Variante (LFP, NMC) und Fall (A, B): Zellmaße (LFP-Länge nach `laenge_regel`; Ah = E·1000/(250·3,2)), Anordnung nach `anordnung`, Innenmaße = Bauraum − 2·Rand (L, B), Höhe = Zellhöhe + unten + oben. Ergebnis je Fall: passt / passt nicht in L, B, H, mit Reserve in mm; NMC: Plätze gesamt und Belegung %.
- Empfindlichkeit: Rand, Zellabstand, Höhen über ihre Bänder (einzeln) → welche Annahme kippt „passt“?
- Ausgaben: `ergebnis.json`, `anordnung.png` (Draufsicht je Variante Fall A, Zellen als Rechtecke/Kreise, Innenrand gestrichelt, Maßzahlen; Fall B als zweite Zeile), `anordnung_lesehilfe.md`, `ERGEBNIS.md` mit **Abgleich ERWARTUNG.md Punkt für Punkt**, `ERGEBNIS_kurz.txt` (≤ 12 Zeilen), `praesentation/bausteine/G1.md` (Kernaussage „(Opus)“).

## Teil 2: Bild C0b
`sim/chemie/varianten_lfp_nmc/varianten.py`: LFP-Balken auf den gemessenen Wert 160 Wh/kg, Bandenden 185/210 gepunktet; Titel entsprechend; `ergebnis.json` darf sich nicht ändern (diff).

## Teil 3: Recherche-Werkzeug (B-BAT-009)
`forschung/lauf.sh`: Die Liste der Quell-URLs eines Themas wird PI im Auftragstext wörtlich mitgegeben mit dem Satz „Zitiere als URL genau eine dieser Adressen, nie eine DOI oder andere Adresse.“ Stelle im Skript finden, wo der Auftrag an PI gebaut wird. **Nicht** laufen lassen (GPU). Nur Syntaxprüfung `bash -n`.

## Abbruch und Rückgabe
Fertig, wenn alles fehlerfrei läuft; Abbruch nach 30 min. Nicht ändern: ENT-Akten, struktur.json, eingaben.json, ERWARTUNG.md. Rückgabe ≤ 15 Zeilen. **→ OPUS**: verfehlte Erwartung, fehlende Eingabe.
