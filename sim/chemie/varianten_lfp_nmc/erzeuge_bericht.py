#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-16). Schreibt ERGEBNIS.md, ERGEBNIS_kurz.txt und den Folienbaustein C0b aus ergebnis.json (keine eigenen Zahlen)."""
import json, os
D = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(D, "..", "..", ".."))
d = json.load(open(os.path.join(D, "ergebnis.json"), encoding="utf-8")); C = d["varianten"]
def F(c, f): return C[c]["faelle"][f]
def g(c, f, key, k): return F(c, f)[key][k]
def pct(x): return f"{x*100:.1f} %".replace(".", ",")
def n1(x): return f"{x:.1f}".replace(".", ",")
def n0(x): return f"{x:.0f}"
la, lb = F("LFP", "A"), F("LFP", "B"); na, nb = F("NMC", "A"), F("NMC", "B")
lg = {w: {f: C["LFP"]["faelle"][f]["gitter"][f"w{w}_k0.75"] for f in "AB"} for w in (160, 185, 210)}
KOPF = ("| Dok.-Nr. | ERG-C0b | Version | 1.0 | Status | Entwurf |\n|---|---|---|---|---|---|\n"
        "| Titel | Ergebnis Variantenvergleich LFP-Blade / NMC-4680 mit Messwerten (800 V, 400 km, 1500 kg) | Ersteller | Claude Sonnet (KI) | Prüfer | Opus (Rohdaten) |\n\n"
        "> **KI-generiert.** Entwurf, nicht freigegeben. Quelle aller Zahlen: `sim/chemie/varianten_lfp_nmc/ergebnis.json` (erzeugt von `varianten.py`, Eingaben `eingaben.json` und `../vergleich_lfp_nmc/eingaben.json`). Keine Deutung, die schreibt Opus.\n\n")
md = [KOPF]
md.append("## Rechenweg und Festlegungen\nWie C0 (Schritte 1–9). LFP: s = 250, p = 1, Ah aus Energie. NMC 4680: s = 217, Ah fest 23,125, p = ceil(E_brutto·1000/(s·U·Ah)), Packmasse = Zellen · 355 g / k, Fall B mit E_ist iteriert. Mitte des LFP-Zellbands = 185 Wh/kg (Bandmitte laut Auftrag); Hauptwert 160 (gemessen) zusätzlich. Packfaktor k 0,75 (Band 0,65–0,85). Bauraum: nötige Pack-Wh/L gegen Zelle-Wh/L × Volumennutzung; „knapp“ = innerhalb ±2 %.\n\n")
md.append("## Tabelle je Variante und Fall (Mitte = LFP 185 Wh/kg bzw. NMC fest, k 0,75)\n\n| Größe | LFP A | LFP B | NMC A | NMC B |\n|---|---|---|---|---|\n")
def row(name, fn):
    md.append(f"| {name} | " + " | ".join(fn(x) for x in (la, lb, na, nb)) + " |\n")
