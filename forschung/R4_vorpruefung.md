| Dok.-Nr. | R4-V-E (Ergebnis zu Auftrag R4-V) | Version | 0.1 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | R4 Vorprüfung der PI-Recherche gegen die Rohtexte | Ersteller | Claude Sonnet (KI) | Prüfer | Opus (offen) |

> **KI-generiert.** Entwurf, nicht geprüft, nicht vom Menschen freigegeben. Vorarbeit für R4 (REQ-D01), erstellt von Sonnet nach `forschung/AUFTRAG_R4_VORPRUEFUNG.md`. Keine Deutung, keine Bewertung, ob ein Wert „richtig“ ist.

Bearbeitet: alle 27 Themen (W01–W17, T01–T09, P01). Beginn 15:19 (`date`), Ende siehe Fußzeile. Kein Netz, kein PI, keine GPU, nichts in `ergebnis/`, `pakete/` geändert.
Methode: Skripte (Python, nur Textsuche, in der Sitzungs-Ablage) lesen `ergebnis/<Nr>.pruefung.txt`, `ergebnis/<Nr>.md` und `pakete/<Nr>.md`. Zeilennummern „Zxx“ sind die Zeilen in `ergebnis/<Nr>.md`. Rohtextzitate sind auf ≤ 200 Zeichen gekürzt; „|“ im Original steht für Infobox-Spalten.
Kennzeichen **→ OPUS** = Rückgabe an Opus laut Auftrag.

## Überblick der Beanstandungen von `pruefe.py` (alle 27 Themen)
Summe: 22 Zeilen „FEHLT im Text der Quelle“, 14 Zeilen „WERT OHNE BELEG“ (Quelle: `ergebnis/*.pruefung.txt`). Zusätzlich in den `.pruefung.txt`: W06 „LINK NIE ABGERUFEN: https://en.wikipedia.org/wiki/Electric_vehicle_battery,“ (der Link steht mit Komma am Ende, Pfad `ergebnis/W06.pruefung.txt`); W05 „0 Belege bestaetigt, 0 Fehler“ (alle Kennwerte „nicht gefunden“, `ergebnis/W05.md`).

## 1. FEHLT-Zeilen gegen den Rohtext (A/B/C)

Ergebnis: **A = 21, B = 0, C = 1.** Kein B-Fall, daher kein B-Fall an Opus. Ein C-Fall.

