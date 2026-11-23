# ERWARTUNG K5: Kühlplatte mit Parallelführung und Z-Verteiler (ENT-158)

KI-generiert (Claude Opus, 2026-11-23), Entwurf. Anforderung: REQ zur Zelltemperaturspreizung ΔT ≤ 5 K beim Schnellladen (siehe K4). Vorschlag ENT-158 (Status vorgeschlagen). Kühlplatte ist freigegeben (ENT-152 bis 156), soll aber optimiert werden (Autor, 22.11.).

## Was gerechnet wird
1. **Verteilerrechnung (1D-Netz, Python):** Die Bahnen des G5-Mäanders werden zu N parallelen Kanälen mit gleichem Querschnitt und der Länge einer Bahn. Verteiler und Sammler liegen als Z-Anordnung gegenüber (Eintritt auf der einen Seite, Austritt auf der anderen). Für Kanäle gelten die Druckverlust-Beziehungen aus K2b (`sim/kuehlung/k2_kuehlplatte`, laminar mit Einlaufkorrektur). Für die Sammelkanäle gilt Reibung plus Impulsänderung an Abzweigen (Annahme: Verlustbeiwert ζ = 1 je Abzweig, Kanalquerschnitt Verteiler = Kanalhöhe × 25 mm; Variante 35 mm). Annahmen Opus.
   Ergebnis: Durchflussanteil je Kanal, Abweichung vom Mittel, Δp der Platte bei Durchfluss ×1 und ×3 gegenüber dem Mäander K2b.
2. **K4-Variante V4 (Elmer, ganzes Pack):** Kühlmitteltemperatur je Kanal linear von T_ein auf T_ein + ΔT_K über die Kanallänge, für alle Kanäle gleich. Durchfluss ×3, also ΔT_K = 10,2 K / 3 = 3,4 K. Ober- und Unterplatte gegenläufig wie in V1. Wärmeübergang h aus der K3-Korrelation für die neue Kanalgeschwindigkeit (Durchfluss ×3 auf N Kanäle verteilt). Laminar bleibt Nu ungefähr konstant, h ändert sich dann kaum; das ist zu prüfen und anzugeben. LFP-Schnellladen (wie V0–V3) und NMC 30 min.

## Erwartung vor der Rechnung
- Verteilung: Mit 25 mm breiten Sammelkanälen weicht jeder Kanal höchstens ±5–15 % vom Mittel ab, die größte Abweichung tritt am Ende des Verteilers auf. Mit 35 mm liegt die Abweichung unter ±10 %.
- Δp der Platte: Trotz Durchfluss ×3 unter 0,22 bar (K2b Mäander), erwartet 0,02–0,1 bar. Nur so lohnt sich die Variante.
- K4 LFP-Schnellladen: ΔT der Zellen 6–8 K (V0 16,4 K; V3 8,1 K), T_max 33–36 °C. Das Ziel von 5 K wird nicht erreicht, weil rund 6 K aus der Wärmeleitung in Zelle und Pad bleiben.
- K4 NMC 30 min: ΔT unter 2 K.
- Verfehlt die Rechnung das Band, wird zuerst die Erwartung überprüft (vergleiche B-BAT-038), nicht das Modell angepasst.

## Prüfung
Bilder mit Zielband: Verteilung je Kanal (±10 %), Δp gegenüber Durchfluss (Mäander und parallel, Linie 0,22 bar), K4-Temperaturfeld V4 neben V0 und V3, Tabelle V0–V4. Opus prüft an den Rohdaten (Elmer-Ausgabe, Kanalanteile).

## Nachtrag 1 (Opus, 2026-11-23): reine Parallelführung verworfen, gruppierte Parallelführung
Ergebnis von Sonnet (verteiler.py): Die Platte hat 120 Kanäle (8 Bahnen × 15 Kanäle, 8 × 4 mm, 1,97 m), nicht wenige breite Bahnen, wie Opus beim Schreiben der Erwartung vor Augen hatte. Ein Sammelkanal von 25 × 4 mm hat 100 mm² Querschnitt, die Kanäle zusammen 3 840 mm². Die Geschwindigkeit im Sammler liegt deshalb bei 1,9–5,8 m/s, sein Staudruck übersteigt den Druckverlust der Kanäle um ein Vielfaches. Die Verteilung weicht um bis zu +700 % bzw. +990 % ab, mittlere Kanäle bleiben fast leer. Erwartung klar verfehlt. Ursache ist die Annahme von Opus (Sammler in Kanalhöhe in der Platte), nicht die Rechnung. Die Aussage „Parallel-Z“ aus ENT-158 gilt in dieser Form nicht.
Neue Variante (Methodenwahl Opus): k parallele Gruppen, jede ein kurzer Mäander aus 8/k Bahnen; k = 2, 4, 8. Gespeist werden die Gruppen aus einem außen liegenden Verteilerrohr Ø 20 bzw. 25 mm (Annahme Opus; ζ = 1 je T-Abzweig, Austritt gleich). Abschätzung vorab (laminar, Δp ∝ Durchfluss × Länge): Gruppen-Δp ≈ 0,215 bar × (3/k) × (1/k) bei Durchfluss ×3, also k = 2: 0,16 bar, k = 4: 0,04 bar, k = 8: 0,01 bar. Staudruck im Rohr Ø 20 bei ×3 (34,5 L/min) etwa 0,018 bar, bei Ø 25 etwa 0,007 bar.
Erwartung: k = 2 verteilt auf ±5 % und bleibt mit 0,15–0,2 bar knapp unter 0,22 bar. k = 4 liegt bei 0,04–0,08 bar und verteilt mit Ø 25 auf ±10 %, mit Ø 20 schlechter. k = 8 verteilt schlecht (> ±20 %). Die Kühlmittelaufwärmung beträgt bei ×3 in jeder Gruppe 3,4 K, gleich für alle k. Das K4-Ergebnis (ΔT 6–8 K) hängt deshalb kaum von k ab; k entscheidet über Δp und Verteilung. Gerechnet wird K4 V4 mit dem besten k, das ±10 % und < 0,22 bar erfüllt.

## Nachtrag 2 (Opus, 2026-11-23): Variante V4p wie gebaut (ohne Gegenlauf)
Im CAD G5.9 sind Ober- und Unterplatte parallel geschaltet, über gemeinsame Steigblöcke und ohne Gegenlauf. K4 V4 hatte Gegenlauf angenommen. V4p rechnet den gebauten Stand nach. Erwartung: LFP ΔT 8,5–10 K, T_max 35–37 °C (der Gegenlauf bringt bei 3,4 K Kühlmittelaufwärmung etwa 1–2 K); NMC ΔT < 2 K. Ist der Unterschied größer als 2 K, wird der Gegenlauf im CAD zum Verbesserungsvorschlag.

## Anforderung (Nachtrag)
- REQ-P09 (Vorgang K5, pm/plan/wissensnetz.py)
- REQ-D06 (Vorgang K5, pm/plan/wissensnetz.py)

Vermerk: Nachtrag Sonnet aus wissensnetz.py, Prüfung Opus offen (2026-11-23). Die Zuordnung Rechenordner zu Vorgang K5 ist von Sonnet gewählt.
