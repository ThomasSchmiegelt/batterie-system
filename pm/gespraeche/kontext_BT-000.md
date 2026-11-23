# Kontext für das Bauteilgespräch: BT-000 Batteriesystem

KI-generiert von pm.py aus Projektdateien (nur eigene Dokumente).

## Ich bin
Batteriesystem (BT-000). Aufgabe: Gesamtsystem im Fahrzeug. Teil von: –. Meine Teile: BT-100 Zelle, BT-200 Zellstack, BT-300 Regelung (BMS), BT-400 Verkabelung und Zellverbinder, BT-500 Struktur und Gehäuse, BT-600 Kühlung, BT-700 Zusatzkomponenten.

## Meine Merkmale (Wert und entscheidende Akte)
- energie_brutto_kWh: noch nicht entschieden  (–)
- nennspannung_V: 800.0 V (ENT-006)
- bauraum_laenge_mm: noch nicht entschieden  (–)
- bauraum_breite_mm: 1430.0 mm (ENT-030)
- bauraum_hoehe_mm: noch nicht entschieden  (–)
- masse_max_kg: noch nicht entschieden  (–)

## Anforderungen an mich (Lastenheft)
| REQ-P01 | Anwendung / Fahrzeugklasse | Pkw, Fahrzeugmasse etwa 1500 kg, Anhaltswert (Autor 2026-11-16); Auslegung rechnet Fall A (mit Batterie) und Fall B (ohne Batterie) als Spanne | Autor | Muss | Vorgabe Autor |
| REQ-P02 | nutzbarer Energieinhalt | aus Reichweite 400 km (Vorgabe Autor 2026-11-16) × Verbrauch (Annahme), Vergleich sim/chemie/vergleich_lfp_nmc | Autor | Muss | Reichweite: Vorgabe Autor |
| REQ-P03 | Systemspannung (Nenn, min, max) | 800 V nominal (ENT-006, Autor 2026-11-16); min/max folgen aus Zellfenster | Autor | Muss | teilweise |
| REQ-P07 | Bauraum (L × B × H) und Masse | L = 1950 mm (ENT-013, Autor 2026-11-17); B = 1430 mm (ENT-030, Autor 2026-11-17); H 130 mm Annahme; Masse offen (30 % Gesamtmasse als Annahme) | Autor | Muss | teilweise |

## Entscheidungen, die mich betreffen (vollständig)
### ENT-001 PI recherchiert ohne Werkzeuge in drei Stufen (2026-11-11, entschieden (Autor, Regel aus Moltbot 2026-11-11), Opus; Variante: alle)
Merkmal: - = None ; Anforderungen: REQ-D01, REQ-D07; Belege: –
## Frage
PI recherchiert ohne Werkzeuge in drei Stufen?
## Alternativen
| Alternative | dafür | dagegen |
|---|---|---|
| PI mit Shell (wie Fusion) | schneller, iterativ | sähe das ganze Home, eingeschleuste Befehle möglich |
## Entscheidung und Begründung
Fremde Texte können versteckte Anweisungen enthalten, eine Sandbox ist nicht verfügbar (bwrap durch AppArmor gesperrt). Ein Skript ohne KI holt die Texte, PI antwortet nur, pruefe.py prüft jedes Zitat.
## Folgen
siehe docs/05_risiken_fmea.md

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

### ENT-003 Opus leitet und verteilt an Sonnet, Haiku, PI ohne Rückfrage (2026-11-11, entschieden (Autor), Autor; Variante: alle)
Merkmal: - = None ; Anforderungen: REQ-D04, REQ-D10; Belege: –
## Frage
Opus leitet und verteilt an Sonnet, Haiku, PI ohne Rückfrage?
## Alternativen
| Alternative | dafür | dagegen |
|---|---|---|
| alles mit Opus | ein Modell, einfach | teuer, kein Test der Arbeitsteilung |
## Entscheidung und Begründung
Vorgabe des Autors 2026-11-11; Kosten; Test des gewerblichen Einsatzes.
## Folgen
siehe docs/05_risiken_fmea.md

### ENT-004 Bauteilbaum bis Stücklistenebene; Schutzteile in Schaltbox unter BT-700 (2026-11-16, entschieden (Mensch), Opus (Vorschlag) / Autor (Freigabe 2026-11-16); Variante: alle)
Merkmal: - = None ; Anforderungen: REQ-D11, REQ-D12, REQ-D13; Belege: B-BAT-004
## Frage
Wie fein wird der Bauteilbaum, damit jedes Teil der Batterie eine Akte und damit ein Maß fürs CAD bekommen kann? Und wohin gehören Schütze, Sicherung, Vorladung, Stecker und Entgasung, die bisher in BT-700 (struktur.json) und in BT-400/BT-500 (Stückliste) standen?
## Alternativen
| Alternative | dafür | dagegen |
|---|---|---|
| Baum bleibt bei 8 Baugruppen, Merkmale direkt an der Baugruppe (z. B. `quertraeger_breite_mm` an BT-500) | kein Umbau | sehr lange Merkmallisten; Bauteilgespräch und Video können einzelne Teile nicht zeigen; Stückliste und Baum bleiben getrennt |
| Baum bis Normteilebene (Schrauben, Dichtringe) | vollständig | viel Pflegeaufwand ohne Nutzen für Auslegung und Video; Autor: „muss nicht auf eine Schraube runtergebrochen werden“ (stueckliste.py) |
| **Baum bis Stücklistenebene (gewählt)**: je Stücklistenposition ein Bauteil, Zelle zusätzlich mit 4 Detailteilen fürs Video | jede Position hat Merkmale und Akte; `stueckliste.py` prüft die Zuordnung in beide Richtungen | 46 statt 8 Bauteile; Merkmale sind ein Vorschlag und wachsen mit der Auslegung |
| Schutzteile unter BT-400 lassen (wie Stückliste) | keine Umnummerierung | widerspricht der Rolle von BT-700 und Videoszene 7 (video/STORYBOARD.md) |
| **Schutzteile unter BT-700, Schütze, Vorladung und Sicherung in einer Schaltbox BT-710 (gewählt)** | folgt der ursprünglichen Bauteilrolle und dem Storyboard; die Schaltbox ist ein Bauraum, den G4 platzieren muss | Stückliste umnummeriert (400.4–400.9 und 500.7 → 700.2–700.8, alte 700.1–700.3 → 700.9–700.11, 500.8 → 500.7) |
## Entscheidung und Begründung
Vorschlag: `pm/bauteile/struktur.json` mit 46 Bauteilen (BT-000 bis BT-780). Jedes Bauteil der Stückliste trägt das Feld `stueckliste` mit seiner Position. `stueckliste.py` bricht ab, wenn eine Position kein Bauteil hat oder umgekehrt. Merkmale gibt es nur dort, wo CAD (Maße), Elektrik (Strom, Querschnitt), Kühlung oder Mechanik sie brauchen. Alle Werte sind `null`, bis eine eigene Akte entscheidet. Grund: REQ-D11 (CAD-Maße nur aus Akten) ist nur erfüllbar, wenn jedes Teil Merkmale hat (B-BAT-004 Punkt 1). REQ-D12 und REQ-D13 brauchen einzelne Teile zum Zeigen und Begründen.
Vorherige Fassung: Scratchpad-Sicherung `struktur_v1_2026-11-11.json`. Inhalt der 8 alten Bauteile unverändert, nur Merkmale ergänzt.
## Folgen
- Neue Merkmale an bestehenden Bauteilen: BT-000 (Energie, Spannung, Bauraum, Masse), BT-100 (format, nennspannung_V, masse_g), BT-200 (reihen_anzahl), BT-300 (architektur), BT-500 (bauweise), BT-600 (kuehlart).
- Gleiche Größe darf nur an einer Stelle entschieden werden. Zellzahl je Reihe: BT-210 `zellen_je_reihe`. Gesamtzahl: BT-200 `zellen_anzahl`. Querträgeranzahl: BT-530 `anzahl`. Die Folgegrößen rechnet ein Skript, nicht eine zweite Akte.
- Video (Szenen 1–8) und Bauteilgespräch können jetzt jedes Teil einzeln zeigen (`pm.py kontext BT-530`).
- Risiken: keine neuen.

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

### ENT-006 Systemspannung 800 V (250 LFP-Zellen in Reihe) (2026-11-16, entschieden (Mensch), Opus (Vorschlag) / Autor (Entscheidung 2026-11-16: „mach 800 Volt“); Variante: alle)
Merkmal: nennspannung_V = 800.0 V; Anforderungen: REQ-P02, REQ-P05, REQ-P06; Belege: B-BAT-006, B-BAT-008
## Frage
400 V oder 800 V? Mit LFP (ENT-005, 3,2 V je Zelle) und 73,9 kWh brutto (Fall A) legt die Spannung die Zellgröße fest. Die Stückliste rechnete mit angenommenen 140 Ah 112 kWh (B-BAT-008).
## Alternativen
| Alternative | dafür | dagegen |
|---|---|---|
| **800 V, 250s (gewählt)** | Schnellladen mit kleinerem Strom (CCS bis 1000 V, 500 A, W12); dünnere HV-Leitungen; Annahme in startwerte.py (> 150 kW Laden) | Zelle nur etwa 92 Ah (Fall A) bis 111 Ah (Fall B) bei 1p, kleiner als eine Long-Blade-Zelle; 250 Messkanäle im BMS |
| 400 V, 125s | Zelle etwa 185 Ah, nahe am Blade-Format | doppelter Strom beim Laden und Fahren, größere Querschnitte |
## Entscheidung und Begründung
Der Autor hat 800 V gewählt. Nennspannung 250 × 3,2 V = 800 V. Die Zellkapazität ist jetzt **keine Annahme mehr**, sondern folgt aus Energie und Spannung: E_brutto / (250 · 3,2 V) bei 1p. Festgelegt wird sie in G1 (Zellmaße, eigene Akte BT-100).
## Folgen
- BT-100: Kapazität und Zellmaße aus der Energie ableiten (G1). Eine Blade-Zelle in Originalgröße würde bei 250s zu viel Energie liefern → kürzere Zelle oder anderes Format (Zerlegungsstudie als Bezug).
- stueckliste.py: Ah je Zelle aus startwerte.json ableiten statt TAB-Annahme 140 Ah.
- BT-310 BMS: 250 Zellspannungen. BT-711/713 Schütze und Sicherung für 800 V DC. BT-410–430: Querschnitte für halben Strom gegenüber 400 V.

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

### ENT-013 Bauraumlänge 1950 mm (verlängert von 1900 mm), für beide Varianten (2026-11-17, entschieden (Mensch), Autor (Entscheidung 2026-11-17: „verlängere den Bauraum“) / Opus (Zahl 1950 aus G1-Vorprüfung); Variante: alle)
Merkmal: bauraum_laenge_mm = 1950.0 mm; Anforderungen: REQ-P07; Belege: B-BAT-012, B-BAT-011
## Frage
Die LFP-Blade-Variante passt in Fall A nicht in den angenommenen Bauraum 1900 × 1400 × 130 mm (B-BAT-012): 125 Zellen je Reihe × 14 mm + 124 × 1 mm Abstand = 1874 mm gegen 1840 mm innen. Wie kommt sie hinein?
## Alternativen
| Alternative | dafür | dagegen |
|---|---|---|
| **Bauraum verlängern (gewählt, Autor)** | Zwischenlage 1 mm bleibt (Wärme- und Brandschutz, Quellausgleich BT-220); Reichweite bleibt 400 km | Fahrzeug braucht 50 mm mehr Länge unter dem Boden; Packmasse +Rahmen |
| ohne Zwischenlage (≤ 0,73 mm) | Bauraum bleibt | kein Platz für Wärmeschutz und Zellquellung |
| kleinere Reichweite bei LFP | Bauraum bleibt | Varianten nicht mehr gleich spezifiziert |
## Entscheidung und Begründung
Der Autor hat entschieden, den Bauraum zu verlängern. Opus legt die Zahl fest: nötig 1874 mm innen + 2 × 30 mm Rand (Annahme) = 1934 mm; gewählt **1950 mm** (16 mm Reserve für Toleranzen und Zellquellung, Annahme). Gilt für **beide** Varianten, damit die Spezifikation gleich bleibt („mit den selben Spezifikationen“, Autor 2026-11-16). Breite 1400 mm und Höhe 130 mm bleiben **Annahmen** aus `startwerte.py` (keine Akte).
## Folgen
- LFP Fall A passt mit 1 mm Zellabstand (Reserve etwa 16 mm). LFP Fall B passt weiterhin nicht (Breite: Zelle 831 mm, zwei Reihen > 1340 mm). Bauraumvolumen 345,8 → 354,9 L, nötige Pack-Energiedichte Fall A sinkt von 214 auf etwa 208 Wh/L.
- NMC: mehr freie Plätze (Reserve wächst).
- Neu rechnen: G1-Vorprüfung, Variantenvergleich C0b (Bauraum aus parameter.json statt 1,9 m), Bilder.
- Lastenheft REQ-P07: Bauraumlänge 1950 mm (Autor), Breite/Höhe offen.

---
*KI-generiert (Claude Opus, 2026-11-17).*

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

### ENT-021 Elektrodenstapel LFP: ein Z-gefalteter Stapel (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Vorgang G1) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: LFP)
Merkmal: bauweise = "Z-gefalteter Einzelstapel" ; Anforderungen: REQ-P06, REQ-P07; Belege: B-BAT-009, B-BAT-012, B-BAT-013
## Frage
Elektrodenstapel LFP – welcher Wert für die Variante LFP?
## Alternativen
| Alternative | dafür | dagegen |
|---|---|---|
| gewählter Wert | belegt bzw. aus G1 abgeleitet | – |
| Originalzelle unverändert | Kaufteil | passt nicht zu 800 V / 73,9 kWh (B-BAT-009) |
## Entscheidung und Begründung
W20: „a single Z-folded electrode stack with 38 double-coated cathode sheets, 39 double-coated anode sheets“. Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025; quellen/blade_zerlegung/).
## Folgen
Geht über parameter_LFP.json in das parametrische Zell-CAD (G2) und die Packanordnung (G4).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-022 Kathodenlagen LFP 38 (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Vorgang G1) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: LFP)
Merkmal: lagen_anzahl = 38.0 ; Anforderungen: REQ-P06, REQ-P07; Belege: B-BAT-009, B-BAT-012, B-BAT-013
## Frage
Kathodenlagen LFP 38 – welcher Wert für die Variante LFP?
## Alternativen
| Alternative | dafür | dagegen |
|---|---|---|
| gewählter Wert | belegt bzw. aus G1 abgeleitet | – |
| Originalzelle unverändert | Kaufteil | passt nicht zu 800 V / 73,9 kWh (B-BAT-009) |
## Entscheidung und Begründung
W20 (38 Kathoden, 39 Anoden, 79 Separatorlagen). Gleicher Querschnitt → gleiche Lagenzahl, nur kürzer. Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025; quellen/blade_zerlegung/).
## Folgen
Geht über parameter_LFP.json in das parametrische Zell-CAD (G2) und die Packanordnung (G4).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-023 Zellgehäuse LFP Aluminium (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Vorgang G1) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: LFP)
Merkmal: werkstoff = "Aluminium, PET-Folie isoliert" ; Anforderungen: REQ-P06, REQ-P07; Belege: B-BAT-009, B-BAT-012, B-BAT-013
## Frage
Zellgehäuse LFP Aluminium – welcher Wert für die Variante LFP?
## Alternativen
| Alternative | dafür | dagegen |
|---|---|---|
| gewählter Wert | belegt bzw. aus G1 abgeleitet | – |
| Originalzelle unverändert | Kaufteil | passt nicht zu 800 V / 73,9 kWh (B-BAT-009) |
## Entscheidung und Begründung
W20: „The BYD cell’s aluminum housing is insulated with an adhesive polyethylene terephthalate (PET) foil“. Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025; quellen/blade_zerlegung/).
## Folgen
Geht über parameter_LFP.json in das parametrische Zell-CAD (G2) und die Packanordnung (G4).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-024 Gehäusewand LFP 0,3 mm (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Vorgang G1) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: LFP)
Merkmal: wandstaerke_mm = 0.3 mm; Anforderungen: REQ-P06, REQ-P07; Belege: B-BAT-009, B-BAT-012, B-BAT-013
## Frage
Gehäusewand LFP 0,3 mm – welcher Wert für die Variante LFP?
## Alternativen
| Alternative | dafür | dagegen |
|---|---|---|
| gewählter Wert | belegt bzw. aus G1 abgeleitet | – |
| Originalzelle unverändert | Kaufteil | passt nicht zu 800 V / 73,9 kWh (B-BAT-009) |
## Entscheidung und Begründung
W20 Tabelle 1 (Can wall thickness sides 0,3 mm). Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025; quellen/blade_zerlegung/).
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

### ENT-027 Elektrodenwickel 4680 (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Vorgang G1) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: NMC)
Merkmal: bauweise = "Wickel (jelly roll), tabless" ; Anforderungen: REQ-P06, REQ-P07; Belege: B-BAT-009, B-BAT-012, B-BAT-013
## Frage
Elektrodenwickel 4680 – welcher Wert für die Variante NMC?
## Alternativen
| Alternative | dafür | dagegen |
|---|---|---|
| gewählter Wert | belegt bzw. aus G1 abgeleitet | – |
| Originalzelle unverändert | Kaufteil | – (bei 4680 ist die Kaufzelle gewählt, ENT-008) |
## Entscheidung und Begründung
W20: „The Tesla 4680 cell features a jelly roll configuration“, tabless-Kontaktierung. Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025; quellen/blade_zerlegung/).
## Folgen
Geht über parameter_NMC.json in das parametrische Zell-CAD (G2) und die Packanordnung (G4).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-028 Zellgehäuse 4680 Stahl (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Vorgang G1) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: NMC)
Merkmal: werkstoff = "Stahl, vernickelt (vermutet)" ; Anforderungen: REQ-P06, REQ-P07; Belege: B-BAT-009, B-BAT-012, B-BAT-013
## Frage
Zellgehäuse 4680 Stahl – welcher Wert für die Variante NMC?
## Alternativen
| Alternative | dafür | dagegen |
|---|---|---|
| gewählter Wert | belegt bzw. aus G1 abgeleitet | – |
| Originalzelle unverändert | Kaufteil | – (bei 4680 ist die Kaufzelle gewählt, ENT-008) |
## Entscheidung und Begründung
W20: „(presumably) nickel-plated steel can“ – Quelle selbst unsicher. Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025; quellen/blade_zerlegung/).
## Folgen
Geht über parameter_NMC.json in das parametrische Zell-CAD (G2) und die Packanordnung (G4).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-029 Gehäusewand 4680 0,4 mm (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Vorgang G1) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: NMC)
Merkmal: wandstaerke_mm = 0.4 mm; Anforderungen: REQ-P06, REQ-P07; Belege: B-BAT-009, B-BAT-012, B-BAT-013
## Frage
Gehäusewand 4680 0,4 mm – welcher Wert für die Variante NMC?
## Alternativen
| Alternative | dafür | dagegen |
|---|---|---|
| gewählter Wert | belegt bzw. aus G1 abgeleitet | – |
| Originalzelle unverändert | Kaufteil | – (bei 4680 ist die Kaufzelle gewählt, ENT-008) |
## Entscheidung und Begründung
W20 Tabelle 1 (0,4 mm). Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025; quellen/blade_zerlegung/).
## Folgen
Geht über parameter_NMC.json in das parametrische Zell-CAD (G2) und die Packanordnung (G4).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-030 Bauraumbreite 1430 mm (verbreitert von 1400 mm), für beide Varianten (2026-11-17, entschieden (Mensch), Autor (Wahl 2026-11-17: „Bauraum breiter: 1430 mm“) / Opus (Zahl); Variante: alle)
Merkmal: bauraum_breite_mm = 1430.0 mm; Anforderungen: REQ-P07; Belege: B-BAT-015
## Frage
Laut Zerlegung (W20, Abb. 5) ist die Elektrode der Blade-Zelle 899,5 mm lang, die Zelle 965 mm: 65,5 mm Endzone (Pole, Kunststoffhalter, Stromschienen) bleiben beim Kürzen gleich. Für 92,4 Ah wird die LFP-Zelle deshalb 681 mm statt 660 mm lang (ENT-015 korrigiert). Zwei Reihen quer = 1362 mm > 1340 mm innen.
## Alternativen
| Alternative | dafür | dagegen |
|---|---|---|
| **Bauraum 1430 mm breit (gewählt, Autor)** | Spezifikation bleibt (400 km, 73,9 kWh), gleiche Lösung wie bei der Länge (ENT-013) | 30 mm mehr Fahrzeugbreite unter dem Boden |
| Zelle 660 mm, 89,2 Ah | Bauraum bleibt | 71,4 kWh (−3,4 %), ~386 km, Varianten ungleich |
| andere Anordnung | – | erst zu rechnen |
## Entscheidung und Begründung
Autor wählt den breiteren Bauraum. Zahl: 2 × 681 mm + 2 × 30 mm Rand (Annahme) = 1422 mm, gewählt 1430 mm (8 mm Reserve). Gilt für beide Varianten. Bauraum jetzt 1950 × 1430 × 130 mm (Höhe weiter Annahme).
## Folgen
Neu rechnen: G1-Anordnung, C0b (Volumen 362,5 L). NMC gewinnt Plätze. Lastenheft REQ-P07.

---
*KI-generiert (Claude Opus, 2026-11-17).*