| Nr | Zeile | Zitat (gekürzt) | Klasse | Begründung |
|---|---|---|---|---|
| T04 | Z8 | GNU General Public License GPL-3.0 | A | Rohtext: Infobox „License … GPL-3.0“, Link-Text „GNU General Public License“ dort als Wikitext getrennt |
| T07 | Z7 | „Ein: Eingabe–Ausgabe-Daten eines teuren Simulators (verstreut im Designraum) …“ | **C** | Kein Quellzitat, sondern eine deutsche Zusammenfassung des Modells (Zelle SMT, Spalte „Ein/Aus“). Keine Zahl. „Eingabe–Ausgabe-Verhalten“ und „Designraum“ stehen im Rohtext, „verstreut“ (scattered) nicht (Suche „scatter“: 0 Treffer). Siehe Fundstelle unten. |
| W01 | Z15 | specific energy of CATL's LFP battery is claimed to be 205 watt-hours per kilogr… | A | Satz steht im Rohtext, nur ein Link-Einschub zwischen „kilogram“ und „(Wh/kg)“ |
| W01 | Z16 | Volumetric energy density = 227–396 W⋅h/L (820–1,430 kJ/L) | A | Infobox-Zeile, Schreibweise „Energy density“ vs. „Volumetric energy density =“ |
| W02 | Z12 | Specific energy density 100 to 250 W·h/kg (360 to 900 kJ/kg) | A | Infobox, Links zwischen den Einheiten |
| W02 | Z13 | Volumetric energy density 250 to 680 W·h/L | A | Infobox, Link nach „L“ |
| W02 | Z14 | Specific power density 1 to 10,000 W/kg | A | Steht nur im eingebetteten Wikitext der Infobox (`"data3":{"wt":"1 to 10,000&nbsp;W/kg…`), nicht als gerenderter Text |
| W02 | Z16 | Cycle durability 400–1,200 cycles | A | Infobox „Cycle durability \| 400–1,200 cycles“ |
| W02 | Z24 | Specialty: up to 450 W h/kg (1,600 kJ/kg) | A | Rohtext mit „W⋅h/kg“ (Sonderzeichen statt Leerzeichen) |
| W07 | Z11 | Nominal cell voltage \| 3.0–3.1 V | A | Infobox, „\|“ im Zitat maskiert |
| W07 | Z12 | Energy density \| 250–375 W·h/L | A | Infobox, Link nach „L“ |
| W09 | Z13 | Cycle durability 400–1,200 cycles [ 11 ] | A | Infobox, Link zwischen Wort und Wert |
| W09 | Z23 | Standard: 250–842 W.h/L | A | Nur im Wikitext der Infobox (`Standard: {{cvt\|250\|–\|842`), nicht gerendert im Paket W09 |
| W09 | Z24 | Specialty: up to 450 W.h/kg | A | Nur im Wikitext (`Specialty: up to {{cvt\|450\|W.h/kg\|kJ/kg}}`), nicht gerendert im Paket W09 |
| W10 | Z21 | Specific energy \| 60–110 Wh /kg | A | Infobox, Link nach „Wh“ |
| W10 | Z22 | a lower specific energy (about 30–110 Wh/kg) | A | Rohtext identisch, Link-Einschub vor „/kg“ |
| W10 | Z23 | Energy density \| 177–202 Wh /L | A | Infobox, Link nach „Wh“ |
| W10 | Z25 | a lower inherent voltage (2.4 V) | A | Rohtext: „their lower inherent voltage (2.4 V)“, nur „a“ statt „their“ |
| W11 | Z14 | Charge temperature interval -20 °C 〜 105 °C | A | Infobox identisch, Trennzeichen 〜 |
| W11 | Z15 | Self-discharge rate 6%ｰ85 °C (month) | A | Infobox identisch (Sonderzeichen ｰ) |
| W13 | Z10 | are typically composed of copper brass or aluminium | A | Rohtext mit Komma und Links: „copper, brass or aluminium“ |
| W14 | Z19 | maximum_voltage : 16V DC | A | Steht nur als Wikitext-Schlüssel (`"maximum_voltage":{"wt":"16V DC"}`) |

Fundstellen im Rohtext (`pakete/<Nr>.md`, ≤ 200 Zeichen):
- T04: `License [https://en.wikipedia.org/wiki/Software_license] | GPL-3.0 [https://en.wikipedia.org/wiki/GNU_General_Public_License]`
- T07 (C), nächste Rohtextstelle: `…relying solely on the input-output behavior. A model is constructed based on modeling the response of the simulator to a limited numbe…` und `…the number and location of samples … in the design space.`
- W01 Z15: `…CATL's LFP battery is claimed to be 205 watt-hours per kilogram [https://en.wikipedia.org/wiki/Watt-hours_per_kilogram] (Wh/kg) on the cell level.`
- W01 Z16: `Volumetric energy density [...] = ... 227–396 W⋅h/L (820–1,430 kJ/L) [ 1 ] [ 2 ]`
- W02 Z12: `Specific energy density | 100 to 250 W·h [https://en.wikipedia.org/wiki/Watt-hour]/kg (360 to 900 kJ [...]/kg)`
- W02 Z13: `Volumetric energy density | 250 to 680 W·h/L [https://en.wikipedia.org/…`
- W02 Z14: `"label3":{"wt":"Specific power density"},"data3":{"wt":"1 to 10,000&nbsp;W/kg<ref name=\"mw\">…`
- W02 Z16: `Cycle durability | 400–1,200 cycles [https://en.wikipedia.org/wiki/Battery_cycle] [ 11 ]`
- W02 Z24: `Specialty: up to 450 W⋅h/kg (1,600 kJ/kg) [ 3 ]`
- W07 Z11: `Nominal cell voltage | 3.0–3.1 V | [https://en.wikipedia.org/wiki/File:Sindelfingen_…`
- W07 Z12: `Energy density [https://en.wikipedia.org/wiki/Energy_density] | 250–375 W·h/L [https://en.wikipedia.org/wiki/Litre]`
- W09 Z13: `Cycle durability | 400–1,200 cycles [https://en.wikipedia.org/wiki/Battery_cycle] [ 11 ]`
- W09 Z23: `"EtoS":{"wt":"Standard: {{cvt|250|–|842<!-- Calculation: 14.26/(((1.82/2)^2*3.14159*6.51)/1000)-->|W.h/L|J/cm3}}…`
- W09 Z24: `<br />Specialty: up to {{cvt|450|W.h/kg|kJ/kg}}<ref name=\"Amprius2024ProductPortfolio\">…`
- W10 Z21: `Specific energy | 60–110 Wh [https://en.wikipedia.org/wiki/Kilowatt-hour]/kg`
- W10 Z22: `…which leads to a lower specific energy [...] (about 30–110 Wh/kg [ 1 ] ) than conventional lithium-ion battery technol…`
- W10 Z23: `Energy density | 177–202 Wh [https://en.wikipedia.org/wiki/Kilowatt-hour]/L`
- W10 Z25: `…disadvantage of lithium-titanate batteries is their lower inherent voltage (2.4 V), which leads to a lower specific energy…`
- W11 Z14: `Charge temperature interval | -20 °C 〜 105 °C |`
- W11 Z15: `Self-discharge rate | 6%ｰ85 °C (month) [ 1 ] |`
- W13 Z10: `…are typically composed of copper [https://en.wikipedia.org/wiki/Copper], brass [https://en.wikipedia.org/wiki/Brass] or aluminium [...] as solid or hollow tubes.`
- W14 Z19: `"electrical":{"wt":"Differential"},"maximum_voltage":{"wt":"16V DC"},"maximum_current":{"wt":""}`

