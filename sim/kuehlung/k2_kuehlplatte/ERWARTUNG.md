| Dok.-Nr. | ERW-K2 | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Erwartung K2: Kühlplatten auslegen (Kanäle, Durchfluss, Druckverlust, Kühlmittelerwärmung) | Ersteller | Claude Opus (KI) | Prüfer | – |

> KI-generiert, vor der Rechnung. Autor: „danach gehen wir die werte an und dann die rechnungen“. Akten ENT-088…090 (2 Platten je 8 mm, oben+unten), REQ-P05, REQ-P09.
## Eingaben (Herkunft)
- Wärme beim Schnellladen: LFP 250 × 55 W = 13,8 kW (K1, I²R); NMC 868 × 6,7 W = 5,8 kW (30 min, 32 A). Auf 2 Platten verteilt (Annahme hälftig).
- Kühlmittel Wasser-Glykol 50/50, ρ 1070, c 3300, Viskosität ≈ 3 mPa·s bei 25 °C (Annahme Lehrbuch); Eintritt 25 °C.
- Kanal (Annahme): Platte 8 mm = 2 × 1,5 mm Blech + 5 mm Kanalhöhe, Kanalbreite 10–20 mm, Stege 3 mm; parallel quer oder längs, Z- oder U-Führung.
- Ziel (Annahme): Kühlmittelerwärmung ≤ 5 K (sonst addiert sie sich zur Zellspreizung über das Pack), Druckverlust ≤ 0,5 bar je Pack, Strömung möglichst laminar-übergang ok.
## Erwartung
1. Durchfluss für ΔT_Kühlmittel 5 K: LFP ≈ 47 L/min, NMC ≈ 20 L/min (Opus-Skript); für 10 K die Hälfte. **LFP 47 L/min ist für einen Kompaktwagen hoch** → wahrscheinlich ΔT 8–10 K zulassen oder Ladeleistung als Grenze.
2. Druckverlust bei 20–30 parallelen Kanälen je Platte und 1,4 m Kanallänge: ≈ 0,1–0,4 bar (LFP), < 0,1 bar (NMC).
3. Re in den Kanälen ≈ 500–2000 (laminar/Übergang), h im Kanal laminar ≈ 500–1000 W/(m²K) → passt zur K0/K1-Annahme h 500.
4. Kühlmittelseitige Spreizung entlang des Packs ist neben REQ-P09 (in der Zelle) ein neuer Beitrag zur Zell-zu-Zell-Spreizung (offen beim Autor, ob Vorgabe).
## Verfehlt
h im Kanal < 300 W/(m²K) (dann K0/K1-Annahme zu optimistisch); Druckverlust > 1 bar bei Zielfluss.

## Nachtrag K2b (2026-11-19, Opus, vor der Rechnung): Blech 1/4/1 mm mit Mäander (ENT-152, Autor-Vorschlag)
Eingaben: Blech 1 mm Al (statt 1,5), Wasserraum 4 mm, Stege 3 mm (gelötet), Platte innen ≈ 1370 × 1990 (LFP) bzw. 1370 × 1890 (NMC). Mäander mit n Bahnen (n = 2, 4, 6, 8, gerade → Ein- und Austritt hinten), jede Bahn aus m parallelen Teilkanälen der Breite w (w = 6, 8, 10, 15, 20, 40 mm), Bahnen längs (in x) oder quer (in y). Durchfluss wie ENT-107/108 (LFP 23, NMC 20 L/min je Pack, hälftig je Platte). Umlenkung: Zuschlag ζ = 1,5 je Umlenkung (statt 30 % pauschal), Annahme Opus. Pad 1 mm k 3, Stegwirkungsgrad wie K2 (Steghöhe jetzt 4 mm).
Erwartung:
1. U ≥ 500 W/(m²K) nur mit w ≤ ≈ 10 mm. Breite Bahnen ohne Teilkanäle (w ≥ 40) liegen bei U ≈ 350–420 (Dh ≈ 8 mm, laminar Nu ≈ 5,4).
2. Δp wächst mit n etwa wie n² … n³ (Weg × Geschwindigkeit). Für w = 8, n = 4, LFP: Δp ≈ 0,05–0,2 bar; n = 8: ≈ 0,4–1 bar.
3. Auswahl voraussichtlich n = 4, w = 8 mm, Bahnen längs: U ≈ 550, Δp < 0,3 bar, hydraulische Leistung < 15 W.
4. Masse beider Platten ≈ 45 kg (Bleche 2 × 1 mm + Stege 27 % des Wasserraums).
Verfehlt, wenn: keine Variante U ≥ 500 bei Δp ≤ 0,5 bar erreicht (dann zurück an Opus: Höhe 4 mm zu klein oder Turbulatoren), oder Masse > 55 kg.

## Anforderung (Nachtrag)
- REQ-P09 (Vorgang K2, pm/plan/wissensnetz.py)

Vermerk: Nachtrag Sonnet aus wissensnetz.py, Prüfung Opus offen (2026-11-23). Die Zuordnung Rechenordner zu Vorgang K2 ist von Sonnet gewählt.
