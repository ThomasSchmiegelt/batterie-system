---
title: "Praxistest der Sprachmodelle Kolibri 1 und Qwen 3.8 27B in einem technischen Entwicklungsablauf"
subtitle: "Testbericht, Version 2.1 vom 25.11.2026"
lang: de
---

| Version | Datum | Status | Ersteller |
|---|---|---|---|
| 2.1 | 25.11.2026 | Entwurf | KI-generiert (Claude Opus, Anthropic). Alle Messwerte stammen aus automatischen Protokollen |

# Kurzfassung

Zwei KI-Sprachmodelle wurden einen Arbeitstag lang in einem echten Entwicklungsablauf eingesetzt: **Kolibri 1** des deutschen Herstellers Aleph Alpha und **Qwen 3.8 27B** des chinesischen Herstellers Alibaba. Beide liefen auf den Servern eines Anbieters, nicht auf eigener Hardware. Sie bekamen Aufgaben aus einem Testprojekt, in dem ein Batteriesystem für ein Elektroauto rechnerisch ausgelegt wird. Jede Antwort wurde automatisch geprüft.

**Wichtigste Ergebnisse:**

- **Kolibri 1 ist schnell und sehr quellentreu.** Werte aus Unterlagen übernahm es fast fehlerfrei, eine Rechercheaufgabe dauerte unter einer Minute. Es fand aber nur wenige Werte, hielt vorgegebene Ausgabeformate kaum ein und machte Fehler, sobald es selbst etwas ableiten sollte.
- **Qwen 3.8 ist gründlich, aber langsam.** In der Recherche fand es fast dreimal so viele belegte Werte wie Kolibri, bei ebenso wenigen Fehlern und mit korrektem Format. Es brauchte dafür aber 5 bis 7 Minuten je Aufgabe. Qwen 3.8 wurde nur in dieser einen Aufgabe geprüft.
- **Texte schreiben (nur Kolibri geprüft):** Ohne genaue Stilvorgabe entstand unbrauchbarer Text. Mit Stilvorgabe und einem Musterabsatz wurde er gut lesbar. Er enthielt aber eine frei erfundene Angabe über eine Person und muss deshalb von einem Menschen gegengelesen werden.
- **Überwachung einer laufenden Rechnung (nur Kolibri geprüft):** Die Antworten waren formal immer korrekt. Die Entscheidungen waren aber ungeduldig: Kolibri startete die Rechnung zu früh neu, statt die Entwicklung abzuwarten.

**Empfehlung:** Kolibri 1 für schnelles Herausziehen von Werten aus Unterlagen, Qwen 3.8 für gründliche Recherche. Beide nur mit automatischer Prüfung dahinter. Texte über Personen nie ungeprüft übernehmen.

# 1 Begriffe

| Begriff | Bedeutung in diesem Bericht |
|----|----------------|
| Sprachmodell | KI-Programm, das auf eine Texteingabe (Auftrag) einen Text als Antwort erzeugt |
| gehostet | Das Modell läuft auf den Servern eines Anbieters. Man schickt den Auftrag über das Internet und erhält die Antwort zurück |
| API | die technische Schnittstelle, über die ein Programm dem Anbieter Aufträge schickt |
| Parameter | Kennzahl für die Größe eines Modells (Milliarden gelernter Zahlenwerte). Mehr Parameter bedeuten meist mehr Wissen, aber auch mehr Rechenaufwand |
| Mixture-of-Experts | Bauart, bei der für jede Antwort nur ein Teil des Modells rechnet. Kolibri 1 hat 78 Mrd. Parameter, davon rechnen je Antwort nur 3,5 Mrd. Das macht es schnell |
| Reasoning | Das Modell „denkt“ vor der Antwort in einem verborgenen Zwischentext nach. Das kostet Zeit, verbessert aber oft das Ergebnis |
| Token | Rechen- und Abrechnungseinheit eines Sprachmodells, etwa ein Wortteil. Rund 1 000 Token entsprechen etwa 700 deutschen Wörtern |
| FP8, 4-Bit | Rechengenauigkeit, mit der ein Modell betrieben wird. Geringere Genauigkeit spart Speicher und Zeit und kann die Qualität leicht senken |
| Zitatprüfung | Ein Programm sucht jedes Zitat, das das Modell angibt, Zeichen für Zeichen im Originaltext der Quelle. Fehlt es dort, gilt es als falsch |
| Zahlenprüfung | Ein Programm prüft, ob jede Zahl im erzeugten Text in der Quelle steht, auf die der Text verweist |
| JSON | festes, maschinenlesbares Textformat für Daten, hier für die Antworten in Test D |
| leere Antwort | Der Aufruf endete ohne Fehlermeldung, aber das Modell lieferte keinen Text |

# 2 Ziel

