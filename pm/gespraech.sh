#!/bin/bash
# gespraech.sh <BT-ID> ["Frage"] -- mit einem Bauteil sprechen (PI, lokales Modell, ohne Werkzeuge).
# KI-generiert (Claude Opus, 2026-11-11).
#   Mit Frage: eine Antwort, Protokoll in pm/gespraeche/<BT>_<zeit>.md, Aktenverweise werden geprüft.
#   Ohne Frage: interaktive PI-Sitzung mit dem Kontext (beenden mit Strg+D).
# Kontext entsteht ohne KI aus eigenen Projektdateien (pm.py kontext). PI hat keine Werkzeuge: es kann nichts lesen, ändern oder ausführen.
set -e; P="$(cd "$(dirname "$0")" && pwd)"; R="$(dirname "$P")"; BT="$1"; shift || true; MODELL="${MODELL:-qwen-gross:latest}"
python3 "$P/pm.py" parameter >/dev/null; python3 "$P/pm.py" kontext "$BT" >/dev/null
K="$P/gespraeche/kontext_$BT.md"
OPT=(--provider ollama --model "$MODELL" --no-tools --no-extensions --no-skills --no-prompt-templates --no-context-files --offline
     --system-prompt "$(cat "$P/ROLLE_BAUTEIL.md")")
if [ -z "$1" ]; then
  exec "$HOME/.npm-global/bin/pi" "${OPT[@]}" @"$K" "Stell dich kurz vor (2 Sätze) und warte auf meine Fragen."
fi
A="$P/gespraeche/${BT}_$(date +%F_%H%M%S).md"
ANTWORT=$("$HOME/.npm-global/bin/pi" "${OPT[@]}" --no-session -p @"$K" "$*" < /dev/null)
{ echo "# Gespräch mit $BT ($(date '+%F %T'), $MODELL, ohne Werkzeuge) – KI-generiert"; echo; echo "**Frage:** $*"; echo; echo "**Antwort:**"; echo; echo "$ANTWORT"; echo
  echo "**Aktenprüfung:**"; for x in $(echo "$ANTWORT" | grep -o -E '(ENT|REQ|B-BAT)-[A-Z]?[0-9]+' | sort -u); do grep -q -- "$x" "$K" && echo "- $x im Kontext ✓" || echo "- $x NICHT im Kontext ✗ (erfunden?)"; done; } > "$A"
cat "$A"
