"""kosten.py -- Kostenrechnung je Baugruppe aus Stückliste (SL3.1) und Eingaben (Aufträge KO1, KO2, REQ-P16).

KI-generiert (Claude Sonnet, 2026-11-18, KO2 2026-11-19), Entwurf.
    python3 pm/kosten/kosten.py [--variante LFP|NMC]    (ohne Angabe: beide)
Eingaben: pm/bauteile/stueckliste_<V>.json (Positionen), pm/kosten/eingaben.json (Preise: ERW-KO1/KO2, Annahmen Opus), pm/kosten/preisregeln.py (Zuordnung)
Ausgabe:  pm/kosten/ergebnis_<V>.json
Basis je Einheit: €/kg x masse_ges_kg, €/Stück x Menge, €/Satz x 1, €/kWh x Energie, €/m x Länge (nur die Position, die die Länge liefert: eingaben.laengen_aus_cad.position), €/L offen bis Volumen vorliegt.
Positionen ohne Masse/Menge/Preis werden als "offen" gezählt und nie als 0. Entfallene Positionen (eingaben.entfaellt) zählen 0 und sind nicht offen. Preis 0 (Fahrzeug) ist ein Preis.
Fertigung: Anteil auf die Nicht-Zell-Summe (Nachtrag 1) + Endprüfung je Pack. Keine Preise im Skript.
Neu KO2: Status je Position in 3 Stufen (verifiziert / abgeleitet / Schätzung), Anteil je Stufe an der Summe, Prüfung gegen ERW-KO2 (+-8 %).
"""
import json, sys, math
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "pm/kosten"))
import preisregeln as PR
EIN = PR.EIN; P = EIN["eur_je"]; num = PR.num
vs = [sys.argv[sys.argv.index("--variante") + 1]] if "--variante" in sys.argv else ["LFP", "NMC"]


def wert(key, V):
    w = P.get(key, {}).get("wert")
    return w.get(V) if isinstance(w, dict) else w


def laenge_m(bt, V):
    """Länge in m aus cad/pack/entwurf/ergebnis_<V>_e2d.json (Methode: eingaben.laengen_aus_cad)."""
    _d = ROOT / f"cad/pack/entwurf/ergebnis_{V}_e2d.json"
    c = json.loads((_d if _d.exists() else ROOT / f"cad/pack/entwurf/ergebnis_{V}_e2.json").read_text())
    if bt == "BT-360": return c["gruppen"]["E2_FPC"]["masse_kg"] / c["annahmen"]["A_e2_fpc_masse_kg_m"]["wert"]
    if bt == "BT-430" and "hv_laenge_gesamt_m" in c.get("e2", {}): return c["e2"]["hv_laenge_gesamt_m"]
    if bt == "BT-430":
        d = c["annahmen"][f"A_e2_hv_aussendurchmesser_{V}_mm"]["wert"]
        return c["gruppen"]["E2_HV_Leitung"]["volumen_cm3"] * 1000 / (math.pi / 4 * d * d) / 1000
    return None


def bewerte(pos, bt, key, V, menge, masse, kwh):
    """-> (eur, grund_offen). Basis aus Einheit."""
    if bt in EIN["entfaellt"] and key == bt: return 0.0, None
    p = P.get(key)
    if p is None: return None, "kein Eintrag in eingaben.json"
    w = wert(key, V); u = p["einheit"]
    if not num(w): return None, "kein Preis"
    if w == 0: return 0.0, None
    if u == "€/kWh": return w * kwh, None
    if u == "€/kg": return (w * masse * p.get("massefaktor", 1.0), None) if num(masse) else (None, "Masse offen")
    if u == "€/Stück": return (w * menge, None) if num(menge) else (None, "Menge offen")
    if u == "€/Satz": return (w * 1, None) if num(menge) else (None, "Menge offen")
    if u == "€/m":
        if EIN["laengen_aus_cad"]["position"].get(bt) != pos: return None, "Detailposition ohne Preiszuordnung (Länge nur für " + str(EIN["laengen_aus_cad"]["position"].get(bt)) + ")"
        L = laenge_m(bt, V)
        return (w * L, None) if L is not None else (None, "Länge nicht in CAD-JSON")
    if u == "€/L": return None, "Volumen offen"
    return None, "Einheit unbekannt"


