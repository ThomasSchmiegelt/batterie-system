#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-18), Entwurf. Auftrag E2 Fortsetzung 5. Ergänzt die vorhandenen cad/pack/entwurf/parameter_<V>.json (werden nicht verändert)
um Block A_e2d_* (Herkunft "ERW-E2 N3" bzw. "abgeleitet") und schreibt cad/pack/entwurf/parameter_<V>_e2d.json. Ändert nichts in pm/.
Abgeleitete Maße (nicht in ERW-E2 N3 genannt) tragen die Herkunft "abgeleitet (Sonnet): ..." und stehen in ERGEBNIS.md unter "Offen"."""
import json
from pathlib import Path
R = Path(__file__).resolve().parents[2]; D = R / "cad/pack/entwurf"
def a(w, h): return {"wert": w, "herkunft": h}
N3 = "ERW-E2 N3"
def ab(t): return "abgeleitet (Sonnet): " + t
E = {
 # ---- Schaltbox innen
 "A_e2d_schuetz_bolzen_n": a(2, N3), "A_e2d_schuetz_bolzen_abstand_mm": a(40, N3), "A_e2d_schuetz_bolzen_d_mm": a(8, N3), "A_e2d_schuetz_bolzen_h_mm": a(15, N3),
 "A_e2d_schuetz_fusslaschen_n": a(2, N3), "A_e2d_schuetz_fusslasche_gewinde_mm": a(5, N3), "A_e2d_schuetz_spulenstecker_mm": a([15, 10, 12], N3),
 "A_e2d_fusslasche_mm": a([20, 9, 2], ab("Laschenbreite 20, Auskragung 9 (< Teilabstand 10), Dicke 2; Bohrung M5 nicht in N3 bemaßt")),
 "A_e2d_schiene_cu_LFP_mm": a([25, 3], N3), "A_e2d_schiene_cu_NMC_mm": a([20, 3], N3), "A_e2d_schiene_bohrung_mm": a(8.5, N3),
 "A_e2d_schiene_biegeradius_innen_faktor_dicke": a(1.0, N3 + ": Biegeradius innen = Dicke"), "A_e2d_schrumpfschlauch_mm": a(0.5, N3),
 "A_e2d_pyro_lasche_gewinde_mm": a(8, N3), "A_e2d_lasche_pyro_schmelz_mm": a([25, 3, 25], ab("Laschen = Querschnitt der Schiene Cu 25 x 3 (LFP) bzw. 20 x 3 (NMC) hat Vorrang; Auskragung 25 ohne Vorgabe")),
 "A_e2d_schmelz_halter_mm": a([40, 40, 95], N3 + ": Schmelzsicherung im Kunststoffhalter"), "A_e2d_schmelz_wand_mm": a(5, ab("Halterwand = (40 - 30) / 2 aus Halter 40 und Sicherung 30")),
 "A_e2d_shunt_steg_mm": a(3, N3 + ": Manganin-Steg 3 mm zwischen Cu-Enden M8"), "A_e2d_shunt_platine_mm": a([80, 40, 1.6], N3), "A_e2d_shunt_stecker_pol": a(4, N3 + " (Stecker 4-polig, Maße fehlen)"),
 "A_e2d_bms_platine_dicke_mm": a(1.6, N3), "A_e2d_bms_abstandsbolzen": a([4, 4, 8], N3 + ": 4 Stück M4, Höhe 8"), "A_e2d_bms_abstandsbolzen_aussen_mm": a(7, ab("Außendurchmesser Sechskant SW7 (Gedächtnis-Normmaß, nicht belegt)")), "A_e2d_bms_abstandsbolzen_einzug_mm": a(5, ab("Lage 5 mm von der Platinenkante, Lage nicht in N3")),
 "A_e2d_bms_stecker_mm": a([30, 15, 12], N3 + ": Stecker 26-polig und 2 x Daisy-Chain 12-polig je 30 x 15 x 12 (Lesart: Maß gilt für alle drei)"),
 "A_e2d_box_flansch_mm": a(12, N3), "A_e2d_box_deckel_mm": a(2, N3), "A_e2d_box_dichtung_mm": a([3, 3], N3), "A_e2d_box_schraube_teilung_mm": a(60, N3 + ": M5 alle 60 mm"), "A_e2d_box_schraube_gewinde_mm": a(5, N3),
 "A_e2d_box_flansch_dicke_mm": a(2, ab("Flanschdicke = Wanddicke A_e2_box_wand_mm 2 mm")), "A_e2d_box_druckausgleich_d_mm": a(20, N3),
 "A_e2d_m5_kopf_mm": a([8.5, 5], ab("Zylinderkopf M5: Ø 8,5 x 5 (Gedächtnis-Normmaß ISO 4762, nicht belegt)")),
 "A_e2d_m4_kopf_mm": a([7, 4], ab("Zylinderkopf M4: Ø 7 x 4 (Gedächtnis-Normmaß ISO 4762, nicht belegt)")),
 "A_e2d_m8_kopf_mm": a([13, 8], ab("Zylinderkopf M8: Ø 13 x 8 (Gedächtnis-Normmaß ISO 4762, nicht belegt)")), "A_e2d_m8_scheibe_mm": a([16, 1.6], ab("Scheibe M8: Ø 16 x 1,6 (Gedächtnis-Normmaß ISO 7089, nicht belegt)")),
 # ---- Kabel
 "A_e2d_kabelschuh_huelse_mm": a(40, N3), "A_e2d_kabelschuh_lasche_mm": a([20, 4], N3 + ": Lasche 20 breit x 4 dick"), "A_e2d_kabelschuh_lasche_laenge_mm": a(20, ab("Palme quadratisch 20 x 20")),
 "A_e2d_kabel_biegeradius_faktor_D": a(5, N3 + ": R >= 5 D"), "A_e2d_kabel_schichten": a(["Leiter", "Isolierung", "Schirm", "Mantel"], N3),
 "A_e2d_kabel_wand_teilung": a(3, ab("Radialwand zwischen Leiter und Außendurchmesser in drei gleiche Teile (Isolierung, Schirm, Mantel); N3 nennt keine Schichtdicken")),
 "A_e2d_clip_mm": a([20, 15, 10], N3), "A_e2d_clip_abstand_mm": a(200, N3),
 "A_e2d_fpc_tab_mm": a([8, 4, 0.2], N3), "A_e2d_ntc_mm": a([3, 2, 1], N3), "A_e2d_ntc_je_cmu": a(4, N3), "A_e2d_fpc_stecker_mm": a([25, 8, 6], N3 + ": 20-polig, an der CMU"),
 "A_e2d_daisy_d_mm": a(4, N3), "A_e2d_daisy_stecker_mm": a([15, 8, 8], N3), "A_e2d_daisy_r_min_mm": a(20, N3),
 # ---- Stecker
 "A_e2d_hv250_flansch_mm": a([90, 70, 8], N3), "A_e2d_hv250_schrauben": a([4, 5], N3 + ": 4 x M5"), "A_e2d_hv250_koerper_mm": a([50, 60], N3 + ": Ø 50 x 60, 90 Grad gewinkelt (liegend)"), "A_e2d_hv250_hebel_mm": a([60, 10, 10], N3),
 "A_e2d_hv250_oring_mm": a([60, 3], ab("O-Ring Mittendurchmesser 60, Schnur 3 (Schnur = Dichtungsmaß 3 aus N3)")),
 "A_e2d_hv40_flansch_mm": a([50, 40, 6], N3), "A_e2d_hv40_schrauben": a([4, 4], N3 + ": 4 x M4"), "A_e2d_nv_flansch_mm": a([50, 30, 5], N3), "A_e2d_nv_schrauben": a([2, 4], N3 + ": 2 x M4"),
 "A_e2d_stecker_schraube_einzug_mm": a(5, ab("Schrauben 5 mm von der Flanschkante")), "A_e2d_stecker_koerper_einzug_mm": a(8, ab("Körper von HV 40 A / NV: Flanschfläche minus 8 mm je Kante (Platz für Schraubenköpfe); Höhe = Hülle aus N1 minus Flansch")),
 "A_e2d_bruecke_mm": a([25, 3, 80], N3), "A_e2d_bruecke_schrauben": a([2, 8], N3 + ": 2 x M8 mit Scheibe"), "A_e2d_hvil_mm": a([15, 10, 8], N3),
 "A_e2d_servicedeckel_mm": a([120, 80, 2], N3), "A_e2d_servicedeckel_schrauben": a([6, 5], N3 + ": 6 x M5 (Senkkopf bündig, Kopfhöhe = Deckeldicke)"), "A_e2d_servicedeckel_dichtung_mm": a([3, 3], N3),
 "A_e2d_servicedeckel_rand_mm": a(12, ab("Rand des Haupt-Deckels um die Serviceöffnung für Dichtung (3) und Senkschrauben; Öffnung im Deckel = 120 x 80 minus 2 x 12")),
 # ---- Verbinder
 "A_e2d_omega_h_mm": a(4, N3 + ": Dehnbogen (Omega) h 4"), "A_e2d_schweiss_mm": a([10, 1, 0.2, 2], N3 + ": 2 Linien 10 x 1, Vertiefung 0,2 je Pol"), "A_e2d_schweiss_abstand_mm": a(5, ab("Abstand der zwei Linien 5 mm (Mitte zu Mitte)")),
 "A_e2d_beruehrschutz_dicke_mm": a(1, N3),
 "A_e2d_lasche_lfp_gewinde_mm": a(8, N3), "A_e2d_lasche_ueberlappung_mm": a(25, N3),
 "A_e2d_fenster": a("letztes Feld (hinten)", ab("Zellverbinder-Details (Omega, Schweißnaht, Berührschutz) nur im hintersten Querträger-Feld voll, sonst vereinfacht; Auftrag AUFTRAG.md Fortsetzung 5 erlaubt das bei zu großer Datei")),
}
for v in ("LFP", "NMC"):
    j = json.load(open(D / f"parameter_{v}.json")); j["A"].update(E)
    j["hinweis"] = "ENTWURF, nicht freigegeben. KI-generiert, cad/pack/entwurf_parameter_e2d.py; Basis parameter_%s.json (unverändert) + Block A_e2d_* (E2 Fortsetzung 5)." % v
    out = D / f"parameter_{v}_e2d.json"; out.write_text(json.dumps(j, indent=1, ensure_ascii=False)); print(out.relative_to(R), len(j["A"]))
