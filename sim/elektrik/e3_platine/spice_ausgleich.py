#!/usr/bin/env python3
"""E3 Ausgleichskreis, SPICE (ngspice). KI-generiert (Claude Sonnet, 2026-11-24), Entwurf.
Werte: ERWARTUNG.md (ERW-E3) bzw. sim/elektrik/e2_elektronik/ergebnis.json. Generisches FET-Modell Level 1, kein Herstellermodell.
Aufruf: source umgebung.sh; nice python3 spice_ausgleich.py"""
import json, subprocess, pathlib, numpy as np
H = pathlib.Path(__file__).resolve().parent
E2 = json.load(open(H.parent / "e2_elektronik/ergebnis.json"))
# Annahmen ERW-E3 (Tabelle "Annahmen Opus"): Widerstände, Herkunft ENT-171/172
VAR = {"LFP": dict(R1=47.0, R2=47.0, Umax=3.65, Unenn=3.2),
       "NMC": dict(R1=64.9, R2=64.9, Umax=4.2, Unenn=3.7)}
# FET Level 1: R_DS,on = 0,5 Ohm (Obergrenze ERW-E3) bei U_GS = 5 V (Modellwahl, offene Frage). KP*W/L*(5-1,5) = 1/0,5
FET = ".model NFET NMOS (LEVEL=1 VTO=1.5 KP=0.2 LAMBDA=0)"
W_L = 1 / (0.5 * 0.2 * 3.5)   # W/L so, dass R_DS,on = 0,5 Ohm im linearen Bereich bei 5 V
def netz(v, p):
    return f"""* Ausgleichskanal {v} (KI-generiert, Sonnet 2026-11-24)
Vz z 0 DC {p['Umax']}
R1 z d {p['R1']}
R2 z d {p['R2']}
M1 d g 0 0 NFET W={W_L:.4f}u L=1u
Vg g 0 DC 5
{FET}
.dc Vz {p['Unenn']-0.2:.3f} {p['Umax']} 0.05
.control
run
set wr_vecnames
wrdata {H}/ausgleich_{v}.dat i(Vz) v(d)
.endc
.end
"""
res = {}
for v, p in VAR.items():
    f = H / f"ausgleich_{v}.cir"; f.write_text(netz(v, p))
    subprocess.run(["nice", "-n", "10", "ngspice", "-b", str(f)], check=True, capture_output=True)
    a = np.loadtxt(H / f"ausgleich_{v}.dat", skiprows=1)
    U = a[:, 0]; I = -a[:, 1]; Ud = a[:, 3]   # Zeile: u, i, u, v(d)
    Rpar = p['R1'] * p['R2'] / (p['R1'] + p['R2'])
    P_R = (U - Ud) ** 2 / (p['R1'] * 1.0)  # Leistung in R1 (R1=R2)
    P_R = (U - Ud) ** 2 / p['R1']; P_FET = Ud * I; P_K = U * I
    def at(x, y): return float(np.interp(x, U, y))
    dQ = E2[v]["ausgleich_dQ_Ah"]; Ium = at(p['Umax'], I); Inn = at(p['Unenn'], I); Imit = at((p['Umax'] + p['Unenn']) / 2, I)
    res[v] = dict(R_parallel_Ohm=Rpar, I_Umax_A=Ium, I_Unenn_A=Inn, I_mittel_A=Imit, U_Unenn_V=p['Unenn'], U_Umax_V=p['Umax'],
        P_Kanal_Umax_W=at(p['Umax'], P_K), P_Widerstand_je_Umax_W=at(p['Umax'], P_R), P_FET_Umax_W=at(p['Umax'], P_FET),
        P_Widerstand_Ausnutzung_Umax=at(p['Umax'], P_R) / 1.0,
        P_CMU_18_Umax_W=18 * at(p['Umax'], P_K), P_CMU_E2_W=E2[v]["cmu_W_alle_kanaele_umax"],
        dQ_Ah=dQ, t_E2_h=E2[v]["ausgleich_h"], t_Umax_h=dQ / Ium, t_Unenn_h=dQ / Inn, t_mittel_h=dQ / Imit,
        verlaengerung_mittel_prozent=100 * (Ium / Imit - 1), verlaengerung_Unenn_prozent=100 * (Ium / Inn - 1),
        kennlinie=dict(U_V=U.tolist(), I_A=I.tolist(), P_kanal_W=P_K.tolist(), P_FET_W=P_FET.tolist()),
        herkunft="ngspice 42, Level-1-FET, U_GS = 5 V (Modellwahl); Widerstände ERW-E3/ENT-171,172; dQ,t_E2: e2_elektronik/ergebnis.json")
    res[v]["P_CMU_Abweichung_E2_prozent"] = 100 * (res[v]["P_CMU_18_Umax_W"] / res[v]["P_CMU_E2_W"] - 1)
json.dump(res, open(H / "ergebnis_ausgleich.json", "w"), indent=1, ensure_ascii=False)
for v in res: print(v, {k: round(x, 4) for k, x in res[v].items() if isinstance(x, float)})
