# Kontext für das Bauteilgespräch: BT-100 Zelle

KI-generiert von pm.py aus Projektdateien (nur eigene Dokumente).

## Ich bin
Zelle (BT-100). Aufgabe: speichert Energie (Chemie, Elektroden, Gehäuse, Pole, Ventil). Teil von: BT-000. Meine Teile: BT-110 Elektrodenstapel, BT-120 Zellgehäuse, BT-130 Zellpole, BT-140 Zellventil.

## Meine Merkmale (Wert und entscheidende Akte)
- chemie: noch nicht entschieden  (–)
- format: noch nicht entschieden  (–)
- laenge_mm: noch nicht entschieden  (–)
- breite_mm: noch nicht entschieden  (–)
- dicke_mm: noch nicht entschieden  (–)
- kapazitaet_Ah: noch nicht entschieden  (–)
- nennspannung_V: noch nicht entschieden  (–)
- masse_g: noch nicht entschieden  (–)
- durchmesser_mm: noch nicht entschieden  (–)
- hoehe_mm: noch nicht entschieden  (–)

## Anforderungen an mich (Lastenheft)
| REQ-P06 | Zellchemie | zwei Varianten gleicher Spezifikation (Autor 2026-11-16): LFP-Blade prismatisch (ENT-005) und NMC811-Rundzelle 4680 (ENT-007…011); Baum ENT-012 | Autor | Muss | entschieden |
| REQ-P10 | Lebensdauer (Zyklen, Jahre, Restkapazität) | offen | Autor | Soll | offen |
| REQ-P11 | Sicherheit: keine Ausbreitung des thermischen Durchgehens bzw. Warnzeit nach Norm | nach Norm (BAT-DOC-07) | Norm | Muss | offen |

## Entscheidungen, die mich betreffen (vollständig)
### ENT-002 Zellmodell mit PyBaMM (2026-11-11, entschieden (Mensch), Opus / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: alle)
Merkmal: - = None ; Anforderungen: REQ-P06, REQ-P10; Belege: –
## Frage
Zellmodell mit PyBaMM?
## Alternativen
| Alternative | dafür | dagegen |
|---|---|---|
| eigenes Ersatzschaltbild | schnell | keine Elektrochemie, keine Alterung |
## Entscheidung und Begründung
Quelloffen, validierte Parametersätze inklusive LFP (Prada2013); Probelauf auf diesem Rechner ok.
## Folgen
siehe docs/05_risiken_fmea.md

### ENT-005 Zellchemie LFP (Blade-Format) als Hauptvariante, NMC als Vergleich (2026-11-16, entschieden (Mensch), Opus (Vorschlag) / Autor (Freigabe 2026-11-16); Variante: LFP)
Merkmal: chemie = LFP ; Anforderungen: REQ-P06, REQ-P10, REQ-P11; Belege: B-BAT-006, B-BAT-005
## Frage
LFP oder NMC für ein Fahrzeug mit 1500 kg und 400 km Reichweite (Vorgabe Autor 2026-11-16)?
## Alternativen
| Alternative | dafür | dagegen |
|---|---|---|
| **LFP, Blade-Format (gewählt)** | Zyklen erfüllt (2500–9000 gegen Bedarf 1000); Nageltest Blade 30–60 °C (W03); Zellwerte belegt und schmal (185–210 Wh/kg); Vorbild | in der Mitte 7–8 % schwerer (499 gegen 464 kg, Fall A); Kälte (W01); 250 statt 220 Zellen in Reihe; Bauraum offen |
| NMC | in der Mitte etwas leichter; höhere Zellspannung | Wh/kg-Band breit, Ebene unsicher (150–275, W06); Zyklen unsicher (nur Li-Ion allgemein); Sauerstofffreisetzung ab 300 °C (W10) |
## Entscheidung und Begründung
Vergleich `sim/chemie/vergleich_lfp_nmc/` (ERWARTUNG, ergebnis.json, DEUTUNG.md; Opus-Gegenrechnung gleich). Die Masse unterscheidet sich nicht belegbar: Die NMC-Spanne 316–758 kg umschließt die LFP-Spanne 414–615 kg (Fall A). Zyklen (REQ-P10) und Sicherheit (REQ-P11) sprechen für LFP. Die frühere NMC-Wahl in `pm/startwerte.py` beruhte auf der unbelegten Annahme 180 Wh/L (B-BAT-004).
NMC bleibt als Vergleichsvariante im Zellmodell (C5).
## Folgen
- BT-100 nennspannung_V aus W01 (3,2 V). Zellen in Reihe bei 800 V: 250 (G3).
- Prüfpunkt: Wh/L der Blade-Zelle aus der Zerlegungsstudie (W19). Reicht er für den Bauraum nicht, wird neu entschieden (ENT ersetzt).
- Heizung BT-760 und Kälteladen werden wichtiger (C5, K0).
- startwerte.py und stueckliste.py rechnen noch mit NMC. Sie werden nach Freigabe auf LFP umgestellt.

