#!/usr/bin/env python3
# KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. Auftrag G2-D (cad/zelle/AUFTRAG_DETAIL.md).
"""Fasst ergebnis_detail_LFP.json und ergebnis_detail_NMC.json zu ergebnis_detail.json zusammen und schreibt
ERGEBNIS_detail.md, detail_lesehilfe.md und den Folienbaustein praesentation/bausteine/G2_detail.md. Alle Zahlen aus den JSON (keine eigenen)."""
import json, os
R = os.environ.get("BATTERIE", "/home/cae/hermes/batterie")
DET = f"{R}/cad/zelle/entwurf/detail"
L = json.load(open(f"{DET}/ergebnis_detail_LFP.json")); N = json.load(open(f"{DET}/ergebnis_detail_NMC.json"))
json.dump({"hinweis": "KI-generiert, ENTWURF (Akten vorgeschlagen). Zusammenfassung aus ergebnis_detail_LFP.json und ergebnis_detail_NMC.json (cad/zelle/detail_bericht.py).", "LFP": L, "NMC": N},
          open(f"{DET}/ergebnis_detail.json", "w"), indent=1, ensure_ascii=False)
s, ln, w = L["stapel"], L["laengen_mm"], N["wickel"]
def f1(x): return f"{x:.1f}".replace(".", ",");
def f2(x): return f"{x:.2f}".replace(".", ",")
def f3(x): return f"{x:.3f}".replace(".", ",")
def ok(b): return "erfüllt" if b else "**verfehlt**"
ueberstand = -w["abstand_wickel_zu_becher_mm"]; passt = w['aussenradius_wickel_max_mm'] <= w['becher_innenradius_mm']
KOPF = lambda nr, titel: (f"| Dok.-Nr. | {nr} | Version | 1.0 | Status | Entwurf |\n|---|---|---|---|---|---|\n| Titel | {titel} | Ersteller | Claude Sonnet (KI) | Prüfer | Opus (Modell, Bilder, Zahlen) |\n\n")
FUSS = "\n---\n*KI-generiert (Claude Sonnet, 2026-11-17), Entwurf, nicht vom Menschen freigegeben.*\n"
ann_l = ", ".join(f"{k[2:]} {v:g}" for k, v in L["annahmen"].items())
ann_n = ", ".join(f"{k[2:]} {v:g}" for k, v in N["annahmen"].items())
tn = N["volumen_je_teil_cm3"]; tl = L["volumen_je_teil_cm3"]
md = KOPF("ERG-G2D", "Ergebnis G2-D: Detailmodell Innenaufbau LFP und 4680 mit Schnittbildern") + f"""> **KI-generiert.** Entwurf, nicht freigegeben; Akten ENT-015 (681 mm) und ENT-031…080 nur „vorgeschlagen“. Quelle aller Zahlen: `cad/zelle/entwurf/detail/ergebnis_detail.json` (aus `ergebnis_detail_LFP.json`, `ergebnis_detail_NMC.json`, erzeugt von `cad/zelle/zelle_detail.py`).

## Was getan
- `cad/zelle/zelle_detail.py` (FreeCAD 1.1.4 headless) baut je Variante das Innenleben aus `parameter_<V>_entwurf.json` (vorher `entwurf_parameter.py` neu gelaufen) und aus `cad/zelle/aufbau_W20.json` (nur die Fahnenbreiten LFP). Ausgabe: `zelle_LFP_detail.FCStd/.step`, `zelle_NMC_detail.FCStd/.step`, OBJ je Teil und Satz in `render/`.
- **LFP:** {s['kathoden']} Kathoden, {s['anoden']} Anoden, {s['separatorlagen']} Separatorlagen mit echten Dicken (je Blatt Folie und zwei Beschichtungen als eigene Körper), Falzbänder, Kathodenfahnen an einem, Anodenfahnen am anderen Ende, Stromschienen, Pole, zweiteilige Kunststoffhalter, O-Ringe, Isolationsbeutel, Al-Gehäuse 0,3 mm mit PET-Folie, Ventil, Füllstopfen.
- **4680:** Spirale als vier Bänder (Kathode, Separator, Anode, Separator; Folie und zwei Beschichtungen je Elektrode getrennt) mit echter archimedischer Spirale ab Kern Ø {2*w['kern_radius_mm']:g} mm, Bandlängen aus den Akten, Ringscheiben als „gefalteter Rand“ oben (Al) und unten (Cu), zwei Tab-Scheiben mit je 6 Dreiecken, Becher, Deckel, Dichtring, Isolierring, Pluspol, Blindniet, Bodenventil, Klebestreifen. Die Spirale ging in FreeCAD (kein Rückfall auf Blender nötig; Laufzeit 5 min).
- `cad/zelle/render_detail.py` (Blender 4.0, Cycles CPU, orthografisch) und `render_detail_beschriftung.py` (PIL: Pfeile, Namen, Maßstabsbalken, Titel, Fußzeile) erzeugen 8 Bilder in `cad/zelle/entwurf/detail/`.

## Zahlen (Fundstelle `ergebnis_detail.json`)
| Größe | Wert | Pfad im JSON |
|---|---|---|
| LFP Stapeldicke | {f3(s['stapeldicke_mm'])} mm | LFP.stapel.stapeldicke_mm |
| LFP Innendicke (14 − 2 × 0,3) | {f1(s['innendicke_mm'])} mm | LFP.stapel.innendicke_mm |
| LFP Rest zur Innendicke | {f3(s['rest_zur_innendicke_mm'])} mm (nach Beutel {f3(s['rest_nach_beutel_mm'])} mm) | LFP.stapel.rest_zur_innendicke_mm, rest_nach_beutel_mm |
| LFP Platz Stromschiene bis Stirnwand | Kathode {f2(ln['innen_platz_stromschiene_bis_wand_kathode'])} mm, Anode {f2(ln['innen_platz_stromschiene_bis_wand_anode'])} mm | LFP.laengen_mm |
| LFP Endzone je Seite ab Separatorrand | {f1(ln['endzone_je_seite_ab_separator'])} mm | LFP.laengen_mm.endzone_je_seite_ab_separator |
| 4680 Windungen Kathode / Anode / Separator | {f2(w['windungen_kathode'])} / {f2(w['windungen_anode'])} / {f2(w['windungen_separator1'])} und {f2(w['windungen_separator2'])} | NMC.wickel.windungen_* |
| 4680 Außenradius Kathode / Anode / Separator | {f2(w['aussenradius_kathode_mm'])} / {f2(w['aussenradius_anode_mm'])} / {f2(w['aussenradius_separator_mm'])} mm | NMC.wickel.aussenradius_* |
| 4680 Becher-Innenradius | {f2(w['becher_innenradius_mm'])} mm | NMC.wickel.becher_innenradius_mm |
| **4680 Abstand Wickel zu Becher** | **{f2(w['abstand_wickel_zu_becher_mm'])} mm** (negativ = Überstand) | NMC.wickel.abstand_wickel_zu_becher_mm |
| 4680 Dicke je Windung | {f2(w['dicke_je_windung_voll_mm'])} mm (solange alle 4 Bänder wickeln; danach kleiner) | NMC.wickel.dicke_je_windung_voll_mm |
| 4680 Wickelhöhe / freie Höhe bis Deckel | z {w['hoehe_z_von_bis_mm'][0]:g}…{w['hoehe_z_von_bis_mm'][1]:g} mm / {f1(w['freie_hoehe_oben_bis_deckel_mm'])} mm | NMC.wickel |
| Volumen Elektroden LFP (Kathoden-Beschichtung / Anoden-Beschichtung / Separator) | {f1(tl['Kathode_Beschichtung'])} / {f1(tl['Anode_Beschichtung'])} / {f1(tl['Separator'])} cm³ | LFP.volumen_je_teil_cm3 |
| Volumen 4680 (Kathoden-Beschichtung / Anoden-Beschichtung / Separator / Becher) | {f1(tn['Kathode_Beschichtung'])} / {f1(tn['Anode_Beschichtung'])} / {f1(tn['Separator'])} / {f1(tn['Becher_Stahl'])} cm³ | NMC.volumen_je_teil_cm3 (ungeschnittener Wickel) |
| Gültigkeit der Solids | LFP {sum(L['gueltig'].values())}/{len(L['gueltig'])}, 4680 {sum(N['gueltig'].values())}/{len(N['gueltig'])} gültig | gueltig |

## Abgleich mit dem Erwartungs-Nachtrag (`cad/zelle/ERWARTUNG.md`, 2026-11-17)
1. **LFP-Stapel 12,48 mm in 13,4 mm, Rest ≈ 0,9 mm:** Ist {f3(s['stapeldicke_mm'])} mm, Rest {f3(s['rest_zur_innendicke_mm'])} mm: {ok(s['rest_zur_innendicke_mm'] >= 0 and abs(s['stapeldicke_mm'] - 12.48) < 0.01)}. Elektrodenlängen 615,5/620/631 mm kommen aus den Akten ENT-032/038/044. Endzone: Das Skript liefert {f1(ln['endzone_je_seite_ab_separator'])} mm je Seite ab Separator (Erwartung „≈ 25–33 mm“, die Untergrenze 25 ist gerundet): {ok(24.5 <= ln['endzone_je_seite_ab_separator'] <= 33)}.
2. **4680 Windungen, Außenradius ≤ 22,6 mm, Kern:** (Opus-Korrektur: ENT-074 Kern Ø {2*w['kern_radius_mm']:g} mm; flächentreue Spirale, Bänder gemeinsam am Kern, `A_NMC_BAND_START_VERSATZ_MM` = 0, da Abb. 5B nicht in aufbau_W20.json.) Kathode {f2(w['windungen_kathode'])} Windungen (Erwartung ≈ 35, Band 30–38 erfüllt; Abweichung zum „≈ 35“ {f2(w['windungen_kathode']-35)}, weil der Wickel am Kern bei R = r₀ beginnt und die erste Windung bis {f2(w['kleinster_innenradius_mm'])} mm nach innen reicht). Außenradius Wickel {f2(w['aussenradius_wickel_max_mm'])} mm (Flächenformel √(r₀² + Σ Dicke·Länge/π) = {f2(w['aussenradius_flaechenformel_mm'])} mm, Erwartung ≈ 22,57) gegen Becher innen {f2(w['becher_innenradius_mm'])} mm, Abstand {f3(w['abstand_wickel_zu_becher_mm'])} mm: {ok(passt)}. Kathode endet bei {f2(w['aussenradius_kathode_mm'])} mm, Anode {f2(w['aussenradius_anode_mm'])} mm, Separator {f2(w['aussenradius_separator_mm'])} mm.
3. **Breiten** (LFP 82,5/85/87 mm in 89,4 mm, 4680 72/73/75 mm in 80 mm): aus den Akten übernommen; 4680 Wickelhöhe {w['hoehe_z_von_bis_mm'][1] - w['hoehe_z_von_bis_mm'][0]:g} mm, oben bleiben {f1(w['freie_hoehe_oben_bis_deckel_mm'])} mm bis Deckelunterseite: erfüllt.
4. **Annahmen** stehen als `A_*` im Skript, in `ergebnis_detail_<V>.json` (Block `annahmen`) und in der Fußzeile jedes Bildes. LFP: {ann_l}. 4680: {ann_n}.

## Abweichungen, Deutungen, offene Punkte
- **Nachlauf 4680 (Opus-Auftrag, ENT-074 = Ø 12,5 mm):** Wickel flächentreu neu gebaut; er passt in den Becher, die Darstellung ist ungeschnitten. Der erste Lauf (feste Steigung 0,45 mm, Kern Ø 14 mm) ergab 1,15 mm Überstand, siehe BEFUNDE B-BAT-015, und ist überholt.
- **Fahnen 4680 (5 und 7,5 mm):** als Ringscheibe „gefalteter Rand“ (Dicke ANNAHME) dargestellt, nicht als Foliensteg; die Breiten 72/73 mm sind als Beschichtungsbreite gelesen (sonst wäre die Anode beschichtet schmaler als die Kathode). Das ist eine Lesart, Opus bitte prüfen.
- **Fahnenbreiten LFP** (27,1 / 20,5 mm) stehen in `aufbau_W20.json` als „Bedeutung unklar“; als Fahnenbreite verwendet (Abb. 5A). Lage der Fahnen mittig (Annahme).
- Nicht modelliert: {'; '.join(L['nicht_modelliert'])}; 4680: {'; '.join(N['nicht_modelliert'])}.
- Pol plus liegt bei x = Zelllänge (wie `zelle.py`), Kathodenfahnen und Ventil dort; Anode und Füllstopfen am anderen Ende.
- Die LFP-Schicht-Dicken sind im Schnittbild nicht sichtbar (0,16 mm bei 26 px/mm = 4 px); deshalb Lagenmodell oben im Bild mit Dicken × {L['annahmen']['A_UEBERHOEHUNG']:g} (Darstellung, keine Messung).
- Laufzeiten: LFP 5 s, 4680 5 min (FreeCAD, ohne GPU); je Bild 20 s bis 2 min (Blender CPU).
""" + FUSS
open(f"{DET}/ERGEBNIS_detail.md", "w", encoding="utf-8").write(md)

