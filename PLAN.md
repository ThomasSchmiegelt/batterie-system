# Plan Batteriesystem

KI-generiert (Claude Opus, 2026-11-11). Reihenfolge nach dem Fahrplan der Vorprojekte: Frage → Literatur → Modell → Validierung → Unsicherheit → Variante → Bericht.

## 0 · Vorgaben, die der Autor festlegt (offen)

| Vorgabe | Vorschlag (nur Vorschlag, nicht festgelegt) | Warum wichtig |
|---|---|---|
| Fahrzeug / Anwendung | Pkw-Mittelklasse | bestimmt Bauraum, Masse, Crashlasten |
| Energieinhalt | offen | bestimmt Zellzahl und Masse |
| Systemspannung | 400 V oder 800 V | Reihenschaltung, Schnellladen, Isolation |
| Zellchemie | LFP wie Blade, Vergleich NMC und Natrium-Ionen | Energiedichte gegen Sicherheit und Kosten |
| Zellform | lange prismatische Zelle (Blade-Prinzip), Vergleich Rundzelle | Zusammenbau, Kühlfläche |
| Kühlung | Flüssigkühlplatte unten, Wasser-Glykol | Schnellladen als Auslegungsfall |
| Auslegungsfall Kühlung | Schnellladen 10→80 % bei heißem Tag (Wert festlegen) | Vorbild Wasserstoff: der Kühler wird am heißesten Lastfall ausgelegt |

## PM · Projektmanagement (laufend, BAT-DOC-12)
- Jede Entscheidung als Akte `pm/entscheidungen/ENT-NNN.md` (Bauteil, Merkmal, Wert). Das CAD liest nur `pm/bauteile/parameter.json`.
- Ziel 1: Bauteilgespräch (`pm/gespraech.sh`). Ziel 2: Abschlussvideo (`video/STORYBOARD.md`).

## 1 · Wissensaufbau und Patente (PI, `forschung/`)
- W01–W07: LFP, Li-Ion allgemein, Blade, thermisches Durchgehen, BMS, Fahrzeugbatterie, Natrium-Ionen.
- W08–W15 (Nutzerwunsch 2026-11-12): Zelltypen/Formate, Zellchemie-Grundlagen, NMC/LTO, Festkörper, Spannungslage/Schnellladen, Kabel/Stromschienen/Schütze/Sicherungen, Steuerung (SOC, SOH, Ausgleich, CAN), Struktur.
- T01–T07 (Werkzeuge, eigener Auftrag AUFTRAG_WERKZEUGE.md): Open-Source-Zellchemie (PyBaMM, PyBOP, BPX, liionpack, BattMo, cideMOD), Ersatzschaltbild (impedance.py), Elektroauslegung (ngspice, KiCad, Modelica), offene BMS-/Ladesoftware (foxBMS, EVerest), Ersatzmodelle (T07).
- P01–P10: Blade-Zelle, Cell-to-Pack, Kühlplatte, Brandschutz zwischen Zellen, Entgasung, Zellverbinder, Messung/BMS, LFP-Kathode, Natrium-Ionen, Cell-to-Body.
- Start: `bash forschung/alles.sh` (Reihenfolge Wissen, Werkzeuge, Patente; etwa 3 h, GPU). Gestartet 2026-11-12 12:05. Danach prüfen Mensch und Claude; das Ergebnis geht in `BEFUNDE.md`.

## 2 · Chemie und Zelle (`sim/chemie/`, PyBaMM)
- Parametersatz LFP `Prada2013` (A123-Zelle 2,3 Ah, Rundzelle) als Ausgangspunkt. Probelauf ok (SOFTWARE.md).
- Auf ein langes Zellformat übertragen: Elektrodenfläche skalieren, Wärmemodell (lumped, dann Strom- und Wärmeverteilung entlang der Zelle).
- Ergebnisse: Entladekurve bei 0,5C/1C/2C, Wärmeleistung, Innenwiderstand über SOC und Temperatur, Alterung.
- Validierung: gegen veröffentlichte Messkurven des Parametersatzes (Quelle im PyBaMM-Zitat).

