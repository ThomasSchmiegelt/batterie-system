# ERWARTUNG X3 – Crash Batteriepack G5 mit Inhalt (Opus, 2026-11-20, vor der Rechnung)
| Dok. | ERW-X3 | Version 0.1 | Entwurf | Ersteller Claude Opus | Prüfer Mensch (offen) |
Autor 2026-11-20: „crashsimulation des Batteriepacks. Ich möchte sehen wie sich die Batterie verformt, … nur Batteriebox mit inhalt“. REQ-P11 (Crash), ENT-151 (keine Knautschzone, Rahmen trägt).
**Methode (Opus):** OpenCourant explizit wie X1b/X2 (sim/mechanik/x1b_knautschzone, gleiche Werkstoffkarten, gleiche Wiederaufsetzregel). Modell aus der G5-Geometrie (cad/baukasten/ausgabe/step bzw. pack_<V>.FCStd):
- **Schalen:** Seitenrahmen (3 Kammern übereinander, Wand aus A_seitenrahmen_wand_mm), Querträger, Boden, Deckel, Unterfahrschutz.
- **Kühlplatten:** Blech 1/4/1 als Ersatzschale mit 2 mm.
- **Zellen:** Volumenblöcke mit gemitteltem Werkstoff wie X1. Zwischenlage und Pad als weiche Schicht.
- **Weggelassen:** Elektrik und Schaltbox. Kühlkreis außen nur als Masse.
- **Lastfälle:**
  - (a) Seitenpfahl Ø 254 mm, quer auf die Mitte der Längsseite, wie X1/X1b: gleiche Energie und Geschwindigkeit, damit es vergleichbar ist.
  - (b) Quetschung nach ECE R100 Anh. 8D (Platte, 100 kN, Pack auf der Gegenseite gestützt).
  - LFP zuerst, NMC danach.
**Ergebnis:**
- Film der Verformung (Seitenansicht und Draufsicht, Zellen farbig nach Verschiebung).
- Eindringung des Pfahls, Eindringung in die erste Zellreihe (Weg der Zellblock-Außenfläche).
- Größte Dehnung im Rahmen, Kraft-Weg-Kurve, Energiebilanz.
**Erwartung (Zahlen vor der Rechnung):**
1. Energiebilanz Fehler < 5 % (Pflicht).
2. (a) Ohne Knautschzone und mit 30 mm Rahmen: Pfahleindringung 40–70 mm (X1b w20 50 mm, mit Knautschzone). Die erste Zellreihe wird 10–40 mm eingedrückt. Das verletzt den Grenzwert „Zellen unverformt“ (Annahme Opus). Er wird voraussichtlich verfehlt und führt dann zu einem Verbesserungsvorschlag (breiterer Rahmen innen auf Kosten der Länge, Schweller-Anbindung, Pfahl-Lastpfad über die Querträger).
3. (b) Quetschung 100 kN: Rahmenverformung < 10 mm, Zellen < 2 mm eingedrückt. Damit wäre ECE R100 Anh. 8D erfüllt.
4. Rechenzeit LFP (a) 1–4 h CPU.
**Verfehlt**, wenn Energiebilanz > 5 % oder Eindringung außerhalb 20–100 mm (dann Modellfehler prüfen, zurück an Opus).
**Pausieren (Autor):** Schritt in rechnen/schritte.txt, OpenCourant-Abschnitte mit Restart-Datei; halt.sh schreibt /STOP in die .ctl-Datei.