Zusatzbefund aus der Gegenprüfung (kein FEHLT, `pruefe.py` meldet ihn nicht) **→ OPUS**:
- **W06 Z22** `| Energiedichte LFP (aktuell) | 150 – 220 (bzw. 210) | Wh/kg* |`: Im Rohtext `pakete/W06.md` steht die Tabelle mit Spaltenkopf `| Li-NMC | LFP | Li-NCA | Sodium-ion | Lead-acid |`. Spalte **Li-NMC**: „150-275 kWh [ 9 ] / 150-220 kWh [ 10 ] / 165 kWh (sales avg 2023)“. Spalte **LFP**: „80-150 kWh [ 9 ] / 210 [ 11 ] / 90-160 kWh [ 10 ] / 135 kWh (sales avg 2023)“. Die Zeile W06 Z22 übernimmt „150-220“ (Wert aus der NMC-Spalte) als LFP. Die Einheit im Rohtext ist „kWh“, die Zeile schreibt „Wh/kg*“. Der Prüfer sieht das nicht, weil „150-220 kWh“ im Text steht.

## 2. WERT OHNE BELEG (14 Zeilen)
Prüfregel: Zahl steht in einer belegten Kennwertzeile (Tabellenzeile mit „Beleg:“) desselben Themas? Dann „aus Zeile Zxx“, sonst „frei“. Die Zeilen sind überwiegend Folgerungen oder Offene Fragen, keine Kennwerte.

