# ERINNERUNGEN – Batteriesystem (Übergabe, neuestes oben)

KI-generiert (Claude Opus).

## 2026-11-18 · E2 Fortsetzung 2 fertig (Sonnet, 09:40)
- ENT-145 (NMC Mäander), ENT-146 (130 mA NMC), ENT-147 (LFP 2050) vorgeschlagen; ENT-115 auf [LFP]. Ergebnis `sim/elektrik/e2_elektronik/ERGEBNIS.md` v0.3, B-BAT-025. Offen für Opus: LFP-Verschaltung, LFP-FPC, ENT-138 vs ENT-144.

## 2026-11-18 · E2
- Autor: „mach e2, denk an das token sparen“. ENT-109 (Schaltbox Deckel vorne, entschieden), B-BAT-024. Sonnet läuft: E2-Akten, CAD Fall b, Bilder, Schaltbild, Kabelplan (AUFTRAG.md „Fortsetzung 2026-11-18“). Danach Opus Stichprobe, dann Crash X.
- Autor: Turm 210 mm ok, „unter der rücksitzbank“ → ENT-144 (Box hinten, ersetzt ENT-109). Opus: Mäander, NMC 130 mA, LFP 2050 mm (vorgeschlagen, Sonnet legt an). Fortsetzung 2 läuft.
- Autor: nach GitHub laden. Privates Repo, schlank (.gitignore vorbereitet), erst nach E2 und Prüfung. Größe dann mit `du` gegen die .gitignore prüfen. Kein git im Projekt bisher, also git init.
- E2 Fortsetzung 2 fertig (ENT-145…147, B-BAT-025). Opus-Fehler „Mitte hinten“ (BA-77) → Nachtrag 2, Fortsetzung 3 läuft. Danach GitHub.
- E2 Fortsetzung 3 fertig (v0.4, B-BAT-026, ENT-148/149). Offen: LFP-Trennstecker +58 mm, Nut Kühlplatte. Freigaben ENT-110…149 offen.
- GitHub: privates Repo batterie-system angelegt, erster Commit (1376 Dateien, ~154 MB, meist PNG). Kein Auto-Push: nur auf Ansage des Autors.
- E2 v1.0 fertig (B-BAT-027, ENT-150 Trennbrücke). Offen: NMC-Verbinder 15×3 (E1) vs 25×3 (CAD), LFP-Lasche, Freigaben ENT-110…150. Nächstes: Crash X.
- Autor: „höheren detailierungsstand erwartet“ → alle 4 Bereiche, Konstruktionsstand. ERWARTUNG Nachtrag 3, Fortsetzung 5 läuft (neue Dateien pack_<V>_e2d.FCStd).
- Autor: „um die Stückliste kümmern … Kostenbewertung“ → REQ-P16 (vorgeschlagen), AEN-018. Sonnet SL2 (AUFTRAG_STUECKLISTE_V2.md), PI W29 Kosten. Danach Opus: pm/kosten/eingaben.json füllen (Belege W29), ERWARTUNG Kosten.
- SL2 fertig (B-BAT-028, 5 BT ergänzt). W29: nur BNEF 97 USD/kWh belegt. ERW-KO1 (pm/kosten/ERWARTUNG.md) geschrieben, Sonnet KO1 läuft.
- KO1 fertig (B-BAT-029): LFP 80, NMC 110 €/kWh, untere Schranke, 100 % Schätzung. Nach E2 v1.1: Stückliste + KO1 neu.
- E2 v1.1 (e2d) fertig, in FreeCAD geöffnet. Opus-Urteil: noch quaderhaft. Offen: M8-Kopf LFP (134 mm), Box innen 116 > 90, Bilder transparent/verrauscht. NMC 25×3 gilt (ENT-096), E1 15×3 veraltet. Autor-Rückmeldung abwarten vor Fortsetzung 6.
- Autor: „das lassen wir ersteinmal wie es ist. später machen wir eine überarbeitungsschleife, dass macht dann opus. jetzt bericht ergänzen, hochladen, crash“. → später Überarbeitungsschleife Detailierung durch Opus selbst (Formen Kaufteile, Farben, Renders, M8-Flachkopf, Schütze liegend).
- Laufen: Sonnet Bericht 0.3 (AUFTRAG_BERICHT_03.md, vorher SL/KO neu), Sonnet X1 (sim/mechanik/x1_seitencrash, ERW-X1), PI W30 Crash-Normen. Nach Bericht: git push.
- PI-Warteschlange losgelöst (setsid): W31 Bauteilpreise, W32 Al-Kennwerte, W33 MSD/Schütz-Maße; Log forschung/warteschlange.log. Danach Opus: pruefe-Ergebnis lesen, Schätzungen → verifiziert.
- Autor-Info: OpenRadioss offiziell eingestellt (Siemens, 01.10.2026), Fortführung OpenCourant/Mirrors → X2 nur damit, nach Freigabe (konzept_werkzeuge…crash.md §4).
- X1 fertig (B-BAT-030): keine Knautschzone im Pack, Zellberührung ≈ 30 kN/20 J. Opus-Fehler in ERW-X1. Frage Autor: Knautschzone im Pack (kostet Zellen) oder alles über Schweller.
- Autor: „ja mach das, kannst du das auch hiemit OpenCourant rechnen“ → X1b Knautschzone w 15/20/30 + X2 OpenCourant (RESF-Fork, AGPLv3, github.com/OpenCourant/OpenCourant, per Websuche bestätigt). Sonnet läuft.
- X1b CalculiX: alle Läufe bei 13–33 % Weg divergiert (Faltung) → Opus gestoppt 18:05. Methodenwechsel X1b+X2 explizit OpenCourant (ERWARTUNG Nachtrag 1, AUFTRAG_X2.md), Sonnet läuft.
- X1b/X2 fertig (B-BAT-031): Knautschprofil bringt nur 0,4–0,6 kJ bis Zellberührung (Ziel 5 kJ), Innenwand biegt zwischen Querträgern. Opus-Empfehlung: keine Knautschzone im Pack, Schweller trägt; optional Studie engere Querträger. Autor entscheidet.
- Opus-Prüfung X1b/X2 (ERGEBNIS.md): tragfähig, Vereinfachungen konservativ → Empfehlung robust. Autor: „opus zum abschluss die studie überprüfen und dann … überarbeitung“; 32 GB RAM (Crash Stufe 2 ≤ 1 Mio Schalen). Nächstes: Überarbeitungsschleife E2 durch Opus.
- OpenCourant latest-20261011 (cb760c2) installiert in ~/cae_projekte/werkzeuge/opencourant, Rauchtest ok (miniqa SMOKE_TEST). X2 wartet auf w-Wahl.

