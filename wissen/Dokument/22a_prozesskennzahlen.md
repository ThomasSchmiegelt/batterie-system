---
typ: dokument
nr: ""
version: ""
status: ""
tags: ["dokument"]
---
# 22a_prozesskennzahlen – Prozesskennzahlen (Zählung)

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

- Datei: `docs/22a_prozesskennzahlen`
- Version: –
- Status: –
- Typ: Projektdokument (Dokumentenlenkung [[Dokument/00_dokumentenlenkung]])

## Genannte Anforderungen (Textvorkommen)
- [[Anforderung/REQ-P09|REQ-P09]]

## Genannte Entscheidungen, Befunde, Bauteile (Textvorkommen)
- [[Befund/B-BAT-001|B-BAT-001]]
- [[Befund/B-BAT-002|B-BAT-002]]
- [[Befund/B-BAT-003|B-BAT-003]]
- [[Befund/B-BAT-004|B-BAT-004]]
- [[Befund/B-BAT-005|B-BAT-005]]
- [[Befund/B-BAT-006|B-BAT-006]]
- [[Befund/B-BAT-007|B-BAT-007]]
- [[Befund/B-BAT-008|B-BAT-008]]
- [[Befund/B-BAT-009|B-BAT-009]]
- [[Befund/B-BAT-010|B-BAT-010]]
- [[Befund/B-BAT-011|B-BAT-011]]
- [[Befund/B-BAT-012|B-BAT-012]]
- [[Befund/B-BAT-013|B-BAT-013]]
- [[Befund/B-BAT-014|B-BAT-014]]
- [[Befund/B-BAT-015|B-BAT-015]]
- [[Befund/B-BAT-016|B-BAT-016]]
- [[Befund/B-BAT-017|B-BAT-017]]
- [[Befund/B-BAT-018|B-BAT-018]]
- [[Befund/B-BAT-019|B-BAT-019]]
- [[Befund/B-BAT-020|B-BAT-020]]
- [[Befund/B-BAT-021|B-BAT-021]]
- [[Befund/B-BAT-022|B-BAT-022]]
- [[Befund/B-BAT-023|B-BAT-023]]
- [[Befund/B-BAT-024|B-BAT-024]]
- [[Befund/B-BAT-025|B-BAT-025]]
- [[Befund/B-BAT-026|B-BAT-026]]
- [[Befund/B-BAT-027|B-BAT-027]]
- [[Befund/B-BAT-028|B-BAT-028]]
- [[Befund/B-BAT-029|B-BAT-029]]
- [[Befund/B-BAT-030|B-BAT-030]]
- [[Befund/B-BAT-031|B-BAT-031]]
- [[Befund/B-BAT-032|B-BAT-032]]
- [[Befund/B-BAT-033|B-BAT-033]]
- [[Befund/B-BAT-034|B-BAT-034]]
- [[Befund/B-BAT-035|B-BAT-035]]
- [[Befund/B-BAT-036|B-BAT-036]]
- [[Befund/B-BAT-037|B-BAT-037]]
- [[Befund/B-BAT-038|B-BAT-038]]
- [[Befund/B-BAT-039|B-BAT-039]]
- [[Befund/B-BAT-040|B-BAT-040]]
- [[Befund/B-BAT-041|B-BAT-041]]
- [[Befund/B-BAT-042|B-BAT-042]]
- [[Befund/B-BAT-043|B-BAT-043]]
- [[Befund/B-BAT-044|B-BAT-044]]
- [[Befund/B-BAT-045|B-BAT-045]]
- [[Befund/B-BAT-046|B-BAT-046]]
- [[Befund/B-BAT-047|B-BAT-047]]
- [[Befund/B-BAT-048|B-BAT-048]]
- [[Entscheidung/ENT-013|ENT-013]]
- [[Entscheidung/ENT-014|ENT-014]]
- [[Entscheidung/ENT-081|ENT-081]]
- [[Entscheidung/ENT-151|ENT-151]]
- [[Entscheidung/ENT-152|ENT-152]]

## Vorgänge, die dieses Dokument nennen
- –

## Inhalt (Kopie aus `docs/22a_prozesskennzahlen.md`)

# Prozesskennzahlen (Zählung)

KI-generiert (Claude Haiku, 2026-11-23), Entwurf, Zählung für BAT-DOC-22 QN4.

Nur Zählung, keine Deutung. Zählungen per `grep` und `awk` am Stand 2026-11-23. Zeilennummern beziehen sich auf die jeweilige Datei. Stichwortsuche case-insensitiv, Treffer je Zeile (Wortteile wie „verfehlte“ zählen mit).

## 1. sim/**/ERWARTUNG.md

Spalte „Nachtrag Überschrift“ zählt Zeilen, die mit `#` beginnen und „Nachtrag“ enthalten. Spalte „Zeilen mit Nachtrag“ zählt alle Zeilen mit dem Wort „Nachtrag“.