## 3 · Zellgeometrie und Zusammenbau (`cad/`, FreeCAD)
- Parametrische Zelle: Länge, Breite, Dicke, Pole, Ventil. Die Abmessungen kommen aus der Recherche (W03, P01), sonst Annahme.
- Pack: Reihen, Träger als Querträger (Cell-to-Pack), Kühlplatte, Wärmeleitpaste, Deckel, Explosionsdarstellung.
- Bauregeln festlegen (Abstände, Isolation, Montagefolge) und mit einem Prüfskript wie `spulen_montage.py` in der Fusion prüfen.

## 4 · Elektrik (`sim/elektrik/`)
- Verschaltung sS/pP aus Spannung und Energie. Zellverbinder (Querschnitt, Verluste), Hauptsicherung, Schütze, Vorladewiderstand, Spannungs- und Temperaturmessung.
- Zielbänder: Spannungsfenster des Umrichters, Verlust im Verbinder (Wert als Annahme festlegen).

## 5 · Kühlung (`sim/kuehlung/`)
- Wärmequelle aus Schritt 2, Kühlplatte als Kanal. Verteilung auf die Kanäle zuerst 1D, dann FluidX3D. Lehre aus Wasserstoff: Der Verteiler entscheidet die Gleichverteilung.
- Zellentemperatur in Elmer (Wärmeleitung Zelle → Paste → Platte). Ziel: maximale Zelltemperatur und Spreizung zwischen den Zellen (Grenzen mit Beleg aus der Recherche, sonst Annahme).

## 6 · Mechanik (`sim/mechanik/`, optional)
- Verspannung der Zellen (Quellen beim Laden), Stoß, Schwingung. Lehre aus Wasserstoff: Lagerung als Fest- und Loslager, Eigenfrequenzen prüfen.

## 7 · Bericht, Abschlussvideo, Unternehmenspräsentation, Bauteilgespräch (`bericht/`, `video/`, `praesentation/`, `pm/`)
- Jedes Kapitel DE und EN, mit Herleitung, Prozessdoku und Lessons Learned.
- Unternehmenspräsentation (REQ-D14, BAT-DOC-14 `praesentation/STORYBOARD.md`): 15 Folien für Entscheider. Vorgaben B0 (Zielgruppe, Firmenvorlage) vom Autor. Jeder Vorgang mit Folie legt unterwegs `praesentation/bausteine/<Vorgang>.md` ab; B5 setzt am Schluss zusammen.

## Netzplan
Projektplan mit kritischem Pfad: `pm/plan/plan_batterie.py` → `plan_batterie.json` (Planer des AI_Framework), `.csv`, `kritischer_pfad.txt`. Dauern sind Annahmen. Ersatzmodelle: `docs/ersatzmodell_einsatz.md` (Vorgänge U1–U4).


## Reihenfolge Autor 2026-11-17 abends
1. Bericht 0.2 nachziehen (läuft). 2. Vorgeschlagene Werte durchgehen (pm/offene_akten.md). 3. Rechnungen: Kühlplatte BT-610, Crash X, Zellmodell C1–C3. 4. **Elektronik** (Autor: „die elektronik muss auch noch berachtet werden“): BMS BT-300…360, Schaltbox BT-710…713, Heizung BT-760, Sensorik BT-770 – Recherche W27 (PI) läuft, danach Erwartung + Auslegung E2.

- 2026-11-17 Autor: „der richtige parametersaz ist wichtig. erst den“ → C2 vor Crash/Elektronik: Quellen (Sonnet) → W28 (PI) → Parametersätze aus W20-Zerlegung + Literatur, Kalibrierung an W20-DCIR und Blade-Pulsdaten (Test#5).

- 2026-11-17 Autor: „einverstanden. mach erst elektronik auch mit darstellung und kabel. dann crash. dann bericht.“ → E2 (BMS, Schaltbox, Kabel, CAD+Render+Schaltbild) → X Crash → Bericht 0.3.
- 2026-11-17 Autor wählt Schaltbox Fall b (auf Deckel vorne); Fortsetzung 2026-11-18, siehe ERINNERUNGEN.
