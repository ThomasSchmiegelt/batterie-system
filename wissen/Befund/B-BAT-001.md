---
typ: befund
tags: ["befund"]
---
# B-BAT-001

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

B-BAT-001 (2026-11-12) PI-Recherche W01 (LFP): Stufe B funktioniert, Zitatprüfung 12/14

Quelle: [[Dokument/BEFUNDE]]

## Vorgänge
- [[Vorgang/R1|R1]] – Wissensaufbau W01-W15 (Chemie, Zelltypen, Spannung, Kabel, Steuerung, Struktur)
- [[Vorgang/R4|R4]] – Recherche prüfen: Zitate, Aussagen, Widersprüche -> BEFUNDE
- [[Vorgang/C2|C2]] – Zellmodell LFP (PyBaMM Prada2013) auf langes Format skalieren

## Text aus BEFUNDE.md

- Erster PI-Lauf im Projekt: 4 min 15 s, 0 Werkzeugaufrufe, keine Links außerhalb des Pakets.
- pruefe.py: zuerst 11 bestätigt / 3 Fehler. Opus am Rohtext (recherche_ablage/926e09b6d3b5.txt, pakete/W01.md): alle 3 Werte stehen in der Quelle, nichts erfunden.
  Ursache 1: Wikipedia-Abruf setzt Link-Adressen „[https://…]“ in den Satz, PI lässt sie weg → pruefe.py ignoriert sie jetzt auf beiden Seiten (Skill web-recherche, auch Fusion). Danach 12/2.
  Ursache 2 (bleibt Fehler, zu Recht): PI kürzt Zitate („(Wh/kg)“ fehlt) bzw. zieht Infobox-Zeilen zusammen.
- Inhaltlich: Werte korrekt übernommen (3,2 V nominal; 3,60–3,65 V Ladeschluss; 2,0–2,8 V Entladeschluss; 95–172 Wh/kg; 2 500–9 000 Zyklen; Kälte: 141,8 / 92,7 / 57,9 / 46,7 mAh/g bei 23 / 0 / −10 / −20 °C).
  Schwächen: Bezeichnung „Spezialeistung“ statt spezifische Kapazität; 12-V-Folgerung für ein Fahrzeug-HV-Pack unerheblich; 66 %/33 % selbst gerechnet (richtig: 65 %/33 %), ohne Kennzeichnung.
- Folge: Ergebnisse brauchen weiter die Lesung durch Opus (R4); pruefe.py allein reicht nicht. Vorgang: [R1] [R4]
