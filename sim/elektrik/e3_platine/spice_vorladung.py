#!/usr/bin/env python3
"""E3 Vorladung bei 912 V, SPICE (ngspice). KI-generiert (Claude Sonnet, 2026-11-24), Entwurf.
Werte: ERWARTUNG.md (ERW-E3): U = 912 V (LFP U_max Pack), C_ZK = 1000 uF, R = 100 Ohm (ERW-E2)."""
import json, subprocess, pathlib, numpy as np
H = pathlib.Path(__file__).resolve().parent
U, C, R = 912.0, 1e-3, 100.0
(H / "vorladung.cir").write_text(f"""* Vorladung (KI-generiert, Sonnet 2026-11-24)
V1 a 0 DC {U}
R1 a c {R}
C1 c 0 {C} ic=0
.tran 1m 1.5 uic
.control
run
wrdata {H}/vorladung.dat i(V1) v(c)
.endc
.end
""")
subprocess.run(["nice", "-n", "10", "ngspice", "-b", str(H / "vorladung.cir")], check=True, capture_output=True)
a = np.loadtxt(H / "vorladung.dat"); t = a[:, 0]; i = -a[:, 1]; uc = a[:, 3]
iR = i; Pr = iR ** 2 * R; E = float(np.trapezoid(Pr, t))
t95 = float(np.interp(0.95 * U, uc, t))
res = dict(U_V=U, C_F=C, R_Ohm=R, I_spitze_A=float(i.max()), E_Widerstand_J=E, E_Kondensator_J=float(0.5 * C * uc[-1] ** 2),
    t_95_ms=1e3 * t95, tau_ms=1e3 * R * C, u_C_Ende_V=float(uc[-1]), t_Ende_s=float(t[-1]),
    Anforderung_Puls_J=450.0, Puls_ok=bool(E <= 450.0), E_800V_J=0.5 * C * 800 ** 2,
    t=t[::5].tolist(), i_A=i[::5].tolist(), uC_V=uc[::5].tolist(),
    herkunft="ngspice 42; U=912 V (ERW-E3 Erwartung 4), C, R aus ERW-E2/ERW-E3; Anforderung 450 J: ERW-E3 BT-712")
json.dump(res, open(H / "ergebnis_vorladung.json", "w"), indent=1)
print({k: round(x, 4) if isinstance(x, float) else x for k, x in res.items() if not isinstance(x, list)})
