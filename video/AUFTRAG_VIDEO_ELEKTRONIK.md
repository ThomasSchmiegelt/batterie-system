# Auftrag: Drittes Video „Batterie, Nachverfolgung, Normen, Elektronik“ (REQ-D13, BAT-DOC-13c)

KI-generiert (Claude Opus, 2026-11-25). Vorgabe des Autors (wörtlich): „in dem video soll wieder die batterie sichtbar sein aber auch das ganze zeugs aus nachverfolgung und normung, requirements soll sichtbar sein und natürlich ein focus auf die elektronikbauteile.“ Kolibri 1 schreibt Storyboard und Texte (Modelltest, docs/26). Die Videos `abschluss.mp4` und `abschluss_wissen.mp4` bleiben unverändert.

## Arbeitsteilung
| Wer | Was | Ausgabe |
|---|---|---|
| Haiku | Daten für die Einblendungen, nur aus den Quellen | `video/elektronik/daten.json` |
| Kolibri (PI, über Sonnet) | Storyboard mit Szenen, Dauer und Einblendtexten (≤ 12 Wörter je Tafel), nur aus daten.json | `video/elektronik/STORYBOARD_kolibri.md` |
| Sonnet | Szenen bauen (Blender und Pillow/matplotlib), rendern, schneiden | `video/elektronik_nachverfolgung.mp4` |
| Opus | Storyboard freigeben, Standbilder prüfen | – |

## Inhalt (≈ 120–150 s, 1280×720, 25 fps)
1. **Batterie** (≈ 20 s): Pack LFP oder NMC aus dem vorhandenen Render-Ablauf (`szenen.py` bzw. `cad/pack/render_pack.sh`), Deckel geht auf, die CMU leuchten in den Endzonen.
2. **Anforderungen** (≈ 20 s): REQ-Liste als Tafel (Nummer, Kurztitel, Wert, Status). Hervorgehoben sind REQ-P15, P17…P21.
3. **Nachverfolgung** (≈ 25 s): Kette Anforderung → Entscheidung (ENT) → Bauteil (BT) → Nachweis (Rechnung/Bild) für 3 Beispiele aus der Elektronik, z. B. REQ-P18 → ENT-192 → BT-323 → FMEDA E3d. Als wachsender Graph aus `pm/graph/graph.json`.
4. **Normen** (≈ 15 s): Normentafel aus docs/07 mit IEC 60664-1, ISO 26262, CISPR 25, UN R100/R94/R135, EU 2023/1542. Markiert, welche als Text vorliegen und welche kostenpflichtig sind.
5. **Elektronik im Fokus** (≈ 45 s):
   - CMU-Platine 3D mit Leiterbahnen, Explosionsansicht nach Lagen, Nahaufnahme Ausgleichskanal
   - Schaltplanblatt Kanal
   - BMS-Platine mit roter HV/NV-Sperrzone
   - Schaltplanblatt Schütz
   - SPICE-Kurven (Vorladung, Schütz)
   - FMEDA-Balken mit Zielband
   - HARA-Sicherheitsziele SG-01…08 mit ASIL
   - Quellen: vorhandene PNG in `sim/elektrik/e3_platine`, `e3c_bms_platine`, `e3d_fmeda` sowie STEP für neue Blender-Kamerafahrten (cae_projekte/batterie/abgabe_2026-11-24)
6. **Schluss** (≈ 10 s): Zahlen auf einen Blick (Teile, DRC 0, SPFM, Masse). Unten „Thomas Schmiegelt“ wie in den anderen Videos.

## Regeln
- Jede Zahl im Bild aus daten.json mit Quellpfad. Was Kolibri erfindet, fliegt raus (Sonnet prüft gegen daten.json).
- Der Autor heißt Konstrukteur, nicht Ingenieur. Vermerk „KI-generiert“ im Abspann.
- Neue Blender-Szenen: vor dem Rendern `bash rechnen/gpu_warten.sh`. Renderzeit vorher nennen; über 1,5 h → Opus. Einzelbilder nach `/home/cae/cae_projekte/batterie_video/elektronik/`. Fertige Bilder werden übersprungen.
- Skript `video/erzeuge_video_elektronik.sh [daten|storyboard|render|zusammen|alles]`.
- Begleittext `video/begleittext_elektronik.md` (BAT-DOC-13c), Register in docs/00, eine Zeile in docs/08, Kolibri-Läufe ins Monitoring (`forschung/modelltest/monitoring.csv`, thema video_*).

## Prüfung
8 Standbilder ins Scratchpad und ansehen: je Szene 1, dazu das letzte Bild. Prüfen: Lesbarkeit der Tafeln (Schrift ≥ 22 px), nichts abgeschnitten, Zahlen = daten.json.

## Nachtrag 1: neue Dramaturgie (Autor 2026-11-25, ersetzt die Reihenfolge der Szenen 1–6)
Wörtlich: „vielleicht beginnt das video mit den requirements, dann wächst langsam der wissensgraph, dann erscheint das blade, das gesamte paket, dann entstehen die steuergeräte … und am ende ist die batterie fertig und verschwindet wieder und nur der wissensgraph bleibt. es wäre schön berechnungen zu sehen.“
1. **Anforderungen** erscheinen als Tafel (REQ-Liste, Normen dazu).
2. **Wissensgraph wächst** im Hintergrund (vorhandenes `video/graph_zeitraffer.py` wiederverwenden). Er wächst während des ganzen Films weiter.
3. **Zelle** (LFP prismatisch, „Blade“) erscheint vor dem Graphen. Kurz eingeblendet die Zellrechnung (Bilder aus sim/chemie).
4. **Gesamtes Pack** baut sich auf. Eingeblendet: Kühlung (sim/kuehlung, z. B. K3/K4) und Crash (sim/mechanik X3), je 3–4 s als Bild-in-Bild.
5. **Steuergeräte entstehen:**
   - CMU-Platinen in den Endzonen und die BMS-Platine in der Schaltbox
   - Explosion nach Lagen, Schaltplan
   - Rechnungen: SPICE (Vorladung, Schütz), Elmer-Wärme E3b, FMEDA
   - Nachverfolgungsketten REQ → ENT → BT → Nachweis als Hervorhebung im Graphen
6. **Batterie fertig**, kurzer Halt mit Zahlen. Dann wird sie durchsichtig und verschwindet (wie `abschluss_wissen`), **nur der Graph bleibt** stehen. Unten „Thomas Schmiegelt“.
Rechnungsbilder nur vorhandene PNG mit Zielband. Jedes Bild ≥ 3 s, Quelle klein in der Ecke. Länge darf auf ≈ 150–180 s wachsen. Renderzeit über 1,5 h → Opus.
