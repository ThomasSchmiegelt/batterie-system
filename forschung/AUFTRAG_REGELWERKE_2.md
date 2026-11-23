# Auftrag Sonnet: Regelwerke, zweiter Teil

KI-generiert (Claude Opus, 2026-11-23). Folgt auf AUFTRAG_REGELWERKE.md.
Stand: W35 (9/1), W36 (20/0), W37 (8/0), W38 (3/0), W39 (7/0) und W42 (6/1) sind bestanden. Die Fehlerquote liegt überall unter 20 %, von Opus geprüft.
W40 hat ein leeres Paket (57 Byte, kein Ergebnis), W41 ebenfalls (45 Byte, 0 Belege).

1. **W40 und W41 reparieren.** Finde heraus, warum `paket.py`/`abruf.py` leer bleibt. Vermutungen: Beim eCFR wird der Redirect nicht verfolgt, bei OSTI wird der Text aus dem PDF nicht gezogen. Repariere das wie vorher, ohne Umgehung und ohne Änderung an Ort und Stelle. Dann `rm forschung/ergebnis/W40.* forschung/ergebnis/W41.* forschung/pakete/W40.md forschung/pakete/W41.md` und neu: `bash rechnen/gpu_warten.sh && bash forschung/lauf.sh wissen W40`, danach W41, losgelöst, Warten über einen Hintergrundbefehl.
2. **Vergleichstabelle** `docs/20_regelwerke_vergleich.md` (Kopf nach BAT-DOC-00, BAT-DOC-20, Entwurf):
   - Zeilen sind die Prüffälle: Schwingung, mechanischer Stoß, Quetschung, Pfahl/Seitenaufprall, Feuer, externer Kurzschluss, Überladung, Tiefentladung, Übertemperatur, thermische Ausbreitung/Warnung, Isolation, Elektrolytaustritt, Wasser/Eintauchen, Kennzeichnung/Batteriepass.
   - Spalten sind EU/UN (R100, R94/95/135, 2023/1542), USA zivil (FMVSS 305/305a), USA DoD (MIL) und China (GB 38031/GB/T 31467).
   - In eine Zelle kommt nur ein Wert mit bestandener Zitatprüfung, mit Kennung Wxx. Alles andere ist „nicht belegt“. **Nicht aus dem Gedächtnis füllen.**
   - Letzte Spalte: welche REQ betroffen ist (pm/anforderungen.json).
3. **`forschung/MANUELL_LADEN.md` ergänzen:** alles, was nach Schritt 1 und 2 noch fehlt, mit Einstiegslink. Die vorhandenen Zeilen bleiben stehen. Dazu gehören Zahlen, die für die REQ fehlen: Crush-Kraft R100 Annex 9D, Schwingungsspektrum Annex 9B, Warnzeit bei thermischer Ausbreitung.
4. Obsidian neu erzeugen (`python3 pm/plan/wissensnetz.py && python3 pm/plan/wissensnetz_obsidian.py`), tote Links 0.
5. Zeile in docs/08.

Abbruch: Zurück an Opus geht alles, was eine Deutung verlangt oder eine REQ ändern würde. Rückmeldung höchstens 6 Zeilen.
