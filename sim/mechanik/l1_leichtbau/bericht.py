#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-24), Entwurf. Erzeugt ERGEBNIS.md aus ergebnis.json (Auftrag L1). Zahlen nur aus ergebnis.json."""
import json, os
O = os.path.dirname(os.path.abspath(__file__)); a = json.load(open(f"{O}/ergebnis.json")); L, N = a["LFP"], a["NMC"]
f0 = lambda x: f"{x:.0f}"; f1 = lambda x: f"{x:.1f}"; f2 = lambda x: f"{x:.2f}"
def rg(v, h): return f"{v['hebel'][h]['spanne_kg'][0]}…{v['hebel'][h]['spanne_kg'][1]}"
rl, rn = L["rueckrechnung"], N["rueckrechnung"]
gr = lambda v: "\n".join(f"| {g['gruppe']} | {f2(g['masse_kg'])} | {'–' if g['nachgerechnet_kg'] is None else f2(g['nachgerechnet_kg'])} | {'–' if g['abw_prozent'] is None else f1(g['abw_prozent'])} | {g['werkstoff']} |" for g in v["gruppen"])
md = f"""| Dok.-Nr. | ERG-L1 | Version | 0.1 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Ergebnis L1: Leichtbau-Potenzial des Packs (OPT-012), Studie ohne CAD-Änderung | Ersteller | Claude Sonnet (KI) | Prüfer | Opus (offen) |

> **KI-generiert** (Claude Sonnet, 2026-11-24). Entwurf, nicht freigegeben. Grundlage `ERWARTUNG.md` (ERW-L1, Opus, nicht geändert). Zahlen aus `ergebnis.json` in diesem Ordner (erzeugt von `leichtbau.py`, Eingang `cad/pack/entwurf/ergebnis_<V>_e2d_e3c.json` und `parameter_<V>.json`, nur gelesen). Die **Einsparspannen der Hebel sind Schätzungen von Opus** (ERWARTUNG.md), nicht gerechnet. Was aus der Geometrie folgt, ist als solches benannt. Es wurde kein CAD geändert.

## Was getan wurde
Massen der Gruppen ab 3 kg aus dem CAD-Ergebnis übernommen und aus Maßen und Dichten nachgerechnet (Plausibilität). Hebelspannen H1 bis H7 aus ERWARTUNG.md als Eingabe addiert (`ergebnis.json`, summe_spanne_kg, masse_neu_kg). Je Hebel zurückgerechnet, welcher Parameter die Spanne erfordern würde (rueckrechnung). Wasserfallbilder mit Zielband REQ-P07. **Band aus W51: offen** (`forschung/ergebnis/W51.md` fehlt, nur `W51.err` und `W51.jsonl` vorhanden, keine bestandene Zitatprüfung).

## Abgleich der Erwartungen
| Nr | Erwartung (ERWARTUNG.md) | Ergebnis (Quelle `ergebnis.json`) | Urteil |
|---|---|---|---|
| 1 | LFP −45…−75 kg → 545–575 kg (80–85 %); NMC −50…−85 kg → 400–430 kg (72–77 %) | Summe der Opus-Spannen LFP −{L['summe_spanne_kg'][0]}…−{L['summe_spanne_kg'][1]} kg → **{f0(L['masse_neu_kg'][0])}…{f0(L['masse_neu_kg'][1])} kg** (Zellanteil {f1(L['zellanteil_neu_prozent'][0])}…{f1(L['zellanteil_neu_prozent'][1])} %); NMC −{N['summe_spanne_kg'][0]}…−{N['summe_spanne_kg'][1]} kg → **{f0(N['masse_neu_kg'][0])}…{f0(N['masse_neu_kg'][1])} kg** (Zellanteil {f1(N['zellanteil_neu_prozent'][0])}…{f1(N['zellanteil_neu_prozent'][1])} %) | im Wesentlichen bestätigt; die Summen der Einzelspannen sind etwas breiter als die Erwartung (Rundung); die Spannen selbst sind ungeprüft (siehe Befunde 1, 2, 4) |
| 2 | LFP-Ziel 528 kg nur mit Cell-to-Pack; NMC 370 kg unerreichbar | LFP: auch mit der oberen Spanne {f0(L['masse_neu_kg'][0])} kg, Lücke zum Ziel {f0(L['luecke_zum_ziel_kg'][0])}…{f0(L['luecke_zum_ziel_kg'][1])} kg. NMC: Zellen allein {f0(N['zellen_kg'])} kg, für 370 kg blieben {f0(N['rest_max_fuer_ziel_kg'])} kg Rest, der Rest wiegt heute {f0(N['rest_kg'])} kg und müsste um {f0(N['rest_muss_sinken_um_kg'])} kg sinken (obere Spanne: Lücke {f0(N['luecke_zum_ziel_kg'][0])}…{f0(N['luecke_zum_ziel_kg'][1])} kg). LFP-Rest muss um {f0(L['rest_muss_sinken_um_kg'])} kg sinken | bestätigt (kein Ziel erreicht, auch nicht mit der oberen Spanne) |
| 3 | H1/H2 größte Hebel; H2 berührt Crash X3 und Dichtheit | H1 ({rg(L,'H1')} kg) und H2 ({rg(L,'H2')} kg) haben die größten Spannen (Summe {L['hebel']['H1']['spanne_kg'][1]+L['hebel']['H2']['spanne_kg'][1]} von höchstens {L['summe_spanne_kg'][1]} kg), aber nur nach Annahme Opus; **die Rückrechnung stellt H1 infrage** (Befund 1) | teilweise bestätigt (Rangfolge ja, Machbarkeit H1 unsicher) |

## Masse der Gruppen ab 3 kg und Nachrechnung (b)
Nachrechnung aus Maßen und Dichten (`parameter_<V>.json`, Block A), Abweichung gegen CAD-Masse; Grenze der Erwartung 5 %. Alle Gruppen liegen innerhalb. Bei Gruppenverbinder und Gruppenbrücke nur Volumen × Dichte Al (Konsistenzprüfung), keine Geometrienachrechnung.

**LFP** (Ist {f1(L['masse_ist_kg'])} kg, Zellen {f1(L['zellen_kg'])} kg, Rest {f1(L['rest_kg'])} kg)

| Gruppe | CAD [kg] | nachgerechnet [kg] | Abw. [%] | Werkstoff (CAD) |
|---|---|---|---|---|
{gr(L)}

**NMC** (Ist {f1(N['masse_ist_kg'])} kg, Zellen {f1(N['zellen_kg'])} kg, Rest {f1(N['rest_kg'])} kg)

| Gruppe | CAD [kg] | nachgerechnet [kg] | Abw. [%] | Werkstoff (CAD) |
|---|---|---|---|---|
{gr(N)}

Gruppen ohne Hebel in der Liste: Querträger (4,2 kg), NMC Zellträger (3,1 kg), Gruppenverbinder (7,9 kg), Gruppenbrücke (3,0 kg). Die Verbinder sind als Al angenommen, „Cu offen“ (`ergebnis_NMC_e2d_e3c.json`).

## Befunde (Abweichungen zur Erwartung, an Opus)
1. **Kühlplatte (H1):** Die 46,9 kg (LFP) sind **nicht 6 mm vollflächig**, sondern Hüllmaß 8 mm (ENT-090) × Füllgrad 0,4 (Annahme Opus 2026-11-17: 2 Bleche je 1,5 mm + Kanalstege) = äquivalent {f1(rl['H1']['aequiv_dicke_ist_mm'])} mm Al je Platte. 6 mm vollflächig wären {f1(rl['H1']['masse_6mm_voll_kg'])} kg. Für −15…−25 kg müsste der Füllgrad auf {f2(rl['H1']['fuellgrad_fuer_spanne'][0])}…{f2(rl['H1']['fuellgrad_fuer_spanne'][1])} fallen, das heißt äquivalent {f1(rl['H1']['aequiv_dicke_fuer_spanne_mm'][0])}…{f1(rl['H1']['aequiv_dicke_fuer_spanne_mm'][1])} mm. Der Ist-Ansatz liegt bereits bei zwei Blechen mit zusammen 3,0 mm plus Stegen; die Spanne verlangt dünnere Bleche **und** Stege. Ob das tragfähig und dicht ist, ist ungeprüft. Die Spanne H1 ist damit wahrscheinlich zu hoch (Opus entscheiden).
2. **Seitenrahmen (H6):** Der Ist-Wert ist **bereits** ein Mehrkammerprofil (Faktor {f2(rl['H6']['faktor_ist'])} gegen Vollprofil {f1(rl['H6']['masse_vollprofil_kg'])} kg; Wand 2,5 mm, 3 Kammern). Die Spanne −5…−10 kg verlangt Wand {f2(rl['H6']['wand_fuer_spanne_mm'][0])}…{f2(rl['H6']['wand_fuer_spanne_mm'][1])} mm (LFP), also unter dem W22-Bereich 2–3 mm. Mit 2,0 mm Wand: {f1(rl['H6']['masse_wand_2mm_kg'])} kg (−{f1(L['gruppen'][2]['masse_kg']-rl['H6']['masse_wand_2mm_kg'])} kg).
3. **Unterfahrschutz (H3):** Im CAD ist er **Al, 3 mm** (`ergebnis_LFP_e2d_e3c.json`, werkstoff Al), nicht Stahl. Der Hebel „Stahl hochfest dünner“ ist daher ein Werkstoffwechsel; die Dichte von Stahl steht nicht in den Akten, deshalb keine Rechnung (neue Annahme, Opus). Die Spanne entspricht {f0(rl['H3']['anteil_prozent'][0])}…{f0(rl['H3']['anteil_prozent'][1])} % der Masse, bei Al äquivalent {f2(rl['H3']['aequiv_al_dicke_mm'][0])}…{f2(rl['H3']['aequiv_al_dicke_mm'][1])} mm.
4. **Pad (H5):** Aus der Geometrie: Fläche des Pads {f0(rl['H5']['pad_flaeche_cm2'])} cm² gegen Zellfußfläche {f0(rl['H5']['zellfussflaeche_cm2'])} cm² (LFP) bzw. {f0(rn['H5']['pad_flaeche_cm2'])} gegen {f0(rn['H5']['zellfussflaeche_cm2'])} cm² (NMC). „Nur unter den Zellen“ spart LFP **{f1(rl['H5']['einsparung_geometrie_kg'])} kg** (−{f0(rl['H5']['anteil_prozent'])} %), NMC **{f1(rn['H5']['einsparung_geometrie_kg'])} kg** (−{f0(rn['H5']['anteil_prozent'])} %), gegen Spanne 4…7 kg: LFP liegt darunter, NMC in der Spanne. „Dünner“ als 1 mm ist ohne Wärmeleitwert nicht zu bewerten (Annahme fehlt).
5. **Verguss (H7):** Ist bereits nur bis halbe Zellhöhe (Anteil {f2(rn['H7']['vergusshoehe_anteil_ist'])}, Annahme AUFTRAG G4). Die Spanne −5…−8 kg verlangt Anteil {f2(rn['H7']['anteil_fuer_spanne'][0])}…{f2(rn['H7']['anteil_fuer_spanne'][1])}. Dichte 300 kg/m³ ist Annahme (PU-Schaum), die Masse wirkt klein gegen Zellmasse, die Sicherheitsfunktion (Propagation) ist nicht gerechnet.
6. **Boden (H2):** Boden ist Al, 3 mm, {f1(L['gruppen'][1]['masse_kg'])} kg; die Spanne −10…−20 kg entspricht {f0(rl['H2']['anteil_boden_prozent'][0])}…{f0(rl['H2']['anteil_boden_prozent'][1])} % des Bodens. Entfällt der Boden ganz, sind es höchstens {f1(rl['H2']['obergrenze_boden_entfaellt_kg'])} kg (ohne Verstärkung der Kühlplatte); dazu entfallen 3 mm Boden + 5 mm Luft = {rl['H2']['hoehe_gewinn_mm']:.0f} mm Bauhöhe (Stapel {f0(L['hoehe_stapel_mm'])} mm, Grenze {f0(L['hoehe_max_mm'])} mm). **H1 und H2 sind nicht additiv:** trägt die Kühlplatte, muss sie dicker werden, das widerspricht H1.
7. **Anforderungsnummer:** Die Erwartung nennt Crash als REQ-P13; im Lastenheft ist REQ-P13 Schutzart/Isolation, **Crash ist REQ-P14** (`docs/01_lastenheft.md`). Hier wird REQ-P14 verwendet.
8. **H4 (Deckel):** Werkstoffdichte Verbund (SMC) steht nicht in den Akten; nur Rückrechnung: Spanne = {f0(rl['H4']['anteil_prozent'][0])}…{f0(rl['H4']['anteil_prozent'][1])} % der Deckelmasse.

## Tabelle je Hebel
Spalte kg: Spanne Opus (ERWARTUNG.md), LFP / NMC. Kosten, Sicherheit, Effizienz und Folgen sind **qualitative Einschätzungen von Sonnet ohne Rechnung**, Prüfung Opus (+ besser, 0 neutral, − schlechter, ? offen). Folge Thermik und Crash sind **nicht nachgewiesen**, sondern Prüfaufträge.

| Hebel | kg LFP / NMC | Rückrechnung (Quelle `ergebnis.json`) | Kosten | Sicherheit | Effizienz | Folge Crash (REQ-P14) / Thermik (REQ-P09) / Fertigung |
|---|---|---|---|---|---|---|
| H1 Kühlplatte dünner/Strangpressprofil | −{rg(L,'H1')} / −{rg(N,'H1')} | Füllgrad {f2(rl['H1']['fuellgrad_ist'])} → {f2(rl['H1']['fuellgrad_fuer_spanne'][0])}…{f2(rl['H1']['fuellgrad_fuer_spanne'][1])} | + (weniger Al; Strangpressprofil: Werkzeug) | − (Dichtheit, Beulen, Druck) | + (Masse) | Crash: Platte ist Teil der Last (Pfahl) → X3 prüfen; Thermik: Kanalquerschnitt und Druckverlust → K-Rechnung neu; Fertigung: Strangpress/Löten |
| H2 Boden + Kühlplatte zusammenlegen | −{rg(L,'H2')} / −{rg(N,'H2')} | {f0(rl['H2']['anteil_boden_prozent'][0])}…{f0(rl['H2']['anteil_boden_prozent'][1])} % des Bodens (LFP); höchstens {f1(rl['H2']['obergrenze_boden_entfaellt_kg'])} kg; Höhe −{rl['H2']['hoehe_gewinn_mm']:.0f} mm | + (weniger Teile) | − (IP67, Aufsetzen, Kühlmittel am Außenrand) | + (Masse, Höhe) | Crash: Boden ist heute die zweite Schale hinter dem Unterfahrschutz → X3 (Boden); Dichtheit: Schweiß-/Dichtnaht außen; nicht additiv mit H1 |
| H3 Unterfahrschutz dünner/Verbund | −{rg(L,'H3')} / −{rg(N,'H3')} | {f0(rl['H3']['anteil_prozent'][0])}…{f0(rl['H3']['anteil_prozent'][1])} %, äquiv. Al {f2(rl['H3']['aequiv_al_dicke_mm'][0])}…{f2(rl['H3']['aequiv_al_dicke_mm'][1])} mm; Ist Al, nicht Stahl | ? (Werkstoff) | − (Steinschlag, Aufsetzen REQ-P14) | + | Crash: Aufsetzen/Pfahl → X3; Thermik 0; Fertigung: neuer Werkstoff |
| H4 Deckel aus Verbund (SMC) | −{rg(L,'H4')} / −{rg(N,'H4')} | {f0(rl['H4']['anteil_prozent'][0])}…{f0(rl['H4']['anteil_prozent'][1])} % der Deckelmasse | ? | ? (Brandschutz, Druckentlastung, Schirmung EMV) | + | Crash gering; Thermik: Wärme/Flamme nach oben, Entgasungsweg → prüfen; EMV: Al schirmt, Verbund nicht |
| H5 Pad nur unter den Zellen/dünner | −{rg(L,'H5')} / −{rg(N,'H5')} (Geometrie: −{f1(rl['H5']['einsparung_geometrie_kg'])} / −{f1(rn['H5']['einsparung_geometrie_kg'])}) | Fläche {f0(rl['H5']['anteil_prozent'])} % (LFP) / {f0(rn['H5']['anteil_prozent'])} % (NMC) | + | 0 (dünner: − Toleranzausgleich) | + (Masse); dünner: − Wärmepfad prüfen | Thermik: Kontaktfläche nur unter Zellen; Spalt zwischen Zellen ohne Pad → K0/K1 neu |
| H6 Seitenrahmen Kammerprofil | −{rg(L,'H6')} / −{rg(N,'H6')} | Ist bereits Kammerprofil; Wand {f2(rl['H6']['wand_fuer_spanne_mm'][0])}…{f2(rl['H6']['wand_fuer_spanne_mm'][1])} mm (LFP) | 0 | − (Seitencrash, Wand unter W22-Bereich 2–3 mm) | + | Crash: Seitenpfahl, Quetschung → X1; Thermik 0; Fertigung: Strangpress, dünnwandig |
| H7 NMC Verguss nur oben | – / −{rg(N,'H7')} | Anteil {f2(rn['H7']['vergusshoehe_anteil_ist'])} → {f2(rn['H7']['anteil_fuer_spanne'][0])}…{f2(rn['H7']['anteil_fuer_spanne'][1])} (Ist schon halbe Höhe) | + | − (Propagation, Fixierung bei Crash) | + | Thermik: Verguss bremst Propagation → Nachweis nötig; Crash: Zellfixierung; Fertigung: weniger Schaum |

## Offen
- Band aus W51 (Serien-Zellanteil): `forschung/ergebnis/W51.md` fehlt, nicht eingetragen.
- Neue Annahmen nötig (nicht getroffen): Dichte Stahl und SMC (H3, H4); Wärmeleitwert Pad und Mindestdicke (H5); Mindestwand Kühlplatte (H1); Mindestwand Seitenrahmen unter 2 mm (H6).
- Die Spannen H1, H3, H6 sind laut Rückrechnung ohne Annahmen außerhalb der Liste nicht belegbar; Opus entscheidet, ob sie gelten oder gesenkt werden.
- Crash- und Thermikfolgen sind Prüfaufträge, nicht nachgewiesen. Das CAD bleibt unverändert (REQ-P07 Ziel nicht neu festgelegt).

*KI-generiert (Claude Sonnet, 2026-11-24), Entwurf, nicht freigegeben.*
"""
open(f"{O}/ERGEBNIS.md", "w", encoding="utf-8").write(md)