Der Test sollte klären, ob sich die beiden Modelle für Aufgaben in einem technischen Entwicklungsablauf eignen und wofür jeweils. Gemessen wurden:

- **Geschwindigkeit:** Wie lange dauert eine Antwort?
- **Verfügbarkeit:** Kommt überhaupt eine Antwort?
- **Quellentreue:** Stimmen Zitate und Zahlen mit den Unterlagen überein?
- **Formattreue:** Hält das Modell eine vorgegebene Ausgabeform ein?
- **Qualität:** Sind Texte lesbar und Entscheidungen sinnvoll?

| | Kolibri 1 | Qwen 3.8 27B |
|---|---|---|
| Hersteller | Aleph Alpha (Deutschland) | Alibaba (China) |
| Bauart | Mixture-of-Experts, 78 Mrd. Parameter, davon 3,5 Mrd. je Antwort aktiv | alle 27 Mrd. Parameter rechnen bei jeder Antwort |
| Sprachen laut Hersteller | Deutsch, Englisch | viele, darunter Deutsch |
| Reasoning | ja | ja |

# 3 Testaufbau

Ein Entwicklungsprojekt arbeitet hier mit mehreren KI-Modellen, die sich die Aufgaben teilen. Ein leitendes Modell (Claude Opus von Anthropic) schrieb die Aufträge für die beiden Testmodelle, schickte sie ab und prüfte jede Antwort mit Prüfprogrammen. Bewertet wurde immer anhand der tatsächlichen Antwort und der Originalquellen, nicht anhand einer Zusammenfassung.

| Punkt | Ausführung |
|----|----------------|
| Zugang | Beide Modelle liefen gehostet beim selben Anbieter. Kolibri 1 lief dort in FP8, für Qwen 3.8 nannte der Anbieter die Rechengenauigkeit nicht |
| Arbeitsweise | Jede Teilaufgabe wurde als einzelner Auftrag geschickt: Text hinein, Text heraus. Die Modelle durften keine Dateien lesen und keine Programme starten |
| Vergleichsmodell | Qwen 3.5 27B, die Vorgängerversion von Qwen 3.8, auf eigener Hardware in 4-Bit. Es bekam in Test A dieselben Aufträge |
| Protokoll | Für jeden Aufruf wurden Dauer, Länge der Antwort, Prüfergebnis und Abbrüche gespeichert |
| Umfang | ein Arbeitstag, 46 Aufrufe: 43 mit Kolibri 1, 3 mit Qwen 3.8 |

Kolibri 1 ließ sich nicht auf eigener Hardware betreiben. Es braucht rund 78 GB Grafikspeicher, vorhanden waren 24 GB.

**Einrichtung.** Bei beiden Modellen waren zwei kleine technische Anpassungen nötig, damit das verwendete Steuerprogramm mit dem Anbieter zusammenarbeitet. Danach liefen beide ohne weitere Störung.

# 4 Aufgaben

**Test A, Recherche.** Das Modell bekam ein Paket mit Texten von Webseiten und aus technischen Regelwerken. Es sollte daraus technische Kennwerte heraussuchen und zu jedem Wert das wörtliche Zitat und die Quelladresse angeben. Drei Themen. Prüfung: Zitatprüfung.

**Test B, Fachtext.** Das Modell bekam eine Tabelle mit nummerierten Fakten zum Projektverlauf. Daraus sollte es einen Abschnitt für ein Sachbuch schreiben, mit Verweis auf die Faktennummer bei jeder Zahl. Zwei Läufe mit je 7 Abschnitten: Lauf 1 mit einfachem Auftrag, Lauf 2 mit ausführlicher Stilvorgabe und einem Musterabsatz. Prüfung: Zahlenprüfung, dazu wurden Stil und Richtigkeit gelesen.

**Test C, Storyboard.** Aus einer Datei mit Projektdaten sollte das Modell den Ablauf eines kurzen Erklärvideos entwerfen (6 Szenen mit Einblendtexten). Prüfung: Jede Zahl und jeder Name wurde mit der Datei verglichen.

**Test D, Überwachung einer Rechnung.** Ein Programm verlegte automatisch die Leiterbahnen einer Elektronikplatine. Diese Rechnung dauert mehrere Minuten und gelingt nicht immer. Das Modell bekam alle 30 Sekunden einen kurzen Zwischenstand und sollte entscheiden: weiterlaufen lassen, mit anderen Einstellungen neu starten, als fertig erklären oder aufgeben. Die erlaubten Einstellungen waren in einer festen Liste vorgegeben, die Antwort musste im JSON-Format kommen. Prüfung: Format, Einhaltung der Liste, Wirkung der Eingriffe.

