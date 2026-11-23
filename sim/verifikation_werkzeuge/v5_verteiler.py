#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-23), Entwurf. QN1 V5: Einzelkanal des 1D-Verteilers (k5 verteiler.dp_kanal, ruft kuehlplatte.kanal K2b) gegen
(a) die exakte Reihenloesung der Poiseuille-Stroemung im Rechteckkanal (Boussinesq-Reihe, unabhaengig von f*Re-Naeherung) und
(b) Shah-London f*Re (96 (1-1,3553a+...)), laminar. Kanal 8 x 4 mm, Laenge = Bahnlaenge Lx aus verteiler.py. Fluid rho, mu aus kuehlplatte.py (wie K5).
Analytisch (a): Q = h^3 w dp/(12 mu L) [1 - 192 h/(pi^5 w) sum_{n odd} tanh(n pi w/(2h))/n^5], w >= h."""
import json, math, sys
from vcommon import *
sys.path.insert(0, f"{R}/sim/kuehlung/k5_parallel"); sys.path.insert(0, f"{R}/sim/kuehlung/k2_kuehlplatte")
import verteiler as VT, kuehlplatte as KP
W, HK = w("V5_kanal_breite_mm")/1000, w("V5_kanal_hoehe_mm")/1000; Lx = VT.Lx; mu, rho = VT.mu, VT.rho
a = HK/W; Dh = 2*W*HK/(W+HK)
S = sum(math.tanh(n*math.pi*W/(2*HK))/n**5 for n in range(1, 2001, 2))
def dp_exakt(Q):   # Q in m3/s
    return Q*12*mu*Lx/(HK**3*W*(1-192*HK/(math.pi**5*W)*S))
def dp_shah(Q):
    u = Q/(W*HK); Re = rho*u*Dh/mu; return KP.fre_lam(a)/Re*Lx/Dh*rho*u*u/2
fall = []
for fak in w("V5_durchfluss_faktoren"):
    Q = VT.V1*fak/VT.M                        # Volumenstrom je Teilkanal wie K5 (Faktor auf Durchfluss x1)
    u = Q/(W*HK); Re = rho*u*Dh/mu
    d = dict(faktor=fak, Q_m3_s=Q, Re=Re, dp_exakt_Pa=dp_exakt(Q), dp_shahlondon_Pa=dp_shah(Q), dp_werkzeug_verteiler_dp_kanal_Pa=VT.dp_kanal(Q), dp_werkzeug_kuehlplatte_kanal_Pa=KP.kanal(W, Lx, Q, HK)["dp_kanal_Pa"])
    d["abw_werkzeug_gegen_exakt_pct"] = 100*(d["dp_werkzeug_verteiler_dp_kanal_Pa"]/d["dp_exakt_Pa"]-1)
    d["abw_werkzeug_gegen_shahlondon_pct"] = 100*(d["dp_werkzeug_verteiler_dp_kanal_Pa"]/d["dp_shahlondon_Pa"]-1)
    d["abw_shahlondon_gegen_exakt_pct"] = 100*(d["dp_shahlondon_Pa"]/d["dp_exakt_Pa"]-1)
    fall.append(d)
lam = [d for d in fall if d["Re"] < 2300]
ref = lam[-1]
out = dict(hinweis="KI-generiert (Claude Sonnet, 2026-11-23), Entwurf. Erzeugt von v5_verteiler.py.", kanal_mm=[W*1e3, HK*1e3], laenge_m=Lx, rho=rho, mu=mu, seitenverhaeltnis=a, faelle=fall,
           laminar_alle=len(lam) == len(fall), abweichung_fein_pct=max(abs(d["abw_werkzeug_gegen_exakt_pct"]) for d in lam), abweichung_gegen_shahlondon_pct=max(abs(d["abw_werkzeug_gegen_shahlondon_pct"]) for d in lam),
           ordnung_beobachtet=None, toleranz_pct=TOL["V5_dp_pct"], bestanden=bool(lam and max(abs(d["abw_werkzeug_gegen_exakt_pct"]) for d in lam) < TOL["V5_dp_pct"] and max(abs(d["abw_werkzeug_gegen_shahlondon_pct"]) for d in lam) < TOL["V5_dp_pct"]))
speichere("V5", out)
