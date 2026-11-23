| Dok.-Nr. | ERW-G1 | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Erwartung G1-Vorprüfung: Zellanordnung beider Varianten im Bauraum 1900 × 1400 × 130 mm | Ersteller | Claude Opus (KI) | Prüfer | – (Mensch offen) |

> **KI-generiert.** Vor der Rechnung festgelegt. Eingaben `eingaben.json`. Vorgang G1 (Vorprüfung vor den Zellmaß-Akten), REQ-P03/P06.

## Erwartung
1. **LFP Fall A:** Zelle 92,4 Ah → Länge etwa 660 mm. Zwei Reihen quer (2 × 660 = 1320 mm ≤ 1340 mm innen). Je Reihe 125 Zellen × 15 mm = 1875 mm > 1840 mm innen → **passt knapp nicht** bei 1 mm Abstand; mit 0,5 mm (1812 mm) passt es. Höhe 90 + 30 = 120 ≤ 130 mm passt.
2. **LFP Fall B:** 111 Ah → etwa 790 mm. Zwei Reihen quer passen nicht (1580 > 1340). Gedreht (Länge in Fahrtrichtung): 2 Reihen × 790 = 1580 ≤ 1840, je Reihe 125 Zellen × 15 = 1875 mm quer > 1340 → passt nicht. **Fall B passt nicht** (wie die Wh/L-Rechnung C0b).
3. **NMC Fall A:** Teilung 48 mm; Innenfläche 1840 × 1340 mm. Etwa 38 Zellen je Reihe, 32 Reihen → etwa 1200 Plätze ≥ 868 → **passt mit Reserve** (rund 70 % der Plätze belegt). Höhe 80 + 30 = 110 mm, 20 mm frei.
4. **NMC Fall B:** 1085 ≤ etwa 1200 → passt knapp.
5. Stärkste Annahme bei LFP: Zellabstand und Rand. Bei NMC: Zellabstand.

## Verfehlte Erwartung
- LFP-Länge Fall A außerhalb 640–680 mm.
- NMC-Plätze außerhalb 1100–1300.
- Ein Ergebnis „passt“ für LFP Fall B.

## Nachtrag 2026-11-17: Lauf 2 mit Bauraumlänge 1950 mm (ENT-013), vor der Rechnung
- LFP A: innen 1890 mm, Stapel 1874 mm → **passt** mit etwa 16 mm Reserve; mit Zellabstand 2 mm (Bandende) nicht mehr (1998 mm).
- LFP B: passt weiterhin nicht (Breite: 2 × 831 mm > 1340 mm; gedreht Stapel 1874 > 1340).
- NMC: Plätze steigen um etwa 1 Reihe in L-Richtung je Reihe (≈ 32 Plätze) auf etwa 1230; Belegung A ≈ 70 %, B ≈ 88 %.
- Verfehlt, wenn LFP A „passt nicht“ oder LFP B „passt“.

## Nachtrag 2026-11-17: Lauf 3 mit Endzone 65,5 mm und Bauraum 1950 × 1430 mm (ENT-015 korrigiert, ENT-030), vor der Rechnung
- LFP A: Zelle 681 mm; zwei Reihen quer 1362 ≤ 1370 mm innen → passt, Reserve B ≈ 8 mm; L unverändert 1874 ≤ 1890 (16 mm).
- LFP B: Zelle ≈ 840 mm → passt weiter nicht.
- NMC: etwa eine Reihe mehr (≈ 1270 Plätze), Belegung A ≈ 68 %.
- Verfehlt, wenn LFP A nicht passt.

## Anforderung (Nachtrag)
- REQ-D11 (Vorgang G1, pm/plan/wissensnetz.py)

Vermerk: Nachtrag Sonnet aus wissensnetz.py, Prüfung Opus offen (2026-11-23). Die Zuordnung Rechenordner zu Vorgang G1 ist von Sonnet gewählt.
