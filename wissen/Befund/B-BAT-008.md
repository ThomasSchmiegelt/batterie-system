---
typ: befund
tags: ["befund"]
---
# B-BAT-008

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

B-BAT-008 (2026-11-16) W19 geprüft; Energiewiderspruch Stückliste 112 kWh gegen 73,9 kWh

Quelle: [[Dokument/BEFUNDE]]

## Vorgänge
- [[Vorgang/R1|R1]] – Wissensaufbau W01-W15 (Chemie, Zelltypen, Spannung, Kabel, Steuerung, Struktur)
- [[Vorgang/V1|V1]] – Lastenheft-Werte REQ-P01..P08 vorschlagen (Fahrzeug, kWh, Spannung, Leistung, Laden, Chemie, Bauraum, Temperatur)
- [[Vorgang/G1|G1]] – Zellmaße als ENT-Akten (aus W03/W08/P01, sonst Annahme)
- [[Vorgang/G3|G3]] – Verschaltung sS/pP aus Spannung und Energie festlegen (ENT)

## Text aus BEFUNDE.md

- W19 (drpress HSET 2022, Studentenarbeit, Sekundärquelle): 20/20 Belege wörtlich bestätigt, inhaltlich schwach. **Gesperrt:** 332 Wh/kg „BYD battery“ (für LFP unplausibel, Bezug fehlt), 155 Wh/100 km Model Y (Einheit falsch), „ordinary 250 Wh/kg“ (Chemie offen), 180 Wh/kg „blade battery“ (Zelle oder Pack unklar). **Als Hinweis verwendbar (Pack, Sekundärquelle):** Volumennutzung Blade-Pack bis 60 %, konventionell etwa 40 %; Zelle ca. 0,6 m × 13,5 mm (Short Blade); Pack BYD Han ca. 79 kWh.
- Folge für den Bauraum: Bei 60 % Volumennutzung braucht die Zelle 357 Wh/L (Fall A) bzw. 427 Wh/L (Fall B). Das ist jetzt die Prüfgröße für die Blade-Zelle (Volumen Long Blade 1,166 L aus W03-Maßen). Die Blade-Kapazität (Ah) und damit die Wh/L der Zelle ist weiter **nicht belegt**.
- Sonnet-Umstellung (pm/AUFTRAG_LFP_UMSTELLUNG_ergebnis.txt): startwerte.json chemie = LFP (ENT-005 vor Bauraumregel), Warnung Bauraum offen; Obsidian 49 Bauteilnotizen (struktur.json hat 49 Einträge inkl. BT-000 und Baugruppen; die Zahl „46“ in früheren Notizen ist falsch). Opus geprüft: startwerte.json, docs/13, wissen/Bauteil, pm.py pruefe 0 Fehler.
- **Widerspruch:** Stückliste 250s × 1p × 3,2 V × 140 Ah = 112,0 kWh gegen Bedarf 73,9 kWh (+51 %). Die 140 Ah sind eine Annahme aus stueckliste.py. Bei 800 V und 1p bräuchte die Zelle 92 Ah, bei 400 V (125s) 185 Ah. Das ist eine Auslegungsfrage (Systemspannung und Zellgröße, G1/G3), dem Autor vorzulegen. Vorgang: [G1] [G3] [V1]
