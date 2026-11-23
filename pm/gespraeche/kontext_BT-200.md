# Kontext für das Bauteilgespräch: BT-200 Zellstack

KI-generiert von pm.py aus Projektdateien (nur eigene Dokumente).

## Ich bin
Zellstack (BT-200). Aufgabe: Zellen in Reihe und parallel, mechanisch verspannt. Teil von: BT-000. Meine Teile: BT-210 Zellreihe, BT-220 Zwischenlage, BT-230 Wärmeleitmaterial, BT-240 Verspannung, BT-250 Zellhalter, BT-260 Verguss.

## Meine Merkmale (Wert und entscheidende Akte)
- verschaltung: noch nicht entschieden  (–)
- zellen_anzahl: noch nicht entschieden  (–)
- reihen_anzahl: noch nicht entschieden  (–)

## Anforderungen an mich (Lastenheft)
| REQ-P02 | nutzbarer Energieinhalt | aus Reichweite 400 km (Vorgabe Autor 2026-11-16) × Verbrauch (Annahme), Vergleich sim/chemie/vergleich_lfp_nmc | Autor | Muss | Reichweite: Vorgabe Autor |
| REQ-P03 | Systemspannung (Nenn, min, max) | 800 V nominal (ENT-006, Autor 2026-11-16); min/max folgen aus Zellfenster | Autor | Muss | teilweise |

## Entscheidungen, die mich betreffen (vollständig)
### ENT-012 Bauteilbaum für zwei Varianten (Zellhalter 4680, Rundzellmaße) (2026-11-16, entschieden (Mensch), Opus (Vorschlag) / Autor (Freigabe 2026-11-17); Variante: alle)
Merkmal: - = None ; Anforderungen: REQ-P06, REQ-P11; Belege: B-BAT-009
## Frage
Der Baum (ENT-004) kennt nur prismatische Zellen. Was braucht die Variante NMC (Rundzelle 4680, ENT-008)?
## Alternativen
| Alternative | dafür | dagegen |
|---|---|---|
| **Ein Baum mit Feld `varianten` je Bauteil (gewählt)** | gemeinsame Teile (Gehäuse, BMS, Schaltbox, Kühlung) nur einmal; Unterschiede sichtbar | Merkmale wie breite/dicke bleiben bei 4680 leer |
| zwei getrennte Bäume | einfache Skripte | doppelte Pflege von rund 40 gleichen Teilen |
## Entscheidung und Begründung
Neu: BT-250 Zellhalter (nur NMC: werkstoff, anordnung, zellabstand_mm, hoehe_mm). BT-100 bekommt durchmesser_mm und hoehe_mm. BT-220 Zwischenlage und BT-240 Verspannung gelten nur für LFP (Rundzellen werden gehalten, nicht verspannt). Fehlt `varianten`, gilt ein Teil für beide. Baum jetzt 50 Einträge. Alte Fassung im Scratchpad (struktur_v2_vor_varianten.json).
## Folgen
- Stückliste NMC braucht eine Position für BT-250; Positionen 200.2/200.4 entfallen bei NMC.
- Kühlung (BT-610) bei 4680: Kühlung am Zellboden oder seitlich (Kühlband) — eigene Akte in K.
- CAD: `cad/zelle` Prisma und Zylinder, `cad/pack` je Variante.

---
*KI-generiert (Claude Opus, 2026-11-16). Status vorgeschlagen.*

