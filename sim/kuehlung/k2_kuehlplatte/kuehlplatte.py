#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. K2: 1D-Hydraulik und Waermeuebergang der Kuehlplatten. Alle Eingaben aus eingaben.json und Ergebnisdateien."""
import json, math, os
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(os.path.join(H, "../../.."))
E = json.load(open(f"{H}/eingaben.json"))
K1 = json.load(open(f"{R}/sim/kuehlung/k1_schnellladen/ergebnis.json"))["faelle"]
kf = E["kuehlmittel"]; rho, c, mu, k = kf["rho_kg_m3"], kf["c_J_kgK"], kf["mu_Pa_s"], kf["k_W_mK"]
Pr = mu*c/k; kan = E["kanal"]; Hk = kan["hoehe_mm"]/1000; st = kan["steg_mm"]/1000; zus = E["hydraulik"]["zuschlag_umlenkung_verteiler"]

def platte(v):
    P = json.load(open(f"{R}/cad/pack/entwurf/parameter_{v}.json")); G = json.load(open(f"{R}/cad/pack/entwurf/ergebnis_{v}.json"))
    rand = P["A"]["A_rand_mm"]["wert"]
    return dict(L=(G["laenge_mm"]-2*rand)/1000, B=(G["breite_mm"]-2*rand)/1000, zellen=P["A"][f"A_zellzahl_{v}"]["wert"],
                quelle=f"cad/pack/entwurf/parameter_{v}.json, ergebnis_{v}.json")

def nu_lam(a):  # a = kurze/lange Seite
    return 8.235*(1-2.0421*a+3.0853*a**2-2.4765*a**3+1.0578*a**4-0.1861*a**5)
def fre_lam(a):
    return 96*(1-1.3553*a+1.9467*a**2-1.7012*a**3+0.9564*a**4-0.2537*a**5)
def gnielinski(Re, f):
    return (f/8)*(Re-1000)*Pr/(1+12.7*math.sqrt(f/8)*(Pr**(2/3)-1))
def kanal(w, Lk, Vk, Hk=Hk):
    """Einzelkanal: w Breite [m], Lk Laenge, Vk Volumenstrom [m3/s] -> Re, Nu, h, dp_kanal"""
    A = w*Hk; Dh = 2*w*Hk/(w+Hk); u = Vk/A; Re = rho*u*Dh/mu; a = min(w, Hk)/max(w, Hk)
    f_l = fre_lam(a)/Re
    Gz = Dh/Lk*Re*Pr; nu_l = nu_lam(a)+0.0668*Gz/(1+0.04*Gz**(2/3))
    if Re <= 2300: f, nu = f_l, nu_l
    else:
        Ret = max(Re, 4000.0); f_t = (0.79*math.log(Ret)-1.64)**-2; nu_t = gnielinski(Ret, f_t)
        if Re >= 4000: f, nu = f_t, nu_t
        else:
            Rl = 2300; Gzl = Dh/Lk*Rl*Pr; nul = nu_lam(a)+0.0668*Gzl/(1+0.04*Gzl**(2/3)); fl = fre_lam(a)/Rl
            Rt = 4000; ft = (0.79*math.log(Rt)-1.64)**-2; nut = gnielinski(Rt, ft)
            s = (Re-Rl)/(Rt-Rl); f = fl+s*(ft-fl); nu = nul+s*(nut-nul)
    dp = f*Lk/Dh*rho*u*u/2
    return dict(Re=Re, Dh_mm=Dh*1000, u_m_s=u, Nu=nu, h=nu*k/Dh, dp_kanal_Pa=dp)