### ENT-031 Bauteilbaum Innenaufbau der Zelle (BT-111…116, 121, 122, 131, 132; BT-140 lage) (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Innenaufbau) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: alle)
Merkmal: - = None ; Anforderungen: REQ-P06; Belege: B-BAT-015
## Frage
Bauteilbaum Innenaufbau der Zelle (BT-111…116, 121, 122, 131, 132; BT-140 lage) – welcher Wert?
## Entscheidung und Begründung
Autor: „kann man die zellen weiter detailieren … Isolatoren und so müssten ja auch noch rein“. Teile nach W20 Abb. 2 (alle inneren Komponenten beider Zellen). Baum jetzt 60 Einträge; BT-115 Wickelkern nur NMC, BT-121 Gehäusefolie nur LFP. Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025), Datei cad/zelle/aufbau_W20.json.
## Folgen
Detailliertes Zell-CAD (G2) und später Zellmodell (C1–C3: Schichtdicken, Flächen).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-032 Kathodenlänge LFP 615,5 mm (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Innenaufbau) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: LFP)
Merkmal: laenge_mm = 615.5 mm; Anforderungen: REQ-P06; Belege: B-BAT-015
## Frage
Kathodenlänge LFP 615,5 mm – welcher Wert für die Variante LFP?
## Entscheidung und Begründung
Original 899,5 mm (Abb.5A) × 92,375/135 (Annahme aktive Länge ∝ Ah). Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025), Datei cad/zelle/aufbau_W20.json.
## Folgen
Detailliertes Zell-CAD (G2) und später Zellmodell (C1–C3: Schichtdicken, Flächen).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-033 Kathodenbreite LFP 82,5 mm (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Innenaufbau) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: LFP)
Merkmal: breite_mm = 82.5 mm; Anforderungen: REQ-P06; Belege: B-BAT-015
## Frage
Kathodenbreite LFP 82,5 mm – welcher Wert für die Variante LFP?
## Entscheidung und Begründung
Abb.5A. Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025), Datei cad/zelle/aufbau_W20.json.
## Folgen
Detailliertes Zell-CAD (G2) und später Zellmodell (C1–C3: Schichtdicken, Flächen).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-034 Kathodenbeschichtung LFP 70 µm je Seite (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Innenaufbau) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: LFP)
Merkmal: beschichtung_um = 70.0 µm; Anforderungen: REQ-P06; Belege: B-BAT-015
## Frage
Kathodenbeschichtung LFP 70 µm je Seite – welcher Wert für die Variante LFP?
## Entscheidung und Begründung
Tab.1 (Einheit im Satz 'mm', gemeint µm). Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025), Datei cad/zelle/aufbau_W20.json.
## Folgen
Detailliertes Zell-CAD (G2) und später Zellmodell (C1–C3: Schichtdicken, Flächen).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-035 Al-Folie LFP 20 µm (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Innenaufbau) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: LFP)
Merkmal: folie_um = 20.0 µm; Anforderungen: REQ-P06; Belege: B-BAT-015
## Frage
Al-Folie LFP 20 µm – welcher Wert für die Variante LFP?
## Entscheidung und Begründung
Tab.1. Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025), Datei cad/zelle/aufbau_W20.json.
## Folgen
Detailliertes Zell-CAD (G2) und später Zellmodell (C1–C3: Schichtdicken, Flächen).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-036 Kathodenblätter LFP 38 (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Innenaufbau) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: LFP)
Merkmal: anzahl = 38.0 ; Anforderungen: REQ-P06; Belege: B-BAT-015
## Frage
Kathodenblätter LFP 38 – welcher Wert für die Variante LFP?
## Entscheidung und Begründung
Tab.1, Text. Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025), Datei cad/zelle/aufbau_W20.json.
## Folgen
Detailliertes Zell-CAD (G2) und später Zellmodell (C1–C3: Schichtdicken, Flächen).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-037 Kathodenfahne LFP 9 mm Überstand (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Innenaufbau) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: LFP)
Merkmal: fahne_mm = 9.0 mm; Anforderungen: REQ-P06; Belege: B-BAT-015
## Frage
Kathodenfahne LFP 9 mm Überstand – welcher Wert für die Variante LFP?
## Entscheidung und Begründung
Abb.5A nennt 27,1 und 9 mm; **Deutung Opus:** 9 mm Fahnenüberstand, 27,1 mm Fahnenzone mit Isolierbeschichtung. Unsicher. Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025), Datei cad/zelle/aufbau_W20.json.
## Folgen
Detailliertes Zell-CAD (G2) und später Zellmodell (C1–C3: Schichtdicken, Flächen).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-038 Anodenlänge LFP 620 mm (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Innenaufbau) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: LFP)
Merkmal: laenge_mm = 620.0 mm; Anforderungen: REQ-P06; Belege: B-BAT-015
## Frage
Anodenlänge LFP 620 mm – welcher Wert für die Variante LFP?
## Entscheidung und Begründung
Kathode + 4,5 mm (Original 904 gegen 899,5, Abb.5A). Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025), Datei cad/zelle/aufbau_W20.json.
## Folgen
Detailliertes Zell-CAD (G2) und später Zellmodell (C1–C3: Schichtdicken, Flächen).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-039 Anodenbreite LFP 85 mm (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Innenaufbau) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: LFP)
Merkmal: breite_mm = 85.0 mm; Anforderungen: REQ-P06; Belege: B-BAT-015
## Frage
Anodenbreite LFP 85 mm – welcher Wert für die Variante LFP?
## Entscheidung und Begründung
Abb.5A. Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025), Datei cad/zelle/aufbau_W20.json.
## Folgen
Detailliertes Zell-CAD (G2) und später Zellmodell (C1–C3: Schichtdicken, Flächen).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-040 Anodenbeschichtung LFP 65 µm je Seite (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Innenaufbau) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: LFP)
Merkmal: beschichtung_um = 65.0 µm; Anforderungen: REQ-P06; Belege: B-BAT-015
## Frage
Anodenbeschichtung LFP 65 µm je Seite – welcher Wert für die Variante LFP?
## Entscheidung und Begründung
Tab.1. Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025), Datei cad/zelle/aufbau_W20.json.
## Folgen
Detailliertes Zell-CAD (G2) und später Zellmodell (C1–C3: Schichtdicken, Flächen).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-041 Cu-Folie LFP 10 µm (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Innenaufbau) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: LFP)
Merkmal: folie_um = 10.0 µm; Anforderungen: REQ-P06; Belege: B-BAT-015
## Frage
Cu-Folie LFP 10 µm – welcher Wert für die Variante LFP?
## Entscheidung und Begründung
Tab.1. Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025), Datei cad/zelle/aufbau_W20.json.
## Folgen
Detailliertes Zell-CAD (G2) und später Zellmodell (C1–C3: Schichtdicken, Flächen).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-042 Anodenblätter LFP 39 (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Innenaufbau) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: LFP)
Merkmal: anzahl = 39.0 ; Anforderungen: REQ-P06; Belege: B-BAT-015
## Frage
Anodenblätter LFP 39 – welcher Wert für die Variante LFP?
## Entscheidung und Begründung
Tab.1, Text. Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025), Datei cad/zelle/aufbau_W20.json.
## Folgen
Detailliertes Zell-CAD (G2) und später Zellmodell (C1–C3: Schichtdicken, Flächen).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-043 Anodenfahne LFP 7 mm Überstand (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Innenaufbau) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: LFP)
Merkmal: fahne_mm = 7.0 mm; Anforderungen: REQ-P06; Belege: B-BAT-015
## Frage
Anodenfahne LFP 7 mm Überstand – welcher Wert für die Variante LFP?
## Entscheidung und Begründung
Abb.5A (20,5 und 7 mm), Deutung wie Kathode, unsicher. Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025), Datei cad/zelle/aufbau_W20.json.
## Folgen
Detailliertes Zell-CAD (G2) und später Zellmodell (C1–C3: Schichtdicken, Flächen).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-044 Separatorlänge (Faltbreite) LFP 631 mm (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Innenaufbau) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: LFP)
Merkmal: laenge_mm = 631.0 mm; Anforderungen: REQ-P06; Belege: B-BAT-015
## Frage
Separatorlänge (Faltbreite) LFP 631 mm – welcher Wert für die Variante LFP?
## Entscheidung und Begründung
Original 915 mm (Abb.5A), Überlänge 15,5 mm gegen Kathode beibehalten. Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025), Datei cad/zelle/aufbau_W20.json.
## Folgen
Detailliertes Zell-CAD (G2) und später Zellmodell (C1–C3: Schichtdicken, Flächen).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-045 Separatorbreite LFP 87 mm (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Innenaufbau) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: LFP)
Merkmal: breite_mm = 87.0 mm; Anforderungen: REQ-P06; Belege: B-BAT-015
## Frage
Separatorbreite LFP 87 mm – welcher Wert für die Variante LFP?
## Entscheidung und Begründung
Abb.5A (~87). Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025), Datei cad/zelle/aufbau_W20.json.
## Folgen
Detailliertes Zell-CAD (G2) und später Zellmodell (C1–C3: Schichtdicken, Flächen).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-046 Separator LFP 12 µm (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Innenaufbau) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: LFP)
Merkmal: dicke_um = 12.0 µm; Anforderungen: REQ-P06; Belege: B-BAT-015
## Frage
Separator LFP 12 µm – welcher Wert für die Variante LFP?
## Entscheidung und Begründung
Tab.1. Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025), Datei cad/zelle/aufbau_W20.json.
## Folgen
Detailliertes Zell-CAD (G2) und später Zellmodell (C1–C3: Schichtdicken, Flächen).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-047 Separatorlagen LFP 78 (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Innenaufbau) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: LFP)
Merkmal: lagen = 78.0 ; Anforderungen: REQ-P06; Belege: B-BAT-015
## Frage
Separatorlagen LFP 78 – welcher Wert für die Variante LFP?
## Entscheidung und Begründung
Tab.1 (Text: 79). Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025), Datei cad/zelle/aufbau_W20.json.
## Folgen
Detailliertes Zell-CAD (G2) und später Zellmodell (C1–C3: Schichtdicken, Flächen).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-048 Separator LFP Z-gefaltet (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Innenaufbau) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: LFP)
Merkmal: bauweise = "ein Band, Z-gefaltet, Rand laminiert" ; Anforderungen: REQ-P06; Belege: B-BAT-015
## Frage
Separator LFP Z-gefaltet – welcher Wert für die Variante LFP?
## Entscheidung und Begründung
Text. Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025), Datei cad/zelle/aufbau_W20.json.
## Folgen
Detailliertes Zell-CAD (G2) und später Zellmodell (C1–C3: Schichtdicken, Flächen).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-049 Isolierrand Kathode LFP 6,5 mm (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Innenaufbau) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: LFP)
Merkmal: breite_mm = 6.5 mm; Anforderungen: REQ-P06; Belege: B-BAT-015
## Frage
Isolierrand Kathode LFP 6,5 mm – welcher Wert für die Variante LFP?
## Entscheidung und Begründung
Abb.5A (rechts 6,5 mm Kathode, 4 mm Anode). Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025), Datei cad/zelle/aufbau_W20.json.
## Folgen
Detailliertes Zell-CAD (G2) und später Zellmodell (C1–C3: Schichtdicken, Flächen).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-050 Stapelfixierung LFP (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Innenaufbau) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: LFP)
Merkmal: art = "Kunststoffschiene, Klebeband, transparenter Isolationsbeutel" ; Anforderungen: REQ-P06; Belege: B-BAT-015
## Frage
Stapelfixierung LFP – welcher Wert für die Variante LFP?
## Entscheidung und Begründung
Text, Abb.2A. Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025), Datei cad/zelle/aufbau_W20.json.
## Folgen
Detailliertes Zell-CAD (G2) und später Zellmodell (C1–C3: Schichtdicken, Flächen).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-051 Gehäusefolie LFP PET (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Innenaufbau) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: LFP)
Merkmal: werkstoff = "PET-Klebefolie" ; Anforderungen: REQ-P06; Belege: B-BAT-015
## Frage
Gehäusefolie LFP PET – welcher Wert für die Variante LFP?
## Entscheidung und Begründung
Text. Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025), Datei cad/zelle/aufbau_W20.json.
## Folgen
Detailliertes Zell-CAD (G2) und später Zellmodell (C1–C3: Schichtdicken, Flächen).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-052 Füllöffnung LFP verschweißt (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Innenaufbau) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: LFP)
Merkmal: verschluss = "verschweißt, Gummistopfen" ; Anforderungen: REQ-P06; Belege: B-BAT-015
## Frage
Füllöffnung LFP verschweißt – welcher Wert für die Variante LFP?
## Entscheidung und Begründung
Text, Abb.4A. Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025), Datei cad/zelle/aufbau_W20.json.
## Folgen
Detailliertes Zell-CAD (G2) und später Zellmodell (C1–C3: Schichtdicken, Flächen).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-053 Innere Stromschiene LFP Al/Cu (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Innenaufbau) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: LFP)
Merkmal: werkstoff = "Al (Kathode) / Cu (Anode)" ; Anforderungen: REQ-P06; Belege: B-BAT-015
## Frage
Innere Stromschiene LFP Al/Cu – welcher Wert für die Variante LFP?
## Entscheidung und Begründung
Abb.2A, 4A (Busbar je Seite). Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025), Datei cad/zelle/aufbau_W20.json.
## Folgen
Detailliertes Zell-CAD (G2) und später Zellmodell (C1–C3: Schichtdicken, Flächen).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-054 Fügeverfahren Fahnen LFP (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Innenaufbau) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: LFP)
Merkmal: fuegeverfahren = "Fahnen Ultraschall verdichtet, an Stromschiene laser-geschweißt" ; Anforderungen: REQ-P06; Belege: B-BAT-015
## Frage
Fügeverfahren Fahnen LFP – welcher Wert für die Variante LFP?
## Entscheidung und Begründung
Text. Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025), Datei cad/zelle/aufbau_W20.json.
## Folgen
Detailliertes Zell-CAD (G2) und später Zellmodell (C1–C3: Schichtdicken, Flächen).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-055 Polisolation LFP (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Innenaufbau) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: LFP)
Merkmal: art = "zweiteiliger Kunststoffhalter, Gummi-O-Ring" ; Anforderungen: REQ-P06; Belege: B-BAT-015
## Frage
Polisolation LFP – welcher Wert für die Variante LFP?
## Entscheidung und Begründung
Text, Abb.2A. Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025), Datei cad/zelle/aufbau_W20.json.
## Folgen
Detailliertes Zell-CAD (G2) und später Zellmodell (C1–C3: Schichtdicken, Flächen).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-056 Ventil LFP seitlich (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Innenaufbau) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: LFP)
Merkmal: lage = "Stirnseite neben Kathodenpol (seitlich)" ; Anforderungen: REQ-P06; Belege: B-BAT-015
## Frage
Ventil LFP seitlich – welcher Wert für die Variante LFP?
## Entscheidung und Begründung
Text, Abb.2A. Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025), Datei cad/zelle/aufbau_W20.json.
## Folgen
Detailliertes Zell-CAD (G2) und später Zellmodell (C1–C3: Schichtdicken, Flächen).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-057 Kathodenlänge 4680 3215 mm (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Innenaufbau) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: NMC)
Merkmal: laenge_mm = 3215.0 mm; Anforderungen: REQ-P06; Belege: B-BAT-015
## Frage
Kathodenlänge 4680 3215 mm – welcher Wert für die Variante NMC?
## Entscheidung und Begründung
Abb.5B. Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025), Datei cad/zelle/aufbau_W20.json.
## Folgen
Detailliertes Zell-CAD (G2) und später Zellmodell (C1–C3: Schichtdicken, Flächen).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-058 Kathodenbreite 4680 72 mm (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Innenaufbau) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: NMC)
Merkmal: breite_mm = 72.0 mm; Anforderungen: REQ-P06; Belege: B-BAT-015
## Frage
Kathodenbreite 4680 72 mm – welcher Wert für die Variante NMC?
## Entscheidung und Begründung
Abb.5B. Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025), Datei cad/zelle/aufbau_W20.json.
## Folgen
Detailliertes Zell-CAD (G2) und später Zellmodell (C1–C3: Schichtdicken, Flächen).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-059 Kathodenbeschichtung 4680 75 µm je Seite (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Innenaufbau) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: NMC)
Merkmal: beschichtung_um = 75.0 µm; Anforderungen: REQ-P06; Belege: B-BAT-015
## Frage
Kathodenbeschichtung 4680 75 µm je Seite – welcher Wert für die Variante NMC?
## Entscheidung und Begründung
Tab.1. Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025), Datei cad/zelle/aufbau_W20.json.
## Folgen
Detailliertes Zell-CAD (G2) und später Zellmodell (C1–C3: Schichtdicken, Flächen).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-060 Al-Folie 4680 20 µm (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Innenaufbau) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: NMC)
Merkmal: folie_um = 20.0 µm; Anforderungen: REQ-P06; Belege: B-BAT-015
## Frage
Al-Folie 4680 20 µm – welcher Wert für die Variante NMC?
## Entscheidung und Begründung
Tab.1. Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025), Datei cad/zelle/aufbau_W20.json.
## Folgen
Detailliertes Zell-CAD (G2) und später Zellmodell (C1–C3: Schichtdicken, Flächen).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-061 Kathodenband 4680: 1 (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Innenaufbau) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: NMC)
Merkmal: anzahl = 1.0 ; Anforderungen: REQ-P06; Belege: B-BAT-015
## Frage
Kathodenband 4680: 1 – welcher Wert für die Variante NMC?
## Entscheidung und Begründung
Tab.1. Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025), Datei cad/zelle/aufbau_W20.json.
## Folgen
Detailliertes Zell-CAD (G2) und später Zellmodell (C1–C3: Schichtdicken, Flächen).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-062 Kathodenfahnen 4680 (tabless) 5 mm (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Innenaufbau) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: NMC)
Merkmal: fahne_mm = 5.0 mm; Anforderungen: REQ-P06; Belege: B-BAT-015
## Frage
Kathodenfahnen 4680 (tabless) 5 mm – welcher Wert für die Variante NMC?
## Entscheidung und Begründung
Abb.5B (2,5 / 5 mm), geschlitzter Folienrand. Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025), Datei cad/zelle/aufbau_W20.json.
## Folgen
Detailliertes Zell-CAD (G2) und später Zellmodell (C1–C3: Schichtdicken, Flächen).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-063 Anodenlänge 4680 3305 mm (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Innenaufbau) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: NMC)
Merkmal: laenge_mm = 3305.0 mm; Anforderungen: REQ-P06; Belege: B-BAT-015
## Frage
Anodenlänge 4680 3305 mm – welcher Wert für die Variante NMC?
## Entscheidung und Begründung
Abb.5B. Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025), Datei cad/zelle/aufbau_W20.json.
## Folgen
Detailliertes Zell-CAD (G2) und später Zellmodell (C1–C3: Schichtdicken, Flächen).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-064 Anodenbreite 4680 73 mm (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Innenaufbau) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: NMC)
Merkmal: breite_mm = 73.0 mm; Anforderungen: REQ-P06; Belege: B-BAT-015
## Frage
Anodenbreite 4680 73 mm – welcher Wert für die Variante NMC?
## Entscheidung und Begründung
Abb.5B. Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025), Datei cad/zelle/aufbau_W20.json.
## Folgen
Detailliertes Zell-CAD (G2) und später Zellmodell (C1–C3: Schichtdicken, Flächen).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-065 Anodenbeschichtung 4680 125 µm je Seite (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Innenaufbau) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: NMC)
Merkmal: beschichtung_um = 125.0 µm; Anforderungen: REQ-P06; Belege: B-BAT-015
## Frage
Anodenbeschichtung 4680 125 µm je Seite – welcher Wert für die Variante NMC?
## Entscheidung und Begründung
Tab.1. Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025), Datei cad/zelle/aufbau_W20.json.
## Folgen
Detailliertes Zell-CAD (G2) und später Zellmodell (C1–C3: Schichtdicken, Flächen).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-066 Cu-Folie 4680 10 µm (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Innenaufbau) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: NMC)
Merkmal: folie_um = 10.0 µm; Anforderungen: REQ-P06; Belege: B-BAT-015
## Frage
Cu-Folie 4680 10 µm – welcher Wert für die Variante NMC?
## Entscheidung und Begründung
Tab.1. Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025), Datei cad/zelle/aufbau_W20.json.
## Folgen
Detailliertes Zell-CAD (G2) und später Zellmodell (C1–C3: Schichtdicken, Flächen).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-067 Anodenband 4680: 1 (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Innenaufbau) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: NMC)
Merkmal: anzahl = 1.0 ; Anforderungen: REQ-P06; Belege: B-BAT-015
## Frage
Anodenband 4680: 1 – welcher Wert für die Variante NMC?
## Entscheidung und Begründung
Tab.1. Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025), Datei cad/zelle/aufbau_W20.json.
## Folgen
Detailliertes Zell-CAD (G2) und später Zellmodell (C1–C3: Schichtdicken, Flächen).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-068 Anodenfahnen 4680 (tabless) 7,5 mm (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Innenaufbau) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: NMC)
Merkmal: fahne_mm = 7.5 mm; Anforderungen: REQ-P06; Belege: B-BAT-015
## Frage
Anodenfahnen 4680 (tabless) 7,5 mm – welcher Wert für die Variante NMC?
## Entscheidung und Begründung
Abb.5B. Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025), Datei cad/zelle/aufbau_W20.json.
## Folgen
Detailliertes Zell-CAD (G2) und später Zellmodell (C1–C3: Schichtdicken, Flächen).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-069 Separatorlänge 4680 3550 mm (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Innenaufbau) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: NMC)
Merkmal: laenge_mm = 3550.0 mm; Anforderungen: REQ-P06; Belege: B-BAT-015
## Frage
Separatorlänge 4680 3550 mm – welcher Wert für die Variante NMC?
## Entscheidung und Begründung
Abb.5B. Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025), Datei cad/zelle/aufbau_W20.json.
## Folgen
Detailliertes Zell-CAD (G2) und später Zellmodell (C1–C3: Schichtdicken, Flächen).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-070 Separatorbreite 4680 75 mm (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Innenaufbau) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: NMC)
Merkmal: breite_mm = 75.0 mm; Anforderungen: REQ-P06; Belege: B-BAT-015
## Frage
Separatorbreite 4680 75 mm – welcher Wert für die Variante NMC?
## Entscheidung und Begründung
Abb.5B. Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025), Datei cad/zelle/aufbau_W20.json.
## Folgen
Detailliertes Zell-CAD (G2) und später Zellmodell (C1–C3: Schichtdicken, Flächen).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-071 Separator 4680 10 µm (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Innenaufbau) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: NMC)
Merkmal: dicke_um = 10.0 µm; Anforderungen: REQ-P06; Belege: B-BAT-015
## Frage
Separator 4680 10 µm – welcher Wert für die Variante NMC?
## Entscheidung und Begründung
Tab.1. Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025), Datei cad/zelle/aufbau_W20.json.
## Folgen
Detailliertes Zell-CAD (G2) und später Zellmodell (C1–C3: Schichtdicken, Flächen).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-072 Separatorlagen 4680: 2 (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Innenaufbau) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: NMC)
Merkmal: lagen = 2.0 ; Anforderungen: REQ-P06; Belege: B-BAT-015
## Frage
Separatorlagen 4680: 2 – welcher Wert für die Variante NMC?
## Entscheidung und Begründung
Tab.1. Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025), Datei cad/zelle/aufbau_W20.json.
## Folgen
Detailliertes Zell-CAD (G2) und später Zellmodell (C1–C3: Schichtdicken, Flächen).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-073 Separator 4680 gewickelt (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Innenaufbau) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: NMC)
Merkmal: bauweise = "zwei Bänder, mit Elektroden gewickelt" ; Anforderungen: REQ-P06; Belege: B-BAT-015
## Frage
Separator 4680 gewickelt – welcher Wert für die Variante NMC?
## Entscheidung und Begründung
Text. Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025), Datei cad/zelle/aufbau_W20.json.
## Folgen
Detailliertes Zell-CAD (G2) und später Zellmodell (C1–C3: Schichtdicken, Flächen).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-074 Wickelkern 4680 etwa Ø 12,5 mm (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Innenaufbau) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: NMC)
Merkmal: durchmesser_mm = 12.5 mm; Anforderungen: REQ-P06; Belege: B-BAT-015
## Frage
Wickelkern 4680 etwa Ø 14 mm – welcher Wert für die Variante NMC?
## Entscheidung und Begründung
**Korrigiert 2026-11-17 (Opus):** Abgeleitet aus der Querschnittsfläche **aller** Bänder: Kathode 3215 × 0,170 + Anode 3305 × 0,260 + 2 Separatoren 3550 × 0,010 = 1477 mm². Becher innen r = 22,6 mm → Kern Ø ≤ 12,75 mm; gewählt 12,5 mm (Außenradius 22,57 mm). Erste Fassung (14 mm) zählte nur die Kathode; das Detailmodell zeigte dann 1,15 mm Überstand (B-BAT-016). **Nicht gemessen**, W20: „Mitte leer“. Quelle: Zerlegung W20, cad/zelle/aufbau_W20.json.
## Folgen
Detailliertes Zell-CAD (G2) und später Zellmodell (C1–C3: Schichtdicken, Flächen).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-075 Wickelfixierung 4680 (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Innenaufbau) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: NMC)
Merkmal: art = "je ein Klebestreifen oben und unten" ; Anforderungen: REQ-P06; Belege: B-BAT-015
## Frage
Wickelfixierung 4680 – welcher Wert für die Variante NMC?
## Entscheidung und Begründung
Text. Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025), Datei cad/zelle/aufbau_W20.json.
## Folgen
Detailliertes Zell-CAD (G2) und später Zellmodell (C1–C3: Schichtdicken, Flächen).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-076 Füllöffnung 4680 Blindniet (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Innenaufbau) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: NMC)
Merkmal: verschluss = "Kupfer-Blindniet im Boden" ; Anforderungen: REQ-P06; Belege: B-BAT-015
## Frage
Füllöffnung 4680 Blindniet – welcher Wert für die Variante NMC?
## Entscheidung und Begründung
Text, Abb.2B. Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025), Datei cad/zelle/aufbau_W20.json.
## Folgen
Detailliertes Zell-CAD (G2) und später Zellmodell (C1–C3: Schichtdicken, Flächen).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-077 Tab-Scheiben 4680 (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Innenaufbau) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: NMC)
Merkmal: werkstoff = "Al-Tab-Scheibe oben (Kathode), Cu-Tab-Scheibe unten (Anode), je 6 Dreiecksflächen" ; Anforderungen: REQ-P06; Belege: B-BAT-015
## Frage
Tab-Scheiben 4680 – welcher Wert für die Variante NMC?
## Entscheidung und Begründung
Text, Abb.4B. Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025), Datei cad/zelle/aufbau_W20.json.
## Folgen
Detailliertes Zell-CAD (G2) und später Zellmodell (C1–C3: Schichtdicken, Flächen).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-078 Fügeverfahren 4680 (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Innenaufbau) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: NMC)
Merkmal: fuegeverfahren = "Laser auf Wickelstirn; Kathoden-Tab punktgeschweißt an Pol, Anoden-Tab an Becher" ; Anforderungen: REQ-P06; Belege: B-BAT-015
## Frage
Fügeverfahren 4680 – welcher Wert für die Variante NMC?
## Entscheidung und Begründung
Text. Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025), Datei cad/zelle/aufbau_W20.json.
## Folgen
Detailliertes Zell-CAD (G2) und später Zellmodell (C1–C3: Schichtdicken, Flächen).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-079 Polisolation 4680 (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Innenaufbau) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: NMC)
Merkmal: art = "Isolier-/Dichtring am Pluspol; Anoden-Kathoden-Isolation oben" ; Anforderungen: REQ-P06; Belege: B-BAT-015
## Frage
Polisolation 4680 – welcher Wert für die Variante NMC?
## Entscheidung und Begründung
Text, Abb.2B. Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025), Datei cad/zelle/aufbau_W20.json.
## Folgen
Detailliertes Zell-CAD (G2) und später Zellmodell (C1–C3: Schichtdicken, Flächen).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-080 Ventil 4680 im Boden (2026-11-17, entschieden (Mensch), Opus (Vorschlag, Innenaufbau) / Autor (Freigabe) / Autor (2026-11-17: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“); Variante: NMC)
Merkmal: lage = "Boden" ; Anforderungen: REQ-P06; Belege: B-BAT-015
## Frage
Ventil 4680 im Boden – welcher Wert für die Variante NMC?
## Entscheidung und Begründung
Text. Quelle: Zerlegung W20 (Cell Rep. Phys. Sci. 6, 102453, 2025), Datei cad/zelle/aufbau_W20.json.
## Folgen
Detailliertes Zell-CAD (G2) und später Zellmodell (C1–C3: Schichtdicken, Flächen).

