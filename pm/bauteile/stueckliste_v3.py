"""stueckliste_v3.py -- Stückliste v0.3 (SL3) je Variante als Quelle der Geometrie (Auftrag G5.1, cad/baukasten/PLAN.md §1, §3, §4).

KI-generiert (Claude Sonnet, 2026-11-19), Auftrag G5.1. Entwurf.
    python3 pm/bauteile/stueckliste_v3.py [--variante LFP|NMC] [--aus-cad]    (ohne Angabe: beide Varianten; --aus-cad: Massen BT-510…560, 610…630 aus cad/baukasten/ausgabe/ergebnis_<V>.json)
Eingaben: struktur.json, stueckliste_<V>.json (v0.2, nur für die Liste der offenen Altpositionen), parameter_<V>.json,
          cad/pack/entwurf/ergebnis_<V>_e2d.json, cad/pack/entwurf/parameter_<V>_e2d.json (A-Blöcke),
          sim/elektrik/e1_querschnitte/ergebnis.json, sim/elektrik/e2_elektronik/eingaben.json (Cu-Dichte), pm/entscheidungen/ENT-*.md (Akten je BT).
Ausgaben: pm/bauteile/stueckliste_<V>.json (Version 0.3), docs/13_stueckliste_<V>.md, docs/13_stueckliste.md (Übersicht beider Varianten),
          cad/baukasten/annahmen.json (alle A-Block-Einträge beider Varianten, zusammengeführt).
Regeln: Masse neuer Positionen = CAD-Volumen x Dichte (Herkunft "CAD-Volumen"). Dichten nur aus A-Blöcken bzw. E2-Eingaben; fehlt eine,
        steht sie in DICHTE_NEU mit Vermerk "NEUE ANNAHME" (Opus bestätigt). Preise nur als Anzeige aus pm/kosten/eingaben.json (SL3.1). Keine Eingriffe in pm/entscheidungen.
Detailstufe: K Konstruktionsstand (Eigenteile, Art E und Opus-Teile), F Kaufteilform (Art K), H Hüllkörper (nur ohne jede Formangabe), "-" keine Geometrie.
"""
import json, re, sys, glob
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "pm/kosten"))
import preisregeln as PR   # SL3.1: Preis wird nur angezeigt (aus pm/kosten/eingaben.json), nicht gerechnet
KOPF = "KI-generiert (Claude Sonnet, 2026-11-19), Auftrag G5.1, ergänzt SL3.1 (Auftrag KO2)"
D = ROOT / "cad/pack/entwurf"
BT = {x["id"]: x for x in json.loads((ROOT / "pm/bauteile/struktur.json").read_text())["bauteile"]}
E1 = json.loads((ROOT / "sim/elektrik/e1_querschnitte/ergebnis.json").read_text())["arten"]
E2EIN = json.loads((ROOT / "sim/elektrik/e2_elektronik/eingaben.json").read_text())["stoffe"]


def akten_je_bt():
    """ENT-Akten je BT (Kopf lesen, nicht ändern). Status 'ersetzt' ausgenommen."""
    M = {}
    for f in sorted(glob.glob(str(ROOT / "pm/entscheidungen/ENT-*.md"))):
        t = Path(f).read_text().split("---")[1]
        d = {}
        for l in t.splitlines():
            m = re.match(r"(\w+):\s*(.*?)(\s+#.*)?$", l)
            if m: d[m[1]] = m[2]
        if d.get("status", "").startswith("ersetzt"): continue
        vs = re.findall(r"[A-Z]{3}", d.get("variante", "")) or None
        for b in re.findall(r"BT-\d+", d.get("bauteile", "")): M.setdefault(b, []).append((d["id"], vs))
    return M
AKTEN = akten_je_bt()


def akten(bt, V):
    return sorted({i for i, vs in AKTEN.get(bt, []) if vs is None or V in vs})


def baugruppe(bt):
    while BT[bt].get("eltern") and BT[bt]["eltern"] != "BT-000": bt = BT[bt]["eltern"]
    return bt


def f3(x): return f"{x:.3f}".replace(".", ",") if isinstance(x, (int, float)) else str(x)


