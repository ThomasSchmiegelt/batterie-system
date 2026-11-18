---
typ: vorgang
status: "ohne Nachweis"
kritisch: false
dauer_AT: 1
es: 21.0
ef: 22.0
puffer: 5.5
ressourcen: ["Sonnet", "Opus"]
tags: ["vorgang", "status/ohneNachweis"]
---
# SL2 – Stückliste fortschreiben nach Auslegung (Mengen, Kauf/Eigen, Werkstoffe, Bezugsquellen)

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

- Status: ohne Nachweis; Dauer 1 AT; ES 21.0, EF 22.0, Puffer 5.5
- Ressourcen: Sonnet, Opus
- Notiz: lebendes Dokument BAT-DOC-13
- Vorgänger: [[wissen/Vorgang/SL1|SL1]], [[wissen/Vorgang/G5|G5]], [[wissen/Vorgang/E2|E2]], [[wissen/Vorgang/E3|E3]], [[wissen/Vorgang/K5|K5]], [[wissen/Vorgang/L1|L1]], [[wissen/Vorgang/X1|X1]]
- Nachfolger: [[wissen/Vorgang/B1|B1]], [[wissen/Vorgang/B5|B5]]

## Anforderungen
- [[wissen/Anforderung/REQ-D01|REQ-D01]] – Jede Zahl ist rückverfolgbar (Rechnung mit Datei oder Quelle mit wörtlichem Beleg)
- [[wissen/Anforderung/REQ-D11|REQ-D11]] – Jede Entscheidung als Akte an Bauteil und Merkmal gebunden; CAD-Maße nur aus diesen Akten

## Bauteile
- [[wissen/Bauteil/BT-000|BT-000]] – Batteriesystem

## Recherche
- –

## Stückliste
- [[wissen/Teil/100.1|100.1]] – Zelle (NMC, Zellformat offen; Rechenregel wie LFP-Platzhalter) (220×, K)
- [[wissen/Teil/200.1|200.1]] – Zellreihe zwischen Querträgern (Cell-to-Pack, ohne Module) (10×, E)
- [[wissen/Teil/200.2|200.2]] – Zwischenlage zwischen Zellen (Wärme- und Brandschutz, Quellausgleich) (220×, K)
- [[wissen/Teil/200.3|200.3]] – Wärmeleitmaterial Zelle → Kühlplatte (1×, K)
- [[wissen/Teil/200.4|200.4]] – Verspannung der Zellreihen (Endplatte/Band) (10×, E)
- [[wissen/Teil/200.5|200.5]] – Zellhalter (hält und teilt Rundzellen, Abstand für Kühlung und Isolation) (1×, K)
- [[wissen/Teil/300.1|300.1]] – BMS-Hauptsteuergerät (1×, K)
- [[wissen/Teil/300.2|300.2]] – Zellüberwachung (Spannung, Ausgleich) (14×, K)
- [[wissen/Teil/300.3|300.3]] – Temperaturfühler Zelle (55×, K)
- [[wissen/Teil/300.4|300.4]] – Strommessung (Shunt oder Hall) (1×, K)
- [[wissen/Teil/300.5|300.5]] – Isolationswächter (1×, K)
- [[wissen/Teil/300.6|300.6]] – Messleitungen bzw. Flexleiterplatte Zelle → Überwachung (14×, K)
- [[wissen/Teil/400.1|400.1]] – Zellverbinder (Zellabgriff, Plus und Minus je Zelle) (0×, E)
- [[wissen/Teil/400.2|400.2]] – Reihenverbinder (Reihenbrücke, bei p > 1 Gruppenbrücke) (219×, E)
- [[wissen/Teil/400.3|400.3]] – HV-Hauptleitung plus/minus im Pack (2×, K)
- [[wissen/Teil/500.1|500.1]] – Gehäusewanne (1×, E)
- [[wissen/Teil/500.2|500.2]] – Deckel mit Dichtung (1×, E)
- [[wissen/Teil/500.3|500.3]] – Querträger (11×, E)
- [[wissen/Teil/500.4|500.4]] – Seitenrahmen / Crashprofil (Seitencrash) (2×, E)
- [[wissen/Teil/500.5|500.5]] – Unterfahrschutz (1×, E)
- [[wissen/Teil/500.6|500.6]] – Befestigungspunkte am Fahrzeug (1×, E)
- [[wissen/Teil/500.7|500.7]] – Druckausgleichselement (atmend, wasserdicht) (1×, K)
- [[wissen/Teil/600.1|600.1]] – Kühlplatte (Wasser-Glykol) (1×, E)
- [[wissen/Teil/600.2|600.2]] – Verteiler und Sammler (1×, E)
- [[wissen/Teil/600.3|600.3]] – Kühlmittelanschlüsse Ein/Aus (2×, K)
- [[wissen/Teil/600.4|600.4]] – Temperaturfühler Kühlmittel (2×, K)
- [[wissen/Teil/600.5|600.5]] – Kühlmittel Wasser-Glykol (1×, K)
- [[wissen/Teil/600.6|600.6]] – Pumpe, Wärmetauscher/Kältemittelkühler (1×, S)
- [[wissen/Teil/700.1|700.1]] – Schaltbox (Gehäuse für Schütze, Vorladung, Hauptsicherung) (1×, E)
- [[wissen/Teil/700.2|700.2]] – Hauptschütz plus und minus (2×, K)
- [[wissen/Teil/700.3|700.3]] – Vorladeschütz mit Vorladewiderstand (1×, K)
- [[wissen/Teil/700.4|700.4]] – Hauptsicherung (ggf. pyrotechnischer Trenner) (1×, K)
- [[wissen/Teil/700.5|700.5]] – Service-Trennstecker (1×, K)
- [[wissen/Teil/700.6|700.6]] – HV-Steckverbinder Pack (Antrieb, Laden) (2×, K)
- [[wissen/Teil/700.7|700.7]] – NV-Steckverbinder (12 V, CAN, Sensorik) (1×, K)
- [[wissen/Teil/700.8|700.8]] – Entgasungsventil mit Entgasungskanal (1×, K)
- [[wissen/Teil/700.9|700.9]] – Heizung (Kälte, −20 °C laut REQ-P08) (1×, K)
- [[wissen/Teil/700.10|700.10]] – Gas-/Drucksensor Früherkennung thermisches Ereignis (1×, K)
- [[wissen/Teil/700.11|700.11]] – Kennzeichnung (Typschild, HV-Warnung) (1×, K)

## Software
- –

## Dokumente
- [[docs/13_stueckliste]]

## Ergebnisse
- ohne Nachweisdatei

## Befunde
- –

## Entscheidungen
- [[wissen/Entscheidung/ENT-001|ENT-001]] – Frage (?)
- [[wissen/Entscheidung/ENT-003|ENT-003]] – Frage (?)
- [[wissen/Entscheidung/ENT-004|ENT-004]] – Frage (?)
- [[wissen/Entscheidung/ENT-006|ENT-006]] – Frage (?)
- [[wissen/Entscheidung/ENT-013|ENT-013]] – Frage (?)
- [[wissen/Entscheidung/ENT-030|ENT-030]] – Frage (?)
- [[wissen/Entscheidung/ENT-091|ENT-091]] – Frage (?)
- [[wissen/Entscheidung/ENT-102|ENT-102]] – Entscheidung und Begründung (?)
- [[wissen/Entscheidung/ENT-103|ENT-103]] – Entscheidung und Begründung (?)

---
*KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten*
