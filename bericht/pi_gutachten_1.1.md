# Gutachter-Stellungnahme – 8 konkrete Schwächen

---

## 1. Widerspruch: Packmasse LFP, desselben „Stand G5.9" zwei unterschiedliche Werte

**Fundstelle (wörtlich):**
- Zusammenfassung, Punkt „Masse": *„Stückliste auf Stand G5.9: LFP 626,8 kg"* (Quelle: `pm/bauteile/stueckliste_LFP.json`)
- REQ-P06, Spalte „Ergebnis": *„beide Packs als G5.9-Modell gebaut: LFP 1347 Teile, **629,6 kg**"* (Quelle: `cad/baukasten/ausgabe/ergebnis_LFP.json`)
- Analog NMC: 486,4 kg (Zusammenfassung) vs. 480,7 kg (REQ-P06).

**Problem:** Dieselbe Baugruppe, derselbe Stand, zwei Massen mit 2,8 bzw. 5,7 kg Unterschied. Der Report erklärt nicht, was in der einen Datei fehlt oder in der anderen doppelt gezählt wird. Für einen Konstrukteur, der die 30 %-Massengrenze prüft, ist unklar, welche Zahl maßgeb ist.

**Vorschlag:** Eine eindeutige Zeile: „Maßgebliche Masse = X kg (Quelle …); Abweichung zur Bauteil-Stückliste Y kg wegen [Fehlende Position / Dopplung]." Beide Werte nebeneinander mit Erklärung, welcher die Freigabe trägt.

---

## 2. REQ-P16 „erfüllt" – trotz fehlendem Zielwert und 29 offenen Positionen

**Fundstelle (wörtlich):**
- REQ-P16, Status-Spalte: *„erfüllt"*
- Dieselbe Zeile, Ergebnis: *„alle Preise Schätzung, Teilsummen"*
- Zusammenfassung, Punkt „Kosten": *„Verifiziert ist nur der Marktpreis 97 USD/kWh (W29), die Pack-Preise selbst sind **Annahmen**. REQ-P16 hat **keinen Zielwert**."*
- Offene Punkte: *„16 (LFP) und 13 (NMC) Positionen sind offen"*

**Problem:** Eine Anforderung, die keinen Zielwert hat, 29 offene Kalkulationspositionen aufweist und deren einziger verifizierter Wert ein Fremdmarktpreis ist, wird als „erfüllt" deklariert. Für einen Konstrukteur, der eine Einkaufs- oder Vergabeentscheidung vorbereitet, suggeriert dies eine Absicherung, die nicht existiert.

**Vorschlag:** Status ändern auf „offen – Zwischenergebnis, alle Werte Annahme, 29 Positionen unbesetzt". Falls der Autor „Ausweisen = Zahlen nennen" will, steht das als Zielwerterklärung in der Lastenheft-Zeile.

---

## 3. NMC-Verlustleistung: drei verschiedene Werte für denselben Lastfall

**Fundstelle (wörtlich):**
- Zusammenfassung, „Elektrik": *„E1: Verluste der Verbinder bei Dauerstrom … NMC **385,4 W** (Querschnitt 15 × 3 mm). E2 … NMC **316,0 W** (Akte 25 × 3 mm)"*
- Kapitel 20, Punkt 4: *„Befund: Verluste **364,5 W** (Ziel ≤ 300 W)"* (Quelle: `e1_querschnitte/ergebnis_g5.json`)

**Problem:** 385,4 W, 316,0 W und 364,5 W werden alle als „NMC-Verlust" bezeichnet, ohne dass ersichtlich ist, welche der drei der aktuell gültige Wert ist (unterschiedliche Querschnitte, unterschiedliche Aktenstände, unterschiedliche Berechnungstiefe). Ein Konstrukteur, der now den Querschnitt für die Fertigung freigibt, kann aus dem Bericht nicht ableiten, welchen der drei er zugrunde legen soll.

