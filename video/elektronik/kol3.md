**Storyboard: Batterie, Nachverfolgung, Normen, Elektronik (Nachtrag 1)**

**Szene 1: Anforderungen (25s)**
Bild: sim/elektrik/e3d_fmeda/e3d_fmeda.png
Tafeln:
1. Anforderungen Pkw Fahrzeugmasse 1500 kg [REQ-P01]
2. Systemspannung 720 880 V [REQ-P03]
3. Dauerleistung 60 kW [REQ-P04]
4. Schnellladen LFP 20 min NMC 30 min [REQ-P05]
5. Normen ISO 26262 IEC 60664-1 CISPR 25 [docs/07]

**Szene 2: Wissensgraph wächst (parallel, gesamte Filmdauer)**
Kein eigenes Bild; `video/graph_zeitraffer.py` läuft im Hintergrund weiter.
Keine Tafeln; Wachstum sichtbar.

**Szene 3: Zelle (25s)**
Bild: sim/chemie/c1_zellmodell/ladekurve.png
Tafeln:
1. Zelle LFP prismatisch Blade [REQ-P06]
2. Ladekurve DCIR Wärme [sim/chemie/c1_zellmodell]
3. Zelltemperatur Spreizung 5 K [REQ-P09]

**Szene 4: Pack baut sich auf (30s)**
Bild: cad/pack/entwurf/pack_LFP_gesamt.png
Bild-in-Bild links: sim/kuehlung/k3_gesamt/k3_vergleich.png
Bild-in-Bild rechts: sim/mechanik/x3_crash_g5/energie_LFP_a.png
Tafeln:
1. Pack baut sich auf [REQ-P07]
2. Kühlung K3 K4 Vergleich [REQ-P12]
3. Crash Pfahl 5 kJ [REQ-P14]
4. Packmasse 619,85 kg [Packmasse LFP masse_bekannt_kg]

**Szene 5: Steuergeräte entstehen (60s)**

Teil 5a – CMU-Platine (15s)
Bild: sim/elektrik/e3_platine/platine_LFP_3d_top.png
Tafeln:
1. CMU Leiterplatte 4 Lagen [REQ-P15]
2. Explosion Lagen Leiterbahnen [sim/elektrik/e3_platine]
3. Nahaufnahme Ausgleichskanal [sim/elektrik/e3_platine]

Teil 5b – BMS-Platine (15s)
Bild: sim/elektrik/e3c_bms_platine/platine_bms_3d_top.png
Tafeln:
1. BMS Platine 134 Teile [BMS teile]
2. Schock Sperrzone Rot [REQ-P13]
3. Schaltplan Schütz [sim/elektrik/e3c_bms_platine/schaltplan_bms_blatt-1.png]

Teil 5c – Rechnungen (15s)
Bild: sim/elektrik/e3d_fmeda/e3d_fmeda.png
Tafeln:
1. SPICE Vorladung 912 V [SPICE Vorladung U_V]
2. Schütz Zener Anzug 37,11 V [SPICE Schuetz zener_anzug v_n_max_V]
3. FMEDA SG-01 ASIL D [FMEDA Ziel SG-01 ASIL]

Teil 5d – Nachverfolgungskette (15s)
Bild: sim/elektrik/e3d_fmeda/e3d_fmeda.png (Graph im Hintergrund)
Tafeln:
1. REQ-P18 Funktionale Sicherheit [REQ-P18]
2. ENT-192 vorgeschlagen [ENT-192]
3. BT-323 Ausgleichskreis [BT-323]
4. Nachweis FMEDA E3d [sim/elektrik/e3d_fmeda/ergebnis.json]

**Szene 6: Batterie fertig (25s)**
Bild: cad/pack/entwurf/pack_LFP_gesamt.png
Tafeln:
1. Batterie fertig 619,85 kg [Packmasse LFP masse_bekannt_kg]
2. Teile Gesamt 244 [CMU LFP teile BMS teile]
3. DRC 0 [CMU LFP drc_verstoesse BMS drc_verstoesse]
4. SPFM 99,00 % [FMEDA Ziel SG-01 SPFM]
5. Masse 619,85 kg [Packmasse LFP masse_bekannt_kg]
6. Thomas Schmiegelt KI-generiert [REQ-D13]
