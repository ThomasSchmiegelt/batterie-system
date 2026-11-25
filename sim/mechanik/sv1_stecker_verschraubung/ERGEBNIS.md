| Dok.-Nr. | ERG-SV1 | Version | 0.3 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Ergebnis SV1: Stecker mit Gegenstück, Steckfreigang, Verschraubungen im Pack-CAD (Fortsetzung Nachtrag 2) | Ersteller | Claude Sonnet (KI) | Prüfer | Opus (offen) |

> **KI-generiert** (Claude Sonnet, 2026-11-25). Entwurf, nicht freigegeben. Grundlage `ERWARTUNG.md` (ERW-SV1, Nachtrag 2, Punkte 1–5, nicht geändert). Version 0.1 (2026-11-24) ist in `/tmp/claude-1003/SV1b/sv1dir/ERGEBNIS.md` gesichert. Zahlen aus `ergebnis_v02.json` (Auszug aus `/home/cae/cae_projekte/batterie/sv1b/out/ergebnis_<V>_e2d_e3c_sv1.json`, Gruppierung `…_gruppen.json`) und aus den DRC-/Router-Dateien unter `/home/cae/cae_projekte/batterie/sv1b/lauf*_*/` (`drc.json`, `fr.log`, `start.txt`, `ende.txt`). Alle Maße der Stecker sind Annahmen ERW-SV1 (`cad/pack/entwurf/annahmen_sv1.json`). Bohrungslagen B3/B4v: Annahme W1 (`sim/elektrik/w1_kolibri_waechter/ERGEBNIS.md`), von Opus als Annahme ERW-SV1 N2 übernommen.

## Version 0.3 (Nachtrag 3, 2026-11-25 11:08 bis 11:40): Entscheidungen Opus umgesetzt
Quellen: `sim/elektrik`-Arbeitskopie `/home/cae/cae_projekte/batterie/sv1b/e3w/` (DRC-Dateien `cmu_<V>_drc.json`, `drc_vor_thermo_<V>.json`, `thermovias_<V>.json`), `sv1b/lauf2_B4/` (Router, `drc.json`), `ergebnis_v03.json` (Pack). **Zusammenfassung: Pack-Teile 2 und 3 erledigt (Zahlen unten); Punkt 1 (Platine) bis auf 3 Thermovias erreicht, Abnahme DRC 0 formal verfehlt, daher nichts nach `e3/` oder `abgabe_2026-11-24/` kopiert (Rückfrage an Opus).**

**Punkt 1: B4, Ecken (2,8|2,8), mit Projektdatei und Daisy-Klasse (`sv1b/lauf2.sh B4 200`, danach `nach.sh`, `nach_nmc.sh`).**
| Schritt | LFP | NMC | Quelle |
|---|---|---|---|
| Router (Pass 18, offen / Verstöße) | 3 / 46 (Handbahn-Nets, siehe Punkt 2a) | durch Übertragung | `lauf2_B4/fr.log` |
| KiCad-DRC nach SES-Import | 0 offen, 2 Bahnbreitenverstöße (0,12 mm) | – | `lauf2_B4/drc.json` |
| nach `via_aufraeumen` (0 Vias entfernt, 2 Bahnen verbreitert) | **0 Verstöße, 0 offen** | **0 Verstöße, 0 offen** (Übertragung: 36 Werte geändert) | `e3w/drc_vor_thermo_<V>.json` |
| Thermovias gesetzt | **144 von 144**, davon 3 als kleine Via 0,45/0,2 mm | 144 von 144, davon 3 klein | `e3w/thermovias_<V>.json` |
| KiCad-DRC danach | **6 Verstöße** (3 × Via-Durchmesser 0,45 < 0,5, 3 × Bohrung < 0,3), 0 offen | 6 (gleiche Arten), 0 offen | `e3w/cmu_<V>_drc.json` |
| zur Information (Kopie, nicht übernommen): Projekt mit Mindest-Via 0,4 / Mindestbohrung 0,2 | 0 Verstöße, 0 offen | 0 Verstöße, 0 offen | `sv1b/test_via/drc.json`, `sv1b/test_via_nmc/drc.json` |
- Die drei kleinen Vias liegen im Netz **T5** bei (53,0 | 13,00), (53,7 | 13,00), (57,7 | 13,00) mm. Die Router-Läufe sind deterministisch (`lauf2_B4`, `lauf3_B4_t3`, `lauf3_B4_t8`: gleiche Punktzahl 973,68, SES-Dateien byte-gleich), eine Wiederholung ändert nichts.
- Die E3-Ausnahme (Opus, Frage 9: Via 0,45/0,2 mm mit Mindest-Via 0,4 und Mindestbohrung 0,2) galt nach E3-ERGEBNIS nur für NMC und steckt in den jetzigen `e3/*.kicad_pro` nicht (beide haben Mindest-Via 0,5 / Bohrung 0,3). **Entscheidung Opus:** Ausnahme auch für LFP (und beide Projektdateien) setzen, dann ist die Abnahme erfüllt; oder anderes Routing. Ich habe die Regel nicht gelockert.
- Hilfsskripte angepasst in Arbeitskopie `sv1b/skripte/` (Pfade auf `e3w`, `route_uebertragen.py` überspringt die Bohrungs-Footprints MH1–MH4, Fehler `KeyError 'MH2'`; `thermovias.py` schreibt die JSON nach `e3w`). Originale unverändert.
- Akten BT-321: ENT-209 `befestigung` (4 × M3, Bolzen 6 mm), ENT-210 `bohrung_d_mm` 3,2, ENT-211 `bohrung_anzahl` 4, Status vorgeschlagen, Abnahme in der Akte als offen vermerkt. `pm.py pruefe`: 211 Entscheidungen, 0 Fehler.
- Das CMU-STEP im Pack ist weiter das alte ohne Bohrungen (`e3/cmu_<V>.step` unverändert); neue STEP mit Bohrungen und Thermovias liegen nur in `sv1b/e3w/cmu_<V>.step` (Prüfung `kicad-cli`: Export ohne Fehler), nicht als `cmu_<V>_mit_bohrungen.step` in der Abgabe.