## Nachtrag 1 (Opus, 2026-11-21, nach dem Probelauf, vor dem Dauerlauf)
Probe (grob, 25 ms): Eindringung 14,9 mm, der Pfahl prallt bei 393 kN ab. Das liegt unter dem Band. Ursachen nach Opus: Die ganze Gegenseite ist eingespannt (zu steif), und die Energie von 5 kJ ist klein. X1b brauchte für 50 mm die weiche Knautschzone. Festlegungen:
1. **Lagerung:** nur die 12 Befestigungshülsen BT-560 fest (wie im Fahrzeug), nicht die ganze Gegenseite.
2. **Energie:** Fall a = 5 kJ (Vergleich X1/X1b), dazu Fall a2 = 20 kJ (Annahme Opus: Anteil des Packs an einem Pfahlaufprall, nicht belegt).
3. **Zellblock:** E 1 GPa, Fließgrenze 20 MPa, ideal plastisch, Dichte aus der Zellmasse (Annahme Opus: Größenordnung homogenisierter Wickel unter Druck, nicht belegt; wirkt stark auf das Ergebnis). Empfindlichkeit: Fall a mit 10 und 40 MPa.
4. **Quetschung (b):** Platte 600 × 600 mm mit drei Halbzylindern R 75 mm, Abstand 30 mm, 100 kN, quer auf die Längsseite (Annahme Opus nach ECE R100 Anh. 8D aus dem Gedächtnis, nicht am Normtext geprüft; den Normtext beim Autor anfragen).
5. **NMC:** Zellen je Feld als homogener Block über die Zellfläche, E und Fließgrenze × Füllgrad (Zellvolumen/Blockvolumen aus ctx.zellen).
Erwartung neu für a mit Hülsenlagerung: 25–60 mm, a2: 50–120 mm. Erste Zellreihe eingedrückt, wenn die Eindringung > Rahmenbreite 30 mm + Spalt.
**Nachtrag 2 (Opus, 2026-11-21):** Fall b wird weggesteuert gerechnet (1 mm/ms, Annahme Sonnet). Ausgewertet wird der Weg beim ersten Erreichen von 100 kN nach dem Anlaufstoß (Kraftspitze < 1 mm Weg zählt nicht). Die Energiebilanz gilt für b nicht. Grenze für b: Rahmenverformung < 10 mm bei 100 kN. Zwei verwaiste Probeläufe von Sonnet (LFP_a_p2, LFP_b_p2) liefen weiter, obwohl ihre Ordner gelöscht waren, und belegten die CPU. Opus hat sie per PID beendet.

**Nachtrag 3 (Opus, 2026-11-21): Modellfehler in LFP_a, Korrektur vor allen weiteren X3-Fällen.**
Befund an den Rohdaten (X3A013/X3A051): 3426 Zellknoten der Reihen x ≈ 927–1105 mm verschieben sich in x um bis zu 319 mm, der Pfahl dringt aber nur 14 mm in y ein. Am Ende stecken noch rund 750 J kinetische Energie im Modell.
Ursache: Jede Zellreihe ist ein eigener Hex-Block mit nur einem Element in x-Richtung und 1 mm Spalt zur Nachbarreihe. Eine Kontaktdefinition gibt es nur zwischen Zellknoten und Schalen (TYPE7 Nr. 1), nicht zwischen den Reihen. Die Reihen neben dem Querträgerspalt bei x = 1016–1046 mm, also genau unter dem Pfahl (xp = 1025), werden gequetscht, durchdringen ihre Nachbarreihen und gleiten frei in x weg. Die Zahlen von LFP_a (13,9 / 8,1 mm, 441 kN) sind damit **ungültig**.
Korrektur (Methodenwahl Opus): Zwischen zwei Querträgern werden die Zellreihen zu einem homogenen Block zusammengefasst, also zu vier Blöcken: x 43–523, 552–1016, 1046–1510 und 1540–2004 mm. Elementgröße in x etwa 15 mm (eine Reihe), E und Fließgrenze werden mit dem Füllgrad 14/15 multipliziert, wie beim NMC-Block. Das physikalische Bild dahinter: Die Reihen sind mit Zwischenlage verpresst und tragen Druck in x gemeinsam. Gleitflächen gibt es dann nur noch an Querträgern und Rahmen.
Erwartung nach der Korrektur: Der Pfahlweg wächst gegenüber dem ungültigen Lauf nicht wesentlich (der Block ist steifer als frei gleitende Reihen), Eindringung 15–40 mm. Kein Zellknoten verschiebt sich um mehr als das 1,5-Fache des Pfahlwegs, die kinetische Energie am Ende liegt unter 5 % von E0, der Energiefehler unter 5 %.
Prüfkriterium für jeden X3-Fall ab jetzt: max |U| der Zellknoten ≤ 1,5 × Pfahlweg (bei b: ≤ 1,5 × Weg der Platte), sonst gilt der Fall als Modellfehler.

