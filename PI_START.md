# Übergabe an PI (Kolibri 1 oder qwen), wenn Claude keine Token mehr hat

KI-generiert (Claude Opus, 2026-11-25). Du arbeitest im Batterieprojekt ~/hermes/batterie. Lies zuerst `CLAUDE.md` (Regeln), dann die obersten Einträge von `ERINNERUNGEN.md` (Stand) und `BEFUNDE.md`.

## Harte Regeln
1. Nichts erfinden. Jede Zahl mit Fundstelle (Datei, Akte ENT-NNN, Recherche W-Nummer). Ohne Beleg heißt der Wert **Annahme**.
2. Kein Maß im CAD ohne Akte: Akten mit `python3 pm/pm.py neu …` anlegen, Status „vorgeschlagen“. **„Entschieden“ und „freigegeben“ setzt nur der Autor.**
3. Erzeugte Dateien nicht von Hand bearbeiten (Liste in CLAUDE.md). Stattdessen die Quelle ändern und das Skript laufen lassen.
4. Vor jeder Änderung an geteilten Skripten (cad/pack/pack_e2d.py, sim/…/*.py) eine Sicherung anlegen oder `git commit`.
5. Vor GPU-Rechnungen `bash rechnen/gpu_warten.sh`. Lange Rechnungen losgelöst starten, nicht im Vordergrund warten.
6. Mitschreiben: eine Zeile in `docs/08_ki_einsatz_protokoll.md` (wer = „PI (Kolibri)“ bzw. „PI (qwen)“) und Beobachtungen über dich selbst in `docs/26_modelltest_kolibri.md`, Abschnitt 4.
7. Kleine Schritte und sofort speichern. Die Datei ist dein Gedächtnis.

## Offene Arbeiten (Stand 2026-11-25, Details in ERINNERUNGEN.md)
- **W1 Wächter:** `sim/elektrik/w1_kolibri_waechter/ERWARTUNG.md`, `rechnen/kolibri_waechter.py`. Ergebnis prüfen bzw. fortsetzen.
- **Video Elektronik:** `video/AUFTRAG_VIDEO_ELEKTRONIK.md`, Daten `video/elektronik/daten.json`.
- **Buch:** `~/hermes/buch/kapitel/entwurf_kolibri_14c_fortsetzung.md` (Regeln ~/hermes/buch/AGENTS.md).
- **SV1 Stecker/Verschraubung:** `sim/mechanik/sv1_stecker_verschraubung/ERWARTUNG.md` Nachtrag 1.
- **L2 Leichtbau** (REQ-P07: LFP ≤ 600, NMC ≤ 450 kg): `sim/mechanik/l1_leichtbau/ERWARTUNG.md` Nachtrag 1.
- **Bericht Kolibri:** `docs/26_modelltest_kolibri.md` fertigstellen, Daten aus `forschung/modelltest/monitoring.csv`.

## Am Ende jeder Sitzung
`ERINNERUNGEN.md` oben ergänzen (Datum, was erledigt, was offen), `python3 pm/pm.py pruefe`, `git add -A && git commit -m "…"`.