## 2026-11-17 Abend – Übergabe für morgen
- Autor: „bitte wieder sparsam mit den token. und nimm b. Vielleicht bereitest du erst alles vor speicherst ab und morgen geht es weiter“
- Erledigt heute: 67 Akten entschieden (AEN-017); K2 Kühlplatte (ENT-104…106 vorgeschlagen, 107/108 Durchfluss entschieden); C1, C2 (Blade 0,877 mΩ gemessen; 4680 30 min bei 1,5C, Plating-Risiko); K1c (LFP 32,7/4,0; 4680 34,0/4,15 bzw. 39,1/6,5); Autor: Auslegung mit Modellwärme, Risiken R-PLAT, R-4680W.
- E2: Teil 1 gerechnet (ergebnis.json). Schaltbox **Fall b (auf dem Deckel vorne)**, Autor-Entscheidung → Akte BT-710 einbauort anlegen. CAD Fall b vorbereitet (Stand in sim/elektrik/e2_elektronik/ERGEBNIS.md „Stand 2026-11-17“).
- Morgen: (1) E2 CAD prüfen, Renders, Schaltbild, Kabelplan; E2-Akten (Annahmen ERWARTUNG-Tabelle + Nachtrag 1) als vorgeschlagen anlegen. (2) Crash X (ERWARTUNG schreiben). (3) Bericht 0.3 (C1/C2/K1c/K2/E2/X). ENT-104…106 noch zur Freigabe vorlegen.

