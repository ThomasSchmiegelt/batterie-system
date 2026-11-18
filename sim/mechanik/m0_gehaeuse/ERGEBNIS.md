| Dok.-Nr. | ERG-M0 | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Ergebnis M0 Gehäuse-Vorauslegung | Ersteller | Claude Sonnet (KI) | Prüfer | Opus (Stichprobe) |

> **KI-generiert.** Claude Sonnet, 2026-11-17, Auftrag M0. Entwurf, nicht freigegeben. Alle Zahlen aus `sim/mechanik/m0_gehaeuse/ergebnis.json` (aus `eingaben.json` durch `gehaeuse.py`).

## Abgleich ERWARTUNG.md
- 1. Höhe LFP 121 ≤ 130: Ist 121 mm, Rest 9: ERFÜLLT
- 1b. Höhe NMC 111, Rest 19: Ist 111 mm, Rest 19: ERFÜLLT
- 2. Länge LFP ≈ 2030 (Band 2000–2060): Ist 2024 mm (netto 1964, Stapel 1874): ERFÜLLT
- 3. Breite LFP: Rahmen 30, Toleranz 4 je Seite: Ist Zellen 1362, Toleranz 8 gesamt = 4 je Seite: ERFÜLLT
- 4. NMC Plätze 1100–1150, ≥ 868, Länge 1950 reicht: Ist 1120 Plätze (ohne Querträger 1260, Verlust 140), Belegung 78 %: ERFÜLLT; Band 1100–1150: ERFÜLLT
- 5. Masse Querträger 1,5 kg je / 4,5 kg: Ist 1.48 kg je, 4.44 kg gesamt (Querschnitt 400 mm², Länge 1370 mm): ERFÜLLT
- Verfehlt-Kriterien: keines eingetreten

## Masse (Dichte Al 2700, Annahme)
- Querträger: 4.44 kg (3 Stück)
- Platten LFP 187.6 kg, NMC 180.7 kg (Boden 3, Deckel 2, Unterfahrschutz 3, Kühlplatten 2 x 8 mm als Vollmaterial = Obergrenze)
- Seitenrahmen: nur Obergrenze Vollprofil 30 x Höhe: LFP 66.5 kg, NMC 59.7 kg; echte Masse offen

## Offene Punkte
- Seitenrahmen: Wandstärke/Profil ohne Beleg, nur Obergrenze Vollprofil (Breite 30 x Höhe) angegeben, keine Annahme gesetzt
- Zellhalter BT-250 (NMC, Rest Höhe) nicht modelliert
- Seitencrash über Schweller: Autor-Frage offen

Bilder: `draufsicht_LFP.png`, `draufsicht_NMC.png`, `schnitt_LFP.png`, `schnitt_NMC.png`; Lesehilfe `m0_lesehilfe.md`.

*KI-generiert, Entwurf. Dokument ERG-M0, Version 1.0.*
