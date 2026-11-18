| Dok.-Nr. | Auftrag B1-d | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Projektbericht Fassung 0.4: Crash X1, X1b/X2 | Ersteller | Claude Opus (KI) | Prüfer | Opus (Stichprobe) |

> KI-generiert, Opus → Sonnet, 2026-11-18. Autor: „bitte passe den bericht mit den erkenntnissen an.“ Es gelten die Regeln aus AUFTRAG_BERICHT.md.
1. Neues Kapitel „Seitencrash“ nach Stückliste und Kosten:
   - Vorgehen: X1 quasistatisch mit CalculiX, X1b/X2 explizit mit OpenCourant. OpenRadioss ist eingestellt, OpenCourant ist der Fork (docs/10, SOFTWARE.md).
   - Ergebnisse aus B-BAT-030 und B-BAT-031, Zahlen aus `sim/mechanik/x1_seitencrash/ergebnis.json` und `x1b_knautschzone/ergebnis_oc.json`.
   - Bilder: kraft_weg.png (X1), energie_bis_zellberuehrung_ueber_w.png, kraft_eindringung_oc.png, ein verformung_oc-Bild.
   - Empfehlung Opus: keine Knautschzone im Pack, der Schweller trägt. Offen ist eine Studie zu Querträgerabstand bzw. Innenwand.
   - Grenzen: Ausschnittmodell, ohne Fahrzeug. Pfahl Ø 254, 100 kN und 5 kJ sind Annahmen (W30 ohne Normwerte).
2. Kapitel Fehler ergänzen:
   - X1-Erwartung: Rahmen als freier Weg gezählt.
   - X1b-Erwartung: Rahmenbiegung übersehen.
   - CalculiX divergiert beim Falten, Methodenwechsel.
   - pkill-Falle (BA-87).
   - Rechnung widerlegt eine Freigabe des Autors (BA-88).
3. Kapitel Werkzeuge: Wiederaufsetzpunkt-Regel und neustart.sh. Befund /RFILE-Segfault.
4. Offene Punkte und Zusammenfassung nachführen. Version 0.4.
Zweimal kompilieren, 0 Fehler, die neuen Seiten als Bild ansehen. Höchstens 40 min. Rückgabe höchstens 3 Zeilen.