## 2026-11-17 abends · Pack
- 103 Akten, 0 Fehler. Eigenes Gehäuse je Variante (LFP 2030, NMC 1950). G4 Freigabe-Render läuft (cad/pack/render_pack.sh). Danach Autor Bilder zeigen. Offen: Bericht auf Stand bringen (K1, K1b, M0, E1, G4), Crash X, Kühlplatte BT-610 Kanäle.

## 2026-11-17 spät · Gehäuse
- REQ-P05: LFP 20 min, NMC 30 min (Autor). K1b fertig. Offen Autor: ENT-092…095 (4680 Halter/Verbinder) freigeben. Nächstes: E (Verbinder, Querschnitte), G3/G4 Pack-CAD.
- ENT-082…091 vorgeschlagen (Querträger 3× 54×26×2,5 Al, Seitenrahmen 30, Kühlplatte oben+unten 2×8 mm, Länge 2030). Offen Autor: Freigabe, Schweller trägt Seitencrash? K1/M0/PI-Patente fertig; PI-Inhalte P02–P13/W23 noch nicht gelesen.

## 2026-11-17 nachmittags · Kühlung, Bericht
- Autor: Breite durch Straßen-/Fahrzeugbreite begrenzt (1430 fest), Länge flexibel. Querträger kosten Länge (ok), Seitenrahmen/Längsträger kosten Breite (LFP-Reserve 8 mm!).
- Autor: 45 °C / 5 K (REQ-P09), Kühlplatte unten (ENT-081), Temperaturverläufe gerendert, Bericht beginnen.
- Laufen parallel (Sonnet): 4680-Detail mit Kern 12,5 mm (ENT-074 korrigiert, flächentreue Spirale); K0 Elmer + pvbatch-Bilder/Film; Bericht 0.1 (bericht/AUFTRAG_BERICHT.md, BAT-DOC-17).
- Erledigt: 4680-Detail korrigiert (22,565 in 22,60 mm), K0 fertig (B-BAT-018, DEUTUNG.md), Bericht 0.1 30 S. mit K0.
- Offen beim Autor: 5 K beim Schnellladen (a Leistung begrenzen / b 10 K beim Laden / c zusätzlich kühlen); ob K0-Renders hochwertig neu (Cycles). Bericht offen: zellen_vergleich.png 660 mm, 683/644 kg.

## 2026-11-17 mittags · Zell-CAD, Detail
- Autor: Modelle aufrufen (FreeCAD geöffnet), Blender-Render (cad/zelle/entwurf/render/), dann „zellen weiter detailieren … gewickelte folie … Isolatoren“.
- Opus liest W20 Abb. 2/4/5 + Tab. 1 → cad/zelle/aufbau_W20.json; Baum 60 Einträge (ENT-031); Akten ENT-032…080 vorgeschlagen. Eigener Fehler: LFP-Länge 681 statt 660 mm (Endzone fest) → Autor: Bauraumbreite 1430 mm (ENT-030). B-BAT-015.
- Läuft: Sonnet Detailmodell + Schnittbilder + Neulauf G1/C0b (cad/zelle/AUFTRAG_DETAIL.md).
- Fertig 12:09 (Sonnet): Detailmodell `cad/zelle/entwurf/detail/` (8 Bilder, ERGEBNIS_detail.md), Lauf 3 G1/C0b, startwerte/Stückliste mit B 1430 mm. Offen für Opus: 4680-Wickel ragt 1,15 mm über den Becher; Bilder und Deutung prüfen; Autor wollte Bescheid (FreeCAD: zelle_*_detail.FCStd).
- Offen beim Autor: Freigabe ENT-014…029 (ENT-015 jetzt 681), ENT-031…080.
- Autor: Thermosimulation → K0 (sim/kuehlung/k0_zelle/, Elmer, CPU) läuft. Zielwerte 45 °C / 5 K sind Annahmen (REQ-P09 offen, Autor fragen). Autor will Bescheid, wenn Detailmodell fertig (dann in FreeCAD öffnen).

