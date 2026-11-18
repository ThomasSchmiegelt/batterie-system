| Dok.-Nr. | Auftrag BILD-1 | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Zusatzgrafiken zum Variantenvergleich und Bildverzeichnis docs/14 | Ersteller | Claude Opus (KI) | Prüfer | Opus (jedes Bild ansehen) |

> **KI-generiert.** Auftrag von Opus an Sonnet (`sonnet-umsetzer`), 2026-11-17. Anlass: Autor: „kann man einige berechnungsergebnisse auch als bilder und grafiken dokumentieren?“ Regeln des Autors: auf jeder Grafik den **Zielbereich** (Band oder Linie, beschriftet, mit Herkunft; ist er nicht belegt: „Annahme“); zu jedem Bild eine **Lesehilfe** für Nicht-Fachleute (3–5 Sätze: was zeigen Achsen/Farben, worauf achten, Aussage).

## Teil 1: `sim/chemie/varianten_lfp_nmc/bilder_zusatz.py`
Liest nur `ergebnis.json` (beide Ordner `vergleich_lfp_nmc/` und `varianten_lfp_nmc/`), ändert keine Zahlen. Vorher `python3 varianten.py` nicht anfassen (läuft ein anderer Auftrag). Drei Bilder:
1. `bauraum.png`: nötige Pack-Energiedichte (Wh/L) gegen verfügbare, je Variante und Fall, Balken. Zielbereich: Linie „nötig“ je Fall; verfügbar als Balken, bei NMC als Band (Volumennutzung 40–60 %). Farbe grün = passt, rot = passt nicht, gelb = knapp (±2 %).
2. `empfindlichkeit.png`: Tornado-Diagramm Packmasse Fall B je Variante: Hub jeder Annahme (Massenanteil Verbrauch, Packfaktor k, Zellwert) als waagrechter Balken um den Mittelwert. Zielbereich: senkrechte Linie 30 % der Gesamtmasse (Annahme).
3. `kriterien.png`: Bewertungstabelle als Grafik (Zeilen: Masse A, Masse B, Bauraum A, Bauraum B, Zyklen, Zellzahl; Spalten LFP, NMC), Ampelfarbe aus den Urteilen in ergebnis.json („erfüllt/knapp/nicht erfüllt/unsicher“), Zahl in jeder Zelle. Keine Gewichtung, keine Gesamtnote.
Je Bild eine Lesehilfe in `bilder_lesehilfe.md`.

## Teil 2: Bildverzeichnis `pm/plan/bilder.py` → `docs/14_ergebnisbilder.md`
Sucht alle `*.png` unter `sim/` und `cad/`, je Bild: Überschrift (Ordner), Bild (relativer Link), Lesehilfe (aus `*lesehilfe*.md` im selben Ordner, Abschnitt zum Bildnamen, sonst „Lesehilfe fehlt“ – als Fehlerliste am Ende), Quelle (ergebnis.json-Pfad), Vorgang (aus Ordner: vergleich_lfp_nmc → C0, varianten_lfp_nmc → C0b, g1_anordnung → G1). Dokumentkopf (BAT-DOC-14, erzeugt, nicht von Hand bearbeiten). In `docs/00_dokumentenlenkung.md` eine Zeile für BAT-DOC-14 ergänzen.

## Abbruch und Rückgabe
Fertig, wenn Skripte fehlerfrei laufen und du jedes neue Bild selbst angesehen hast (Lesbarkeit, Überlappungen). Abbruch nach 30 min. Rückgabe ≤ 12 Zeilen: Bilder, was jedes zeigt, Auffälligkeiten. **→ OPUS**: Urteil in ergebnis.json fehlt oder widerspricht sich.
