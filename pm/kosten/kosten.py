"""kosten.py -- Kostenrechnung je Baugruppe aus Stückliste und Eingaben (Auftrag KO1, REQ-P16).

KI-generiert (Claude Sonnet, 2026-11-18), Entwurf.
    python3 pm/kosten/kosten.py [--variante LFP|NMC]    (ohne Angabe: beide)
Eingaben: pm/bauteile/stueckliste_<V>.json, pm/kosten/eingaben.json (Preise: ERW-KO1, Annahmen Opus)
Ausgabe:  pm/kosten/ergebnis_<V>.json
Basis je Einheit: €/kg x masse_ges_kg, €/Stück x menge, €/kWh x Energie, €/Satz x 1; €/m: Länge aus ergebnis_<V>_e2.json (Nachtrag 1); €/L: Volumen offen bis K2.
Positionen ohne Masse/Menge/Preis werden als "offen" gezählt und nie als 0. Preis 0 (Fahrzeug) ist ein Preis.
Fertigung: Anteil auf die Nicht-Zell-Summe (Nachtrag 1) + Endprüfung je Pack. Keine Preise im Skript.
"""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
EIN = json.loads((ROOT / "pm/kosten/eingaben.json").read_text())
P = EIN["eur_je"]
vs = [sys.argv[sys.argv.index("--variante") + 1]] if "--variante" in sys.argv else ["LFP", "NMC"]
num = lambda x: isinstance(x, (int, float)) and not isinstance(x, bool)

def preis(bt, V):
    w = P.get(bt, {}).get("wert")
    return w.get(V) if isinstance(w, dict) else w

import math
def laenge_m(bt, V):
    """Länge in m aus cad/pack/entwurf/ergebnis_<V>_e2.json (Methode: eingaben.json laengen_aus_cad)."""
    _d = ROOT / f"cad/pack/entwurf/ergebnis_{V}_e2d.json"
    c = json.loads((_d if _d.exists() else ROOT / f"cad/pack/entwurf/ergebnis_{V}_e2.json").read_text())
    if bt == "BT-360": return c["gruppen"]["E2_FPC"]["masse_kg"] / c["annahmen"]["A_e2_fpc_masse_kg_m"]["wert"]
    if bt == "BT-430" and "hv_laenge_gesamt_m" in c.get("e2", {}): return c["e2"]["hv_laenge_gesamt_m"]   # direkt aus e2/e2d (Auftrag BERICHT_03 Vorher)
    if bt == "BT-430":
        d = c["annahmen"][f"A_e2_hv_aussendurchmesser_{V}_mm"]["wert"]
        return c["gruppen"]["E2_HV_Leitung"]["volumen_cm3"] * 1000 / (math.pi / 4 * d * d) / 1000
    return None

def bewerte(bt, V, menge, masse, kwh):
    """-> (eur, grund_offen). Basis aus Einheit."""
    p = P.get(bt)
    if p is None: return None, "kein Eintrag in eingaben.json"
    w = preis(bt, V); u = p["einheit"]
    if not num(w): return None, "kein Preis"
    if w == 0: return 0.0, None
    if u == "€/kWh": return w * kwh, None
    if u == "€/kg": return (w * masse * p.get("massefaktor", 1.0), None) if num(masse) else (None, "Masse offen")
    if u == "€/Stück": return (w * menge, None) if num(menge) else (None, "Menge offen")
    if u == "€/Satz": return (w * 1, None) if num(menge) else (None, "Menge offen")
    if u == "€/m":
        L = laenge_m(bt, V)
        return (w * L, None) if L is not None else (None, "Länge nicht in CAD-JSON")
    if u == "€/L": return None, "Volumen offen bis K2"
    return None, "Einheit unbekannt"

def lauf(V, zellfaktor=1.0):
    S = json.loads((ROOT / f"pm/bauteile/stueckliste_{V}.json").read_text()); kwh = S["summen"]["energie_kWh"]
    z = []
    for r in S["positionen"]:
        bt = r["bt"]
        if bt == "BT-720" and V == "LFP":
            z.append(dict(pos=r["pos"], bt=bt, baugruppe=r["baugruppe"], eur_ges=0.0, status="ersetzt durch BT-721/722 (LFP)", benennung=r["benennung"])); continue
        e, g = bewerte(bt, V, r.get("menge_" + V), r.get("masse_ges_kg"), kwh)
        if e is not None and bt == "BT-100": e *= zellfaktor
        z.append(dict(pos=r["pos"], bt=bt, baugruppe=r["baugruppe"], benennung=r["benennung"], menge=r.get("menge_" + V), masse_ges_kg=r.get("masse_ges_kg"),
                      eur_je=preis(bt, V), einheit=P.get(bt, {}).get("einheit"), eur_ges=e, status="bepreist" if e is not None else "offen", grund_offen=g, herkunft=P.get(bt, {}).get("herkunft"), preis_status=P.get(bt, {}).get("status")))
    zo = EIN["fehlende_bt_zuordnung"]
    for f in S["fehlende_bt"]:
        m = zo.get(f["gruppe"])
        if m is None:
            z.append(dict(pos="(fehlt)", bt=None, baugruppe=None, benennung=f["benennung"], eur_ges=None, status="offen", grund_offen="kein BT, kein Preis (nicht im CAD)")); continue
        menge, masse = f.get("anzahl"), f.get("masse_kg")
        e, g = bewerte(m["bt"], V, menge, masse, kwh)
        z.append(dict(pos="(fehlende_bt)", bt=m["bt"], baugruppe=m["baugruppe"], benennung=f["benennung"], menge=menge, masse_ges_kg=masse, eur_je=preis(m["bt"], V), einheit=P[m["bt"]]["einheit"],
                      eur_ges=e, status="bepreist" if e is not None else "offen", grund_offen=g, herkunft=P[m["bt"]]["herkunft"] + "; Menge/Masse: stueckliste_%s.json fehlende_bt" % V, preis_status=P[m["bt"]].get("status")))
    return S, kwh, z

