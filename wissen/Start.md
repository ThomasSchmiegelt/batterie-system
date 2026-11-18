---
typ: start
tags: ["start"]
---
# Wissensnetz Batterieprojekt

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

Projektdauer (kritischer Pfad): 35.5 AT (Annahmen). Vorgänge: 47; fertig: 9, ohne Nachweis: 9, offen: 29.

Weiter: [[PLAN]] · [[BEFUNDE]] · [[docs/03_anforderungsverfolgung]] · [[docs/13_stueckliste]] · [Netzplan-Ansicht](pm/plan/wissensnetz.html)

## Stückliste nach Art

| Art | Bedeutung | Positionen |
|---|---|---|
| K | Kaufteil | 25 |
| E | Eigenteil | 13 |
| S | Schnittstelle zum Fahrzeug | 1 |
| | gesamt | 39 |

## Kritischer Pfad
[[wissen/Vorgang/S0|S0]] → [[wissen/Vorgang/R1|R1]] → [[wissen/Vorgang/R2|R2]] → [[wissen/Vorgang/R3|R3]] → [[wissen/Vorgang/R4|R4]] → [[wissen/Vorgang/V1|V1]] → [[wissen/Vorgang/V2|V2]] → [[wissen/Vorgang/C1|C1]] → [[wissen/Vorgang/C2|C2]] → [[wissen/Vorgang/C3|C3]] → [[wissen/Vorgang/G3|G3]] → [[wissen/Vorgang/G4|G4]] → [[wissen/Vorgang/K1|K1]] → [[wissen/Vorgang/K2|K2]] → [[wissen/Vorgang/K3|K3]] → [[wissen/Vorgang/K5|K5]] → [[wissen/Vorgang/U1|U1]] → [[wissen/Vorgang/U2|U2]] → [[wissen/Vorgang/U3|U3]] → [[wissen/Vorgang/U4|U4]] → [[wissen/Vorgang/B1|B1]] → [[wissen/Vorgang/B3|B3]] → [[wissen/Vorgang/B4|B4]]

## Offene Vorgänge

