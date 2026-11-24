#!/usr/bin/env python3
"""E3d grobe FMEDA der CMU-Platine. KI-generiert (Claude Sonnet, 2026-11-24), Entwurf.
Grundlage: ERWARTUNG.md (FIT, Ausfallartenanteile, Diagnosedeckungen = Annahmen Opus, Herkunft ERW-E3d).
Liest ../e3_platine/cmu_<V>_bom.csv (nur lesen). Schreibt fmeda_<V>.csv, ergebnis.json, e3d_fmeda.png.
Aufruf: source umgebung.sh; python3 fmeda.py"""
import csv, json, sys, pathlib
H = pathlib.Path(__file__).resolve().parent; BOM = H.parent / "e3_platine"
# ---- Annahmen aus ERWARTUNG.md (nichts hinzugefuegt) ----
FIT = {"Widerstand Chip": 0.3, "Kondensator MLCC": 0.5, "MOSFET klein": 1, "TVS-Diode": 1, "AFE-IC": 20, "Sekundaerschutz-IC": 5, "Uebertrager": 2, "Stecker": 2, "NTC-Eingang": 1}
ARTEN = {
 "Widerstand Chip": [("offen", .6), ("Kurzschluss", .1), ("Drift", .3)],
 "Kondensator MLCC": [("Kurzschluss", .4), ("offen", .3), ("Drift", .3)],
 "MOSFET klein": [("Kurzschluss D-S", .4), ("offen", .4), ("Drift", .2)],
 "TVS-Diode": [("Kurzschluss", .6), ("offen", .4)],
 "AFE-IC": [("Messfehler", .5), ("Ausfall Kommunikation", .3), ("Ausgleich haengt an", .2)],
 "Sekundaerschutz-IC": [("loest nicht aus", .5), ("loest falsch aus", .5)],
 "Uebertrager": [("offen", .7), ("Kurzschluss Wicklung", .3)],
 "Stecker": [("offen", .7), ("Kurzschluss benachbarter Pins", .3)],
 "NTC-Eingang": [("offen", .5), ("Kurzschluss", .5)]}
DC_MESS = 0.99    # AFE-Selbsttest und Plausibilisierung (Messfehler)
DC_LB = 0.99      # Leitungsbruch-Diagnose (FSR-02)
DC_AUSGL = 0.90   # Ausgleichsstrom-Ueberwachung ueber die Zellspannung
DC_SEK = 0.90     # Starttest des Sekundaerschutzes
KLASSE = {"R": "Widerstand Chip", "C": "Kondensator MLCC", "NMOS_generisch": "MOSFET klein", "Doppel_NMOS_generisch": "MOSFET klein", "OVP6_generisch": "Sekundaerschutz-IC", "TVS_generisch": "TVS-Diode",
          "AFE_generisch_18K": "AFE-IC", "Sekundaerschutz_generisch": "Sekundaerschutz-IC", "Uebertrager_generisch": "Uebertrager",
          "FPC_24": "Stecker", "Daisy_Stecker": "Stecker", "NTC_Eingang": "NTC-Eingang"}
NCMU = {"LFP": 14, "NMC": 13}   # Auftrag Opus; cad/pack/entwurf/ergebnis_<V>_e2d_e3.json anzahl_cmu
SICHER_KOM = "Kommunikationsverlust, BMS-Timeout fuehrt in den sicheren Zustand (Laden beendet)"

def rolle(ref, wert, fp, kl):
    if kl == "R": return "Ausgleichswiderstand" if "2512" in fp else "Filterwiderstand Zellabgriff"
    if kl == "C": return "Entkopplung AFE-VCC" if "Entkopplung" in wert else "Filterkondensator Zellabgriff"
    return {"NMOS_generisch": "Ausgleichs-FET", "Doppel_NMOS_generisch": "Ausgleichs-FET", "OVP6_generisch": "Sekundaerschutz", "TVS_generisch": "TVS Daisy-Chain", "AFE_generisch_18K": "AFE", "Sekundaerschutz_generisch": "Sekundaerschutz",
            "Uebertrager_generisch": "Uebertrager Daisy-Chain", "FPC_24": "Zellabgriff-Stecker J1", "Daisy_Stecker": "Daisy-Chain-Stecker", "NTC_Eingang": "NTC-Stecker"}[kl]

