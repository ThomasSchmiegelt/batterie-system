---
typ: dokument
nr: "BAT-DOC-22"
version: "0.1"
status: "Entwurf"
tags: ["dokument"]
---
# BAT-DOC-22 – Qualitätsnachweis: Glaubwürdigkeit der Kernergebnisse

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

- Datei: `docs/22_qualitaetsnachweis`
- Version: 0.1
- Status: Entwurf
- Typ: Projektdokument (Dokumentenlenkung [[Dokument/00_dokumentenlenkung]])

## Genannte Anforderungen (Textvorkommen)
- [[Anforderung/REQ-P02|REQ-P02]]
- [[Anforderung/REQ-P07|REQ-P07]]
- [[Anforderung/REQ-P09|REQ-P09]]
- [[Anforderung/REQ-P12|REQ-P12]]
- [[Anforderung/REQ-P14|REQ-P14]]

## Genannte Entscheidungen, Befunde, Bauteile (Textvorkommen)
- [[Befund/B-BAT-042|B-BAT-042]]
- [[Befund/B-BAT-047|B-BAT-047]]
- [[Befund/B-BAT-049|B-BAT-049]]

## Vorgänge, die dieses Dokument nennen
- –

## Inhalt (Kopie aus `docs/22_qualitaetsnachweis.md`)

| Dok.-Nr. | BAT-DOC-22 | Version | 0.1 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Qualitätsnachweis: Glaubwürdigkeit der Kernergebnisse | Ersteller | Claude Opus (KI) | Prüfer | – (Mensch offen) |

> **KI-generiert.** Entwurf, nicht vom Menschen freigegeben. Testprojekt „KI im Engineering“, kein Produkt.

Vorgabe des Autors (2026-11-23): „wir müssen uns was überlegen um die qualität des ergebnisses zu belegen“, danach „ja, setze den qualitätsnachweis so auf“.
Das Schema lehnt sich an die Glaubwürdigkeitsbewertung für Modelle und Simulationen an (NASA-STD-7009, ASME V&V 10/20). Die Stufen und Texte unten sind ein **eigener Vorschlag von Opus** und keine Abschrift der Norm. Ob NASA-STD-7009 frei verfügbar ist, klärt Recherche W44.

## 1 Kategorien und Stufen (0–4)
| Kategorie | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| W Werkzeug geprüft | nicht geprüft | läuft, plausibel | Testfall mit bekannter Lösung bestanden | mehrere Testfälle, Konvergenzordnung bestätigt | Testfälle automatisch bei jedem Lauf |
| L Lösung geprüft | keine Prüfung | Bilanzen (Energie, Masse) geprüft | eine Netz- oder Zeitschrittvariante | Netzstudie mit Fehlerband (GCI) | Fehlerband für alle Ausgaben |
| V Validierung | keine | Vergleich mit realen Produkten (Größenordnung) | Vergleich mit veröffentlichtem Versuch, ähnlicher Fall | veröffentlichter Versuch, gleicher Fall | eigener Versuch |
| E Eingaben | überwiegend Annahmen | Annahmen benannt (Graph `herkunft`) | Haupteingaben belegt (Quelle mit Zitat) | alle wesentlichen Eingaben belegt | gemessen |
| U Unsicherheit | keine Angabe | Schätzung | Empfindlichkeit der 3 Haupteinflüsse | Band aus Empfindlichkeit plus Numerik | statistisch (Monte Carlo) |
| R Robustheit | Einzelfall | 2 Varianten | zweite Methode gleiche Größe, Abweichung erklärt | mehrere Methoden konsistent | – |
| D Durchsicht | keine | Opus | Opus und unabhängiges Modell (PI) | Mensch (Autor) | externer Fachmann |

Die Gesamtstufe eines Ergebnisses ist die **niedrigste** Kategorie, nicht der Mittelwert. Eine Angabe wie „rechnerisch erfüllt“ im V-Modell gilt erst ab Gesamtstufe 2 als Freigabegrundlage. Das ist ein Vorschlag, die Entscheidung trifft der Autor.

