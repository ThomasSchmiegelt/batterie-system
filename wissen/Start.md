---
typ: start
tags: ["start"]
---
# Wissensnetz Batterieprojekt

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

Projektdauer (kritischer Pfad): 35.5 AT (Annahmen). Vorgänge: 50; fertig: 16, ohne Nachweis: 9, offen: 25.

Weiter: [[Dokument/PLAN]] · [[Dokument/BEFUNDE]] · [[Dokument/03_anforderungsverfolgung]] · [[Dokument/13_stueckliste]] · Netzplan-Ansicht (`pm/plan/wissensnetz.html`, im Repo)

## Einstiege

- Bericht: [[Bericht/Abschlussbericht]] (Version 1.2)
- V-Modell-Matrix: [[Dokument/06_verifikationsplan]] (Bewertung je Anforderung in den Anforderungsnotizen, Tag `bewertung/...`)
- Workflow: [[Dokument/17_workflow_schleife]] · Freigaberunde: [[Dokument/19_freigaberunde]]
- Normen und Regelwerke: [[Dokument/07_normen_und_vorschriften]]
- Präsentation: [[Dokument/praesentation__STORYBOARD]] (34 Folienbausteine, Ordner wissen/Baustein)
- Steckbriefe: [[Steckbrief/BT-610_LFP|BT-610_LFP]]
- Dokumente: Ordner wissen/Dokument (33 Notizen)

## Verifikation der Anforderungen

| Bewertung | Anzahl |
|---|---|
| nachgewiesen | 18 |
| offen | 15 |
| blockiert | 1 |
| verfehlt | 3 |
| rechnerisch erfüllt (nicht validiert) | 1 |
| gesamt | 38 |

## Stückliste nach Art

| Art | Bedeutung | Positionen |
|---|---|---|
| K | Kaufteil | 25 |
| E | Eigenteil | 13 |
| S | Schnittstelle zum Fahrzeug | 1 |
| | gesamt | 39 |

## Kritischer Pfad
[[Vorgang/S0|S0]] → [[Vorgang/R1|R1]] → [[Vorgang/R2|R2]] → [[Vorgang/R3|R3]] → [[Vorgang/R4|R4]] → [[Vorgang/V1|V1]] → [[Vorgang/V2|V2]] → [[Vorgang/C1|C1]] → [[Vorgang/C2|C2]] → [[Vorgang/C3|C3]] → [[Vorgang/G3|G3]] → [[Vorgang/G4|G4]] → [[Vorgang/K1|K1]] → [[Vorgang/K2|K2]] → [[Vorgang/K3|K3]] → [[Vorgang/K5|K5]] → [[Vorgang/U1|U1]] → [[Vorgang/U2|U2]] → [[Vorgang/U3|U3]] → [[Vorgang/U4|U4]] → [[Vorgang/B1|B1]] → [[Vorgang/B3|B3]] → [[Vorgang/B4|B4]]

## Offene Vorgänge

