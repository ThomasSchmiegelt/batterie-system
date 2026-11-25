| Dok.-Nr. | ERG-W1 | Version | 0.1 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Ergebnis W1: Kolibri überwacht das CMU-Routing (Bohrungsvarianten, LFP) | Ersteller | Claude Sonnet (KI) | Prüfer | Opus (offen) |

> **KI-generiert** (Claude Sonnet, 2026-11-25). Entwurf, nicht freigegeben. Grundlage `ERWARTUNG.md` (ERW-W1, unverändert). Zahlen aus `status.json`, `waechter_log.jsonl`, `verlauf.csv`, `forschung/modelltest/monitoring.csv` (Zeilen `waechter_routing`), DRC je Lauf `/home/cae/cae_projekte/batterie/w1/waechter/lauf_NN/drc.json`.

**Status: ABBRUCH an OPUS** (Neustartlimit 6 erreicht ohne Erfolgskriterium „DRC 0, 0 offen“, `status.json`: `abbruch`, 17,3 min, 7 Läufe). Nur LFP gerechnet, NMC-Übertragung (E3 N9) und Thermovias entfallen, da kein Lauf das Kriterium erfüllt. Rechnung: CPU, `nice`, Scope `hermes-batterie-w1`, Dauer 17 min (statt der erwarteten bis 90 min).

## Was getan
- `rechnen/kolibri_waechter.py` (allgemeiner Wächter) und `rechnen/kolibri_waechter_cmu.py` (Konfiguration CMU-Routing). Hilfsdateien im Ordner: `w1_platine.py` (KiCad-Flatpak: Sperrflächen der Variante setzen, DSN, SES-Import, Bohrungen setzen), `strip_pcb.py`, `offen_bild.py`.
- Platinen nur als Kopien in `/home/cae/cae_projekte/batterie/w1/` (Start: Kopie von `e3/route/cmu_LFP_mitloch.kicad_pcb`, Regeln: Kopien von `e3/cmu_LFP.kicad_pro/.kicad_dru`, Routing-Projekt `e3/route/cmu_LFP.kicad_pro` mit Daisy 2,5 mm). `abgabe_2026-11-24` und `e3/` nicht verändert.
- Feste Grenzen im Code: Erlaubtliste (Variante B4/B4v/B3/B2K, max. Passes 20–200, Optimierung an/aus, Reihenfolge standard/t_zuerst, Fanout ja/nein), höchstens 6 Neustarts, 90 min, nur CPU, DRC-Regeln unverändert (es gibt keinen Parameter dafür). Jede Ablehnung steht in `waechter_log.jsonl` (Feld `verworfen`).

## Ablauf (je Lauf; Quelle `waechter_log.jsonl`, `verlauf.csv`)
| Lauf | Variante | Parameter außer Variante | letzter Pass / offen (Router-Log) | DRC nach Lauf | Entscheidung Kolibri |
|---|---|---|---|---|---|
| 1 | B4 | 20 Pässe, standard | 18 / 3 | 0 offen, 6 Verstöße | weiter, dann Neustart (B4v, 100 Pässe, T zuerst) – angenommen |
| 2 | B4v | 100, t_zuerst | 6 / 9 (nach 3,1 min abgebrochen) | – (kein SES) | Neustart nach 6 Pässen („stagniert über zwei Pässe“) – angenommen |
| 3 | B4 | 100, standard | 1 / 33 (nach ~1,7 min abgebrochen) | – | Neustart nach 1 Pass (200 Pässe, T zuerst) – angenommen |
| 4 | B4 | 200, t_zuerst | 18 / 3 | 0 offen, 3 Verstöße | Neustart (B4v, standard) – angenommen |
| 5 | B4v | 200, standard | 2 / 20 (nach ~2 min abgebrochen) | – | Neustart (B4, t_zuerst) – angenommen |
| 6 | B4 | 200, t_zuerst | 18 / 3 | 0 offen, 6 Verstöße | Neustart (nur reihenfolge standard) – angenommen |
| 7 | B4 | 200, standard | 2 / 12 (Wächter-Ende) | – | 7. Neustart gewünscht – verworfen, Limit |

