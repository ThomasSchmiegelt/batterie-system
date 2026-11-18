| Dok.-Nr. | Auftrag X1b-R | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Wiederaufsetzpunkte und neustart.sh für X1b | Ersteller | Claude Opus (KI) | Prüfer | Opus |

> KI-generiert, Opus → Sonnet, 2026-11-18. Autor: „schreibe auch ein .sh datei zum neustart die ich ohne dich ausführen kann, so das alles wieder startet“. Regel AGENTS.md → Rechnen → Wiederaufsetzpunkt.

Stand: LFP_w15 ist fertig. LFP_w20 und NMC_w15 laufen (kette.sh, nach_w15.sh). Ausstehend sind LFP_w30, NMC_w30 und NMC_w20.

1. Die laufenden Läufe und Skripte **nicht stören**. kette.sh, nach_w15.sh und lauf.sh nicht in place ändern, nur neue Dateien schreiben bzw. per `mv` ersetzen.
2. `x1b.py`, nur für neue Decks:
   - Pfahlweg in 10 Schritte teilen, Schritt k mit NBACK 2 = UMAX·k/10.
   - Im ersten Schritt `*RESTART,WRITE,FREQUENCY=1`.
   - Ausgabe wie bisher.
   - Dazu Erzeugung eines Fortsetzungsdecks `x1r.inp` mit `*RESTART,READ` (letzter fertiger Schritt aus der .rout) und den restlichen Schritten.
   - `auswerten.py` führt x1 und x1r zusammen.
   - Vorher an einem kleinen Netz testen: abbrechen nach Schritt 3, fortsetzen, Ergebnis gleich einem Durchlauf (Kraft < 2 %).
3. `neustart.sh` im Ordner, für den Autor:
   - Ohne Argumente: Läufe mit „fertig“ in ccx.log überspringen. Angefangene mit .rout fortsetzen (x1r). Angefangene ohne .rout (die alten Einschritt-Decks) neu starten. Übrige neu erzeugen und rechnen.
   - 2 Ketten mit je 4 Threads, jeder Lauf in `systemd-run --user --scope --unit=hermes-batterie-x1b-<fall>`, also pausierbar mit `~/bin/rechnung pause|weiter`. Losgelöst mit setsid nohup.
   - Am Ende `auswerten.py`.
   - Prüft vorher, ob schon ccx für x1b läuft, und bricht dann mit Meldung ab, damit nichts doppelt läuft.
   - Kopf mit Aufruf, Abbruch und Logdatei (`neustart.log`).
4. `LIESMICH_NEUSTART.md`, 5 Zeilen für den Autor: wann, wie, was passiert.
5. Neustart testen, ohne die laufenden Läufe zu stören: Trockenlauf `neustart.sh --zeigen`, der nur auflistet, was er tun würde.
Rückgabe höchstens 4 Zeilen.