**Punkt 2: Freigangsregel Platinenstecker (FPC, Daisy): Steckerlänge + Steckweg 8 + 5 mm, quer 2 mm** (Annahme Opus ERW-SV1 N3; ich habe „Steckweg + 5 mm“ ab der Steckerbasis gezählt, wie in v0.1 die 25 mm, also Länge + Steckweg + 5 mm). Außenstecker unverändert (+25 mm, Handraum Ø 75). Neuzählung (`ergebnis_v03.json`, Pack mit `PACK_SV1=1`, Ausgabe nur `_sv1`):
| Klasse | LFP v0.2 → v0.3 | NMC v0.2 → v0.3 |
|---|---|---|
| Gesamt | 211 → **71** | 215 → **117** |
| B Freigang gegen Nachbarstecker auf der CMU | 20 → 0 | 20 → 0 |
| C Platinenstecker gegen festes Teil | 162 → 42 | 169 → 91 |
| D BMS gegen Nachbarstecker | 2 → 2 | 2 → 2 |
| E BMS gegen Schaltbox | 6 → 6 | 6 → 6 |
| F Deckelstecker | 18 → 18 | 18 → 18 |
| G Schütz-Spulenstecker | 3 → 3 | 0 → 0 |
- **Rest in Klasse C LFP (42):** alle gegen den Seitenrahmen (je 14 für FPC, Daisy-In, Daisy-Out), Überlappung je 280–304 mm³; der Freigang reicht bis x 2021, der Seitenrahmen beginnt bei x 2020 (Überlappung **1 mm** in Querrichtung zur Wand, Beispiel CMU 00).
- **Rest in Klasse C NMC (91):** 39 wie LFP gegen den Seitenrahmen (13 je Stecker), dazu 52 Daisy-Freigänge gegen Zellträger und Verguss (Feld 0 und 3; Überlappung je 710 mm³ Zellträger und 1410 mm³ Verguss; Freigang x 29–41 bzw. 1909–1921, y 82–110, z 20–30): Die Aussparung gilt nur der Buchse (Punkt 3), nicht dem Freigang davor.
- Klassen D, E, F, G sind unverändert (Regel gilt dort nicht): Maße siehe v0.2 Punkt 3. Offen an Opus.

