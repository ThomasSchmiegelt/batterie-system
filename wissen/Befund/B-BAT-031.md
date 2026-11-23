---
typ: befund
tags: ["befund"]
---
# B-BAT-031

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

B-BAT-031 (2026-11-18) X1b/X2 OpenCourant: Knautschprofil bringt kaum Reserve, die Rahmen-Innenwand gibt zuerst nach

Quelle: [[Dokument/BEFUNDE]]

## Vorgänge
- [[Vorgang/X1|X1]] – Seitencrash Pfahl, quasistatisch: Eindringung in Gehäuse/Querträger (CalculiX, plastisch, Kontakt)
- [[Vorgang/X2|X2]] – Seitencrash dynamisch (OpenRadioss, Installation nur nach Freigabe)

## Text aus BEFUNDE.md

- Explizit (OpenCourant latest-20261011), Pfahl 1500 kg mit 5 kJ. Energie bis zur Zellberührung (4 mm):

  | Variante | Energie | Anteil an 5 kJ |
  |---|---|---|
  | LFP w15 | 416 J | 8 % |
  | LFP w20 | 455 J | 9 % |
  | LFP w30 | 568 J | 11 % |
  | NMC w20 | 523 J | 10 % |

- Eindringung 49–52 mm, Energiefehler ≤ 0,01 %. Gegenprüfung mit CalculiX bei 2 mm: +7…14 %.
- **Deutung (Opus):** Das Profil staucht mit ≈ 80 kN. Diese Kraft biegt die Innenwand zwischen den Querträgern (Spannweite ≈ 500 mm) schon, bevor das Profil zusammengefaltet ist. Mehr Breite w hilft daher kaum, von 15 auf 30 mm sind es nur +37 %.
- 5 kJ bei 80 kN brauchen etwa 60 mm Weg. Das ist bei fester Breite nicht unterzubringen.
- **Folge:** Eine Knautschzone im Pack lohnt sich nicht (LFP −2,4 % Energie für +10 % Reserve). Der Seitencrash bleibt beim Schweller (ENT 2026-11-17). Wer Reserve will, braucht eine steifere Innenwand bzw. engere Querträger, als eigene Studie.
- **Werkzeug:** /RFILE-Zwischendateien in OpenCourant latest-20261011 nicht lesbar (Segfault). Der Neustart läuft über 10 Abschnitte (Vergleich 0 Abweichung). Opus-Fehler in ERW-X1b: Erwartung ab w 20 mm, 5 kJ, ohne die Rahmenbiegung zu bedenken. Vorgang: [X1] [X2]
