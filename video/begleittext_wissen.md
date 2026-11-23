| Dok.-Nr. | BAT-DOC-13b | Version | 0.1 | Status | freigegeben (Autor 2026-11-23) |
|---|---|---|---|---|---|
| Titel | Zweites Abschlussvideo „Batterie und Wissensgraph“: Begleittext (DE) | Ersteller | Claude Sonnet (KI) | Prüfer | – |

> **KI-generiert.** Erzeugt von `video/begleittext_wissen.py` aus `video/begleittext.md` und `datenquellen.json` des Graphen (Stand 2026-11-23). Im Video steht nur der Name; dieser Text begleitet es. Entwurf, nicht freigegeben.

Die Szenen 1 bis 8 sind dieselben wie im ersten Video (`video/abschluss.mp4`). Neu sind der durchsichtige Grund mit dem wachsenden Wissensgraphen dahinter und der Schluss (Abschnitt unten).

## Szene 1: BT-100 Zelle (1 bis 12 s)

Zelle (BT-100). Aufgabe: speichert Energie (Chemie, Elektroden, Gehäuse, Pole, Ventil). Teil von: BT-000. Meine Teile: BT-110 Elektrodenstapel, BT-120 Zellgehäuse, BT-130 Zellpole, BT-140 Zellventil.

Entscheidungen, die die Form bestimmen (Quelle: Akten `pm/entscheidungen/`):

- **ENT-002** Zellmodell mit PyBaMM. Merkmal: - = None ; Anforderungen: REQ-P06, REQ-P10; Belege: –
- **ENT-005** Zellchemie LFP. Merkmal: chemie = LFP ; Anforderungen: REQ-P06, REQ-P10, REQ-P11; Belege: B-BAT-006, B-BAT-005
- **ENT-012** Bauteilbaum für zwei Varianten. Merkmal: - = None ; Anforderungen: REQ-P06, REQ-P11; Belege: B-BAT-009
- **ENT-014** Zellformat LFP: Blade-Querschnitt 90 × 14 mm, verkürzt. Merkmal: format = "prismatisch, Blade-Querschnitt, verkürzt" ; Anforderungen: REQ-P06, REQ-P07; Belege: B-BAT-009, B-BAT-012, B-BAT-013
- **ENT-015** Zelllänge LFP 681 mm. Merkmal: laenge_mm = 681.0 mm; Anforderungen: REQ-P06, REQ-P07; Belege: B-BAT-009, B-BAT-012, B-BAT-013
- **ENT-016** Zellhöhe. Merkmal: breite_mm = 90.0 mm; Anforderungen: REQ-P06, REQ-P07; Belege: B-BAT-009, B-BAT-012, B-BAT-013
- **ENT-017** Zelldicke LFP 14 mm. Merkmal: dicke_mm = 14.0 mm; Anforderungen: REQ-P06, REQ-P07; Belege: B-BAT-009, B-BAT-012, B-BAT-013
- **ENT-018** Zellkapazität LFP 92,4 Ah. Merkmal: kapazitaet_Ah = 92.4 Ah; Anforderungen: REQ-P06, REQ-P07; Belege: B-BAT-009, B-BAT-012, B-BAT-013
- **ENT-019** Nennspannung LFP 3,2 V. Merkmal: nennspannung_V = 3.2 V; Anforderungen: REQ-P06, REQ-P07; Belege: B-BAT-009, B-BAT-012, B-BAT-013
- **ENT-020** Zellmasse LFP etwa 1850 g. Merkmal: masse_g = 1850.0 g; Anforderungen: REQ-P06, REQ-P07; Belege: B-BAT-009, B-BAT-012, B-BAT-013

Anforderungen:

| REQ-P06 | Zellchemie | zwei Varianten gleicher Spezifikation (Autor 2026-11-16): LFP-Blade prismatisch (ENT-005) und NMC811-Rundzelle 4680 (ENT-007…011); Baum ENT-012 | Autor | Muss | entschieden |
| REQ-P10 | Lebensdauer (Zyklen, Jahre, Restkapazität) | offen | Autor | Soll | offen |
| REQ-P11 | Sicherheit: keine Ausbreitung des thermischen Durchgehens bzw. Warnzeit nach Norm | nach Norm (BAT-DOC-07) | Norm | Muss | offen |

## Szene 2: BT-200 Zellstack (12 bis 24 s)

Zellstack (BT-200). Aufgabe: Zellen in Reihe und parallel, mechanisch verspannt. Teil von: BT-000. Meine Teile: BT-210 Zellreihe, BT-220 Zwischenlage, BT-230 Wärmeleitmaterial, BT-240 Verspannung, BT-250 Zellhalter, BT-260 Verguss.

Entscheidungen, die die Form bestimmen (Quelle: Akten `pm/entscheidungen/`):

