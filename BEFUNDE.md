# BEFUNDE – Batteriesystem

KI-generiert (Claude Opus). Je Befund: Nummer B-BAT-NNN, Datum, Aussage mit Zahl, Fundstelle (Datei/Lauf/Quelle), Erwartung erfüllt ja/nein.



## B-BAT-001 (2026-11-12) PI-Recherche W01 (LFP): Stufe B funktioniert, Zitatprüfung 12/14
- Erster PI-Lauf im Projekt: 4 min 15 s, 0 Werkzeugaufrufe, keine Links außerhalb des Pakets.
- pruefe.py: zuerst 11 bestätigt / 3 Fehler. Opus am Rohtext (recherche_ablage/926e09b6d3b5.txt, pakete/W01.md): alle 3 Werte stehen in der Quelle, nichts erfunden.
  Ursache 1: Wikipedia-Abruf setzt Link-Adressen „[https://…]“ in den Satz, PI lässt sie weg → pruefe.py ignoriert sie jetzt auf beiden Seiten (Skill web-recherche, auch Fusion). Danach 12/2.
  Ursache 2 (bleibt Fehler, zu Recht): PI kürzt Zitate („(Wh/kg)“ fehlt) bzw. zieht Infobox-Zeilen zusammen.
- Inhaltlich: Werte korrekt übernommen (3,2 V nominal; 3,60–3,65 V Ladeschluss; 2,0–2,8 V Entladeschluss; 95–172 Wh/kg; 2 500–9 000 Zyklen; Kälte: 141,8 / 92,7 / 57,9 / 46,7 mAh/g bei 23 / 0 / −10 / −20 °C).
  Schwächen: Bezeichnung „Spezialeistung“ statt spezifische Kapazität; 12-V-Folgerung für ein Fahrzeug-HV-Pack unerheblich; 66 %/33 % selbst gerechnet (richtig: 65 %/33 %), ohne Kennzeichnung.
- Folge: Ergebnisse brauchen weiter die Lesung durch Opus (R4); pruefe.py allein reicht nicht. Vorgang: [R1] [R4]

## B-BAT-002 (2026-11-12) „0 Belege“ hieß „nicht geprüft“: Zitate ohne „Beleg:“ rutschten durch
- T02, T05, T06, T08 (und W05) meldeten 0 bestätigte Belege. Ursache: PI zitierte wörtlich, aber ohne das Schlüsselwort, z. B. `Zweck: „foxBMS is a free, open …“ (URL)`; pruefe.py erkannte nur `Beleg: „…“ (URL)`.
- Gefahr: solche Zitate wären ungeprüft in die Ergebnisse gegangen. Behoben: pruefe.py prüft jedes Zitat ≥ 12 Zeichen mit Quellenangabe in Klammern (Skill web-recherche, auch Fusion).
- Neu geprüft: T05 6/0, T06 4/0, T08 9/0 (vorher 0/0). W05: 0/0 bleibt, PI meldet ehrlich „nicht gefunden“ (die Wikipedia-Seite zum BMS enthält kaum Kennwerte). T02: 0/1, Zitate kursiv mit angehängter Wortzählung, ein Satz ins Deutsche übersetzt → T02 bei R4 neu rechnen.
- Anweisungsartiger Text „ignore previous instructions“ in T02 stammt von PI selbst (Feststellung „kein solches Muster gefunden“), nicht aus den Quellen.
- Folge: Zählung „Belege bestätigt“ ist nur mit Blick auf „0“ aussagekräftig; 0 heißt jetzt: keine Zitate gefunden → Opus liest. Vorgang: [R2] [R4]

## B-BAT-003 (2026-11-12) Patente P02–P10: Spalten verrutscht (Opus-Fehler in lauf.sh), PI blieb ehrlich
- `IFS=$'\t' read` fasst leere Felder zusammen (Tab gilt als Leerraum). Bei Themen ohne Inhaber rückte der deutsche Zweck („Kühlung“) in die Suchspalte → 0 Treffer; P06–P10 brachen ab (paket.py IndexError bei leerer Trefferliste).
- PI auf leeren Paketen: meldete „Trefferliste leer, keine Auswertung möglich“, erfand keine Patente (Links nicht aus dem Paket: 0).
- Behoben: Tabs vor dem Einlesen in ein Nicht-Leerraumzeichen getauscht; paket.py verträgt leere Trefferlisten. P02–P10 und T02 neu gerechnet (nachlauf2.sh): T02 jetzt 4/0. Patente danach weiter leer: Google Patents antwortet mit HTTP 503 (Bot-Schutz nach dem ersten Durchlauf). Nicht umgangen; einmaliger Versuch nach 2 h (nachlauf3.sh). Alternativen mit Anmeldung (EPO OPS, Lens.org) bräuchten die Zustimmung des Autors. Vorgang: [R3]

## B-BAT-004 (2026-11-16) Analyse: Was fehlt für die komplette Batterie (Struktur gegen Information)
Fundstellen: `pm/bauteile/struktur.json`, `stueckliste.json`, `parameter.json`, `pm/startwerte.json`, `pm/entscheidungen/`, `forschung/ergebnis/*.pruefung.txt`. Erwartung: entfällt (Bestandsaufnahme, keine Rechnung).
1. **Struktur zu flach.** struktur.json hat 8 Bauteile. Merkmale gibt es nur bei BT-100 (5) und BT-200 (2). BT-300 bis BT-700 haben keine. Die Stückliste hat 37 Positionen, aber keine davon ist ein eigenes Bauteil. Folge: Für Gehäuse, Querträger, Kühlplatte, Zellverbinder usw. kann `pm.py pruefe` keine Akte annehmen, also gibt es kein Maß fürs CAD. Das ist der Hauptblocker.
2. **Keine Maßentscheidung.** parameter.json: alle 7 Merkmale `null`. ENT-001…003 betreffen Methoden. ENT-002 (PyBaMM) steht noch auf „vorgeschlagen“.
3. **Widerspruch Energie.** startwerte.json: 73,9 kWh brutto. stueckliste.json: 79,9 kWh (219s1p × 100 Ah × 3,65 V, beide Zellwerte Annahme). Die Zellzahl ist auf ganze Reihen gerundet, die Energie aber nicht zurückgeführt.
4. **Widerspruch Chemie gegen Vorbild.** Die Startwerte wählen NMC, weil die LFP-Packdichte als 180 Wh/L **angenommen** ist (startwerte.py, „Zelle × Füllgrad ~0,6“, unbelegt), nötig wären 214 Wh/L. Die Recherche belegt für Blade-LFP nur Werte je kg (190–210 Wh/kg Zelle, W03), keinen Wert je Liter. Die Stückliste führt deshalb eine „lang prismatische NMC-Zelle“. Für dieses Format gibt es in der Recherche keinen Beleg, das Blade-Format ist LFP (W03). Die Entscheidung LFP/NMC hängt an einer unbelegten Zahl.
5. **Belegte Zellmaße vorhanden.** W03, 0 Fehler: Long Blade 960 × 90 × 13,5 mm, Short Blade 450–580 mm. Sie passen in den angenommenen Bauraum 1,9 × 1,4 × 0,13 m (TAB_FZ Kompakt, Annahme). Damit könnte G1 starten, sobald die Chemie feststeht.
6. **Lücken bei Grenzwerten.** W04 (thermisches Durchgehen) liefert keine Batteriewerte, nur Digitallogik und Chemie. W05 hat 0 Belege. Für REQ-P09 (max. Zelltemperatur, Spreizung) und REQ-P11 gibt es nur W16 (Fenster +20…+30 °C). Die übrigen Grenzen bleiben Annahmen. Patente: nur P01, P02–P10 sind wegen der 503-Sperre leer (B-BAT-003).
7. **Prüfung offen.** R4 (Opus liest alle Ergebnisse) ist nicht abgeschlossen. Zitatfehler über 0: W01 2, W02 5, W06 1, W07 2, W09 3, W10 4, W11 2, W13 1, W14 1, T04 1, T07 1.
Folge: Vor dem CAD (G1/G4) stehen drei Schritte: (a) Bauteilbaum bis zur Stücklistenebene erweitern, mit Merkmalen; (b) Chemie LFP/NMC vom Autor entscheiden lassen, mit der Wh/L-Frage als offener Annahme; (c) Startsatz und Lastenheft freigeben (V2). Vorgang: [R4] [V1] [G1] [SL1]

## B-BAT-005 (2026-11-16) R4: Recherche geprüft, kein erfundener Wert, ein Spaltenfehler (PI), Wh/L-Frage bleibt offen
- Vorprüfung Sonnet (forschung/R4_vorpruefung.md, 5 min): 22 FEHLT-Zeilen = 21 Wortlaut abweichend, Wert im Rohtext / 0 Wert fehlt im Rohtext / 1 unklar (T07 Z7, ohne Zahl). Erwartung „keine erfundenen Zahlen, Wortlautfehler wie B-BAT-001“: erfüllt.
- Opus-Stichprobe an pakete/: W02 Z12 („100 to 250 W·h“ steht in Infobox, Zeile 94) ✓. W01 Z15 („Next gen: 180–205 Wh/kg“, Zeile 9) ✓. **W06 Z22 falsch zugeordnet:** Rohtext (Zeilen 10–18) Kopf „Li-NMC | LFP | …“, erster Block 150-275 / 150-220 / 165 = NMC, zweiter Block 80-150 / 210 / 90-160 / 135 = LFP. PI gab 150–220 als LFP aus (Fehler eines lokalen Agenten, Tabelle mit verlorenen Spaltengrenzen).
- W01 Z16 „LFP 227–396 Wh/L“: Rechenkommentar im Rohtext `3.96/((1.85/2)^2*3.14159*6.495/1000)` = 18650-Rundzelle. Für das Blade-Format gibt es keinen Wh/L-Wert. Die Chemiewahl LFP/NMC (B-BAT-004 Punkt 4) bleibt unbelegt.
- Ergebnis: forschung/R4_ergebnis.md (verwendbare Werte mit Bauteil/Merkmal, gesperrte Werte, Lücken mit Weg). Neue Quelle: Zerlegungsstudie Blade/4680 (doi:10.1016/j.xcrp.2025.102453, CC-BY), automatisch nicht abrufbar. Thema W18 (314-Ah-LFP-Zelle, thermisch) gestartet.
- Folge für PI-Aufträge: Tabellen ohne Spaltengrenzen sind fehleranfällig. pruefe.py findet das nicht, weil der Wert im Text steht. Vorgang: [R4]

## B-BAT-025 (2026-11-18) E2 Fortsetzung 2: NMC-Mäander machbar, LFP nicht; LFP-FPC passt nicht an den Querträgern vorbei
Quelle `cad/pack/entwurf/ergebnis_{LFP,NMC}_e2.json`, `sim/elektrik/e2_elektronik/ERGEBNIS.md` v0.3. NMC: 4 Bänder à 7 Spalten, Plus/Mitte/Minus hinten, HV intern 1,19 m, 11,34 W, 0 Kollisionen, FPC 30,7 m, Hälften 112/105 Gruppen. LFP: 2 Reihen reichen nicht (4 Durchläufe nötig), 9 Kollisionen FPC–Querträger (18 mm frei über dem Profil, FPC 20 mm), 6 von 14 FPC-Stücken ohne Platz.

## B-BAT-038 (2026-11-21) Thermik K3/K4 Probe: Pack ΔT 16 K, Erwartung von Opus falsch, LBM an der Stabilitätsgrenze
- K4 LFP Schnellladen (sim/kuehlung/k3_gesamt/elmer/ergebnis.json): T_max 42,6 °C, ΔT 16,4 K. Die Erwartung 33–37 °C hatte die Kühlmittelaufwärmung von 10,2 K aus K2b vergessen (Opus-Fehler). Das Ergebnis ist plausibel, **verfehlt aber ΔT ≤ 5 K** und wird zum Verbesserungsvorschlag. Varianten gegensinnig und Durchfluss ×2 sind beauftragt.
- K3 FluidX3D: τ ≈ 0,502 bei Re 760 mit 2 Zellen/mm, also Δp +228 %, h +129 %, Temperatur NaN. Methode geändert: Re 100/200, 4 Zellen/mm, Nu und f·Re der ausgebildeten Strömung übertragen.

## B-BAT-037 (2026-11-21) Nachtrag Zahlen zur Kollisionsbereinigung G5 (Opus, aus den Laufausgaben der Sitzung 2026-11-19/20)
- Erster Gesamtlauf LFP (2026-11-19): 1342 Teile, 628,89 kg, 67 Fehler (Massenabweichungen und Kollisionen zusammen). Größte Kollisionen: Zellen 217/218/248/249 ↔ Verteiler/Sammler je 18 253–21 092 mm³, weil die Verteiler in der Endzone lagen.
- NMC aus G5.4 (Sonnet): 5 Kollisionen des Trennsteckers mit der Schaltbox, die größte Hauptschütz minus 60 381 mm³, Wanne 7 960 mm³.
- Nach Verteiler außen, Kragen und Einbauorten (2026-11-20): LFP 31 Fehler, darunter 17 Kollisionen, NMC 15. Größte: Kabelschuh HV ↔ Kühlplatte 1 190 mm³ bzw. 1 217 mm³.
- Danach LFP 1 Kollision, dann 0 und NMC 0.
- HV-Leitung: Der Eintritt knapp über dem Boxboden hätte eine Schlaufe bis z ≈ 275 mm erfordert (Sonnet G5.4). Behoben mit Eintritt auf Höhe Hülsenende + Biegeradius.
- Schützmasse: 0,8 kg je Stück statt 0,4 kg, bei 2 Stück also 0,8 kg zu viel in Stückliste und CAD (vor der Korrektur).
- Warteschlange: Nach G5_ALLE ging sie ins Leere, 21 h ohne Rechnung (2026-11-20 10:29 bis 2026-11-21 07:50, rechnen/verlauf.log). Bemerkt hat es Opus, erst bei der Fortsetzung.

## B-BAT-036 (2026-11-20) G5 kollisionsfrei, Datenblätter eingearbeitet
- Montage LFP 1343 Teile, 628,8 kg und NMC 3601 Teile, 480,0 kg: 0 Kollisionen (cad/baukasten/ausgabe/pruefung_<V>.txt).
- Die Kühlplatte (Wunsch Autor) bleibt unverändert. Kabelschuhe und Kühlmittelfühler bekommen Durchführungen mit wasserfreiem Kragen bzw. sitzen hinter der Plattenlasche. Die Steckerschrauben enden im Deckel (Einnietmutter). Das Typschild ist verschoben. Über dem HV-Eintritt sitzt keine Flanschschraube.
- DB2 (Sonnet): 7 Datenblattwerte in cad/baukasten/annahmen_datenblatt.json (wird zuletzt gelesen), forschung/datenblaetter_eingearbeitet.md.
- Offen aus DB2 (Stufe F, nicht gelöst): Der Schütz hat Innengewinde statt Bolzen. Die Pyrosicherung verlangt eine Schiene 23,75 × 4 mit M6 (Modell 25 × 3, M8). HV40 ist 22 % höher. Zwei Werte sind aus der Zeichnung gelesen.
- Rechnungen laufen ab jetzt über die anhaltbare Warteschlange rechnen/ (LIESMICH.md).

## B-BAT-035 (2026-11-19) KO2 Kosten mit Datenblättern und Kühlkreis; Opus-Fehler Zwischenlage
- KO2 (pm/kosten/ergebnis_<V>.json): LFP 6 793 € / 91,9 €/kWh, NMC 8 717 € / 117,4 €/kWh. ERW-KO2: LFP +8,7 % **verfehlt**, NMC +1,4 % erfüllt. Verifiziert + abgeleitet nur 0,2 % der Summe.
- Ursache LFP: Opus hatte die Zwischenlage BT-220 als 1 mm Mica-Vollmaterial festgelegt (242 Stück, 41,5 kg, 249 €). Korrektur: Schaumpad 300 kg/m³ (≈ 4,5 kg). Erwartet werden danach ≈ 89 €/kWh, der Neulauf läuft.
- Datenblattmassen: Hauptschütz GLFX250 0,8 kg statt 0,45 kg, Vorladeschütz + Widerstand 0,41 kg statt 0,15 kg (annahmen_g5.json).

## B-BAT-034 (2026-11-19) K2b Blech-Kühlplatte 1/4/1 mm mit Mäander (Autor-Vorschlag ENT-152)
- 48 Varianten je Pack (sim/kuehlung/k2_kuehlplatte/ergebnis_k2b.json). U ≥ 500 nur mit mehr Bahnen oder schmalen Teilkanälen. **Auswahl Opus n = 8 Bahnen längs, w = 8 mm: U 558 W/(m²K), Δp 0,215 bar, 46,6 kg für 2 Platten** (statt 75,5 kg), Plattendicke 6 statt 8 mm (ENT-152…156).
- ERW-K2b teils verfehlt: n = 4, w = 8 längs ergibt U 487 statt ≈ 550. Breite Kanäle (w = 40) liegen bei 405–518 statt 350–420, weil die Einlaufströmung (Graetz-Term) Nu anhebt. Δp bei n = 8 ist mit 0,215 bar kleiner als erwartet (0,4–1). Erfüllt: Δp bei n = 4 (0,05 bar), Masse 38–49 kg.
- Offen: Der Kontaktwiderstand Zelle–Pad–Blech ist nicht gerechnet, die Reserve beträgt 12 %.

## B-BAT-033 (2026-11-19) G5 Zwischenstand: Kühlplatte mit echten Kanälen +28 kg, Recherche liefert keine Kaufteilmaße
- Kühlplatten (2 Stück) mit den K2-Kanälen (4 × 5 mm, Steg 3, 281 je Platte, Blech 1,5): **75,5 kg statt 46,9 kg**. Der alte Füllgrad 0,4 (A_KUEHLPLATTE_FUELLGRAD) passte nicht zur K2-Geometrie (dort 0,64). Erwartung ERW-G5 75 kg: erfüllt. Fundstelle cad/baukasten/ausgabe/ergebnis_LFP.json (Teillauf gehaeuse,kuehlung).
- Seitenrahmen 3-Kammer-Profil 14,5 kg. ERW-G5 6–7 kg **verfehlt**: Opus hielt die alten 21,8 kg für ein Vollprofil, sie enthielten aber schon Kammern (Vollprofil wären 60 kg). Profilfläche 790 mm² ist geprüft.
- Schaltbox mit liegenden Geräten: Innenhöhe 70 mm (Ziel ≤ 90), Turm 77 mm über dem Packdeckel, Oberkante LFP 198 mm (Grenze 210). Erwartung erfüllt.
- W31 (Preise) und W34 (Kaufteilformen): Die Quellen (Wikipedia) nennen keine Preise und keine Maße. Von den Kaufteilen sind 4–6 Positionen weiter in Stufe H. W32: Al-Dichte 2,70 g/cm³, E 69 GPa, Rp0,2 100–260 MPa (6005) sind bestätigt, die Dichte gilt jetzt als belegt. Für Maße und Preise braucht es Datenblätter von Herstellern (Frage an den Autor).

## B-BAT-032 (2026-11-19) Entscheidung: keine Knautschzone im Pack (ENT-151)
- Autor folgt der Opus-Empfehlung aus B-BAT-031. Studie engere Querträger entfällt. Schnittstelle: Schweller stoppt den Pfahl vor dem Rahmen (Zellberührung ≈ 30 kN, X1). Erwartung: –.

## B-BAT-031 (2026-11-18) X1b/X2 OpenCourant: Knautschprofil bringt kaum Reserve, die Rahmen-Innenwand gibt zuerst nach
- Explizit (OpenCourant latest-20261011), Pfahl 1500 kg mit 5 kJ. Energie bis zur Zellberührung (4 mm):

  | Variante | Energie | Anteil an 5 kJ |
  |---|---|---|
  | LFP w15 | 416 J | 8 % |
  | LFP w20 | 455 J | 9 % |
  | LFP w30 | 568 J | 11 % |
  | NMC w20 | 523 J | 10 % |

- Eindringung 49–52 mm, Energiefehler ≤ 0,01 %. Gegenprüfung mit CalculiX bei 2 mm: +7…14 %.
- **Deutung (Opus):** Das Profil staucht mit ≈ 80 kN. Diese Kraft biegt die Innenwand zwischen den Querträgern (Spannweite ≈ 500 mm) schon, bevor das Profil zusammengefaltet ist. Mehr Breite w hilft daher kaum, von 15 auf 30 mm sind es nur +37 %.
- 5 kJ bei 80 kN brauchen etwa 60 mm Weg. Das ist bei fester Breite nicht unterzubringen.
- **Folge:** Eine Knautschzone im Pack lohnt sich nicht (LFP −2,4 % Energie für +10 % Reserve). Der Seitencrash bleibt beim Schweller (ENT 2026-11-17). Wer Reserve will, braucht eine steifere Innenwand bzw. engere Querträger, als eigene Studie.
- **Werkzeug:** /RFILE-Zwischendateien in OpenCourant latest-20261011 nicht lesbar (Segfault). Der Neustart läuft über 10 Abschnitte (Vergleich 0 Abweichung). Opus-Fehler in ERW-X1b: Erwartung ab w 20 mm, 5 kJ, ohne die Rahmenbiegung zu bedenken. Vorgang: [X1] [X2]

## B-BAT-030 (2026-11-18) X1 Seitenpfahl: Pack hat keine Knautschzone, Zellberührung bei ≈ 30 kN
- CalculiX quasistatisch, Pfahl Ø 254 (Annahme). Die Innenwand des Seitenrahmens erreicht die Zellen nach 1 mm (LFP-Verbinder) bzw. 0 mm (NMC, gerade Reihen). Das geschieht bei 29–31 kN und 18–20 J, auch auf dem Querträger (LF2 ≈ LF1). PEEQ 21 % nach 5,5 mm. Netzstudie < 1 %.
- Opus-Fehler: In der Erwartung (1–3 kJ, 30–80 kN) waren die 30 mm Rahmen als freier Weg gezählt.
- Folge: Der Seitencrash muss vollständig über den Schweller gehen (Autor 2026-11-17). Eine Knautschzone im Pack (≈ 15–30 mm je Seite, Annahme) kostet bei fester Breite Zellen → Frage an den Autor. X2 (dynamisch) bringt erst mit Fahrzeugstruktur etwas. Vorgang: [X1]

## B-BAT-029 (2026-11-18) KO1 Kosten: LFP ≈ 80 €/kWh, NMC ≈ 110 €/kWh, vollständig geschätzt
- Untere Schranke: 15 Positionen bei LFP und 12 bei NMC haben keine Masse bzw. Menge. Werte:

  | Variante | €/Pack | €/kWh | Zellanteil |
  |---|---|---|---|
  | LFP | 5 933 | 80,3 | 62 % |
  | NMC | 8 151 | 109,8 | 68 % |

- Verifiziert ist nur der BNEF-Packpreis BEV 2024 von 97 USD/kWh (W29), etwa 89 €/kWh. Er dient zum Abgleich. 100 % der Summe beruhen auf Schätzungen (ERW-KO1).
- Wirkung des Zellpreises: ±20 % beim Zellpreis ergeben ±12,5 % (LFP) bzw. ±13,7 % (NMC) beim Packpreis.
- Opus-Fehler in Lauf 1: Fertigungszuschlag auf die Zellen gerechnet, Kühlplatte als Vollmaterial. Korrigiert in Nachtrag 1.
- REQ-P16 ohne Zielwert (Autor).
- Vorgang: [KO1]

## B-BAT-028 (2026-11-18) SL2 Stückliste je Variante: Massen stimmen (±1,3 %), fünf Bauteile fehlten im Baum, vier Zählwidersprüche CAD/E1
- `docs/13_stueckliste_<V>.md` v0.2: je 38 Positionen; LFP 619 kg (+1,2 % gegen pack_massen), NMC 471 kg (−0,4 %); NMC über G4-Band 390–430 kg. Kostenspalten leer, Gerüst `pm/kosten/`.
- Baum erweitert (Opus): BT-260 Verguss (NMC), BT-361 FPC-Halter, BT-440 Pol-Anschlusslaschen, BT-721 Trennbrücke, BT-722 Servicedeckel (LFP), BT-720 bauform (ENT-150 umgehängt). CMU → BT-320, FPC → BT-360 bestätigt. Dichtungen bleiben in BT-520/BT-710.
- **Zählwidersprüche, nach E2 v1.1 klären:**
  - LFP-Reihenverbinder: CAD 130, E1 249. Bei 250 Zellen in Reihe sind 249 nötig.
  - NMC-Abgriffe: 868 gegen 1736. Das ist eine Definitionsfrage: je Gruppe 218 Spannungsabgriffe, je Zelle 2 Pole.
  - NMC-Gruppenverbinder: 217 gegen 216. Möglicherweise ist die Endlasche mitgezählt.
  - HV-Leitung: CAD 0,5/0,4 kg, nur Cu, gegen E1 1,8/1,2 kg. Die E1-Werte sind eine Schätzung mit Isolierung. Es gilt CAD plus Isolierung.
- Vorgang: [SL2]

## B-BAT-027 (2026-11-18) E2 v1.0: Trennbrücke LFP (0 mm Höhe), Al-Verlust höher als erwartet, NMC-Verbinderquerschnitt widersprüchlich
- LFP-Trennstecker → Trennbrücke unter Servicedeckel (ENT-150, Autor „wie du meinst“), Packhöhe vorn 121 mm. Nut + Serviceöffnung 1,5 % der oberen Kühlfläche (für K2).
- Al-Verbinder LFP 73,5 W gegen ≤ 50 W: Opus-Erwartung zu tief, bei 194 A Schnellladen vertretbar (Querverbinder 18,9 W nachgerechnet).
- **Widerspruch NMC:** E1 wählt Gruppenverbinder 15×3 mm, das Pack-CAD zeichnet 25×3 mm → 461 W bzw. 316 W. Das CAD muss den Akten-Querschnitt lesen; Klärung vor M/X. LFP-Lasche im 1-mm-Spalt nur Stumpfstoß (Bohrungsrand 0,8 mm) → konstruktiv offen. Merkmal BT-720 bauform fehlt in struktur.json (ENT-150 unter einbauort). Vorgang: [E2]

## B-BAT-026 (2026-11-18) E2 abgeschlossen (Entwurf): beide Varianten ohne Kollision, Erwartung Nachtrag 2 erfüllt
- ERGEBNIS.md v0.4: HV intern LFP 1,18 m / 15,2 W, NMC 1,19 m / 11,3 W; Elektronik 6,4 / 7,1 kg; FPC LFP 16 mm, 4 Lagen; NMC 216 Brücken nach Mäander. Opus-Fehler „Mitte hinten“ (Nachtrag 2) behoben.
- Offen: LFP-Trennstecker vorn 58 mm über Deckel (Packhöhe dort 179 mm); 2 mm Nut in der oberen Kühlplatte LFP für den Querverbinder; Anschlusslaschen, Verlust der Al-Verbinder. ENT-122 auf [NMC] gesetzt (Sonnet, Opus bestätigt). Vorgang: [E2]

## B-BAT-024 (2026-11-18) E2 Elektronik Teil 1: Abgriffe, Ausgleich, Vorladung ok; HV-Verlust 13 W/m akzeptiert; Schaltbox Fall b
- Teil 1 (`sim/elektrik/e2_elektronik/ERGEBNIS.md`): 251/218 Abgriffe, Ausgleich 12,3 h, Vorladung 8 A/320 J/300 ms. Opus-Fehler in der Erwartung: ≤ 15 W bei 3–5 m HV-Leitung war mit 50 mm² nicht möglich (≈ 13 W/m, nur beim Schnellladen). NMC-Heizung 26 min unter dem Band, weil die Zellmasse kleiner ist (308 kg).
- CMU-Wärme NMC 9,95 W bei Nennspannung, bei Ladeschluss über 10 W → Rechnung mit Zellhöchstspannung nachholen.
- Autor: Schaltbox auf dem Deckel vorne (ENT-109). Antworten auf Sonnets Fragen 1–3 im Nachtrag 1 der ERWARTUNG; 4: 139 A (1,5C) gilt; 5: Höchstspannung LFP 3,65 V, NMC 4,2 V (Annahme). Vorgang: [E2]

## B-BAT-023 (2026-11-17) C2 Kalibrierung: Blade-Widerstand gemessen 0,877 mΩ; 4680 schafft 30 min bei 1,5C, Plating-Risiko im Modell
- Blade 25 °C, 15–90 % SOC: RMS 15,3 mV, R10 Modell 0,827 / Messung 0,877 mΩ (Test#5). Temperaturfit verfehlt (158 mV), OCV des Literatursatzes 143 mV daneben → **DFN für LFP nicht belastbar; Opus: für Wärme den gemessenen Widerstand nutzen** (unsere Zelle 1,28 mΩ → 48 W statt 55 W bei 2,1C; K1 war konservativ).
- 4680 (Chen2020-Material, W20-Geometrie, DCIR 6,4 mΩ im Band): 10→80 % in 29,7 min bei 1,5C CC-CV → REQ-P05 erfüllbar. Wärme 7,4 W (Modell) bzw. 11,5 W (I·ΔU) gegen K1b-Annahme 6,7 W → K1c: LFP 32,7 °C / 4,0 K ✓; 4680 mit Modellwärme 34,0 / 4,15 ✓, mit I·ΔU 39,1 / 6,5 ✗ (5 K). Opus: Differenz der Maße = Mischungswärme der Konzentrationsgradienten (I·ΔU gegen Gleichgewichts-OCV, obere Schranke); Autor: „einverstanden“ → Auslegung mit Modellwärme, I·ΔU als ungünstigster Fall; 4680-30 min „knapp, nicht abgesichert“; Plating als Risiko R-… **Anodenpotential < 0 V in allen Läufen (auch 1C)** → Plating-Risiko laut generischem Satz; ohne 4680-Messdaten nicht entscheidbar.
- openpyxl ins venv installiert (requirements.txt nachtragen). Vorgang: [C2]

## B-BAT-022 (2026-11-17) C1 Zellmodell: NMC bestätigt K1, aber 10→80 % erst in 36 min; LFP-Parametersatz passt nicht
- PyBaMM (Sonnet): NMC Chen2020 23,19 Ah, DCIR 6,4 mΩ, Wärme 6,9 W (K1 6,7 W ✓). CC-CV: 4,2 V nach 21,8 min, 80 % nach 36,2 min → REQ-P05 (30 min) mit diesem Satz verfehlt (Satz ist 21700, nicht 4680).
- LFP Prada2013: halbe Beladung, Skalierung ×1,9 → DCIR 0,76 mΩ, Wärme 32,8 W gegen Messung 1,46 mΩ / 55 W. K1 bleibt bei Messung. → C2 Kalibrierung (Blade-Pulsdatensatz quellen/blade_datensatz). DEUTUNG.md. Vorgang: [C1]

## B-BAT-021 (2026-11-17) Kühlplatten K2: laminar, U nur mit 4-mm-Kanälen ≥ 500; Durchfluss offen
- K2 (Sonnet, 1D): Re 27–188, h_Kanal 260–316 W/(m²K) (Erwartung Opus 500–1000 zu optimistisch: laminar Nu ≈ 4–5). Mit Stegen auf Grundfläche bezogen und Pad/Blech in Reihe: U 565–595 nur bei 4 × 5 mm Kanälen. Δp ≈ 0,005 bar, Pumpe < 1 W. Mäander ohne Nutzen.
- Durchfluss für ΔT_Kühlmittel 5 K: LFP 47 L/min, NMC 20 L/min; bei 10 K halbiert, U gleich (laminar). Autor: „ja setzte deinen vorschlag um.“ → ENT-107 LFP 23 L/min (10 K), ENT-108 NMC 20 L/min (5 K). ENT-104…106 vorgeschlagen. Vorgang: [K2]

## B-BAT-020 (2026-11-17) Fixierung, Kontaktierung, Kühlung der 4680 nach Herstellervergleich
- Autor: „du musst aber auch fixierung sowie kontaktierung der rundzellen vorsehen“; „schau mal erst wie andere hersteller das ... machen“; „verteile die rechereche“. PI W24 (24/0), W25 (10/0), W26 (14/0), P14 leer; Sonnet Quellensuche; Haiku Tabelle forschung/vergleich_rundzellen.md.
- Belegt: einseitige Kontaktierung (Lucid, Rivian, Tesla), Al-Verbinder (Lucid), Verguss zwischen Zelle und Kühlung (Tesla), Ableiterscheiben Al 400 µm / Cu 260 µm, DCIR 4680 5,4–7 mΩ (bestätigt K0-Annahme 6,5).
- **Widerspruch:** Becherwand 4680 laut W24/W25 (batterydesign.net, Sammelseite) 0,5–0,6 mm, ENT-029 0,4 mm aus W20 (eigene Zerlegung, Primärquelle). Opus: ENT-029 bleibt, W24-Wert als Band in der Akte nennen; Unterschied evtl. Zellgeneration.
- Nicht belegt: wo Hersteller Rundzellen kühlen (Seite/Boden/oben) – nur Vorab-Websuche (Tesla Seitenbänder), nicht zitatgeprüft.
- Vorschlag ENT-092…095 [NMC]: Träger unten + Verguss, Al-Verbinder einseitig oben, Laserschweißen (Annahme), isolierendes Pad zwischen Verbindern und oberer Kühlplatte. K1b (h_eff 214 oben): NMC 20 min 42,8 °C/8,1 K ✗, 25 min 36,8/5,4 ✗ (knapp), 30 min 33,3/3,8 ✓; 25 min erfüllt bei Bedeckung φ ≥ 0,7. Erwartung Opus 1–3 K zu hoch (Pad-Widerstand überschätzt bzw. Verguss/Boden trägt mehr). - Autor: „30 minuten“ → REQ-P05: NMC-4680 schnellladen 10→80 % in 30 min (LFP 20 min). Erster bewusster Spezifikationsunterschied der Varianten. Verbinder schmal genügt (φ 0,5), Auslegung E.
- **G4 Pack-CAD (Entwurf):** 0 Kollisionen; LFP 611 kg (C0b 616), NMC 480 kg (C0b 411): Packfaktor 0,64 statt 0,75, weil NMC das auf LFP ausgelegte Gehäuse (2030 mm), zwei Kühlplatten und Verguss trägt. Folge Opus: „gleiche Spezifikation“ kostet NMC ≈ 70 kg; NMC-eigenes Gehäuse (1950 mm) wäre leichter – Autor: „2 kürzer und eigenes gehäuse“ → ENT-102 (LFP 2030), ENT-103 (NMC 1950); ENT-096…101 freigegeben („1 ja“). G4 neu: NMC 1950 mm → 473 kg (−7 kg, Opus-Schätzung 15–25 kg zu hoch: Länge betraf nur Wanne/Platten-Enden). Restlicher Mehrbedarf gegen C0b: zwei Kühlplatten, Verguss, Träger.
- Werkzeug: Monitor-/Warte-Befehle mit `pgrep -f "…lauf.sh…"` fanden den eigenen Befehl (Sonnet bei W26 bemerkt, Opus vorher bei W-Läufen) → Muster mit `^bash` bzw. `[l]auf.sh` verankern.
- Bericht 0.2 (43 S.) nutzt ergebnis.json; Rundung K1b P3 dort 36,8/5,4 (abgeschnitten) statt 36,9/5,5.
- Autor: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“ → alle 67 vorgeschlagenen Akten entschieden (Mensch); 103/103 entschieden. Abgeleitete Werte (ENT-015/018/020/032/038/044/074) und unsichere Lesarten (ENT-028/029/037/043/062/068) bleiben im Text als solche benannt.
Vorgang: [G4] [K1]

## B-BAT-019 (2026-11-17) Schnellladen in den Griff bekommen (K1); Gehäuserecherche W21
- Autor: „Ja das schnellladen müssen wir in den griff bekommen. man läd schwellenartig könnte auch sein, oder nur bestimmte zellen im wechsel, kühlen kann man auch und dann natürlcih begrenzen. mach die renderings neu. bei der gesamtbatterie müssen verstrebungen vorgehalten werden du kannst mal eine recherche machen wie ein batteriegehäuse aufgebaut ist.“
- Opus vorab: Bei fester Ladezeit erzeugt konstanter Strom die wenigste Joulewärme; Stufen +9 %, Puls/Zellen im Wechsel +100 %. In Reihe führen alle Zellen denselben Strom → Wechsel einzelner Zellen nur bei Parallelgruppen und dann wärmer. Spreizung hängt am Wärmeweg: nur beidseitige Kühlung oder kleinerer Strom (LFP ≤ 1,29C, NMC ≤ 1,02C stationär) bringt 5 K. Prüfung durch Rechnung K1.
- Autor (Nachtrag): „bei der Breite sind wir nicht so variabel letzten endes von straßenbreite begrenzt, länge ist etwas einfacher.“ → Breite 1430 mm gilt als fest, Länge darf wachsen. Folge Opus: Querträger quer zur Fahrtrichtung kosten Länge (zulässig); ein Längsträger zwischen den zwei LFP-Zellreihen und breitere Seitenrahmen kosten Breite (Reserve 8 mm) → kritisch, Seitenrahmenbreite aus W22 gegen den angenommenen Rand prüfen.
- Verstrebungen: struktur.json hat BT-530 Querträger, BT-540 Seitenrahmen, BT-550 Unterfahrschutz; W21 soll Werte liefern. Wichtig für Bauraum: Querträger kosten Länge/Breite (G1-Reserve LFP 16/8 mm!). - W21 (12/0): Bauweise CTP, Wanne/Deckel/Rahmen Alu; keine Maße. W22 (Lauf 3, 13/1): Querträger-Profil 54 × 26 mm, Wand 2–3 mm, Oberprofil 19 × 30 mm (US9045030, Pack 2,7 × 1,5 m); Seitenlast ≈ 600 kN bei > 2600 kg, Alu-Strangpress > 20 % leichter als Stahl (US20200148066). **Gesperrt:** SSAB „1,8 mm“ (Zitat zweimal nicht im Text). Seitenrahmenbreite weiter ohne Beleg. Lehre: Suchbegriffe zu breit → Paketgrenze 8000 Zeichen je Quelle schnitt die Maßstellen ab.
- **K1 Ergebnis:** LFP mit Kühlung oben+unten erfüllt REQ-P09 bei 20 min (33,8 °C/4,6 K). Stufen ≈ wirkungslos, Puls/Wechsel schlechter, h/Vorkühlung nur T_max. NMC K3 mit Tab-Scheibe: 20 min 38,9 °C/5,8 K (knapp), 25 min 34,0 °C/3,8 K (erfüllt). Annahme Spalt-k_z 31 W/mK. DEUTUNG.md.
- **M0:** LFP 121 mm hoch, 2024 mm lang (3 Querträger); NMC 111 mm, 1120 Plätze für 868. Akten ENT-082…091 vorgeschlagen (u. a. ENT-088 ersetzt ENT-081, ENT-091 2030 mm ersetzt ENT-013). Offen: Seitencrash über Schweller (Autor), NMC-Zellen gleichmäßig auf Felder verteilen (G4).
- Autor: „ja gehen wir ersteinmal so ins rennen. du musst aber auch fixierung sowie kontaktierung der rundzellen vorsehen“ → ENT-082…091 entschieden (Mensch), Seitencrash über Schweller akzeptiert. **Konflikt (Opus):** 4680 hat Plus- und Minuspol oben (Minus am Becherrand) → Zellverbinder liegen oben, wo K1/ENT-088 die obere Kühlplatte annimmt. Kühlung oben nur über isolierte Verbinderebene oder Kühlung unten + Seite. Recherche P14/W24 läuft.
Vorgang: [K1] [M1]

## B-BAT-018 (2026-11-17) K0 Wärme Einzelzelle: Schnellladen verfehlt 5 K bei beiden, 45 °C bei NMC
- Elmer, CPU, Bilanz < 0,001 %, Netz 0,017 K. 1C: LFP 30,1 °C/3,0 K, NMC 33,5 °C/4,8 K (Vorgabe erfüllt). 2,1C 20 min: LFP 43,1 °C/10,6 K, NMC Boden 53,6 °C/16,0 K, NMC Mantel 49,9 °C/18,1 K.
- Verfehlte Erwartung NMC: Opus-Fehler (Filmwiderstand am 16,6-cm²-Boden vergessen, 18 K bei 2,1C). DEUTUNG.md.
- pvbatch ohne Python-Modul → Blender-Workbench-Render und 3 MP4. VTU (595 MB) nach /home/cae/cae_projekte/batterie/k0_zelle/elmer verschoben (Link).
- Offen beim Autor: Umgang mit 5 K beim Schnellladen; Gehäuse-c/Dichte fehlt in eingaben.json (ganze Masse im Kern). Bericht: 683/644-kg-Zielband zwischen empfindlichkeit.png und kriterien.png uneinheitlich (verschiedene Bezugsfälle). Vorgang: [K0]

## B-BAT-017 (2026-11-17) Vorgaben Kühlung (REQ-P09, ENT-081); Bericht begonnen
- Autor: „45 °C und 5 K passen, Kühlplatte unten, bitte auch temperaturverläufe grafisch am besten als gerendertes Bild, und für die dikoumentation abspeichern, fange auch an den bericht zu schreiben“.
- REQ-P09: T_max ≤ 45 °C, Spreizung in der Zelle ≤ 5 K (festgelegt). ENT-081 BT-600 kuehlart = Kühlplatte unten (beide Varianten, entschieden). K0: K1 Hauptfall, gerenderte Temperaturbilder und Film (pvbatch) nachbeauftragt.
- Bericht BAT-DOC-17 (bericht/bericht.tex, LaTeX wie Fusion-Bericht, Lesehilfe je Bild, Begriffskästen) an Sonnet nach Gliederung von Opus. Vorgang: [K0] [B1]

## B-BAT-016 (2026-11-17) Detailmodell Innenaufbau fertig; 4680-Wickel ragte über den Becher (Opus-Fehler im Kern)
- Sonnet (cad/zelle/AUFTRAG_DETAIL.md, 42 min, CPU): FreeCAD-Detailmodelle beider Zellen, 7 Schnitt-/Explosionsbilder, Neulauf G1/C0b mit 1430 mm (LFP A passt, Reserve L 16 / B 8 mm; nötig 203,9 Wh/L; NMC 1260 Plätze).
- LFP-Stapel 12,476 mm in 13,4 mm (Rest 0,92 mm) – wie erwartet. Bild LFP_schnitt angesehen: Schichtfolge, Fahnen, Stromschiene, Halter, O-Ring, Isolationsbeutel erkennbar und beschriftet.
- **Verfehlt:** 4680-Wickel Außenradius 23,75 mm > 22,6 mm. Ursache 1 (Opus): ENT-074 Kern Ø 14 mm nur aus Kathodenfläche abgeleitet; mit allen Bändern (1477 mm²) Kern ≤ 12,75 mm → ENT-074 auf 12,5 mm korrigiert. Ursache 2 (Modell): feste Steigung 0,45 mm auch dort, wo nur noch Anode/Separator liegt → flächentreue Spirale. **Behoben 12:30:** Außenradius 22,565 mm in 22,60 mm (0,035 mm Luft), Kathode 36,7 Windungen. Rest: erste Windung ragt 0,45 mm in den Kern (Band um die Spirallinie zentriert), Startversatz der Bänder Annahme 0.
- Offen: Lesart Fahnenmaße (LFP 27,1/9 und 20,5/7 mm; 4680 2,5/5 und 7,5/2,5 mm), Isolierrand und Klebeband nicht modelliert. Vorgang: [G2]

## B-BAT-015 (2026-11-17) Innenaufbau beider Zellen aus der Zerlegung; Korrektur LFP-Länge 681 mm; Bauraumbreite 1430 mm
- Autor: „kann man die zellen weiter detailieren ist die nmc nicht eine gewickelte folie? Isolatoren und so müssten ja auch noch rein. auch eine LFP sollte detailiertzer dargestellt werden“.
- Opus liest W20 Tabelle 1, Abb. 2 (alle Innenbauteile), Abb. 4 (Kontaktierung), Abb. 5 (Elektrodenmaße) → cad/zelle/aufbau_W20.json. Werte aus Abbildungen sind von Opus abgelesen (pruefe.py kann Bilder nicht prüfen). Tabelle 1: Einheit „mm“ ist µm (Satzfehler; Probe: Blade-Stapel 38 × 160 + 39 × 140 + 78 × 12 µm = 12,5 mm bei 14 mm Zelle).
- **Eigener Fehler gefunden:** ENT-015 (660 mm) skalierte die Endzone mit. Elektrode 899,5 von 965 mm → Endzone 65,5 mm bleibt fest → **681 mm**. Zwei Reihen 1362 mm > 1340 mm innen → Autor wählt Bauraumbreite **1430 mm** (ENT-030, entschieden). ENT-015 korrigiert (vorgeschlagen).
- 4680-Wickel: Kathode 3215 × 72 mm, Anode 3305 × 73, Separator 2 × 3550 × 75; Wickeldicke je Windung ≈ 0,45 mm → ≈ 34 Windungen, Kern Ø ≈ 14 mm (**abgeleitet, nicht gemessen**).
- Baum: BT-111 Kathode, 112 Anode, 113 Separator, 114 Isolierrand, 115 Wickelkern [NMC], 116 Fixierung/Isolationsbeutel, 121 Gehäusefolie [LFP], 122 Füllöffnung, 131 Stromschiene/Tab-Scheibe, 132 Polisolation; BT-140 lage. 60 Einträge (ENT-031). Akten ENT-032…080 vorgeschlagen.
- Unsicher: Bedeutung der Fahnenmaße in Abb. 5A (27,1/9 bzw. 20,5/7 mm). Vorgang: [G1] [G2] [C1]
- **Nachtrag Detailmodell (Sonnet, 2026-11-17, `cad/zelle/entwurf/detail/ERGEBNIS_detail.md`):** 4680-Wickel aus den Akten (Kern Ø 14 mm, 0,45 mm je Windung, Bandlängen 3215/3305/3550 mm) ragt 1,15 mm über den Becher (Außenradius 23,75 mm gegen 22,60 mm innen; Kathode 34,5 Windungen, endet bei 22,68 mm). Erwartung „Außenradius ≤ 22,6 mm“ verfehlt, offen an Opus (Verdichtung oder Kern?). LFP-Stapel 12,476 mm in 13,4 mm: erfüllt.

## B-BAT-014 (2026-11-17) G1: Zellmaße je Variante als Akten (ENT-014…029, vorgeschlagen)
- Autor: „ja mach“ (Zellmaße als Akten vorschlagen).
- LFP [LFP]: Blade-Querschnitt verkürzt, 660 × 90 × 14 mm, 92,4 Ah, 3,2 V, ~1850 g (Annahme: Masse ∝ Ah), Z-gefalteter Einzelstapel mit 38 Kathodenlagen, Gehäuse Aluminium (PET-isoliert), Wand 0,3 mm. Länge ∝ Ah ist **Annahme** (Polzonen vernachlässigt).
- NMC [NMC]: 4680 Ø 46 × 80 mm, Wickel (tabless), Stahl vernickelt (Quelle: „presumably“), Wand 0,4 mm.
- Belege W20 (Zerlegung, Tabelle 1 und Fließtext, von Opus am Rohtext gelesen), G1-Rechnung. pm.py pruefe: 29 Akten, 0 Fehler.
- G2-Entwurf fertig (cad/zelle/, FreeCAD 1.1.4 headless): LFP 0,8316 L, 355,6 Wh/L; 4680 0,1330 L, 643,6 Wh/L (Opus nachgerechnet, = W20). Parametertest Länge 700 mm ohne Codeänderung. Bilder angesehen: plausibel; Polmaße Annahme (LFP Ø 10 mm auf 14 mm Stirnfläche, eng; W20 nennt Gewindepole seitlich → Polform später prüfen). Innenaufbau nicht modelliert. Standardlauf bricht ohne freigegebene Akten mit FEHLT ab (gewollt). Vorgang: [G1] [G2]

## B-BAT-013 (2026-11-17) Entscheidungen des Autors: ENT-012 freigegeben, Bauraum verlängert (ENT-013)
- Autor 2026-11-17: „ENT 012 ist freigegeben, verlängere den Bauraum, dokumentiere die entscheidungen“.
- ENT-012 (Baum mit Varianten, BT-250 Zellhalter) entschieden (Mensch). ENT-013: BT-000 bauraum_laenge_mm = 1950 mm für beide Varianten; Zahl von Opus aus G1 (1874 mm Stapel + 2 × 30 mm Rand = 1934 mm, + 16 mm Reserve). Breite 1400 und Höhe 130 mm bleiben Annahmen.
- Nachgeführt: Lastenheft REQ-P03 (800 V), REQ-P06 (zwei Varianten), REQ-P07 (L 1950 mm); docs/09 AEN-006…011; docs/04 (13 Akten, 0 Fehler).
- Neulauf (Sonnet, Opus nachgerechnet): nötig Fall A 208 Wh/L (vorher 214), LFP B 262; LFP A jetzt **erfüllt** (+2,3 %) und passt geometrisch mit 16 mm Reserve bei 1 mm Zellabstand. LFP B passt weiter nicht (Breite). NMC 1232 Plätze, Belegung 70/88 %. Massen unverändert. Erwartung (Nachtrag) erfüllt.
- Werkzeughinweis: erzeuge_bericht.py setzt die Kernaussage im Folienbaustein auf „(Opus)“ zurück → Skript muss vorhandene Kernaussage erhalten (offen für Sonnet). Vorgang: [G1] [V1] [C0]

## B-BAT-012 (2026-11-17) G1-Vorprüfung Zellanordnung: LFP-Blade passt nur ohne Zwischenraum, NMC-4680 mit Reserve
- Rechnung sim/geometrie/g1_anordnung/ (Sonnet; Opus Bild angesehen, Zählung NMC nachvollzogen: 32 Reihen × ~38 = 1200 Plätze).
- LFP A: 92,4 Ah → Zelle 660 × 90 × 14 mm, zwei Reihen quer (1320 ≤ 1340 mm). 125 Zellen je Reihe = 1874 mm gegen 1840 mm innen: passt nicht bei 1 mm Abstand; Grenze 0,73 mm. Blade-Zwischenlage (BT-220) und Wärmeschutz haben so keinen Platz. Höhe 120/130 mm passt.
- LFP B: 116,2 Ah → 831 mm, passt in keiner Lage. (Erwartung nannte 111 Ah/790 mm: Opus hatte die C0-Energie statt der C0b-Energie 93,0 kWh eingesetzt; Urteil unverändert.)
- NMC A: 868 von 1200 Plätzen (72 %), Höhenreserve 20 mm; NMC B: 1085 (90 %).
- Folge: Bestätigt C0b geometrisch. LFP braucht mehr Länge (≥ 1,93 m bei 1 mm), dünnere Rand-Annahme oder Fall A mit kleinerer Reichweite. Annahmen Rand 30 mm / Höhen bestätigt unkritisch; kritisch nur der LFP-Zellabstand. Vorgang: [G1] [G4]

## B-BAT-011 (2026-11-16) Variantenvergleich mit Messwerten: NMC-4680 ein Drittel leichter, LFP-Blade im Bauraum knapp
- Rechnung sim/chemie/varianten_lfp_nmc/ (Sonnet; Opus-Gegenrechnung gleich). Fall A: LFP 616 kg (160 Wh/kg gemessen; 469 kg bei 210 Gen 2), NMC 411 kg (217s×4p = 868 Zellen, 74,3 kWh). Anteil 41 % gegen 27 %.
- Fall B: LFP 93,0 kWh / 775 kg, NMC 86,6 kWh Bedarf, 5p → 92,8 kWh / 514 kg.
- Bauraum: LFP A −0,3 % (knapp), B nicht erfüllt; NMC erfüllt. Zyklen: LFP erfüllt, NMC unsicher.
- Stückliste je Variante: LFP 38 Pos., NMC 37 Pos. (200.2/200.4 entfallen, 200.5 Zellhalter neu; struktur.json BT-250 → 200.5 von Opus eingetragen). Offen: Zellen je Reihe und Fühler bei NMC aus LFP-Annahme (G4); Bild zeigt LFP-Balken bei Bandmitte statt Messwert.
- Deutung DEUTUNG.md. Vorgang: [C0] [V1] [G3]

## B-BAT-010 (2026-11-16) Zwei Varianten parallel: LFP-Blade und NMC-4680, gleiche Spezifikation
- Autor: „kannst du auch zwei varianten paralell bauen? bei mit den selben spezifikationen“; Wahl NMC = Rundzelle 4680.
- Umsetzung (Sonnet, Auftrag pm/AUFTRAG_VARIANTEN.md, Opus geprüft): Akten haben `variante:` (null = alle); pm.py pruefe erlaubt gleiche Merkmale in verschiedenen Varianten; parameter.json (gemeinsam) + parameter_LFP/NMC.json; startwerte.py/stueckliste.py `--variante`. Gemeinsam: ENT-004 Baum, ENT-006 800 V.
- Akten: ENT-005 nur [LFP]; ENT-007…011 [NMC] (NMC811, Rundzelle 4680, 23,125 Ah, 3,7 V, 355 g; W20), entschieden (Mensch, Formatwahl des Autors, Werte gemessen). ENT-012 (vorgeschlagen): Baum mit Feld `varianten`, BT-250 Zellhalter (NMC), BT-100 durchmesser/hoehe, BT-220/240 nur LFP; 50 Einträge.
- Fehler von Sonnet gemeldet und von Opus behoben: stueckliste.py las `_par["BT-000"]` statt `_par["parameter"]["BT-000"]` (Spannung kam still aus startwerte, Wert zufällig gleich).
- Variantenvergleich mit Messwerten (C0b) läuft, Erwartung vorher. Vorgang: [C0] [G1] [G3] [V1]

## B-BAT-009 (2026-11-16) Zerlegungsstudie Blade (W20): Gen-1-Zelle 160 Wh/kg, 355 Wh/L; Bauraum Fall A genau an der Grenze
- Quelle: Cell Rep. Phys. Sci. 6, 102453 (2025), CC-BY, PDF vom Autor in quellen/blade_zerlegung/. PI-Lauf W20: 0/21, weil PI die DOI statt der file://-URL angab. Opus: URL ersetzt → 17/21; die 4 Reste stehen im Fließtext (pdftotext ohne -layout, zweispaltiger Satz). Z25 („around 23 of the heat“) gesperrt: Bruch bei der Textumwandlung verloren.
- **Blade-Zelle (gemessen, Tabelle 1):** 135 Ah, 432 Wh, 3,2 V, Fenster 2,6–3,65 V, 2,7 ± 0,3 kg, 1216 mL, **160 Wh/kg, 355,3 Wh/L**, 965 × 90 × 14 mm, Wandstärke Gehäuse 0,3 mm, ein Z-gefalteter Elektrodenstapel, Aktivmasse etwa 60 % der Zellmasse. Zum Vergleich Tesla 4680 (NMC811): 241 Wh/kg, 643 Wh/L.
- **Folge Bauraum:** 355 Wh/L × 60 % Volumennutzung (W19) = 213 Wh/L Pack. Nötig: 214 (Fall A), 256 (Fall B). Fall A passt knapp, Fall B nicht. Prüfpunkt von ENT-005 damit **an der Grenze, nicht klar erfüllt**.
- **Folge Masse:** 160 Wh/kg liegt unter dem C0-Band 185–210 (W03, Hersteller, Long Blade 2.0). Mit 160 Wh/kg, Zellanteil 0,75: Packmasse Fall A 616 kg (543–711), Fall B 739 kg. Eine 4680-NMC-Zelle ergäbe Fall A etwa 409 kg. Der Satz „kein belegter Massenunterschied“ (B-BAT-006) gilt nur mit den Herstellerwerten der 2. Generation.
- Folge 800 V (ENT-006): Eine Original-Blade-Zelle (135 Ah) gäbe 250s × 135 Ah × 3,2 V = 108 kWh. Nötig 92 Ah (A) → bei gleichem Querschnitt etwa 660 mm statt 965 mm Länge (G1).
- Werkzeuglücke: lauf.sh/AUFTRAG muss PI die genaue Quell-URL vorgeben; pruefe.py scheitert an zweispaltigem PDF-Satz (pdftotext -layout). Vorgang: [R4] [C0] [G1] [V1]

## B-BAT-008 (2026-11-16) W19 geprüft; Energiewiderspruch Stückliste 112 kWh gegen 73,9 kWh
- W19 (drpress HSET 2022, Studentenarbeit, Sekundärquelle): 20/20 Belege wörtlich bestätigt, inhaltlich schwach. **Gesperrt:** 332 Wh/kg „BYD battery“ (für LFP unplausibel, Bezug fehlt), 155 Wh/100 km Model Y (Einheit falsch), „ordinary 250 Wh/kg“ (Chemie offen), 180 Wh/kg „blade battery“ (Zelle oder Pack unklar). **Als Hinweis verwendbar (Pack, Sekundärquelle):** Volumennutzung Blade-Pack bis 60 %, konventionell etwa 40 %; Zelle ca. 0,6 m × 13,5 mm (Short Blade); Pack BYD Han ca. 79 kWh.
- Folge für den Bauraum: Bei 60 % Volumennutzung braucht die Zelle 357 Wh/L (Fall A) bzw. 427 Wh/L (Fall B). Das ist jetzt die Prüfgröße für die Blade-Zelle (Volumen Long Blade 1,166 L aus W03-Maßen). Die Blade-Kapazität (Ah) und damit die Wh/L der Zelle ist weiter **nicht belegt**.
- Sonnet-Umstellung (pm/AUFTRAG_LFP_UMSTELLUNG_ergebnis.txt): startwerte.json chemie = LFP (ENT-005 vor Bauraumregel), Warnung Bauraum offen; Obsidian 49 Bauteilnotizen (struktur.json hat 49 Einträge inkl. BT-000 und Baugruppen; die Zahl „46“ in früheren Notizen ist falsch). Opus geprüft: startwerte.json, docs/13, wissen/Bauteil, pm.py pruefe 0 Fehler.
- **Widerspruch:** Stückliste 250s × 1p × 3,2 V × 140 Ah = 112,0 kWh gegen Bedarf 73,9 kWh (+51 %). Die 140 Ah sind eine Annahme aus stueckliste.py. Bei 800 V und 1p bräuchte die Zelle 92 Ah, bei 400 V (125s) 185 Ah. Das ist eine Auslegungsfrage (Systemspannung und Zellgröße, G1/G3), dem Autor vorzulegen. Vorgang: [G1] [G3] [V1]

## B-BAT-007 (2026-11-16) Freigaben ENT-004/005; W18 geprüft; Blade-Zerlegungsstudie nicht abrufbar
- Autor 2026-11-16: „1500 kg sind erst einmal Anhaltswert, 2 und 3 gebe ich frei“ → ENT-004 (Bauteilbaum) und ENT-005 (BT-100 chemie = LFP) „entschieden (Mensch)“. REQ-P01 = Anhaltswert; Auslegung führt Fall A und B als Spanne (73,9–88,7 kWh brutto, LFP 499–599 kg).
- W18 (314-Ah-LFP-Prismenzelle, ESS-Format, nicht Blade): 17 Belege bestätigt, 1 Fehler. Gesperrt: Unsicherheiten 26/10/9,5 % (nicht im Rohtext). Verwendbar für das Elmer-Zellmodell (Bezug: andere Zelle, Analogie): λ Dicke 4,11, Breite 21,04, Höhe 19,82 W/(m·K) (Verhältnis ≈ 5:1); c_p 1112 J/(kg·K); Wärme 0,5C ≈ 22/23 W bei 5,638 kg; isotropes Modell 23–59 % Fehler bei der Spitzenerhöhung. Folge: Zellmodell orthotrop.
- Zerlegungsstudie doi:10.1016/j.xcrp.2025.102453 (CC-BY, OpenAlex „gold OA“): ScienceDirect/Cell 403, RWTH-Repositorium Bot-Sperre (JS-Challenge), Fraunhofer-Publica Anubis-Sperre, Elsevier-API nur mit Schlüssel. Automatisch nicht zu holen. Ersatz: W19 (drpress HSET „Feasibility of BYD blade batteries“, PDF abrufbar), läuft.
- Fund für C2/C3: Datensatz „Battery State-of-power Measurement“ (Borealis, doi:10.5683/SP3/RPCWBY, CC-BY 4.0) mit Pulsmessungen an BYD Blade 135 Ah, 2,6–3,6 V, −10 bis 40 °C, 10-s-Pulse, ganzes Leben bis 80 % SOH. Readme in quellen/blade_datensatz/. Kann Innenwiderstand des Zellmodells eichen (Messung statt Annahme). Vorgang: [R4] [C2] [V1]

## B-BAT-006 (2026-11-16) Chemievergleich LFP/NMC bei 1500 kg und 400 km: kein belegter Massenunterschied
- Rechnung `sim/chemie/vergleich_lfp_nmc/` (Sonnet nach Auftrag, 2 min; Opus-Gegenrechnung mit eigenem Skript gleich). Erwartung (ERWARTUNG.md, vorher) Punkte 1–6 erfüllt.
- Fall A (1500 kg mit Batterie): 73,9 kWh brutto. Packmasse LFP 499 kg (414–615), NMC 464 kg (316–758). Batterieanteil 33,3 % bzw. 30,9 %, beide über der Annahme 30 %.
- Fall B (1500 kg ohne Batterie): 88,7 bzw. 87,4 kWh brutto (+20 %/+18 %, 6 Iterationsschritte). Packmasse 599 bzw. 549 kg, Anteil 28,5 % bzw. 26,8 %.
- Zyklenbedarf 1000: LFP erfüllt, NMC unsicher. Zellen in Reihe bei 800 V: 250 / 220. Bauraum (214 Wh/L nötig): für LFP offen.
- Stärkste Annahme: LFP Zellanteil am Pack (Hub 196 kg), NMC Zellband (Hub 434 kg).
- Folge: Vorschlag ENT-005 LFP-Blade als Hauptvariante. Die NMC-Wahl in startwerte.py beruhte auf einer unbelegten Annahme. Rückfrage an den Autor: 1500 kg mit oder ohne Batterie? Vorgang: [C0] [V1]

## B-BAT-039 Crash LFP_a ungültig: Zellreihen ohne gegenseitigen Kontakt (2026-11-21, Opus)
Die Kennzahlen von LFP_a sahen gut aus: Eindringung 13,9 mm, Zellreihe 8,1 mm, Energiefehler 0,19 %. Das Verformungsbild zeigte aber in Packmitte einen Streifen, der sich um 60 mm verschoben hatte, und am Ende stand eine Restbewegung von 750 J. Die Rohdaten belegen: 3426 Zellknoten verschieben sich in x um bis zu 319 mm. Ursache ist, dass jede Reihe ein eigener Block mit 1 mm Spalt ist und es zwischen den Reihen keinen Kontakt gibt. Die Reihen unter dem Pfahl neben dem Querträgerspalt durchdringen ihre Nachbarreihen. Korrektur nach ERWARTUNG Nachtrag 3: 4 homogene Blöcke, Füllgrad 14/15, und eine neue automatische Modellprüfung (max |U| der Zellen ≤ 1,5 × Pfahlweg, Restbewegung < 5 %). Lehre: Energiebilanz und Kennzahlen allein erkennen diesen Fehler nicht. Erst das Bild hat ihn gezeigt.

## B-BAT-040 Thermik-Varianten K4 und Crash LFP_a neu (2026-11-21, Opus)
- K4, Tabelle T_max/ΔT aus rechnen/log_K4_*.txt, LFP-Schnellladen: V0 42,6/16,4; V1 gegensinnig 38,4/10,5; V2 Durchfluss ×2 37,0/11,1; V3 beides 34,8/8,1. Die Schätzung von Opus vorab (11–12 / 10–11 / 7–8 K) traf. Keine Variante erreicht ΔT ≤ 5 K, daher wird eine Parallelführung mit Z-Verteiler zum Verbesserungsvorschlag. NMC 30 min: V0 34,1/5,9, V3 30,1/1,5. Dauerfahrt: LFP 29,0/3,8, NMC 29,7/3,0.
- X3 LFP_a nach der Korrektur (Nachtrag 3): Pfahl 13,6 mm, Zellblock 6,7 mm, Innenwand 7,8 mm, 472 kN, Energiefehler 0,18 %, max |U| der Zellen 7,4 mm. Opus-Fehler im Kriterium „kinetische Energie am Ende < 5 %“: Darin steckte auch der Rückprall des Pfahls (17,6 %). Neu gilt die kinetische Energie ohne Pfahl, das sind 2,4 %. Modellprüfung bestanden. Das Kennzahlenbild entspricht dem ungültigen Lauf (13,9/8,1 mm), weil die gleitenden Reihen weit vom Pfahl wenig zur Steifigkeit beitrugen.
- Zweiter Fehler: In der untesteten Auswertung von Sonnet war `pw` nicht definiert; bei der Reparatur der Zeile hat Opus den Rest der Zeile in einen Kommentar verschoben. Beides ist behoben, die Auswertung ist an LFP_a getestet.
