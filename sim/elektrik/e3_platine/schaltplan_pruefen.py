#!/usr/bin/env python3
"""E3: vergleicht die Netzliste des Schaltplans (kicad-cli sch export netlist) mit der Layout-Netzliste cmu_<V>.net (SKiDL). Verglichen wird die Verbindungsstruktur (Menge der Pin-Gruppen je Netz, Referenz + Pinnummer), nicht die Netznamen.
KI-generiert (Claude Sonnet, 2026-11-24), Entwurf. Ausgabe: ergebnis_schaltplan.json"""
import re, json, subprocess, pathlib
H = pathlib.Path(__file__).resolve().parent; O = pathlib.Path("/home/cae/cae_projekte/batterie/e3"); K = "/home/cae/hermes/batterie/werkzeuge/kicad-cli.sh"
def sexp(t):
    tok = re.findall(r'"(?:[^"\\]|\\.)*"|\(|\)|[^\s()"]+', t); pos = 0
    def rd():
        nonlocal pos
        x = tok[pos]; pos += 1
        if x == "(":
            l = []
            while tok[pos] != ")": l.append(rd())
            pos += 1; return l
        return x.strip('"')
    return rd()
def nets(f):
    t = sexp(pathlib.Path(f).read_text()); out = {}
    def walk(n):
        if isinstance(n, list):
            if n and n[0] == "net" and any(isinstance(c, list) and c[0] == "node" for c in n):
                name = [c for c in n if isinstance(c, list) and c[0] == "name"][0][1]
                out[name] = frozenset((c[1][1], c[2][1]) for c in n if isinstance(c, list) and c[0] == "node")
            for c in n: walk(c)
    walk(t); return out
erg = {}
for V in ("LFP", "NMC"):
    sch = O / f"schaltplan_{V}" / f"cmu_{V}.kicad_sch"; netz = O / f"schaltplan_{V}" / f"cmu_{V}_sch.net"
    subprocess.run([K, "sch", "export", "netlist", "--format", "kicadsexpr", "-o", str(netz), str(sch)], capture_output=True)
    ej = O / f"schaltplan_{V}" / "erc.json"; subprocess.run([K, "sch", "erc", "--severity-all", "--format", "json", "-o", str(ej), str(sch)], capture_output=True); vl = [v for s_ in json.load(open(ej))["sheets"] for v in s_["violations"]]
    a = nets(netz); b = nets(H / f"cmu_{V}.net")
    ga = {g for g in a.values() if len(g) >= 2}; gb = {g for g in b.values() if len(g) >= 2}
    ra = {r for g in a.values() for r, p in g}; rb = {r for g in b.values() for r, p in g}
    erg[V] = dict(netze_schaltplan=len(ga), netze_layout=len(gb), nur_im_schaltplan=len(ga - gb), nur_im_layout=len(gb - ga), teile_schaltplan=len(ra), teile_layout=len(rb),
                  beispiele_abweichung=[sorted(g)[:6] for g in list(ga ^ gb)[:3]], gleich=(ga == gb), erc_fehler=sum(v['severity'] == 'error' for v in vl), erc_warnungen=sum(v['severity'] == 'warning' for v in vl))
    print(V, erg[V])
json.dump(erg, open(H / "ergebnis_schaltplan.json", "w"), indent=1, ensure_ascii=False)
