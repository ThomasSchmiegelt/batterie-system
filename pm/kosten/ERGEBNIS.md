| Dok.-Nr. | BAT-ERG-KO | Version | 0.2 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Ergebnis Kosten KO2 und Stückliste SL3.1 | Ersteller | Claude Sonnet (KI) | Prüfer | Opus (offen) |

> **KI-generiert** (Claude Sonnet, 2026-11-19), Entwurf, nicht geprüft. Erwartung: `pm/kosten/ERWARTUNG.md` Nachtrag 2 (ERW-KO2). Zahlen aus `pm/kosten/ergebnis_LFP.json` und `ergebnis_NMC.json`.

## KO2 (Punkt für Punkt gegen ERW-KO2)

| ERW-KO2 | Ergebnis | Urteil |
|---|---|---|
| 1 Status in 3 Stufen | je Position `preis_status`, `preis_stufe`; Summe je Stufe in `eur_je_stufe` | erfüllt |
| 2 f_serie 0,35; EKC14-40 9,04 €, NTC 0,13 € | `pm/kosten/eingaben.json` `f_serie` 0,35, `eur_je.BT-713.teile` (Sicherung 9,04), `eur_je.BT-330` 0,13; Arcol HS50 nicht verwendet | erfüllt |
| 3 BT-713 = 44,04 € | eingaben.json `eur_je.BT-713.wert`, Teile Pyro 35 (Schätzung) + Sicherung 9,04 (abgeleitet) | erfüllt |
| 4 BT-610 12 €/kg × echte Masse | LFP 46,59 kg = 559 €, NMC 44,70 kg = 536 € (Quelle `sim/kuehlung/k2_kuehlplatte/ergebnis_k2b.json`, längs, 8 Bahnen, Teilkanal 8 mm) | erfüllt |
| 5 Kühlkreis BT-661…665 = 188 € | 60 + 70 + 35 + 15 + 8 = 188 € je Variante (Positionen 660.1…660.5); BT-660 entfällt | erfüllt |
| 6 Mengen/Normteile | BT-350/570/750/780 je 1, BT-630/640 je 2, BT-560 12 × 1,50 €, BT-580 4 €/Stück, BT-590 je Art, BT-450 6 €/kg, BT-240 entfällt | erfüllt |
| 7 BT-360/430 nach Länge | €/m nur für Position 300.6 bzw. 400.3; 360.3 (0 €) und 360.4 (3 €/Stück) nach Opus-Nachtrag | erfüllt |

**Erwartung gegen Ergebnis (Stand nach Opus-Nachtrag 2026-11-19, Deutung KO2 in ERWARTUNG.md):**

| | LFP | NMC |
|---|---|---|
| Erwartung | 6.250 € / 85 €/kWh | 8.600 € / 116 €/kWh |
| Ergebnis | 6.588 € / 89,1 €/kWh (5,4 %) | 8.753 € / 117,9 €/kWh (1,8 %) |
| Band ±8 % | 5.750–6.750 €: im Band | 7.912–9.288 €: im Band |
| verifiziert + abgeleitet an der Summe (< 1 %) | 0,25 % (erfüllt) | 0,18 % (erfüllt) |
| offene Positionen | 4 | 3 (alle mit Grund ausgewiesen) |

**Verlauf:** Erster Lauf LFP 6 793 € (+8,7 %, verfehlt) wegen der Mica-Zwischenlage BT-220 (249 €, Opus-Fehler). Nach der Korrektur (Schaum_Zwischenlage 300 kg/m³, 6 €/kg, 4,45 kg = 26,7 €) liegen beide Varianten im Band (LFP Opus-Erwartung nachher ≈ 6 570 €, Ergebnis 6.588 €).

