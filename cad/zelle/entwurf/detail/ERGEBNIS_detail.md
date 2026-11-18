| Dok.-Nr. | ERG-G2D | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Ergebnis G2-D: Detailmodell Innenaufbau LFP und 4680 mit Schnittbildern | Ersteller | Claude Sonnet (KI) | Prüfer | Opus (Modell, Bilder, Zahlen) |

> **KI-generiert.** Entwurf, nicht freigegeben; Akten ENT-015 (681 mm) und ENT-031…080 nur „vorgeschlagen“. Quelle aller Zahlen: `cad/zelle/entwurf/detail/ergebnis_detail.json` (aus `ergebnis_detail_LFP.json`, `ergebnis_detail_NMC.json`, erzeugt von `cad/zelle/zelle_detail.py`).

## Was getan
- `cad/zelle/zelle_detail.py` (FreeCAD 1.1.4 headless) baut je Variante das Innenleben aus `parameter_<V>_entwurf.json` (vorher `entwurf_parameter.py` neu gelaufen) und aus `cad/zelle/aufbau_W20.json` (nur die Fahnenbreiten LFP). Ausgabe: `zelle_LFP_detail.FCStd/.step`, `zelle_NMC_detail.FCStd/.step`, OBJ je Teil und Satz in `render/`.
- **LFP:** 38 Kathoden, 39 Anoden, 78 Separatorlagen mit echten Dicken (je Blatt Folie und zwei Beschichtungen als eigene Körper), Falzbänder, Kathodenfahnen an einem, Anodenfahnen am anderen Ende, Stromschienen, Pole, zweiteilige Kunststoffhalter, O-Ringe, Isolationsbeutel, Al-Gehäuse 0,3 mm mit PET-Folie, Ventil, Füllstopfen.
- **4680:** Spirale als vier Bänder (Kathode, Separator, Anode, Separator; Folie und zwei Beschichtungen je Elektrode getrennt) mit echter archimedischer Spirale ab Kern Ø 12.5 mm, Bandlängen aus den Akten, Ringscheiben als „gefalteter Rand“ oben (Al) und unten (Cu), zwei Tab-Scheiben mit je 6 Dreiecken, Becher, Deckel, Dichtring, Isolierring, Pluspol, Blindniet, Bodenventil, Klebestreifen. Die Spirale ging in FreeCAD (kein Rückfall auf Blender nötig; Laufzeit 5 min).
- `cad/zelle/render_detail.py` (Blender 4.0, Cycles CPU, orthografisch) und `render_detail_beschriftung.py` (PIL: Pfeile, Namen, Maßstabsbalken, Titel, Fußzeile) erzeugen 8 Bilder in `cad/zelle/entwurf/detail/`.

## Zahlen (Fundstelle `ergebnis_detail.json`)
| Größe | Wert | Pfad im JSON |
|---|---|---|
| LFP Stapeldicke | 12,476 mm | LFP.stapel.stapeldicke_mm |
| LFP Innendicke (14 − 2 × 0,3) | 13,4 mm | LFP.stapel.innendicke_mm |
| LFP Rest zur Innendicke | 0,924 mm (nach Beutel 0,724 mm) | LFP.stapel.rest_zur_innendicke_mm, rest_nach_beutel_mm |
| LFP Platz Stromschiene bis Stirnwand | Kathode 22,45 mm, Anode 22,20 mm | LFP.laengen_mm |
| LFP Endzone je Seite ab Separatorrand | 24,7 mm | LFP.laengen_mm.endzone_je_seite_ab_separator |
| 4680 Windungen Kathode / Anode / Separator | 36,66 / 36,93 / 38,89 und 38,44 | NMC.wickel.windungen_* |
| 4680 Außenradius Kathode / Anode / Separator | 22,17 / 22,52 / 22,56 mm | NMC.wickel.aussenradius_* |
| 4680 Becher-Innenradius | 22,60 mm | NMC.wickel.becher_innenradius_mm |
| **4680 Abstand Wickel zu Becher** | **0,04 mm** (negativ = Überstand) | NMC.wickel.abstand_wickel_zu_becher_mm |
| 4680 Dicke je Windung | 0,45 mm (solange alle 4 Bänder wickeln; danach kleiner) | NMC.wickel.dicke_je_windung_voll_mm |
| 4680 Wickelhöhe / freie Höhe bis Deckel | z 1…76 mm / 2,4 mm | NMC.wickel |
| Volumen Elektroden LFP (Kathoden-Beschichtung / Anoden-Beschichtung / Separator) | 270,1 / 267,2 / 51,4 cm³ | LFP.volumen_je_teil_cm3 |
| Volumen 4680 (Kathoden-Beschichtung / Anoden-Beschichtung / Separator / Becher) | 34,7 / 60,2 / 5,3 / 5,2 cm³ | NMC.volumen_je_teil_cm3 (ungeschnittener Wickel) |
| Gültigkeit der Solids | LFP 18/18, 4680 17/17 gültig | gueltig |

