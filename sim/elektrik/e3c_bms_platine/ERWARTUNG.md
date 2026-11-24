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