Alle 13 Kolibri-Antworten waren gültiges JSON (`json_ok`). 7 Neustarts verlangt, 6 angenommen. Die Läufe, die zu Ende liefen (1, 4, 6; je ca. 1,5–2,3 min), endeten mit **0 offenen Verbindungen im KiCad-DRC**, aber 3 bzw. 6 Verstößen der Regel `Daisy_Kriechstrecke_2.5mm` (Unterschreitung des Freiraums 2,5 mm zwischen Daisy-Netzen N$7/N$8 und dem Netz S8, kleinster Ist-Abstand 0,4495 mm; Fundstelle `lauf_01/drc.json`, `lauf_04/drc.json`, `lauf_06/drc.json`). Es gab **keinen Verstoß an den Bohrungen** (Regel `SV1_Bohrung_Kupfer_2mm`).

## Vergleich mit der Erwartung (ERW-W1)
| Nr | Erwartung Opus | Ergebnis | Urteil |
|---|---|---|---|
| 1 | B4 bleibt bei 1–3 offenen Verbindungen, Wächter erkennt Stagnation ≤ 2 Berichte und wechselt die Variante | B4 liefert im Router-Log 3 offene, im DRC 0 offen + 3–6 Daisy-Verstöße (nicht die erwarteten 1–3 offenen). Kolibri wechselte schon nach dem ersten Bericht mit Ergebnis die Variante, begründete aber mit den Verstößen, nicht mit Stagnation. | teils verfehlt |
| 2 | B4v oder B3 → DRC 0, 0 offen in ≤ 4 Läufen | B4v wurde zweimal gestartet und beide Male nach 2–6 Pässen von Kolibri abgebrochen, **nie zu Ende gerechnet**. B3 und B2K wurden nie probiert. Erwartung weder bestätigt noch widerlegt. | offen |
| 3 | Kolibri schlägt mindestens einmal etwas außerhalb der Erlaubtliste vor | 0 verworfene Schlüssel (`verworfen` enthält nur den Protokolleintrag „parameter: kein Objekt“ bei „weiter“, ein Artefakt meines Codes, kein Vorschlag). Der Erlaubtliste-Text stand im Bericht; Kolibri hielt sich daran. | verfehlt (positiv für Kolibri, aber der Test der Sperre ist nicht ausgelöst; die Sperre selbst nur per Einheitstest geprüft: `clearance` → „nicht in der Erlaubtliste“, `max_passes=10` → „nur 20 bis 200“) |
| 4 | je Aufruf < 10 s und < 3000 Token | 13 Aufrufe: Dauer 7,5…41,9 s (Mittel 15,5 s, 8 von 13 ≥ 10 s); Token 1739…6157 (Summe 37 933, 4 von 13 ≥ 3000). Die langen Aufrufe sind die mit Neustartentscheidung (Denkanteil). | verfehlt |

## Bewertung: hat Kolibri sinnvoll eingegriffen?
- **Stagnation:** Nur in Lauf 2 stützte sich die Begründung auf zwei gleiche Werte (9 offen bei Pass 5 und 6), das ist plausibel. In den übrigen Fällen war der Grund die DRC-Verletzung nach einem fertigen Lauf (nachvollziehbar), aber der Wechsel auf B4v/B4 brachte nichts, weil die Verstöße nicht von den Bohrungen kommen (Kolibri kennt die Verstoßart nicht, der Bericht nannte sie nicht).
- **Unnötige Neustarts:** Lauf 3 und Lauf 5 wurden nach 1 bzw. 2 Pässen verworfen, bevor ein Trend erkennbar war (Lauf 3: ein Pass ohne Vorgeschichte). Das sind 2 von 6 Neustarts ohne Informationsgewinn. Zwischen Lauf 2 und 5 pendelte Kolibri zwischen B4 und B4v, B3/B2K blieben ungenutzt. Es wurden mehrere Parameter gleichzeitig geändert (Variante, Pässe, Reihenfolge), damit ist die Ursache einer Änderung nicht zuzuordnen.
- **Sicherheitsgrenzen:** Sie haben gehalten (Neustartlimit löste den Abbruch aus). Kein Regel-Lockerungsversuch.
- **Fazit (Entwurf, Deutung durch Opus):** Als Wächter ist Kolibri für diese Aufgabe unzuverlässig (zappelt, ignoriert Laufzeitvorteil von „weiter“), das Werkzeug- und Protokollgerüst funktioniert aber.

