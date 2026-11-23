---
typ: dokument
nr: "BAT-DOC-13"
version: "0.3"
status: "Entwurf"
tags: ["dokument"]
---
# BAT-DOC-13 – Stückliste Konstruktionsstand (SL3), Übersicht

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

- Datei: `docs/13_stueckliste`
- Version: 0.3
- Status: Entwurf
- Typ: Projektdokument (Dokumentenlenkung [[Dokument/00_dokumentenlenkung]])

## Genannte Anforderungen (Textvorkommen)
- –

## Genannte Entscheidungen, Befunde, Bauteile (Textvorkommen)
- –

## Vorgänge, die dieses Dokument nennen
- [[Vorgang/V1|V1]] – Lastenheft-Werte REQ-P01..P08 vorschlagen (Fahrzeug, kWh, Spannung, Leistung, Laden, Chemie, Bauraum, Temperatur)
- [[Vorgang/SL1|SL1]] – Grobe Stückliste aus Startsatz (Baugruppen, Mengen mit Herleitung)
- [[Vorgang/G4|G4]] – Pack: Zellanordnung, Querträger, Kühlplatte, Deckel
- [[Vorgang/SL2|SL2]] – Stückliste fortschreiben nach Auslegung (Mengen, Kauf/Eigen, Werkstoffe, Bezugsquellen)

## Inhalt (Kopie aus `docs/13_stueckliste.md`)

| Dok.-Nr. | BAT-DOC-13 | Version | 0.3 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Stückliste Konstruktionsstand (SL3), Übersicht | Ersteller | Claude Sonnet (KI), pm/bauteile/stueckliste_v3.py | Prüfer | Opus (Stichprobe), Mensch offen |

> **KI-generiert.** (KI-generiert (Claude Sonnet, 2026-11-19), Auftrag G5.1, ergänzt SL3.1 (Auftrag KO2).) Entwurf, nicht freigegeben. Ersetzt die grobe Stückliste v0.1 (`stueckliste.py`) in dieser Datei; die Positionen je Variante stehen in `13_stueckliste_LFP.md` und `13_stueckliste_NMC.md`.

| Größe | LFP | NMC |
|---|---|---|
| Positionen gesamt | 56 | 56 |
| Stufe K | 18 | 20 |
| Stufe F | 28 | 28 |
| Stufe H | 4 | 4 |
| Stufe - | 6 | 4 |
| Anteil H [%] | 7.1 | 7.1 |
| Positionen Masse offen | 10 | 8 |
| Masse gesamt [kg] | 626,768 | 486,362 |
| Masse CAD e2d [kg] | 620,566 | 483,153 |
| Abweichung gegen CAD [%] | 1.0 | 0.66 |
| Zellen | 250 | 868 |
| Energie [kWh] | 73.92 | 74.27 |

Quellen: `pm/bauteile/stueckliste_<V>.json` (Feld `pruefsummen`).

---
*KI-generiert (Claude Sonnet, 2026-11-19), Auftrag G5.1, ergänzt SL3.1 (Auftrag KO2). Entwurf, nicht freigegeben. Dokument BAT-DOC-13, Version 0.3.*

