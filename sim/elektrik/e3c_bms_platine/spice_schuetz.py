#!/usr/bin/env python3
"""E3c N1 (OPT-006): Schützspule mit Sparschaltung, SPICE (ngspice 42, CPU). KI-generiert (Claude Sonnet, 2026-11-24), Entwurf.
Werte nur aus ERWARTUNG.md Nachtrag 1 (ERW-E3c N1): 12 V, Spule 8 Ohm / 50 mH, Anzug 100 ms voller Strom, Halten 0,3 x I_Anzug per PWM 20 kHz, Abfallstrom 0,15 x I_Anzug, Zener 36 V.
Nicht in der Erwartung (generisch, nur für die Rechnung): Schalter Ron 1 mOhm / Roff 1 GOhm, Diodenmodell IS=1e-10 RS=0,05 N=1,2, Halten dauert 100 ms (bis 0,2 s) vor dem Öffnen.
Topologie: HS-Schalter taktet; Freilaufdiode D_PWM von GND (hinter dem Low-Side-FET) auf das HS-Ende der Spule; Löschpfad Spulenende N -> D_FREI -> Zener (36 V) -> GND.
Fälle: Zener = Löschung über D_FREI + Zener; nur Freilauf = Zener durch Kurzschluss ersetzt (nur Dioden). Öffnen aus dem Halten (t=0,2 s) und aus dem Anzug (t=0,1 s, Worst Case)."""
import json, subprocess, pathlib, numpy as np
H = pathlib.Path(__file__).resolve().parent
U, R, L, TA, FPWM, KH, KA, UZ = 12.0, 8.0, 0.05, 0.1, 20000.0, 0.3, 0.15, 36.0
IA = U / R; IH = KH * IA; IFALL = KA * IA; DUTY = KH           # Dauer-Tastverhältnis im Halten: D*U = I_Halt*R -> D = 0,3 (Folge der Annahmen)
def lauf(name, zener, t_open, t_end, DUTY=DUTY):
    zz = f"DZ 0 z DZM\n.model DZM D(IS=1e-10 RS=0.05 N=1.2 BV={UZ} IBV=1e-3)" if zener else "VZ z 0 DC 0"
    (H / f"schuetz_{name}.cir").write_text(f"""* Schuetzspule Sparschaltung {name} (KI-generiert, Sonnet 2026-11-24)
VB vb 0 DC {U}
Bhs chs 0 V = (time < {TA}) ? 1 : ((time < {t_open}) ? ((time*{FPWM} - floor(time*{FPWM})) < {DUTY} ? 1 : 0) : 0)
Bls cls 0 V = (time < {t_open}) ? 1 : 0
SHS vb p chs 0 SW
SLS n 0 cls 0 SW
.model SW SW(Vt=0.5 Vh=0.1 Ron=0.001 Roff=1e9)
RL p m {R}
LL m n {L} ic=0
DPWM 0 p DD
DFREI n z DD
.model DD D(IS=1e-10 RS=0.05 N=1.2)
{zz}
.tran 0.5u {t_end} 0 0.5u uic
.control
run
wrdata {H}/schuetz_{name}.dat i(LL) v(n) v(p)
.endc
.end
""")
    subprocess.run(["nice", "-n", "10", "ngspice", "-b", str(H / f"schuetz_{name}.cir")], check=True, capture_output=True)
    a = np.loadtxt(H / f"schuetz_{name}.dat"); return a[:, 0], a[:, 1], a[:, 3], a[:, 5]
def i_mittel(d):   # mittlerer Haltestrom (letzte 5 ms vor dem Öffnen), Zener-Fall, kurzer Lauf
    t_, i_, _, _ = lauf("kal", True, 0.2, 0.2005, d); return float(i_[(t_ >= 0.195) & (t_ < 0.2)].mean())
lo, hi = 0.2, 0.6
for _ in range(9):
    mid = (lo + hi) / 2
    if i_mittel(mid) < IH: lo = mid
    else: hi = mid