## 2 Kernergebnisse (zu bewerten)
| Nr | Ergebnis | Quelle | REQ |
|---|---|---|---|
| Q1 | T_max und Spreizung beim Schnellladen (K4 V4p) | sim/kuehlung/k3_gesamt/elmer_*_V4p | P09 |
| Q2 | Δp und Verteilung der Kühlplatte (K5) | sim/kuehlung/k5_parallel | P12 |
| Q3 | Zellverschiebung im Pfahlcrash (X3 a) | sim/mechanik/x3_crash_g5 | P14 |
| Q4 | Quetschung 100 kN (X3 b) | sim/mechanik/x3_crash_g5 | P14 |
| Q5 | Verluste der Verbinder (E1 G5) | sim/elektrik/e1_querschnitte | P13/P15 |
| Q6 | Ladezeit NMC 10→80 % (PyBaMM) | sim/chemie | P05 |
| Q7 | Packmasse | Stückliste | P07 |
| Q8 | Energieinhalt | Stückliste, startwerte | P02 |
| Q9 | Herstellkosten | pm/kosten | P16 |
| Q10 | Hüllmaß Pack | CAD G5.9 | P07 |

## 3 Arbeitspakete
| AP | Inhalt | Wer | GPU |
|---|---|---|---|
| QN1 | Werkzeug-Testfälle mit bekannter Lösung (Elmer, FluidX3D, OpenRadioss, PyBaMM, Verteiler-1D) → Kategorie W | Sonnet nach `sim/verifikation_werkzeuge/ERWARTUNG.md` | FluidX3D ja |
| QN2 | Vergleich mit realen Packs (Energiedichte, Masse, Volumen) → Kategorie V Stufe 1 | PI-Recherche W43, dann Sonnet nach `sim/vergleich_produkte/ERWARTUNG.md` | PI ja |
| QN3 | Bewertungstabelle je Q1–Q10 aus Akten, Graph (`herkunft`) und Ergebnissen; Skript `pm/plan/qualitaet.py` → Abschnitt 4 | Sonnet, Deutung Opus | nein |
| QN4 | Kennzahlen Prozess Schleife 1 (Erwartungen getroffen, gefundene Fehler nach Finder und Phase, Wächter-Fehlalarme) | Haiku zählt, Opus deutet | nein |
| QN5 | Netz- und Zeitschrittstudie für Q1 und Q3 (GCI) → Kategorie L | Schleife 2 | ja |
| QN6 | Empfindlichkeit der 3 Haupteinflüsse für Q1, Q3, Q7 → Kategorie U | Schleife 2 | teils |
| QN7 | Wiederholungstest aus frischem Checkout | Schleife 2, vor dem Abschluss | nein |
| QN8 | Erklärung der Abweichung K3 gegen K2 (Δp +232 %) mit QN1-Ergebnis FluidX3D | Opus | – |

## 4 Bewertung

Erzeugt von `pm/plan/qualitaet.py` (Sonnet) am 2026-11-23 17:01. Regeln siehe Kopf des Skripts. Stufe 0–4 nach Abschnitt 1, Gesamt = Minimum der bekannten Stufen, `*` = es gibt offene Kategorien ("? (Opus)"), die den Wert nur senken können. W nach Regel Opus (3 bestanden mit Ordnung, 2 ohne Ordnung, 0 verfehlt, 1 kein Testfall, - nicht anwendbar) aus `sim/verifikation_werkzeuge/ergebnis.json` (vorhanden), V aus `sim/vergleich_produkte/ergebnis.json` (vorhanden).

| Ergebnis | W | L | V | E | U | R | D | Gesamt (Min.) | begrenzt durch |
|---|---|---|---|---|---|---|---|---|---|
| Q1-LFP T_max und Spreizung Schnellladen, LFP (V4p) | 3 | 1 | 0 | 1 | 0 | 1 | 1 | **0** | V,U |
| Q1-NMC T_max und Spreizung Schnellladen, NMC (V4p) | 3 | 1 | 0 | 1 | 0 | 1 | 1 | **0** | V,U |
| Q2 Δp Kühlplatte (K5) | 2 | 1 (Opus) | 0 | 1 | 0 | 1 | 2 (Opus) | **0** | V,U |
| Q3 Zellverschiebung Pfahlcrash | 2 | 1 (Opus) | 0 | 1 | 0 | 1 (Opus) | 1 | **0** | V,U |
| Q4 Quetschung 100 kN | 2 | 0 (Opus) | 0 | 1 | 0 | 0 | 1 | **0** | L,V,U,R |
| Q5 Verluste Verbinder (E1 G5) | 1 | 0 | 0 | 1 (Opus) | 0 | 1 | 1 | **0** | L,V,U |
| Q6 Ladezeit NMC 10→80 % | 2 | 0 | 0 | 1 (Opus) | 0 (Opus) | 1 | 2 | **0** | L,V,U |
| Q7 Packmasse | - | 1 (Opus) | 0 | 1 | 0 (Opus) | 1 (Opus) | 2 (Opus) | **0** | V,U |
| Q8 Energieinhalt | - | 1 (Opus) | 1 | 1 | 0 (Opus) | 1 (Opus) | 1 (Opus) | **0** | U |
| Q9 Herstellkosten | - | 0 | 0 | 1 (Opus) | 0 | 1 | 2 (Opus) | **0** | L,V,U |
| Q10 Hüllmaß Pack | - | 1 (Opus) | 0 | 1 | 1 (Opus) | 1 (Opus) | 1 | **0** | V |

