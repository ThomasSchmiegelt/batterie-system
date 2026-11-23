# Kontext für das Bauteilgespräch: BT-600 Kühlung

KI-generiert von pm.py aus Projektdateien (nur eigene Dokumente).

## Ich bin
Kühlung (BT-600). Aufgabe: führt Wärme ab, beim Schnellladen. Teil von: BT-000. Meine Teile: BT-610 Kühlplatte, BT-620 Verteiler und Sammler, BT-630 Kühlmittelanschlüsse, BT-640 Temperaturfühler Kühlmittel, BT-650 Kühlmittel, BT-660 Schnittstelle Fahrzeugkreis.

## Meine Merkmale (Wert und entscheidende Akte)
- kuehlart: "Kühlplatte oben und unten"  (ENT-088)

## Anforderungen an mich (Lastenheft)
| REQ-P05 | Schnellladen 10 → 80 % | LFP 20 min, NMC-4680 30 min (Autor 2026-11-17 „30 minuten“, nach K1b; Variantenunterschied) | Autor | Muss | festgelegt |
| REQ-P08 | Umgebungstemperatur Betrieb und Laden | offen (°C) | Autor / Norm | Muss | offen |
| REQ-P09 | max. Zelltemperatur und Spreizung | T_max ≤ 45 °C, Spreizung in der Zelle ≤ 5 K (Autor 2026-11-17) | Autor | Muss | festgelegt |
| REQ-P12 | Kühlmittel und Anschlüsse | Vorschlag Wasser-Glykol | Autor | Soll | offen |

## Entscheidungen, die mich betreffen (vollständig)
### ENT-081 Kühlart Kühlplatte unten, für beide Varianten (2026-11-17, entschieden (Mensch), Autor (Entscheidung 2026-11-17: „Kühlplatte unten“); Variante: alle)
Merkmal: kuehlart = "Kühlplatte unten" ; Anforderungen: REQ-P09; Belege: B-BAT-017
## Frage
Wie werden die Zellen gekühlt? (K0-Fälle: K1 Boden, K2 4680 Mantel)
## Alternativen
| Alternative | dafür | dagegen |
|---|---|---|
| **Kühlplatte unten (gewählt, Autor)** | eine Platte für beide Varianten; LFP: Wärmeweg in der gut leitenden Ebene (90 mm); 4680: axial gut leitend | Wärme nur über eine Fläche; Spreizung über die Höhe |
| 4680 seitliche Kühlbänder | kurze Wege zum Mantel | radial schlecht leitend, aufwendig |
## Entscheidung und Begründung
Autor legt Kühlplatte unten fest, zusammen mit den Zielen REQ-P09: T_max ≤ 45 °C, Spreizung in der Zelle ≤ 5 K.
## Folgen
K0: Fall K1 ist der Hauptfall, K2 nur Vergleich. Folgt: Kühlplatte BT-610 auslegen (Kanäle, Durchfluss), Wärmeleitmaterial BT-230.

---
*KI-generiert (Claude Opus, 2026-11-17).*

### ENT-088 Kühlart: Kühlplatte oben und unten (2026-11-17, entschieden (Mensch), Opus (Vorschlag M0) / Autor (2026-11-17: „ja gehen wir ersteinmal so ins rennen“); Variante: alle)
Merkmal: kuehlart = "Kühlplatte oben und unten" ; Anforderungen: REQ-P09; Belege: B-BAT-019
## Frage
Gehäuse-Vorauslegung M0 (sim/mechanik/m0_gehaeuse/).
## Entscheidung und Begründung
K1: nur so erfüllen beide Varianten REQ-P09 beim Schnellladen (LFP 20 min 33,8 °C/4,6 K; NMC 25 min 34,0 °C/3,8 K). sim/kuehlung/k1_schnellladen/DEUTUNG.md.
## Folgen
Gehäuse-CAD (G4), Crash X, Kühlplatte K2.

---
*KI-generiert (Claude Opus, 2026-11-17).*

