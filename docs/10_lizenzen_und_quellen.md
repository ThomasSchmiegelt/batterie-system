| Dok.-Nr. | BAT-DOC-10 | Version | 0.1 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Lizenzen und Quellen | Ersteller | Claude Opus (KI) | Prüfer | – (Mensch offen) |

> **KI-generiert.** Entwurf, nicht vom Menschen freigegeben. Testprojekt „KI im Engineering“, kein Produkt.

## Software
| Paket | Lizenz | Hinweis |
|---|---|---|
| PyBaMM | BSD-3-Clause (laut Projekt, prüfen) | Parametersätze mit Literaturzitat angeben |
| FreeCAD | LGPL-2.0+ (prüfen) | – |
| ElmerFEM | GPL/LGPL (prüfen) | – |
| FluidX3D | eigene Lizenz, nicht MIT | geänderte Quellen veröffentlichen, Referenzen zitieren |
| gmsh | GPL (prüfen) | – |
| Blender | GPL | – |

## Fremdquellen
Patentschriften, Seiten, PDFs: nur lokal (`quellen/`, `forschung/*_ablage/`), nie ins Repo. Zitate kurz und wörtlich mit URL.

## Quellen außerhalb des Repos (Ergänzung 2026-11-16, KI-generiert)
| Quelle | Lizenz | Ablage | Verwendung |
|---|---|---|---|
| techscience.com FHMT 29043 (314-Ah-LFP, thermisch), W18 | Verlag, OA (Lizenz im PDF prüfen) | forschung/pakete/W18.md (Auszug) | Kennwerte mit Zitat, keine Texte im Repo |
| drpress HSET 3 (2022) „Feasibility of BYD blade batteries“, W19 | OA (Lizenz prüfen) | forschung/pakete/W19.md | Hinweise, Sekundärquelle |
| Borealis doi:10.5683/SP3/RPCWBY, Pulsdatensatz BYD Blade 135 Ah | CC-BY 4.0 (Namensnennung) | quellen/blade_datensatz/0_readme.txt; Daten (Test#5 252 MB, SOP_summary, Protokolle) in /home/cae/cae_projekte/batterie/blade_datensatz/, Link quellen/blade_datensatz/daten; Download 2026-11-17 | später C2/C3 Eichung |
| Cell Rep. Phys. Sci. 2025, doi:10.1016/j.xcrp.2025.102453 | CC-BY | nicht abrufbar | – |
| OpenCourant (Fortsetzung von OpenRadioss), Release latest-20261011 (Commit cb760c2), github.com/OpenCourant/OpenCourant | AGPLv3; intern genutzt, nicht weitergegeben (Auftrag X1b/X2, vom Autor freigegeben) | /home/cae/cae_projekte/werkzeuge/opencourant/ (Binärpaket OpenCourant_linux64.zip, SHA256 6cb419677ca36d73acb96218cc0cf5e4f7d50494d9c7812ba27935e3c0f8ec94 = GitHub-Digest des Assets); Rauchtest-Deck qa-tests/miniqa/SMOKE_TEST (Download 2026-11-18, liegt nur im Werkzeugordner) | X2 dynamischer Pfahl |

---
*KI-generiert (Claude Opus, 2026-11-11). Status Entwurf. Freigabe nur durch den Autor.*