### ENT-145 Verschaltung Mäander (4 Bänder aus Spaltenzügen): Plus, Minus, Mitte hinten (2026-11-18, vorgeschlagen, Opus (Vorschlag, AUFTRAG E2 Fortsetzung 2; Geometrie Sonnet); Variante: NMC)
Merkmal: verschaltung = maeander ; Anforderungen: REQ-P02; Belege: B-BAT-024
## Frage
BT-200 Verschaltung so wählen, dass Plus, Minus und die Mitte (Service-Trennstecker, ENT-131) in der hinteren Endzone liegen (Schaltbox hinten, ENT-144). Eine Leitung längs durch das Pack ist nicht erlaubt.
## Alternativen
| Alternative | dafür | dagegen |
|---|---|---|
| Reihen in Längsrichtung nacheinander (Plus hinten, Minus vorn) | einfach | Minus oder Mitte vorn, Leitung längs durch das Pack |
| Mäander mit 4 Bändern (diese Akte) | Plus, Mitte, Minus hinten, keine Längsleitung | Gruppenverbinder von G4 (je 4 Zellen einer Querreihe) passen nicht, müssen auf Spaltenzüge umgestellt werden |
| LFP (prismatisch) | – | **nicht machbar**: nur 2 Zellreihen (je 125 Zellen), nötig sind 4 Durchläufe. Deshalb gilt diese Akte nur für NMC. |
## Entscheidung und Begründung
NMC 217s4p, 868 Zellen: 28 Spalten (y) × 31 Reihen (x). 4 Bänder zu je 7 Spalten. In jedem Band läuft ein Spaltenzug (Zickzack entlang x, danach nächste Spalte): Band 1 hinten→vorn, Band 2 vorn→hinten, Band 3 hinten→vorn, Band 4 vorn→hinten. Gruppe = 4 aufeinanderfolgende Zellen des Zuges (217 Gruppen: Bänder 56 / 56 / 56 / 49). Anschlüsse: Plus Band 1 Anfang (hinten, y außen), Mitte = Ende Band 2 und Anfang Band 3 (hinten, y Mitte, nebeneinander), Minus Ende Band 4 (hinten, y außen). Alle vier liegen in der letzten Zellreihe der jeweiligen Spalte (cad/pack/entwurf/ergebnis_NMC_e2.json, e2.verschaltung.alle_anschluesse_hinten = true).
Folge der Zählung: Hälfte A = 112 Gruppen (Plus bis Mitte), Hälfte B = 105 Gruppen. Die Mitte liegt damit nicht bei 108,5 Gruppen (≈ 413 V / 387 V Nennspannung). Das ist durch die Spaltenzahl vorgegeben (e2.verschaltung.gruppen_hälfte_A/B). Zellabstand im Zug normal 48 mm, 84 Schritte (von 867) länger (Querträger, fehlende Reihe in Spalten 21 bis 27, größter 230,6 mm).
Status vorgeschlagen, Freigabe nur durch den Menschen.
## Folgen
Zellverbinder (Gruppenverbinder und Reihenbrücken aus G4) sind in `pack.py` noch nach G4 gezeichnet (je 4 Zellen quer) und entsprechen dieser Folge nicht; Umbau offen (Opus). HV-Leitungen intern: Plus 744 mm, Minus 408 mm, Mittenleitungen je 11 mm (e2.hv). LFP: Verschaltung offen, siehe Alternativen.

---
*KI-generiert (Claude Sonnet, 2026-11-18), im Auftrag von Opus.*

### ENT-148 Verschaltung LFP Schleife 2 Reihen: Plus und Minus hinten, Mitte vorn (2026-11-18, vorgeschlagen, Opus (Vorschlag, AUFTRAG E2 Fortsetzung 3; Geometrie Sonnet); Variante: LFP)
Merkmal: verschaltung = schleife_2reihen ; Anforderungen: REQ-P02; Belege: B-BAT-024
## Frage
BT-200 Verschaltung LFP (250s1p, 2 Zellreihen zu je 125 Zellen) so, dass Plus und Minus hinten bei der Schaltbox liegen (ENT-144) und der Service-Trennstecker von oben zugänglich ist (ERWARTUNG Nachtrag 2).
## Alternativen
| Alternative | dafür | dagegen |
|---|---|---|
| Mäander mit 4 Durchläufen (ENT-145) | alles hinten | LFP hat nur 2 Reihen (Opus Nachtrag 2) |
| Schleife 2 Reihen (diese Akte) | Plus und Minus hinten, keine Längsleitung | Mitte vorn auf dem Querverbinder der Reihen |
## Entscheidung und Begründung
Kette beginnt hinten (Plus), läuft Reihe 0 nach vorn, Querverbinder vorn (Mitte, Trennstecker mit Deckelöffnung), Reihe 1 zurück nach hinten (Minus). Herkunft: ERWARTUNG.md Nachtrag 2. Status vorgeschlagen, Freigabe nur durch den Menschen.
## Folgen
HV intern LFP nur hinten (Plus, Minus), Mitte vorn mit Trennstecker. ENT-145 bleibt auf variante [NMC].

---
*KI-generiert (Claude Sonnet, 2026-11-18), im Auftrag von Opus.*

