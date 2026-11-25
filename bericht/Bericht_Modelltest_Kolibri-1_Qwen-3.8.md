# Bericht: Praxistest der Sprachmodelle Kolibri 1 und Qwen 3.8 27B in einem technischen Entwicklungsablauf

| Version | Datum | Status | Ersteller |
|---|---|---|---|
| 2.0 | 2026-11-25 | Entwurf | KI-generiert (Claude Opus), Messwerte aus automatischen Protokollen |

Änderung gegenüber 1.0: Qwen 3.8 27B als zweites gehostetes Modell aufgenommen, dazu ein zweiter Fachtext-Lauf von Kolibri 1 mit Stilvorgabe.

## 1 Ziel
Der Test sollte zeigen, wie sich zwei gehostete Sprachmodelle in einem bestehenden, mehrstufigen KI-Arbeitsablauf eines technischen Entwicklungsprojekts bewähren:
- **Kolibri 1** (Aleph Alpha, Mixture-of-Experts, 78 Mrd. Parameter gesamt, 3,5 Mrd. aktiv, Deutsch und Englisch, Reasoning)
- **Qwen 3.8 27B** (dichtes Modell, 27 Mrd. Parameter, Reasoning)

Gemessen wurden Geschwindigkeit, Zuverlässigkeit der Antworten, Treue zu Quellen und Zahlen, Formattreue und die Qualität von Texten und Entscheidungen. Der Ablauf war ein Testprojekt zur Auslegung eines Batteriesystems.

## 2 Testaufbau
| Punkt | Ausführung |
|---|---|
| Zugang | beide Modelle über dieselbe OpenAI-kompatible API eines Drittanbieters. Der Server meldete für Kolibri die Variante `kolibri-1-fp8`. Die Quantisierung von Qwen 3.8 wurde nicht gemeldet |
| Aufruf | Kommandozeilen-Agent „pi“, ohne Werkzeuge (reiner Text rein, Text raus), ein Aufruf je Teilaufgabe |
| Steuerung und Prüfung | Ein anderes KI-Modell bereitete die Aufträge vor und prüfte jede Antwort mit Skripten. Die Bewertung erfolgte an den Rohdaten |
| Referenz | ein lokal betriebenes Modell der Vorgängerreihe (Qwen 3.5 27B, 4-Bit) mit denselben Eingaben, nur in Test A |
| Protokoll | je Aufruf: Dauer, Ausgabelänge, Prüfergebnis, Abbruch |
| Zeitraum | ein Arbeitstag, 46 protokollierte Aufrufe (Kolibri 43, Qwen 3.8 3) |

Kolibri 1 ließ sich nicht lokal betreiben: In FP8 braucht es rund 78 GB Grafikspeicher, vorhanden waren 24 GB.

**Einrichtung.** Für beide Modelle beim selben Anbieter waren dieselben zwei Anpassungen nötig:
- Der Server lehnt die Nachrichtenrolle `developer` ab (HTTP 422). Nötig ist deshalb die Kompatibilitätsoption „keine developer-Rolle“.
- Der API-Schlüssel musste ausdrücklich übergeben werden.

## 3 Aufgaben
| Test | Aufgabe | Prüfung | Kolibri 1 | Qwen 3.8 |
|---|---|---|---|---|
| A Recherche | Aus einem vorbereiteten Quellenpaket (Webseiten, Regelwerkstexte) Kennwerte mit wörtlichem Zitat und Quell-URL herausziehen. 3 Themen | Skript prüft jedes Zitat wörtlich gegen den abgerufenen Quelltext | ja | ja |
| B Fachtext | Aus einer Faktentabelle einen Sachbuchabschnitt schreiben, jede Zahl mit Verweis auf ihren Eintrag. Lauf 1 ohne, Lauf 2 mit Stilvorgabe, je 7 Abschnitte | Skript prüft jede Zahl gegen den genannten Eintrag, Stil und Zuschreibung gelesen | ja | nein |
| C Storyboard | Aus einer Datendatei ein Storyboard für ein Erklärvideo mit 6 Szenen entwerfen | jede Zahl und jeder Name gegen die Datendatei | ja | nein |
| D Rechenwächter | Eine laufende Rechnung (automatisches Leiterplatten-Routing) alle 30 s bewerten. Antwort nur als JSON: weiter, neu starten mit Parametern aus einer festen Erlaubtliste, fertig oder aufgeben | JSON-Gültigkeit, Erlaubtliste, Wirkung der Eingriffe | ja | nein |

