---
typ: vorgang
status: "fertig"
kritisch: false
dauer_AT: 0.5
es: 6
ef: 6.5
puffer: 20.0
ressourcen: ["Opus"]
tags: ["vorgang", "status/fertig"]
---
# SL1 – Grobe Stückliste aus Startsatz (Baugruppen, Mengen mit Herleitung)

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

- Status: fertig; Dauer 0.5 AT; ES 6, EF 6.5, Puffer 20.0
- Ressourcen: Opus
- Notiz: erledigt 2026-11-12 (Vorschlags-Startsatz)
- Vorgänger: [[Vorgang/V1|V1]]
- Nachfolger: [[Vorgang/SL2|SL2]]

## Anforderungen
- [[Anforderung/REQ-D01|REQ-D01]] – Jede Zahl ist rückverfolgbar (Rechnung mit Datei oder Quelle mit wörtlichem Beleg)

## Bauteile
- [[Bauteil/BT-000|BT-000]] – Batteriesystem

## Recherche
- –

## Stückliste
- [[Teil/100.1|100.1]] – Zelle (NMC, Zellformat offen; Rechenregel wie LFP-Platzhalter) (220×, K)
- [[Teil/200.1|200.1]] – Zellreihe zwischen Querträgern (Cell-to-Pack, ohne Module) (10×, E)
- [[Teil/200.2|200.2]] – Zwischenlage zwischen Zellen (Wärme- und Brandschutz, Quellausgleich) (220×, K)
- [[Teil/200.3|200.3]] – Wärmeleitmaterial Zelle → Kühlplatte (1×, K)
- [[Teil/200.4|200.4]] – Verspannung der Zellreihen (Endplatte/Band) (10×, E)
- [[Teil/200.5|200.5]] – Zellhalter (hält und teilt Rundzellen, Abstand für Kühlung und Isolation) (1×, K)
- [[Teil/300.1|300.1]] – BMS-Hauptsteuergerät (1×, K)
- [[Teil/300.2|300.2]] – Zellüberwachung (Spannung, Ausgleich) (14×, K)
- [[Teil/300.3|300.3]] – Temperaturfühler Zelle (55×, K)
- [[Teil/300.4|300.4]] – Strommessung (Shunt oder Hall) (1×, K)
- [[Teil/300.5|300.5]] – Isolationswächter (1×, K)
- [[Teil/300.6|300.6]] – Messleitungen bzw. Flexleiterplatte Zelle → Überwachung (14×, K)
- [[Teil/400.1|400.1]] – Zellverbinder (Zellabgriff, Plus und Minus je Zelle) (0×, E)
- [[Teil/400.2|400.2]] – Reihenverbinder (Reihenbrücke, bei p > 1 Gruppenbrücke) (219×, E)
- [[Teil/400.3|400.3]] – HV-Hauptleitung plus/minus im Pack (2×, K)
- [[Teil/500.1|500.1]] – Gehäusewanne (1×, E)
- [[Teil/500.2|500.2]] – Deckel mit Dichtung (1×, E)
- [[Teil/500.3|500.3]] – Querträger (11×, E)
- [[Teil/500.4|500.4]] – Seitenrahmen / Crashprofil (Seitencrash) (2×, E)
- [[Teil/500.5|500.5]] – Unterfahrschutz (1×, E)
- [[Teil/500.6|500.6]] – Befestigungspunkte am Fahrzeug (1×, E)
- [[Teil/500.7|500.7]] – Druckausgleichselement (atmend, wasserdicht) (1×, K)
- [[Teil/600.1|600.1]] – Kühlplatte (Wasser-Glykol) (1×, E)
- [[Teil/600.2|600.2]] – Verteiler und Sammler (1×, E)
- [[Teil/600.3|600.3]] – Kühlmittelanschlüsse Ein/Aus (2×, K)
- [[Teil/600.4|600.4]] – Temperaturfühler Kühlmittel (2×, K)
- [[Teil/600.5|600.5]] – Kühlmittel Wasser-Glykol (1×, K)
- [[Teil/600.6|600.6]] – Pumpe, Wärmetauscher/Kältemittelkühler (1×, S)
- [[Teil/700.1|700.1]] – Schaltbox (Gehäuse für Schütze, Vorladung, Hauptsicherung) (1×, E)
- [[Teil/700.2|700.2]] – Hauptschütz plus und minus (2×, K)
- [[Teil/700.3|700.3]] – Vorladeschütz mit Vorladewiderstand (1×, K)
- [[Teil/700.4|700.4]] – Hauptsicherung (ggf. pyrotechnischer Trenner) (1×, K)
- [[Teil/700.5|700.5]] – Service-Trennstecker (1×, K)
- [[Teil/700.6|700.6]] – HV-Steckverbinder Pack (Antrieb, Laden) (2×, K)
- [[Teil/700.7|700.7]] – NV-Steckverbinder (12 V, CAN, Sensorik) (1×, K)
- [[Teil/700.8|700.8]] – Entgasungsventil mit Entgasungskanal (1×, K)
- [[Teil/700.9|700.9]] – Heizung (Kälte, −20 °C laut REQ-P08) (1×, K)
- [[Teil/700.10|700.10]] – Gas-/Drucksensor Früherkennung thermisches Ereignis (1×, K)
- [[Teil/700.11|700.11]] – Kennzeichnung (Typschild, HV-Warnung) (1×, K)

## Software
- –

## Dokumente
- [[Dokument/13_stueckliste]]

## Ergebnisse
- ✓ `pm/bauteile/stueckliste.json`
- ✓ `docs/13_stueckliste.md`

## Befunde
- [[Befund/B-BAT-004|B-BAT-004]] – B-BAT-004 (2026-11-16) Analyse: Was fehlt für die komplette Batterie (Struktur gegen Information)

## Entscheidungen
- [[Entscheidung/ENT-001|ENT-001]] – Frage (?)
- [[Entscheidung/ENT-003|ENT-003]] – Frage (?)
- [[Entscheidung/ENT-004|ENT-004]] – Frage (?)
- [[Entscheidung/ENT-006|ENT-006]] – Frage (?)
- [[Entscheidung/ENT-013|ENT-013]] – Frage (?)
- [[Entscheidung/ENT-030|ENT-030]] – Frage (?)
- [[Entscheidung/ENT-091|ENT-091]] – Frage (?)
- [[Entscheidung/ENT-102|ENT-102]] – Entscheidung und Begründung (?)
- [[Entscheidung/ENT-103|ENT-103]] – Entscheidung und Begründung (?)
- [[Entscheidung/ENT-147|ENT-147]] – Frage (vorgeschlagen)

---
*KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten*
