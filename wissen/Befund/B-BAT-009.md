---
typ: befund
tags: ["befund"]
---
# B-BAT-009

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

B-BAT-009 (2026-11-16) Zerlegungsstudie Blade (W20): Gen-1-Zelle 160 Wh/kg, 355 Wh/L; Bauraum Fall A genau an der Grenze

Quelle: [[Dokument/BEFUNDE]]

## Vorgänge
- [[Vorgang/R1|R1]] – Wissensaufbau W01-W15 (Chemie, Zelltypen, Spannung, Kabel, Steuerung, Struktur)
- [[Vorgang/R4|R4]] – Recherche prüfen: Zitate, Aussagen, Widersprüche -> BEFUNDE
- [[Vorgang/V1|V1]] – Lastenheft-Werte REQ-P01..P08 vorschlagen (Fahrzeug, kWh, Spannung, Leistung, Laden, Chemie, Bauraum, Temperatur)
- [[Vorgang/G1|G1]] – Zellmaße als ENT-Akten (aus W03/W08/P01, sonst Annahme)

## Text aus BEFUNDE.md

- Quelle: Cell Rep. Phys. Sci. 6, 102453 (2025), CC-BY, PDF vom Autor in quellen/blade_zerlegung/. PI-Lauf W20: 0/21, weil PI die DOI statt der file://-URL angab. Opus: URL ersetzt → 17/21; die 4 Reste stehen im Fließtext (pdftotext ohne -layout, zweispaltiger Satz). Z25 („around 23 of the heat“) gesperrt: Bruch bei der Textumwandlung verloren.
- **Blade-Zelle (gemessen, Tabelle 1):** 135 Ah, 432 Wh, 3,2 V, Fenster 2,6–3,65 V, 2,7 ± 0,3 kg, 1216 mL, **160 Wh/kg, 355,3 Wh/L**, 965 × 90 × 14 mm, Wandstärke Gehäuse 0,3 mm, ein Z-gefalteter Elektrodenstapel, Aktivmasse etwa 60 % der Zellmasse. Zum Vergleich Tesla 4680 (NMC811): 241 Wh/kg, 643 Wh/L.
- **Folge Bauraum:** 355 Wh/L × 60 % Volumennutzung (W19) = 213 Wh/L Pack. Nötig: 214 (Fall A), 256 (Fall B). Fall A passt knapp, Fall B nicht. Prüfpunkt von ENT-005 damit **an der Grenze, nicht klar erfüllt**.
- **Folge Masse:** 160 Wh/kg liegt unter dem C0-Band 185–210 (W03, Hersteller, Long Blade 2.0). Mit 160 Wh/kg, Zellanteil 0,75: Packmasse Fall A 616 kg (543–711), Fall B 739 kg. Eine 4680-NMC-Zelle ergäbe Fall A etwa 409 kg. Der Satz „kein belegter Massenunterschied“ (B-BAT-006) gilt nur mit den Herstellerwerten der 2. Generation.
- Folge 800 V (ENT-006): Eine Original-Blade-Zelle (135 Ah) gäbe 250s × 135 Ah × 3,2 V = 108 kWh. Nötig 92 Ah (A) → bei gleichem Querschnitt etwa 660 mm statt 965 mm Länge (G1).
- Werkzeuglücke: lauf.sh/AUFTRAG muss PI die genaue Quell-URL vorgeben; pruefe.py scheitert an zweispaltigem PDF-Satz (pdftotext -layout). Vorgang: [R4] [C0] [G1] [V1]
