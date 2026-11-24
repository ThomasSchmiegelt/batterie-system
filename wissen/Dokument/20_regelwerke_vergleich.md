---
typ: dokument
nr: "BAT-DOC-20"
version: "0.1"
status: "Entwurf"
tags: ["dokument"]
---
# BAT-DOC-20 – Regelwerke im Vergleich: Prüffälle nach EU/UN, USA und China

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

- Datei: `docs/20_regelwerke_vergleich`
- Version: 0.1
- Status: Entwurf
- Typ: Projektdokument (Dokumentenlenkung [[Dokument/00_dokumentenlenkung]])

## Genannte Anforderungen (Textvorkommen)
- [[Anforderung/REQ-G01|REQ-G01]]
- [[Anforderung/REQ-G02|REQ-G02]]
- [[Anforderung/REQ-P03|REQ-P03]]
- [[Anforderung/REQ-P08|REQ-P08]]
- [[Anforderung/REQ-P10|REQ-P10]]
- [[Anforderung/REQ-P11|REQ-P11]]
- [[Anforderung/REQ-P13|REQ-P13]]
- [[Anforderung/REQ-P14|REQ-P14]]

## Genannte Entscheidungen, Befunde, Bauteile (Textvorkommen)
- –

## Vorgänge, die dieses Dokument nennen
- –

## Inhalt (Kopie aus `docs/20_regelwerke_vergleich.md`)

| Dok.-Nr. | BAT-DOC-20 | Version | 0.1 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Regelwerke im Vergleich: Prüffälle nach EU/UN, USA und China | Ersteller | Claude Sonnet (KI), Auftrag Opus | Prüfer | – (Mensch offen) |

> **KI-generiert.** Entwurf, nicht vom Menschen freigegeben. Testprojekt „KI im Engineering“, kein Produkt. Keine rechtliche Bewertung.
> **Zielmarkt (Autor, Freigaberunde 2026-11-24): nur Europa.** Maßgebend sind EU/UN. Die Spalten USA und China dienen nur dem Vergleich.

Erzeugt am 2026-11-23 nach `forschung/AUFTRAG_REGELWERKE_2.md`.

## Lesehilfe
- Eine Zelle enthält nur einen Wert, dessen Zitat die automatische Prüfung bestanden hat (`pruefe.py`), mit Kennung des Themas (Wxx, Ergebnis in `forschung/ergebnis/Wxx.md`, Prüfung in `Wxx.pruefung.txt`). Alles andere steht als **nicht belegt**. Nichts ist aus dem Gedächtnis ergänzt.
- „nicht belegt“ heißt: Das Ergebnis des Themas nennt keinen geprüften Wert. Es heißt nicht, dass die Regel keinen Wert enthält. Die Annexe von R100 wurden mit den Teilthemen W35b–W35e nachgeholt (Auszug über Suchbegriffe, daher nicht vollständig). Die Beschleunigungstabelle von Annex 9B fehlt im Auszug.
- Nicht übernommen, weil die Zitatprüfung fehlschlug oder der Wert nicht im Zitat steht: W35 „5,0 l“ (Tippfehler in der URL), W40 „0,2 Ω Barriere→Barriere“ und Seitencrash „54 km/h“, W41 „1 : 5 Mio.“, W35d „−40 °C“ (Zitat fehlgeschlagen).
- Spalte „UN-Text laut W36“: W36 enthält Texte aus R94/R95/R135, ordnet die einzelnen Zahlen aber nicht je Regelung zu. Die Zuordnung steht dort nicht und wird hier nicht erfunden.
- Die Spalten USA DoD und China sind fast leer. Gründe: W42 liefert nur Ausgabedaten von MIL-STD-810/461 (kein Prüfwert, MIL-PRF-32565 nicht abgerufen). W38 liefert nur Normnummer und Titel von GB/T 31467-2023; GB 38031 ist nicht abgerufen.