- **ENT-012** Bauteilbaum für zwei Varianten. Merkmal: - = None ; Anforderungen: REQ-P06, REQ-P11; Belege: B-BAT-009
- **ENT-148** Verschaltung LFP Schleife 2 Reihen: Plus und Minus hinten, Mitte vorn. Merkmal: verschaltung = schleife_2reihen ; Anforderungen: REQ-P02; Belege: B-BAT-024

Anforderungen:

| REQ-P02 | nutzbarer Energieinhalt | aus Reichweite 400 km (Vorgabe Autor 2026-11-16) × Verbrauch (Annahme), Vergleich sim/chemie/vergleich_lfp_nmc | Autor | Muss | Reichweite: Vorgabe Autor |
| REQ-P03 | Systemspannung (Nenn, min, max) | 800 V nominal (ENT-006, Autor 2026-11-16); min/max folgen aus Zellfenster | Autor | Muss | teilweise |

## Szene 3: BT-300 Regelung (BMS) (24 bis 34 s)

Regelung (BMS) (BT-300). Aufgabe: misst, schützt, gleicht aus, schaltet. Teil von: BT-000. Meine Teile: BT-310 BMS-Hauptsteuergerät, BT-320 Zellüberwachung, BT-330 Temperaturfühler Zelle, BT-340 Strommessung, BT-350 Isolationswächter, BT-360 Messleitungen.

Entscheidungen, die die Form bestimmen (Quelle: Akten `pm/entscheidungen/`):

- **ENT-110** Zentrales BMS mit Zellüberwachung. Merkmal: architektur = zentral_BMS_CMU_Daisy-Chain ; Anforderungen: REQ-P15; Belege: B-BAT-024

Anforderungen:

| REQ-P11 | Sicherheit: keine Ausbreitung des thermischen Durchgehens bzw. Warnzeit nach Norm | nach Norm (BAT-DOC-07) | Norm | Muss | offen |
| REQ-P15 | Messung und BMS: Zellspannung, Temperatur, Isolationswächter | Umfang offen | Autor | Muss | offen |

## Szene 4: BT-400 Verkabelung (34 bis 44 s)

Verkabelung und Zellverbinder (BT-400). Aufgabe: leitet den Hochvoltstrom von Zelle zu Zelle und zur Schaltbox. Teil von: BT-000. Meine Teile: BT-410 Zellverbinder, BT-420 Reihenverbinder, BT-430 HV-Hauptleitung, BT-440 Stromschiene, BT-450 Berührschutz.

Entscheidungen, die die Form bestimmen (Quelle: Akten `pm/entscheidungen/`):

- **ENT-004** Bauteilbaum bis Stücklistenebene; Schutzteile in Schaltbox unter BT-700. Merkmal: - = None ; Anforderungen: REQ-D11, REQ-D12, REQ-D13; Belege: B-BAT-004

Anforderungen:

| REQ-P04 | Dauer- und Spitzenleistung Entladen | offen (kW, s) | Autor | Muss | offen |
| REQ-P13 | Schutzart, Isolation, Berührschutz | nach Norm | Norm | Muss | offen |

## Szene 5: BT-500 Struktur (44 bis 58 s)

Struktur und Gehäuse (BT-500). Aufgabe: trägt, schützt, dichtet, Crash. Teil von: BT-000. Meine Teile: BT-510 Gehäusewanne, BT-520 Deckel mit Dichtung, BT-530 Querträger, BT-540 Seitenrahmen, BT-550 Unterfahrschutz, BT-560 Befestigungspunkte, BT-570 Druckausgleichselement, BT-580 Dichtungen, BT-590 Verbindungs- und Normteile.

Entscheidungen, die die Form bestimmen (Quelle: Akten `pm/entscheidungen/`):

- **ENT-004** Bauteilbaum bis Stücklistenebene; Schutzteile in Schaltbox unter BT-700. Merkmal: - = None ; Anforderungen: REQ-D11, REQ-D12, REQ-D13; Belege: B-BAT-004

Anforderungen:

| REQ-P07 | Bauraum (L × B × H) und Masse | L = 1950 mm (ENT-013, Autor 2026-11-17); B = 1430 mm (ENT-030, Autor 2026-11-17); H 130 mm Annahme; Masse offen (30 % Gesamtmasse als Annahme) | Autor | Muss | teilweise |
| REQ-P13 | Schutzart, Isolation, Berührschutz | nach Norm | Norm | Muss | offen |
| REQ-P14 | Mechanik: Stoß, Schwingung, Crash | nach Norm | Norm | Muss | offen |

## Szene 6: BT-600 Kühlung (58 bis 72 s)

Kühlung (BT-600). Aufgabe: führt Wärme ab, beim Schnellladen. Teil von: BT-000. Meine Teile: BT-610 Kühlplatte, BT-620 Verteiler und Sammler, BT-630 Kühlmittelanschlüsse, BT-640 Temperaturfühler Kühlmittel, BT-650 Kühlmittel, BT-660 Schnittstelle Fahrzeugkreis.

Entscheidungen, die die Form bestimmen (Quelle: Akten `pm/entscheidungen/`):

