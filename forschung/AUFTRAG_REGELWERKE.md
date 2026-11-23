# Auftrag Sonnet: Recherche der Regelwerke EU, USA und China (W35–W41)

KI-generiert (Claude Opus, 2026-11-23). Vorgabe des Autors (2026-11-23): China nur, falls in der EU nichts zu finden ist. Ein Vergleich China, EU und US ist trotzdem „hoch interessant“. Freigabe für den Plan: „ja, das klingt gut“.
Grundlage: `docs/07_normen_und_vorschriften.md`. Keine fremden Texte ins Repo. Pakete und Quellen bleiben, wo `paket.py` sie ablegt (gitignored).

## Getestete Zugänge (Opus, curl)
- EU-Amtsblatt: `https://publications.europa.eu/resource/celex/<CELEX>` mit `Accept: application/xhtml+xml` und `Accept-Language: eng` gibt 200 (Beispiel: 32023R1542). Bei `text/html` kommt 404.
- eCFR (USA): `https://www.ecfr.gov/api/renderer/v1/content/enhanced/current/title-49?part=571&section=571.305` gibt 200.
- unece.org: 403. eur-lex.europa.eu: WAF. Beide **nicht** umgehen, auch nicht mit falschem User-Agent.

## Aufgaben
1. `paket.py` muss diese Zugänge abrufen können, auch mit dem Accept-Header. Laufende Skripte nicht an Ort und Stelle ändern. Prüfe an W37, dass das Paket nicht leer ist und die gesuchten Begriffe enthält.
2. Themen in `forschung/themen_wissen.tsv`. Die vorhandenen Einträge W38 und W39 bleiben stehen und werden höchstens ergänzt.
   - **W35:** UN R100 Rev. 3 und GTR 20. Suche die CELEX-Nummern der Veröffentlichung im EU-Amtsblatt (UN-Regelungen stehen dort als „UN Regulation No 100“, CELEX-Präfix meist 4…X…). Den Weg zur Nummer hältst du fest.
   - **W36:** UN R94, R95 und R135 (Pfahl), jeweils mit dem Teil zur elektrischen Sicherheit nach dem Aufprall.
   - **W37:** EU 2023/1542 (Artikel zu Kennzeichnung, CO₂, Batteriepass, Entnehmbarkeit, Sicherheit stationär/Traktion), 2023/1230 Art. 1 (Ausnahmen Fahrzeuge) und 2024/1689.
   - **W40:** USA FMVSS 305 (eCFR). Prüfe auch, ob es 305a gibt.
   - **W41:** offene Berichte, die Prüfverfahren für Traktionsbatterien vergleichen (EU JRC, NREL, Sandia, NHTSA), mit Zugangsprüfung.
   - Suchbegriffe englisch, zum Beispiel: crush, kN, mechanical shock, vibration, fire resistance, external short circuit, overcharge, thermal propagation, warning, minutes, isolation resistance, Ω/V, electrolyte leakage, post-crash.
3. Jede URL mit HTTP 200 prüfen. Was nicht erreichbar ist, gehört in die Rückmeldung.
4. `rm forschung/STOP` (stammt vom Herunterfahren am 22.11., der Autor hat die Recherche freigegeben). Danach nacheinander und losgelöst (setsid), jedes Thema einzeln: `bash rechnen/gpu_warten.sh && bash forschung/lauf.sh wissen W35`, ebenso W36, W37, W38, W39, W40, W41. Das Log kommt nach `rechnen/log_regelwerke.txt`.
5. Nach jedem Thema `pruefe.py`. Gezählt werden die bestandenen und die fehlgeschlagenen Zitate je Thema.
6. Zeile in docs/08.

## Abbruch
Zurück an Opus geht, wenn ein Paket leer ist, ein Zugang nur durch Umgehung ginge oder ein Zitatprüfung mehr als 20 % Fehler hat. Du deutest keine Inhalte und übernimmst keine Werte ins Lastenheft. Rückmeldung höchstens 6 Zeilen.
