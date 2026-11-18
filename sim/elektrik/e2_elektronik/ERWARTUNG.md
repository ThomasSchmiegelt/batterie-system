| Dok.-Nr. | ERW-E2 | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Erwartung E2: Elektronik (BMS, Schaltbox, Kabel) beider Varianten, mit Darstellung | Ersteller | Claude Opus (KI) | Prüfer | – |

> KI-generiert (Opus), vor der Rechnung. Autor 2026-11-17: „mach erst elektronik auch mit darstellung und kabel“. W27 (7 Belege) liefert fast nichts Bemaßbares → **alle Auslegungswerte unten sind Annahmen Opus** (Lehrbuch-/Gedächtniswissen), bis Akten entschieden sind. Lastfälle aus E1 (`sim/elektrik/e1_querschnitte/ergebnis.json`): LFP 250s1p, NMC 217s4p; Spitze 10 s 240/230 A, Laden LFP 194 A, NMC 1,5C = 139 A.
## Annahmen Opus (Auslegungsvorschlag)
| BT | Merkmal | LFP | NMC | Begründung |
|---|---|---|---|---|
| BT-300 | architektur | zentral BMS + Zellüberwachung (CMU) in isolierter Daisy-Chain | gleich | Stand der Technik Serie |
| BT-320 | kanaele je CMU / anzahl | 18 / 14 | 18 / 13 | 18-Kanal-Mess-IC üblich; ⌈s/18⌉ |
| BT-320 | ausgleich / Strom | passiv / 150 mA | passiv / 150 mA | |
| BT-330 | Fühler | 4 je CMU = 56 | 4 je CMU = 52 | NTC auf Verbinder |
| BT-340 | prinzip / bereich | Shunt + Hall redundant / ±500 A | gleich | Spitze 240 A ×2 |
| BT-350 | ansprechwert | Warnung 500 Ω/V = 400 kΩ, Fehler 100 Ω/V = 80 kΩ | gleich | ECE R100 aus Gedächtnis (Beleg fehlt) |
| BT-360 | art / breite | flexible Leiterplatte (FPC) / 20 mm | gleich | |
| BT-711 | Schütze | 2 × 250 A / 1000 V DC + Vorladeschütz | gleich | Laden 194 A Dauer |
| BT-712 | Vorladung | C_ZK 1000 µF (Annahme), R 100 Ω → τ 100 ms, 95 % nach 300 ms | gleich | |
| BT-713 | Sicherung | Pyrosicherung + Schmelzsicherung 350 A | 315 A | |
| BT-720 | Service-Trennstecker | Mitte der Reihe (≤ 400 V je Hälfte), 250 A | gleich | |
| BT-730 | HV-Stecker | 2 (Antrieb/Laden 250 A; Nebenverbraucher 40 A) | gleich | |
| BT-740 | NV-Stecker | 1 × 26-polig | gleich | |
| BT-760 | Heizung | PTC im Kühlkreis (Fahrzeug), 5 kW | 5 kW | |
| BT-770 | Gas-/Drucksensor | Druck + H₂/CO₂ | gleich | Frühwarnung Durchgehen |
| BT-710/310 | Einbauort | vorne mittig im Pack (Fall a) oder auf dem Deckel vorne (Fall b) | gleich | |
## Erwartung
1. Spannungsabgriffe LFP 251, NMC 218; Messleitungslänge je Pack ≈ 25–40 m Bahn (FPC entlang der Zellreihen).
2. Ausgleich: 2 % Kapazitätsunterschied (1,85 Ah, beide Varianten 92,4 Ah je Reihe) → ≈ 12 h bei 150 mA; Wärme je CMU ≤ 10 W.
3. Vorladung: Spitzenstrom ≈ 8 A, Energie im Widerstand ≈ 320 J, ≤ 300 ms.
4. Heizung: Zellen von −10 auf +15 °C: LFP ≈ 460 kg Zellen × ~1000 J/(kg K) × 25 K ≈ 11–12 MJ → ≈ 40 min bei 5 kW; NMC ≈ 30–35 min.
5. Schaltbox (Schütze, Sicherungen, Shunt, Vorladung, BMS) ≈ 350 × 300 × 90 mm, 6–9 kg. Fall a kostet ≈ 250–350 mm Packlänge (passt zur Regel „Länge darf wachsen“, Breite fest); Fall b ≈ 90–110 mm Aufbau über dem Deckel.
6. HV-Leitungen intern (Reihenenden → Schaltbox, 50/35 mm² nach ENT-100/101): ≈ 3–5 m je Pack; Verluste ≤ 15 W bei 194 A.
7. Elektronik-Masse gesamt ≈ 12–18 kg je Pack.
## Verfehlt
Schaltbox passt in Fall a nicht ohne > 400 mm Länge; Ausgleich > 24 h; Kollisionen im CAD.

