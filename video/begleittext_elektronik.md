| Dok.-Nr. | BAT-DOC-13c | Version | 0.2 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Drittes Video „Batterie, Nachverfolgung, Normen, Elektronik“: Begleittext (DE) | Ersteller | Claude Sonnet 5.5 (KI), Storyboard-Rohtext Kolibri 1 | Prüfer | – (Prüfung Opus offen) |

> **KI-generiert.** Video `video/elektronik_nachverfolgung.mp4` (165 s, 1280x720, 25 fps), gebaut von `video/erzeuge_video_elektronik.sh`; Szenen 4 und 5 (CMU, BMS) sind echte 3D-Szenen (Blender EEVEE, RGBA, `video/szenen_elektronik3d.py`), der Rest aus vorhandenen Bildern. Stand v1 (Bildfolge): `video/elektronik_nachverfolgung_v1.mp4`. Zahlen nur aus `video/elektronik/daten.json`. Storyboard: `video/elektronik/STORYBOARD_kolibri.md`, Prüfung: `video/elektronik/pruefung_storyboard.txt`. Im Video steht nur der Name des Autors (Konstrukteur); dieser Text begleitet es. Entwurf, nicht freigegeben.

Vorgabe des Autors (2026-11-25): Das Video beginnt mit den Anforderungen, der Wissensgraph wächst, dann erscheinen Zelle, Pack und die Steuergeräte, am Ende verschwindet die Batterie und nur der Graph bleibt.

## Szene 1: Anforderungen und Normen (0 bis 25 s)
Tafel mit Nummer, Kurztitel, Wert und Status (`pm/anforderungen.json`). Hervorgehoben: REQ-P15 und REQ-P17 bis P21 (Elektronik). Danach die Normentafel aus `docs/07_normen_und_vorschriften.md`, grün „frei“, rot „kostenpflichtig“.

## Szene 2: Wissensgraph (über den ganzen Film)
Die Bildfolge des Graphen (`video/graph_zeitraffer.py`, Ordner `/home/cae/cae_projekte/batterie_video/wissen/graph/`) liegt als Hintergrund und wächst bis etwa 122 s weiter. Am Schluss bleibt er allein stehen.

## Szene 3: Zelle (25 bis 50 s)
LFP-Blade-Zelle (REQ-P06), Ladekurve, DCIR und Wärme aus `sim/chemie/c1_zellmodell`. Bildunterschriften korrigiert (v2): Ladekurve LFP und NMC bis 80 % mit Zielzeit; DCIR im 10-s-Puls bei 10, 25, 40 °C; „Wärme je Zelle über der Zeit (LFP, Modell) mit Zielband“ (vorher fälschlich „Spreizung höchstens 5 K“, das Bild zeigt keine Spreizung).

## Szene 4: Pack baut sich auf, Deckel öffnet (50 bis 80 s), 3D
Neue Blender-Szene `pack`: Zellen in sechs Bändern, Rahmen, Kühlplatte, Verbinder, CMU (orange), Schaltbox mit Inhalt und HV-Leitungen erscheinen nacheinander, der Deckel schließt (17 bis 18 s) und klappt dann um die hintere Kante auf (22 bis 25,6 s), der Schaltboxdeckel hebt ab. Quelle: Pack-Netz `e2d_e3c` (`cad/pack`, FreeCAD-Tessellierung wie in E3). Bild-in-Bild Kühlung K3/K4 (`sim/kuehlung/k3_gesamt/k3_vergleich.png`) und Crash (`sim/mechanik/x3_crash_g5/energie_LFP_a.png`). Packmasse aus `cad/pack/entwurf/ergebnis_LFP_e2d_e3c.json`.

