# ERGEBNIS K5: gruppierte Parallelführung (ENT-158, ERWARTUNG Nachtrag 1)

| Dokument | BAT-K5-ERG, Version 0.2, Status Entwurf, Ersteller Claude Sonnet 5.5 (Auftrag Opus 2026-11-23), Prüfer Opus (offen), Stand 2026-11-23 |
|---|---|

> **KI-generiert (Claude Sonnet), Entwurf, nicht freigegeben.**

Rechnung `verteiler.py` (1D-Netz, Sekunden), Bilder `bilder.py`, Daten `ergebnis_verteiler.json` (Abschnitt `gruppen`; alte Einzelkanal-Variante unter `faelle`, als verworfen gekennzeichnet). K4 V4: `../k3_gesamt/k4_elmer.py` (Gruppenzahl aus `gruppen.bestes`). Annahme Sonnet: ζ = 1 je T-Abzweig bezogen auf die Rohrgeschwindigkeit; Abzweigteilung = Plattenbreite/k; Impulsbeiwert 1.

## Verteilung und Δp (ergebnis_verteiler.json, gruppen.faelle, Durchfluss ×3)
| k (Bahnen/Gruppe) | Rohr | max. Abweichung | Δp [bar] | beide Kriterien (±10 %, < 0,22 bar) |
|---|---|---|---|---|
| 2 (4) | Ø 25 | 2,0 % | 0,171 | ja (bestes) |
| 2 (4) | Ø 20 | 4,7 % | 0,182 | ja |
| 4 (2) | Ø 25 | 15,2 % | 0,046 | nein |
| 4 (2) | Ø 20 | 34,2 % | 0,057 | nein |
| 8 (1) | Ø 25 | 76,6 % | 0,017 | nein |
| 8 (1) | Ø 20 | 159,6 % | 0,030 | nein |
Mäander K2b ×3: 0,700 bar. Staudruck im Rohr ×3: 0,007 (Ø 25), 0,018 bar (Ø 20). Bild: `verteilung.png`, `dp_durchfluss.png`.
## K4 V4 (k = 2, Ø 25, ×3; ../k3_gesamt/elmer_*_V4/ergebnis.json)
Log (rechnen/log_K4_*_V4.txt): LFP Re 1139, u 0,60 m/s, h_Kanal 532, h_eff 771 W/m²K, ΔT_Fluid 3,39 K; NMC Re 991, h_Kanal 517, h_eff 748 W/m²K, ΔT_Fluid 1,67 K.
| Variante | LFP T_max [°C] | LFP ΔT [K] | NMC T_max [°C] | NMC ΔT [K] |
|---|---|---|---|---|
| V0 | 42,6 | 16,4 | 34,1 | 5,9 |
| V3 | 34,8 | 8,1 | 30,1 | 1,5 |
| V4 | 34,1 | 7,6 | 29,8 | 1,3 |
(V1/V2 siehe k3_gesamt/ERGEBNIS.md.) Bild: `k4_vergleich_V0_V3_V4.png` (angesehen; Feld bei V4 über die Fläche nahezu gleichmäßig, Randzonen adiabat).
## K4 V4p: gebaute Variante ohne Gegenlauf (Sonnet, 2026-11-23, Auftrag Opus; ../k3_gesamt/elmer_*_V4p/ergebnis.json)
V4p = V4 mit gleichsinnig durchströmter Ober- und Unterplatte, wie das CAD G5.9 gebaut ist (Steigblöcke gemeinsam). Hinweis: Im Parallelzweig von `k4_elmer.py` wurde V_GEGEN vorher nicht abgefragt, die obere Platte lief dort immer gegensinnig. Erster V4p-Lauf lieferte deshalb dieselben Zahlen wie V4 und wurde verworfen; nach der Korrektur (`Tf_top = Tf`, wenn V_GEGEN falsch) neu gerechnet. V4 selbst ändert sich nicht. Logs rechnen/log_K4_{LFP,NMC}_V4p.txt.
| Variante | LFP T_max [°C] | LFP ΔT [K] | NMC T_max [°C] | NMC ΔT [K] |
|---|---|---|---|---|
| V4 (Gegenlauf) | 34,1 | 7,6 | 29,8 | 1,3 |
| V4p (gebaut) | 35,6 | 9,6 | 30,6 | 2,6 |
Gegenlauf bringt damit 1,4 bis 2,0 K weniger T_max-Anstieg bzw. ΔT (LFP ΔT 2,0 K, NMC 1,3 K). Erwartung Opus (vorher): LFP ΔT 8,5–10 K, T_max 35–37 °C: erfüllt. NMC ΔT < 2 K: **verfehlt** (2,6 K), ΔT_Fluid NMC 1,7 K, Gegenlauf wirkt dort stärker als erwartet. Ziel ΔT ≤ 5 K (Annahme Opus): LFP verfehlt (wie V4), NMC erreicht. Bild: `k4_vergleich_V0_V3_V4_V4p.png` (Skript `k4_vergleich.py`, angesehen).
## Bezug zur Erwartung
Erfüllt: k = 2 verteilt auf ±5 % (2,0/4,7 %), Δp 0,15–0,2 bar (0,171/0,182); k = 4 Δp 0,04–0,08, mit Ø 25 ±10 % **knapp verfehlt** (15,2 %); k = 8 > ±20 %. K4 LFP ΔT 7,6 K im Band 6–8, T_max 34,1 °C im Band 33–36; NMC 1,3 K unter 2 K. Das Ziel 5 K wird nicht erreicht (wie erwartet).
## Offen
Mäander mit k = 2 braucht Verteilerrohr außen (Geometrie, G5-Kollision). Ersatzbeiwerte ζ/Impuls sind Annahmen. Δp-Gewinn gegenüber ×3-Mäander (0,70 bar): 76 %. Vorbehalt: 1D-Netz, keine CFD des Verteilers.
