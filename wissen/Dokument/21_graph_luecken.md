---
typ: dokument
nr: "BAT-DOC-21"
version: "0.1"
status: "Entwurf"
tags: ["dokument"]
---
# BAT-DOC-21 – Lücken im Wissensgraphen

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

- Datei: `docs/21_graph_luecken`
- Version: 0.1
- Status: Entwurf
- Typ: Projektdokument (Dokumentenlenkung [[Dokument/00_dokumentenlenkung]])

## Genannte Anforderungen (Textvorkommen)
- [[Anforderung/REQ-D02|REQ-D02]]
- [[Anforderung/REQ-D06|REQ-D06]]
- [[Anforderung/REQ-G01|REQ-G01]]
- [[Anforderung/REQ-G02|REQ-G02]]
- [[Anforderung/REQ-P01|REQ-P01]]
- [[Anforderung/REQ-P04|REQ-P04]]
- [[Anforderung/REQ-P07|REQ-P07]]
- [[Anforderung/REQ-P08|REQ-P08]]
- [[Anforderung/REQ-P10|REQ-P10]]
- [[Anforderung/REQ-P11|REQ-P11]]
- [[Anforderung/REQ-P13|REQ-P13]]
- [[Anforderung/REQ-P14|REQ-P14]]

## Genannte Entscheidungen, Befunde, Bauteile (Textvorkommen)
- [[Bauteil/BT-210|BT-210]]
- [[Bauteil/BT-250|BT-250]]
- [[Entscheidung/ENT-001|ENT-001]]
- [[Entscheidung/ENT-002|ENT-002]]
- [[Entscheidung/ENT-003|ENT-003]]

## Vorgänge, die dieses Dokument nennen
- –

## Inhalt (Kopie aus `docs/21_graph_luecken.md`)

| Dok.-Nr. | BAT-DOC-21 | Version | 0.1 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Lücken im Wissensgraphen | Ersteller | Claude Sonnet (KI), pm/graph/frage.py luecken | Prüfer | – (Opus, Mensch offen) |

> **KI-generiert.** Entwurf, nicht vom Menschen freigegeben. Testprojekt „KI im Engineering“, kein Produkt. Erzeugt am 2026-11-23 aus `pm/graph/graph.json`, nicht von Hand bearbeiten.

## Anforderung ohne verifiziert_durch (9)
- REQ-D02: Jedes Dokument hat einen Kopf nach BAT-DOC-00 und ist als KI-generiert gekennzeichnet (offen)
- REQ-D06: Erwartung vor jeder Rechnung, Vergleich danach (offen)
- REQ-G01: Maschinenrichtlinie (EU 2023/1230) (offen)
- REQ-G02: Kennzeichnung, CO₂-Fußabdruck und Batteriepass nach VO (EU) 2023/1542 (offen)
- REQ-P04: Dauer- und Spitzenleistung Entladen (offen)
- REQ-P08: Umgebungstemperatur Betrieb und Laden (offen)
- REQ-P10: Lebensdauer (Zyklen, Jahre, Restkapazität) (offen)
- REQ-P11: Sicherheit: keine Ausbreitung des thermischen Durchgehens bzw. Warnzeit nach Norm (offen)
- REQ-P13: Schutzart, Isolation, Berührschutz (offen)

## Rechnung ohne gehoert_zu (keine ERWARTUNG mit Abschnitt „Anforderung“; Hinweis: erwähnte REQ) (4)
- `sim/chemie/varianten_lfp_nmc`  erwähnt: –
- `sim/chemie/vergleich_lfp_nmc`  erwähnt: REQ-D06, REQ-P01
- `sim/mechanik/m0_gehaeuse`  erwähnt: –
- `sim/mechanik/x3_crash_g5`  erwähnt: REQ-P11

## Rechnung ohne verwendet-Kante (eingaben.json fehlt oder ohne Präfixformat; Zusatzprüfung, nicht im Schema) (1)
- `sim/mechanik/m0_gehaeuse`

## Entscheidung ohne belegt_durch (3)
- ENT-001: PI recherchiert ohne Werkzeuge in drei Stufen (entschieden (Autor, Regel aus Moltbot 2026-11-11))
- ENT-002: Zellmodell mit PyBaMM (entschieden (Mensch))
- ENT-003: Opus leitet und verteilt an Sonnet, Haiku, PI ohne Rückfrage (entschieden (Autor))

## Merkmal ohne legt_fest, das eine Rechnung verwendet (stärkste Lücke: Rechnung nutzt Wert ohne Akte) (2)
- BT-210.zellen_je_reihe
- BT-250.zellabstand_mm

## Merkmal ohne legt_fest, aber mit Wert in parameter*.json (0)

## Merkmal ohne legt_fest gesamt: 99 von 202

## Anforderung „verfehlt“, deren Kriterium eine Annahme ist (4)
- REQ-P07 → annahme_opus:REQ-P07.H (Kriterium H <= 130 (Annahme Opus))
- REQ-P07 → startwert:abgeleitet.masse_kg (Startwert (Vorschlag))
- REQ-P14 → annahme_opus:REQ-P14.dy_a (Kriterium dy_a <= 0.5 (Annahme Opus))
- REQ-P14 → annahme_opus:REQ-P14.dy_b (Kriterium dy_b <= 0.5 (Annahme Opus))

## Unaufgelöste Kanten (Ziel nicht vorhanden) (0)


---
*KI-generiert (Claude Sonnet, 2026-11-23). Status Entwurf. Freigabe nur durch den Autor.*

