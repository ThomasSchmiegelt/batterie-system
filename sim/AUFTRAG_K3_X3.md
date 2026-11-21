# AUFTRAG (Sonnet) K3/K4 Thermik bzw. X3 Crash – Einrichtung, nicht Dauerlauf
KI-generiert (Claude Opus, 2026-11-20). Je ein Agent pro Teil. Erwartung: sim/kuehlung/k3_gesamt/ERWARTUNG.md bzw. sim/mechanik/x3_crash_g5/ERWARTUNG.md. Lies sie zuerst.
**Was du tust:**
1. Skripte im jeweiligen Ordner: Geometrie/Netz aus G5 (cad/baukasten/ausgabe), Eingaben (eingaben.json mit Herkunft je Wert), Lauf, Auswertung (ergebnis.json), Bilder mit Zielband und Lesehilfe, Film (ffmpeg, mp4).
   - Thermik: FluidX3D-Vorlage /home/cae/fluidx3d_tauscher (eigene Kopie nach sim/kuehlung/k3_gesamt/fluidx3d/, nichts am Original ändern).
   - Crash: Vorlage sim/mechanik/x1b_knautschzone (kette.sh, neustart.sh, Werkstoffe).
2. Kurzer Probelauf (≤ 15 min, grobe Auflösung), um zu zeigen, dass die Kette läuft und anhaltbar ist: einmal `touch rechnen/STOP` testen, dann weiterlaufen lassen.
3. Den Dauerlauf NICHT selbst abwarten. Je Lauf eine Zeile in rechnen/schritte.txt anhängen: `ID | ja/nein (GPU) | bash sim/…/lauf.sh <fall>`. Der Lauf muss wiederaufsetzbar sein und $RECHNEN_STOP prüfen, siehe rechnen/LIESMICH.md. Danach je Rechnung einen Schritt „auswerten“ und als letzten Schritt `PI_<ID> | nein | bash rechnen/pi_pruefung.sh <ordner>`.
4. ERGEBNIS.md als Vorlage mit den Erwartungspunkten anlegen, die Zahlen bleiben leer. Die Auswertung füllt sie automatisch.
5. Folienbaustein praesentation/bausteine/K3.md bzw. X3.md (Bilder kommen später).
**Regeln:** Keine Änderung an cad/baukasten/. Jeder Zahlenwert hat eine Herkunft. Neue Annahmen nur benennen (Liste in der Rückgabe), keine Grenzwerte erfinden. GPU: nicht starten, solange ollama ein Modell geladen hat (`curl -s localhost:11434/api/ps`).
**Zurück an Opus:** Der Probelauf verfehlt die Größenordnung der Erwartung, oder ein Wert fehlt.
**Rückgabe:** ≤ 6 Zeilen.