def summe(z, kwh):
    bg = {}
    for r in z:
        b = bg.setdefault(r["baugruppe"] or "ohne", dict(eur_pack=0.0, positionen=0, positionen_offen=0, offen_liste=[]))
        b["positionen"] += 1
        if r["eur_ges"] is None: b["positionen_offen"] += 1; b["offen_liste"].append(f'{r["bt"] or r["benennung"]} ({r.get("grund_offen")})')
        else: b["eur_pack"] += r["eur_ges"]
    mat = sum(b["eur_pack"] for b in bg.values())
    fe = EIN["fertigung"]; zell = sum(r["eur_ges"] for r in z if r["bt"] == "BT-100" and r["eur_ges"] is not None); fert = fe["anteil_auf_summe"] * (mat - zell) + fe["endpruefung_eur_pack"]
    return bg, mat, fert, mat + fert

for V in vs:
    S, kwh, z = lauf(V)
    bg, mat, fert, tot = summe(z, kwh)
    n_offen = sum(b["positionen_offen"] for b in bg.values())
    zell = sum(r["eur_ges"] for r in z if r["bt"] == "BT-100" and r["eur_ges"] is not None)
    for b in bg.values(): b["anteil_an_teilsumme_pct"] = 100 * b["eur_pack"] / tot; b["eur_je_kWh"] = b["eur_pack"] / kwh
    fert_b = dict(eur_pack=fert, anteil_an_teilsumme_pct=100 * fert / tot, eur_je_kWh=fert / kwh)
    # Empfindlichkeit Zellpreis +-20 %
    emp = {}
    for f in (0.8, 1.2):
        _, k2, z2 = lauf(V, f); _, _, _, t2 = summe(z2, k2)
        emp[f"zellpreis_x{f}"] = dict(summe_eur_pack=t2, aenderung_pct=100 * (t2 - tot) / tot)
    # Prüfungen gegen ERW-KO1
    nz = [r for r in z if r["bt"] != "BT-100" and r["eur_ges"] is not None]
    gross = sorted(((r["eur_ges"] / tot * 100, r["bt"], r["pos"]) for r in nz), reverse=True)[:5]
    zb = EIN["zielband"]
    pr = dict(zellanteil_pct=100 * zell / tot, zellanteil_im_band=zb["zellanteil_pct"][0] <= 100 * zell / tot <= zb["zellanteil_pct"][1],
              zellanteil_verfehlt_schwelle=(100 * zell / tot < 60 or 100 * zell / tot > 85),
              groesste_nichtzellpositionen_pct=[dict(pct=round(p, 2), bt=b, pos=ps) for p, b, ps in gross],
              nichtzellposition_ueber_10pct=any(p > 10 for p, _, _ in gross),
              summe_im_band=zb[V]["pack_eur"][0] <= tot <= zb[V]["pack_eur"][1], eur_kwh_im_band=zb[V]["eur_kwh"][0] <= tot / kwh <= zb[V]["eur_kwh"][1],
              abstand_beleg_eur_kwh=tot / kwh - EIN["beleg_packpreis"]["eur_je_kWh_berechnet"], beleg_eur_kwh=EIN["beleg_packpreis"]["eur_je_kWh_berechnet"])
    # Anteil der Summe, der auf Schätzungen beruht (Preis-Status je Position; Fertigung = Schätzung). Verifiziert ist nur der Packpreis-Beleg W29, er ist keine Position.
    ver = sum(r["eur_ges"] for r in z if r["eur_ges"] is not None and r.get("preis_status", "").startswith("verifiziert"))
    sch = tot - ver
    out = dict(status_werte=EIN["status_werte"], anteil_schaetzung_an_summe_pct=100 * sch / tot, anteil_verifiziert_an_summe_pct=100 * ver / tot, beleg_packpreis=EIN["beleg_packpreis"], hinweis="KI-generiert (Claude Sonnet), Entwurf. Preise nur aus eingaben.json (ERW-KO1 Annahmen). Summe ist eine Teilsumme (untere Schranke), solange Positionen offen sind.",
               variante=V, energie_kWh=kwh, quelle_energie=f"pm/bauteile/stueckliste_{V}.json summen.energie_kWh",
               positionen_offen_gesamt=n_offen, summe_vollstaendig=n_offen == 0, material_kauf_summe_eur=mat, fertigung=fert_b,
               summe_eur_pack=tot, summe_eur_je_kWh=tot / kwh, zellkosten_eur=zell, je_baugruppe=bg, empfindlichkeit=emp, pruefung_erwartung=pr, positionen=z)
    (ROOT / f"pm/kosten/ergebnis_{V}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print(V, f"Teilsumme {tot:.0f} EUR  {tot/kwh:.1f} EUR/kWh  Zellanteil {100*zell/tot:.1f} %  offen {n_offen}")
