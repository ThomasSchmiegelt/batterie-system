# AUFTRAG G5.8 (Sonnet): Renders der G5-Modelle, Bilder im Bericht tauschen

KI-generiert (Claude Opus, 2026-11-19). Autor: „schau mal ob du die Modelle noch rendern kannst und im bericht austauschen“. REQ-D12, Regel „Ergebnisse als Bild“.

## Eingang
- cad/baukasten/ausgabe/pack_<V>.FCStd. Objekte sind nach BT gruppiert, das Label ist der Teilname. LFP ist aktuell. **NMC zuerst neu montieren:** `source umgebung.sh; PACK_VARIANTE=NMC G5_STEP=0 $FREECAD_APPIMAGE freecadcmd cad/baukasten/montage.py` (≈ 6 min, im Hintergrund).
- Farben und Rauheit: cad/baukasten/farben.json (Werkstoff → Farbe). Den Werkstoff je Teil gibt ergebnis_<V>.json.
- Vorlage für Stil und Kamera: cad/pack/render_pack.py (Blender, Cycles CPU) und label_e2d.py (Beschriftung).

## Aufgabe
1. `cad/baukasten/render_g5_export.py` (freecadcmd): Liest das FCStd und schreibt je BT ein Netz (STL oder OBJ, Toleranz 0,3 mm) mit Farbe nach `cad/baukasten/ausgabe/netz/<V>/`. Dazu eine Indexdatei mit BT, Werkstoff, Farbe und Bounding Box.
2. `cad/baukasten/render_g5.py` (Blender -b, Cycles CPU, Samples per Umgebungsvariable, Standard 32). Ansichten je Variante:
   - gesamt
   - explosion: Stufen nach z-Lage der BT; Kühlkreis BT-661…665 nach hinten versetzt
   - schnitt: Viertelschnitt mit Mäander-Kühlplatte, Pad und Zelle
   - ecke: Rückwand mit Verteiler, Laschen und Fühler
   - schaltbox: Deckel ausgeblendet
   - kuehlkreis: Pumpe, Ventil, Chiller, Schläuche
   Ausgabe nach `cad/baukasten/bilder/g5_<V>_<ansicht>.png`.
3. Beschriftung wie label_e2d.py: BT-Nummern an den Hauptteilen und eine Lesehilfe-Zeile unten (was man sieht, Maße L × B × H aus ergebnis_<V>.json).
4. Bericht bericht/bericht.tex:
   - Die g4_pack_*-Bilder (Zeilen um 620–640) und eventuelle e2/e2d-Packbilder durch die g5-Bilder ersetzen. Die neuen Bilder nach bericht/bilder/ kopieren.
   - Bildunterschriften an G5 anpassen: Blech-Kühlplatte mit Mäander, Verteiler außen, Kühlkreis hinten, Maße und Massen aus ergebnis_<V>.json.
   - Version 0.5 im Kopf (3 Stellen).
   - pdflatex zweimal, 0 Fehler. Danach docs/14 (Bildverzeichnis) nachführen.
5. Folienbaustein praesentation/bausteine/G5.md (1 Satz, Bild, Zahlen mit Quellpfad).

## Regeln
- Keine Änderung an cad/baukasten/teile/, kern.py, montage.py und den Annahmen.
- Bilder selbst ansehen (Read). Teile müssen erkennbar sein, kein schwarzes Bild, Zielband/Lesehilfe lesbar.
- Abbruch: Wenn Blender länger als 20 min je Bild braucht, Samples halbieren. Wenn der NMC-Lauf scheitert, LFP fertig machen und NMC melden.
- Rückgabe ≤ 5 Zeilen: Bilder (Pfade), Bericht-PDF-Seitenzahl, Probleme.
