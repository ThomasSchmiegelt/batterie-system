| Dok.-Nr. | ERW-E3c | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Erwartung E3c: BMS-Leiterplatte BT-311 (KiCad) und LFP-Kollisionen Servicedeckel | Ersteller | Claude Opus (KI) | Prüfer | – |

> KI-generiert (Opus, 2026-11-24), vor der Rechnung. Auftrag Autor: „mach die offenen punkte“. Regel „erst konservativ“ (Optimierungen → `pm/optimierungen.md`). Alle Werte sind **Annahmen Opus** (Herkunft „ERW-E3c“), sofern keine Akte genannt ist.

## Anforderung
REQ-P15, REQ-P17, REQ-P18, REQ-P19, REQ-P20, REQ-P13

## Teil A: LFP-Kollisionen (cad/pack, PACK_E3=1)
- Die 2 × M8-Köpfe der Trennbrücke ragen in den Servicedeckel BT-722, je 212 mm³. Abhilfe: lichte Höhe innen im Deckel ≥ Kopfhöhe + 3 mm, als Akte BT-722 (Merkmal anlegen, falls es fehlt, und melden).
- Schmelz_Lasche_A gegen Schiene_5: 0,0017 mm³, eine verschraubte Berührung. In der Kollisionsprüfung als Kontakt zulassen (Schwelle 0,01 mm³ nur für verschraubte Paare, Liste im Skript).
- Erwartung: LFP 0 Kollisionen, Höhenzuwachs Deckel ≤ 10 mm.

## Teil B: BMS-Platine BT-311
| Block | Annahme (konservativ) |
|---|---|
| Rechner | generischer Mikrocontroller ASIL D (Lockstep), eigenes Symbol, LQFP-144 |
| Versorgung 12 V | Verpolschutz, TVS nach ISO 7637-2, Systembasis-IC mit Watchdog (generisch) |
| Bus | 2 × CAN-FD-Transceiver (Fahrzeug, Laden), Gleichtaktdrossel |
| Schützansteuerung BT-715 | 3 Kanäle (Plus, Minus, Vorladung), High-Side- und Low-Side-Schalter, **Zener-Löschung** für schnelles Öffnen. Sparschaltung = OPT-006, nicht bauen |
| Sekundärpfad FSR-06 | Leitung vom Sekundärschutz der CMUs öffnet die Schütze ohne Software (Hardware-UND) |
| Daisy-Chain-Master | Übertrager mit **verstärkter Isolation** zur ersten CMU |
| Strommessung BT-340 | Shunt-ADC auf der HV-Seite, Daten über einen digitalen Isolator (verstärkt) |
| Trennung HV/NV | Kriechstrecke 10 mm, Luftstrecke 8 mm (inkl. Höhe 3000 m, Faktor 1,25), durchgehende Sperrzone. Schlitz = OPT-009, nicht bauen |
| Platine | 4 Lagen, FR4, Abstand im NV-Bereich 0,15 mm, im HV-Bereich wie ENT-168 0,2 mm |

## Erwartung
1. ≈ 150–220 Teile, Platine ≈ 160 × 100 mm. Sie passt in die Schaltbox (ENT-144, Maße aus parameter.json). Passt sie nicht → OPUS.
2. Die Sperrzone HV/NV ist als Linie ≥ 10 mm sichtbar. Nur Übertrager, Isolator und Shunt-ADC-Isolator überbrücken sie.
3. Routing vollständig, DRC 0, Prüfung Kriechstrecke ≥ Luftstrecke ok.
4. Masse ≈ 60–90 g.
5. Bilder wie bei E3: 3D iso/top, Explosionsansicht mit hervorgehobener Sperrzone, Platine in der Schaltbox.

## Abbruch → OPUS
Passt nicht in die Schaltbox; Sperrzone nicht durchgehend möglich; fehlendes Maß; jede neue Annahme.

## Nachtrag 1: OPT-006 Sparschaltung Schütze (Opus, 2026-11-24, Auftrag Autor „machen wir deine reihenfolge durch“)
Ziel: Haltestrom nach dem Anzug absenken, Löschung bleibt schnell. Annahmen Opus (ERW-E3c N1), solange keine Schützdaten vorliegen:
- Spule 12 V, R = 8 Ω, L = 50 mH (Anzug 1,5 A, 18 W)
- Anzugzeit 100 ms mit vollem Strom, danach Halten mit 0,3 × I_Anzug per PWM 20 kHz
- Abfallstrom 0,15 × I_Anzug
- Topologie:
  - Der High-Side-Schalter taktet. Der Freilauf beim Takten läuft über eine Diode vom Spulenende auf GND hinter dem Low-Side-FET (langsamer Abbau, kleine Welligkeit).
  - Beim Öffnen sperrt der Low-Side-FET. Der Strom muss dann über die Zener (z. B. 36 V) und klingt schnell ab.
  - Ein Hardware-UND (FSR-06) wirkt weiter auf beide Schalter.

## Erwartung N1
1. Haltestrom 0,45 A ± 10 %, Welligkeit < 10 %, Haltleistung ≈ 1,6 W statt 18 W (−90 %, ≈ 3 × 16 W = 49 W weniger im Dauerbetrieb).
2. Abfallzeit Strom bis 0,15 × I_Anzug: mit Zener ≈ 2–4 ms, nur mit Freilaufdiode ≈ 30–40 ms. Die Zener ist also Pflicht für SG-01/03 (Trennen innerhalb der FTTI).
3. Fehlerbetrachtung:
   - PWM bleibt dauernd an → voller Strom, nur Wärme, sicher.
   - PWM bleibt aus → das Schütz fällt ab. Das betrifft SG-05 (Verfügbarkeit) → Diagnose über den Spulenstrom-Shunt (vorhanden).
4. Platine: + ≈ 3 Dioden und Treiberanteil, Routing DRC 0, ERC 0, Schaltplan nachführen.

Abbruch → OPUS: Abfallzeit > 10 ms mit Zener; Platz reicht nicht.