**Nachtrag 2026-11-16 (Opus):** Autor: „kannst du auch zwei varianten paralell bauen? bei mit den selben spezifikationen“ und Wahl NMC = Rundzelle 4680. Diese Akte gilt deshalb nur für die Variante LFP. NMC ist keine Vergleichsrechnung mehr, sondern eine eigene Variante (ENT-007…011). Messwerte Blade Gen 1 (B-BAT-009): 160 Wh/kg, 355 Wh/L.

### ENT-007 Zellchemie NMC811 für Variante NMC (2026-11-16, entschieden (Mensch), Autor (Wahl „Rundzelle 4680“, 2026-11-16) / Werte W20; Variante: NMC)
Merkmal: chemie = NMC ; Anforderungen: REQ-P06; Belege: B-BAT-009
## Frage
Welche Chemie hat die zweite Variante?
## Alternativen
| Alternative | dafür | dagegen |
|---|---|---|
| siehe ENT-008 (Formatwahl) | | |
## Entscheidung und Begründung
NMC811, belegt in der Zerlegung (W20: „The Tesla 4680 cell utilizes NMC811 chemistry“). Quelle: Cell Rep. Phys. Sci. 6, 102453 (2025), CC-BY, PDF in quellen/blade_zerlegung/ (W20, B-BAT-009).
## Folgen
Gilt nur für die Variante NMC. Bei 800 V (ENT-006): 217 Zellen in Reihe; Parallelzahl und Zellhalter folgen in G3/G4. Zellmaße Ø 46 × 80 mm brauchen eigene Merkmale im Bauteilbaum (ENT-012, vorgeschlagen).

---
*KI-generiert (Claude Opus, 2026-11-16).*

### ENT-008 Zellformat Rundzelle 4680 für Variante NMC (2026-11-16, entschieden (Mensch), Autor (Wahl „Rundzelle 4680“, 2026-11-16) / Werte W20; Variante: NMC)
Merkmal: format = Rundzelle 4680 ; Anforderungen: REQ-P06; Belege: B-BAT-009
## Frage
Welches Zellformat hat die NMC-Variante?
## Alternativen
| Alternative | dafür | dagegen |
|---|---|---|
| siehe ENT-008 (Formatwahl) | | |
## Entscheidung und Begründung
Autor wählte 4680 (beste Datenlage: gemessen in derselben Studie wie Blade; stärkster Kontrast prismatisch CTP gegen Rundzelle). Alternativen: NMC prismatisch (keine Messdaten), Pouch (keine Quelle). Quelle: Cell Rep. Phys. Sci. 6, 102453 (2025), CC-BY, PDF in quellen/blade_zerlegung/ (W20, B-BAT-009).
## Folgen
Gilt nur für die Variante NMC. Bei 800 V (ENT-006): 217 Zellen in Reihe; Parallelzahl und Zellhalter folgen in G3/G4. Zellmaße Ø 46 × 80 mm brauchen eigene Merkmale im Bauteilbaum (ENT-012, vorgeschlagen).

---
*KI-generiert (Claude Opus, 2026-11-16).*

