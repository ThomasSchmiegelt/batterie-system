# Konzept: Pre-/Postprocessing, Kühlart, Kabelverlegung, Seitencrash

> **KI-generiert** (Claude Opus, 2026-11-12). Status: Entwurf, Vorschlag. Anlass: Nutzer 2026-11-12: „für die Kühlung muss wahrscheinlich auch das Sketch-to-Prompt genutzt werden … wie sieht es mit Kabelverlegung aus? auch sollen Kühlmöglichkeiten betrachtet werden, Luft und Wasser. Geht ein Seitencrash?“
> Zahlen ohne Beleg sind **Annahmen**; Belege kommen aus Recherche W16, W17, T08, T09.

## 1 Sketch-to-Prompt als Pre- und Postprocessing (Vorgänge W1, W2)

**Bestand** (`~/sketch-to-prompt`): STL im Browser drehen, Linien auf das Bauteil zeichnen, Text dazu. Ausgabe `sketch.json` mit den 3D-Punkten jeder Linie, der Kamera und den sichtbaren Teilen. Ein eigenes Werkzeug zum Festlegen von Querschnitten wurde in den Projekten nicht gefunden. Vorhanden sind nur fest programmierte Schnittbilder (z. B. `fusion/stellarator/kuehlung_schnittbild.py`).

**Vorschlag ohne Änderung am Werkzeug:**
- **Preprocessing:** Der Nutzer zeichnet Ein- und Auslass, Lagerung, Lastangriff oder Kabelweg auf das Modell und schreibt dazu „Linie 1 = Einlass“. Claude ordnet jeder Linie die getroffenen Flächen zu und setzt daraus die Randbedingungen für Elmer, FluidX3D oder CalculiX.
- **Postprocessing:** Eine Linie und die Blickrichtung aus `sketch.json` spannen eine Ebene auf. Das ist der gewünschte Schnitt. Ein Skript wertet das Feld (Geschwindigkeit, Temperatur, Spannung) in dieser Ebene aus. Die Antwort kommt als Bild aus derselben Blickrichtung (Regel „Skizzen als Input“).

**Mögliche Erweiterung** (eigenes, öffentliches Repo, nur mit Freigabe): Auswahl „Art der Linie“ (Einlass, Auslass, Lager, Last, Schnitt, Kabel) und Ergebnisfelder als Farben auf dem STL.

## 2 Kühlart: Luft gegen Wasser (Vorgang K0, Recherche W16)

| | Luft | Wasser-Glykol (Kühlplatte) |
|---|---|---|
| Wirkprinzip | Gebläse, Luft strömt zwischen Zellen oder Modulen | Kühlplatte unter den Zellen, Pumpe, Wärmetauscher |
| Wärmeübergang | gering (Annahme: Größenordnung 10–100 W/m²K) | hoch (Annahme: Größenordnung 1000 W/m²K und mehr) |
| Aufwand | einfach, leicht, kein Leck | Pumpe, Dichtungen, Leckgefahr |
| Eignung Schnellladen | voraussichtlich nicht für 2C und mehr | Stand der Technik bei Schnellladern (zu belegen, W16) |

Entscheidung mit einer 1D-Wärmebilanz: Wärme beim Schnellladen (aus dem Zellmodell C3) gegen abführbare Leistung je Kühlart bei 40 °C Umgebung (REQ-P08). Beide Kühlarten lassen sich mit FluidX3D rechnen, Luft wie Wasser.

## 3 Kabelverlegung (Vorgang L1, Recherche T09)

1. **Weg skizzieren:** Der Nutzer zeichnet den Kabelweg in Sketch-to-Prompt auf das Pack-Modell (3D-Punkte).
2. **Regeln prüfen** mit einem Skript nach dem Vorbild von `spulen_montage.py` (Fusion): Biegeradius ≥ k·d (k aus Datenblatt, sonst Annahme), Abstand Hochvolt zu Niedervolt, Abstand zu Kühlleitungen und scharfen Kanten, keine Überschneidung.
3. **Modell:** Rohr entlang der Punkte (FreeCAD-Sweep), Querschnitt aus Vorgang E1 (Strom, Erwärmung).
4. Werkzeugoption: FreeCAD „Cables Workbench“ (Erweiterung, Lizenz wird in T09 geprüft). Ohne Erweiterung genügt ein eigener Sweep.

## 4 Seitencrash (Vorgänge X1, X2, Recherche W17, T08)

**Ja, in zwei Stufen:**
- **X1 quasistatisch** mit CalculiX (vorhanden: `~/.local/bin/ccx`): Ein starrer Pfahl drückt seitlich auf Gehäuse und Querträger, mit plastischem Werkstoff und Kontakt. Ergebnis: Eindringung, verglichen mit dem Abstand zur ersten Zelle (Zielband: keine Zelle berührt; Grenze als Annahme, bis W17 die Prüfnorm nennt). Aussagekraft: Steifigkeit und Reserve, keine Crashdynamik.
- **X2 dynamisch** mit OpenRadioss (expliziter Crashlöser, offen; Lizenz in T08). **Nicht installiert.** Herunterladen und Installieren nur nach ausdrücklicher Freigabe des Autors.
- Grenzen: ohne Fahrzeugstruktur und ohne Werkstoffkennwerte für hohe Dehnraten nur ein Vergleich von Varianten, kein Nachweis.

## 5 Wo es im Plan steht

`pm/plan/plan_batterie.py`: W1, W2 (Werkzeug), K0 (Kühlart), L1 (Kabel), X1, X2 (Crash). Der kritische Pfad bleibt bei 35,5 Arbeitstagen (Annahme), denn die neuen Vorgänge liegen neben ihm.