| Nr | Zeile | Art | Zahlen in der Zeile | Vermerk |
|---|---|---|---|---|
| W01 | Z36 | Folgerung Kühlung | 0 °C, −20 °C, 23 °C; 66 %, 33 % | Temperaturen 0, −20, 23 °C: aus Z24 (Zitat „23, 0, -10, and -20 °C … 141.8, 92.7, 57.9 and 46.7 mAh/g“). 66 % und 33 %: **frei** (siehe Abschnitt 3, selbst gerechnet) |
| W01 | Z43 | Offene Frage | −10 °C, +45 °C | −10 °C: aus Z24. +45 °C: **frei** (in `pakete/W01.md` keine „45 °C“) |
| W02 | Z29 | Folgerung Fertigung | Tautpunkt < −50 °C; < 100 ppm H₂O | −50 °C: aus Z21; 100 ppm: aus Z20 |
| W02 | Z30 | Folgerung Kühlung | 5–45 °C | aus Z19 |
| W02 | Z44 | Widerspruchsvermerk | 0,35–2,5 %/Monat; 1,5–2 %/Monat; 8 %/Monat bei 21 °C; 1999 | 0,35–2,5: aus Z15. 1,5–2, 8 %, 21 °C, 1999: **frei** (keine Tabellenzeile), stehen aber im Paket: „typically stated by manufacturers to be 1.5–2% per month“ und „In 1999, self-discharge per month was measured at 8% at 21 °C, 15% at 40 °C, 31% at 60 °C.“ (`pakete/W02.md`) |
| W03 | Z42 | Folgerung Sicherheit | Nadeltest 30–60 °C | aus Z32 |
| W07 | Z33 | Offene Frage | −30 °C | aus Z16 |
| W10 | Z41 | Folgerung Kühlung | ≥ 300 °C | aus Z14 |
| W11 | Z28 | Folgerung Kühlung | 20–30 %; > 60 °C | 20–30 %: aus Z17; > 60 °C: aus Z20 |
| W11 | Z34 | Offene Frage | 10 000–100 000 Zyklen; −20…+105 °C | −20…+105 °C: aus Z14. 10 000–100 000 Zyklen: **frei** als Tabellenzeile, im Paket als Infobox-Wikitext `"CD":{"wt":"{{nowrap\|10,000-100,000 [[Battery cycle\|cycles]]}}` (`pakete/W11.md`) |
| W12 | Z38 | Offene Frage | < 0 °C, > 45 °C | **frei** (in `pakete/W12.md` keine „45 °C“; 5–45 °C steht in W02 Z19, anderes Thema) |
| W16 | Z24 | Folgerung Zelle | +20…+30 °C | aus Z11 |
| W16 | Z33 | Offene Frage | 0,5–1,7 K/W | **frei** (keine Tabellenzeile). Im Paket: „contact between the device case and heat sink may have a thermal resistance between 0.5 and 1.7 °C/W“ (`pakete/W16.md`, Gehäuse–Kühlkörper bei Halbleitern, nicht Zelle) |
| W16 | Z34 | Offene Frage | 0 °C | **frei** (Schwelle der Frage, keine Quellzahl) |

## 3. Selbst gerechnete oder umgeformte Werte in den Kennwerttabellen
Suche: Zahlen in Spalte „Wert“, die im zugehörigen Beleg-Zitat nicht wörtlich stehen (Skript), dann je Fall im Paket nachgesehen.

**3a. Umgerechnet, in Zahlen gesetzt oder zusammengefasst (Wert weicht vom Wortlaut ab):**

| Nr | Zeile | Wert in Tabelle | Rohtext / Beleg | Art |
|---|---|---|---|---|
| W01 | Z36 (Folgerung) | „≈ 66 %“ bei 0 °C, „≈ 33 %“ bei −20 °C | Rohtext nur mAh/g: 141.8 (23 °C), 92.7 (0 °C), 46.7 (−20 °C). Quotient 92.7/141.8 = 0.6537, 46.7/141.8 = 0.3293 (Python, nur zur Nachprüfung) | Quotient, nicht im Text. 0.6537 entspricht ≈ 65 %, nicht 66 % |
| W06 | Z17 | „90 % nach ca. 6,5 a“ | „after six years and six months of service“ | Wort → Dezimalzahl |
| W06 | Z21 | „≤ 0,5 C (50 % Kapazität/h)“ | „charging rates not exceeding half of the capacity of the battery“ | Umdeutung „half of the capacity“ → 0,5 C und „/h“ |
| W03 | Z28 | „9 min“ | „reaching 10% to 97% state of charge in nine minutes“ | Wort → Zahl |
| W09 | Z18 | „≈ 0 – 6 V“ | „possible range of roughly zero to 6 volts“ | Wort → Zahl |
| W13 | Z12 | „bis 10⁵ (Hundertausende)“ | „can momentarily reach hundreds of thousands of amperes“ | Zehnerpotenz aus Wortangabe; „bis 10⁵“ ist eine Obergrenze, der Text sagt „hundreds of thousands“ |
| W13 | Z9 | „10 (bis bis zu 50 mm Ø Rohr)“ | Zitat nennt nur „as little as 10 square millimetres“; im Paket „metal tubes 50 millimetres (2.0 in) in diameter or more as busbars“ | Aus „50 mm oder mehr“ wird „bis zu 50 mm“ |
| W16 | Z20 | „3×“ | „Copper is three times as dense …“ | Wort → Zahl |
| W06 | Z22 | „150 – 220 (bzw. 210) Wh/kg*“ | Beleg-Zitat „150-220 kWh“ / „210“ | Einheit geändert; Spaltenzuordnung siehe Abschnitt 1 Zusatzbefund **→ OPUS** |

