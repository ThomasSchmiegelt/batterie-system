| Dok.-Nr. | BAT-PM-OPT | Version | 0.1 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Optimierungsliste (zurückgestellt, erst konservativ entwickeln) | Ersteller | Claude Opus (KI) | Prüfer | – (Autor offen) |

> KI-generiert (Claude Opus, 2026-11-24). Vorgabe Autor 2026-11-24: „entwickel als erst konservativ, optimierung machen wir später, schreibe dir aber auf, was man optimieren kann. Bewerte das gleich richtung kosten, sicherheit, effizienz“.
> **Bewertung** gegenüber dem konservativen Stand: **+** besser, **0** neutral, **−** schlechter, **?** unklar. Die Einschätzung stammt von Opus, ungerechnet, sofern keine Quelle steht. **Prio:** A lohnt sich bald, B später, C nur bei Bedarf.
> Neue Einträge schreibt jeder Agent, der beim konservativen Auslegen eine Optimierung erkennt (OPT-NNN fortlaufend).

| Nr | Optimierung | konservativer Stand | Kosten | Sicherheit | Effizienz | Prio | Herkunft |
|---|---|---|---|---|---|---|---|
| OPT-001 | Aktiver Zellausgleich, kapazitiv (KR1 K6) | passiv + Wärmeleitpad (ENT-184) | − mehr Schalter, Treiber, Steuerung | − mehr Fehlerarten, FSR-Nachweis aufwendiger | + kaum Verlustwärme, Energie wird verschoben (Reichweitengewinn vermutlich klein) | C | KR1 Lauf 3 |
| OPT-002 | Ausgleich nur in Ruhephasen mit Ziel-SOC-Logik (Software) | Ausgleich beim Laden und in Ruhe | 0 nur Software | 0 | + weniger Wärme während des Ladens | B | KR1 Kasten T3 |
| OPT-003 | Thermische Vias weglassen (E3b: konservativ 93,9 °C statt 52,6 °C, Reserve 11 K) | 8 Vias je Widerstandspaar (ENT-187) | + etwas billigere Platine | − weniger Wärmereserve | 0 | C | ERW-E3b |
| OPT-004 | Kupferflächen bzw. Metallkern statt Wärmeleitpad | Pad zur Wand (ENT-184) | ? Metallkern teurer, Kupferflächen billig | + kein Pad, das sich löst | 0 | B | ENT-184 Folgen |
| OPT-005 | Vorladung mit MOSFET und Strombegrenzung statt Widerstand + Schütz | Vorladeschütz + Widerstand ≥ 450 J (ERW-E3) | ? | ? Halbleiter fällt anders aus als ein Schütz (FSR-06) | 0 | B | ERW-E3 BT-712 |
| OPT-006 | Schützansteuerung mit Sparschaltung (Haltestrom) und schneller Löschung | einfache Ansteuerung | − etwas Elektronik | + schnelleres Abschalten | + weniger Spulenleistung im Dauerbetrieb | A | BT-715, umgesetzt (E3c N1: Haltestrom 0,435 A, 1,5 W statt 18 W, Abfall mit Zener 0,26/1,43 ms; ENT-198/199 vorgeschlagen) |
| OPT-007 | AFE mit integrierter ASIL-D-Diagnose statt separatem Sekundärschutz BT-325 | zwei unabhängige Messwege (F-S2, ASIL D) | + weniger Bauteile | ? Nachweis der Unabhängigkeit schwieriger | 0 | C | HARA FSR-01 |
| OPT-008 | Abstand innerhalb der CMU < 0,2 mm mit Schutzlack (PD1) | 0,2 mm, PD2 (ENT-168) | + kleinere Platine | − Reserve sinkt, Lack muss geprüft werden | 0 | C | ERW-E3 N4/N5 |
| OPT-009 | Leiterplatte mit CTI ≥ 600 oder Schlitzfräsung an der HV/NV-Grenze BT-311 | Abstand 10 mm verstärkt, Standard-FR4 | − teureres Material bzw. Fräsen | 0 | 0, kleinere BMS-Platine | B | ERW-E3 N4 |
| OPT-010 | Zwei CMU zu einer Platine zusammenlegen (weniger Stecker und Übertrager) | 1 CMU je 18 Zellen | + weniger Teile | ? größere Spannung auf einer Platine | 0 | C | E3 |
| OPT-011 | Ausgleichswiderstände aus der E24-Reihe statt E96 (NMC) | 2 × 64,9 Ω E96 (ENT-172) | + Standardteil | 0 | − Ausgleich 7 % langsamer (34 Ω) | C | ENT-172 |
| OPT-012 | Fernziel Cell-to-Pack (Zellen tragend, ohne Module): LFP 528 / NMC 370 kg (Zellanteil 88/83 %, Bestwert BYD Han 90 %, W51). Das Pflichtziel ist seit AEN-022 600/450 kg (L2) | Stand Schleife 1 | ? | ? Crash prüfen | + Reichweite | A | REQ-P07, Schleife 2 |
| OPT-013 | Zweiter Schalter in Reihe zum Ausgleichs-FET (E3d: SG-02 SPFM 95,71 % statt Ziel 97 %, mit Schalter 97,85 %) | ein Ausgleichs-FET je Zelle | − 18 FET je CMU mehr, Platz auf der Platine | + Kurzschluss des FET entlädt die Zelle nicht mehr dauernd (SPFM SG-02, ergebnis.json Block massnahmen) | 0 | **erledigt → umgesetzt als Pflicht (ERW-E3 N7, SG-02 ASIL C)** | E3d, ERW-E3d |
| OPT-014 | Platine BT-311 mit weniger Lagen oder kleinerer Fläche (E3c: 4 Lagen 160 x 100 mm, Bauhöhe 9,3 mm gegen Platz 200 x 150 mm) | 4 Lagen, ENT-188..190 | + Fertigung günstiger, mehr Platz im Pack | 0 Kriechstrecke 10 mm bleibt | 0 | C | ENT-188, ENT-189, ENT-190 |
| OPT-015 | Mehrheitsentscheid 2oo3 mit Notlauf ≥ 10 s statt 1oo2 (KR2 K3, Rang 2) | 1oo2, gestuft, Hardwarepfad (KR2 K1) | − dritter Messkanal | 0 bis − (2oo3 gegen 1oo2 im Nachweis) | + weniger Liegenbleiber durch Fehlmessung | B | KR2 |
