| Dok.-Nr. | Auftrag E1 | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Ströme, Querschnitte, Verluste der Verbinder und HV-Leitung | Ersteller | Claude Opus (KI) | Prüfer | Opus (Stichprobe) |

> KI-generiert, Opus → Sonnet, 2026-11-17. Erwartung ERWARTUNG.md (nicht ändern). Sparsam.
1. `eingaben.json` (Herkunft je Wert, aus ERWARTUNG, Akten ENT-006, ENT-093, M0-Geometrie `sim/mechanik/m0_gehaeuse/ergebnis.json` für Verbinderlängen, Stückliste).
2. `querschnitte.py`: Lastfälle (Laden je Variante, Spitze, Dauer, je bei Nenn- und Entladeschlussspannung); je Verbinderart Strom, Querschnitt nach Stromdichte und nach Erwärmung (einfaches Wärmebilanzmodell Verbinder → Pad → Kühlplatte, Annahmen benennen), gewählte Maße (Normbreiten), Widerstand, Verluste, Spannungsabfall; Masse Al/Cu.
3. `ergebnis.json`, `ERGEBNIS.md` (Abgleich Punkt für Punkt), Bild `querschnitte.png` (Balken je Verbinderart beide Varianten, Zielband), `verluste.png`, Lesehilfe `e1_lesehilfe.md`, Baustein `praesentation/bausteine/E1.md`, `pm/plan/bilder.py`.
≤ 30 min, CPU. Rückgabe ≤ 4 Zeilen.
