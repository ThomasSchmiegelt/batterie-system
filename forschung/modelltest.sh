#!/usr/bin/env bash
# KI-generiert (Claude Opus, 2026-11-25). Modelltest: dasselbe Recherchepaket mit einem anderen Modell über PI rechnen,
# Zitate mit pruefe.py prüfen und je Lauf eine Zeile ins Monitoring schreiben. Die Ergebnisse von lauf.sh bleiben unberührt.
# Aufruf: bash forschung/modelltest.sh <provider> "<modell>" <kurzname> <auftrag:wissen|patente|werkzeuge> W51 W48 ...
# Beispiel: bash forschung/modelltest.sh franconia "Kolibri 1" kolibri wissen W51
set -u; cd "$(dirname "$0")"
PROV="$1"; MOD="$2"; KURZ="$3"; AUF="$4"; shift 4
S=~/.hermes/skills/cae/patent-recherche; W=~/.hermes/skills/cae/web-recherche
OUT=modelltest/$KURZ; mkdir -p "$OUT"; MON=modelltest/monitoring.csv
[ -f "$MON" ] || echo "datum;modell;thema;dauer_s;zeichen;belege_ok;belege_fehler;abbruch;belege_ok_roh" > "$MON"
KEY=(); if [ "$PROV" = franconia ]; then eval "$(grep '^export FRANCONIA_API_KEY=' ~/.bashrc | tail -1)"; KEY=(--api-key "$FRANCONIA_API_KEY"); fi
for nr in "$@"; do
  [ -f pakete/$nr.md ] || { echo "$nr: kein Paket"; continue; }
  urls=$(grep -E '^## https?://' pakete/$nr.md | sed 's/^## //')
  t0=$(date +%s)
  timeout 1800 "$HOME/.npm-global/bin/pi" --provider "$PROV" --model "$MOD" "${KEY[@]}" --no-tools --no-extensions --no-skills \
    --no-prompt-templates --no-context-files --no-session --mode json < /dev/null \
    -p @AUFTRAG_${AUF^^}.md @pakete/$nr.md "Führe den Auftrag für Paket $nr aus. Antworte NUR mit dem Inhalt der Ergebnisdatei (Markdown). Quell-URLs dieses Themas (wörtlich):
$urls
Zitiere als URL genau eine dieser Adressen, nie eine DOI oder andere Adresse." > $OUT/$nr.jsonl 2> $OUT/$nr.err
  rc=$?; dt=$(( $(date +%s) - t0 ))
  python3 $S/pi_antwort.py $OUT/$nr.jsonl pakete/$nr.md $OUT/$nr.roh.md >/dev/null 2>&1
  # Formatabweichung (Kolibri: URL ohne Klammern) zählen und normalisieren; Inhalt bleibt unverändert
  roh_ok=$(python3 $W/pruefe.py $OUT/$nr.roh.md 2>/dev/null | tail -1 | grep -oE "^[0-9]+" || echo 0)
  sed -E 's#(Beleg: "[^"]*") (https?://[^ |]+)#\1 (\2)#g' $OUT/$nr.roh.md > $OUT/$nr.md 2>/dev/null
  ok=0; fe=0; z=0
  if [ -s $OUT/$nr.md ]; then
    z=$(wc -m < $OUT/$nr.md); python3 $W/pruefe.py $OUT/$nr.md > $OUT/$nr.pruefung.txt 2>&1
    ok=$(grep -oE '[0-9]+ Belege bestaetigt' $OUT/$nr.pruefung.txt | grep -oE '^[0-9]+' || echo 0)
    fe=$(grep -oE '[0-9]+ Fehler' $OUT/$nr.pruefung.txt | tail -1 | grep -oE '^[0-9]+' || echo 0)
  fi
  echo "$(date '+%F %T');$KURZ;$nr;$dt;$z;$ok;$fe;$rc;$roh_ok" | tee -a "$MON"
done
