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
| ngspice 42 | BSD-3-Clause (laut Projekt, prüfen), Paket aus Ubuntu noble, nur intern | E3 |
| SKiDL 3.0.0, spicelib 1.6.4 | MIT (laut Projekt, prüfen) | E3 |
| KiCad 10.0.8 (Flatpak) | GPL-3, KiCad-Bibliotheken CC-BY-SA 4.0 mit Ausnahme (laut Projekt, prüfen); Footprints nur in der Platine verwendet, nicht ins Repo kopiert | E3 |
| Freerouting 2.5.0 (CLI) | GPL-3 (laut Projekt, prüfen), intern genutzt, nicht weitergegeben | E3, Routing-Versuch |
| networkx | BSD-3-Clause (laut Projekt, prüfen) | Wissensgraph pm/graph/graph.py |
| lxml | BSD-3-Clause (laut Projekt, prüfen) | ReqIF-Prüfung pm/graph/reqif.py; das OMG-XSD wird nur zur Prüfung in ein Temp-Verzeichnis geladen, nicht abgelegt |
| Blender | GPL | – |
| python-pptx 1.0.2 | MIT (pip show, 2026-11-23); Abhängigkeiten lxml, XlsxWriter, Pillow | Vorgang B5, erzeugt praesentation/unternehmenspraesentation.pptx; nur lokal installiert in .venv |

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
| Herstellerdatenblatt, https://www.farnell.com/datasheets/4551906.pdf (Abruf 2026-11-19) | Herstellerdatenblatt, nur intern, nicht im Repo | quellen/datenblaetter/BT-711_gigavac_GX14.pdf | G5.5b Maße Kaufteile |
| Herstellerdatenblatt, https://www.glvac.com/Public/Uploads/uploadfile/files/20241223pdf/GLFX250.pdf (Abruf 2026-11-19) | Herstellerdatenblatt, nur intern, nicht im Repo | quellen/datenblaetter/BT-711_glvac_GLFX250.pdf | G5.5b Maße Kaufteile |
| Herstellerdatenblatt, https://img.klsele.com/admin/product_upload/20210927113957HFE82V-250.pdf (Abruf 2026-11-19) | Herstellerdatenblatt, nur intern, nicht im Repo | quellen/datenblaetter/BT-711_hongfa_HFE82V-250.pdf | G5.5b Maße Kaufteile |
| Herstellerdatenblatt, https://cdn.shopify.com/s/files/1/0607/9699/3689/files/gv200.pdf (Abruf 2026-11-19) | Herstellerdatenblatt, nur intern, nicht im Repo | quellen/datenblaetter/BT-712_gigavac_GV200.pdf | G5.5b Maße Kaufteile |
| Herstellerdatenblatt, https://www.nijkerk-ne.com/wp-content/uploads/sensata-el-pyrofuse-datasheet.pdf (Abruf 2026-11-19) | Herstellerdatenblatt, nur intern, nicht im Repo | quellen/datenblaetter/BT-713_sensata_pyrofuse.pdf | G5.5b Maße Kaufteile |
| Herstellerdatenblatt, https://www.isabellenhuette.com/hubfs/Files/Data-sheets/IVT-S.pdf (Abruf 2026-11-19) | Herstellerdatenblatt, nur intern, nicht im Repo | quellen/datenblaetter/BT-340_isabellenhuette_IVT-S.pdf | G5.5b Maße Kaufteile |
| Herstellerdatenblatt, https://www.bender.de/fileadmin/content/Products/d/e/iso165Cx_D00154_D_XXEN.pdf (Abruf 2026-11-19) | Herstellerdatenblatt, nur intern, nicht im Repo | quellen/datenblaetter/BT-350_bender_iso165C.pdf | G5.5b Maße Kaufteile |
| Herstellerdatenblatt, https://dalroad.com/wp-content/uploads/2015/06/AMP-MSD.pdf (Abruf 2026-11-19) | Herstellerdatenblatt, nur intern, nicht im Repo | quellen/datenblaetter/BT-720_te_AMP-MSD.pdf | G5.5b Maße Kaufteile |
| Herstellerdatenblatt, https://dalroad.com/wp-content/uploads/2015/06/ENG_SS_108-94297_B1.pdf (Abruf 2026-11-19) | Herstellerdatenblatt, nur intern, nicht im Repo | quellen/datenblaetter/BT-730_te_HVP800_180.pdf | G5.5b Maße Kaufteile |
| Herstellerdatenblatt, https://dalroad.com/wp-content/uploads/2015/06/AMP-HVP-800.pdf (Abruf 2026-11-19) | Herstellerdatenblatt, nur intern, nicht im Repo | quellen/datenblaetter/BT-730_te_HVP800_katalog.pdf | G5.5b Maße Kaufteile |
| Herstellerdatenblatt, https://www.tti.com/content/dam/ttiinc/manufacturers/molex/Products/PDF/molex-mx150-datasheet.pdf (Abruf 2026-11-19) | Herstellerdatenblatt, nur intern, nicht im Repo | quellen/datenblaetter/BT-740_molex_MX150.pdf | G5.5b Maße Kaufteile |
| Herstellerdatenblatt, https://kr.gore.com/system/files/2024-08/gore-auto-batteries-snapfit-datasheet-us.pdf (Abruf 2026-11-19) | Herstellerdatenblatt, nur intern, nicht im Repo | quellen/datenblaetter/BT-570_gore_auto-batteries-snapfit.pdf | G5.5b Maße Kaufteile |
| Herstellerdatenblatt, https://vernay.com/wp-content/uploads/2025/06/2025_VernayVoltaVent-4pg_web.pdf (Abruf 2026-11-19) | Herstellerdatenblatt, nur intern, nicht im Repo | quellen/datenblaetter/BT-750_vernay_VoltaVent.pdf | G5.5b Maße Kaufteile |
| Herstellerdatenblatt, https://catalogue.pfisterer.com/de/300-013-260/Datasheet.pdf/ (Abruf 2026-11-19) | Herstellerdatenblatt, nur intern, nicht im Repo | quellen/datenblaetter/BT-590_pfisterer_300013260.pdf | G5.5b Maße Kaufteile |
| Herstellerdatenblatt, https://www.tecomotive.de/download/datasheets/CWA400_PWM_EN.pdf (Abruf 2026-11-19) | Herstellerdatenblatt, nur intern, nicht im Repo | quellen/datenblaetter/BT-661_pierburg_CWA400_PWM.pdf | G5.5b Maße Kaufteile |
| Herstellerdatenblatt, https://tecomotive.de/download/datasheets/CWA100-3_EN.pdf (Abruf 2026-11-19) | Herstellerdatenblatt, nur intern, nicht im Repo | quellen/datenblaetter/BT-661_pierburg_CWA100-3.pdf | G5.5b Maße Kaufteile |
| Herstellerdatenblatt, https://www.rheinmetall.com/Rheinmetall%20Group/brochure-download/Power-Systems/F0001e1124-PS-Coolant-Valves.pdf (Abruf 2026-11-19) | Herstellerdatenblatt, nur intern, nicht im Repo | quellen/datenblaetter/BT-663_pierburg_CoolantValves.pdf | G5.5b Maße Kaufteile |
| Herstellerdatenblatt, https://www.rheinmetall.com/Rheinmetall%20Group/brochure-download/Power-Systems/F0006e1124-PS-Electrical-Controlled-Thermostat.pdf (Abruf 2026-11-19) | Herstellerdatenblatt, nur intern, nicht im Repo | quellen/datenblaetter/BT-663_pierburg_3-2-Thermostat.pdf | G5.5b Maße Kaufteile |
| Herstellerdatenblatt, https://static.chipdip.ru/lib/939/DOC013939204.pdf (Abruf 2026-11-19) | Herstellerdatenblatt, nur intern, nicht im Repo | quellen/datenblaetter/BT-330_vishay_NTCS0603E3.pdf | G5.5b Maße Kaufteile |
| Herstellerdatenblatt, https://www.mikrocontroller.net/attachment/322106/30201-101674.pdf (Abruf 2026-11-19) | Herstellerdatenblatt, nur intern, nicht im Repo | quellen/datenblaetter/BT-712_vishay_RH050.pdf | G5.5b Maße Kaufteile |
| Herstellerdatenblatt, https://catalogue.pfisterer.com/en/300-010-010/Datasheet.pdf/ (Abruf 2026-11-19) | Herstellerdatenblatt, nur intern, nicht im Repo | quellen/datenblaetter/BT-590_pfisterer_300010010.pdf | G5.5b Maße Kaufteile |
| Herstellerdatenblatt, https://www.farnell.com/datasheets/3930084.pdf (Abruf 2026-11-19) | Herstellerdatenblatt, nur intern, nicht im Repo | quellen/datenblaetter/BT-770_amphenol_SGX_TRDU5.pdf | G5.5b Maße Kaufteile |
| Herstellerdatenblatt, https://sc.kyocera-avx.com/wp-content/uploads/Temperature-sensor_94082-1.pdf (Abruf 2026-11-19) | Herstellerdatenblatt, nur intern, nicht im Repo | quellen/datenblaetter/BT-640_kyocera-avx_94082.pdf | G5.5b Maße Kaufteile |
| Herstellerdatenblatt, https://www.dalroad.com/wp-content/uploads/2015/06/AMP_HVA_280.pdf (Abruf 2026-11-19) | Herstellerdatenblatt, nur intern, nicht im Repo | quellen/datenblaetter/BT-730_te_HVA280_katalog.pdf | G5.5b Maße Kaufteile |
| Herstellerdatenblatt, https://uploadcdn.oneyac.com/attachments/files/brand_pdf/teconnectivity/ENG_SS_108-32020_C.pdf (Abruf 2026-11-19) | Herstellerdatenblatt, nur intern, nicht im Repo | quellen/datenblaetter/BT-730_te_HVA280_spec108-32020.pdf | G5.5b Maße Kaufteile |
| Herstellerdatenblatt, https://cdn.promelec.ru/upload/grab/www.te.com/usa-en/product-1-2103124-1.datasheet.pdf (Abruf 2026-11-19) | Herstellerdatenblatt, nur intern, nicht im Repo | quellen/datenblaetter/BT-730_te_HVA280_header_1-2103124-1.pdf | G5.5b Maße Kaufteile |
| TRIZ-Widerspruchsmatrix 39×39 (Zellinhalte), https://github.com/seogineer/triz-solver, Datei skills/triz-analysis/data/contradiction-matrix.json v0.4.0 (Abruf 2026-11-24) | MIT laut GitHub-API; die Matrix selbst ist eine Tatsachentabelle nach Altschuller, Rechtslage der Abschrift nicht geprüft | pm/kreativ/triz_daten.json (nur Prinzipnummern, eigene deutsche Kurznamen, keine fremden Erläuterungen) | KR1 Kreativwerkzeug |
| TRIZ-Matrix Excel-Abschrift, https://github.com/arvindvenkatadri/triz_network, TRIZ_Matrix.xls (Abruf 2026-11-24) | ungeklärt, nur privat (keine Lizenzdatei) | nur zum Vergleich benutzt, nichts übernommen, Kopie nicht im Repo | KR1 Gegenprüfung der Matrix (Ergebnis in triz_daten.json, Feld gegenpruefung) |

---
*KI-generiert (Claude Opus, 2026-11-11). Status Entwurf. Freigabe nur durch den Autor.*

## Nachtrag 2026-11-24 (Opus): Normtexte vom Autor, Elektronik-Werkzeuge
| Quelle | Lizenz / Nutzung | Ablage |
|---|---|---|
| UN R100 Rev. 3, R94 Rev. 4, R95 Rev. 4, R135 (Grundtext 2015, Rev. 1 Amend. 1 und 2) (UNECE, PDF vom Autor) | frei veröffentlicht von UNECE; nur Auswertung und kurze Zitate im Repo | `quellen/normen/` (gitignore) |
| EU 2023/1542 (EUR-Lex, DE) | Weiterverwendung erlaubt (Beschluss 2011/833/EU) | `quellen/normen/` (gitignore) |
| ISO 26262, CISPR 25, IEC 60664-1, ISO 16750 | kostenpflichtig, liegen nicht vor (Autor 2026-11-24); Werte daraus bleiben Annahmen | – |
| COTRONIC, Fachartikel „Kriech- und Luftstrecken richtig auslegen“ (20.10.2025), vom Autor im Chat eingefügt | nur Methode genutzt, kein Text im Repo, kein Beleg | – |
