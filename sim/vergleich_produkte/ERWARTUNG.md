# ERWARTUNG QN2: Vergleich mit realen Batteriepacks

KI-generiert (Claude Opus, 2026-11-23). Gehört zu BAT-DOC-22, Kategorie V Stufe 1.

## Anforderung
REQ-P02, REQ-P07.

## Steckbrief
Unsere Werte: Energie brutto aus startwerte/Stückliste (LFP 73,92, NMC 74,27 kWh), Masse aus der Stückliste (LFP 626,8, NMC 486,4 kg), Hüllmaß aus CAD (LFP 2373 × 1430 × 245, NMC 2273 × 1430 × 228 mm).

## Vorrechnung
Gravimetrisch: LFP 73,92/626,8 ≈ 118 Wh/kg, NMC 74,27/486,4 ≈ 153 Wh/kg. Volumetrisch: LFP 73,92 kWh / 0,831 m³ ≈ 89 Wh/l, NMC 74,27 / 0,741 m³ ≈ 100 Wh/l (Hüllquader).

## Erwartung
Die Vergleichswerte stammen nur aus Recherche W43 mit bestandener Zitatprüfung. Die folgende Erwartung ist eine Einschätzung von Opus aus dem Gedächtnis:
- LFP-Blade-Packs (Cell-to-Pack) liegen bei etwa 140–160 Wh/kg. Unser LFP-Pack liegt 15–25 % darunter, weil Rahmen und Kühlung konservativ sind. Die Pfahlrechnung hat einen steifen Rahmen gezeigt (B-BAT-042).
- NMC-Packs mit Rundzellen liegen bei etwa 150–180 Wh/kg. Unser NMC-Pack liegt im unteren Bereich.
- Volumetrisch liegen wir unter den Produkten, weil der Hüllquader Hohlräume mitzählt.
Liegt ein Wert außerhalb ±40 % der Produktspanne, ist das ein Warnsignal für einen Modellfehler (Masse oder Energie). Dann geht es zurück an Opus.

## Plausibilitätskriterien
Gleiche Bezugsgrößen: Pack brutto, nicht Zelle. Werte auf Zellebene werden getrennt ausgewiesen und nicht mit Packwerten vermischt.

## Abbruchkriterien (Wächter)
Keine Rechnung, nur Auswertung.

## Informationsgewinn der Varianten
Keine Varianten.

## Zielband Bild
Streudiagramm Wh/kg über Wh/l. Die Produkte sind Punkte mit Quelle Wxx, unsere zwei Packs hervorgehoben, das Band der Produktspanne je Chemie schattiert.

## Prüfung
Sonnet, 2026-11-23 (Opus-Prüfung offen):
- Erwartung Wh/kg und Wh/l: **nicht prüfbar**, W43 hat keine geprüfte Packmasse und keine Packmaße (siehe ERGEBNIS.md).
- Erwartung Energie: unsere 73,92 und 74,27 kWh liegen in der Produktspanne 57,3–118 kWh (`ergebnis.json`), Warnband ±40 % nicht verletzt.
- Zitatprüfung W43: 15 bestätigt, 2 Fehler (Z17 Seal Leergewicht, Z23 Model 3), beide ausgeschlossen; Z40 ist Fragetext.
- Bild `w43_vergleich.png` angesehen: Zielband (Spanne, Warnband) beschriftet, Linien plausibel, Fußzeile jetzt umbrochen.