### Begründung mit Quellpfad
- **Q1-LFP**: W=3: ergebnis.json::faelle.V1 bestanden, Ordnung bestätigt; Wärmequelle V4p aus K1 (I²R, R aus K0-Eingaben, Annahme), nicht aus PyBaMM: k3_gesamt/k4_elmer.py Z.82 liest sim/kuehlung/k1_schnellladen/ergebnis.json; nur der Fall LFP_P0_K3_R128 nutzt C2-Widerstand 1,28 mΩ; L=1: sim/kuehlung/k3_gesamt/ERGEBNIS.md erwähnt Bilanz/Energiefehler; V=0: kein Vergleich mit Produkten oder Versuch; E=1: graph herkunft REQ-P09+sim/kuehlung/k3_gesamt: 7 Annahmen, 0 Quellen/Normen (100% Annahmen), alle bis zur Wurzel aufgelöst (docs/22 §1: Stufe 1 = Annahmen benannt); U=0: sim/kuehlung/k3_gesamt/ERGEBNIS.md ohne Unsicherheitsangabe; R=1: sim/kuehlung/k3_gesamt/ERGEBNIS.md nennt Varianten; D=1: docs/08: 13 Zeilen zu k3_gesamt, davon 1 Opus-Prüfung ok, 0 mit PI
- **Q1-NMC**: W=3: ergebnis.json::faelle.V1 bestanden, Ordnung bestätigt; Wärmequelle V4p aus K1 (I²R, R aus K0-Eingaben, Annahme), nicht aus PyBaMM: k3_gesamt/k4_elmer.py Z.82 liest sim/kuehlung/k1_schnellladen/ergebnis.json; nur der Fall LFP_P0_K3_R128 nutzt C2-Widerstand 1,28 mΩ; L=1: sim/kuehlung/k3_gesamt/ERGEBNIS.md erwähnt Bilanz/Energiefehler; V=0: kein Vergleich mit Produkten oder Versuch; E=1: graph herkunft REQ-P09+sim/kuehlung/k3_gesamt: 7 Annahmen, 0 Quellen/Normen (100% Annahmen), alle bis zur Wurzel aufgelöst (docs/22 §1: Stufe 1 = Annahmen benannt); U=0: sim/kuehlung/k3_gesamt/ERGEBNIS.md ohne Unsicherheitsangabe; R=1: sim/kuehlung/k3_gesamt/ERGEBNIS.md nennt Varianten; D=1: docs/08: 13 Zeilen zu k3_gesamt, davon 1 Opus-Prüfung ok, 0 mit PI
- **Q2**: W=2: ergebnis.json::faelle.V5 bestanden, Ordnung nicht bestimmt; L=1 (Opus): (Opus, ersetzt Skriptwert 0) Massenbilanz im Netz geschlossen, keine Diskretisierungsstudie; V=0: kein Vergleich mit Produkten oder Versuch; E=1: graph herkunft REQ-P12+sim/kuehlung/k5_parallel: 4 Annahmen, 0 Quellen/Normen (100% Annahmen), alle bis zur Wurzel aufgelöst (docs/22 §1: Stufe 1 = Annahmen benannt); U=0: sim/kuehlung/k5_parallel/ERGEBNIS.md ohne Unsicherheitsangabe; R=1: sim/kuehlung/k5_parallel/ERGEBNIS.md nennt Varianten; D=2 (Opus): (Opus, ersetzt Skriptwert 0) Opus prüfte K5 an Rohdaten, PI unabhängige Durchsicht (docs/08, K5)
- **Q3**: W=2: ergebnis.json::faelle.V3 bestanden, Ordnung nicht bestimmt; L=1 (Opus): (Opus, ersetzt Skriptwert 0) Energiefehler 0,18 % geprüft (x3 ergebnis.json), keine Netzstudie; V=0: kein Vergleich mit Produkten oder Versuch; E=1: graph herkunft REQ-P14+sim/mechanik/x3_crash_g5: 14 Annahmen, 0 Quellen/Normen (100% Annahmen), alle bis zur Wurzel aufgelöst (docs/22 §1: Stufe 1 = Annahmen benannt); U=0: sim/mechanik/x3_crash_g5/ERGEBNIS.md ohne Unsicherheitsangabe; R=1 (Opus): (Opus, ersetzt Skriptwert 0) Varianten s10/s40 nahezu gleich; D=1: docs/08: 16 Zeilen zu x3_crash, davon 3 Opus-Prüfung ok, 0 mit PI
- **Q4**: W=2: ergebnis.json::faelle.V3 bestanden, Ordnung nicht bestimmt; L=0 (Opus): (Opus, ersetzt Skriptwert 0) Lauf ab etwa 5 ms instabil, Ursache ungeklärt (B-BAT-042); V=0: kein Vergleich mit Produkten oder Versuch; E=1: graph herkunft REQ-P14+sim/mechanik/x3_crash_g5: 14 Annahmen, 0 Quellen/Normen (100% Annahmen), alle bis zur Wurzel aufgelöst (docs/22 §1: Stufe 1 = Annahmen benannt); U=0: sim/mechanik/x3_crash_g5/ERGEBNIS.md ohne Unsicherheitsangabe; R=0: sim/mechanik/x3_crash_g5/ERGEBNIS.md Einzelfall; D=1: docs/08: 16 Zeilen zu x3_crash, davon 3 Opus-Prüfung ok, 0 mit PI
- **Q5**: W=1: kein Testfall für das E1-Netz (Regel Opus), Stufe 1; L=0: sim/elektrik/e1_querschnitte/ERGEBNIS.md ohne Bilanz; V=0: kein Vergleich mit Produkten oder Versuch; E=1 (Opus): (Opus, ersetzt Skriptwert ? (Opus)) Ströme aus Startwerten (Annahme), Längen aus CAD, Leiterwerkstoff benannt: aufgelöst, nicht belegt; U=0: sim/elektrik/e1_querschnitte/ERGEBNIS.md ohne Unsicherheitsangabe; R=1: sim/elektrik/e1_querschnitte/ERGEBNIS.md nennt Varianten; D=1: docs/08: 6 Zeilen zu e1_querschnitte, davon 1 Opus-Prüfung ok, 0 mit PI
- **Q6**: W=2: sim/verifikation_werkzeuge/ergebnis_V4.json::saetze.NMC (Ladung +0.26 %, bestanden=True, keine Ordnung); L=0: sim/chemie/varianten_lfp_nmc/ERGEBNIS.md ohne Bilanz; V=0: kein Vergleich mit Produkten oder Versuch; E=1 (Opus): (Opus, ersetzt Skriptwert ? (Opus)) NMC-Parametersatz aus Literatur (PyBaMM), benannt, nicht an der Projektzelle gemessen; U=0 (Opus): (Opus, ersetzt Skriptwert ? (Opus)) keine Empfindlichkeit gerechnet; R=1: sim/chemie/varianten_lfp_nmc/ERGEBNIS.md nennt Varianten; D=2: docs/08: 8 Zeilen zu varianten_lfp_nmc, davon 1 Opus-Prüfung ok, 1 mit PI
- **Q7**: W=-: kein Simulationswerkzeug (Stückliste/CAD), W nicht anwendbar; L=1 (Opus): (Opus, ersetzt Skriptwert ? (Opus)) Bilanz CAD gegen Stückliste: Summe < 2 %, aber 29 Positionen > 2 % (B-BAT-047); V=0: kein Vergleich mit Produkten oder Versuch; E=1: graph herkunft REQ-P07: 2 Annahmen, 0 Quellen/Normen (100% Annahmen), alle bis zur Wurzel aufgelöst (docs/22 §1: Stufe 1 = Annahmen benannt); U=0 (Opus): (Opus, ersetzt Skriptwert ? (Opus)) kein Band; R=1 (Opus): (Opus, ersetzt Skriptwert ? (Opus)) zwei Wege (CAD, Stückliste), Abweichung je Position unerklärt; D=2 (Opus): (Opus, ersetzt Skriptwert 0) Opus und PI-Gutachten Punkt 1 (bericht/pi_gutachten_1.1.md)
- **Q8**: W=-: kein Simulationswerkzeug (Stückliste/CAD), W nicht anwendbar; L=1 (Opus): (Opus, ersetzt Skriptwert ? (Opus)) Zellzahl × Zellenergie gegen Stückliste geprüft; V=1: sim/vergleich_produkte/ergebnis.json::kategorie_V.Q8; E=1: graph herkunft REQ-P02: 1 Annahmen, 0 Quellen/Normen (100% Annahmen), alle bis zur Wurzel aufgelöst (docs/22 §1: Stufe 1 = Annahmen benannt); U=0 (Opus): (Opus, ersetzt Skriptwert ? (Opus)) kein Band; R=1 (Opus): (Opus, ersetzt Skriptwert ? (Opus)) Startwert und Stückliste stimmen überein, keine unabhängige Methode; D=1 (Opus): (Opus, ersetzt Skriptwert 0) Opus
- **Q9**: W=-: kein Simulationswerkzeug (Stückliste/CAD), W nicht anwendbar; L=0: pm/kosten/ERGEBNIS.md ohne Bilanz; V=0: kein Vergleich mit Produkten oder Versuch; E=1 (Opus): (Opus, ersetzt Skriptwert ? (Opus)) Preise benannt, 99,8 % geschätzt (pm/kosten); U=0: pm/kosten/ERGEBNIS.md ohne Unsicherheitsangabe; R=1: pm/kosten/ERGEBNIS.md nennt Varianten; D=2 (Opus): (Opus, ersetzt Skriptwert 0) Opus und PI-Gutachten Punkt 2
- **Q10**: W=-: kein Simulationswerkzeug (Stückliste/CAD), W nicht anwendbar; Wärmequelle V4p aus K1 (I²R, R aus K0-Eingaben, Annahme), nicht aus PyBaMM: k3_gesamt/k4_elmer.py Z.82 liest sim/kuehlung/k1_schnellladen/ergebnis.json; nur der Fall LFP_P0_K3_R128 nutzt C2-Widerstand 1,28 mΩ; L=1 (Opus): (Opus, ersetzt Skriptwert ? (Opus)) Kollisionsprüfung 0, Maß aus CAD-Hülle; V=0: kein Vergleich mit Produkten oder Versuch; E=1: graph herkunft REQ-P07: 2 Annahmen, 0 Quellen/Normen (100% Annahmen), alle bis zur Wurzel aufgelöst (docs/22 §1: Stufe 1 = Annahmen benannt); U=1 (Opus): (Opus, ersetzt Skriptwert ? (Opus)) Fertigungstoleranzen nicht betrachtet, Maß deterministisch; R=1 (Opus): (Opus, ersetzt Skriptwert ? (Opus)) nur CAD; D=1: docs/08: 25 Zeilen zu G5.9, davon 1 Opus-Prüfung ok, 0 mit PI

