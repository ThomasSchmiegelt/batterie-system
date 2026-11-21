# KI-generiert (Claude Sonnet, 2026-11-19), Entwurf. Auftrag G5.4. Hilfsmodul (kein Generator) für verbinder.py und elektronik.py.
"""Gemeinsame Verschaltungslogik: Reihenfolge der Zellen (LFP Schleife 2 Reihen, ENT-148; NMC Mäander, ENT-145), Abgriffe (taps),
Zuordnung zu den CMU (ENT-116/117), Lage der CMU in den Endzonen. Übertragen aus cad/pack/pack_e2d.py (Abschnitt E2) und
cad/pack/e2_verdrahtung.py (nmc_maeander, cmu_zuordnung); die Rechnung ist gleich, nur Eingänge kommen aus ctx und p()/a().
Das Ergebnis wird einmal je Lauf in ctx.verdr abgelegt."""
import math
from kern import p, a, VAR


def nmc_maeander(cells, d, t, rand, nspalten_band=7):
    """NMC 217s4p: Zellen in Reihen (x), je Reihe Spalten k (y). 4 Bänder à 7 Spalten, in jedem Band ein Spaltenzug; Gruppen = je 4 aufeinanderfolgende
    Zellen des Pfades. (Übertragen aus e2_verdrahtung.nmc_maeander.)"""
    nk = max(c["k"] for c in cells) + 1
    pfad = []
    for b in range(nk // nspalten_band):
        for j in range(nspalten_band):
            k = b * nspalten_band + j
            col = sorted([i for i, c in enumerate(cells) if c["k"] == k], key=lambda i: cells[i]["cx"])
            nach_vorn = ((b % 2 == 0) == (j % 2 == 0))
            pfad += col[::-1] if nach_vorn else col
    assert len(pfad) == len(cells) and len(set(pfad)) == len(cells), (len(pfad), len(cells))
    gr = [pfad[i:i + 4] for i in range(0, len(pfad), 4)]
    assert all(len(g) == 4 for g in gr)
    bandlen = [sum(1 for g in gr if cells[g[0]]["k"] // nspalten_band == b) for b in range(nk // nspalten_band)]
    taps = [(cells[g[0]]["cx"], cells[g[0]]["cy"]) for g in gr] + [(cells[gr[-1][-1]]["cx"], cells[gr[-1][-1]]["cy"])]
    kette = [dict(name=n, zelle=z) for n, z in (("Plus", pfad[0]), ("Mitte_A_Ende_Band2", pfad[sum(bandlen[:2]) * 4 - 1]),
                                                 ("Mitte_B_Anfang_Band3", pfad[sum(bandlen[:2]) * 4]), ("Minus", pfad[-1]))]
    return dict(pfad=pfad, gruppen=gr, taps=taps, gruppen_je_band=bandlen, anschluesse=kette)


def cmu_zuordnung(taps, ncmu, kanaele, x_vorn, x_hinten, y_min, y_max, laenge_cmu):
    """Jede CMU bekommt `kanaele` aufeinanderfolgende Abgriffe; Endzone = die mit kleinerem fernstem Abstand (Kapazität je Endzone: Innenbreite // CMU-Länge)."""
    cap = int((y_max - y_min) // laenge_cmu)
    grp = [list(range(i * kanaele, min((i + 1) * kanaele, len(taps)))) for i in range(ncmu)]
    assert grp[-1] and sum(len(g) for g in grp) == len(taps), (ncmu, len(taps))
    pref = []
    for g in grp:
        dv = max(abs(taps[i][0] - x_vorn) for i in g); dh = max(abs(taps[i][0] - x_hinten) for i in g); pref.append((dv, dh))
    seite = ["vorn" if dv <= dh else "hinten" for dv, dh in pref]
    for s, o in (("vorn", "hinten"), ("hinten", "vorn")):
        while seite.count(s) > cap:
            kand = [i for i in range(ncmu) if seite[i] == s]
            i = min(kand, key=lambda i: pref[i][1 if s == "vorn" else 0] - pref[i][0 if s == "vorn" else 1]); seite[i] = o
    return dict(gruppen=grp, seite=seite)


def verdr(ctx):
    """Verschaltung, Abgriffe, CMU-Lagen. Rückgabe-Dict (Schlüssel siehe unten), gecached in ctx.verdr."""
    if hasattr(ctx, "verdr"): return ctx.verdr
    rand, B, L = ctx.rand, ctx.B, ctx.L
    ymin, ymax = rand, B - rand
    cmuL, cmuB, cmuD = a("A_e2_cmu_mm"); ncmu, nkan = int(p("BT-320", "anzahl")), int(p("BT-320", "kanaele"))
    fw = p("BT-360", "breite_mm"); rhv = a(f"A_e2_hv_aussendurchmesser_{VAR}_mm") / 2
    xv_in, xh_in = rand, L - rand
    R = dict(ymin=ymin, ymax=ymax, xv_in=xv_in, xh_in=xh_in, cmuL=cmuL, cmuB=cmuB, cmuD=cmuD, ncmu=ncmu)
    if VAR == "NMC":
        cells = [dict(c, row=c["reihe"]) for c in ctx.zellen]
        mw = nmc_maeander(cells, ctx.zell_mass["D"], ctx.zell_mass["teilung"], rand)
        taps = mw["taps"]; tap_row = None; ans = {a_["name"]: cells[a_["zelle"]] for a_ in mw["anschluesse"]}
        R.update(mw=mw, ans=ans, cells=cells)
    else:
        r0c = sorted([c for c in ctx.zellen if c["reihe"] == 0], key=lambda c: -c["cx"]); r1c = sorted([c for c in ctx.zellen if c["reihe"] == 1], key=lambda c: c["cx"])
        kette = r0c + r1c
        ft, fh = a("A_e2_fpc_dicke_mm"), a("A_e2_fpc_halter_mm"); nl = 4; hh = fh - nl * ft
        yg = {0: ymin + hh + ft / 2, 1: ymax - hh - ft / 2}; taps = []; tap_row = []; nr0 = len(r0c)
        for i in range(len(kette) + 1):
            if i == 0: x, rw = kette[0]["cx"], 0
            elif i == len(kette): x, rw = kette[-1]["cx"], 1
            elif i == nr0: x, rw = kette[i - 1]["cx"], 0
            else: x, rw = (kette[i - 1]["cx"] + kette[i]["cx"]) / 2, (0 if i < nr0 else 1)
            taps.append((x, yg[rw])); tap_row.append(rw)
        R.update(kette=kette, nr0=nr0, yg=yg, nl=nl, hh=hh)
    asg = cmu_zuordnung(taps, ncmu, nkan, xv_in + cmuD / 2, xh_in - cmuD / 2, ymin, ymax, cmuL)
    grp_t, seite = asg["gruppen"], asg["seite"]; mean_y = [sum(taps[i][1] for i in g) / len(g) for g in grp_t]
    ypos = [None] * ncmu
    for sd in ("vorn", "hinten"):
        ids = sorted([j for j in range(ncmu) if seite[j] == sd], key=lambda j: mean_y[j]); n = len(ids)
        if n == 0: continue
        ys = []
        for j in ids: ys.append(max(mean_y[j], ys[-1] + cmuL) if ys else max(mean_y[j], ymin + cmuL / 2))
        for i in range(n - 1, -1, -1): ys[i] = min(ys[i], (ys[i + 1] - cmuL) if i < n - 1 else ymax - cmuL / 2)
        for j, y in zip(ids, ys): ypos[j] = y
    lane = [None] * ncmu
    hv_y = [c["cy"] for c in R["ans"].values()] if VAR == "NMC" else []
    for j in sorted(range(ncmu), key=lambda j: ypos[j]):
        for dd in sorted(range(-int(cmuL / 2 - fw / 2), int(cmuL / 2 - fw / 2) + 1), key=abs):
            y = ypos[j] + dd
            if all(abs(y - h) >= 2 * rhv + 5 + fw / 2 + 1 for h in hv_y) and all(abs(y - l) >= fw + 2 for l in lane if l is not None): lane[j] = y; break
        assert lane[j] is not None, j
    R.update(taps=taps, tap_row=tap_row, grp_t=grp_t, seite=seite, ypos=ypos, lane=lane,
             cmu_x={"vorn": (xv_in, xv_in + cmuD), "hinten": (xh_in - cmuD, xh_in)})
    ctx.verdr = R
    return R
