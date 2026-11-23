# Freigaberunde 2026-11-23 (moderiert von Opus, Antworten des Autors wörtlich als Auswahl)

KI-generiert (Claude Opus). Auftrag des Autors: „bitte moderiere die Freigaberunde“. Die Optionen hat Opus vorgeschlagen, die Auswahl traf der Autor.

## Runde 1
| Punkt | Entscheidung Autor |
|---|---|
| REQ-P07 Länge | ≤ 2400 mm (Radstand Kompaktwagen etwa 2,6–2,7 m, Annahme) |
| REQ-P09 Spreizung | ΔT ≤ 5 K **zwischen den Zellen** (neu auswerten) |
| REQ-P07 Höhe | 130 mm im Zellbereich, Schaltbox als Dom bis 250 mm |
| REQ-P07 Masse | Startwerte als Ziel: LFP ≤ 528 kg, NMC ≤ 370 kg (beide verfehlt, Leichtbauziel Schleife 2) |

## Runde 2
| Punkt | Entscheidung Autor |
|---|---|
| REQ-P08 Umgebung | Betrieb −20 … +45 °C, Laden 0 … +45 °C (Vorheizen unter 0 °C) |
| REQ-P10 Lebensdauer | SOH ≥ 70 % nach 200.000 km |
| REQ-P14 Crash | Zellen ≤ 0,5 mm (Pfahl 5 kJ und Quetschung), Quetschung nach R100 mit 100–105 kN |
| REQ-P03/P04 | U_nenn 720–880 V, U_min/U_max ausweisen; P_spitze nach Startwert, P_dauer ≥ 60 kW |

## Runde 3
| Punkt | Entscheidung Autor |
|---|---|
| REQ-P12/P13 | Wasser-Glykol, Δp je Platte ≤ 0,5 bar, Verteilung ±10 %, IP67, R_iso ≥ 100 Ω/V (R100) |
| REQ-P15 | Messumfang: Zellspannung je Reihe, Temperaturfühler, Isolationswächter (Stücklistenposition) |
| REQ-G02 | Batteriepass, Kennzeichnung und CO₂-Fußabdruck nach EU 2023/1542 als **Muss** |
| 43 Akten / 219 Annahmen | Delegation an Opus (siehe unten) |

## Delegation (Autor, wörtlich)
„wo du etwas emphelen kannst, kannst du es selber freigeben. Bei den rest frag mich.“
Opus legt das eng aus: Es betrifft technische Akten und Annahmen mit klarer Empfehlung. Anforderungswerte, Abwägungen ohne klare Empfehlung, Dokumentfreigaben und alles nach außen bleiben beim Autor. Der Status lautet `entschieden (Opus, delegiert durch Autor 2026-11-23)`.

## Runde 4: Selbstfreigaben Opus (Begründung je Gruppe)
| Akten | Status neu | Begründung |
|---|---|---|
| ENT-104, 105, 106 (Kanal 4 × 5 mm, Al-Platte quer) | ersetzt durch ENT-153/154/155 | gleiches Merkmal, die freigegebene Blechplatte (ENT-152 ff., Autor) hat sie abgelöst |
| ENT-109 (Schaltbox Deckel vorne) | ersetzt durch ENT-144 | ENT-144 (hinten, entschieden) ist gebaut |
| ENT-147 (Bauraumlänge LFP 2050 mm) | verworfen | überholt durch G5.9-Länge 2373 mm und REQ-P07 L ≤ 2400 mm (Autor, Runde 1) |
| ENT-110 bis 143 außer 138-Konflikt, 146, 149, 150 (BMS, Schütze, Sicherungen, Stecker, Heizung, Sensoren, Biegeradien) | entschieden (Opus, delegiert) | Stand der Technik und untereinander stimmig. Beispiele: Schütz 250 A über Dauerstrom LFP 194 A und Ladestrom von etwa 200 A; Isolationswarnung 400 kΩ = 500 Ω/V liegt über dem R100-Minimum von 100 Ω/V; Vorladung 100 Ω / 300 ms passt zu etwa 1 mF. Herkunft: Vorschläge aus B-BAT-024 |
| ENT-138 (BMS in der Schaltbox hinten) | entschieden (Opus, delegiert) | stimmig mit ENT-144 |
| ENT-145 (NMC Mäander) und 148 (LFP Schleife) | entschieden (Opus, delegiert) | verschiedene Varianten, kein Widerspruch, so gebaut |
| Annahmen A_* ohne Rechnungsbezug (etwa 190) | bestätigt als Konstruktionsannahme (Opus, delegiert) | Detailmaße ohne Einfluss auf eine REQ-Bewertung, Graph: keine `verwendet`-Kante |
| Annahmen A_* mit Rechnungsbezug (etwa 30, z. B. A_rand_mm, A_luft_mm, A_seitenrahmen_*, A_pad_mm, A_quertraeger_*) | bleiben Annahme, markiert als **Stellgröße Schleife 2** | Daran hängen die verfehlten REQ P14 (Pfahl) und P09 (ΔT). Sie werden in Schleife 2 verändert und gehören deshalb jetzt nicht festgeschrieben |
| A_zellzahl_LFP/NMC, A_zellabstand_* und Merkmale BT-210.zellen_je_reihe, BT-250.zellabstand_mm | eigene Akten anlegen, Wert wie gebaut, entschieden (Opus, delegiert) | Die Zellzahl folgt aus 800 V (ENT-006) und der Zellspannung. Sie darf keine Annahme sein |
Vor dem Übernehmen in parameter.json wird das CAD vorher und nachher gebaut und verglichen. Kollisionen, Masse und Maße müssen gleich bleiben. Weicht etwas ab, wird zurückgenommen und der Autor gefragt.