## 2026-11-17 · Bilder, G1-Vorprüfung
- Autor: „machen wir weiter“, „kann man einige berechnungsergebnisse auch als bilder und grafiken dokumentieren?“ → Bildverzeichnis docs/16_ergebnisbilder.md (pm/plan/bilder.py, 6 Bilder), Zusatzgrafiken bauraum/empfindlichkeit/kriterien (LFP Hauptwert 160 Wh/kg).
- G1-Vorprüfung (B-BAT-012): LFP A passt nur bei ≤ 0,73 mm Zellabstand; NMC A 72 % der Plätze. lauf.sh gibt PI jetzt die Quell-URLs vor (ungetestet im Lauf).
- Autor: ENT-012 frei, Bauraum verlängern → ENT-013 L 1950 mm (B-BAT-013), Lastenheft/AEN nachgeführt; Neulauf G1/C0b läuft.
- Autor „ja mach“: G1-Akten ENT-014…029 vorgeschlagen (B-BAT-014) → Freigabe offen. G2-Entwurf (cad/zelle/entwurf/) läuft bei Sonnet.

## 2026-11-16 abends · Stand zum Weitermachen
- Autor: „bitte beende, wir machen morgen weiter“.
- Nächste Schritte: (1) Autor: ENT-012 freigeben. (2) Sonnet: Bild C0b LFP-Balken auf 160 Wh/kg. (3) G1 Zellmaße je Variante (LFP Sonderzelle ~92 Ah; NMC 4680 Ø46×80 Akten durchmesser/hoehe nach ENT-012). (4) G3/G4: Zellen je Reihe, Zellhalter, Fühler für 4680. (5) C2: Blade-Pulsdatensatz (Borealis) für Innenwiderstand. (6) Werkzeug: lauf.sh muss PI die genaue Quell-URL vorgeben (B-BAT-009).
- Nichts läuft im Hintergrund.

## 2026-11-16 · Zwei Varianten
- Autor: zwei Varianten parallel, gleiche Spezifikation; NMC = 4680. Varianten in Akten (`variante:`), parameter_<V>.json, `--variante` (B-BAT-010). ENT-007…011 NMC entschieden, ENT-012 Baum (BT-250 Zellhalter) vorgeschlagen. C0b fertig (B-BAT-011): NMC-4680 411 kg, LFP-Blade 616 kg (Fall A); LFP-Bauraum knapp. Offen: ENT-012 Freigabe; Bild LFP-Balken auf 160; NMC Zellen je Reihe (G4).

## 2026-11-16 · 800 V, Zerlegungsstudie
- Autor: „studie ist abgelegt, mach 800 Volt“ → ENT-006 BT-000 800 V entschieden (Mensch); Stückliste 250s×1p, 92,4 Ah, 73,9 kWh (Sonnet, geprüft).
- W20 (B-BAT-009): Blade Gen 1 gemessen 160 Wh/kg, 355 Wh/L, 135 Ah, 2,7 kg. Bauraum Fall A knapp (213/214), Fall B nicht. LFP-Pack Fall A ~616 kg. → Autor: ENT-005 halten oder C0 mit Messwerten neu rechnen (C0b)?

## 2026-11-16 · Freigaben, W18, Suche Zerlegungsstudie
- Autor: „1500 kg sind erst einmal Anhaltswert, 2 und 3 gebe ich frei, zu 4, ich habe keine Zerlegungsstudie, du kannst gerne eine Recherche machen.“ → ENT-004/005 entschieden (Mensch), REQ-P01 Anhaltswert (Fall A/B als Spanne).
- W18 geprüft (B-BAT-007). Zerlegungsstudie überall gesperrt (403/Bot-Sperren); W19 (drpress-PDF) läuft. Blade-135-Ah-Pulsdatensatz (Borealis, CC-BY) für C2 gefunden.
- Sonnet: pm/AUFTRAG_LFP_UMSTELLUNG.md (startwerte.py folgt ENT-005, Stückliste LFP, Obsidian 46 BT, Bildbeschriftung) läuft.
- W19 fertig (B-BAT-008): Volumennutzung Blade-Pack 60 % → Zelle braucht 357 Wh/L (A). Sonnet-Umstellung LFP fertig und geprüft. Offen beim Autor: Energie Stückliste 112 kWh (140 Ah Annahme) gegen 73,9 kWh → 800 V/92 Ah oder 400 V/185 Ah?
- Falle: Warteschleife `pgrep -f "lauf.sh wissen W18"` findet sich selbst → nie fertig. Richtig: `pgrep -f "^bash forschung/lauf.sh …"`.

