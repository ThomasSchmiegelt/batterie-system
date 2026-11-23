# Auftrag Sonnet: Ergebnisse der Freigaberunde umsetzen

KI-generiert (Claude Opus, 2026-11-23). Quelle ist `pm/freigaberunde_2026-11-23.md`, Runden 1–4. Dort steht jede Entscheidung mit Wer und Warum. Du setzt um und entscheidest nichts.

1. **CAD vorher:** Sichere `cad/baukasten/ausgabe/ergebnis_{LFP,NMC}.json` als `*_vor_freigabe.json`.
2. **Akten (Runde 4):** Status und Felder setzen.
   - `ersetzt`: Bei ENT-104/105/106 trägst du in der neuen Akte (153/154/155) `ersetzt: ENT-10x` ein, wenn das Feld dort leer ist. Ist es belegt, setzt du in der alten Akte den Status „ersetzt durch ENT-…“.
   - ENT-109: ersetzt durch ENT-144.
   - ENT-147: Status „verworfen (Opus, delegiert durch Autor 2026-11-23)“.
   - Alle übrigen offenen Akten nach der Tabelle: `status: entschieden (Opus, delegiert durch Autor 2026-11-23)   # pm/freigaberunde_2026-11-23.md Runde 4`.
   - Neue Akten mit `pm.py neu`:
     - Zellzahl je Variante (Merkmal aus struktur.json, z. B. BT-210 zellen_je_reihe) und Zellabstand (BT-250 zellabstand_mm).
     - Werte **wie gebaut** aus der CAD-Ausgabe oder annahmen.json, ohne sie zu ändern.
     - Belege: ENT-006 und Pfad der CAD-Ausgabe.
     - Status wie oben.
   - Danach `pm.py pruefe` (0 Fehler), `register`, `parameter`.
3. **Annahmen:** In `cad/baukasten/annahmen*.json` ein Feld je Annahme ergänzen:
   - `status: "bestaetigt (Opus, delegiert)"`, wenn der Graph keine `verwendet`-Kante zeigt;
   - `status: "Stellgroesse Schleife 2"`, wenn eine Rechnung sie verwendet;
   - die Annahmen, die durch eine neue Akte ersetzt sind, bekommen den Status „ersetzt durch ENT-…“.

   Das CAD darf sich dadurch nicht ändern (nur ein Metadatenfeld). Prüfe, dass die Leser der Dateien das Feld vertragen.
4. **Anforderungen (Runden 1–3)** in `pm/anforderungen.json` und `docs/01_lastenheft.md` (Quelle der Wahrheit ist anforderungen.json; im Lastenheft den Text angleichen):
   - P07: L ≤ 2400 mm; H ≤ 130 mm im Zellbereich, Dom Schaltbox ≤ 250 mm; Masse LFP ≤ 528 kg, NMC ≤ 370 kg.
   - P09: Spreizung zwischen den Zellen. Der Nachweisschlüssel bleibt vorerst der Zellblockwert, mit dem Hinweis „neu auswerten: ΔT zwischen Zellen (Schleife 2)“.
   - P08, P10, P14, P03/P04, P12, P13, P15 und G02 laut Tabelle.

   Bei allen bestätigten Kriterien gilt `herkunft_kriterium: "Autor (Freigaberunde 2026-11-23)"` und `bestaetigt_autor: true`. G02 bekommt Priorität Muss.
   Das Messen der Höhe im Zellbereich und am Dom braucht CAD-Schlüssel. Wenn es sie nicht gibt, Nachweis „offen“ und melden.
5. **CAD nachher:** `bash cad/baukasten/lauf_g5.sh alle` (oder der Befehl, den rechnen/schritte.txt für G5 nutzt), danach Vergleich mit den Sicherungen: Kollisionen, Masse, Maße, Teilezahl. **Jede Abweichung** → die Akte zurück auf „vorgeschlagen“, parameter neu, und an Opus melden.
6. `verifikation.py`, `pm.py freigabe`, `graph.py`, `wissensnetz_obsidian.py`, `praesentation/erzeuge.py` und PDF neu erzeugen. Zeile in docs/08.

Rückmeldung höchstens 6 Zeilen: Akten gesetzt, neue Akten, CAD-Vergleich, neue Zählung V-Modell, was in docs/19 übrig bleibt.
