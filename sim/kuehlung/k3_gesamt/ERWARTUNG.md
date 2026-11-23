# ERWARTUNG K3/K4 – Thermik Gesamtsystem (Opus, 2026-11-20, vor der Rechnung)
| Dok. | ERW-K3 | Version 0.1 | Entwurf | Ersteller Claude Opus | Prüfer Mensch (offen) |
Autor 2026-11-20: „Thermische Betrachtung des gesamtsystems mit Fluidx3d“. REQ-P05 (Schnellladen), REQ-P07 (Temperatur), Akten ENT-152…157.
**Methode (Opus):** FluidX3D rechnet nur Fluid und Fluidtemperatur, keine Wärmeleitung im Festkörper. Deshalb zwei Stufen:
- **K3 FluidX3D (GPU):** Strömung in EINER Blech-Kühlplatte, Mäander 8 Bahnen längs, Teilkanal 8 × 4 mm, Steg 3, Umlenkkammer 30 mm (Geometrie aus cad/baukasten/ausgabe/step oder kuehlung._maeander). Durchfluss und Eintrittstemperatur wie K2b (sim/kuehlung/k2_kuehlplatte/ergebnis_k2b.json), Wandwärmestrom gleichmäßig = Zellwärme LFP K1c / Plattenfläche / 2 Platten. Auflösung ≥ 8 Zellen über 4 mm. Passt das nicht in den GPU-Speicher, einen Streifen aus 2 Bahnen + 1 Umlenkung über die ganze Länge rechnen und auf 8 Bahnen hochrechnen (vermerken).
  Ergebnis: Druckverlust, mittleres h je Bahn, Totzonen in den Umlenkungen (Geschwindigkeit < 10 % des Mittels), Austrittstemperatur. Bilder: Geschwindigkeit in Kanalmitte, Temperatur des Fluids.
- **K4 Elmer (CPU):** 3D-Wärmeleitung des ganzen Packs (Zellen als Block mit anisotroper Leitfähigkeit aus K1, Zwischenlage Schaum, Pad, Blech, Rahmen, Boden, Deckel). Randbedingung an den Kanalflächen: h je Bahn und Fluidtemperatur je Ort aus K3 (Aufwärmung entlang des Mäanders). Lastfall LFP Schnellladen 10→80 % in 20 min, Q(t) aus K1c; dazu NMC 30 min. Stationär zusätzlich Dauerfahrt (Q aus K1, 1C).
**Erwartung (Zahlen vor der Rechnung):**
1. Δp je Platte innerhalb ± 30 % von K2b (laminar + Graetz). Weicht es stärker ab, ist eine der beiden Rechnungen falsch, dann zurück an Opus.
2. h_eff innerhalb ± 30 % von K2b. Totzonen nur in den Außenecken der Umlenkkammern, Anteil < 5 % der Kanalfläche.
3. Kühlmittelaufwärmung Ein→Aus = Q_ges / (ṁ · cp), ± 5 % (Energiebilanz, Pflicht).
4. K4 LFP Schnellladen: T_max 33–37 °C (K1c ideal 32,7 °C plus Aufwärmung entlang des Mäanders und Pad), ΔT im Pack 4–7 K, die heißeste Zelle am Austritt (hinten rechts). NMC: T_max 35–40 °C.
5. Grenzwerte: T_max ≤ 45 °C und ΔT ≤ 5 K (Annahme Opus, bisher K1). ΔT > 5 K wäre ein Verbesserungsvorschlag (z. B. Gegenstrom oben/unten).
**Verfehlt**, wenn ein Wert außerhalb seines Bandes liegt oder die Energiebilanz > 5 % abweicht.
**Pausieren (Autor):** Beide Rechnungen laufen als Schritte in rechnen/schritte.txt und müssen $RECHNEN_STOP prüfen: FluidX3D in Abschnitten mit gespeicherten Feldern, Elmer mit Restart-Datei je Abschnitt.