**3b. Zahl steht im Paket, aber nicht im Beleg-Zitat der Zeile (Zitat zu kurz oder von anderer Stelle):**

| Nr | Zeile | Zahl | Fundstelle im Paket |
|---|---|---|---|
| W01 | Z15 | 180 (von 180–205) | `Next gen: 180–205 Wh/kg [ 3 ]` |
| W02 | Z11 | 3,85 V | Infobox `Nominal cell voltage | 3.6 / 3.7 / 3.8 / 3.85 V`; Zitat nennt nur „3.6 or 3.7 V“ |
| W09 | Z11 | 3,85 V | wie W02 Z11 |
| W02 | Z18 | 372 mAh/g | `…1339 coulombs per gram (372 mAh/g)`; Zitat vor der Klammer abgeschnitten |
| W06 | Z14 | 40–45 % Kathode | `cathodes alone accounting for 40–45% of this material cost`, anderer Satz als das Zitat |
| W08 | Z17 | 3 V (CR123A) | Paketzeile: `3 (lithium) 3.6 (Li-ion)` in Nachbarspalte; das Beleg-Zitat „1,500 (lithium) 700 (Li–ion rechargeable)“ ist die Spalte davor (Kapazität) und stützt die Zahl nicht |
| W08 | Z18 | 17 mm (CR123A) | Paketzeile: `H: 34.5 mm Ø: 17 mm`; Beleg-Zitat „A lithium primary battery, not interchangeable with zinc types“ nennt keine Zahl |
| W10 | Z20 | NMC111, 532 | im Paket `NMC111`, `NMC532`; Zitat nennt nur 622 und 811 |
| W10 | Z28 | 6 000 | Infobox `Cycle durability | 6000–+45 000 cycles`; Zitat nennt nur 45,000 |
| W11 | Z18 | 3 min | `charged from 10% to 80% in 3 minutes`, Zitat vorher abgeschnitten |
| W13 | Z13 | 75, 90, 105 °C | `60, 75, and 90 °C` und `In the United States, 105 °C is allowed with ambient of 40 °C`; Zitat endet bei „60“ |
| W13 | Z14 | 50 A (Bündel) | `has an ampacity of 50 A when the ambient air is 30 °C`; anderer Satz als das Zitat |
| W15 | Z16 | 230 USD/kWh | `to around $230/kWh for BEV200 vehicles`; Zitat endet bei „$545/kWh“ |

Weitere Auffälligkeiten (keine Berechnung, nur Hinweis): W13 Z18, W13 Z19 und W06 Z23 haben keine oder eine abweichend geformte URL am Zeilenende (W06 Z23: „Referenz [17]“ in der Klammer). Die Zitate stehen im Paket (W13: „…open in one second“ / „…blow in 0.1 seconds“).

## 4. Widersprüche und Mehrfachwerte zwischen Themen
Quelle für Werte: `ergebnis/<Nr>.md` Zeile Zxx; Beleg-URL steht in dieser Zeile. Kürzel: WP = Wikipedia.

