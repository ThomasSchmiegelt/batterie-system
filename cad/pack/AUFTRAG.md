| Dok.-Nr. | Auftrag G4 | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Pack-CAD LFP und NMC (FreeCAD, Entwurf) mit Render | Ersteller | Claude Opus (KI) | Prüfer | Opus (Stichprobe) |

> KI-generiert, Opus → Sonnet, 2026-11-17. Erwartung ERWARTUNG.md (nicht ändern). Sparsam; Rückgabe ≤ 5 Zeilen.
1. `entwurf_parameter.py` wie `cad/zelle/entwurf_parameter.py`: Maße aus allen Akten (entschieden + vorgeschlagen) je Variante → `entwurf/parameter_<V>.json`; fehlende Maße (Deckel, Boden, Unterfahrschutz, Trägerhöhe, Vergusshöhe) aus `sim/mechanik/m0_gehaeuse/eingaben.json` als `A_*`-Annahmen.
2. `pack.py` (freecadcmd, Parameter per Umgebungsvariable): Wanne, Deckel, Seitenrahmen, 3 Querträger (54 × 26 × 2,5 Hohlprofil), Kühlplatten oben/unten, Unterfahrschutz; Zellen als vereinfachte Körper (Zelle aus cad/zelle als Hülle, nicht Detail); LFP Zellverbinder 25 × 3; NMC Träger, Verguss bis halbe Höhe (Annahme), Gruppenverbinder 25 × 3, Zellabgriffe 12 × 1, Pad. Kollisionsprüfung (paarweise Schnittvolumen benachbarter Teile = 0), Massen, Schwerpunkt → `entwurf/ergebnis_<V>.json`. FCStd + STEP.
3. Bilder: Explosion und Viertelschnitt je Variante (Blender CPU wie cad/zelle/render_detail.py oder FreeCAD-Ansicht), Massenbalken mit Zielband aus C0b, Lesehilfe `pack_lesehilfe.md`, `ERGEBNIS.md` mit Abgleich, Baustein `praesentation/bausteine/G4.md`, bilder.py.
≤ 60 min, CPU.
