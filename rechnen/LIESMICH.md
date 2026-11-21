# Rechen-Warteschlange (anhalten, Rechner aus, weiterrechnen)
KI-generiert (Claude Opus, 2026-11-20), Entwurf. Autor 2026-11-20: „ich möchte die Berechnungen auch immer anhalten können und auch den rechner abschalten können … die berechnung wieder starten können.“

| Was | Befehl |
|---|---|
| Starten / Weiterrechnen (auch nach dem Einschalten) | `bash rechnen/start.sh` |
| Anhalten (sauber, Rechner darf danach aus) | `bash rechnen/halt.sh` → warten, bis „ANGEHALTEN – Rechner kann aus“ erscheint |
| Stand ansehen | `bash rechnen/status.sh` |
| Einen Schritt neu rechnen | `rm rechnen/fertig/<ID>` |

**So funktioniert es:** `rechnen/schritte.txt` listet die Schritte der Reihe nach (`ID | GPU ja/nein | Befehl`). Jeder fertige Schritt hinterlässt `rechnen/fertig/<ID>`. Beim Start werden fertige Schritte übersprungen.
**Anhalten:** `halt.sh` legt `rechnen/STOP` an und meldet es dem laufenden Schritt.
- Rechnungen mit Wiederaufsetzpunkt (OpenCourant `/STOP`, Elmer-Restart, FluidX3D-Zwischenstand) schreiben ihren Stand und hören auf. Beim Start rechnen sie von dort weiter.
- Kurze Schritte (Montage, Renders, Bericht) werden abgebrochen und beim nächsten Start ganz neu gerechnet.
- Jeder Schritt bekommt die Umgebungsvariable `RECHNEN_STOP=/home/cae/hermes/batterie/rechnen/STOP`. Lange Rechnungen müssen diese Datei regelmäßig prüfen und ihren Zwischenstand schreiben (Regel für neue Skripte, AGENTS.md „Wiederaufsetzpunkt“).
**GPU:** Schritte mit GPU = ja laufen nie gleichzeitig mit PI/ollama. Die Warteschlange arbeitet ohnehin nacheinander.
**Log:** `rechnen/verlauf.log`.
