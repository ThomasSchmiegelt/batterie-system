#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. Auftrag G4. Massenbalken mit Zielband, entwurf/ergebnis.json, pack_lesehilfe.md, ERGEBNIS.md, Baustein G4.
Zahlen nur aus entwurf/ergebnis_<V>.json und sim/chemie/varianten_lfp_nmc/ergebnis.json. Bänder: ERWARTUNG.md (Opus) Punkt 3."""
import json, os
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")); D = f"{R}/cad/pack/entwurf"
BAND = {"LFP": (560, 620), "NMC": (390, 430)}   # ERWARTUNG.md Punkt 3
RES = {v: json.load(open(f"{D}/ergebnis_{v}.json")) for v in ("LFP", "NMC")}
C0 = json.load(open(f"{R}/sim/chemie/varianten_lfp_nmc/ergebnis.json"))["varianten"]
C0A = {v: C0[v]["faelle"]["A"]["hauptwert"]["m_pack_kg"] for v in RES}
NAME = {"Zellen": "Zellen", "Kuehlplatte": "Kühlplatten (Füllgrad 0,4)", "Seitenrahmen": "Seitenrahmen (Mehrkammer)", "Unterfahrschutz": "Unterfahrschutz", "Boden": "Boden", "Deckel": "Deckel",
        "Quertraeger": "Querträger", "Zellverbinder": "Verbinder/Abgriffe", "Gruppenverbinder": "Verbinder/Abgriffe", "Gruppenbruecke": "Verbinder/Abgriffe", "Pad": "Pad, Zellträger, Verguss", "Zelltraeger": "Pad, Zellträger, Verguss", "Verguss": "Pad, Zellträger, Verguss", "Zellabgriff": "Verbinder/Abgriffe"}
FARB = {"Zellen": "#1f77b4", "Kühlplatten (Füllgrad 0,4)": "#17becf", "Seitenrahmen (Mehrkammer)": "#7f7f7f", "Unterfahrschutz": "#444444", "Boden": "#aaaaaa", "Deckel": "#cccccc", "Querträger": "#ff7f0e", "Verbinder/Abgriffe": "#d62728", "Pad, Zellträger, Verguss": "#bcbd22"}
fig, ax = plt.subplots(figsize=(11, 6.5))
for i, v in enumerate(RES):
    agg = {}
    for g, x in RES[v]["gruppen"].items():
        if x["masse_bekannt"]: agg[NAME[g]] = agg.get(NAME[g], 0) + x["masse_kg"]
    b = 0
    for k in FARB:
        if k in agg: ax.bar(i, agg[k], 0.5, bottom=b, color=FARB[k], label=k if i == 0 else None, edgecolor="white"); b += agg[k]
    lo, hi = BAND[v]; ax.add_patch(plt.Rectangle((i - 0.38, lo), 0.76, hi - lo, fill=False, ec="green", lw=2.5, hatch="//", alpha=.9))
    ax.text(i, b + 12, f"CAD {RES[v]['masse_bekannt_kg']:.0f} kg", ha="center", fontweight="bold")
    ax.plot([i - 0.38, i + 0.38], [C0A[v]] * 2, color="black", ls="--"); ax.text(i + 0.4, C0A[v], f"C0b Fall A {C0A[v]:.0f} kg", va="center", fontsize=9)
ax.plot([], [], color="green", lw=2.5, label="Zielband ERWARTUNG (LFP 560–620, NMC 390–430)")
ax.set_xticks(range(2)); ax.set_xticklabels([f"LFP ({RES['LFP']['zellen']} Zellen)", f"NMC ({RES['NMC']['zellen']} Zellen)"]); ax.set_ylabel("Masse [kg]"); ax.set_xlim(-0.6, 1.9); ax.set_ylim(0, 900)
ax.set_title("G4: Packmasse aus CAD-Volumen (Dichten Pad/Zellträger/Verguss, Kühlplatten-Füllgrad, Rahmenprofil: Annahmen)", fontsize=10); ax.legend(loc="upper right", fontsize=8)
fig.text(.01, .01, "KI-generiert (Claude Sonnet), Entwurf, nicht freigegeben. Quelle: cad/pack/entwurf/ergebnis_LFP.json, ergebnis_NMC.json; C0b: sim/chemie/varianten_lfp_nmc/ergebnis.json", fontsize=7)
fig.tight_layout(); fig.savefig(f"{D}/pack_massen.png", dpi=110); plt.close(fig)
dev = {v: 100 * (RES[v]["masse_bekannt_kg"] / C0A[v] - 1) for v in RES}
ok = {v: BAND[v][0] <= RES[v]["masse_bekannt_kg"] <= BAND[v][1] for v in RES}
json.dump({"hinweis": "KI-generiert, Entwurf. Sammelergebnis G4, erzeugt von cad/pack/pack_massen.py", "masse_kg": {v: RES[v]["masse_bekannt_kg"] for v in RES}, "c0b_fall_A_kg": C0A, "abweichung_prozent": dev, "im_band": ok, "baender": BAND, "quellen": ["cad/pack/entwurf/ergebnis_LFP.json", "cad/pack/entwurf/ergebnis_NMC.json"]}, open(f"{D}/ergebnis.json", "w"), indent=1, ensure_ascii=False)
L, N = RES["LFP"], RES["NMC"]
ST = "; ".join(v + ": " + ", ".join(f"{k} {n}" for k, n in sorted(__import__('collections').Counter(str(x.get('status', '')).split(' ')[0] for b in json.load(open(f'{D}/parameter_{v}.json'))['parameter'].values() for x in b.values() if x.get('wert') is not None).items())) for v in RES)
V0 = {v: json.load(open(f"{D}/ergebnis_{v}_vollmaterial.json")) for v in RES}
open(f"{D}/pack_lesehilfe.md", "w", encoding="utf-8").write(f"""> **KI-generiert** (Claude Sonnet, 2026-11-17), Entwurf.