- **ENT-081** Kühlart Kühlplatte unten, für beide Varianten. Merkmal: kuehlart = "Kühlplatte unten" ; Anforderungen: REQ-P09; Belege: B-BAT-017
- **ENT-088** Kühlart: Kühlplatte oben und unten. Merkmal: kuehlart = "Kühlplatte oben und unten" ; Anforderungen: REQ-P09; Belege: B-BAT-019

Anforderungen:

| REQ-P05 | Schnellladen 10 → 80 % | LFP 20 min, NMC-4680 30 min (Autor 2026-11-17 „30 minuten“, nach K1b; Variantenunterschied) | Autor | Muss | festgelegt |
| REQ-P08 | Umgebungstemperatur Betrieb und Laden | offen (°C) | Autor / Norm | Muss | offen |
| REQ-P09 | max. Zelltemperatur und Spreizung | T_max ≤ 45 °C, Spreizung in der Zelle ≤ 5 K (Autor 2026-11-17) | Autor | Muss | festgelegt |
| REQ-P12 | Kühlmittel und Anschlüsse | Vorschlag Wasser-Glykol | Autor | Soll | offen |

## Szene 7: BT-700 Zusatzkomponenten (72 bis 82 s)

Zusatzkomponenten (BT-700). Aufgabe: Schütze, Sicherung, Vorladung, Stecker, Entgasung. Teil von: BT-000. Meine Teile: BT-710 Schaltbox, BT-720 Service-Trennstecker, BT-730 HV-Steckverbinder, BT-740 NV-Steckverbinder, BT-750 Pack-Entgasung, BT-760 Heizung, BT-770 Gas- und Drucksensor, BT-780 Kennzeichnung.

Entscheidungen, die die Form bestimmen (Quelle: Akten `pm/entscheidungen/`):

- **ENT-004** Bauteilbaum bis Stücklistenebene; Schutzteile in Schaltbox unter BT-700. Merkmal: - = None ; Anforderungen: REQ-D11, REQ-D12, REQ-D13; Belege: B-BAT-004

Anforderungen:

| REQ-P11 | Sicherheit: keine Ausbreitung des thermischen Durchgehens bzw. Warnzeit nach Norm | nach Norm (BAT-DOC-07) | Norm | Muss | offen |
| REQ-P13 | Schutzart, Isolation, Berührschutz | nach Norm | Norm | Muss | offen |
| REQ-P15 | Messung und BMS: Zellspannung, Temperatur, Isolationswächter | Umfang offen | Autor | Muss | offen |

## Szene 8: BT-000 Gesamtsystem (82 bis 110 s)

Batteriesystem (BT-000). Aufgabe: Gesamtsystem im Fahrzeug. Teil von: –. Meine Teile: BT-100 Zelle, BT-200 Zellstack, BT-300 Regelung (BMS), BT-400 Verkabelung und Zellverbinder, BT-500 Struktur und Gehäuse, BT-600 Kühlung, BT-700 Zusatzkomponenten.

Entscheidungen, die die Form bestimmen (Quelle: Akten `pm/entscheidungen/`):