## Vergleich
| Prüffall | EU/UN (R100, R94/95/135, 2023/1542) | USA zivil (FMVSS 305/305a) | USA DoD (MIL) | China (GB 38031, GB/T 31467) | betroffene REQ |
|---|---|---|---|---|---|
| Schwingung | W35c/W35d: sinusförmig, logarithmischer Sweep 7 Hz bis 50 Hz und zurück in 15 min, 12 Wiederholungen, 3 h gesamt, in Montage-Hochrichtung, danach 1 h Beobachtung; Beschleunigungstabelle: Zahlen fehlen im Auszug | nicht belegt | nicht belegt (W42: nur MIL-STD-810 Ausgabedaten, kein Wert) | nicht belegt | REQ-P14 |
| mechanischer Stoß | nicht belegt (W35e nennt keinen Stoßwert) | nicht belegt | nicht belegt | nicht belegt | REQ-P14 |
| Quetschung | W35b: Kraft mindestens 100 kN, höchstens 105 kN (außer nach Absatz 6.4.2 abweichend); Einsetzzeit unter 3 min; Haltezeit mindestens 100 ms, höchstens 10 s (Zitat in 42021X2190 bestätigt, in der Fassung 42024X1955 nicht gefunden) | nicht belegt | nicht belegt | nicht belegt | REQ-P14 |
| Pfahl / Seitenaufprall | W36: Front 56 ± 1 km/h; Seite (Barriere) 50 ± 1 km/h; Pfahl 32 ± 1 km/h, Winkel 75° ± 3°, Pfahl-Ø 254 ± 6 mm, Beschleunigung ≤ 1,5 m/s²; W35: Lagebezug 300 mm im hinteren Montagebereich (Bedeutung nicht geprüft) | W40: Front bis einschließlich 48 km/h; Heck bis einschließlich 80 km/h; Seite: Zahl nicht im Zitat | nicht belegt | nicht belegt | REQ-P14 |
| Feuer | W35d: mittlere Flammentemperatur 800 °C innerhalb von 30 s erreicht, Beflammung 2 min; W35e: Prüfung nötig bei brennbarem Elektrolyt; W35: entfällt, wenn das REESS mehr als 1,5 m über dem Boden liegt | W40: 305a schützt vor „fire, explosion, and gas venting“ (nur Schutzumfang, kein Wert) | nicht belegt | nicht belegt | REQ-P11 |
| externer Kurzschluss | nicht belegt (W35e liefert keinen Wert) | nicht belegt | nicht belegt | nicht belegt | REQ-P11, REQ-P14 |
| Überladung | W35e: Prüfende, wenn die REESS-Temperatur 10 °C über der maximalen Betriebstemperatur liegt; Betrieb ohne Überladeschutz endet 12 h nach Ladebeginn; Stabilisierung bei Temperaturgradient unter 2 °C je Stunde | nicht belegt | nicht belegt | nicht belegt | REQ-P11 |
| Tiefentladung | W35e: Entladung auf 25 % der Nennspannung; Stabilisierung bei Temperaturgradient unter 4 °C je 2 h | nicht belegt | nicht belegt | nicht belegt | REQ-P11 |
| Übertemperatur | W35d: Temperaturzyklus Hochlage 60 ± 2 °C (Tieflage −40 °C: Zitat fehlgeschlagen, nicht übernommen); W35e: Grenze 10 °C über der maximalen Betriebstemperatur (Überladeprüfung) | nicht belegt | nicht belegt | nicht belegt | REQ-P08, REQ-P11 |
| thermische Ausbreitung / Warnung | W35d: Warnung 5 min vor einer gefährlichen Situation im Fahrgastraum (Zitat: „5 minutes prior to the presence of a hazardous situation inside the passenger compartment“) | W40b: Warnung muss innerhalb von 3 min nach Beginn des thermischen Ereignisses aktivieren; Signal mindestens 5 min aktiv; W40: Definition „sequential occurrence of thermal runaway within a REESS“ | nicht belegt | nicht belegt | REQ-P11 |
| Isolation | W35/W36: ≥ 100 Ω/V (DC-Bus), ≥ 500 Ω/V (AC-Bus); Hochspannung ab > 60 V DC bzw. > 30 V AC; nach Aufprall ≤ 30 VAC bzw. 60 VDC oder Energie < 2,0 J; Kontaktwiderstand < 0,1 Ω | W40: ≥ 100 Ω/V (DC), ≥ 500 Ω/V (AC); Restspannung ≤ 30 VAC bzw. 60 VDC; Barriere→Chassis < 0,1 Ω; Geltung ab > 60 VDC bzw. 30 VAC | nicht belegt | nicht belegt | REQ-P13, REQ-P03 |
| Elektrolytaustritt | W36: ≤ 7 % des Elektrolyten (offene Traktionsbatterie zusätzlich max. 5,0 l); Messzeit 30 min nach Aufprall; W35: nach außen ≤ 7 Vol.-%, im Fahrgastraum kein Austritt | W40: max. 5,0 l Elektrolyt; keine sichtbare Spur im Fahrgastraum | nicht belegt | nicht belegt | REQ-P14 |
| Wasser / Eintauchen | W35: 24 h Pause vor erneuter Isolationsprüfung; W35e: Isolation nach Wasser nach Annex 7A | W40b: Waschtest Düse 6,3 mm, 11,9–13,2 l/min, 30–35 kPa, Abstand 3,0–3,2 m, 60–75 s je m²; Watbecken 10–15 cm tief, 500 m, 20–24 km/h; Isolationsprüfung frühestens 24 h danach | nicht belegt | nicht belegt | REQ-P13 |
| Kennzeichnung / Batteriepass | W37b (2023/1542, 13/0): Batteriepass und QR-Code ab 18.02.2027; Industriebatterie ab > 2 kWh; Entsorgungssymbol mindestens 3 % der größten Seite, höchstens 5 × 5 cm; Kennzeichnung Cd über 0,002 %, Pb über 0,004 %; Ersatzteilverfügbarkeit mindestens 5 Jahre; Entnehmbarkeit ohne Spezialwerkzeug (Artikelbezug und Geltung für EV-Batterien: Opus prüfen); W37: EV-Batterie Informationspflicht zu Leistung und Haltbarkeit | nicht belegt | nicht belegt | nicht belegt | REQ-G02, REQ-P10 |

