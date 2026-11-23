# KI-generiert (Claude Sonnet, 2026-11-23), Entwurf. Auftrag video/AUFTRAG_VIDEO_WISSEN.md (REQ-D13, BAT-DOC-13b).
# Baut den Obsidian-Wissensgraphen (wissen/, ohne _bilder) im Obsidian-Stil nach und lässt ihn nach dem echten Projektdatum wachsen.
# Aufruf: python3 video/graph_zeitraffer.py [daten|bilder] [erstes letztes]   (daten = nur Knoten, Kanten, Datumsquellen; bilder = Einzelbilder, vorhandene werden übersprungen)
# Datum je Knoten: ENT datum: -> B-BAT-Überschrift in BEFUNDE.md -> Datei-Datum der Ergebnisdatei (Recherche) -> Erst-Commit in git -> Datum des Nachbarn mit kleinstem Datum.
import os, re, sys, json, subprocess, math, datetime
import numpy as np
R = "/home/cae/hermes/batterie"; W = f"{R}/wissen"; OUT = "/home/cae/cae_projekte/batterie_video/wissen/graph"
NF = 3150; GEND = 2680          # Gesamtbilder (2750 + 400 Schluss), Bild bei dem der Graph 100 % erreicht (E3 in szenen.py)
FARBE = {"Anforderung": (240, 160, 60), "Baustein": (200, 120, 220), "Bauteil": (90, 170, 255), "Befund": (240, 90, 90), "Bericht": (255, 230, 90),
         "Dokument": (160, 160, 175), "Entscheidung": (90, 220, 150), "Nachweis": (120, 220, 220), "Recherche": (250, 140, 190), "Software": (170, 140, 255),
         "Steckbrief": (255, 200, 120), "Teil": (130, 150, 255), "Vorgang": (200, 210, 100), "Start": (255, 255, 255)}

def knoten():
    ids = []
    for d in sorted(os.listdir(W)):
        p = f"{W}/{d}"
        if d == "_bilder": continue
        if os.path.isdir(p): ids += [f"{d}/{f[:-3]}" for f in sorted(os.listdir(p)) if f.endswith(".md")]
        elif d.endswith(".md"): ids.append(d[:-3])
    return ids

def kanten(ids):
    S = set(ids); base = {}
    for i in ids: base.setdefault(i.split("/")[-1], []).append(i)
    E = set()
    for i in ids:
        t = open(f"{W}/{i}.md", encoding="utf-8").read()
        for m in re.finditer(r"\[\[([^\]|#]+)", t):
            z = m.group(1).strip()
            if z.endswith(".md"): z = z[:-3]
            if z not in S:
                c = base.get(z.split("/")[-1]); z = c[0] if c and len(c) == 1 else None
            if z and z != i: E.add(tuple(sorted((i, z))))
    return sorted(E)

def quelle(i):
    """Quelldatei(en) einer Notiz im Repo (relativ), für git-Datum."""
    d, _, n = i.rpartition("/")
    if d == "Dokument":
        c = [f"docs/{n}.md", n.replace("__", "/") + ".md", f"{n}.md", n.replace("__", "/")]
        return [x for x in c if os.path.exists(f"{R}/{x}")][:1]
    if d == "Nachweis":
        t = open(f"{W}/{i}.md", encoding="utf-8").read(); m = re.search(r'^datei: "([^"]+)"', t, re.M); return [m.group(1)] if m else []
    if d == "Anforderung": return ["pm/anforderungen.json"]
    if d == "Bauteil": return ["pm/bauteile/struktur.json"]
    if d in ("Teil",): return ["pm/bauteile/stueckliste.json"]
    if d == "Vorgang": return ["pm/plan/plan_batterie.py"]
    if d == "Software": return ["docs/SOFTWARE.md"] if os.path.exists(f"{R}/docs/SOFTWARE.md") else ["SOFTWARE.md"]
    if d == "Baustein": return [f"praesentation/bausteine/{n}.md"]
    if d == "Bericht": return ["bericht/bericht.tex"]
    if d == "Steckbrief": return []
    if i == "Start": return []
    return []

def datum_git(pfade):
    for p in pfade:
        if not os.path.exists(f"{R}/{p}"): continue
        o = subprocess.run(["git", "log", "--diff-filter=A", "--format=%ad", "--date=short", "--", p], cwd=R, capture_output=True, text=True).stdout.split()
        if o: return o[-1]
    return None

