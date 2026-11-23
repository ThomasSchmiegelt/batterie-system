---
typ: befund
tags: ["befund"]
---
# B-BAT-040

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

Thermik-Varianten K4 und Crash LFP_a neu (2026-11-21, Opus)

Quelle: [[Dokument/BEFUNDE]]

## Vorgänge
- –

## Text aus BEFUNDE.md

- K4, Tabelle T_max/ΔT aus rechnen/log_K4_*.txt, LFP-Schnellladen: V0 42,6/16,4; V1 gegensinnig 38,4/10,5; V2 Durchfluss ×2 37,0/11,1; V3 beides 34,8/8,1. Die Schätzung von Opus vorab (11–12 / 10–11 / 7–8 K) traf. Keine Variante erreicht ΔT ≤ 5 K, daher wird eine Parallelführung mit Z-Verteiler zum Verbesserungsvorschlag. NMC 30 min: V0 34,1/5,9, V3 30,1/1,5. Dauerfahrt: LFP 29,0/3,8, NMC 29,7/3,0.
- X3 LFP_a nach der Korrektur (Nachtrag 3): Pfahl 13,6 mm, Zellblock 6,7 mm, Innenwand 7,8 mm, 472 kN, Energiefehler 0,18 %, max |U| der Zellen 7,4 mm. Opus-Fehler im Kriterium „kinetische Energie am Ende < 5 %“: Darin steckte auch der Rückprall des Pfahls (17,6 %). Neu gilt die kinetische Energie ohne Pfahl, das sind 2,4 %. Modellprüfung bestanden. Das Kennzahlenbild entspricht dem ungültigen Lauf (13,9/8,1 mm), weil die gleitenden Reihen weit vom Pfahl wenig zur Steifigkeit beitrugen.
- Zweiter Fehler: In der untesteten Auswertung von Sonnet war `pw` nicht definiert; bei der Reparatur der Zeile hat Opus den Rest der Zeile in einen Kommentar verschoben. Beides ist behoben, die Auswertung ist an LFP_a getestet.
- X3 LFP_a2 (20 kJ): Pfahl 38,2 mm (Erwartung 50–120 mm verfehlt, steifer), Zellblock 16,1 mm, 657 kN, Energiefehler 0,2 %, max |U| der Zellen 22,2 mm, kinetische Energie 1,5 %, Modellprüfung bestanden. Im Bild ist der Querträger in Packmitte direkt getroffen und trägt ein (Opus, Stichprobe Bild).
