# KI-generiert (Claude Sonnet, 2026-11-18), Entwurf. Auftrag E2 Fortsetzung 2. Reine Geometrie/Topologie (kein FreeCAD), von pack.py (PACK_E2=1) importiert.
"""Zuordnung Messabgriffe -> CMU, FPC-Längen, NMC-Mäander (ENT-145). Alle Maße kommen als Argumente aus pack.py (Akten, Block A)."""
import math


def nmc_maeander(cells, d, t, rand, nspalten_band=7):
    """NMC 217s4p: Zellen liegen in Reihen (x) mit je 28 Zellen in Spalten k (y). 4 Bänder à 7 Spalten, in jedem Band ein Spaltenzug (Zickzack entlang x).
    Band 1 startet hinten (x groß) in Spalte 0, Band 2 vorn, Band 3 hinten, Band 4 vorn; Ende Band 4 hinten. Gruppen = je 4 aufeinanderfolgende Zellen des Pfades."""
    for c in cells:
        off = d / 2 + (t / 2 if c["row"] % 2 else 0)
        c["k"] = int(round((c["cy"] - rand - off) / t))
    nk = max(c["k"] for c in cells) + 1
    pfad = []
    for b in range(nk // nspalten_band):
        for j in range(nspalten_band):
            k = b * nspalten_band + j
            col = sorted([i for i, c in enumerate(cells) if c["k"] == k], key=lambda i: cells[i]["cx"])
            nach_vorn = ((b % 2 == 0) == (j % 2 == 0))      # Band 1 (b=0), Spalte 0: hinten -> vorn; Band 2 (b=1), Spalte 0: vorn -> hinten
            pfad += col[::-1] if nach_vorn else col
    assert len(pfad) == len(cells) and len(set(pfad)) == len(cells), (len(pfad), len(cells))
    gr = [pfad[i:i + 4] for i in range(0, len(pfad), 4)]
    assert all(len(g) == 4 for g in gr)
    dist = [math.hypot(cells[a]["cx"] - cells[b]["cx"], cells[a]["cy"] - cells[b]["cy"]) for a, b in zip(pfad, pfad[1:])]
    bandlen = [sum(1 for g in gr if cells[g[0]]["k"] // nspalten_band == b) for b in range(nk // nspalten_band)]
    taps = [(cells[g[0]]["cx"], cells[g[0]]["cy"]) for g in gr] + [(cells[gr[-1][-1]]["cx"], cells[gr[-1][-1]]["cy"])]
    kette = [dict(name=n, zelle=z) for n, z in (("Plus", pfad[0]), ("Mitte_A_Ende_Band2", pfad[sum(bandlen[:2]) * 4 - 1]), ("Mitte_B_Anfang_Band3", pfad[sum(bandlen[:2]) * 4]), ("Minus", pfad[-1]))]
    return dict(pfad=pfad, gruppen=gr, taps=taps, schritt_max_mm=max(dist), schritt_normal_mm=sorted(dist)[len(dist) // 2],
                bruecken_ueber_1p05t=sum(1 for x in dist if x > 1.05 * t), gruppen_je_band=bandlen, hälfte_A_gruppen=sum(bandlen[:2]), hälfte_B_gruppen=sum(bandlen[2:]), anschluesse=kette)


def cmu_zuordnung(taps, ncmu, kanaele, x_vorn, x_hinten, y_min, y_max, laenge_cmu, y_der_tap=None):
    """Jede CMU bekommt kanaele aufeinanderfolgende Abgriffe. Endzone = die mit kleinerem fernstem Abstand (Kapazität je Endzone: Innenbreite // CMU-Länge)."""
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
    return dict(gruppen=grp, seite=seite, kapazitaet_je_endzone=cap, fern_vorn=[p[0] for p in pref], fern_hinten=[p[1] for p in pref])


def lane_y(werte, min_abstand, y_min, y_max, sperr=()):
    """Spuren (y) sortiert nach Sollwert, mit Mindestabstand und Sperrbereichen (y0,y1); gibt Liste in Eingangsreihenfolge."""
    idx = sorted(range(len(werte)), key=lambda i: werte[i]); res = [None] * len(werte); last = y_min - 1e9
    for i in idx:
        y = max(werte[i], last + min_abstand, y_min)
        moved = True
        while moved:
            moved = False
            for a, b in sperr:
                if y > a - min_abstand / 2 and y < b + min_abstand / 2: y = b + min_abstand / 2; moved = True
        res[i] = y; last = y
    return res