def einstufung(rl, art, massnahme=()):
    """(SG-01, SG-02) je als (Kategorie, DC, Begruendung). Kategorie: sicher | RF (SPF mit Restfehleranteil 1-DC) | MPF (latent 1-DC)."""
    S = lambda b: ("sicher", 0, b)
    nichtrel = "keine Wirkung auf die Zellspannungsgrenze"
    if rl == "Filterwiderstand Zellabgriff":
        dc = DC_LB if art == "offen" else DC_MESS; w = "Leitungsbruch" if art == "offen" else "Messfehler am Zellabgriff"
        return (("MPF", dc, f"{w}; AFE-Diagnose deckt, Rest faengt der unabhaengige Sekundaerschutz (FSR-01), latent"),
                ("RF", dc, f"{w}; kein zweiter Weg fuer Tiefentladung, Restfehler (1-DC)"))
    if rl == "Filterkondensator Zellabgriff":
        if art == "Kurzschluss": return (("MPF", DC_MESS, "Zellabgriff kurzgeschlossen = Messfehler; AFE-Plausibilisierung, Rest Sekundaerschutz, latent"), ("RF", DC_MESS, "Messfehler; Restfehler (1-DC)"))
        return (S("aendert nur die Filterwirkung (EMV), keine statische Messabweichung"),) * 2
    if rl == "Entkopplung AFE-VCC": return (S("VCC-Ausfall = AFE-Ausfall, " + SICHER_KOM),) * 2
    if rl == "Ausgleichswiderstand":
        if art == "Kurzschluss": return (S("Ausgleich entlaedt die Zelle, senkt die Spannung"), ("RF", DC_AUSGL, "doppelter Ausgleichsstrom bei aktivem Ausgleich; Ueberwachung ueber Zellspannung 90 %, Restfehler (konservative Einstufung)"))
        return (S("Ausgleich schwaecher oder aus, Zellspannungsmessung begrenzt Laden"), S("kein zusaetzlicher Ausgleichsstrom"))
    if rl == "Ausgleichs-FET":
        if art == "Kurzschluss D-S":
            sg2 = ("MPF", DC_AUSGL, "Massnahme M1: zweiter Schalter in Reihe, Einzelfehler entlaedt nicht mehr, latent") if "M1" in massnahmen_aktiv(massnahme) else ("RF", DC_AUSGL, "Ausgleich dauernd an, Zelle wird dauernd entladen; Ueberwachung 90 %, Restfehler (dominant, ERW 2)")
            if "M2" in massnahme: sg2 = (sg2[0], 0.99, sg2[2] + "; M2: Ueberwachung 99 % (Was-waere-wenn)")
            return (S("Entladen senkt die Zellspannung"), sg2)
        return (S("Ausgleich faellt aus oder Parameterdrift; Zellspannungsmessung begrenzt Laden"),) * 2 if art == "offen" else (S("Drift (Rdson, Leckstrom) ohne Dauerentladung angenommen"),) * 2
    if rl == "AFE":
        if art == "Messfehler": return (("MPF", DC_MESS, "AFE-Selbsttest 99 %, Rest deckt unabhaengiger Sekundaerschutz (ERW), latent"), ("RF", DC_MESS, "kein zweiter Weg fuer Tiefentladung, Restfehler (1-DC)"))
        if art == "Ausfall Kommunikation": return (S(SICHER_KOM),) * 2
        sg2 = ("RF", DC_AUSGL, "Ausgleich haengt an (ungefaehr eine Zelle dauernd entladen, ganzes IC-Anteil angesetzt); Ueberwachung 90 %, Restfehler")
        if "M2" in massnahme: sg2 = ("RF", 0.99, sg2[2] + "; M2: 99 % (Was-waere-wenn)")
        return (S("Ausgleich entlaedt, senkt die Zellspannung"), sg2)
    if rl == "Sekundaerschutz":
        if art == "loest nicht aus": return (("MPF", DC_SEK, "latenter Fehler, der Hauptweg (AFE) ist unabhaengig; Starttest 90 %, Rest latent"), S("Sekundaerschutz prueft nur Ueberspannung, fuer SG-02 ohne Funktion"))
        return (S("loest falsch aus = sicherer Zustand (Verfuegbarkeit, nicht SG-01)"), S("Sekundaerschutz ohne Funktion fuer SG-02"))
    if rl == "Zellabgriff-Stecker J1":
        dc = DC_LB if art == "offen" else DC_MESS
        return (("RF", dc, "gemeinsame Ursache: AFE und Sekundaerschutz liegen am selben Stecker, kein unabhaengiger Weg; AFE-Diagnose deckt, Restfehler (konservativ)"),
                ("RF", dc, "Leitungsbruch bzw. Messfehler; Restfehler (1-DC)"))
    if rl in ("TVS Daisy-Chain", "Uebertrager Daisy-Chain", "Daisy-Chain-Stecker"): return (S(SICHER_KOM + " (Isolation SG-07 nicht Umfang)"),) * 2
    if rl == "NTC-Stecker": return (S(nichtrel + " (betrifft SG-03)"),) * 2
    sys.exit(f"OFFEN: keine Einstufung fuer Rolle {rl} / {art}")