## Nachtrag 1 (Opus, 2026-11-21, nach dem Probelauf)
**K4 (Elmer), Deutung:** T_max 42,6 °C und ΔT 16,4 K verfehlen das Band. Den Fehler hat Opus in der Erwartung gemacht: Das Band 33–37 °C nahm K1c (Kühlmittel konstant) und vergaß die Aufwärmung des Kühlmittels von 10,2 K, die K2b selbst schon ausweist (dT_K). Die Wärme stimmt: 66 kJ je Zelle in 1200 s ≈ 55 W/Zelle, ≈ I²R mit 194 A und 1,28 mΩ. Korrigierte Erwartung: T_max ≈ 32,7 + 10 ≈ 43 °C, ΔT ≈ 4 + 10 ≈ 14–17 K. Das Ergebnis ist also plausibel. **Es verfehlt aber die Grenze ΔT ≤ 5 K**, daraus wird ein Verbesserungsvorschlag. Zusätzlich zu rechnen: (V1) obere und untere Platte gegensinnig durchströmt, (V2) Durchfluss ×2, (V3) V1 + V2, dazu NMC 30 min und Dauerfahrt 1C. Erwartung V1: ΔT ≈ 8–10 K, V2: Kühlmittel-ΔT 5 K, ΔT Pack ≈ 9–11 K, V3: ΔT ≈ 5–7 K.
**K3 (FluidX3D), Deutung:** Mit 2 Zellen/mm, u_lb 0,05 und Re 760 liegt τ ≈ 0,502. Das ist an der Stabilitätsgrenze von LBM und erklärt Δp/h-Fehler und NaN. Neue Methode: Im laminaren Bereich sind f·Re und Nu der ausgebildeten Strömung unabhängig von Re. Gerechnet wird deshalb bei Re 100 und Re 200 (Nachweis der Re-Unabhängigkeit), 4 Zellen/mm, τ ≥ 0,53 (prüfen und ausgeben), Pr_sim 1 (Nu ausgebildet hängt nicht von Pr ab). Daraus h bei Re 760 = Nu_FX · k / D_h × Graetz-Faktor wie K2b. Umlenkung: ζ bei Re 100/200, Trend nennen.
Erwartung neu: f·Re (Darcy) 62 ± 10 % (Rechteck 2:1), Nu ± 15 % vom K2b-Ansatz, Energiebilanz < 5 %. Bei Abweichung zurück an Opus.
**Nachtrag 2 (Opus, 2026-11-21):** Probe Bahn Re 100: f·Re 62,4 (Soll 62 ± 10 %), Nu 5,73 (K2b-Ansatz 5,77). Das bestätigt die Methode. In der Umlenkung liefern die Einlassränder nur 52 % des Flusses, nicht stationär. Sie gilt deshalb nur qualitativ (Totzonenbild). ζ bleibt für K4 bei 1,5 aus K2b, im Bericht als nicht durch FluidX3D bestätigt vermerkt.
**Nachtrag 3 – Fall `film` (Opus, 2026-11-21, vor der Rechnung):** Autor: „ich würde die durchströmung gerne als video haben“. Methode wie die bestätigte Bahnprobe (Re 200, 4 Zellen/mm, Pr_sim 1, τ ≥ 0,52).
- **Gebiet:** 2 Bahnen + 1 Umlenkkammer. Länge: Vorlauf ≥ 10 Kanalhöhen (≥ 40 mm) vor der Umlenkung, dazu so viel Bahnlänge, wie die GPU fasst, mindestens 150 mm je Bahn. Einlass als Geschwindigkeitsrand am Anfang des Vorlaufs, Auslass als Druckrand am Ende der Rückbahn.
- **Schrittzahl:** bis stationär (Änderung des Durchflusses < 1 % über 1 Durchlaufzeit), höchstens 3 Durchlaufzeiten. Bilder gleichmäßig verteilt, 600 Bilder.
- **Erwartung:**
  1. Durchfluss durch die Rückbahn = Einlass ± 5 % (Massenerhalt, Pflicht).
  2. Totzonen (u < 10 % des Mittels) nur in den Außenecken der Umlenkkammer, < 15 % der Kammerfläche, < 5 % des Gebiets.
  3. Ungleiche Verteilung auf die 8 Teilkanäle nach der Umlenkung: Innenkanal (kurzer Weg) mit bis zu +20 % Durchfluss, Außenkanal −20 %. Gleicht sich nach etwa 20 Kanalhöhen aus.
  4. Temperatur: Wandnahe Grenzschicht wächst entlang der Bahn. Die Mischung in der Umlenkung baut sie ab (heller Streifen hinter der Umlenkung). Aufwärmung bei Re 200 nur qualitativ, nicht auf den Betrieb übertragbar.
- **Verfehlt**, wenn Punkt 1 > 5 % abweicht oder der Lauf instabil wird (NaN). Dann zurück an Opus.

## Anforderung (Nachtrag)
- REQ-P09 (Vorgang K3, pm/plan/wissensnetz.py)

Vermerk: Nachtrag Sonnet aus wissensnetz.py, Prüfung Opus offen (2026-11-23). Die Zuordnung Rechenordner zu Vorgang K3/K4 ist von Sonnet gewählt.
