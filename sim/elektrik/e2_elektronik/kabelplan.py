# KI-generiert (Claude Sonnet, 2026-11-18), Entwurf. Auftrag E2 Fortsetzung 2. Draufsicht Kabelplan (matplotlib) und Tabelle von/nach/Länge/Querschnitt.
# Zahlen nur aus cad/pack/entwurf/ergebnis_<V>_e2.json (erzeugt von cad/pack/pack.py PACK_E2=1).  Aufruf: python3 kabelplan.py
import json, os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
R = "/home/cae/hermes/batterie"; D = os.path.dirname(os.path.abspath(__file__)); QS = {"LFP": 50, "NMC": 35}   # Querschnitt aus ENT-100/101 (parameter_<V>.json BT-430)
tab = []
for V in ("LFP", "NMC"):
    r = json.load(open(f"{R}/cad/pack/entwurf/ergebnis_{V}_e2.json")); e = r["e2"]; g = e["geometrie"]; Lg, B = r["gehaeuse_L_mm"], r["breite_mm"]; A = r["annahmen"]
    P = json.load(open(f"{R}/cad/pack/entwurf/parameter_{V}.json"))["parameter"]; qs = P["BT-430"]["querschnitt_mm2"]["wert"]; fwb = P["BT-360"]["breite_mm"]["wert"]; fwe = P["BT-360"]["breite_mm"]["entscheidung"]
    fig, ax = plt.subplots(figsize=(17, 12.5)); ax.set_aspect("equal"); ax.set_xlim(-60, Lg + 60); ax.set_ylim(-60, B + 60)
    ax.add_patch(Rectangle((0, 0), Lg, B, fc="#eeeeee", ec="#555", lw=1.5))
    for xq in r["quertraeger_x_mm"]: ax.add_patch(Rectangle((xq, 30), 26, B - 60, fc="#d8c8b0", ec="#a08060", lw=0.6))
    # Zellen: grob als Hintergrund (nur Gehäuseinnenraum)
    ax.add_patch(Rectangle((30, 30), Lg - 60, B - 60, fc="#f7f7f7", ec="#999", lw=0.8))
    if e["verschaltung"]["variante"] == "NMC":
        for t in g["taps"]: ax.plot(t[0], t[1], ".", color="#9ab", ms=1.5)
    bx, by, bz = e["schaltbox_x0_y0_z0_mm"]; ax.add_patch(Rectangle((bx, by), e["schaltbox_L_mm"], e["schaltbox_B_mm"], fc="#a8e6bd", ec="#1a7a3a", lw=1.5, alpha=0.85)); ax.text(bx + e["schaltbox_L_mm"] / 2, by + e["schaltbox_B_mm"] / 2, f"Schaltbox\n{e['schaltbox_L_mm']:.0f} x {e['schaltbox_B_mm']:.0f} x {e['schaltbox_H_mm']:.0f} mm", ha="center", va="center", fontsize=11)
    for c in g["cmu"]:
        x0 = c["x"] - 5; ax.add_patch(Rectangle((x0, c["y"] - 60), 10, 120, fc="#d92020", ec="#600", lw=0.8)); ax.text(c["x"] + (22 if c["seite"] == "vorn" else -22), c["y"], f"CMU {c['i']:02d}", ha="left" if c["seite"] == "vorn" else "right", va="center", fontsize=8, color="#900")
    for f in g["fpc"]:
        ln = [x for x in e["fpc"] if x["cmu"] == f["cmu"] and (("reihe" not in x) or x["reihe"] == f.get("reihe"))][0]
        ok = f.get("platziert", True); xy = f["xy"]; ax.plot([p[0] for p in xy], [p[1] for p in xy], color="#e0a000", ls="-" if ok else "--", lw=2.2 if ok else 1.4, zorder=3)
        for s_ in f.get("stub", []): ax.plot([xy[0][0] if False else s_[0], s_[0]], [xy[-1][1], s_[1]], "-", color="#f2cf70", lw=0.5, zorder=2)
        xm = (xy[0][0] + xy[-1][0]) / 2; ym = xy[-1][1]; ax.text(xm, ym + 8 + 14 * (f["cmu"] % 3), f"FPC {f['cmu']:02d}: {ln['laenge_mm']/1000:.2f} m" + ("" if ok else " (kein Platz)"), fontsize=7.5, color="#7a5800", ha="center")
    for h in g["hv"]:
        xy = h["xy"]
        if len(xy) == 2: ax.plot([xy[0][0], xy[0][0]], [xy[0][1], xy[1][1]], "-", color="#c0009a", lw=4, zorder=4); ax.text(xy[0][0] - 20, (xy[0][1] + xy[1][1]) / 2, f"{h['name']}  {h['laenge_mm']:.0f} mm", color="#c0009a", fontsize=9, ha="right", rotation=90, va="center")
        else: ax.plot(xy[0][0], xy[0][1], "o", color="#c0009a", ms=7, zorder=4)
        # Gebiet Trennstecker
    if e["verschaltung"]["variante"] == "LFP":
        st = e["stecker_lfp"]; ax.plot([st["x"], st["x"]], [31, B - 31], "-", color="#7a7a7a", lw=5, alpha=0.8, zorder=3); ax.text(st["x"] + 20, 120, f"Querverbinder (Mitte) {st['querverbinder_laenge_mm']/1000:.2f} m, Al 25x3", fontsize=8, color="#444", rotation=90, va="bottom")
    if e["verschaltung"]["variante"] == "LFP":
        st = e["stecker_lfp"]; bl = st["bruecke_mm"]; ox, oy = st["serviceoeffnung_mm"][1], st["serviceoeffnung_mm"][0]
        ax.add_patch(Rectangle((st["oeffnung_x0_mm"], st["y"] - oy / 2), ox, oy, fc="none", ec="#036", ls="--", lw=1.5, zorder=5)); ax.add_patch(Rectangle((st["x"] - 12.5, st["y"] - bl[2] / 2), bl[0], bl[2], fc="#6aa8ff", ec="#036", zorder=6))
        ax.text(st["x"] + 70, st["y"], f"Service-Trennbrücke (Cu {bl[0]:.0f} x {bl[1]:.0f}, 2 x M8)\nunter Servicedeckel {oy:.0f} x {ox:.0f} mm, 0 mm über Deckel\n(ENT-150, Höhe vorn {e['hoehe_vorn_mm']:.0f} mm)", fontsize=8, ha="left", va="center")
    else:
        mm = [h for h in g["hv"] if h["name"].startswith("Mitte")]; px = mm[0]["xy"][0][0]; py = sum(h["xy"][0][1] for h in mm) / 2
        pl = A["A_e2_trennstecker_mm"]["wert"]; ax.add_patch(Rectangle((px - pl[0] / 2, py - pl[1] / 2), pl[0], pl[1], fc="#6aa8ff", ec="#036", zorder=5)); ax.text(px - 60, py, "Service-\nTrennstecker", fontsize=8, ha="right", va="center")
    ax.set_xlabel("x in mm (0 = vorn, Lg = hinten)"); ax.set_ylabel("y in mm")
    n_f = e["fpc_nicht_platziert"]
    ttl = f"Kabelplan {V} (Draufsicht): Messleitungen (FPC) {e['fpc_laenge_gesamt_m']:.1f} m" + (f", HV intern {e['hv_laenge_gesamt_m']:.2f} m, Verlust {e['hv_verlust_W']:.1f} W bei Ladestrom" if e["hv_gebaut"] else ", HV intern nicht gebaut")
    fig.text(0.02, 0.965, "KI-generiert · Entwurf", fontsize=15, color="#a01414", fontweight="bold", bbox=dict(fc="#ffecec", ec="#a01414")); fig.text(0.02, 0.93, ttl, fontsize=14)
    sub = f"Gehäuse {Lg:.0f} x {B:.0f} mm; rot = CMU hochkant in den Endzonen; gelb = FPC (Länge je CMU); magenta = HV-Leitung {qs:.0f} mm², Biegeradius ≥ {e['biegeradius_mm']:.0f} mm; grün = Schaltbox hinten unter der Rücksitzbank; blau = Service-Trennbrücke (LFP) bzw. -Trennstecker (NMC); grau = Querverbinder Mitte (LFP)"
    if n_f: sub += f"; gestrichelt = {n_f} FPC-Stücke ohne Platz im Seitenspalt (Länge trotzdem gezählt)"
    import textwrap; ax.text(0, B + 75, "\n".join(textwrap.wrap(sub, 150)), fontsize=9.5, color="#333", va="bottom")
    ax.text(0, -52, f"KI-generiert (Claude Sonnet, 2026-11-18), Entwurf, nicht freigegeben. Quelle: cad/pack/entwurf/ergebnis_{V}_e2.json (e2.fpc, e2.hv, e2.geometrie). Lesehilfe: lesehilfe.md", fontsize=8.5, color="#555")
    fig.subplots_adjust(top=0.88); fig.savefig(f"{D}/kabelplan_{V}.png", dpi=110); plt.close(fig)
    # Tabelle
    rows = []
    if True:
        for h in e["hv"]: rows.append((V, h["strecke"].split(" ->")[0].replace(" Zelle", ""), h["strecke"].split("-> ")[1], f"{h['laenge_mm']:.0f}", f"{qs:.0f} mm² Cu"))
        rows.append((V, "Schaltbox", "HV-Stecker 250 A (2 Leitungen)", f"{e['hv_kurze_leitungen_box_stecker_mm']:.0f} (gesamt)", f"{qs:.0f} mm² Cu"))
    if V == "LFP": rows.append((V, "Querverbinder Mitte (vorn, 2 Hälften)", "Zellen vorn / Trennbrücke (Lücke 30 mm)", f"{e['stecker_lfp']['querverbinder_laenge_mm']:.0f}", "Al 25 x 3 mm (wie Zellverbinder G4)"))
    for x in e["fpc"]:
        nm = f"CMU {x['cmu']:02d}" + (f" Reihe {x['reihe']}" if "reihe" in x else ""); tp = "Zellverbinder-Abgriffe " + ("(Reihe %d, Seitenspalt)" % x["reihe"] if "reihe" in x else "(Verbinderebene unter Pad)")
        rows.append((V, nm, tp + ("" if x["platziert"] else ", kein Platz"), f"{x['laenge_mm']:.0f}", f"FPC {fwb:.0f} mm breit ({fwe})"))
    tab += rows
with open(f"{D}/kabelplan_tabelle.md", "w") as f:
    f.write("| Variante | von | nach | Länge mm | Querschnitt / Art |\n|---|---|---|---|---|\n")
    for r_ in tab: f.write("| " + " | ".join(r_) + " |\n")
print("OK", len(tab))