| Größe | Thema/Zeile | Wert | Beleg-URL |
|---|---|---|---|
| Energiedichte LFP Zelle (Wh/kg) | W01 Z14 | 95–172 | WP Lithium_iron_phosphate_battery |
| | W01 Z15 | 180–205 (CATL 2024) | WP Lithium_iron_phosphate_battery |
| | W03 Z16 / Z17 / Z18 | 190–210 (BYD Long Blade 2.0) / 192 (Geely Aegis) / 185 (SVOLT) | WP Blade_battery |
| | W07 Z14 | 185 (LFP als Vergleichswert) | WP Sodium-ion_battery |
| | W06 Z22 | 150–220 bzw. 210, Zuordnung fraglich (siehe Abschnitt 1 Zusatzbefund); Rohtext-LFP-Spalte 80–150 / 210 / 90–160 / 135 | WP Electric_vehicle_battery |
| | W01 Paket (Fließtext, keine Tabellenzeile) | „BYD's LFP battery specific energy is 150 Wh/kg“ | WP Lithium_iron_phosphate_battery |
| Energiedichte LFP Zelle (Wh/L) | W01 Z16 | 227–396 (Wikitext-Kommentar: Berechnung für Rundzelle 18650/32140, Lithium Werks) | WP Lithium_iron_phosphate_battery |
| Energiedichte NMC / Li-Ion Zelle (Wh/kg) | W02 Z12 | 100–250 (Li-Ion allgemein) | WP Lithium-ion_battery |
| | W02 Z24 / W09 Z24 | bis 450 (Spezialzelle, Si-Anode) | WP Lithium-ion_battery |
| | W01 Z30 (Folgerung; Quelle im Paket) | NMC > 300 („best NMC … over 300“) | WP Lithium_iron_phosphate_battery |
| | W06 Paket, Spalte Li-NMC (keine Tabellenzeile) | 150–275 / 150–220 / 165 (Verkaufsmittel 2023), Einheit „kWh“ im Rohtext | WP Electric_vehicle_battery |
| Energiedichte Li-Ion (Wh/L) | W02 Z13 | 250–680 | WP Lithium-ion_battery |
| | W09 Z23 | 250–842 (gleiche Seite, Wikitext) | WP Lithium-ion_battery |
| | W08 Z9 | 250–670 (LiPo) | WP Lithium_polymer_battery |
| Energiedichte Pack (Wh/kg, Wh/L) | – | keine Zeile in irgendeinem Thema | – |
| Zellspannung LFP | W01 Z11 / W08 Z13 / W09 Z12 | 3,2 V | WP LFP_battery / List_of_battery_sizes / Lithium-ion_battery |
| | W01 Z21 | ~3,3 V (Arbeitsspannung); im Paket außerdem „Working voltage = 3.0 ~ 3.3 V“, Modul 3,25 V | WP Lithium_iron_phosphate |
| Zellspannung NMC / Li-Ion | W10 Z13 | 3,6–3,7 V | WP NMC |
| | W02 Z11 / W09 Z11 | 3,6–3,85 V (Zitat: „3.6 or 3.7 V“) | WP Lithium-ion_battery |
| | W06 Z12 / W15 Z13 | 3–4 V | WP Electric_vehicle_battery |
| | W10 Z33 | 3,7 V (Li-Ion-Referenz) | WP Lithium_titanate_battery |
| Zellspannung LTO | W10 Z24 vs. Z25 | 2,3 V vs. 2,4 V (selbe Seite) | WP Lithium_titanate_battery |
| Zellspannung SIB | W07 Z11 | 3,0–3,1 V | WP Sodium-ion_battery |
| Zyklenzahl LFP | W01 Z17 | 2 500–9 000 | WP LFP_battery |
| | W08 Z14 | 2000+ | WP List_of_battery_sizes |
| | W03 Z22 / Z23 | > 3 500 (Geely Aegis) / > 5 000 (SVOLT) | WP Blade_battery |
| Zyklenzahl Li-Ion allgemein | W02 Z16 / W09 Z13 | 400–1 200 | WP Lithium-ion_battery |
| Zyklenzahl LTO / SIB | W10 Z28 / W10 Z34 / W07 Z15 | 6 000–45 000+ / ~1 000 bei 55 °C / > 10 000 | WP Lithium_titanate_battery / WP Sodium-ion_battery |
| EOL-Kriterium | W06 Z16 | 80 % (Zitat: „capability at 80% DOD is less than 80% of rated“) | WP Electric_vehicle_battery |
| | W15 Z15 | 80 % der Anfangskapazität | WP Electric_vehicle_battery |
| | W14 Z13 | ~70–80 % SoH | WP State_of_health |
| | W10 Z34 | 80 % (LTO-Zyklentest) | WP Lithium_titanate_battery |
| Temperaturfenster | W02 Z19 | 5–45 °C (Laden, empfohlen) | WP Lithium-ion_battery |
| | W16 Z11 | +20 bis +30 °C (nominal) | WP Battery_thermal_management |
| | W03 Z27 | −43…60 °C (SVOLT Offroad) | WP Blade_battery |
| | W11 Z14 / Z20 | −20…+105 °C Laden / > 60 °C Betrieb (Festkörper) | WP Solid-state_battery |
| | W13 Z13 | Leiteroberfläche 60 / 75 / 90 (US 105) °C | WP Ampacity |
| Ladeleistung | W06 Z18 | 30–80 kW (typisch Schnellladen) | WP Electric_vehicle_battery |
| | W12 Z13 | bis 500 kW (CCS) | WP Combined_Charging_System |
| | W12 Z17 | bis 220 kW bei 500 A | WP Combined_Charging_System |
| | W12 Z14 / Z15 | 1000 V und 500 A (Grenzwerte; Z17 nennt dazu „220 kW bei 500 A“, Z13 „500 kW“; Zusammenhang nicht ausgewertet) | WP Combined_Charging_System |
| | W12 Z18 / Z19 | 125 A bei 850 V (IEC 62196-3, 2014) | WP Combined_Charging_System |
| Laderate / Ladezeit | W03 Z19 / Z20 / Z28 | 2,45 C, 17 min (10→80 %) / 6 C, 8,5 min / 9 min (10→97 %) | WP Blade_battery |
| | W06 Z21 | ≤ 0,5 C (Alterungsempfehlung) | WP Electric_vehicle_battery |
| | W11 Z18 | 10→80 % in 3 min (Prototyp) | WP Solid-state_battery |
| Zellmaße | W03 Z11 / Z12 / Z13 | 960 × 90 × 13,5 mm (BYD Long Blade Gen. 1) | WP Blade_battery |
| | W03 Z14 / Z15 | 580 mm (Geely Aegis „Short Blade“) / ≈ 450–580 mm (BYD Short Blade 2.0) | WP Blade_battery |
| | W08 Z15 / Z16 | 18650: 65 mm / 68 mm mit Schutzschaltung | WP List_of_battery_sizes |
| Selbstentladung (Nebengröße) | W02 Z15; W08 Z10; W11 Z15 | 0,35–2,5 %/Monat; ≈ 5 %/Monat (LiPo); 6 %/Monat (Festkörper); W02 Z44: 1,5–2 und 8 % (1999) im selben Thema | WP Lithium-ion_battery / Lithium_polymer_battery / Solid-state_battery |
| Zellpreis / Packpreis (Nebengröße) | W01 Z23 / W06 Z23 / W02 Z17 / W15 Z16 | ~100 USD/kWh Zelle 2023 / < 100 (LFP-Zelle 2023) / 108 Pack (Ende 2025) / 545 → 230 Pack (PHEV → BEV) | WP LFP_battery / Electric_vehicle_battery / Lithium-ion_battery |

