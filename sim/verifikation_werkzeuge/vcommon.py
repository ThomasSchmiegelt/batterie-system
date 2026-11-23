"""KI-generiert (Claude Sonnet, 2026-11-23), Entwurf. Gemeinsame Helfer QN1 (Eingaben, Ordnung, Ergebnis schreiben)."""
import json, math, os
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(os.path.join(H, "../.."))
E = json.load(open(f"{H}/eingaben.json"))
def w(n): return E[n]["wert"]
TOL = w("toleranz")
def ordnung(h, err):
    """beobachtete Ordnung zwischen aufeinanderfolgenden Stufen: p = ln(e1/e2)/ln(h1/h2); err als Betrag"""
    return [math.log(err[i]/err[i+1])/math.log(h[i]/h[i+1]) if err[i] > 0 and err[i+1] > 0 else None for i in range(len(h)-1)]
def speichere(fall, d):
    json.dump(d, open(f"{H}/ergebnis_{fall}.json", "w"), indent=1)
    print(fall, json.dumps({k: v for k, v in d.items() if k in ("bestanden", "abweichung_fein_pct", "ordnung_beobachtet")}))