| Test | Kolibri 1 | Qwen 3.8 |
|---|---|---|
| A Recherche | geprüft | geprüft |
| B Fachtext | geprüft | nicht geprüft |
| C Storyboard | geprüft | nicht geprüft |
| D Überwachung | geprüft | nicht geprüft |

Qwen 3.8 stand erst im Lauf des Tages zur Verfügung. Deshalb wurde es nur in Test A geprüft.

# 5 Ergebnisse

## 5.1 Geschwindigkeit und Verfügbarkeit

| Test | Modell | Aufrufe | Dauer je Aufruf | leere Antworten |
|---|---|---|---|---|
| A Recherche | Kolibri 1 | 3 | 35 bis 59 s | 0 |
| A Recherche | Qwen 3.8 | 3 | 302 bis 395 s | 0 |
| A Recherche | Vergleichsmodell | 3 | etwa 140 s | 0 |
| B Fachtext, Lauf 1 | Kolibri 1 | 18 | 57 bis 126 s | **9** |
| B Fachtext, Lauf 2 | Kolibri 1 | 7 | 37 bis 75 s | 0 |
| C Storyboard | Kolibri 1 | 2 | 109 bis 126 s | 1 |
| D Überwachung | Kolibri 1 | 13 | 8 bis 42 s | 0 |

- **Kolibri 1** erzeugte rund 155 Token je Sekunde. Etwa 90 % davon entfielen auf das verborgene Nachdenken (Reasoning), nur etwa 10 % auf die sichtbare Antwort.
- **Qwen 3.8** war in Test A 6- bis 8-mal langsamer als Kolibri 1 und auch langsamer als das Vergleichsmodell auf eigener Hardware.
- **Leere Antworten** gab es nur bei Kolibri 1, und nur bei langen Aufträgen, die nach 105 bis 126 Sekunden abbrachen. Vermutlich begrenzt der Anbieter die Laufzeit, das wurde aber nicht geprüft. In Lauf 2 von Test B waren die Aufträge kürzer, alle Antworten kamen nach höchstens 75 Sekunden, keine war leer. Qwen 3.8 lief beim selben Anbieter bis zu 395 Sekunden ohne Abbruch. Eine einheitliche Zeitgrenze für alle Modelle ist deshalb unwahrscheinlich.

## 5.2 Quellentreue

| Test | Kolibri 1 | Qwen 3.8 | Vergleichsmodell |
|---|---|---|---|
| A: Zitate über alle 3 Themen | 13 Zitate, **keines falsch** | **38 Zitate, 1 falsch** | 29 Zitate, 1 falsch |
| B, Lauf 1: Zahlen mit Beleg | 99 von 101, nach einer Korrekturrunde 103 von 103 | – | – |
| B, Lauf 2: Zahlen mit Beleg | 60 von 60 | – | – |
| C: Storyboard | 4 Fehler: ein Zielwert als erreichtes Ergebnis ausgegeben, eine Summe gebildet, die es in den Daten nicht gab | – | – |

Je Thema fand Qwen 3.8 in Test A 10 bis 17 belegte Werte, Kolibri 1 nur 3 bis 6.

## 5.3 Formattreue

- **Kolibri 1, Test A:** Der Auftrag verlangte die Quelladresse in runden Klammern hinter dem Zitat. Kolibri hielt das in keinem Fall ein. Das Prüfprogramm erkannte deshalb zunächst kein einziges Zitat. Erst nachdem ein Programm das Format automatisch angepasst hatte, ließ sich prüfen: Alle Zitate waren wörtlich richtig.
- **Qwen 3.8, Test A:** Das Format wurde eingehalten, alle Zitate waren ohne Anpassung prüfbar.
- **Kolibri 1, Test B, Lauf 2:** Die Vorgabe „Belege gesammelt am Absatzende“ wurde eingehalten.
- **Kolibri 1, Test D:** Alle 13 Antworten waren gültiges JSON, alle hielten die Liste der erlaubten Einstellungen ein.

## 5.4 Qualität von Text und Entscheidungen (nur Kolibri 1)

**Test B, Lauf 1, einfacher Auftrag.** Der Text bestand überwiegend aus kurzen, aneinandergereihten Sätzen mit einem Verweis nach fast jedem Satz. Einzelne Sätze waren so verkürzt, dass der Sinn verloren ging. Eine Handlung, die die Software ausgeführt hatte, wurde einer Person zugeschrieben. Als lesbarer Text war das Ergebnis nicht verwendbar.

**Test B, Lauf 2, mit Stilvorgabe.** Die Vorgabe verlangte zusammenhängende Absätze, legte fest, wer als handelnd genannt werden darf, und enthielt einen Musterabsatz. Das Ergebnis war deutlich besser: erzählender, gut lesbarer Text, der auch Fehler der Software sachlich benannte. Drei Mängel blieben:

