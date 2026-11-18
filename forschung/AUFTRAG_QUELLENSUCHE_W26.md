| Dok.-Nr. | Auftrag Q-W26 | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Quellensuche: Kühlung und Kontaktierung von Rundzellen bei BMW Gen6, Lucid, Rivian, Tesla 2170, weitere | Ersteller | Claude Opus (KI) | Prüfer | Opus |

> KI-generiert. Opus → Sonnet, 2026-11-17. Autor: „verteile die rechereche bitte an agenten wie sonnet haiku oder pi“.
1. Mit WebSearch (standard) offen zugängliche Quellen finden (Wikipedia, Herstellerseiten, batterydesign.net, Fachpresse, Google Patents), je Hersteller 1–2, zu: Zellformat, Kühlung (Boden/Seite/Pol), Zellverbinder/Kontaktierung, Fixierung (Kleber, Verguss, Halter).
2. Jede URL mit `curl -s -o /dev/null -w "%{http_code}"` prüfen (nur 200 aufnehmen; keine Seiten mit Bezahlschranke, keine gefälschten User-Agents).
3. Neue Zeile `W26` in `forschung/themen_wissen.tsv` (Format wie W25: Nr, Suchbegriffe kommagetrennt eng auf Maße/Kühlung/Verbinder, URLs mit Leerzeichen, max. 6, wozu). Nicht selbst zusammenfassen.
4. Dann `setsid nohup bash -c 'while pgrep -f "lauf.sh" >/dev/null; do sleep 20; done; bash forschung/lauf.sh wissen W26' > forschung/lauf_W26.log 2>&1 < /dev/null &` (GPU nur nacheinander).
Abbruch 15 min. Rückgabe ≤ 4 Zeilen: URLs je Hersteller, was fehlt.
