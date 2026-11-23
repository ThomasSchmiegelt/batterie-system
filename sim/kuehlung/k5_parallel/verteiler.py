#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-23), Entwurf. Auftrag Opus 2026-11-23, ERWARTUNG.md (K5), ENT-158.
1D-Netz Z-Verteiler: N parallele Teilkanaele (8 x 4 mm, Laenge = Bahnlaenge des G5-Maeanders), Verteiler und Sammler gegenueber (Z: beide Sammelkanaele
durchstroemt in gleicher Richtung, Eintritt am Kanal 0, Austritt am Kanal N-1). Annahmen laut ERWARTUNG: Sammelquerschnitt Kanalhoehe x 25 mm (Variante 35 mm),
zeta = 1 je Abzweig. Auslegung dieses Skripts (Opus pruefen): zeta = 1 sowohl am Eintritts- als auch am Austrittsabzweig je Kanal, bezogen auf die Kanalgeschwindigkeit;
Impulsaenderung (Bernoulli-Anteil, Beiwert 1) im Verteiler als Druckrueckgewinn, im Sammler als Druckabfall; Wandreibung Darcy mit Rechteckprofil-f wie K2b (kuehlplatte.py).
Anschluss-Stutzen ohne Verlust (Annahme). Kanal-dp aus kuehlplatte.kanal (K2b). Daten: ergebnis_k2b.json (Fall LFP_P0, laengs, 8 Bahnen, 8 mm), G5-Plattenmasse."""
import json, math, os, sys
import numpy as np
from scipy.optimize import fsolve
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(os.path.join(H, "../../.."))
sys.path.insert(0, f"{R}/sim/kuehlung/k2_kuehlplatte"); import kuehlplatte as KP
rho, mu = KP.rho, KP.mu
ZETA = 1.0
k2 = json.load(open(f"{R}/sim/kuehlung/k2_kuehlplatte/ergebnis_k2b.json"))["faelle"]
f0 = [f for f in k2 if f["fall"] == "LFP_P0" and f["fuehrung"] == "laengs" and f["n_bahnen"] == 8 and f["breite_mm"] == 8][0]
P = json.load(open(f"{R}/cad/pack/entwurf/parameter_LFP.json"))["A"]; PG = json.load(open(f"{R}/cad/pack/entwurf/ergebnis_LFP.json"))
rand = P["A_rand_mm"]["wert"]; Lx, Ly = (PG["laenge_mm"]-2*rand)/1000, (PG["breite_mm"]-2*rand)/1000      # Platte, Kanalrichtung x (= Bahnlaenge), Verteilrichtung y
M = f0["m_teilkanaele"]*f0["n_bahnen"]; W, HK = 0.008, 0.004; PITCH = Ly/M
V1 = f0["V_pack_L_min"]/2/6e4                      # m3/s je Platte, Durchfluss x1 (K2b)
def f_darcy(Re, a):
    if Re <= 2300: return KP.fre_lam(a)/Re
    ft = lambda r: (0.79*math.log(r)-1.64)**-2
    if Re >= 4000: return ft(Re)
    fl = KP.fre_lam(a)/2300; s = (Re-2300)/1700; return fl+s*(ft(4000)-fl)
def dp_kanal(Q): return KP.kanal(W, Lx, abs(Q), HK)["dp_kanal_Pa"]*(1 if Q >= 0 else -1)
def dp_rohr(Q, bsam):
    A = bsam*HK; Dh = 2*bsam*HK/(bsam+HK); u = abs(Q)/A; Re = max(rho*u*Dh/mu, 1.0)
    return f_darcy(Re, HK/bsam)*PITCH/Dh*rho*u*u/2
def loese(fak, bsam_mm):
    b = bsam_mm/1000; A = b*HK; Qt = V1*fak; N = M
    def prof(Q):
        G = np.cumsum(Q); F = Qt-G                    # Fluss im Sammler (hinter Kanal i), Fluss im Verteiler (hinter Abzweig i)
        pout = np.zeros(N)                           # Austritt am Ende (N-1): Bezugsdruck 0, rueckwaerts aufbauen
        for i in range(N-2, -1, -1):
            pout[i] = pout[i+1]+dp_rohr(G[i], b)+rho/2*(max(G[i+1], 0)**2-G[i]**2)/A**2    # Sammler beschleunigt Richtung Austritt
        pin = np.zeros(N); pin[0] = pout[0]+dp_kanal(Q[0])+2*ZETA*rho/2*(Q[0]/(W*HK))**2
        for i in range(N-1):
            pin[i+1] = pin[i]-dp_rohr(F[i], b)+rho/2*(F[i]**2-(F[i+1] if i+1 < N-1 else 0.0)**2)/A**2   # Verteiler verzoegert (Rueckgewinn)
        return pin, pout
    def res(Q):
        pin, pout = prof(Q); r = [pin[i]-pout[i]-dp_kanal(Q[i])-2*ZETA*rho/2*(Q[i]/(W*HK))**2 for i in range(1, N)]
        return np.array(r+[(Q.sum()-Qt)/Qt*1e3])
    Q0 = np.full(N, Qt/N); Q, info, ier, msg = fsolve(res, Q0, full_output=True, xtol=1e-12)
    pin, pout = prof(Q)
    return dict(Q=Q, anteil=Q/(Qt/N), dp_Pa=pin[0]-pout[N-1], ier=ier, res_max=float(np.abs(res(Q)).max()), u_sam_max=Qt/A, Re_sam=rho*Qt/A*(2*b*HK/(b+HK))/mu,
                u_kanal_mittel=Qt/N/(W*HK), Re_kanal_mittel=KP.kanal(W, Lx, Qt/N, HK)["Re"], h_kanal=KP.kanal(W, Lx, Qt/N, HK)["h"])
def maeander(fak):
    n = f0["n_bahnen"]; m = f0["m_teilkanaele"]; r = KP.kanal(W, Lx, V1*fak/m, HK)
    return (n*r["dp_kanal_Pa"]+(n-1)*1.5*rho*r["u_m_s"]**2/2)/1e5
def gruppen(fak, k, d_mm):
    """Nachtrag 1 (Auftrag Opus 2026-11-23): k parallele Gruppen aus je n=8/k Bahnen (Maeander wie K2b, zeta_Umlenk 1,5), Verteilrohr/Sammelrohr aussen Durchmesser d, Z-Anordnung
    (Eintritt Gruppe 0, Austritt Gruppe k-1), Teilung der Abzweige = Plattenbreite/k, zeta = 1 je T-Abzweig (Ein- und Austritt), bezogen auf die Rohrgeschwindigkeit des Abzweigs (gleicher Durchmesser) = Annahme Sonnet."""
    d = d_mm/1000; A = math.pi*d*d/4; n = 8//k; m = f0["m_teilkanaele"]; Qt = V1*fak; L = Ly/k
    def dpg(Q):
        Q = abs(Q); r = KP.kanal(W, Lx, Q/m, HK); return n*r["dp_kanal_Pa"]+(n-1)*1.5*rho*r["u_m_s"]**2/2
    def dpr(Q):
        u = abs(Q)/A; Re = max(rho*u*d/mu, 1.0); f = 64/Re if Re <= 2300 else (f_darcy(Re, 1.0) if False else (0.79*math.log(max(Re, 4000.0))-1.64)**-2 if Re >= 4000 else 64/2300+(Re-2300)/1700*((0.79*math.log(4000)-1.64)**-2-64/2300))
        return f*L/d*rho*u*u/2
    zb = lambda Q: 2*ZETA*rho/2*(Q/A)**2
    def prof(Q):
        G = np.cumsum(Q); F = Qt-G; pout = np.zeros(k)
        for i in range(k-2, -1, -1): pout[i] = pout[i+1]+dpr(G[i])+rho/2*(G[i+1]**2-G[i]**2)/A**2
        pin = np.zeros(k); pin[0] = pout[0]+dpg(Q[0])+zb(Q[0])
        for i in range(k-1): pin[i+1] = pin[i]-dpr(F[i])+rho/2*(F[i]**2-(F[i+1] if i+1 < k-1 else 0.0)**2)/A**2
        return pin, pout
    def res(Q):
        pin, pout = prof(Q); return np.array([pin[i]-pout[i]-dpg(Q[i])-zb(Q[i]) for i in range(1, k)]+[(Q.sum()-Qt)/Qt*1e3])
    Q, info, ier, msg = fsolve(res, np.full(k, Qt/k), full_output=True, xtol=1e-12); pin, pout = prof(Q)
    rg = KP.kanal(W, Lx, Qt/k/m, HK)
    return dict(k=k, d_mm=d_mm, bahnen_je_gruppe=n, durchfluss_fak=fak, anteil=[float(x) for x in Q/(Qt/k)], max_abw_pct=float(np.abs(Q/(Qt/k)-1).max()*100), dp_bar=float((pin[0]-pout[k-1])/1e5),
                u_rohr_m_s=Qt/A, staudruck_bar=rho*(Qt/A)**2/2/1e5, Re_rohr=rho*Qt/A*d/mu, Re_kanal=rg["Re"], u_kanal_m_s=rg["u_m_s"], h_kanal_W_m2K=rg["h"], dT_fluid_K=None, ier=int(ier), residuum_max=float(np.abs(res(Q)).max()))
if __name__ == "__main__":
    out = dict(hinweis="KI-generiert (Claude Sonnet, 2026-11-23), Entwurf. Erzeugt von verteiler.py (ERWARTUNG K5, ENT-158).", N_kanaele=M, kanal_mm=[W*1e3, HK*1e3], kanal_laenge_m=Lx, verteilrichtung_m=Ly, teilung_mm=PITCH*1e3,
               V_je_platte_L_min_x1=V1*6e4, zeta=ZETA, quelle="ergebnis_k2b.json (LFP_P0 laengs 8 Bahnen 8 mm): m_teilkanaele*n_bahnen; Lx,Ly aus parameter_LFP.json/ergebnis_LFP.json (Platte = Bauraum - 2 Rand)",
               dp_maeander_k2b_bar_x1_Datei=f0["dp_bar"], dp_maeander_nachgerechnet_bar_x1=maeander(1.0), faelle={}, sweep=dict(fak=[], maeander=[], p25=[], p35=[]))
    out["status_einzelkanal"] = "verworfen (Nachtrag 1 ERWARTUNG): 120 Einzelkanaele am Sammler in Kanalhoehe; Ergebnis bleibt als Beleg stehen"
    for b in (25, 35):
        for fak in (1, 3):
            s = loese(fak, b); a = s["anteil"]
            out["faelle"][f"b{b}_x{fak}"] = dict(sammel_mm=b, durchfluss_fak=fak, dp_bar=s["dp_Pa"]/1e5, anteil_min=float(a.min()), anteil_max=float(a.max()), max_abw_pct=float(np.abs(a-1).max()*100),
                   i_max_abw=int(np.abs(a-1).argmax()), u_sammel_m_s=s["u_sam_max"], Re_sammel=s["Re_sam"], u_kanal_mittel_m_s=s["u_kanal_mittel"], Re_kanal_mittel=s["Re_kanal_mittel"], h_kanal_W_m2K=s["h_kanal"],
                   ier=s["ier"], residuum_max=s["res_max"], anteil=[float(x) for x in a], dp_maeander_bar=maeander(fak))
    for fak in np.arange(0.5, 4.01, 0.5):
        out["sweep"]["fak"].append(float(fak)); out["sweep"]["maeander"].append(maeander(fak))
        for b in (25, 35): out["sweep"][f"p{b}"].append(loese(fak, b)["dp_Pa"]/1e5)
    G = {}; sw = {"fak": [float(x) for x in np.arange(0.5, 4.01, 0.5)]}
    for k in (2, 4, 8):
        for d in (20, 25):
            for fak in (1, 3): G[f"k{k}_d{d}_x{fak}"] = gruppen(fak, k, d)
            sw[f"k{k}_d{d}"] = [gruppen(fa, k, d)["dp_bar"] for fa in sw["fak"]]
    out["gruppen"] = dict(beschreibung=gruppen.__doc__, faelle=G, sweep=sw)
    gut = [(v["dp_bar"], key) for key, v in G.items() if v["durchfluss_fak"] == 3 and v["max_abw_pct"] <= 10 and v["dp_bar"] < 0.22]
    out["gruppen"]["kriterium"] = "x3: max. Abweichung <= 10 % und dp < 0,22 bar; bei Gleichstand kleineres dp"; out["gruppen"]["erfuellt"] = sorted(gut); out["gruppen"]["bestes"] = min(gut)[1] if gut else None
    json.dump(out, open(f"{H}/ergebnis_verteiler.json", "w"), indent=1, ensure_ascii=False)
    for k, v in out["faelle"].items(): print(k, {q: v[q] for q in ("dp_bar", "max_abw_pct", "i_max_abw", "Re_sammel", "Re_kanal_mittel", "h_kanal_W_m2K", "ier", "residuum_max", "dp_maeander_bar")})
    print("N", M, "Mäander x1 Datei/nachgerechnet", f0["dp_bar"], out["dp_maeander_nachgerechnet_bar_x1"])
    for k, v in G.items(): print(k, round(v["dp_bar"], 4), round(v["max_abw_pct"], 2), "Re_Kanal", round(v["Re_kanal"]), "h", round(v["h_kanal_W_m2K"]), "q", round(v["staudruck_bar"], 4), v["ier"])
    print("erfuellt:", out["gruppen"]["erfuellt"], "bestes:", out["gruppen"]["bestes"])
