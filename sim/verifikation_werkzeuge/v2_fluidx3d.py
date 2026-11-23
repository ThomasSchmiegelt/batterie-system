#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-23), Entwurf. QN1 V2: FluidX3D (Build der Kopie sim/kuehlung/k3_gesamt/fluidx3d, bin/FluidX3D, SRT, wie K3) -
Spalt zwischen zwei Platten, Abstand h (Zellen), periodisch in x und z, Volumenkraft G (= fz) in z, Wand = TYPE_S (Halfway-Bounce-Back, Wand zwischen Fluid- und Festzelle).
Analytisch: u(y) = G y (h - y)/(2 nu); u_max = G h^2/(8 nu); u_mittel = G h^2/(12 nu) (Delta p = 12 mu L u_mittel/h^2 gleichwertig, G = Delta p/(rho L)).
Je Aufloesung h: Abweichung u_mittel und u_max (Profil an Zellmitten, Maximum der Zellwerte gegen analytischen Wert am selben Ort), Massenerhalt (mittleres rho), Profilfehler (L2).
Zwei Reihen: nu = K3 (tau 0,532) und nu = 0,1 (tau 0,8, Zusatz). Aufruf (nach rechnen/gpu_warten.sh): python3 v2_fluidx3d.py [--probe]"""
import json, os, subprocess, sys, shutil, math, time
import numpy as np
from vcommon import *
FXD = f"{R}/sim/kuehlung/k3_gesamt/fluidx3d"; U_MAX = w("V2_u_max_ziel_lbm"); HS = w("V2_aufloesungen_h_zellen")
STOP = os.environ.get("RECHNEN_STOP", f"{R}/rechnen/STOP")
def lauf(h, nu, tag):
    D = f"{H}/lauf_V2/{tag}_h{h}"; shutil.rmtree(D, ignore_errors=True); os.makedirs(D)
    Nx, Ny, Nz = 4, h+2, 4                      # Wand je 1 Zelle oben/unten (Festzellen), Fluidzellen y = 1..h
    wgeo = np.ones((Nz, Ny, Nx), np.uint8); wgeo[:, 0, :] = 0; wgeo[:, -1, :] = 0
    G = 8*nu*U_MAX/h**2; um0 = G*h*h/(12*nu)
    steps = max(20000, int(2.0*h*h/nu)); stat = max(1000, steps//50)
    wgeo.tofile(f"{D}/geometrie.bin"); alpha = nu
    open(f"{D}/fall.txt", "w").write(f"{D}/geometrie.bin {D} {Nx} {Ny} {Nz} {nu:.8g} {2*alpha:.8g} {G:.8g} {um0:.8g} {steps} {stat} 0\n")
    if os.path.exists(STOP): sys.exit("STOP gefunden")
    t0 = time.time(); r = subprocess.run([f"{FXD}/bin/FluidX3D"], cwd=FXD, capture_output=True, text=True, env=dict(os.environ, TAUSCHER_FALL=f"{D}/fall.txt", FX_Q_T="0.0", FX_Q_U0="0.0", RECHNEN_STOP=STOP))
    open(f"{D}/fluidx3d.log", "w").write(r.stdout[-6000:]+r.stderr[-2000:])
    if r.returncode == 75: sys.exit("STOP erkannt")
    if r.returncode: sys.exit(f"FluidX3D Fehler {r.returncode} ({D})")
    dt = time.time()-t0
    if dt > 600: sys.exit(f"Waechter: Fall dauerte {dt:.0f} s > 600 s")
    st = np.loadtxt(f"{D}/stat.txt", comments="#"); st = np.atleast_2d(st)
    # Profil aus feld.bin: ulong M, M x uint Index, M x (ux uy uz rho T) float
    raw = open(f"{D}/feld.bin", "rb").read(); M = int(np.frombuffer(raw[:8], np.uint64)[0]); idx = np.frombuffer(raw[8:8+4*M], np.uint32)
    v = np.frombuffer(raw[8+4*M:8+4*M+20*M], np.float32).reshape(M, 5); y = (idx // Nx) % Ny
    uz = np.array([v[y == j, 2].mean() for j in range(1, h+1)]); rho_m = float(v[:, 3].mean())
    yc = np.arange(h)+0.5; ua = G*yc*(h-yc)/(2*nu)
    um_ist = float(uz.mean()); um_ana = G*h*h/(12*nu); umax_ist = float(uz.max()); umax_ana_zelle = float(ua[np.argmax(uz)]); umax_ana = G*h*h/(8*nu)
    drift = float(abs(st[-1, 1]-st[-2, 1])/abs(st[-1, 1])) if len(st) > 1 else None
    return dict(h=h, nu=nu, tau=0.5+3*nu, G=G, Nx=Nx, Ny=Ny, Nz=Nz, schritte=steps, dauer_s=dt, u_mittel_ist=um_ist, u_mittel_ana=um_ana, abw_u_mittel_pct=100*(um_ist/um_ana-1),
                u_max_ist=umax_ist, u_max_ana_exakt=umax_ana, u_max_ana_zellmitte=umax_ana_zelle, abw_u_max_pct=100*(umax_ist/umax_ana-1), abw_u_max_zellmitte_pct=100*(umax_ist/umax_ana_zelle-1),
                profil_L2_rel_pct=float(100*np.linalg.norm(uz-ua)/np.linalg.norm(ua)), massenerhalt_rho_abw_pct=100*(rho_m-1), drift_letzter_stat=drift,
                u_mittel_stat_txt=float(st[-1, 1]), profil_uz=uz.tolist())
if __name__ == "__main__":
    out = dict(hinweis="KI-generiert (Claude Sonnet, 2026-11-23), Entwurf. Erzeugt von v2_fluidx3d.py.", werkzeug="FluidX3D bin/FluidX3D (SRT, D3Q19, FP32), Kopie k3_gesamt/fluidx3d", reihen={})
    for tag, nu in (("tauK3", w("V2_viskositaet_lbm")), ("tau0p8", w("V2_viskositaet_zusatz_lbm"))):
        res = []
        for h in HS:
            r = lauf(h, nu, tag); res.append(r); print(tag, "h", h, "u_mittel abw %.3f %%" % r["abw_u_mittel_pct"], "u_max abw %.3f %%" % r["abw_u_max_pct"], "rho %.2e" % r["massenerhalt_rho_abw_pct"], "%.0f s" % r["dauer_s"], flush=True)
        hh = [r["h"] for r in res]; e = [abs(r["abw_u_mittel_pct"]) for r in res]
        out["reihen"][tag] = dict(nu=nu, tau=0.5+3*nu, stufen=res, ordnung_u_mittel_zwischen_stufen=ordnung([1/x for x in hh], e), ordnung_u_mittel_8_16_32=ordnung([1/x for x in hh[2:]], e[2:]))
    k3 = out["reihen"]["tauK3"]["stufen"]; ue20 = [r for r in k3 if r["h"] >= 20]
    out.update(abweichung_fein_pct=max(abs(r["abw_u_mittel_pct"]) for r in ue20), ordnung_beobachtet=out["reihen"]["tauK3"]["ordnung_u_mittel_8_16_32"], massenerhalt_max_pct=max(abs(r["massenerhalt_rho_abw_pct"]) for r in k3),
               toleranz_pct=TOL["V2_ueber20_pct"], toleranz_massenerhalt_pct=TOL["V2_massenerhalt_pct"],
               bestanden=bool(max(abs(r["abw_u_mittel_pct"]) for r in ue20) < TOL["V2_ueber20_pct"] and max(abs(r["massenerhalt_rho_abw_pct"]) for r in k3) < TOL["V2_massenerhalt_pct"]),
               anmerkung="Bewertet wird die Reihe nu = K3 (tau 0,532), Stufen h >= 20 Zellen (h = 32); Reihe tau 0,8 ist Zusatz. Abweichung = u_mittel (gleichwertig Delta p bei gegebener Kraft).")
    speichere("V2", out)