def lauf(V, zellfaktor=1.0):
    S = json.loads((ROOT / f"pm/bauteile/stueckliste_{V}.json").read_text()); kwh = S["summen"]["energie_kWh"]
    z = []
    for r in S["positionen"]:
        bt = r["bt"]; key = PR.schluessel(r["pos"], bt)
        e, g = bewerte(r["pos"], bt, key, V, r.get("menge_" + V), r.get("masse_ges_kg"), kwh)
        if e is not None and bt == "BT-100": e *= zellfaktor
        ent = bt in EIN["entfaellt"] and key == bt
        pj = PR.preis_je(r["pos"], bt, V)
        status = "entfällt" if ent else ("bepreist" if e is not None else "offen")
        z.append(dict(pos=r["pos"], bt=bt, preis_schluessel=key, baugruppe=r["baugruppe"], benennung=r["benennung"], menge=r.get("menge_" + V), masse_ges_kg=r.get("masse_ges_kg"), masse_quelle=r.get("masse_quelle"),
                      eur_je=pj["wert"], einheit=pj["einheit"], eur_ges=e, status=status, grund_offen=g, herkunft=pj["herkunft"], preis_status=pj["status"], preis_stufe=PR.stufe(pj["status"]), teile=pj.get("teile")))
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


def je_stufe(z, fert):
    """Euro je Stufe (verifiziert / abgeleitet / Schätzung). Preise mit teile werden nach Teilwert aufgeteilt. Fertigung = Schätzung."""
    s = {"verifiziert": 0.0, "abgeleitet": 0.0, "Schätzung": fert}
    for r in z:
        if r["eur_ges"] is None or r["eur_ges"] == 0: continue
        if r.get("teile"):
            tw = sum(t["wert"] for t in r["teile"])
            for t in r["teile"]: s[PR.stufe(t["status"])] += r["eur_ges"] * t["wert"] / tw
        else: s[PR.stufe(r["preis_stufe"]) if r["preis_stufe"] != "offen" else "Schätzung"] += r["eur_ges"]
    return s


