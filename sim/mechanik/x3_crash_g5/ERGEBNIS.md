# ERGEBNIS X3 – Crash Batteriepack G5 (Vorlage + Probelauf)
| Dok. | ERG-X3 | Version 0.1 | Entwurf | Ersteller Claude Sonnet (KI-generiert) | Prüfer Opus (offen) |
> **KI-generiert (Claude Sonnet, 2026-11-21), Entwurf, ungeprüft.** Zahlen kommen aus `ergebnis.json` (Schlüssel `<Fall>`), von `auswerten.py` gefüllt. Leer = Dauerlauf noch nicht gerechnet.

## Stand
Kette: `x3.py` (Deck) → `lauf.sh` (OpenCourant, 10 Abschnitte, Restart, `$RECHNEN_STOP` + `/STOP` in X3_000k.ctl) → `auswerten.sh` (Zahlen, Bilder, Film). Warteschlange: X3_LFP_a, X3_LFP_a_AUSW, PI_X3.
**Probelauf** (grob, 25 ms, 12 min, 6 CPU): `ergebnis.json`/`LFP_a_probe25`: Energiebilanzfehler 0,57 %, Pfahl-Eindringung 14,9 mm (Pfahl prallt ab, Kraft max 393 kN), Zellblock-Vorderseite 26 mm (Animation). Nur Funktionsnachweis, grobes Netz, Platzhalter-Zellwerkstoff.

**LFP_a (erster Dauerlauf): ungültig (Nachtrag 3).** Modellfehler, Zellreihen gleiten frei (ERWARTUNG.md Nachtrag 3). Rohdaten: `lauf/LFP_a_ungueltig_N3`, Bilder/Film `*_LFP_a_ungueltig_N3.*`, Zahlen in `ergebnis.json` Schlüssel `LFP_a_ungueltig_N3`. Keine Zahl daraus verwenden. Neuer Lauf mit 4 Blöcken folgt.

## Erwartungspunkte (ERWARTUNG.md) – Dauerlauf LFP_a, Auswertung füllt
| Nr | Erwartung | Ist (ergebnis.json) | erfüllt |
|---|---|---|---|
| 1 | Energiebilanzfehler < 5 % | | |
| 2a | Pfahl-Eindringung 40–70 mm (Grenze 20–100) | | |
| 2b | Erste Zellreihe 10–40 mm eingedrückt | | |
| 3 | (b) Quetschung 100 kN: Rahmen < 10 mm, Zellen < 2 mm | nicht gebaut (offen) | |
| 4 | Rechenzeit LFP (a) 1–4 h | | |

## Nachtrag 1 umgesetzt (2026-11-21)
Lagerung nur 12 Hülsen (UFS-Ende), a2 = 20 kJ, a_s10/a_s40 (Zellfließgrenze), b = 3 Halbzylinder R75, Abstand 30, masselose Wand mit 1 mm/ms (Annahme Sonnet, Weggeber; Auswertung bei 100 kN), NMC = 4 homogene Blöcke × Füllgrad 0,782 (eingaben.json NMC.zellbloecke). Erwartungsband a 25–60, a2 50–120 mm. Probe b/a (grob, abgebrochen wegen CPU-Last durch Dauerlauf): Kraft springt schon bei < 1 mm Weg auf ~105 kN (Kontaktstoß, dynamisch), Aussage erst nach Dauerlauf. Energiebilanz bei b nicht anwendbar (Weggeber).

## Offene Fragen / Annahmen (an Opus)
1. Zellblock-Werkstoff: ERWARTUNG sagt „wie X1“, X1 hat keinen. Platzhalter E 1 GPa, Fließgrenze 20 MPa, nu 0,3 (`eingaben.json`, markiert). Ergebnis hängt stark daran.
2. Lastfall (b): Größe und Lage der Platte nach ECE R100 Anh. 8D fehlen im Projekt; nicht gebaut. NMC: Rundzellen-Geometrie nicht umgesetzt (x3.py bricht ab).
3. Kühlplatten-Mittelebenen z = 14/112 mm (Annahme), Gegenseite (Außenwand y = B) voll eingespannt, UFS-Hülsen als Vierkant 20×20, Pad/Zwischenlage nicht modelliert (Reihenspalt 1 mm).
4. Kontakt: nur Zellknoten gegen Schalen (Solid-Fläche /SURF/PART liefert Fehler 1104), kein Zell-Selbstkontakt; Netz im Dauerlauf HN 12 / HF 40 / HY 20 / NZ 6.
5. Probe zeigt Abprallen bei 15 mm: Rahmen+Zellen sehr steif oder Einspannung zu hart; Dauerlauf-Netz abwarten, dann Deutung durch Opus.
