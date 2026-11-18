#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. Auftrag G4 (cad/pack/AUFTRAG.md).
Wie cad/zelle/entwurf_parameter.py (Akten entschieden + vorgeschlagen), dazu Block "A" mit A_*-Annahmen aus
sim/mechanik/m0_gehaeuse/eingaben.json und AUFTRAG.md. Schreibt cad/pack/entwurf/parameter_<V>.json. Ändert nichts in pm/."""
import sys, json
from pathlib import Path
R = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(R / "pm"))
import pm as P
E = json.load(open(R / "sim/mechanik/m0_gehaeuse/eingaben.json", encoding="utf-8"))
hs = E["hoehenstapel_mm"]; q = E["quertraeger"]
def a(w, h): return {"wert": w, "herkunft": h}
A = {
 "A_deckel_mm": a(hs["deckel"], "M0 eingaben.json hoehenstapel_mm.deckel (Annahme)"),
 "A_boden_mm": a(hs["boden"], "M0 eingaben.json hoehenstapel_mm.boden (Annahme)"),
 "A_unterfahrschutz_mm": a(hs["unterfahrschutz"], "M0 eingaben.json (Annahme)"),
 "A_luft_mm": a(hs["luft"], "M0 eingaben.json (Annahme)"),
 "A_kuehlplatte_mm": a(hs["kuehlplatte_je"], "M0 eingaben.json (Annahme); Vollmaterial, real hohl"),
 "A_pad_mm": a(hs["waermeleitschicht_je"], "M0 eingaben.json waermeleitschicht_je (Annahme)"),
 "A_rand_mm": a(E["rand_mm"]["wert"], "M0 eingaben.json rand_mm (Annahme)"),
 "A_hoehe_max_mm": a(E["hoehe_max_mm"]["wert"], "M0 eingaben.json (Annahme)"),
 "A_quertraeger_anzahl": a(q["anzahl"], "M0 eingaben.json (Annahme Opus)"),
 "A_quertraeger_hoehe_mm": a(q["hoehe_mm"], "M0 eingaben.json (W22, US9045030)"),
 "A_quertraeger_breite_mm": a(q["breite_L_mm"], "M0 eingaben.json (W22, US9045030)"),
 "A_quertraeger_wand_mm": a(q["wand_mm"], "M0 eingaben.json (Annahme, Mitte 2-3 mm)"),
 "A_quertraeger_spiel_mm": a(q["spiel_je_seite_mm"], "M0 eingaben.json (Annahme)"),
 "A_alu_dichte_kg_m3": a(E["alu_dichte_kg_m3"]["wert"], "M0 eingaben.json (Annahme)"),
 "A_zellabstand_LFP_mm": a(E["zellen"]["LFP"]["abstand_mm"], "M0 eingaben.json (G1)"),
 "A_zellabstand_NMC_mm": a(E["zellen"]["NMC"]["abstand_mm"], "M0 eingaben.json (G1)"),
 "A_zellzahl_LFP": a(E["zellen"]["LFP"]["anzahl"], "M0 eingaben.json (G1)"),
 "A_zellzahl_NMC": a(E["zellen"]["NMC"]["anzahl"], "M0 eingaben.json (G1 Fall A)"),
 "A_zellverbinder_LFP_mm": a([25, 3], "AUFTRAG G4: Querschnitt 25 x 3 (Breite x Dicke)"),
 "A_gruppenverbinder_NMC_mm": a([25, 3], "AUFTRAG G4: Querschnitt 25 x 3 (Breite x Dicke)"),
 "A_zellabgriff_NMC_mm": a([12, 1], "AUFTRAG G4: 12 x 1 (Durchmesser x Dicke, Scheibe auf dem Pluspol)"),
 "A_vergusshoehe_anteil_NMC": a(0.5, "AUFTRAG G4: Verguss bis halbe Zellhöhe (Annahme)"),
 "A_KUEHLPLATTE_FUELLGRAD": a(0.4, "Annahme Opus 2026-11-17: 2 Bleche je 1,5 mm + Kanalstege, Füllgrad 0,4 (Masse = Volumen x Füllgrad x Al-Dichte)"),
 "A_seitenrahmen_wand_mm": a(2.5, "Annahme Opus 2026-11-17: Mehrkammerprofil, Wand 2,5 mm (W22-Wandbereich)"),
 "A_seitenrahmen_kammern": a(3, "Annahme Opus 2026-11-17: 3 Kammern über die Rahmenbreite"),
 "A_dichte_pad_kg_m3": a(2500, "Annahme Opus 2026-11-17"), "A_dichte_zelltraeger_kg_m3": a(1200, "Annahme Opus 2026-11-17 (PC)"), "A_dichte_verguss_kg_m3": a(300, "Annahme Opus 2026-11-17 (PU-Schaum)"),
 # ---- E2 (Auftrag E2, Fortsetzung 2026-11-18): Maße ERW-E2 Nachtrag 1 (L x B x H mm, Masse kg), Herkunft "ERW-E2 N1". Was eine Akte hat (BT-310 Platine, BT-430 Biegeradius), kommt aus den Akten ENT-110ff.
 "A_e2_schuetz_mm": a([80, 60, 75], "ERW-E2 N1 Hauptschütz"), "A_e2_schuetz_masse_kg": a(0.45, "ERW-E2 N1"),
 "A_e2_vorladeschuetz_mm": a([40, 30, 40], "ERW-E2 N1 Vorladeschütz"), "A_e2_vorladewiderstand_mm": a([60, 20, 20], "ERW-E2 N1"), "A_e2_vorlade_masse_kg": a(0.15, "ERW-E2 N1 (Schütz + Widerstand zusammen)"),
 "A_e2_pyro_mm": a([30, 30, 80], "ERW-E2 N1 Pyrosicherung Ø30 x 80, als Quader 30 x 30 x 80 (Vereinfachung)"), "A_e2_pyro_masse_kg": a(0.15, "ERW-E2 N1"),
 "A_e2_schmelz_mm": a([30, 30, 85], "ERW-E2 N1"), "A_e2_schmelz_masse_kg": a(0.10, "ERW-E2 N1"),
 "A_e2_shunt_mm": a([80, 40, 15], "ERW-E2 N1 Shunt mit Messplatine"), "A_e2_shunt_masse_kg": a(0.10, "ERW-E2 N1"),
 "A_e2_bms_masse_kg": a(0.4, "ERW-E2 N1 BMS-Platine (Maße aus Akte BT-310)"),
 "A_e2_cmu_mm": a([120, 60, 10], "ERW-E2 N1 CMU-Platine"), "A_e2_cmu_masse_kg": a(0.08, "ERW-E2 N1"),
 "A_e2_fpc_dicke_mm": a(0.3, "ERW-E2 N1"), "A_e2_fpc_masse_kg_m": a(0.05, "ERW-E2 N1"), "A_e2_fpc_halter_mm": a(3.0, "ERW-E2 N1 (FPC plus Halter)"),
 "A_e2_hv250_mm": a([90, 70, 60], "ERW-E2 N1"), "A_e2_hv250_masse_kg": a(0.4, "ERW-E2 N1"), "A_e2_hv40_mm": a([50, 40, 40], "ERW-E2 N1"), "A_e2_hv40_masse_kg": a(0.15, "ERW-E2 N1"),
 "A_e2_nv_mm": a([50, 30, 40], "ERW-E2 N1"), "A_e2_nv_masse_kg": a(0.05, "ERW-E2 N1"),
 "A_e2_trennstecker_mm": a([80, 50, 60], "ERW-E2 N1, oben zugänglich (Deckelöffnung)"), "A_e2_trennstecker_masse_kg": a(0.2, "ERW-E2 N1"),
 "A_e2_gas_mm": a([30, 30, 20], "ERW-E2 N1"), "A_e2_gas_masse_kg": a(0.03, "ERW-E2 N1"),
 "A_e2_hv_aussendurchmesser_LFP_mm": a(14, "ERW-E2 N1"), "A_e2_hv_aussendurchmesser_NMC_mm": a(12, "ERW-E2 N1"),
 "A_e2_box_wand_mm": a(2, "ERW-E2 N1 Schaltbox Al, Wand 2 mm"), "A_e2_box_rand_mm": a(15, "ERW-E2 N1 Rand 15 mm um den Inhalt"), "A_e2_box_hoehe_max_mm": a(90, "ERW-E2 N1 H ≤ 90"),
 "A_e2_box_teilabstand_mm": a(10, "NEUE ANNAHME (Platzhalter, in ERW-E2 N1 nicht gesetzt; Opus entscheiden): Abstand zwischen den Teilen in der Schaltbox"),
 "A_traeger_dicke_NMC_mm": a(2.5, "NEUE ANNAHME (Platzhalter, in M0 nicht gesetzt; Opus entscheiden)"),
}
def ok(e):
    s = str(e.get("status", ""))
    return (s.startswith("entschieden") or s.startswith("vorgeschlagen")) and e.get("merkmal") not in (None, "-")
def main():
    bt = P.struktur(); ers = {e.get("ersetzt") for e in P.alle()}; V = P.varianten()
    akten = [e for e in P.alle() if ok(e) and e["id"] not in ers]
    out_dir = R / "cad/pack/entwurf"; out_dir.mkdir(parents=True, exist_ok=True)
    for v in V:
        out = {b: {m: {"wert": None, "entscheidung": None} for m in d["merkmale"]} for b, d in bt.items()}
        for gruppe in (False, True):
            for e in akten:
                if bool(e.get("variante")) != gruppe: continue
                if gruppe and v not in P.vset(e): continue
                for b in e.get("bauteile") or []:
                    d = {"wert": e.get("wert"), "einheit": e.get("einheit"), "entscheidung": e["id"], "status": e.get("status")}
                    if gruppe: d["variante"] = v
                    out[b][e["merkmal"]] = d
        f = out_dir / f"parameter_{v}.json"
        f.write_text(json.dumps({"hinweis": "ENTWURF, nicht freigegeben. KI-generiert, cad/pack/entwurf_parameter.py; Akten entschieden + vorgeschlagen, Block A = A_*-Annahmen.", "parameter": out, "A": A}, indent=1, ensure_ascii=False))
        print(f.relative_to(R))
main()