→ **OPUS:** Jeder Eintrag dieser Tabelle betrifft eine Auslegungsgröße (Energiedichte, Spannung, Zyklen, EOL, Temperatur, Ladeleistung, Zellmaße). Die Tabelle wertet nicht, ob zwei Werte denselben Bezug haben (Zelle/Pack, Gen. 1/2.0, Normal-/Kaltbetrieb).

## 5. Lücken für die Auslegung
Suche: `ergebnis/*.md` (Tabellen und Text) und `pakete/*.md` (Rohtext, Stichwörter: Ah, Ω, coolant, A/mm, maximum temperature, ΔT).

| Größe | Ergebnis | Fundstelle / Anmerkung |
|---|---|---|
| Max. Zelltemperatur (Hersteller) | **keine Quelle** | `ergebnis/W04.md` Z15 „Maximale zulässige Zelltemperatur (Hersteller) \| nicht gefunden“. Nur Nachbarwerte: NMC O₂-Freisetzung 300 °C (W10 Z14), SVOLT-Betrieb bis 60 °C (W03 Z27), Festkörper > 60 °C (W11 Z20), Ofentest 300 °C (W03 Z33) |
| Temperaturspreizung zwischen Zellen | **keine Quelle** | nur qualitativ: „radialer Temperaturgradient“ (W02 Z30, ohne Zahl); `pakete/W16.md`: ΔT nur für Kühlkörper-Geometrien |
| Zellinnenwiderstand | **keine Quelle** | nur qualitativ in den Paketen (W03: „lower internal resistance“, W02 „internal resistance … may increase“ bei Kälte); keine mΩ-Angabe in `pakete/*.md` |
| Wh/L einer LFP-Zelle | **belegt**, mit Einschränkung: W01 Z16 (227–396 Wh/L) | gilt laut Wikitext-Kommentar für Rundzellen 18650/32140 (Lithium Werks), nicht für Blade |
| Wh/L eines LFP-Packs | **keine Quelle** | |
| Kapazität (Ah) einer Blade-Zelle | **keine Quelle** | In `pakete/W03.md` kein „Ah“. Treffer in W01-Paket (700 Ah / 1400 Ah, stationäre Module), W07 (SIB), W10 (LTO) betreffen andere Zellen. Pack-kWh Blade: W03 Z24–Z26 (8,3–21,5; 91,4; 95,7 kWh) |
| Masse einer Blade-Zelle | **keine Quelle** | In `pakete/W03.md` keine kg-Angabe |
| Zellverbinder-Querschnitt | **teilweise**: W13 Z9 „10 mm² (Mindestmaß Schiene)“, allgemein, nicht Zellverbinder | Beleg: WP Busbar |
| Stromdichte (A/mm²) im Zellverbinder | **keine Quelle** | Nur Kabel-Ampacity 70 A / 50 A (W13 Z14) und Skin-Effekt > 8 mm (W13 Z11); „A/mm“ im Paket nicht gefunden |
| Zulässige Kühlmitteltemperatur | **keine Quelle** | `pakete/W16.md` nennt „coolant“ ohne Temperaturwert |

