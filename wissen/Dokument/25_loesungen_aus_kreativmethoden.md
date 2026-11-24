---
typ: dokument
nr: "BAT-DOC-25"
version: "0.1"
status: "Entwurf"
tags: ["dokument"]
---
# BAT-DOC-25 – Lösungen aus Kreativ- und Lösungsfindung: wer hat was gefunden, was wurde verworfen

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

- Datei: `docs/25_loesungen_aus_kreativmethoden`
- Version: 0.1
- Status: Entwurf
- Typ: Projektdokument (Dokumentenlenkung [[Dokument/00_dokumentenlenkung]])

## Genannte Anforderungen (Textvorkommen)
- [[Anforderung/REQ-D15|REQ-D15]]

## Genannte Entscheidungen, Befunde, Bauteile (Textvorkommen)
- [[Befund/B-BAT-051|B-BAT-051]]
- [[Befund/B-BAT-053|B-BAT-053]]
- [[Befund/B-BAT-055|B-BAT-055]]
- [[Bauteil/BT-311|BT-311]]
- [[Bauteil/BT-324|BT-324]]
- [[Entscheidung/ENT-168|ENT-168]]
- [[Entscheidung/ENT-171|ENT-171]]
- [[Entscheidung/ENT-172|ENT-172]]
- [[Entscheidung/ENT-184|ENT-184]]
- [[Entscheidung/ENT-185|ENT-185]]
- [[Entscheidung/ENT-187|ENT-187]]

## Vorgänge, die dieses Dokument nennen
- [[Vorgang/KR1|KR1]] – Kreativmethode + Paarvergleich, Pilot Zellausgleich (pm/kreativ)

## Inhalt (Kopie aus `docs/25_loesungen_aus_kreativmethoden.md`)

| Dok.-Nr. | BAT-DOC-25 | Version | 0.1 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Lösungen aus Kreativ- und Lösungsfindung: wer hat was gefunden, was wurde verworfen | Ersteller | Claude Opus (KI) | Prüfer | – (Autor offen) |

> KI-generiert (Claude Opus, 2026-11-24). Auftrag Autor 2026-11-24: „kannst du noch lösungen dokumentieren die du aufgrund einer kreativ entscheidung getroffen hast“. Anforderung REQ-D15.
> **Zuschreibung:** In der Spalte „Herkunft“ steht, wer die Lösung gefunden hat (Methode, PI, Sonnet, Opus) und wer entschieden hat (Autor oder Opus delegiert). Vorgaben des Autors sind als solche gekennzeichnet.
> **Pflege:** Jede KR-Sitzung trägt hier ihr Ergebnis ein (METHODE.md, Stufe 9). Eine Lösung, die Opus ohne formale Sitzung aus eigener Abwägung gefunden hat, steht in Teil B.

## Teil A: Lösungen aus formalen Kreativsitzungen (pm/kreativ/)
| Nr | Problem (Widerspruch) | gewählte Lösung | verworfene Alternativen (Grund) | Herkunft | Entscheidung | Akte | Nachweis |
|---|---|---|---|---|---|---|---|
| KR1 | Ausgleichszeit kürzer, ohne dass die CMU heißer wird (B-BAT-051: 112–184 °C) | **K2: passiver Ausgleich + Wärmeleitpad zur Rahmenwand**, dazu 8 thermische Vias je Widerstandspaar | K6 aktiv kapazitiv (Rang 1 mit 0,563, aber innerhalb der Empfindlichkeit; mehr Fehlerarten, Reife unbelegt → OPT-001) · K4 Widerstände auf Kühlplatte (Leitungen, Fehlerarten) · K5 aktiv induktiv (Kosten, Reife) · K1 Ist und K3 getaktet (Festforderung 105 °C verfehlt; K3 verdoppelt die Wärme) | Kasten und Konzepte Opus (Lauf 2/3), TRIZ und Kopfstand PI, Paarurteile PI, Gewichte **Autor** (21 Paare) | **Autor** 2026-11-24 | ENT-184, ENT-185…187 | `pm/kreativ/KR1/ERGEBNIS.md`, E3b: 52,6 °C konservativ |
| KR2 | Bei Überladung/Übertemperatur trennen (SG-01/03), aber nicht unerwartet während der Fahrt (SG-05) | *läuft* | *läuft* | Kasten und Konzepte Opus, Gewichte **Autor** (10 Paare) | offen | – | `pm/kreativ/KR2/` |

**Lehren aus der Methode** (B-BAT-053): Drei Fehler von Opus im Pilot KR1 – zufällige Konzeptauswahl, undefiniertes Kriterium, fehlende Festforderung. Behoben in METHODE.md.

## Teil B: Lösungen, die Opus aus eigener Abwägung gefunden hat (ohne formale Sitzung)
Kein Kasten und kein Paarvergleich. Opus hat die Lösung als Ingenieururteil vorgeschlagen und meist selbst entschieden (delegiert, klare Empfehlung). Nach der Regel „erst konservativ“ wurde die bewährte Variante gewählt.

