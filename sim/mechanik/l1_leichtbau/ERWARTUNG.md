| Dok.-Nr. | ERW-L1 | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Erwartung L1: Leichtbau-Potenzial des Packs (OPT-012), Studie ohne CAD-Änderung | Ersteller | Claude Opus (KI) | Prüfer | – |

> KI-generiert (Opus, 2026-11-24). Auftrag Autor: „machen wir deine reihenfolge durch“, Wahl „Ziel neu ableiten“ (REQ-P07). Alle Einsparwerte sind **Schätzungen Opus**. Die Studie zeigt nur das Potenzial, das CAD bleibt unverändert, bis der Autor das Ziel neu festlegt.

## Anforderung
REQ-P07, REQ-P13 (Crash), REQ-P09 (Thermik)

## Ist (cad/pack/entwurf/ergebnis_<V>_e2d_e3c.json, gruppen)
| | LFP | NMC |
|---|---|---|
| Zellen | 462,5 kg (250 × 1,85) | 308,1 kg (868 × 0,355) |
| Rest | 157,3 kg | 174,3 kg |
| Pack | 619,8 kg | 482,4 kg |
| Zellanteil | 74,6 % | 63,9 % |
| Ziel REQ-P07 | 528 kg (87,6 %) | 370 kg (83,3 %) |

Größte Posten (beide etwa gleich): Kühlplatte 44–47, Boden 23–24, Unterfahrschutz 23–24, Seitenrahmen 20–22, Deckel 15–16, Pad 13–14 kg. Dazu bei NMC: Verguss 11, Gruppenverbinder 8 kg.

## Aufgabe
Für jede Gruppe ≥ 3 kg:
- (a) Material, Dicke bzw. Querschnitt und Akte aus parameter.json bzw. dem Skript.
- (b) Masse nachrechnen (Plausibilität ± 5 %).
- (c) Hebel nach der Liste unten mit Einsparung in kg.
- (d) Folge für Crash, Thermik und Fertigung, Bewertung nach Kosten, Sicherheit und Effizienz.
Keine CAD-Änderung, nur Rechnung (`leichtbau.py` → `ergebnis.json`, Wasserfallbild Ist → Hebel → neu mit Zielband REQ-P07 und dem Band aus W51 (wenn fertig) und Lesehilfe).

| Hebel | Schätzung Opus |
|---|---|
| H1 Kühlplatte: Kanalblech dünner bzw. als Strangpressprofil, Stand prüfen (47 kg ≈ 6 mm Al vollflächig?) | −15 … −25 kg |
| H2 Boden und Kühlplatte zusammenlegen (Kühlplatte trägt) | −10 … −20 kg |
| H3 Unterfahrschutz aus Stahl hochfest dünner bzw. Verbund | −5 … −10 kg |
| H4 Deckel aus Verbund (SMC) statt Al bzw. Stahl | −5 … −8 kg |
| H5 Pad (Gap-Filler) dünner bzw. nur unter den Zellen | −4 … −7 kg |
| H6 Seitenrahmen: Strangpressprofil mit Kammern statt Vollquerschnitt | −5 … −10 kg |
| H7 NMC: Verguss nur oben statt voll | −5 … −8 kg |

## Erwartung
1. Summe der Hebel: LFP ≈ −45 … −75 kg → **≈ 545–575 kg (80–85 %)**, NMC ≈ −50 … −85 kg → **≈ 400–430 kg (72–77 %)**.
2. **LFP-Ziel 528 kg nur mit Cell-to-Pack** (größere Zellen, Zellen tragend). **NMC 370 kg ist mit diesen Zellen unerreichbar**, weil 308 kg Zellen ein Rest von nur 62 kg wären. Weicht das ab → OPUS.
3. H1/H2 sind die größten Hebel. H2 berührt Crash X3 (Boden) und die Dichtheit → Pfad Schleife 2.

## Abbruch → OPUS
Masse der Gruppe nicht nachvollziehbar (> 5 %); Hebel braucht eine neue Annahme außerhalb der Liste.

## Nachtrag 1 (Opus, 2026-11-24, Prüfung)
- **Meine Hebelschätzungen waren zu optimistisch.** Die Kühlplatte ist bereits 3,2 mm Al-äquivalent (8 mm × Füllgrad 0,4). Seitenrahmen und Verguss sind schon leicht. Der Unterfahrschutz ist Al 3 mm. H1 und H2 sind nicht additiv.
- Neu geschätzt (Opus): H1/H2 zusammen −10 … −20, H4 −3 … −6, H5 −1,6 (LFP) bzw. −5,4 (NMC), H3 0 … −5, H6/H7 ≈ 0. **LFP ≈ −20 … −35 kg, NMC ≈ −25 … −40 kg.**
- W51 (9 Belege, 0 Fehler): Richtwert LFP 70 %, NMC 65 %, Schnitt 62,9 %, Bestwert 90 % (BYD Han). Ist: LFP 74,6 %, NMC 63,9 %, also üblich.
- Folge: REQ-P07 neu LFP ≤ 600 / NMC ≤ 450 kg (Autor, AEN-022). Benötigt sind LFP −20, NMC −32 kg → L2 im CAD mit Crash- und Thermik-Nachweis.
- Crash heißt REQ-P14 (nicht P13), korrigiert.
