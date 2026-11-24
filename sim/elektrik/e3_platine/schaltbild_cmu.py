#!/usr/bin/env python3
"""Blockbild der CMU aus cmu_<V>_teile.json (Zahlen von dort). KI-generiert (Claude Sonnet, 2026-11-24), Entwurf."""
import json, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
H = "/home/cae/hermes/batterie/sim/elektrik/e3_platine"; d = json.load(open(f"{H}/cmu_LFP_teile.json")); n = json.load(open(f"{H}/cmu_NMC_teile.json"))
cnt = lambda t, k: sum(1 for x in t["teile"] if x["name"] == k)
fig, ax = plt.subplots(figsize=(12, 6)); ax.set_xlim(0, 12); ax.set_ylim(0, 6); ax.axis("off")
def box(x, y, w, h, txt, c="#dfe9f5"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05", fc=c, ec="k")); ax.text(x + w / 2, y + h / 2, txt, ha="center", va="center", fontsize=9)
def pf(x1, y1, x2, y2): ax.annotate("", (x2, y2), (x1, y1), arrowprops=dict(arrowstyle="->"))
box(0.2, 2.4, 1.8, 1.2, f"FPC 24-polig\n19 Zellabgriffe T0..T18\n+ Abschaltleitung", "#f3e6c8")
box(2.6, 2.4, 2.2, 1.2, f"Filter je Abgriff\n19 x R + 18 x C\n(100 Ohm / 100 nF)")
box(5.4, 2.0, 2.0, 2.0, "AFE generisch\n18 Kanäle\nASIL-D-fähig (BT-322)", "#cfe8cf")
box(2.6, 4.6, 2.4, 1.0, f"Ausgleich je Kanal\n2 x R parallel + FET\n18 Kanäle: {cnt(d,'NMOS_generisch')} FET, 36 R", "#f5d5d5")
box(5.4, 0.3, 2.0, 1.2, "Sekundärschutz\n(BT-325, eigene\nAbschaltleitung)", "#f5d5d5")
box(8.2, 3.6, 1.8, 1.0, f"{cnt(d,'Uebertrager_generisch')} x Übertrager\n(BT-324)")
box(10.4, 3.6, 1.4, 1.0, f"{cnt(d,'Daisy_Stecker')} x Daisy-\nChain-Stecker", "#f3e6c8")
box(8.2, 1.6, 2.0, 1.0, f"{cnt(d,'NTC_Eingang')} x NTC-Eingang", "#f3e6c8")
for a in [(2.0, 3.0, 2.6, 3.0), (4.8, 3.0, 5.4, 3.0), (3.8, 4.6, 3.8, 3.6), (6.4, 1.5, 6.4, 2.0), (7.4, 3.3, 8.2, 4.0), (10.0, 4.1, 10.4, 4.1), (8.2, 2.1, 7.4, 2.5)]: pf(*a)
ax.text(6, 0.0, f"Teile je CMU (Netzliste): LFP {len(d['teile'])}, NMC {len(n['teile'])}; Widerstände Ausgleich LFP 2 x 47 Ohm, NMC 2 x 64,9 Ohm", ha="center", fontsize=9)
ax.set_title("E3 CMU-Blockbild (Lesehilfe: Pfeile = Signal- bzw. Messrichtung; kein Zielband, es ist ein Schaltbild)\nKI-generiert (Claude Sonnet, 2026-11-24), Entwurf", fontsize=10)
fig.savefig(f"{H}/schaltbild_cmu.png", dpi=110, bbox_inches="tight")
