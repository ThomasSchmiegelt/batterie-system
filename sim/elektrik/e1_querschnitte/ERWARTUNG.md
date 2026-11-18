| Dok.-Nr. | ERW-E1 | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Erwartung E1: Ströme und Querschnitte (Zellverbinder, Reihenverbinder, HV-Hauptleitung), beide Varianten | Ersteller | Claude Opus (KI) | Prüfer | – |

> KI-generiert, vor der Rechnung. Autor 2026-11-17: „ja“ (E nach Freigabe ENT-092…095). REQ-P05 (LFP 20 min, NMC 30 min), ENT-006 800 V.
## Eingaben (Herkunft)
- Schnellladen 10→80 %: LFP 2,1C = 194 A (92,4 Ah, 250s1p); NMC 1,4C auf 92,5 Ah Gruppe = 130 A Pack, 32 A je Zelle (217s4p). Aus REQ-P05/Stückliste.
- Fahren: Spitze 150 kW für 10 s, Dauer 60 kW (**Annahmen**, Kompaktwagen). Bei 800 V Nenn: 188 A Spitze, 75 A Dauer; bei Entladeschluss (LFP 2,5 V·250 = 625 V; NMC 3,0 V·217 = 651 V) entsprechend mehr.
- Grenzen (**Annahmen**): Verbinder-Erwärmung ≤ 30 K über Kühlplatte bei Dauerlast, Stromdichte-Richtwert Al ≈ 2–3 A/mm², Cu ≈ 4–5 A/mm² (Lehrbuch, Annahme); Spannungsabfall gesamt ≤ 0,5 %.
## Erwartung
1. Maßgeblich: LFP Schnellladen 194 A dauernd (20 min) bzw. Spitze bei Entladeschluss ≈ 240 A.
2. LFP Reihenverbinder Al ≈ 70–100 mm² (z. B. 25 × 3 mm), 249 Stück.
3. NMC Gruppenverbinder (Parallel 4 + Reihe) Al ≈ 50–80 mm² für ≈ 130–230 A; Zellabgriff je Zelle ≈ 10–20 mm² (32 A Laden, Spitze ≈ 58 A).
4. HV-Hauptleitung Cu ≈ 35–50 mm².
5. Verluste in allen Verbindern bei 194 A < 100 W (< 0,1 % von 150 kW Ladeleistung).
## Verfehlt
Querschnitt außerhalb der Bänder um > 50 %; Verluste > 300 W.
