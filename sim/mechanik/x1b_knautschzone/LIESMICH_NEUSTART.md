| Dok.-Nr. | LIESMICH-X1b-R | Version | 0.2 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Neustart der X1b/X2-Läufe (OpenCourant) | Ersteller | Claude Sonnet (KI) | Prüfer | Opus (offen) |

> **KI-generiert**, Claude Sonnet, 2026-11-18. Entwurf, nicht freigegeben. Die alte CalculiX-Fassung steht in `LIESMICH_NEUSTART_ccx.md` und `neustart_ccx.sh`.

1. **Wann:** Nach Absturz, Neustart des Rechners oder Abbruch. Nicht starten, solange ein X2-Lauf aktiv ist (das Skript bricht dann selbst ab).
2. **Wie:** `cd /home/cae/hermes/batterie/sim/mechanik/x1b_knautschzone && bash neustart.sh` (vorher `bash neustart.sh --zeigen` listet nur auf, was getan würde). Einzelne Fälle: `bash neustart.sh LFP_w20`. Fälle: LFP_w20, LFP_w15, LFP_w30, NMC_w20.
3. **Was passiert:** Jeder Lauf besteht aus 10 Abschnitten, jeder endet normal und schreibt eine Restart-Datei `X2_<k>_0001.rst`. Fertige Fälle (`fertig.txt`) werden übersprungen, angefangene setzen beim ersten fehlenden Abschnitt fort (verloren geht höchstens ein Abschnitt, 1 bis 2 min), fehlende werden neu erzeugt. Zwei Ketten mit je 4 Threads, nur CPU, am Ende `auswerten_oc.py` (Bilder, `ergebnis_oc.json`).
4. **Pausieren und Abbrechen:** `~/bin/rechnung pause` und `weiter` (Scope `hermes-batterie-x2-<fall>`). Abbrechen mit `pkill -f neustart_haupt; pkill -f lauf_oc.sh; pkill -INT -f engine_linux64_gf`, danach gilt wieder Punkt 2.
5. **Wo nachsehen:** `neustart.log`, `lauf_oc/<fall>/engine_<k>.log` (Fortschritt, Zeit T in ms bis 50), Ergebnisse und Restart-Dateien liegen auf der großen Platte unter `/home/cae/cae_projekte/batterie/x2_lauf/<fall>/` (Symlink `lauf_oc/<fall>`); die `.rst` können nach der Auswertung gelöscht werden.

*KI-generiert, Entwurf. Dokument LIESMICH-X1b-R, Version 0.2.*