---
*KI-generiert (Claude Opus, 2026-11-23). Status Entwurf. Freigabe nur durch den Autor.*

## Nachtrag QN4 (Opus, 2026-11-23)
Die Zählung von Haiku (docs/22a) zeigt, dass Schleife 1 keine maschinenlesbaren Prozesskennzahlen hinterlassen hat. Ob eine Erwartung getroffen wurde, steht nirgends als Feld (0 Treffer). 36 von 48 Befunden nennen keinen Finder, und in docs/08 sind die Akteure uneinheitlich geschrieben. Die Kennzahlen für Schleife 1 lassen sich nur von Hand aus dem Text rekonstruieren, das macht Opus bei Bedarf. Ab Schleife 2 gelten die Pflichtzeilen „Erwartung:“ und „Gefunden von:“ in der ERWARTUNG (sim/VORLAGE_ERWARTUNG.md), und in BEFUNDE steht der Finder in der Überschrift.

## 5 Kernaussage (Opus, 2026-11-23)
Kein Kernergebnis erreicht derzeit Gesamtstufe 1 oder höher. Das liegt nicht an den Werkzeugen. Die Löser haben ihre Testfälle bestanden (W 2–3, QN1), mit Ausnahme des LFP-Zellmodells (W 0, B-BAT-049). Begrenzt wird durchgehend durch **V (keine Validierung)** und **U (keine Unsicherheitsangabe)**, bei Crash und Elektrik zusätzlich durch L (keine Netzstudie). Die Ergebnisse der Schleife 1 sind deshalb als **Tendenz und Variantenvergleich** brauchbar, nicht als Freigabenachweis. Diesen Schluss tragen auch die V-Modell-Bewertungen „rechnerisch erfüllt (nicht validiert)“.
Was die Stufe am stärksten hebt (Vorschlag für Schleife 2):
1. U: Empfindlichkeit der 3 Haupteinflüsse für Q1, Q3 und Q7 (QN6). Das hebt U auf 2 und braucht nur Rechenzeit.
2. L: Netzstudie für Q1 und Q3 (QN5).
3. V: Veröffentlichte Versuche (Kühlplatte, Zellquetschung) mit Zitatprüfung und die Packmassen realer Produkte (W43 fand keine geprüfte Packmasse, W43b nötig). Wirklich belastbar macht es erst ein eigener Versuch (Versuchsplan).