| Vorgang | Name | Status | Dauer AT | Puffer |
|---|---|---|---|---|
| [[wissen/Vorgang/W1\|W1]] | Preprocessing mit Sketch-to-Prompt: Ein-/Auslass, Lager, Lasten, Kabelwege auf das STL zeichnen | offen | 2 | 5.5 |
| [[wissen/Vorgang/W2\|W2]] | Postprocessing: Schnittebenen aus Skizzenlinie + Blickrichtung, Feldwerte (Strömung, Spannung) je Schnitt | offen | 2 | 5.5 |
| [[wissen/Vorgang/C1\|C1]] | ERWARTUNG Zellmodell (Entladekurve, Wärme, Innenwiderstand) | offen | 0.5 | 0.0 |
| [[wissen/Vorgang/C2\|C2]] | Zellmodell LFP (PyBaMM Prada2013) auf langes Format skalieren | offen | 2 | 0.0 |
| [[wissen/Vorgang/C3\|C3]] | Ratentest 0,5C/1C/2C, Wärmeleistung, R_i über SOC und T | offen | 1 | 0.0 |
| [[wissen/Vorgang/C4\|C4]] | Validierung gegen veröffentlichte Messkurven, Abgleich Erwartung | offen | 1 | 12.0 |
| [[wissen/Vorgang/C5\|C5]] | Alterung (Zyklen, Kalender) und Vergleich NMC / Natrium-Ionen | offen | 2 | 13.0 |
| [[wissen/Vorgang/G2\|G2]] | Parametrische Zelle FreeCAD (liest parameter.json) | offen | 2 | 2.0 |
| [[wissen/Vorgang/G4\|G4]] | Pack: Zellanordnung, Querträger, Kühlplatte, Deckel | offen | 3 | 0.0 |
| [[wissen/Vorgang/G5\|G5]] | Bauregeln + Prüfskript (Abstände, Isolation, Montagefolge) | offen | 1 | 3.0 |
| [[wissen/Vorgang/K0\|K0]] | Kühlart Luft gegen Wasser (1D-Wärmebilanz Schnellladen, W16), Entscheidung ENT | offen | 1 | 2.0 |
| [[wissen/Vorgang/E1\|E1]] | Zellverbinder/Kabel: Querschnitt, Verluste, Erwärmung (Zielband als Annahme) | offen | 2 | 9.0 |
| [[wissen/Vorgang/E2\|E2]] | Schutzkonzept: Sicherung, Schütze, Vorladung, Isolationswächter | offen | 2 | 9.0 |
| [[wissen/Vorgang/L1\|L1]] | Kabelverlegung: Weg skizzieren (Sketch-to-Prompt), Prüfskript Biegeradius/Abstand HV-NV/Kühlleitung, FreeCAD-Sweep | offen | 3 | 8.0 |
| [[wissen/Vorgang/E3\|E3]] | Steuerung/BMS: Messkonzept, Ladezustand, Ausgleich (Konzept, offene Software aus T06) | offen | 2 | 10.0 |
| [[wissen/Vorgang/E4\|E4]] | Schaltungsmodell ngspice/Modelica: Vorladung, Kurzschluss | offen | 2 | 11.0 |
| [[wissen/Vorgang/K1\|K1]] | ERWARTUNG Kühlung Schnellladen (max. Zelltemperatur, Spreizung) | offen | 0.5 | 0.0 |
| [[wissen/Vorgang/K2\|K2]] | Kanalverteilung 1D (Verteiler, Druckverlust) | offen | 1 | 0.0 |
| [[wissen/Vorgang/K3\|K3]] | Elmer: Zelle -> Paste -> Platte, Schnellladefall | offen | 3 | 0.0 |
| [[wissen/Vorgang/K4\|K4]] | FluidX3D: Strömung Kühlplatte bzw. Luftkanal (Gegenprüfung 1D) | offen | 2 | 1.0 |
| [[wissen/Vorgang/K5\|K5]] | Deutung Kühlung, Abgleich Erwartung, Änderungsvorschlag | offen | 1 | 0.0 |
| [[wissen/Vorgang/U1\|U1]] | ERWARTUNG Ersatzmodell: Zielgröße, Gültigkeitsbereich, Mindestgüte (z. B. Rangkorrelation) | offen | 0.5 | 0.0 |
| [[wissen/Vorgang/U2\|U2]] | Versuchsplan (Latin Hypercube): Durchfluss, Eintritt, C-Rate, Plattenmaß -> Elmer-Läufe | offen | 3 | 0.0 |
| [[wissen/Vorgang/U3\|U3]] | Ersatzmodell anpassen (Gauß-Prozess), Kreuzvalidierung gegen zurückgehaltene Läufe | offen | 1 | 0.0 |
| [[wissen/Vorgang/U4\|U4]] | Optimierung Kühlplatte/Ladeprofil mit Ersatzmodell, Bestwerte mit Elmer bestätigen | offen | 2 | 0.0 |
| [[wissen/Vorgang/X1\|X1]] | Seitencrash Pfahl, quasistatisch: Eindringung in Gehäuse/Querträger (CalculiX, plastisch, Kontakt) | offen | 3 | 3.0 |
| [[wissen/Vorgang/X2\|X2]] | Seitencrash dynamisch (OpenRadioss, Installation nur nach Freigabe) | offen | 4 | 3.0 |
| [[wissen/Vorgang/B3\|B3]] | Abschlussvideo (Storyboard -> Blender -> ffmpeg) | offen | 3 | 0.0 |
| [[wissen/Vorgang/B5\|B5]] | Unternehmenspräsentation aus Folienbausteinen erzeugen (pptx + PDF, DE/EN), Zahlen gegen Quellen prüfen | offen | 2 | 1.0 |

## Nicht installierte Software

| Software | Status | Vorgänge |
|---|---|---|
| [[wissen/Software/foxBMS\|foxBMS]] | nicht installiert / nicht geprüft | [[wissen/Vorgang/E3\|E3]] |
| [[wissen/Software/ngspice\|ngspice]] | nicht installiert / nicht geprüft | [[wissen/Vorgang/E4\|E4]] |
| [[wissen/Software/OpenModelica\|OpenModelica]] | nicht installiert / nicht geprüft | [[wissen/Vorgang/E4\|E4]] |
| [[wissen/Software/OpenRadioss\|OpenRadioss]] | nicht installiert / nicht geprüft | [[wissen/Vorgang/X2\|X2]] |

## Recherche-Stand

