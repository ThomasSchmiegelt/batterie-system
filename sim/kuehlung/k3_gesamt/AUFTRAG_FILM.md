# AUFTRAG K3-Film (Sonnet): Durchströmung der Kühlplatte als Video
KI-generiert (Claude Opus, 2026-11-21). Autor: „ich würde die durchströmung gerne als video haben“. Regel: Ergebnisse als Bild/Film mit Lesehilfe.
**Was:** Ein eigener FluidX3D-Fall `film` in deiner Kopie sim/kuehlung/k3_gesamt/fluidx3d/ (nicht am Original).
- Geometrie: Ausschnitt der Mäanderplatte mit 2 Bahnen (je 8 Teilkanäle), einer Umlenkkammer und dem Eintritt aus der Eintrittskammer. Wenn der GPU-Speicher reicht, die ganze Plattenbreite über ≥ 400 mm Länge mit beiden Umlenkungen am hinteren Ende.
- Rechnung: Re 200, 4 Zellen/mm, Pr_sim 1, wie die bestätigte Bahnprobe. Start aus der Ruhe, damit der Film das Füllen zeigt, dann stationär.
- Darstellung mit `#define GRAPHICS` (Bilder auf die Platte, kein X11):
  (a) Draufsicht in Kanalmitte, Geschwindigkeitsbetrag farbig (gleiche Farbskala im ganzen Film, Farbbalken), dazu Stromlinien bzw. Partikel, wenn FluidX3D das kann.
  (b) Gleiche Ansicht, Fluidtemperatur bei beheizter Wand.
- Je 1 Bild alle N Schritte, ≈ 20 s Film bei 30 fps.
- Beschriftung je Bild mit PIL: Titel, Lesehilfe-Zeile (Strömung, Re im Film 200 statt 760 im Betrieb und warum, Totzonen in den Ecken der Umlenkung), KI-Kasten, Zeit in ms.
- ffmpeg H.264: k3_durchstroemung_geschwindigkeit.mp4 und k3_durchstroemung_temperatur.mp4, dazu je ein Standbild (png) für den Bericht.
- Hinweis aus K3-Nachtrag 2: Die Umlenkränder lieferten nur 52 % des Flusses. Im Film den Einlass als Geschwindigkeitsrand weit vor der Umlenkung setzen (Vorlauf ≥ 10 Kanalhöhen), damit der Fluss stimmt. Den Durchfluss im Film prüfen und auf dem Standbild angeben (Soll ± 5 %).
**Warteschlange:** Den Lauf nicht selbst lange abwarten. Eine Probe ≤ 5 min ist erlaubt, nur wenn ollama nichts geladen hat. Dann als Schritt `K3_FILM | ja | bash sim/kuehlung/k3_gesamt/lauf.sh film` direkt nach K3_AUSW in rechnen/schritte.txt einfügen. Die übrigen Zeilen nicht anfassen. Der Lauf prüft $RECHNEN_STOP je Bildabschnitt.
**Bericht:** Standbilder als Abbildung im K-Kapitel, Verweis auf die mp4-Dateien. praesentation/bausteine/K3.md um die Filme ergänzen.
**Rückgabe:** ≤ 4 Zeilen.
