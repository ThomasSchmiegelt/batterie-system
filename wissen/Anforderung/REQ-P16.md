---
typ: anforderung
gruppe: "REQ-P"
methode: "A"
ebene: "System"
bewertung: "nachgewiesen"
tags: ["anforderung", "bewertung/nachgewiesen"]
kriterium_aus: ["Autor"]
verifiziert_durch: ["pm/kosten/ergebnis_LFP.json::anteil_schaetzung_an_summe_pct", "pm/kosten/ergebnis_LFP.json::summe_eur_pack", "pm/kosten/ergebnis_NMC.json::anteil_schaetzung_an_summe_pct", "pm/kosten/ergebnis_NMC.json::summe_eur_pack"]
---
# REQ-P16

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

Herstellkosten je Variante ausweisen (€/kWh Pack, Anteile je Baugruppe)

- Wert (Lastenheft): kein Zielwert (Autor 2026-11-18: „lass offen“); Preise als Schätzung oder verifiziert kennzeichnen
- Priorität: Soll
- Vom Autor bestätigt: nein

## Verifikation (V-Modell-Matrix)

- Methode: A (A Analyse, S Simulation, I Inspektion, T Test, R Review)
- Ebene: System
- Kriterium: Kosten_Summe LFP vorhanden [Autor]<br>Kosten_Summe NMC vorhanden [Autor]<br>Anteil_Schaetzung LFP vorhanden [Autor]<br>Anteil_Schaetzung NMC vorhanden [Autor]
- Ist-Wert: [Kosten_Summe LFP] LFP Kosten_Summe = vorhanden [pm/kosten/ergebnis_LFP.json :: summe_eur_pack]; [Kosten_Summe NMC] NMC Kosten_Summe = vorhanden [pm/kosten/ergebnis_NMC.json :: summe_eur_pack]; [Anteil_Schaetzung LFP] LFP Anteil_Schaetzung = vorhanden [pm/kosten/ergebnis_LFP.json :: anteil_schaetzung_an_summe_pct]; [Anteil_Schaetzung NMC] NMC Anteil_Schaetzung = vorhanden [pm/kosten/ergebnis_NMC.json :: anteil_schaetzung_an_summe_pct]
- Bewertung: **nachgewiesen**
- Matrix: [[Dokument/06_verifikationsplan]] · Lastenheft: [[Dokument/01_lastenheft]] · Verfolgung: [[Dokument/03_anforderungsverfolgung]]

## Nachweisdateien
- [[Nachweis/pm_kosten_ergebnis_LFP.json|pm/kosten/ergebnis_LFP.json]]
- [[Nachweis/pm_kosten_ergebnis_NMC.json|pm/kosten/ergebnis_NMC.json]]

## Vorgänge
- –
