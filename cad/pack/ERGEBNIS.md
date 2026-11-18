| Dok.-Nr. | ERG-G4 | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Ergebnis G4: Pack-CAD LFP und NMC (Entwurf) | Ersteller | Claude Sonnet (KI) | Prüfer | Opus (Stichprobe) |

> **KI-generiert.** Claude Sonnet, 2026-11-17, Auftrag G4. Entwurf, nicht freigegeben. Zahlen aus `cad/pack/entwurf/ergebnis_LFP.json`, `ergebnis_NMC.json`, `ergebnis.json`; Maße aus `cad/pack/entwurf/parameter_<V>.json` (Akten entschieden + vorgeschlagen, Block A = Annahmen, Bauraumlänge je Variante (LFP ENT-102, NMC ENT-103)).

## Abgleich ERWARTUNG.md
1. LFP: Gehäuse 2030 x 1430 mm (erwartet 2030 x 1430), Höhe 121 mm (≤ 130, M0 121), 250 Zellen (2 x 125), 3 Querträger, Kollisionen 0 bei 385 geprüften Paaren: ERFÜLLT. Gehäuse = Bauraumlänge nach Freigabe (LFP 2030 mm ENT-102, NMC 1950 mm ENT-103).
2. NMC: 868 Zellen, je Feld 217 (4 Felder), Träger unten, Verguss (halbe Zellhöhe, Annahme), Verbinder oben, Pad, Kühlplatten. Höhe 115 mm (erwartet 111, ≤ 130): ERFÜLLT; Abweichung gegen 111: +4 mm, weil Zellabgriffe (1 mm) und Gruppenverbinder (3 mm) über der Zelle liegen und M0 sie nicht im Stapel hatte. Kollisionen 0 bei 5379 Paaren: ERFÜLLT.
3. Masse (Teile mit bekannter Masse): LFP 611.9 kg, erwartet 560–620, C0b Fall A 616 kg, Abweichung -0.7 %: ERFÜLLT. NMC 473.4 kg, erwartet 390–430, C0b Fall A 411 kg, Abweichung +15.2 %: VERFEHLT (> 15 % → Opus). Massen nach Nachtrag (siehe unten; Erstlauf Vollmaterial in `ergebnis_<V>_vollmaterial.json`).
4. Schwerpunkt (Abweichung von der Mitte, ± 20 mm): LFP x -1.4, y -0.0 mm: ERFÜLLT; NMC x -12.3, y -11.2 mm: ERFÜLLT (Erstbelegung der NMC-Felder von links ergab x −40,5 mm, siehe `ergebnis_NMC_erstbelegung_links.json`, danach Zellen mittig im Feld).

## Offene Punkte (an Opus)
- Neue Annahme Platzhalter: NMC-Zellträger Dicke 2.5 mm (in M0 nicht gesetzt).
- Dichten Pad, Zellträger, Verguss, Kühlplatten-Füllgrad und Rahmenprofil sind Annahmen (Nachtrag).
- Verbinder als Aluminium angesetzt (Annahme, Kupfer offen).
- LFP: Zellen ohne Pole (Hüllkörper), Zellverbinder 25 x 3 nur am äußeren Zellende (3 mm in 4 mm Toleranz), je zwei Nachbarzellen, ohne Polarität; innen Zellen stoßen an (keine Verbinder in der Mitte).
- NMC: Gruppenverbinder je 4 Zellen eine Sammelschiene plus Reihenbrücke (Brücke stößt an, Länge Zellteilung minus Abgriffdurchmesser, nicht 48 mm wie E1), Zellabgriffe als Scheiben Ø 12 x 1; M0 hatte diese nicht im Höhenstapel (+4 mm).
- Bauraum nach Freigabe: LFP 2030 mm (ENT-102), NMC eigenes Gehäuse 1950 mm (ENT-103).

## Bilder (cad/pack/entwurf/)
`pack_<V>_gesamt|explosion|laengs|quer|schnitt.png` (je Variante, Beschriftung der Teile, Maßstabsbalken 200 mm in Schnitten), `pack_massen.png` (Zielband). Lesehilfe: `pack_lesehilfe.md`. Wiederholung ohne Codeänderung: `bash cad/pack/render_pack.sh`.

## Nachtrag 2026-11-17 (Auftrag Opus): Massenannahmen und Schnittbilder
- Annahmen (Opus), in `parameter_<V>.json` Block A: Kühlplatte Füllgrad A_KUEHLPLATTE_FUELLGRAD 0,4 (2 Bleche je 1,5 mm + Kanalstege); Seitenrahmen Mehrkammerprofil, Wand 2,5 mm, 3 Kammern; Dichten Pad 2500, Zellträger (PC) 1200, Verguss (PU-Schaum) 300 kg/m³. Geometrie unverändert (Volumenkörper), nur Massen und Schwerpunkt.
- Vorher (Vollmaterial, ohne Pad/Träger/Verguss): LFP 705.5 kg, NMC 556.5 kg (`ergebnis_<V>_vollmaterial.json`). Jetzt: LFP 611.9 kg (ERFÜLLT, Band 560–620), NMC 473.4 kg (VERFEHLT, Band 390–430, +15.2 % gegen C0b 411 kg). Kühlplatten je Pack 46.6 kg, Seitenrahmen LFP 21.7 kg, NMC 20.1 kg.
- Schwerpunkt jetzt: LFP x -1.4, y -0.0 mm; NMC x -12.3, y -11.2 mm (Soll ± 20 mm).
- Gruppenverbinder NMC geändert (je 4 Zellen kurz + Reihenbrücke, wie E1-Nachtrag), Kollisionen weiter 0. Viertelschnitt: Kamera an der Schnittecke (Ausschnitt 380 mm), Deckel weggelassen, Beschriftungsanker auf dem Teil.

## Nachtrag „Freigabestand“ 2026-11-17
- Der Autor hat ENT-096…101 freigegeben und für NMC ein eigenes Gehäuse von 1950 mm entschieden (ENT-103, LFP 2030 mm = ENT-102). Maße neu aus den Akten (`parameter_<V>.json`, Status siehe dort: LFP: entschieden 17, vorgeschlagen 36; NMC: entschieden 26, vorgeschlagen 29).
- Gehäuse jetzt LFP 2030 x 1430 x 121 mm, NMC 1950 x 1430 x 115 mm; Zellen 250 / 868 (NMC gleichmäßig auf 4 Felder, je 217).
- Masse: LFP 611.9 kg (ERFÜLLT, Band 560–620, -0.7 % gegen C0b), NMC 473.4 kg (VERFEHLT, Band 390–430, +15.2 % gegen C0b). Schwerpunkt LFP x -1.4, y -0.0 mm; NMC x -12.3, y -11.2 mm. Kollisionen 0 / 0.
- Beschriftung: Anker werden aus der Teilegeometrie berechnet (sichtbarer Eckpunkt per Strahltest, Teile ohne sichtbaren Punkt bleiben unbeschriftet). Neue Ansicht `pack_<V>_ecke.png` zeigt im Schnitt die Zellverbinder (LFP) an der Außenwand.

*KI-generiert, Entwurf. Dokument ERG-G4, Version 1.0.*
