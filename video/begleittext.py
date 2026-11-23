# KI-generiert (Claude Sonnet, 2026-11-23), Entwurf. Erzeugt video/begleittext.md aus `pm.py kontext <BT>` (nicht frei geschrieben). Auftrag video/AUFTRAG_VIDEO.md.
import subprocess, re, os, datetime
R = "/home/cae/hermes/batterie"
SZ = [(1, "BT-100", "Zelle", "1 bis 12 s"), (2, "BT-200", "Zellstack", "12 bis 24 s"), (3, "BT-300", "Regelung (BMS)", "24 bis 34 s"), (4, "BT-400", "Verkabelung", "34 bis 44 s"),
      (5, "BT-500", "Struktur", "44 bis 58 s"), (6, "BT-600", "Kühlung", "58 bis 72 s"), (7, "BT-700", "Zusatzkomponenten", "72 bis 82 s"), (8, "BT-000", "Gesamtsystem", "82 bis 110 s")]
o = ["| Dok.-Nr. | BAT-DOC-13-T | Version | 0.1 | Status | Entwurf |", "|---|---|---|---|---|---|", "| Titel | Abschlussvideo: Begleittext (DE) | Ersteller | Claude Sonnet (KI) | Prüfer | – |", "",
     "> **KI-generiert.** Erzeugt von `video/begleittext.py` aus `python3 pm/pm.py kontext <BT>` (Stand " + datetime.date.today().isoformat() + "). Im Video steht nur der Name; dieser Text begleitet es. Entwurf, nicht freigegeben.", ""]
for n, bt, name, zeit in SZ:
    txt = subprocess.run(["python3", f"{R}/pm/pm.py", "kontext", bt], capture_output=True, text=True, cwd=R).stdout
    f = f"{R}/pm/gespraeche/kontext_{bt}.md"; k = open(f).read() if os.path.exists(f) else txt
    o += [f"## Szene {n}: {bt} {name} ({zeit})", ""]
    m = re.search(r"## Ich bin\n(.*?)\n\n", k, re.S)
    if m: o += [m.group(1), ""]
    ents = [x for x in re.findall(r"### (ENT-\d+) (.*?)\n(Merkmal: .*?)\n", k) if not re.search(r"Variante: NMC\)", x[1])]   # Video zeigt Variante LFP
    if ents:
        o += ["Entscheidungen, die die Form bestimmen (Quelle: Akten `pm/entscheidungen/`):", ""]
        for e, t, mk in ents: o.append(f"- **{e}** {t.split(' (')[0]}. {mk}")
    else: o.append("Keine Entscheidungsakte zu diesem Bauteil im Kontext gefunden.")
    ra = re.search(r"## Anforderungen an mich \(Lastenheft\)\n(.*?)\n\n", k, re.S)
    if ra: o += ["", "Anforderungen:", "", ra.group(1)]
    o.append("")
o += ["## Gestaltungsentscheidungen der KI (Darstellung, keine Auslegung)", "", "- Obere Pad-Lage (BT-230 oben) erscheint erst mit der Struktur (Szene 5) und hebt in Szene 6 ab, sonst verdeckt sie den Zellblock.", "- Obere Kühlplattenhälfte (BT-610 oben) und Schaltboxdeckel (BT-710 eloxiert) erscheinen erst in der Explosion.", "- Stahl-Befestigungsmaterial BT-590 ist ausgeblendet (verdeckt Innenteile).", "- Szene 1 beginnt mit einer einzelnen Zelle (aus dem gemeinsamen BT-100-Netz abgetrennt: erste Zelle in x, erste von zwei in y), danach erscheint der Rest.", "- Ergebnisbilder (Kühlung V4p, Crash X3) werden nicht eingeblendet; die Ergebnisse stehen in den Berichten der Akten (sim/kuehlung/k3_gesamt, sim/mechanik/x3_crash_g5).", "",
     "---", "KI-generiert (Claude Sonnet). Entwurf, nicht freigegeben. Bildtext im Video nur: Thomas Schmiegelt."]
open(f"{R}/video/begleittext.md", "w").write("\n".join(o) + "\n"); print("begleittext.md", len(o), "Zeilen")