**Lesehilfe zu pack_massen.png.** Zwei gestapelte Säulen: links der LFP-Pack, rechts der NMC-Pack, jeweils aus den Massen der Bauteile im CAD (Zellen blau, Kühlplatten türkis, Rahmen und Wanne grau, Querträger orange). Das grün schraffierte Rechteck ist das Zielband aus der Erwartung, die gestrichelte schwarze Linie die Masse aus der Chemierechnung C0b. LFP liegt bei {L['masse_bekannt_kg']:.0f} kg, NMC bei {N['masse_bekannt_kg']:.0f} kg. Liegt die Säule über dem Band, sind die Platten im Modell zu schwer angesetzt (Kühlplatten mit Füllgrad 0,4 und Mehrkammer-Rahmen sind Annahmen).

**Lesehilfe zu pack_LFP_gesamt.png, pack_NMC_gesamt.png.** Blick schräg von oben auf das geschlossene Gehäuse (Deckel, Rahmen, Unterfahrschutz). Maße im Titel aus dem Modell.

**Lesehilfe zu pack_LFP_explosion.png, pack_NMC_explosion.png.** Alle Schichten auseinandergezogen, von unten Unterfahrschutz, Boden, Kühlplatte, Pad, Zellen mit Querträgern und Verbindern, Pad, Kühlplatte, Deckel. Abstände sind nur Darstellung. Die Linien zeigen auf das beschriftete Teil.

**Lesehilfe zu pack_LFP_laengs.png, pack_NMC_laengs.png.** Schnitt in Längsrichtung durch die Mitte (halbe Breite). Zu sehen sind die Zellschicht zwischen den Kühlplatten und die drei Querträger als Hohlprofile. Der schwarze Balken ist 200 mm lang.

**Lesehilfe zu pack_LFP_quer.png, pack_NMC_quer.png.** Schnitt quer durch einen Querträger: das orange Hohlprofil läuft über die ganze Breite, darüber und darunter Kühlplatten. Balken 200 mm.

**Lesehilfe zu pack_LFP_schnitt.png, pack_NMC_schnitt.png.** Viertelschnitt: ein Viertel des Packs ist weggeschnitten, man sieht Zellen, Querträger und Plattenschichten im Inneren; der Deckel ist weggelassen.\n\n**Lesehilfe zu pack_LFP_ecke.png, pack_NMC_ecke.png.** Derselbe Viertelschnitt, Blick auf die Schnittfläche an der Außenwand: LFP zeigt dort die Zellverbinder (kurze Kupfer-/Alu-Laschen am äußeren Zellende), NMC Zellträger, Verguss, Abgriffe und Gruppenverbinder.