- **ENT-001** PI recherchiert ohne Werkzeuge in drei Stufen. Merkmal: - = None ; Anforderungen: REQ-D01, REQ-D07; Belege: –
- **ENT-002** Zellmodell mit PyBaMM. Merkmal: - = None ; Anforderungen: REQ-P06, REQ-P10; Belege: –
- **ENT-003** Opus leitet und verteilt an Sonnet, Haiku, PI ohne Rückfrage. Merkmal: - = None ; Anforderungen: REQ-D04, REQ-D10; Belege: –
- **ENT-004** Bauteilbaum bis Stücklistenebene; Schutzteile in Schaltbox unter BT-700. Merkmal: - = None ; Anforderungen: REQ-D11, REQ-D12, REQ-D13; Belege: B-BAT-004
- **ENT-005** Zellchemie LFP. Merkmal: chemie = LFP ; Anforderungen: REQ-P06, REQ-P10, REQ-P11; Belege: B-BAT-006, B-BAT-005
- **ENT-006** Systemspannung 800 V. Merkmal: nennspannung_V = 800.0 V; Anforderungen: REQ-P02, REQ-P05, REQ-P06; Belege: B-BAT-006, B-BAT-008
- **ENT-012** Bauteilbaum für zwei Varianten. Merkmal: - = None ; Anforderungen: REQ-P06, REQ-P11; Belege: B-BAT-009
- **ENT-013** Bauraumlänge 1950 mm. Merkmal: bauraum_laenge_mm = 1950.0 mm; Anforderungen: REQ-P07; Belege: B-BAT-012, B-BAT-011
- **ENT-014** Zellformat LFP: Blade-Querschnitt 90 × 14 mm, verkürzt. Merkmal: format = "prismatisch, Blade-Querschnitt, verkürzt" ; Anforderungen: REQ-P06, REQ-P07; Belege: B-BAT-009, B-BAT-012, B-BAT-013
- **ENT-015** Zelllänge LFP 681 mm. Merkmal: laenge_mm = 681.0 mm; Anforderungen: REQ-P06, REQ-P07; Belege: B-BAT-009, B-BAT-012, B-BAT-013
- **ENT-016** Zellhöhe. Merkmal: breite_mm = 90.0 mm; Anforderungen: REQ-P06, REQ-P07; Belege: B-BAT-009, B-BAT-012, B-BAT-013
- **ENT-017** Zelldicke LFP 14 mm. Merkmal: dicke_mm = 14.0 mm; Anforderungen: REQ-P06, REQ-P07; Belege: B-BAT-009, B-BAT-012, B-BAT-013
- **ENT-018** Zellkapazität LFP 92,4 Ah. Merkmal: kapazitaet_Ah = 92.4 Ah; Anforderungen: REQ-P06, REQ-P07; Belege: B-BAT-009, B-BAT-012, B-BAT-013
- **ENT-019** Nennspannung LFP 3,2 V. Merkmal: nennspannung_V = 3.2 V; Anforderungen: REQ-P06, REQ-P07; Belege: B-BAT-009, B-BAT-012, B-BAT-013
- **ENT-020** Zellmasse LFP etwa 1850 g. Merkmal: masse_g = 1850.0 g; Anforderungen: REQ-P06, REQ-P07; Belege: B-BAT-009, B-BAT-012, B-BAT-013
- **ENT-021** Elektrodenstapel LFP: ein Z-gefalteter Stapel. Merkmal: bauweise = "Z-gefalteter Einzelstapel" ; Anforderungen: REQ-P06, REQ-P07; Belege: B-BAT-009, B-BAT-012, B-BAT-013
- **ENT-022** Kathodenlagen LFP 38. Merkmal: lagen_anzahl = 38.0 ; Anforderungen: REQ-P06, REQ-P07; Belege: B-BAT-009, B-BAT-012, B-BAT-013
- **ENT-023** Zellgehäuse LFP Aluminium. Merkmal: werkstoff = "Aluminium, PET-Folie isoliert" ; Anforderungen: REQ-P06, REQ-P07; Belege: B-BAT-009, B-BAT-012, B-BAT-013
- **ENT-024** Gehäusewand LFP 0,3 mm. Merkmal: wandstaerke_mm = 0.3 mm; Anforderungen: REQ-P06, REQ-P07; Belege: B-BAT-009, B-BAT-012, B-BAT-013
- **ENT-030** Bauraumbreite 1430 mm. Merkmal: bauraum_breite_mm = 1430.0 mm; Anforderungen: REQ-P07; Belege: B-BAT-015
- **ENT-031** Bauteilbaum Innenaufbau der Zelle. Merkmal: - = None ; Anforderungen: REQ-P06; Belege: B-BAT-015
- **ENT-032** Kathodenlänge LFP 615,5 mm. Merkmal: laenge_mm = 615.5 mm; Anforderungen: REQ-P06; Belege: B-BAT-015
- **ENT-033** Kathodenbreite LFP 82,5 mm. Merkmal: breite_mm = 82.5 mm; Anforderungen: REQ-P06; Belege: B-BAT-015
- **ENT-034** Kathodenbeschichtung LFP 70 µm je Seite. Merkmal: beschichtung_um = 70.0 µm; Anforderungen: REQ-P06; Belege: B-BAT-015
- **ENT-035** Al-Folie LFP 20 µm. Merkmal: folie_um = 20.0 µm; Anforderungen: REQ-P06; Belege: B-BAT-015
- **ENT-036** Kathodenblätter LFP 38. Merkmal: anzahl = 38.0 ; Anforderungen: REQ-P06; Belege: B-BAT-015
- **ENT-037** Kathodenfahne LFP 9 mm Überstand. Merkmal: fahne_mm = 9.0 mm; Anforderungen: REQ-P06; Belege: B-BAT-015
- **ENT-038** Anodenlänge LFP 620 mm. Merkmal: laenge_mm = 620.0 mm; Anforderungen: REQ-P06; Belege: B-BAT-015
- **ENT-039** Anodenbreite LFP 85 mm. Merkmal: breite_mm = 85.0 mm; Anforderungen: REQ-P06; Belege: B-BAT-015
- **ENT-040** Anodenbeschichtung LFP 65 µm je Seite. Merkmal: beschichtung_um = 65.0 µm; Anforderungen: REQ-P06; Belege: B-BAT-015
- **ENT-041** Cu-Folie LFP 10 µm. Merkmal: folie_um = 10.0 µm; Anforderungen: REQ-P06; Belege: B-BAT-015
- **ENT-042** Anodenblätter LFP 39. Merkmal: anzahl = 39.0 ; Anforderungen: REQ-P06; Belege: B-BAT-015
- **ENT-043** Anodenfahne LFP 7 mm Überstand. Merkmal: fahne_mm = 7.0 mm; Anforderungen: REQ-P06; Belege: B-BAT-015
- **ENT-044** Separatorlänge. Merkmal: laenge_mm = 631.0 mm; Anforderungen: REQ-P06; Belege: B-BAT-015
- **ENT-045** Separatorbreite LFP 87 mm. Merkmal: breite_mm = 87.0 mm; Anforderungen: REQ-P06; Belege: B-BAT-015
- **ENT-046** Separator LFP 12 µm. Merkmal: dicke_um = 12.0 µm; Anforderungen: REQ-P06; Belege: B-BAT-015
- **ENT-047** Separatorlagen LFP 78. Merkmal: lagen = 78.0 ; Anforderungen: REQ-P06; Belege: B-BAT-015
- **ENT-048** Separator LFP Z-gefaltet. Merkmal: bauweise = "ein Band, Z-gefaltet, Rand laminiert" ; Anforderungen: REQ-P06; Belege: B-BAT-015
- **ENT-049** Isolierrand Kathode LFP 6,5 mm. Merkmal: breite_mm = 6.5 mm; Anforderungen: REQ-P06; Belege: B-BAT-015
- **ENT-050** Stapelfixierung LFP. Merkmal: art = "Kunststoffschiene, Klebeband, transparenter Isolationsbeutel" ; Anforderungen: REQ-P06; Belege: B-BAT-015
- **ENT-051** Gehäusefolie LFP PET. Merkmal: werkstoff = "PET-Klebefolie" ; Anforderungen: REQ-P06; Belege: B-BAT-015
- **ENT-052** Füllöffnung LFP verschweißt. Merkmal: verschluss = "verschweißt, Gummistopfen" ; Anforderungen: REQ-P06; Belege: B-BAT-015
- **ENT-053** Innere Stromschiene LFP Al/Cu. Merkmal: werkstoff = "Al (Kathode) / Cu (Anode)" ; Anforderungen: REQ-P06; Belege: B-BAT-015
- **ENT-054** Fügeverfahren Fahnen LFP. Merkmal: fuegeverfahren = "Fahnen Ultraschall verdichtet, an Stromschiene laser-geschweißt" ; Anforderungen: REQ-P06; Belege: B-BAT-015
- **ENT-055** Polisolation LFP. Merkmal: art = "zweiteiliger Kunststoffhalter, Gummi-O-Ring" ; Anforderungen: REQ-P06; Belege: B-BAT-015
- **ENT-056** Ventil LFP seitlich. Merkmal: lage = "Stirnseite neben Kathodenpol (seitlich)" ; Anforderungen: REQ-P06; Belege: B-BAT-015
- **ENT-081** Kühlart Kühlplatte unten, für beide Varianten. Merkmal: kuehlart = "Kühlplatte unten" ; Anforderungen: REQ-P09; Belege: B-BAT-017
- **ENT-082** Querträger: Anzahl 3, quer zur Fahrtrichtung. Merkmal: anzahl = 3.0 ; Anforderungen: REQ-P07; Belege: W22, B-BAT-019
- **ENT-083** Querträger: Profilbreite 26 mm. Merkmal: breite_mm = 26.0 mm; Anforderungen: REQ-P07; Belege: W22
- **ENT-084** Querträger: Profilhöhe 54 mm. Merkmal: hoehe_mm = 54.0 mm; Anforderungen: REQ-P07; Belege: W22
- **ENT-085** Querträger: Wandstärke 2,5 mm. Merkmal: wandstaerke_mm = 2.5 mm; Anforderungen: REQ-P07; Belege: W22
- **ENT-086** Querträger: Aluminium-Strangpressprofil. Merkmal: werkstoff = "Al-Strangpressprofil" ; Anforderungen: REQ-P07; Belege: W22
- **ENT-087** Seitenrahmen: Breite 30 mm je Seite. Merkmal: breite_mm = 30.0 mm; Anforderungen: REQ-P07; Belege: B-BAT-019
- **ENT-088** Kühlart: Kühlplatte oben und unten. Merkmal: kuehlart = "Kühlplatte oben und unten" ; Anforderungen: REQ-P09; Belege: B-BAT-019
- **ENT-089** Kühlplatten: Anzahl 2. Merkmal: anzahl = 2.0 ; Anforderungen: REQ-P09; Belege: B-BAT-019
- **ENT-090** Kühlplatte: Dicke 8 mm. Merkmal: dicke_mm = 8.0 mm; Anforderungen: REQ-P07; Belege: B-BAT-019
- **ENT-091** Bauraumlänge 2030 mm. Merkmal: bauraum_laenge_mm = 2030.0 mm; Anforderungen: REQ-P07; Belege: B-BAT-019
- **ENT-096** Reihenverbinder Al 25 × 3 mm. Merkmal: breite_mm = 25.0 mm; Anforderungen: REQ-P05; Belege: B-BAT-020
- **ENT-097** Reihenverbinder Dicke 3 mm. Merkmal: dicke_mm = 3.0 mm; Anforderungen: REQ-P05; Belege: B-BAT-020
- **ENT-098** Reihenverbinder Werkstoff Al. Merkmal: werkstoff = "Al" ; Anforderungen: REQ-P05; Belege: B-BAT-020
- **ENT-100** HV-Hauptleitung LFP 50 mm² Cu. Merkmal: querschnitt_mm2 = 50.0 mm2; Anforderungen: REQ-P05; Belege: B-BAT-020
- **ENT-102** Bauraumlänge LFP 2030 mm. Merkmal: bauraum_laenge_mm = 2030.0 mm; Anforderungen: REQ-P07; Belege: B-BAT-020
- **ENT-104** Kühlplatte: Kanalbreite 4 mm. Merkmal: kanal_breite_mm = 4.0 mm; Anforderungen: REQ-P09; Belege: B-BAT-021
- **ENT-105** Kühlplatte: Kanalhöhe 5 mm. Merkmal: kanal_hoehe_mm = 5.0 mm; Anforderungen: REQ-P09; Belege: B-BAT-021
- **ENT-106** Kühlplatte: Werkstoff Al, gelötete Platte mit parallelen Kanälen quer. Merkmal: werkstoff = "Al, gelötet, parallele Kanäle quer, 1 Durchgang" ; Anforderungen: REQ-P09; Belege: B-BAT-021
- **ENT-107** Kühlmitteldurchfluss LFP 23 L/min beim Schnellladen. Merkmal: durchfluss_L_min = 23.0 L/min; Anforderungen: REQ-P09; Belege: B-BAT-021
- **ENT-109** Schaltbox auf dem Deckel vorne. Merkmal: einbauort = deckel_vorne ; Anforderungen: REQ-P13; Belege: B-BAT-024
- **ENT-110** Zentrales BMS mit Zellüberwachung. Merkmal: architektur = zentral_BMS_CMU_Daisy-Chain ; Anforderungen: REQ-P15; Belege: B-BAT-024
- **ENT-111** CMU 18 Kanäle. Merkmal: kanaele = 18.0 -; Anforderungen: REQ-P15; Belege: B-BAT-024
- **ENT-112** CMU-Anzahl LFP 14. Merkmal: anzahl = 14.0 -; Anforderungen: REQ-P15; Belege: B-BAT-024
- **ENT-114** Zellausgleich passiv. Merkmal: ausgleich = passiv ; Anforderungen: REQ-P15; Belege: B-BAT-024
- **ENT-115** Ausgleichsstrom 150 mA. Merkmal: ausgleichsstrom_mA = 150.0 mA; Anforderungen: REQ-P15; Belege: B-BAT-024
- **ENT-116** Temperaturfühler LFP 56. Merkmal: anzahl = 56.0 -; Anforderungen: REQ-P15; Belege: B-BAT-024
- **ENT-118** Strommessung Shunt plus Hall redundant. Merkmal: prinzip = Shunt_Hall_redundant ; Anforderungen: REQ-P15; Belege: B-BAT-024
- **ENT-119** Strommessbereich ±500 A. Merkmal: messbereich_A = 500.0 A; Anforderungen: REQ-P15; Belege: B-BAT-024
- **ENT-120** Isolationswächter Warnschwelle 400 kΩ. Merkmal: ansprechwert_kOhm = 400.0 kOhm; Anforderungen: REQ-P13; Belege: B-BAT-024
- **ENT-121** Messleitungen als flexible Leiterplatte. Merkmal: art = FPC ; Anforderungen: REQ-P15; Belege: B-BAT-024
- **ENT-123** Hauptschütze 250 A. Merkmal: nennstrom_A = 250.0 A; Anforderungen: REQ-P05; Belege: B-BAT-024
- **ENT-124** Hauptschütze 1000 V DC. Merkmal: nennspannung_V = 1000.0 V; Anforderungen: REQ-P03; Belege: B-BAT-024
- **ENT-125** Vorladewiderstand 100 Ω. Merkmal: widerstand_Ohm = 100.0 Ohm; Anforderungen: REQ-P03; Belege: B-BAT-024
- **ENT-126** Vorladezeit 300 ms. Merkmal: vorladezeit_ms = 300.0 ms; Anforderungen: REQ-P03; Belege: B-BAT-024
- **ENT-127** Hauptsicherung Pyro- plus Schmelzsicherung. Merkmal: art = Pyro_plus_Schmelzsicherung ; Anforderungen: REQ-P13; Belege: B-BAT-024
- **ENT-128** Hauptsicherung LFP 350 A. Merkmal: nennstrom_A = 350.0 A; Anforderungen: REQ-P13; Belege: B-BAT-024
- **ENT-130** Service-Trennstecker 250 A. Merkmal: nennstrom_A = 250.0 A; Anforderungen: REQ-P13; Belege: B-BAT-024
- **ENT-132** HV-Stecker Anzahl 2. Merkmal: anzahl = 2.0 -; Anforderungen: REQ-P13; Belege: B-BAT-024
- **ENT-133** HV-Stecker Antrieb/Laden 250 A. Merkmal: nennstrom_A = 250.0 A; Anforderungen: REQ-P13; Belege: B-BAT-024
- **ENT-134** NV-Stecker 26-polig. Merkmal: polzahl = 26.0 -; Anforderungen: REQ-P13; Belege: B-BAT-024
- **ENT-135** Heizung PTC im Kühlkreis. Merkmal: art = PTC_im_Kuehlkreis_Fahrzeug ; Anforderungen: REQ-P08; Belege: B-BAT-024
- **ENT-136** Heizleistung 5 kW. Merkmal: leistung_kW = 5.0 kW; Anforderungen: REQ-P08; Belege: B-BAT-024
- **ENT-137** Gas- und Drucksensor. Merkmal: prinzip = Druck_plus_H2_CO2 ; Anforderungen: REQ-P11; Belege: B-BAT-024
- **ENT-138** BMS-Hauptsteuergerät auf dem Deckel hinten, in der Schaltbox. Merkmal: einbauort = deckel_hinten ; Anforderungen: REQ-P15; Belege: B-BAT-024
- **ENT-139** BMS-Platine Länge 200 mm. Merkmal: laenge_mm = 200.0 mm; Anforderungen: REQ-P15; Belege: B-BAT-024
- **ENT-140** BMS-Platine Breite 150 mm. Merkmal: breite_mm = 150.0 mm; Anforderungen: REQ-P15; Belege: B-BAT-024
- **ENT-141** BMS-Platine Höhe 20 mm. Merkmal: hoehe_mm = 20.0 mm; Anforderungen: REQ-P15; Belege: B-BAT-024
- **ENT-142** HV-Leitung Biegeradius 5×D = 70 mm. Merkmal: biegeradius_min_mm = 70.0 mm; Anforderungen: REQ-P13; Belege: B-BAT-024
- **ENT-144** Schaltbox auf dem Deckel hinten, unter der Rücksitzbank. Merkmal: einbauort = deckel_hinten ; Anforderungen: REQ-P13; Belege: B-BAT-024
- **ENT-147** Bauraumlänge LFP 2050 mm. Merkmal: bauraum_laenge_mm = 2050.0 mm; Anforderungen: REQ-P07; Belege: B-BAT-024
- **ENT-148** Verschaltung LFP Schleife 2 Reihen: Plus und Minus hinten, Mitte vorn. Merkmal: verschaltung = schleife_2reihen ; Anforderungen: REQ-P02; Belege: B-BAT-024
- **ENT-149** Messleitung FPC Breite LFP 16 mm. Merkmal: breite_mm = 16.0 mm; Anforderungen: REQ-P02; Belege: B-BAT-024
- **ENT-150** Service-Trennbrücke LFP unter Servicedeckel. Merkmal: bauform = trennbruecke_servicedeckel_vorn ; Anforderungen: REQ-P13; Belege: B-BAT-024
- **ENT-151** Keine Knautschzone im Pack, Seitencrash über Schweller. Merkmal: crashkonzept = schweller_traegt_keine_knautschzone_im_pack ; Anforderungen: REQ-P14; Belege: B-BAT-030, B-BAT-031
- **ENT-152** Kühlplatte aus Blech 1/4/1 mm mit Mäander. Merkmal: dicke_mm = 6.0 mm; Anforderungen: REQ-P05, REQ-P09; Belege: B-BAT-033
- **ENT-153** Kühlplatte: Al-Blech 1 mm gelötet, Mäander 8 Bahnen längs. Merkmal: werkstoff = "Al-Blech 1 mm, gelötet, Mäander 8 Bahnen längs, Teilkanäle" ; Anforderungen: REQ-P05, REQ-P09; Belege: B-BAT-034
- **ENT-154** Kühlplatte: Wasserraum 4 mm. Merkmal: kanal_hoehe_mm = 4.0 mm; Anforderungen: REQ-P05, REQ-P09; Belege: B-BAT-034
- **ENT-155** Kühlplatte: Teilkanal 8 mm. Merkmal: kanal_breite_mm = 8.0 mm; Anforderungen: REQ-P05, REQ-P09; Belege: B-BAT-034
- **ENT-156** Kühlplatte: 8 Mäander-Bahnen. Merkmal: kanal_anzahl = 8.0 ; Anforderungen: REQ-P05, REQ-P09; Belege: B-BAT-034
- **ENT-157** Kühlmodul hinten am Pack. Merkmal: einbauort = hinten_am_pack ; Anforderungen: REQ-P05, REQ-P09; Belege: B-BAT-034
- **ENT-158** Kühlplatte optimieren: zwei parallele Mäander. Merkmal: kanalfuehrung = gruppiert_k2 ; Anforderungen: REQ-P05, REQ-P09; Belege: B-BAT-038, B-BAT-040, B-BAT-043, sim/kuehlung/k5_parallel/ergebnis_verteiler.json, sim/kuehlung/k3_gesamt/elmer_LFP_P0_V4/ergebnis.json
- **ENT-159** Kühlplatte: Verteilerrohr außen Ø 25 mm für zwei parallele Mäander. Merkmal: verteilerrohr_d_mm = 25.0 mm; Anforderungen: REQ-P09, REQ-P12; Belege: B-BAT-043, sim/kuehlung/k5_parallel/ergebnis_verteiler.json