---
*KI-generiert (Claude Opus, 2026-11-17). Status vorgeschlagen.*

### ENT-081 Kühlart Kühlplatte unten, für beide Varianten (2026-11-17, entschieden (Mensch), Autor (Entscheidung 2026-11-17: „Kühlplatte unten“); Variante: alle)
Merkmal: kuehlart = "Kühlplatte unten" ; Anforderungen: REQ-P09; Belege: B-BAT-017
## Frage
Wie werden die Zellen gekühlt? (K0-Fälle: K1 Boden, K2 4680 Mantel)
## Alternativen
| Alternative | dafür | dagegen |
|---|---|---|
| **Kühlplatte unten (gewählt, Autor)** | eine Platte für beide Varianten; LFP: Wärmeweg in der gut leitenden Ebene (90 mm); 4680: axial gut leitend | Wärme nur über eine Fläche; Spreizung über die Höhe |
| 4680 seitliche Kühlbänder | kurze Wege zum Mantel | radial schlecht leitend, aufwendig |
## Entscheidung und Begründung
Autor legt Kühlplatte unten fest, zusammen mit den Zielen REQ-P09: T_max ≤ 45 °C, Spreizung in der Zelle ≤ 5 K.
## Folgen
K0: Fall K1 ist der Hauptfall, K2 nur Vergleich. Folgt: Kühlplatte BT-610 auslegen (Kanäle, Durchfluss), Wärmeleitmaterial BT-230.

---
*KI-generiert (Claude Opus, 2026-11-17).*

### ENT-082 Querträger: Anzahl 3, quer zur Fahrtrichtung (2026-11-17, entschieden (Mensch), Opus (Vorschlag M0) / Autor (2026-11-17: „ja gehen wir ersteinmal so ins rennen“); Variante: alle)
Merkmal: anzahl = 3.0 ; Anforderungen: REQ-P07; Belege: W22, B-BAT-019
## Frage
Gehäuse-Vorauslegung M0 (sim/mechanik/m0_gehaeuse/).
## Entscheidung und Begründung
Annahme Opus: teilt die Länge in 4 Felder; Autor: „auch querstreben bei den rundzellen“. Ob 3 für den Seitencrash reichen, prüft X (Crash).
## Folgen
Gehäuse-CAD (G4), Crash X, Kühlplatte K2.

---
*KI-generiert (Claude Opus, 2026-11-17).*

### ENT-083 Querträger: Profilbreite 26 mm (2026-11-17, entschieden (Mensch), Opus (Vorschlag M0) / Autor (2026-11-17: „ja gehen wir ersteinmal so ins rennen“); Variante: alle)
Merkmal: breite_mm = 26.0 mm; Anforderungen: REQ-P07; Belege: W22
## Frage
Gehäuse-Vorauslegung M0 (sim/mechanik/m0_gehaeuse/).
## Entscheidung und Begründung
W22 (US9045030): Profil „approximately 54 millimeters high, 26 millimeters wide“.
## Folgen
Gehäuse-CAD (G4), Crash X, Kühlplatte K2.

---
*KI-generiert (Claude Opus, 2026-11-17).*

### ENT-084 Querträger: Profilhöhe 54 mm (2026-11-17, entschieden (Mensch), Opus (Vorschlag M0) / Autor (2026-11-17: „ja gehen wir ersteinmal so ins rennen“); Variante: alle)
Merkmal: hoehe_mm = 54.0 mm; Anforderungen: REQ-P07; Belege: W22
## Frage
Gehäuse-Vorauslegung M0 (sim/mechanik/m0_gehaeuse/).
## Entscheidung und Begründung
W22 (US9045030), passt unter Zellhöhe 80/90 mm.
## Folgen
Gehäuse-CAD (G4), Crash X, Kühlplatte K2.

---
*KI-generiert (Claude Opus, 2026-11-17).*

### ENT-085 Querträger: Wandstärke 2,5 mm (2026-11-17, entschieden (Mensch), Opus (Vorschlag M0) / Autor (2026-11-17: „ja gehen wir ersteinmal so ins rennen“); Variante: alle)
Merkmal: wandstaerke_mm = 2.5 mm; Anforderungen: REQ-P07; Belege: W22
## Frage
Gehäuse-Vorauslegung M0 (sim/mechanik/m0_gehaeuse/).
## Entscheidung und Begründung
W22: „wall thickness of between approximately 2 and 3 millimeters“; Mitte gewählt.
## Folgen
Gehäuse-CAD (G4), Crash X, Kühlplatte K2.

---
*KI-generiert (Claude Opus, 2026-11-17).*

### ENT-086 Querträger: Aluminium-Strangpressprofil (2026-11-17, entschieden (Mensch), Opus (Vorschlag M0) / Autor (2026-11-17: „ja gehen wir ersteinmal so ins rennen“); Variante: alle)
Merkmal: werkstoff = "Al-Strangpressprofil" ; Anforderungen: REQ-P07; Belege: W22
## Frage
Gehäuse-Vorauslegung M0 (sim/mechanik/m0_gehaeuse/).
## Entscheidung und Begründung
W22 (US20200148066): Alu-Strangpressprofil trägt die Seitenlast bei „>20% weight savings“ gegenüber Stahl.
## Folgen
Gehäuse-CAD (G4), Crash X, Kühlplatte K2.

---
*KI-generiert (Claude Opus, 2026-11-17).*

### ENT-087 Seitenrahmen: Breite 30 mm je Seite (2026-11-17, entschieden (Mensch), Opus (Vorschlag M0) / Autor (2026-11-17: „ja gehen wir ersteinmal so ins rennen“); Variante: alle)
Merkmal: breite_mm = 30.0 mm; Anforderungen: REQ-P07; Belege: B-BAT-019
## Frage
Gehäuse-Vorauslegung M0 (sim/mechanik/m0_gehaeuse/).
## Entscheidung und Begründung
Kein Beleg. Folgt aus fester Breite 1430 (Autor) − 2 × 681 mm LFP-Zellen − 2 × 4 mm Toleranz. Setzt voraus, dass der Fahrzeugschweller den Seitencrash größtenteils aufnimmt (Frage an Autor). M0: sim/mechanik/m0_gehaeuse/ergebnis.json.
## Folgen
Gehäuse-CAD (G4), Crash X, Kühlplatte K2.

---
*KI-generiert (Claude Opus, 2026-11-17).*

### ENT-088 Kühlart: Kühlplatte oben und unten (2026-11-17, entschieden (Mensch), Opus (Vorschlag M0) / Autor (2026-11-17: „ja gehen wir ersteinmal so ins rennen“); Variante: alle)
Merkmal: kuehlart = "Kühlplatte oben und unten" ; Anforderungen: REQ-P09; Belege: B-BAT-019
## Frage
Gehäuse-Vorauslegung M0 (sim/mechanik/m0_gehaeuse/).
## Entscheidung und Begründung
K1: nur so erfüllen beide Varianten REQ-P09 beim Schnellladen (LFP 20 min 33,8 °C/4,6 K; NMC 25 min 34,0 °C/3,8 K). sim/kuehlung/k1_schnellladen/DEUTUNG.md.
## Folgen
Gehäuse-CAD (G4), Crash X, Kühlplatte K2.

---
*KI-generiert (Claude Opus, 2026-11-17).*

### ENT-089 Kühlplatten: Anzahl 2 (oben, unten) (2026-11-17, entschieden (Mensch), Opus (Vorschlag M0) / Autor (2026-11-17: „ja gehen wir ersteinmal so ins rennen“); Variante: alle)
Merkmal: anzahl = 2.0 ; Anforderungen: REQ-P09; Belege: B-BAT-019
## Frage
Gehäuse-Vorauslegung M0 (sim/mechanik/m0_gehaeuse/).
## Entscheidung und Begründung
Folgt aus ENT-088.
## Folgen
Gehäuse-CAD (G4), Crash X, Kühlplatte K2.

---
*KI-generiert (Claude Opus, 2026-11-17).*

### ENT-090 Kühlplatte: Dicke 8 mm (2026-11-17, entschieden (Mensch), Opus (Vorschlag M0) / Autor (2026-11-17: „ja gehen wir ersteinmal so ins rennen“); Variante: alle)
Merkmal: dicke_mm = 8.0 mm; Anforderungen: REQ-P07; Belege: B-BAT-019
## Frage
Gehäuse-Vorauslegung M0 (sim/mechanik/m0_gehaeuse/).
## Entscheidung und Begründung
Annahme (Größenordnung aus Literatursuche, nicht zitatgeprüft). M0: Höhe LFP 121 mm ≤ 130, NMC 111 mm.
## Folgen
Gehäuse-CAD (G4), Crash X, Kühlplatte K2.

---
*KI-generiert (Claude Opus, 2026-11-17).*

### ENT-091 Bauraumlänge 2030 mm (wegen 3 Querträgern) (2026-11-17, entschieden (Mensch), Opus (Vorschlag M0) / Autor (2026-11-17: „ja gehen wir ersteinmal so ins rennen“); Variante: alle)
Merkmal: bauraum_laenge_mm = 2030.0 mm; Anforderungen: REQ-P07; Belege: B-BAT-019
## Frage
Gehäuse-Vorauslegung M0 (sim/mechanik/m0_gehaeuse/).
## Entscheidung und Begründung
M0: LFP-Gehäuselänge 2024 mm (1874 Zellen + 3 × 30 mm Querträger + 2 × 30 mm Rand); gerundet 2030. Gilt für beide Varianten (gleiche Spezifikation); NMC käme mit 1950 aus. Autor: „länge ist etwas einfacher“.
## Folgen
Gehäuse-CAD (G4), Crash X, Kühlplatte K2.

---
*KI-generiert (Claude Opus, 2026-11-17).*

### ENT-092 Zellhalter 4680: Kunststoffträger unten plus Verguss (2026-11-17, entschieden (Mensch), Opus (Vorschlag nach W24–W26, vergleich_rundzellen.md) / Autor (2026-11-17: „ja“); Variante: NMC)
Merkmal: anordnung = "Träger unten + Verguss" ; Anforderungen: REQ-P09; Belege: W26
## Entscheidung und Begründung
Belegt (W26, Tesla Model 3): Verguss (Potting) zwischen Zelle und Kühlsystem „zum Anbinden und Schutz“. Träger aus Kunststoff positioniert die Zellen im Raster aus M0 (Annahme). Werkstoffe PC/PU und Verguss­höhe: Annahme, später.
## Folgen
G4 Pack-CAD (Halter, Verbinder), E Querschnitt, K1b Wärme oben über Verbinder.

---
*KI-generiert (Claude Opus, 2026-11-17).*

### ENT-093 Zellverbinder 4680: einseitig oben, Al (2026-11-17, entschieden (Mensch), Opus (Vorschlag nach W24–W26, vergleich_rundzellen.md) / Autor (2026-11-17: „ja“); Variante: NMC)
Merkmal: werkstoff = "Al" ; Anforderungen: REQ-P09; Belege: W26
## Entscheidung und Begründung
Belegt: Lucid, Rivian, Tesla kontaktieren einseitig (W26); Lucid Al-Verbinder (W26). Plus am Deckelpol, Minus an der Becherschulter. Querschnitt folgt aus Elektrik E.
## Folgen
G4 Pack-CAD (Halter, Verbinder), E Querschnitt, K1b Wärme oben über Verbinder.

---
*KI-generiert (Claude Opus, 2026-11-17).*

### ENT-094 Zellverbinder 4680: Laserschweißen (2026-11-17, entschieden (Mensch), Opus (Vorschlag nach W24–W26, vergleich_rundzellen.md) / Autor (2026-11-17: „ja“); Variante: NMC)
Merkmal: verbindung = "Laserschweißen" ; Anforderungen: REQ-P09; Belege: B-BAT-020
## Entscheidung und Begründung
Annahme Opus (kein Zitatbeleg; Model 3 nutzt Al-Drahtbonden auf Ni-Stahl, W26). Bei 4680-Strömen (bis ≈ 50 A je Zelle beim Schnellladen) sind Drahtbonds knapp; Laser auf Verbinderblech. Prüfen in E.
## Folgen
G4 Pack-CAD (Halter, Verbinder), E Querschnitt, K1b Wärme oben über Verbinder.

---
*KI-generiert (Claude Opus, 2026-11-17).*

### ENT-095 Wärmeleitschicht oben: elektrisch isolierend über den Zellverbindern (2026-11-17, entschieden (Mensch), Opus (Vorschlag nach W24–W26, vergleich_rundzellen.md) / Autor (2026-11-17: „ja“); Variante: NMC)
Merkmal: werkstoff = "Gap-Pad, elektrisch isolierend" ; Anforderungen: REQ-P09; Belege: B-BAT-020
## Entscheidung und Begründung
Folgt aus ENT-088 (Kühlplatte oben) und ENT-093 (Verbinder oben). Wärme oben: Al-Ableiterscheibe → Deckel → Verbinder → Pad → Platte. Leitfähigkeit/Dicke Annahme, K1-Nachrechnung nötig.
## Folgen
G4 Pack-CAD (Halter, Verbinder), E Querschnitt, K1b Wärme oben über Verbinder.

---
*KI-generiert (Claude Opus, 2026-11-17).*

### ENT-096 Reihenverbinder Al 25 × 3 mm (75 mm²), beide Varianten (2026-11-17, entschieden (Mensch), Opus (Vorschlag nach E1, sim/elektrik/e1_querschnitte/ergebnis.json) / Autor (2026-11-17: „1 ja“); Variante: alle)
Merkmal: breite_mm = 25.0 mm; Anforderungen: REQ-P05; Belege: B-BAT-020
## Entscheidung und Begründung
E1: LFP 194 A Laden → 75 mm² bei 2,6 A/mm² (Annahme Richtwert). Für NMC-Gruppenverbinder gleiches Profil gewählt (Opus): senkt NMC-Verlust von 385 auf ≈ 285 W (< 300 W Annahmegrenze), ein Teil für beide Varianten. Stromdichte-Richtwerte und Leistungsannahmen (150 kW Spitze, 60 kW Dauer) sind Annahmen.
## Folgen
G4 Pack-CAD, Stückliste 400.x.

---
*KI-generiert (Claude Opus, 2026-11-17).*

### ENT-097 Reihenverbinder Dicke 3 mm (2026-11-17, entschieden (Mensch), Opus (Vorschlag nach E1, sim/elektrik/e1_querschnitte/ergebnis.json) / Autor (2026-11-17: „1 ja“); Variante: alle)
Merkmal: dicke_mm = 3.0 mm; Anforderungen: REQ-P05; Belege: B-BAT-020
## Entscheidung und Begründung
Siehe ENT-096. Stromdichte-Richtwerte und Leistungsannahmen (150 kW Spitze, 60 kW Dauer) sind Annahmen.
## Folgen
G4 Pack-CAD, Stückliste 400.x.

---
*KI-generiert (Claude Opus, 2026-11-17).*

### ENT-098 Reihenverbinder Werkstoff Al (2026-11-17, entschieden (Mensch), Opus (Vorschlag nach E1, sim/elektrik/e1_querschnitte/ergebnis.json) / Autor (2026-11-17: „1 ja“); Variante: alle)
Merkmal: werkstoff = "Al" ; Anforderungen: REQ-P05; Belege: B-BAT-020
## Entscheidung und Begründung
Wie Zellverbinder ENT-093 (Lucid Al, W26); gleiches Material vermeidet Kontaktkorrosion. Stromdichte-Richtwerte und Leistungsannahmen (150 kW Spitze, 60 kW Dauer) sind Annahmen.
## Folgen
G4 Pack-CAD, Stückliste 400.x.

---
*KI-generiert (Claude Opus, 2026-11-17).*

### ENT-099 Zellabgriff 4680: 12 × 1 mm Al (2026-11-17, entschieden (Mensch), Opus (Vorschlag nach E1, sim/elektrik/e1_querschnitte/ergebnis.json) / Autor (2026-11-17: „1 ja“); Variante: NMC)
Merkmal: breite_mm = 12.0 mm; Anforderungen: REQ-P05; Belege: B-BAT-020
## Entscheidung und Begründung
E1: 32 A Laden je Zelle (Spitze ≈ 58 A) → 12 mm². Stromdichte-Richtwerte und Leistungsannahmen (150 kW Spitze, 60 kW Dauer) sind Annahmen.
## Folgen
G4 Pack-CAD, Stückliste 400.x.

---
*KI-generiert (Claude Opus, 2026-11-17).*

### ENT-100 HV-Hauptleitung LFP 50 mm² Cu (2026-11-17, entschieden (Mensch), Opus (Vorschlag nach E1, sim/elektrik/e1_querschnitte/ergebnis.json) / Autor (2026-11-17: „1 ja“); Variante: LFP)
Merkmal: querschnitt_mm2 = 50.0 mm2; Anforderungen: REQ-P05; Belege: B-BAT-020
## Entscheidung und Begründung
E1: 194 A Laden, 4 A/mm² Richtwert (Annahme). Stromdichte-Richtwerte und Leistungsannahmen (150 kW Spitze, 60 kW Dauer) sind Annahmen.
## Folgen
G4 Pack-CAD, Stückliste 400.x.

---
*KI-generiert (Claude Opus, 2026-11-17).*