### ENT-009 Kapazität 4680: 23,125 Ah (2026-11-16, entschieden (Mensch), Autor (Wahl „Rundzelle 4680“, 2026-11-16) / Werte W20; Variante: NMC)
Merkmal: kapazitaet_Ah = 23.125 Ah; Anforderungen: REQ-P06; Belege: B-BAT-009
## Frage
Kapazität je Zelle der NMC-Variante?
## Alternativen
| Alternative | dafür | dagegen |
|---|---|---|
| siehe ENT-008 (Formatwahl) | | |
## Entscheidung und Begründung
Kaufzelle, Wert gemessen (W20 Tabelle 1, C/10). Parallelzahl folgt daraus (G3). Quelle: Cell Rep. Phys. Sci. 6, 102453 (2025), CC-BY, PDF in quellen/blade_zerlegung/ (W20, B-BAT-009).
## Folgen
Gilt nur für die Variante NMC. Bei 800 V (ENT-006): 217 Zellen in Reihe; Parallelzahl und Zellhalter folgen in G3/G4. Zellmaße Ø 46 × 80 mm brauchen eigene Merkmale im Bauteilbaum (ENT-012, vorgeschlagen).

---
*KI-generiert (Claude Opus, 2026-11-16).*

### ENT-010 Nennspannung 4680: 3,7 V (2026-11-16, entschieden (Mensch), Autor (Wahl „Rundzelle 4680“, 2026-11-16) / Werte W20; Variante: NMC)
Merkmal: nennspannung_V = 3.7 V; Anforderungen: REQ-P06; Belege: B-BAT-009
## Frage
Nennspannung je Zelle der NMC-Variante?
## Alternativen
| Alternative | dafür | dagegen |
|---|---|---|
| siehe ENT-008 (Formatwahl) | | |
## Entscheidung und Begründung
W20 Tabelle 1 (Fenster 2,5–4,3 V). Ersetzt für diese Variante die Annahme 3,65 V (W10, NMC allgemein). Quelle: Cell Rep. Phys. Sci. 6, 102453 (2025), CC-BY, PDF in quellen/blade_zerlegung/ (W20, B-BAT-009).
## Folgen
Gilt nur für die Variante NMC. Bei 800 V (ENT-006): 217 Zellen in Reihe; Parallelzahl und Zellhalter folgen in G3/G4. Zellmaße Ø 46 × 80 mm brauchen eigene Merkmale im Bauteilbaum (ENT-012, vorgeschlagen).

---
*KI-generiert (Claude Opus, 2026-11-16).*

### ENT-011 Masse 4680: 355 g (2026-11-16, entschieden (Mensch), Autor (Wahl „Rundzelle 4680“, 2026-11-16) / Werte W20; Variante: NMC)
Merkmal: masse_g = 355.0 g; Anforderungen: REQ-P06; Belege: B-BAT-009
## Frage
Masse je Zelle der NMC-Variante?
## Alternativen
| Alternative | dafür | dagegen |
|---|---|---|
| siehe ENT-008 (Formatwahl) | | |
## Entscheidung und Begründung
W20 Tabelle 1 (241 Wh/kg, 643 Wh/L). Quelle: Cell Rep. Phys. Sci. 6, 102453 (2025), CC-BY, PDF in quellen/blade_zerlegung/ (W20, B-BAT-009).
## Folgen
Gilt nur für die Variante NMC. Bei 800 V (ENT-006): 217 Zellen in Reihe; Parallelzahl und Zellhalter folgen in G3/G4. Zellmaße Ø 46 × 80 mm brauchen eigene Merkmale im Bauteilbaum (ENT-012, vorgeschlagen).

---
*KI-generiert (Claude Opus, 2026-11-16).*

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