Qwen 3.8 wurde erst im Lauf des Tages verfügbar und nur in Test A geprüft.

## 4 Messwerte

### 4.1 Geschwindigkeit und Verfügbarkeit
| Test | Modell | Aufrufe | Dauer je Aufruf (min / Median / max) | leere Antworten |
|---|---|---|---|---|
| A Recherche | Kolibri 1 | 3 | 35 / 55 / 59 s | 0 |
| A Recherche | Qwen 3.8 | 3 | 302 / 361 / 395 s | 0 |
| A Recherche | Referenz lokal | 3 | ≈ 140 s | 0 |
| B Fachtext, Lauf 1 | Kolibri 1 | 18 | 57 / 105 / 126 s | **9** |
| B Fachtext, Lauf 2 | Kolibri 1 | 7 | 37 / – / 75 s | 0 |
| C Storyboard | Kolibri 1 | 2 | 109 / – / 126 s | 1 |
| D Wächter | Kolibri 1 | 13 | 8 / 13 / 42 s | 0 |

- **Kolibri 1** gab rund **155 Token/s** aus (gemessen in Test A), davon etwa **90 % Reasoning-Token**, die nicht im Ergebnis erscheinen. Test D: 1 739–6 157 Token je Entscheidung.
- **Qwen 3.8** war in Test A **6- bis 8-mal langsamer** als Kolibri und auch langsamer als die lokale Referenz. Token je Sekunde wurden nicht erfasst.
- **Leere Antworten** traten nur bei Kolibri auf, nur bei großen Eingaben und nur nach 105–126 s Laufzeit. Das deutet auf eine Zeitgrenze beim Anbieter hin (nicht geprüft). In Lauf 2 von Test B waren die Teilaufträge kleiner, alle Antworten kamen nach höchstens 75 s, keine war leer. Qwen 3.8 lief bis 395 s ohne Abbruch. Eine feste Zeitgrenze für alle Modelle ist damit unwahrscheinlich.

### 4.2 Treue zu Quellen und Zahlen
| Test | Kolibri 1 | Qwen 3.8 | Referenz lokal |
|---|---|---|---|
| A Zitate (3 Themen) | 13 Zitate, **0 falsch** | **38 Zitate, 1 falsch** | 29 Zitate, 1 falsch |
| B Zahlen, Lauf 1 | 99 von 101 belegt, nach einer Korrekturrunde 103 von 103 | – | – |
| B Zahlen, Lauf 2 | 60 von 60 im genannten Eintrag | – | – |
| C Storyboard | 4 Werte gestrichen: ein Zielwert als Ergebnis ausgegeben, eine nicht vorhandene Summe gebildet | – | – |

In Test A fand Qwen 3.8 je Thema 10–17 belegte Werte, Kolibri 3–6.

### 4.3 Formattreue
- **Test A, Kolibri 1:** Die Vorgabe „URL in runden Klammern hinter dem Zitat“ wurde in keinem Fall eingehalten. Ohne Nachbearbeitung erkannte das Prüfskript kein einziges Zitat. Nach einer automatischen Formatkorrektur waren alle Zitate wörtlich richtig.
- **Test A, Qwen 3.8:** Das Format wurde eingehalten. Alle Zitate wurden ohne Nachbearbeitung erkannt.
- **Test B, Lauf 2, Kolibri 1:** Die Vorgabe „Fundstellen gesammelt am Absatzende“ wurde eingehalten.
- **Test D, Kolibri 1:** JSON-Antworten 13 von 13 gültig, Erlaubtliste 13 von 13 Mal eingehalten.

### 4.4 Qualität von Text und Entscheidungen (nur Kolibri 1)
- **Test B, Lauf 1, ohne Stilvorgabe:** Der Text bestand überwiegend aus aneinandergereihten Kurzsätzen mit einem Verweis nach fast jedem Satz. Einzelne Sätze waren sinnentstellt verkürzt. Eine Handlung der Software wurde einer Person zugeschrieben. Als Fließtext war das Ergebnis nicht verwendbar.
- **Test B, Lauf 2, mit Stilvorgabe:** Die Vorgabe umfasste zusammenhängende Absätze, Regeln zur Zuschreibung und einen Musterabsatz. Daraus entstand deutlich lesbarer, erzählender Fließtext, in dem auch die Fehler der Software sachlich benannt wurden. Es blieben drei Mängel:
  1. **eine erfundene Angabe über eine Person**, die in keiner Eingabe stand
  2. ein Wechsel der Erzählperspektive innerhalb des Textes
  3. Zahlen, die als Wort ausgeschrieben sind („acht“) und deshalb der automatischen Zahlenprüfung entgehen
  Das Ergebnis ist als Rohfassung zum Überarbeiten verwendbar, nicht als fertiger Text.
