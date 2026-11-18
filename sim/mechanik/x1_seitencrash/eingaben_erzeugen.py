#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-18), Entwurf. Auftrag X1. Schreibt eingaben.json aus ERWARTUNG.md (ERW-X1) und cad/pack/entwurf/parameter_<V>.json (nur lesen)."""
import json, math
from pathlib import Path
R = Path(__file__).resolve().parents[3]
def a(w, h): return {"wert": w, "herkunft": h}
out = {"hinweis": "KI-generiert, Entwurf. Jeder Wert mit Herkunft.",
 "werkstoff": {"E_MPa": a(70000, "ERW-X1 Annahme Opus (EN AW-6082 T6)"), "nu": a(0.33, "ERW-X1 Annahme Opus"), "Rp02_MPa": a(260, "ERW-X1 Annahme Opus"), "Rm_MPa": a(310, "ERW-X1 Annahme Opus"), "Bruchdehnung": a(0.10, "ERW-X1 Annahme Opus"),
   "bilinear_hinweis": "Modellierung: Fliessgrenze 260 bei PEEQ 0, 310 bei PEEQ 0.10 (Gerade Rp0,2 -> Rm bei Bruchdehnung; Umsetzung von 'bilinear' aus ERW-X1)"},
 "pfahl": {"durchmesser_mm": a(254, "ERW-X1 Annahme Opus"), "starr": a(True, "ERW-X1; umgesetzt als Hex-Platte mit E = 100 x E_Stahl (2.1e7 MPa), Verschiebung vorgegeben"), "richtung": a("quer (+y), Achse senkrecht (z)", "ERW-X1 Annahme Opus (90 Grad)")},
 "last_restkraft_kN": a(100, "ERW-X1 Annahme Opus (Linie im Bild)"),
 "lastfaelle": {"LF1": "Pfahlmitte x = Mitte zwischen Querträger 1 und 2", "LF2": "Pfahlmitte x = Mitte Querträger 2"},
 "frei_weg": {}, "varianten": {}}
for v in ("LFP", "NMC"):
    J = json.load(open(R / f"cad/pack/entwurf/parameter_{v}.json")); A = {k: x["wert"] for k, x in J["A"].items()}; P = J["parameter"]
    L = float(P["BT-000"]["bauraum_laenge_mm"]["wert"]); B = float(P["BT-000"]["bauraum_breite_mm"]["wert"])
    rand, nq = A["A_rand_mm"], int(A["A_quertraeger_anzahl"]); qb, qh, qw, sp = A["A_quertraeger_breite_mm"], A["A_quertraeger_hoehe_mm"], A["A_quertraeger_wand_mm"], A["A_quertraeger_spiel_mm"]
    pad, kp, bod, ufs, luft = A["A_pad_mm"], A["A_kuehlplatte_mm"], A["A_boden_mm"], A["A_unterfahrschutz_mm"], A["A_luft_mm"]
    z_ku = ufs + luft + bod; z_cell0 = z_ku + kp + pad
    if v == "LFP":
        Dc = float(P["BT-100"]["dicke_mm"]["wert"]); Hc = float(P["BT-100"]["breite_mm"]["wert"]); n = int(A["A_zellzahl_LFP"]); ab = A["A_zellabstand_LFP_mm"]
        nz = n // 2; pitch = Dc + ab; Lg_calc = nz * Dc + (nz - 1) * ab + nq * (qb + 2 * sp) + 2 * rand
        x = rand + (L - Lg_calc) / 2; grp = [nz // (nq + 1) + (1 if i < nz % (nq + 1) else 0) for i in range(nq + 1)]; pos = []
        for gi, g in enumerate(grp):
            x += g * pitch - ab + sp
            if gi < nq: pos.append(x); x += qb + sp
        extra = 0.0; frei = {"Zellverbinder_mm": 1.0, "Zellkoerper_mm": 4.0, "herkunft": "pack.py: Zellverbinder bei y = rand+1, Zellen ab y = rand+4; ERW-X1 nennt 30 + 1 mm"}
    else:
        d = float(P["BT-100"]["durchmesser_mm"]["wert"]); Hc = float(P["BT-100"]["hoehe_mm"]["wert"]); ab = A["A_zellabstand_NMC_mm"]
        feld = (L - 2 * rand - nq * qb - nq * 2 * sp) / (nq + 1); pos = []; x = rand
        for f in range(nq + 1):
            x += feld + sp
            if f < nq: pos.append(x); x += qb + sp
        extra = A["A_zellabgriff_NMC_mm"][1] + A["A_gruppenverbinder_NMC_mm"][1]
        t = d + ab; frei = {"gerade_Reihen_mm": 0.0, "ungerade_Reihen_mm": round(t / 2, 3), "herkunft": "pack.py: Hexagonalraster, gerade Reihen beginnen bei y = rand (Zelle berührt Rahmeninnenseite), ungerade bei rand + t/2. ERW-X1 '41,6 mm' = Reihenabstand in x (t*sqrt(3)/2), nicht ein Weg in y -> Opus fragen"}
    zdk = z_cell0 + Hc + extra + pad + kp; h = zdk - z_ku
    out["varianten"][v] = {"L_mm": L, "B_mm": B, "rahmen_breite_mm": rand, "rahmen_hoehe_mm": h, "rahmen_wand_mm": A["A_seitenrahmen_wand_mm"], "rahmen_kammern": int(A["A_seitenrahmen_kammern"]),
        "quertraeger_x0_mm": pos, "quertraeger_breite_mm": qb, "quertraeger_hoehe_mm": qh, "quertraeger_wand_mm": qw, "quertraeger_spiel_mm": sp, "quertraeger_zmitte_ueber_rahmenunterkante_mm": z_cell0 + Hc / 2 - z_ku,
        "boden_dicke_mm": bod, "herkunft": f"cad/pack/entwurf/parameter_{v}.json (BT-000 Länge/Breite, Block A), Formeln aus cad/pack/pack.py (nur gelesen)"}
    out["frei_weg"][v] = frei
out["modell_ausschnitt"] = {"quertraeger_laenge_mm": a(300, "ERW-X1 'Querträger auf 300 mm Länge angeschlossen'"), "boden_streifen": "Boden (3 mm) als Streifen y = Rahmeninnenseite bis 300 mm, x volle Länge (Auslegung aus ERW-X1 'Bodenwanne als Streifen', Streifenbreite 300 = Querträgerlänge: Modellierungsdetail, Opus bestätigen)",
   "festhaltung": "Gegenseite fest (ERW-X1): Querträgerenden und Bodenstreifenrand bei y = 300 sowie Rahmenenden x = 0 und x = L voll eingespannt (Modelldetail, Opus bestätigen)",
   "kontakt": "reibungsfrei, Penalty linear (Zahlenwert numerisch, kein Material)"}
json.dump(out, open(Path(__file__).parent / "eingaben.json", "w"), indent=1, ensure_ascii=False)
for v in out["varianten"]: print(v, out["varianten"][v]["rahmen_hoehe_mm"], out["varianten"][v]["quertraeger_x0_mm"], out["varianten"][v]["quertraeger_zmitte_ueber_rahmenunterkante_mm"])