def rechne():
    out = {"hinweis": "KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. Erzeugt von kuehlplatte.py aus eingaben.json.", "Pr": Pr, "platten": {}, "waerme": {}, "faelle": []}
    for v in ("LFP", "NMC"): out["platten"][v] = platte(v)
    for fn, F in E["waerme"]["faelle"].items():
        v = F["var"]; q = K1[fn]["E_quelle_exakt_J"]/F["dauer_s"]; n = out["platten"][v]["zellen"]
        out["waerme"][fn] = dict(var=v, W_je_zelle=q, zellen=n, W_pack=q*n, W_je_platte=q*n/E["platten"]["anzahl"],
                                 quelle=f"sim/kuehlung/k1_schnellladen/ergebnis.json faelle.{fn}.E_quelle_exakt_J / {F['dauer_s']} s")
    for fn, W in out["waerme"].items():
        P = out["platten"][W["var"]]
        for w_mm in kan["breiten_mm"]:
            for fh in kan["fuehrung"]:
                Lk, Bq = (P["B"], P["L"]) if fh == "quer" else (P["L"], P["B"])  # Kanallaenge, Verteilbreite
                n = int(Bq/(w_mm/1000+st)); 
                for dT in kan["dT_kuehlmittel_K"]:
                    Vp = W["W_je_platte"]/(rho*c*dT); r = kanal(w_mm/1000, Lk, Vp/n)
                    dp = (1+zus)*r["dp_kanal_Pa"]; Vtot = 2*Vp
                    out["faelle"].append(dict(fall=fn, var=W["var"], breite_mm=w_mm, fuehrung=fh, dT_K=dT, n_kanaele=n, kanal_laenge_m=Lk,
                        V_pack_L_min=Vtot*6e4, V_je_platte_L_min=Vp*6e4, V_kanal_L_min=Vp/n*6e4, Re=r["Re"], Dh_mm=r["Dh_mm"], u_m_s=r["u_m_s"], Nu=r["Nu"], h_W_m2K=r["h"],
                        dp_kanal_bar=r["dp_kanal_Pa"]/1e5, dp_bar=dp/1e5, P_hyd_W=dp*Vtot,
                        ok_h=r["h"] >= E["ziele"]["h_min_W_m2K"], ok_dp=dp/1e5 <= E["ziele"]["dp_max_bar_je_pack"], ok_dT=dT <= E["ziele"]["dT_kuehlmittel_max_K"]))
    # Auswahl: je Fall (und je dT) kleinster dp mit h >= 500
    out["auswahl"] = {}
    for fn in out["waerme"]:
        for dT in [None]+kan["dT_kuehlmittel_K"]:
            c_ = [x for x in out["faelle"] if x["fall"] == fn and x["ok_h"] and (dT is None or x["dT_K"] == dT)]
            key = f"{fn}|{'alle' if dT is None else dT}"
            out["auswahl"][key] = min(c_, key=lambda x: x["dp_bar"]) if c_ else None
    json.dump(out, open(f"{H}/ergebnis.json", "w"), indent=1, ensure_ascii=False)
    return out
if __name__ == "__main__": 
    o = rechne(); print(json.dumps(o["waerme"], indent=1)); 
    for k_, x in o["auswahl"].items(): print(k_, x and {q: x[q] for q in ("breite_mm", "fuehrung", "dT_K", "V_pack_L_min", "Re", "h_W_m2K", "dp_bar", "P_hyd_W")})


def nachtrag():
    N = E["nachtrag"]; kal = N["k_Al_W_mK"]; tp = N["pad"]["dicke_mm"]/1000; kp = N["pad"]["k_W_mK"]; tb = N["blech_mm"]/1000
    out = {"hinweis": "KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. Nachtrag K2 (Opus-Auftrag), h auf Plattengrundflaeche und Zusatzvarianten.", "faelle": []}
    pl = {v: platte(v) for v in ("LFP", "NMC")}
    for fn, F in E["waerme"]["faelle"].items():
        v = F["var"]; P = pl[v]; q = K1[fn]["E_quelle_exakt_J"]/F["dauer_s"]; Wp = q*P["zellen"]/E["platten"]["anzahl"]
        for hmm in N["hoehen_mm"]:
            Hh = hmm/1000
            for w_mm in N["breiten_mm"]:
                for fh in kan["fuehrung"]:
                    for ng in N["durchgaenge"]:
                        Lk0, Bq = (P["B"], P["L"]) if fh == "quer" else (P["L"], P["B"])
                        n = int(Bq/ng/(w_mm/1000+st))
                        if n < 1: continue
                        for dT in kan["dT_kuehlmittel_K"]:
                            Vp = Wp/(rho*c*dT); r = kanal(w_mm/1000, Lk0*ng, Vp/n, Hh)
                            m = math.sqrt(2*r["h"]/(kal*st)); eta = math.tanh(m*Hh)/(m*Hh)
                            heff = r["h"]*(w_mm/1000+2*eta*Hh)/(w_mm/1000+st)
                            U = 1/(1/heff+tp/kp+tb/kal); dp = (1+zus)*r["dp_kanal_Pa"]
                            out["faelle"].append(dict(fall=fn, var=v, hoehe_mm=hmm, breite_mm=w_mm, fuehrung=fh, durchgaenge=ng, dT_K=dT, n_parallel=n, kanal_laenge_m=Lk0*ng,
                                V_pack_L_min=2*Vp*6e4, Re=r["Re"], h_Kanal=r["h"], eta_steg=eta, h_eff_Grund=heff, U_gesamt=U, dp_bar=dp/1e5, P_hyd_W=dp*2*Vp,
                                ok_U=U >= 500, ok_dp=dp/1e5 <= 0.5))
    out["auswahl"] = {}
    for fn in E["waerme"]["faelle"]:
        for tag, lim in (("alle_dT", 99), ("dT_max_5K", 5)):
            c_ = [x for x in out["faelle"] if x["fall"] == fn and x["ok_U"] and x["ok_dp"] and x["dT_K"] <= lim]
            out["auswahl"][f"{fn}|{tag}"] = min(c_, key=lambda x: x["P_hyd_W"]) if c_ else None
        out["auswahl"][f"{fn}|bestes_U"] = max([x for x in out["faelle"] if x["fall"] == fn and x["ok_dp"]], key=lambda x: x["U_gesamt"])
    json.dump(out, open(f"{H}/ergebnis_nachtrag.json", "w"), indent=1, ensure_ascii=False); return out


