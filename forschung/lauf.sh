#!/bin/bash
# lauf.sh [patente|wissen|werkzeuge] [nr] -- PI-Rechercheagent für Patente und Wissensaufbau, sicher in drei Stufen.
# KI-generiert (Claude Opus, 2026-11-11). Vorlage: fusion/docs/recherche/pi (Belegprüfung), moltbot (PI ohne Werkzeuge).
#
#  A  paket.py (keine KI): sucht/holt Patentschriften bzw. Seiten -> pakete/<nr>.md, Rohtexte recherche_ablage/
#  B  PI ohne Werkzeuge (--no-tools, kein Netz, keine Dateien): liest AUFTRAG + Paket, antwortet -> ergebnis/<nr>.md
#  C  pruefe.py: steht jedes Zitat wörtlich in der abgerufenen Quelle? -> ergebnis/<nr>.pruefung.txt
# Warum ohne Werkzeuge: fremde Texte können versteckte Anweisungen enthalten; ohne Sandbox (bwrap durch AppArmor gesperrt)
# sähe PI mit Lese-Werkzeug das ganze Home (auth.json). So kann das Modell nur antworten.
# Pausieren: ~/bin/rechnung pause (Scope hermes-batterie-recherche). Abbruch: touch STOP. Fertige Themen werden übersprungen.
# Dauer: je Thema ca. 1 min Stufe A, 3-8 min Stufe B (qwen-gross, GPU; nicht gleichzeitig mit GX auf der GPU).
cd "$(dirname "$0")"; ART="${1:-alle}"; NUR="${2:-}"; MODELL="${MODELL:-qwen-gross:latest}"
S=~/.hermes/skills/cae/patent-recherche; W=~/.hermes/skills/cae/web-recherche; mkdir -p pakete ergebnis
log() { echo "$(date '+%F %T') $*" | tee -a verlauf.log; }
sammeln() {   # Zwischenstand: Sammeldateien nach JEDEM Thema neu schreiben (Nutzer 2026-11-12: „denk daran das pi zwischenspeichert“)
python3 - <<'PY'
from pathlib import Path
for art, k in (("patente", "P"), ("wissen", "W"), ("werkzeuge", "T")):
    e = sorted(Path("ergebnis").glob(f"{k}[0-9]*.md"))
    if not e: continue
    t = [f"# {art.capitalize()} – Ergebnis PI (UNGEPRÜFT durch Menschen)\n\nKI-generiert: PI (lokales Modell, ohne Werkzeuge) aus abgerufenen Texten; Zitate automatisch geprüft (pruefe.py).\n"]
    for f in e:
        if f.name.endswith(".pruefung.txt"): continue
        p = f.with_suffix(".pruefung.txt")
        t.append(f"\n## {f.stem}\n\n{f.read_text()}\n\nPrüfung: {p.read_text().strip().splitlines()[-1] if p.exists() else 'fehlt'}\n")
    Path(f"{art.upper()}.md").write_text("".join(t))
PY
}
thema() {   # $1 = patente|wissen, $2 = nr, Rest = Paketargumente
  local art=$1 nr=$2 auf=${AUF:-$1}; shift 2
  [ -e STOP ] && { log STOP; exit 0; }
  [ -s ergebnis/$nr.md ] && { log "$nr schon fertig"; return; }
  [ -s pakete/$nr.md ] || python3 $S/paket.py $art $nr "$@" >> verlauf.log 2>&1 || { log "$nr Paket fehlgeschlagen"; return; }
  # B-BAT-009: Quell-URLs des Pakets wörtlich an PI (Stufe A holt sie, Stufe B darf nur diese zitieren)
  local urlliste; urlliste=$(grep -E '^## https?://' pakete/$nr.md | sed 's/^## //')
  local urlsatz="Quell-URLs dieses Themas (wörtlich):
$urlliste
Zitiere als URL genau eine dieser Adressen, nie eine DOI oder andere Adresse."
  log "$nr PI startet"
  timeout 1800 systemd-run --user --scope --unit=hermes-batterie-recherche-$nr-$$ -q \
    "$HOME/.npm-global/bin/pi" --provider ollama --model "$MODELL" --no-tools --no-extensions --no-skills \
      --no-prompt-templates --no-context-files --no-session --offline --mode json < /dev/null \
      -p @AUFTRAG_${auf^^}.md @pakete/$nr.md "Führe den Auftrag für Paket $nr aus. Antworte NUR mit dem Inhalt der Ergebnisdatei (Markdown). $urlsatz" \
    > ergebnis/$nr.jsonl 2> ergebnis/$nr.err
  python3 $S/pi_antwort.py ergebnis/$nr.jsonl pakete/$nr.md ergebnis/$nr.md | tee -a verlauf.log
  [ -s ergebnis/$nr.md ] && { python3 $W/pruefe.py ergebnis/$nr.md > ergebnis/$nr.pruefung.txt 2>&1; log "$nr $(tail -1 ergebnis/$nr.pruefung.txt)"; }
  sammeln
  python3 ../pm/plan/wissensnetz.py >/dev/null 2>&1 && python3 ../pm/plan/wissensnetz_ansicht.py >/dev/null 2>&1   # Wissensnetz live
}
if [ "$ART" = patente ] || [ "$ART" = alle ]; then
  # Tab ist für read ein Leerraumzeichen: leere Felder würden zusammengefasst (Inhaber leer -> Spalten verrutscht, B-BAT-003).
  # Deshalb Tabs vorher in ein Nicht-Leerraumzeichen tauschen.
  grep -v '^#' themen_patente.tsv | tr '\t' '\037' | while IFS=$'\037' read -r nr inh q wozu; do
    [ -n "$NUR" ] && [ "$NUR" != "$nr" ] && continue
    thema patente "$nr" "$q" --n 6 --ab 2015 ${inh:+--inhaber "$inh"}
  done
fi
if [ "$ART" = wissen ] || [ "$ART" = alle ]; then
  grep -v '^#' themen_wissen.tsv | while IFS=$'\t' read -r nr such urls wozu; do
    [ -n "$NUR" ] && [ "$NUR" != "$nr" ] && continue
    thema wissen "$nr" $urls --suche "$such"
  done
fi
if [ "$ART" = werkzeuge ] || [ "$ART" = alle ]; then
  grep -v '^#' themen_werkzeuge.tsv | while IFS=$'\t' read -r nr such urls wozu; do
    [ -n "$NUR" ] && [ "$NUR" != "$nr" ] && continue
    AUF=werkzeuge thema wissen "$nr" $urls --suche "$such"
  done
fi
sammeln
log "LAUF FERTIG ($ART)"
