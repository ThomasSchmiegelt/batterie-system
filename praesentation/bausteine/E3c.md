> **KI-generiert** (Claude Sonnet, 2026-11-24), Entwurf. Folienbaustein Vorgang E3c.

# Die BMS-Platine trennt Hochvolt und Niedervolt durch einen kupferfreien Streifen
**Kernaussage: Die BMS-Platine (160 x 100 mm, 131 Teile) ist vollständig geroutet, DRC 0, und trennt Hochvolt und Niedervolt durch eine 10 mm breite Sperrzone (gemessen 10,4 mm).**

**Bild:** sim/elektrik/e3c_bms_platine/platine_bms_explosion.png (Sperrzone rot, Soll 10 mm beschriftet); sim/elektrik/e3c_bms_platine/platine_bms_einbau.png (Zielband: Platz BT-310); Schaltplan mit Drähten und HV/NV-Rahmen: sim/elektrik/e3c_bms_platine/schaltplan_bms.pdf

**Zahlen** (Quelle sim/elektrik/e3c_bms_platine/ergebnis_platine.json, ergebnis_schaltplan.json):
- Platine 160 x 100 mm, 4 Lagen, 131 Teile, Masse 66,54 g
- Kupferabstand NV/HV 10,4 mm, nur 4 Teile überbrücken (Übertrager, Isolatoren)
- Schaltplan: ERC 0 Verstöße, Netzliste gleich Layout (98 Netze)
- Platine im Pack-STEP: LFP und NMC je 0 Kollisionen (cad/pack/entwurf/ergebnis_<V>_e2d_e3c.json)
- Servicedeckel LFP: 0 Kollisionen (cad/pack/entwurf/ergebnis_LFP_e2d_e3.json)
- Passivwerte offen; Bericht sim/elektrik/e3c_bms_platine/ERGEBNIS.md

*KI-generiert, Entwurf.*