**Nachtrag 4 (Opus, 2026-11-23): Instabilität im Fall b (LFP_b, Lauf vom 22.11.)**
Befund an den Rohdaten (lauf/LFP_b/X3_0002.out): Bis t = 5,16 ms läuft der Fall mit konstantem Zeitschritt 5,1e-5 ms. Dann meldet der Kontakt /INTER/TYPE7/1 (Zellknoten gegen Schalen) Warnungen, der Zeitschritt fällt in wenigen Zyklen auf 1e-12 ms (Knoten 10776, 442540, 14830), die Energien steigen auf 1e19. Der Löser rechnete so 2,5 h (700 000 Zyklen) weiter und schrieb keine Restart-Datei, Abschnitt 3 brach mit „X3_0002_0001.rst NOT FOUND“ ab. In den Fällen a lief derselbe Kontakt stabil. Bei b drücken drei starre Zylinder (Masse 0, weggesteuert 1 mm/ms) den Rahmen in den weichen Zellblock; vermutlich wird die Kontaktsteifigkeit aus der steifen Schale (Istf = 0) gegenüber dem weichen Block zu hoch, und ein einzelner Knoten springt durch (Annahme Opus, nicht bewiesen).
Korrektur (Methodenwahl Opus), nur für Lastfall b, damit die Fälle a vergleichbar bleiben:
1. Kontakt 1 mit Istf = 4 (Minimum aus Master- und Slave-Steifigkeit) und Inacti = 6 (Anfangsdurchdringungen sanft lösen).
2. /DT/NODA/CST mit Skalierung 0,9 und Mindestzeitschritt 2e-5 ms (Massenzugabe statt Zeitschrittkollaps).
3. Wächter für alle Fälle in lauf.sh: Ein Abschnitt, der länger als 45 min läuft (normal 19–22 min) oder ohne Restart-Datei endet, bricht ab und meldet FEHLER.
Erwartung: Der Fall läuft durch, die Massenzugabe bleibt unter 1 % der Gesamtmasse (574,5 kg, also < 5,7 kg); liegt sie darüber, gilt das Ergebnis als unsicher. 100 kN werden nach 2–8 mm Plattenweg erreicht (Rahmen und Block als Feder einige 10 kN/mm), Rahmenverformung bei 100 kN < 10 mm, Zellen < 2 mm. Prüfkriterium wie Nachtrag 3: max |U| der Zellknoten ≤ 1,5 × Plattenweg. Der instabile Lauf bleibt als lauf/LFP_b_instabil_N4 erhalten. Ob 100 kN schon vor 5,16 ms erreicht waren, wird an X3T01/X3T02 nachgesehen (Vergleichswert für den neuen Lauf).