for V in vs:
    S, kwh, z = lauf(V)
    bg, mat, fert, tot = summe(z, kwh)
    n_offen = sum(b["positionen_offen"] for b in bg.values())
    zell = sum(r["eur_ges"] for r in z if r["bt"] == "BT-100" and r["eur_ges"] is not None)
    for b in bg.values(): b["anteil_an_teilsumme_pct"] = 100 * b["eur_pack"] / tot; b["eur_je_kWh"] = b["eur_pack"] / kwh
    fert_b = dict(eur_pack=fert, anteil_an_teilsumme_pct=100 * fert / tot, eur_je_kWh=fert / kwh)
    emp = {}
    for f in (0.8, 1.2):
        _, k2, z2 = lauf(V, f); _, _, _, t2 = summe(z2, k2)
        emp[f"zellpreis_x{f}"] = dict(summe_eur_pack=t2, aenderung_pct=100 * (t2 - tot) / tot)
    nz = [r for r in z if r["bt"] != "BT-100" and r["eur_ges"] is not None]
    gross = sorted(((r["eur_ges"] / tot * 100, r["bt"], r["pos"]) for r in nz), reverse=True)[:5]
    zb = EIN["zielband"]
    pr = dict(zellanteil_pct=100 * zell / tot, zellanteil_im_band=zb["zellanteil_pct"][0] <= 100 * zell / tot <= zb["zellanteil_pct"][1],
              zellanteil_verfehlt_schwelle=(100 * zell / tot < 60 or 100 * zell / tot > 85),
              groesste_nichtzellpositionen_pct=[dict(pct=round(p, 2), bt=b, pos=ps) for p, b, ps in gross],
              nichtzellposition_ueber_10pct=any(p > 10 for p, _, _ in gross),
              summe_im_band=zb[V]["pack_eur"][0] <= tot <= zb[V]["pack_eur"][1], eur_kwh_im_band=zb[V]["eur_kwh"][0] <= tot / kwh <= zb[V]["eur_kwh"][1],
              abstand_beleg_eur_kwh=tot / kwh - EIN["beleg_packpreis"]["eur_je_kWh_berechnet"], beleg_eur_kwh=EIN["beleg_packpreis"]["eur_je_kWh_berechnet"])
    # KO2: Prüfung gegen ERW-KO2 (Nachtrag 2): +-8 %, Anteil verifiziert/abgeleitet < 1 %
    ek = EIN["erwartung_ko2"]; tol = ek["toleranz_pct"] / 100; st = je_stufe(z, fert)
    va = 100 * (st["verifiziert"] + st["abgeleitet"]) / tot
    ko2 = dict(erwartung_pack_eur=ek[V]["pack_eur"], erwartung_eur_kwh=ek[V]["eur_kwh"], toleranz_pct=ek["toleranz_pct"],
               band_pack_eur=[ek[V]["pack_eur"] * (1 - tol), ek[V]["pack_eur"] * (1 + tol)], band_eur_kwh=[ek[V]["eur_kwh"] * (1 - tol), ek[V]["eur_kwh"] * (1 + tol)],
               abweichung_pack_pct=100 * (tot / ek[V]["pack_eur"] - 1), abweichung_eur_kwh_pct=100 * ((tot / kwh) / ek[V]["eur_kwh"] - 1),
               summe_im_band=ek[V]["pack_eur"] * (1 - tol) <= tot <= ek[V]["pack_eur"] * (1 + tol),
               anteil_verifiziert_abgeleitet_pct=va, anteil_verifiziert_abgeleitet_unter_grenze=va < ek["anteil_verifiziert_abgeleitet_max_pct"],
               offene_ohne_grund=[r["pos"] for r in z if r["status"] == "offen" and not r.get("grund_offen")], herkunft=ek["herkunft"])
    out = dict(status_werte=EIN["status_werte"], eur_je_stufe=st, anteil_je_stufe_pct={k: 100 * v / tot for k, v in st.items()},
               anteil_schaetzung_an_summe_pct=100 * st["Schätzung"] / tot, anteil_verifiziert_an_summe_pct=100 * st["verifiziert"] / tot, anteil_abgeleitet_an_summe_pct=100 * st["abgeleitet"] / tot,
               beleg_packpreis=EIN["beleg_packpreis"], hinweis="KI-generiert (Claude Sonnet), Entwurf. Preise nur aus eingaben.json (ERW-KO1/KO2 Annahmen Opus). Summe ist eine Teilsumme (untere Schranke), solange Positionen offen sind.",
               variante=V, energie_kWh=kwh, quelle_energie=f"pm/bauteile/stueckliste_{V}.json summen.energie_kWh",
               positionen_offen_gesamt=n_offen, summe_vollstaendig=n_offen == 0, material_kauf_summe_eur=mat, fertigung=fert_b,
               summe_eur_pack=tot, summe_eur_je_kWh=tot / kwh, zellkosten_eur=zell, je_baugruppe=bg, empfindlichkeit=emp, pruefung_erwartung=pr, pruefung_ko2=ko2, positionen=z)
    (ROOT / f"pm/kosten/ergebnis_{V}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print(V, f"Teilsumme {tot:.0f} EUR  {tot/kwh:.1f} EUR/kWh  Zellanteil {100*zell/tot:.1f} %  offen {n_offen}  KO2-Band {'ja' if ko2['summe_im_band'] else 'NEIN'} ({ko2['abweichung_pack_pct']:+.1f} %)  verif/abgel. {va:.2f} %")
