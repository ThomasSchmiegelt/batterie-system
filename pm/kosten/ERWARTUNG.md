| Dok.-Nr. | ERW-KO1 | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Erwartung und Annahmen Kostenbewertung (REQ-P16) | Ersteller | Claude Opus (KI) | Prüfer | – |

> KI-generiert (Opus, 2026-11-18), vor der Rechnung. Autor: „auch eine Kostenbewertung vornehmen“.
**Belege:** Nur W29 liefert Preise, alle von BNEF 2024 als Packpreis gesamt:
- BEV 97 USD/kWh: „Prices for battery electric vehicles (BEVs) came in at $97/kWh“
- China 94 USD/kWh
- Ausblick −3 USD/kWh für 2025
Zellpreise, die Aufteilung LFP/NMC und Bauteilpreise sind **nicht belegt**: IEA 403, batterydesign 404. Alles unten sind **Annahmen Opus** (Herkunft „ERW-KO1“), Größenordnung Serie 2025/26, Großserie ≥ 100 000 Packs/Jahr, Herstellkosten ohne Gemeinkosten und Marge. Kurs 1 USD = 0,92 EUR (Annahme).

| BT | Annahme | Einheit |
|---|---|---|
| BT-100 Zelle | LFP 50, NMC (4680) 75 | €/kWh |
| BT-210/240 Reihe, Verspannung | Stahl 3, Al-Profil 6 | €/kg (Masse aus Stückliste) |
| BT-220 Zwischenlage / BT-230 Wärmeleitmaterial | 6 / 20 | €/kg |
| BT-250 Zellhalter (NMC) / BT-260 Verguss (NMC) | Kunststoff 6 / 10 | €/kg |
| BT-310 BMS / BT-320 CMU / BT-330 NTC | 120 / 15 / 0,5 | €/Stück |
| BT-340 Strommessung / BT-350 Isolationswächter | 40 / 20 | €/Stück |
| BT-360 FPC / BT-361 Halter | 8 €/m / 0,3 €/Stück | |
| BT-410/420/440 Verbinder, Laschen | Al 8, Cu 14 (verarbeitet) | €/kg |
| BT-430 HV-Leitung | 25 | €/m |
| BT-510/520/530/540 Wanne, Deckel, Träger, Rahmen | Al verarbeitet 6 (Strangpress/Blech), Druckguss 5 | €/kg |
| BT-550 Unterfahrschutz | Stahl 3, Al 6 | €/kg |
| BT-560 Befestigung / BT-570 Druckausgleich | 0,5 €/Schraube / 5 €/Stück | |
| BT-610/620 Kühlplatte, Verteiler | Al gelötet 12 | €/kg |
| BT-630 Anschluss / BT-640 Fühler / BT-650 Kühlmittel | 10 €/Stück / 3 €/Stück / 3 €/L | |
| BT-660 Schnittstelle, BT-760 Heizung (PTC im Fahrzeug) | 0 (Fahrzeug) | |
| BT-710 Schaltbox-Gehäuse + Stromschienen | Al 8, Cu 14 | €/kg |
| BT-711 Schütz / BT-712 Vorladung / BT-713 Pyro + Schmelz | 45 / 25 / 35 + 20 | €/Stück |
| BT-720 Trennung | LFP Brücke + Deckel (BT-721/722) 15, NMC Stecker 40 | €/Stück |
| BT-730 HV-Stecker 250 A / 40 A / BT-740 NV | 60 / 20 / 15 | €/Stück |
| BT-750 Entgasung / BT-770 Gassensor / BT-780 Kennzeichnung | 8 / 25 / 2 | €/Stück |
| Fertigung | Montage + Prüfung: 10 % auf die Material- und Kaufteilsumme, dazu 50 € Endprüfung je Pack | |

**Erwartung:**
- Pack LFP 5 500–7 000 € (75–95 €/kWh). Pack NMC 7 000–9 000 € (95–120 €/kWh).
- Zellanteil 65–80 %, Gehäuse und Struktur 8–15 %, Elektronik und Schaltbox 4–8 %, Kühlung 2–5 %.
- Abgleich mit dem Beleg 97 USD/kWh ≈ 89 €/kWh: LFP darunter oder ungefähr gleich, NMC darüber.
- Empfindlichkeit: Ein Zellpreis ±20 % ändert den Packpreis um ±13–16 %.

**Verfehlt:**
- Zellanteil < 60 % oder > 85 %.
- Eine Nicht-Zell-Position > 10 % des Packs.
- Eine Position ohne Masse oder Menge, die so durchrutscht. Sie muss als „offen“ ausgewiesen werden.