*KI-generiert, Entwurf.*
""")
import re   # je Bild ein eigener Absatz "Lesehilfe zu <Datei>" (bilder.py sucht je Dateiname)
_t = open(f"{D}/pack_lesehilfe.md", encoding="utf-8").read(); _o = []
for ab in re.split(r"\n\s*\n", _t):
    m = re.match(r"\*\*Lesehilfe zu ([^*]*)\.\*\*(.*)", ab, re.S)
    if m and "," in m.group(1): _o += [f"**Lesehilfe zu {n.strip()}.**{m.group(2)}" for n in m.group(1).split(",")]
    else: _o.append(ab)
open(f"{D}/pack_lesehilfe.md", "w", encoding="utf-8").write("\n\n".join(_o))
f1 = lambda x: f"{x:.1f}"; jn = lambda c: "ERFÜLLT" if c else "VERFEHLT"
open(f"{R}/cad/pack/ERGEBNIS.md", "w", encoding="utf-8").write(f"""| Dok.-Nr. | ERG-G4 | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Ergebnis G4: Pack-CAD LFP und NMC (Entwurf) | Ersteller | Claude Sonnet (KI) | Prüfer | Opus (Stichprobe) |

> **KI-generiert.** Claude Sonnet, 2026-11-17, Auftrag G4. Entwurf, nicht freigegeben. Zahlen aus `cad/pack/entwurf/ergebnis_LFP.json`, `ergebnis_NMC.json`, `ergebnis.json`; Maße aus `cad/pack/entwurf/parameter_<V>.json` (Akten entschieden + vorgeschlagen, Block A = Annahmen, Bauraumlänge je Variante (LFP ENT-102, NMC ENT-103)).