Anforderungen:

| REQ-P01 | Anwendung / Fahrzeugklasse | Pkw, Fahrzeugmasse etwa 1500 kg, Anhaltswert (Autor 2026-11-16); Auslegung rechnet Fall A (mit Batterie) und Fall B (ohne Batterie) als Spanne | Autor | Muss | Vorgabe Autor |
| REQ-P02 | nutzbarer Energieinhalt | aus Reichweite 400 km (Vorgabe Autor 2026-11-16) × Verbrauch (Annahme), Vergleich sim/chemie/vergleich_lfp_nmc | Autor | Muss | Reichweite: Vorgabe Autor |
| REQ-P03 | Systemspannung (Nenn, min, max) | 800 V nominal (ENT-006, Autor 2026-11-16); min/max folgen aus Zellfenster | Autor | Muss | teilweise |
| REQ-P07 | Bauraum (L × B × H) und Masse | L = 1950 mm (ENT-013, Autor 2026-11-17); B = 1430 mm (ENT-030, Autor 2026-11-17); H 130 mm Annahme; Masse offen (30 % Gesamtmasse als Annahme) | Autor | Muss | teilweise |

## Gestaltungsentscheidungen der KI (Darstellung, keine Auslegung)

- Obere Pad-Lage (BT-230 oben) erscheint erst mit der Struktur (Szene 5) und hebt in Szene 6 ab, sonst verdeckt sie den Zellblock.
- Obere Kühlplattenhälfte (BT-610 oben) und Schaltboxdeckel (BT-710 eloxiert) erscheinen erst in der Explosion.
- Stahl-Befestigungsmaterial BT-590 ist ausgeblendet (verdeckt Innenteile).
- Szene 1 beginnt mit einer einzelnen Zelle (aus dem gemeinsamen BT-100-Netz abgetrennt: erste Zelle in x, erste von zwei in y), danach erscheint der Rest.
- Ergebnisbilder (Kühlung V4p, Crash X3) werden nicht eingeblendet; die Ergebnisse stehen in den Berichten der Akten (sim/kuehlung/k3_gesamt, sim/mechanik/x3_crash_g5).

