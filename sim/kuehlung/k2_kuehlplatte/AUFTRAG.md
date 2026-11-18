| Dok.-Nr. | Auftrag K2 | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Kühlplatten: 1D-Hydraulik und Wärmeübergang, beide Varianten | Ersteller | Claude Opus (KI) | Prüfer | Opus (Stichprobe) |

> KI-generiert, Opus → Sonnet. Erwartung ERWARTUNG.md (nicht ändern). Sparsam.
1. `eingaben.json` (Herkunft je Wert), Plattenmaße aus `cad/pack/entwurf/parameter_<V>.json`.
2. `kuehlplatte.py`: Varianten Kanalbreite 10/15/20 mm, Führung quer/längs, ΔT_Kühlmittel 5/8/10 K → Durchfluss, Re, Nu/h (laminar entwickelnd, Gnielinski im Übergang), Druckverlust (Kanal + Umlenkungen/Verteiler pauschal 30 %, Annahme), Pumpenleistung. Auswahl: kleinster Druckverlust mit h ≥ 500.
3. `ergebnis.json`, `ERGEBNIS.md` (Abgleich), Bilder `durchfluss_druck.png` (Kennfeld mit Zielbändern), `platte_<V>.png` (Kanalbild Draufsicht), Lesehilfe, Baustein `praesentation/bausteine/K2.md`, bilder.py.
≤ 30 min, CPU. Rückgabe ≤ 4 Zeilen.
