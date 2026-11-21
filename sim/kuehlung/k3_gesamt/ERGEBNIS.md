# ERGEBNIS K3/K4 – Thermik Gesamtsystem (Einrichtung und Probelauf)
| Dok. | ERG-K3 | Version 0.1 | Entwurf | Ersteller Claude Sonnet (KI-generiert) | Prüfer Opus (offen) |
> **KI-generiert (Claude Sonnet, 2026-11-21), Entwurf, nicht freigegeben.** Zahlen stammen aus `ergebnis.json` (K3) und `elmer/ergebnis.json` (K4); sie werden von `lauf.sh auswerten|k4` neu geschrieben.

**Stand:** Kette läuft (FluidX3D bahn + umlenk, Elmer LFP). Die Probeergebnisse **verfehlen die Erwartung** (siehe unten), nicht freigegeben. NMC-K4 und Dauerfahrt-K4 sind nicht eingerichtet (offen).

| Erwartung (ERWARTUNG.md) | Band | Ist | Fundstelle |
|---|---|---|---|
| 1 Δp je Platte gegen K2b | ±30 % | siehe ergebnis.json `dp_abw_prozent` | ergebnis.json |
| 2 h gegen K2b h_Kanal | ±30 % | `h_abw_prozent` | ergebnis.json |
| 2 Totzonen Anteil | < 5 % | `totzone_anteil_gesamtflaeche` (Kammer: `totzone_anteil_kammer`) | ergebnis.json |
| 3 Aufwärmung Energiebilanz | ±5 % | `bilanz_fx_abw_prozent` (NaN, Temperatur im Einlassfall instabil) und `dT_kuehlmittel_K` | ergebnis.json |
| 4 K4 LFP T_max | 33–37 °C | `T_max_Zellblock_C` | elmer/ergebnis.json |
| 4 K4 ΔT im Pack | 4–7 K | `dT_Zellblock_K` | elmer/ergebnis.json |
| 5 Grenzen | T_max ≤ 45 °C, ΔT ≤ 5 K | (Annahme Opus) | – |

Bilder: `k3_umlenk_u.png`, `k3_umlenk_T.png`, `k3_vergleich.png`, `k4_temperatur_LFP.png`, Film `k3_film.mp4` (Höhenschnitte des Endfelds, kein Zeitverlauf). Lesehilfe: Farbe = Strömungsgeschwindigkeit bzw. Temperatur, rot/cyan = Zielband.

## Befunde (an Opus)
1. **FluidX3D bahn:** f_Darcy ≈ 0,115 gegen 0,081 (Theorie) bei 8x4 mm, Nu aus dem Quellenmodell ≈ 14,5 (numerisch erwartet 5,77); mit Breite 32 mm ebenfalls ≈ 14,6 (erwartet 8,26). Die h-Methode (Quelle im Fluid, Wand T = 0, nach `stellarator/tauscher_cfd.py`) stimmt hier nicht. Das Werkzeug wurde nicht angepasst (Pr_sim = 2,5, ohne Smagorinsky; Pr 24,75 gab NaN). `k3_pruefung_nu.py` rechnet den Vergleich.
2. **FluidX3D umlenk:** Ein-/Auslass als TYPE_E; Bahnmittel u = 0,0295 statt 0,05 (Gitter), ζ = 69 (K2b: 1,5), Temperatur NaN. Das Geschwindigkeitsbild ist qualitativ plausibel (Strahl entlang der Kammer), die Zahlen nicht. Δp-Vergleich (+228 %) ist deshalb nicht belastbar.
3. **Vergleichsbasis h:** K2b h_Kanal enthält Graetz-Anlauf je Bahn (Nu 6,3), ein ausgebildeter Strom hat Nu 4,1 (-35 % auch bei richtiger Rechnung).
4. **K4 LFP (h aus K2b, nicht aus FluidX3D):** T_max und ΔT außerhalb des Erwartungsbands, heißeste Stelle hinten (x klein, letzte Bahn) wie erwartet. Ursache zu klären: Fluidaufwärmung 10,16 K allein liegt über dem ΔT-Ziel.

## Neue Annahmen (Sonnet benennt, Opus prüft)
Pr_sim = 2,5; k_Schaum 0,05 W/mK (BT-220 ohne Wert); cp Al 900, cp Pad 1000 J/kgK; Ober- und Unterplatte durchströmt gleichsinnig; Außenflächen adiabat, Rahmen/Boden/Deckel nicht modelliert; Zellblock homogenisiert (Zelle + Schaum in Reihe in Stapelrichtung); Q je Zelle konstant (K1 P0); Umlenkgebiet 80 mm Bahnstück je Seite.

## Offen
NMC 30 min und Dauerfahrt 1C (K4), Wiederaufsetzpunkt (Läufe < 30 min, stattdessen STOP-Prüfung vor Start/je FluidX3D-Abschnitt), Ursache der Nu/ζ-Abweichung, Eintrittstemperatur-Wahl (T_ein 25 °C aus K1).
*KI-generiert (Claude Sonnet), Entwurf, nicht freigegeben.*

## Nachtrag 1 (Sonnet, 2026-11-21): neue Methode eingerichtet, Probe Re 100
> KI-generiert, Entwurf. Die Zahlen der ersten Fassung (2 Zellen/mm, τ 0,502) sind überholt; ergebnis.json wird von `lauf.sh auswerten` neu erzeugt.
- **K3:** 4 Zellen/mm, Pr_sim 1, u0 = 0,05·Re/100, τ wird ausgegeben, Abbruch bei τ < 0,52 (Re 100: τ 0,532, Re 200: u0 0,1, τ 0,532). Probe Bahn Re 100 (lauf_bahn_re100_probe/ergebnis.json): f·Re = 62,4, Nu(Quellenmodell) = 5,73 gegen numerisch 5,77 (pruefung_nu.json). Methode trägt. Umrechnung Quellenmodell → Wandwärme über das numerische Verhältnis 4,126/5,768 (Annahme Sonnet), Graetz-Faktor aus K2b.
- **Offen K3-Umlenkung:** Das Einlass-/Auslass-Gebiet (TYPE_E) liefert nur etwa die Hälfte des Sollflusses in der Bahn (Fluss Bahn 1 / Einlassebene ≈ 0,52, Bahn 2 / Bahn 1 ≈ 1,1, nicht stationär), Temperatur-Bilanz nicht erreichbar, ζ ≈ 100 nicht belastbar. Ausgewertet wird mit dem tatsächlichen Re (Re_eff). Vorschlag an Opus: Umlenkung als zusammengesetztes Gebiet mit Volumenkraft je Bahn oder Druckrand statt Geschwindigkeitsrand.
- **K4:** `k4_elmer.py netz|rechnen|auswerten --fall LFP_P0|NMC_P4|LFP_DAUER|NMC_DAUER --var V0..V3` (V1 obere Platte gegensinnig, V2 Durchfluss ×2 mit h und Kühlmittel-ΔT neu aus K2b-Formeln, V3 = V1+V2; Dauerfahrt stationär, Q = (1C·Ah)²·R0). Probe aller Pfade (3 Schritte) läuft. Neue Annahmen: NMC-Block homogenisiert über die ganze Plattenfläche, Höhe 80 mm, Zwischenraum k 0,05 W/mK; Durchfluss/Eintritt bei Dauerfahrt wie Schnellladen.
- Schritte in rechnen/schritte.txt: K3_bahn/umlenk 100/200 (GPU ja), K3_AUSW, K4_LFP_V0–V3, K4_NMC_V0/V3, K4_LFP_DAUER, K4_NMC_DAUER, PI_K3.
