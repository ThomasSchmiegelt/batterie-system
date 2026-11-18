| Dok.-Nr. | Auftrag B1-a | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Projektbericht Batteriesystem, Fassung 0.1 (DE), Zwischenstand | Ersteller | Claude Opus (KI) | Prüfer | Opus (Inhalt, Zahlen), Mensch (Freigabe) |

> **KI-generiert.** Auftrag von Opus an Sonnet (`sonnet-umsetzer`), 2026-11-17. Autor: „fange auch an den bericht zu schreiben“. Vorgang B1 (vorgezogen als Zwischenstand), BAT-DOC-17.

## Form
- `bericht/bericht.tex` (LaTeX, pdflatex), Stil wie `~/hermes/fusion/bericht/projektbericht/ki_im_maschinenbau.tex`: Makros `\lesehilfe{…}` und `\bild{…}` von dort übernehmen (Präambel lesen), Begriffskasten „Begriffe in diesem Abschnitt“ am Anfang von Kapiteln mit neuen Fachwörtern. Kopf: Dokumentnummer BAT-DOC-17, Version 0.1, Status Entwurf, „KI-generiert (Claude Opus/Sonnet)“, Autor Thomas Schmiegelt. Fußzeile KI-generiert.
- Bilder: nach `bericht/bilder/` **kopieren** (nicht verlinken) mit Quellpfad im Bildtext. Zu **jedem** Bild eine Lesehilfe für Nicht-Fachleute (aus den `*lesehilfe*.md`, sprachlich glätten). Zielbereich im Bild erwähnen.
- **Jede Zahl** aus einer Ergebnisdatei (`ergebnis.json`, Akten, BEFUNDE) mit Fundstelle als Fußnote oder Klammer (Pfad bzw. ENT-/B-BAT-Nummer, Recherche W-Nummer). Keine eigene Rechnung, keine neue Zahl. Annahmen als „Annahme“ kennzeichnen. Status der Akten nennen (entschieden durch den Autor / vorgeschlagen).
- Sprache: klar, kurze Sätze, Ingenieur als Leser, kein Werbeton.

## Gliederung (Vorgabe Opus) und Kernaussagen
1. **Zusammenfassung** (½ Seite): zwei Varianten LFP-Blade und NMC-4680 bei gleicher Spezifikation; NMC ein Drittel leichter (411 gegen 616 kg, Fall A), LFP langlebiger und sicherer; Bauraum 1950 × 1430 × 130 mm; Stand: Zellen als Detail-CAD, Wärmesimulation läuft. Platzhalter für K0-Ergebnis.
2. **Auftrag und Vorgaben**: Fahrzeug 1500 kg (Anhaltswert, Fall A mit / Fall B ohne Batterie), 400 km, 800 V (ENT-006), Bauraum (ENT-013, ENT-030), Kühlplatte unten (ENT-081), Ziele 45 °C / 5 K (REQ-P09), zwei Varianten (Autor 16.11.). Tabelle Lastenheft REQ-P01…P10 mit Stand (aus docs/01).
3. **Vorgehen mit KI-Agenten**: Rollen (Mensch, Opus, Sonnet, Haiku, PI lokal, Maschine), Akten ENT → parameter.json → CAD, Erwartung vor jeder Rechnung, Zitatprüfung der Recherche (pruefe.py), Freigabe nur durch den Menschen. Zahlen aus docs/08 (Anzahl Aufträge je Agent). Kurz.
4. **Recherche und Datenlage**: R4 (gesperrte Werte, z. B. W06-Spaltenfehler), W18 (thermische Kennwerte), W19 (Volumennutzung 60 %, schwache Quelle), W20 Zerlegungsstudie (Tabelle der gemessenen Zellwerte beider Zellen). Quelle: forschung/R4_ergebnis.md, BEFUNDE B-BAT-005…009.
5. **Chemie: von der Annahme zur Messung**: C0 (Herstellerwerte, „kein belegter Massenunterschied“) → C0b (Messwerte: NMC ein Drittel leichter). Bilder packmasse (beide), kriterien, empfindlichkeit. Deutungen aus DEUTUNG.md beider Ordner. Ehrlich: die erste Empfehlung hielt nicht.
6. **Systemauslegung**: 800 V, 250s×1p (LFP) bzw. 217s×4p (NMC), Zellkapazität abgeleitet, Bauraumprüfung G1 (Lauf 1–3: 1900 → 1950 → 1430 mm Breite, warum). Bilder anordnung, bauraum.
7. **Zelle: Maße, Innenaufbau, CAD**: Akten ENT-014…080 (Status vorgeschlagen), Tabelle Innenaufbau beider Zellen (aus cad/zelle/aufbau_W20.json), Bilder: Vergleichsrender, LFP-Schnitt, LFP-Explosion, 4680-Viertelschnitt, -Draufsicht. Hinweis: 4680-Bilder werden nach Korrektur des Wickelkerns (ENT-074, B-BAT-016) ersetzt – aktuellen Stand in `cad/zelle/entwurf/detail/` verwenden.
8. **Wärme der Einzelzelle (K0)**: Abschnitt anlegen mit Methode aus sim/kuehlung/k0_zelle/AUFTRAG.md und eingaben.json; Ergebnisse als Platzhalter „folgt“ (K0 läuft). Nicht erfinden.
9. **Fehler und Korrekturen**: Tabelle aus BEFUNDE: NMC-Wahl aus unbelegter 180-Wh/L-Annahme; W06 LFP/NMC-Spalte vertauscht (PI); W19 „332 Wh/kg“ trotz bestandener Zitatprüfung gesperrt; W20 DOI statt Datei; Zelllänge 660 → 681 mm (Endzone); Wickelkern 14 → 12,5 mm; stueckliste.py falscher JSON-Pfad. Je Zeile: wer fand es, wie, Folge. Das ist ein Kernkapitel für „KI im Engineering“.
10. **Entscheidungen**: Tabelle aller Akten mit Status (aus docs/04_entscheidungen.md, gekürzt: gemeinsame, LFP, NMC).
11. **Offene Punkte und nächste Schritte**: Freigaben ENT-014…080, Polmaße/Fahnen-Lesart, K0-Ergebnis, Kühlplatte BT-610, Verschaltung G3, Pack G4, Zellmodell C1–C3 (PyBaMM, Blade-Pulsdatensatz), Crash, Bericht EN.
Anhang: Begriffe (Glossar), Quellen (W-Nummern mit URL aus forschung/themen_*.tsv, Zerlegungsstudie mit DOI und CC-BY), Software (SOFTWARE.md, Versionen FreeCAD 1.1.4, Blender 4.0.2, Elmer).

## Ausgabe und Abbruch
`bericht/bericht.tex`, `bericht/bilder/`, `bericht/bericht.pdf` (zweimal kompilieren, 0 Fehler, Warnungen nennen). Register `docs/00_dokumentenlenkung.md`: Zeile BAT-DOC-17. Abbruch 60 min. Nicht ändern: Ergebnisdateien, Akten. Keine GPU. PDF-Seiten stichprobenartig als Bild ansehen (pdftoppm). Rückgabe ≤ 12 Zeilen: Seitenzahl, Kapitel mit Platzhaltern, Zahlen ohne Fundstelle (sollten 0 sein), Auffälligkeiten.
