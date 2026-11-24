# Im KiCad-Flatpak: uebertragen LFP -> NMC. KI-generiert (Claude Sonnet, 2026-11-24), Entwurf.
# Begründung: Netzliste, Footprints und Platzierung beider Varianten sind gleich, nur Werte (Ausgleichs-R 47 / 64,9 Ohm, OVP-Schwelle) unterscheiden sich (cmu_<V>_teile.json).
# Die Router-Läufe für NMC blieben bei 2 offen (Lauf 10, vier Wiederholungen), LFP war vollständig. Übertragen: geroutetes LFP-Board laden, Werte nach NMC setzen, speichern.
import json, pcbnew
H = "/home/cae/hermes/batterie/sim/elektrik/e3_platine"; D = "/home/cae/cae_projekte/batterie/e3/route"
a = json.load(open(f"{H}/cmu_LFP_teile.json"))["teile"]; n = {t["ref"]: t for t in json.load(open(f"{H}/cmu_NMC_teile.json"))["teile"]}
assert all(t["pins"] == n[t["ref"]]["pins"] and t["footprint"] == n[t["ref"]]["footprint"] for t in a)
b = pcbnew.LoadBoard(f"{D}/cmu_LFP_geroutet.kicad_pcb"); k = 0
for fp in b.GetFootprints():
    v = n[fp.GetReference()]["value"][:40]
    if fp.GetValue() != v: fp.SetValue(v); k += 1
b.Save(f"{D}/cmu_NMC_geroutet.kicad_pcb"); print("Werte geändert", k)
