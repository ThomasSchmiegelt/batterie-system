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