## Szene 5: Steuergeräte (80 bis 140 s)
- Szene 5 (80 bis 110 s, 3D, eine durchgehende Kamerafahrt, Szene `steuer`): vom ganzen Pack in die Endzone zur ersten CMU (hinten, y 30 bis 150 mm, hochkant an der Endwand), Explosion nach Lagen senkrecht zur Platine mit Vias als Kupferstäben (4 Lagen, 110 Teile, DRC 0; `sim/elektrik/e3_platine/ergebnis_platine.json`), dann zur Schaltbox an die BMS-Platine (134 Teile, DRC 0; `sim/elektrik/e3c_bms_platine/ergebnis_platine.json`, rote HV/NV-Sperrzone x = 100 bis 110 mm) mit Explosion; Umgebung wird durchsichtig. Lage aus dem Pack-STEP `e2d_e3c` (`cad/pack/pack_e2d.py`, CMU-Abbildung der Platinenachsen (Seite „vorn“ im Code = kleines x, Bauteile zum Packinneren); Lageprüfung im Blender-Log: Bounding Box Pack-Teil gegen Detailmodell 0,1 mm (CMU und BMS), Platinenkörper 0,1 mm; BMS-Ecke `bms_platine_bbox_mm` in `cad/pack/entwurf/ergebnis_LFP_e2d_e3c.json`). Schaltpläne als Einblendung.
- Rechnungen: SPICE Vorladung 912 V, SPICE Schütz Zener 37,11 V, Elmer-Wärme E3b, FMEDA (CMU LFP SG-01: SPFM 99,93 %, LFM 96,72 %, Ziel ASIL D 99 % und 90 %; `sim/elektrik/e3d_fmeda/ergebnis.json`).
- Nachverfolgung im Graphen: REQ-P18 → ENT-192 (vorgeschlagen) → BT-323 → FMEDA E3d und B-BAT-055; REQ-P19 → ENT-195 → BT-311; REQ-P15 → ENT-184 → BT-321. Danach die Sicherheitsziele SG-01 bis SG-08 mit ASIL (`docs/24_gefahrenanalyse_hara.md`).

## Szene 6: Batterie fertig (140 bis 165 s)
Zahlen auf einen Blick (Packmasse, Teile, DRC, SPFM), dann wird die Batterie durchsichtig, der Graph bleibt. Abspann: KI-generiert, Autor Konstrukteur.

## Integrationsgrenzen (ehrlich)
- Die 3D-Szenen sind Darstellung: Farben, Zeitplan, Kamerapfade, Lagenabstand 11 mm und überhöhte Kupferdicke 0,35 mm sind gewählt, keine Rechengröße. Die obere Kühlplatte ist durchsichtig (Alpha 0,22), sonst verdeckt sie Zellen und CMU. Zellen sind Hüllkörper aus dem Pack-Netz.
- CMU und BMS stehen am Einbauort im Pack-Koordinatensystem, die Kamera fährt ohne Schnitt. Beim Austausch der Pack-Platine gegen das Detailmodell (mit Leiterbahnen) springt das Bild kurz (CMU: Ausblenden des orangen Quaders, BMS: Austausch). Das Wärmeleitpad ist in der Explosion weggelassen (im Pack nicht modelliert).
- Via-Stabradius und Lagenabstand 11 mm sind Darstellung. Die rote Sperrzone stammt aus `bms_explosion_blender.py` (x = 100 bis 110 mm, ERGEBNIS E3c).
- Alpha-Überlagerung (Hashed) rauscht leicht (32 bis 48 Samples). Der Wissensgraph ist hinter dem Pack nur an den Rändern sichtbar.
- Auf der Platine in Bild 1 der Szene „Rechnungen“ und bei den Ketten gilt wie in v1: Graph per Raster vergrößert (unscharf).
- Kolibri 1 lieferte in Lauf 1 nichts; Zahlen und Namen wurden gegen daten.json geprüft, 4 Fehler gestrichen (siehe pruefung_storyboard.txt).
- Die Beschriftungen der Zellenbilder sind aus den Bildtiteln übernommen; daten.json enthält keine Bildunterschriften (offen, Opus).
- Das Dokument ist Entwurf; Freigabe durch den Autor offen.

---
KI-generiert (Claude Sonnet 5.5), BAT-DOC-13c, Entwurf, 2026-11-25.