## 2026-11-16 · Analyse komplette Batterie
- Nutzer: „es soll eine komplette batterie gebaut werden. dazu soll die struktur in die informationen genutzt werden analysiere es gut“.
- CLAUDE.md: Abschnitt „Ziel: eine komplette Batterie“ (Struktur, Information, Rechnung), Befehle, Datenfluss. Analyse → BEFUNDE B-BAT-004.
- Nächster Schritt: Bauteilbaum erweitern (Vorschlag an Autor), Chemie LFP/NMC durch Autor, V2.
- Nutzer: „ja, erweitere den Bauteilbaum und mach R4 parallel“; Projekt wurde von der Claude-Instanz aus ~/hermes/fusion angelegt → deren Gedächtnis gelesen, Regeln übernommen.
- Bauteilbaum: 46 Bauteile (ENT-004 vorgeschlagen), Schaltbox BT-710; Stückliste 38 Pos. umnummeriert (400.4–9, 500.7 → 700.x), stueckliste.py prüft Pos↔BT. parameter.json: 125 offene Merkmale. Alte Fassung im Scratchpad struktur_v1_2026-11-11.json. Obsidian-Bauteilnotizen zeigen noch nur die 8 Baugruppen (Teil → Gruppe), Nacharbeit wissensnetz_obsidian.py.
- R4: Vorprüfung an Sonnet (forschung/AUFTRAG_R4_VORPRUEFUNG.md → R4_vorpruefung.md, _kurz.txt); danach liest Opus B-Fälle + Stichprobe.
- R4 fertig (B-BAT-005, forschung/R4_ergebnis.md): 0 erfundene Werte; W06 Z22 (LFP 150–220) gesperrt, ist NMC; Wh/L-Frage offen. Zerlegungsstudie Blade (doi:10.1016/j.xcrp.2025.102453) → Autor soll PDF in quellen/ legen, dann W19 per file://. W18 (314-Ah-LFP thermisch) läuft ab 15:25, Neustart: `bash forschung/lauf.sh wissen W18`.
- Offen für Sonnet nach W18: wissensnetz_obsidian.py Bauteilnotizen für alle 46 BT (Teil → eigenes BT).
- Autor: 1500 kg, 400 km, LFP/NMC vergleichen → sim/chemie/vergleich_lfp_nmc (B-BAT-006): kein belegter Massenunterschied; ENT-005 LFP-Blade vorgeschlagen. Rückfrage offen: 1500 kg mit/ohne Batterie. Nach Freigabe: startwerte.py/stueckliste.py auf LFP umstellen (Sonnet). Bild: Grenzbeschriftung Fall A kosmetisch.

## 2026-11-11 19:40 · Projektmanagement
- Nutzer: Projektmanagement als weitere Stufe; Entscheidungen dokumentieren; Ziel: am Ende mit dem Bauteil sprechen (PI); Abschlussvideo Zelle → Stack → Regelung → Verkabelung → Struktur → Kühlung → Zusatzkomponenten.
- Gebaut: pm/ (struktur.json BT-000…700, entscheidungen/ENT-001…003 + VORLAGE, pm.py pruefe/register/parameter/kontext/neu, gespraech.sh + ROLLE_BAUTEIL.md), docs/12_projektmanagement.md, video/STORYBOARD.md, REQ-D11…D13.
- Test Bauteilgespräch BT-100: 33 s, 4/4 Aktenverweise gültig. Fehler gefunden: PI -p wartete auf stdin → `< /dev/null` (auch in forschung/lauf.sh).