- **Test D, Entscheidungen:** Von 13 Entscheidungen waren 7 Neustarts und 6 „weiter“. Die Begründungen waren nachvollziehbar formuliert. Zwei Neustarts kamen jedoch nach nur 1–2 Durchläufen, bevor sich ein Trend zeigen konnte. Eine vielversprechende Variante wurde zweimal zu früh abgebrochen, zwei weitere erlaubte Varianten wurden nie versucht. Innerhalb der Grenze von 6 Neustarts wurde das Ziel nicht erreicht. Eine spätere Auswertung zeigte, dass die überwachte Rechnung selbst falsch aufgesetzt war: Eine Regeldatei fehlte, das Ziel war so nicht erreichbar. Die Ungeduld der Entscheidungen bleibt als Befund bestehen. Dass das Ziel verfehlt wurde, lässt sich dem Modell aber nicht zurechnen.

## 5 Beobachtungen
1. **Sehr hohe Treue zur Vorlage bei Kolibri 1.** In allen Tests wurden Zitate und Zahlen nahezu fehlerfrei aus den Unterlagen übernommen. Erfundene Zitate traten nicht auf.
2. **Stilvorgaben wirken stark.** Mit Musterabsatz und klaren Regeln wurde Kolibris Fließtext deutlich besser, und es gab keine leeren Antworten mehr. Angaben über Personen müssen trotzdem gegengelesen werden: Die automatische Zahlenprüfung findet sie nicht.
3. **Schwäche beim Ableiten über die Vorlage hinaus (Kolibri 1).** Wo eine eigene Ableitung verlangt war, etwa eine Summe statt eines Einzelwerts oder die Trennung von Ziel und Ergebnis, entstanden Fehler.
4. **Belegdichte und Format:** Qwen 3.8 zog fast dreimal so viele belegte Werte heraus wie Kolibri 1, bei gleich niedriger Fehlerquote und ohne Formatnachbearbeitung. Kolibri befolgt feste Ausgabeformate nur locker.
5. **Geschwindigkeit:** Kolibri 1 antwortete in Test A in unter einer Minute, Qwen 3.8 brauchte 5–7 Minuten.
6. **Ungeduldige Steuerentscheidungen (Kolibri 1).** Als Wächter reagierte das Modell auf kurzfristige Schwankungen, statt einen Trend abzuwarten.

## 6 Grenzen des Tests
- ein Arbeitstag, kleine Stichprobe (46 Aufrufe), eine Anwendung, ein Anbieter
- **Qwen 3.8 nur in Test A (3 Aufrufe).** Für Fachtext, Storyboard und Wächter liegt kein Vergleich vor.
- Aufrufe ohne Werkzeuge. Die Eignung als selbstständig arbeitender Agent mit Dateizugriff ist nicht geprüft.
- Die Quantisierung von Qwen 3.8 beim Anbieter ist unbekannt, die lokale Referenz lief in 4 Bit. Die Geschwindigkeiten hängen auch von Last und Infrastruktur des Anbieters ab.
- Die Prompts für Test A wurden für die Referenz entwickelt und nicht auf eines der beiden Modelle abgestimmt.
- Kosten wurden nicht erfasst.

## 7 Fazit
| Einsatz | Empfehlung |
|---|---|
| schnelle, quellentreue Extraktion, Faktengerüste | **Kolibri 1**, mit automatischer Format- und Zahlenprüfung danach |
| gründliche Recherche mit vielen belegten Werten | **Qwen 3.8 27B**, wenn Wartezeiten von Minuten tragbar sind |
| Fließtext | Kolibri 1 nur mit Stilvorgabe und Musterabsatz, als Rohfassung mit menschlicher Durchsicht, besonders bei Angaben über Personen |
| Aufgaben mit eigener Ableitung, Steuerung laufender Rechnungen | im Test nicht ausreichend (Kolibri 1), Qwen 3.8 nicht geprüft |

Allgemein empfohlen:
- kleine Teilaufträge
- automatische Prüfung hinter jedem Aufruf
- bei Wächteraufgaben eine feste Mindestlaufzeit vor jedem Neustart

Sinnvoll wäre ein Folgetest, der Qwen 3.8 in den Tests B bis D prüft, die Prompts auf beide Modelle abstimmt und den Werkzeuggebrauch untersucht.
