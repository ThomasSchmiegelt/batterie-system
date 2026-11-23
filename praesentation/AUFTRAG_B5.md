# Auftrag Sonnet: Unternehmenspräsentation erzeugen (Vorgang B5, REQ-D14)

KI-generiert (Claude Opus, 2026-11-23). Anlass ist der Autor (2026-11-23): „bei dem ersten projekt haben wir noch die präsentation und das video vergessen“.
Plan: `praesentation/STORYBOARD.md`. Die Folien und Regeln dort gelten. Die Vorgaben B0 sind vom Autor nicht festgelegt, deshalb gelten die Vorschlagswerte, und auf der Titelfolie steht „Vorgaben Vorschlag KI“.

## Ausgaben
1. `python-pptx` in `.venv` installieren und in `docs/10` eintragen (Lizenz MIT, Version).
2. **Folienbausteine nachziehen:** Bausteine, deren Zahlen noch „leer“ oder „folgen“ sind (zum Beispiel X3, K5_parallel, G5_9), aktualisierst du aus den Ergebnisdateien. Die Zahlen liest ein Skript, du tippst keine ab.
   - Der Baustein `V_Modell.md` kommt aus `docs/06_verifikationsplan.md` (Zählung je Bewertung).
3. **`praesentation/erzeuge.py`** schreibt `praesentation/unternehmenspraesentation.pptx` (16:9, neutrale Vorlage, DE) mit 15 Folien und Anhang nach Storyboard. Dabei weicht es in drei Punkten ab:
   - Folie 9 „Sicherheit“ zeigt Crash X3 (Pfahl a/a2, Quetschung b bis 5 ms). X1/X2 kommen nur in den Anhang.
   - Folie 10 „Nachweisstand“ ist die V-Modell-Zählung aus docs/06, ehrlich mit „nicht definiert“.
   - Folie 3 nimmt Ziel und Ist aus `pm/anforderungen.json` und docs/06.
   - Jede Zahl liest das Skript aus der Quelldatei. In den Notizen jeder Folie stehen Sprechertext, Quellpfade und ENT-Verweise.
   - Fußzeile jeder Folie: „KI-generiert – Entwurf, nicht freigegeben | Thomas Schmiegelt | <Nr>“.
   - Bilder aus `bericht/bilder` oder den Rechenordnern, jedes mit Zielband (vorhandene Bilder verwenden).
4. PDF mit `soffice --headless --convert-to pdf`, danach jede Seite als PNG (pdftoppm, 60 dpi) ins Scratchpad. Prüfe jede Seite **ansehen**: kein Text über dem Rand, keine Überlappung, Bilder lesbar. Zu korrigieren ist das im Skript.
5. Englische Fassung nur als Schalter `--en`, nicht erzeugen.
6. Zeile in docs/08.

## Abbruch
Zurück an Opus geht jede Zahl ohne Quelldatei, jeder Widerspruch zwischen Baustein und Ergebnis und jede neue Kernaussage, die über den Baustein hinausgeht. Du deutest nichts.
Rückmeldung höchstens 6 Zeilen mit Pfad, Folienzahl und den Folien, die Mängel hatten.
