---
typ: befund
tags: ["befund"]
---
# B-BAT-015

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

B-BAT-015 (2026-11-17) Innenaufbau beider Zellen aus der Zerlegung; Korrektur LFP-Länge 681 mm; Bauraumbreite 1430 mm

Quelle: [[Dokument/BEFUNDE]]

## Vorgänge
- [[Vorgang/C1|C1]] – ERWARTUNG Zellmodell (Entladekurve, Wärme, Innenwiderstand)
- [[Vorgang/G1|G1]] – Zellmaße als ENT-Akten (aus W03/W08/P01, sonst Annahme)
- [[Vorgang/G2|G2]] – Parametrische Zelle FreeCAD (liest parameter.json)

## Text aus BEFUNDE.md

- Autor: „kann man die zellen weiter detailieren ist die nmc nicht eine gewickelte folie? Isolatoren und so müssten ja auch noch rein. auch eine LFP sollte detailiertzer dargestellt werden“.
- Opus liest W20 Tabelle 1, Abb. 2 (alle Innenbauteile), Abb. 4 (Kontaktierung), Abb. 5 (Elektrodenmaße) → cad/zelle/aufbau_W20.json. Werte aus Abbildungen sind von Opus abgelesen (pruefe.py kann Bilder nicht prüfen). Tabelle 1: Einheit „mm“ ist µm (Satzfehler; Probe: Blade-Stapel 38 × 160 + 39 × 140 + 78 × 12 µm = 12,5 mm bei 14 mm Zelle).
- **Eigener Fehler gefunden:** ENT-015 (660 mm) skalierte die Endzone mit. Elektrode 899,5 von 965 mm → Endzone 65,5 mm bleibt fest → **681 mm**. Zwei Reihen 1362 mm > 1340 mm innen → Autor wählt Bauraumbreite **1430 mm** (ENT-030, entschieden). ENT-015 korrigiert (vorgeschlagen).
- 4680-Wickel: Kathode 3215 × 72 mm, Anode 3305 × 73, Separator 2 × 3550 × 75; Wickeldicke je Windung ≈ 0,45 mm → ≈ 34 Windungen, Kern Ø ≈ 14 mm (**abgeleitet, nicht gemessen**).
- Baum: BT-111 Kathode, 112 Anode, 113 Separator, 114 Isolierrand, 115 Wickelkern [NMC], 116 Fixierung/Isolationsbeutel, 121 Gehäusefolie [LFP], 122 Füllöffnung, 131 Stromschiene/Tab-Scheibe, 132 Polisolation; BT-140 lage. 60 Einträge (ENT-031). Akten ENT-032…080 vorgeschlagen.
- Unsicher: Bedeutung der Fahnenmaße in Abb. 5A (27,1/9 bzw. 20,5/7 mm). Vorgang: [G1] [G2] [C1]
- **Nachtrag Detailmodell (Sonnet, 2026-11-17, `cad/zelle/entwurf/detail/ERGEBNIS_detail.md`):** 4680-Wickel aus den Akten (Kern Ø 14 mm, 0,45 mm je Windung, Bandlängen 3215/3305/3550 mm) ragt 1,15 mm über den Becher (Außenradius 23,75 mm gegen 22,60 mm innen; Kathode 34,5 Windungen, endet bei 22,68 mm). Erwartung „Außenradius ≤ 22,6 mm“ verfehlt, offen an Opus (Verdichtung oder Kern?). LFP-Stapel 12,476 mm in 13,4 mm: erfüllt.