| Vorgang | Name | Status | Dauer AT | Puffer |
|---|---|---|---|---|
| [[Vorgang/W1\|W1]] | Preprocessing mit Sketch-to-Prompt: Ein-/Auslass, Lager, Lasten, Kabelwege auf das STL zeichnen | offen | 2 | 5.5 |
| [[Vorgang/W2\|W2]] | Postprocessing: Schnittebenen aus Skizzenlinie + Blickrichtung, Feldwerte (Strömung, Spannung) je Schnitt | offen | 2 | 5.5 |
| [[Vorgang/C1\|C1]] | ERWARTUNG Zellmodell (Entladekurve, Wärme, Innenwiderstand) | offen | 0.5 | 0.0 |
| [[Vorgang/C2\|C2]] | Zellmodell LFP (PyBaMM Prada2013) auf langes Format skalieren | offen | 2 | 0.0 |
| [[Vorgang/C3\|C3]] | Ratentest 0,5C/1C/2C, Wärmeleistung, R_i über SOC und T | offen | 1 | 0.0 |
| [[Vorgang/C4\|C4]] | Validierung gegen veröffentlichte Messkurven, Abgleich Erwartung | offen | 1 | 12.0 |
| [[Vorgang/C5\|C5]] | Alterung (Zyklen, Kalender) und Vergleich NMC / Natrium-Ionen | offen | 2 | 13.0 |
| [[Vorgang/G2\|G2]] | Parametrische Zelle FreeCAD (liest parameter.json) | offen | 2 | 2.0 |
| [[Vorgang/G4\|G4]] | Pack: Zellanordnung, Querträger, Kühlplatte, Deckel | offen | 3 | 0.0 |
| [[Vorgang/G5\|G5]] | Bauregeln + Prüfskript (Abstände, Isolation, Montagefolge) | offen | 1 | 3.0 |
| [[Vorgang/K0\|K0]] | Kühlart Luft gegen Wasser (1D-Wärmebilanz Schnellladen, W16), Entscheidung ENT | offen | 1 | 2.0 |
| [[Vorgang/E1\|E1]] | Zellverbinder/Kabel: Querschnitt, Verluste, Erwärmung (Zielband als Annahme) | offen | 2 | 9.0 |
| [[Vorgang/E2\|E2]] | Schutzkonzept: Sicherung, Schütze, Vorladung, Isolationswächter | offen | 2 | 9.0 |
| [[Vorgang/L1\|L1]] | Kabelverlegung: Weg skizzieren (Sketch-to-Prompt), Prüfskript Biegeradius/Abstand HV-NV/Kühlleitung, FreeCAD-Sweep | offen | 3 | 8.0 |
| [[Vorgang/K1\|K1]] | ERWARTUNG Kühlung Schnellladen (max. Zelltemperatur, Spreizung) | offen | 0.5 | 0.0 |
| [[Vorgang/K2\|K2]] | Kanalverteilung 1D (Verteiler, Druckverlust) | offen | 1 | 0.0 |
| [[Vorgang/K3\|K3]] | Elmer: Zelle -> Paste -> Platte, Schnellladefall | offen | 3 | 0.0 |
| [[Vorgang/K4\|K4]] | FluidX3D: Strömung Kühlplatte bzw. Luftkanal (Gegenprüfung 1D) | offen | 2 | 1.0 |
| [[Vorgang/K5\|K5]] | Deutung Kühlung, Abgleich Erwartung, Änderungsvorschlag | offen | 1 | 0.0 |
| [[Vorgang/U1\|U1]] | ERWARTUNG Ersatzmodell: Zielgröße, Gültigkeitsbereich, Mindestgüte (z. B. Rangkorrelation) | offen | 0.5 | 0.0 |
| [[Vorgang/U2\|U2]] | Versuchsplan (Latin Hypercube): Durchfluss, Eintritt, C-Rate, Plattenmaß -> Elmer-Läufe | offen | 3 | 0.0 |
| [[Vorgang/U3\|U3]] | Ersatzmodell anpassen (Gauß-Prozess), Kreuzvalidierung gegen zurückgehaltene Läufe | offen | 1 | 0.0 |
| [[Vorgang/U4\|U4]] | Optimierung Kühlplatte/Ladeprofil mit Ersatzmodell, Bestwerte mit Elmer bestätigen | offen | 2 | 0.0 |
| [[Vorgang/X1\|X1]] | Seitencrash Pfahl, quasistatisch: Eindringung in Gehäuse/Querträger (CalculiX, plastisch, Kontakt) | offen | 3 | 3.0 |
| [[Vorgang/X2\|X2]] | Seitencrash dynamisch (OpenRadioss, Installation nur nach Freigabe) | offen | 4 | 3.0 |

## Nicht installierte Software

| Software | Status | Vorgänge |
|---|---|---|
| [[Software/foxBMS\|foxBMS]] | nicht installiert / nicht geprüft | [[Vorgang/E3\|E3]] |
| [[Software/OpenModelica\|OpenModelica]] | nicht installiert / nicht geprüft | [[Vorgang/E4\|E4]] |
| [[Software/OpenRadioss\|OpenRadioss]] | nicht installiert / nicht geprüft | [[Vorgang/X2\|X2]] |

## Recherche-Stand

