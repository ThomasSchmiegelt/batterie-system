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

## Nachtrag 1 (Opus, 2026-11-18, nach dem Lauf)
**Deutung:** Mein Fehler in der Erwartung: Ich habe die 30 mm Seitenrahmen als freien Weg bis zur Zelle gezählt. Der Rahmen ist aber selbst der Bauraum. Hinter seiner Innenwand liegen die Zellen mit 0–4 mm Abstand (LFP 1 mm zum Verbinder, 4 mm zur Zelle; NMC gerade Reihen 0 mm). Das Kriterium im Lauf ist richtig gewählt: Die Innenwand verschiebt sich bis zum Spalt. Ergebnis:
- Bei 29–31 kN und etwa 20 J berührt die Innenwand die erste Zelle, in beiden Varianten. Das Pack hat **keine eigene Knautschzone**.
- PEEQ > 10 % schon ab 1,5 mm Pfahlweg.
- LF2 ≈ LF1, weil die Querträger auf diesem kurzen Weg nicht mittragen.
- Die Netzstudie ist erfüllt (< 1 %).
**Folge:** Die Entscheidung „Seitencrash über den Schweller“ (2026-11-17) ist zwingend. Der Schweller muss die ganze Seitenenergie aufnehmen, das Pack trägt keine 100 kN. Will man Reserve im Pack, braucht es eine Knautschzone von etwa 15–30 mm je Seite (Annahme). Bei fester Breite 1430 mm kostet das Zellbreite: LFP hat nur 8 mm Reserve, NMC eine Zellreihe → Autor.
Die Randbedingungen, die Sonnet gesetzt hat (Einspannung bei y = 300, Bodenstreifen 300 mm, Penalty 1e5), bestätige ich für einen Variantenvergleich.

## Anforderung (Nachtrag)
- REQ-P14 (Vorgang X1, pm/plan/wissensnetz.py)
- REQ-P11 (Vorgang X1, pm/plan/wissensnetz.py)

Vermerk: Nachtrag Sonnet aus wissensnetz.py, Prüfung Opus offen (2026-11-23). Die Zuordnung Rechenordner zu Vorgang X1 ist von Sonnet gewählt.