### ENT-014 Zellformat LFP: Blade-Querschnitt 90 × 14 mm, verkürzt (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Vorgang G1) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: LFP)
Merkmal: format = "prismatisch, Blade-Querschnitt, verkürzt" ; Anforderungen: REQ-P06, REQ-P07; Belege: B-BAT-009, B-BAT-012, B-BAT-013
## Frage
Zellformat LFP – welcher Wert für die Variante LFP?
## Alternativen
| Alternative | dafür | dagegen |
|---|---|---|
| gewählter Wert | belegt bzw. aus G1 abgeleitet | – |
| Originalzelle unverändert | Kaufteil | passt nicht zu 800 V / 73,9 kWh (B-BAT-009) |
## Entscheidung und Begründung
Querschnitt der gemessenen Blade-Zelle bleibt (W20: 965 × 90 × 14 mm), Länge folgt aus der Kapazität bei 800 V und 1p (ENT-006). Alternative Originalzelle 135 Ah: ergäbe 108 kWh statt 73,9 (B-BAT-009). Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025; quellen/blade_zerlegung/).
## Folgen
Geht über parameter_LFP.json in das parametrische Zell-CAD (G2) und die Packanordnung (G4).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-015 Zelllänge LFP 681 mm (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Vorgang G1) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: LFP)
Merkmal: laenge_mm = 681.0 mm; Anforderungen: REQ-P06, REQ-P07; Belege: B-BAT-009, B-BAT-012, B-BAT-013
## Frage
Zelllänge LFP 660 mm – welcher Wert für die Variante LFP?
## Alternativen
| Alternative | dafür | dagegen |
|---|---|---|
| gewählter Wert | belegt bzw. aus G1 abgeleitet | – |
| Originalzelle unverändert | Kaufteil | passt nicht zu 800 V / 73,9 kWh (B-BAT-009) |
## Entscheidung und Begründung
**Korrigiert 2026-11-17 (Opus):** Elektrodenlänge 899,5 mm × 92,375/135 = 615,5 mm, dazu die feste Endzone 965 − 899,5 = 65,5 mm (W20 Abb. 5: Pole, Halter, Stromschienen) → **681 mm**. Erste Fassung (660 mm) skalierte die Endzone mit und war zu kurz. **Annahme:** aktive Länge ∝ Kapazität. Zwei Reihen quer: 1362 mm ≤ 1370 mm innen nach ENT-030. Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025).
## Folgen
Geht über parameter_LFP.json in das parametrische Zell-CAD (G2) und die Packanordnung (G4).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-016 Zellhöhe (Merkmal breite) LFP 90 mm (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Vorgang G1) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: LFP)
Merkmal: breite_mm = 90.0 mm; Anforderungen: REQ-P06, REQ-P07; Belege: B-BAT-009, B-BAT-012, B-BAT-013
## Frage
Zellhöhe (Merkmal breite) LFP 90 mm – welcher Wert für die Variante LFP?
## Alternativen
| Alternative | dafür | dagegen |
|---|---|---|
| gewählter Wert | belegt bzw. aus G1 abgeleitet | – |
| Originalzelle unverändert | Kaufteil | passt nicht zu 800 V / 73,9 kWh (B-BAT-009) |
## Entscheidung und Begründung
Blade-Querschnitt gemessen (W20 Tabelle 1: Height 90 mm). Zelle steht hochkant; 90 + 30 mm Boden/Deckel = 120 ≤ 130 mm Bauraumhöhe. Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025; quellen/blade_zerlegung/).
## Folgen
Geht über parameter_LFP.json in das parametrische Zell-CAD (G2) und die Packanordnung (G4).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-017 Zelldicke LFP 14 mm (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Vorgang G1) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: LFP)
Merkmal: dicke_mm = 14.0 mm; Anforderungen: REQ-P06, REQ-P07; Belege: B-BAT-009, B-BAT-012, B-BAT-013
## Frage
Zelldicke LFP 14 mm – welcher Wert für die Variante LFP?
## Alternativen
| Alternative | dafür | dagegen |
|---|---|---|
| gewählter Wert | belegt bzw. aus G1 abgeleitet | – |
| Originalzelle unverändert | Kaufteil | passt nicht zu 800 V / 73,9 kWh (B-BAT-009) |
## Entscheidung und Begründung
W20 Tabelle 1 (14 mm; W03 nennt 13,5 mm für Gen 1 laut Hersteller – Messwert gewählt). 125 Zellen je Reihe + 1 mm Abstand = 1874 mm ≤ 1890 mm innen. Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025; quellen/blade_zerlegung/).
## Folgen
Geht über parameter_LFP.json in das parametrische Zell-CAD (G2) und die Packanordnung (G4).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-018 Zellkapazität LFP 92,4 Ah (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Vorgang G1) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: LFP)
Merkmal: kapazitaet_Ah = 92.4 Ah; Anforderungen: REQ-P06, REQ-P07; Belege: B-BAT-009, B-BAT-012, B-BAT-013
## Frage
Zellkapazität LFP 92,4 Ah – welcher Wert für die Variante LFP?
## Alternativen
| Alternative | dafür | dagegen |
|---|---|---|
| gewählter Wert | belegt bzw. aus G1 abgeleitet | – |
| Originalzelle unverändert | Kaufteil | passt nicht zu 800 V / 73,9 kWh (B-BAT-009) |
## Entscheidung und Begründung
73,9 kWh × 1000 / (250 × 3,2 V) = 92,375 Ah bei 1p (ENT-006, Fall A). Gilt für Fall A (1500 kg mit Batterie); Fall B passt nicht in den Bauraum (B-BAT-013). Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025; quellen/blade_zerlegung/).
## Folgen
Geht über parameter_LFP.json in das parametrische Zell-CAD (G2) und die Packanordnung (G4).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-019 Nennspannung LFP 3,2 V (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Vorgang G1) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: LFP)
Merkmal: nennspannung_V = 3.2 V; Anforderungen: REQ-P06, REQ-P07; Belege: B-BAT-009, B-BAT-012, B-BAT-013
## Frage
Nennspannung LFP 3,2 V – welcher Wert für die Variante LFP?
## Alternativen
| Alternative | dafür | dagegen |
|---|---|---|
| gewählter Wert | belegt bzw. aus G1 abgeleitet | – |
| Originalzelle unverändert | Kaufteil | passt nicht zu 800 V / 73,9 kWh (B-BAT-009) |
## Entscheidung und Begründung
W20 Tabelle 1 (3,2 V, Fenster 2,6–3,65 V), W01. Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025; quellen/blade_zerlegung/).
## Folgen
Geht über parameter_LFP.json in das parametrische Zell-CAD (G2) und die Packanordnung (G4).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-020 Zellmasse LFP etwa 1850 g (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Vorgang G1) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: LFP)
Merkmal: masse_g = 1850.0 g; Anforderungen: REQ-P06, REQ-P07; Belege: B-BAT-009, B-BAT-012, B-BAT-013
## Frage
Zellmasse LFP etwa 1850 g – welcher Wert für die Variante LFP?
## Alternativen
| Alternative | dafür | dagegen |
|---|---|---|
| gewählter Wert | belegt bzw. aus G1 abgeleitet | – |
| Originalzelle unverändert | Kaufteil | passt nicht zu 800 V / 73,9 kWh (B-BAT-009) |
## Entscheidung und Begründung
2,7 kg × 92,375/135 = 1847 g, gerundet 1850 g. **Annahme:** Masse ∝ Kapazität (Gehäuse leicht überschätzt). Ergibt 160 Wh/kg wie gemessen. Prüfung später am CAD (G2). Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025; quellen/blade_zerlegung/).
## Folgen
Geht über parameter_LFP.json in das parametrische Zell-CAD (G2) und die Packanordnung (G4).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-025 Zelldurchmesser 4680: 46 mm (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Vorgang G1) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: NMC)
Merkmal: durchmesser_mm = 46.0 mm; Anforderungen: REQ-P06, REQ-P07; Belege: B-BAT-009, B-BAT-012, B-BAT-013
## Frage
Zelldurchmesser 4680 – welcher Wert für die Variante NMC?
## Alternativen
| Alternative | dafür | dagegen |
|---|---|---|
| gewählter Wert | belegt bzw. aus G1 abgeleitet | – |
| Originalzelle unverändert | Kaufteil | – (bei 4680 ist die Kaufzelle gewählt, ENT-008) |
## Entscheidung und Begründung
W20: „a diameter of 46 mm and a height of 80 mm“; Merkmal neu durch ENT-012. Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025; quellen/blade_zerlegung/).
## Folgen
Geht über parameter_NMC.json in das parametrische Zell-CAD (G2) und die Packanordnung (G4).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-026 Zellhöhe 4680: 80 mm (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Vorgang G1) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: NMC)
Merkmal: hoehe_mm = 80.0 mm; Anforderungen: REQ-P06, REQ-P07; Belege: B-BAT-009, B-BAT-012, B-BAT-013
## Frage
Zellhöhe 4680 – welcher Wert für die Variante NMC?
## Alternativen
| Alternative | dafür | dagegen |
|---|---|---|
| gewählter Wert | belegt bzw. aus G1 abgeleitet | – |
| Originalzelle unverändert | Kaufteil | – (bei 4680 ist die Kaufzelle gewählt, ENT-008) |
## Entscheidung und Begründung
W20 (s. o.). Stehend: 80 + 30 mm = 110 ≤ 130 mm. Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025; quellen/blade_zerlegung/).
## Folgen
Geht über parameter_NMC.json in das parametrische Zell-CAD (G2) und die Packanordnung (G4).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

