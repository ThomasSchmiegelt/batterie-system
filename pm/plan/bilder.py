#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. Auftrag BILD-1 Teil 2.
Sucht alle *.png unter sim/ und cad/ und erzeugt docs/16_ergebnisbilder.md (nicht von Hand bearbeiten)."""
import os, re, glob, datetime
R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
VORGANG = {"vergleich_lfp_nmc": "C0", "varianten_lfp_nmc": "C0b", "g1_anordnung": "G1", "entwurf": "G2", "render": "G2", "detail": "G2", "k0_zelle": "K0", "bilder": "K0", "k1_schnellladen": "K1", "e1_querschnitte": "E1"}
bilder = sorted(p for t in ("sim", "cad") for p in glob.glob(os.path.join(R, t, "**", "*.png"), recursive=True))
# K0-R (2026-11-17): Workbench-Renderings render_*.png / verlauf_*.mp4 sind Vorstufe, ersetzt durch cycles_*; nicht mehr gezeigt (Dateien bleiben)
bilder = [p for p in bilder if not (os.path.basename(p).startswith("render_") and "k0_zelle" in p)]

def lesehilfe(ordner, name):
    for f in sorted(glob.glob(os.path.join(ordner, "*lesehilfe*.md"))):
        txt = open(f, encoding="utf-8").read()
        for absatz in re.split(r"\n\s*\n", txt):
            if re.search(r"Lesehilfe zu\s+\**\s*`?" + re.escape(name), absatz):
                return re.sub(r"^\*\*Lesehilfe zu [^*]*\*\*\s*", "", absatz.strip()), os.path.relpath(f, R)
    return None, None

datum = datetime.date.today().isoformat()
out = ["""| Dok.-Nr. | BAT-DOC-16 | Version | 0.1 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Ergebnisbilder mit Lesehilfe | Ersteller | Claude Sonnet (KI), Auftrag Opus | Prüfer | – (Opus offen) |

> **KI-generiert.** Entwurf, nicht vom Menschen freigegeben. **Erzeugt von `pm/plan/bilder.py`, nicht von Hand bearbeiten.** Stand: %s.

Alle Bilder unter `sim/` und `cad/` mit Lesehilfe für Nicht-Fachleute, Quelle und Vorgang. Zielbänder und Grenzen sind in den Bildern beschriftet; Annahmen sind als solche benannt.
""" % datum]
fehler = []
ordner_alt = None
for p in bilder:
    ordner = os.path.dirname(p); name = os.path.basename(p)
    rel = os.path.relpath(ordner, R)
    if ordner != ordner_alt:
        out.append(f"\n## {rel}\n")
        ordner_alt = ordner
    lh, lhf = lesehilfe(ordner, name)
    erg = os.path.join(ordner, "ergebnis.json")
    if not os.path.exists(erg): erg = os.path.join(ordner, "ergebnis_detail.json")
    if not os.path.exists(erg): erg = os.path.join(os.path.dirname(ordner), "ergebnis.json")  # render/ -> entwurf/..
    quelle = os.path.relpath(erg, R) if os.path.exists(erg) else "ergebnis.json fehlt"
    vorg = "G4" if rel.startswith("cad/pack") else VORGANG.get(os.path.basename(ordner), "unbekannt")
    if os.path.basename(ordner) == "bilder" and os.path.basename(os.path.dirname(ordner)) in VORGANG: vorg = VORGANG[os.path.basename(os.path.dirname(ordner))]
    out.append(f"### {name}\n\n![{name}]({os.path.relpath(p, os.path.join(R, 'docs'))})\n")
    out.append(f"**Lesehilfe:** {lh if lh else 'Lesehilfe fehlt'}\n")
    out.append(f"- Quelle: `{quelle}`" + (f"; Lesehilfe: `{lhf}`" if lhf else ""))
    out.append(f"- Vorgang: {vorg}\n")
    if not lh: fehler.append(os.path.relpath(p, R))
    if quelle.endswith("fehlt"): fehler.append(os.path.relpath(p, R) + " (Quelle ergebnis.json fehlt)")
videos = sorted(p for t in ("sim", "cad") for p in glob.glob(os.path.join(R, t, "**", "*.mp4"), recursive=True) if not (os.path.basename(p).startswith("verlauf_") and "k0_zelle" in p))
if videos:
    out.append("\n## Videos (MP4)\n")
    for p in videos:
        ordner = os.path.dirname(p); name = os.path.basename(p); lh, lhf = lesehilfe(ordner, name)
        if not lh:
            f0 = sorted(glob.glob(os.path.join(ordner, "*lesehilfe*.md")))
            lh = "siehe Lesehilfe der Standbilder (gleiche Darstellung, Bildfolge aus der Rechnung)" if f0 else "Lesehilfe fehlt"; lhf = os.path.relpath(f0[0], R) if f0 else None
        out.append(f"- [{name}]({os.path.relpath(p, os.path.join(R, 'docs'))}) (Vorgang {VORGANG.get(os.path.basename(ordner), 'unbekannt')}): {lh}")
out.append("\n## Fehlerliste\n")
out += [f"- {f}" for f in fehler] if fehler else ["- keine (jedes Bild hat Lesehilfe und Quelle)"]
out.append("\n---\n*KI-generiert (Claude Sonnet), Entwurf, nicht vom Menschen freigegeben. Erzeugt von pm/plan/bilder.py.*\n")
open(os.path.join(R, "docs", "16_ergebnisbilder.md"), "w", encoding="utf-8").write("\n".join(out))
print(len(bilder), "Bilder,", len(fehler), "Fehler")
