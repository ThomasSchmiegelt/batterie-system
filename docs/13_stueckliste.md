| Dok.-Nr. | BAT-DOC-13 | Version | 0.1 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Grobe Stückliste | Ersteller | Claude Opus (KI), pm/bauteile/stueckliste.py | Prüfer | – (Mensch offen) |

> **Variante: (ohne Variantenangabe); Zellformat offen.**
> **KI-generiert.** Nicht von Hand bearbeiten, das Skript schreibt die Datei neu. Baugruppen und Hauptkomponenten, keine Normteile.
> Mengen hängen am **Startsatz (Vorschlag, nicht freigegeben)** und an **Annahmen**; sie ändern sich mit Lastenheft und Auslegung.

Startsatz: „Kompaktwagen, 400 km Reichweite, in 20 min auf 80 %, Mitteleuropa“ → NMC, 800 V, 73.9 kWh brutto.

**Zellverschaltung:** 220s × 1p = **220 Zellen**, 73.9 kWh (3.65 V Annahme; 92.0 Ah je Zelle abgeleitet aus Energie und 800 V, ENT-006; Annahme bisher 100 Ah).

Art: K = Kaufteil, E = Eigenteil (wird im Projekt konstruiert), S = Schnittstelle zum Fahrzeug (nur Anforderung).

## BT-100 Zelle

| Pos. | Bauteil | Benennung | Menge | Herleitung | Art | Auslegung (Vorgang) | Recherche | Bemerkung |
|---|---|---|---|---|---|---|---|---|
| 100.1 | BT-100 | Zelle (NMC, Zellformat offen; Rechenregel wie LFP-Platzhalter) | 220 | 220s × 1p | K | C2, G1 | W01, W03, W08, W10, P01 | Energie 73.9 kWh bei 92.0 Ah (Annahme bisher 100 Ah); Ah abgeleitet aus Energie und 800 V (ENT-006); Maße folgen in G1 |

## BT-200 Zellstack

| Pos. | Bauteil | Benennung | Menge | Herleitung | Art | Auslegung (Vorgang) | Recherche | Bemerkung |
|---|---|---|---|---|---|---|---|---|
| 200.1 | BT-210 | Zellreihe zwischen Querträgern (Cell-to-Pack, ohne Module) | 10 | 220 / 24 | E | G4 | W03, P02 | Alternative: Module, falls CTP verworfen |
| 200.2 | BT-220 | Zwischenlage zwischen Zellen (Wärme- und Brandschutz, Quellausgleich) | 220 | 1 je Zelle | K | G4, M1 | W04, P04 | Werkstoff offen (z. B. Glimmer, Aerogel) |
| 200.3 | BT-230 | Wärmeleitmaterial Zelle → Kühlplatte | 1 | 1 Lage, Fläche aus G4 | K | G4, K3 | W16, P03 |  |
| 200.4 | BT-240 | Verspannung der Zellreihen (Endplatte/Band) | 10 | 1 je Reihe | E | M1 | W15 | Quellen der Zellen beim Laden |

## BT-250 Zellhalter

| Pos. | Bauteil | Benennung | Menge | Herleitung | Art | Auslegung (Vorgang) | Recherche | Bemerkung |
|---|---|---|---|---|---|---|---|---|
| 200.5 | BT-250 | Zellhalter (hält und teilt Rundzellen, Abstand für Kühlung und Isolation) | 1 | 1 Satz | K | G4 | – | Maße offen, G4; nur NMC (Rundzelle) |

## BT-300 Regelung (BMS)

| Pos. | Bauteil | Benennung | Menge | Herleitung | Art | Auslegung (Vorgang) | Recherche | Bemerkung |
|---|---|---|---|---|---|---|---|---|
| 300.1 | BT-310 | BMS-Hauptsteuergerät | 1 | – | K | E3 | W05, W14, T06 | Ladezustand, Alterung, Schutzlogik, Fahrzeug-CAN |
| 300.2 | BT-320 | Zellüberwachung (Spannung, Ausgleich) | 14 | 220 / 16 | K | E3 | W05, W14, P07 | passiver oder aktiver Ausgleich offen |
| 300.3 | BT-330 | Temperaturfühler Zelle | 55 | 220 / 4 | K | E3, K3 | W05 |  |
| 300.4 | BT-340 | Strommessung (Shunt oder Hall) | 1 | – | K | E3 | W14 |  |
| 300.5 | BT-350 | Isolationswächter | 1 | – | K | E2 | W13 | REQ-P13 |
| 300.6 | BT-360 | Messleitungen bzw. Flexleiterplatte Zelle → Überwachung | 14 | 1 je Überwachungsbaustein | K | E3, L1 | P07 |  |

## BT-400 Verkabelung und Zellverbinder

| Pos. | Bauteil | Benennung | Menge | Herleitung | Art | Auslegung (Vorgang) | Recherche | Bemerkung |
|---|---|---|---|---|---|---|---|---|
| 400.1 | BT-410 | Zellverbinder (Zellabgriff, Plus und Minus je Zelle) | 0 | entfällt bei p = 1 (Reihenverbinder 400.2 sind die Zellverbinder) | E | E1 | W13, P06 | Querschnitt aus Strom und Erwärmung (E1); Opus 2026-11-17: Mengen aus s und p |
| 400.2 | BT-420 | Reihenverbinder (Reihenbrücke, bei p > 1 Gruppenbrücke) | 219 | s − 1 = 220 − 1 | E | E1, L1 | W13 | Opus 2026-11-17: aus s abgeleitet (LFP 249, NMC 216) |
| 400.3 | BT-430 | HV-Hauptleitung plus/minus im Pack | 2 | – | K | E1, L1 | W13, T09 | Verlegung skizzieren (Sketch-to-Prompt) |

