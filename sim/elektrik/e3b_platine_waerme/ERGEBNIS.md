| Dok.-Nr. | ERG-E3b | Version | 0.1 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Ergebnis E3b: Temperatur der CMU-Platine mit Wärmeleitpad (ENT-184), Elmer | Ersteller | Claude Sonnet (KI), Auftrag Opus | Prüfer | Opus (offen) |

> **KI-generiert** (Claude Sonnet, 2026-11-24), Entwurf, nicht vom Menschen freigegeben, Prüfung Opus offen. Anforderungen: REQ-P15, REQ-P20, REQ-P09. Grundlage: `ERWARTUNG.md` (unverändert). Alle Zahlen aus `ergebnis.json` (je Lauf `lauf/<Fall>_<Var>_<Netz>/res.json`).

## Was getan wurde
- Lage der CMU im CAD geprüft (`cad/pack/pack_e2d.py` Z. 207 ff.): CMU hochkant in den Endzonen, Rückseite bündig an der Innenkante des Seitenrahmens (x0 = `rand`), Rahmen aus Al (Vollprofil) und mit beiden Kühlplatten- und Pad-Blöcken im selben Modell (Kontaktfläche, keine Verbindung modelliert). Das Pad liegt also zwischen CMU und Seitenrahmen, nicht auf der Kühlplatte. Wand als Randbedingung 45 °C (Erwartung).
- Wärmequellen aus `/home/cae/cae_projekte/batterie/e3/cmu_<V>.kicad_pcb`: 36 Widerstände R_2512 (Footprint 3,2 x 6,3 mm, gedreht), 18 FETs SOT-23 (2,9 x 1,3 mm) auf F.Cu. Leistungen aus `sim/elektrik/e3_platine/ergebnis_ausgleich.json`: LFP 0,27164 W je Widerstand, 0,01169 W je FET, zusammen 9,9896 W; NMC 0,26354 W / 0,00820 W, 9,6351 W. Als Flussrandbedingung auf der Footprint-Fläche. Die Summe der Bilanz (Wand + Oberseite) stimmt mit P überein (a LFP 9,753 + 0,236 = 9,989 W).
- Modell: Platine 1,6 mm als homogener Quader (λ quer 0,3; in der Ebene mit 4 Cu-Lagen 70/35/35/70 µm vollflächig: λ_xy = 51,9 W/mK), Vias unter jedem Widerstandspaar (18 Paare, je 8 Vias Ø 0,3 mm) als Zone mit λ_z = 5,16 W/mK (gefüllte Kupferzylinder, Anteil 1,25 %), Pad 1 mm, λ = 3 W/mK, 120 x 60 mm. Oberseite h = 5 W/m²K plus Strahlung ε = 0,9 gegen 45 °C (Elmer `Radiation = Idealized`), Seiten adiabat. Fall (c): Rückseite ebenso h = 5 plus Strahlung.
- Netz gmsh (Tetraeder), grob 0,8 mm (143 768 bis 228 238 Tetraeder) und fein 0,5 mm (558 997 bis 904 454); Elmer 26.2, stationär, CPU, nice. Alle 18 Läufe (6 Fälle x 2 Netze, 6 Sensitivität) liefen in wenigen Minuten (Start 11:00, Ende 11:13, Skript `lauf_alle.sh`, Neustart `neustart.sh`).
- Zusätzlich (keine neue Annahme, nur Grenzfall der gegebenen Zahlen): Sensitivität `cu0`, Kupferlagen ohne Beitrag zur Querleitung (λ_xy = 0,8 W/mK).

## Ergebnis (T_max in °C, feines Netz, Quelle `ergebnis.json`, Block `vergleich`)
| Fall | LFP | NMC | Sensitivität cu0 LFP / NMC |
|---|---|---|---|
| (a) Pad + Vias | 49,07 | 48,93 | 52,64 / 52,40 |
| (b) Pad ohne Vias | 57,11 | 56,69 | 93,92 / 92,45 |
| (c) ohne Pad | 120,30 | 118,00 | 152,88 / 149,75 |

Grenze 105 °C (Annahme): (a) und (b) mit Reserve 48 K und mehr, (c) überschritten. Wärmestrom in die Wand (Elmer, `Q_wand_W`): (a) LFP 9,75 W = 97,6 %, NMC 9,41 W = 97,6 %; (b) LFP 9,36 W = 93,7 %, NMC 9,03 W = 93,7 %. Bild: `e3b_temperatur.png` (Lesehilfe `lesehilfe.md`), selbst angesehen: Felder plausibel, heiße Zonen an den beiden Widerstandsreihen, kalter Rand rechts (keine Quellen), Grenze beschriftet.

