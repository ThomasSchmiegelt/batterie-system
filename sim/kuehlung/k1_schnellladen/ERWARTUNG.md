| Dok.-Nr. | ERW-K1 | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Erwartung K1: Schnellladen in den Griff bekommen (Ladeprofile, Kühlung, Begrenzung) | Ersteller | Claude Opus (KI) | Prüfer | – (Mensch offen) |

> **KI-generiert.** Vor der Rechnung. Autor 2026-11-17: „Ja das schnellladen müssen wir in den griff bekommen. man läd schwellenartig könnte auch sein, oder nur bestimmte zellen im wechsel, kühlen kann man auch und dann natürlcih begrenzen.“ Modell, Netz, Stoffwerte wie K0 (`../k0_zelle/eingaben.json`), Vorgabe REQ-P09: T_max ≤ 45 °C, Spreizung ≤ 5 K. Vorab-Schätzung mit Opus-Skript.

## Grundsatz vorab (Physik)
Bei festem Ladehub (10 → 80 %) und fester Zeit erzeugt **konstanter Strom die wenigste Joulewärme** (∫I²R dt ist bei gleichem ∫I dt minimal für I = konst.). Stufen- und Pulsprofile helfen thermisch nur, wenn sie Wärme an den Anfang legen, solange die Zelle kalt ist; elektrochemisch (Lithium-Plating) können sie trotzdem sinnvoll sein – das bildet K1 **nicht** ab (Zellmodell C1–C3).
„Nur bestimmte Zellen im Wechsel“: In einer Reihenschaltung führen alle Zellen denselben Strom. LFP 250s1p: nicht möglich. NMC 217s4p: Abschalten einer von vier Parallelzellen erhöht den Strom der übrigen um 4/3 (Wärme × 1,8). Packhälften im Wechsel = Puls mit 50 % Takt bei doppeltem Strom → Wärme × 2. Wird als Profil P2 gerechnet.

## Profile (alle 10 → 80 %, Kühlung K1 h = 500, Start 25 °C)
| Profil | Verlauf | Wärme relativ zu P0 | erwartet LFP | erwartet NMC |
|---|---|---|---|---|
| P0 | konstant 2,1C, 20 min (= K0 L2) | 1,00 | 43,1 °C / 10,6 K | 53,6 °C / 16,0 K |
| P1 Stufen | 3C bis 40 %, 2C bis 65 %, 1,385C bis 80 %, 20 min | 1,09 | Spitze ΔT ≈ 10–12 K (während 3C), am Ende ≈ 5–7 K; T_max ± 2 K zu P0 | ähnlich, Spitze ΔT ≈ 15–18 K |
| P2 Puls/Wechsel | 4,2C an / 0 aus, Takt 60 s, 50 %, 20 min | 2,00 | T_max ≈ 55–60 °C, ΔT schwankt um ≈ 20 K | T_max ≈ 75–85 °C → schlechter |
| P3 begrenzt | konstant 1,68C, 25 min | 0,80 | ≈ 40 °C / ≈ 7–8 K | ≈ 47–50 °C / ≈ 11–13 K |
| P4 begrenzt | konstant 1,4C, 30 min | 0,67 | ≈ 37 °C / ≈ 5–6 K | ≈ 42–44 °C / ≈ 8–9 K |
Stationär nötig für 5 K: LFP ≤ 1,29C (≈ 33 min), NMC ≤ 1,02C (≈ 41 min).

