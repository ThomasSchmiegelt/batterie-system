#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-23), Entwurf. Bilder K5 (Nachtrag 1) aus ergebnis_verteiler.json: verteilung.png, dp_durchfluss.png. Zahlen im Titel aus der Datei."""
import json, os
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
H = os.path.dirname(os.path.abspath(__file__)); r = json.load(open(f"{H}/ergebnis_verteiler.json")); G = r["gruppen"]["faelle"]; SW = r["gruppen"]["sweep"]
FUSS = "KI-generiert (Claude Sonnet), Entwurf, nicht freigegeben. 1D-Netz, Annahmen ERWARTUNG K5 Nachtrag 1; Quelle ergebnis_verteiler.json."
fig, ax = plt.subplots(1, 3, figsize=(14, 5), sharey=True)
for a, k in zip(ax, (2, 4, 8)):
    a.axhspan(0.9, 1.1, color="green", alpha=0.2, label="Zielband +-10 %")
    for d, c in ((20, "tab:red"), (25, "tab:blue")):
        v = G[f"k{k}_d{d}_x3"]; a.plot(range(1, k+1), v["anteil"], "-o", c=c, label=f"Rohr {d} mm: max. Abw. {v['max_abw_pct']:.1f} %, dp {v['dp_bar']:.3f} bar")
    a.set_yscale("log"); a.set_title(f"k = {k} Gruppen ({8//k} Bahnen je Gruppe), Durchfluss x3", fontsize=9); a.set_xlabel("Gruppe (1 = Eintrittsseite)"); a.legend(fontsize=7); a.grid(alpha=0.3)
ax[0].set_ylabel("Durchfluss je Gruppe / Mittelwert [-]")
fig.suptitle(f"K5 gruppierte Parallelfuehrung: Verteilung je Gruppe; bestes: {r['gruppen']['bestes']}", fontsize=11)
fig.text(0.01, 0.005, "Lesehilfe: 1 = Gruppe bekommt genau ihren Anteil. Im gruenen Band ist die Verteilung gut. Nur k = 2 liegt ganz im Band; bei k = 8 bleiben Gruppen fast leer.", fontsize=7)
fig.text(0.01, 0.04, FUSS, fontsize=7); fig.tight_layout(rect=(0, 0.07, 1, 0.95)); fig.savefig(f"{H}/verteilung.png", dpi=110)
fig, a = plt.subplots(figsize=(9, 5.5))
mae = r["sweep"]["maeander"]; a.plot(r["sweep"]["fak"], mae, "k-o", label="Maeander (K2b, 8 Bahnen)")
for k, c in ((2, "tab:red"), (4, "tab:orange"), (8, "tab:purple")):
    a.plot(SW["fak"], SW[f"k{k}_d25"], "-s", c=c, label=f"k = {k}, Rohr 25 mm"); a.plot(SW["fak"], SW[f"k{k}_d20"], "--", c=c, label=f"k = {k}, Rohr 20 mm")
a.axhline(0.22, color="g", ls="--", label="Grenze 0,22 bar (K2b Maeander x1)"); a.axvline(3, color="gray", ls=":")
a.set_xlabel("Durchfluss, Vielfaches von K2b (11,5 L/min je Platte = x1)"); a.set_ylabel("Druckverlust je Platte [bar]")
a.set_title(f"K5 Druckverlust x3: Maeander {mae[SW['fak'].index(3.0)]:.2f} bar, k=2 {G['k2_d25_x3']['dp_bar']:.2f}, k=4 {G['k4_d25_x3']['dp_bar']:.2f}, k=8 {G['k8_d25_x3']['dp_bar']:.3f} (Rohr 25)", fontsize=9); a.legend(fontsize=7); a.grid(alpha=0.3)
fig.text(0.01, 0.045, "Lesehilfe: Je tiefer die Kurve, desto weniger Pumpendruck. Unter der gruenen Linie ist der Druck kleiner als beim freigegebenen Maeander im Normalbetrieb.", fontsize=7)
fig.text(0.01, 0.01, FUSS, fontsize=7); fig.tight_layout(rect=(0, 0.07, 1, 1)); fig.savefig(f"{H}/dp_durchfluss.png", dpi=110)
