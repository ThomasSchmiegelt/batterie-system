---
typ: anforderung
gruppe: "REQ-P"
methode: "I"
ebene: "Subsystem"
bewertung: "nachgewiesen (Kriterium Annahme, Autor offen)"
tags: ["anforderung", "bewertung/nachgewiesen"]
verifiziert_durch: ["pm/bauteile/stueckliste_LFP.json::positionen[bt=BT-320].pos", "pm/bauteile/stueckliste_LFP.json::positionen[bt=BT-330].pos", "pm/bauteile/stueckliste_LFP.json::positionen[bt=BT-350].pos", "pm/bauteile/stueckliste_NMC.json::positionen[bt=BT-320].pos", "pm/bauteile/stueckliste_NMC.json::positionen[bt=BT-330].pos", "pm/bauteile/stueckliste_NMC.json::positionen[bt=BT-350].pos"]
---
# REQ-P15

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

Messung und BMS: Zellspannung, Temperatur, Isolationswächter

- Wert (Lastenheft): Umfang offen
- Priorität: Muss
- Vom Autor bestätigt: nein

## Verifikation (V-Modell-Matrix)

- Methode: I (A Analyse, S Simulation, I Inspektion, T Test, R Review)
- Ebene: Subsystem
- Kriterium: CMU vorhanden [Annahme Opus]<br>Temperaturfuehler vorhanden [Annahme Opus]<br>Isolationswaechter vorhanden [Annahme Opus]
- Ist-Wert: [CMU] LFP CMU = vorhanden [pm/bauteile/stueckliste_LFP.json :: positionen[bt=BT-320].pos]; NMC CMU = vorhanden [pm/bauteile/stueckliste_NMC.json :: positionen[bt=BT-320].pos]; [Temperaturfuehler] LFP Temperaturfuehler = vorhanden [pm/bauteile/stueckliste_LFP.json :: positionen[bt=BT-330].pos]; NMC Temperaturfuehler = vorhanden [pm/bauteile/stueckliste_NMC.json :: positionen[bt=BT-330].pos]; [Isolationswaechter] LFP Isolationswaechter = vorhanden [pm/bauteile/stueckliste_LFP.json :: positionen[bt=BT-350].pos]; NMC Isolationswaechter = vorhanden [pm/bauteile/stueckliste_NMC.json :: positionen[bt=BT-350].pos]
- Bewertung: **nachgewiesen (Kriterium Annahme, Autor offen)**
- Matrix: [[Dokument/06_verifikationsplan]] · Lastenheft: [[Dokument/01_lastenheft]] · Verfolgung: [[Dokument/03_anforderungsverfolgung]]

## Nachweisdateien
- [[Nachweis/pm_bauteile_stueckliste_LFP.json|pm/bauteile/stueckliste_LFP.json]]
- [[Nachweis/pm_bauteile_stueckliste_NMC.json|pm/bauteile/stueckliste_NMC.json]]

## Vorgänge
- [[Vorgang/E3|E3]] – Steuerung/BMS: Messkonzept, Ladezustand, Ausgleich (Konzept, offene Software aus T06)

## Bauteile
- [[Bauteil/BT-300|BT-300]]
- [[Bauteil/BT-310|BT-310]]
- [[Bauteil/BT-320|BT-320]]
- [[Bauteil/BT-330|BT-330]]
- [[Bauteil/BT-340|BT-340]]
- [[Bauteil/BT-360|BT-360]]
- [[Bauteil/BT-361|BT-361]]
- [[Bauteil/BT-700|BT-700]]
- [[Bauteil/BT-740|BT-740]]