1. **Eine Angabe über eine Person war frei erfunden.** Sie stand in keiner Unterlage.
2. Der Text wechselte zwischen „der Autor“ und „ich“.
3. Einige Zahlen waren als Wort geschrieben, etwa „acht“. Die Zahlenprüfung erkennt nur Ziffern und übersah sie deshalb.

Das Ergebnis taugt als Rohfassung, die ein Mensch überarbeitet, nicht als fertiger Text.

**Test D, Überwachung.** Von 13 Entscheidungen waren 7 Neustarts und 6 „weiterlaufen“. Die Begründungen waren verständlich formuliert. Zwei Neustarts kamen aber schon nach ein bis zwei Rechendurchgängen, bevor erkennbar war, ob die Rechnung vorankommt. Eine Einstellung, die gut aussah, wurde zweimal zu früh abgebrochen, zwei andere erlaubte Einstellungen wurden nie versucht. Das Ziel wurde nicht erreicht.

Eine spätere Auswertung zeigte allerdings, dass die überwachte Rechnung selbst falsch aufgesetzt war: Eine Datei mit Regeln fehlte, und das Ziel war damit gar nicht erreichbar. Dass das Ziel verfehlt wurde, liegt also nicht am Modell. Die ungeduldigen Entscheidungen bleiben trotzdem ein Befund.

# 6 Beobachtungen

1. **Kolibri 1 übernimmt Unterlagen sehr treu.** Erfundene Zitate kamen in keinem Test vor.
2. **Eine genaue Stilvorgabe verbessert Texte stark.** Mit Musterabsatz und klaren Regeln wurde Kolibris Text gut lesbar. Angaben über Personen bleiben ein Risiko, weil keine automatische Prüfung sie erkennt.
3. **Eigene Schlüsse sind Kolibris Schwäche.** Sollte das Modell über die Unterlagen hinausdenken, etwa eine Summe bilden oder Ziel und Ergebnis auseinanderhalten, entstanden Fehler.
4. **Qwen 3.8 findet mehr.** Es lieferte fast dreimal so viele belegte Werte wie Kolibri 1, bei gleich niedriger Fehlerquote und im richtigen Format.
5. **Kolibri 1 ist viel schneller.** Unter einer Minute gegenüber 5 bis 7 Minuten bei Qwen 3.8.
6. **Als Aufpasser war Kolibri 1 zu ungeduldig.** Es reagierte auf kurze Schwankungen, statt eine Entwicklung abzuwarten.

# 7 Grenzen des Tests

- Der Test lief einen Tag, mit wenigen Aufrufen (46), in einem einzigen Projekt und bei einem einzigen Anbieter. Die Ergebnisse sind Hinweise, keine gesicherten Aussagen.
- **Qwen 3.8 wurde nur in der Recherche geprüft (3 Aufrufe).** Zu Textqualität, Storyboard und Überwachung gibt es für Qwen 3.8 keine Aussage.
- Die Modelle arbeiteten ohne Zugriff auf Dateien oder Programme. Wie gut sie als selbstständig handelnde Assistenten arbeiten, wurde nicht geprüft.
- Die Geschwindigkeit hängt auch von Auslastung und Technik des Anbieters ab. Sie kann zu anderen Zeiten oder bei anderen Anbietern deutlich anders sein.
- Die Aufträge für Test A waren für das Vergleichsmodell geschrieben und nicht auf eines der beiden Testmodelle abgestimmt.
- Kosten wurden nicht erfasst.

# 8 Fazit und Empfehlung

| Aufgabe | Empfehlung |
|-------|----------|
| schnell Werte aus vorhandenen Unterlagen herausziehen | **Kolibri 1**, mit automatischer Prüfung von Format und Zahlen danach |
| gründlich recherchieren, möglichst viele belegte Werte | **Qwen 3.8 27B**, wenn einige Minuten Wartezeit je Aufgabe tragbar sind |
| lesbare Texte schreiben | Kolibri 1 nur mit genauer Stilvorgabe und Musterabsatz. Das Ergebnis ist eine Rohfassung, die ein Mensch durchsieht, besonders bei Angaben über Personen |
| eigene Schlüsse ziehen, laufende Rechnungen steuern | Kolibri 1 im Test nicht ausreichend, Qwen 3.8 nicht geprüft |

**Allgemein empfohlen:**

- Aufträge in kleine Teile zerlegen. Das verhinderte bei Kolibri 1 die leeren Antworten.
- Jede Antwort automatisch prüfen, bevor sie weiterverwendet wird.
- Bei Überwachungsaufgaben eine feste Mindestwartezeit vorgeben, bevor ein Neustart erlaubt ist.

Ein Folgetest sollte Qwen 3.8 auch in den Tests B bis D prüfen, die Aufträge auf beide Modelle abstimmen und die Arbeit mit Werkzeugen (Dateizugriff, Programme) einbeziehen.
