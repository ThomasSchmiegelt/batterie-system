---
typ: befund
tags: ["befund"]
---
# B-BAT-004

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

B-BAT-004 (2026-11-16) Analyse: Was fehlt für die komplette Batterie (Struktur gegen Information)

Quelle: [[Dokument/BEFUNDE]]

## Vorgänge
- [[Vorgang/R1|R1]] – Wissensaufbau W01-W15 (Chemie, Zelltypen, Spannung, Kabel, Steuerung, Struktur)
- [[Vorgang/R2|R2]] – Werkzeuge T01-T07 (Open Source Zellchemie, Elektroauslegung, Ersatzmodelle)
- [[Vorgang/R3|R3]] – Patente P01-P10
- [[Vorgang/R4|R4]] – Recherche prüfen: Zitate, Aussagen, Widersprüche -> BEFUNDE
- [[Vorgang/R5|R5]] – Werkzeugwahl festlegen (ENT): Zellmodell, Packmodell, Schaltung
- [[Vorgang/V1|V1]] – Lastenheft-Werte REQ-P01..P08 vorschlagen (Fahrzeug, kWh, Spannung, Leistung, Laden, Chemie, Bauraum, Temperatur)
- [[Vorgang/SL1|SL1]] – Grobe Stückliste aus Startsatz (Baugruppen, Mengen mit Herleitung)
- [[Vorgang/C2|C2]] – Zellmodell LFP (PyBaMM Prada2013) auf langes Format skalieren
- [[Vorgang/C5|C5]] – Alterung (Zyklen, Kalender) und Vergleich NMC / Natrium-Ionen
- [[Vorgang/G1|G1]] – Zellmaße als ENT-Akten (aus W03/W08/P01, sonst Annahme)
- [[Vorgang/G4|G4]] – Pack: Zellanordnung, Querträger, Kühlplatte, Deckel
- [[Vorgang/K0|K0]] – Kühlart Luft gegen Wasser (1D-Wärmebilanz Schnellladen, W16), Entscheidung ENT
- [[Vorgang/E1|E1]] – Zellverbinder/Kabel: Querschnitt, Verluste, Erwärmung (Zielband als Annahme)
- [[Vorgang/E2|E2]] – Schutzkonzept: Sicherung, Schütze, Vorladung, Isolationswächter
- [[Vorgang/E3|E3]] – Steuerung/BMS: Messkonzept, Ladezustand, Ausgleich (Konzept, offene Software aus T06)
- [[Vorgang/E4|E4]] – Schaltungsmodell ngspice/Modelica: Vorladung, Kurzschluss
- [[Vorgang/U1|U1]] – ERWARTUNG Ersatzmodell: Zielgröße, Gültigkeitsbereich, Mindestgüte (z. B. Rangkorrelation)

## Text aus BEFUNDE.md

Fundstellen: `pm/bauteile/struktur.json`, `stueckliste.json`, `parameter.json`, `pm/startwerte.json`, `pm/entscheidungen/`, `forschung/ergebnis/*.pruefung.txt`. Erwartung: entfällt (Bestandsaufnahme, keine Rechnung).
1. **Struktur zu flach.** struktur.json hat 8 Bauteile. Merkmale gibt es nur bei BT-100 (5) und BT-200 (2). BT-300 bis BT-700 haben keine. Die Stückliste hat 37 Positionen, aber keine davon ist ein eigenes Bauteil. Folge: Für Gehäuse, Querträger, Kühlplatte, Zellverbinder usw. kann `pm.py pruefe` keine Akte annehmen, also gibt es kein Maß fürs CAD. Das ist der Hauptblocker.
2. **Keine Maßentscheidung.** parameter.json: alle 7 Merkmale `null`. ENT-001…003 betreffen Methoden. ENT-002 (PyBaMM) steht noch auf „vorgeschlagen“.
3. **Widerspruch Energie.** startwerte.json: 73,9 kWh brutto. stueckliste.json: 79,9 kWh (219s1p × 100 Ah × 3,65 V, beide Zellwerte Annahme). Die Zellzahl ist auf ganze Reihen gerundet, die Energie aber nicht zurückgeführt.
4. **Widerspruch Chemie gegen Vorbild.** Die Startwerte wählen NMC, weil die LFP-Packdichte als 180 Wh/L **angenommen** ist (startwerte.py, „Zelle × Füllgrad ~0,6“, unbelegt), nötig wären 214 Wh/L. Die Recherche belegt für Blade-LFP nur Werte je kg (190–210 Wh/kg Zelle, W03), keinen Wert je Liter. Die Stückliste führt deshalb eine „lang prismatische NMC-Zelle“. Für dieses Format gibt es in der Recherche keinen Beleg, das Blade-Format ist LFP (W03). Die Entscheidung LFP/NMC hängt an einer unbelegten Zahl.
5. **Belegte Zellmaße vorhanden.** W03, 0 Fehler: Long Blade 960 × 90 × 13,5 mm, Short Blade 450–580 mm. Sie passen in den angenommenen Bauraum 1,9 × 1,4 × 0,13 m (TAB_FZ Kompakt, Annahme). Damit könnte G1 starten, sobald die Chemie feststeht.
6. **Lücken bei Grenzwerten.** W04 (thermisches Durchgehen) liefert keine Batteriewerte, nur Digitallogik und Chemie. W05 hat 0 Belege. Für REQ-P09 (max. Zelltemperatur, Spreizung) und REQ-P11 gibt es nur W16 (Fenster +20…+30 °C). Die übrigen Grenzen bleiben Annahmen. Patente: nur P01, P02–P10 sind wegen der 503-Sperre leer (B-BAT-003).
7. **Prüfung offen.** R4 (Opus liest alle Ergebnisse) ist nicht abgeschlossen. Zitatfehler über 0: W01 2, W02 5, W06 1, W07 2, W09 3, W10 4, W11 2, W13 1, W14 1, T04 1, T07 1.
Folge: Vor dem CAD (G1/G4) stehen drei Schritte: (a) Bauteilbaum bis zur Stücklistenebene erweitern, mit Merkmalen; (b) Chemie LFP/NMC vom Autor entscheiden lassen, mit der Wh/L-Frage als offener Annahme; (c) Startsatz und Lastenheft freigeben (V2). Vorgang: [R4] [V1] [G1] [SL1]