**Punkt 3: NMC-Daisy-Buchsen, Aussparung in Zellträger und Verguss (Variante a).** Harte Kollisionen NMC **52 → 0** (LFP 0). Ausgesparte Volumina (`ergebnis_v03.json`, `aussparung_daisy_buchsen_mm3`): Zellträger Feld 0 1320 mm³, Verguss Feld 0 19 800 mm³, Zellträger Feld 3 240 mm³, Verguss Feld 3 3600 mm³ (22 Buchsen in Feld 0, 4 in Feld 3). Masse bekannt NMC 483,667 kg (v0.2: 483,676 kg), LFP 621,134 kg. Der Verguss selbst hat keine Dichte (Akte offen), seine Massenänderung ist nicht enthalten.

**Bilder:** je Variante Schaltbox und Endzone neu (`sv1_<V>_schaltbox.png`, `sv1_<V>_endzone.png`), Zielband 0 Verletzungen beschriftet, Lesehilfe im Bild. Pack-Dateien nur mit Suffix `_sv1` überschrieben (`/home/cae/cae_projekte/batterie/e2/pack_<V>_e2d_e3c_sv1.*`, `netz_<V>_e2d_e3c_sv1_*.json`, `cad/pack/entwurf/ergebnis_<V>_e2d_e3c_sv1.json`), keine `_e3c`-Dateien. Sicherungen: `/tmp/claude-1003/SV1b/` (`pack_e2d.py.vor_n3`, `ERGEBNIS_v02.md`, `sv1dir/`).

**Offen (an Opus):** (a) Via-Ausnahme 0,45/0,2 mm auch für LFP, damit DRC 0 gilt, danach Kopie nach `e3/` und `abgabe_2026-11-24/` als `cmu_<V>_mit_bohrungen.step` plus Pack neu; (b) Platinenstecker-Freigang 1 mm gegen den Seitenrahmen (Quer 2 mm bei 1 mm Abstand der Stecker zur Wand), NMC-Freigang in Verguss und Zellträger; (c) Klassen D, E, F, G unverändert.

---
### Stand v0.2 (2026-11-25 vormittags, unverändert)

**Status v0.2: ABBRUCH an OPUS bei Punkt 1 (durch Nachtrag 3 überholt)** (weder B3 noch B4v erreicht DRC 0 und 0 offen; Ursache sind Bauteile an den Bohrungsorten, nicht das Routing). `e3/` und `abgabe_2026-11-24/` sind unverändert, ebenso `cad/pack/pack_e2d.py` und `cad/pack/entwurf/`.

## Was getan
- **Punkt 1:** Routing der CMU LFP mit Freerouting (`-mp 200 -mt 5`, nice, Scope `hermes-batterie-sv1b-*`, CPU, ohne Wächter) für B3, dann B4v. Skripte `sv1b/lauf.sh`, `sv1b/lauf2.sh` (nutzen `w1_platine.py`, `strip_pcb.py`, Startplatine `w1/start/start_LFP.kicad_pcb`). Daisy-Regel 2,5 mm (ENT-183) angewendet.
- **Punkt 2:** Router-Log gegen KiCad-DRC verglichen.
- **Punkt 3:** Pack-Arbeitskopie `sv1b/pack_e2d_sv1b.py` (nur Schreibziele nach `sv1b/out`, `sv1b/out_e2` geändert, Bounding Boxen der Verletzungspaare ergänzt), beide Varianten neu gerechnet, Verletzungen mit `sv1b/gruppen.py` nach Klassen gruppiert.
- **Punkt 4:** NMC-Kollisionen (52) nach Bounding Box ausgewertet.
- **Punkt 5:** Akten ENT-200 bis ENT-208 (vorgeschlagen), `pm.py pruefe` 0 Fehler, `register`, `parameter`.
- Bilder Schaltbox und Endzone je Variante neu gerendert (Blender CPU, `sv1b/render_sv1b.py`) und beschriftet.

## Punkt 1: CMU-Bohrungen (LFP)
Abnahme laut ERW: DRC 0, 0 offen, 144 Thermovias. **Nicht erreicht.** Läufe 1 und 2 unterscheiden sich in einem Punkt (Fehler im Werkzeugablauf, siehe Punkt 2b). Lauf 2 ist maßgebend.

