# KI-generiert (Claude Sonnet, 2026-11-18), Entwurf. Auftrag E2 Fortsetzung. Blockschaltbild HV/NV je Variante (matplotlib).
# Werte aus cad/pack/entwurf/parameter_<V>.json (Akten ENT-110ff, vorgeschlagen). Reihenfolge der Bauteile im HV-Pfad ist eine Darstellung, keine Auslegung.
import json, sys, os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
E1 = json.load(open(f"{R}/sim/elektrik/e2_elektronik/eingaben.json"))
def bild(v):
    P = json.load(open(f"{R}/cad/pack/entwurf/parameter_{v}.json"))["parameter"]
    g = lambda b, m: P[b][m]["wert"]; ent = lambda b, m: P[b][m]["entscheidung"]
    s, p = E1[v]["s"], E1[v]["p"]
    ER = json.load(open(f"{R}/cad/pack/entwurf/ergebnis_{v}_e2.json"))["e2"]; vs = ER["verschaltung"]
    if v == "LFP":
        t1, t2 = f"Zellstring Hälfte 1 (Reihe 0)\n{vs['zellen_je_reihe']} Zellen, Plus hinten → vorn", f"Zellstring Hälfte 2 (Reihe 1)\n{s - vs['zellen_je_reihe']} Zellen, vorn → Minus hinten"
        t3 = f"Service-\nTrennstecker vorn\n(Deckelöffnung)\n{g('BT-720','nennstrom_A'):.0f} A"
    else:
        t1, t2 = f"Zellstring Hälfte 1 (Band 1+2)\n{vs['gruppen_hälfte_A']} Gruppen à {p} Zellen, Plus hinten", f"Zellstring Hälfte 2 (Band 3+4)\n{vs['gruppen_hälfte_B']} Gruppen à {p} Zellen, Minus hinten"
        t3 = f"Service-\nTrennstecker hinten\n(über den Mittenanschlüssen)\n{g('BT-720','nennstrom_A'):.0f} A"
    fig, ax = plt.subplots(figsize=(16, 9.5)); ax.set_xlim(0, 160); ax.set_ylim(0, 95); ax.axis("off")
    def kasten(x, y, w, h, t, fc="#eef2f7", ec="#333", fs=10):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3", fc=fc, ec=ec, lw=1.4)); ax.text(x + w / 2, y + h / 2, t, ha="center", va="center", fontsize=fs)
    def linie(pts, c="#b00020", lw=2.4, ls="-"):
        ax.plot([q[0] for q in pts], [q[1] for q in pts], color=c, lw=lw, ls=ls, solid_capstyle="round")
    ax.text(2, 92, f"Schaltbild Pack {v} ({s}s{p}p)", fontsize=16, weight="bold")
    ax.text(2, 85.2, f"HV intern {ER['hv_laenge_gesamt_m']:.2f} m (Cu {g('BT-430','querschnitt_mm2'):.0f} mm²), Verlust {ER['hv_verlust_W']:.1f} W bei Ladestrom; Stand v0.4", fontsize=9, color="#444")
    ax.text(2, 88.5, "HV rot, Messkette blau, NV grau. Werte aus Akten (vorgeschlagen, Annahme ERW-E2). HV-Reihenfolge nur Darstellung.", fontsize=10, color="#444")
    ax.add_patch(Rectangle((118, 85), 40, 8, fc="#ffe5e5", ec="#a00", lw=2)); ax.text(138, 89, "KI-generiert · Entwurf", ha="center", va="center", fontsize=14, weight="bold", color="#a00")
    # Zellstring
    kasten(2, 52, 36, 14, t1, "#dbe8ff", fs=8)
    kasten(46, 52, 20, 14, t3, "#fff3c4", fs=7)
    kasten(80, 52, 30, 14, t2, "#dbe8ff", fs=8)
    linie([(38, 59), (46, 59)]); linie([(66, 59), (80, 59)])
    # Schaltbox
    ax.add_patch(Rectangle((2, 4), 114, 40, fc="#fafafa", ec="#555", lw=1.6, ls="--")); ax.text(4, 41, "Schaltbox (hinten, Turm unter der Rücksitzbank, ENT-144)", fontsize=11, weight="bold")
    kasten(5, 24, 22, 9, f"Pyrosicherung +\nSchmelzsicherung {g('BT-713','nennstrom_A'):.0f} A", "#ffd6d6", fs=9)
    kasten(33, 24, 20, 9, f"Hauptschütz +\n{g('BT-711','nennstrom_A'):.0f} A / {g('BT-711','nennspannung_V'):.0f} V", "#ffd6d6", fs=9)
    kasten(33, 10, 20, 9, f"Vorladeschütz +\nR {g('BT-712','widerstand_Ohm'):.0f} Ω, {g('BT-712','vorladezeit_ms'):.0f} ms", "#ffd6d6", fs=9)
    kasten(67, 24, 20, 9, f"Shunt + Hall\n{g('BT-340','messbereich_A'):.0f} A, redundant", "#ffd6d6", fs=9)
    kasten(92, 24, 20, 9, f"Hauptschütz −\n{g('BT-711','nennstrom_A'):.0f} A / {g('BT-711','nennspannung_V'):.0f} V", "#ffd6d6", fs=9)
    ax.text(68, 21.2, "Strom-Signal → BMS", fontsize=8, color="#1560bd")
    # HV+ : Zellstring Hälfte 1 → Sicherung → Hauptschütz + (parallel Vorladung) → HV-Stecker
    linie([(16, 52), (16, 33)]); linie([(27, 28.5), (33, 28.5)]); linie([(27, 28.5), (27, 14.5), (33, 14.5)])
    linie([(53, 14.5), (57, 14.5), (57, 28.5)]); linie([(53, 28.5), (57, 28.5), (57, 38), (130, 38)])
    # HV− : Zellstring Hälfte 2 → Shunt → Hauptschütz − → HV-Stecker
    linie([(95, 52), (95, 46), (77, 46), (77, 33)]); linie([(87, 28.5), (92, 28.5)]); linie([(112, 28.5), (120, 28.5), (120, 31), (130, 31)])
    ax.text(58.5, 39, "HV+", fontsize=9, color="#b00020"); ax.text(124, 39.2, "HV+", fontsize=9, color="#b00020"); ax.text(121, 22.5, "HV−", fontsize=9, color="#b00020")
    # Stecker
    kasten(130, 30, 28, 10, f"HV-Stecker 1: Antrieb/Laden\n{g('BT-730','nennstrom_A'):.0f} A (2 Stecker, 2. 40 A\nNebenverbraucher)", "#ffd6d6", fs=8)
    kasten(130, 12, 28, 10, "Isolationswächter\nWarnung 400 kΩ (500 Ω/V)\nFehler 80 kΩ (100 Ω/V)", "#e6e6e6", fs=8)
    linie([(122, 38), (122, 17), (130, 17)], c="#b00020", lw=1.4, ls=":")
    # Messkette
    kasten(2, 74, 36, 9, f"CMU {g('BT-320','kanaele'):.0f} Kanäle × {g('BT-320','anzahl'):.0f}\n{s + 1} Abgriffe, passiver Ausgleich {g('BT-320','ausgleichsstrom_mA'):.0f} mA", "#d9ecff", fs=9)
    kasten(46, 74, 28, 9, f"FPC-Messleitung {g('BT-360','breite_mm'):.0f} mm\nNTC {g('BT-330','anzahl'):.0f} (4 je CMU)", "#d9ecff", fs=9)
    kasten(82, 74, 26, 9, "BMS-Hauptsteuergerät\n(Daisy-Chain isoliert)", "#d9ecff", fs=9)
    linie([(38, 78.5), (46, 78.5)], c="#1560bd", lw=1.8); linie([(74, 78.5), (82, 78.5)], c="#1560bd", lw=1.8)
    linie([(17, 66), (17, 74)], c="#1560bd", lw=1.8, ls="--"); linie([(95, 66), (95, 74)], c="#1560bd", lw=1.8, ls="--")
    ax.text(18, 69.5, "Spannung je Zelle", fontsize=8, color="#1560bd")
    kasten(112, 66, 46, 8, f"Gas-/Drucksensor (Pack): Druck + H₂/CO₂", "#e6e6e6", fs=9)
    kasten(112, 48, 46, 9, f"NV-Stecker {g('BT-740','polzahl'):.0f}-polig", "#e6e6e6", fs=9)
    linie([(108, 78.5), (135, 78.5), (135, 74)], c="#1560bd", lw=1.2, ls="--"); linie([(135, 66), (135, 57)], c="#555", lw=1.2, ls=":")
    ax.text(2, 1, f"KI-generiert (Claude Sonnet, 2026-11-18), Entwurf, nicht freigegeben. Quellen: cad/pack/entwurf/parameter_{v}.json (Akten ENT-110 bis ENT-149), sim/elektrik/e2_elektronik/eingaben.json.", fontsize=8, color="#555")
    fig.savefig(f"{R}/sim/elektrik/e2_elektronik/schaltbild_{v}.png", dpi=110, bbox_inches="tight"); plt.close(fig)
for v in (sys.argv[1:] or ["LFP", "NMC"]): bild(v)