## Befund B-BAT-005
B-BAT-005 (2026-11-16) R4: Recherche geprüft, kein erfundener Wert, ein Spaltenfehler (PI), Wh/L-Frage bleibt offen
- Vorprüfung Sonnet (forschung/R4_vorpruefung.md, 5 min): 22 FEHLT-Zeilen = 21 Wortlaut abweichend, Wert im Rohtext / 0 Wert fehlt im Rohtext / 1 unklar (T07 Z7, ohne Zahl). Erwartung „keine erfundenen Zahlen, Wortlautfehler wie B-BAT-001“: erfüllt.
- Opus-Stichprobe an pakete/: W02 Z12 („100 to 250 W·h“ steht in Infobox, Zeile 94) ✓. W01 Z15 („Next gen: 180–205 Wh/kg“, Zeile 9) ✓. **W06 Z22 falsch zugeordnet:** Rohtext (Zeilen 10–18) Kopf „Li-NMC | LFP | …“, erster Block 150-275 / 150-220 / 165 = NMC, zweiter Block 80-150 / 210 / 90-160 / 135 = LFP. PI gab 150–220 als LFP aus (Fehler eines lokalen Agenten, Tabelle mit verlorenen Spaltengrenzen).
- W01 Z16 „LFP 227–396 Wh/L“: Rechenkommentar im Rohtext `3.96/((1.85/2)^2*3.14159*6.495/1000)` = 18650-Rundzelle. Für das Blade-Format gibt es keinen Wh/L-Wert. Die Chemiewahl LFP/NMC (B-BAT-004 Punkt 4) bleibt unbelegt.
- Ergebnis: forschung/R4_ergebnis.md (verwendbare Werte mit Bauteil/Merkmal, gesperrte Werte, Lücken mit Weg). Neue Quelle: Zerlegungsstudie Blade/4680 (doi:10.1016/j.xcrp.2025.102453, CC-BY), automatisch nicht abrufbar. Thema W18 (314-Ah-LFP-Zelle, thermisch) gestartet.
- Folge für PI-Aufträge: Tabellen ohne Spaltengrenzen sind fehleranfällig. pruefe.py findet das nicht, weil der Wert im Text steht. Vorgang: [R4]