## 2026-11-11 19:00 · Verteilung + gewerblicher Maßstab
- Nutzer: „auch soll opus die arbeiten an sonnet, haiku und pi deligieren, ohne dass ich das laufend sagen muss. das ganze soll auch so eine Art testprojekt für den gewerblichen einsatz sein. daher auch bitte dokumentationsunterlagen entsprechend speichern auch an anforderungen denken.“
- CLAUDE.md (Arbeitsteilung, Regeln), .claude/agents/sonnet-umsetzer.md (model sonnet), haiku-helfer.md (model haiku). PI über forschung/lauf.sh.
- docs/ BAT-DOC-00…11: Lenkung, Lastenheft (REQ-P01…P15 Werte offen, REQ-D01…D10), Pflichtenheft, Nachverfolgung, Entscheidungen ENT-001…003, FMEA, Verifikationsplan, Normenliste (nur Namen, Recherche offen), KI-Einsatzprotokoll, Änderungen, Lizenzen, Prozess.
- Offen: Vorgaben REQ-P01…P08 vom Autor; Normen-Recherche als PI-Thema (URLs fehlen noch).

## 2026-11-11 · Projekt angelegt (nur Vorbereitung)
- Nutzer: „nächste idee. diese findet hier statt. /home/cae/hermes/batterie ein komplettes batteriesystem soll entwickelt werden. mit chemie der Zellen, geometrisches darstellung der Zellen, zusammenbau der gesamten Batterie, auslegung der elektrik, kühlung der batterie ist auch wichtig. wissensaufbau und patentrecherche. … hier beispiel einer batterie. https://www.byd.com/de/technologie/blade-battery . lege alles an was benötigt wird. mach nur die vorbereitung … nehme diese Projekte als basis fusion, wasserstoff, E-Maschinen Agent. software sollte komplett vorhanden sein.“
  Dazu: „du kannst auch für pi einen recherche agenten für Patente und wissensaufbau anlegen“.
- Angelegt: README, AGENTS.md, PLAN.md (Vorgaben offen!), SOFTWARE.md, BEFUNDE.md, LESSONS_LEARNED.md, Ordnerbaum, .venv (PyBaMM 26.10.1.1 u. a.), umgebung.sh, .gitignore.
- Rechercheagent: forschung/lauf.sh (A paket.py ohne KI → B PI --no-tools → C pruefe.py), Themen P01–P10, W01–W07. Neuer Skill ~/.hermes/skills/cae/patent-recherche (patente.py, paket.py, pi_antwort.py). NOCH NICHT GESTARTET.
- BYD-Seite liefert ohne JavaScript keinen Inhalt → Kennwerte über Recherche W03/P01.
- Kein git init, nichts committet, kein GitHub.
- Nächster Schritt: Vorgaben aus PLAN.md 0 vom Nutzer; dann `bash forschung/lauf.sh` (GPU frei? GX/ollama prüfen).