## Abgleich ERWARTUNG.md
1. LFP: Gehäuse {L['laenge_mm']:.0f} x {L['breite_mm']:.0f} mm (erwartet 2030 x 1430), Höhe {L['hoehe_mm']:.0f} mm (≤ 130, M0 121), {L['zellen']} Zellen (2 x 125), 3 Querträger, Kollisionen {L['anzahl_kollisionen']} bei {L['kollisionspaare_geprueft']} geprüften Paaren: {jn(L['anzahl_kollisionen']==0 and L['hoehe_mm']<=130)}. Gehäuse = Bauraumlänge nach Freigabe (LFP 2030 mm ENT-102, NMC 1950 mm ENT-103).
2. NMC: {N['zellen']} Zellen, je Feld {N['zellen']//4} (4 Felder), Träger unten, Verguss (halbe Zellhöhe, Annahme), Verbinder oben, Pad, Kühlplatten. Höhe {N['hoehe_mm']:.0f} mm (erwartet 111, ≤ 130): {jn(N['hoehe_mm']<=130)}; Abweichung gegen 111: +{N['hoehe_mm']-111:.0f} mm, weil Zellabgriffe (1 mm) und Gruppenverbinder (3 mm) über der Zelle liegen und M0 sie nicht im Stapel hatte. Kollisionen {N['anzahl_kollisionen']} bei {N['kollisionspaare_geprueft']} Paaren: {jn(N['anzahl_kollisionen']==0)}.
3. Masse (Teile mit bekannter Masse): LFP {f1(L['masse_bekannt_kg'])} kg, erwartet 560–620, C0b Fall A {C0A['LFP']:.0f} kg, Abweichung {dev['LFP']:+.1f} %: {jn(ok['LFP'])}. NMC {f1(N['masse_bekannt_kg'])} kg, erwartet 390–430, C0b Fall A {C0A['NMC']:.0f} kg, Abweichung {dev['NMC']:+.1f} %: {jn(ok['NMC'])} (> 15 % → Opus). Massen nach Nachtrag (siehe unten; Erstlauf Vollmaterial in `ergebnis_<V>_vollmaterial.json`).
4. Schwerpunkt (Abweichung von der Mitte, ± 20 mm): LFP x {L['schwerpunkt_abw_mm'][0]:+.1f}, y {L['schwerpunkt_abw_mm'][1]:+.1f} mm: {jn(all(abs(a)<=20 for a in L['schwerpunkt_abw_mm']))}; NMC x {N['schwerpunkt_abw_mm'][0]:+.1f}, y {N['schwerpunkt_abw_mm'][1]:+.1f} mm: {jn(all(abs(a)<=20 for a in N['schwerpunkt_abw_mm']))} (Erstbelegung der NMC-Felder von links ergab x −40,5 mm, siehe `ergebnis_NMC_erstbelegung_links.json`, danach Zellen mittig im Feld).

## Offene Punkte (an Opus)
- Neue Annahme Platzhalter: NMC-Zellträger Dicke {N['annahmen']['A_traeger_dicke_NMC_mm']['wert']} mm (in M0 nicht gesetzt).
- Dichten Pad, Zellträger, Verguss, Kühlplatten-Füllgrad und Rahmenprofil sind Annahmen (Nachtrag).
- Verbinder als Aluminium angesetzt (Annahme, Kupfer offen).
- LFP: Zellen ohne Pole (Hüllkörper), Zellverbinder 25 x 3 nur am äußeren Zellende (3 mm in 4 mm Toleranz), je zwei Nachbarzellen, ohne Polarität; innen Zellen stoßen an (keine Verbinder in der Mitte).
- NMC: Gruppenverbinder je 4 Zellen eine Sammelschiene plus Reihenbrücke (Brücke stößt an, Länge Zellteilung minus Abgriffdurchmesser, nicht 48 mm wie E1), Zellabgriffe als Scheiben Ø 12 x 1; M0 hatte diese nicht im Höhenstapel (+4 mm).
- Bauraum nach Freigabe: LFP 2030 mm (ENT-102), NMC eigenes Gehäuse 1950 mm (ENT-103).

## Bilder (cad/pack/entwurf/)
`pack_<V>_gesamt|explosion|laengs|quer|schnitt.png` (je Variante, Beschriftung der Teile, Maßstabsbalken 200 mm in Schnitten), `pack_massen.png` (Zielband). Lesehilfe: `pack_lesehilfe.md`. Wiederholung ohne Codeänderung: `bash cad/pack/render_pack.sh`.

## Nachtrag 2026-11-17 (Auftrag Opus): Massenannahmen und Schnittbilder
- Annahmen (Opus), in `parameter_<V>.json` Block A: Kühlplatte Füllgrad A_KUEHLPLATTE_FUELLGRAD 0,4 (2 Bleche je 1,5 mm + Kanalstege); Seitenrahmen Mehrkammerprofil, Wand 2,5 mm, 3 Kammern; Dichten Pad 2500, Zellträger (PC) 1200, Verguss (PU-Schaum) 300 kg/m³. Geometrie unverändert (Volumenkörper), nur Massen und Schwerpunkt.
- Vorher (Vollmaterial, ohne Pad/Träger/Verguss): LFP {V0['LFP']['masse_bekannt_kg']:.1f} kg, NMC {V0['NMC']['masse_bekannt_kg']:.1f} kg (`ergebnis_<V>_vollmaterial.json`). Jetzt: LFP {L['masse_bekannt_kg']:.1f} kg ({jn(ok['LFP'])}, Band 560–620), NMC {N['masse_bekannt_kg']:.1f} kg ({jn(ok['NMC'])}, Band 390–430, {dev['NMC']:+.1f} % gegen C0b {C0A['NMC']:.0f} kg). Kühlplatten je Pack {L['gruppen']['Kuehlplatte']['masse_kg']:.1f} kg, Seitenrahmen LFP {L['gruppen']['Seitenrahmen']['masse_kg']:.1f} kg, NMC {N['gruppen']['Seitenrahmen']['masse_kg']:.1f} kg.
- Schwerpunkt jetzt: LFP x {L['schwerpunkt_abw_mm'][0]:+.1f}, y {L['schwerpunkt_abw_mm'][1]:+.1f} mm; NMC x {N['schwerpunkt_abw_mm'][0]:+.1f}, y {N['schwerpunkt_abw_mm'][1]:+.1f} mm (Soll ± 20 mm).
- Gruppenverbinder NMC geändert (je 4 Zellen kurz + Reihenbrücke, wie E1-Nachtrag), Kollisionen weiter {N['anzahl_kollisionen']}. Viertelschnitt: Kamera an der Schnittecke (Ausschnitt 380 mm), Deckel weggelassen, Beschriftungsanker auf dem Teil.

## Nachtrag „Freigabestand“ 2026-11-17
- Der Autor hat ENT-096…101 freigegeben und für NMC ein eigenes Gehäuse von 1950 mm entschieden (ENT-103, LFP 2030 mm = ENT-102). Maße neu aus den Akten (`parameter_<V>.json`, Status siehe dort: {ST}).
- Gehäuse jetzt LFP {L['laenge_mm']:.0f} x {L['breite_mm']:.0f} x {L['hoehe_mm']:.0f} mm, NMC {N['laenge_mm']:.0f} x {N['breite_mm']:.0f} x {N['hoehe_mm']:.0f} mm; Zellen {L['zellen']} / {N['zellen']} (NMC gleichmäßig auf 4 Felder, je {N['zellen']//4}).
- Masse: LFP {L['masse_bekannt_kg']:.1f} kg ({jn(ok['LFP'])}, Band 560–620, {dev['LFP']:+.1f} % gegen C0b), NMC {N['masse_bekannt_kg']:.1f} kg ({jn(ok['NMC'])}, Band 390–430, {dev['NMC']:+.1f} % gegen C0b). Schwerpunkt LFP x {L['schwerpunkt_abw_mm'][0]:+.1f}, y {L['schwerpunkt_abw_mm'][1]:+.1f} mm; NMC x {N['schwerpunkt_abw_mm'][0]:+.1f}, y {N['schwerpunkt_abw_mm'][1]:+.1f} mm. Kollisionen {L['anzahl_kollisionen']} / {N['anzahl_kollisionen']}.
- Beschriftung: Anker werden aus der Teilegeometrie berechnet (sichtbarer Eckpunkt per Strahltest, Teile ohne sichtbaren Punkt bleiben unbeschriftet). Neue Ansicht `pack_<V>_ecke.png` zeigt im Schnitt die Zellverbinder (LFP) an der Außenwand.

*KI-generiert, Entwurf. Dokument ERG-G4, Version 1.0.*
""")
os.makedirs(f"{R}/praesentation/bausteine", exist_ok=True)
open(f"{R}/praesentation/bausteine/G4.md", "w", encoding="utf-8").write(f"""> **KI-generiert** (Claude Sonnet, 2026-11-17), Entwurf. Folienbaustein Vorgang G4 (Pack-CAD).

# Beide Packs als parametrisches CAD
**Kernaussage (Opus einzusetzen): Beide Packs stehen als kollisionsfreies Entwurfs-CAD ({L['laenge_mm']:.0f} x {L['breite_mm']:.0f} x {L['hoehe_mm']:.0f} mm LFP, {N['laenge_mm']:.0f} x {N['breite_mm']:.0f} x {N['hoehe_mm']:.0f} mm NMC); die Masse liegt mit {L['masse_bekannt_kg']:.0f} kg (LFP, im Zielband: {jn(ok['LFP'])}) und {N['masse_bekannt_kg']:.0f} kg (NMC, {dev['NMC']:+.0f} % gegen C0b, Zielband {jn(ok['NMC'])}) auf Basis gesetzter Massenannahmen.**

**Bild:** cad/pack/entwurf/pack_massen.png (Zielband LFP 560–620 kg, NMC 390–430 kg), pack_LFP_explosion.png, pack_NMC_explosion.png, *_quer.png, *_ecke.png

**Zahlen** (Quelle cad/pack/entwurf/ergebnis_LFP.json, ergebnis_NMC.json, ergebnis.json):
- Masse LFP {L['masse_bekannt_kg']:.0f} kg, NMC {N['masse_bekannt_kg']:.0f} kg (C0b Fall A {C0A['LFP']:.0f} / {C0A['NMC']:.0f} kg)
- Kollisionen {L['anzahl_kollisionen']} / {N['anzahl_kollisionen']}; Schwerpunktabweichung LFP {L['schwerpunkt_abw_mm'][0]:+.1f} mm, NMC {N['schwerpunkt_abw_mm'][0]:+.1f} mm in x
- Teil der Akten freigegeben (ENT-096…103), Rest vorgeschlagen; Massenannahmen (Füllgrad, Profil, Dichten) bei Opus

*KI-generiert, Entwurf.*
""")
print("OK", dev, ok)
