# Bericht: Praxistest des Sprachmodells Kolibri 1 in einem technischen Entwicklungsablauf

| Version | Datum | Status | Ersteller |
|---|---|---|---|
| 1.0 | 2026-11-25 | Entwurf | KI-generiert (Claude Opus), Messwerte aus automatischen Protokollen |

## 1 Ziel
Der Test sollte zeigen, wie sich das Sprachmodell **Kolibri 1** (Aleph Alpha, Mixture-of-Experts, 78 Mrd. Parameter gesamt, 3,5 Mrd. aktiv, Deutsch und Englisch) in einem bestehenden, mehrstufigen KI-Arbeitsablauf eines technischen Entwicklungsprojekts bewährt. Gemessen wurden Geschwindigkeit, Zuverlässigkeit der Antworten, Treue zu Quellen und Zahlen, Formattreue und die Qualität von Entscheidungen. Der Ablauf war ein Testprojekt zur Auslegung eines Batteriesystems.

## 2 Testaufbau
| Punkt | Ausführung |
|---|---|
| Zugang | gehostete OpenAI-kompatible API eines Drittanbieters. Der Server meldete die Variante `kolibri-1-fp8` |
| Aufruf | Kommandozeilen-Agent „pi“, ohne Werkzeuge (reiner Text rein, Text raus), ein Aufruf je Teilaufgabe |
| Steuerung und Prüfung | Ein anderes KI-Modell bereitete die Aufträge vor und prüfte jede Antwort mit Skripten. Die Bewertung erfolgte an den Rohdaten |
| Vergleich | ein lokal betriebenes Modell der 27-Mrd.-Klasse (Qwen 3.5 27B, 4-Bit) mit denselben Eingaben, nur in Test A |
| Protokoll | je Aufruf: Dauer, Ausgabelänge, Token, Prüfergebnis, Abbruch |
| Zeitraum | ein Arbeitstag, 36 protokollierte Aufrufe |

Lokaler Betrieb war nicht möglich. Das Modell braucht in FP8 rund 78 GB Grafikspeicher, vorhanden waren 24 GB.

**Einrichtung.** Zwei Anpassungen waren nötig:
- Der Server lehnt die Nachrichtenrolle `developer` ab (HTTP 422). Deshalb ist für diesen Anbieter die Kompatibilitätsoption „keine developer-Rolle“ nötig.
- Der API-Schlüssel musste ausdrücklich übergeben werden.

## 3 Aufgaben
| Test | Aufgabe | Prüfung |
|---|---|---|
| A Recherche | Aus einem vorbereiteten Quellenpaket (Webseiten, Regelwerkstexte) Kennwerte mit wörtlichem Zitat und Quell-URL herausziehen. 3 Themen | Skript prüft jedes Zitat wörtlich gegen den abgerufenen Quelltext |
| B Fachtext | Aus einer Faktentabelle mit 78 Einträgen einen Sachbuchabschnitt schreiben. Jede Zahl mit Verweis auf ihren Eintrag. 7 Abschnitte | Skript prüft jede Zahl gegen den genannten Eintrag. Stil und Zuschreibung wurden gelesen |
| C Storyboard | Aus einer Datendatei ein Storyboard für ein Erklärvideo mit 6 Szenen und Einblendtexten entwerfen | jede Zahl und jeder Name gegen die Datendatei |
| D Rechenwächter | Eine laufende Rechnung (automatisches Leiterplatten-Routing) alle 30 s anhand eines Zustandsberichts bewerten. Antwort nur als JSON: weiter, neu starten mit Parametern aus einer festen Erlaubtliste, fertig oder aufgeben | JSON-Gültigkeit, Einhaltung der Erlaubtliste, Wirkung der Eingriffe |

## 4 Messwerte

### 4.1 Geschwindigkeit und Verfügbarkeit
| Test | Aufrufe | Dauer je Aufruf (min / Median / max) | leere Antworten |
|---|---|---|---|
| A Recherche | 3 | 35 / 55 / 59 s | 0 |
| B Fachtext | 18 | 57 / 105 / 126 s | **9** |
| C Storyboard | 2 protokolliert | 109 / – / 126 s | 1 |
| D Wächter | 13 | 8 / 13 / 42 s | 0 |

- Die Ausgabe lief mit rund **155 Token/s** (gemessen in Test A). Davon waren etwa **90 % Reasoning-Token**, die nicht im Ergebnis erscheinen.
- Das Vergleichsmodell brauchte für Test A lokal rund 140 s je Thema. Kolibri war damit 2,5- bis 4-mal schneller.
- **Leere Antworten** traten nur bei großen Eingaben auf und nur nach 105–126 s Laufzeit. Das deutet auf eine Zeitgrenze auf der Anbieterseite hin (nicht geprüft). Kleinere Teilaufträge beseitigten das.
- Test D: 1 739–6 157 Token je Entscheidung.

