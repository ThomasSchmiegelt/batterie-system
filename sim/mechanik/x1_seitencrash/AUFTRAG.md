| Dok.-Nr. | Auftrag X1 | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Seitenpfahl quasistatisch, CalculiX | Ersteller | Claude Opus (KI) | Prüfer | Opus (Rohdaten) |

> KI-generiert, Opus → Sonnet, 2026-11-18. Erwartung und Annahmen: ERWARTUNG.md (nicht ändern, keine eigenen Annahmen; fehlt etwas → melden).
1. `eingaben.json` aus ERWARTUNG und CAD-Parametern. Jeder Wert mit Herkunft.
2. `x1.py`: Geometrie und Netz (gmsh), CalculiX-Deck mit Kontakt, Pfahl weggesteuert, NLGEOM, Plastizität. Je Variante LF1 und LF2.
   - Netzstudie: 2 Netze im Ausschnitt, Spitzenkraft-Abweichung < 10 %.
   - Start mit nice und systemd-run --user --scope, nur CPU, höchstens 8 Threads.
3. Auswertung `ergebnis.json` mit Kraft-Weg-Kurven, Kraft und Energie bei Zellberührung, max. PEEQ und Ort.
4. Bilder mit Zielband und Lesehilfe:
   - `kraft_weg.png` (4 Kurven, Linie 100 kN Annahme)
   - je LF ein Verformungsbild mit PEEQ (ccx2paraview oder pvbatch, wie K0)
5. `ERGEBNIS.md` mit Abgleich gegen die Erwartung, `lesehilfe.md`, Folienbaustein `praesentation/bausteine/X1.md`.
Rechnet ein Lauf länger als 30 min oder konvergiert nicht → abbrechen, Log-Auszug an OPUS. Höchstens 120 min gesamt. Rückgabe höchstens 5 Zeilen.
