# AUFTRAG PI: Prüfbericht nach lauf_g5.sh (lokal, ollama)
KI-generiert (Claude Opus, 2026-11-20). Läuft automatisch am Ende von cad/baukasten/lauf_g5.sh.
Du darfst nur lesen und genau eine Datei schreiben: cad/baukasten/ausgabe/PI_BERICHT_G5.md. Keine anderen Dateien ändern, nichts löschen.
1. Lies cad/baukasten/ausgabe/lauf_g5.log und nenne jede Zeile mit "FEHLER" oder "Traceback".
2. Aus cad/baukasten/ausgabe/pruefung_LFP.txt und pruefung_NMC.txt: erste Zeile (Teile, Masse, Maße), Anzahl Fehler, Anzahl Zeilen mit "Kollision", die 10 größten Kollisionen (Wert in mm³).
3. Prüfe mit ls, ob es diese Bilder in bericht/bilder/ gibt und ob sie neuer als bericht/bericht.tex sind: g5_{LFP,NMC}_{gesamt,explosion,schnitt,ecke,schaltbox,kuehlkreis,draufsicht,kabelplan,bruecke}.png.
4. Aus bericht/bericht.log: Seitenzahl ("Output written"), Zeilen mit "! " (LaTeX-Fehler), fehlende Dateien ("not found").
5. Aus pm/kosten/ergebnis_LFP.json und ergebnis_NMC.json: Gesamtkosten und €/kWh.
Schreibe nur Zahlen mit Quelldatei, keine Deutung. Höchstens 40 Zeilen.