## B-BAT-025 (2026-11-18) E2 Fortsetzung 2: NMC-Mäander machbar, LFP nicht; LFP-FPC pass

## Befund B-BAT-006
B-BAT-006) gilt nur mit den Herstellerwerten der 2. Generation.
- Folge 800 V (ENT-006): Eine Original-Blade-Zelle (135 Ah) gäbe 250s × 135 Ah × 3,2 V = 108 kWh. Nötig 92 Ah (A) → bei gleichem Querschnitt etwa 660 mm statt 965 mm Länge (G1).
- Werkzeuglücke: lauf.sh/AUFTRAG muss PI die genaue Quell-URL vorgeben; pruefe.py scheitert an zweispaltigem PDF-Satz (pdftotext -layout). Vorgang: [R4] [C0] [G1] [V1]

## B-BAT-008 (2026-11-16) W19 geprüft; Energiewiderspruch Stückliste 112 kWh gegen 73,9 kWh
- W19 (drpress HSET 2022, Studentenarbeit, Sekundärquelle): 20/20 Belege wörtlich bestätigt, inhaltlich schwach. **Gesperrt:** 332 Wh/kg „BYD battery“ (für LFP unplausibel, Bezug fehlt), 155 Wh/100 km Model Y (Einheit falsch), „ordinary 250 Wh/kg“ (Chemie offen), 180 Wh/kg „blade battery“ (Zelle oder Pack unklar). **Als Hinweis verwendbar (Pack, Sekundärquelle):** Volumennutzung Blade-Pack bis 60 %, konventionell etwa 40 %; Zelle ca. 0,6 m × 13,5 mm (Short Blade); Pack BYD Han ca. 79 kWh.
- Folge für den Bauraum: Bei 60 % Volumennutzung braucht die Zelle 357 Wh/L (Fall A) bzw. 427 Wh/L (Fall B). Das ist jetzt die Prüfgröße für die Blade-Zelle (Volumen Long Blade 1,166 L aus W03-Maßen). Die Blade-Kapazität (Ah) und damit die Wh/L der Zelle ist weiter **nicht belegt**.
- Sonnet-Umstellung (pm/AUFTRAG_LFP_UMSTELLUNG_ergebnis.txt): startwerte.json chemie = LFP (ENT-005 vor Bauraumregel), Warnung Bauraum offen; Obsidian 49 Bauteilnotizen (struktur.json hat 49 Einträge inkl. BT-000 und Ba

## Befund B-BAT-009
B-BAT-009 (2026-11-16) Zerlegungsstudie Blade (W20): Gen-1-Zelle 160 Wh/kg, 355 Wh/L; Bauraum Fall A genau an der Grenze
- Quelle: Cell Rep. Phys. Sci. 6, 102453 (2025), CC-BY, PDF vom Autor in quellen/blade_zerlegung/. PI-Lauf W20: 0/21, weil PI die DOI statt der file://-URL angab. Opus: URL ersetzt → 17/21; die 4 Reste stehen im Fließtext (pdftotext ohne -layout, zweispaltiger Satz). Z25 („around 23 of the heat“) gesperrt: Bruch bei der Textumwandlung verloren.
- **Blade-Zelle (gemessen, Tabelle 1):** 135 Ah, 432 Wh, 3,2 V, Fenster 2,6–3,65 V, 2,7 ± 0,3 kg, 1216 mL, **160 Wh/kg, 355,3 Wh/L**, 965 × 90 × 14 mm, Wandstärke Gehäuse 0,3 mm, ein Z-gefalteter Elektrodenstapel, Aktivmasse etwa 60 % der Zellmasse. Zum Vergleich Tesla 4680 (NMC811): 241 Wh/kg, 643 Wh/L.
- **Folge Bauraum:** 355 Wh/L × 60 % Volumennutzung (W19) = 213 Wh/L Pack. Nötig: 214 (Fall A), 256 (Fall B). Fall A passt knapp, Fall B nicht. Prüfpunkt von ENT-005 damit **an der Grenze, nicht klar erfüllt**.
- **Folge Masse:** 160 Wh/kg liegt unter dem C0-Band 185–210 (W03, Hersteller, Long Blade 2.0). Mit 160 Wh/kg, Zellanteil 0,75: Packmasse Fall A 616 kg (543–711), Fall B 739 kg. Eine 4680-NMC-Zelle ergäbe Fall A etwa 409 kg. Der Satz „kein belegter Massenunterschied“ (B-BAT-006) gilt nur mit den Herstellerwerten der 2. Generation.
- Folge 800 V (ENT-006): Eine Original-Blade-Zelle (135 Ah) gäbe 250s × 135 Ah × 3,2 V = 108 kWh. Nötig 92 Ah (A) → bei gleichem Querschnitt etwa 660 mm statt 965 mm Länge (G1).
- We

## Befund B-BAT-012
B-BAT-012 (2026-11-17) G1-Vorprüfung Zellanordnung: LFP-Blade passt nur ohne Zwischenraum, NMC-4680 mit Reserve
- Rechnung sim/geometrie/g1_anordnung/ (Sonnet; Opus Bild angesehen, Zählung NMC nachvollzogen: 32 Reihen × ~38 = 1200 Plätze).
- LFP A: 92,4 Ah → Zelle 660 × 90 × 14 mm, zwei Reihen quer (1320 ≤ 1340 mm). 125 Zellen je Reihe = 1874 mm gegen 1840 mm innen: passt nicht bei 1 mm Abstand; Grenze 0,73 mm. Blade-Zwischenlage (BT-220) und Wärmeschutz haben so keinen Platz. Höhe 120/130 mm passt.
- LFP B: 116,2 Ah → 831 mm, passt in keiner Lage. (Erwartung nannte 111 Ah/790 mm: Opus hatte die C0-Energie statt der C0b-Energie 93,0 kWh eingesetzt; Urteil unverändert.)
- NMC A: 868 von 1200 Plätzen (72 %), Höhenreserve 20 mm; NMC B: 1085 (90 %).
- Folge: Bestätigt C0b geometrisch. LFP braucht mehr Länge (≥ 1,93 m bei 1 mm), dünnere Rand-Annahme oder Fall A mit kleinerer Reichweite. Annahmen Rand 30 mm / Höhen bestätigt unkritisch; kritisch nur der LFP-Zellabstand. Vorgang: [G1] [G4]

## B-BAT-011 (2026-11-16) Variantenvergleich mit Messwerten: NMC-4680 ein Drittel leichter, LFP-Blade im Bauraum knapp
- Rechnung sim/chemie/varianten_lfp_nmc/ (Sonnet; Opus-Gegenrechnung gleich). Fall A: LFP 616 kg (160 Wh/kg gemessen; 469 kg bei 210 Gen 2), NMC 411 kg (217s×4p = 868 Zellen, 74,3 kWh). Anteil 41 % gegen 27 %.
- Fall B: LFP 93,0 kWh / 775 kg, NMC 86,6 kWh Bedarf, 5p → 92,8 kWh / 514 kg.
- Bauraum: LFP A −0,3 % (knapp), B nicht erfüllt; NMC erfüllt. Zyklen: LFP erfüllt, NMC unsich

## Befund B-BAT-013
B-BAT-013 (2026-11-17) Entscheidungen des Autors: ENT-012 freigegeben, Bauraum verlängert (ENT-013)
- Autor 2026-11-17: „ENT 012 ist freigegeben, verlängere den Bauraum, dokumentiere die entscheidungen“.
- ENT-012 (Baum mit Varianten, BT-250 Zellhalter) entschieden (Mensch). ENT-013: BT-000 bauraum_laenge_mm = 1950 mm für beide Varianten; Zahl von Opus aus G1 (1874 mm Stapel + 2 × 30 mm Rand = 1934 mm, + 16 mm Reserve). Breite 1400 und Höhe 130 mm bleiben Annahmen.
- Nachgeführt: Lastenheft REQ-P03 (800 V), REQ-P06 (zwei Varianten), REQ-P07 (L 1950 mm); docs/09 AEN-006…011; docs/04 (13 Akten, 0 Fehler).
- Neulauf (Sonnet, Opus nachgerechnet): nötig Fall A 208 Wh/L (vorher 214), LFP B 262; LFP A jetzt **erfüllt** (+2,3 %) und passt geometrisch mit 16 mm Reserve bei 1 mm Zellabstand. LFP B passt weiter nicht (Breite). NMC 1232 Plätze, Belegung 70/88 %. Massen unverändert. Erwartung (Nachtrag) erfüllt.
- Werkzeughinweis: erzeuge_bericht.py setzt die Kernaussage im Folienbaustein auf „(Opus)“ zurück → Skript muss vorhandene Kernaussage erhalten (offen für Sonnet). Vorgang: [G1] [V1] [C0]

## B-BAT-012 (2026-11-17) G1-Vorprüfung Zellanordnung: LFP-Blade passt nur ohne Zwischenraum, NMC-4680 mit Reserve
- Rechnung sim/geometrie/g1_anordnung/ (Sonnet; Opus Bild angesehen, Zählung NMC nachvollzogen: 32 Reihen × ~38 = 1200 Plätze).
- LFP A: 92,4 Ah → Zelle 660 × 90 × 14 mm, zwei Reihen quer (1320 ≤ 1340 mm). 125 Zellen je Reihe = 1874 mm gegen 1840 mm innen: passt nicht bei 1 mm Absta