## 2026-11-12
- Nutzer: „kannst du PI vielleicht schon auf die recherche für das Batterieprojekt ansetzen …“ und „auch wo und wie kann uns ein surrogatmodell helfen. Im AI_Framework gibt es einen Planer.“
- Recherche läuft losgelöst: `forschung/alles.sh` (W01–W15, T01–T07, P01–P10), Log forschung/verlauf.log, Abbruch `touch forschung/STOP`. paket.py: Pause 2 s + 3 Versuche (Wikipedia 429).
- Netzplan: pm/plan/plan_batterie.py → JSON auch in ai_workspace/ai_framework/data/plans/batteriesystem_batterie.json (gitignored). 35,5 AT Annahme.
- Ersatzmodell-Einschätzung: docs/ersatzmodell_einsatz.md.
- Nächster Schritt nach Recherche: Opus prüft (R4), dann Lastenheft-Vorschlag V1 an Nutzer.
- 12:30 W01 geprüft (B-BAT-001): PI ok, pruefe.py ignoriert jetzt Link-Adressen (Vorversion in Scratchpad gesichert). Lauf geht weiter (W02 …).
- Startparameter (Nutzer: „so wenig wie möglich in natürlicher Sprache“): pm/startwerte.py "<Satz>" → docs/startparameter.md. 4 Angaben: Fahrzeug, Reichweite, Ladezeit 10→80 %, Einsatzgebiet. Vorschlagssatz wartet auf Nutzer. Offener Widerspruch: LFP 180 Wh/L zu niedrig? (W03).
- Nutzer: Sketch-to-Prompt für Kühlung, Pre/Post-Querschnitte, Kabelverlegung, Luft/Wasser, Seitencrash, Ereignisprotokoll Buch → docs/konzept_werkzeuge_kuehlung_kabel_crash.md; Plan W1/W2/K0/L1/X1/X2; Themen W16/W17 (Nachlauf forschung/nachlauf.sh wartet auf ALLES FERTIG), T08/T09. Buch: ~/hermes/buch/ereignissprotokoll_batterie/ereignisprotokoll.md (BA-01…14). OpenRadioss nicht installiert, nur nach Freigabe. Offen: welches „Querschnitt-Postprocessing-Tool“ meint der Nutzer?
- PI speichert nach jedem Thema (lauf.sh sammeln()).
- Wissensnetz: pm/plan/wissensnetz.py (Verknüpfungen V, Software SW) → wissensnetz.json, BAT-DOC-03 erzeugt, Planer-Notizen. Ansicht: Sonnet baut pm/plan/wissensnetz_ansicht.py → wissensnetz.html (läuft, Opus prüft). Befunde verknüpfen mit „Vorgang: [ID]“.
- Wissensnetz-Ansicht fertig (Sonnet, von Opus geprüft): pm/plan/wissensnetz.html, ?knoten=ID. Aktualisiert sich nach jedem Recherchethema (ab Block werkzeuge; laufender Block wissen nutzt noch alte lauf.sh). Auffällig: W05 0 Belege → bei R4 prüfen.
- Obsidian: Vault = /home/cae/hermes/batterie, Notizen wissen/ (erzeugt, Marker wissen/.erzeugt), Einstieg wissen/Start.md. Obsidian NICHT installiert. wissensnetz.py erzeugt JSON+HTML+Obsidian. B-BAT-002: pruefe.py prüft jetzt jedes Zitat mit (URL); T02 bei R4 neu rechnen (rm forschung/ergebnis/T02.* und lauf.sh werkzeuge T02).
- 13:15 B-BAT-003: Patente P02–P10 Spaltenfehler behoben, alte Ergebnisse im Scratchpad alt_patente/. forschung/nachlauf2.sh rechnet P02–P10 + T02 nach W17.
- Stückliste BAT-DOC-13: pm/bauteile/stueckliste.py → docs/13_stueckliste.md (37 Pos., Mengen aus startwerte.json). Nutzer: heute nur Vorbereitung.
- 13:30 Recherche W01–W17, T01–T09 fertig (T02 neu 4/0, W16 10/0, W17 14/0). Patente P02–P10: Google 503-Sperre, leere Ergebnisse im Scratchpad alt_patente/leer_503; nachlauf3.sh versucht ~15:30 einmal. Nächster Schritt R4 (Opus liest alles) – Nutzer: heute nur Vorbereitung.
- Stückliste im Netzplan: SL1 (fertig), SL2 (vor B1); wissensnetz.json Feld teile + stueckliste. Sonnet baut Anzeige (HTML-Abschnitt/Filter, Obsidian wissen/Teil/).
- TextFold: vom Nutzer verworfen („Nein. Wir nehmen Obsidian.“), nicht installiert. Notizen/Lesehilfe = Obsidian.
- Unternehmenspräsentation eingeplant (Nutzer: „…am Ende eine Präsentation mit raus springt. Das ist eine Unternehmenspräsentation“): REQ-D14, praesentation/STORYBOARD.md (BAT-DOC-14), Bausteine praesentation/bausteine/<Vorgang>.md, Vorgänge B0 (Zielgruppe/Firmenvorlage, offen beim Nutzer) und B5 (erzeuge.py, python-pptx noch nicht installiert). Regel in CLAUDE.md. Hinweis: BAT-DOC-13 doppelt vergeben (Stückliste und Video-Storyboard).
- 2026-11-12 18:00 Nutzer: Patente (P02–P10, 503-Sperre) hinten angestellt.