## Wissensgraph im Hintergrund und Schluss (nur Variante „Batterie und Wissensgraph“)

- Der Graph zeigt alle Notizen des Obsidian-Tresors `wissen/` ohne `_bilder`: **622 Knoten** und **2847 Kanten** (jeder `[[…]]`-Link in Text und Kopf). Quelle der Zahlen: `/home/cae/cae_projekte/batterie_video/wissen/graph/datenquellen.json`.
- Er ist **nachgebaut, nicht aus Obsidian aufgenommen**: Die Zeitrafferfunktion von Obsidian ordnet nach dem Erstellungszeitpunkt der Datei, `wissen/` wird aber bei jedem Lauf neu erzeugt, alle Dateien hätten denselben Zeitpunkt. Deshalb ordnet ein Skript (`video/graph_zeitraffer.py`) die Knoten nach dem **echten Projektdatum** aus den Quellen.
- Datumsquellen (Knoten je Quelle): über Nachbar 145, git direkt 189, B-BAT 38, B-BAT (git blame) 11, ENT 162, über Nachbar (Kette) 3, W 74. Entscheidungen: Datum der Akte; Befunde: Überschrift in `BEFUNDE.md` (sonst `git blame`); Recherchen: Datum der Ergebnisdatei; alle anderen: das frühere von Erst-Commit in git und dem frühesten Quelldatum der direkt verlinkten Nachbarn (Bauteil und Anforderung bekommen so das Datum ihrer ersten Akte).
- Ehrlicher Hinweis: Das Repo ist erst seit 2026-11-18 in git. 33.3 % der Knoten tragen das Datum 2026-11-18, git direkt allein 23.8 %. Die Verteilung über die Zeit im Video läuft nach Rang (Datum, dann ID), nicht nach Kalendertagen, damit der Graph gleichmäßig wächst.
- Der Graph wächst vom ersten Bild bis zum Ende der Explosion/Rückführung (Bild 2680) auf 100 %. Danach folgen 16 s: 6 s wird das Gehäuse (BT-5xx und die oberen Abdeckungen BT-610 oben und BT-230 oben) durchsichtig (Alpha 1 auf 0,15), 5 s blenden alle Teile aus, 5 s zeigen nur den Graphen. Darstellungsentscheidung der KI, keine Auslegung.
- Der Graph ist eine Darstellung der Ordnung der Akten, kein Rechenergebnis.

---
KI-generiert (Claude Sonnet). Entwurf, nicht freigegeben. Bildtext im Video nur: Thomas Schmiegelt.
