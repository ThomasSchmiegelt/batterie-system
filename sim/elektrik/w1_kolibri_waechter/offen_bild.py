# KI-generiert (Claude Sonnet, 2026-11-25), Entwurf. W1: Bild offen(t) aus verlauf.csv, waechter_log.jsonl, status.json (alle Zahlen und Titel daraus).
import json, csv, datetime, pathlib
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
D = pathlib.Path(__file__).resolve().parent
log = [json.loads(z) for z in open(D / "waechter_log.jsonl")]; st = json.load(open(D / "status.json"))
t0 = datetime.datetime.strptime(log[0]["zeit"], "%Y-%m-%d %H:%M:%S")
def tm(z): return (datetime.datetime.strptime(z, "%Y-%m-%d %H:%M:%S") - t0).total_seconds() / 60
var = {}; start = {}
for e in log:
    if e["ereignis"] == "lauf_start": var[e["lauf"]] = e["parameter"]["bohrungsvariante"]; start[e["lauf"]] = tm(e["zeit"])
FARBE = {"B4": "#2a6fb0", "B4v": "#c8691a", "B3": "#2e8b57", "B2K": "#8a5aa8"}
pts = {}
for r in csv.DictReader(open(D / "verlauf.csv"), delimiter=";"): pts.setdefault(int(r["lauf"]), []).append((float(r["t_s"]) / 60, int(r["offen"])))
fig, ax = plt.subplots(figsize=(11, 5.6)); ymax = max([o for p in pts.values() for _, o in p] + [1])
ax.axhspan(-0.5, 0.5, color="#2e8b57", alpha=0.18); ax.text(0.5, 0.0, "Zielband: 0 offene Verbindungen", va="center", fontsize=9, color="#1f5e3a")
for l, p in pts.items():
    ax.plot([x for x, _ in p], [y for _, y in p], "-o", color=FARBE.get(var[l], "k"), ms=4, lw=1.6, label=f"Lauf {l}: {var[l]}")
for e in log:
    if e["ereignis"] == "lauf_ende":
        d = e["ergebnis"]; x = tm(e["zeit"])
        if d.get("ses"): ax.plot(x, d["offen"], "D", color="k", ms=7); ax.annotate(f"DRC: {d['offen']} offen, {d['drc_verletzungen']} Verstöße", (x, d["offen"]), (6, 8), textcoords="offset points", fontsize=8)
    if e["ereignis"] != "kolibri": continue
    x = tm(e["zeit"]); ent = e.get("entscheidung", "")
    if ent.startswith("angenommen: neustart"): ax.axvline(x, color="#b3261e", lw=1.4, ls="--"); ax.text(x, ymax * 1.02, "Neustart", rotation=90, va="bottom", ha="right", fontsize=8, color="#b3261e")
    elif ent.startswith("verworfen"): ax.plot(x, ymax * 0.97, "x", color="#555", ms=8);
    else: ax.plot(x, ymax * 0.97, "|", color="#888", ms=8)
    if e.get("verworfen"): ax.plot(x, ymax * 0.90, "s", mfc="none", mec="#b3261e", ms=8)
ax.plot([], [], "|", color="#888", label="Kolibri: weiter / fertig (angenommen)"); ax.plot([], [], "x", color="#555", label="Kolibri-Antwort verworfen"); ax.plot([], [], "s", mfc="none", mec="#b3261e", label="Vorschlag außerhalb der Erlaubtliste verworfen"); ax.plot([], [], "D", color="k", label="Ergebnis nach Lauf (SES, DRC)")
ax.set_xlabel("Zeit seit Start des Wächters [min]"); ax.set_ylabel("offene Verbindungen (Freerouting, je Pass)"); ax.set_ylim(-1, ymax * 1.12); ax.grid(alpha=0.25)
ax.set_title(f"W1: offene Verbindungen je Pass, Status {st['status']}, {st['laeufe']} Läufe, {st['neustarts']} Neustarts, {st['minuten']} min", fontsize=11)
ax.legend(fontsize=8, loc="upper right"); fig.text(0.01, 0.005, "KI-generiert (Claude Sonnet, 2026-11-25), Entwurf. Quelle: waechter_log.jsonl, verlauf.csv, status.json", fontsize=7)
fig.tight_layout(rect=(0, 0.02, 1, 1)); fig.savefig(D / "offen.png", dpi=150); print("ok")