## Nachtrag 1 (Opus, 2026-11-18, nach Lauf 1)
**Deutung:** Der Lauf ist nachgerechnet (Zellen 3 696 € von 6 465 €, also 57,2 %). Der Verfehlt-Fall hat zwei Gründe, und beide liegen bei mir, nicht beim Pack:
- (a) Die Fertigung mit 10 % auf die Zellen ist falsch. Montagekosten hängen nicht am Zellpreis.
- (b) Die Kühlplatte ist mit Vollmaterial-Masse gerechnet, real ist sie hohl.
**Korrektur (Annahmen):**
- Fertigung: 10 % auf die Nicht-Zell-Summe, dazu 50 €/Pack.
- Kühlplatte BT-610: Masse × 0,6 (Kanalanteil ≈ 40 %), bis K2 eine Hohlmasse liefert.
**Erwartung neu:** LFP ≈ 5 800 € (≈ 79 €/kWh, Zellanteil ≈ 63 %). NMC ≈ 7 900 € (≈ 106 €/kWh, Zellanteil ≈ 70 %).
Die Auslegungen in docs/18 bestätige ich:
- BT-721 und BT-722 zusammen 15 €.
- BT-713 und BT-730 als Satz.
**Offene Positionen** (17/14): Sie bleiben als untere Schranke ausgewiesen und gelten nicht als Abbruch. Neu gerechnet wird nach der Stückliste zu E2 v1.1. Längen für BT-360/430 aus `ergebnis_<V>_e2.json`, Kühlmittelvolumen offen bis K2.

## Nachtrag 2 = ERW-KO2 (Opus, 2026-11-19, vor dem Lauf): Stückliste SL3.1, Datenblätter, Blech-Kühlplatte, Kühlkreis
Autor 2026-11-19: „pass bitte auch die stückliste an und die Preisgestaltung“.
**Preisregeln (Opus):**
1. Status je Preis eine von drei Stufen: „verifiziert (Wxx/Datenblatt)“, „abgeleitet aus Distributorpreis“, „Schätzung (Annahme Opus)“.
2. Distributorpreis (Menge 1) ist kein Serienpreis. Serie = Distributorpreis × f_serie, **f_serie = 0,35** (Annahme Opus, Schätzung für ≥ 50 000 Packs/Jahr), Status „abgeleitet aus Distributorpreis“. Belegt sind: EKC14-40 25,84 € → 9,04 €; NTCS0603 0,37 € → 0,13 €. Arcol HS50 (5,64 £) wird nicht verwendet, weil Datenblatt und Preis nicht zum gewählten Typ (Vishay RH050) gehören.
3. BT-713 Satz = Pyro 35 (Schätzung) + Schmelzsicherung 9,04 (abgeleitet) = 44,04 €.
4. BT-610 Kühlplatte: 12 €/kg × **echte CAD-Masse** (Blech 1/4/1, ENT-152…156). Der Faktor 0,6 aus Nachtrag 1 entfällt, weil die Masse jetzt hohl gerechnet ist.
5. Kühlkreis außen (ENT-157, jetzt im Lieferumfang des Packs, BT-660 = 0 entfällt), Serienschätzung Opus: Pumpe BT-661 60 €, Chiller BT-662 70 €, Ventil BT-663 35 €, Schläuche + T-Stück BT-664 15 €/Satz, Ausgleichsbehälter BT-665 8 €.
6. Neue/geklärte Mengen: BT-350 1, BT-570 1, BT-630 2, BT-640 2, BT-750 1, BT-780 1 (SL3). BT-560 Befestigung 1,50 €/Stück (Hülse + M10). BT-580 Dichtungen 4 €/Stück (Mittel aus Deckel- und Kleindichtungen). BT-590: Schraube 0,10, Kabelschuh 1,50, Clip 0,10, Schrumpfschlauch 0,20 €/Stück. BT-450 Berührschutz 6 €/kg. BT-240 entfällt (keine Verspannung).
7. HV-Leitung BT-430 und FPC BT-360 nach Länge aus der Geometrie (€/m), sobald G5.7 die Längen liefert, sonst offen.
**Erwartung KO2:** LFP ≈ 6 250 € ≈ 85 €/kWh (KO1 80; + Kühlplatte ≈ +225 €, + Kühlkreis 188 €, + Normteile/Dichtungen ≈ +40 €, Sicherung −11 €). NMC ≈ 8 600 € ≈ 116 €/kWh (KO1 110, gleiche Zuschläge). Anteil „verifiziert/abgeleitet“ an der Summe < 1 % (Zellpreis bleibt Schätzung). Verfehlt, wenn eine Variante außerhalb ± 8 % liegt oder eine Position ohne Menge/Masse nicht als „offen“ ausgewiesen wird.
**Deutung KO2 (Opus, nach dem Lauf):** LFP 6 793 € (+8,7 %) verfehlt. Die Ursache ist ein Fehler von Opus in G5.1b: Ich hatte die Zwischenlage BT-220 als 1 mm Mica-Vollmaterial festgelegt. Das ergibt 242 × 0,17 kg = 41,5 kg und 249 €. Real ist das ein komprimierbares Schaumpad zum Quellausgleich. Korrektur: Werkstoff Schaum_Zwischenlage 300 kg/m³ (≈ 4,5 kg), 6 €/kg (Schätzung) → LFP ≈ 6 570 € ≈ 89 €/kWh, im Band. Weitere Entscheidungen: FPC-Detail 360.3 ist im FPC-Preis enthalten (0 €). Daisy-Kette 360.4 kostet 3 €/Stück (Schätzung). Datenblattmassen gelten für Hauptschütz 0,8 kg und Vorladeschütz + Widerstand 0,41 kg (annahmen_g5.json, damit CAD und Stückliste gleich rechnen).
