| Dok.-Nr. | ERW-X1 | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Erwartung X1: Seitenpfahl quasistatisch auf das Pack (CalculiX) | Ersteller | Claude Opus (KI) | Prüfer | – |

> KI-generiert (Opus, 2026-11-18), vor der Rechnung. Autor: „jetzt … crash“. Vorgang X1 (plan_batterie.py), REQ-P14. Autor 2026-11-17: Seitencrash über den Schweller akzeptiert (B-BAT-019/M0). Das Pack trägt also nur den **Rest**, den der Schweller durchlässt.

## Frage
Wie viel Kraft und Energie nimmt das Gehäuse mit Seitenrahmen und Querträgern auf, bevor der Pfahl die erste Zelle erreicht? Das wird je Variante und Pfahllage gerechnet. Ergebnis ist ein Variantenvergleich und die Reserve, kein Nachweis (Konzept docs/konzept_…crash.md §4).

## Belege und Annahmen
| Größe | Wert | Herkunft |
|---|---|---|
| Seitenaufprall-Last Fahrzeug > 2600 kg | ≈ 600 kN | **Beleg** W22: „is known to be on the order of 600 kN“ (US20200148066A1). Nur Größenordnung, gilt für das ganze Fahrzeug |
| MDB-Prüfung | 1500 kg, 50 km/h, 90° | **Beleg** W17 (Wikipedia Crashworthiness) |
| Pfahl | Ø 254 mm, starr, quer zur Fahrtrichtung (90°) | **Annahme Opus** (Pfahltest aus dem Gedächtnis, Beleg fehlt) |
| Restkraft hinter dem Schweller, die das Pack tragen soll | 100 kN | **Annahme Opus**, Größenordnung der Quetschprüfung für Packs aus dem Gedächtnis (UN R100 bzw. GB 38031), Beleg fehlt → W30 |
| Werkstoff Seitenrahmen, Querträger, Wanne | EN AW-6082 T6: E 70 GPa, ν 0,33, Rp0,2 260 MPa, Rm 310 MPa, Bruchdehnung 10 %, bilinear | **Annahme Opus** |
| Geometrie | aus `cad/pack/entwurf_parameter.py` / `pack.py`: Seitenrahmen 30 mm, Querträger 3 × 54×26×2,5, Wanne, Länge LFP 2050 / NMC 1950 | Akten bzw. Entwurf |
| Freier Weg bis zur Zelle | Innenkante Seitenrahmen bis erste Zelle aus dem CAD (LFP ≈ 30 + 1 mm, NMC aus Feld 1) | CAD |

## Modell
- Schalenmodell (S4/S3, gmsh oder cgx) eines Ausschnitts: Seitenrahmen über die volle Packlänge, Querträger auf 300 mm Länge angeschlossen, Bodenwanne als Streifen.
- Gegenseite fest. Die Zellen werden nicht modelliert, nur ihre Lage als Messebene.
- Pfahl weggesteuert, starr, mit Kontakt. Geometrisch und werkstofflich nichtlinear.
- Lastfälle je Variante:
  - **LF1** Pfahl mittig zwischen zwei Querträgern (ungünstig)
  - **LF2** Pfahl auf einem Querträger
- Ausgabe:
  - Kraft-Weg-Kurve bis zur Zellberührung
  - Kraft und Energie bei Zellberührung
  - plastische Dehnung, max. Wert und Ort
  - Bild der Verformung mit Zielband

## Erwartung
- **LF1:** Der Seitenrahmen biegt sich zwischen den Querträgern (Spannweite ≈ 500 mm). Spitzenkraft **30–80 kN**, bevor der freie Weg verbraucht ist. Energie **1–3 kJ**.
- **LF2:** Der Querträger knickt bzw. staucht. Grob gilt A = 400 mm² × 260 MPa ≈ 100 kN, plus Rahmen: **80–150 kN**.
- Folge: Ohne Schweller hält das Pack die Restkraft von 100 kN in LF1 voraussichtlich **nicht**. Das stimmt mit der Entscheidung „Schweller trägt“ überein. LF2 knapp.
- NMC hat in Feld 1 mehr freien Weg (41,6 mm Endzone, seitlich aus dem CAD) und nimmt deshalb mehr Energie auf.
- Plastische Dehnung im Rahmen > 10 % bei Zellberührung in LF1 → Rissgefahr markieren.

## Verfehlt
- LF1 > 150 kN: Modell zu steif, Randbedingung prüfen.
- LF1 < 15 kN: Rahmen schwächer als angenommen, Querschnitt prüfen.
- Keine Konvergenz bis 80 % des freien Wegs.
- Energie bei Zellberührung < 0,5 kJ.
