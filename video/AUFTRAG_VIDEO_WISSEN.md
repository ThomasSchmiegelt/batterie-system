# Auftrag Sonnet: Zweites Abschlussvideo „Batterie und Wissensgraph“ (REQ-D13, BAT-DOC-13b)

KI-generiert (Claude Opus, 2026-11-23). Vorgabe des Autors (wörtlich): „ich hätte gerne ein zusätzliches video, prinzipiell so wie jetzt nur als hintergrund sollte man sehen wie der obsidian wissensgraph wächst, das gibt es als funktion in obsidian, das ist im hintergrund und baut sich langsam auf. wenn die batterie fertig ist wird das gesamte batteriegehäuse langsam transparent, am ende gibt es nur den wissensgraphen“

Das freigegebene Video `video/abschluss.mp4` und `video/szenen.py` bleiben unverändert. Wenn du etwas teilst, dann über einen Schalter (`VIDEO_VARIANTE=wissen`), der ohne Schalter dasselbe Ergebnis wie bisher liefert.

## Entscheidung Opus (delegiert): Graph wird nachgebaut, nicht aus Obsidian aufgenommen
Die Zeitrafferfunktion von Obsidian (Graph → „Animate“) ordnet die Notizen nach dem Erstellungszeitpunkt der Datei. `wissen/` wird bei jedem Lauf neu erzeugt, alle Dateien hätten denselben Zeitpunkt, und der Graph wäre sofort fertig. Deshalb baut ein Skript den Graphen im Obsidian-Stil nach (gleiche Notizen, gleiche Links) und ordnet ihn nach dem **echten Projektdatum** aus den Quellen. Im Begleittext steht das in einem Satz.

## Ausgaben
1. **`video/graph_zeitraffer.py`** (matplotlib oder Pillow, venv):
   - Knoten sind alle Notizen in `wissen/` außer `_bilder`. Kanten sind alle `[[…]]`-Links in Text und Frontmatter, wie im Obsidian-Graphen.
   - Datum je Knoten, in dieser Reihenfolge: `datum:` der Quellakte (ENT), Datum im Kopf von `BEFUNDE.md` (B-BAT), Datum der Ergebnisdatei bzw. Zeile in docs/08 (W), Erst-Commit in git (`git log --diff-filter=A --format=%ad --date=short -- <quelle> | tail -1`). Fehlt alles, gilt das Datum des Nachbarn mit dem kleinsten Datum. Innerhalb eines Tages geht es nach ID.
   - Die Zählung „Knoten je Quelle des Datums“ gibst du aus und schreibst sie als JSON neben die Bilder.
   - Layout: Kräfte-Layout einmal für den fertigen Graphen berechnen, mit festem Seed. Die Knoten erscheinen an ihrer Endposition, mit kurzem Einblenden und Aufwachsen. Kanten erscheinen, sobald beide Enden da sind.
   - Optik wie der Obsidian-Graph: dunkler Grund (#1e1e1e), Knoten als Punkte, Größe nach Grad, Farbe je Typ (Gruppen wie in Obsidian), dünne graue Kanten. Keine Beschriftung und kein Text im Bild.
   - Langsames Zoomen oder Drehen ist erlaubt. 1280×720, 25 fps, Einzelbilder nach `/home/cae/cae_projekte/batterie_video/wissen/graph/%04d.png`. Fertige Bilder werden übersprungen.
   - Zeitachse: Der Graph wächst vom ersten Bild bis zum Ende der Explosion/Rückführung (E3 in szenen.py) auf 100 %, danach steht er. Die Verteilung über die Zeit läuft nach Rang, nicht nach Kalendertagen, damit er gleichmäßig wächst.
2. **Batterie mit durchsichtigem Hintergrund:** `szenen.py` mit `VIDEO_VARIANTE=wissen`:
   - `film_transparent`, ohne Bodenplatte, RGBA-PNG nach `…/batterie_video/wissen/teile/`.
   - Nach E3 kommen etwa 16 s dazu: 6 s wird das Gehäuse (Wanne, Deckel, Rahmen und Struktur, also BT-5xx; prüfe die Zuordnung in `pm/bauteile/struktur.json`) langsam durchsichtig, Alpha 1 → 0,15. Danach 5 s, in denen alle Teile auf 0 ausblenden. Die letzten 5 s zeigen nur den Graphen.
   - Das Ausblenden geht über den Alpha-Wert des Materials. Die Einstellung für EEVEE (blend method oder render method je nach Blender-Version) stellst du im Test fest.
   - Die Kamera bleibt wie bisher. In der Schlussphase darf sie langsam zurückfahren.
3. **`video/erzeuge_video_wissen.sh`** mit `text|graph|render|zusammen|alles`, gebaut wie `erzeuge_video.sh`:
   - ffmpeg legt die Teile-Bilder über die Graph-Bilder (overlay).
   - Unten steht nur „Thomas Schmiegelt“, wie im ersten Video.
   - Ausgabe `video/abschluss_wissen.mp4`, H.264.
   - Vor dem Rendern `bash rechnen/gpu_warten.sh`. Losgelöst im Scope `hermes-batterie-video-wissen`, pausierbar.
   - Die Graph-Bilder sind CPU-Arbeit und dürfen parallel laufen.
4. **Begleittext** `video/begleittext_wissen.md`: Kopf BAT-DOC-13b, Entwurf. Erzeugt aus dem bestehenden Begleittext und ergänzt um einen Abschnitt zum Graphen mit Knoten- und Kantenzahl aus dem Skript.
5. Register in `docs/00` (BAT-DOC-13b) und eine Zeile in docs/08.

## Erwartung Opus
- **Graph:** etwa 600 Knoten. Kanten gibt es in der Größenordnung 2 000–6 000.
- **Datum:** Mehr als 70 % der Knoten bekommen ein Datum aus der Quelle selbst (ENT, B-BAT, W) oder aus git. Weil das Repo erst seit 2026-11-18 in git ist, häufen sich die git-Daten an diesem Tag. Steht der Anteil „git 2026-11-18“ über 40 %, meldest du das, denn dann wächst der Graph an dieser Stelle in einem Sprung.
- **Länge:** Das erste Video hat 2750 Bilder. Mit 400 Bildern Schluss sind es etwa 3150 Bilder, also 126 s.
- **Renderzeit:** Die Teile brauchen etwa so lange wie beim ersten Video. Der Graph braucht unter 1 s je Bild auf der CPU.
- Nenne die Renderzeit vor dem Rendern. Liegt sie über 2 h, geht es zurück an Opus.

## Prüfung
- Lege 8 Standbilder ins Scratchpad und sieh sie an: Anfang, 25 %, 50 %, Ende der Explosion, Gehäuse halb durchsichtig, Teile fast weg, nur Graph, letztes Bild.
- Prüfe dabei: Der Graph ist sichtbar hinter der Batterie, nichts ist abgeschnitten, und außer dem Namen steht kein Text im Bild.
- `abschluss.mp4` hat denselben Hash wie vorher.

## Abbruch
Zurück an Opus geht es,
- wenn das Alpha-Ausblenden in EEVEE nicht geht,
- wenn mehr als 40 % der Daten aus git 2026-11-18 stammen,
- wenn die Renderzeit über 2 h liegt.

Rückmeldung höchstens 6 Zeilen.