| Thema | Status | Prüfung |
|---|---|---|
| [[wissen/Recherche/P01\|P01]] | fertig | 2 Belege bestaetigt, 0 Fehler |
| [[wissen/Recherche/P02\|P02]] | fertig | 2 Belege bestaetigt, 0 Fehler |
| [[wissen/Recherche/P03\|P03]] | fertig | 6 Belege bestaetigt, 0 Fehler |
| [[wissen/Recherche/P04\|P04]] | fertig | 6 Belege bestaetigt, 0 Fehler |
| [[wissen/Recherche/P05\|P05]] | fertig | 6 Belege bestaetigt, 0 Fehler |
| [[wissen/Recherche/P06\|P06]] | fertig | 6 Belege bestaetigt, 0 Fehler |
| [[wissen/Recherche/P07\|P07]] | fertig | 6 Belege bestaetigt, 0 Fehler |
| [[wissen/Recherche/P08\|P08]] | fertig | 6 Belege bestaetigt, 0 Fehler |
| [[wissen/Recherche/P09\|P09]] | fertig | 6 Belege bestaetigt, 0 Fehler |
| [[wissen/Recherche/P10\|P10]] | fertig | 6 Belege bestaetigt, 0 Fehler |
| [[wissen/Recherche/T01\|T01]] | fertig | 5 Belege bestaetigt, 0 Fehler |
| [[wissen/Recherche/T02\|T02]] | fertig | 4 Belege bestaetigt, 0 Fehler |
| [[wissen/Recherche/T03\|T03]] | fertig | 2 Belege bestaetigt, 0 Fehler |
| [[wissen/Recherche/T04\|T04]] | fertig | 3 Belege bestaetigt, 1 Fehler |
| [[wissen/Recherche/T05\|T05]] | fertig | 6 Belege bestaetigt, 0 Fehler |
| [[wissen/Recherche/T06\|T06]] | fertig | 4 Belege bestaetigt, 0 Fehler |
| [[wissen/Recherche/T07\|T07]] | fertig | 2 Belege bestaetigt, 1 Fehler |
| [[wissen/Recherche/T08\|T08]] | fertig | 9 Belege bestaetigt, 0 Fehler |
| [[wissen/Recherche/T09\|T09]] | fertig | 1 Belege bestaetigt, 0 Fehler |
| [[wissen/Recherche/W01\|W01]] | fertig | 12 Belege bestaetigt, 2 Fehler |
| [[wissen/Recherche/W02\|W02]] | fertig | 8 Belege bestaetigt, 5 Fehler |
| [[wissen/Recherche/W03\|W03]] | fertig | 24 Belege bestaetigt, 0 Fehler |
| [[wissen/Recherche/W04\|W04]] | fertig | 5 Belege bestaetigt, 0 Fehler |
| [[wissen/Recherche/W05\|W05]] | fertig | 0 Belege bestaetigt, 0 Fehler |
| [[wissen/Recherche/W06\|W06]] | fertig | 11 Belege bestaetigt, 1 Fehler |
| [[wissen/Recherche/W07\|W07]] | fertig | 8 Belege bestaetigt, 2 Fehler |
| [[wissen/Recherche/W08\|W08]] | fertig | 12 Belege bestaetigt, 0 Fehler |
| [[wissen/Recherche/W09\|W09]] | fertig | 10 Belege bestaetigt, 3 Fehler |
| [[wissen/Recherche/W10\|W10]] | fertig | 19 Belege bestaetigt, 4 Fehler |
| [[wissen/Recherche/W11\|W11]] | fertig | 10 Belege bestaetigt, 2 Fehler |
| [[wissen/Recherche/W12\|W12]] | fertig | 12 Belege bestaetigt, 0 Fehler |
| [[wissen/Recherche/W13\|W13]] | fertig | 10 Belege bestaetigt, 1 Fehler |
| [[wissen/Recherche/W14\|W14]] | fertig | 8 Belege bestaetigt, 1 Fehler |
| [[wissen/Recherche/W15\|W15]] | fertig | 10 Belege bestaetigt, 0 Fehler |
| [[wissen/Recherche/W16\|W16]] | fertig | 10 Belege bestaetigt, 0 Fehler |
| [[wissen/Recherche/W17\|W17]] | fertig | 14 Belege bestaetigt, 0 Fehler |

---
*KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten*
