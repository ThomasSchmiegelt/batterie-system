---
typ: anforderung
gruppe: "REQ-P"
methode: "S"
ebene: "System"
bewertung: "verfehlt (Kriterium Annahme, Autor offen)"
tags: ["anforderung", "bewertung/verfehlt"]
verifiziert_durch: ["sim/mechanik/x3_crash_g5/ergebnis.json::LFP_a.zellblock_vorderseite_dy_max_mm", "sim/mechanik/x3_crash_g5/ergebnis.json::LFP_b.zellblock_vorderseite_dy_max_mm", "sim/mechanik/x3_crash_g5/ergebnis.json::NMC_a.zellblock_vorderseite_dy_max_mm", "sim/mechanik/x3_crash_g5/ergebnis.json::NMC_b.zellblock_vorderseite_dy_max_mm"]
---
# REQ-P14

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

Mechanik: Stoß, Schwingung, Crash

- Wert (Lastenheft): Zellverschiebung ≤ 0,5 mm bei Pfahl 5 kJ und bei Quetschung nach R100 (100–105 kN) (Autor, Freigaberunde 2026-11-23)
- Priorität: Muss
- Vom Autor bestätigt: ja

## Verifikation (V-Modell-Matrix)

- Methode: S (A Analyse, S Simulation, I Inspektion, T Test, R Review)
- Ebene: System
- Kriterium: dy_a <= 0.5 mm [Autor (Freigaberunde 2026-11-23)]<br>dy_b <= 0.5 mm [Autor (Freigaberunde 2026-11-23)]
- Ist-Wert: [dy_a] LFP dy_a = 6.732 [sim/mechanik/x3_crash_g5/ergebnis.json :: LFP_a.zellblock_vorderseite_dy_max_mm]; NMC dy_a = 8.279 [sim/mechanik/x3_crash_g5/ergebnis.json :: NMC_a.zellblock_vorderseite_dy_max_mm]; [dy_b] LFP dy_b = 0.0188 [sim/mechanik/x3_crash_g5/ergebnis.json :: LFP_b.zellblock_vorderseite_dy_max_mm]; NMC dy_b = 2.591 [sim/mechanik/x3_crash_g5/ergebnis.json :: NMC_b.zellblock_vorderseite_dy_max_mm]
- Bewertung: **verfehlt (Kriterium Annahme, Autor offen)**
- Matrix: [[Dokument/06_verifikationsplan]] · Lastenheft: [[Dokument/01_lastenheft]] · Verfolgung: [[Dokument/03_anforderungsverfolgung]]

## Nachweisdateien
- [[Nachweis/sim_mechanik_x3_crash_g5_ergebnis.json|sim/mechanik/x3_crash_g5/ergebnis.json]]

## Vorgänge
- [[Vorgang/M1|M1]] – Mechanik: Zellverspannung, Eigenfrequenzen, Lagerung
- [[Vorgang/X1|X1]] – Seitencrash Pfahl, quasistatisch: Eindringung in Gehäuse/Querträger (CalculiX, plastisch, Kontakt)
- [[Vorgang/X2|X2]] – Seitencrash dynamisch (OpenRadioss, Installation nur nach Freigabe)

## Bauteile
- [[Bauteil/BT-120|BT-120]]
- [[Bauteil/BT-220|BT-220]]
- [[Bauteil/BT-240|BT-240]]
- [[Bauteil/BT-260|BT-260]]
- [[Bauteil/BT-500|BT-500]]
- [[Bauteil/BT-510|BT-510]]
- [[Bauteil/BT-530|BT-530]]
- [[Bauteil/BT-540|BT-540]]
- [[Bauteil/BT-550|BT-550]]
- [[Bauteil/BT-560|BT-560]]
