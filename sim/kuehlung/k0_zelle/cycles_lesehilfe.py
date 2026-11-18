#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. Auftrag K0-R. Erzeugt bilder/cycles_lesehilfe.md (alle Zahlen aus ergebnis.json)."""
import json, os
H = os.path.dirname(os.path.abspath(__file__)); E = json.load(open(f"{H}/ergebnis.json")); ZT = E["ziel_T_max_C"]; VMAX = E["farbskala_max_C"]
KOPF = """| Dok.-Nr. | LH-K0C | Version | 0.1 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Lesehilfe zu den Cycles-Temperaturbildern K0 | Ersteller | Claude Sonnet (KI), Auftrag Opus | Prüfer | – (Opus offen) |

> **KI-generiert.** Entwurf, nicht vom Menschen freigegeben. Quelle aller Zahlen: `sim/kuehlung/k0_zelle/ergebnis.json`. Ersetzt die Workbench-Bilder `render_*` (Vorstufe, Dateien bleiben).
"""
SCHN = {"LFP_K1_L2": "LFP-Zelle in echter Proportion (681 × 90 × 14 mm), halbe Dicke weggeschnitten: man blickt schräg von vorn-oben auf die Schnittfläche. Unten die Kühlplatte (graue Platte, nur angedeutet, Annahme). Der cyanfarbene Rahmen markiert die Lupe (links unten), die die Schnittfläche am Boden vergrößert zeigt.",
        "NMC_K1_L2": "NMC-Rundzelle 4680, ein Viertel weggeschnitten, Blick leicht von oben. Die durchsichtige Hülle zeigt, wo das weggeschnittene Viertel des Bechers saß. Unten die Kühlplatte (angedeutet, Annahme).",
        "NMC_K2_L2": "NMC-Rundzelle 4680, ein Viertel weggeschnitten, Blick leicht von oben. Das Kühlband (grau) liegt rechts hinten am Mantel (25 % des Umfangs), nur zum Vergleich."}
B = [KOPF]
for f, txt in SCHN.items():
    for t in (0, 300, 600, 900, 1200):
        T = E["faelle"][f]["T_max_t_C"][t // 10]
        B.append(f"**Lesehilfe zu `cycles_{f}_t{t:04d}.png`** {f.replace('_', ' ')} nach {t} s ({t/60:.0f} min) Schnellladen, T_max = {T:.1f} °C. {txt} Farbe = Temperatur (Skala 25–{VMAX:g} °C, in allen Bildern gleich): dunkel/violett kühl, orange/gelb heiß. Cyan an der Farbskala = Vorgabe {ZT:g} °C (REQ-P09). Annahmen: Kühlmittel 25 °C, h = 500 W/(m²·K). Die Farben sind mit leichter Schattierung gerendert, damit die Form lesbar ist; die Temperatur ist an der Farbe auf etwa ±1 K ablesbar, an stark schattierten Flächen etwas ungenauer.\n")
B.append(f"**Lesehilfe zu `tafel_L2.png`** Bildtafel: drei Zeilen (LFP K1, NMC K1, NMC K2), fünf Spalten (t = 0, 300, 600, 900, 1200 s), gemeinsame Skala 25–{VMAX:g} °C, Vorgabe {ZT:g} °C cyan an der Skala. So sieht man, wie sich die Zellen beim Schnellladen erwärmen und wo es heiß wird. Quelle: `ergebnis.json`.\n")
B.append("Videos (MP4, 41 Bilder, 8 Bilder/s) mit derselben Darstellung: `cycles_LFP_K1_L2.mp4`, `cycles_NMC_K1_L2.mp4`, `cycles_NMC_K2_L2.mp4`. Gerendert mit Blender Cycles (nur CPU), Temperaturen aus den Elmer-Ergebnisdateien (`elmer/fall_*/case_t*.vtu`).\n\n---\n*KI-generiert (Claude Sonnet), Entwurf, nicht vom Menschen freigegeben.*\n")
open(f"{H}/bilder/cycles_lesehilfe.md", "w").write("\n".join(B))
