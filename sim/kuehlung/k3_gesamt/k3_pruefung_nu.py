#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-21), Entwurf. Pruefung der FluidX3D-Methode (Quelle im Fluid, Wand T=0) am Rechteckkanal 8x4 mm:
analytisch/numerisch (Finite Differenzen, ausgebildet laminar): u aus Poisson(-1), T aus Poisson(-1)*u-frei: Quelle gleichmaessig. Nu_Quelle = h Dh/k mit h = q V/(A Tm), Tm = int(uT)/int(u).
Zum Vergleich Nu der Wandwaerme (K2b: 4,12 fuer Seitenverhaeltnis 0,5, aus kuehlplatte.nu_lam)."""
import numpy as np, scipy.sparse as sp, scipy.sparse.linalg as sl, json
def poisson(nx, ny, a, b):
    hx, hy = a/(nx+1), b/(ny+1); N = nx*ny
    Ix, Iy = sp.identity(nx), sp.identity(ny)
    Dx = sp.diags([1, -2, 1], [-1, 0, 1], (nx, nx))/hx**2; Dy = sp.diags([1, -2, 1], [-1, 0, 1], (ny, ny))/hy**2
    L = sp.kron(Iy, Dx)+sp.kron(Dy, Ix); return L.tocsc(), hx, hy
import sys; a, b = float(sys.argv[1]) if len(sys.argv) > 1 else 8.0, 4.0; nx, ny = int(20*a), 80
L, hx, hy = poisson(nx, ny, a, b); one = np.ones(nx*ny)
u = sl.spsolve(L, -one); T = sl.spsolve(L, -one)   # D=1, q=1
Tm = (u*T).sum()/u.sum(); V = a*b; A = 2*(a+b); Dh = 4*V/A
Nu = (V/A/Tm)*Dh                                  # h = q V/(A Tm), D = 1
a_ = 0.5; nu_l = 8.235*(1-2.0421*a_+3.0853*a_**2-2.4765*a_**3+1.0578*a_**4-0.1861*a_**5)
out = dict(Nu_Quellenmodell_numerisch=float(Nu), Nu_Wandwaerme_K2b_ausgebildet=nu_l, verhaeltnis=float(Nu/nu_l), hinweis="KI-generiert (Claude Sonnet), Entwurf")
json.dump(out, open("pruefung_nu.json", "w"), indent=1); print(out)