## Abgleich ERWARTUNG.md
| Nr. | Erwartung | Befund | Urteil |
|---|---|---|---|
| 1 | Mit Pad T_max 60–80 °C, Reserve ≥ 25 K | 49,07 / 48,93 °C (a); Grenze mit 56 K Reserve eingehalten | **verfehlt (Band, nach unten)**; Aussage Grenze ok |
| 2 | Ohne Vias 80–100 °C | 57,11 / 56,69 °C; mit cu0 93,92 / 92,45 °C | **verfehlt (Band, nach unten)**; mit cu0 im Band |
| 3 | Ohne Pad 100–130 °C, im Band der E3-Abschätzung (`../e3_platine/ergebnis_waerme.json`: LFP 114,4–183,7, NMC 111,9–178,8) | 120,30 / 118,00 °C | **ok** |
| 4 | Wand ≈ 90 % von P; Zellen in der Endzone < 1 K | Wand 93,7–97,6 % (siehe oben); 14 CMU x 9,75 W = 136,5 W (LFP, a). Zellerwärmung nicht abgeschätzt (keine Fläche und kein Kopplungswert im Auftrag) | Wandanteil **ok**, Zellwirkung **offen** |
| 5 | Netzunterschied < 2 K | größter Unterschied 0,55 K (c NMC), a 0,01 K, b 0,19 K | **ok** |

Deutung der Abweichung 1/2 (Hinweis, Entscheidung Opus): Der Unterschied kommt aus den vier Kupferlagen. Mit λ_xy = 51,9 W/mK verteilt die Platine die Wärme in der Ebene, bei Kupfer ohne Beitrag (cu0) liegt (b) im Erwartungsband. Wie viel Kupferfläche die Lagen wirklich haben, steht nirgends (Layout ungeroutet).

## Offene Fragen an Opus
1. Thermische Anbindung der Wand an die Kühlplatte: im CAD berührt der Seitenrahmen die Kühlplatten, Verbindung (Schraube, Schweißung, Wärmeleitpfad) und Wandtemperatur sind nicht modelliert. 45 °C ist die Annahme der Erwartung. Welche Wandtemperatur ist maßgeblich?
2. Kupferflächenanteil der vier Lagen: Ergebnis (a) 49 bis 53 °C, (b) 57 bis 94 °C, je nach Annahme. Neue Annahme oder Layout-Auswertung nötig.
3. Vias: im Layout (`cmu_<V>.kicad_pcb`) sind keine Vias gesetzt (0 `(via`); die 8 Vias je Paar sind Annahme Opus und noch nicht ins Layout übernommen. Modelliert als gefüllte Cu-Zylinder (Obergrenze). Hülsenwand (z. B. 25 µm) wäre eine neue Annahme.
4. Erwartungsband 1 und 2 verfehlt (nach unten): Band korrigieren oder Modell prüfen? Das Werkzeug wurde nicht angepasst.
5. Zellerwärmung durch den Wandwärmestrom (Erwartung 4, < 1 K) nicht abgeschätzt.
6. Bauraum: 10 mm CMU-Dicke plus Pad 1 mm gegen die Platine mit Bauteilhöhe nicht geprüft (Folge ENT-184). Das Layout ist noch nicht vollständig geroutet (219 Verbindungen offen, `ergebnis_platine.json`); die Lage der Quellen kann sich ändern.
7. Bauteilkörper, Lot und Strahlung auf der Platinenrückseite in (a)/(b) sind nicht modelliert (Heizfläche = Footprint-Fläche).

## Dateien
`e3b_rechnen.py` (Netz, sif), `lauf_einzel.py`, `lauf_alle.sh`, `neustart.sh`, `e3b_auswerten.py`, `ergebnis.json`, `e3b_temperatur.png`, `lesehilfe.md`, `lauf/` (Netze, sif, vtu, Logs je Lauf).

## Vorschlag Zeile für `docs/08_ki_einsatz_protokoll.md`
Siehe Protokoll (bereits eingetragen).

---
*KI-generiert (Claude Sonnet, 2026-11-24), Entwurf, nicht vom Menschen freigegeben.*