| Lauf | Variante | Router (letzter Pass, offen / Verstöße) | KiCad-DRC: offen | KiCad-DRC: Verstöße (Arten) | Dauer (start.txt/ende.txt) |
|---|---|---|---|---|---|
| lauf2_B3 | B3: (2,8\|2,8), (2,8\|57,2), (117,2\|30) | Pass 18: 3 / 50 | 0 | 18 (Sperrfläche 6, Bohrung-Kupfer 6, Courtyard 2, Bahnbreite 3, Lötstopp 1), **kein Daisy-Verstoß** | 10:44:35–10:48:19 |
| lauf2_B4v | B4v: 4 Ecken bei 4,8 mm | Pass 25: 10 / 46 | 3 | 10 (Sperrfläche 4, Bohrung-Kupfer 4, Courtyard 2) | 10:43:46–11:01:21 |
| lauf_B3 (ohne Daisy-Klasse) | B3 | Pass 18: 4 / 4 | 1 | 32 (davon 6 Daisy-Freiraum) | 10:38:53–10:42:52 |
| lauf_B4v (ohne Daisy-Klasse) | B4v | Pass 21: 9 / 0 | 3 | 30 (davon 3 Daisy-Freiraum) | 10:43:06–10:51:30 |

(Drei Läufe und der Pack-Lauf liefen gleichzeitig auf 8 Kernen, Zeiten daher nicht mit W1 vergleichbar.)

**Befund (Quelle `lauf2_B3/drc.json`, `lauf2_B4v/drc.json`, `frei_pruefung.txt`):** Die verbleibenden Verstöße sind **Bauteile am Bohrungsort**, kein Routingproblem:
- **B3, Bohrung (117,2 | 30):** liegt auf den Pads von **D2** (Pad 1: Abstand 0 mm, Pad 2: 0,73 mm) und im Courtyard von **D2 und J7**, auf den Handbahnen N$11/N$12 (Abstand 0 mm statt 2,0 mm). Der übrige Teil von B3 (zwei Eckbohrungen) ist unauffällig: 0 offen, kein Daisy-Verstoß.
- **B4v, Ecken (4,8 | 4,8) und (4,8 | 55,2):** liegen auf den Pads von **R20 (Pad 2 Netz D1)** und **R38 (Pad 1 Netz T10)** (Abstand 0,025 mm), R21/R39 haben 1,42 mm statt 2,0 mm. Die 3 offenen Verbindungen sind die dadurch gesperrten Netze T10, D1.
- Abstand Kupfer zu Bohrungskante an den Platzierungen **ohne Router-Bahnen** (nur Pads und 19 Handbahnen; `sv1b/frei.py`, Platinenkontur -0,05 bis 120,05 mm, daher ±0,05 mm): B4 (Ist, W1-Lage) MH1 2,11 mm (R20-2), MH2 8,10 mm, MH3 2,01 mm (R38-1), MH4 8,06 mm; B4v links 0,07 und -0,02 mm, rechts 5,57/5,55 mm; B3 Mitte rechts -1,25 mm (Bahn N$11).

**Frage an Opus (nicht selbst entschieden, keine eigenen Annahmen):** Die Lage der dritten B3-Bohrung und der linken B4v-Bohrungen kollidiert mit platzierten Bauteilen. Mögliche Lagen aus `frei_pruefung.txt` (Abstand zu Pads und Handbahnen ≥ 2,0 mm, Router-Bahnen noch nicht berücksichtigt, **nicht gerechnet**):
1. B3 mit den **zwei rechten Ecken** (117,2 | 2,8: 8,10 mm; 117,2 | 57,2: 8,06 mm) plus eine Bohrung links bei y ≈ 22–25 oder 35–38 (x = 2,8; freie Strecken 22..25 und 35..38 mm).
2. B3 nach Wortlaut der ERW („Langseite“): Ecken wie B4 plus Mitte (60 | 57,2): 2,02 mm (R47-1) bzw. (60 | 2,8): 2,12 mm (R29-2); knapp.
3. Ursprung B4 (2,8 mm): MH1 und MH3 haben 2,11 bzw. 2,01 mm, also gerade eingehalten, aber SV1 v0.1 konnte so nicht vollständig routen. Mit der Daisy-Klasse (Punkt 2b) wurde B4 hier nicht neu gerechnet.

