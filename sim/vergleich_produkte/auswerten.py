#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-23), Entwurf. Auswertung QN2 nach sim/vergleich_produkte/ERWARTUNG.md.
Liest: forschung/ergebnis/W43.md + W43.pruefung.txt (nur Zeilen ohne FEHLT), pm/bauteile/stueckliste_{LFP,NMC}.json,
cad/baukasten/ausgabe/ergebnis_{LFP,NMC}.json. Schreibt ergebnis.json und w43_vergleich.png. Keine Zahl aus dem Gedächtnis."""
import json, re
from pathlib import Path
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
R = Path(__file__).resolve().parents[2]; O = Path(__file__).parent
w = (R/"forschung/ergebnis/W43.md").read_text(); pr = (R/"forschung/ergebnis/W43.pruefung.txt").read_text()
fehl = [m.group(1) for m in re.finditer(r'FEHLT im Text der Quelle: "([^"]+)"', pr)]
prod = []
for z in w.splitlines():
    c = [x.strip() for x in z.strip().strip("|").split("|")]
    if len(c) == 4 and c[2] == "kWh":
        q = re.search(r'Beleg: "([^"]+)" \((https[^)]+)\)', c[3]); zitat, url = q.groups()
        ok = zitat not in fehl
        nums = [float(x.replace(",", ".")) for x in re.findall(r"\d+(?:,\d+)?", c[1].replace(" ", ""))] if "kWh" == c[2] else []
        prod.append({"name": c[0], "kWh_text": c[1], "kWh_werte": nums, "zitat": zitat, "quelle": url, "zitat_geprueft": ok})
verw = [p for p in prod if p["zitat_geprueft"] and p["name"].startswith("Kapazität (") and "Ø" not in p["name"]]
unser = {}
for v in ("LFP", "NMC"):
    sl = json.load(open(R/f"pm/bauteile/stueckliste_{v}.json")); cd = json.load(open(R/f"cad/baukasten/ausgabe/ergebnis_{v}.json"))
    E = sl["summen"]["energie_kWh"]; m = sl["summen"]["masse_stueckliste_kg"]
    vol = cd["laenge_mm"]*cd["breite_mm"]*cd["hoehe_max_mm"]/1e6
    unser[v] = {"energie_kWh": E, "masse_kg": m, "Wh_kg": round(E*1000/m, 1), "huell_l": round(vol, 1), "Wh_l": round(E*1000/vol, 1),
                "quelle": f"pm/bauteile/stueckliste_{v}.json summen; cad/baukasten/ausgabe/ergebnis_{v}.json (Hüllquader laenge*breite*hoehe_max)"}
alle = [x for p in verw for x in p["kWh_werte"]]
lo, hi = min(alle), max(alle)
chk = {v: {"im_band_40pct": bool(lo*0.6 <= unser[v]["energie_kWh"] <= hi*1.4)} for v in unser}
erg = {"hinweis": "KI-generiert (Claude Sonnet), Entwurf", "quelle_produkte": "forschung/ergebnis/W43.md (Zitatprüfung W43.pruefung.txt: 15 bestätigt, 2 Fehler, Fehler-Zeilen ausgeschlossen)",
       "produkte_kWh": verw, "ausgeschlossen_zitat_fehlt": [p["name"] for p in prod if not p["zitat_geprueft"]],
       "produktspanne_kWh": [lo, hi], "unser": unser, "pruefung_band_40pct": chk,
       "wh_kg_vergleich": "nicht möglich: W43 enthält mit bestandener Zitatprüfung keine Packmasse (kg) und kein Packvolumen",
       "kategorie_V": {"Q8": 1}, "kategorie_V_hinweis": "Q8 Stufe 1 nur Energie (Fahrzeugangabe, brutto/netto unklar); Q7 und Q10 ohne Vergleichswert, bleiben 0"}
(O/"ergebnis.json").write_text(json.dumps(erg, ensure_ascii=False, indent=1))
fig, ax = plt.subplots(figsize=(9, 5.5))
ax.axvspan(lo, hi, color="#cfe3f5", label=f"Produktspanne W43 {lo:g}–{hi:g} kWh")
ax.axvspan(lo*0.6, lo, color="#eeeeee"); ax.axvspan(hi, hi*1.4, color="#eeeeee", label="Warnband ±40 % um die Spanne")
for i, p in enumerate(verw):
    v = p["kWh_werte"]; ax.plot([min(v), max(v)], [i, i], "o-", color="#245a8d", lw=3)
    ax.text(max(v)+1.5, i, f'{p["kWh_text"]} kWh  ({p["quelle"].rsplit("/",1)[1]})', va="center", fontsize=8)
for v, c in (("LFP", "#c0392b"), ("NMC", "#27ae60")):
    ax.axvline(unser[v]["energie_kWh"], color=c, ls="--", lw=2, label=f'unser {v}-Pack {unser[v]["energie_kWh"]:g} kWh')
ax.set_yticks(range(len(verw))); ax.set_yticklabels([p["name"].replace("Kapazität ", "") for p in verw], fontsize=8)
ax.set_xlabel("Energieinhalt Batterie des Fahrzeugs in kWh (Wikipedia-Angabe, brutto/netto offen)"); ax.set_xlim(lo*0.6-5, hi*1.4+25); ax.legend(fontsize=8, loc="lower right")
ax.set_title(f"Energieinhalt: unsere Packs {unser['LFP']['energie_kWh']:g} / {unser['NMC']['energie_kWh']:g} kWh gegen {len(verw)} Produktangaben")
fig.text(0.01, 0.01, "KI-generiert (Claude Sonnet), Entwurf. Lesehilfe: blaue Linie = Spanne eines Produkts, hellblau = alle Produkte, grau = Warnband;\nliegen die gestrichelten Linien darin, ist der Energieinhalt plausibel.\nKein Wh/kg-Vergleich: W43 liefert keine geprüfte Packmasse.", fontsize=7, va="bottom")
fig.tight_layout(rect=(0, 0.07, 1, 1)); fig.savefig(O/"w43_vergleich.png", dpi=130)
print(json.dumps({"spanne": [lo, hi], "unser": {k: v["Wh_kg"] for k, v in unser.items()}, "band": chk}))
