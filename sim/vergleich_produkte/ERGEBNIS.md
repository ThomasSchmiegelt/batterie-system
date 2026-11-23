| Dok.-Nr. | BAT-DOC-22-V | Version | 0.1 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | QN2 Vergleich mit realen Batteriepacks | Ersteller | Claude Sonnet (KI) | Prüfer | – (Opus offen) |

> **KI-generiert.** Entwurf, nicht vom Menschen freigegeben.

Gehört zu `ERWARTUNG.md` (Opus), BAT-DOC-22, REQ-P02/P07. Skript: `auswerten.py`, Daten: `ergebnis.json`, Bild: `w43_vergleich.png`.

## Was getan
W43 (veröffentlichte Packdaten) und W44 (NASA-STD-7009) per Recherche gerechnet (`forschung/ergebnis/W43.md`, `W44.md`, Zitatprüfung `W43.pruefung.txt`: 15 bestätigt, 2 Fehler). Auswertung nur mit Zeilen mit bestandenem Zitat.

## Zahlen (alle aus `ergebnis.json`)
- Produktangaben Energie (Wikipedia, Fahrzeugangabe): Seal 61,4 und 82,5; Han 76,9; Model Y 60–81; Lucid Air 88–118; ID.3 (China) 57,3 kWh. Spanne 57,3–118 kWh. Ausgeschlossen (Zitat fehlt): Tesla Model 3.
- Unsere Packs: LFP 73,92 kWh, NMC 74,27 kWh (`pm/bauteile/stueckliste_*.json`). Beide liegen in der Produktspanne und im Warnband ±40 %.
- Unsere Dichten (nur eigene Werte, ohne Vergleich): LFP 117,9 Wh/kg und 89,0 Wh/l, NMC 152,7 Wh/kg und 100,3 Wh/l (Masse Stückliste, Volumen Hüllquader aus CAD).

## Nicht möglich (offene Frage an Opus)
- **Kein Wh/kg- und Wh/l-Vergleich:** W43 enthält mit bestandener Zitatprüfung weder Packmasse noch Packmaße. Die Erwartung (Streudiagramm Wh/kg über Wh/l, Spanne 140–160 und 150–180 Wh/kg) ist damit nicht prüfbar, und das Bild zeigt statt dessen den Energieinhalt. Der einzige Massewert (Seal, Leergewicht des Fahrzeugs) ist ausgeschlossen (Zitat fehlt) und ohnehin keine Packmasse. Vorschlag: W43b mit Quellen, die Packmasse nennen (Opus entscheidet über Quellen; keine Werte aus dem Gedächtnis).
- Die Werte sind Fahrzeugangaben, brutto/netto unklar; Chemie nur beim Seal (LFP) und ID.3 (NMC) im Zitat belegt. Eine Trennung LFP/NMC gibt die Spanne daher nicht her.
- Rundzellen-Packs mit 4680 kamen in W43 nicht vor (Wikipedia-Seite `Tesla_4680_battery` 404, kein Ersatz gesucht).
- Kategorie V: Q8 Stufe 1 (nur Energie, Größenordnung), Q7 und Q10 bleiben 0.

## W44 NASA-STD-7009
Seite `https://standards.nasa.gov/standard/NASA/NASA-STD-7009` erreichbar (HTTP 200), Paket nur 1579 Zeichen (Landeseite). Belegt: Version B (2024), Schlagworte u. a. credibility, sensitivity analysis, uncertainty, validation, verification. **Nicht belegt:** ob die Norm frei herunterladbar ist, und die Gliederung der Glaubwürdigkeitsbewertung (Stufen). Offene Frage: Dokument-PDF müsste von Hand geladen werden (Autor), Ablage in `quellen/`.

## Prüfung
Siehe `ERWARTUNG.md`, Abschnitt Prüfung (Sonnet, Opus-Prüfung offen).

---
*KI-generiert (Claude Sonnet, 2026-11-23). Status Entwurf.*
