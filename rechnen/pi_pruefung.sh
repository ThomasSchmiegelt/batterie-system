#!/bin/bash
# KI-generiert (Claude Opus, 2026-11-20). PI (lokal, ollama, Werkzeuge read/bash/write) prüft einen Rechenordner gegen seine ERWARTUNG.md und schreibt PI_PRUEFUNG.md hinein.
cd /home/cae/hermes/batterie; D="$1"
timeout 3600 "$HOME/.npm-global/bin/pi" --provider ollama --model "${MODELL:-qwen-gross:latest}" --no-extensions --no-skills --no-session --tools read,bash,write -p \
"Ordner $D. Lies $D/ERWARTUNG.md und $D/ergebnis.json (und Logs dort). Schreibe NUR die Datei $D/PI_PRUEFUNG.md: je nummeriertem Erwartungspunkt der Ist-Wert mit Quelle (Datei, Schlüssel), erfüllt/verfehlt, dazu jede Zeile mit FEHLER/Error/Traceback aus den Logs. Keine Deutung, keine anderen Dateien ändern. Höchstens 40 Zeilen."