### ENT-101 HV-Hauptleitung NMC 35 mm² Cu (2026-11-17, entschieden (Mensch), Opus (Vorschlag nach E1, sim/elektrik/e1_querschnitte/ergebnis.json) / Autor (2026-11-17: „1 ja“); Variante: NMC)
Merkmal: querschnitt_mm2 = 35.0 mm2; Anforderungen: REQ-P05; Belege: B-BAT-020
## Entscheidung und Begründung
E1: 130 A Laden (30 min) bzw. Spitze 150 kW. Stromdichte-Richtwerte und Leistungsannahmen (150 kW Spitze, 60 kW Dauer) sind Annahmen.
## Folgen
G4 Pack-CAD, Stückliste 400.x.

---
*KI-generiert (Claude Opus, 2026-11-17).*

### ENT-102 Bauraumlänge LFP 2030 mm (eigenes Gehäuse je Variante) (2026-11-17, entschieden (Mensch), Autor (2026-11-17: „2 kürzer und eigenes gehäuse“) / Opus (Zahl); Variante: LFP)
Merkmal: bauraum_laenge_mm = 2030.0 mm; Anforderungen: REQ-P07; Belege: B-BAT-020
## Entscheidung und Begründung
Bisher gemeinsam (ENT-091). Autor 2026-11-17: „2 kürzer und eigenes gehäuse“ für NMC → 2030 mm gilt nur noch für LFP (M0: 2024 mm).
## Folgen
G4 neu (NMC-Gehäuse 1950 mm), Breite 1430 bleibt gemeinsam. Zweiter bewusster Variantenunterschied nach REQ-P05.

---
*KI-generiert (Claude Opus, 2026-11-17).*

### ENT-103 Bauraumlänge NMC 1950 mm (eigenes Gehäuse je Variante) (2026-11-17, entschieden (Mensch), Autor (2026-11-17: „2 kürzer und eigenes gehäuse“) / Opus (Zahl); Variante: NMC)
Merkmal: bauraum_laenge_mm = 1950.0 mm; Anforderungen: REQ-P07; Belege: B-BAT-020
## Entscheidung und Begründung
Autor 2026-11-17: „2 kürzer und eigenes gehäuse“. M0: 1120 Plätze bei 1950 mm mit 3 Querträgern für 868 Zellen. G4: Packfaktor 0,64 im LFP-Gehäuse; eigenes Gehäuse spart Masse.
## Folgen
G4 neu (NMC-Gehäuse 1950 mm), Breite 1430 bleibt gemeinsam. Zweiter bewusster Variantenunterschied nach REQ-P05.

---
*KI-generiert (Claude Opus, 2026-11-17).*

### ENT-104 Kühlplatte: Kanalbreite 4 mm (2026-11-17, vorgeschlagen, Opus (Vorschlag nach K2, sim/kuehlung/k2_kuehlplatte/ergebnis_nachtrag.json); Variante: alle)
Merkmal: kanal_breite_mm = 4.0 mm; Anforderungen: REQ-P09; Belege: B-BAT-021
## Entscheidung und Begründung
K2-Nachtrag (864 Varianten): nur 4-mm-Kanäle erreichen U ≥ 500 W/(m²K) bezogen auf die Grundfläche (LFP 595, NMC 565) bei Δp ≈ 0,005 bar; Mäander bringt kein höheres U (laminar), nur Druckverlust. Stegwirkungsgrad, Pad, k_Kühlmittel 0,40 sind Annahmen; Kontaktwiderstand Zelle–Pad fehlt noch. Fertigung (≈ 280 Kanäle je Platte, gelötet) offen.
## Folgen
K0/K1-Annahme h 500 bleibt gültig (U 565–595). Durchfluss: Autor-Frage (ΔT Kühlmittel 5 K → LFP 47 L/min; 10 K → 23 L/min, U unverändert, da laminar).

---
*KI-generiert (Claude Opus, 2026-11-17).*

### ENT-105 Kühlplatte: Kanalhöhe 5 mm (2026-11-17, vorgeschlagen, Opus (Vorschlag nach K2, sim/kuehlung/k2_kuehlplatte/ergebnis_nachtrag.json); Variante: alle)
Merkmal: kanal_hoehe_mm = 5.0 mm; Anforderungen: REQ-P09; Belege: B-BAT-021
## Entscheidung und Begründung
K2-Nachtrag (864 Varianten): nur 4-mm-Kanäle erreichen U ≥ 500 W/(m²K) bezogen auf die Grundfläche (LFP 595, NMC 565) bei Δp ≈ 0,005 bar; Mäander bringt kein höheres U (laminar), nur Druckverlust. Stegwirkungsgrad, Pad, k_Kühlmittel 0,40 sind Annahmen; Kontaktwiderstand Zelle–Pad fehlt noch. Fertigung (≈ 280 Kanäle je Platte, gelötet) offen.
## Folgen
K0/K1-Annahme h 500 bleibt gültig (U 565–595). Durchfluss: Autor-Frage (ΔT Kühlmittel 5 K → LFP 47 L/min; 10 K → 23 L/min, U unverändert, da laminar).

---
*KI-generiert (Claude Opus, 2026-11-17).*

### ENT-106 Kühlplatte: Werkstoff Al, gelötete Platte mit parallelen Kanälen quer (2026-11-17, vorgeschlagen, Opus (Vorschlag nach K2, sim/kuehlung/k2_kuehlplatte/ergebnis_nachtrag.json); Variante: alle)
Merkmal: werkstoff = "Al, gelötet, parallele Kanäle quer, 1 Durchgang" ; Anforderungen: REQ-P09; Belege: B-BAT-021
## Entscheidung und Begründung
K2-Nachtrag (864 Varianten): nur 4-mm-Kanäle erreichen U ≥ 500 W/(m²K) bezogen auf die Grundfläche (LFP 595, NMC 565) bei Δp ≈ 0,005 bar; Mäander bringt kein höheres U (laminar), nur Druckverlust. Stegwirkungsgrad, Pad, k_Kühlmittel 0,40 sind Annahmen; Kontaktwiderstand Zelle–Pad fehlt noch. Fertigung (≈ 280 Kanäle je Platte, gelötet) offen.
## Folgen
K0/K1-Annahme h 500 bleibt gültig (U 565–595). Durchfluss: Autor-Frage (ΔT Kühlmittel 5 K → LFP 47 L/min; 10 K → 23 L/min, U unverändert, da laminar).

---
*KI-generiert (Claude Opus, 2026-11-17).*

### ENT-107 Kühlmitteldurchfluss LFP 23 L/min beim Schnellladen (ΔT Kühlmittel 10 K) (2026-11-17, entschieden (Mensch), Opus (Vorschlag) / Autor (2026-11-17: „ja setzte deinen vorschlag um.“); Variante: LFP)
Merkmal: durchfluss_L_min = 23.0 L/min; Anforderungen: REQ-P09; Belege: B-BAT-021
## Entscheidung und Begründung
K2: laminar, U unabhängig vom Durchfluss. LFP 13,8 kW Wärme → 23 L/min bei 10 K Erwärmung (47 L/min für 5 K unrealistisch für Kompaktwagen); NMC 5,8 kW → 20 L/min bei 5 K. Die Erwärmung entlang des Packs addiert sich zur Zell-zu-Zell-Spreizung (nicht Teil von REQ-P09, das in der Zelle gilt).
## Folgen
Schnittstelle Fahrzeugkreis BT-660; Pumpe/Kühler im Fahrzeug.

---
*KI-generiert (Claude Opus, 2026-11-17).*

### ENT-108 Kühlmitteldurchfluss NMC 20 L/min beim Schnellladen (ΔT Kühlmittel 5 K) (2026-11-17, entschieden (Mensch), Opus (Vorschlag) / Autor (2026-11-17: „ja setzte deinen vorschlag um.“); Variante: NMC)
Merkmal: durchfluss_L_min = 20.0 L/min; Anforderungen: REQ-P09; Belege: B-BAT-021
## Entscheidung und Begründung
K2: laminar, U unabhängig vom Durchfluss. LFP 13,8 kW Wärme → 23 L/min bei 10 K Erwärmung (47 L/min für 5 K unrealistisch für Kompaktwagen); NMC 5,8 kW → 20 L/min bei 5 K. Die Erwärmung entlang des Packs addiert sich zur Zell-zu-Zell-Spreizung (nicht Teil von REQ-P09, das in der Zelle gilt).
## Folgen
Schnittstelle Fahrzeugkreis BT-660; Pumpe/Kühler im Fahrzeug.

---
*KI-generiert (Claude Opus, 2026-11-17).*

### ENT-109 Schaltbox auf dem Deckel vorne (Fall b), beide Varianten (2026-11-18, ersetzt, Opus (Vorschlag Fall a/b, ERW-E2) / Autor (2026-11-17: Fall b); Variante: LFP, NMC)
Merkmal: einbauort = deckel_vorne ; Anforderungen: REQ-P13; Belege: B-BAT-024
## Entscheidung und Begründung
Fall a (vordere Endzone) verlängert das Pack um Boxlänge + 10 mm, also ≥ 360 mm. Fall b (auf dem Deckel vorne) hält die Länge und kostet nur Höhe im vorderen Bereich, unter den Vordersitzen/Fußraum. Der Deckel über den Zellen bleibt frei für die obere Kühlplatte (ENT-088).
## Alternativen
a: in der vorderen Endzone im Pack (geschützt, aber länger). c: getrennt im Motorraum (lange HV-Leitungen, eigene Abdichtung).
## Folgen
Höhenzuwachs vorne (≤ 90 mm + Halter) im CAD melden. Durchführung HV/NV durch den Deckel, abgedichtet (BT-730/740).

---
*KI-generiert (Claude Opus, 2026-11-18).*

### ENT-110 Zentrales BMS mit Zellüberwachung (CMU) in isolierter Daisy-Chain (2026-11-18, vorgeschlagen, Opus (Annahme ERW-E2); Variante: alle)
Merkmal: architektur = zentral_BMS_CMU_Daisy-Chain ; Anforderungen: REQ-P15; Belege: B-BAT-024
## Frage
Auslegungswert architektur von BT-300 für E2 (Elektronik, Kabel).
## Alternativen
Keine geprüft; Annahme Opus (ERW-E2 Annahmen-Tabelle bzw. Nachtrag 1), Lehrbuch-/Gedächtniswissen, kein Beleg aus Recherche W27.
## Entscheidung und Begründung
Zentrales BMS mit Zellüberwachung (CMU) in isolierter Daisy-Chain. Herkunft: sim/elektrik/e2_elektronik/ERWARTUNG.md (ERW-E2). Status vorgeschlagen, Freigabe nur durch den Mensch.
## Folgen
Eingabe für cad/pack/pack.py (E2) und sim/elektrik/e2_elektronik/elektronik.py.

---
*KI-generiert (Claude Sonnet, 2026-11-18), im Auftrag von Opus.*

### ENT-111 CMU 18 Kanäle (2026-11-18, vorgeschlagen, Opus (Annahme ERW-E2); Variante: alle)
Merkmal: kanaele = 18.0 -; Anforderungen: REQ-P15; Belege: B-BAT-024
## Frage
Auslegungswert kanaele von BT-320 für E2 (Elektronik, Kabel).
## Alternativen
Keine geprüft; Annahme Opus (ERW-E2 Annahmen-Tabelle bzw. Nachtrag 1), Lehrbuch-/Gedächtniswissen, kein Beleg aus Recherche W27.
## Entscheidung und Begründung
CMU 18 Kanäle. Herkunft: sim/elektrik/e2_elektronik/ERWARTUNG.md (ERW-E2). Status vorgeschlagen, Freigabe nur durch den Mensch.
## Folgen
Eingabe für cad/pack/pack.py (E2) und sim/elektrik/e2_elektronik/elektronik.py.

---
*KI-generiert (Claude Sonnet, 2026-11-18), im Auftrag von Opus.*

### ENT-112 CMU-Anzahl LFP 14 (2026-11-18, vorgeschlagen, Opus (Annahme ERW-E2); Variante: LFP)
Merkmal: anzahl = 14.0 -; Anforderungen: REQ-P15; Belege: B-BAT-024
## Frage
Auslegungswert anzahl von BT-320 für E2 (Elektronik, Kabel).
## Alternativen
Keine geprüft; Annahme Opus (ERW-E2 Annahmen-Tabelle bzw. Nachtrag 1), Lehrbuch-/Gedächtniswissen, kein Beleg aus Recherche W27.
## Entscheidung und Begründung
CMU-Anzahl LFP 14. Herkunft: sim/elektrik/e2_elektronik/ERWARTUNG.md (ERW-E2). Status vorgeschlagen, Freigabe nur durch den Mensch.
## Folgen
Eingabe für cad/pack/pack.py (E2) und sim/elektrik/e2_elektronik/elektronik.py.

---
*KI-generiert (Claude Sonnet, 2026-11-18), im Auftrag von Opus.*

### ENT-113 CMU-Anzahl NMC 13 (2026-11-18, vorgeschlagen, Opus (Annahme ERW-E2); Variante: NMC)
Merkmal: anzahl = 13.0 -; Anforderungen: REQ-P15; Belege: B-BAT-024
## Frage
Auslegungswert anzahl von BT-320 für E2 (Elektronik, Kabel).
## Alternativen
Keine geprüft; Annahme Opus (ERW-E2 Annahmen-Tabelle bzw. Nachtrag 1), Lehrbuch-/Gedächtniswissen, kein Beleg aus Recherche W27.
## Entscheidung und Begründung
CMU-Anzahl NMC 13. Herkunft: sim/elektrik/e2_elektronik/ERWARTUNG.md (ERW-E2). Status vorgeschlagen, Freigabe nur durch den Mensch.
## Folgen
Eingabe für cad/pack/pack.py (E2) und sim/elektrik/e2_elektronik/elektronik.py.

---
*KI-generiert (Claude Sonnet, 2026-11-18), im Auftrag von Opus.*

### ENT-114 Zellausgleich passiv (2026-11-18, vorgeschlagen, Opus (Annahme ERW-E2); Variante: alle)
Merkmal: ausgleich = passiv ; Anforderungen: REQ-P15; Belege: B-BAT-024
## Frage
Auslegungswert ausgleich von BT-320 für E2 (Elektronik, Kabel).
## Alternativen
Keine geprüft; Annahme Opus (ERW-E2 Annahmen-Tabelle bzw. Nachtrag 1), Lehrbuch-/Gedächtniswissen, kein Beleg aus Recherche W27.
## Entscheidung und Begründung
Zellausgleich passiv. Herkunft: sim/elektrik/e2_elektronik/ERWARTUNG.md (ERW-E2). Status vorgeschlagen, Freigabe nur durch den Mensch.
## Folgen
Eingabe für cad/pack/pack.py (E2) und sim/elektrik/e2_elektronik/elektronik.py.

---
*KI-generiert (Claude Sonnet, 2026-11-18), im Auftrag von Opus.*

### ENT-115 Ausgleichsstrom 150 mA (2026-11-18, vorgeschlagen, Opus (Annahme ERW-E2); Variante: LFP)
Merkmal: ausgleichsstrom_mA = 150.0 mA; Anforderungen: REQ-P15; Belege: B-BAT-024
## Frage
Auslegungswert ausgleichsstrom_mA von BT-320 für E2 (Elektronik, Kabel).
## Alternativen
Keine geprüft; Annahme Opus (ERW-E2 Annahmen-Tabelle bzw. Nachtrag 1), Lehrbuch-/Gedächtniswissen, kein Beleg aus Recherche W27.
## Entscheidung und Begründung
Ausgleichsstrom 150 mA. Herkunft: sim/elektrik/e2_elektronik/ERWARTUNG.md (ERW-E2). Status vorgeschlagen, Freigabe nur durch den Mensch.
## Folgen
Eingabe für cad/pack/pack.py (E2) und sim/elektrik/e2_elektronik/elektronik.py.

---
*KI-generiert (Claude Sonnet, 2026-11-18), im Auftrag von Opus.*

### ENT-116 Temperaturfühler LFP 56 (4 je CMU) (2026-11-18, vorgeschlagen, Opus (Annahme ERW-E2); Variante: LFP)
Merkmal: anzahl = 56.0 -; Anforderungen: REQ-P15; Belege: B-BAT-024
## Frage
Auslegungswert anzahl von BT-330 für E2 (Elektronik, Kabel).
## Alternativen
Keine geprüft; Annahme Opus (ERW-E2 Annahmen-Tabelle bzw. Nachtrag 1), Lehrbuch-/Gedächtniswissen, kein Beleg aus Recherche W27.
## Entscheidung und Begründung
Temperaturfühler LFP 56 (4 je CMU). Herkunft: sim/elektrik/e2_elektronik/ERWARTUNG.md (ERW-E2). Status vorgeschlagen, Freigabe nur durch den Mensch.
## Folgen
Eingabe für cad/pack/pack.py (E2) und sim/elektrik/e2_elektronik/elektronik.py.

---
*KI-generiert (Claude Sonnet, 2026-11-18), im Auftrag von Opus.*

### ENT-117 Temperaturfühler NMC 52 (4 je CMU) (2026-11-18, vorgeschlagen, Opus (Annahme ERW-E2); Variante: NMC)
Merkmal: anzahl = 52.0 -; Anforderungen: REQ-P15; Belege: B-BAT-024
## Frage
Auslegungswert anzahl von BT-330 für E2 (Elektronik, Kabel).
## Alternativen
Keine geprüft; Annahme Opus (ERW-E2 Annahmen-Tabelle bzw. Nachtrag 1), Lehrbuch-/Gedächtniswissen, kein Beleg aus Recherche W27.
## Entscheidung und Begründung
Temperaturfühler NMC 52 (4 je CMU). Herkunft: sim/elektrik/e2_elektronik/ERWARTUNG.md (ERW-E2). Status vorgeschlagen, Freigabe nur durch den Mensch.
## Folgen
Eingabe für cad/pack/pack.py (E2) und sim/elektrik/e2_elektronik/elektronik.py.

---
*KI-generiert (Claude Sonnet, 2026-11-18), im Auftrag von Opus.*

### ENT-118 Strommessung Shunt plus Hall redundant (2026-11-18, vorgeschlagen, Opus (Annahme ERW-E2); Variante: alle)
Merkmal: prinzip = Shunt_Hall_redundant ; Anforderungen: REQ-P15; Belege: B-BAT-024
## Frage
Auslegungswert prinzip von BT-340 für E2 (Elektronik, Kabel).
## Alternativen
Keine geprüft; Annahme Opus (ERW-E2 Annahmen-Tabelle bzw. Nachtrag 1), Lehrbuch-/Gedächtniswissen, kein Beleg aus Recherche W27.
## Entscheidung und Begründung
Strommessung Shunt plus Hall redundant. Herkunft: sim/elektrik/e2_elektronik/ERWARTUNG.md (ERW-E2). Status vorgeschlagen, Freigabe nur durch den Mensch.
## Folgen
Eingabe für cad/pack/pack.py (E2) und sim/elektrik/e2_elektronik/elektronik.py.

---
*KI-generiert (Claude Sonnet, 2026-11-18), im Auftrag von Opus.*

### ENT-119 Strommessbereich ±500 A (2026-11-18, vorgeschlagen, Opus (Annahme ERW-E2); Variante: alle)
Merkmal: messbereich_A = 500.0 A; Anforderungen: REQ-P15; Belege: B-BAT-024
## Frage
Auslegungswert messbereich_A von BT-340 für E2 (Elektronik, Kabel).
## Alternativen
Keine geprüft; Annahme Opus (ERW-E2 Annahmen-Tabelle bzw. Nachtrag 1), Lehrbuch-/Gedächtniswissen, kein Beleg aus Recherche W27.
## Entscheidung und Begründung
Strommessbereich ±500 A. Herkunft: sim/elektrik/e2_elektronik/ERWARTUNG.md (ERW-E2). Status vorgeschlagen, Freigabe nur durch den Mensch.
## Folgen
Eingabe für cad/pack/pack.py (E2) und sim/elektrik/e2_elektronik/elektronik.py.

---
*KI-generiert (Claude Sonnet, 2026-11-18), im Auftrag von Opus.*

### ENT-120 Isolationswächter Warnschwelle 400 kΩ (500 Ω/V) (2026-11-18, vorgeschlagen, Opus (Annahme ERW-E2); Variante: alle)
Merkmal: ansprechwert_kOhm = 400.0 kOhm; Anforderungen: REQ-P13; Belege: B-BAT-024
## Frage
Auslegungswert ansprechwert_kOhm von BT-350 für E2 (Elektronik, Kabel).
## Alternativen
Keine geprüft; Annahme Opus (ERW-E2 Annahmen-Tabelle bzw. Nachtrag 1), Lehrbuch-/Gedächtniswissen, kein Beleg aus Recherche W27.
## Entscheidung und Begründung
Isolationswächter Warnschwelle 400 kΩ (500 Ω/V). Herkunft: sim/elektrik/e2_elektronik/ERWARTUNG.md (ERW-E2). Status vorgeschlagen, Freigabe nur durch den Mensch.
## Folgen
Eingabe für cad/pack/pack.py (E2) und sim/elektrik/e2_elektronik/elektronik.py.

---
*KI-generiert (Claude Sonnet, 2026-11-18), im Auftrag von Opus.*

### ENT-121 Messleitungen als flexible Leiterplatte (2026-11-18, vorgeschlagen, Opus (Annahme ERW-E2); Variante: alle)
Merkmal: art = FPC ; Anforderungen: REQ-P15; Belege: B-BAT-024
## Frage
Auslegungswert art von BT-360 für E2 (Elektronik, Kabel).
## Alternativen
Keine geprüft; Annahme Opus (ERW-E2 Annahmen-Tabelle bzw. Nachtrag 1), Lehrbuch-/Gedächtniswissen, kein Beleg aus Recherche W27.
## Entscheidung und Begründung
Messleitungen als flexible Leiterplatte. Herkunft: sim/elektrik/e2_elektronik/ERWARTUNG.md (ERW-E2). Status vorgeschlagen, Freigabe nur durch den Mensch.
## Folgen
Eingabe für cad/pack/pack.py (E2) und sim/elektrik/e2_elektronik/elektronik.py.

---
*KI-generiert (Claude Sonnet, 2026-11-18), im Auftrag von Opus.*

### ENT-122 Messleitung FPC Breite 20 mm (2026-11-18, vorgeschlagen, Opus (Annahme ERW-E2); Variante: NMC)
Merkmal: breite_mm = 20.0 mm; Anforderungen: REQ-P15; Belege: B-BAT-024
## Frage
Auslegungswert breite_mm von BT-360 für E2 (Elektronik, Kabel).
## Alternativen
Keine geprüft; Annahme Opus (ERW-E2 Annahmen-Tabelle bzw. Nachtrag 1), Lehrbuch-/Gedächtniswissen, kein Beleg aus Recherche W27.
## Entscheidung und Begründung
Messleitung FPC Breite 20 mm. Herkunft: sim/elektrik/e2_elektronik/ERWARTUNG.md (ERW-E2). Status vorgeschlagen, Freigabe nur durch den Mensch.
## Folgen
Eingabe für cad/pack/pack.py (E2) und sim/elektrik/e2_elektronik/elektronik.py.