## Nachtrag 1 (Opus, 2026-11-17, nach Teil 1, vor CAD)
**Deutung Teil 1:** Punkt 6 war mein Fehler. 50 mm² Cu hat 0,34 mΩ/m, bei 194 A sind das ≈ 13 W/m. 40–65 W fallen nur während 20 min Schnellladen an, das ist akzeptiert. Punkt 4: NMC 26 min ist plausibel, weil die Zellmasse kleiner ist. Mein Band war zu hoch.
**Maße für das CAD (Annahmen Opus, Herkunft „ERW-E2 N1“, typische Serienteile):**
| Teil | Maß L×B×H mm | Masse kg |
|---|---|---|
| Hauptschütz (2×) | 80×60×75 | 0,45 |
| Vorladeschütz + Widerstand | 40×30×40 + 60×20×20 | 0,15 |
| Pyrosicherung | Ø30×80 | 0,15 |
| Schmelzsicherung | 30×30×85 | 0,10 |
| Shunt mit Messplatine | 80×40×15 | 0,10 |
| BMS-Platine | 200×150×20 | 0,4 |
| Schaltbox-Gehäuse Al, Wand 2 mm | aus Inhalt + 15 mm Rand, H ≤ 90 | aus Fläche |
| CMU-Platine | 120×60×10 | 0,08 |
| FPC-Messleitung | Breite 20, Dicke 0,3 | 0,05 kg/m |
| HV-Stecker 250 A / 40 A | 90×70×60 / 50×40×40 | 0,4 / 0,15 |
| NV-Stecker 26-polig | 50×30×40 | 0,05 |
| Service-Trennstecker | 80×50×60, oben zugänglich (Deckelöffnung) | 0,2 |
| Gas-/Drucksensor | 30×30×20 | 0,03 |
| HV-Leitung (BT-430) | Außendurchmesser LFP 14, NMC 12 mm; Biegeradius 5 × D = 70 / 60 mm | Cu + Isolierung |
**Lage (Vorgabe Opus):**
- Der Deckel ist durch die obere Kühlplatte belegt (ENT-088 LFP, NMC über Pad). Deshalb gilt in beiden Varianten: **CMU-Platinen in den Endzonen vorn und hinten**, nicht auf den Zellen.
- FPC:
  - LFP: im Spalt zwischen Zellende und Seitenrahmen. Das sind 8 mm Reserve. Prüfen, ob 0,3 mm FPC plus Halter mit 3 mm passen.
  - NMC: in der Verbinderebene unter dem Pad.
- HV-Leitungen nur in den Endzonen. Die Reihenenden und die Mitte der Reihe (Service-Trennstecker) bestimmst du aus der Verschaltung in `cad/pack/pack.py`.
  - Muss eine Leitung längs durch das Pack: **nicht bauen**, sondern Länge und freien Querschnitt an OPUS melden.
- Fall a: Schaltbox und BMS in der vorderen Endzone, Packlänge wächst um die Boxlänge plus 10 mm. Fall b: auf dem Deckel vorne, Höhenzuwachs melden.

## Nachtrag 2 (Opus, 2026-11-18, nach Fortsetzung 2)
**Deutung:** Dass LFP „nicht machbar“ ist, war mein Fehler. Die Vorgabe „Mitte hinten“ war unnötig streng. Der Service-Trennstecker muss nur von oben zugänglich sein, er muss nicht an der Box sitzen.
- **LFP:** Mit 2 Reihen liegen Plus und Minus hinten bei der Box, wenn die Kette hinten beginnt, nach vorn läuft und zurückkommt. Die Mitte mit dem Trennstecker liegt dann vorne, auf dem Querverbinder der Reihen.
- **Annahmen:**
  - FPC LFP 16 mm breit. 18 Kanäle passen, an den Querträgern sind 18 mm frei.
  - Im Seitenspalt bis 4 FPC übereinander (4 × 0,3 mm + Halter ≤ 3 mm).
  - Hälften NMC 413/387 V nehme ich an. Dass eine Hälfte ≤ 400 V bleibt, war eine Annahme und ist keine Norm.
  - Cu-Dichte 8,96 g/cm³ ist ein Stoffwert und braucht keine Akte.
  - Teilabstand in der Box 10 mm bestätigt (Annahme).