## Kühlung (Profil P0)
| Fall | Änderung | erwartet LFP | erwartet NMC |
|---|---|---|---|
| Kh1000 | h = 1000 W/(m²K) | T_max −3…−5 K, ΔT unverändert | T_max −8…−10 K, ΔT unverändert |
| Kh2000 | h = 2000 | T_max −5…−8 K, ΔT unverändert | T_max ≈ 41–44 °C ✓, ΔT ≈ 16 K ✗ |
| K3 beidseitig | Kühlplatte unten **und** oben (LFP Schmalseiten; NMC Boden und Deckel, Annahme elektrisch isoliert), h = 500 | ΔT ≈ ÷4 → ≈ 3 K ✓, T_max ≈ 35 °C ✓ | ΔT ≈ 4–5 K (knapp), T_max ≈ 38–40 °C ✓ |
| V15 | Start 15 °C (Vorkühlung), K1 | T_max −10 K, ΔT unverändert | dito |
**Kernaussage vorab:** Die Spreizung hängt am Wärmeweg in der Zelle, nicht am h-Wert. Nur **kürzerer Weg (beidseitig)** oder **kleinerer Strom** bringt ΔT unter 5 K. Besserer Kontakt/Vorkühlung senkt nur T_max.
## Kombinationen
K3 + P1, K3 + P0 mit h 1000, NMC Kh2000 + P3 – erwartet: LFP K3 erfüllt beides bei 20 min; NMC braucht K3 + h ≥ 1000 oder K3 + P3.
## Verfehlt
- Wärmeintegral eines Profils weicht > 2 % von der Tabelle ab (Profil falsch umgesetzt).
- P0 weicht > 0,3 K von K0 L2 ab.
- K3 senkt ΔT bei LFP um weniger als die Hälfte (dann Wärmeweg anders als gedacht).

## Nachtrag K1b (2026-11-17, vor der Rechnung) – Wärme oben über Verbinder und Isolierpad (ENT-092…095, vorgeschlagen)
Autor: „ja, starte K1b“. Modell (Annahme Opus): oberer Kühlrand der 4680 als Ersatz-Wärmeübergang h_eff = φ / (1/h + t_pad/k_pad + t_v/k_v), Bedeckung φ = 0,5 (Band 0,3–0,7), Pad 1 mm, k_pad 3 W/mK (Band 1–6), Verbinder Al 1,5 mm (k 237), h 500 → **h_eff ≈ 214 W/(m²K)** (Band ≈ 100–330). Unten unverändert (h 500 über Becherboden + Tab-Scheibe wie Nachtrag).
Erwartung NMC: P0 (20 min) K3b ≈ 44–46 °C / 8–10 K (zwischen K1 53,6/16,0 und K3 38,9/5,8); P3 (25 min) ≈ 38–40 °C / 5,5–7 K → 5 K knapp verfehlt; P4 (30 min) ≈ 35 °C / ≈ 4,5–5 K → knapp erfüllt. Stärkster Hebel: Bedeckung φ und k_pad.
Verfehlt: P0 K3b außerhalb 41–49 °C; h_eff im Modell ≠ Formel ± 1 %.

## Nachtrag K1c (2026-11-17, vor der Rechnung) – Wärme aus C2 statt I²R-Schätzung
- LFP: gemessener Blade-10-s-Widerstand 25 °C 0,877 mΩ (Test#5 über C2) → unsere 92,4-Ah-Zelle 1,28 mΩ → 48 W bei 2,1C (statt 55 W). Fall K3 P0 erwartet ≈ 32,8 °C / ≈ 4,0 K (Skalierung ~0,87 auf Erwärmung und ΔT).
- NMC 4680, 1,5C CC-CV 10→80 % in 29,7 min (C2): Wärme zeitabhängig aus `sim/chemie/c2_kalibrierung/schnellladen_Q_t.csv`; zwei Maße: Modell gesamt (mittel 7,4 W) und I·ΔU (mittel 11,5 W, konservativ). K3b: erwartet mit 7,4 W ≈ 34–35 °C / 4,2–4,6 K (knapp erfüllt), mit 11,5 W ≈ 38–40 °C / 6–7 K (**5 K verfehlt**).
- Verfehlt: Wärmeintegral ≠ CSV ± 2 %.

## Anforderung (Nachtrag)
- REQ-D06 (Vorgang K1, pm/plan/wissensnetz.py)
- REQ-P09 (Vorgang K1, pm/plan/wissensnetz.py)

Vermerk: Nachtrag Sonnet aus wissensnetz.py, Prüfung Opus offen (2026-11-23). Die Zuordnung Rechenordner zu Vorgang K1 ist von Sonnet gewählt.