def massnahmen_aktiv(m): return set(m)

def rechne(v, massnahme=()):
    zeilen = []
    with open(BOM / f"cmu_{v}_bom.csv", encoding="utf-8") as f:
        rows = list(csv.DictReader(f, delimiter=";"))
    if any(z["Bauteilklasse"] == "Doppel_NMOS_generisch" for z in rows): massnahme = tuple(sorted(set(massnahme) | {"M1"}))   # v0.2: M1 (zwei Schalter in Reihe, Doppel-N-FET) ist Ist-Stand der Stückliste (ERW-E3 N7, ENT-192)
    if True:
        for z in rows:
            kl = z["Bauteilklasse"]
            if kl not in KLASSE: sys.exit(f"OFFEN: Bauteilklasse {kl} ({z['Ref']}) ohne Zeile in der Annahmentabelle")
            ak = KLASSE[kl]; rl = rolle(z["Ref"], z["Wert"], z["Footprint"], kl)
            for art, anteil in ARTEN[ak]:
                lam = FIT[ak] * anteil
                for sg, e in zip(("SG-01", "SG-02"), einstufung(rl, art, massnahme)):
                    kat, dc, beg = e
                    spf = lam * (1 - dc) if kat == "RF" else 0.0
                    mpf = lam * (1 - dc) if kat == "MPF" else 0.0
                    sr = lam if kat != "sicher" else 0.0
                    zeilen.append(dict(Ref=z["Ref"], Klasse=ak, Rolle=rl, FIT=FIT[ak], Ausfallart=art, Anteil=anteil, lambda_FIT=lam, SG=sg, Einstufung=kat, DC=dc if kat != "sicher" else "",
                                       lambda_SR=sr, lambda_RF=spf, lambda_MPF_latent=mpf, Begruendung=beg))
    return zeilen
def summe(zeilen, sg):
    z = [r for r in zeilen if r["SG"] == sg]
    sr = sum(r["lambda_SR"] for r in z); rf = sum(r["lambda_RF"] for r in z); ml = sum(r["lambda_MPF_latent"] for r in z)
    return dict(lambda_SR_FIT=sr, lambda_SPF_RF_FIT=rf, lambda_MPF_latent_FIT=ml, SPFM=1 - rf / sr, LFM=1 - ml / (sr - rf), PMHF_Beitrag_FIT=rf)