| Ordner | Nachtrag (Überschrift) | Zeilen mit Nachtrag | „verfehlt“ (Zeilen) | „Erwartung verfehlt“ | „getroffen“ | „erfüllt“ (Zeilen) |
|---|---|---|---|---|---|---|
| sim/chemie/c1_zellmodell | 1 | 2 | 11 | 0 | 0 | – |
| sim/chemie/c2_kalibrierung | 1 | 2 | 15 | 0 | 0 | – |
| sim/chemie/varianten_lfp_nmc | 3 | 3 | 16, 25 | 0 | 0 | 12, 13, 24, 25, 28 |
| sim/chemie/vergleich_lfp_nmc | 1 | 1 | 19 | 0 | 0 | 15 |
| sim/elektrik/e1_querschnitte | 1 | 3 | 16, 21 | 0 | 0 | – |
| sim/elektrik/e2_elektronik | 4 | 5 | 33, 77, 99 | 0 | 0 | – |
| sim/geometrie/g1_anordnung | 3 | 4 | 14, 23, 29 | 0 | 0 | – |
| sim/kuehlung/k0_zelle | 1 | 2 | 11, 14 | 0 | 0 | – |
| sim/kuehlung/k1_schnellladen | 3 | 5 | 31, 38, 39, 43, 44 | 0 | 0 | 30, 38, 43 |
| sim/kuehlung/k2_kuehlplatte | 2 | 3 | 16, 26 | 0 | 0 | – |
| sim/kuehlung/k3_gesamt | 2 | 5 | 14, 18, 30 | 0 | 0 | – |
| sim/kuehlung/k5_parallel | 3 | 4 | 15, 21 | 0 | 0 | 23 |
| sim/mechanik/m0_gehaeuse | 1 | 1 | 17 | 0 | 0 | – |
| sim/mechanik/x1b_knautschzone | 2 | 3 | 24 | 0 | 0 | – |
| sim/mechanik/x1_seitencrash | 2 | 3 | 41 | 0 | 0 | 52 |
| sim/mechanik/x3_crash_g5 | 2 | 12 | 19, 22 | 0 | 0 | 20 |
| sim/vergleich_produkte | 0 | 0 | – | 0 | 0 | – |
| sim/verifikation_werkzeuge | 0 | 0 | 35 | 0 | 0 | – |

Summe der Spalte „Nachtrag (Überschrift)“: 32. Davon 16 Dateien mit mindestens einer Überschrift, 2 Dateien ohne (vergleich_produkte, verifikation_werkzeuge). Insgesamt 18 Dateien.

Hinweis: Die Zeile „Erwartung verfehlt“ (Wortlaut) kommt in keiner Datei vor. Das Wort „verfehlt“ steht in einzelnen Zeilen auch als „verfehlte“ (z. B. vergleich_lfp_nmc, Zeile 19).

## 2. BEFUNDE.md, Befunde ## B-BAT-NNN

Insgesamt 48 Befunde (Überschriften `## B-BAT-`). Sortiert nach Nummer. „In Klammern“ zeigt die Klammern der Überschrift, die nach dem Datum folgen. Ein Akteur steht nur dann dort, wenn er dort als Wort genannt ist.

| Nummer | Datum | Klammern in der Überschrift | Akteur in Klammern |
|---|---|---|---|
| B-BAT-001 | 2026-11-12 | (LFP) | – |
| B-BAT-002 | 2026-11-12 | – | – |
| B-BAT-003 | 2026-11-12 | (Opus-Fehler in lauf.sh) | – (Opus nur im Klammertext als Fehlerquelle) |
| B-BAT-004 | 2026-11-16 | (Struktur gegen Information) | – |
| B-BAT-005 | 2026-11-16 | (PI) | PI |
| B-BAT-006 | 2026-11-16 | – | – |
| B-BAT-007 | 2026-11-16 | – | – |
| B-BAT-008 | 2026-11-16 | – | – |
| B-BAT-009 | 2026-11-16 | (W20) | – |
| B-BAT-010 | 2026-11-16 | – | – |
| B-BAT-011 | 2026-11-16 | – | – |
| B-BAT-012 | 2026-11-17 | – | – |
| B-BAT-013 | 2026-11-17 | (ENT-013) | – |
| B-BAT-014 | 2026-11-17 | (ENT-014…029, vorgeschlagen) | – |
| B-BAT-015 | 2026-11-17 | – | – |
| B-BAT-016 | 2026-11-17 | (Opus-Fehler im Kern) | – (Opus nur im Klammertext als Fehlerquelle) |
| B-BAT-017 | 2026-11-17 | (REQ-P09, ENT-081) | – |
| B-BAT-018 | 2026-11-17 | – | – |
| B-BAT-019 | 2026-11-17 | (K1) | – |
| B-BAT-020 | 2026-11-17 | – | – |
| B-BAT-021 | 2026-11-17 | – | – |
| B-BAT-022 | 2026-11-17 | – | – |
| B-BAT-023 | 2026-11-17 | – | – |
| B-BAT-024 | 2026-11-18 | – | – |
| B-BAT-025 | 2026-11-18 | – | – |
| B-BAT-026 | 2026-11-18 | (Entwurf) | – |
| B-BAT-027 | 2026-11-18 | (0 mm Höhe) | – |
| B-BAT-028 | 2026-11-18 | (±1,3 %) | – |
| B-BAT-029 | 2026-11-18 | – | – |
| B-BAT-030 | 2026-11-18 | – | – |
| B-BAT-031 | 2026-11-18 | – | – |
| B-BAT-032 | 2026-11-19 | (ENT-151) | – |
| B-BAT-033 | 2026-11-19 | – | – |
| B-BAT-034 | 2026-11-19 | (Autor-Vorschlag ENT-152) | – |
| B-BAT-035 | 2026-11-19 | – | – |
| B-BAT-036 | 2026-11-20 | – | – |
| B-BAT-037 | 2026-11-21 | (Opus, aus den Laufausgaben der Sitzung 2026-11-19/20) | Opus |
| B-BAT-038 | 2026-11-21 | – | – |
| B-BAT-039 | 2026-11-21 | (2026-11-21, Opus) | Opus |
| B-BAT-040 | 2026-11-21 | (2026-11-21, Opus) | Opus |
| B-BAT-041 | 2026-11-22 | (2026-11-22, Opus) | Opus |
| B-BAT-042 | 2026-11-23 | (2026-11-23, Opus) | Opus |
| B-BAT-043 | 2026-11-23 | (2026-11-23, Opus) | Opus |
| B-BAT-044 | 2026-11-23 | (2026-11-23, Opus) | Opus |
| B-BAT-045 | 2026-11-23 | (2026-11-23, Opus) | Opus |
| B-BAT-046 | 2026-11-23 | (2026-11-23, Opus) | Opus |
| B-BAT-047 | 2026-11-23 | (2026-11-23, Opus) | Opus |
| B-BAT-048 | 2026-11-23 | (2026-11-23, Opus) | Opus |