## Punkt 2: Router-Log gegen KiCad-DRC
- **Beobachtung 2a:** Der Router meldet in `lauf2_B3` 3 unverbundene Verbindungen (N$11 J7-1→D2-1, N$12 J7-2→D2-2, N$7 J6-1→D1-1; `lauf2_B3/fr.log`), KiCad meldet 0 unverbunden (`lauf2_B3/drc.json`). Gleiches in W1 `lauf_04` (3 gemeldet, 0 im DRC). Alle drei sind **Daisy-Netze mit Handbahn**; die Handbahnen stehen als `(wire … (type route))` im DSN (`lauf2_B3/cmu_LFP.dsn`). N$8, ebenfalls mit Handbahn, wird nicht gemeldet. Ursache der Router-Zählung **nicht abschließend geklärt** (nicht untersucht, ob der Router die Handbahnen wegen der 46–50 gezählten Abstandsverstöße nicht als Verbindung wertet). **Maßgebend ist der KiCad-DRC** (Vorgabe Opus).
- **Befund 2b (Werkzeugfehler, Ursache der Daisy-Verstöße in W1):** `w1_platine.py bereit` lädt die Platine ohne passende Projektdatei. KiCad nimmt dann die Standard-Netzklassen und schreibt `cmu_LFP.kicad_pro` mit nur der Klasse „Default“ (geprüft: `lauf_B3/cmu_LFP.kicad_pro` hat nur Default; `lauf2_B3/cmu_LFP.kicad_pro` hat Default, Ausgleich, Daisy 2,5). Im DSN von W1 `lauf_04` fehlt deshalb die Klasse Daisy (`grep "(class"` zeigt nur `kicad_default`), im DSN von `lauf2_*` steht `(class Daisy N$11 N$12 N$7 N$8`. Das erklärt die Daisy-Verstöße (3 bis 6, kleinster Ist-Abstand 0,4495 mm) und die schnellen Pässe (0,4 s) in W1: **der Router hat die Daisy-Regel 2,5 mm dort nie bekommen.** Abhilfe in `sv1b/lauf2.sh`: Projektdatei als `basis.kicad_pro` neben die Basisplatine legen. Folge für W1: Das Fazit (Verstöße kommen nicht von den Bohrungen, Kolibri sinnlos gewechselt) bleibt richtig, die Erklärung „Router hält 2,5 mm nicht ein“ (W1 Auffälligkeit 2) ist damit ersetzt. `w1_platine.py` und `rechnen/kolibri_waechter_cmu.py` habe ich nicht geändert (Eingriff nur auf Ansage).
- Der Router meldet bei Daisy-Klasse 46 bis 50 Verstöße schon im ersten Pass (`fr.log`), auch im E3-Lauf (`e3/route/fr_LFP_a.log`: 47). Der Wert bleibt im Lauf konstant; im DRC ist davon nur noch das Handbahn-Gerüst betroffen (0 Daisy-Verstöße in `lauf2_B3`).

## Punkt 3: Freigangslogik (211/215 Verletzungen)
Neurechnung mit der Arbeitskopie: **LFP 211, NMC 215 Verletzungen, harte Kollisionen LFP 0, NMC 52, Teile 1183 bzw. 2916** (`ergebnis_v02.json`), also identisch mit v0.1 (Quelle `ergebnis.json`). Die Hypothese „Freigang wird gegen eigenes Kabel, eigenen Stecker oder Nachbarzellen geprüft“ trifft **nur teilweise** zu:
- **Eigene Teile desselben Steckers (Gegenstück, Kabelstecker, Platine, Flansch, Schrauben): 0 Treffer in beiden Varianten.** Der Code nimmt sie bereits aus (`cfg_["prefix"]`, `grp_ok`, `names_ok` in `pack_e2d.py` Zeile ca. 845); Klasse A der Gruppierung ist leer. Eine Änderung der Ausnahmen würde keine Verletzung beseitigen, deshalb **nicht geändert**.
- Verteilung (`ergebnis_v02.json`, `gruppen_detail`):

| Klasse | LFP | NMC | Inhalt |
|---|---|---|---|
| A eigenes Teil | 0 | 0 | bereits ausgenommen |
| B Freigang gegen Nachbarstecker auf der CMU | 20 | 20 | Freigang In/Out gegen den Nachbarstecker, je 192 mm³ (quer 10 mm trifft den Nachbarn) |
| C CMU-Platinenstecker (Daisy, FPC) gegen festes Teil | 162 | 169 | Seitenrahmen 14 je Stecker, Kühlplatte, Pad, Zelle, bei LFP zusätzlich Querverbinder (7) und Lasche (1), bei NMC Verguss, Zellträger |
| D BMS-Stecker gegen Nachbarstecker | 2 | 2 | J_DAISY1 gegen J_DAISY2 (je 576 mm³) |
| E BMS-Stecker gegen Schaltbox/Bauteile | 6 | 6 | 5 gegen Schaltbox-Wanne (Volumen 57–1008 mm³), 1 gegen Schraubenkopf HV 250 A |
| F Deckelstecker (Freigang, Handraum Ø 75) | 18 | 18 | Nachbarstecker, Flansche, Deckel, obere Kühlplatte, Gas-Drucksensor |
| G Schütz-Spulenstecker | 3 | 0 | gegen Pyrosicherung, Schmelzsicherung, Halter (LFP) |

