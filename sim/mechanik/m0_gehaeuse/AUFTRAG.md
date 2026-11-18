| Dok.-Nr. | Auftrag M0 | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Gehäuse-Vorauslegung beide Varianten | Ersteller | Claude Opus (KI) | Prüfer | Opus (Stichprobe) |

> KI-generiert. Opus → Sonnet, 2026-11-17. Erwartung `ERWARTUNG.md` (nicht ändern). Sparsam arbeiten.
1. `eingaben.json` aus ERWARTUNG (Herkunft je Wert), Zellmaße aus `cad/zelle/entwurf/parameter_<V>_entwurf.json`, Zellzahl/Anordnung aus `sim/geometrie/g1_anordnung/` (Funktionen wiederverwenden).
2. `gehaeuse.py`: Höhenstapel je Variante, Länge mit 3 Querträgern, Seitenrahmenbreite aus fester Breite, NMC-Plätze mit Querträgern (Sechseck- oder Rechteckraster wie G1), Masse Querträger/Rahmen/Platten (Dichte Al 2700, Annahme). `ergebnis.json`, `ERGEBNIS.md` mit Abgleich Punkt für Punkt.
3. Bilder (Zielband, Lesehilfe `m0_lesehilfe.md`): `draufsicht_<V>.png` (Zellfeld, Querträger, Rahmen, Maße), `schnitt_<V>.png` (Höhenstapel mit Maßen, Grenze 130 mm).
4. `praesentation/bausteine/M0.md`, `pm/plan/bilder.py` laufen lassen.
Abbruch 30 min, CPU. Nicht ändern: Akten, Erwartung. Rückgabe ≤ 5 Zeilen. → OPUS bei verfehlter Erwartung.