## Abgleich mit dem Erwartungs-Nachtrag (`cad/zelle/ERWARTUNG.md`, 2026-11-17)
1. **LFP-Stapel 12,48 mm in 13,4 mm, Rest ≈ 0,9 mm:** Ist 12,476 mm, Rest 0,924 mm: erfüllt. Elektrodenlängen 615,5/620/631 mm kommen aus den Akten ENT-032/038/044. Endzone: Das Skript liefert 24,7 mm je Seite ab Separator (Erwartung „≈ 25–33 mm“, die Untergrenze 25 ist gerundet): erfüllt.
2. **4680 Windungen, Außenradius ≤ 22,6 mm, Kern:** (Opus-Korrektur: ENT-074 Kern Ø 12.5 mm; flächentreue Spirale, Bänder gemeinsam am Kern, `A_NMC_BAND_START_VERSATZ_MM` = 0, da Abb. 5B nicht in aufbau_W20.json.) Kathode 36,66 Windungen (Erwartung ≈ 35, Band 30–38 erfüllt; Abweichung zum „≈ 35“ 1,66, weil der Wickel am Kern bei R = r₀ beginnt und die erste Windung bis 5,80 mm nach innen reicht). Außenradius Wickel 22,56 mm (Flächenformel √(r₀² + Σ Dicke·Länge/π) = 22,56 mm, Erwartung ≈ 22,57) gegen Becher innen 22,60 mm, Abstand 0,035 mm: erfüllt. Kathode endet bei 22,17 mm, Anode 22,52 mm, Separator 22,56 mm.
3. **Breiten** (LFP 82,5/85/87 mm in 89,4 mm, 4680 72/73/75 mm in 80 mm): aus den Akten übernommen; 4680 Wickelhöhe 75 mm, oben bleiben 2,4 mm bis Deckelunterseite: erfüllt.
4. **Annahmen** stehen als `A_*` im Skript, in `ergebnis_detail_<V>.json` (Block `annahmen`) und in der Fußzeile jedes Bildes. LFP: POL_D 10, POL_H 3, PET_FOLIE_MM 0.05, BEUTEL_MM 0.1, BB_DICKE_MM 1, HALTER_BREITE_MM 40, ORING_R_MM 1, VENTIL_D_MM 8, VENTIL_H_MM 0.5, VENTIL_Y_MM 25, STOPFEN_D_MM 3, STOPFEN_H_MM 1.5, STOPFEN_Y_MM -25, UEBERHOEHUNG 20, ENDZONE_FENSTER_MM 110. 4680: NMC_POL_D 12, NMC_POL_H 1, NMC_RAND_MM 0.3, NMC_TABSCHEIBE_MM 0.3, NMC_TABSCHEIBE_R 21, NMC_TAB_SEKTOR_GRAD 50, NMC_DICHTRING_BREITE 2, NMC_DICHTRING_H 1, NMC_DECKEL_MM 0.4, NMC_ISOLIERRING_H 0.7, NMC_POST_D 4, NMC_NIET_D 8, NMC_NIET_H 0.5, NMC_VENTIL_D 10, NMC_VENTIL_X 12, NMC_KLEBE_H 8, NMC_KLEBE_DICKE 0.05, NMC_BAND_START_VERSATZ_MM 0, PUNKTE_JE_WINDUNG 72.

## Abweichungen, Deutungen, offene Punkte
- **Nachlauf 4680 (Opus-Auftrag, ENT-074 = Ø 12,5 mm):** Wickel flächentreu neu gebaut; er passt in den Becher, die Darstellung ist ungeschnitten. Der erste Lauf (feste Steigung 0,45 mm, Kern Ø 14 mm) ergab 1,15 mm Überstand, siehe BEFUNDE B-BAT-015, und ist überholt.
- **Fahnen 4680 (5 und 7,5 mm):** als Ringscheibe „gefalteter Rand“ (Dicke ANNAHME) dargestellt, nicht als Foliensteg; die Breiten 72/73 mm sind als Beschichtungsbreite gelesen (sonst wäre die Anode beschichtet schmaler als die Kathode). Das ist eine Lesart, Opus bitte prüfen.
- **Fahnenbreiten LFP** (27,1 / 20,5 mm) stehen in `aufbau_W20.json` als „Bedeutung unklar“; als Fahnenbreite verwendet (Abb. 5A). Lage der Fahnen mittig (Annahme).
- Nicht modelliert: Isolierrand Kathode 6,5 mm (BT-114); Klebeband/Kunststoffschiene BT-116; Faltbögen nur als gerades Band; Fahnen nicht zu Bündeln verdichtet; 4680: Foliensteg der Fahnen (5 / 7,5 mm) einzeln: durch Ringscheibe 'gefalteter Rand' angedeutet (ANNAHME Dicke); Elektrolyt; Deckel nur als Scheibe, Sicken und Bördelung fehlen.
- Pol plus liegt bei x = Zelllänge (wie `zelle.py`), Kathodenfahnen und Ventil dort; Anode und Füllstopfen am anderen Ende.
- Die LFP-Schicht-Dicken sind im Schnittbild nicht sichtbar (0,16 mm bei 26 px/mm = 4 px); deshalb Lagenmodell oben im Bild mit Dicken × 20 (Darstellung, keine Messung).
- Laufzeiten: LFP 5 s, 4680 5 min (FreeCAD, ohne GPU); je Bild 20 s bis 2 min (Blender CPU).

---
*KI-generiert (Claude Sonnet, 2026-11-17), Entwurf, nicht vom Menschen freigegeben.*