- **Zur Klasse C (Maße, LFP CMU 00, `out/ergebnis_LFP_e2d_e3c_sv1.json`):** Freigang Daisy-In x 2001–2029, y 12–60, z 17–35 mm; Zelle_218 reicht bis x 2004 (Überlappung 3 mm); Kühlplatte und Pads enden bei x 2020 (Freigang quer 10 mm geht 9 mm darüber hinaus); der Freigang nach unten (z 17 bis 20) schneidet Kühlplatte unten (z 11–19) und Pad unten (z 19–20). Ursache ist die Annahme quer 10 mm plus 25 mm Greifraum: Der Freigang ist größer als der Platz zwischen Zellende und Endwand. Das ist **eine echte Verletzung der angenommenen Freigangsregel**, kein Skriptfehler.
- **Echte Verletzungen an Opus mit Maß** (Entscheidung: Regel lockern, Stecker verlegen oder Freigang nur dort, wo er Zugriff braucht): Klassen B, C, D, E, F, G; alle Paare mit Volumen und Bounding Box stehen in `sv1b/out/ergebnis_<V>_e2d_e3c_sv1.json` (Feld `steckfreigang_verletzungen`).

## Punkt 4: NMC-Daisy, 52 harte Kollisionen
Quelle `sv1b/out/ergebnis_NMC_e2d_e3c_sv1.json` (Feld `kollisionen`, mit Bounding Box):
- **26 Daisy-Gegenstücke (Buchse, 8 × 15 × 8 mm)** der CMU 01–11 (Feld 0, Buchsen bei x 31–39) und 00, 12 (Feld 3, x 1911–1919) liegen bei z 22–30 mm. Feld 0 und Feld 3 haben **Zellträger** (z 20–22,5; Überlappung je Buchse **60 mm³**) und **Verguss** (z 22,5–60; Überlappung je Buchse **900 mm³** = 8 × 15 × 7,5 mm, die Buchse liegt ganz im Verguss). 26 Buchsen × 2 Teile = 52.
- Bei LFP gibt es weder Verguss noch Zellträger an dieser Stelle (0 Kollisionen).
- **Vorschlag zur Lage (nicht umgesetzt):** a) Aussparung im Zellträger und im Verguss um jede Daisy-Buchse (8 × 15 × 7,5 mm, wie die vorhandene Aussparung für die CMU), oder b) Buchsen der Daisy-Stecker bei NMC so legen, dass sie unterhalb z 22 bzw. außerhalb x 30–480 bzw. 1470–1920 liegen. Entscheidung Opus.

## Punkt 5: Akten (alle Status „vorgeschlagen“, Opus ERW-SV1 N2)
ENT-200 BT-711 `steckfreigang_mm`; ENT-201 BT-720; ENT-202 BT-730; ENT-203 BT-740; ENT-204 BT-360; ENT-205 BT-311 `steckfreigang_mm`; ENT-206 BT-311 `befestigung` (6 × M3, Bolzen 8 mm); ENT-207 BT-311 `bohrung_d_mm` 3,2 (aus der CMU-Zeile der ERW **übernommen**, Opus bitte bestätigen); ENT-208 BT-311 `bohrung_anzahl` 6. Werte `steckfreigang_mm` sind Textregeln aus `annahmen_sv1.json` (Steckweg, Kappe 10, Greifraum 25, quer 10, Handraum Ø 75). `pm.py pruefe`: 208 Entscheidungen, 0 Fehler. `pm.py parameter` übernimmt sie erst nach Status „entschieden“.
**Nicht angelegt:** BT-321 `befestigung`, `bohrung_d_mm`, `bohrung_anzahl` (Lage und Anzahl hängen an der offenen Entscheidung aus Punkt 1).

