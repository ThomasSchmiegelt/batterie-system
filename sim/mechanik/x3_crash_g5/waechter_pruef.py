#!/usr/bin/env python3
# KI-generiert (Claude Sonnet, 2026-11-23), Entwurf. Waechter-Kriterien X3 (ERWARTUNG.md Nachtrag 6).
# Kriterien: dt < dt0/10 (dt0 = erste Zyklenzeile von X3_0001.out) oder |ERROR| > 10 % (Fall a) bzw. > 50 % (Fall b).
# Live:    waechter_pruef.py live <X3_000k.out> <lauf-ordner>   -> Exit 0 ok, 1 ausloesen (Grund auf stdout), 2 keine Daten
# Offline: waechter_pruef.py offline <lauf-ordner> [Zeit_ms_ab_dem_nicht_mehr_geprueft wird nicht benoetigt]
import re, sys, json, glob, os
ZEILE = re.compile(r'^\s*(\d+)\s+([-+.\dE]+)\s+([-+.\dE]+)\s+[A-Z]+\s+\d+\s+([-+.\d]+)%')
def zeilen(pfad, nur_letzte=False):
    try:
        with open(pfad, 'rb') as f:
            if nur_letzte:
                f.seek(0, 2); n = f.tell(); f.seek(max(0, n - 16384)); txt = f.read().decode('latin1')
            else:
                txt = f.read().decode('latin1')
    except OSError:
        return []
    out = []
    for l in txt.splitlines():
        m = ZEILE.match(l)
        if m: out.append((int(m.group(1)), float(m.group(2)), float(m.group(3)), float(m.group(4))))
    return out
def dt0(ordner):
    z = zeilen(os.path.join(ordner, 'X3_0001.out'))
    return z[0][2] if z else None
def art(ordner):
    return json.load(open(os.path.join(ordner, 'modell.json'))).get('lastfall_art', 'a')
def grenze_err(a): return float('inf') if a == 'b' else 10.0  # Fall b: nur dt-Kriterium (Opus, Nachtrag 6)
def verletzt(z, d0, lim):
    if z[2] < d0 / 10: return 'dt %.4g < dt0/10 = %.4g (Zyklus %d, t=%.4g ms)' % (z[2], d0 / 10, z[0], z[1])
    if abs(z[3]) > lim: return '|ERROR| %.1f %% > %g %% (Zyklus %d, t=%.4g ms)' % (abs(z[3]), lim, z[0], z[1])
    return None
if __name__ == '__main__':
    if sys.argv[1] == 'live':
        z = zeilen(sys.argv[2], True); d0 = dt0(sys.argv[3])
        if not z or d0 is None: sys.exit(2)
        g = verletzt(z[-1], d0, grenze_err(art(sys.argv[3])))
        if g: print(g); sys.exit(1)
        sys.exit(0)
    o = sys.argv[2].rstrip('/'); d0 = dt0(o); lim = grenze_err(art(o))
    mn, mx, hit, n = 1e9, 0.0, None, 0
    for p in sorted(glob.glob(os.path.join(o, 'X3_00[0-9][0-9].out'))):
        if p.endswith('X3_0000.out'): continue
        for z in zeilen(p):
            n += 1; mn = min(mn, z[2] / d0); mx = max(mx, abs(z[3]))
            g = verletzt(z, d0, lim)
            if g and not hit: hit = os.path.basename(p) + ': ' + g
    print('%-26s Fall %s dt0=%.4g Zeilen=%d min dt/dt0=%.3f max|ERR|=%.2f%% -> %s' % (os.path.basename(o), art(o), d0, n, mn, mx, 'AUSLOESUNG ' + hit if hit else 'keine'))
