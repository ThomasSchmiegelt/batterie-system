#!/bin/bash
# KI-generiert (Claude Opus, 2026-11-25). Startet PI im Batterieprojekt, damit der Autor ohne Claude weiterarbeiten kann.
# PI liest AGENTS.md (Kontextdatei) und bekommt PI_START.md (Regeln + offene Arbeiten) als Zusatz-Systemprompt.
#
#   ./start_pi.sh                    neue Sitzung mit Kolibri 1 (Franconia)
#   ./start_pi.sh --weiter           letzte Sitzung fortsetzen
#   ./start_pi.sh --lokal            mit qwen-gross lokal (ollama) statt Kolibri
#   ./start_pi.sh -p "Frage"         eine Frage, dann Ende
#   ./start_pi.sh --modell <id> --anbieter <name>   anderes Modell (z. B. "Qwen 3.8 27B" bei franconia)
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; cd "$ROOT"
export PATH="$HOME/.npm-global/bin:$PATH"
PROVIDER="franconia"; MODEL="Kolibri 1"; ARGS=()
while [ $# -gt 0 ]; do
  case "$1" in
    --weiter)   ARGS+=(--continue) ;;
    --lokal)    PROVIDER="ollama"; MODEL="qwen-gross:latest" ;;
    --modell)   MODEL="$2"; shift ;;
    --anbieter) PROVIDER="$2"; shift ;;
    *)          ARGS+=("$1") ;;
  esac; shift
done
set +eu; [ -f umgebung.sh ] && source umgebung.sh >/dev/null 2>&1; set -eu
KEY=()
if [ "$PROVIDER" = "franconia" ]; then
  eval "$(grep '^export FRANCONIA_API_KEY=' ~/.bashrc | tail -1)" || true
  [ -n "${FRANCONIA_API_KEY:-}" ] || { echo "FEHLER: FRANCONIA_API_KEY fehlt in ~/.bashrc" >&2; exit 1; }
  KEY=(--api-key "$FRANCONIA_API_KEY")
elif [ "$PROVIDER" = "ollama" ]; then
  curl -sf --max-time 3 http://localhost:11434 >/dev/null || { echo "FEHLER: Ollama nicht erreichbar" >&2; exit 1; }
fi
echo "PI: $PROVIDER / $MODEL  –  Regeln und offene Arbeiten: PI_START.md"
exec pi --provider "$PROVIDER" --model "$MODEL" "${KEY[@]}" --append-system-prompt PI_START.md ${ARGS[@]+"${ARGS[@]}"}