| Thema | Status | Prüfung |
|---|---|---|
| [[Recherche/P01\|P01]] | fertig | 2 Belege bestaetigt, 0 Fehler |
| [[Recherche/P02\|P02]] | fertig | 2 Belege bestaetigt, 0 Fehler |
| [[Recherche/P03\|P03]] | fertig | 6 Belege bestaetigt, 0 Fehler |
| [[Recherche/P04\|P04]] | fertig | 6 Belege bestaetigt, 0 Fehler |
| [[Recherche/P05\|P05]] | fertig | 6 Belege bestaetigt, 0 Fehler |
| [[Recherche/P06\|P06]] | fertig | 6 Belege bestaetigt, 0 Fehler |
| [[Recherche/P07\|P07]] | fertig | 6 Belege bestaetigt, 0 Fehler |
| [[Recherche/P08\|P08]] | fertig | 6 Belege bestaetigt, 0 Fehler |
| [[Recherche/P09\|P09]] | fertig | 6 Belege bestaetigt, 0 Fehler |
| [[Recherche/P10\|P10]] | fertig | 6 Belege bestaetigt, 0 Fehler |
| [[Recherche/P11\|P11]] | fertig | 3 Belege bestaetigt, 0 Fehler |
| [[Recherche/P12\|P12]] | fertig | 5 Belege bestaetigt, 0 Fehler |
| [[Recherche/P13\|P13]] | fertig | 6 Belege bestaetigt, 0 Fehler |
| [[Recherche/P14\|P14]] | fertig | 0 Belege bestaetigt, 0 Fehler |
| [[Recherche/T01\|T01]] | fertig | 5 Belege bestaetigt, 0 Fehler |
| [[Recherche/T02\|T02]] | fertig | 4 Belege bestaetigt, 0 Fehler |
| [[Recherche/T03\|T03]] | fertig | 2 Belege bestaetigt, 0 Fehler |
| [[Recherche/T04\|T04]] | fertig | 3 Belege bestaetigt, 1 Fehler |
| [[Recherche/T05\|T05]] | fertig | 6 Belege bestaetigt, 0 Fehler |
| [[Recherche/T06\|T06]] | fertig | 4 Belege bestaetigt, 0 Fehler |
| [[Recherche/T07\|T07]] | fertig | 2 Belege bestaetigt, 1 Fehler |
| [[Recherche/T08\|T08]] | fertig | 9 Belege bestaetigt, 0 Fehler |
| [[Recherche/T09\|T09]] | fertig | 1 Belege bestaetigt, 0 Fehler |
| [[Recherche/W01\|W01]] | fertig | 12 Belege bestaetigt, 2 Fehler |
| [[Recherche/W02\|W02]] | fertig | 8 Belege bestaetigt, 5 Fehler |
| [[Recherche/W03\|W03]] | fertig | 24 Belege bestaetigt, 0 Fehler |
| [[Recherche/W04\|W04]] | fertig | 5 Belege bestaetigt, 0 Fehler |
| [[Recherche/W05\|W05]] | fertig | 0 Belege bestaetigt, 0 Fehler |
| [[Recherche/W06\|W06]] | fertig | 11 Belege bestaetigt, 1 Fehler |
| [[Recherche/W07\|W07]] | fertig | 8 Belege bestaetigt, 2 Fehler |
| [[Recherche/W08\|W08]] | fertig | 12 Belege bestaetigt, 0 Fehler |
| [[Recherche/W09\|W09]] | fertig | 10 Belege bestaetigt, 3 Fehler |
| [[Recherche/W10\|W10]] | fertig | 19 Belege bestaetigt, 4 Fehler |
| [[Recherche/W11\|W11]] | fertig | 10 Belege bestaetigt, 2 Fehler |
| [[Recherche/W12\|W12]] | fertig | 12 Belege bestaetigt, 0 Fehler |
| [[Recherche/W13\|W13]] | fertig | 10 Belege bestaetigt, 1 Fehler |
| [[Recherche/W14\|W14]] | fertig | 8 Belege bestaetigt, 1 Fehler |
| [[Recherche/W15\|W15]] | fertig | 10 Belege bestaetigt, 0 Fehler |
| [[Recherche/W16\|W16]] | fertig | 10 Belege bestaetigt, 0 Fehler |
| [[Recherche/W17\|W17]] | fertig | 14 Belege bestaetigt, 0 Fehler |
| [[Recherche/W18\|W18]] | fertig | 17 Belege bestaetigt, 1 Fehler |
| [[Recherche/W19\|W19]] | fertig | 20 Belege bestaetigt, 0 Fehler |
| [[Recherche/W20\|W20]] | fertig | 17 Belege bestaetigt, 4 Fehler |
| [[Recherche/W21\|W21]] | fertig | 12 Belege bestaetigt, 0 Fehler |
| [[Recherche/W22\|W22]] | fertig | 13 Belege bestaetigt, 1 Fehler |
| [[Recherche/W23\|W23]] | fertig | 12 Belege bestaetigt, 0 Fehler |
| [[Recherche/W24\|W24]] | fertig | 24 Belege bestaetigt, 0 Fehler |
| [[Recherche/W25\|W25]] | fertig | 10 Belege bestaetigt, 0 Fehler |
| [[Recherche/W26\|W26]] | fertig | 14 Belege bestaetigt, 0 Fehler |
| [[Recherche/W27\|W27]] | fertig | 7 Belege bestaetigt, 0 Fehler |
| [[Recherche/W28\|W28]] | fertig | 12 Belege bestaetigt, 11 Fehler |
| [[Recherche/W29\|W29]] | fertig | 8 Belege bestaetigt, 4 Fehler |
| [[Recherche/W30\|W30]] | fertig | 15 Belege bestaetigt, 0 Fehler |
| [[Recherche/W31\|W31]] | fertig | 6 Belege bestaetigt, 3 Fehler |
| [[Recherche/W32\|W32]] | fertig | 7 Belege bestaetigt, 5 Fehler |
| [[Recherche/W33\|W33]] | fertig | 5 Belege bestaetigt, 3 Fehler |
| [[Recherche/W34\|W34]] | fertig | 10 Belege bestaetigt, 2 Fehler |
| [[Recherche/W35\|W35]] | fertig | 9 Belege bestaetigt, 1 Fehler |
| [[Recherche/W35b\|W35b]] | fertig | 6 Belege bestaetigt, 1 Fehler |
| [[Recherche/W35c\|W35c]] | fertig | 8 Belege bestaetigt, 0 Fehler |
| [[Recherche/W35d\|W35d]] | fertig | 13 Belege bestaetigt, 1 Fehler |
| [[Recherche/W35e\|W35e]] | fertig | 7 Belege bestaetigt, 0 Fehler |
| [[Recherche/W36\|W36]] | fertig | 20 Belege bestaetigt, 0 Fehler |
| [[Recherche/W37\|W37]] | fertig | 8 Belege bestaetigt, 0 Fehler |
| [[Recherche/W37b\|W37b]] | fertig | 13 Belege bestaetigt, 0 Fehler |
| [[Recherche/W37c\|W37c]] | fertig | 1 Belege bestaetigt, 0 Fehler |
| [[Recherche/W38\|W38]] | fertig | 3 Belege bestaetigt, 0 Fehler |
| [[Recherche/W39\|W39]] | fertig | 7 Belege bestaetigt, 0 Fehler |
| [[Recherche/W40\|W40]] | fertig | 14 Belege bestaetigt, 1 Fehler |
| [[Recherche/W40b\|W40b]] | fertig | 13 Belege bestaetigt, 0 Fehler |
| [[Recherche/W41\|W41]] | fertig | 6 Belege bestaetigt, 1 Fehler |
| [[Recherche/W42\|W42]] | fertig | 6 Belege bestaetigt, 1 Fehler |
| [[Recherche/W43\|W43]] | fertig | 15 Belege bestaetigt, 2 Fehler |
| [[Recherche/W44\|W44]] | fertig | 3 Belege bestaetigt, 0 Fehler |
| [[Recherche/W47\|W47]] | fertig | 9 Belege bestaetigt, 0 Fehler |
| [[Recherche/W48\|W48]] | fertig | 11 Belege bestaetigt, 0 Fehler |
| [[Recherche/W49\|W49]] | fertig | 6 Belege bestaetigt, 0 Fehler |
| [[Recherche/W50\|W50]] | fertig | 11 Belege bestaetigt, 0 Fehler |
| [[Recherche/W51\|W51]] | fertig | 9 Belege bestaetigt, 0 Fehler |

---
*KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten*