---
*KI-generiert (Claude Sonnet, 2026-11-18), im Auftrag von Opus.*

### ENT-123 Hauptschütze 250 A (2026-11-18, vorgeschlagen, Opus (Annahme ERW-E2); Variante: alle)
Merkmal: nennstrom_A = 250.0 A; Anforderungen: REQ-P05; Belege: B-BAT-024
## Frage
Auslegungswert nennstrom_A von BT-711 für E2 (Elektronik, Kabel).
## Alternativen
Keine geprüft; Annahme Opus (ERW-E2 Annahmen-Tabelle bzw. Nachtrag 1), Lehrbuch-/Gedächtniswissen, kein Beleg aus Recherche W27.
## Entscheidung und Begründung
Hauptschütze 250 A. Herkunft: sim/elektrik/e2_elektronik/ERWARTUNG.md (ERW-E2). Status vorgeschlagen, Freigabe nur durch den Mensch.
## Folgen
Eingabe für cad/pack/pack.py (E2) und sim/elektrik/e2_elektronik/elektronik.py.

---
*KI-generiert (Claude Sonnet, 2026-11-18), im Auftrag von Opus.*

### ENT-124 Hauptschütze 1000 V DC (2026-11-18, vorgeschlagen, Opus (Annahme ERW-E2); Variante: alle)
Merkmal: nennspannung_V = 1000.0 V; Anforderungen: REQ-P03; Belege: B-BAT-024
## Frage
Auslegungswert nennspannung_V von BT-711 für E2 (Elektronik, Kabel).
## Alternativen
Keine geprüft; Annahme Opus (ERW-E2 Annahmen-Tabelle bzw. Nachtrag 1), Lehrbuch-/Gedächtniswissen, kein Beleg aus Recherche W27.
## Entscheidung und Begründung
Hauptschütze 1000 V DC. Herkunft: sim/elektrik/e2_elektronik/ERWARTUNG.md (ERW-E2). Status vorgeschlagen, Freigabe nur durch den Mensch.
## Folgen
Eingabe für cad/pack/pack.py (E2) und sim/elektrik/e2_elektronik/elektronik.py.

---
*KI-generiert (Claude Sonnet, 2026-11-18), im Auftrag von Opus.*

### ENT-125 Vorladewiderstand 100 Ω (2026-11-18, vorgeschlagen, Opus (Annahme ERW-E2); Variante: alle)
Merkmal: widerstand_Ohm = 100.0 Ohm; Anforderungen: REQ-P03; Belege: B-BAT-024
## Frage
Auslegungswert widerstand_Ohm von BT-712 für E2 (Elektronik, Kabel).
## Alternativen
Keine geprüft; Annahme Opus (ERW-E2 Annahmen-Tabelle bzw. Nachtrag 1), Lehrbuch-/Gedächtniswissen, kein Beleg aus Recherche W27.
## Entscheidung und Begründung
Vorladewiderstand 100 Ω. Herkunft: sim/elektrik/e2_elektronik/ERWARTUNG.md (ERW-E2). Status vorgeschlagen, Freigabe nur durch den Mensch.
## Folgen
Eingabe für cad/pack/pack.py (E2) und sim/elektrik/e2_elektronik/elektronik.py.

---
*KI-generiert (Claude Sonnet, 2026-11-18), im Auftrag von Opus.*

### ENT-126 Vorladezeit 300 ms (2026-11-18, vorgeschlagen, Opus (Annahme ERW-E2); Variante: alle)
Merkmal: vorladezeit_ms = 300.0 ms; Anforderungen: REQ-P03; Belege: B-BAT-024
## Frage
Auslegungswert vorladezeit_ms von BT-712 für E2 (Elektronik, Kabel).
## Alternativen
Keine geprüft; Annahme Opus (ERW-E2 Annahmen-Tabelle bzw. Nachtrag 1), Lehrbuch-/Gedächtniswissen, kein Beleg aus Recherche W27.
## Entscheidung und Begründung
Vorladezeit 300 ms. Herkunft: sim/elektrik/e2_elektronik/ERWARTUNG.md (ERW-E2). Status vorgeschlagen, Freigabe nur durch den Mensch.
## Folgen
Eingabe für cad/pack/pack.py (E2) und sim/elektrik/e2_elektronik/elektronik.py.

---
*KI-generiert (Claude Sonnet, 2026-11-18), im Auftrag von Opus.*

### ENT-127 Hauptsicherung Pyro- plus Schmelzsicherung (2026-11-18, vorgeschlagen, Opus (Annahme ERW-E2); Variante: alle)
Merkmal: art = Pyro_plus_Schmelzsicherung ; Anforderungen: REQ-P13; Belege: B-BAT-024
## Frage
Auslegungswert art von BT-713 für E2 (Elektronik, Kabel).
## Alternativen
Keine geprüft; Annahme Opus (ERW-E2 Annahmen-Tabelle bzw. Nachtrag 1), Lehrbuch-/Gedächtniswissen, kein Beleg aus Recherche W27.
## Entscheidung und Begründung
Hauptsicherung Pyro- plus Schmelzsicherung. Herkunft: sim/elektrik/e2_elektronik/ERWARTUNG.md (ERW-E2). Status vorgeschlagen, Freigabe nur durch den Mensch.
## Folgen
Eingabe für cad/pack/pack.py (E2) und sim/elektrik/e2_elektronik/elektronik.py.

---
*KI-generiert (Claude Sonnet, 2026-11-18), im Auftrag von Opus.*

### ENT-128 Hauptsicherung LFP 350 A (2026-11-18, vorgeschlagen, Opus (Annahme ERW-E2); Variante: LFP)
Merkmal: nennstrom_A = 350.0 A; Anforderungen: REQ-P13; Belege: B-BAT-024
## Frage
Auslegungswert nennstrom_A von BT-713 für E2 (Elektronik, Kabel).
## Alternativen
Keine geprüft; Annahme Opus (ERW-E2 Annahmen-Tabelle bzw. Nachtrag 1), Lehrbuch-/Gedächtniswissen, kein Beleg aus Recherche W27.
## Entscheidung und Begründung
Hauptsicherung LFP 350 A. Herkunft: sim/elektrik/e2_elektronik/ERWARTUNG.md (ERW-E2). Status vorgeschlagen, Freigabe nur durch den Mensch.
## Folgen
Eingabe für cad/pack/pack.py (E2) und sim/elektrik/e2_elektronik/elektronik.py.

---
*KI-generiert (Claude Sonnet, 2026-11-18), im Auftrag von Opus.*

### ENT-129 Hauptsicherung NMC 315 A (2026-11-18, vorgeschlagen, Opus (Annahme ERW-E2); Variante: NMC)
Merkmal: nennstrom_A = 315.0 A; Anforderungen: REQ-P13; Belege: B-BAT-024
## Frage
Auslegungswert nennstrom_A von BT-713 für E2 (Elektronik, Kabel).
## Alternativen
Keine geprüft; Annahme Opus (ERW-E2 Annahmen-Tabelle bzw. Nachtrag 1), Lehrbuch-/Gedächtniswissen, kein Beleg aus Recherche W27.
## Entscheidung und Begründung
Hauptsicherung NMC 315 A. Herkunft: sim/elektrik/e2_elektronik/ERWARTUNG.md (ERW-E2). Status vorgeschlagen, Freigabe nur durch den Mensch.
## Folgen
Eingabe für cad/pack/pack.py (E2) und sim/elektrik/e2_elektronik/elektronik.py.

---
*KI-generiert (Claude Sonnet, 2026-11-18), im Auftrag von Opus.*

### ENT-130 Service-Trennstecker 250 A (2026-11-18, vorgeschlagen, Opus (Annahme ERW-E2); Variante: alle)
Merkmal: nennstrom_A = 250.0 A; Anforderungen: REQ-P13; Belege: B-BAT-024
## Frage
Auslegungswert nennstrom_A von BT-720 für E2 (Elektronik, Kabel).
## Alternativen
Keine geprüft; Annahme Opus (ERW-E2 Annahmen-Tabelle bzw. Nachtrag 1), Lehrbuch-/Gedächtniswissen, kein Beleg aus Recherche W27.
## Entscheidung und Begründung
Service-Trennstecker 250 A. Herkunft: sim/elektrik/e2_elektronik/ERWARTUNG.md (ERW-E2). Status vorgeschlagen, Freigabe nur durch den Mensch.
## Folgen
Eingabe für cad/pack/pack.py (E2) und sim/elektrik/e2_elektronik/elektronik.py.

---
*KI-generiert (Claude Sonnet, 2026-11-18), im Auftrag von Opus.*

### ENT-131 Service-Trennstecker in der Mitte der Reihe (2026-11-18, vorgeschlagen, Opus (Annahme ERW-E2); Variante: NMC)
Merkmal: einbauort = reihenmitte ; Anforderungen: REQ-P13; Belege: B-BAT-024
## Frage
Auslegungswert einbauort von BT-720 für E2 (Elektronik, Kabel).
## Alternativen
Keine geprüft; Annahme Opus (ERW-E2 Annahmen-Tabelle bzw. Nachtrag 1), Lehrbuch-/Gedächtniswissen, kein Beleg aus Recherche W27.
## Entscheidung und Begründung
Service-Trennstecker in der Mitte der Reihe. Herkunft: sim/elektrik/e2_elektronik/ERWARTUNG.md (ERW-E2). Status vorgeschlagen, Freigabe nur durch den Mensch.
## Folgen
Eingabe für cad/pack/pack.py (E2) und sim/elektrik/e2_elektronik/elektronik.py.

---
*KI-generiert (Claude Sonnet, 2026-11-18), im Auftrag von Opus.*

### ENT-132 HV-Stecker Anzahl 2 (2026-11-18, vorgeschlagen, Opus (Annahme ERW-E2); Variante: alle)
Merkmal: anzahl = 2.0 -; Anforderungen: REQ-P13; Belege: B-BAT-024
## Frage
Auslegungswert anzahl von BT-730 für E2 (Elektronik, Kabel).
## Alternativen
Keine geprüft; Annahme Opus (ERW-E2 Annahmen-Tabelle bzw. Nachtrag 1), Lehrbuch-/Gedächtniswissen, kein Beleg aus Recherche W27.
## Entscheidung und Begründung
HV-Stecker Anzahl 2. Herkunft: sim/elektrik/e2_elektronik/ERWARTUNG.md (ERW-E2). Status vorgeschlagen, Freigabe nur durch den Mensch.
## Folgen
Eingabe für cad/pack/pack.py (E2) und sim/elektrik/e2_elektronik/elektronik.py.

---
*KI-generiert (Claude Sonnet, 2026-11-18), im Auftrag von Opus.*

### ENT-133 HV-Stecker Antrieb/Laden 250 A (2026-11-18, vorgeschlagen, Opus (Annahme ERW-E2); Variante: alle)
Merkmal: nennstrom_A = 250.0 A; Anforderungen: REQ-P13; Belege: B-BAT-024
## Frage
Auslegungswert nennstrom_A von BT-730 für E2 (Elektronik, Kabel).
## Alternativen
Keine geprüft; Annahme Opus (ERW-E2 Annahmen-Tabelle bzw. Nachtrag 1), Lehrbuch-/Gedächtniswissen, kein Beleg aus Recherche W27.
## Entscheidung und Begründung
HV-Stecker Antrieb/Laden 250 A. Herkunft: sim/elektrik/e2_elektronik/ERWARTUNG.md (ERW-E2). Status vorgeschlagen, Freigabe nur durch den Mensch.
## Folgen
Eingabe für cad/pack/pack.py (E2) und sim/elektrik/e2_elektronik/elektronik.py.

---
*KI-generiert (Claude Sonnet, 2026-11-18), im Auftrag von Opus.*

### ENT-134 NV-Stecker 26-polig (2026-11-18, vorgeschlagen, Opus (Annahme ERW-E2); Variante: alle)
Merkmal: polzahl = 26.0 -; Anforderungen: REQ-P13; Belege: B-BAT-024
## Frage
Auslegungswert polzahl von BT-740 für E2 (Elektronik, Kabel).
## Alternativen
Keine geprüft; Annahme Opus (ERW-E2 Annahmen-Tabelle bzw. Nachtrag 1), Lehrbuch-/Gedächtniswissen, kein Beleg aus Recherche W27.
## Entscheidung und Begründung
NV-Stecker 26-polig. Herkunft: sim/elektrik/e2_elektronik/ERWARTUNG.md (ERW-E2). Status vorgeschlagen, Freigabe nur durch den Mensch.
## Folgen
Eingabe für cad/pack/pack.py (E2) und sim/elektrik/e2_elektronik/elektronik.py.

---
*KI-generiert (Claude Sonnet, 2026-11-18), im Auftrag von Opus.*

### ENT-135 Heizung PTC im Kühlkreis (Fahrzeug) (2026-11-18, vorgeschlagen, Opus (Annahme ERW-E2); Variante: alle)
Merkmal: art = PTC_im_Kuehlkreis_Fahrzeug ; Anforderungen: REQ-P08; Belege: B-BAT-024
## Frage
Auslegungswert art von BT-760 für E2 (Elektronik, Kabel).
## Alternativen
Keine geprüft; Annahme Opus (ERW-E2 Annahmen-Tabelle bzw. Nachtrag 1), Lehrbuch-/Gedächtniswissen, kein Beleg aus Recherche W27.
## Entscheidung und Begründung
Heizung PTC im Kühlkreis (Fahrzeug). Herkunft: sim/elektrik/e2_elektronik/ERWARTUNG.md (ERW-E2). Status vorgeschlagen, Freigabe nur durch den Mensch.
## Folgen
Eingabe für cad/pack/pack.py (E2) und sim/elektrik/e2_elektronik/elektronik.py.

---
*KI-generiert (Claude Sonnet, 2026-11-18), im Auftrag von Opus.*

### ENT-136 Heizleistung 5 kW (2026-11-18, vorgeschlagen, Opus (Annahme ERW-E2); Variante: alle)
Merkmal: leistung_kW = 5.0 kW; Anforderungen: REQ-P08; Belege: B-BAT-024
## Frage
Auslegungswert leistung_kW von BT-760 für E2 (Elektronik, Kabel).
## Alternativen
Keine geprüft; Annahme Opus (ERW-E2 Annahmen-Tabelle bzw. Nachtrag 1), Lehrbuch-/Gedächtniswissen, kein Beleg aus Recherche W27.
## Entscheidung und Begründung
Heizleistung 5 kW. Herkunft: sim/elektrik/e2_elektronik/ERWARTUNG.md (ERW-E2). Status vorgeschlagen, Freigabe nur durch den Mensch.
## Folgen
Eingabe für cad/pack/pack.py (E2) und sim/elektrik/e2_elektronik/elektronik.py.

---
*KI-generiert (Claude Sonnet, 2026-11-18), im Auftrag von Opus.*

### ENT-137 Gas- und Drucksensor (2026-11-18, vorgeschlagen, Opus (Annahme ERW-E2); Variante: alle)
Merkmal: prinzip = Druck_plus_H2_CO2 ; Anforderungen: REQ-P11; Belege: B-BAT-024
## Frage
Auslegungswert prinzip von BT-770 für E2 (Elektronik, Kabel).
## Alternativen
Keine geprüft; Annahme Opus (ERW-E2 Annahmen-Tabelle bzw. Nachtrag 1), Lehrbuch-/Gedächtniswissen, kein Beleg aus Recherche W27.
## Entscheidung und Begründung
Gas- und Drucksensor. Herkunft: sim/elektrik/e2_elektronik/ERWARTUNG.md (ERW-E2). Status vorgeschlagen, Freigabe nur durch den Mensch.
## Folgen
Eingabe für cad/pack/pack.py (E2) und sim/elektrik/e2_elektronik/elektronik.py.

---
*KI-generiert (Claude Sonnet, 2026-11-18), im Auftrag von Opus.*

### ENT-138 BMS-Hauptsteuergerät auf dem Deckel hinten, in der Schaltbox (ENT-144) (2026-11-18, vorgeschlagen, Opus (Annahme ERW-E2); Variante: alle)
Merkmal: einbauort = deckel_hinten ; Anforderungen: REQ-P15; Belege: B-BAT-024
## Frage
Auslegungswert einbauort von BT-310 für E2 (Elektronik, Kabel).
## Alternativen
Keine geprüft; Annahme Opus (ERW-E2 Annahmen-Tabelle bzw. Nachtrag 1), Lehrbuch-/Gedächtniswissen, kein Beleg aus Recherche W27.
## Entscheidung und Begründung
BMS-Hauptsteuergerät auf dem Deckel vorne (Fall b). Herkunft: sim/elektrik/e2_elektronik/ERWARTUNG.md (ERW-E2). Status vorgeschlagen, Freigabe nur durch den Mensch.
## Folgen
Eingabe für cad/pack/pack.py (E2) und sim/elektrik/e2_elektronik/elektronik.py.

---
*KI-generiert (Claude Sonnet, 2026-11-18), im Auftrag von Opus.*

### ENT-139 BMS-Platine Länge 200 mm (2026-11-18, vorgeschlagen, Opus (Annahme ERW-E2); Variante: alle)
Merkmal: laenge_mm = 200.0 mm; Anforderungen: REQ-P15; Belege: B-BAT-024
## Frage
Auslegungswert laenge_mm von BT-310 für E2 (Elektronik, Kabel).
## Alternativen
Keine geprüft; Annahme Opus (ERW-E2 Annahmen-Tabelle bzw. Nachtrag 1), Lehrbuch-/Gedächtniswissen, kein Beleg aus Recherche W27.
## Entscheidung und Begründung
BMS-Platine Länge 200 mm. Herkunft: sim/elektrik/e2_elektronik/ERWARTUNG.md (ERW-E2). Status vorgeschlagen, Freigabe nur durch den Mensch.
## Folgen
Eingabe für cad/pack/pack.py (E2) und sim/elektrik/e2_elektronik/elektronik.py.

---
*KI-generiert (Claude Sonnet, 2026-11-18), im Auftrag von Opus.*

### ENT-140 BMS-Platine Breite 150 mm (2026-11-18, vorgeschlagen, Opus (Annahme ERW-E2); Variante: alle)
Merkmal: breite_mm = 150.0 mm; Anforderungen: REQ-P15; Belege: B-BAT-024
## Frage
Auslegungswert breite_mm von BT-310 für E2 (Elektronik, Kabel).
## Alternativen
Keine geprüft; Annahme Opus (ERW-E2 Annahmen-Tabelle bzw. Nachtrag 1), Lehrbuch-/Gedächtniswissen, kein Beleg aus Recherche W27.
## Entscheidung und Begründung
BMS-Platine Breite 150 mm. Herkunft: sim/elektrik/e2_elektronik/ERWARTUNG.md (ERW-E2). Status vorgeschlagen, Freigabe nur durch den Mensch.
## Folgen
Eingabe für cad/pack/pack.py (E2) und sim/elektrik/e2_elektronik/elektronik.py.

---
*KI-generiert (Claude Sonnet, 2026-11-18), im Auftrag von Opus.*

### ENT-141 BMS-Platine Höhe 20 mm (2026-11-18, vorgeschlagen, Opus (Annahme ERW-E2); Variante: alle)
Merkmal: hoehe_mm = 20.0 mm; Anforderungen: REQ-P15; Belege: B-BAT-024
## Frage
Auslegungswert hoehe_mm von BT-310 für E2 (Elektronik, Kabel).
## Alternativen
Keine geprüft; Annahme Opus (ERW-E2 Annahmen-Tabelle bzw. Nachtrag 1), Lehrbuch-/Gedächtniswissen, kein Beleg aus Recherche W27.
## Entscheidung und Begründung
BMS-Platine Höhe 20 mm. Herkunft: sim/elektrik/e2_elektronik/ERWARTUNG.md (ERW-E2). Status vorgeschlagen, Freigabe nur durch den Mensch.
## Folgen
Eingabe für cad/pack/pack.py (E2) und sim/elektrik/e2_elektronik/elektronik.py.

---
*KI-generiert (Claude Sonnet, 2026-11-18), im Auftrag von Opus.*

### ENT-142 HV-Leitung Biegeradius 5×D = 70 mm (LFP) (2026-11-18, vorgeschlagen, Opus (Annahme ERW-E2); Variante: LFP)
Merkmal: biegeradius_min_mm = 70.0 mm; Anforderungen: REQ-P13; Belege: B-BAT-024
## Frage
Auslegungswert biegeradius_min_mm von BT-430 für E2 (Elektronik, Kabel).
## Alternativen
Keine geprüft; Annahme Opus (ERW-E2 Annahmen-Tabelle bzw. Nachtrag 1), Lehrbuch-/Gedächtniswissen, kein Beleg aus Recherche W27.
## Entscheidung und Begründung
HV-Leitung Biegeradius 5×D = 70 mm (LFP). Herkunft: sim/elektrik/e2_elektronik/ERWARTUNG.md (ERW-E2). Status vorgeschlagen, Freigabe nur durch den Mensch.
## Folgen
Eingabe für cad/pack/pack.py (E2) und sim/elektrik/e2_elektronik/elektronik.py.

---
*KI-generiert (Claude Sonnet, 2026-11-18), im Auftrag von Opus.*

### ENT-143 HV-Leitung Biegeradius 5×D = 60 mm (NMC) (2026-11-18, vorgeschlagen, Opus (Annahme ERW-E2); Variante: NMC)
Merkmal: biegeradius_min_mm = 60.0 mm; Anforderungen: REQ-P13; Belege: B-BAT-024
## Frage
Auslegungswert biegeradius_min_mm von BT-430 für E2 (Elektronik, Kabel).
## Alternativen
Keine geprüft; Annahme Opus (ERW-E2 Annahmen-Tabelle bzw. Nachtrag 1), Lehrbuch-/Gedächtniswissen, kein Beleg aus Recherche W27.
## Entscheidung und Begründung
HV-Leitung Biegeradius 5×D = 60 mm (NMC). Herkunft: sim/elektrik/e2_elektronik/ERWARTUNG.md (ERW-E2). Status vorgeschlagen, Freigabe nur durch den Mensch.
## Folgen
Eingabe für cad/pack/pack.py (E2) und sim/elektrik/e2_elektronik/elektronik.py.

---
*KI-generiert (Claude Sonnet, 2026-11-18), im Auftrag von Opus.*

