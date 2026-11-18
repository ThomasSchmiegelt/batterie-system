| Dok.-Nr. | Auftrag C0 | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Chemievergleich LFP/NMC: Skript, Bild, Ergebnis, Folienbaustein | Ersteller | Claude Opus (KI) | Prüfer | Opus (Rohdaten) |

> **KI-generiert.** Auftrag von Opus an Sonnet (`sonnet-umsetzer`), 2026-11-16. Vorgang C0 (neu), REQ-P01/P02/P06/P07/P10.

## Ziel
Ein Skript rechnet aus `eingaben.json` den Vergleich LFP gegen NMC für die Fälle A und B. **Nur die Zahlen aus `eingaben.json` verwenden, keine eigenen Werte einführen.** Fehlt etwas, Abbruch und Meldung an Opus.

## Eingang
`sim/chemie/vergleich_lfp_nmc/eingaben.json`, `ERWARTUNG.md` (nur lesen, nicht ändern).

## Rechenweg (genau so umsetzen)
Für jede Chemie c, jeden Fall f ∈ {A, B}, jeden Zellwert w aus dem Band [unten, Mitte, oben] und jeden Packfaktor k aus [band unten, wert, band oben]:
1. Verbrauch V(m) = V_ref · (1 + a · (m − m_ref) / m_ref), mit a = `massenanteil_verbrauch`. Fall A: m = 1500 fest, also V = V_ref.
2. E_netto = Reichweite · V / 100 [kWh]. E_brutto = E_netto / (1 − reserve).
3. Packmasse m_pack = E_brutto · 1000 / (w · k) [kg].
4. Fall B: m = 1500 + m_pack. Schritte 1–3 wiederholen, bis sich m_pack um < 0,1 kg ändert. Höchstens 50 Schritte, sonst Fehler „konvergiert nicht“. Schrittzahl ausgeben.
5. Zellen in Reihe s = ceil(U_sys / U_zelle). Nur Spannung, Kapazität je Zelle ist unbekannt.
6. Zyklenbedarf = km_leben / Reichweite · sicherheit_zyklen. Vergleich mit dem Zyklenband: „erfüllt“ (unten ≥ Bedarf), „unsicher“ (Band umfasst Bedarf), „nicht erfüllt“ (oben < Bedarf).
7. Nötige Pack-Energiedichte Wh/L = E_brutto · 1000 / (L·B·H·1000). Vergleich mit `zelle_Wh_L`: Bei `null` steht „offen (keine Quelle)“. Bei NMC Band nennen, Hinweis „Zelle, nicht Pack; allgemein Li-Ion“.
8. Batterieanteil = m_pack / Gesamtmasse (A: /1500, B: /(1500+m_pack)), gegen `grenze_batterieanteil`.
9. Empfindlichkeit: Packmasse bei a ∈ band (nur Fall B), bei k ∈ band, bei w ∈ band. Welche Annahme bewegt die Packmasse am stärksten?

## Ausgabe (alle in `sim/chemie/vergleich_lfp_nmc/`)
- `vergleich.py` (KI-generiert-Kopf, nur numpy/matplotlib/json; Laufzeit Sekunden, deshalb ohne Scope).
- `ergebnis.json`: alle Zahlen je Chemie/Fall/Bandpunkt, dazu Iterationsschritte.
- `packmasse.png`: Packmasse LFP und NMC, Fälle A und B, Balken = Mitte, Fehlerbalken = Spanne über w und k. **Grenze** als waagrechte, beschriftete Linie „30 % der Gesamtmasse (Annahme)“, für A bei 450 kg, für B je Balken (aus Rechnung). Titelzahlen aus `ergebnis.json` formatiert, nicht hart eingetragen. Darunter oder als Datei `packmasse_lesehilfe.md`: Lesehilfe für Nicht-Fachleute (3–5 Sätze).
- `ERGEBNIS.md`: Dokumentkopf (Ersteller Sonnet, Prüfer Opus, Entwurf, KI-generiert in Kopf und Fußzeile). Tabelle je Chemie und Fall, Empfindlichkeit, **Abgleich mit ERWARTUNG.md Punkt für Punkt** (erfüllt / verfehlt, mit Zahl). Keine Empfehlung, keine Deutung. Die schreibt Opus.
- `ERGEBNIS_kurz.txt` (≤ 15 Zeilen): Kernzahlen und Abgleich mit der Erwartung.
- `praesentation/bausteine/C0.md`: Kernaussage als Platzhalter „(Opus)“, Bild `sim/chemie/vergleich_lfp_nmc/packmasse.png`, Zahlen mit Quellpfad `ergebnis.json`.

## Abbruch und Rückgabe
- Fertig, wenn alle Dateien existieren und `python3 vergleich.py` fehlerfrei läuft. Abbruch nach 30 min.
- **→ OPUS**: verfehlte Erwartung, fehlende Eingabe, Konvergenzproblem.
