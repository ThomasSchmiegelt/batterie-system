---
typ: anforderung
gruppe: "REQ-P"
methode: "S"
ebene: "Subsystem"
bewertung: "rechnerisch erfüllt (nicht validiert) (Kriterium Annahme, Autor offen)"
tags: ["anforderung", "bewertung/rechnerisch_erfüllt_nicht_validiert"]
verifiziert_durch: ["pm/bauteile/stueckliste_LFP.json::positionen[bt=BT-650].werkstoff", "sim/kuehlung/k5_parallel/ergebnis_verteiler.json::gruppen.faelle.k2_d25_x3.dp_bar", "sim/kuehlung/k5_parallel/ergebnis_verteiler.json::gruppen.faelle.k2_d25_x3.max_abw_pct"]
---
# REQ-P12

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

Kühlmittel und Anschlüsse

- Wert (Lastenheft): Kühlmittel Wasser-Glykol, Δp je Platte ≤ 0,5 bar, Verteilung ±10 % (Autor, Freigaberunde 2026-11-23)
- Priorität: Soll
- Vom Autor bestätigt: ja

## Verifikation (V-Modell-Matrix)

- Methode: S (A Analyse, S Simulation, I Inspektion, T Test, R Review)
- Ebene: Subsystem
- Kriterium: Kuehlmittel vorhanden [Autor (Freigaberunde 2026-11-23)]<br>dp_Platte <= 0.5 bar [Autor (Freigaberunde 2026-11-23)]<br>Verteilung_abw <= 10 % [Autor (Freigaberunde 2026-11-23)]
- Ist-Wert: [Kuehlmittel] LFP Kuehlmittel = vorhanden [pm/bauteile/stueckliste_LFP.json :: positionen[bt=BT-650].werkstoff]; [dp_Platte] dp_Platte = 0.1709 [sim/kuehlung/k5_parallel/ergebnis_verteiler.json :: gruppen.faelle.k2_d25_x3.dp_bar]; [Verteilung_abw] Verteilung_abw = 2.05 [sim/kuehlung/k5_parallel/ergebnis_verteiler.json :: gruppen.faelle.k2_d25_x3.max_abw_pct]
- Bewertung: **rechnerisch erfüllt (nicht validiert) (Kriterium Annahme, Autor offen)**
- Matrix: [[Dokument/06_verifikationsplan]] · Lastenheft: [[Dokument/01_lastenheft]] · Verfolgung: [[Dokument/03_anforderungsverfolgung]]

## Nachweisdateien
- [[Nachweis/pm_bauteile_stueckliste_LFP.json|pm/bauteile/stueckliste_LFP.json]]
- [[Nachweis/sim_kuehlung_k5_parallel_ergebnis_verteiler.json|sim/kuehlung/k5_parallel/ergebnis_verteiler.json]]

## Vorgänge
- [[Vorgang/K0|K0]] – Kühlart Luft gegen Wasser (1D-Wärmebilanz Schnellladen, W16), Entscheidung ENT

## Bauteile
- [[Bauteil/BT-600|BT-600]]
- [[Bauteil/BT-610|BT-610]]
- [[Bauteil/BT-630|BT-630]]
- [[Bauteil/BT-650|BT-650]]
- [[Bauteil/BT-660|BT-660]]