row("Reihe s", lambda x: str(x["mitte"]["zellen"] // x["mitte"]["p"]))
row("parallel p", lambda x: str(x["mitte"]["p"]))
row("Zellen", lambda x: str(x["mitte"]["zellen"]))
row("E_brutto Bedarf [kWh]", lambda x: n1(x["mitte"]["E_brutto_kWh"]))
row("E_ist [kWh]", lambda x: n1(x["mitte"]["E_ist_kWh"]))
row("Ah je Zelle", lambda x: n1(x["mitte"]["ah_noetig"]))
row("Packmasse Mitte [kg]", lambda x: n1(x["mitte"]["m_pack_kg"]))
row("Spanne über w und k [kg]", lambda x: f"{n0(x['m_pack_spanne_kg'][0])}–{n0(x['m_pack_spanne_kg'][1])}")
row("Gesamtmasse [kg]", lambda x: n0(x["mitte"]["gesamtmasse_kg"]))
row("Batterieanteil Mitte", lambda x: pct(x["mitte"]["batterieanteil"]))
row("Grenze 30 % [kg]", lambda x: n0(x["grenze_kg"]))
row("Anteil unter Grenze (Mitte)", lambda x: "ja" if x["anteil_unter_grenze"] else "nein")
row("Pack-Wh/L nötig", lambda x: n1(x["pack_Wh_L_noetig"]))
row("Bauraum", lambda x: x["bauraum_urteil"])
row("Schritte Fall B", lambda x: str(x["schritte"]))
md.append(f"\nZyklenbedarf {n0(d['zyklenbedarf'])}: LFP {C['LFP']['zyklen_urteil']} (Band {C['LFP']['zyklen_band']}), NMC {C['NMC']['zyklen_urteil']} (Band {C['NMC']['zyklen_band']}, keine 4680-Quelle).\n")
md.append("\n## LFP nach Zellwert (k 0,75)\n\n| w [Wh/kg] | Packmasse A [kg] | Anteil A | Ah A | E_brutto B [kWh] | Packmasse B [kg] | Anteil B | Ah B |\n|---|---|---|---|---|---|---|---|\n")
for w in (160, 185, 210):
    a, b = lg[w]["A"], lg[w]["B"]
    md.append(f"| {w}{' (gemessen, Hauptwert)' if w==160 else ' (Mitte)' if w==185 else ' (Hersteller)'} | {n1(a['m_pack_kg'])} | {pct(a['batterieanteil'])} | {n1(a['ah_noetig'])} | {n1(b['E_brutto_kWh'])} | {n1(b['m_pack_kg'])} | {pct(b['batterieanteil'])} | {n1(b['ah_noetig'])} |\n")
md.append("\n## NMC 4680 nach Packfaktor k (Zellwert fest)\n\n| k | Packmasse A [kg] | p A | Anteil A | Packmasse B [kg] | p B | Anteil B |\n|---|---|---|---|---|---|---|\n")
for k in (0.65, 0.75, 0.85):
    a, b = na["gitter"][f"k{k}"], nb["gitter"][f"k{k}"]
    md.append(f"| {k} | {n1(a['m_pack_kg'])} | {a['p']} | {pct(a['batterieanteil'])} | {n1(b['m_pack_kg'])} | {b['p']} | {pct(b['batterieanteil'])} |\n")
md.append("\n## Bauraum je Volumennutzung\n\n| Variante/Fall | nötig [Wh/L] | Volumennutzung | verfügbar [Wh/L] | Abweichung | Urteil |\n|---|---|---|---|---|---|\n")
for c in ("LFP", "NMC"):
    for f in "AB":
        for b in F(c, f)["bauraum"]:
            md.append(f"| {c} {f} | {n1(F(c,f)['pack_Wh_L_noetig'])} | {str(b['volumennutzung']).replace('.',',')} | {n1(b['verfuegbar_Wh_L'])} | {pct(b['abweichung'])} | {b['urteil']} |\n")
md.append("\n## Empfindlichkeit (Hub der Packmasse in kg, Mitte, je Größe einzeln)\n\n| Variante/Fall | Hub k | Hub w | Hub a | stärkste |\n|---|---|---|---|---|\n")
for c in ("LFP", "NMC"):
    for f in "AB":
        h = F(c, f)["empfindlichkeit_hub_kg"]
        md.append(f"| {c} {f} | {n0(h['k'])} | {n0(h['w']) if 'w' in h else '–'} | {n0(h['a']) if 'a' in h else '–'} | {F(c,f)['staerkste_annahme']} |\n")
# Abgleich
E_hb = lg[160]["B"]["E_brutto_kWh"]
def ok(b): return "erfüllt" if b else "verfehlt"
md.append("\n## Abgleich mit ERWARTUNG.md (Punkt für Punkt)\n\n")
md.append(f"1. Energie: Fall A {n1(la['mitte']['E_brutto_kWh'])} kWh für beide (erwartet 73,9): {ok(abs(la['mitte']['E_brutto_kWh']-73.9)<0.05)}. Fall B LFP {n1(lg[160]['B']['E_brutto_kWh'])} kWh bei 160 Wh/kg ({n1(lg[185]['B']['E_brutto_kWh'])} bei 185, {n1(lg[210]['B']['E_brutto_kWh'])} bei 210), erwartet 92–95: {ok(92<=E_hb<=95)}. Fall B NMC {n1(nb['mitte']['E_brutto_kWh'])} kWh Bedarf (E_ist {n1(nb['mitte']['E_ist_kWh'])}), erwartet 84–86: {ok(84<=nb['mitte']['E_brutto_kWh']<=86)}.\n")
md.append(f"2. Zellen: LFP {la['mitte']['zellen']}s × 1p, {n1(lg[160]['A']['ah_noetig'])} Ah (erwartet 250s, etwa 92 Ah): {ok(la['mitte']['zellen']==250 and 90<=lg[160]['A']['ah_noetig']<=94)}. NMC 217s × {na['mitte']['p']}p = {na['mitte']['zellen']} Zellen (erwartet 868): {ok(na['mitte']['zellen']==868)}; E_ist {n1(na['mitte']['E_ist_kWh'])} kWh (erwartet etwa 74): {ok(abs(na['mitte']['E_ist_kWh']-74)<1)}. Fall B p = {nb['mitte']['p']} (erwartet 5 möglich): {ok(nb['mitte']['p']==5)}.\n")
md.append(f"3. Masse Fall A: LFP {n0(lg[160]['A']['m_pack_kg'])} kg bei 160 (erwartet etwa 615, Prüfband 560–670): {ok(560<=lg[160]['A']['m_pack_kg']<=670)}; LFP {n0(lg[210]['A']['m_pack_kg'])} kg bei 210 (erwartet etwa 470): {ok(abs(lg[210]['A']['m_pack_kg']-470)<15)}; NMC {n0(na['mitte']['m_pack_kg'])} kg (erwartet etwa 410, Prüfband 370–450): {ok(370<=na['mitte']['m_pack_kg']<=450)}. NMC leichter als LFP auch bei 210 ({n0(lg[210]['A']['m_pack_kg'])} gegen {n0(na['mitte']['m_pack_kg'])} kg): {ok(lg[210]['A']['m_pack_kg']>na['mitte']['m_pack_kg'])}.\n")
md.append(f"4. Anteil Fall A: LFP {pct(lg[160]['A']['batterieanteil'])} bei 160 (erwartet etwa 40 %, über 30 %): {ok(lg[160]['A']['batterieanteil']>0.30 and 0.38<=lg[160]['A']['batterieanteil']<=0.42)}; NMC {pct(na['mitte']['batterieanteil'])} (erwartet etwa 27 %, unter 30 %): {ok(na['anteil_unter_grenze'] and 0.26<=na['mitte']['batterieanteil']<=0.28)}.\n")
bl = lambda f: F("LFP", f)["bauraum"][0]
md.append(f"5. Bauraum: LFP A nötig {n1(la['pack_Wh_L_noetig'])} gegen {n1(bl('A')['verfuegbar_Wh_L'])} Wh/L verfügbar, Urteil „{bl('A')['urteil']}“ (erwartet knapp nicht erfüllt oder gerade erfüllt): {ok('knapp' in bl('A')['urteil'])}. LFP B {n1(lb['pack_Wh_L_noetig'])} gegen {n1(bl('B')['verfuegbar_Wh_L'])}, „{bl('B')['urteil']}“ (erwartet nicht erfüllt): {ok(bl('B')['urteil']=='nicht erfüllt')}. NMC verfügbar {n1(na['bauraum'][0]['verfuegbar_Wh_L'])}–{n1(na['bauraum'][1]['verfuegbar_Wh_L'])} Wh/L (erwartet 257–386), A „{na['bauraum_urteil']}“, B „{nb['bauraum_urteil']}“ (erwartet erfüllt): {ok(na['bauraum_urteil']=='erfüllt' and nb['bauraum_urteil']=='erfüllt')}.\n")
md.append(f"6. Zyklen: LFP {C['LFP']['zyklen_urteil']} (erwartet erfüllt): {ok(C['LFP']['zyklen_urteil']=='erfüllt')}; NMC {C['NMC']['zyklen_urteil']} (erwartet unsicher): {ok(C['NMC']['zyklen_urteil']=='unsicher')}.\n")
md.append("7. Deutung vorab: kein Rechenergebnis, nicht abgeglichen (Opus).\n\n**Verfehlte-Erwartung-Kriterien:** LFP-Packmasse A 560–670 kg: "
          f"{ok(560<=lg[160]['A']['m_pack_kg']<=670)}; NMC 370–450 kg: {ok(370<=na['mitte']['m_pack_kg']<=450)}; NMC-Parallelzahl A = 4: {ok(na['mitte']['p']==4)}; Fall B konvergiert (LFP {lb['schritte']}, NMC {nb['schritte']} Schritte): erfüllt.\n")
# ---- Lauf 3 (Bauraum 1,95 x 1,43 x 0,13 m): Vergleich mit gesichertem Lauf 2, Zahlen nur aus den beiden ergebnis*.json (Hauptwert = Grundlage von bauraum.png: LFP 160 Wh/kg, NMC fest) ----
_l2f = os.path.join(D, "ergebnis_lauf2.json")
if os.path.exists(_l2f):
    d2 = json.load(open(_l2f, encoding="utf-8")); C2 = d2["varianten"]
    def _h(CC, c, f): x = CC[c]["faelle"][f]; return x.get("hauptwert", x)
    def _b(CC, c, f): h = _h(CC, c, f); return (h.get("bauraum") or CC[c]["faelle"][f]["bauraum"])[0]
    def _n(CC, c, f): h = _h(CC, c, f); return h.get("pack_Wh_L_noetig", CC[c]["faelle"][f]["pack_Wh_L_noetig"])
    md.append(f"\n## Lauf 3 (Bauraum 1,95 × 1,43 × 0,13 m, ENT-030)\nKI-generiert (Claude Sonnet, 2026-11-17), Entwurf. Volumen {n1(d['bauraum_Liter'])} L (Lauf 2: {n1(d2['bauraum_Liter'])} L, `ergebnis_lauf2.json`). Grundlage wie `bauraum.png`: Hauptwert (LFP 160 Wh/kg, k 0,75). Massen und Energien sind unverändert (Bauraum geht nicht ein): LFP A {n1(_h(C,'LFP','A')['m_pack_kg'])} kg (Lauf 2 {n1(_h(C2,'LFP','A')['m_pack_kg'])}), NMC A {n1(na['mitte']['m_pack_kg'])} kg (Lauf 2 {n1(C2['NMC']['faelle']['A']['mitte']['m_pack_kg'])}).\n\n| Größe | Lauf 2 | Lauf 3 |\n|---|---|---|\n")
    for c, f in (("LFP", "A"), ("LFP", "B"), ("NMC", "A"), ("NMC", "B")):
        md.append(f"| {c} {f}: nötig / verfügbar [Wh/L], Abweichung, Urteil | {n1(_n(C2,c,f))} / {n1(_b(C2,c,f)['verfuegbar_Wh_L'])}, {_b(C2,c,f)['abweichung']*100:+.1f} %, {_b(C2,c,f)['urteil']} | {n1(_n(C,c,f))} / {n1(_b(C,c,f)['verfuegbar_Wh_L'])}, {_b(C,c,f)['abweichung']*100:+.1f} %, {_b(C,c,f)['urteil']} |\n")
    md.append(f"\nAbgleich mit dem Nachtrag in `ERWARTUNG.md` (Lauf 3: nötig Fall A ≈ 204 und LFP B ≈ 257 Wh/L, LFP A erfüllt +4,6 %, LFP B nicht, NMC erfüllt, Massen unverändert):\n"
              f"- nötig Fall A {n1(_n(C,'LFP','A'))} Wh/L (erwartet ≈ 204): {ok(abs(_n(C,'LFP','A')-204)<=1)}\n"
              f"- LFP A {_b(C,'LFP','A')['urteil']}, {_b(C,'LFP','A')['abweichung']*100:+.1f} % (erwartet erfüllt, +4,6 %; Rundung der Erwartung): {ok(_b(C,'LFP','A')['urteil']=='erfüllt' and abs(_b(C,'LFP','A')['abweichung']*100-4.6)<=0.3)}\n"
              f"- LFP B {_b(C,'LFP','B')['urteil']} (erwartet nicht erfüllt): {ok(_b(C,'LFP','B')['urteil']=='nicht erfüllt')}; nötig {n1(_n(C,'LFP','B'))} Wh/L (erwartet ≈ 257): {ok(abs(_n(C,'LFP','B')-257)<=1)}\n"
              f"- NMC A {na['bauraum_urteil']}, NMC B {nb['bauraum_urteil']} (erwartet erfüllt): {ok(na['bauraum_urteil']=='erfüllt' and nb['bauraum_urteil']=='erfüllt')}\n"
              f"- Massen unverändert (Hauptwert LFP A, NMC A): {ok(abs(_h(C,'LFP','A')['m_pack_kg']-_h(C2,'LFP','A')['m_pack_kg'])<1e-6 and abs(na['mitte']['m_pack_kg']-C2['NMC']['faelle']['A']['mitte']['m_pack_kg'])<1e-6)}\n"
              "Verfehlt-Kriterium des Nachtrags (Masse ändert sich oder LFP A nicht erfüllt): nicht eingetreten, wenn alle Punkte oben „erfüllt“ sind.\n")
md.append("\n---\n*KI-generiert (Claude Sonnet), Entwurf, nicht vom Menschen freigegeben.*\n")
open(os.path.join(D, "ERGEBNIS.md"), "w", encoding="utf-8").write("".join(md))
kurz = f"""KI-generiert (Claude Sonnet, 2026-11-16). Quelle: sim/chemie/varianten_lfp_nmc/ergebnis.json
Energie A brutto {n1(la['mitte']['E_brutto_kWh'])} kWh; B brutto LFP {n1(lg[160]['B']['E_brutto_kWh'])} (160 Wh/kg) / NMC {n1(nb['mitte']['E_brutto_kWh'])}
LFP: 250s×1p, {n1(lg[160]['A']['ah_noetig'])} Ah (A, 160). Packmasse A: 160 {n0(lg[160]['A']['m_pack_kg'])}, 185 {n0(lg[185]['A']['m_pack_kg'])}, 210 {n0(lg[210]['A']['m_pack_kg'])} kg; B (160) {n0(lg[160]['B']['m_pack_kg'])} kg
NMC 4680: 217s×{na['mitte']['p']}p = {na['mitte']['zellen']} Zellen (A), E_ist {n1(na['mitte']['E_ist_kWh'])} kWh, {n0(na['mitte']['m_pack_kg'])} kg; B {nb['mitte']['p']}p = {nb['mitte']['zellen']} Zellen, {n0(nb['mitte']['m_pack_kg'])} kg
Anteil A: LFP160 {pct(lg[160]['A']['batterieanteil'])}, LFP185 {pct(lg[185]['A']['batterieanteil'])}, NMC {pct(na['mitte']['batterieanteil'])} (Grenze 30 %); B: LFP160 {pct(lg[160]['B']['batterieanteil'])}, NMC {pct(nb['mitte']['batterieanteil'])}
Bauraum: LFP A {bl('A')['urteil']} ({n1(la['pack_Wh_L_noetig'])} nötig / {n1(bl('A')['verfuegbar_Wh_L'])}), LFP B {bl('B')['urteil']}; NMC A {na['bauraum_urteil']}, B {nb['bauraum_urteil']}
Zyklen: Bedarf {n0(d['zyklenbedarf'])}; LFP {C['LFP']['zyklen_urteil']}, NMC {C['NMC']['zyklen_urteil']}
Schritte Fall B: LFP {lb['schritte']}, NMC {nb['schritte']}; stärkste Annahme: LFP A {la['staerkste_annahme']}, NMC A {na['staerkste_annahme']}
Abgleich ERWARTUNG: siehe ERGEBNIS.md; Verfehlungen: NMC-Bedarf Fall B {n1(nb['mitte']['E_brutto_kWh'])} kWh liegt über Erwartung 84–86 (Pkt 1), sonst Pkt 1–6 wie erwartet
"""
open(os.path.join(D, "ERGEBNIS_kurz.txt"), "w", encoding="utf-8").write(kurz)
bs = os.path.join(ROOT, "praesentation", "bausteine"); os.makedirs(bs, exist_ok=True)
_alt = os.path.join(bs, "C0b.md"); _kern = "**Kernaussage:** (Opus)"
if os.path.exists(_alt):  # vorhandene Kernaussage erhalten (nicht auf "(Opus)" zurücksetzen)
    for _z in open(_alt, encoding="utf-8").read().splitlines():
        if _z.startswith("**Kernaussage") and "(Opus)" not in _z[-8:]: _kern = _z
open(_alt, "w", encoding="utf-8").write(f"""> **KI-generiert** (Claude Sonnet, 2026-11-16), Entwurf. Folienbaustein Vorgang C0b.

# Variantenvergleich LFP-Blade gegen NMC-4680 (Messwerte)
{_kern}

**Bild:** sim/chemie/varianten_lfp_nmc/packmasse.png (Zielband: Grenze 30 % der Gesamtmasse, Annahme)

**Zahlen** (Quelle sim/chemie/varianten_lfp_nmc/ergebnis.json):
- Packmasse Fall A: LFP {n0(lg[160]['A']['m_pack_kg'])} kg (160 Wh/kg) bis {n0(lg[210]['A']['m_pack_kg'])} kg (210), NMC 4680 {n0(na['mitte']['m_pack_kg'])} kg
- Batterieanteil Fall A: LFP {pct(lg[160]['A']['batterieanteil'])} (160), NMC {pct(na['mitte']['batterieanteil'])}
- Zellen: LFP 250s×1p, NMC 217s×{na['mitte']['p']}p = {na['mitte']['zellen']} Zellen (A)
- Bauraum Fall A ({n1(d['bauraum_Liter'])} L): LFP {bl('A')['urteil']} ({n1(la['pack_Wh_L_noetig'])} Wh/L nötig, {n1(bl('A')['verfuegbar_Wh_L'])} verfügbar), NMC {na['bauraum_urteil']}

*KI-generiert, Entwurf.*
""")