if __name__ == "__main__":
    ZIEL = {"SG-01": dict(ASIL="D", SPFM=.99, LFM=.90), "SG-02": dict(ASIL="C", SPFM=.97, LFM=.80)}
    erg = dict(erstellt="Claude Sonnet (KI), 2026-11-24", eingabe="sim/elektrik/e3_platine/cmu_<V>_bom.csv", ziel=ZIEL,
               annahmen=dict(FIT=FIT, DC_MESS=DC_MESS, DC_LB=DC_LB, DC_AUSGL=DC_AUSGL, DC_SEK=DC_SEK, herkunft="ERWARTUNG.md (ERW-E3d, Annahmen Opus)"), cmu={}, pack={}, top={}, massnahmen={})
    for v in ("LFP", "NMC"):
        zl = rechne(v)
        with open(H / f"fmeda_{v}.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(zl[0]), delimiter=";"); w.writeheader()
            for r in zl: w.writerow({k: (f"{x:.6g}" if isinstance(x, float) else x) for k, x in r.items()})
        erg["cmu"][v] = {sg: summe(zl, sg) for sg in ZIEL}; erg["cmu"][v]["Teile"] = len({r["Ref"] for r in zl})
        n = NCMU[v]; erg["pack"][v] = {"anzahl_CMU": n}
        for sg in ZIEL:
            c = erg["cmu"][v][sg]
            erg["pack"][v][sg] = dict(SPFM=c["SPFM"], LFM=c["LFM"], PMHF_Beitrag_FIT=n * c["PMHF_Beitrag_FIT"], lambda_SR_FIT=n * c["lambda_SR_FIT"],
                                      hinweis="nur CMU-Platinen, identische CMU: Quoten gleich, FIT summiert; ohne BMS-Rechner, Schuetze, Software")
        agg = {}
        for r in zl:
            if r["lambda_RF"] + r["lambda_MPF_latent"] > 0:
                k = (r["SG"], f'{r["Rolle"]} {r["Ausfallart"]}'); a = agg.setdefault(k, dict(SPF_RF=0, MPF_latent=0, refs=set())); a["SPF_RF"] += r["lambda_RF"]; a["MPF_latent"] += r["lambda_MPF_latent"]; a["refs"].add(r["Ref"])
        erg["top"][v] = {sg: [dict(posten=k[1], SPF_RF_FIT=a["SPF_RF"], MPF_latent_FIT=a["MPF_latent"], anzahl_Teile=len(a["refs"]))
                              for k, a in sorted(((k, a) for k, a in agg.items() if k[0] == sg), key=lambda t: -(t[1]["SPF_RF"] + t[1]["MPF_latent"]))[:5]] for sg in ZIEL}
    # Ziel verfehlt? dann Was-waere-wenn weiterer Massnahmen (M1 ist ab v0.2 Ist-Stand und steckt in den Zahlen oben)
    verfehlt = [f"{sg} {m}" for sg, z in ZIEL.items() for m in ("SPFM", "LFM") if erg["cmu"]["LFP"][sg][m] < z[m]]
    erg["verfehlt"] = verfehlt
    if verfehlt:
        for name, m in (("M2 Ueberwachung Ausgleich 99 % statt 90 % (Was-waere-wenn, nicht umgesetzt)", ("M2",))):
            zl = rechne("LFP", m); erg["massnahmen"][name] = {sg: summe(zl, sg) for sg in ZIEL}
    json.dump(erg, open(H / "ergebnis.json", "w"), indent=1, ensure_ascii=False)
    print("verfehlt:", verfehlt)
    for v in erg["cmu"]:
        for sg in ZIEL: c = erg["cmu"][v][sg]; print(v, sg, f'SR {c["lambda_SR_FIT"]:.3f} RF {c["lambda_SPF_RF_FIT"]:.4f} MPFl {c["lambda_MPF_latent_FIT"]:.4f} SPFM {c["SPFM"]*100:.2f} LFM {c["LFM"]*100:.2f}')
    for k, x in erg["massnahmen"].items(): print(k, {sg: (round(x[sg]["SPFM"]*100, 2), round(x[sg]["LFM"]*100, 2)) for sg in ZIEL})