### ENT-144 Schaltbox auf dem Deckel hinten, unter der Rücksitzbank (Turm 89 mm), beide Varianten (2026-11-18, entschieden (Mensch), Opus (Vorschlag Turm) / Autor (2026-11-18: „ja, das ist ok. das wird unter der rücksitzbank verortet.“); Variante: LFP, NMC)
Merkmal: einbauort = deckel_hinten ; Anforderungen: REQ-P13; Belege: B-BAT-024
## Entscheidung und Begründung
Fall a (vordere Endzone) verlängert das Pack um Boxlänge + 10 mm, also ≥ 360 mm. Fall b (auf dem Deckel) hält die Länge. Die Box steht als Turm am hinteren Packende unter der Rücksitzbank, dort darf die Packhöhe lokal 210 mm statt 130 mm betragen (Autor 2026-11-18). Ersetzt ENT-109 (vorne). Der Deckel über den Zellen bleibt frei für die obere Kühlplatte (ENT-088).
## Alternativen
a: in der vorderen Endzone im Pack (geschützt, aber länger). c: getrennt im Motorraum (lange HV-Leitungen, eigene Abdichtung).
## Folgen
Turm 89 mm über dem Deckel hinten (CAD E2). Verschaltungsfolge so, dass Plus, Minus und Mitte hinten liegen. Durchführung HV/NV durch den Deckel, abgedichtet (BT-730/740).

---
*KI-generiert (Claude Opus, 2026-11-18).*

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

### ENT-146 Ausgleichsstrom NMC 130 mA (2026-11-18, vorgeschlagen, Opus (Annahme, AUFTRAG E2 Fortsetzung 2); Variante: NMC)
Merkmal: ausgleichsstrom_mA = 130.0 mA; Anforderungen: REQ-P15; Belege: B-BAT-024
## Frage
Ausgleichsstrom der NMC-Zellüberwachung (BT-320). Bei 150 mA und Höchstspannung 4,2 V erzeugt eine CMU mit 18 Kanälen 11,34 W (ENT-115, ERW-E2 Punkt 2, sim/elektrik/e2_elektronik/ergebnis.json), das Band war ≤ 10 W.
## Alternativen
150 mA beibehalten (CMU 11,34 W, Erwartung verfehlt); 130 mA (diese Akte).
## Entscheidung und Begründung
130 mA nur für NMC. CMU-Wärme ≈ 9,8 W bei 4,2 V, Ausgleichszeit ≈ 14 h (Rechnung `elektronik.py`). ENT-115 gilt danach nur für LFP (variante [LFP]). Vorgabe Opus (AUFTRAG E2, Fortsetzung 2, Punkt 1b). Status vorgeschlagen, Freigabe nur durch den Menschen.
## Folgen
`elektronik.py` rechnet NMC mit 130 mA; Abgleich in ERGEBNIS.md.

---
*KI-generiert (Claude Sonnet, 2026-11-18), im Auftrag von Opus.*

### ENT-147 Bauraumlänge LFP 2050 mm (CMU hochkant in beiden Endzonen, je +10 mm) (2026-11-18, vorgeschlagen, Opus (Annahme, AUFTRAG E2 Fortsetzung 2); Variante: LFP)
Merkmal: bauraum_laenge_mm = 2050.0 mm; Anforderungen: REQ-P07; Belege: B-BAT-024
## Frage
LFP-Gehäuse: Die Endzone vorn/hinten ist 3,0 mm frei (cad/pack/entwurf/ergebnis_LFP_e2.json, e2.freier_spalt_endzone_vorn_mm im Lauf vom 2026-11-18). Die CMU-Platine (120 × 60 × 10 mm) steht hochkant (Dicke 10 mm in Längsrichtung).
## Alternativen
2030 mm beibehalten (CMU passt nicht); CMU auf dem Deckel (Deckel ist durch die obere Kühlplatte belegt, ENT-088).
## Entscheidung und Begründung
LFP bauraum_laenge_mm = 2050 (je Endzone +10 mm). Ersetzt ENT-102 (LFP 2030). NMC bleibt bei ENT-103 (1950 mm; Endzone 41,6 mm reicht). Vorgabe Opus. Status vorgeschlagen, Freigabe nur durch den Menschen (ENT-102 ist vom Autor entschieden).
## Folgen
Gehäuse-CAD LFP, Masse (Rahmen, Kühlplatten), Crash X, Kühlplatte K2.

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

### ENT-149 Messleitung FPC Breite LFP 16 mm (2026-11-18, vorgeschlagen, Opus (Vorschlag, AUFTRAG E2 Fortsetzung 3; Geometrie Sonnet); Variante: LFP)
Merkmal: breite_mm = 16.0 mm; Anforderungen: REQ-P02; Belege: B-BAT-024
## Frage
Breite der Messleitung FPC (BT-360) für LFP.
## Alternativen
| Alternative | dafür | dagegen |
|---|---|---|
| 20 mm (ENT-122) | – | passt an den LFP-Querträgern nicht vorbei (18 mm frei, v0.3) |
| 16 mm (diese Akte) | 18 Kanäle passen, 18 mm frei an Querträgern | – |
## Entscheidung und Begründung
FPC LFP 16 mm breit (Annahme Opus, ERWARTUNG Nachtrag 2). Im Seitenspalt bis 4 FPC übereinander (4 × 0,3 mm + Halter ≤ 3 mm). ENT-122 (20 mm) gilt nur noch für NMC (variante [NMC] gesetzt). Status vorgeschlagen, Freigabe nur durch den Menschen.
## Folgen
pack.py LFP liest die Breite aus ENT-149.

---
*KI-generiert (Claude Sonnet, 2026-11-18), im Auftrag von Opus.*

### ENT-150 Service-Trennbrücke LFP unter Servicedeckel (2026-11-18, vorgeschlagen, Opus (Vorschlag, AUFTRAG E2 Änderung zu Punkt 4, Autor 2026-11-18); Geometrie Sonnet; Variante: LFP)
Merkmal: bauform = trennbruecke_servicedeckel_vorn ; Anforderungen: REQ-P13; Belege: B-BAT-024
## Frage
Ausführung des Service-Trennstecker für LFP (BT-720): Stecker 60 mm hoch steht 58 mm über dem Deckel (Oberkante 179 mm gegen 130 mm).
## Alternativen
| Alternative | dafür | dagegen |
|---|---|---|
| Stecker 80 x 50 x 60 über dem Deckel (ENT-131) | steckbar | Höhe 179 mm, über M0-Grenze 130 mm |
| Service-Trennbrücke in der Verbinderebene (diese Akte) | 0 mm Höhenzuwachs über dem Deckel | nur mit Werkzeug in der Werkstatt; Öffnung 120 x 80 mm durch Pad, obere Kühlplatte und Deckel |
## Entscheidung und Begründung
Verschraubte Cu-Brücke (2 x M8, mit HV-Interlock-Kontakt) im Querverbinder vorn, unter einem abgedichteten Servicedeckel (Öffnung 120 x 80 mm, Deckel 2 mm, flach, bündig im Gehäusedeckel). Annahmen „ERW-E2 N3“: Brücke Cu 25 x 3 mm, Überlappung 25 mm je Seite, Lücke im Querverbinder 30 mm (Platzhalter). Merkmal „bauform“ fehlt in struktur.json für BT-720, deshalb unter einbauort. ENT-131 gilt nur noch für NMC. Status vorgeschlagen, Freigabe nur durch den Menschen.
## Folgen
pack.py LFP: Brücke statt Stecker, Höhe vorn 121 mm. Trennen nur mit Werkzeug (Pyrosicherung und Schütze trennen im Fehlerfall). Fehlendes Merkmal „bauform“ in BT-720.

---
*KI-generiert (Claude Sonnet, 2026-11-18), im Auftrag von Opus.*

### ENT-151 Keine Knautschzone im Pack, Seitencrash über Schweller (2026-11-19, entschieden (Mensch), Opus (Vorschlag), Autor entschieden 2026-11-19 („verwerfe die knautschzone“); Variante: LFP, NMC)
Merkmal: crashkonzept = schweller_traegt_keine_knautschzone_im_pack ; Anforderungen: REQ-P14; Belege: B-BAT-030, B-BAT-031
## Frage
Bekommt der Pack eine eigene Knautschzone im Seitenrahmen (BT-540), oder nimmt die Fahrzeugstruktur (Schweller) den Seitenpfahl allein auf?
## Alternativen
| Alternative | dafür | dagegen |
|---|---|---|
| Knautschprofil im Pack, w = 15/20/30 mm (X1b/X2) | Reserve im Pack selbst | bringt nur 0,4 bis 0,6 kJ bis zur Zellberührung (Ziel 5 kJ), kostet bei fester Breite 1430 mm Zellen (LFP −2,4 % Energie für +10 % Reserve) |
| Studie mit engeren Querträgern und steiferer Innenwand | könnte die Innenwand stützen | zusätzliche Masse und Länge, Ergebnis offen |
| **Schweller trägt, keine Knautschzone im Pack (diese Akte)** | volle Breite für Zellen, wie Autor-Vorgabe vom 2026-11-17 | Pack hängt von der Fahrzeugstruktur ab, Schnittstelle (Kraft ≤ 30 kN an der Zelle) muss im Lastenheft an das Fahrzeug weitergegeben werden |
## Entscheidung und Begründung
Keine Knautschzone im Pack. X1 (B-BAT-030) zeigt Zellberührung bei ≈ 30 kN bzw. 20 J. X1b/X2 mit OpenCourant (B-BAT-031) zeigen: Das Knautschprofil nimmt nur ≈ 10 % der Zielenergie auf, weil die Rahmen-Innenwand zwischen den Querträgern zuerst nachgibt. Die Opus-Prüfung hält die Vereinfachungen für konservativ, die Empfehlung ist also robust.
## Folgen
Seitenrahmen BT-540 bleibt das Rahmenprofil aus ENT-082…091 (Breite 30 mm), ohne Knautschprofil. Die Rolle von BT-540 in struktur.json ist angepasst. Schnittstelle zum Fahrzeug: Der Schweller muss den Pfahl (R135) vor dem Rahmen stoppen (Zellberührung ≈ 30 kN, X1) → Vermerk in REQ-P14 bzw. in der Schnittstellenliste. Die Studie mit engeren Querträgern entfällt.

---
*KI-generiert (Claude Opus, 2026-11-19).*

### ENT-152 Kühlplatte aus Blech 1/4/1 mm mit Mäander (Autor-Vorschlag) (2026-11-19, entschieden (Mensch), Autor 2026-11-19 („kühlplatten aus blech … oben und unten 1mm stark dazwischen 4mm bauraum für wasser, es müssten auch schleifen modelliert werden“); Opus Ausarbeitung; Variante: LFP, NMC)
Merkmal: dicke_mm = 6.0 mm; Anforderungen: REQ-P05, REQ-P09; Belege: B-BAT-033
## Frage
Wie wird die Kühlplatte BT-610 aufgebaut: gelötete Platte 8 mm mit 281 parallelen Querkanälen (ENT-090/104/105/106) oder Blech 1 + 4 + 1 mm mit Mäander?
## Alternativen
| Alternative | dafür | dagegen |
|---|---|---|
| 8 mm, 1,5-mm-Bleche, 281 Querkanäle 4 × 5 mm (bisher) | K2: U 565–595 W/(m²K), Δp ≈ 0,005 bar | 75,5 kg für 2 Platten (G5), Sammelkanäle verteilen ungleich |
| **Blech 1 mm oben und unten, 4 mm Wasserraum, Stege bilden einen Mäander (diese Akte)** | ≈ 45 kg (−30 kg), Pack 4 mm niedriger, Strömung über die Bahnen geführt (keine Fehlverteilung) | Δp und U hängen von Bahnzahl und Teilkanalbreite ab → K2b; 1-mm-Blech: Druckfestigkeit/Beulen prüfen |
## Entscheidung und Begründung
Vorschlag nach Autor: Plattendicke 6 mm = 2 × 1 mm Al-Blech + 4 mm Wasserraum. Stege A_g5_kanal_steg_mm (3 mm, gelötet) teilen den Wasserraum in n Mäander-Bahnen aus parallelen Teilkanälen. Bahnzahl n und Teilkanalbreite kommen aus K2b (sim/kuehlung/k2_kuehlplatte, ERWARTUNG Nachtrag K2b), dann eigene Akte für kanal_anzahl/kanal_breite_mm; ENT-104 (Höhe 5) wird durch Höhe 4 ersetzt, ENT-106 (parallel quer) durch Mäander.
## Folgen
Höhenstapel −4 mm (beide Platten). Masse Kühlplatten ≈ 45 kg statt 75,5 kg (ERW-G5 Nachtrag). Ein- und Austritt bei gerader Bahnzahl am selben Ende (hinten) → Verteiler/Sammler hinten bleiben. Kühlkreis außerhalb des Packs (Pumpe, Ventil, Chiller, Ausgleichsbehälter, Schläuche) wird als BT-661…665 modelliert.

---
*KI-generiert (Claude Opus, 2026-11-19).*

### ENT-153 Kühlplatte: Al-Blech 1 mm gelötet, Mäander 8 Bahnen längs (2026-11-19, entschieden (Mensch), Opus (Auswahl aus K2b nach Autor-Vorschlag ENT-152); Variante: LFP, NMC)
Merkmal: werkstoff = "Al-Blech 1 mm, gelötet, Mäander 8 Bahnen längs, Teilkanäle" ; Anforderungen: REQ-P05, REQ-P09; Belege: B-BAT-034
## Frage
Kanalführung der Blech-Kühlplatte 1/4/1 mm (ENT-152): Bahnzahl, Teilkanalbreite, Führung.
## Alternativen
| Variante (K2b, LFP 23 L/min) | U W/(m²K) | Δp bar | Masse 2 Platten kg |
|---|---|---|---|
| n = 4, w = 6, quer (Sonnet-Vorschlag) | 522 | 0,032 | 49,1 |
| n = 4, w = 8, längs (Opus-Erwartung) | 487 (unter Ziel) | 0,051 | 45,2 |
| **n = 8, w = 8, längs (diese Akte)** | **558** | **0,215** | **46,6** |
| n = 8, w = 6, quer | 594 | 0,129 | 49,1 (Austritt vorn, zweiter Verteiler nötig) |
## Entscheidung und Begründung
n = 8 Bahnen längs mit Teilkanälen 8 mm, Stege 3 mm, Wasserraum 4 mm: 12 % Reserve über U 500 für den nicht gerechneten Kontaktwiderstand (Zelle–Pad–Blech), Δp ≤ 0,5 bar. Längs mit gerader Bahnzahl: Ein- und Austritt hinten links/rechts, passt zu Verteiler und Sammler (G5). NMC: U ≈ 545, gleiche Geometrie (sim/kuehlung/k2_kuehlplatte/ergebnis_k2b.json).
## Folgen
kuehlung.py baut Mäander mit 8 Bahnen. ΔT Kühlmittel LFP 10,2 K bei 23 L/min (ENT-108). Kontaktwiderstand bleibt offenes Risiko.

---
*KI-generiert (Claude Opus, 2026-11-19).*

### ENT-154 Kühlplatte: Wasserraum 4 mm (2026-11-19, entschieden (Mensch), Opus (Auswahl aus K2b nach Autor-Vorschlag ENT-152); Variante: LFP, NMC)
Merkmal: kanal_hoehe_mm = 4.0 mm; Anforderungen: REQ-P05, REQ-P09; Belege: B-BAT-034
## Frage
Kanalführung der Blech-Kühlplatte 1/4/1 mm (ENT-152): Bahnzahl, Teilkanalbreite, Führung.
## Alternativen
| Variante (K2b, LFP 23 L/min) | U W/(m²K) | Δp bar | Masse 2 Platten kg |
|---|---|---|---|
| n = 4, w = 6, quer (Sonnet-Vorschlag) | 522 | 0,032 | 49,1 |
| n = 4, w = 8, längs (Opus-Erwartung) | 487 (unter Ziel) | 0,051 | 45,2 |
| **n = 8, w = 8, längs (diese Akte)** | **558** | **0,215** | **46,6** |
| n = 8, w = 6, quer | 594 | 0,129 | 49,1 (Austritt vorn, zweiter Verteiler nötig) |
## Entscheidung und Begründung
n = 8 Bahnen längs mit Teilkanälen 8 mm, Stege 3 mm, Wasserraum 4 mm: 12 % Reserve über U 500 für den nicht gerechneten Kontaktwiderstand (Zelle–Pad–Blech), Δp ≤ 0,5 bar. Längs mit gerader Bahnzahl: Ein- und Austritt hinten links/rechts, passt zu Verteiler und Sammler (G5). NMC: U ≈ 545, gleiche Geometrie (sim/kuehlung/k2_kuehlplatte/ergebnis_k2b.json).
## Folgen
kuehlung.py baut Mäander mit 8 Bahnen. ΔT Kühlmittel LFP 10,2 K bei 23 L/min (ENT-108). Kontaktwiderstand bleibt offenes Risiko.

---
*KI-generiert (Claude Opus, 2026-11-19).*

### ENT-155 Kühlplatte: Teilkanal 8 mm (Steg 3 mm) (2026-11-19, entschieden (Mensch), Opus (Auswahl aus K2b nach Autor-Vorschlag ENT-152); Variante: LFP, NMC)
Merkmal: kanal_breite_mm = 8.0 mm; Anforderungen: REQ-P05, REQ-P09; Belege: B-BAT-034
## Frage
Kanalführung der Blech-Kühlplatte 1/4/1 mm (ENT-152): Bahnzahl, Teilkanalbreite, Führung.
## Alternativen
| Variante (K2b, LFP 23 L/min) | U W/(m²K) | Δp bar | Masse 2 Platten kg |
|---|---|---|---|
| n = 4, w = 6, quer (Sonnet-Vorschlag) | 522 | 0,032 | 49,1 |
| n = 4, w = 8, längs (Opus-Erwartung) | 487 (unter Ziel) | 0,051 | 45,2 |
| **n = 8, w = 8, längs (diese Akte)** | **558** | **0,215** | **46,6** |
| n = 8, w = 6, quer | 594 | 0,129 | 49,1 (Austritt vorn, zweiter Verteiler nötig) |
## Entscheidung und Begründung
n = 8 Bahnen längs mit Teilkanälen 8 mm, Stege 3 mm, Wasserraum 4 mm: 12 % Reserve über U 500 für den nicht gerechneten Kontaktwiderstand (Zelle–Pad–Blech), Δp ≤ 0,5 bar. Längs mit gerader Bahnzahl: Ein- und Austritt hinten links/rechts, passt zu Verteiler und Sammler (G5). NMC: U ≈ 545, gleiche Geometrie (sim/kuehlung/k2_kuehlplatte/ergebnis_k2b.json).
## Folgen
kuehlung.py baut Mäander mit 8 Bahnen. ΔT Kühlmittel LFP 10,2 K bei 23 L/min (ENT-108). Kontaktwiderstand bleibt offenes Risiko.

---
*KI-generiert (Claude Opus, 2026-11-19).*

### ENT-156 Kühlplatte: 8 Mäander-Bahnen (2026-11-19, entschieden (Mensch), Opus (Auswahl aus K2b nach Autor-Vorschlag ENT-152); Variante: LFP, NMC)
Merkmal: kanal_anzahl = 8.0 ; Anforderungen: REQ-P05, REQ-P09; Belege: B-BAT-034
## Frage
Kanalführung der Blech-Kühlplatte 1/4/1 mm (ENT-152): Bahnzahl, Teilkanalbreite, Führung.
## Alternativen
| Variante (K2b, LFP 23 L/min) | U W/(m²K) | Δp bar | Masse 2 Platten kg |
|---|---|---|---|
| n = 4, w = 6, quer (Sonnet-Vorschlag) | 522 | 0,032 | 49,1 |
| n = 4, w = 8, längs (Opus-Erwartung) | 487 (unter Ziel) | 0,051 | 45,2 |
| **n = 8, w = 8, längs (diese Akte)** | **558** | **0,215** | **46,6** |
| n = 8, w = 6, quer | 594 | 0,129 | 49,1 (Austritt vorn, zweiter Verteiler nötig) |
## Entscheidung und Begründung
n = 8 Bahnen längs mit Teilkanälen 8 mm, Stege 3 mm, Wasserraum 4 mm: 12 % Reserve über U 500 für den nicht gerechneten Kontaktwiderstand (Zelle–Pad–Blech), Δp ≤ 0,5 bar. Längs mit gerader Bahnzahl: Ein- und Austritt hinten links/rechts, passt zu Verteiler und Sammler (G5). NMC: U ≈ 545, gleiche Geometrie (sim/kuehlung/k2_kuehlplatte/ergebnis_k2b.json).
## Folgen
kuehlung.py baut Mäander mit 8 Bahnen. ΔT Kühlmittel LFP 10,2 K bei 23 L/min (ENT-108). Kontaktwiderstand bleibt offenes Risiko.

---
*KI-generiert (Claude Opus, 2026-11-19).*

### ENT-157 Kühlmodul hinten am Pack (unter der Rücksitzbank) (2026-11-19, entschieden (Mensch), Autor 2026-11-19 („ja das darf hinten sitzen“), Vorschlag Opus; Variante: LFP, NMC)
Merkmal: einbauort = hinten_am_pack ; Anforderungen: REQ-P05, REQ-P09; Belege: B-BAT-034
## Frage
Wo sitzt der äußere Kühlkreis (Pumpe, 3/2-Wege-Ventil, Chiller, Ausgleichsbehälter, Schläuche, BT-661…665)?
## Alternativen
| Alternative | dafür | dagegen |
|---|---|---|
| **Kühlmodul hinten am Pack, hinter der Rückwand (diese Akte)** | kurze Schläuche, Pack mit Kühlkreis als eine Einheit prüfbar und im Video zeigbar | Pack + 245 mm (LFP) Länge unter der Rücksitzbank |
| im Vorderwagen | Platz beim Kältekreis | lange Schläuche, Pack-Modell endet an den Stutzen |
## Entscheidung und Begründung
Autor: hinten. Die Länge darf wachsen (Autor 2026-11-17), die Breite 1430 mm bleibt fest. Lage nach cad/baukasten/teile/kuehlung.py (_modul): Geräte quer in einer Reihe auf Stutzenhöhe.
## Folgen
Gesamtlänge LFP ≈ 2295 mm mit Kühlmodul. Kältemittelleitungen vom Chiller zum Fahrzeug-Kältekreis sind Fahrzeugseite (nicht modelliert).

---
*KI-generiert (Claude Opus, 2026-11-19).*