### 4.2 Treue zu Quellen und Zahlen
| Test | Ergebnis Kolibri 1 | Vergleichsmodell |
|---|---|---|
| A Zitate (3 Themen) | 13 Zitate, **0 falsch** | 29 Zitate, 1 falsch |
| B Zahlen | 99 von 101 belegt, nach einer Korrekturrunde 103 von 103 | – |
| C Storyboard | 4 Werte gestrichen: ein Zielwert als Ergebnis ausgegeben, eine nicht vorhandene Summe gebildet | – |

### 4.3 Formattreue
- **Test A:** Die Vorgabe „URL in runden Klammern hinter dem Zitat“ wurde in allen Fällen nicht eingehalten. Ohne Nachbearbeitung erkannte das Prüfskript deshalb kein einziges Zitat. Nach einer automatischen Formatkorrektur waren alle Zitate wörtlich richtig.
- **Test D:** JSON-Antworten 13 von 13 gültig. Die Erlaubtliste wurde 13 von 13 Mal eingehalten.

### 4.4 Qualität von Text und Entscheidungen
- **Test B, Stil:** Der Text bestand überwiegend aus aneinandergereihten Kurzsätzen mit einem Verweis nach fast jedem Satz. Einzelne Sätze waren sinnentstellt verkürzt. Es gab eine falsche Zuschreibung: Eine Handlung der Software wurde einer Person zugeschrieben. Als Fließtext ist das Ergebnis nicht verwendbar, als geprüftes Faktengerüst schon.
- **Test D, Entscheidungen:** Von 13 Entscheidungen waren 7 Neustarts und 6 „weiter“. Die Begründungen waren nachvollziehbar formuliert. Zwei Neustarts kamen jedoch nach nur 1–2 Durchläufen, bevor sich ein Trend zeigen konnte. Eine vielversprechende Variante wurde zweimal zu früh abgebrochen, zwei weitere erlaubte Varianten wurden nie versucht. Innerhalb der Grenze von 6 Neustarts wurde das Ziel nicht erreicht.

## 5 Beobachtungen
1. **Sehr hohe Treue zur Vorlage.** In allen Tests wurden Zitate und Zahlen nahezu fehlerfrei aus den gegebenen Unterlagen übernommen. Erfundene Zitate traten nicht auf.
2. **Schwäche beim Rechnen über die Vorlage hinaus.** Wo die Aufgabe eine eigene Ableitung verlangte, etwa Summe statt Einzelwert oder Ziel und Ergebnis unterscheiden, entstanden Fehler.
3. **Geringe Belegdichte.** In Test A zog Kolibri weniger als halb so viele belegte Werte heraus wie das Vergleichsmodell.
4. **Formatvorgaben werden locker befolgt.** Feste Ausgabeformate brauchen eine automatische Prüfung oder Nachbearbeitung.
5. **Ungeduldige Steuerentscheidungen.** Als Wächter reagierte das Modell auf kurzfristige Schwankungen, statt einen Trend abzuwarten. Dazu kommt eine Wartezeit von bis zu 42 s je Entscheidung.
6. **Antwortzeit hoch bei großen Eingaben.** Ab etwa 100 s Laufzeit traten leere Antworten auf.

## 6 Grenzen des Tests
- ein Arbeitstag, kleine Stichprobe (36 Aufrufe), eine Anwendung, ein Anbieter
- Aufrufe ohne Werkzeuge. Die Eignung als selbstständig arbeitender Agent mit Dateizugriff ist nicht geprüft.
- Das Vergleichsmodell lief lokal in 4-Bit-Quantisierung, Kolibri gehostet in FP8. Die Geschwindigkeiten sind daher nur bedingt vergleichbar.
- Die Prompts waren für das Vergleichsmodell entwickelt worden und nicht auf Kolibri abgestimmt.
- Kosten wurden nicht erfasst.

## 7 Fazit
Kolibri 1 eignet sich in diesem Ablauf für **schnelle, quellentreue Extraktion** und für **Faktengerüste**, wenn eine automatische Prüfung nachgeschaltet ist. Für **lesbaren Fließtext**, für **Aufgaben mit eigener Ableitung** und für **Steuerentscheidungen über laufende Rechnungen** reichte die Qualität im Test nicht aus. Empfohlen wird:
- kleine Teilaufträge, um leere Antworten zu vermeiden
- automatische Format- und Zahlenprüfung hinter jedem Aufruf
- bei Wächteraufgaben eine feste Mindestlaufzeit vor jedem Neustart

Ein Folgetest mit auf das Modell abgestimmten Prompts und einer Prüfung des Werkzeuggebrauchs wäre sinnvoll.