## Befund B-BAT-017
B-BAT-017 (2026-11-17) Vorgaben Kühlung (REQ-P09, ENT-081); Bericht begonnen
- Autor: „45 °C und 5 K passen, Kühlplatte unten, bitte auch temperaturverläufe grafisch am besten als gerendertes Bild, und für die dikoumentation abspeichern, fange auch an den bericht zu schreiben“.
- REQ-P09: T_max ≤ 45 °C, Spreizung in der Zelle ≤ 5 K (festgelegt). ENT-081 BT-600 kuehlart = Kühlplatte unten (beide Varianten, entschieden). K0: K1 Hauptfall, gerenderte Temperaturbilder und Film (pvbatch) nachbeauftragt.
- Bericht BAT-DOC-17 (bericht/bericht.tex, LaTeX wie Fusion-Bericht, Lesehilfe je Bild, Begriffskästen) an Sonnet nach Gliederung von Opus. Vorgang: [K0] [B1]

## B-BAT-016 (2026-11-17) Detailmodell Innenaufbau fertig; 4680-Wickel ragte über den Becher (Opus-Fehler im Kern)
- Sonnet (cad/zelle/AUFTRAG_DETAIL.md, 42 min, CPU): FreeCAD-Detailmodelle beider Zellen, 7 Schnitt-/Explosionsbilder, Neulauf G1/C0b mit 1430 mm (LFP A passt, Reserve L 16 / B 8 mm; nötig 203,9 Wh/L; NMC 1260 Plätze).
- LFP-Stapel 12,476 mm in 13,4 mm (Rest 0,92 mm) – wie erwartet. Bild LFP_schnitt angesehen: Schichtfolge, Fahnen, Stromschiene, Halter, O-Ring, Isolationsbeutel erkennbar und beschriftet.
- **Verfehlt:** 4680-Wickel Außenradius 23,75 mm > 22,6 mm. Ursache 1 (Opus): ENT-074 Kern Ø 14 mm nur aus Kathodenfläche abgeleitet; mit allen Bändern (1477 mm²) Kern ≤ 12,75 mm → ENT-074 auf 12,5 mm korrigiert. Ursache 2 (Modell): feste Steigung 0,45 mm auch dort, wo nur noch Anode/Separator liegt → flächentre

## Befund B-BAT-019
B-BAT-019 (2026-11-17) Schnellladen in den Griff bekommen (K1); Gehäuserecherche W21
- Autor: „Ja das schnellladen müssen wir in den griff bekommen. man läd schwellenartig könnte auch sein, oder nur bestimmte zellen im wechsel, kühlen kann man auch und dann natürlcih begrenzen. mach die renderings neu. bei der gesamtbatterie müssen verstrebungen vorgehalten werden du kannst mal eine recherche machen wie ein batteriegehäuse aufgebaut ist.“
- Opus vorab: Bei fester Ladezeit erzeugt konstanter Strom die wenigste Joulewärme; Stufen +9 %, Puls/Zellen im Wechsel +100 %. In Reihe führen alle Zellen denselben Strom → Wechsel einzelner Zellen nur bei Parallelgruppen und dann wärmer. Spreizung hängt am Wärmeweg: nur beidseitige Kühlung oder kleinerer Strom (LFP ≤ 1,29C, NMC ≤ 1,02C stationär) bringt 5 K. Prüfung durch Rechnung K1.
- Autor (Nachtrag): „bei der Breite sind wir nicht so variabel letzten endes von straßenbreite begrenzt, länge ist etwas einfacher.“ → Breite 1430 mm gilt als fest, Länge darf wachsen. Folge Opus: Querträger quer zur Fahrtrichtung kosten Länge (zulässig); ein Längsträger zwischen den zwei LFP-Zellreihen und breitere Seitenrahmen kosten Breite (Reserve 8 mm) → kritisch, Seitenrahmenbreite aus W22 gegen den angenommenen Rand prüfen.
- Verstrebungen: struktur.json hat BT-530 Querträger, BT-540 Seitenrahmen, BT-550 Unterfahrschutz; W21 soll Werte liefern. Wichtig für Bauraum: Querträger kosten Länge/Breite (G1-Reserve LFP 16/8 mm!). - W21 (12/0): Bauweise CTP, Wa