**Nachtrag 5 (Opus, 2026-11-23): Nachtrag 4 verworfen, Fall b nur bis 5 ms**
Probe mit Nachtrag 4 (Sonnet, bis 8 ms): Mit Istf = 4 und /DT/NODA/CST wurde es schlimmer. Der Kontakt-Zeitschritt fiel schon bei 0,535 ms auf 6e-10 ms, die Massenzugabe stieg auf 6,3e4 kg. Der weichere Kontakt lässt die Knoten tiefer eindringen, und /DT/NODA/CST greift nicht beim Zeitschritt des Kontakts. Die beiden Deck-Änderungen werden zurückgenommen. Der Wächter in lauf.sh bleibt, er hat in der Probe sofort angeschlagen.
Neuer Befund aus dem alten Lauf (lauf/LFP_b_instabil_N4, X3T01/02, stabil bis 5,15 ms): Die Kraft der drei Zylinder überschreitet 100 kN schon kurz nach dem ersten Kontakt (t ≈ 0,65 ms) und erreicht bei 5,15 ms 757 kN. Meine Erwartung von 2–8 mm Plattenweg bis 100 kN war falsch. Der Lastpfad läuft quer über Rahmen und Querträger axial auf die Abstützung, und das ist viel steifer als die angenommenen „einige 10 kN/mm“. Ob die ersten 100 kN nur der Anlaufstoß sind (Regel aus Nachtrag 2: eine Spitze unter 1 mm Weg zählt nicht), entscheidet die Auswertung.
Methode (Opus): Die gesuchte Größe, der Weg bei 100 kN, liegt im stabilen Bereich 0–5 ms. Fall b wird deshalb bis 5 ms gerechnet und ausgewertet, Kraft bei 5 ms etwa 750 kN, also das 7,5-Fache der Prüfkraft. LFP_b wird aus Abschnitt 1 des alten Laufs ausgewertet, ohne neue Rechnung. NMC_b rechnet mit X3_TSTOP = 5 und X3_NSEG = 1. Grenze, die im Bericht steht: Das Verhalten jenseits von etwa 750 kN wird nicht berechnet, die Ursache der Instabilität bleibt ungeklärt.
Erwartung: Weg bei 100 kN nach dem Anlaufstoß unter 2 mm, Rahmenverformung ≪ 10 mm, Zellen unter 1 mm eingedrückt; Prüfkriterium max |U| der Zellknoten ≤ 1,5 × Plattenweg, angewendet auf die Bilder bis 5 ms.

**Nachtrag 6 (Opus, 2026-11-23): Schärferer Wächter während des Laufs** (Vorgabe Autor: „ja, bau den schärferen Wächter ein“)
lauf.sh liest während jedes Abschnitts alle 60 s die letzte Zyklenzeile der laufenden X3_00kk.out und beendet die Engine per PID mit FEHLER, wenn
1. der Zeitschritt unter 1/10 des Startzeitschritts des Laufs fällt (erste Zyklenzeile von X3_0001.out), oder
2. der Energiefehler (Spalte ERROR) betragsmäßig über 10 % liegt (Fall a). Für Fall b gilt die Energiebilanz nicht (Nachtrag 2), dort nur |ERROR| > 50 % als Zeichen eines Zusammenbruchs.
Dazu bleiben die 45-min-Grenze und die Prüfung auf die Restart-Datei. Der Grund steht in FEHLER_waechter.txt und in der Zeile im verlauf.log.
Erwartung: Keiner der gültigen Läufe (LFP_a, a2, a_s10, a_s40, LFP_b bis 5 ms) hätte ausgelöst, der instabile LFP_b (Kollaps bei 5,16 ms) und die Probe nach Nachtrag 4 hätten innerhalb von 1–2 min nach dem Kollaps ausgelöst. Würde ein gültiger Lauf auslösen, wird die Schwelle nicht still gelockert, sondern Opus entscheidet.
Entscheidung Opus (23.11., nach Offline-Prüfung Sonnet): Für Fall b gilt nur das Zeitschritt-Kriterium. Der Energiefehler bezieht sich dort auf eine Anfangsenergie von null, denn die Zylinder sind weggesteuert. Er steht ab Kontaktbeginn auf −99,9 % und ist damit kein Maß. Das dt-Kriterium hätte den instabilen Lauf bei t = 5,160 ms ausgelöst und keinen gültigen Lauf.

## Anforderung (Nachtrag)
REQ-P14 (Zuordnung Opus 2026-11-23)
