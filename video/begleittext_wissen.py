# KI-generiert (Claude Sonnet, 2026-11-23), Entwurf. Erzeugt video/begleittext_wissen.md aus video/begleittext.md und ergänzt einen Abschnitt zum Wissensgraphen (Zahlen aus .../wissen/graph/datenquellen.json).
import json, datetime
R = "/home/cae/hermes/batterie"; J = "/home/cae/cae_projekte/batterie_video/wissen/graph/datenquellen.json"
t = open(f"{R}/video/begleittext.md", encoding="utf-8").read(); j = json.load(open(J))
rest = t.split("\n## Szene 1", 1)[1]; rest = "\n## Szene 1" + rest.rsplit("\n---\nKI-generiert", 1)[0]
q = j["quelle"]; z = ", ".join(f"{k} {v}" for k, v in q.items())
o = ["| Dok.-Nr. | BAT-DOC-13b | Version | 0.1 | Status | Entwurf |", "|---|---|---|---|---|---|", "| Titel | Zweites Abschlussvideo „Batterie und Wissensgraph“: Begleittext (DE) | Ersteller | Claude Sonnet (KI) | Prüfer | – |", "",
     "> **KI-generiert.** Erzeugt von `video/begleittext_wissen.py` aus `video/begleittext.md` und `datenquellen.json` des Graphen (Stand " + datetime.date.today().isoformat() + "). Im Video steht nur der Name; dieser Text begleitet es. Entwurf, nicht freigegeben.", "",
     "Die Szenen 1 bis 8 sind dieselben wie im ersten Video (`video/abschluss.mp4`). Neu sind der durchsichtige Grund mit dem wachsenden Wissensgraphen dahinter und der Schluss (Abschnitt unten).", "", rest.strip("\n"), "",
     "## Wissensgraph im Hintergrund und Schluss (nur Variante „Batterie und Wissensgraph“)", "",
     f"- Der Graph zeigt alle Notizen des Obsidian-Tresors `wissen/` ohne `_bilder`: **{j['knoten']} Knoten** und **{j['kanten']} Kanten** (jeder `[[…]]`-Link in Text und Kopf). Quelle der Zahlen: `{J}`.",
     "- Er ist **nachgebaut, nicht aus Obsidian aufgenommen**: Die Zeitrafferfunktion von Obsidian ordnet nach dem Erstellungszeitpunkt der Datei, `wissen/` wird aber bei jedem Lauf neu erzeugt, alle Dateien hätten denselben Zeitpunkt. Deshalb ordnet ein Skript (`video/graph_zeitraffer.py`) die Knoten nach dem **echten Projektdatum** aus den Quellen.",
     f"- Datumsquellen (Knoten je Quelle): {z}. Entscheidungen: Datum der Akte; Befunde: Überschrift in `BEFUNDE.md` (sonst `git blame`); Recherchen: Datum der Ergebnisdatei; alle anderen: das frühere von Erst-Commit in git und dem frühesten Quelldatum der direkt verlinkten Nachbarn (Bauteil und Anforderung bekommen so das Datum ihrer ersten Akte).",
     f"- Ehrlicher Hinweis: Das Repo ist erst seit 2026-11-18 in git. {j['anteil_knoten_mit_datum_2026-11-18_prozent']} % der Knoten tragen das Datum 2026-11-18, git direkt allein {j['anteil_git_direkt_2026-11-18_prozent']} %. Die Verteilung über die Zeit im Video läuft nach Rang (Datum, dann ID), nicht nach Kalendertagen, damit der Graph gleichmäßig wächst.",
     "- Der Graph wächst vom ersten Bild bis zum Ende der Explosion/Rückführung (Bild 2680) auf 100 %. Danach folgen 16 s: 6 s wird das Gehäuse (BT-5xx und die oberen Abdeckungen BT-610 oben und BT-230 oben) durchsichtig (Alpha 1 auf 0,15), 5 s blenden alle Teile aus, 5 s zeigen nur den Graphen. Darstellungsentscheidung der KI, keine Auslegung.",
     "- Der Graph ist eine Darstellung der Ordnung der Akten, kein Rechenergebnis.", "", "---", "KI-generiert (Claude Sonnet). Entwurf, nicht freigegeben. Bildtext im Video nur: Thomas Schmiegelt."]
open(f"{R}/video/begleittext_wissen.md", "w", encoding="utf-8").write("\n".join(o) + "\n"); print("video/begleittext_wissen.md fertig")