**Vorschlag:** Einen Satz: „Maßgeblicher Wert für die Freigabe: X W (Quelle …, Stand …). Die übrigen Werte sind historische Zwischenstände." Die drei Zahlen in einer kleinen Tabelle mit Querschnitt, Akte und Datum.

---

## 4. LFP-Schnellladen: Ziel 20 min nicht prüfbar – aber nicht als „nicht erreichbar" deklariert

**Fundstelle (wörtlich):**
- Zusammenfassung: *„Schnellladezeit … vom Autor festgelegt: LFP 20 min … die LFP-Parametersatz aus PyBaMM **passt nicht**, die Blade-Zelle ist mit 0,877 mΩ gemessen."*
- REQ-P05, Status: *„offen"*; Ergebnis: *„Ladezeit LFP **nicht am Zellmodell bestätigt**"*
- Offene Punkte, Zellmodell C3: *„Der LFP-Parametersatz passt nicht (Temperaturfit 158 mV, Ruhespannung 143 mV daneben)"*

**Problem:** „Offen" suggeriert, die Frage sei noch prüfbar und könnte bei weiterer Arbeit „erfüllt" werden. In Wirklichkeit ist der Parametersatz bekanntlich unbrauchbar, Messdaten fehlen, und der Bericht listet unter Risken, dass dies solange der Fall ist, die Anforderung nicht verifiziert werden kann. Für einen Konstrukteur, der die Ladeelektronik jetzt auslegt, ist die entscheidende Antwort: *„Mit dem verfügbaren Zellmodell kann das 20-min-Ziel weder bestätigt noch widerlegt werden; eine Freigabe auf dieser Basis ist nicht möglich."*

**Vorschlag:** REQ-P05 Status auf „offen – LFP: Verifikation unmöglich bis Zelle geliefert" (oder ein eigener Status „blockiert") und in der Zusammenfassung einen klaren Satz: „LFP 20 min: nicht nachweisbar; NMC 30 min: am Modell 29,7 min, aber Plating-Risiko."

---

## 5. Packhöhe 130 mm: mal „Annahme", mal „Grenze überschritten"

**Fundstelle (wörtlich):**
- Zusammenfassung, „Bauraum": *„Höhe 130 mm (**Annahme**)"*
- Zusammenfassung, „Elektrik": *„Packhöhe vorn LFP 134 mm (**Grenze 130 mm überschritten**)"*
- REQ-P07, Zielwert: *„H 130 mm (Annahme)"*

**Problem:** Derselbe Wert wird im selben Dokument durch einen Strich als bloße „Annahme" (daher nicht prüfbar) bezeichnet, durch den nächsten als „Grenze", deren Überschreitung ein „Verstoß" ist. Ein Konstrukteur weiß nicht, ob 130 mm verhandelbar ist (dann: ein Design-Freigabe-Vorgang) oder hart (dann: 4 mm Übermaß ist ein Konformitätsfehler).

**Vorschlag:** In REQ-P07 den Status von „Annahme" auf „Annahme des Autors, vom Autor als Freigabelimit bestätigt (ENT-XXX)" heraufstufen – oder explizit schreiben: „130 mm ist Annahme ohne Aktenbeleg; die 4 mm Überschreitung E2D ist daher kein formaler Verstoß, aber ein Freigabe-Hindernis."

---

## 6. Druckverlust: 0,715 / 0,70 / 0,215 / 0,17 bar – kein Designwert benannt

**Fundstelle (wörtlich):**
- Kapitel 20, Punkt 6: *„K3 (FluidX3D) liefert Δp **+232 % gegenüber der Korrelation (0,715 gegen 0,215 bar)**"*
- Kapitel 20, Punkt 5: *„Der dreifache Durchfluss senkt Δp (**0,70 auf 0,17 bar** je Platte)"*
- Offene Punkte: *„K2 ist eine 1D-Rechnung (Kanal 4 × 5 mm, laminar). Nicht gerechnet: Strömung im 3D-Modell"*