LH = KOPF("LH-G2D", "Lesehilfe zu den Detailbildern der Zellen (G2-D)") + f"""> **KI-generiert.** Entwurf, nicht freigegeben. Akten nur „vorgeschlagen“. Quelle der Zahlen: `cad/zelle/entwurf/detail/ergebnis_detail.json`. Begriffe: **Kathode** = Pluselektrode (Aluminiumfolie, beschichtet mit dem Speichermaterial); **Anode** = Minuselektrode (Kupferfolie, beschichtet mit Graphit); **Separator** = dünne, poröse Trennfolie, die Kathode und Anode elektrisch trennt, aber Ionen durchlässt; **Z-Faltung** = der Separator ist ein einziges Band, das wie eine Ziehharmonika zwischen den Elektroden hin und her gefaltet wird; **tabless** = ohne einzelne Anschlussfahnen: der Folienrand der Wickelstirn wird umgelegt und flächig mit einer Scheibe verschweißt. Zielbänder gibt es hier nicht (Form, keine Rechengröße); Annahmen stehen in der Fußzeile jedes Bildes.

**Lesehilfe zu `LFP_gesamt.png`** Die LFP-Zelle von außen: ein flacher Aluminiumkörper mit blauer PET-Schutzfolie. An den kurzen Enden sitzen die Pole (Plus Aluminium, Minus Kupfer), am Plusende das Ventil für den Überdruck und am Minusende der Gummistopfen der Füllöffnung. Der Balken ist 100 mm lang. Es ist dasselbe Modell, das in den anderen Bildern aufgeschnitten wird.

**Lesehilfe zu `LFP_schnitt.png`** Längsschnitt durch das Plusende: Die Zelle ist hier in der Mitte aufgeschnitten. Rechts sieht man den Stapel aus {s['kathoden']} Kathoden, {s['anoden']} Anoden und {s['separatorlagen']} Separatorlagen, zusammen {f2(s['stapeldicke_mm'])} mm dick in {f1(s['innendicke_mm'])} mm Innenraum. Links davon laufen die Kathodenfahnen (dünne Alufolien) zur Stromschiene, dann folgen der zweiteilige Kunststoffhalter und der Pol mit O-Ring. Die einzelnen Schichten sind im Gesamtschnitt nur Striche; oben im Bild steht ein Modellausschnitt mit **20-facher Dicke** (Darstellung, keine Messung), in dem Beschichtung, Folie und Separator getrennt zu erkennen sind. Der Balken ist 10 mm lang.

**Lesehilfe zu `LFP_explosion.png`** Explosionsbild der Endzone: Die Teile sind in Richtung der Zellachse und nach oben auseinandergezogen (Pol mit O-Ring links außen, dann Halter, Stromschiene, Stapelende; darüber Isolationsbeutel und Gehäuse mit Folie, beide nur als Hälfte, damit man hineinsieht). Der Kunststoffhalter besteht aus zwei Hälften, die hier zusammenliegen. Der Balken ist 10 mm lang. So sieht man, in welcher Reihenfolge die Zelle montiert wird.

**Lesehilfe zu `NMC_gesamt.png`** Die 4680-Rundzelle von außen: ein Stahlbecher (er ist der Minuspol), oben der Deckel mit dem kleinen Pluspol und einem schwarzen Dichtring. Boden, Blindniet und Ventil sind von außen nicht zu sehen, sie erscheinen im Viertelschnitt. Der Balken ist 20 mm lang.

**Lesehilfe zu `NMC_viertelschnitt.png`** Ein Viertel der Zelle ist weggeschnitten. Im Inneren sieht man den Wickel (vier Bänder, die zur Spirale aufgerollt sind: {f1(w['windungen_kathode'])} Windungen der Kathode), in der Mitte den leeren Kern, unten die Kupfer-Tab-Scheibe mit 6 Dreiecken, oben die Aluminium-Tab-Scheibe, darüber Isolierring, Deckel, Dichtring und Pluspol. Der Wickel passt mit {f2(w['abstand_wickel_zu_becher_mm'])} mm Abstand in den Becher. Der Balken ist 10 mm lang.

**Lesehilfe zu `NMC_draufsicht.png`** Blick von oben auf den Querschnitt durch den Wickel auf halber Höhe: eine **archimedische Spirale** (die Windungen liegen dicht an dicht; der Abstand beträgt {f2(w['dicke_je_windung_voll_mm'])} mm, solange alle vier Bänder wickeln, und wird kleiner, sobald Kathode und Anode enden), in der Mitte der leere Kern Ø {2*w['kern_radius_mm']:g} mm, außen der Stahlbecher. Dunkle Streifen sind Anode und Kathode, helle die Separatoren und Folien. Der Balken ist 10 mm lang.

**Lesehilfe zu `NMC_ausschnitt.png`** Zoom auf 6 mm am Becherrand desselben Schnitts. Die Pfeile zeigen auf die Lagen: Anode (Kupferfolie 10 µm zwischen zwei Graphitschichten 125 µm), Separator (10 µm), Kathode (Aluminiumfolie 20 µm zwischen zwei Schichten 75 µm). Die Reihenfolge von außen nach innen ist Becher, Separator, Anode, Separator, Kathode. Dünne weiße Linien können Separator oder Aluminiumfolie sein; die Pfeile geben die Lage an (Radius aus den Akten berechnet). Der Balken ist 1 mm lang.

Hinweis: Farben und Werkstoffe sind Anmutung, keine Messung.
""" + FUSS
open(f"{DET}/detail_lesehilfe.md", "w", encoding="utf-8").write(LH)

