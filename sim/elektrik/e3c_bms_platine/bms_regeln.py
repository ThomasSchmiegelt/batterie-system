# Schreibt .kicad_pro (Netzklassen, Severities) und .kicad_dru (HV/NV-Kriechstrecke) für E3c. KI-generiert (Claude Sonnet, 2026-11-24), Entwurf.
# Werte: ERWARTUNG ERW-E3c Teil B (Abstand NV 0,15 mm, HV 0,2 mm wie ENT-168, Kriechstrecke HV/NV ENT-191 = 10 mm, Luftstrecke 8 mm inkl. Höhe 3000 m). Breite der Leistungsnetze = Platzhalter (Strom nicht bekannt).
import json, sys, re, pathlib
H = pathlib.Path(__file__).resolve().parent; OUT = pathlib.Path("/home/cae/cae_projekte/batterie/e3c")
def ent(i): return float(re.search(r"^wert: ([^\s#]+)", (H.parents[2] / f"pm/entscheidungen/ENT-{i}.md").read_text(), re.M).group(1))
PJ = json.load(open(H.parents[2] / "pm/bauteile/parameter.json"))["parameter"]["BT-311"]   # E3c N1: ENT-191/195/196 aus parameter.json
k_hv, k_hvnv = ent(168), PJ["kriechstrecke_hv_nv_mm"]["wert"]       # 0,2 mm HV-Bereich (ENT-168); 10 mm (ENT-191)
k_nv, luft = PJ["abstand_nv_mm"]["wert"], PJ["luftstrecke_hv_nv_mm"]["wert"]   # ENT-196 (0,15 mm NV), ENT-195 (8 mm)
LP = 0.4                                # Platzhalter Leiterbahnbreite Leistungsnetze (Haltestrom BT-715 nicht festgelegt)
info = json.load(open(H / "layout_info.json")); teile = json.load(open(H / "bms_teile.json"))["teile"]
netze = {n for t in teile for n in t["pins"].values() if n}
leist = sorted(n for n in netze if n in ("VBAT_IN", "VBAT", "VBAT_F") or n.endswith(("_SPULE_P", "_SPULE_N", "_ZENER")))
cls = lambda n, c, w=0.2: dict(name=n, clearance=c, track_width=w, via_diameter=0.6, via_drill=0.3, diff_pair_gap=0.25, diff_pair_width=0.2, diff_pair_via_gap=0.25, microvia_diameter=0.3, microvia_drill=0.1, wire_width=6, bus_width=12, line_style=0, pcb_color="rgba(0, 0, 0, 0.000)", schematic_color="rgba(0, 0, 0, 0.000)")
pro = {"meta": {"filename": "bms.kicad_pro", "version": 3},
       "board": {"design_settings": {"rules": {"min_clearance": k_nv, "min_track_width": 0.15, "min_copper_edge_clearance": 0.3},
                 "rule_severities": {"silk_over_copper": "ignore", "silk_overlap": "ignore", "lib_footprint_issues": "ignore", "lib_footprint_mismatch": "ignore"}}},
       "net_settings": {"classes": [cls("Default", k_nv), cls("HV", k_hv), cls("Leistung", k_nv, LP)], "meta": {"version": 4},
                        "netclass_patterns": [{"netclass": "HV", "pattern": n} for n in info["hv_netze"]] + [{"netclass": "Leistung", "pattern": n} for n in leist]}}
json.dump(pro, open(OUT / "bms.kicad_pro", "w"), indent=1)
(OUT / "bms.kicad_dru").write_text(f'''(version 1)
(rule "HV_NV_Kriechstrecke_{k_hvnv:g}mm"
  (condition "A.NetClass == 'HV' && B.NetClass != 'HV'")
  (constraint clearance (min {k_hvnv}mm)))
(rule "Pad_zu_Pad_im_Bauteil_Gehaeuseraster"
  (condition "A.Type == 'Pad' && B.Type == 'Pad' && A.Parent == B.Parent && A.NetClass == B.NetClass")
  (constraint clearance (min 0.15mm)))
''')
chk = dict(hv_nv=dict(kriech_mm=k_hvnv, luft_mm=luft, ok=k_hvnv >= luft), innerhalb_hv=dict(abstand_mm=k_hv), innerhalb_nv=dict(abstand_mm=k_nv), leistungsnetze=leist, leistung_breite_mm_platzhalter=LP,
           hinweis="Luftstrecke 8 mm und Abstand NV 0,15 mm aus ERWARTUNG ERW-E3c (Annahme Opus); Akten ENT-195/ENT-196, Werte aus parameter.json.")
json.dump(chk, open(H / "ergebnis_kriechstrecke.json", "w"), indent=1, ensure_ascii=False); print(chk)