→ **OPUS:** alle „keine Quelle“-Zeilen sind Auslegungsgrößen (Annahme oder neue Recherche nötig; hier keine Annahme gesetzt).

## 6. Zählung A/B/C je Thema (FEHLT-Zeilen)
Themen ohne FEHLT-Zeile: je A = 0, B = 0, C = 0.

| Thema | A | B | C | | Thema | A | B | C |
|---|---|---|---|---|---|---|---|---|
| W01 | 2 | 0 | 0 | | T04 | 1 | 0 | 0 |
| W02 | 5 | 0 | 0 | | T07 | 0 | 0 | 1 |
| W07 | 2 | 0 | 0 | | W09 | 3 | 0 | 0 |
| W10 | 4 | 0 | 0 | | W11 | 2 | 0 | 0 |
| W13 | 1 | 0 | 0 | | W14 | 1 | 0 | 0 |
| W03, W04, W05, W06, W08, W12, W15, W16, W17, T01–T03, T05, T06, T08, T09, P01 | 0 | 0 | 0 | | **Summe** | **21** | **0** | **1** |

## Offene Fragen und Rückgabe an Opus
1. **W06 Z22 (LFP-Energiedichte aus der NMC-Spalte übernommen)** → OPUS, siehe Abschnitt 1 Zusatzbefund.
2. T07 Z7 (C): Zusammenfassung ohne wörtliche Quelle, keine Zahl.
3. Widersprüche der Auslegungsgrößen (Abschnitt 4) und Lücken (Abschnitt 5) → OPUS.
4. Abschnitt 3: W13 Z9 („bis 50 mm“ statt „50 mm oder mehr“), W13 Z12, W01 Z36 (65 % statt 66 %), W08 Z17/Z18 (Beleg-Zitat stützt Wert nicht) → OPUS.

## Zeile für `docs/08_ki_einsatz_protokoll.md` (Vorschlag)
`| 2026-11-16 | Sonnet (sonnet-umsetzer) | R4 Vorprüfung PI-Recherche gegen Rohtexte, 27 Themen | forschung/R4_vorpruefung.md, R4_vorpruefung_kurz.txt | Stichprobe durch Opus offen | FEHLT 22 (A 21, B 0, C 1); 1 Zusatzbefund W06 Z22 |`

---
*KI-generiert (Claude Sonnet), Entwurf, nicht freigegeben. Testprojekt „KI im Engineering“. Ende der Bearbeitung: Mo 16. Nov 15:23 CET 2026*