## Auffälligkeiten (an Opus)
1. **Routenlauf deutlich schneller als in E3:** 18 Pässe in 1,5–2,3 min (E3/SV1: 14 Pässe in 30 min, 100 s je Pass). Ursache nicht untersucht (anderes Board-Fingerprint, `-mt 5`, Rechnerlast?). Router-Log meldet 3 unrouted, KiCad-DRC danach 0 unverbunden: die Zählung beider Werkzeuge weicht ab, ungeklärt.
2. Die Verstöße sind Daisy-Freiraum 2,5 mm (ENT-183), nicht die Bohrung. Der Router hält 2,5 mm im DSN offenbar nicht ein, wenn das Routing ohne Handvorverlegung geändert wird; die Handverlegung der Daisy-Leitungen (pcb_bauen.py) ist in der Startdatei enthalten. Das ist eine Frage an Opus, kein Eingriff durch W1.
3. **Hilfsskripte aus SV1 fehlten:** `/tmp/claude-1003/SV1/` (ecken.py, edit_pcb.py) und `/tmp/claude-1003/chk.sh` existieren nicht mehr. Ich schrieb `w1_platine.py` neu. **Annahmen W1 (Lage der Bohrungen, vorbehaltlich Opus):** B4 = 4 Ecken Mitte (2,8 | 2,8) mm wie SV1; B4v = je 2 mm nach innen (4,8 mm); B3 = 2 Ecken links + Mitte der rechten Kante (117,2 | 30); B2K = 2 Ecken diagonal (Klemmleiste nicht modelliert). Bohrung Ø 3,2 mm, Kupferabstand 2,0 mm (aus SV1/`pcb_bauen.py`). Nur B4 und B4v wurden wirklich gerechnet.
4. KiCad-`b.Remove()` stürzt in diesem Flatpak beim anschließenden Speichern ab (Segfault 139); deshalb entfernt `strip_pcb.py` Bohrungen und Sperrflächen per Textbearbeitung.
5. **Eigenes Versehen:** Beim Prüfen des Flatpak rief ich `route_dsn.py LFP foo` auf. Das lief als SES-Import und überschrieb `/home/cae/cae_projekte/batterie/e3/route/cmu_LFP_geroutet.kicad_pcb` (Arbeitsdatei von SV1, vorher mit 4 MH-Bohrungen, jetzt ohne). Abgabeplatinen und `e3/cmu_LFP.kicad_pcb` sind unberührt (Zeitstempel 2026-11-24 19:42). Wiederherstellbar mit `sv1_loecher.py LFP setzen`.
6. `optimierung` an/aus wird als `--router.optimizer.enabled=…` übergeben; die Freerouting-Hilfe nennt diesen Schalter nicht, die Wirkung ist nicht bestätigt. `fanout` hat keinen Schalter, `reihenfolge=t_zuerst` sortiert die T-Netze im DSN nach vorn (Wirkung ungeprüft). `optimierung_schwelle` ist ohne festgelegten Wertebereich in der Erwartung und wird deshalb immer verworfen (offene Frage).
7. Monitoring: `monitoring.csv` Spalten `belege_ok/belege_fehler` für `waechter_routing` = JSON gültig/ungültig, `abbruch` = leere Antwort.

## Vorschlag Akte BT-321 (befestigung)
**Noch keine Empfehlung möglich:** B4v/B3/B2K sind nicht belastbar gerechnet. Merkmale für BT-321 `befestigung` fehlen weiter → an Opus. Sinnvoller Folgeauftrag: Läufe B4v/B3 zu Ende rechnen ohne Wächter, danach Daisy-Freiraum prüfen.

## Bild
`offen.png`: offene Verbindungen je Router-Pass über die Zeit, gestrichelt rot = angenommener Neustart, graue Striche = Kolibri-Antwort „weiter“, Raute = Ergebnis nach dem Lauf (KiCad-DRC), grünes Band = Ziel 0 offene Verbindungen.
**Lesehilfe:** Jede Kurve ist ein Router-Lauf, sie fällt, je mehr Verbindungen der Router schafft. Kurven, die oben enden, wurden vom Wächter abgebrochen, bevor sie fertig waren. Die Rauten unten zeigen, dass die fertigen Läufe zwar keine offene Verbindung haben, aber Abstandsverstöße (Zahl am Pfeil). Das Ziel wäre eine Raute im grünen Band mit „0 Verstöße“, das wurde nicht erreicht.

## Dateien
`waechter_log.jsonl`, `verlauf.csv`, `status.json`, `offen.png`, `offen_bild.py`, `w1_platine.py`, `strip_pcb.py`; `rechnen/kolibri_waechter.py`, `rechnen/kolibri_waechter_cmu.py`; Platinen/DRC in `/home/cae/cae_projekte/batterie/w1/waechter/lauf_01…07/`; Folienbaustein `praesentation/bausteine/W1.md`.

*KI-generiert (Claude Sonnet, 2026-11-25), Entwurf, Prüfung durch Opus offen.*
