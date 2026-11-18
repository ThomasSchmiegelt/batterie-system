| Dok.-Nr. | Auftrag G2 | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Parametrische Zelle FreeCAD (beide Varianten), Entwurfslauf mit vorgeschlagenen Akten | Ersteller | Claude Opus (KI) | Prüfer | Opus (Modell und Bild) |

> **KI-generiert.** Auftrag von Opus an Sonnet (`sonnet-umsetzer`), 2026-11-17. Vorgang G2. Erwartung: `cad/zelle/ERWARTUNG.md`.

## Ziel
1. `cad/zelle/zelle.py` (FreeCAD-Python, headless über `$FREECAD_APPIMAGE` aus `umgebung.sh`, z. B. `freecadcmd`-Modus der AppImage; erst `--help` prüfen): `--variante LFP|NMC`, `--parameter <datei>` (Standard `pm/bauteile/parameter_<V>.json`). Liest BT-100 (Maße, Format), BT-120 (Wand). LFP: Quader mit Gehäuse als Hohlkörper (Wand), zwei Pole an den Stirnseiten. NMC: Zylinder mit Wand, Pol oben. **Polmaße und nicht belegte Details als benannte Konstanten `ANNAHME_*` oben im Skript**, im Bild als „Annahme“ beschriftet. Kein anderes Maß im Code.
2. **Entwurfslauf:** Die Akten ENT-014…029 sind nur „vorgeschlagen“ und stehen deshalb noch nicht in parameter_LFP.json. Erzeuge im Scratchpad eine Entwurfsparameterdatei (kleines Skript `cad/zelle/entwurf_parameter.py`: wie `pm.py parameter`, aber nimmt auch Status „vorgeschlagen“; schreibt nach `cad/zelle/entwurf/parameter_<V>_entwurf.json`, Kopf „ENTWURF, nicht freigegeben“). Damit beide Varianten bauen.
3. Ausgaben in `cad/zelle/entwurf/`: `zelle_<V>.FCStd`, `zelle_<V>.step`, `zelle_<V>.png` (isometrisch; Maßtext; Titel „Entwurf – Akten vorgeschlagen“), `ergebnis.json` (Außenmaße, Volumen, Wh/L aus Kapazität × Spannung / Volumen), `zelle_lesehilfe.md`, `ERGEBNIS.md` mit Abgleich ERWARTUNG Punkt für Punkt, Folienbaustein `praesentation/bausteine/G2.md` (Kernaussage „(Opus)“).
   PNG: falls FreeCAD headless nicht rendert, mit matplotlib aus der exportierten Geometrie (Eckpunkte/Tessellierung) zeichnen.
4. Nebenbei: `sim/chemie/varianten_lfp_nmc/erzeuge_bericht.py` soll eine vorhandene Kernaussage in `praesentation/bausteine/C0b.md` erhalten (nicht auf „(Opus)“ zurücksetzen). Danach `pm/plan/bilder.py`.

## Abbruch und Rückgabe
Fertig, wenn beide Varianten ohne Fehler bauen und die Bilder angesehen sind. Abbruch nach 45 min oder wenn FreeCAD headless nicht startet (dann Fehlermeldung zurück, nicht basteln). Nicht ändern: ENT-Akten, struktur.json, parameter*.json in pm/. Keine GPU. Rückgabe ≤ 12 Zeilen. **→ OPUS**: verfehlte Erwartung, fehlender Parameter.