os.makedirs(f"{R}/praesentation/bausteine", exist_ok=True)
bp = f"{R}/praesentation/bausteine/G2_detail.md"
kern = "**Kernaussage:** (Opus)"
BS = f"""> **KI-generiert** (Claude Sonnet, 2026-11-17), Entwurf. Folienbaustein Vorgang G2 (Detailmodell Innenaufbau).

# Innenaufbau beider Zellen im Schnitt
{kern}

**Bild:** cad/zelle/entwurf/detail/LFP_schnitt.png und NMC_viertelschnitt.png (kein Zielband; Form des Innenaufbaus, Annahmen in der Fußzeile; zusätzlich NMC_draufsicht.png, NMC_ausschnitt.png, LFP_explosion.png)

**Zahlen** (Quelle cad/zelle/entwurf/detail/ergebnis_detail.json):
- LFP: {s['kathoden']} Kathoden, {s['anoden']} Anoden, {s['separatorlagen']} Separatorlagen = {f2(s['stapeldicke_mm'])} mm in {f1(s['innendicke_mm'])} mm Innendicke (Rest {f2(s['rest_zur_innendicke_mm'])} mm)
- 4680: {f1(w['windungen_kathode'])} Windungen der Kathode, {f2(w['dicke_je_windung_voll_mm'])} mm je Windung, Kern Ø {2*w['kern_radius_mm']:g} mm
- 4680: Wickel (flächentreu) Außenradius {f2(w['aussenradius_wickel_max_mm'])} mm gegen {f2(w['becher_innenradius_mm'])} mm Becher innen, passt

*KI-generiert, Entwurf.*
"""
if os.path.exists(bp):   # Kernaussage erhalten
    for z in open(bp, encoding="utf-8").read().splitlines():
        if z.startswith("**Kernaussage") and "(Opus)" not in z[-8:]: BS = BS.replace(kern, z)
open(bp, "w", encoding="utf-8").write(BS)
print("OK ergebnis_detail.json, ERGEBNIS_detail.md, detail_lesehilfe.md, G2_detail.md")
