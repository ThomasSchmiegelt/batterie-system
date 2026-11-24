#!/usr/bin/env python3
"""Bild i(t) der Schützspule (E3c N1). Zahlen aus ergebnis_schuetz.json. KI-generiert (Claude Sonnet, 2026-11-24), Entwurf."""
import json, pathlib, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
H = pathlib.Path(__file__).resolve().parent; r = json.load(open(H / "ergebnis_schuetz.json")); a = r["annahmen"]; z = r["zener_halten"]
fig, ax = plt.subplots(1, 3, figsize=(17, 6.3)); fig.subplots_adjust(top=0.80, bottom=0.30, wspace=0.28)
v = r["verlauf_zener_halten"]; ax[0].plot([1e3 * x for x in v["t_s"]], v["i_A"], color="C0"); ax[0].set_title("a) Anzug, Halten (PWM), Öffnen (Zener-Löschung)", fontsize=10)
ax[0].axhspan(0.9 * a["I_Halt_soll_A"], 1.1 * a["I_Halt_soll_A"], color="green", alpha=0.25, label="Zielband Halten 0,45 A ± 10 %"); ax[0].axhline(a["I_Abfall_A"], color="r", ls="--", label="Abfallstrom 0,225 A")
ax[0].axvline(100, color="0.5", ls=":"); ax[0].axvline(200, color="0.5", ls=":"); ax[0].set_xlabel("Zeit in ms"); ax[0].set_ylabel("Spulenstrom in A"); ax[0].legend(fontsize=7.5, loc="center right")
p = r["pwm_zoom"]; ax[1].plot(p["t_ms"], p["i_A"], color="C0"); ax[1].axhspan(0.9 * a["I_Halt_soll_A"], 1.1 * a["I_Halt_soll_A"], color="green", alpha=0.25, label="Zielband 0,45 A ± 10 %")
ax[1].set_title(f"b) Halten, 2,5 ms Ausschnitt (20 kHz): Mittel {z['i_halt_mittel_A']:.3f} A, Welligkeit {100 * z['welligkeit_pp_rel']:.2f} % (Ziel < 10 %)", fontsize=9); ax[1].set_xlabel("Zeit in ms"); ax[1].set_ylabel("Spulenstrom in A"); ax[1].legend(fontsize=8); ax[1].set_ylim(0.3, 0.6)
for nm, c, lb in (("zener_halten", "C0", "Zener, aus Halten"), ("zener_anzug", "C2", "Zener, aus Anzug"), ("freilauf_halten", "C1", "nur Freilauf, aus Halten"), ("freilauf_anzug", "C3", "nur Freilauf, aus Anzug")):
    ax[2].plot(r[nm]["zoom_t_ms"], r[nm]["zoom_i_A"], color=c, label=f"{lb}: {r[nm]['t_fall_bis_0_15_ms']:.2f} ms")
ax[2].axhline(a["I_Abfall_A"], color="r", ls="--", label="Abfallstrom 0,225 A"); ax[2].axvspan(2, 4, color="C0", alpha=0.15, label="Erwartung Zener 2–4 ms"); ax[2].axvspan(30, 40, color="C1", alpha=0.15, label="Erwartung nur Freilauf 30–40 ms")
ax[2].axvline(10, color="k", ls=":", label="Abbruchgrenze 10 ms (Zener)"); ax[2].set_xscale("symlog", linthresh=1); ax[2].set_xlim(-1.5, 50); ax[2].set_xlabel("Zeit ab Öffnen in ms (symlog)"); ax[2].set_ylabel("Spulenstrom in A"); ax[2].legend(fontsize=6.8); ax[2].set_title("c) Öffnen: Abfall bis 0,15 x I_Anzug", fontsize=10)
for x in ax: x.grid(alpha=0.3)
fig.text(0.5, 0.955, "E3c N1 (OPT-006): Schützspule 12 V, 8 Ω, 50 mH, Sparschaltung (SPICE) mit Zielbändern", ha="center", fontsize=12, fontweight="bold")
fig.text(0.5, 0.90, "Annahmen ERW-E3c N1: Anzug 1,5 A über 100 ms, Halten 0,3 x I_Anzug per PWM 20 kHz (Tastverhältnis auf Mittelwert nachgeregelt), Abfallstrom 0,15 x I_Anzug, Zener 36 V. Diodenmodell generisch.", ha="center", fontsize=8.5)
fig.text(0.5, 0.135, "Lesehilfe: Bild a zeigt den ganzen Ablauf: der Strom steigt in 100 ms auf 1,5 A, wird dann per Takten auf rund 0,45 A (grünes Band) gehalten und bei 200 ms durch Öffnen beider Schalter beendet. Bild b vergrößert das Halten: die Welligkeit ist winzig, weil die Spule glättet.\n"
         "Bild c zeigt das Öffnen: Die Zener-Löschung (blau, grün) baut den Strom in wenigen Millisekunden ab; ohne Zener (orange, rot), nur über die Freilaufdioden, dauert es länger. Gestrichelt: Abfallstrom. Je kürzer die Kurve bis dahin, desto schneller fällt das Schütz ab.\n"
         "Zielbänder: grün = Halten 0,45 A ± 10 % (Erwartung N1 1), blau/orange getönt = erwartete Abfallzeit (N1 2). Gemessene Werte stehen in der Legende (ergebnis_schuetz.json).", ha="center", fontsize=8, va="center")
fig.text(0.5, 0.02, "KI-generiert (Claude Sonnet, 2026-11-24), Entwurf. Quelle: sim/elektrik/e3c_bms_platine/ergebnis_schuetz.json (ngspice 42).", ha="center", fontsize=8)
fig.savefig(H / "spice_schuetz.png", dpi=110)
