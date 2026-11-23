---
typ: befund
tags: ["befund"]
---
# B-BAT-049

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

Werkzeug-Testfälle QN1: Löser verifiziert, LFP-Zellmodell liefert nur die halbe Kapazität (2026-11-23, gefunden von Sonnet/Tor QN1, Deutung Opus)

Quelle: [[Dokument/BEFUNDE]]

## Vorgänge
- –

## Text aus BEFUNDE.md

- Bestanden mit bekannter Lösung: Elmer −0,23 % (Ordnung 2,00), FluidX3D −0,07 % bei 32 Zellen (Ordnung etwa 2), OpenRadioss −0,48 %, Verteiler-1D 0,06 %, PyBaMM NMC +0,26 %, SPM/DFN < 10 mV.
- **Verfehlt: PyBaMM LFP.** Die entnommene Ladung beträgt 48,6 Ah statt 92,4 Ah (−47 %). Das deckt sich mit C1. Deutung Opus: Der LFP-Parametersatz bildet die Projektzelle nicht ab, vermutlich wegen Stöchiometriefenster bzw. Elektrodenfläche. Das ist kein Fehler des Löseres. Folge: Alle LFP-Ergebnisse aus PyBaMM (Ladezeit, Wärmequelle) haben Glaubwürdigkeit W = 0. REQ-P05 LFP bleibt zu Recht blockiert. Die Wärmequellen der LFP-Thermik (K1/K4) müssen in Schleife 2 auf ihre Herkunft geprüft werden.
- **QN8 (Δp K3 +232 %):** FluidX3D unterschätzt die Rohrströmung bei grober Auflösung, bei 4–5 Zellen um −4 bis −6 %. Es überschätzt sie nicht. Deutung Opus: Die +232 % kommen nicht vom Löser, sondern aus dem Vergleich. Vermutlich fehlen in der 1D-Korrelation (K2) die Umlenk- sowie Ein- und Auslaufverluste der Mäander, oder K3 wertet den Druck an anderer Stelle aus. Prüfung in Schleife 2: K3-Geometrie ohne Umlenkungen gegen K2.
- V1 mit ungerader Elementzahl ausgewertet: gültig. Bei gerader Zahl liegt ein Knoten im Maximum und das Ergebnis wäre trivial exakt.
