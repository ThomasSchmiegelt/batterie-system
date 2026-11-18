| Dok.-Nr. | Auftrag C1 | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | PyBaMM-Zellmodell LFP und NMC, Wärme und Widerstand | Ersteller | Claude Opus (KI) | Prüfer | Opus (Stichprobe) |

> KI-generiert, Opus → Sonnet. Erwartung ERWARTUNG.md (nicht ändern). `.venv/bin/python` (PyBaMM 26.10). Sparsam, CPU.
1. `eingaben.json` (Parametersatz, Skalierungsfaktor Fläche aus Akten via parameter_<V>.json, Herkunft).
2. `zellmodell.py`: SPMe oder DFN mit lumped thermal; Läufe: C/20-Kapazität; Schnellladen 10→80 % (LFP 2,1C, NMC 1,4C, CC-CV bis Ladeschluss), Wärme Q(t) (gesamt, irreversibel, reversibel); 10-s-Puls DCIR bei 50 % SOC und 10/25/40 °C.
3. `ergebnis.json` (Q(t) als Tabelle für K1-Wiederverwendung), `ERGEBNIS.md` (Abgleich), Bilder `waerme_<V>.png` (Q(t) gegen I²R-Annahme), `dcir.png`, `ladekurve.png`, Lesehilfe, Baustein `praesentation/bausteine/C1.md`, bilder.py.
≤ 45 min. Rückgabe ≤ 4 Zeilen.
