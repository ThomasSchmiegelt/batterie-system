---
typ: befund
tags: ["befund"]
---
# B-BAT-005

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

B-BAT-005 (2026-11-16) R4: Recherche geprüft, kein erfundener Wert, ein Spaltenfehler (PI), Wh/L-Frage bleibt offen

Quelle: [[Dokument/BEFUNDE]]

## Vorgänge
- [[Vorgang/R1|R1]] – Wissensaufbau W01-W15 (Chemie, Zelltypen, Spannung, Kabel, Steuerung, Struktur)
- [[Vorgang/R2|R2]] – Werkzeuge T01-T07 (Open Source Zellchemie, Elektroauslegung, Ersatzmodelle)
- [[Vorgang/R4|R4]] – Recherche prüfen: Zitate, Aussagen, Widersprüche -> BEFUNDE
- [[Vorgang/C2|C2]] – Zellmodell LFP (PyBaMM Prada2013) auf langes Format skalieren
- [[Vorgang/C5|C5]] – Alterung (Zyklen, Kalender) und Vergleich NMC / Natrium-Ionen
- [[Vorgang/U1|U1]] – ERWARTUNG Ersatzmodell: Zielgröße, Gültigkeitsbereich, Mindestgüte (z. B. Rangkorrelation)

## Text aus BEFUNDE.md

- Vorprüfung Sonnet (forschung/R4_vorpruefung.md, 5 min): 22 FEHLT-Zeilen = 21 Wortlaut abweichend, Wert im Rohtext / 0 Wert fehlt im Rohtext / 1 unklar (T07 Z7, ohne Zahl). Erwartung „keine erfundenen Zahlen, Wortlautfehler wie B-BAT-001“: erfüllt.
- Opus-Stichprobe an pakete/: W02 Z12 („100 to 250 W·h“ steht in Infobox, Zeile 94) ✓. W01 Z15 („Next gen: 180–205 Wh/kg“, Zeile 9) ✓. **W06 Z22 falsch zugeordnet:** Rohtext (Zeilen 10–18) Kopf „Li-NMC | LFP | …“, erster Block 150-275 / 150-220 / 165 = NMC, zweiter Block 80-150 / 210 / 90-160 / 135 = LFP. PI gab 150–220 als LFP aus (Fehler eines lokalen Agenten, Tabelle mit verlorenen Spaltengrenzen).
- W01 Z16 „LFP 227–396 Wh/L“: Rechenkommentar im Rohtext `3.96/((1.85/2)^2*3.14159*6.495/1000)` = 18650-Rundzelle. Für das Blade-Format gibt es keinen Wh/L-Wert. Die Chemiewahl LFP/NMC (B-BAT-004 Punkt 4) bleibt unbelegt.
- Ergebnis: forschung/R4_ergebnis.md (verwendbare Werte mit Bauteil/Merkmal, gesperrte Werte, Lücken mit Weg). Neue Quelle: Zerlegungsstudie Blade/4680 (doi:10.1016/j.xcrp.2025.102453, CC-BY), automatisch nicht abrufbar. Thema W18 (314-Ah-LFP-Zelle, thermisch) gestartet.
- Folge für PI-Aufträge: Tabellen ohne Spaltengrenzen sind fehleranfällig. pruefe.py findet das nicht, weil der Wert im Text steht. Vorgang: [R4]
