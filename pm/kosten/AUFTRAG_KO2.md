# AUFTRAG SL3.1 + KO2 (Sonnet)

KI-generiert (Claude Opus, 2026-11-19). Autor: „pass bitte auch die stückliste an und die Preisgestaltung“. Erwartung: pm/kosten/ERWARTUNG.md Nachtrag 2 (ERW-KO2). REQ-P16.

## SL3.1 Stückliste (pm/bauteile/stueckliste_v3.py, nicht cad/baukasten anfassen)
1. Neue Felder je Kaufteil: `hersteller_typ`, `datenblatt` (Datei in quellen/datenblaetter/, Seite), `masse_quelle` „Datenblatt“, wo das Datenblatt eine Masse nennt. Quelle: forschung/datenblaetter.md und cad/baukasten/annahmen_g5.json (gewählte Typen: GLVAC GLFX250, Gigavac GV200, Sensata STPS500, Eaton EKC14-40, Isabellenhütte IVT-S, Gore AVS 70, Vernay VoltaVent, Amphenol SGX TRDU5, Kyocera AVX 94082, Vishay NTCS0603E3, Vishay RH050, Pfisterer 300 013 260/300 010 010, Pierburg CWA100-3). Ohne Datenblatt bleibt es bei „Schätzung“.
2. Kühlplatte BT-610 jetzt Blech 1/4/1 mit Mäander (ENT-152…156): Benennung, Werkstoff, Masse bis G5.7 aus K2b (46,6 kg LFP; NMC aus ergebnis_k2b.json), masse_quelle „K2b (bis G5-CAD)“. Kühlkreis 660.1–660.5: Massen aus annahmen_g5.json (A_g5_*_masse_kg), Schläuche „G5-CAD (folgt)“.
3. Neues Feld je Position `preis`: {wert, einheit, status, herkunft} nach den Preisregeln in ERW-KO2 (Quelle der Werte: pm/kosten/eingaben.json, die du dafür anpasst, siehe KO2). Die Stückliste zeigt den Preis an, sie rechnet ihn nicht selbst.
4. docs/13_stueckliste*.md neu erzeugen, mit Spalten Hersteller/Typ, Masse, Masse-Quelle, Preis, Preis-Status.

## KO2 Kosten (pm/kosten/)
1. eingaben.json nach ERW-KO2 Punkt 1–7 ändern (neue Einträge BT-450, 580, 590 je Art, 661–665; BT-610 ohne Faktor 0,6; BT-713 44,04; f_serie als eigener Eintrag mit Herkunft; je Eintrag status in den 3 Stufen). Alte Werte nicht löschen, sondern als `wert_ko1` stehen lassen.
2. kosten.py für SL3 lauffähig (Positionen statt fehlende_bt; Stückzahl × €/Stück, Masse × €/kg, Länge × €/m, sonst „offen“). Ergebnis ergebnis_<V>.json, Bilder kosten_<V>.png und kosten_vergleich.png mit Zielband und Lesehilfe (Regel: Ergebnisse als Bild), docs/18 neu (doku.py).
3. ERGEBNIS: Abschnitt „KO2“ in pm/kosten/ERGEBNIS.md (anlegen, falls es fehlt), Punkt für Punkt gegen ERW-KO2.
4. Ein Befehl für den Neulauf nach der Gesamtmontage: `python3 pm/bauteile/stueckliste_v3.py --aus-cad && python3 pm/kosten/kosten.py && python3 pm/kosten/bilder.py && python3 pm/kosten/doku.py`. In ERGEBNIS.md notieren.
5. Folienbaustein praesentation/bausteine/KO2.md.
Abbruch/Rückgabe an Opus: Erwartung verfehlt, Widerspruch Stückliste ↔ Akte, neue Preisannahme nötig (keine eigenen Preise erfinden). Rückgabe ≤ 6 Zeilen.
