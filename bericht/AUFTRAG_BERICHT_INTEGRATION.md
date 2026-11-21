# AUFTRAG (Sonnet): Eigenes Berichtskapitel „Geometrische Integration durch KI – Grenzen, Fehler, Unsicherheiten“
KI-generiert (Claude Opus, 2026-11-20). Autor 2026-11-20: „solche infos sind für mich sehr wichtig. Ich habe viele Kollegen die arbeiten im Bereich geometrischer integration und glauben KI kann diese tätigkeiten nicht ausführen. Bitte schreibe solche Infos auch rückwirkend gesondert in den bericht.“
**Ziel:** Ein eigenes Kapitel in bericht/bericht.tex, vor „Offene Punkte“ bzw. vor dem Schluss. Leser sind Fachleute der Packaging- und Geometrie-Integration, die skeptisch sind. Der Ton ist nüchtern: nichts beschönigen, nichts dramatisieren. Jede Aussage hat eine Quelle (Datei, Befundnummer).
**Quellen (rückwirkend, alle lesen, nur gekürzt per grep):**
- BEFUNDE.md (alle B-BAT)
- docs/08_ki_einsatz_protokoll.md (Spalten Prüfung und Ergebnis)
- docs/09_aenderungen.md
- ~/hermes/buch/ereignissprotokoll_batterie/ereignisprotokoll.md (BA-Einträge zu Geometrie, CAD, Kollision, Datenblatt, Erwartung verfehlt; nur sinngemäß, kein Zitat nötig)
- alle ERWARTUNG.md mit „verfehlt“: `grep -ril verfehlt --include=ERWARTUNG.md --include=ERGEBNIS.md .`
- forschung/datenblaetter_eingearbeitet.md, forschung/datenblaetter_fuer_autor.md
- cad/baukasten/ausgabe/pruefung_<V>.txt
- ERINNERUNGEN.md
**Gliederung:**
1. Kurzfassung (5 Sätze): Was die KI in der Integration geleistet hat (Zahlen: Teile, Kollisionen am Ende 0/0, Stückliste aus CAD) und wo sie Menschen braucht.
2. Tabelle „Fehler der KI selbst“: Datum | was | wer hat es gefunden (Erwartungsprüfung, Prüflauf, anderer Agent, Autor) | Folge (kg, €, mm) | Behebung | Quelle. Mindestens diese Fälle:
   - Zwischenlage als 1 mm massiver Glimmer: 41,5 kg, 249 €, gefunden über die verfehlte Kostenerwartung (B-BAT-035).
   - Schützmasse 0,8 kg je Stück statt 0,4 kg: Summe für zwei als Einzelwert genommen, von Opus im PDF gefunden.
   - Seitenrahmen-Erwartung falsch (B-BAT-033).
   - Füllgrad 0,4 passte nicht zur K2-Geometrie.
   - Verteiler zuerst in die Endzone gelegt, obwohl dort kein Platz war (LFP 16 mm, NMC 0 mm), mit Kollisionen mit Zellen.
   - HV-Eintritt der Schaltbox zu tief, Leitung brauchte eine Schlaufe bis 275 mm Höhe.
   - Trennstecker NMC unter der Schaltbox.
   - Kabelschuhe und Fühler in der Kühlplatte.
   - Steckerschrauben bis in die Kühlplatte.
   - Abb. 43–49 im Bericht 0.5 zeigten noch den alten E2-Stand. Vom Autor gefunden, nicht von der KI.
   - Sonnet hielt das NMC-Modell für aktuell, obwohl es veraltet war.
   - Renderfehler KeyError, gefunden vom PI-Prüfbericht.
   - Weitere Fälle aus BEFUNDE und Buch.
3. Tabelle „Abweichungen Datenblatt ↔ Modell (offen)“: Schütz mit Innengewinde statt Bolzen, Pyrosicherung mit Schiene 23,75 × 4 und M6 (Modell 25 × 3, M8), HV40 22 % höher, Shunt-Bohrung teilt sich den Schlüssel mit den Schienen, Kabelschuh-Zuordnung unklar, Datenblattmassen gegen Annahmen. Alles aus datenblaetter_eingearbeitet.md.
4. Tabelle „Unsichere Werte“: aus Zeichnungen gelesen (Bolzenabstand, RH050), Teile ohne Datenblatt (Chiller, Isolationswächter, Stecker, Behälter), Annahmen Stufe F/K/H mit Anteil an der Masse.
5. Verlauf der Kollisionsbereinigung G5 als kleine Tabelle oder Bild:
   - erster Gesamtlauf: 67 Fehler, darunter rund 50 Kollisionen
   - dann 31 Fehler und 17 Kollisionen (LFP)
   - dann 0 / 0 (LFP / NMC)
   Zahlen aus docs/08, BEFUNDE und pruefung_*.txt. Was fehlt, als „nicht protokolliert“ kennzeichnen.
6. Was die KI nicht kann bzw. wo der Mensch nötig war: Bauraumvorgaben (Breite 1430 mm), Entscheidung zur Kühlplatte, Freigaben, Downloads hinter Login, Prüfung der Bilder auf fachliche Plausibilität.
   Dazu, wie die Fehler gefunden wurden: Erwartung vor der Rechnung, automatische Kollisionsprüfung, Gegenprüfung am PDF, zweiter Agent.
7. Lehren für die Integration (3–6 Punkte, aus den Fällen abgeleitet).
**Regeln:**
- Zahlen nur aus den Quellen.
- Fehlt eine Zahl, „nicht protokolliert“ schreiben.
- Keine Personennamen. Der Autor heißt „Autor“.
- Kopf und Version unverändert lassen (0.5). Das Kapitel bekommt den Vermerk „KI-generiert (Sonnet), Prüfung Opus offen“.
- pdflatex zweimal, 0 Fehler.
- Dazu eine kurze Fassung als praesentation/bausteine/KI_Integration.md.
**Laufende Arbeit:** Die Warteschlange rechnen/ baut den Bericht gelegentlich neu (pdflatex). Das stört nicht, nur bericht.tex nicht gleichzeitig mit einem anderen Werkzeug umschreiben.
**Rückgabe:** ≤ 5 Zeilen (Seitenzahlen des Kapitels, Anzahl Fälle je Tabelle, Lücken).
