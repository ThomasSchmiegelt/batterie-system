# AUFTRAG DB2 (Sonnet): Datenblattwerte in die Geometrie
KI-generiert (Claude Opus, 2026-11-20). Autor: „Integriere zuerst die erkenntnisse aus den Datenblättern“. REQ-P13, REQ-P16.
**Ziel:** Jedes A_-Maß und jede A_-Masse eines Kaufteils, für die forschung/datenblaetter.md bzw. pm/bauteile/kaufteile_datenblatt.json einen Datenblattwert hat, wird durch diesen Wert ersetzt.
**Wohin:** NUR in die neue Datei cad/baukasten/annahmen_datenblatt.json, im selben Format wie annahmen_g5.json, mit Herkunft „Datenblatt <Datei> S. x (Wert im PDF-Text geprüft: ja/nein)“. kern.py und stueckliste_v3.py lesen diese Datei zuletzt.
annahmen_g5.json, annahmen.json und teile/*.py nicht ändern, dort arbeitet Opus gleichzeitig.
**Schritte:**
1. Eine Tabelle erstellen: Schlüssel A_… | alter Wert | Datenblattwert | Datei/Seite. Die Schlüssel findest du mit `grep -o 'a("A_[a-z0-9_]*' cad/baukasten/teile/kaufteile.py cad/baukasten/teile/schaltbox.py cad/baukasten/teile/elektronik.py`.
2. Jeden Wert mit `pdftotext -layout quellen/datenblaetter/<Datei>` im PDF nachsehen. Nur Werte, die im Text stehen. Hat ein Datenblatt nur eine Hüllmaß-Zeichnung als Bild, die Seite mit Read als Bild ansehen und „aus Zeichnung“ vermerken.
3. Bei Schützen und Sicherungen auch Bolzengröße und Bolzenabstand, wenn das Modell dafür einen Schlüssel hat.
4. Prüflauf: `source umgebung.sh; PACK_VARIANTE=LFP G5_STEP=0 G5_NUR=schaltbox,kaufteile,elektronik,normteile,verbinder $FREECAD_APPIMAGE freecadcmd cad/baukasten/montage.py`. Neue Kollisionen nur melden, nicht lösen.
5. Ausgabe: forschung/datenblaetter_eingearbeitet.md (die Tabelle, Kopf KI-generiert Sonnet). Eine Zeile für docs/08.
**Abbruch / zurück an Opus:** Ein Datenblattwert passt nicht zur Akte (z. B. Strom oder Spannung), oder ein Teil wird größer als 20 % und passt nicht mehr in die Schaltbox (Innenhöhe 66 mm).
**Rückgabe:** ≤ 5 Zeilen.