| Nr | Problem | Lösung | verworfene Alternative (Grund) | Anlass / gefunden von | Entscheidung | Akte / Stelle |
|---|---|---|---|---|---|---|
| L-01 | Daisy-Chain zwischen CMUs: Isolation | Nur die letzte Strecke zum BMS ist verstärkt isoliert, zwischen Nachbar-CMUs reicht Basisisolierung (≈ 2 × 76 V) | überall verstärkt (unnötig groß) | Opus (ERW-E3) | Opus | ERW-E3, BT-324 |
| L-02 | Ausgleichswiderstand: Wärme verteilen | 2 Widerstände 2512 parallel je Kanal statt einem | ein Widerstand 1 W (Hotspot, Derating knapp) | Opus (ERW-E3) | Opus | ENT-171/172 |
| L-03 | NMC-Ausgleichsstrom genau treffen | 2 × 64,9 Ω (E96) statt 2 × 68 Ω (E24) | E24 34 Ω (7 % langsamer → OPT-011) | SPICE E3 (Sonnet) zeigte die Abweichung, Lösung Opus | Opus | ENT-172 |
| L-04 | Daisy-Stecker zu hoch (10,9 mm > 10 mm Bauraum) | 2-polig liegend, Raster ≤ 1,25 mm, Höhe ≤ 5 mm | Bauraum vergrößern (Packhöhe) | Kollision gefunden von Sonnet, Lösung Opus | Opus | ERW-E3 N3 |
| L-05 | Routing scheiterte (0,5-mm-Pinfeld) | Abstand innerhalb der CMU 0,2 mm (Leiterplattenspalte, PD2 ≤ 100 V), 2,5 mm nur Klasse gegen Klasse über die Trennstelle | Router wechseln oder Platine vergrößern (Ursache lag in der Regel, nicht im Werkzeug) | Fehler von Opus selbst erkannt | Opus | ENT-168 |
| L-06 | Thermovias leiten nicht (isolierte Inseln) | Vias im Netz der Widerstandspads, je Netz eine B.Cu-Fläche, Pad elektrisch isolierend | isolierte Inseln (kein Wärmepfad) | Opus beim Prüfen von E3 | Opus | ENT-187, ERW-E3 N6 |
| L-07 | 6 Thermovias passten nicht | örtlich eine Via 0,45/0,2 mm | Neuverlegen oder 138 genügen lassen | Sonnet fragte, Opus entschied | Opus | ERGEBNIS E3 Frage 9 |
| L-08 | Sekundärschutz misst nur die Summe (B-BAT-055) | 3 × 6-Zellen-Überspannungsschutz, je Zelle, wired-OR auf ABSCHALT | ein 18-Kanal-Baustein (kein bewährtes generisches Teil), AFE-interne Diagnose (OPT-007) | Fehler gefunden von Sonnet in der FMEDA, Lösung Opus | Opus | ERW-E3 N7, FSR-12 |
| L-09 | SG-02 verfehlt ASIL C (FET-Kurzschluss entlädt dauernd) | 2 FETs in Reihe je Kanal (Doppel-FET SOT-363) | bessere Diagnose allein (M2, nur Was-wäre-wenn) | Maßnahme M1 vorgeschlagen von Sonnet (E3d), Entscheidung Opus | Opus | ERW-E3 N7 |
| L-10 | Kommunikationsausfall in der FMEDA als „sicher“ gewertet | Zeitüberwachung im BMS als Pflicht (FSR-11) | Einstufung als gefährlich (strenger, ohne Gegenmaßnahme) | Frage von Sonnet, Lösung Opus | Opus | docs/24 FSR-11 |
| L-11 | Freerouting-CLI stürzt ab | Jar mit eigener Java-25-Laufzeit | Router aufgeben, von Hand routen | Opus | Opus (Installation vom Autor freigegeben) | `~/.local/opt/freerouting/` |
| L-12 | LFP-Servicedeckel: M8-Köpfe ragen hinein | lichte Höhe ≥ Kopfhöhe + 3 mm | flachere Schrauben (Sonderteil) | Opus | Opus | ERW-E3c Teil A |

## Teil C: Vorgaben des Autors, die eine Lösung bestimmt haben
| Vorgabe | Wirkung |
|---|---|
| „Paarbewertung hinter die Kreativtechnik schalten“ | Paarvergleich mit Konsistenzprüfung als Stufe 6–8 der Methode |
| Wahl K2 statt K6 (KR1) | konservative Lösung, K6 bleibt OPT-001 |
| „erst konservativ, Optimierung später“ | Alternativen mit Risiko kommen in `pm/optimierungen.md` statt ins Design |
| Auslegungshöhe 3000 m | Luftstrecken mit Höhenfaktor 1,25 (L-05, BT-311) |
| ASIL D für SG-01 | zwei unabhängige Messwege, dadurch erst L-08 nötig |

