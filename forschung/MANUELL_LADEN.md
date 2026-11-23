# Quellen zum Herunterladen von Hand (Autor)

KI-generiert (Claude Opus, 2026-11-23). Vorgabe des Autors: „die die fehlen, schreibe mir am ende als liste am besten mit link dann lade ich sie händisch“.
Ablage: `quellen/normen/` (in .gitignore, kommt nicht ins Repo). Danach nimmt `paket.py` die Datei als lokale Quelle.
Die Links sind Einstiegsseiten, die Opus aus dem Gedächtnis kennt. Die genaue PDF-Adresse ist nicht geprüft. Die Liste wird am Ende der Läufe W35–W42 ergänzt.

| Nr | Dokument | Einstieg | Suchbegriff / Hinweis | Dateiname |
|---|---|---|---|---|
| W35 | UN GTR Nr. 20 (Electric Vehicle Safety), Phase 1 und Änderung Phase 2 | https://unece.org/transport/standards/transport/vehicle-regulations-wp29/global-technical-regulations-gtrs | „GTR No. 20“ | GTR20.pdf |
| W42 | MIL-PRF-32565 (Rechargeable Battery, lithium) | https://quicksearch.dla.mil/ | Document ID „MIL-PRF-32565“, neueste Revision | MIL-PRF-32565.pdf |
| W42 | MIL-STD-810 (Environmental Engineering Considerations), Rev. H | https://quicksearch.dla.mil/ | „MIL-STD-810“ | MIL-STD-810H.pdf |
| W42 | MIL-STD-461 (EMV), Rev. G | https://quicksearch.dla.mil/ | „MIL-STD-461“ | MIL-STD-461G.pdf |
| W42 | NAVSEA S9310-AQ-SAF-010 (Navy Lithium Battery Safety) | über Suchmaschine, ob öffentlich verfügbar (ggf. „Distribution A“) | „S9310-AQ-SAF-010“ | S9310.pdf |
| W41 | EU JRC: Berichte zu Prüfnormen für Traktionsbatterien | https://publications.jrc.ec.europa.eu/repository/ | „electric vehicle battery safety standards“, „abuse test“ | JRC_*.pdf |
| W41 | NHTSA: Berichte zur Sicherheit von Fahrzeugbatterien | https://www.nhtsa.gov/research-data | „lithium-ion battery safety“, „thermal runaway“ | NHTSA_*.pdf |
| W38 | GB 38031-2025 (China, Pflichtnorm) | https://openstd.samr.gov.cn/ | „GB 38031“. Dort nur zum Lesen, ein Download ist oft gesperrt. Dann nichts laden, nur die Gliederung abschreiben. | – |

## Ergänzung 2026-11-23 (Sonnet, bereinigt nach Folgeauftrag)
Die R100-Annexe, Artikel der 2023/1542, Art. 2 der 2023/1230 und FMVSS 305a sind automatisch geholt (Teilthemen W35b–W35e, W37b, W37c, W40b), siehe `docs/20_regelwerke_vergleich.md`. Von Hand nötig bleibt nur (zusätzlich zu den Zeilen oben):

| Nr | Was fehlt | Zahl für REQ | Einstieg | Hinweis | Dateiname |
|---|---|---|---|---|---|
| W36 | R94, R95, R135 einzeln, um die Zahlen in W36 je Regelung zuzuordnen | REQ-P14 | unece.org war per curl 403 | Zuordnung nur von Hand über die UNECE-Seiten | R94.pdf, R95.pdf, R135.pdf |