## Befund B-BAT-009
B-BAT-009 (2026-11-16) Zerlegungsstudie Blade (W20): Gen-1-Zelle 160 Wh/kg, 355 Wh/L; Bauraum Fall A genau an der Grenze
- Quelle: Cell Rep. Phys. Sci. 6, 102453 (2025), CC-BY, PDF vom Autor in quellen/blade_zerlegung/. PI-Lauf W20: 0/21, weil PI die DOI statt der file://-URL angab. Opus: URL ersetzt → 17/21; die 4 Reste stehen im Fließtext (pdftotext ohne -layout, zweispaltiger Satz). Z25 („around 23 of the heat“) gesperrt: Bruch bei der Textumwandlung verloren.
- **Blade-Zelle (gemessen, Tabelle 1):** 135 Ah, 432 Wh, 3,2 V, Fenster 2,6–3,65 V, 2,7 ± 0,3 kg, 1216 mL, **160 Wh/kg, 355,3 Wh/L**, 965 × 90 × 14 mm, Wandstärke Gehäuse 0,3 mm, ein Z-gefalteter Elektrodenstapel, Aktivmasse etwa 60 % der Zellmasse. Zum Vergleich Tesla 4680 (NMC811): 241 Wh/kg, 643 Wh/L.
- **Folge Bauraum:** 355 Wh/L × 60 % Volumennutzung (W19) = 213 Wh/L Pack. Nötig: 214 (Fall A), 256 (Fall B). Fall A passt knapp, Fall B nicht. Prüfpunkt von ENT-005 damit **an der Grenze, nicht klar erfüllt**.
- **Folge Masse:** 160 Wh/kg liegt unter dem C0-Band 185–210 (W03, Hersteller, Long Blade 2.0). Mit 160 Wh/kg, Zellanteil 0,75: Packmasse Fall A 616 kg (543–711), Fall B 739 kg. Eine 4680-NMC-Zelle ergäbe Fall A etwa 409 kg. Der Satz „kein belegter Massenunterschied“ (B-BAT-006) gilt nur mit den Herstellerwerten der 2. Generation.
- Folge 800 V (ENT-006): Eine Original-Blade-Zelle (135 Ah) gäbe 250s × 135 Ah × 3,2 V = 108 kWh. Nötig 92 Ah (A) → bei gleichem Querschnitt etwa 660 mm statt 965 mm Länge (G1).
- We

## Befund B-BAT-024
B-BAT-024 (2026-11-18) E2 Elektronik Teil 1: Abgriffe, Ausgleich, Vorladung ok; HV-Verlust 13 W/m akzeptiert; Schaltbox Fall b
- Teil 1 (`sim/elektrik/e2_elektronik/ERGEBNIS.md`): 251/218 Abgriffe, Ausgleich 12,3 h, Vorladung 8 A/320 J/300 ms. Opus-Fehler in der Erwartung: ≤ 15 W bei 3–5 m HV-Leitung war mit 50 mm² nicht möglich (≈ 13 W/m, nur beim Schnellladen). NMC-Heizung 26 min unter dem Band, weil die Zellmasse kleiner ist (308 kg).
- CMU-Wärme NMC 9,95 W bei Nennspannung, bei Ladeschluss über 10 W → Rechnung mit Zellhöchstspannung nachholen.
- Autor: Schaltbox auf dem Deckel vorne (ENT-109). Antworten auf Sonnets Fragen 1–3 im Nachtrag 1 der ERWARTUNG; 4: 139 A (1,5C) gilt; 5: Höchstspannung LFP 3,65 V, NMC 4,2 V (Annahme). Vorgang: [E2]

## B-BAT-023 (2026-11-17) C2 Kalibrierung: Blade-Widerstand gemessen 0,877 mΩ; 4680 schafft 30 min bei 1,5C, Plating-Risiko im Modell
- Blade 25 °C, 15–90 % SOC: RMS 15,3 mV, R10 Modell 0,827 / Messung 0,877 mΩ (Test#5). Temperaturfit verfehlt (158 mV), OCV des Literatursatzes 143 mV daneben → **DFN für LFP nicht belastbar; Opus: für Wärme den gemessenen Widerstand nutzen** (unsere Zelle 1,28 mΩ → 48 W statt 55 W bei 2,1C; K1 war konservativ).
- 4680 (Chen2020-Material, W20-Geometrie, DCIR 6,4 mΩ im Band): 10→80 % in 29,7 min bei 1,5C CC-CV → REQ-P05 erfüllbar. Wärme 7,4 W (Modell) bzw. 11,5 W (I·ΔU) gegen K1b-Annahme 6,7 W → K1c: LFP 32,7 °C / 4,0 K ✓; 4680 mit Modellwärme 34,0 / 4,15 ✓, mit I·ΔU 39,1 / 6,5 ✗ (5 K). Opus: Differenz de