DKAL = (lo + hi) / 2   # Tastverhältnis nachgeregelt (Stromregelung über den Spulenstrom-Shunt), damit der Mittelwert 0,45 A erreicht (Duty ist Stellgröße, nicht Annahme)
DUTY0 = DUTY; DUTY = DKAL
res = {"annahmen": dict(U_V=U, R_Ohm=R, L_H=L, Anzugzeit_s=TA, PWM_Hz=FPWM, Halten_Faktor=KH, Abfall_Faktor=KA, Zener_V=UZ, Tastverhaeltnis_nachgeregelt=DKAL, Tastverhaeltnis_ohne_Regelung_U_R=DUTY0, I_Anzug_A=IA, I_Halt_soll_A=IH, I_Abfall_A=IFALL, quelle="ERWARTUNG.md Nachtrag 1 (ERW-E3c N1); Tastverhältnis ohne Regelung = I_Halt*R/U = 0,3; mit Diodenabfall im Freilauf nachgeregelt auf Mittelwert 0,45 A")}
daten = {}
for name, zener, to, te in (("zener_halten", True, 0.2, 0.26), ("freilauf_halten", False, 0.2, 0.28), ("zener_anzug", True, 0.1, 0.16), ("freilauf_anzug", False, 0.1, 0.18)):
    t, i, vn, vp = lauf(name, zener, to, te, DUTY); daten[name] = (t, i, vn, to)
    pre = (t >= to - 0.05) & (t < to)
    iw = i[(t >= to - 0.005) & (t < to)]; post = (t >= to)
    k = np.where(post & (i <= IFALL))[0]; tf = float(t[k[0]] - to) if len(k) else None
    k5 = np.where(post & (i <= 0.05 * IA))[0]
    d = dict(zener=zener, t_open_s=to, i_max_A=float(i[t < to].max()), t_fall_bis_0_15_ms=None if tf is None else 1e3 * tf, v_n_max_V=float(vn[post].max()), i_bei_oeffnen_A=float(i[np.searchsorted(t, to) - 1]), E_zener_J=float(np.trapezoid(np.where(post, np.clip(vn - 0, 0, None) * i, 0), t)) if zener else None)
    if name.endswith("halten"):
        d.update(i_halt_mittel_A=float(iw.mean()), i_halt_min_A=float(iw.min()), i_halt_max_A=float(iw.max()), welligkeit_pp_rel=float((iw.max() - iw.min()) / iw.mean()), P_halt_Spule_W=float(np.mean(iw ** 2) * R),
                 P_anzug_Spule_W=IA ** 2 * R, P_einsparung_rel=float(1 - np.mean(iw ** 2) * R / (IA ** 2 * R)), P_halt_Speisung_W=float(U * np.mean(np.where(True, iw, 0)) * 0 + np.mean(iw) * U * 0 + 0))
    res[name] = d
del_keys = [r for r in res if isinstance(res[r], dict) and "P_halt_Speisung_W" in res[r]]
for r in del_keys: res[r].pop("P_halt_Speisung_W")
res["erwartung_N1"] = dict(haltestrom_A=0.45, haltestrom_toleranz=0.10, welligkeit_max=0.10, P_halt_W=1.6, abfall_zener_ms=[2, 4], abfall_freilauf_ms=[30, 40], abbruch="Abfallzeit mit Zener > 10 ms")
res["abgleich"] = dict(
    n1_1_haltestrom_ok=abs(res["zener_halten"]["i_halt_mittel_A"] / IH - 1) <= 0.10, n1_1_welligkeit_ok=res["zener_halten"]["welligkeit_pp_rel"] < 0.10,
    n1_2_zener_abfall_ms_halten=res["zener_halten"]["t_fall_bis_0_15_ms"], n1_2_zener_abfall_ms_anzug=res["zener_anzug"]["t_fall_bis_0_15_ms"],
    n1_2_freilauf_abfall_ms_halten=res["freilauf_halten"]["t_fall_bis_0_15_ms"], n1_2_freilauf_abfall_ms_anzug=res["freilauf_anzug"]["t_fall_bis_0_15_ms"],
    abbruch_zener_ueber_10ms=bool(max(res["zener_halten"]["t_fall_bis_0_15_ms"], res["zener_anzug"]["t_fall_bis_0_15_ms"]) > 10))
res["herkunft"] = "ngspice 42, spice_schuetz.py; Werte ERWARTUNG.md N1; generische Schalter-/Diodenmodelle (Kopfzeile des Skripts)"
dec = lambda x, n=4: [round(float(v), n) for v in x]
for nm, (t, i, vn, to) in daten.items():
    m = (t >= to - 0.0015) & (t <= to + (0.012 if "zener" in nm else 0.05)); step = 1 if "zener" in nm else 4
    res[nm]["zoom_t_ms"] = dec(1e3 * (t[m][::step] - to), 4); res[nm]["zoom_i_A"] = dec(i[m][::step], 5)
t, i, vn, to = daten["zener_halten"]; res["verlauf_zener_halten"] = dict(t_s=dec(t[::200], 5), i_A=dec(i[::200], 5))
m = (t >= 0.19) & (t < 0.1925); res["pwm_zoom"] = dict(t_ms=dec(1e3 * t[m], 4), i_A=dec(i[m], 5))
json.dump(res, open(H / "ergebnis_schuetz.json", "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k in ("abgleich",)}, indent=1)); print({k: round(v, 4) if isinstance(v, float) else v for k, v in res["zener_halten"].items() if not isinstance(v, list)})
