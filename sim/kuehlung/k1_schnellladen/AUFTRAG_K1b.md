| Dok.-Nr. | Auftrag K1b | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | 4680: obere Kühlung über Verbinder und Isolierpad | Ersteller | Claude Opus (KI) | Prüfer | Opus (Stichprobe) |

> KI-generiert, Opus → Sonnet, 2026-11-17. Erwartung: Nachtrag K1b in ERWARTUNG.md (nicht ändern). Sparsam.
1. Skripte aus K1 wiederverwenden. Neuer Kühlfall `K3b` (nur NMC): oben Robin-Rand mit h_eff nach Formel aus ERWARTUNG (Werte in eingaben.json mit Herkunft „Annahme Opus“), unten wie K3-Nachtrag.
2. Fälle: P0, P3, P4 mit K3b; Empfindlichkeit P3: φ 0,3/0,7 und k_pad 1/6 (4 Läufe).
3. Ergebnis: Abschnitt „8 Nachtrag K1b“ in ERGEBNIS.md mit Abgleich, ergebnis.json ergänzen, landkarte.png und verlauf_kuehlung_NMC.png aktualisieren, K1.md Zahlen nachziehen, bilder.py.
CPU, nice, ≤ 30 min. Rückgabe ≤ 4 Zeilen.