**Problem:** Für die Pumpenauslegung (Verbesserung 5) braucht der Konstrukteur **einen** Δp-Wert. Der Bericht führt vier Zahlen aus verschiedenen Rechnungsstufen (1D-Korrelation, FluidX3D, K5-Optimierung) nebeneinander, bezeichnet K3 als „+232 % über der Korrelation" und K2 als nicht 3D-validiert – nennt aber keinen „für die Auslegung maßgeblichen" Wert.

**Vorschlag:** Ein Satz in Kapitel 20, Punkt 5: „Für die Pumpenauslegung wird der konservative Wert Z bar (Quelle …) angesetzt; die übrigen Werte sind untere/obere Schranken." Oder: „Konsens-Δp = max(K2, K3) = …"

---

## 7. Fehlende Gesamtbewertung: kein Go/No-Go, keine Priorisierung der verfehlten Kernziele

**Fundstelle (wörtlich):**
- Zusammenfassung, Kernaussage Kapitel 2: *„Von 16 Produktanforderungen sind 3 erfüllt, 2 verfehlt, 8 offen und 3 nicht untersucht"*
- REQ-P07: *„verfehlt"*; REQ-P09: *„verfehlt"*; REQ-P14: *„offen … Normnachweis fehlt"*
- Kapitel 20 Prioritätentabelle: Reihenfolge 1–8, aber *„Die Reihenfolge ist ein **Vorschlag** …; die Entscheidung liegt beim Autor."*

**Problem:** Ein Pkw-Entwickler, der den Bericht als Entscheidungsvorlage liest, findet: Masse verfehlt (beide Varianten), ΔT verfehlt, Crash-Nachweis fehlt, Schnellladen LFP unprüfbar, Kosten ungesichert – und dann eine „Vorschlags"-Prioritätentabelle. Es fehlt ein Absatz, der zusammenfasst: *„Die Spezifikation wird im aktuellen Stand nicht erreicht. Die drei größten Lücken sind …, deren Schließung erfordert …, bevor eine Freigabe sinnvoll ist."* Ohne diesen Satz bleibt der Bericht eine Sammlung von Teilbereichen ohne konstruktives Urteil.

**Vorschlag:** Absatzeinleitung in Kapitel 2 oder am Ende der Zusammenfassung: „Gesamtbeurteilung (KI-Vorschlag, nicht freigegeben): Die Variante LFP verfehlt Masse und ΔT, NMC verfehlt Masse; Crash-Nachweis und LFP-Ladekurve fehlen. Eine Freigabe der Spezifikation ist mit dem vorliegenden Stand nicht möglich. Voraussetzung: [3 konkrete Schritte]."

---

## 8. REQ-P03 „erfüllt" – min/max-Spannung nicht ermittelt, NMC-Nennspannung fehlt

**Fundstelle (wörtlich):**
- REQ-P03, Status: *„erfüllt"*
- Dieselbe Zeile, Ergebnis: *„NMC Nennspannung in der Quelle **nicht ausgewiesen**; **min und max nicht ermittelt**"*

**Problem:** 800 V ist ein Betriebsfenster, kein Einzelwert. Ohne minimale und maximale Spannung (bei 0 %/100 % SOC, Extremtemperaturen, unter Last) kann ein Konstrukteur weder die Isolation auslegen noch die DC/DC-Grenzfrequenz bestimmen noch die Hochsicherheits-Überspannungsfestlegung (ECE R100) abschließen. „Reihenanzahl bekannt" ≠ „Systemspannung definiert."

**Vorschlag:** Status auf „offen – Zellenzahl gesetzt, Spannungsband (min/max) nicht berechnet". Ergänzung: „Nennspannung NMC = 217 × 3,6 V (Annahme, Datenblatt W…)" oder explizit: „Nennspannung fehlt; erst nach Messung der Zelle bestimmbar."

---

*Gutachter-Hinweis: Alle acht Punkte sind aus dem vorliegenden Text ablesbar; es wurden keine externen Zahlen eingeführt. Die Vorschläge betreffen die Darstellungslogik und Status-Deutlichkeit, nicht die korrigierende Berechnung.*
