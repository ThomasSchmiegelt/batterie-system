| Dok.-Nr. | BAT-DOC-13c | Version | 0.1 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Drittes Video „Batterie, Nachverfolgung, Normen, Elektronik“: Begleittext (DE) | Ersteller | Claude Sonnet 5.5 (KI), Storyboard-Rohtext Kolibri 1 | Prüfer | – (Prüfung Opus offen) |

> **KI-generiert.** Video `video/elektronik_nachverfolgung.mp4` (165 s, 1280x720, 25 fps), gebaut von `video/erzeuge_video_elektronik.sh` aus vorhandenen Bildern (kein neuer Blender-Lauf). Zahlen nur aus `video/elektronik/daten.json`. Storyboard: `video/elektronik/STORYBOARD_kolibri.md`, Prüfung: `video/elektronik/pruefung_storyboard.txt`. Im Video steht nur der Name des Autors (Konstrukteur); dieser Text begleitet es. Entwurf, nicht freigegeben.

Vorgabe des Autors (2026-11-25): Das Video beginnt mit den Anforderungen, der Wissensgraph wächst, dann erscheinen Zelle, Pack und die Steuergeräte, am Ende verschwindet die Batterie und nur der Graph bleibt.

## Szene 1: Anforderungen und Normen (0 bis 25 s)
Tafel mit Nummer, Kurztitel, Wert und Status (`pm/anforderungen.json`). Hervorgehoben: REQ-P15 und REQ-P17 bis P21 (Elektronik). Danach die Normentafel aus `docs/07_normen_und_vorschriften.md`, grün „frei“, rot „kostenpflichtig“.

## Szene 2: Wissensgraph (über den ganzen Film)
Die Bildfolge des Graphen (`video/graph_zeitraffer.py`, Ordner `/home/cae/cae_projekte/batterie_video/wissen/graph/`) liegt als Hintergrund und wächst bis etwa 122 s weiter. Am Schluss bleibt er allein stehen.

## Szene 3: Zelle (25 bis 50 s)
LFP-Blade-Zelle (REQ-P06), Ladekurve, DCIR und Wärme aus `sim/chemie/c1_zellmodell`.

## Szene 4: Pack (50 bis 80 s)
Pack im Schnitt, Explosion, Gesamtansicht (`cad/pack/entwurf`). Bild-in-Bild: Kühlung K3/K4 (`sim/kuehlung/k3_gesamt/k3_vergleich.png`) und Crash Pfahl 5 kJ (`sim/mechanik/x3_crash_g5/energie_LFP_a.png`). Packmasse 619,85 kg (`cad/pack/entwurf/ergebnis_LFP_e2d_e3c.json`).

## Szene 5: Steuergeräte (80 bis 140 s)
- CMU-Platine, 4 Lagen, 110 Teile, DRC 0 (`sim/elektrik/e3_platine/ergebnis_platine.json`), Explosion nach Lagen, Nahaufnahme, Schaltplan Kanal.
- BMS-Platine, 134 Teile, DRC 0 (`sim/elektrik/e3c_bms_platine/ergebnis_platine.json`), rote HV/NV-Sperrzone, Schaltplanblatt.
- Rechnungen: SPICE Vorladung 912 V, SPICE Schütz Zener 37,11 V, Elmer-Wärme E3b, FMEDA (CMU LFP SG-01: SPFM 99,93 %, LFM 96,72 %, Ziel ASIL D 99 % und 90 %; `sim/elektrik/e3d_fmeda/ergebnis.json`).
- Nachverfolgung im Graphen: REQ-P18 → ENT-192 (vorgeschlagen) → BT-323 → FMEDA E3d und B-BAT-055; REQ-P19 → ENT-195 → BT-311; REQ-P15 → ENT-184 → BT-321. Danach die Sicherheitsziele SG-01 bis SG-08 mit ASIL (`docs/24_gefahrenanalyse_hara.md`).

## Szene 6: Batterie fertig (140 bis 165 s)
Zahlen auf einen Blick (Packmasse, Teile, DRC, SPFM), dann wird die Batterie durchsichtig, der Graph bleibt. Abspann: KI-generiert, Autor Konstrukteur.

## Integrationsgrenzen (ehrlich)
- Das Pack „baut sich auf“ als Bildfolge Schnitt, Explosion, Gesamtansicht aus vorhandenen PNG, nicht als neue 3D-Kamerafahrt. Neue Blender-Szenen (Deckel öffnet, CMU leuchten, CMU/BMS-3D-Kamerafahrt) sind nicht gerendert.
- Die Zelle erscheint als Einzelbild, nicht animiert. Die Szene „Batterie verschwindet“ ist ein Überblenden des Gesamtbilds.
- Bei den Nachverfolgungsketten ist der Graph per Raster vergrößert (unscharf); die Beschriftungen stehen links als Liste mit Linien zu den Knoten.
- Kolibri 1 lieferte in Lauf 1 nichts; Zahlen und Namen wurden gegen daten.json geprüft, 4 Fehler gestrichen (siehe pruefung_storyboard.txt).
- Das Dokument ist Entwurf; Freigabe durch den Autor offen.

---
KI-generiert (Claude Sonnet 5.5), BAT-DOC-13c, Entwurf, 2026-11-25.
