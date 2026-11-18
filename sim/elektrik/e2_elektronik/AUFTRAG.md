| Dok.-Nr. | Auftrag E2 | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Elektronik und Kabel: Rechnung, CAD, Render, Schaltbild | Ersteller | Claude Opus (KI) | Prüfer | Opus (Stichprobe) |

> KI-generiert, Opus → Sonnet. Erwartung und Annahmen: ERWARTUNG.md (nicht ändern, keine eigenen Annahmen; fehlt etwas → als offene Frage melden). `source umgebung.sh`, CPU, nice. Bestehende Pack-Skripte `cad/pack/` erweitern, nicht ersetzen; Maße aus parameter_<V>.json bzw. für E2 aus `sim/elektrik/e2_elektronik/eingaben.json` (Annahmen mit Herkunft „ERW-E2“).
1. `eingaben.json`, `elektronik.py`: Punkte 1–4, 6, 7 der Erwartung je Variante → `ergebnis.json`, `ERGEBNIS.md` (Abgleich-Tabelle).
2. CAD (FreeCAD, `cad/pack/pack.py` mit Schalter E2): Schaltbox mit Schützen, Sicherung, Shunt, BMS-Platine; CMU-Platinen auf den Zellreihen; FPC-Messleitungen; HV-Leitungen intern (Reihenenden → Service-Trennstecker → Schaltbox → HV-Stecker) mit Biegeradius aus Akte BT-430; NV-Stecker, Gas-/Drucksensor. **Beide Einbaufälle a und b**, Kollisionsprüfung, Längen-/Höhenzuwachs und Masse → `ergebnis.json`.
3. Bilder (Blender Cycles CPU, wie `render_pack.sh`; Elektronik farbig hervorgehoben, Rest grau-transparent): je Variante Gesamt, Draufsicht Kabelweg, Schnitt durch die Schaltbox, Detail CMU + FPC an den Zellen; dazu `schaltbild_<V>.png` (Blockschaltbild HV/NV mit Schützen, Vorladung, Sicherungen, Trennstecker, Isolationswächter, Messkette; matplotlib) und `kabelplan_<V>.png` (Draufsicht, Leitungen mit Querschnitt und Länge beschriftet). Lesehilfe `lesehilfe.md`, Baustein `praesentation/bausteine/E2.md`.
Große Dateien (FCStd, STEP, blend) nach /home/cae/cae_projekte/batterie/e2/ mit Link. ≤ 120 min. Rückgabe ≤ 5 Zeilen. → OPUS bei Kollision, Verfehlt-Fall oder fehlendem Maß.

## Fortsetzung 2026-11-18 (Opus → Sonnet)
Antworten auf deine Fragen: 1–3 siehe ERWARTUNG Nachtrag 1 (Maße, Biegeradius 5×D, Lage). 4: 139 A gilt. 5: Höchstspannung LFP 3,65 V, NMC 4,2 V. Damit CMU-Wärme in `elektronik.py` zusätzlich rechnen. 6: gedeutet (Nachtrag 1). Einbauort Schaltbox: **Fall b, ENT-109 entschieden**. Fall a nicht bauen.
Schritte:
1. Akten: Für jede Zeile der Annahmen-Tabelle und von Nachtrag 1, deren Merkmal in `struktur.json` existiert, `python3 pm/pm.py neu …` aufrufen. Status „vorgeschlagen“, wer „Opus (Annahme ERW-E2)“, belege [B-BAT-024]. Ein fehlendes Merkmal nicht anlegen, sondern in der Rückgabe auflisten. Danach `pm.py pruefe` mit 0 Fehlern und `pm.py register`.
2. `cad/pack/entwurf_parameter.py`: die E2-Maße aus den Akten lesen (entschieden + vorgeschlagen). Was ohne Akte bleibt, als A_* mit Herkunft „ERW-E2 N1“.
3. Auftrag oben, Punkte 2–3 (CAD, Kollision, Bilder) nur für Fall b. Dazu: Schaltbild (schemdraw oder matplotlib, PNG) und Kabelplan (Tabelle von/nach/Länge/Querschnitt in ERGEBNIS.md). Lesehilfe und Folienbaustein `praesentation/bausteine/E2.md`. ERGEBNIS.md auf Version 0.2.
Abbruch → OPUS: Kollision, Leitung längs durch das Pack, Höhenzuwachs > 120 mm, fehlendes Maß.

## Fortsetzung 2 (2026-11-18, Opus → Sonnet)
Autor: Schaltbox als Turm am **hinteren** Packende unter der Rücksitzbank (ENT-144 ersetzt ENT-109). Packhöhe dort 210 mm ist erlaubt.
1. Akten mit `pm.py neu` anlegen. Status vorgeschlagen, wer „Opus“, belege [B-BAT-024]:
   - (a) BT-200 verschaltung = „maeander“. Reihen abwechselnd hin und zurück, so dass Plus, Minus und Mitte (Service-Trennstecker) in der hinteren Endzone liegen. Geht das bei der Reihenzahl nicht: melden und nicht bauen.
   - (b) Ausgleichsstrom NMC 130 mA, ersetzt ENT-115 nur für NMC: ENT-115 auf variante [LFP] setzen. Begründung: CMU-Wärme 11,34 W bei 4,2 V → ≈ 9,8 W; Ausgleich ≈ 14 h.
   - (c) LFP bauraum_laenge_mm 2050, ersetzt ENT-091 für LFP. Begründung: CMU hochkant in beiden Endzonen, je +10 mm. NMC bleibt.
2. CAD: Box hinten. CMU hochkant in den Endzonen (LFP nach (c), NMC passt mit 41,6 mm). Dazu FPC, HV intern nach (a), Kollisionsprüfung.
3. Renders wie im Auftrag, Kabelplan (Tabelle + kabelplan_<V>.png), Messleitungslänge, HV-Verlust, Elektronikmasse. ERGEBNIS.md v0.3, Baustein E2 nachführen.
Abbruch → OPUS wie oben.

## Fortsetzung 3 (2026-11-18, Opus → Sonnet)
Grundlage ist ERWARTUNG Nachtrag 2. ENT-138 hat Opus auf deckel_hinten gesetzt.
1. Akten anlegen, Status vorgeschlagen:
   - (a) LFP verschaltung „schleife_2reihen“: Plus und Minus hinten, Mitte und Trennstecker vorne. ENT-145 auf variante [NMC] lassen.
   - (b) FPC-Breite LFP 16 mm.
   - Wenn es kein Merkmal dafür gibt: als A_* mit Herkunft „ERW-E2 N2“ und auflisten.
2. CAD:
   - LFP: HV intern und Trennstecker vorne mit Deckelöffnung. FPC 16 mm, bis 4 Lagen je Spur.
   - NMC: Brücken der Gruppenverbinder an den Wendestellen des Mäanders. Die Verguss-Aussparung für die CMU setzen.
   - Dann Kollisionsprüfung.
3. HV-Leitungsmasse mit Cu 8,96 g/cm³. Schaltbild auf v0.3 bringen. Renders und Kabelplan neu. ERGEBNIS.md v0.4 mit Abgleich gegen Nachtrag 2. Baustein E2 nachführen.
Abbruch → OPUS wie oben.