def blame_datum(n):
    z = [k for k, l in enumerate(open(f"{R}/BEFUNDE.md", encoding="utf-8"), 1) if l.startswith(f"## {n} ")]
    if not z: return None
    o = subprocess.run(["git", "blame", "--porcelain", "-L", f"{z[0]},{z[0]}", "--", "BEFUNDE.md"], cwd=R, capture_output=True, text=True).stdout
    if o.startswith("0000000000"): return None            # noch nicht committet
    m = re.search(r"^author-time (\d+)", o, re.M)
    return datetime.date.fromtimestamp(int(m.group(1))).isoformat() if m else None

def daten(ids, E):
    """Eigene Quelle: ENT, B-BAT (Überschrift, sonst git blame), W. Übrige: Minimum aus git-Datum und frühestem eigenem Datum der direkten Nachbarn."""
    bef = {m.group(1): m.group(2) for m in re.finditer(r"^## (B-BAT-\d+) \((\d{4}-\d{2}-\d{2})", open(f"{R}/BEFUNDE.md", encoding="utf-8").read(), re.M)}
    D, Q = {}, {}
    for i in ids:
        d, _, n = i.rpartition("/")
        if d == "Entscheidung":
            m = re.search(r"^datum:\s*(\d{4}-\d{2}-\d{2})", open(f"{R}/pm/entscheidungen/{n}.md", encoding="utf-8").read(), re.M)
            if m: D[i], Q[i] = m.group(1), "ENT"
        elif d == "Befund":
            if n in bef: D[i], Q[i] = bef[n], "B-BAT"
            else:
                g = blame_datum(n)
                if g: D[i], Q[i] = g, "B-BAT (git blame)"
        elif d == "Recherche" and os.path.exists(f"{R}/forschung/ergebnis/{n}.md"):
            D[i], Q[i] = datetime.date.fromtimestamp(os.path.getmtime(f"{R}/forschung/ergebnis/{n}.md")).isoformat(), "W"
    eigen = dict(D)
    nb = {i: set() for i in ids}
    for a, b in E: nb[a].add(b); nb[b].add(a)
    for i in ids:
        if i in D: continue
        g = datum_git(quelle(i)); c = [eigen[j] for j in nb[i] if j in eigen]; nd = min(c) if c else None
        if g and nd: D[i], Q[i] = (nd, "über Nachbar") if nd < g else (g, "git direkt")
        elif g: D[i], Q[i] = g, "git direkt"
        elif nd: D[i], Q[i] = nd, "über Nachbar"
    for _ in range(10):                       # Rest (ohne git und ohne eigenen Nachbarn): Nachbar mit kleinstem Datum, wiederholt
        neu = {}
        for i in ids:
            if i in D: continue
            c = [D[j] for j in nb[i] if j in D]
            if c: neu[i] = min(c)
        for i, v in neu.items(): D[i], Q[i] = v, "über Nachbar (Kette)"
        if not neu: break
    for i in ids:
        if i not in D: D[i], Q[i] = min(D.values()), "über Nachbar (Kette)"
    return D, Q

def aufbau():
    ids = knoten(); E = kanten(ids); D, Q = daten(ids, E)
    return ids, E, D, Q

def zaehlung(ids, D, Q):
    global _D; _D = D
    z = {}
    for i in ids: z[Q[i]] = z.get(Q[i], 0) + 1
    gd = {}
    for i in ids:
        if Q[i] == "git direkt": gd[D[i]] = gd.get(D[i], 0) + 1
    return {"knoten": len(ids), "quelle": z, "anteil_prozent": {k: round(100 * v / len(ids), 1) for k, v in z.items()}, "git_je_tag": gd,
            "anteil_aus_quelle_selbst_oder_git_prozent": round(100 * (len(ids) - z.get("über Nachbar (Kette)", 0)) / len(ids), 1),
            "anteil_git_direkt_2026-11-18_prozent": round(100 * gd.get("2026-11-18", 0) / len(ids), 1),
            "anteil_knoten_mit_datum_2026-11-18_prozent": round(100 * sum(1 for i in ids if D[i] == "2026-11-18") / len(ids), 1),
            "knoten_je_datum": dict(sorted(__import__("collections").Counter(D[i] for i in ids).items()))}