Zusammen: Akteur „Opus“ in Klammern bei 11 Befunden (B-BAT-037, 039 bis 048). Akteur „PI“ bei 1 (B-BAT-005). Bei 36 Befunden steht kein Akteur in Klammern.

Auffälligkeit: Im Dokument stehen die Befunde nicht in Nummernfolge (z. B. B-BAT-025 und 038 vor 037). Die Tabelle ist nach Nummer sortiert. Bei B-BAT-039 bis 048 steht Datum und „Opus“ in derselben Klammer, bei B-BAT-037 steht „Opus“ im Klammerzusatz.

## 3. docs/08_ki_einsatz_protokoll.md

Gezählt werden Tabellenzeilen ab der Kopfzeile, ohne Kopf- und Trennzeile. Spalte 3 („Agent / Modell“). Wert wie dort geschrieben. Insgesamt 140 Zeilen.

| Akteur (Spalte „Agent / Modell“, wie geschrieben) | Zeilen |
|---|---|
| Sonnet (sonnet-umsetzer) | 73 |
| Sonnet (Agent sonnet-umsetzer) | 18 |
| Opus | 9 |
| Claude Opus | 7 |
| PI (lokal, --no-tools) | 4 |
| Haiku (haiku-helfer) | 4 |
| Sonnet (Agent) | 3 |
| PI (ohne Werkzeuge) | 3 |
| PI (lauf.sh) | 3 |
| PI (qwen-gross, ohne Werkzeuge) | 2 |
| PI (lokal) | 2 |
| web-fetch-Agent | 1 |
| Web-Abruf (Opus-Unteragent) | 1 |
| Sonnet (sonnet-umsetzer) + PI (qwen-gross, lokal) | 1 |
| Sonnet (Agent mit Websuche) | 1 |
| Sonnet ×2 (sonnet-umsetzer) | 1 |
| Sonnet | 1 |
| PI (warteschlange.sh, losgelöst) | 1 |
| PI (Gutachten) + Sonnet (sonnet-umsetzer) | 1 |
| Opus → Sonnet (2×), Haiku | 1 |
| Opus → Sonnet (2×) | 1 |
| Opus → Sonnet | 1 |
| Maschine + PI (ollama, Werkzeuge) | 1 |
| **Summe** | **140** |

Hinweis: Die Schreibweise ist uneinheitlich (z. B. „Sonnet (Agent sonnet-umsetzer)“, „Sonnet (sonnet-umsetzer)“, „Claude Opus“ und „Opus“). Die Werte sind so gezählt, wie sie dort stehen, nicht zusammengefasst.

## 4. Wächter und Alarm

| Pfad | „Wächter“ oder „waechter“ (Zeilen) | „Alarm“ (Zeilen) |
|---|---|---|
| rechnen/verlauf.log | 0 | 0 |
| sim/mechanik/x3_crash_g5 (Dateien direkt im Ordner) | 15 | 0 |

Aufschlüsselung x3_crash_g5: ERWARTUNG.md 4 Zeilen, lauf.sh 8 Zeilen, waechter_pruef.py 3 Zeilen. Unterordner `lauf/` und `__pycache__/` nicht einbezogen. Die Zahl 15 ist die Summe der drei Dateien.

