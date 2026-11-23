---
typ: befund
tags: ["befund"]
---
# B-BAT-002

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

B-BAT-002 (2026-11-12) „0 Belege“ hieß „nicht geprüft“: Zitate ohne „Beleg:“ rutschten durch

Quelle: [[Dokument/BEFUNDE]]

## Vorgänge
- [[Vorgang/R1|R1]] – Wissensaufbau W01-W15 (Chemie, Zelltypen, Spannung, Kabel, Steuerung, Struktur)
- [[Vorgang/R2|R2]] – Werkzeuge T01-T07 (Open Source Zellchemie, Elektroauslegung, Ersatzmodelle)
- [[Vorgang/R4|R4]] – Recherche prüfen: Zitate, Aussagen, Widersprüche -> BEFUNDE
- [[Vorgang/R5|R5]] – Werkzeugwahl festlegen (ENT): Zellmodell, Packmodell, Schaltung
- [[Vorgang/E3|E3]] – Steuerung/BMS: Messkonzept, Ladezustand, Ausgleich (Konzept, offene Software aus T06)
- [[Vorgang/E4|E4]] – Schaltungsmodell ngspice/Modelica: Vorladung, Kurzschluss
- [[Vorgang/X1|X1]] – Seitencrash Pfahl, quasistatisch: Eindringung in Gehäuse/Querträger (CalculiX, plastisch, Kontakt)
- [[Vorgang/X2|X2]] – Seitencrash dynamisch (OpenRadioss, Installation nur nach Freigabe)

## Text aus BEFUNDE.md

- T02, T05, T06, T08 (und W05) meldeten 0 bestätigte Belege. Ursache: PI zitierte wörtlich, aber ohne das Schlüsselwort, z. B. `Zweck: „foxBMS is a free, open …“ (URL)`; pruefe.py erkannte nur `Beleg: „…“ (URL)`.
- Gefahr: solche Zitate wären ungeprüft in die Ergebnisse gegangen. Behoben: pruefe.py prüft jedes Zitat ≥ 12 Zeichen mit Quellenangabe in Klammern (Skill web-recherche, auch Fusion).
- Neu geprüft: T05 6/0, T06 4/0, T08 9/0 (vorher 0/0). W05: 0/0 bleibt, PI meldet ehrlich „nicht gefunden“ (die Wikipedia-Seite zum BMS enthält kaum Kennwerte). T02: 0/1, Zitate kursiv mit angehängter Wortzählung, ein Satz ins Deutsche übersetzt → T02 bei R4 neu rechnen.
- Anweisungsartiger Text „ignore previous instructions“ in T02 stammt von PI selbst (Feststellung „kein solches Muster gefunden“), nicht aus den Quellen.
- Folge: Zählung „Belege bestätigt“ ist nur mit Blick auf „0“ aussagekräftig; 0 heißt jetzt: keine Zitate gefunden → Opus liest. Vorgang: [R2] [R4]
