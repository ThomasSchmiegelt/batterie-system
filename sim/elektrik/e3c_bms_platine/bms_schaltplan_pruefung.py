#!/usr/bin/env python3
"""Vergleicht die Netzliste des Schaltplans (kicad-cli sch export netlist) mit der des Layouts (bms.kicad_pcb, Pads je Netz) und mit bms_teile.json.
Vergleich als Zerlegung der Pins in Netze (Netznamen dürfen sich bei unbenannten Netzen unterscheiden). KI-generiert (Claude Sonnet, 2026-11-24).
Aufruf: python3 bms_schaltplan_pruefung.py (nach bms_schaltplan.py, erc, netzliste, pcb-Auszug) -> ergebnis_schaltplan.json"""
import json, subprocess, pathlib, xml.etree.ElementTree as ET
H = pathlib.Path(__file__).resolve().parent; S = pathlib.Path("/home/cae/cae_projekte/batterie/e3c/schaltplan"); W = "/home/cae/hermes/batterie/werkzeuge"
subprocess.run([f"{W}/kicad-cli.sh", "sch", "export", "netlist", "--format", "kicadxml", "-o", str(S / "netz_sch.xml"), str(S / "bms_schaltplan.kicad_sch")], check=True, capture_output=True)
subprocess.run([f"{W}/kicad-cli.sh", "sch", "erc", "--format", "json", "--severity-all", "-o", str(S / "erc.json"), str(S / "bms_schaltplan.kicad_sch")], capture_output=True)
erc = json.load(open(S / "erc.json")); nerc = sum(len(s["violations"]) for s in erc["sheets"])
sch = {}
for n in ET.parse(S / "netz_sch.xml").getroot().iter("net"):
    pins = frozenset((x.get("ref"), x.get("pin")) for x in n.iter("node"))
    if len(pins) > 1: sch[pins] = n.get("name")
tl = json.load(open(H / "bms_teile.json"))["teile"]; q = {}
for t in tl:
    for p, n in t["pins"].items():
        if n: q.setdefault(n, set()).add((t["ref"], p))
quelle = {frozenset(v) for v in q.values() if len(v) > 1}
subprocess.run(["bash", f"{W}/kicad-python.sh", str(H / "bms_pcb_netze.py")], check=True, capture_output=True)
pcb = {frozenset(map(tuple, v)) for v in json.load(open("/home/cae/cae_projekte/batterie/e3c/pcb_netze.json")).values() if len(v) > 1}
A = set(sch)
def diff(a, b): return dict(nur_in_a=len(a - b), nur_in_b=len(b - a))
res = dict(erc_verstoesse=nerc, netze_schaltplan=len(A), netze_quelle=len(quelle), netze_layout=len(pcb), schaltplan_vs_quelle=diff(A, quelle), schaltplan_vs_layout=diff(A, pcb),
           teile_schaltplan=len({r for k in A for r, _ in k}), teile_quelle=len(tl), quelle="/home/cae/cae_projekte/batterie/e3c/schaltplan/netz_sch.xml, erc.json, pcb_netze.json, bms_teile.json")
json.dump(res, open(H / "ergebnis_schaltplan.json", "w"), indent=1, ensure_ascii=False); print(json.dumps(res, ensure_ascii=False))
