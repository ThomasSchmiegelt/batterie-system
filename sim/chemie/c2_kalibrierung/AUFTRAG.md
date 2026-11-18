| Dok.-Nr. | Auftrag C2 | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Parametersätze kalibrieren (Blade an Test#5, 4680 an DCIR), Schnellladen neu | Ersteller | Claude Opus (KI) | Prüfer | Opus (Stichprobe) |

> KI-generiert, Opus → Sonnet. Methode und Erwartung: ERWARTUNG.md (nicht ändern). `.venv/bin/python`, PyBaMM 26.10, CPU, nice. Rohdaten nur lesen (`quellen/blade_datensatz/daten/`), Zwischendaten nach /home/cae/cae_projekte/batterie/c2/.
1. `daten_blade.py`: Test#5-xlsx einlesen (Struktur zuerst ansehen und in ERGEBNIS.md beschreiben), Pulse extrahieren (Strom, Spannung, T, SOC), 10-s-Widerstand je SOC/T → `blade_pulse.csv`, Bild `blade_widerstand.png`.
2. `parameter_<V>.py`: PyBaMM-Parametersätze nach Methode; nur Werte aus W20/W24/W28 (pruefe.py bestanden), Akten, Materialsatz; jede Abweichung als Annahme mit Herkunft in `eingaben.json`.
3. `kalibrieren.py`: Blade-Kalibrierung (a)–(c) mit scipy (wenige freie Parameter, ≤ 6), Gütemaß; dann 4680 an DCIR.
4. `schnellladen.py`: Läufe nach ERWARTUNG Punkt 4; Q(t) als Tabelle für K1-Wiederverwendung.
5. `ergebnis.json`, `ERGEBNIS.md` (Abgleich), Bilder `kalibrierung_blade.png` (Messung gg. Modell, mehrere SOC/T), `dcir_vergleich.png`, `schnellladen_4680.png` (Strom, Spannung, Anodenpotential, SOC; 30-min-Linie), `waerme_vergleich.png` (Modell gg. K1-Annahme); Lesehilfe; Baustein `praesentation/bausteine/C2.md`; bilder.py.
≤ 90 min. Rückgabe ≤ 5 Zeilen. → OPUS bei RMS > 30 mV oder fehlenden Daten.