## BT-500 Struktur und Gehäuse

| Pos. | Bauteil | Benennung | Menge | Herleitung | Art | Auslegung (Vorgang) | Recherche | Bemerkung |
|---|---|---|---|---|---|---|---|---|
| 500.1 | BT-510 | Gehäusewanne | 1 | – | E | G4, X1 | W15, P10 | Werkstoff offen (Alu-Strangpress/Guss, Stahl) |
| 500.2 | BT-520 | Deckel mit Dichtung | 1 | 1 Satz | E | G4 | W15 | Schutzart REQ-P13 |
| 500.3 | BT-530 | Querträger | 11 | 10 Reihen + 1 | E | G4, X1 | W15, P02 | tragen und trennen Zellreihen |
| 500.4 | BT-540 | Seitenrahmen / Crashprofil (Seitencrash) | 2 | links, rechts | E | X1, X2 | W17, T08 |  |
| 500.5 | BT-550 | Unterfahrschutz | 1 | – | E | M1 | W15 | Steinschlag, Aufsetzen |
| 500.6 | BT-560 | Befestigungspunkte am Fahrzeug | 1 | 1 Satz | E | M1 | – | Fest-/Loslager (Lehre Wasserstoff) |
| 500.7 | BT-570 | Druckausgleichselement (atmend, wasserdicht) | 1 | – | K | G5 | – |  |

## BT-600 Kühlung

| Pos. | Bauteil | Benennung | Menge | Herleitung | Art | Auslegung (Vorgang) | Recherche | Bemerkung |
|---|---|---|---|---|---|---|---|---|
| 600.1 | BT-610 | Kühlplatte (Wasser-Glykol) | 1 | 1 oder je Reihe, aus K0/K3 | E | K0, K3, U4 | W16, P03 | Alternative Luftkühlung: Gebläse + Kanäle (Entscheidung K0) |
| 600.2 | BT-620 | Verteiler und Sammler | 1 | 1 Satz | E | K2, K4 | P03 | Gleichverteilung entscheidet (Lehre Wasserstoff); Austritt ≥ Eintritt (Regel des Autors aus Fusion, hier prüfen) |
| 600.3 | BT-630 | Kühlmittelanschlüsse Ein/Aus | 2 | – | K | K2 | – |  |
| 600.4 | BT-640 | Temperaturfühler Kühlmittel | 2 | Ein, Aus | K | K3, E3 | – |  |
| 600.5 | BT-650 | Kühlmittel Wasser-Glykol | 1 | Füllmenge aus K2 | K | K2 | W16 | REQ-P12 |
| 600.6 | BT-660 | Pumpe, Wärmetauscher/Kältemittelkühler | 1 | Fahrzeugseite | S | K0 | W16 | nur Schnittstelle: Durchfluss, Eintrittstemperatur |

## BT-700 Zusatzkomponenten

| Pos. | Bauteil | Benennung | Menge | Herleitung | Art | Auslegung (Vorgang) | Recherche | Bemerkung |
|---|---|---|---|---|---|---|---|---|
| 700.1 | BT-710 | Schaltbox (Gehäuse für Schütze, Vorladung, Hauptsicherung) | 1 | – | E | E2, G4 | W13 | Trennstelle Stack/Fahrzeug; Einbauort aus G4 |
| 700.2 | BT-711 | Hauptschütz plus und minus | 2 | – | K | E2 | W13 | 800 V DC, Strom aus REQ-P04/P05 |
| 700.3 | BT-712 | Vorladeschütz mit Vorladewiderstand | 1 | 1 Satz | K | E2, E4 | W13 | Einschaltstrom der Umrichterkondensatoren |
| 700.4 | BT-713 | Hauptsicherung (ggf. pyrotechnischer Trenner) | 1 | – | K | E2 | W13 | Kurzschlussfall E4 |
| 700.5 | BT-720 | Service-Trennstecker | 1 | – | K | E2 | W13 | Werkstatt: Pack spannungsfrei schalten |
| 700.6 | BT-730 | HV-Steckverbinder Pack (Antrieb, Laden) | 2 | – | K | E2, L1 | W12, W13 |  |
| 700.7 | BT-740 | NV-Steckverbinder (12 V, CAN, Sensorik) | 1 | – | K | E3 | W14 |  |
| 700.8 | BT-750 | Entgasungsventil mit Entgasungskanal | 1 | 1 Satz | K | G5 | W04, P05 | thermisches Durchgehen, REQ-P11 |
| 700.9 | BT-760 | Heizung (Kälte, −20 °C laut REQ-P08) | 1 | – | K | K0, C5 | W01, W16 | oder über Kühlkreis (Fahrzeugseite) |
| 700.10 | BT-770 | Gas-/Drucksensor Früherkennung thermisches Ereignis | 1 | – | K | E3, F1 | W04 | Warnzeit REQ-P11 |
| 700.11 | BT-780 | Kennzeichnung (Typschild, HV-Warnung) | 1 | 1 Satz | K | B4 | – | Normen BAT-DOC-07 |

## Annahmen

- `U_zelle` = {'LFP': 3.2, 'NMC': 3.65}
- `Ah_zelle` = {'LFP': 140, 'NMC': 100}
- `kanaele_je_ueberwachung` = 16
- `zellen_je_tempfuehler` = 4
- `zellen_je_reihe` = 24

---
*KI-generiert. 39 Positionen. Vorgänge siehe pm/plan/wissensnetz.html.*
