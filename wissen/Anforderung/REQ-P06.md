---
typ: anforderung
gruppe: "REQ-P"
methode: "I"
ebene: "System"
bewertung: "nachgewiesen"
tags: ["anforderung", "bewertung/nachgewiesen"]
kriterium_aus: ["Autor"]
verifiziert_durch: ["cad/baukasten/ausgabe/ergebnis_LFP.json::teile", "cad/baukasten/ausgabe/ergebnis_NMC.json::teile"]
---
# REQ-P06

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

Zellchemie

- Wert (Lastenheft): zwei Varianten gleicher Spezifikation (Autor 2026-11-16): LFP-Blade prismatisch (ENT-005) und NMC811-Rundzelle 4680 (ENT-007…011); Baum ENT-012
- Priorität: Muss
- Vom Autor bestätigt: ja

## Verifikation (V-Modell-Matrix)

- Methode: I (A Analyse, S Simulation, I Inspektion, T Test, R Review)
- Ebene: System
- Kriterium: CAD_Pack LFP vorhanden [Autor]<br>CAD_Pack NMC vorhanden [Autor]
- Ist-Wert: [CAD_Pack LFP] LFP CAD_Pack = vorhanden [cad/baukasten/ausgabe/ergebnis_LFP.json :: teile]; [CAD_Pack NMC] NMC CAD_Pack = vorhanden [cad/baukasten/ausgabe/ergebnis_NMC.json :: teile]
- Bewertung: **nachgewiesen**
- Matrix: [[Dokument/06_verifikationsplan]] · Lastenheft: [[Dokument/01_lastenheft]] · Verfolgung: [[Dokument/03_anforderungsverfolgung]]

## Nachweisdateien
- [[Nachweis/cad_baukasten_ausgabe_ergebnis_LFP.json|cad/baukasten/ausgabe/ergebnis_LFP.json]]
- [[Nachweis/cad_baukasten_ausgabe_ergebnis_NMC.json|cad/baukasten/ausgabe/ergebnis_NMC.json]]

## Vorgänge
- [[Vorgang/V1|V1]] – Lastenheft-Werte REQ-P01..P08 vorschlagen (Fahrzeug, kWh, Spannung, Leistung, Laden, Chemie, Bauraum, Temperatur)
- [[Vorgang/V2|V2]] – Freigabe Lastenheft durch Autor
- [[Vorgang/C2|C2]] – Zellmodell LFP (PyBaMM Prada2013) auf langes Format skalieren
- [[Vorgang/C5|C5]] – Alterung (Zyklen, Kalender) und Vergleich NMC / Natrium-Ionen

## Bauteile
- [[Bauteil/BT-100|BT-100]]
- [[Bauteil/BT-110|BT-110]]
- [[Bauteil/BT-111|BT-111]]
- [[Bauteil/BT-112|BT-112]]
- [[Bauteil/BT-113|BT-113]]
- [[Bauteil/BT-114|BT-114]]
- [[Bauteil/BT-115|BT-115]]
- [[Bauteil/BT-116|BT-116]]
- [[Bauteil/BT-121|BT-121]]
- [[Bauteil/BT-122|BT-122]]
- [[Bauteil/BT-131|BT-131]]
- [[Bauteil/BT-132|BT-132]]
- [[Bauteil/BT-250|BT-250]]
