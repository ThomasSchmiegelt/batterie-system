| Dok.-Nr. | ERW-X1b | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Erwartung X1b (Knautschzone im Pack, CalculiX) und X2 (dynamisch, OpenCourant) | Ersteller | Claude Opus (KI) | Prüfer | – |

> KI-generiert (Opus, 2026-11-18), vor der Rechnung. Autor auf die Frage Knautschzone ja/nein: „ja mach das, kannst du das auch hiemit OpenCourant rechnen“. Grundlage X1 (B-BAT-030): ohne Knautschzone Zellberührung bei ≈ 30 kN / 20 J.

## Annahmen Opus (Herkunft „ERW-X1b“)
| Größe | Wert |
|---|---|
| Knautschprofil außen am Seitenrahmen | Al 6082 T6 wie X1, Breite w, Höhe wie Rahmen, Wände 2 mm, 2 Kammern (1 Mittelsteg); Innenwand und Zellabstand unverändert wie X1 |
| Varianten | w = 15, 20, 30 mm je Seite |
| Ziel | Zellberührung erst bei ≥ 100 kN (Restkraft-Annahme X1) und Energie bis Zellberührung ≥ 2 kJ |
| Breite fest 1430 mm | Die Knautschzone geht von der Zellbreite ab. LFP: 8 mm Reserve, Rest kürzt die Zelle (2 Zellen quer). NMC: Reihen fallen weg, wenn der Platz nicht mehr reicht. Energieverlust in % je w aus dem CAD bzw. der Geometrie rechnen, nicht schätzen |
| X2 Aufprall | Pfahl Ø 254, starr, Masse 1500 kg (MDB-Masse W17 als Stellvertreter), Geschwindigkeit so, dass die Energie gleich der **Restenergie hinter dem Schweller von 5 kJ** ist (Annahme: ≈ 10 % von ½·1500·(32 km/h)² ≈ 59 kJ) → v ≈ 2,6 m/s. Dehnrate vernachlässigt (6082 ist kaum ratenabhängig) |

## Erwartung
- **X1b quasistatisch:** Mittlere Stauchkraft des Profils 60–120 kN.
  - Energie bis Zellberührung: w 15 → 1,0–1,8 kJ, w 20 → 1,5–2,5 kJ, w 30 → 2,5–4 kJ.
  - Ziel ≥ 100 kN und ≥ 2 kJ erreicht ab w ≈ 20 mm.
  - Energieverlust ≈ 1,5–2,5 % (w 20) bzw. 3–4 % (w 30).
- **X2 dynamisch, mit dem gewählten w:** Kraftspitzen 1,2–1,5 × quasistatisch durch Trägheit. Eindringung bei 5 kJ kleiner als w, also keine Zellberührung, wenn X1b ≥ 2 kJ bei ≈ 0,8 w liefert. Energiebilanz: Fehler < 5 %, Hourglass-Energie < 10 %.
- Abgleich: X2 und X1b weichen bei gleicher Eindringung um höchstens 30 % in der Kraft ab.

## Verfehlt
- Auch bei w 30 unter 2 kJ.
- Energieverlust > 5 %.
- X2: Energiebilanz > 5 %, Hourglass > 10 % oder Abbruch.
- OpenCourant nicht lauffähig oder Lizenz unklar.

## Nachtrag 1 (Opus, 2026-11-18 18:05): Methodenwechsel
**Befund:** Alle fünf CalculiX-Läufe brachen bei 13–33 % des Pfahlwegs ab, wegen Kontakt- bzw. Residuumsdivergenz. Selbstkontakt war abgeschaltet, weil er nicht konvergierte. Dünnwandige Profile, die sich falten, sind für einen impliziten Löser der schwierigste Fall. `auswerten.py` bricht an fehlenden Schlüsseln ab. Opus hat die Läufe gestoppt.
**Entscheidung (Methodenwahl Opus):** X1b und X2 werden zusammengelegt und **explizit mit OpenCourant** gerechnet, mit Selbstkontakt der Faltwände.
- Lastfall: Pfahl Ø 254, 1500 kg, 5 kJ (v ≈ 2,6 m/s), LF1 zwischen den Querträgern.
- Varianten: LFP w 15/20/30, NMC w 20.
- Kriterium: keine Zellberührung (Innenwand-Verschiebung < Spalt) bei aufgenommenen 5 kJ. Dazu Spitzenkraft und Energiebilanz.
- CalculiX bleibt Gegenprüfung der Anfangssteifigkeit: Kraft bei 2 mm, bis 30 % Abweichung erlaubt.
**Erwartung unverändert:** Ab w ≈ 20 mm werden 5 kJ ohne Zellberührung aufgenommen.

## Anforderung (Nachtrag)
- REQ-P14 (Vorgang X2, pm/plan/wissensnetz.py)

Vermerk: Nachtrag Sonnet aus wissensnetz.py, Prüfung Opus offen (2026-11-23). Die Zuordnung Rechenordner zu Vorgang X2 ist von Sonnet gewählt.
