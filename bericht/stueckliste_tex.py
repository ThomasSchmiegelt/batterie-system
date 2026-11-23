#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-23). Entwurf.
Erzeugt bericht/stueckliste_<V>.tex (longtable) aus pm/bauteile/stueckliste_<V>.json
und pm/kosten/ergebnis_<V>.json. Summenabgleich gegen summen.* und summe_eur_pack (Grenze 0,1 %)."""
import json, sys, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def de(x, n):
    s = f"{x:,.{n}f}".replace(",", "X").replace(".", ",").replace("X", "\\,")
    return s
def tex(s):
    for a, b in [("\\", "/"), ("&", "\\&"), ("%", "\\%"), ("_", "\\_\\allowbreak{}"), ("#", "\\#"), ("$", "\\$"), ("{", "\\{"), ("}", "\\}"), ("/", "/\\allowbreak{}")]:
        s = s.replace(a, b)
    return s
def num(x): return x if isinstance(x, (int, float)) else None
fehler = []
for v in ["LFP", "NMC"]:
    S = json.load(open(f"{R}/pm/bauteile/stueckliste_{v}.json"))
    K = json.load(open(f"{R}/pm/kosten/ergebnis_{v}.json"))
    kp = {p["pos"]: p for p in K["positionen"]}
    gr = {}
    for p in S["positionen"]:
        gr.setdefault(p["baugruppe"], []).append(p)
    L = [r"{\small\setlength{\tabcolsep}{2.5pt}",
         r"\begin{longtable}{@{}l l p{4.2cm} p{2.3cm} r r r r p{1.5cm}@{}}",
         r"\toprule Pos. & BT & Benennung & Werkstoff & Menge & kg/St. & kg ges. & EUR ges. & Quelle\\\midrule\endfirsthead",
         r"\toprule Pos. & BT & Benennung & Werkstoff & Menge & kg/St. & kg ges. & EUR ges. & Quelle\\\midrule\endhead",
         r"\bottomrule\endlastfoot"]
    gm = ge = 0.0; n = 0
    for bg in sorted(gr):
        sm = se = 0.0; names = {p.get("bt_name") for p in gr[bg]}
        L.append(rf"\multicolumn{{9}}{{@{{}}l}}{{\textbf{{{tex(bg)} {tex(gr[bg][0].get('bt_name') or '')}}}}}\\")
        for p in gr[bg]:
            n += 1
            m = num(p.get("masse_ges_kg")); mj = num(p.get("masse_je_kg"))
            e = num(kp[p["pos"]].get("eur_ges"))
            if m: sm += m
            if e: se += e
            q = "CAD" if (p.get("geometrie") or {}).get("detailstufe") in ("F", "K") or "cad/" in (p.get("quelle") or "") else "Annahme"
            if p.get("art") == "K" and "Akte" in (p.get("masse_quelle") or ""): q = "Akte"
            L.append(" & ".join([tex(p["pos"]), tex(p["bt"]), tex(p["benennung"]), tex(p.get("werkstoff") or ""),
                str(p.get("menge_" + v, "")), de(mj, 3) if mj is not None else "offen",
                de(m, 2) if m is not None else "offen", de(e, 0) if e is not None else "offen", q]) + r"\\")
        L.append(rf"\multicolumn{{6}}{{@{{}}r}}{{\emph{{Zwischensumme {tex(bg)}}}}} & {de(sm,2)} & {de(se,0)} & \\\midrule")
        gm += sm; ge += se
    fert = K["fertigung"]["eur_pack"]
    L.append(rf"\multicolumn{{6}}{{@{{}}r}}{{Fertigung (Annahme, 10\,\% der Nicht-Zell-Summe plus 50 EUR)}} & & {de(fert,0)} & \\")
    L.append(rf"\multicolumn{{6}}{{@{{}}r}}{{\textbf{{Summe {v}}}}} & \textbf{{{de(gm,2)}}} & \textbf{{{de(ge+fert,0)}}} & \\")
    L.append(r"\end{longtable}}")
    L.append(rf"\tquelle{{\path{{pm/bauteile/stueckliste_{v}.json}}, \path{{pm/kosten/ergebnis_{v}.json}}. Positionen mit „offen“ haben keine Masse bzw. keinen Preis und fehlen in den Summen (Untergrenze). Alle Preise sind Annahmen.}}")
    open(f"{R}/bericht/stueckliste_{v}.tex", "w").write("\n".join(L) + "\n")
    dm = abs(gm / S["summen"]["masse_stueckliste_kg"] - 1) * 100
    de_ = abs((ge + fert) / K["summe_eur_pack"] - 1) * 100
    print(f"{v}: {n} Pos., Masse {gm:.3f} vs {S['summen']['masse_stueckliste_kg']} ({dm:.4f} %), EUR {ge+fert:.1f} vs {K['summe_eur_pack']:.1f} ({de_:.4f} %)")
    if dm > 0.1 or de_ > 0.1: fehler.append(v)
if fehler: print("ABWEICHUNG > 0,1 % :", fehler); sys.exit(1)