- **Erwartung:**
  - LFP: HV intern etwa 0,5–1,5 m, Verlust etwa 6–20 W bei 194 A, 0 Kollisionen.
  - Elektronikmasse mit HV-Leitungen je Variante 7–12 kg. Das Band 12–18 kg war zu hoch.
  - Bei NMC brauchen die Gruppenverbinder an den Wendestellen eigene Brücken, sonst Kollision.
**Verfehlt:** Kollision, die bleibt; LFP-Trennstecker von oben nicht zugänglich.

## Nachtrag 3 (Opus, 2026-11-18): Detailierung bis Konstruktionsstand
Autor: „ich hätte mir einen höheren detailierungsstand erwartet“. Gewählt sind alle vier Bereiche, Stufe Konstruktionsstand: erkennbare Serienteile, Bolzen und Schrauben ab M5, Biegeradien, Dichtungen. **Alle Maße sind Annahmen Opus (Herkunft „ERW-E2 N3“)**, typische Serienteile, ohne Beleg.
| Bereich | Teil | Annahme |
|---|---|---|
| Box innen | Hauptschütz | Körper wie N1. 2 Bolzen M8 oben, Abstand 40, Ø8×15. 2 Fußlaschen M5. Spulenstecker 15×10×12 |
| | Stromschienen | Cu LFP 25×3, NMC 20×3, Bohrung 8,5, Biegeradius innen = Dicke, Schrumpfschlauch 0,5 (außer an den Kontaktflächen) |
| | Pyro- / Schmelzsicherung | Laschen M8. Schmelzsicherung im Kunststoffhalter 40×40×95 |
| | Shunt | Manganin-Steg 3 mm zwischen Cu-Enden M8, Messplatine 80×40×1,6 mit Stecker 4-polig |
| | BMS-Platine | 200×150×1,6 auf 4 Abstandsbolzen M4 h 8, Stecker 26-polig, 2 × Daisy-Chain, 12-polig intern (je 30×15×12) |
| | Gehäuse | Flansch 12, Deckel 2, Dichtung 3×3 umlaufend, M5 alle 60 mm, Druckausgleich Ø 20 |
| Kabel | HV-Leitung | Bahn als Sweep mit R ≥ 5 D. Schnitt: Leiter, Isolierung, Schirm, Mantel. Rohrkabelschuh M8 (Hülse 40, Lasche 20×4). Clips 20×15×10 alle 200 mm |
| | FPC | Abgriff je Zellpol: Ni-Tab 8×4×0,2 auf den Verbinder. NTC 3×2×1 auf 4 Verbindern je CMU. Stecker 20-polig 25×8×6 an der CMU |
| | Daisy-Chain | verdrillte Leitung Ø 4 zwischen den CMUs, Stecker 15×8×8, R ≥ 20 |
| Stecker | HV 250 A | Flansch 90×70×8, 4 × M5, O-Ring, Steckkörper Ø 50×60, Verriegelungshebel 60×10×10, 90° gewinkelt |
| | HV 40 A / NV 26-polig | Flansch 50×40×6, 4 × M4 / Flansch 50×30×5, 2 × M4 |
| | Trennbrücke LFP | Brücke Cu 25×3×80, 2 × M8 mit Scheibe, HVIL-Brücke 15×10×8, Servicedeckel 120×80×2 mit 6 × M5 und Dichtung 3×3 |
| Verbinder | Zellverbinder | Dehnbogen (Omega) h 4. Laserschweißnaht dargestellt: 2 Linien 10×1, Vertiefung 0,2 je Pol. Berührschutz-Abdeckung aus Kunststoff 1 mm über jeder Polreihe |
| | Laschen | LFP: statt Stumpfstoß im 1-mm-Spalt 90° nach oben in die Endzone abkanten, Überlappung 25, M8. NMC: Überlappung 25 wie N1 |
| | NMC-Querschnitt | Das CAD liest den Querschnitt der Gruppenverbinder aus der E1-Akte (15×3), nicht 25×3 (B-BAT-027). Verlust neu rechnen |
**Erwartung:** 0 Kollisionen, nach Anpassungen höchstens an der Lage, nicht an den Maßen. Elektronikmasse +1…3 kg je Variante. NMC-Verbinderverlust ≈ 460 W mit 15×3; ob 15×3 thermisch reicht, entscheidet Opus danach. Teilezahl etwa 3–5 × höher.
**Verfehlt:** ein Maß müsste geändert werden, damit es passt; Packhöhe vorn > 130 mm; Lasche LFP auch abgekantet nicht unterzubringen.
