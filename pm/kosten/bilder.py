"""bilder.py -- Bilder zu KO1 aus pm/kosten/ergebnis_<V>.json (KI-generiert, Claude Sonnet, 2026-11-18, Entwurf). Zahlen nur aus den Ergebnisdateien."""
import json
from pathlib import Path
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
R = Path(__file__).resolve().parents[2] / "pm/kosten"
EIN = json.loads((R / "eingaben.json").read_text()); D = {v: json.loads((R / f"ergebnis_{v}.json").read_text()) for v in ("LFP", "NMC")}
NAMEN = {"BT-100": "Zelle", "BT-200": "Zellverbund", "BT-300": "BMS/Sensorik", "BT-400": "Verbinder/Leitung", "BT-500": "Gehäuse/Struktur", "BT-600": "Kühlung", "BT-700": "Schaltbox/Stecker", "Fertigung": "Fertigung (10 % Nicht-Zell + 50 €)"}
FARBE = ["#4C72B0", "#55A868", "#C44E52", "#8172B2", "#CCB974", "#64B5CD", "#8C8C8C", "#DD8452"]
def teile(d):
    t = {k: d["je_baugruppe"][k]["eur_je_kWh"] for k in NAMEN if k in d["je_baugruppe"]}; t["Fertigung"] = d["fertigung"]["eur_je_kWh"]; return t
def zeichne(ax, vs):
    for i, v in enumerate(vs):
        b = 0
        for (k, w), c in zip(teile(D[v]).items(), FARBE):
            ax.bar(i, w, 0.5, bottom=b, color=c, label=NAMEN[k] if i == 0 else None, edgecolor="white", linewidth=0.5)
            if w > 4: ax.text(i, b + w / 2, f"{w:.1f}", ha="center", va="center", fontsize=8, color="white")
            b += w
        lo, hi = EIN["zielband"][v]["eur_kwh"]
        ax.fill_between([i - 0.35, i + 0.35], lo, hi, color="none", edgecolor="black", hatch="//", linewidth=1, label="Zielband (ERW-KO1, Schätzung)" if i == 0 else None)
        ax.text(i, max(b, hi) + 2, f"Teilsumme {b:.1f} €/kWh\n{D[v]['summe_eur_pack']:.0f} €/Pack, {D[v]['positionen_offen_gesamt']} Pos. offen", ha="center", fontsize=8)
    ax.axhline(EIN["beleg_packpreis"]["eur_je_kWh_berechnet"], color="red", ls="--", label=f"Beleg W29 (Status: verifiziert, Zitat geprüft): 97 USD/kWh = {EIN['beleg_packpreis']['eur_je_kWh_berechnet']:.1f} €/kWh")
    ax.set_xticks(range(len(vs))); ax.set_xticklabels(vs); ax.set_ylabel("€ je kWh Pack (Herstellkosten, Annahmen)"); ax.set_ylim(0, 165 if len(vs) > 1 else 210)
fuss = "Lesehilfe: Jeder Balken ist ein Pack mit rund 74 kWh. Die Farbstücke zeigen, wohin das Geld geht; der schwarze Rahmen ist der erwartete Bereich, rot gestrichelt der veröffentlichte Marktpreis.\nSumme ist eine Untergrenze: offene Stücklistenpositionen sind nicht mitgezählt. Status aller Balken: Schätzung (Annahme Opus, ERW-KO1), nur die rote Linie ist verifiziert (W29, Zitat geprüft). KI-generiert, Entwurf."
for v in ("LFP", "NMC", "vergleich"):
    vs = ["LFP", "NMC"] if v == "vergleich" else [v]
    fig, ax = plt.subplots(figsize=(8 if v == "vergleich" else 5.5, 6.5)); zeichne(ax, vs)
    ax.set_title("Herstellkosten Pack: Vergleich LFP / NMC" if v == "vergleich" else f"Herstellkosten Pack {v}", fontsize=11)
    ax.legend(fontsize=7, loc="upper left", ncol=1 if v != "vergleich" else 2)
    import textwrap; fig.text(0.01, 0.005, "\n".join(textwrap.fill(x, 105 if v == "vergleich" else 75) for x in fuss.split("\n")), fontsize=6.5, va="bottom"); fig.tight_layout(rect=(0, 0.16, 1, 1))
    fig.savefig(R / ("kosten_vergleich.png" if v == "vergleich" else f"kosten_{v}.png"), dpi=130); plt.close(fig)