**Nachtrag Opus 2026-11-19 umgesetzt:**
- (a) BT-220 LFP: Werkstoff Schaum_Zwischenlage (`cad/baukasten/farben.json`), Preis 6 €/kg Schätzung.
- (b) 360.3 FPC-Detail im FPC-Preis enthalten (Eintrag `BT-360:Detail`, 0 €/Stück, Status Schätzung); 360.4 Daisy-Kette 3 €/Stück (`BT-360:Daisy`, Schätzung, 11/12 Stück). Damit sind beide nicht mehr offen.
- (c) `stueckliste_v3.py` lädt `cad/baukasten/annahmen_g5.json` nach den A-Blöcken (spätere Quelle überschreibt, wie `kern.py`); Schütz-/Vorlademasse mit masse_quelle „Datenblatt (annahmen_g5.json)“. Die Gleichheitsprüfung gegen die e2d-CAD-Gruppen ist dafür zu einem Vermerk geworden (`pruefsummen.abweichung_gegen_e2d_gruppen`: Schaltbox-Inhalt +0,96 kg, das e2d-CAD zieht nach).
- (d) Typen eingetragen: Isolationswächter Bender iso1685, HV-Stecker TE HVP 800 / HVA 280, NV-Stecker TE AMPSEAL, Ventil Pierburg 3/2-Wege, Schlauch EPDM DN19 (Gates 4175EC). Chiller und Behälter ohne Typ.

**Offen / Fragen an Opus:**
1. Hauptschütz: `A_e2_schuetz_masse_kg` = 0,8 kg gilt in CAD und Stückliste je Gerät, bei Menge 2 ergibt das 1,6 kg. Datenblatt GLFX250 nennt ca. 0,4 kg je Schütz (zusammen 0,8 kg). Falls „0,8 kg“ die Gesamtmasse meint, muss der Wert 0,4 sein.
2. Offene Positionen: LFP 200.1, 400.1, 600.2, 600.5; NMC 200.1, 600.2, 600.5 (BT-210 Anordnung ohne Masse, BT-410 LFP, BT-620 Masse, BT-650 Volumen). BT-210 Vorschlag: als „entfällt“ führen.
3. Stücklistenmasse jetzt LFP 630,17 kg (Band 615–630 aus cad/baukasten/ERWARTUNG.md: knapp darüber), NMC 488,42 kg (Band 470–486: darüber); Ursachen Kühlkreis, K2b-Plattenmasse, Datenblattmassen.
4. Datenblätter fehlen für Isolationswächter, NV-Stecker, Schlauch (Autorliste); Chiller und Behälter ohne Typ.
5. Frühere Zwischenstände der Kostenrechnung zählten die FPC-Länge dreifach; jetzt nur Position 300.6.
6. Massen BT-510…550, 620, 630 sind bis zur Gesamtmontage die e2d-Obergrenzen; `--aus-cad` geht erst, wenn `cad/baukasten/ausgabe/ergebnis_<V>.json` kein G5_NUR mehr trägt (Teillauf).

## SL3.1 Stückliste
- Neue Felder je Position: `hersteller_typ`, `datenblatt` (Datei, Seite), `masse_datenblatt_kg`, `preis` {wert, einheit, status, herkunft}. Datenquelle `pm/bauteile/kaufteile_datenblatt.json` (aus `forschung/datenblaetter.md`), Preis aus `pm/kosten/eingaben.json` über `pm/kosten/preisregeln.py`.
- BT-610: Blech 1/4/1 mit Mäander, Masse K2b, Quelle „K2b (bis G5-CAD)“; Kühlkreis 660.1…660.5 mit Massen aus `cad/baukasten/annahmen_g5.json` (Schläuche „G5-CAD (folgt)“).
- Dokumente neu: `docs/13_stueckliste_LFP.md`, `docs/13_stueckliste_NMC.md`, `docs/13_stueckliste.md`, `docs/18_kosten.md`. Nebenwirkung: `stueckliste_v3.py` schreibt wie bisher `cad/baukasten/annahmen.json` neu (Inhalt unverändert).

## Neulauf nach der Gesamtmontage
`python3 pm/bauteile/stueckliste_v3.py --aus-cad && python3 pm/kosten/kosten.py && python3 pm/kosten/bilder.py && python3 pm/kosten/doku.py`

## Bilder
`pm/kosten/kosten_LFP.png`, `kosten_NMC.png`, `kosten_vergleich.png` (Zielband ERW-KO2 ±8 % beschriftet, Lesehilfe im Bild, angesehen: Balken, Band und Beleg lesbar, LFP-Balken liegt am oberen Rand des Bands). Folienbaustein: `praesentation/bausteine/KO2.md`.

*KI-generiert (Claude Sonnet, 2026-11-19), Entwurf. Nicht freigegeben.*