def k2b():
    """K2b (KI-generiert, Claude Sonnet, 2026-11-19, Entwurf): Blech 1/4/1 mm, Maeander n Bahnen je m Teilkanaele. Eingaben eingaben.json 'k2b'."""
    Q = E["k2b"]; Hh = Q["hoehe_mm"]/1000; tb = Q["blech_mm"]/1000; s = Q["steg_mm"]/1000; ts = Q["trennsteg_mm"]/1000
    kal = E["nachtrag"]["k_Al_W_mK"]; tp = Q["pad"]["dicke_mm"]/1000; kp = Q["pad"]["k_W_mK"]; z = Q["zeta_umlenkung"]
    out = {"hinweis": "KI-generiert (Claude Sonnet, 2026-11-19), Entwurf. Erzeugt von kuehlplatte.k2b() aus eingaben.json (k2b).", "faelle": []}
    pl = {v: platte(v) for v in ("LFP", "NMC")}
    for fn, V in Q["V_pack_L_min"].items():
        F = E["waerme"]["faelle"][fn]; v = F["var"]; P = pl[v]
        Wp = K1[fn]["E_quelle_exakt_J"]/F["dauer_s"]*P["zellen"]/E["platten"]["anzahl"]
        Vp = V/2/6e4; dT = Wp/(rho*c*Vp); A = P["L"]*P["B"]
        for fh in Q["fuehrung"]:
            Lb, Bq = (P["L"], P["B"]) if fh == "laengs" else (P["B"], P["L"])
            for n in Q["n_bahnen"]:
                bb = (Bq-(n-1)*ts)/n
                for w_mm in Q["breiten_mm"]:
                    w = w_mm/1000; m = int(math.floor((bb+s)/(w+s)))
                    if m < 1: continue
                    r = kanal(w, Lb, Vp/m, Hh)
                    mm_ = math.sqrt(2*r["h"]/(kal*s)); eta = math.tanh(mm_*Hh)/(mm_*Hh)
                    heff = r["h"]*(w+2*eta*Hh)/(w+s); U = 1/(1/heff+tp/kp+tb/kal)
                    dp = n*r["dp_kanal_Pa"]+(n-1)*z*rho*r["u_m_s"]**2/2
                    Akan = n*m*w*Lb; mass = 2*(2*tb*A+(A-Akan)*Hh)*Q["rho_Al"]
                    out["faelle"].append(dict(fall=fn, var=v, fuehrung=fh, n_bahnen=n, breite_mm=w_mm, m_teilkanaele=m, bahnbreite_mm=bb*1000, weg_m=n*Lb,
                        V_pack_L_min=V, Re=r["Re"], h_Kanal=r["h"], eta_steg=eta, h_eff=heff, U_gesamt=U, dp_bar=dp/1e5, P_hyd_W=dp*2*Vp, dT_K=dT, masse_2_platten_kg=mass,
                        ok_U=U >= Q["U_ziel"], ok_dp=dp/1e5 <= Q["dp_ziel_bar"]))
    json.dump(out, open(f"{H}/ergebnis_k2b.json", "w"), indent=1, ensure_ascii=False); return out