## Masse
`ergebnis_v02.json`: Zusatzmasse der SV1-Gruppen (Stecker, Gegenstücke, Schrauben) LFP 1,334 kg, NMC 1,456 kg (Bildbeschriftung). v0.1 nannte Gesamtmassendifferenz 1,29 bzw. 1,26 kg. Die beiden Größen haben andere Definition (Gruppensumme gegen Gesamtmasse vorher/nachher), der Unterschied ist nicht weiter untersucht. Erwartung 0,3–0,6 kg weiterhin verfehlt (Annahmemassen der Kabelstecker).

## Abgleich mit Erwartung (Nachtrag 2)
| Punkt | Erwartung | Ergebnis | Urteil |
|---|---|---|---|
| 1 | B3, sonst B4v: DRC 0, 0 offen, 144 Thermovias | B3: 0 offen, aber 18 Verstöße (Bauteile an der Bohrung); B4v: 3 offen, 10 Verstöße; Thermovias nicht gesetzt | verfehlt, Abbruch an Opus |
| 2 | Abweichung klären | Router zählt Handbahn-Nets unverbunden, KiCad nicht (Ursache offen); Daisy-Klasse fehlte in W1 (geklärt) | teils geklärt |
| 3 | Freigangslogik, Eigene Teile in Ausnahmen | eigene Teile: 0 Treffer, schon ausgenommen; Rest echte Verletzungen der angenommenen Regel | Hypothese nicht bestätigt |
| 4 | 52 Kollisionen prüfen, Lage melden | 26 Buchsen in Zellträger/Verguss, Vorschlag gemeldet | erledigt (Entscheidung offen) |
| 5 | Akten zu neuen Merkmalen | 9 Akten, BT-321 offen | teilweise |

## Offen (an Opus)
1. Lage der Bohrungen (Punkt 1), dann BT-321-Akten, Rechnung erneut ab `sv1b/lauf2.sh` (Skript nimmt Variante B3|B4v|B4|B2K aus `w1_platine.py`; für eine neue Lage muss `w1_platine.py` `lagen()` geändert werden, das habe ich nicht getan). Danach NMC per Übertragung, Thermovias (`thermovias.py`), `via_aufraeumen.py` (3 Bahnbreitenverstöße 0,12 mm in `lauf2_B3` sind damit behebbar).
2. W1: Erklärung der Daisy-Verstöße ersetzen (Punkt 2b); Fazit zu Kolibri neu bewerten, falls gewünscht.
3. Freigangsregel quer 10 mm / Greifraum 25 mm gegen Platz an der Endwand (Punkt 3), NMC-Aussparungen (Punkt 4).
4. BMS-Platine: Bohrungen und Routing weiter offen (ENT-206 bis ENT-208).
5. ENT-207: Bohrungsdurchmesser BMS bestätigen.
6. Router-Zählung (Punkt 2a) bleibt ungeklärt.

## Integrationsgrenzen
Pack-Arbeitskopie unterscheidet sich vom Original nur in Schreibzielen, Bounding-Box-Feldern und der CMU-STEP-Variable (`CMU_STEP`); gleiche Zahlen (211/215/52, 1183/2916 Teile). Das CMU-STEP im Pack ist weiterhin das alte ohne Bohrungen. Bilder neu gerendert, Geometrie unverändert; die 52 NMC-Kollisionen sind auf den Bildern nicht markiert. Freie-Lage-Prüfung (`frei.py`) kennt nur Pads und Handbahnen, keine Router-Bahnen und keine Innenlagen.

## Dateien
`sim/mechanik/sv1_stecker_verschraubung/ERGEBNIS.md`, `ergebnis_v02.json`, `sv1_<V>_{schaltbox,endzone}.png` (neu; Sicherung der alten in `/tmp/claude-1003/SV1b/sv1dir/`), `frei_pruefung.txt`; Arbeitsdateien `/home/cae/cae_projekte/batterie/sv1b/` (`lauf.sh`, `lauf2.sh`, `lauf*_B3`, `lauf*_B4v`, `pack_e2d_sv1b.py`, `pack_analyse.sh`, `gruppen.py`, `frei.py`, `render_sv1b.py`, `label_sv1b.py`, `akten.py`, `out/`, `out_e2/`, `bilder/`); `pm/entscheidungen/ENT-200…208.md`; `praesentation/bausteine/SV1.md`.

> KI-generiert (Claude Sonnet, 2026-11-25), Entwurf, nicht freigegeben.