### ENT-158 Kühlplatte optimieren: zwei parallele Mäander (k = 2) aus Verteilerrohr Ø 25 statt eines Mäanders (2026-11-22, entschieden (Mensch), Opus (Vorschlag) / Autor (Freigabe); Variante: alle)
Merkmal: kanalfuehrung = gruppiert_k2 ; Anforderungen: REQ-P05, REQ-P09; Belege: B-BAT-038, B-BAT-040, B-BAT-043, sim/kuehlung/k5_parallel/ergebnis_verteiler.json, sim/kuehlung/k3_gesamt/elmer_LFP_P0_V4/ergebnis.json
## Frage
Die freigegebene Mäander-Kühlplatte (ENT-152 bis 156) verfehlt beim LFP-Schnellladen das Ziel ΔT ≤ 5 K (Annahme Opus). K4 Elmer liefert ΔT 16,4 K bei T_max 42,6 °C (B-BAT-038). Etwa 10 K davon sind die Aufwärmung des Kühlmittels entlang des Mäanders (K2b 10,2 K). Der Autor hat die Platte freigegeben mit dem Zusatz „muss aber optimiert werden“ (2026-11-22). Zu entscheiden ist, wie das Kühlmittel geführt wird.
## Alternativen
| Alternative | dafür | dagegen |
|---|---|---|
| V0 Mäander, 8 Bahnen in Reihe (Ist) | einfach, ein Ein- und ein Auslass, gerechnet | ΔT 16,4 K (B-BAT-038) |
| V1 obere und untere Platte gegenläufig | kein neues Bauteil | ΔT 10,5 K (B-BAT-040) |
| V2 Durchfluss ×2 | nur die Pumpe ändert sich | ΔT 11,1 K, doppelter Pumpendruck |
| V3 = V1 + V2 | beste gerechnete Variante | ΔT 8,1 K, Ziel trotzdem verfehlt |
| **Parallelführung, Bahnen parallel mit Z-Verteiler (Vorschlag)** | Bei gleichem Durchfluss bleibt die Kühlmittelaufwärmung gleich (10 K, nur längs statt quer verteilt). Der Gewinn liegt im Druckverlust: ein Achtel des Durchflusses und ein Achtel der Weglänge je Bahn, Δp grob 1/64 (laminar). Damit ist mehrfacher Durchfluss bei weniger Pumpendruck möglich. Lehre Wasserstoff B-BZ-004 (Z-Anordnung 1,07:1) | Gleichverteilung hängt am Verteiler (eigene Rechnung nötig), neuer Verteiler/Sammler, Kollisionsprüfung G5 |
## Entscheidung und Begründung
Vorschlag Opus: Parallelführung mit Z-Verteiler, dazu Durchfluss ×3 und gegenläufige Durchströmung von Ober- und Unterplatte (V1). Erwartung vor der Rechnung: Druckverlust der Platte trotz ×3 kleiner als K2b (0,22 bar); Kühlmittelanteil an ΔT etwa 2 K; ΔT gesamt 6–8 K, weil die etwa 6 K aus der Wärmeleitung in Zelle und Pad bleiben. 5 K erreicht man damit allein nicht, dafür wäre zusätzlich der Wärmeweg Zelle–Platte zu verbessern (Pad λ, Anpressung). Korrektur Opus: Eine frühere Aussage im Chat („die Aufwärmung fällt auf wenige Kelvin“) galt nur bei höherem Durchfluss. Nachweis durch eine Verteilerrechnung (Gleichverteilung ≤ ±10 % je Bahn) und K4 mit der neuen Randbedingung. Erst danach entscheidet der Autor.
## Folgen
BT-610 Geometrie (Verteiler, Sammler, Stege), G5-Montage (Kollisionen am Verteiler außen), Pumpe/Druckverlust (K2b neu), Stückliste und Kosten. Bis zur Freigabe gilt der Mäander (ENT-152 bis 156).

## Überarbeitung nach der Rechnung K5 (Opus, 2026-11-23)
- Die reine Parallelführung mit Z-Verteiler in der Platte ist verworfen (B-BAT-043). Die 120 Kanäle lassen sich aus einem Sammler in Plattenhöhe nicht gleichmäßig speisen: Abweichung bis +990 %, Δp bei ×3 0,44 bar.
- Neuer Vorschlag: Die Platte wird in **zwei parallele Mäander mit je 4 Bahnen** geteilt. Beide werden aus einem außen liegenden Verteilerrohr Ø 25 mm gespeist, mit dreifachem Durchfluss (34,5 L/min je Platte), Ober- und Unterplatte gegenläufig.
- Rechnung: Die Verteilung weicht um höchstens 2,0 % ab, Δp der Platte 0,171 bar (Mäander bei ×3: 0,70 bar, heute bei ×1: 0,215 bar). K4 LFP-Schnellladen: T_max 34,1 °C, ΔT 7,6 K (bisher V0 16,4 K, V3 8,1 K). NMC: ΔT 1,3 K. Alle Werte liegen im Erwartungsband (ERWARTUNG K5, Nachtrag 1).
- Verglichen mit V3 (Mäander, gegenläufig, Durchfluss ×2) gewinnt die Variante bei ΔT nur 0,5 K. Ihr eigentlicher Vorteil ist der Druckverlust (0,17 statt etwa 0,45 bar bei mehr Durchfluss) und damit die kleinere Pumpe. Alternativen k = 4 (Verteilung ±15 %) und k = 8 (±77 %) verfehlen ±10 %.
- Offen für den Autor (Grenzwertfrage): Die ΔT von 7,6 K enthalten das Temperaturgefälle innerhalb der Zellen, also von der Kühlseite zur Mitte. Ob REQ „ΔT ≤ 5 K“ den Unterschied **zwischen** Zellen meint (übliche Lesart, gemessen an Zellsensoren) oder jede Temperatur im Block, entscheidet, ob das Ziel schon erreicht ist. Das sollte vor weiteren Maßnahmen am Pad geklärt werden.
- Folgen: BT-610 bekommt eine Trennung der Platte in zwei Hälften und zwei Anschlüsse je Platte, dazu das Verteilerrohr außen (Kollisionsprüfung G5). Pumpe mit 3-fachem Durchfluss, Stückliste und Kosten.

### ENT-159 Kühlplatte: Verteilerrohr außen Ø 25 mm für zwei parallele Mäander (2026-11-23, entschieden (Mensch), Opus (Vorschlag, Teil von ENT-158) / Autor (Freigabe); Variante: alle)
Merkmal: verteilerrohr_d_mm = 25.0 mm; Anforderungen: REQ-P09, REQ-P12; Belege: B-BAT-043, sim/kuehlung/k5_parallel/ergebnis_verteiler.json
KI-generiert (Claude Opus, 2026-11-23). Eigene Akte, weil das CAD je Merkmal eine Akte braucht; inhaltlich Teil von ENT-158.
## Frage
Welcher Innendurchmesser des außen liegenden Verteilerrohrs speist die zwei parallelen Mäander je Platte gleichmäßig?
## Alternativen
| Alternative | dafür | dagegen |
|---|---|---|
| Ø 20 mm | kleiner, leichter | Verteilung ±4,7 %, Δp 0,182 bar (×3) |
| **Ø 25 mm** | Verteilung ±2,0 %, Δp 0,171 bar (×3) | etwas mehr Bauraum außen |
| Sammler in der Platte (Kanalhöhe) | kein Rohr | Verteilung bis +990 %, verworfen (B-BAT-043) |
## Entscheidung und Begründung
Ø 25 mm. Beide Rohre erfüllen ±10 %; Ø 25 hat die Reserve für Fertigungstoleranzen und den kleineren Druckverlust (sim/kuehlung/k5_parallel/ergebnis_verteiler.json, Abschnitt gruppen). Annahme: ζ = 1 je T-Abzweig.
## Folgen
Rohr außen am Pack (Lage im CAD, Kollisionsprüfung G5), Anschlüsse je Plattenhälfte, Stückliste und Kosten.

## Befund B-BAT-004
B-BAT-004 (2026-11-16) Analyse: Was fehlt für die komplette Batterie (Struktur gegen Information)
Fundstellen: `pm/bauteile/struktur.json`, `stueckliste.json`, `parameter.json`, `pm/startwerte.json`, `pm/entscheidungen/`, `forschung/ergebnis/*.pruefung.txt`. Erwartung: entfällt (Bestandsaufnahme, keine Rechnung).
1. **Struktur zu flach.** struktur.json hat 8 Bauteile. Merkmale gibt es nur bei BT-100 (5) und BT-200 (2). BT-300 bis BT-700 haben keine. Die Stückliste hat 37 Positionen, aber keine davon ist ein eigenes Bauteil. Folge: Für Gehäuse, Querträger, Kühlplatte, Zellverbinder usw. kann `pm.py pruefe` keine Akte annehmen, also gibt es kein Maß fürs CAD. Das ist der Hauptblocker.
2. **Keine Maßentscheidung.** parameter.json: alle 7 Merkmale `null`. ENT-001…003 betreffen Methoden. ENT-002 (PyBaMM) steht noch auf „vorgeschlagen“.
3. **Widerspruch Energie.** startwerte.json: 73,9 kWh brutto. stueckliste.json: 79,9 kWh (219s1p × 100 Ah × 3,65 V, beide Zellwerte Annahme). Die Zellzahl ist auf ganze Reihen gerundet, die Energie aber nicht zurückgeführt.
4. **Widerspruch Chemie gegen Vorbild.** Die Startwerte wählen NMC, weil die LFP-Packdichte als 180 Wh/L **angenommen** ist (startwerte.py, „Zelle × Füllgrad ~0,6“, unbelegt), nötig wären 214 Wh/L. Die Recherche belegt für Blade-LFP nur Werte je kg (190–210 Wh/kg Zelle, W03), keinen Wert je Liter. Die Stückliste führt deshalb eine „lang prismatische NMC-Zelle“. Für dieses Format gibt es in der Recherche keinen Beleg, das Blade-Fo

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