def bauen(V, aus_cad=False):
    E2P = f"cad/pack/entwurf/ergebnis_{V}_e2d.json"
    E2 = json.loads((ROOT / E2P).read_text()); G = E2["gruppen"]; X = E2["e2"]; A = E2["annahmen"]
    P = json.loads((ROOT / f"pm/bauteile/parameter_{V}.json").read_text())["parameter"]
    alt = json.loads((ROOT / f"pm/bauteile/stueckliste_{V}.json").read_text())   # v0.2 oder v0.3 (Altpositionen nur über stueckliste.json)
    altpos = json.loads((ROOT / "pm/bauteile/stueckliste.json").read_text())["positionen"]
    for _k, _v in [kv for _f in ("annahmen_g5.json", "annahmen_datenblatt.json") if (ROOT / "cad/baukasten" / _f).exists() for kv in json.loads((ROOT / "cad/baukasten" / _f).read_text()).items()]:   # Opus 2026-11-19: wie kern.py, spätere Quelle (annahmen_g5.json) überschreibt die A-Blöcke
        if not _k.startswith("_") and isinstance(_v, dict) and "wert" in _v and not (isinstance(_v["wert"], dict) and set(_v["wert"]) <= {"LFP", "NMC"}): A[_k] = _v
    am = lambda k: A[k]["wert"]
    # ---- Dichten (kg/m3) mit Herkunft
    DICHTE = {"Al": (am("A_alu_dichte_kg_m3"), f"{E2P} annahmen.A_alu_dichte_kg_m3"),
              "Cu": (E2EIN["rho_Cu_kg_m3"], "sim/elektrik/e2_elektronik/eingaben.json stoffe.rho_Cu_kg_m3 (Opus 2026-11-18)"),
              "Pad": (am("A_dichte_pad_kg_m3"), f"{E2P} annahmen.A_dichte_pad_kg_m3"),
              "Zelltraeger": (am("A_dichte_zelltraeger_kg_m3"), f"{E2P} annahmen.A_dichte_zelltraeger_kg_m3 (PC)"),
              "Verguss": (am("A_dichte_verguss_kg_m3"), f"{E2P} annahmen.A_dichte_verguss_kg_m3 (PU-Schaum)")}
    FW = json.loads((ROOT / "cad/baukasten/farben.json").read_text())["werkstoffe"]   # G5.1b: Dichten kommen von dort (Opus 2026-11-19)
    for k, w in (("Stahl", "Stahl"), ("Kunststoff", "Kunststoff"), ("Dichtung", "EPDM"), ("Mica", "Schaum_Zwischenlage")):
        DICHTE[k] = (FW[w]["dichte_kg_m3"], f"cad/baukasten/farben.json werkstoffe.{w} ({FW[w]['herkunft']})")
    DICHTE_NEU = {}
    vol = lambda grp: G[grp]["volumen_cm3"]
    m_vol = lambda cm3, w: cm3 * 1e-6 * DICHTE[w][0]       # kg
    Z = []

    def add(pos, bt, ben, art, wst, gen, stufe, lage, farbe, menge, masse_ges=None, masse_quelle=None, quelle="", bem="", hinweis=None, akt=None, mq=None):
        if menge is None: menge = "offen"
        r = dict(pos=pos, bt=bt, benennung=ben, art=art, werkstoff=wst, bemerkung=bem, quelle=quelle)
        r["menge_" + V] = menge
        r["masse_ges_kg"] = round(masse_ges, 6) if masse_ges is not None else "offen"
        r["masse_je_kg"] = round(masse_ges / menge, 6) if (masse_ges is not None and isinstance(menge, (int, float)) and menge) else "offen"
        r["masse_quelle"] = masse_quelle if masse_ges is not None else "offen (keine CAD-Geometrie, keine Akte)"
        r["geometrie"] = dict(generator=gen, detailstufe=stufe, lage=lage, farbe=farbe)
        r["akten"] = akt if akt is not None else akten(bt, V)
        r["kosten_je_eur"] = None; r["kosten_ges_eur"] = None
        r["baugruppe"] = baugruppe(bt); r["bt_name"] = BT[bt]["name"]
        if hinweis: r["hinweis_opus"] = hinweis
        if mq: r["menge_quelle"] = mq
        assert bt in BT, bt
        Z.append(r)

    def grp(g, w=None):   # Masse je Stück aus CAD-Gruppe (CAD-Masse), sonst Volumen x Dichte
        x = G[g]
        return x["masse_kg"] if w is None else m_vol(x["volumen_cm3"], w)
    GE = "Q = CAD-Gruppe"
    CQ = lambda g: f"{E2P} gruppen.{g}"
    cad_vd = "CAD-Volumen x Dichte"
    # ---------------------------------------------------------------- Zelle
    zel_b = "zelle.zelle_prismatisch" if V == "LFP" else "zelle.zelle_rund"
    add("100.1", "BT-100", f"Zelle ({P['BT-100']['format']['wert'].strip(chr(34))}, {V})", "K", "Zelle (Masse aus Akte, Hüllkörper)", zel_b, "F",
        "Zellfeld zwischen den Kühlplatten, Raster nach A_zellabstand", "zelle_blau" if V == "LFP" else "zelle_gruen", G["Zellen"]["anzahl"],
        G["Zellen"]["anzahl"] * P["BT-100"]["masse_g"]["wert"] / 1000, "Akte (BT-100 masse_g)", f"{CQ('Zellen')}; parameter_{V}.json BT-100 masse_g = {P['BT-100']['masse_g']['wert']}")
    add("200.1", "BT-210", "Zellreihe zwischen Querträgern (Anordnung, kein Eigenteil)", "E", "-", None, "-", "-", "-", None,
        hinweis="Anordnung der Zellen, keine eigene Geometrie; Masse steckt in 100.1. Opus bestätigen.")
    if V == "LFP":
        zl_n = G["Zellen"]["anzahl"] - 2 * (int(am("A_quertraeger_anzahl")) + 1)   # 250 - 2 x 4 = 242 (Opus 2026-11-19): 2 Reihen je Feld, Spalte = Zellen - 1 je Reihe und Feld
        zl_vol_mm3 = P["BT-100"]["laenge_mm"]["wert"] * P["BT-100"]["breite_mm"]["wert"] * am("A_zellabstand_LFP_mm")
        add("200.2", "BT-220", "Zwischenlage zwischen Zellen (Schaum, je Spalt eines Feldes)", "K", "Schaum_Zwischenlage", "zelle.zwischenlage", "K", "in jedem Spalt zwischen benachbarten Zellen eines Feldes, Dicke A_zellabstand_LFP_mm", "pad_grau", zl_n,
            zl_n * zl_vol_mm3 * 1e-9 * DICHTE["Mica"][0], "Annahme (Opus 2026-11-19: Menge, Werkstoff Schaum_Zwischenlage 300 kg/m3; Masse = Zellfläche x Dicke x Dichte, noch nicht CAD)", "Opus 2026-11-19 (AUFTRAG_G5_4 G5.1b Nr. 4)",
            hinweis="Menge 242 = 250 - 2 x 4 (Opus). Masse aus Zellfläche (Länge x Breite) x A_zellabstand_LFP_mm x Dichte Schaum_Zwischenlage; CAD-Stufe folgt in zelle.py.")
    add("200.3", "BT-230", "Wärmeleitmaterial / Pad Zelle-Kühlplatte", "K", "Pad", "zelle.pad", "F", "zwischen Zellfeld und Kühlplatte (oben und unten)", "pad_grau", G["Pad"]["anzahl"],
        grp("Pad"), cad_vd, CQ("Pad"))
    if V == "LFP":
        add("200.4", "BT-240", "Verspannung der Zellreihen: entfällt als Teil", "E", "-", None, "-", "-", "-", None,
            bem="Entfällt als Teil (Opus 2026-11-19): Querträger und Rahmen nehmen die Quellkraft auf (Cell-to-Pack).")
    else:
        add("200.5", "BT-250", "Zellhalter / Zellträger", "E", "Kunststoff (PC, Annahme A_dichte_zelltraeger)", "zelle.zelltraeger", "K", "unter den Zellen, 4 Träger (ENT-092)", "kunststoff_schwarz", G["Zelltraeger"]["anzahl"],
            grp("Zelltraeger"), cad_vd, CQ("Zelltraeger"),
            hinweis="PLAN §4.2 nennt BT-240 (varianten nur LFP), ENT-092 und v0.2 führen BT-250 (varianten NMC). BT-250 beibehalten, Opus bestätigen.")
        add("220.2", "BT-220", "Verguss Zellfeld (Zellen bis halbe Höhe)", "E", "PU-Schaum (Annahme A_dichte_verguss)", "zelle.verguss", "K", "Zellfeld unten, bis A_vergusshoehe_anteil_NMC", "kunststoff_schwarz", G["Verguss"]["anzahl"],
            grp("Verguss"), cad_vd, CQ("Verguss"),
            hinweis="PLAN §4.2: BT-220 (varianten in struktur.json nur LFP); ENT-092 nennt Verguss unter BT-250. Zuordnung Opus klären.")
    # ---------------------------------------------------------------- Elektronik/Sensorik
    am_e = f"{E2P} annahmen A_e2_*_masse_kg (ERW-E2 N1)"
    add("300.1", "BT-310", "BMS-Platine", "K", "Platine", "elektronik.bms_platine", "F", "Schaltbox, Platine auf 4 Abstandsbolzen M4", "platine_gruen", 1, am("A_e2_bms_masse_kg"), "Annahme (ERW-E2 N1)", am_e)
    cm = G["E2_CMU"]
    add("300.2", "BT-320", "Zellüberwachung CMU (Platine)", "K", "Platine (Masse ERW-E2 N1)", "elektronik.cmu", "F", "Endzonen vorn/hinten am Zellfeldrand (E2-Anordnung)", "platine_gruen", cm["anzahl"], cm["masse_kg"],
        "Annahme (ERW-E2 N1 A_e2_cmu_masse_kg)", CQ("E2_CMU"))
    ntc_je_mm3 = am("A_e2d_ntc_mm")[0] * am("A_e2d_ntc_mm")[1] * am("A_e2d_ntc_mm")[2]
    ntc_n = X["details"]["ntc"]
    ntc_cm3 = ntc_n * ntc_je_mm3 * 1e-3
    add("300.3", "BT-330", "Temperaturfühler Zelle (NTC)", "K", "Kunststoff/Keramik (Annahme Kunststoff)", "elektronik.ntc", "F", "auf FPC an der Zelle, 3 x 2 x 1 mm (A_e2d_ntc_mm)", "kunststoff_schwarz", ntc_n,
        m_vol(ntc_cm3, "Kunststoff"), cad_vd, f"{E2P} e2.details.ntc, annahmen.A_e2d_ntc_mm; Dichte Kunststoff aus farben.json",
        hinweis="NTC-Volumen aus A_e2d_ntc_mm x Anzahl; CAD-Gruppe E2_FPC_Detail fasst Tabs, NTC und Stecker zusammen und wird dafür geteilt.")
    add("300.4", "BT-340", "Shunt (Strommessung)", "K", "Cu/Manganin mit Platine", "elektronik.shunt", "F", "Schaltbox", "platine_gruen", 1, am("A_e2_shunt_masse_kg"), "Annahme (ERW-E2 N1)", am_e)
    add("300.5", "BT-350", "Isolationswächter", "K", "offen", "elektronik.isolationswaechter", "H", "Schaltbox (ENT-120 nennt nur den Ansprechwert)", "platine_gruen", 1,
        hinweis="Menge 1 (Opus 2026-11-19). Keine Formangabe in W33, Akte oder Annahme: Stufe H bis W34.")
    fp = G["E2_FPC"]
    add("300.6", "BT-360", "Flexleiterplatte FPC Zelle -> CMU", "K", "FPC (Masse ERW-E2 N1)", "elektronik.fpc", "F", "Seitenspalt bzw. Verbinderebene, Pfade aus e2.geometrie.fpc", "platine_gruen", fp["anzahl"], fp["masse_kg"],
        "Annahme (ERW-E2 N1 A_e2_fpc_masse_kg_m)", CQ("E2_FPC"))
    if "E2_FPC_Halter" in G:
        hl = G["E2_FPC_Halter"]
        add("361.1", "BT-361", "FPC-Halter", "K", "Kunststoff (Annahme)", "elektronik.fpc_halter", "F", "Seitenspalt, A_e2_fpc_halter_mm", "kunststoff_schwarz", hl["anzahl"], m_vol(hl["volumen_cm3"], "Kunststoff"), cad_vd,
            f"{CQ('E2_FPC_Halter')}; Dichte Kunststoff aus farben.json", "FPC-Halter unter BT-361 (Opus 2026-11-19)")
    fd = G["E2_FPC_Detail"]; fd_ohne_ntc = fd["volumen_cm3"] - ntc_cm3
    add("360.3", "BT-360", "FPC-Detail (Tabs, FPC-Stecker an der CMU)", "K", "Cu-Tab/Kunststoff (Annahme Kunststoff)", "elektronik.fpc_detail", "F", "Zelltabs am Pol, Stecker an der CMU", "kunststoff_schwarz",
        X["details"]["tabs"] + X["details"]["fpc_stecker"], m_vol(fd_ohne_ntc, "Kunststoff"), cad_vd, f"{CQ('E2_FPC_Detail')} Volumen minus NTC; Dichte Kunststoff aus farben.json", mq="CAD",
        hinweis="Mischteil (Cu-Tab 0,2 mm, Kunststoffstecker) mit Kunststoffdichte gerechnet; Masse klein, Opus bestätigen.")
    dk = G["E2_Daisy"]
    add("360.4", "BT-360", "Daisy-Chain-Leitung mit Steckern", "K", "Kabel/Kunststoff (Annahme Kunststoff)", "elektronik.daisy_kette", "F", "CMU zu CMU / BMS, Ø4 mm, Radius ≥ 20 mm", "kunststoff_schwarz", X["details"]["daisy_kabel"],
        m_vol(dk["volumen_cm3"], "Kunststoff"), cad_vd, f"{CQ('E2_Daisy')} (Kabel + Stecker); Dichte Kunststoff aus farben.json",
        hinweis="PLAN §4.2 nennt 360.2/360.3 für drei Teile; hier 361.1 Halter, 360.3 Detail, 360.4 Daisy. Menge = Kabelzahl, Masse inkl. Stecker.")
    # ---------------------------------------------------------------- Verbindungstechnik
    if V == "LFP":
        zv = G["Zellverbinder"]; n_e1 = E1["LFP Zell-/Reihenverbinder (BT-410/420)"]["stueck"]
        assert n_e1 == G["Zellen"]["anzahl"] - 1
        add("400.1", "BT-410", "Zellverbinder (Zellabgriff, Plus und Minus je Zelle): LFP nicht vorhanden", "E", "-", None, "-", "-", "-", None,
            hinweis="LFP hat keinen Zellabgriff; Reihenverbinder stehen in 400.2 (BT-420). Position nur aus Altliste v0.2, Opus: streichen?")
        add("400.2", "BT-420", "Zellverbinder = Reihenverbinder (s - 1)", "E", "Al", "verbinder.zellverbinder_lfp", "K", "zwischen den Zellpolen, Omega-Dehnbogen, Schweißlinien (Fenster hinten voll)", "al_blank", n_e1,
            n_e1 * zv["masse_kg"] / zv["anzahl"], cad_vd, f"{CQ('Zellverbinder')} (CAD {zv['anzahl']} Stück, Masse je Stück); Stückzahl nach PLAN §4.3 = E1 {n_e1} = Zellen - 1",
            hinweis=f"Widerspruch CAD {zv['anzahl']} / E1 {n_e1}: 249 gilt (PLAN §4.3), CAD zieht nach. A_CAD 25 x 3 = 75 mm2, A_E1 {E1['LFP Zell-/Reihenverbinder (BT-410/420)']['A_mm2']} mm2.")
    else:
        zg = G["Zellabgriff"]; n_e1 = E1["NMC Zellabgriff (BT-410)"]["stueck"]
        add("400.1", "BT-410", "Zellabgriff (Plus und Minus je Zelle)", "E", "Al", "verbinder.zellabgriff", "K", "Scheibe 12 x 1 auf jedem Pol, Laserschweißung", "al_blank", n_e1, n_e1 * zg["masse_kg"] / zg["anzahl"], cad_vd,
            f"{CQ('Zellabgriff')} (CAD {zg['anzahl']} Stück, Masse je Stück); Stückzahl nach PLAN §4.3 = E1 {n_e1}",
            hinweis=f"Widerspruch CAD {zg['anzahl']} / E1 {n_e1}: {n_e1} gilt (PLAN §4.3), CAD zieht nach.")
        gv = G["Gruppenverbinder"]; gb = G["Gruppenbruecke"]
        add("400.2", "BT-420", "Gruppenverbinder = Sammelblech (je 4 Zellen)", "E", "Al (Annahme, Cu offen)", "verbinder.gruppenverbinder", "K", "über 4 Zellen je Gruppe", "al_blank", gv["anzahl"], gv["masse_kg"], cad_vd, CQ("Gruppenverbinder"),
            hinweis=f"E1 nennt {E1['NMC Gruppenverbinder (BT-420)']['stueck']} Stück ({E1['NMC Gruppenverbinder (BT-420)']['masse_gesamt_kg']:.2f} kg): PLAN §4.3, CAD gilt (217 Sammelbleche).")
        add("420.2", "BT-420", "Gruppenbrücke (Reihenbrücke)", "E", "Al (Annahme, Cu offen)", "verbinder.gruppenbruecke", "K", "zwischen benachbarten Gruppen", "al_blank", gb["anzahl"], gb["masse_kg"], cad_vd, CQ("Gruppenbruecke"))
    # HV-Leitung: A_CAD gegen A_E1
    hvk = f"{'LFP' if V == 'LFP' else 'NMC'} HV-Hauptleitung (BT-430)"
    e1h = E1[hvk]; A_cad = P["BT-430"]["querschnitt_mm2"]["wert"]; L_cad = X["hv_laenge_gesamt_m"]
    hv = G["E2_HV_Leitung"]
    add("400.3", "BT-430", "HV-Leitung im Pack (Leiter Cu)", "K", "Cu (Leiter, Isolierung ohne Wert)", "verbinder.hv_leitung", "F", "Zelle -> Schaltbox, Verlegung hinten (ENT-144), Radius ≥ 5 D", "hv_orange", len(X["hv"]), hv["masse_kg"],
        "CAD-Volumen x Dichte (Länge x A_CAD x Dichte Cu)", f"{CQ('E2_HV_Leitung')}; A_CAD parameter_{V}.json BT-430 querschnitt_mm2",
        hinweis=(f"A_CAD {A_cad} mm2 {'=' if abs(A_cad - e1h['A_mm2']) < 1e-9 else '!='} A_E1 {e1h['A_mm2']} mm2 (sim/elektrik/e1_querschnitte/ergebnis.json). "
                 f"Masse CAD {hv['masse_kg']:.3f} kg (Länge gesamt {L_cad:.3f} m, ergebnis e2d e2.hv_laenge_gesamt_m), E1 {e1h['masse_gesamt_kg']:.3f} kg ({e1h['stueck']} x {e1h['laenge_mm']} mm). CAD-Verlegung gilt (PLAN §4.3)."))
    # Laschen und Stromschienen BT-440 (struktur.json BT-440)
    la = G["E2_Lasche"]
    add("440.1", "BT-440", "Plus-/Minus-Anschlusslasche (Pol)", "E", "Al", "verbinder.pol_lasche", "K", "Reihenenden hinten, M8, Überlappung 25 mm", "al_blank", la["anzahl"], la["masse_kg"], cad_vd, CQ("E2_Lasche"))
    sc = G["E2_Stromschiene"]
    add("440.2", "BT-440", "Stromschienen der Schaltbox (Cu)", "E", f"Cu {'25' if V == 'LFP' else '20'} x 3", "verbinder.stromschiene", "K", "Schaltbox, biegeweich, Bohrung 8,5, Schrumpfschlauch", "cu", sc["anzahl"], sc["masse_kg"], cad_vd, CQ("E2_Stromschiene"), hinweis="Stückzahl aus CAD: 12 Verbindungen nach ctx.schaltbox[schienen] (SL3 hatte 6 aus E2d, Sonnet G5.4).", mq="CAD")
    if V == "NMC":
        bs = G["E2_Beruehrschutz"]
        add("450.1", "BT-450", "Berührschutz über den Verbindern (Platten)", "E", "Kunststoff (Annahme)", "verbinder.beruehrschutz", "K", "über Gruppenverbindern, Dicke 1 mm", "kunststoff_schwarz", bs["anzahl"], m_vol(bs["volumen_cm3"], "Kunststoff"), cad_vd,
            f"{CQ('E2_Beruehrschutz')}; Dichte Kunststoff aus farben.json")
    # ---------------------------------------------------------------- Gehäuse
    add("500.1", "BT-510", "Gehäusewanne (im CAD: Boden)", "E", "Al", "gehaeuse.wanne", "K", "Packboden über Unterfahrschutz, X 0 bis Gehäuselänge, Y Mitte 0", "al_blank", G["Boden"]["anzahl"], grp("Boden"), cad_vd, CQ("Boden"))
    add("520.1", "BT-520", "Deckel", "E", "Al", "gehaeuse.deckel", "K", "über den Zellen, Aussparungen Service/Schaltbox", "al_eloxiert", G["Deckel"]["anzahl"], grp("Deckel"), cad_vd, CQ("Deckel"))
    if V == "LFP":
        sd = G["E2_Servicedeckel"]
        add("520.2", "BT-520", "Servicedeckel (Senkschrauben bündig)", "E", "Al", "gehaeuse.servicedeckel", "K", "Deckelöffnung 120 x 80 vorn über der Trennbrücke", "al_eloxiert", sd["anzahl"], sd["masse_kg"], cad_vd, CQ("E2_Servicedeckel"))
    add("500.3", "BT-530", "Querträger", "E", "Al", "gehaeuse.quertraeger", "K", "quer im Zellfeld, x aus ergebnis quertraeger_x_mm", "al_blank", G["Quertraeger"]["anzahl"], grp("Quertraeger"), cad_vd, CQ("Quertraeger"))
    add("500.4", "BT-540", "Seitenrahmen (Rahmenprofil, keine Knautschzone nach ENT-151)", "E", "Al (Vollprofil, Obergrenze)", "gehaeuse.seitenrahmen", "K", "umlaufend außen, Breite 30 (ENT-087), Mehrkammer", "al_blank", 4, grp("Seitenrahmen"), cad_vd, CQ("Seitenrahmen"), bem="Menge 4 = 2 Längs- und 2 Querprofile (Opus 2026-11-19)")
    add("500.5", "BT-550", "Unterfahrschutz", "E", "Al", "gehaeuse.unterfahrschutz", "K", "unter der Wanne, Z = 0", "al_blank", G["Unterfahrschutz"]["anzahl"], grp("Unterfahrschutz"), cad_vd, CQ("Unterfahrschutz"))
    add("500.6", "BT-560", "Befestigungspunkte am Fahrzeug (Stahlhülse)", "E", "Stahl (Hülse)", "gehaeuse.befestigung", "K", "6 je Längsseite am Seitenrahmen", "stahl_blank", 12,
        hinweis="Menge 12 = 6 je Längsseite, Annahme Opus A_g5_befestigung_n_je_seite (Vorgabe Opus 2026-11-19, noch nicht in annahmen.json, da A-Blöcke e2d sie nicht enthalten).")
    add("500.7", "BT-570", "Druckausgleichselement (atmend, wasserdicht)", "K", "offen", "kaufteile.druckausgleich", "F", "Rückwand, Ø 20 mm (A_e2d_box_druckausgleich_d_mm)", "kunststoff_schwarz", 1,
        hinweis="Ø20 mm stammt aus ERW-E2 N3 für die Schaltbox (Annahme); Übertragung auf das Pack-Element und Masse offen, W34 abwarten.")
    dg = G["E2_Dichtung"]
    add("580.1", "BT-580", "Dichtungen (Deckel, Schaltbox, Servicedeckel)", "K", "EPDM", "normteile.dichtung", "F", "Flächen- bzw. Schnurdichtung 3 x 3 mm an den Flanschen", "dichtung", dg["anzahl"], m_vol(dg["volumen_cm3"], "Dichtung"), cad_vd,
        f"{CQ('E2_Dichtung')}; Dichte Dichtung (EPDM) aus farben.json", mq="CAD")
    for pos, g_, ben, gen, w_, lage, farbe in [
            ("590.1", "E2_Schraube", "Schrauben (M4/M5/M8, Stahl)", "normteile.schraube", "Stahl", "Schaltbox, Stecker, Schütze, Verbinder", "stahl_blank"),
            ("590.2", "E2_Kabelschuh", "Kabelschuhe (Hülse + Palme)", "normteile.kabelschuh", "Cu", "an den HV-Leitungen", "cu"),
            ("590.3", "E2_Clip", "Kabelclips", "normteile.clip", "Kunststoff", "Kabelführung, alle 200 mm", "kunststoff_schwarz"),
            ("590.4", "E2_Schrumpfschlauch", "Schrumpfschlauch 0,5 mm", "normteile.schrumpfschlauch", "Kunststoff", "über den Stromschienen", "hv_orange")]:
        if g_ not in G: continue
        add(pos, "BT-590", ben, "K", {"Stahl": "Stahl (Annahme)", "Cu": "Cu", "Kunststoff": "Kunststoff (Annahme)"}[w_], gen, "F", lage, farbe, G[g_]["anzahl"], m_vol(vol(g_), w_), cad_vd,
            f"{CQ(g_)}; Dichte {w_} = " + ("Cu aus E2-Eingaben" if w_ == "Cu" else "farben.json"), mq="CAD")
    # ---------------------------------------------------------------- Kühlung
    add("600.1", "BT-610", "Kühlplatte", "E", "Al (Vollmaterial, Obergrenze, Füllgrad)", "kuehlung.kuehlplatte", "K", "über und unter dem Zellfeld, mit Kanälen (ENT-104/105)", "al_blank", G["Kuehlplatte"]["anzahl"], grp("Kuehlplatte"), cad_vd, CQ("Kuehlplatte"))
    add("600.2", "BT-620", "Verteiler und Sammler", "E", "offen", "kuehlung.verteiler", "K", "an der Kühlplatte, Kanäle quer (ENT-106)", "al_blank", 2, hinweis="Menge 2 (Opus-Vorgabe 2026-11-19).")
    add("600.3", "BT-630", "Kühlmittelanschlüsse Ein/Aus", "K", "offen", "kuehlung.anschluss", "K", "Kühlplattenende", "al_blank", 2, hinweis="Generator kuehlung.anschluss, Menge 2, Stufe K (Opus-Vorgabe 2026-11-19).")
    add("600.4", "BT-640", "Temperaturfühler Kühlmittel", "K", "offen", "kaufteile.temperaturfuehler_kuehlmittel", "H", "an den Anschlüssen (Ein/Aus)", "kunststoff_schwarz", 2, hinweis="Menge 2 (Opus 2026-11-19). Keine Formangabe: Stufe H bis W34.")
    add("600.5", "BT-650", "Kühlmittel Wasser-Glykol", "K", "Flüssigkeit", None, "-", "in den Kanälen", "-", None, hinweis="Flüssigkeit, keine Geometrie (PLAN §3: Detailstufe -).")
    add("600.6", "BT-660", "Pumpe, Wärmetauscher/Kältemittelkühler", "S", "außerhalb", None, "-", "Fahrzeugkreis (jetzt BT-661…665, Positionen 660.1…660.5)", "-", None, hinweis="Art S; Kühlkreis wird seit Opus-Zusatz 2026-11-19 als Positionen 660.1…660.5 modelliert (Detailstufe -).")
    for pos_, bt_, ben_, wst_, gen_, lage_, mq_ in (
            ("660.1", "BT-661", "Kühlmittelpumpe (elektrisch)", "offen", "kuehlung.pumpe", "im Kühlkreis außerhalb der Kühlplatten", None),
            ("660.2", "BT-662", "Chiller (Kältemittel-Wasser-Wärmetauscher)", "offen", "kuehlung.chiller", "im Kühlkreis", None),
            ("660.3", "BT-663", "3/2-Wege-Ventil", "offen", "kuehlung.ventil", "im Kühlkreis", None),
            ("660.4", "BT-664", "Kühlmittelschläuche", "offen", "kuehlung.schlauch", "zwischen Packanschlüssen, Pumpe, Chiller, Ventil, Behälter", "CAD"),
            ("660.5", "BT-665", "Ausgleichsbehälter", "offen", "kuehlung.ausgleichsbehaelter", "im Kühlkreis", None)):
        add(pos_, bt_, ben_, "K", wst_, gen_, "F", lage_, "kunststoff_schwarz", 1, hinweis="Opus-Zusatz 2026-11-19 (Autor: Kühlkreis modellieren). Masse aus G5-CAD (folgt).", mq=mq_)
    # ---------------------------------------------------------------- Schaltbox
    sb = G["E2_Schaltbox"]
    add("700.1", "BT-710", "Schaltbox (Gehäuse)", "E", "Al", "schaltbox.gehaeuse", "K", f"Deckel hinten (ENT-144), x0,y0,z0 = {X['schaltbox_x0_y0_z0_mm']}", "al_blank", sb["anzahl"], sb["masse_kg"], cad_vd, CQ("E2_Schaltbox"))
    if "E2_Schaltbox_Deckel" in G:
        sbd = G["E2_Schaltbox_Deckel"]
        add("700.1b", "BT-710", "Schaltbox-Deckel", "E", "Al", "schaltbox.deckel", "K", "auf der Schaltbox, Dichtung 3 x 3, M5 alle 60 mm", "al_eloxiert", sbd["anzahl"], sbd["masse_kg"], cad_vd, CQ("E2_Schaltbox_Deckel"))
    INH = [("700.2", "BT-711", "Hauptschütz", 2, 2 * am("A_e2_schuetz_masse_kg"), "kaufteile.schuetz_haupt", "liegend in der Schaltbox, Bolzen 2 x M8"),
           ("700.3", "BT-712", "Vorladeschütz und Vorladewiderstand (Widerstandsmasse 0 gesetzt)", 2, am("A_e2_vorlade_masse_kg"), "kaufteile.schuetz_vorlade", "liegend in der Schaltbox"),
           ("700.4", "BT-713", "Pyrosicherung und Schmelzsicherung", 2, am("A_e2_pyro_masse_kg") + am("A_e2_schmelz_masse_kg"), "kaufteile.sicherungen", "Schaltbox, Pyro Ø30 x 80, Schmelz im Halter 40 x 40 x 95")]
    STE = [("700.6", "BT-730", "HV-Steckverbinder 250 A und 40 A", 2, am("A_e2_hv250_masse_kg") + am("A_e2_hv40_masse_kg"), "kaufteile.hv_stecker", "Schaltbox, Flansch 90 x 70 x 8 bzw. 50 x 40 x 6"),
           ("700.7", "BT-740", "NV-Steckverbinder 26-polig", 1, am("A_e2_nv_masse_kg"), "kaufteile.nv_stecker", "Schaltbox, Flansch 50 x 30 x 5"),
           ("700.10", "BT-770", "Gas- und Drucksensor", 1, am("A_e2_gas_masse_kg"), "kaufteile.gassensor", "Schaltbox")]
    for pos, bt, ben, n, m, gen, lage in INH + STE:
        add(pos, bt, ben, "K", "E2 Teil (Masse ERW-E2 N1)", gen, "F", lage, "kunststoff_schwarz", n, m, "Datenblatt (cad/baukasten/annahmen_g5.json, Opus 2026-11-19)" if pos in ("700.2", "700.3") else "Annahme (ERW-E2 N1)", am_e)
    chk = sum(r["masse_ges_kg"] for r in Z if r["pos"] in [p[0] for p in INH])
    pass
    inh_all = sum(r["masse_ges_kg"] for r in Z if r["pos"] in [p[0] for p in INH] + ["300.1", "300.4"])
    ABW = {"schaltbox_inhalt_kg": round(inh_all - G["E2_Schaltbox_Inhalt"]["masse_kg"], 6)}   # Opus 2026-11-19: Datenblattmassen aus annahmen_g5.json, e2d-CAD zieht nach
    ste_all = sum(r["masse_ges_kg"] for r in Z if r["pos"] in [p[0] for p in STE] + (["700.5"] if V == "NMC" else []))
    if V == "NMC":
        add("700.5", "BT-720", "Service-Trennstecker", "K", "E2 Teil (Masse ERW-E2 N1)", "kaufteile.trennstecker", "F", "in der Reihenmitte, oben zugänglich (ENT-131)", "hv_orange", 1, am("A_e2_trennstecker_masse_kg"), "Annahme (ERW-E2 N1)", am_e)
        ste_all += am("A_e2_trennstecker_masse_kg")
    ABW["stecker_sensor_kg"] = round(ste_all - G["E2_Stecker_Sensor"]["masse_kg"], 6)
    if V == "LFP":
        tb, ts = G["E2_Trennbruecke"], G["E2_Trennbrueckenschraube"]
        add("720.2", "BT-720", "Service-Trennbrücke mit Schrauben (LFP, ENT-150)", "K", "Cu 25 x 3 + Stahlschrauben", "verbinder.trennbruecke", "K", "Querverbinder vorn, unter dem Servicedeckel, 2 x M8", "cu", tb["anzahl"],
            tb["masse_kg"] + m_vol(ts["volumen_cm3"], "Stahl"), cad_vd, f"{CQ('E2_Trennbruecke')} + {CQ('E2_Trennbrueckenschraube')}; Schraubendichte Stahl aus farben.json",
            hinweis="Menge = Brückenteile laut CAD-Gruppe; Schrauben (6) in der Masse enthalten.")
    add("700.8", "BT-750", "Entgasungsventil mit Entgasungskanal", "K", "offen", "kaufteile.entgasungsventil", "H", "Rückwand", "kunststoff_schwarz", 1, hinweis="Menge 1 (Opus 2026-11-19). Keine Formangabe (W34 läuft): Stufe H bis W34.")
    add("700.9", "BT-760", "Heizung (Kälte, −20 °C laut REQ-P08)", "K", "im Fahrzeug-Kühlkreis (ENT-135)", None, "-", "außerhalb des Packs (PTC im Kühlkreis des Fahrzeugs, ENT-135 vorgeschlagen)", "-", None, hinweis="Heizung im Fahrzeug-Kühlkreis, keine Pack-Geometrie. Opus bestätigen.")
    add("700.11", "BT-780", "Kennzeichnung (Typschild, HV-Warnung)", "K", "offen", "kaufteile.typschild", "H", "auf dem Deckel", "kunststoff_schwarz", 1, hinweis="Menge 1 (Opus 2026-11-19). Keine Formangabe: Stufe H bis W34.")
    # Opus-Vorgabe 2026-11-19: Masse künftig aus G5-CAD; alter Wert bleibt als masse_alt_kg
    NEU = {"BT-510", "BT-520", "BT-530", "BT-540", "BT-550", "BT-560", "BT-610", "BT-620", "BT-630", "BT-661", "BT-662", "BT-663", "BT-664", "BT-665"}
    for r in Z:
        if r["bt"] in NEU:
            r["masse_alt_kg"] = r["masse_ges_kg"]; r["masse_quelle"] = "G5-CAD (folgt)"
    # ---------------------------------------------------------------- SL3.1: Kühlplatte aus K2b, Kühlkreis aus annahmen_g5.json (Auftrag KO2)
    AG5 = json.loads((ROOT / "cad/baukasten/annahmen_g5.json").read_text())
    K2B_P = "sim/kuehlung/k2_kuehlplatte/ergebnis_k2b.json"
    K2B = json.loads((ROOT / K2B_P).read_text())["faelle"]
    mae = AG5["A_g5_maeander"]["wert"]
    fk = [f for f in K2B if f["var"] == V and f["fuehrung"] == mae["fuehrung"] and f["n_bahnen"] == mae["bahnen"] and f["breite_mm"] == mae["teilkanal_mm"]]
    assert len(fk) == 1, (V, len(fk))
    for r in Z:
        if r["bt"] == "BT-610":
            r["benennung"] = f"Kühlplatte (Blech 1/4/1 mm, Mäander {mae['bahnen']} Bahnen {mae['fuehrung']}, Teilkanal {mae['teilkanal_mm']} mm)"
            r["werkstoff"] = "Al-Blech 1/4/1 mm gelötet (hohl, ENT-152…156)"
            r["masse_ges_kg"] = round(fk[0]["masse_2_platten_kg"], 6)
            m_ = r["menge_" + V]; r["masse_je_kg"] = round(fk[0]["masse_2_platten_kg"] / m_, 6) if isinstance(m_, (int, float)) and m_ else "offen"
            r["masse_quelle"] = "K2b (bis G5-CAD)"; r["quelle"] = f"{K2B_P} fall {fk[0]['fall']}, {mae['fuehrung']}, {mae['bahnen']} Bahnen, Teilkanal {mae['teilkanal_mm']} mm (masse_2_platten_kg); Wahl A_g5_maeander in annahmen_g5.json"
            r["akten"] = sorted(set(r["akten"]) | {f"ENT-{n}" for n in (152, 153, 154, 155, 156)})
    for pos_, k_ in (("660.1", "A_g5_pumpe_masse_kg"), ("660.2", "A_g5_chiller_masse_kg"), ("660.3", "A_g5_ventil_masse_kg"), ("660.5", "A_g5_behaelter_masse_kg")):
        for r in Z:
            if r["pos"] == pos_:
                r["masse_ges_kg"] = AG5[k_]["wert"] * r["menge_" + V]; r["masse_je_kg"] = AG5[k_]["wert"]
                r["masse_quelle"] = f"Annahme Opus 2026-11-19 (cad/baukasten/annahmen_g5.json {k_}, bis Datenblatt)"
    for r in Z:
        if r["pos"] == "660.4": r["masse_quelle"] = "G5-CAD (folgt)"
    # ---------------------------------------------------------------- SL3.1: Typen und Datenblätter (pm/bauteile/kaufteile_datenblatt.json, aus forschung/datenblaetter.md)
    DB = json.loads((ROOT / "pm/bauteile/kaufteile_datenblatt.json").read_text())
    for r in Z:
        d = DB.get(r["pos"])
        if d is None: r["hersteller_typ"] = None; r["datenblatt"] = []; continue
        r["hersteller_typ"] = d["hersteller_typ"]; r["datenblatt"] = d["datenblatt"]
        n_ = r["menge_" + V]
        m_db = d.get("masse_ges_kg") if "masse_ges_kg" in d else (d["masse_je_kg"] * n_ if d.get("masse_je_kg") is not None and isinstance(n_, (int, float)) else None)
        r["masse_datenblatt_kg"] = round(m_db, 6) if m_db is not None else None; r["masse_datenblatt_hinweis"] = d["masse_hinweis"]
        if m_db is None: continue
        if r["masse_ges_kg"] == "offen":   # keine andere Quelle: Datenblattmasse wird übernommen
            r["masse_ges_kg"] = round(m_db, 6); r["masse_je_kg"] = round(m_db / n_, 6); r["masse_quelle"] = "Datenblatt"
        elif abs(r["masse_ges_kg"] - m_db) < 1e-9:
            r["masse_quelle"] = "Datenblatt"
        else:   # Annahme ERW-E2 N1 hängt am CAD (Prüfsummen); Abweichung nur ausweisen, nicht ändern
            r["hinweis_opus"] = (r.get("hinweis_opus", "") + f" Datenblattmasse {m_db:.4g} kg weicht von der Annahmemasse {r['masse_ges_kg']:.4g} kg ab (CAD zieht nach Freigabe nach).").strip()
    if aus_cad:   # G5.1b Nr. 6: nach G5.7 Massen dieser Positionen aus der Montage lesen (ergebnis_<V>.json, nur ganze Läufe ohne G5_NUR)
        ep = ROOT / f"cad/baukasten/ausgabe/ergebnis_{V}.json"
        er = json.loads(ep.read_text()); assert not er.get("nur"), "ergebnis_%s.json stammt aus einem Teillauf (G5_NUR)" % V
        zm = {z["pos"]: z for z in er["positionen"]}
        for r in Z:
            if r["bt"] in NEU and r["pos"] in zm:
                z = zm[r["pos"]]; r["masse_ges_kg"] = z["masse_cad_kg"]; r["masse_quelle"] = f"G5-CAD (cad/baukasten/ausgabe/ergebnis_{V}.json)"
                m_ = r["menge_" + V]; r["masse_je_kg"] = round(z["masse_cad_kg"] / m_, 6) if isinstance(m_, (int, float)) and m_ else "offen"
    # ---------------------------------------------------------------- SL3.1: Preis je Position (nur Anzeige aus pm/kosten/eingaben.json, Zuordnung pm/kosten/preisregeln.py)
    for r in Z: r["preis"] = PR.preis_je(r["pos"], r["bt"], V)
    # ---------------------------------------------------------------- Abgleich mit Altliste
    vorhanden_bt = {r["bt"] for r in Z}
    ungedeckt = [p for p in altpos if p["teil"] in BT and not (BT[p["teil"]].get("varianten") and V not in BT[p["teil"]]["varianten"]) and p["teil"] not in vorhanden_bt]
    assert not ungedeckt, [(p["pos"], p["teil"]) for p in ungedeckt]
    gruppen_zuordnung = {"Zellen", "Pad", "Zelltraeger", "Verguss", "Boden", "Deckel", "Quertraeger", "Seitenrahmen", "Unterfahrschutz", "Kuehlplatte", "Zellverbinder", "Zellabgriff", "Gruppenverbinder", "Gruppenbruecke",
                         "E2_CMU", "E2_Schaltbox_Inhalt", "E2_Schraube", "E2_HV_Leitung", "E2_Kabelschuh", "E2_Clip", "E2_Stromschiene", "E2_Schrumpfschlauch", "E2_Schaltbox", "E2_Dichtung", "E2_Schaltbox_Deckel", "E2_Stecker_Sensor",
                         "E2_Lasche", "E2_Trennbruecke", "E2_Trennbrueckenschraube", "E2_Servicedeckel", "E2_FPC", "E2_FPC_Halter", "E2_FPC_Detail", "E2_Daisy", "E2_Beruehrschutz"}
    assert set(G) <= gruppen_zuordnung, set(G) - gruppen_zuordnung
    Z.sort(key=lambda r: (r["baugruppe"], r["bt"], r["pos"]))
    # ---------------------------------------------------------------- Summen
    pos_ids = [r["pos"] for r in Z]; assert len(set(pos_ids)) == len(pos_ids)
    m_sum = sum(r["masse_ges_kg"] for r in Z if r["masse_ges_kg"] != "offen")
    stufen = {}
    for r in Z: stufen[r["geometrie"]["detailstufe"]] = stufen.get(r["geometrie"]["detailstufe"], 0) + 1
    bg = {}
    for r in Z:
        if r["masse_ges_kg"] != "offen": bg[r["baugruppe"]] = bg.get(r["baugruppe"], 0) + r["masse_ges_kg"]
    m_cad = E2["masse_bekannt_kg"]
    pruef = dict(abweichung_gegen_e2d_gruppen=ABW, positionen_gesamt=len(Z), positionen_je_detailstufe=stufen, anteil_H_prozent=round(100 * stufen.get("H", 0) / len(Z), 1),
                 positionen_masse_offen=sum(1 for r in Z if r["masse_ges_kg"] == "offen"),
                 masse_gesamt_kg=round(m_sum, 3), masse_je_baugruppe_kg={k: round(v, 3) for k, v in sorted(bg.items())},
                 masse_cad_e2d_kg=round(m_cad, 3), quelle_masse_cad=f"{E2P} masse_bekannt_kg", abweichung_gegen_cad_prozent=round(100 * (m_sum / m_cad - 1), 2),
                 hinweis_abweichung="SL3 enthält Stückzahlkorrekturen (PLAN §4.3) und Massen der im CAD mit 0 gesetzten Teile (CAD-Volumen x Dichte); das CAD zieht in G5.2/G5.7 nach.",
                 zellen=G["Zellen"]["anzahl"], energie_kWh=round(G["Zellen"]["anzahl"] * P["BT-100"]["nennspannung_V"]["wert"] * P["BT-100"]["kapazitaet_Ah"]["wert"] / 1000, 2))
    erw = {"LFP": dict(pos=(42, 58), masse=(615, 630)), "NMC": dict(pos=(47, 63), masse=(470, 486))}[V]
    pruef["erwartung_cad_baukasten_ERWARTUNG_md"] = dict(positionen_band=erw["pos"], positionen_im_band=erw["pos"][0] <= len(Z) <= erw["pos"][1],
                                                         masse_band_kg=erw["masse"], masse_im_band=erw["masse"][0] <= m_sum <= erw["masse"][1])
    entf = [f"{p['pos']} {p['benennung']}" for p in altpos if p["teil"] in BT and BT[p["teil"]].get("varianten") and V not in BT[p["teil"]]["varianten"] and p["teil"] not in vorhanden_bt]
    dichten = {k: dict(wert=v[0], einheit="kg/m3", herkunft=v[1]) for k, v in DICHTE.items()}
    out = dict(hinweis=KOPF + ". Entwurf. Stückliste v0.3 als Quelle der Geometrie (cad/baukasten/PLAN.md), Kosten nur als Anzeige (Feld preis, aus pm/kosten/eingaben.json).", variante=V, version="0.3",
               quellen=[E2P, f"cad/pack/entwurf/parameter_{V}_e2d.json", f"pm/bauteile/parameter_{V}.json", "sim/elektrik/e1_querschnitte/ergebnis.json", "sim/elektrik/e2_elektronik/eingaben.json", "pm/bauteile/struktur.json", "pm/entscheidungen/ENT-*.md", "cad/baukasten/PLAN.md"],
               summen=dict(masse_stueckliste_kg=pruef["masse_gesamt_kg"], zellen=pruef["zellen"], energie_kWh=pruef["energie_kWh"], hinweis="Kompatibilität zu pm/kosten/kosten.py (liest summen.energie_kWh)"), fehlende_bt=[], pruefsummen=pruef, dichten_kg_m3=dichten, neue_annahmen_dichte=sorted(DICHTE_NEU), entfaellt=entf, positionen=Z)
    (ROOT / f"pm/bauteile/stueckliste_{V}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
    return out


def doku(V, o):
    Z = o["positionen"]; pr = o["pruefsummen"]
    md = [f"| Dok.-Nr. | BAT-DOC-13 | Version | 0.3 | Status | Entwurf |\n|---|---|---|---|---|---|\n| Titel | Stückliste Konstruktionsstand (SL3) – Variante {V} | Ersteller | Claude Sonnet (KI), pm/bauteile/stueckliste_v3.py | Prüfer | Opus (Stichprobe), Mensch offen |\n\n"
          f"> **KI-generiert.** ({KOPF}.) Nicht von Hand bearbeiten: `python3 pm/bauteile/stueckliste_v3.py --variante {V}` schreibt die Datei neu. Entwurf, nicht freigegeben.\n"
          "> Quelle der Geometrie (cad/baukasten/PLAN.md §1): jede Position trägt einen Generator `<modul>.<funktion>`. Preise sind eine Anzeige aus `pm/kosten/eingaben.json` (SL3.1), gerechnet wird in `pm/kosten/kosten.py`. Hersteller/Typ und Datenblatt aus `pm/bauteile/kaufteile_datenblatt.json` (Quelle `forschung/datenblaetter.md`).\n\n"
          f"**Positionen:** {pr['positionen_gesamt']} (Stufe K/F/H/-: " + " / ".join(str(pr['positionen_je_detailstufe'].get(s, 0)) for s in ("K", "F", "H", "-")) + f"), Stufe H {pr['anteil_H_prozent']} %. "
          f"**Masse gesamt:** {pr['masse_gesamt_kg']:.2f} kg (CAD e2d {pr['masse_cad_e2d_kg']:.2f} kg, {pr['abweichung_gegen_cad_prozent']:+.2f} %). **Zellen:** {pr['zellen']}, {pr['energie_kWh']} kWh. "
          f"Positionen mit Masse „offen“: {pr['positionen_masse_offen']}.\n\n"
          "Art: K Kaufteil, E Eigenteil, S Systemteil außerhalb. Stufe: K Konstruktionsstand, F Kaufteilform, H Hüllkörper, - keine Geometrie. Masse „offen“: keine CAD-Geometrie, keine Akte.\n"]
    bgn = None
    for r in Z:
        if r["baugruppe"] != bgn:
            bgn = r["baugruppe"]; md.append(f"\n## {bgn} {BT[bgn]['name']}\n\n| Pos. | BT | Benennung | Hersteller / Typ (Datenblatt, Seite) | Menge | Masse je [kg] | Masse ges. [kg] | Masse-Quelle | Preis | Preis-Status | Art | Generator | Stufe | Akten | Hinweis an Opus |\n|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n")
        g = r["geometrie"]
        hd = (r["hersteller_typ"] + " (" + "; ".join(f"{x['datei']}, {x['seite']}" for x in r["datenblatt"]) + ")") if r.get("hersteller_typ") else "–"
        pz = r["preis"]; ptxt = (f3(pz["wert"]) + " " + pz["einheit"]) if isinstance(pz["wert"], (int, float)) and pz["einheit"] != "–" else ("0 (entfällt)" if pz["status"] == "entfällt" else "offen")
        md.append(f"| {r['pos']} | {r['bt']} {r['bt_name']} | {r['benennung']} | {hd} | {r['menge_' + V]} | {f3(r['masse_je_kg'])} | {f3(r['masse_ges_kg'])} | {r['masse_quelle']} | {ptxt} | {pz['status']} | {r['art']} | {g['generator'] or '–'} | {g['detailstufe']} | {', '.join(r['akten']) or '–'} | {r.get('hinweis_opus', '')} |\n")
    md.append("\n## Masse je Baugruppe\n\n| Baugruppe | Masse [kg] |\n|---|---|\n" + "".join(f"| {k} {BT[k]['name']} | {f3(v)} |\n" for k, v in pr["masse_je_baugruppe_kg"].items()))
    md.append("\n## Dichten (kg/m3) und neue Annahmen\n\n| Werkstoff | Wert | Herkunft |\n|---|---|---|\n" + "".join(f"| {k} | {v['wert']} | {v['herkunft']} |\n" for k, v in o["dichten_kg_m3"].items()))
    md.append(f"\n---\n*{KOPF}. Entwurf, nicht freigegeben. {len(Z)} Positionen. Dokument BAT-DOC-13, Version 0.3.*\n")
    (ROOT / f"docs/13_stueckliste_{V}.md").write_text("".join(md))


def uebersicht(R):
    md = ["| Dok.-Nr. | BAT-DOC-13 | Version | 0.3 | Status | Entwurf |\n|---|---|---|---|---|---|\n| Titel | Stückliste Konstruktionsstand (SL3), Übersicht | Ersteller | Claude Sonnet (KI), pm/bauteile/stueckliste_v3.py | Prüfer | Opus (Stichprobe), Mensch offen |\n\n"
          f"> **KI-generiert.** ({KOPF}.) Entwurf, nicht freigegeben. Ersetzt die grobe Stückliste v0.1 (`stueckliste.py`) in dieser Datei; die Positionen je Variante stehen in `13_stueckliste_LFP.md` und `13_stueckliste_NMC.md`.\n\n"
          "| Größe | " + " | ".join(R) + " |\n|---|" + "---|" * len(R) + "\n"]
    zeilen = [("Positionen gesamt", lambda p: p["positionen_gesamt"]), ("Stufe K", lambda p: p["positionen_je_detailstufe"].get("K", 0)), ("Stufe F", lambda p: p["positionen_je_detailstufe"].get("F", 0)),
              ("Stufe H", lambda p: p["positionen_je_detailstufe"].get("H", 0)), ("Stufe -", lambda p: p["positionen_je_detailstufe"].get("-", 0)), ("Anteil H [%]", lambda p: p["anteil_H_prozent"]),
              ("Positionen Masse offen", lambda p: p["positionen_masse_offen"]), ("Masse gesamt [kg]", lambda p: f3(p["masse_gesamt_kg"])), ("Masse CAD e2d [kg]", lambda p: f3(p["masse_cad_e2d_kg"])),
              ("Abweichung gegen CAD [%]", lambda p: p["abweichung_gegen_cad_prozent"]), ("Zellen", lambda p: p["zellen"]), ("Energie [kWh]", lambda p: p["energie_kWh"])]
    for n, f in zeilen: md.append(f"| {n} | " + " | ".join(str(f(R[v]["pruefsummen"])) for v in R) + " |\n")
    md.append(f"\nQuellen: `pm/bauteile/stueckliste_<V>.json` (Feld `pruefsummen`).\n\n---\n*{KOPF}. Entwurf, nicht freigegeben. Dokument BAT-DOC-13, Version 0.3.*\n")
    (ROOT / "docs/13_stueckliste.md").write_text("".join(md))


def annahmen():
    BL = {V: json.loads((D / f"parameter_{V}_e2d.json").read_text())["A"] for V in ("LFP", "NMC")}
    def einheit(n):
        for suf, e in (("_kg_m3", "kg/m3"), ("_kg_m", "kg/m"), ("_mm", "mm"), ("_kg", "kg")):
            if n.endswith(suf): return e
        return "-"
    out = {"_kopf": KOPF + ". Alle Einträge der A-Blöcke von cad/pack/entwurf/parameter_<V>_e2d.json, LFP und NMC zusammengeführt."}
    for n in sorted(set(BL["LFP"]) | set(BL["NMC"]), key=lambda k: list(BL["LFP"]).index(k) if k in BL["LFP"] else 9999):
        vs = [v for v in BL if n in BL[v]]; ws = {v: BL[v][n]["wert"] for v in vs}; hs = {v: BL[v][n]["herkunft"] for v in vs}
        gleich = len({json.dumps(w) for w in ws.values()}) == 1
        out[n] = dict(wert=ws[vs[0]] if gleich else ws, einheit=einheit(n), herkunft=hs[vs[0]] if len({*hs.values()}) == 1 else hs, varianten=vs)
    (ROOT / "cad/baukasten/annahmen.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
    return len(out) - 1, [n for n, x in out.items() if n != "_kopf" and isinstance(x["wert"], dict) and set(x["wert"]) == {"LFP", "NMC"} and x["wert"]["LFP"] != x["wert"]["NMC"]]


if __name__ == "__main__":
    Vs = [sys.argv[sys.argv.index("--variante") + 1]] if "--variante" in sys.argv else ["LFP", "NMC"]
    R = {}
    for V in Vs:
        R[V] = bauen(V, "--aus-cad" in sys.argv); doku(V, R[V]); p = R[V]["pruefsummen"]
        print(V, p["positionen_gesamt"], "Positionen", p["positionen_je_detailstufe"], f"{p['masse_gesamt_kg']:.2f} kg (CAD {p['masse_cad_e2d_kg']:.2f}, {p['abweichung_gegen_cad_prozent']:+.2f} %)", p["erwartung_cad_baukasten_ERWARTUNG_md"])
    if len(Vs) == 2:
        uebersicht(R); n, diff = annahmen(); print("annahmen.json:", n, "Einträge, unterschiedliche Werte je Variante:", diff)
