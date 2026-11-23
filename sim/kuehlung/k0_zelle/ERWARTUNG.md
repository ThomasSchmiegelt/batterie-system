| Dok.-Nr. | ERW-K0 | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Erwartung K0: Wärmesimulation einer Zelle je Variante (Elmer) | Ersteller | Claude Opus (KI) | Prüfer | – (Mensch offen) |

> **KI-generiert.** Vor der Rechnung. Eingaben `eingaben.json`. Vorgang K0 (Vorstudie Kühlung), REQ-P05/P09. Vorab-Schätzung mit Opus-Skript (Wärme I²R, Wärmeweg q·L²/2k).

## Erwartung
1. **Wärme:** LFP 92 Ah, R 1,46 mΩ: 1C ≈ 12,5 W, 2,1C ≈ 55 W je Zelle. 4680, R 6,5 mΩ: 1C ≈ 3,5 W, 2,1C ≈ 15 W. Je Volumen erzeugt die 4680 etwa doppelt so viel Wärme (W20 sagt qualitativ dasselbe).
2. **Leitfähigkeit:** Schichtmischung LFP: in der Ebene ≈ 28, quer ≈ 1,0 W/(m·K). Gemessen (W18, andere LFP-Zelle): 20 bzw. 4,1. In der Ebene passt die Mischung (± 40 %), **quer liegt sie viermal zu tief** → Stoffwerte der nassen Beschichtung sind unsicher; Hauptfall LFP mit W18-Werten. 4680: axial ≈ 21, radial ≈ 1,2 W/(m·K).
3. **L1 (1C, Boden gekühlt, stationär):** LFP ΔT in der Zelle ≈ 3–4 K (Weg 90 mm in der Ebene), T_max ≈ 30 °C. 4680 ΔT ≈ 4–5 K axial, T_max ≈ 31 °C. Beide im Ziel (Annahme 45 °C, 5 K).
4. **L2 (2,1C, 20 min, transient):** stationär wären LFP ≈ 13 K, 4680 ≈ 18 K Spreizung; in 20 min wird der stationäre Zustand nicht ganz erreicht (Zeitkonstante LFP grob m·c/(h·A) ≈ 1850 g · 1112 / (500 · 0,0095 m²) ≈ 430 s → nahezu stationär). Erwartet: LFP T_max ≈ 40–45 °C, ΔT ≈ 10–13 K; 4680 Boden T_max ≈ 45–50 °C, ΔT ≈ 15–18 K → **ΔT-Ziel 5 K von beiden verfehlt**, 4680 auch T_max knapp.
5. **K2 (4680 seitlich):** radiale Leitung schlecht (1,2) → ΔT eher größer als Boden-Kühlung; erwartet 20 K oder mehr.
6. **Stärkste Annahmen:** Innenwiderstand (Faktor 2 Band), h-Wert, Quer-/Radialleitfähigkeit.
## Verfehlt
- Wärme L1 außerhalb ±10 % von Punkt 1 (Rechenfehler).
- LFP L1 ΔT > 8 K oder < 1 K.
- Energiebilanz (Wärmestrom am Kühlrand = Quelle, stationär) weicht > 2 % ab.

## Anforderung (Nachtrag)
- REQ-P09 (Vorgang K0, pm/plan/wissensnetz.py)
- REQ-P12 (Vorgang K0, pm/plan/wissensnetz.py)

Vermerk: Nachtrag Sonnet aus wissensnetz.py, Prüfung Opus offen (2026-11-23). Die Zuordnung Rechenordner zu Vorgang K0 ist von Sonnet gewählt.