## Ergänzend (kein Regelwerk, offene Berichte, W41)
USABC/NREL-Berichte (nur Hinweis, kein Prüfwert für das Lastenheft): Abuse-Tests bei 100 % SOC und 10–30 °C Umgebung; Nageldurchmesser 3 mm im Durchstoßtest; Thermal-Ramp auf Pack-Ebene nicht empfohlen. W41 hat 6 Belege bestätigt, 1 Fehler.

## Prüfstand der Quellen
| Thema | Inhalt | Belege bestätigt / Fehler | Fundstelle |
|---|---|---|---|
| W35 | UN R100 (EU-Codifizierung CELEX 42021X2190, 42024X1955) | 9 / 1 | `forschung/ergebnis/W35.pruefung.txt` |
| W36 | UN R94/R95/R135 | 20 / 0 | `forschung/ergebnis/W36.pruefung.txt` |
| W37 | 2023/1542, 2023/1230, 2024/1689 (nur Erwägungsgründe; 2024/1689 ohne Werte) | 8 / 0 | `forschung/ergebnis/W37.pruefung.txt` |
| W38 | GB/T 31467-2023 (nur Titel) | 3 / 0 | `forschung/ergebnis/W38.pruefung.txt` |
| W40 | FMVSS 305 und 305a (eCFR), neu gerechnet 2026-11-23 | 14 / 1 | `forschung/ergebnis/W40.pruefung.txt` |
| W41 | USABC/NREL-Berichte, neu gerechnet 2026-11-23 | 6 / 1 | `forschung/ergebnis/W41.pruefung.txt` |
| W35b | R100 Annex 9D Quetschung | 6 / 1 | `forschung/ergebnis/W35b.pruefung.txt` |
| W35c | R100 Annex 9B Schwingung | 8 / 0 | `forschung/ergebnis/W35c.pruefung.txt` |
| W35d | R100 Warnung, Ausbreitung, Temperatur, Feuer | 13 / 1 | `forschung/ergebnis/W35d.pruefung.txt` |
| W35e | R100 Überladung, Tiefentladung, Feuer, Wasser | 7 / 0 | `forschung/ergebnis/W35e.pruefung.txt` |
| W37b | 2023/1542 Kennzeichnung, Batteriepass, Entnehmbarkeit | 13 / 0 | `forschung/ergebnis/W37b.pruefung.txt` |
| W37c | 2023/1230 Art. 2 Ausnahmen (PI ohne Beleg; Nachtrag Sonnet) | 1 / 0 (Nachtrag) | `forschung/ergebnis/W37c.nachtrag.pruefung.txt` |
| W40b | FMVSS 305a Warnung, Wasch- und Watetest | 13 / 0 | `forschung/ergebnis/W40b.pruefung.txt` |
| W42 | MIL-STD-810/461 (Wikipedia, nur Ausgabedaten) | 6 / 1 | `forschung/ergebnis/W42.pruefung.txt` |

## Offene Punkte für Opus (keine Deutung hier)
- REQ-G01 (Maschinenverordnung): PI-Ergebnis W37c enthält keinen Beleg. Ersatzweise ist in `forschung/ergebnis/W37c.nachtrag.md` ein von Sonnet gewähltes Zitat zu Art. 2 Abs. 2 Buchst. g (Kraftfahrzeuge im Geltungsbereich 2018/858 ausgenommen, außer montierte Maschinen) maschinell geprüft (1/0). Ob das für das Pack gilt, entscheidet Opus.
- Offen sind nur noch: Beschleunigungstabelle Annex 9B, Werte für Stoß, externen Kurzschluss, Warnzeit-Zusammenhang R100 (5 min) gegenüber FMVSS 305a (3 min, Opus deuten), GTR 20, DoD, GB 38031.
- Ob die W36-Zahlen R94, R95 oder R135 zuzuordnen sind, ist offen.

---
*KI-generiert (Claude Sonnet, 2026-11-23). Status Entwurf. Freigabe nur durch den Autor.*