def layout(ids, E):
    import networkx as nx
    G = nx.Graph(); G.add_nodes_from(ids); G.add_edges_from(E)
    pos = nx.spring_layout(G, k=3.0 / math.sqrt(len(ids)), iterations=300, seed=42, weight=None)
    P = np.array([pos[i] for i in ids]); P -= np.median(P, 0)
    ax = np.percentile(np.abs(P[:, 0]), 97); ay = np.percentile(np.abs(P[:, 1]), 97)
    P[:, 0] = np.clip(P[:, 0] / ax, -1.08, 1.08); P[:, 1] = np.clip(P[:, 1] / ay, -1.08, 1.08)   # x/y getrennt auf das Bildformat strecken, Ausreißer nach innen
    return P, dict(G.degree())

def bilder(a0, a1):
    from PIL import Image, ImageDraw
    from multiprocessing import Pool
    ids, E, D, Q = aufbau(); P, deg = layout(ids, E); os.makedirs(OUT, exist_ok=True)
    rang = sorted(range(len(ids)), key=lambda k: (D[ids[k]], ids[k])); t0 = np.zeros(len(ids))
    for r, k in enumerate(rang): t0[k] = 8 + r / (len(ids) - 1) * (GEND - 8 - 25)   # Erscheinen nach Rang (nicht nach Kalendertagen)
    ix = {i: k for k, i in enumerate(ids)}; EI = np.array([(ix[a], ix[b]) for a, b in E]); te = np.maximum(t0[EI[:, 0]], t0[EI[:, 1]])
    col = np.array([FARBE.get(i.split("/")[0], FARBE["Start"]) for i in ids]); gr = np.array([deg[i] for i in ids])
    json.dump({"knoten": len(ids), "kanten": len(E), **zaehlung(ids, D, Q), "datum_je_knoten": {i: [D[i], Q[i]] for i in ids}}, open(f"{OUT}/datenquellen.json", "w"), ensure_ascii=False, indent=1)
    args = [(f, P, t0, te, EI, col, gr) for f in range(a0, a1 + 1) if not os.path.exists(f"{OUT}/{f:04d}.png")]
    with Pool(6) as p: p.map(einbild, args, chunksize=8)

def einbild(a):
    from PIL import Image, ImageDraw
    f, P, t0, te, EI, col, gr = a; S = 2; Wd, H = 1280 * S, 720 * S
    s = min(1.0, f / (NF - 1)); zoom = 1.0 + 0.04 * s
    X = (P[:, 0] * 560 * zoom + 640) * S; Y = (P[:, 1] * 318 * zoom + 360) * S
    X = X + 6 * S * math.sin(f / 260.0); Y = Y + 4 * S * math.cos(f / 310.0)       # leichte Drift
    im = Image.new("RGB", (Wd, H), (30, 30, 30)); lay = Image.new("RGBA", (Wd, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for (a_, b_), t in zip(EI, te):
        w = min(1.0, (f - t) / 14.0)
        if w <= 0: continue
        d.line([(X[a_], Y[a_]), (X[b_], Y[b_])], fill=(150, 150, 150, int(70 * w)), width=S)
    im.paste(lay, (0, 0), lay); d = ImageDraw.Draw(im)
    for k in range(len(P)):
        w = (f - t0[k]) / 12.0
        if w <= 0: continue
        w = min(1.0, w); e = 1 - (1 - w) ** 2; r = (2.2 + 0.95 * math.sqrt(gr[k])) * S * e * (1.0 + 0.5 * (1 - w))
        c = tuple(int(v * (0.5 + 0.5 * w)) for v in col[k])
        d.ellipse([X[k] - r, Y[k] - r, X[k] + r, Y[k] + r], fill=c)
    im.resize((1280, 720), Image.LANCZOS).save(f"{OUT}/{f:04d}.png")

if __name__ == "__main__":
    m = sys.argv[1] if len(sys.argv) > 1 else "daten"
    if m == "daten":
        ids, E, D, Q = aufbau(); z = zaehlung(ids, D, Q); print(len(ids), "Knoten", len(E), "Kanten"); print(json.dumps(z, ensure_ascii=False, indent=1))
    else:
        a0, a1 = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (0, NF - 1); bilder(a0, a1); print("GRAPH FERTIG", a0, a1)
