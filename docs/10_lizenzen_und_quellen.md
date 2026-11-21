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

---
*KI-generiert (Claude Opus, 2026-11-11). Status Entwurf. Freigabe nur durch den Autor.*
