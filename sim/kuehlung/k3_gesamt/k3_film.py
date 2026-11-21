#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-21), Entwurf. K3-Film: Durchstroemung der Kuehlplatte als Video (AUFTRAG_FILM.md, ERWARTUNG.md Nachtrag 3).
Aufruf: python3 k3_film.py rechnen [--probe] | bild
Gebiet: 2 Bahnen (je 15 Teilkanaele 8x4 mm) + Umlenkkammer, Einlass-Geschwindigkeitsrand am Bahnanfang, Re 200, 4 Zellen/mm, Pr_sim 1, beheizte Wand T=1, Eintritt T=0.
Bilder: FluidX3D wird ohne eigene Grafik betrieben (Mittelebene als Rohdaten, Darstellung hier, feste Farbskala); Abweichung vom Wortlaut 'GRAPHICS' siehe ERGEBNIS."""
import json, os, subprocess, sys, shutil, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
H = os.path.dirname(os.path.abspath(__file__)); FXD = f"{H}/fluidx3d"
E = json.load(open(f"{H}/eingaben.json")); G = E["geometrie_mm"]; KM = E["kuehlmittel"]
probe = "--probe" in sys.argv; zpm = E["fx"]["zellen_je_mm"]; c = lambda mm: int(round(mm*zpm))
RE = 200.0; u0 = 0.05*RE/100; w_mm, H_mm = 8.0, G["hoehe"]; Dh = 2*w_mm*H_mm/(w_mm+H_mm); dh_c = Dh*zpm
nu = u0*dh_c/RE; D = nu/E["fx"]["Pr_sim"]; tau = 0.5+3*nu
LL_MM, ZA_MM, NFRAMES = 200, 60, 600
aus = f"{H}/lauf_film" + ("_probe" if probe else "")
sx, bl, tr, nw, nh, m_ = c(G["steg"]), c(G["blech"]), c(G["trennsteg"]), c(w_mm), c(H_mm), G["teilkanaele_je_bahn"]
bb = c(G["bahnbreite"]); pitch = nw+sx; mrg0 = (bb-(m_*pitch-sx))//2; Ll, Lk = c(LL_MM), c(G["kammer"]); za = 1+c(ZA_MM)
Nx, Ny, Nz = 2*bb+tr, nh+2*bl, Ll+Lk+2; xs = bb+tr
dt_ms = 1000*(1/zpm/1000)*u0/(RE*KM["mu"]/KM["rho"]/(Dh/1000))      # Gitterschritt in ms: dx*u_lat/u_phys, u_phys = Re nu/Dh

def geom():
    w = np.zeros((Nz, Ny, Nx), np.uint8)
    for lane in (0, 1):
        for i in range(m_):
            x0 = lane*(bb+tr)+mrg0+i*pitch
            w[1:Ll+1, bl:bl+nh, x0:x0+nw] = 1; w[0, bl:bl+nh, x0:x0+nw] = 3 if lane == 0 else 4
    w[Ll+1:Ll+1+Lk, bl:bl+nh, 1:Nx-1] = 1
    return w

def rechnen():
    if tau < E["fx"]["tau_min"]: print("ABBRUCH tau"); sys.exit(2)
    if not probe and os.path.exists(f"{aus}/ergebnis.json"): print("fertig"); return
    if os.environ.get("RECHNEN_STOP") and os.path.exists(os.environ["RECHNEN_STOP"]): sys.exit(75)
    if subprocess.run("curl -s localhost:11434/api/ps | grep -q '\"name\"'", shell=True).returncode == 0: print("ollama belegt GPU"); sys.exit(76)
    w = geom(); shutil.rmtree(aus, ignore_errors=True); os.makedirs(f"{aus}/frames"); w.tofile(f"{aus}/geometrie.bin")
    steps = int(3*Nz/u0) if not probe else 2000; sa = steps//NFRAMES if not probe else 100
    nA_in = int((w[0] == 3).sum()); nfl = int((w > 0).sum())
    open(f"{aus}/fall.txt", "w").write(f"{aus}/geometrie.bin {aus} {Nx} {Ny} {Nz} {nu:.6g} {2*D:.6g} 0 {u0:.6g} {sa*(steps//sa)} {sa} 2 {xs} {za}\n")
    print("Gitter", Nx, Ny, Nz, "Zellen", Nx*Ny*Nz/1e6, "M, Schritte", steps, "Bild alle", sa, "dt_ms", dt_ms, flush=True)
    r = subprocess.run([f"{FXD}/bin/FluidX3D_film"], cwd=FXD, capture_output=True, text=True, env=dict(os.environ, TAUSCHER_FALL=f"{aus}/fall.txt", FX_Q_T="0.0", FX_Q_U0="0.0"))
    open(f"{aus}/fluidx3d.log", "w").write(r.stdout[-8000:]+r.stderr[-3000:])
    if r.returncode == 75: print("STOP"); sys.exit(75)
    if r.returncode: print("FluidX3D Fehler", r.returncode); sys.exit(1)
    auswerten(w, nA_in, sa)

def auswerten(w, nA_in, sa):
    F = np.array([[float(x) for x in l.split()[1:]] for l in open(f"{aus}/stat.txt") if l.startswith("#F")])
    t, fe, f1, f2 = F.T; soll = u0*nA_in; nan = bool(np.isnan(F).any())
    dur = Nz/u0; per = max(1, int(dur/(t[1]-t[0]))); k = len(t)-1
    drift = abs(f2[k]-f2[max(0, k-per)])/abs(f2[k]) if k >= per else None
    ff = np.load if False else None
    d = np.fromfile(f"{aus}/feld.bin", dtype=np.uint8)   # Felder: Lesen wie k3_fluidx3d.umlenk
    M = int(np.frombuffer(d[:8].tobytes(), np.uint64)[0]); idx = np.frombuffer(d[8:8+4*M].tobytes(), np.uint32)
    v = np.frombuffer(d[8+4*M:8+24*M].tobytes(), np.float32).reshape(M, 5)
    uz = np.zeros(Nx*Ny*Nz, np.float32); ux = uz.copy(); uz[idx] = v[:, 2]; ux[idx] = v[:, 0]
    fl = np.zeros(Nx*Ny*Nz, bool); fl[idx] = True; uz, ux, fl = [a.reshape(Nz, Ny, Nx) for a in (uz, ux, fl)]
    ym = Ny//2; cz = slice(Ll+1, Ll+1+Lk); fch = fl[cz, ym]; vel = np.hypot(ux[cz, ym], uz[cz, ym]); vm = vel[fch].mean()
    tot_k = float((vel[fch] < 0.1*vm).sum()/fch.sum())
    vb = np.abs(uz[1:Ll+1, ym]); fb = fl[1:Ll+1, ym]; tot_g = float((vel[fch] < 0.1*vm).sum()/(fch.sum()+fb.sum()))
    def kan(z):   # Fluss je Teilkanal der Rueckbahn in Ebene z
        return np.array([-uz[z][:, mrg0+i*pitch+bb+tr:mrg0+i*pitch+bb+tr+nw].sum() for i in range(m_)])
    out = dict(hinweis="KI-generiert (Claude Sonnet, 2026-11-21), Entwurf. Erzeugt von k3_film.py (ERWARTUNG.md Nachtrag 3).", probe=probe, gitter=[Nx, Ny, Nz], zellen_je_mm=zpm, Re=RE, tau=tau, u0=u0, dt_ms_je_schritt=dt_ms,
        bilder=len(t), schritte_gesamt=float(t[-1]), durchlaufzeiten=float(t[-1]*u0/Nz), nan=nan,
        punkt1_fluss_rueckbahn_zu_einlass=float(f2[-max(1, per//2):].mean()/soll), punkt1_fluss_hinbahn_zu_einlass=float(f1[-max(1, per//2):].mean()/soll), punkt1_fluss_einlassebene_zu_soll=float(fe[-1]/soll),
        punkt1_soll_toleranz=0.05, stationaer_aenderung_rueckbahn_letzte_durchlaufzeit=drift,
        punkt2_totzone_anteil_kammer=tot_k, punkt2_totzone_anteil_gesamt=tot_g, punkt2_soll_kammer=0.15, punkt2_soll_gesamt=0.05)
    k1 = kan(Ll-c(4)); out["punkt3_kanalfluss_rel_nach_umlenkung"] = (k1/k1.mean()).round(3).tolist()
    k2 = kan(za); out["punkt3_kanalfluss_rel_in_messebene_z"+str(za)] = (k2/k2.mean()).round(3).tolist(); out["punkt3_soll"] = "Innen bis +20 %, Aussen -20 %, gleicht sich nach ~20 Kanalhoehen aus"
    json.dump(out, open(f"{aus}/ergebnis.json", "w"), indent=1, ensure_ascii=False); print(json.dumps(out, ensure_ascii=False))
    os.remove(f"{aus}/feld.bin") if not probe else None


# ---------------- Darstellung ----------------
def cmap(a, stops):
    xs_ = np.linspace(0, 1, len(stops)); s = np.array(stops, float)
    return np.stack([np.interp(a, xs_, s[:, i]) for i in range(3)], -1).astype(np.uint8)
VIR = [(68, 1, 84), (59, 82, 139), (33, 145, 140), (94, 201, 98), (253, 231, 37)]
INF = [(0, 0, 4), (87, 16, 110), (188, 55, 84), (249, 142, 9), (252, 255, 164)]
def fnt(s, b=False):
    for p in (f"/usr/share/fonts/truetype/dejavu/DejaVuSans{'-Bold' if b else ''}.ttf",):
        if os.path.exists(p): return ImageFont.truetype(p, s)
    return ImageFont.load_default()
W_, H_ = 1920, 1080; SC = 0.80; FW, FH = int(Nx*SC*0.9), int(Nz*SC*0.9)   # Feld 1224 x 664
def rahmen(art, k, nk, t_ms, fld, p_xy, erg):
    im = Image.new("RGB", (W_, H_), (24, 26, 30)); d = ImageDraw.Draw(im)
    titel = {"v": "Durchströmung der Kühlplatte: Geschwindigkeit", "T": "Durchströmung der Kühlplatte: Temperatur bei beheizter Wand"}[art]
    d.text((30, 14), titel, font=fnt(34, True), fill="white")
    d.rectangle((30, 62, 1000, 100), fill=(120, 20, 20)); d.text((38, 68), "KI-generiert (Claude Sonnet), Entwurf, nicht freigegeben", font=fnt(24, True), fill="white")
    x0, y0 = 30, 115; FWd = 1250; FHd = int(FWd*Nz/Nx)
    im.paste(fld.resize((FWd, FHd), Image.NEAREST), (x0, y0))
    for (px, pz) in p_xy:
        X, Y = x0+px*FWd/Nx, y0+pz*FHd/Nz; d.ellipse((X-2, Y-2, X+2, Y+2), fill=(255, 255, 255))
    d.rectangle((x0-1, y0-1, x0+FWd, y0+FHd), outline=(200, 200, 200))
    # Beschriftungen im Feld
    f = fnt(20, True); d.text((x0+10, y0+6), "Bahn 1 (hin, Einlass oben)", font=f, fill="white"); d.text((x0+FWd//2+60, y0+6), "Bahn 2 (zurück, Auslass oben)", font=f, fill="white")
    d.text((x0+FWd//2-110, y0+FHd-30), "Umlenkkammer", font=f, fill="white")
    # Farbbalken rechts
    bx = x0+FWd+60; by = y0; bh = 460; g = np.linspace(1, 0, bh)[:, None]*np.ones((1, 40))
    cb = cmap(g, VIR if art == "v" else INF); im.paste(Image.fromarray(cb), (bx, by)); d.rectangle((bx-1, by-1, bx+40, by+bh), outline="white")
    for val in ([0, 0.5, 1.0, 1.5, 2.0, 2.5] if art == "v" else [0, 0.25, 0.5, 0.75, 1.0]):
        mx = 2.5 if art == "v" else 1.0; yy = by+bh-int(val/mx*bh); d.line((bx+40, yy, bx+50, yy), fill="white"); d.text((bx+56, yy-10), f"{val:g}", font=fnt(20), fill="white")
    d.text((bx-5, by-34), "u / ū (ū = mittlere Kanalgeschw.)" if art == "v" else "T (0 = Eintritt, 1 = Wand)", font=fnt(17), fill="white")
    d.text((bx-5, by+bh+14), f"Zeit {t_ms:7.1f} ms", font=fnt(30, True), fill=(255, 220, 90))
    d.text((bx-5, by+bh+56), f"Bild {k+1}/{nk}", font=fnt(20), fill="white")
    d.text((bx-5, by+bh+90), f"Durchfluss Rückbahn / Einlass:\n{100*erg['punkt1_fluss_rueckbahn_zu_einlass']:.1f} % (Soll 100 ± 5 %)" if erg else "", font=fnt(20), fill=(140, 230, 140))
    ly = y0+FHd+14
    txt = ("Lesehilfe: Draufsicht in halber Kanalhöhe. Helle Farbe = schnell; weiße Punkte = mitgeschwommene Teilchen. Das Wasser-Glykol-Gemisch tritt oben in Bahn 1 ein, läuft nach unten, wird in der Kammer\n"
           "umgelenkt und kehrt in Bahn 2 zurück. Re = 200 im Film (im Betrieb Re ≈ 760): bei 4 Zellen/mm lässt sich Re 760 nicht stabil rechnen; die Strömung bleibt laminar, das Bild ist qualitativ.\n"
           "Dunkle Bereiche in der Umlenkkammer (besonders außen) sind Totzonen mit kaum Strömung; die Zahlen dazu stehen in ergebnis_film.json." if art == "v" else
           "Lesehilfe: Draufsicht in halber Kanalhöhe. Die Kanalwand ist heiß (T = 1), das Fluid tritt kalt (T = 0) ein: Die warme Randschicht (hell) wächst entlang der Bahn. Die Umlenkung mischt sie auf.\n"
           "Re = 200 im Film (im Betrieb Re ≈ 760): bei 4 Zellen/mm lässt sich Re 760 nicht stabil rechnen. Temperatur nur qualitativ, nicht auf den Betrieb übertragbar (Pr im Modell 1, real etwa 25).\n"
           "Wo das Fluid fast stillsteht (Totzonen in der Kammer), nimmt es besonders viel Wandwärme auf.")
    d.multiline_text((30, ly), txt, font=fnt(17), fill=(220, 220, 220), spacing=4)
    d.text((30, H_-34), "KI-generiert (Claude Sonnet, 2026-11-21), Entwurf. Quelle: sim/kuehlung/k3_gesamt/lauf_film/ (FluidX3D, geänderte Fassung, Lizenz siehe fluidx3d/LICENSE.md)", font=fnt(16), fill=(170, 170, 170))
    return im

def bild(dirn=None):
    dirn = dirn or aus; erg = json.load(open(f"{dirn}/ergebnis.json")); w = np.fromfile(f"{dirn}/geometrie.bin", np.uint8).reshape(Nz, Ny, Nx)
    solid = w[:, Ny//2, :] == 0; fr = sorted(os.listdir(f"{dirn}/frames")); nk = len(fr); sa = int(erg["schritte_gesamt"]/nk)
    rng = np.random.default_rng(1); inl = np.where(w[0, Ny//2] == 3)[0]
    def seed(n): return np.stack([rng.choice(inl, n)+rng.random(n), 1+rng.random(n)*c(40)], 1)
    P = seed(1500); outd = f"{dirn}/png"; os.makedirs(outd, exist_ok=True)
    for k, fn in enumerate(fr):
        b = np.fromfile(f"{dirn}/frames/{fn}", np.uint8).reshape(Nz, Nx, 3).astype(np.float32)
        uxf, uzf, Tf = (b[..., 0]-128)/127*3*u0, (b[..., 1]-128)/127*3*u0, b[..., 2]/255
        sp = np.hypot(uxf, uzf)/u0
        iv = cmap(np.clip(sp/2.5, 0, 1), VIR); iv[solid] = (70, 70, 70)
        it = cmap(np.clip(Tf, 0, 1), INF); it[solid] = (70, 70, 70)
        ix = np.clip(P[:, 0].astype(int), 0, Nx-1); iz = np.clip(P[:, 1].astype(int), 0, Nz-1)
        for _ in range(4):   # sa Schritte in 4 Teilschritten
            ix = np.clip(P[:, 0].astype(int), 0, Nx-1); iz = np.clip(P[:, 1].astype(int), 0, Nz-1)
            P[:, 0] += uxf[iz, ix]*sa/4; P[:, 1] += uzf[iz, ix]*sa/4
        ix = np.clip(P[:, 0].astype(int), 0, Nx-1); iz = np.clip(P[:, 1].astype(int), 0, Nz-1)
        bad = solid[iz, ix] | (P[:, 1] < 0) | (P[:, 1] >= Nz-1)
        bad |= (rng.random(len(P)) < 0.004)
        if bad.any(): P[bad] = seed(int(bad.sum()))
        t_ms = (k+1)*sa*dt_ms; last = (k == nk-1)
        for art, img in (("v", iv), ("T", it)):
            rahmen(art, k, nk, t_ms, Image.fromarray(img), P, erg).save(f"{outd}/{art}_{k:04d}.png")
    for art, name in (("v", "geschwindigkeit"), ("T", "temperatur")):
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-i", f"{outd}/{art}_%04d.png", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", f"{H}/k3_durchstroemung_{name}.mp4"], check=True)
        shutil.copy(f"{outd}/{art}_{nk-1:04d}.png", f"{H}/k3_durchstroemung_{name}.png")
    shutil.copy(f"{dirn}/ergebnis.json", f"{H}/ergebnis_film.json" if "probe" not in dirn else f"{outd}/ergebnis_probe.json")
    print("Film fertig", nk, "Bilder, dt_ms", dt_ms)

if __name__ == "__main__":
    {"rechnen": rechnen, "bild": bild}[sys.argv[1]]()
