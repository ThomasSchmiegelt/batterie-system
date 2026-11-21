#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-20), Entwurf. K3: FluidX3D-Strömung der Kühlplatte (Mäander LFP, Teilkanal 8x4 mm).
Aufruf: python3 k3_fluidx3d.py bahn|umlenk|auswerten [--probe]
  bahn   : periodisches Stück eines Teilkanals, Volumenkraft -> Reibungsbeiwert f, Wärmeübergang h (Quelle im Fluid, Wand T=0; Methode wie stellarator/tauscher_cfd.py)
  umlenk : 2 Bahnen + Umlenkkammer 30 mm, Einlass/Auslass, adiabate Wand, Quelle -> Umlenkverlust zeta, Totzonen, Aufwärmung
Alle Zahlen aus eingaben.json und sim/kuehlung/k2_kuehlplatte/ergebnis_k2b.json. Ausgabe: lauf_<modus>[_probe]/ , ergebnis.json."""
import json, os, subprocess, sys, math
import numpy as np
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(os.path.join(H, "../../.."))
E = json.load(open(f"{H}/eingaben.json")); G = E["geometrie_mm"]; KM = E["kuehlmittel"]; FXD = f"{H}/fluidx3d"
probe = "--probe" in sys.argv
REN = int(sys.argv[sys.argv.index("--re")+1]) if "--re" in sys.argv else E["fx"]["Re_liste"][0]
zpm = E["fx"]["zellen_je_mm_probe"] if probe else E["fx"]["zellen_je_mm"]; tag = f"_re{REN}" + ("_probe" if probe else "")
K2 = [f for f in json.load(open(f"{R}/sim/kuehlung/k2_kuehlplatte/ergebnis_k2b.json"))["faelle"]
      if f["fall"] == E["fall"] and f["fuehrung"] == "laengs" and f["n_bahnen"] == 8 and f["breite_mm"] == 8][0]
Pr = KM["mu"]*KM["c"]/KM["k"]; w_mm, H_mm = float(os.environ.get("K3_W_MM", 8)), G["hoehe"]   # K3_W_MM nur fuer die Methodenpruefung
Dh_mm = 2*w_mm*H_mm/(w_mm+H_mm)
c = lambda mm: int(round(mm*zpm))
Re = float(REN); u0 = 0.05*Re/100; dh_c = Dh_mm*zpm; Pr_sim = E["fx"]["Pr_sim"]; nu = u0*dh_c/Re; D = nu/Pr_sim; tau = 0.5+3*nu
print("tau", tau, "u0", u0, "Re", Re, flush=True)
if tau < E["fx"]["tau_min"]: print("ABBRUCH: tau < tau_min"); sys.exit(2)   # Pr_sim: Annahme Sonnet (siehe eingaben.json), Nu im ausgebildeten laminaren Strom ~ unabhaengig von Pr
u_phys = K2["Re"]*KM["mu"]/(KM["rho"]*Dh_mm/1000)

def fxlauf(aus, w, Nx, Ny, Nz, fz, steps, stat, modus, q, exe="FluidX3D"):
    os.makedirs(aus, exist_ok=True); w.astype(np.uint8).tofile(f"{aus}/geometrie.bin")
    open(f"{aus}/fall.txt", "w").write(f"{aus}/geometrie.bin {aus} {Nx} {Ny} {Nz} {nu:.6g} {2*D:.6g} {fz:.6g} {u0:.6g} {steps} {stat} {modus}\n")
    r = subprocess.run([f"{FXD}/bin/{exe}"], cwd=FXD, capture_output=True, text=True,
                       env=dict(os.environ, TAUSCHER_FALL=f"{aus}/fall.txt", FX_Q_T=f"{q:.6e}", FX_Q_U0="0.0"))
    open(f"{aus}/fluidx3d.log", "w").write(r.stdout[-8000:]+r.stderr[-3000:])
    if r.returncode == 75: print("STOP erkannt"); sys.exit(75)
    if r.returncode != 0: print("FluidX3D Fehler", r.returncode); sys.exit(1)

def bahn():
    # Teilkanal w x H, Steg je halb links/rechts, Blech oben/unten (Festzellen). Achsen: x Breite, y Hoehe, z Stroemung.
    sx, bl = c(G["steg"]), c(G["blech"]); nw, nh = c(w_mm), c(H_mm)
    Nx, Ny, Nz = nw+sx, nh+2*bl, 64 if not probe else 32
    w = np.zeros((Nz, Ny, Nx), np.uint8); x0 = sx//2; w[:, bl:bl+nh, x0:x0+nw] = 1
    nfl = int(w.sum()); A = 2*(nw+nh)*Nz
    fre = 96*(1-1.3553*0.5+1.9467*0.25-1.7012*0.125+0.9564*0.0625-0.2537*0.03125)   # Darcy f*Re Rechteck 0,5 (wie kuehlplatte.fre_lam)
    fz = fre/Re/4*2*u0**2/dh_c
    Nu0 = 5.0; q = Nu0*D/dh_c*4/dh_c
    aus = f"{H}/lauf_bahn{tag}"; steps = E["fx"]["schritte_bahn"]//(4 if probe else 1)
    for v in range(5):      # Antrieb nachregeln (kurze Laeufe), dann ein langer Lauf fuer die Temperatur
        fxlauf(aus, w, Nx, Ny, Nz, fz, int(5*dh_c**2/nu), 20000, 0, q)
        d = np.loadtxt(f"{aus}/stat.txt", comments="#"); m = d[int(0.7*len(d)):]
        u = m[:, 1].mean(); re = u*dh_c/nu
        print("Versuch", v, "fz", fz, "Re", re, flush=True)
        if abs(re/Re-1) < 0.03: break
        fz *= Re/re     # laminar: f ~ 1/Re
    fxlauf(aus, w, Nx, Ny, Nz, fz, steps, 20000, 0, q)
    d = np.loadtxt(f"{aus}/stat.txt", comments="#"); m = d[int(0.8*len(d)):]; u, Tm = m[:, 1].mean(), m[:, 2].mean(); re = u*dh_c/nu
    drift = float((m[-1, 2]-m[0, 2])/Tm)   # relative Aenderung von T_m im letzten Fuenftel (Konvergenzmass)
    f_fan = fz*dh_c/(2*u**2); f_D = 4*f_fan; fRe = f_D*re
    h_lb = q*nfl/(A*Tm); Nu = h_lb*dh_c/D; h = Nu*KM["k"]/(Dh_mm/1000)
    out = dict(modus="bahn", probe=probe, gitter=[Nx, Ny, Nz], zellen_je_mm=zpm, Re=float(re), Re_soll=Re, Pr=Pr, Pr_sim=Pr_sim, f_Darcy=float(f_D), f_Re_Darcy=float(fRe), tau=tau, u0=u0, Nu=float(Nu), h_W_m2K=float(h),
               T_m_schwankung=float(m[:, 2].std()/Tm), T_m_drift_letztes_fuenftel=drift, fz=fz, versuche=v+1,
               k2b=dict(h_Kanal=K2["h_Kanal"], f_Darcy=None, quelle="ergebnis_k2b.json"))
    json.dump(out, open(f"{aus}/ergebnis.json", "w"), indent=1); print(json.dumps(out)); return out

def umlenk():
    sx, bl, tr = c(G["steg"]), c(G["blech"]), c(G["trennsteg"]); nw, nh, m_ = c(w_mm), c(H_mm), G["teilkanaele_je_bahn"]
    bb = c(G["bahnbreite"]); pitch = nw+sx; mrg0 = (bb-(m_*pitch-sx))//2
    Ll, Lk = c(E["fx"]["lane_lang_umlenk_mm"]), c(G["kammer"])
    Nx, Ny, Nz = 2*bb+tr, nh+2*bl, Ll+Lk+2     # z=0 Ein-/Auslassebene (Rand), z=Nz-1 Endwand
    w = np.zeros((Nz, Ny, Nx), np.uint8)
    for lane in (0, 1):
        for i in range(m_):
            x0 = lane*(bb+tr)+mrg0+i*pitch
            w[1:Ll+1, bl:bl+nh, x0:x0+nw] = 1                     # Bahn
            w[0, bl:bl+nh, x0:x0+nw] = 3 if lane == 0 else 4      # Einlass / Auslass
    w[Ll+1:Ll+1+Lk, bl:bl+nh, 1:Nx-1] = 1                         # Umlenkkammer ueber beide Bahnen
    nA_in = int((w[0] == 3).sum()); nfl = int((w > 0).sum())
    q = 2e-5/ (nfl/ (nA_in)) * 1.0 if False else 0.0
    # Quelle so, dass T_aus ~ 1: q = u0*nA_in/nfl / 1  (Bilanz q*nfl = T*u0*nA_in)
    q = 1.0*u0*nA_in/nfl
    aus = f"{H}/lauf_umlenk{tag}"; steps = E["fx"]["schritte_umlenk"]//(3 if probe else 1)
    fxlauf(aus, w, Nx, Ny, Nz, 0.0, steps, 5000, 1, q, exe="FluidX3D")
    f = open(f"{aus}/feld.bin", "rb"); M = int(np.frombuffer(f.read(8), np.uint64)[0])
    idx = np.frombuffer(f.read(4*M), np.uint32); v = np.frombuffer(f.read(20*M), np.float32).reshape(M, 5)
    ux = np.zeros(Nx*Ny*Nz, np.float32); uy = ux.copy(); uz = ux.copy(); rho = np.ones(Nx*Ny*Nz, np.float32); T = ux.copy(); fl = np.zeros(Nx*Ny*Nz, bool)
    ux[idx], uy[idx], uz[idx], rho[idx], T[idx] = v.T; fl[idx] = True
    sh = (Nz, Ny, Nx); ux, uy, uz, rho, T, fl = [a.reshape(sh) for a in (ux, uy, uz, rho, T, fl)]
    np.savez(f"{aus}/feld.npz", ux=ux, uz=uz, T=T, fl=fl)   # unkomprimiert (schneller), ohne uy/rho/w
    za = 1+int(0.6*Ll)        # Messebene in der Bahn (entwickelt)
    l1, l2 = w[za] == 1, w[za] == 1
    xs1 = np.zeros(Nx, bool); xs1[:bb] = True; xs2 = ~xs1
    s1 = fl[za] & xs1[None, :]; s2 = fl[za] & xs2[None, :]
    p1, p2 = (rho[za][s1].mean()-1)/3, (rho[za][s2].mean()-1)/3     # p = rho c_s^2, c_s^2 = 1/3
    ubar = np.abs(uz[za][s1]).mean()
    bahn_erg = json.load(open(f"{H}/lauf_bahn{tag}/ergebnis.json"))
    Re_eff = Re*ubar/u0; fD = bahn_erg["f_Re_Darcy"]/Re_eff          # laminar: f = (f Re)/Re mit dem tatsaechlichen Re der Bahn
    fl_in = uz[0][fl[0] & xs1[None, :]].sum(); fl_1 = uz[za][s1].sum(); fl_2 = -uz[za][s2].sum()
    dp_total = p1-p2; dp_fric = fD*(2*(Ll-za+1)/dh_c)*ubar**2/2     # Reibung beider Bahnstuecke bis zur Kammer (rho=1)
    zeta = (dp_total-dp_fric)/(ubar**2/2)
    # Totzonen: Kammer (z > Ll), Mittelebene, |u| < 10 % des Mittels
    ym = Ny//2; cz = slice(Ll+1, Ll+1+Lk); fch = fl[cz, ym, :]; vel = np.sqrt(ux[cz, ym, :]**2+uz[cz, ym, :]**2)
    vm = vel[fch].mean(); tot = (vel[fch] < 0.1*vm).sum(); anteil_kammer = tot/fch.sum()
    vb = np.abs(uz[1:Ll+1, ym, :]); fb = fl[1:Ll+1, ym, :]; vbm = vb[fb].mean(); tot_b = (vb[fb] < 0.1*vbm).sum()
    # Totzone gesamte Gitterflaeche (Bahnen + Kammer, Mittelebene), Webs nicht mitgezaehlt
    anteil_ges = (tot+0)/(fch.sum()+fb.sum())
    # Aufwaermung: Mischtemperatur im Auslassbereich (Bahn 2, Ebene z=2) gegen Bilanz q nfl/(u0 nA_in) (Gitter-T)
    zo = 2; so = fl[zo] & xs2[None, :]; Tmix = (np.abs(uz[zo][so])*T[zo][so]).sum()/np.abs(uz[zo][so]).sum()
    T_bil = q*nfl/(u0*nA_in)
    out = dict(modus="umlenk", probe=probe, Re_soll=Re, Re_eff=float(Re_eff), fluss_lane1_zu_einlass=float(fl_1/fl_in), fluss_lane2_zu_lane1=float(fl_2/fl_1), tau=tau, gitter=[Nx, Ny, Nz], zellen_je_mm=zpm, u_bahn_mittel_gitter=float(ubar), u_soll=u0,
               dp_gesamt_lb=float(dp_total), dp_reibung_lb=float(dp_fric), zeta_umlenkung=float(zeta), zeta_K2b=1.5,
               totzone_anteil_kammer=float(anteil_kammer), totzone_anteil_bahn=float(tot_b/fb.sum()), totzone_anteil_gesamtflaeche=float(anteil_ges),
               T_aus_misch_lb=float(Tmix), T_aus_bilanz_lb=float(T_bil), bilanz_abw_prozent=float(100*(Tmix/T_bil-1)),
               fluidzellen=nfl, einlass_zellen=nA_in, quelle_lb=q)
    json.dump(out, open(f"{aus}/ergebnis.json", "w"), indent=1); print(json.dumps(out)); return out

def auswerten():
    rho, c_ = KM["rho"], KM["c"]; n = 8; Lb = G["bahnlaenge"]/1000; u = u_phys; Dh = Dh_mm/1000
    a_ = 0.5; nu_l = 8.235*(1-2.0421*a_+3.0853*a_**2-2.4765*a_**3+1.0578*a_**4-0.1861*a_**5)
    pq = json.load(open(f"{H}/pruefung_nu.json"))["Nu_Quellenmodell_numerisch"]
    gz = K2["h_Kanal"]*Dh/KM["k"]/nu_l          # Graetz-Faktor wie K2b: Nu(K2b)/Nu ausgebildet
    out = dict(hinweis="KI-generiert (Claude Sonnet, 2026-11-21), Entwurf. Erzeugt von k3_fluidx3d.py auswerten (Methode ERWARTUNG.md Nachtrag 1).", re={}, graetz_faktor_k2b=gz, Nu_ausgebildet_theorie_wand=nu_l, Nu_quellenmodell_numerisch=pq)
    for r_ in E["fx"]["Re_liste"]:
        A = json.load(open(f"{H}/lauf_bahn_re{r_}/ergebnis.json")); B = json.load(open(f"{H}/lauf_umlenk_re{r_}/ergebnis.json"))
        Nu_w = A["Nu"]*nu_l/pq      # Umrechnung Quellenmodell -> Wandwaerme ueber das numerische Verhaeltnis (Annahme Sonnet, k3_pruefung_nu.py)
        out["re"][str(r_)] = dict(tau=A["tau"], f_Re_Darcy=A["f_Re_Darcy"], f_Re_theorie=64*0.9 if False else None, Nu_quelle=A["Nu"], Nu_wand_umgerechnet=Nu_w,
            h_760_W_m2K=Nu_w*gz*KM["k"]/Dh, zeta=B["zeta_umlenkung"], Re_eff_umlenk=B.get("Re_eff"), fluss_lane1_zu_einlass=B.get("fluss_lane1_zu_einlass"), fluss_lane2_zu_lane1=B.get("fluss_lane2_zu_lane1"), totzone_kammer=B["totzone_anteil_kammer"], totzone_gesamt=B["totzone_anteil_gesamtflaeche"], bilanz_abw_prozent=B["bilanz_abw_prozent"])
    R_ = out["re"][str(E["fx"]["Re_liste"][-1])]
    dp = (n*R_["f_Re_Darcy"]/K2["Re"]*Lb/Dh+(n-1)*R_["zeta"])*rho*u*u/2
    out.update(dp_platte_bar_fx=dp/1e5, dp_platte_bar_k2b=K2["dp_bar"], dp_abw_prozent=100*(dp/1e5/K2["dp_bar"]-1), h_fx=R_["h_760_W_m2K"], h_k2b_Kanal=K2["h_Kanal"], h_abw_prozent=100*(R_["h_760_W_m2K"]/K2["h_Kanal"]-1),
        fRe_Re100_gegen_Re200_prozent=100*(out["re"]["200"]["f_Re_Darcy"]/out["re"]["100"]["f_Re_Darcy"]-1), Nu_Re100_gegen_Re200_prozent=100*(out["re"]["200"]["Nu_quelle"]/out["re"]["100"]["Nu_quelle"]-1),
        erwartung=dict(f_Re=62, f_Re_band_prozent=10, Nu_band_prozent=15, bilanz_band_prozent=5, quelle="ERWARTUNG.md Nachtrag 1"))
    json.dump(out, open(f"{H}/ergebnis.json", "w"), indent=1, ensure_ascii=False); print(json.dumps({k: v for k, v in out.items() if k != "re"}, ensure_ascii=False)[:600]); return out

if __name__ == "__main__":
    {"bahn": bahn, "umlenk": umlenk, "auswerten": auswerten}[sys.argv[1]]()
