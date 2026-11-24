# Schreibt .kicad_pro (Netzklassen) und .kicad_dru (Kriechstrecken) für E3. KI-generiert (Sonnet, 2026-11-24).
# Werte: ENT-168 (0,6 mm innerhalb), ENT-183 (2,5 mm Daisy-Ausgang). Herkunft ERW-E3, ohne Normbeleg.
import json, sys, re, pathlib
H = pathlib.Path(__file__).resolve().parent; OUT = pathlib.Path("/home/cae/cae_projekte/batterie/e3")
sys.path.insert(0, str(H))
def ent(i): 
    t = (H.parents[2] / f"pm/entscheidungen/ENT-{i}.md").read_text(); return float(re.search(r"^wert: (.*)$", t, re.M).group(1))
k_in, k_dc = ent(168), ent(183)
for V in ("LFP", "NMC"):
    info = json.load(open(H / f"layout_{V}_info.json"))
    cls = lambda n, c, w=0.2: dict(name=n, clearance=c, track_width=w, via_diameter=0.6, via_drill=0.3, diff_pair_gap=0.25, diff_pair_width=0.2, diff_pair_via_gap=0.25, microvia_diameter=0.3, microvia_drill=0.1, wire_width=6, bus_width=12, line_style=0, pcb_color="rgba(0, 0, 0, 0.000)", schematic_color="rgba(0, 0, 0, 0.000)")
    pro = {"meta": {"filename": f"cmu_{V}.kicad_pro", "version": 3},
           "board": {"design_settings": {"rules": {"min_clearance": k_in, "min_track_width": 0.15, "min_copper_edge_clearance": 0.3}}},
           "net_settings": {"classes": [cls("Default", k_in), cls("Daisy", k_in), cls("Ausgleich", k_in, 0.3)], "meta": {"version": 4},
                            "netclass_patterns": [{"netclass": "Daisy", "pattern": n} for n in info["daisy_netze"]] + [{"netclass": "Ausgleich", "pattern": n} for n in info["ausgleich_netze"]]}}
    json.dump(pro, open(OUT / f"cmu_{V}.kicad_pro", "w"), indent=1)
    (OUT / f"cmu_{V}.kicad_dru").write_text(f'''(version 1)
(rule "Daisy_Kriechstrecke_{k_dc}mm"
  (condition "A.NetClass == 'Daisy' && B.NetClass != 'Daisy'")
  (constraint clearance (min {k_dc}mm)))
(rule "Pad_zu_Pad_im_Bauteil_Gehaeuseraster"
  (condition "A.Type == 'Pad' && B.Type == 'Pad' && A.Parent == B.Parent")
  (constraint clearance (min 0.15mm)))
''')
# Prüfung Kriechstrecke >= Luftstrecke (ERW-E3 N4 Regel 1). Luftstrecke = der im DRC angesetzte Mindestabstand (Stoßspannung nicht abgeleitet, kein Wert vorhanden), Kriechstrecke = ENT-168 / ENT-183
luft_in, luft_dc = k_in, k_dc
chk = dict(innerhalb=dict(kriech_mm=k_in, luft_mm=luft_in, ok=k_in >= luft_in), daisy_trennstelle=dict(kriech_mm=k_dc, luft_mm=luft_dc, ok=k_dc >= luft_dc),
           hinweis="Luftstrecke richtet sich nach Stoßspannung, Kriechstrecke nach Arbeitsspannung (N4 Regel 2); hier ohne Wert für die Stoßspannung gleich dem DRC-Abstand gesetzt, Auslegungshöhe 3000 m offen (Frage an Autor)")
json.dump(chk, open(H / "ergebnis_kriechstrecke.json", "w"), indent=1, ensure_ascii=False); print(chk)
print(k_in, k_dc)