## Befund B-BAT-008
B-BAT-008 (2026-11-16) W19 geprüft; Energiewiderspruch Stückliste 112 kWh gegen 73,9 kWh
- W19 (drpress HSET 2022, Studentenarbeit, Sekundärquelle): 20/20 Belege wörtlich bestätigt, inhaltlich schwach. **Gesperrt:** 332 Wh/kg „BYD battery“ (für LFP unplausibel, Bezug fehlt), 155 Wh/100 km Model Y (Einheit falsch), „ordinary 250 Wh/kg“ (Chemie offen), 180 Wh/kg „blade battery“ (Zelle oder Pack unklar). **Als Hinweis verwendbar (Pack, Sekundärquelle):** Volumennutzung Blade-Pack bis 60 %, konventionell etwa 40 %; Zelle ca. 0,6 m × 13,5 mm (Short Blade); Pack BYD Han ca. 79 kWh.
- Folge für den Bauraum: Bei 60 % Volumennutzung braucht die Zelle 357 Wh/L (Fall A) bzw. 427 Wh/L (Fall B). Das ist jetzt die Prüfgröße für die Blade-Zelle (Volumen Long Blade 1,166 L aus W03-Maßen). Die Blade-Kapazität (Ah) und damit die Wh/L der Zelle ist weiter **nicht belegt**.
- Sonnet-Umstellung (pm/AUFTRAG_LFP_UMSTELLUNG_ergebnis.txt): startwerte.json chemie = LFP (ENT-005 vor Bauraumregel), Warnung Bauraum offen; Obsidian 49 Bauteilnotizen (struktur.json hat 49 Einträge inkl. BT-000 und Baugruppen; die Zahl „46“ in früheren Notizen ist falsch). Opus geprüft: startwerte.json, docs/13, wissen/Bauteil, pm.py pruefe 0 Fehler.
- **Widerspruch:** Stückliste 250s × 1p × 3,2 V × 140 Ah = 112,0 kWh gegen Bedarf 73,9 kWh (+51 %). Die 140 Ah sind eine Annahme aus stueckliste.py. Bei 800 V und 1p bräuchte die Zelle 92 Ah, bei 400 V (125s) 185 Ah. Das ist eine Auslegungsfrage (Systemspannung und Zellgröße, G

## Befund B-BAT-009
B-BAT-009 (2026-11-16) Zerlegungsstudie Blade (W20): Gen-1-Zelle 160 Wh/kg, 355 Wh/L; Bauraum Fall A genau an der Grenze
- Quelle: Cell Rep. Phys. Sci. 6, 102453 (2025), CC-BY, PDF vom Autor in quellen/blade_zerlegung/. PI-Lauf W20: 0/21, weil PI die DOI statt der file://-URL angab. Opus: URL ersetzt → 17/21; die 4 Reste stehen im Fließtext (pdftotext ohne -layout, zweispaltiger Satz). Z25 („around 23 of the heat“) gesperrt: Bruch bei der Textumwandlung verloren.
- **Blade-Zelle (gemessen, Tabelle 1):** 135 Ah, 432 Wh, 3,2 V, Fenster 2,6–3,65 V, 2,7 ± 0,3 kg, 1216 mL, **160 Wh/kg, 355,3 Wh/L**, 965 × 90 × 14 mm, Wandstärke Gehäuse 0,3 mm, ein Z-gefalteter Elektrodenstapel, Aktivmasse etwa 60 % der Zellmasse. Zum Vergleich Tesla 4680 (NMC811): 241 Wh/kg, 643 Wh/L.
- **Folge Bauraum:** 355 Wh/L × 60 % Volumennutzung (W19) = 213 Wh/L Pack. Nötig: 214 (Fall A), 256 (Fall B). Fall A passt knapp, Fall B nicht. Prüfpunkt von ENT-005 damit **an der Grenze, nicht klar erfüllt**.
- **Folge Masse:** 160 Wh/kg liegt unter dem C0-Band 185–210 (W03, Hersteller, Long Blade 2.0). Mit 160 Wh/kg, Zellanteil 0,75: Packmasse Fall A 616 kg (543–711), Fall B 739 kg. Eine 4680-NMC-Zelle ergäbe Fall A etwa 409 kg. Der Satz „kein belegter Massenunterschied“ (B-BAT-006) gilt nur mit den Herstellerwerten der 2. Generation.
- Folge 800 V (ENT-006): Eine Original-Blade-Zelle (135 Ah) gäbe 250s × 135 Ah × 3,2 V = 108 kWh. Nötig 92 Ah (A) → bei gleichem Querschnitt etwa 660 mm statt 965 mm Länge (G1).
- We

## Befund B-BAT-011
B-BAT-011 (2026-11-16) Variantenvergleich mit Messwerten: NMC-4680 ein Drittel leichter, LFP-Blade im Bauraum knapp
- Rechnung sim/chemie/varianten_lfp_nmc/ (Sonnet; Opus-Gegenrechnung gleich). Fall A: LFP 616 kg (160 Wh/kg gemessen; 469 kg bei 210 Gen 2), NMC 411 kg (217s×4p = 868 Zellen, 74,3 kWh). Anteil 41 % gegen 27 %.
- Fall B: LFP 93,0 kWh / 775 kg, NMC 86,6 kWh Bedarf, 5p → 92,8 kWh / 514 kg.
- Bauraum: LFP A −0,3 % (knapp), B nicht erfüllt; NMC erfüllt. Zyklen: LFP erfüllt, NMC unsicher.
- Stückliste je Variante: LFP 38 Pos., NMC 37 Pos. (200.2/200.4 entfallen, 200.5 Zellhalter neu; struktur.json BT-250 → 200.5 von Opus eingetragen). Offen: Zellen je Reihe und Fühler bei NMC aus LFP-Annahme (G4); Bild zeigt LFP-Balken bei Bandmitte statt Messwert.
- Deutung DEUTUNG.md. Vorgang: [C0] [V1] [G3]

## B-BAT-010 (2026-11-16) Zwei Varianten parallel: LFP-Blade und NMC-4680, gleiche Spezifikation
- Autor: „kannst du auch zwei varianten paralell bauen? bei mit den selben spezifikationen“; Wahl NMC = Rundzelle 4680.
- Umsetzung (Sonnet, Auftrag pm/AUFTRAG_VARIANTEN.md, Opus geprüft): Akten haben `variante:` (null = alle); pm.py pruefe erlaubt gleiche Merkmale in verschiedenen Varianten; parameter.json (gemeinsam) + parameter_LFP/NMC.json; startwerte.py/stueckliste.py `--variante`. Gemeinsam: ENT-004 Baum, ENT-006 800 V.
- Akten: ENT-005 nur [LFP]; ENT-007…011 [NMC] (NMC811, Rundzelle 4680, 23,125 Ah, 3,7 V, 355 g; W20), entschieden (Mensch, Formatwahl des Autors, Werte gemesse

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

## Befund B-BAT-015
B-BAT-015 (2026-11-17) Innenaufbau beider Zellen aus der Zerlegung; Korrektur LFP-Länge 681 mm; Bauraumbreite 1430 mm
- Autor: „kann man die zellen weiter detailieren ist die nmc nicht eine gewickelte folie? Isolatoren und so müssten ja auch noch rein. auch eine LFP sollte detailiertzer dargestellt werden“.
- Opus liest W20 Tabelle 1, Abb. 2 (alle Innenbauteile), Abb. 4 (Kontaktierung), Abb. 5 (Elektrodenmaße) → cad/zelle/aufbau_W20.json. Werte aus Abbildungen sind von Opus abgelesen (pruefe.py kann Bilder nicht prüfen). Tabelle 1: Einheit „mm“ ist µm (Satzfehler; Probe: Blade-Stapel 38 × 160 + 39 × 140 + 78 × 12 µm = 12,5 mm bei 14 mm Zelle).
- **Eigener Fehler gefunden:** ENT-015 (660 mm) skalierte die Endzone mit. Elektrode 899,5 von 965 mm → Endzone 65,5 mm bleibt fest → **681 mm**. Zwei Reihen 1362 mm > 1340 mm innen → Autor wählt Bauraumbreite **1430 mm** (ENT-030, entschieden). ENT-015 korrigiert (vorgeschlagen).
- 4680-Wickel: Kathode 3215 × 72 mm, Anode 3305 × 73, Separator 2 × 3550 × 75; Wickeldicke je Windung ≈ 0,45 mm → ≈ 34 Windungen, Kern Ø ≈ 14 mm (**abgeleitet, nicht gemessen**).
- Baum: BT-111 Kathode, 112 Anode, 113 Separator, 114 Isolierrand, 115 Wickelkern [NMC], 116 Fixierung/Isolationsbeutel, 121 Gehäusefolie [LFP], 122 Füllöffnung, 131 Stromschiene/Tab-Scheibe, 132 Polisolation; BT-140 lage. 60 Einträge (ENT-031). Akten ENT-032…080 vorgeschlagen.
- Unsicher: Bedeutung der Fahnenmaße in Abb. 5A (27,1/9 bzw. 20,5/7 mm). Vorgang: [G1] [G2] [C1]
- **Nachtra

## Befund B-BAT-017
B-BAT-017 (2026-11-17) Vorgaben Kühlung (REQ-P09, ENT-081); Bericht begonnen
- Autor: „45 °C und 5 K passen, Kühlplatte unten, bitte auch temperaturverläufe grafisch am besten als gerendertes Bild, und für die dikoumentation abspeichern, fange auch an den bericht zu schreiben“.
- REQ-P09: T_max ≤ 45 °C, Spreizung in der Zelle ≤ 5 K (festgelegt). ENT-081 BT-600 kuehlart = Kühlplatte unten (beide Varianten, entschieden). K0: K1 Hauptfall, gerenderte Temperaturbilder und Film (pvbatch) nachbeauftragt.
- Bericht BAT-DOC-17 (bericht/bericht.tex, LaTeX wie Fusion-Bericht, Lesehilfe je Bild, Begriffskästen) an Sonnet nach Gliederung von Opus. Vorgang: [K0] [B1]

## B-BAT-016 (2026-11-17) Detailmodell Innenaufbau fertig; 4680-Wickel ragte über den Becher (Opus-Fehler im Kern)
- Sonnet (cad/zelle/AUFTRAG_DETAIL.md, 42 min, CPU): FreeCAD-Detailmodelle beider Zellen, 7 Schnitt-/Explosionsbilder, Neulauf G1/C0b mit 1430 mm (LFP A passt, Reserve L 16 / B 8 mm; nötig 203,9 Wh/L; NMC 1260 Plätze).
- LFP-Stapel 12,476 mm in 13,4 mm (Rest 0,92 mm) – wie erwartet. Bild LFP_schnitt angesehen: Schichtfolge, Fahnen, Stromschiene, Halter, O-Ring, Isolationsbeutel erkennbar und beschriftet.
- **Verfehlt:** 4680-Wickel Außenradius 23,75 mm > 22,6 mm. Ursache 1 (Opus): ENT-074 Kern Ø 14 mm nur aus Kathodenfläche abgeleitet; mit allen Bändern (1477 mm²) Kern ≤ 12,75 mm → ENT-074 auf 12,5 mm korrigiert. Ursache 2 (Modell): feste Steigung 0,45 mm auch dort, wo nur noch Anode/Separator liegt → flächentre

## Befund B-BAT-019
B-BAT-019 (2026-11-17) Schnellladen in den Griff bekommen (K1); Gehäuserecherche W21
- Autor: „Ja das schnellladen müssen wir in den griff bekommen. man läd schwellenartig könnte auch sein, oder nur bestimmte zellen im wechsel, kühlen kann man auch und dann natürlcih begrenzen. mach die renderings neu. bei der gesamtbatterie müssen verstrebungen vorgehalten werden du kannst mal eine recherche machen wie ein batteriegehäuse aufgebaut ist.“
- Opus vorab: Bei fester Ladezeit erzeugt konstanter Strom die wenigste Joulewärme; Stufen +9 %, Puls/Zellen im Wechsel +100 %. In Reihe führen alle Zellen denselben Strom → Wechsel einzelner Zellen nur bei Parallelgruppen und dann wärmer. Spreizung hängt am Wärmeweg: nur beidseitige Kühlung oder kleinerer Strom (LFP ≤ 1,29C, NMC ≤ 1,02C stationär) bringt 5 K. Prüfung durch Rechnung K1.
- Autor (Nachtrag): „bei der Breite sind wir nicht so variabel letzten endes von straßenbreite begrenzt, länge ist etwas einfacher.“ → Breite 1430 mm gilt als fest, Länge darf wachsen. Folge Opus: Querträger quer zur Fahrtrichtung kosten Länge (zulässig); ein Längsträger zwischen den zwei LFP-Zellreihen und breitere Seitenrahmen kosten Breite (Reserve 8 mm) → kritisch, Seitenrahmenbreite aus W22 gegen den angenommenen Rand prüfen.
- Verstrebungen: struktur.json hat BT-530 Querträger, BT-540 Seitenrahmen, BT-550 Unterfahrschutz; W21 soll Werte liefern. Wichtig für Bauraum: Querträger kosten Länge/Breite (G1-Reserve LFP 16/8 mm!). - W21 (12/0): Bauweise CTP, Wa

## Befund B-BAT-020
B-BAT-020 (2026-11-17) Fixierung, Kontaktierung, Kühlung der 4680 nach Herstellervergleich
- Autor: „du musst aber auch fixierung sowie kontaktierung der rundzellen vorsehen“; „schau mal erst wie andere hersteller das ... machen“; „verteile die rechereche“. PI W24 (24/0), W25 (10/0), W26 (14/0), P14 leer; Sonnet Quellensuche; Haiku Tabelle forschung/vergleich_rundzellen.md.
- Belegt: einseitige Kontaktierung (Lucid, Rivian, Tesla), Al-Verbinder (Lucid), Verguss zwischen Zelle und Kühlung (Tesla), Ableiterscheiben Al 400 µm / Cu 260 µm, DCIR 4680 5,4–7 mΩ (bestätigt K0-Annahme 6,5).
- **Widerspruch:** Becherwand 4680 laut W24/W25 (batterydesign.net, Sammelseite) 0,5–0,6 mm, ENT-029 0,4 mm aus W20 (eigene Zerlegung, Primärquelle). Opus: ENT-029 bleibt, W24-Wert als Band in der Akte nennen; Unterschied evtl. Zellgeneration.
- Nicht belegt: wo Hersteller Rundzellen kühlen (Seite/Boden/oben) – nur Vorab-Websuche (Tesla Seitenbänder), nicht zitatgeprüft.
- Vorschlag ENT-092…095 [NMC]: Träger unten + Verguss, Al-Verbinder einseitig oben, Laserschweißen (Annahme), isolierendes Pad zwischen Verbindern und oberer Kühlplatte. K1b (h_eff 214 oben): NMC 20 min 42,8 °C/8,1 K ✗, 25 min 36,8/5,4 ✗ (knapp), 30 min 33,3/3,8 ✓; 25 min erfüllt bei Bedeckung φ ≥ 0,7. Erwartung Opus 1–3 K zu hoch (Pad-Widerstand überschätzt bzw. Verguss/Boden trägt mehr). - Autor: „30 minuten“ → REQ-P05: NMC-4680 schnellladen 10→80 % in 30 min (LFP 20 min). Erster bewusster Spezifikationsunterschied der Varianten.

## Befund B-BAT-021
B-BAT-021 (2026-11-17) Kühlplatten K2: laminar, U nur mit 4-mm-Kanälen ≥ 500; Durchfluss offen
- K2 (Sonnet, 1D): Re 27–188, h_Kanal 260–316 W/(m²K) (Erwartung Opus 500–1000 zu optimistisch: laminar Nu ≈ 4–5). Mit Stegen auf Grundfläche bezogen und Pad/Blech in Reihe: U 565–595 nur bei 4 × 5 mm Kanälen. Δp ≈ 0,005 bar, Pumpe < 1 W. Mäander ohne Nutzen.
- Durchfluss für ΔT_Kühlmittel 5 K: LFP 47 L/min, NMC 20 L/min; bei 10 K halbiert, U gleich (laminar). Autor: „ja setzte deinen vorschlag um.“ → ENT-107 LFP 23 L/min (10 K), ENT-108 NMC 20 L/min (5 K). ENT-104…106 vorgeschlagen. Vorgang: [K2]

## B-BAT-020 (2026-11-17) Fixierung, Kontaktierung, Kühlung der 4680 nach Herstellervergleich
- Autor: „du musst aber auch fixierung sowie kontaktierung der rundzellen vorsehen“; „schau mal erst wie andere hersteller das ... machen“; „verteile die rechereche“. PI W24 (24/0), W25 (10/0), W26 (14/0), P14 leer; Sonnet Quellensuche; Haiku Tabelle forschung/vergleich_rundzellen.md.
- Belegt: einseitige Kontaktierung (Lucid, Rivian, Tesla), Al-Verbinder (Lucid), Verguss zwischen Zelle und Kühlung (Tesla), Ableiterscheiben Al 400 µm / Cu 260 µm, DCIR 4680 5,4–7 mΩ (bestätigt K0-Annahme 6,5).
- **Widerspruch:** Becherwand 4680 laut W24/W25 (batterydesign.net, Sammelseite) 0,5–0,6 mm, ENT-029 0,4 mm aus W20 (eigene Zerlegung, Primärquelle). Opus: ENT-029 bleibt, W24-Wert als Band in der Akte nennen; Unterschied evtl. Zellgeneration.
- Nicht belegt: wo Hersteller Rundzellen kühlen (Seite/Boden/oben

## Befund B-BAT-024
B-BAT-024 (2026-11-18) E2 Elektronik Teil 1: Abgriffe, Ausgleich, Vorladung ok; HV-Verlust 13 W/m akzeptiert; Schaltbox Fall b
- Teil 1 (`sim/elektrik/e2_elektronik/ERGEBNIS.md`): 251/218 Abgriffe, Ausgleich 12,3 h, Vorladung 8 A/320 J/300 ms. Opus-Fehler in der Erwartung: ≤ 15 W bei 3–5 m HV-Leitung war mit 50 mm² nicht möglich (≈ 13 W/m, nur beim Schnellladen). NMC-Heizung 26 min unter dem Band, weil die Zellmasse kleiner ist (308 kg).
- CMU-Wärme NMC 9,95 W bei Nennspannung, bei Ladeschluss über 10 W → Rechnung mit Zellhöchstspannung nachholen.
- Autor: Schaltbox auf dem Deckel vorne (ENT-109). Antworten auf Sonnets Fragen 1–3 im Nachtrag 1 der ERWARTUNG; 4: 139 A (1,5C) gilt; 5: Höchstspannung LFP 3,65 V, NMC 4,2 V (Annahme). Vorgang: [E2]

## B-BAT-023 (2026-11-17) C2 Kalibrierung: Blade-Widerstand gemessen 0,877 mΩ; 4680 schafft 30 min bei 1,5C, Plating-Risiko im Modell
- Blade 25 °C, 15–90 % SOC: RMS 15,3 mV, R10 Modell 0,827 / Messung 0,877 mΩ (Test#5). Temperaturfit verfehlt (158 mV), OCV des Literatursatzes 143 mV daneben → **DFN für LFP nicht belastbar; Opus: für Wärme den gemessenen Widerstand nutzen** (unsere Zelle 1,28 mΩ → 48 W statt 55 W bei 2,1C; K1 war konservativ).
- 4680 (Chen2020-Material, W20-Geometrie, DCIR 6,4 mΩ im Band): 10→80 % in 29,7 min bei 1,5C CC-CV → REQ-P05 erfüllbar. Wärme 7,4 W (Modell) bzw. 11,5 W (I·ΔU) gegen K1b-Annahme 6,7 W → K1c: LFP 32,7 °C / 4,0 K ✓; 4680 mit Modellwärme 34,0 / 4,15 ✓, mit I·ΔU 39,1 / 6,5 ✗ (5 K). Opus: Differenz de

## Befund B-BAT-030
B-BAT-030 (2026-11-18) X1 Seitenpfahl: Pack hat keine Knautschzone, Zellberührung bei ≈ 30 kN
- CalculiX quasistatisch, Pfahl Ø 254 (Annahme). Die Innenwand des Seitenrahmens erreicht die Zellen nach 1 mm (LFP-Verbinder) bzw. 0 mm (NMC, gerade Reihen). Das geschieht bei 29–31 kN und 18–20 J, auch auf dem Querträger (LF2 ≈ LF1). PEEQ 21 % nach 5,5 mm. Netzstudie < 1 %.
- Opus-Fehler: In der Erwartung (1–3 kJ, 30–80 kN) waren die 30 mm Rahmen als freier Weg gezählt.
- Folge: Der Seitencrash muss vollständig über den Schweller gehen (Autor 2026-11-17). Eine Knautschzone im Pack (≈ 15–30 mm je Seite, Annahme) kostet bei fester Breite Zellen → Frage an den Autor. X2 (dynamisch) bringt erst mit Fahrzeugstruktur etwas. Vorgang: [X1]

## B-BAT-029 (2026-11-18) KO1 Kosten: LFP ≈ 80 €/kWh, NMC ≈ 110 €/kWh, vollständig geschätzt
- Untere Schranke: 15 Positionen bei LFP und 12 bei NMC haben keine Masse bzw. Menge. Werte:

  | Variante | €/Pack | €/kWh | Zellanteil |
  |---|---|---|---|
  | LFP | 5 933 | 80,3 | 62 % |
  | NMC | 8 151 | 109,8 | 68 % |

- Verifiziert ist nur der BNEF-Packpreis BEV 2024 von 97 USD/kWh (W29), etwa 89 €/kWh. Er dient zum Abgleich. 100 % der Summe beruhen auf Schätzungen (ERW-KO1).
- Wirkung des Zellpreises: ±20 % beim Zellpreis ergeben ±12,5 % (LFP) bzw. ±13,7 % (NMC) beim Packpreis.
- Opus-Fehler in Lauf 1: Fertigungszuschlag auf die Zellen gerechnet, Kühlplatte als Vollmaterial. Korrigiert in Nachtrag 1.
- REQ-P16 ohne Zielwert (Autor).
- Vorgang: [KO1]

## 

## Befund B-BAT-031
B-BAT-031. Studie engere Querträger entfällt. Schnittstelle: Schweller stoppt den Pfahl vor dem Rahmen (Zellberührung ≈ 30 kN, X1). Erwartung: –.

## B-BAT-031 (2026-11-18) X1b/X2 OpenCourant: Knautschprofil bringt kaum Reserve, die Rahmen-Innenwand gibt zuerst nach
- Explizit (OpenCourant latest-20261011), Pfahl 1500 kg mit 5 kJ. Energie bis zur Zellberührung (4 mm):

  | Variante | Energie | Anteil an 5 kJ |
  |---|---|---|
  | LFP w15 | 416 J | 8 % |
  | LFP w20 | 455 J | 9 % |
  | LFP w30 | 568 J | 11 % |
  | NMC w20 | 523 J | 10 % |

- Eindringung 49–52 mm, Energiefehler ≤ 0,01 %. Gegenprüfung mit CalculiX bei 2 mm: +7…14 %.
- **Deutung (Opus):** Das Profil staucht mit ≈ 80 kN. Diese Kraft biegt die Innenwand zwischen den Querträgern (Spannweite ≈ 500 mm) schon, bevor das Profil zusammengefaltet ist. Mehr Breite w hilft daher kaum, von 15 auf 30 mm sind es nur +37 %.
- 5 kJ bei 80 kN brauchen etwa 60 mm Weg. Das ist bei fester Breite nicht unterzubringen.
- **Folge:** Eine Knautschzone im Pack lohnt sich nicht (LFP −2,4 % Energie für +10 % Reserve). Der Seitencrash bleibt beim Schweller (ENT 2026-11-17). Wer Reserve will, braucht eine steifere Innenwand bzw. engere Querträger, als eigene Studie.
- **Werkzeug:** /RFILE-Zwischendateien in OpenCourant latest-20261011 nicht lesbar (Segfault). Der Neustart läuft über 10 Abschnitte (Vergleich 0 Abweichung). Opus-Fehler in ERW-X1b: Erwartung ab w 20 mm, 5 kJ, ohne die Rahmenbiegung zu bedenken. Vorgang: [X1] [X2]

## B-BAT-030 

## Befund B-BAT-033
B-BAT-033 (2026-11-19) G5 Zwischenstand: Kühlplatte mit echten Kanälen +28 kg, Recherche liefert keine Kaufteilmaße
- Kühlplatten (2 Stück) mit den K2-Kanälen (4 × 5 mm, Steg 3, 281 je Platte, Blech 1,5): **75,5 kg statt 46,9 kg**. Der alte Füllgrad 0,4 (A_KUEHLPLATTE_FUELLGRAD) passte nicht zur K2-Geometrie (dort 0,64). Erwartung ERW-G5 75 kg: erfüllt. Fundstelle cad/baukasten/ausgabe/ergebnis_LFP.json (Teillauf gehaeuse,kuehlung).
- Seitenrahmen 3-Kammer-Profil 14,5 kg. ERW-G5 6–7 kg **verfehlt**: Opus hielt die alten 21,8 kg für ein Vollprofil, sie enthielten aber schon Kammern (Vollprofil wären 60 kg). Profilfläche 790 mm² ist geprüft.
- Schaltbox mit liegenden Geräten: Innenhöhe 70 mm (Ziel ≤ 90), Turm 77 mm über dem Packdeckel, Oberkante LFP 198 mm (Grenze 210). Erwartung erfüllt.
- W31 (Preise) und W34 (Kaufteilformen): Die Quellen (Wikipedia) nennen keine Preise und keine Maße. Von den Kaufteilen sind 4–6 Positionen weiter in Stufe H. W32: Al-Dichte 2,70 g/cm³, E 69 GPa, Rp0,2 100–260 MPa (6005) sind bestätigt, die Dichte gilt jetzt als belegt. Für Maße und Preise braucht es Datenblätter von Herstellern (Frage an den Autor).

## B-BAT-032 (2026-11-19) Entscheidung: keine Knautschzone im Pack (ENT-151)
- Autor folgt der Opus-Empfehlung aus B-BAT-031. Studie engere Querträger entfällt. Schnittstelle: Schweller stoppt den Pfahl vor dem Rahmen (Zellberührung ≈ 30 kN, X1). Erwartung: –.

## B-BAT-031 (2026-11-18) X1b/X2 OpenCourant: Knautschprofil bringt kaum Reserve, die 

## Befund B-BAT-034
B-BAT-034 (2026-11-19) K2b Blech-Kühlplatte 1/4/1 mm mit Mäander (Autor-Vorschlag ENT-152)
- 48 Varianten je Pack (sim/kuehlung/k2_kuehlplatte/ergebnis_k2b.json). U ≥ 500 nur mit mehr Bahnen oder schmalen Teilkanälen. **Auswahl Opus n = 8 Bahnen längs, w = 8 mm: U 558 W/(m²K), Δp 0,215 bar, 46,6 kg für 2 Platten** (statt 75,5 kg), Plattendicke 6 statt 8 mm (ENT-152…156).
- ERW-K2b teils verfehlt: n = 4, w = 8 längs ergibt U 487 statt ≈ 550. Breite Kanäle (w = 40) liegen bei 405–518 statt 350–420, weil die Einlaufströmung (Graetz-Term) Nu anhebt. Δp bei n = 8 ist mit 0,215 bar kleiner als erwartet (0,4–1). Erfüllt: Δp bei n = 4 (0,05 bar), Masse 38–49 kg.
- Offen: Der Kontaktwiderstand Zelle–Pad–Blech ist nicht gerechnet, die Reserve beträgt 12 %.

## B-BAT-033 (2026-11-19) G5 Zwischenstand: Kühlplatte mit echten Kanälen +28 kg, Recherche liefert keine Kaufteilmaße
- Kühlplatten (2 Stück) mit den K2-Kanälen (4 × 5 mm, Steg 3, 281 je Platte, Blech 1,5): **75,5 kg statt 46,9 kg**. Der alte Füllgrad 0,4 (A_KUEHLPLATTE_FUELLGRAD) passte nicht zur K2-Geometrie (dort 0,64). Erwartung ERW-G5 75 kg: erfüllt. Fundstelle cad/baukasten/ausgabe/ergebnis_LFP.json (Teillauf gehaeuse,kuehlung).
- Seitenrahmen 3-Kammer-Profil 14,5 kg. ERW-G5 6–7 kg **verfehlt**: Opus hielt die alten 21,8 kg für ein Vollprofil, sie enthielten aber schon Kammern (Vollprofil wären 60 kg). Profilfläche 790 mm² ist geprüft.
- Schaltbox mit liegenden Geräten: Innenhöhe 70 mm (Ziel ≤ 90), Turm 77 mm über dem Packdec

## Befund B-BAT-038
B-BAT-038 (2026-11-21) Thermik K3/K4 Probe: Pack ΔT 16 K, Erwartung von Opus falsch, LBM an der Stabilitätsgrenze
- K4 LFP Schnellladen (sim/kuehlung/k3_gesamt/elmer/ergebnis.json): T_max 42,6 °C, ΔT 16,4 K. Die Erwartung 33–37 °C hatte die Kühlmittelaufwärmung von 10,2 K aus K2b vergessen (Opus-Fehler). Das Ergebnis ist plausibel, **verfehlt aber ΔT ≤ 5 K** und wird zum Verbesserungsvorschlag. Varianten gegensinnig und Durchfluss ×2 sind beauftragt.
- K3 FluidX3D: τ ≈ 0,502 bei Re 760 mit 2 Zellen/mm, also Δp +228 %, h +129 %, Temperatur NaN. Methode geändert: Re 100/200, 4 Zellen/mm, Nu und f·Re der ausgebildeten Strömung übertragen.

## B-BAT-037 (2026-11-21) Nachtrag Zahlen zur Kollisionsbereinigung G5 (Opus, aus den Laufausgaben der Sitzung 2026-11-19/20)
- Erster Gesamtlauf LFP (2026-11-19): 1342 Teile, 628,89 kg, 67 Fehler (Massenabweichungen und Kollisionen zusammen). Größte Kollisionen: Zellen 217/218/248/249 ↔ Verteiler/Sammler je 18 253–21 092 mm³, weil die Verteiler in der Endzone lagen.
- NMC aus G5.4 (Sonnet): 5 Kollisionen des Trennsteckers mit der Schaltbox, die größte Hauptschütz minus 60 381 mm³, Wanne 7 960 mm³.
- Nach Verteiler außen, Kragen und Einbauorten (2026-11-20): LFP 31 Fehler, darunter 17 Kollisionen, NMC 15. Größte: Kabelschuh HV ↔ Kühlplatte 1 190 mm³ bzw. 1 217 mm³.
- Danach LFP 1 Kollision, dann 0 und NMC 0.
- HV-Leitung: Der Eintritt knapp über dem Boxboden hätte eine Schlaufe bis z ≈ 275 mm erfordert (Sonnet G5.4). Behoben mit Eintritt auf H

## Befund B-BAT-040
B-BAT-040 Thermik-Varianten K4 und Crash LFP_a neu (2026-11-21, Opus)
- K4, Tabelle T_max/ΔT aus rechnen/log_K4_*.txt, LFP-Schnellladen: V0 42,6/16,4; V1 gegensinnig 38,4/10,5; V2 Durchfluss ×2 37,0/11,1; V3 beides 34,8/8,1. Die Schätzung von Opus vorab (11–12 / 10–11 / 7–8 K) traf. Keine Variante erreicht ΔT ≤ 5 K, daher wird eine Parallelführung mit Z-Verteiler zum Verbesserungsvorschlag. NMC 30 min: V0 34,1/5,9, V3 30,1/1,5. Dauerfahrt: LFP 29,0/3,8, NMC 29,7/3,0.
- X3 LFP_a nach der Korrektur (Nachtrag 3): Pfahl 13,6 mm, Zellblock 6,7 mm, Innenwand 7,8 mm, 472 kN, Energiefehler 0,18 %, max |U| der Zellen 7,4 mm. Opus-Fehler im Kriterium „kinetische Energie am Ende < 5 %“: Darin steckte auch der Rückprall des Pfahls (17,6 %). Neu gilt die kinetische Energie ohne Pfahl, das sind 2,4 %. Modellprüfung bestanden. Das Kennzahlenbild entspricht dem ungültigen Lauf (13,9/8,1 mm), weil die gleitenden Reihen weit vom Pfahl wenig zur Steifigkeit beitrugen.
- Zweiter Fehler: In der untesteten Auswertung von Sonnet war `pw` nicht definiert; bei der Reparatur der Zeile hat Opus den Rest der Zeile in einen Kommentar verschoben. Beides ist behoben, die Auswertung ist an LFP_a getestet.
- X3 LFP_a2 (20 kJ): Pfahl 38,2 mm (Erwartung 50–120 mm verfehlt, steifer), Zellblock 16,1 mm, 657 kN, Energiefehler 0,2 %, max |U| der Zellen 22,2 mm, kinetische Energie 1,5 %, Modellprüfung bestanden. Im Bild ist der Querträger in Packmitte direkt getroffen und trägt ein (Opus, Stichprobe Bild).

## B-BA

## Befund B-BAT-043
B-BAT-043 Parallelführung mit Z-Verteiler in der Platte funktioniert nicht (2026-11-23, Opus)
- Die Verteilerrechnung (Sonnet, sim/kuehlung/k5_parallel) zeigt: Die Platte hat 120 Kanäle mit zusammen 3 840 mm² Querschnitt. Ein Sammler in Kanalhöhe (25 × 4 mm = 100 mm²) verteilt das Kühlmittel extrem ungleich, einzelne Kanäle bekommen bis zum 11-Fachen des Mittels, mittlere fast nichts. Bei Durchfluss ×3 steigt Δp auf 0,44 bar.
- Fehler von Opus: Beim Schreiben der Erwartung hatte Opus wenige breite Bahnen vor Augen statt 120 einzelner Kanäle. Die Erwartung war klar verfehlt, Sonnet brach deshalb ab, wie im Auftrag vorgesehen, ohne die Erwartung anzupassen.
- Neue Variante: k parallele kurze Mäander aus einem außen liegenden Verteilerrohr (ERWARTUNG Nachtrag 1). ENT-158 muss danach überarbeitet werden.
- K5 gerechnet (23.11.): Mit k = 2 parallelen Mäandern aus einem Rohr Ø 25 weicht die Verteilung um höchstens 2 % ab, Δp liegt bei ×3 bei 0,171 bar. K4 LFP: ΔT 7,6 K, T_max 34,1 °C. NMC: ΔT 1,3 K. Opus hat Re (etwa 1100) und Δp (Schätzung 0,16 bar) im Kopf nachgerechnet, beides passt. ENT-158 ist überarbeitet (wert gruppiert_k2). Offen für den Autor: ob ΔT ≤ 5 K die Spreizung zwischen den Zellen meint oder auch das Gefälle innerhalb einer Zelle.
- G5.9 im CAD (Sonnet, 23.11.): 0 Kollisionen, Breite 1430 mm, Länge +38 mm (LFP 2373, NMC 2273 mm), Platte −0,22 kg, je 2 Verteiler- und Sammelrohre Ø 25 zusammen 0,49 kg, Kosten +0,16 % (LFP) bzw. +0,11 % (NMC). Alles im Erwartungsband 

