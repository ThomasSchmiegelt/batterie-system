# KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. Auftrag G2: ergebnis.json, ERGEBNIS.md, Lesehilfe, Folienbaustein G2 aus ergebnis_<V>.json (keine eigenen Zahlen).
import json, os
R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
D = f"{R}/cad/zelle/entwurf"
E = {v: json.load(open(f"{D}/ergebnis_{v}.json")) for v in ("LFP", "NMC")}
json.dump({"hinweis": "KI-generiert, ENTWURF (Akten vorgeschlagen), nicht freigegeben. Sammlung aus ergebnis_LFP.json und ergebnis_NMC.json (zelle.py)", **E}, open(f"{D}/ergebnis.json", "w"), indent=1, ensure_ascii=False)
l, n = E["LFP"], E["NMC"]
# Referenzwerte der Erwartung (aus ERWARTUNG.md Text) nur zum Vergleich
ref = {"LFP": 0.832, "NMC": 0.133}
dl = (l["aussenvolumen_L"] / ref["LFP"] - 1) * 100; dn = (n["aussenvolumen_L"] / ref["NMC"] - 1) * 100
kopf = lambda nr, t: f"| Dok.-Nr. | {nr} | Version | 1.0 | Status | Entwurf |\n|---|---|---|---|---|---|\n| Titel | {t} | Ersteller | Claude Sonnet (KI) | Prüfer | Opus (Modell und Bild) |\n\n> **KI-generiert.** Entwurf, nicht freigegeben. Akten ENT-014…029 nur \"vorgeschlagen\". Quelle aller Zahlen: `cad/zelle/entwurf/ergebnis.json`.\n\n"
fuss = "\n\n---\n*KI-generiert (Claude Sonnet), Entwurf, nicht vom Menschen freigegeben.*\n"
open(f"{D}/../ERGEBNIS.md", "w", encoding="utf-8").write(kopf("ERG-G2", "Ergebnis G2: parametrische Zelle LFP und NMC (Entwurfslauf)") + f"""## Was getan
`cad/zelle/entwurf_parameter.py` erzeugt `entwurf/parameter_<V>_entwurf.json` (Status entschieden + vorgeschlagen). `cad/zelle/zelle.py` baut daraus je Variante FCStd und STEP (FreeCAD {'1.1.4'} headless, `freecadcmd`). `zelle_bild.py` zeichnet die PNG aus der Tessellierung (matplotlib, da FreeCAD headless nicht rendert). `zelle_bericht.py` erzeugt dieses Dokument.

## Abgleich ERWARTUNG (cad/zelle/ERWARTUNG.md), Punkt für Punkt
| Nr | Erwartung | Ergebnis (Quelle) | Urteil |
|---|---|---|---|
| 1 | LFP 660 × 90 × 14 mm, 0,832 L, Wand 0,3 mm, zwei Pole an Stirnseiten, Polmaße Annahme, ≈ 355 Wh/L | {l['masse_eingabe']['laenge_mm']:.0f} × {l['masse_eingabe']['breite_mm']:.0f} × {l['masse_eingabe']['dicke_mm']:.0f} mm, Wand {l['wandstaerke_mm']} mm, Außenvolumen {l['aussenvolumen_L']:.4f} L ({dl:+.2f} % gegen 0,832), {l['energie_Wh']:.2f} Wh → {l['Wh_pro_L']:.1f} Wh/L; Pole ANNAHME Ø {l['annahmen']['ANNAHME_POL_DURCHMESSER_MM']} mm, {l['annahmen']['ANNAHME_POL_HOEHE_MM']} mm Überstand (`ergebnis_LFP.json`) | erfüllt (Abweichung < 1 %) |
| 2 | NMC Ø 46 × 80 mm, 0,133 L, Wand 0,4 mm, Plus oben, Minus Becherrand | Ø {n['masse_eingabe']['durchmesser_mm']:.0f} × {n['masse_eingabe']['hoehe_mm']:.0f} mm, Wand {n['wandstaerke_mm']} mm, Außenvolumen {n['aussenvolumen_L']:.5f} L ({dn:+.2f} % gegen 0,133), {n['energie_Wh']:.2f} Wh → {n['Wh_pro_L']:.1f} Wh/L; Pluspol ANNAHME Ø {n['annahmen']['ANNAHME_NMC_POL_DURCHMESSER_MM']} mm, {n['annahmen']['ANNAHME_NMC_POL_HOEHE_MM']} mm (`ergebnis_NMC.json`) | erfüllt (Abweichung < 1 %) |
| 3 | Masse nicht aus CAD | Gehäusematerialvolumen LFP {l['gehaeuse_materialvolumen_cm3']:.2f} cm³, NMC {n['gehaeuse_materialvolumen_cm3']:.2f} cm³ nur als Kontrollgröße; keine Masse aus CAD | erfüllt |
| 4 | Modell liest nur parameter_<V>.json | Maße nur aus Parameterdatei; Test: Länge 700 mm in Kopie der Parameterdatei ergab ohne Codeänderung 0,882 L (Lauf im Scratchpad, nicht im Repo abgelegt). Fehlt ein Merkmal, bricht zelle.py ab (FEHLT). Im Code stehen nur ANNAHME_*-Konstanten (Pole) | erfüllt |
| 5 | STEP, PNG, Volumen in ergebnis.json | `zelle_LFP.step`, `zelle_NMC.step`, `zelle_LFP.png`, `zelle_NMC.png`, `ergebnis.json` | erfüllt |

Bounding Box mit Polen: LFP {l['bbox_mit_polen_mm'][0]:.0f} × {l['bbox_mit_polen_mm'][1]:.0f} × {l['bbox_mit_polen_mm'][2]:.0f} mm (Pole stehen 3 mm je Seite über das Gehäuse; Annahme), NMC {n['bbox_mit_polen_mm'][0]:.0f} × {n['bbox_mit_polen_mm'][1]:.0f} × {n['bbox_mit_polen_mm'][2]:.0f} mm. Wh/L bezieht sich auf das Gehäuseaußenvolumen ohne Pole (wie in der Erwartung).

## Offene Punkte (zurück an Opus)
- Polmaße sind Annahmen (keine Akte, keine Quelle). Vorschlag: eigene Akte oder Beleg suchen.
- Das Gehäuse ist ein leerer Hohlkörper (Innenaufbau BT-110 nicht modelliert). Material und Isolierfolie (ENT-023, ENT-028) sind nicht abgebildet.
- Die Pole im NMC-Bild zeigen kleine Darstellungsartefakte der Tiefensortierung (nur Bild, nicht Geometrie).
- `parameter_<V>.json` in pm/ enthält die Zellmaße noch nicht (nur Entwurfsdatei); Standardlauf von zelle.py bricht darum mit FEHLT ab, bis die Akten freigegeben sind.
- Nebenarbeit: `erzeuge_bericht.py` (C0b) erhält jetzt eine vorhandene Kernaussage. Die von Hand ergänzte Bauraum-Zeile in C0b.md wird vom Skript weiterhin überschrieben; ich habe C0b.md nach dem Testlauf aus der Sicherung wiederhergestellt (unverändert).
""" + fuss)
open(f"{D}/zelle_lesehilfe.md", "w", encoding="utf-8").write(kopf("LH-G2", "Lesehilfe zu den Zellbildern (G2)") + f"""**Lesehilfe zu `zelle_LFP.png`** Das Bild zeigt eine Batteriezelle vom Typ LFP als flache, lange Platte (Blade). Links die ganze Zelle (Länge maßstäblich, Breite und Dicke zur besseren Sicht vergrößert), rechts das Ende mit dem Pluspol (roter Stummel). Das Gehäuse ist hier nur eine dünne Hülle (Wand {l['wandstaerke_mm']} mm); das Innere ist nicht gezeichnet. Die Polgröße ist eine Annahme, keine belegte Zahl. Der Rechenkasten unten nennt Maße, Volumen ({l['aussenvolumen_L']:.3f} L) und Energie je Liter ({l['Wh_pro_L']:.0f} Wh/L). Ein Zielband gibt es nicht; Vergleichswert ist die Erwartung 0,832 L. Entwurf: Akten sind noch nicht freigegeben.

**Lesehilfe zu `zelle_NMC.png`** Das Bild zeigt eine runde Zelle (Format 4680, Becher) von der Seite und im Ausschnitt oben. Der rote Kreis oben ist der Pluspol; der Minuspol ist der Rand des Bechers. Das Gehäuse ist nur eine dünne Hülle (Wand {n['wandstaerke_mm']} mm), das Innere ist nicht gezeichnet. Der Pol ist eine Annahme. Der Rechenkasten nennt Maße, Volumen ({n['aussenvolumen_L']:.3f} L) und Energie je Liter ({n['Wh_pro_L']:.0f} Wh/L); Vergleichswert aus der Erwartung ist 0,133 L. Entwurf, nicht freigegeben.
""" + fuss)
bs = f"{R}/praesentation/bausteine"; os.makedirs(bs, exist_ok=True)
open(f"{bs}/G2.md", "w", encoding="utf-8").write(f"""> **KI-generiert** (Claude Sonnet, 2026-11-17), Entwurf. Folienbaustein Vorgang G2 (parametrische Zelle).

# Beide Zellen als parametrisches CAD
**Kernaussage (Opus): <von Opus einzusetzen>. Rechenstand: LFP-Blade {l['aussenvolumen_L']:.3f} L und NMC-4680 {n['aussenvolumen_L']:.3f} L bauen aus den Akten (Entwurf) ohne Fehler; {l['Wh_pro_L']:.0f} gegen {n['Wh_pro_L']:.0f} Wh/L auf Zellebene.**

**Bild:** cad/zelle/entwurf/zelle_LFP.png und zelle_NMC.png (kein Zielband; Vergleich mit Erwartung 0,832 L bzw. 0,133 L; Polmaße als Annahme beschriftet)

**Zahlen** (Quelle cad/zelle/entwurf/ergebnis.json):
- LFP: {l['masse_eingabe']['laenge_mm']:.0f} × {l['masse_eingabe']['breite_mm']:.0f} × {l['masse_eingabe']['dicke_mm']:.0f} mm, Wand {l['wandstaerke_mm']} mm, {l['aussenvolumen_L']:.3f} L, {l['energie_Wh']:.1f} Wh, {l['Wh_pro_L']:.1f} Wh/L
- NMC: Ø {n['masse_eingabe']['durchmesser_mm']:.0f} × {n['masse_eingabe']['hoehe_mm']:.0f} mm, Wand {n['wandstaerke_mm']} mm, {n['aussenvolumen_L']:.4f} L, {n['energie_Wh']:.1f} Wh, {n['Wh_pro_L']:.1f} Wh/L
- Alle Akten ENT-014…029 noch nur vorgeschlagen; Polmaße Annahme

*KI-generiert, Entwurf.*
""")
print("ok")
