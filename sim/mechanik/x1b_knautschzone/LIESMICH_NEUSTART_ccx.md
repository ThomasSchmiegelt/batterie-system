| Dok.-Nr. | LIESMICH-X1b-R | Version | 0.1 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Neustart der X1b-Läufe | Ersteller | Claude Sonnet (KI) | Prüfer | Opus (offen) |

> **KI-generiert**, Claude Sonnet, 2026-11-18. Entwurf, nicht freigegeben.

1. **Wann:** Nach Absturz, Neustart des Rechners oder Abbruch. Nicht starten, solange noch ein ccx für X1b läuft (das Skript bricht dann selbst ab).
2. **Wie:** `cd /home/cae/hermes/batterie/sim/mechanik/x1b_knautschzone && bash neustart.sh` (vorher `bash neustart.sh --zeigen` listet nur auf, was getan würde). Läufe, die an der Divergenz abbrachen, werden gemeldet und übersprungen, mit `--wiederholen` neu gerechnet.
3. **Was passiert:** Fertige Läufe (`Job finished` im Log) werden übersprungen, angefangene am letzten fertigen Schritt (von 10) aus der Restart-Datei fortgesetzt (`x1r1`, `x1r2` …), Läufe ohne Restart-Datei und fehlende neu gerechnet. Zwei Ketten mit je 4 Threads, nur CPU, am Ende `auswerten.py` (Bilder, ergebnis.json).
4. **Pausieren und Abbrechen:** `~/bin/rechnung pause` und `weiter` (Scope `hermes-batterie-x1b-<fall>`). Abbrechen mit `pkill -f neustart; pkill -x ccx`, danach gilt wieder Punkt 2.
5. **Wo nachsehen:** `neustart.log` (Ablauf), `lauf/<fall>/x1.sta` (Fortschritt, Spalte TOT TIME bis 1,0), Restart-Dateien (einige GB je Lauf) unter `/home/cae/cae_projekte/batterie/x1b_restart/`; sie können nach der Auswertung gelöscht werden.

*KI-generiert, Entwurf. Dokument LIESMICH-X1b-R, Version 0.1.*
